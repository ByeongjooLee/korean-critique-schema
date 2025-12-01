#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
위키피디아 API를 활용하여 인물 정보에 참조 링크 추가
"""
import requests
import json
import time
from typing import Dict, Optional
import sys
import io

# Windows 콘솔 UTF-8 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)

class WikipediaEnricher:
    def __init__(self):
        self.wiki_api_url = "https://ko.wikipedia.org/api/rest_v1/page/summary/"
        self.search_api_url = "https://ko.wikipedia.org/w/api.php"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.cache = {}
        self.cache_file = 'wikipedia_cache.json'
        self.load_cache()

    def load_cache(self):
        """캐시 파일 로드"""
        try:
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                self.cache = json.load(f)
            print(f"캐시 로드 완료: {len(self.cache)}개 항목")
        except FileNotFoundError:
            print("캐시 파일 없음, 새로 생성합니다")
            self.cache = {}

    def save_cache(self):
        """캐시 파일 저장"""
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(self.cache, f, ensure_ascii=False, indent=2)
        print(f"캐시 저장 완료: {len(self.cache)}개 항목")

    def search_wikipedia(self, name: str) -> Optional[Dict]:
        """위키피디아에서 인물 검색"""
        # 캐시 확인
        if name in self.cache:
            return self.cache[name]

        try:
            # 검색 API 사용
            params = {
                'action': 'query',
                'format': 'json',
                'list': 'search',
                'srsearch': name,
                'srlimit': 1,
                'utf8': 1
            }

            response = requests.get(self.search_api_url, params=params, headers=self.headers, timeout=10)

            if response.status_code != 200:
                print(f"[DEBUG] {name} - Status: {response.status_code}")
                return None

            data = response.json()
            search_results = data.get('query', {}).get('search', [])

            if not search_results:
                self.cache[name] = None
                return None

            # 첫 번째 결과의 제목으로 상세 정보 가져오기
            page_title = search_results[0]['title']

            # Summary API로 상세 정보 가져오기
            summary_url = f"{self.wiki_api_url}{requests.utils.quote(page_title)}"
            summary_response = requests.get(summary_url, headers=self.headers, timeout=10)

            if summary_response.status_code != 200:
                self.cache[name] = None
                return None

            summary_data = summary_response.json()

            result = {
                'title': summary_data.get('title'),
                'url': summary_data.get('content_urls', {}).get('desktop', {}).get('page'),
                'extract': summary_data.get('extract'),
                'description': summary_data.get('description')
            }

            # 캐시에 저장
            self.cache[name] = result

            # API 부하 방지
            time.sleep(0.1)

            return result

        except Exception as e:
            print(f"[WARN] {name} 검색 중 오류: {e}")
            self.cache[name] = None
            return None

    def enrich_persons_json(self, input_json: str, output_json: str):
        """JSON 파일의 인물 정보에 위키피디아 링크 추가"""
        # JSON 로드
        with open(input_json, 'r', encoding='utf-8') as f:
            persons = json.load(f)

        print(f"\n총 {len(persons)}명의 인물에 대해 위키피디아 검색 시작...")

        enriched_count = 0
        for i, (name, info) in enumerate(persons.items(), 1):
            if i % 10 == 0:
                print(f"[{i}/{len(persons)}] 처리 중...", flush=True)

            # 이미 위키피디아 정보가 있으면 스킵
            if 'wikipedia' in info and info['wikipedia']:
                enriched_count += 1
                continue

            # 위키피디아 검색
            wiki_data = self.search_wikipedia(name)

            if wiki_data:
                info['wikipedia'] = wiki_data
                enriched_count += 1
                if i % 10 == 0:
                    print(f"  {name}: {wiki_data.get('url')}")

        # 결과 저장
        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump(persons, f, ensure_ascii=False, indent=2)

        # 캐시 저장
        self.save_cache()

        print(f"\n완료!")
        print(f"- 총 인물: {len(persons)}명")
        print(f"- 위키피디아 링크 추가: {enriched_count}명")
        print(f"- 출력 파일: {output_json}")

    def update_convert_to_xml(self, enriched_json: str, convert_file: str = 'convert_to_xml.py'):
        """convert_to_xml.py 업데이트하여 위키피디아 링크 포함"""
        # JSON 로드
        with open(enriched_json, 'r', encoding='utf-8') as f:
            persons = json.load(f)

        # convert_to_xml.py 읽기
        with open(convert_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 새로운 코드 생성 (위키피디아 정보 포함)
        new_code_lines = ["# API + Wikipedia로부터 자동 수집된 인물 데이터", "self.persons.update({"]

        for name, info in sorted(persons.items()):
            role = info.get('role', 'other')
            era = info.get('era', '')
            definition = info.get('definition', '')
            wiki = info.get('wikipedia')

            # 기본 정보 생성
            person_dict = f"'{name}': {{'role': '{role}'"

            # 위키피디아 URL 추가
            if wiki and wiki.get('url'):
                wiki_url = wiki['url']
                person_dict += f", 'wikipedia': '{wiki_url}'"

            person_dict += "}"

            # 주석 추가
            comment = ""
            if era:
                comment = f"  # {era}"
                if definition:
                    comment += f" - {definition[:50]}"
            elif definition:
                comment = f"  # {definition[:50]}"

            if wiki and wiki.get('description'):
                if comment:
                    comment += f" | Wiki: {wiki['description'][:30]}"
                else:
                    comment = f"  # Wiki: {wiki['description'][:50]}"

            new_code_lines.append(f"    {person_dict},{comment}")

        new_code_lines.append("})")

        new_code = '\n'.join(new_code_lines)

        # 기존 API 데이터 부분 교체
        import re

        # 기존 API 데이터가 있으면 제거
        if "# API로부터 자동 수집된 인물 데이터" in content:
            pattern = r"\n\s*# API로부터 자동 수집된 인물 데이터\n\s*self\.persons\.update\(\{[^}]*\}\)"
            content = re.sub(pattern, '', content, flags=re.DOTALL)

        if "# API + Wikipedia로부터 자동 수집된 인물 데이터" in content:
            pattern = r"\n\s*# API \+ Wikipedia로부터 자동 수집된 인물 데이터\n\s*self\.persons\.update\(\{[^}]*\}\)"
            content = re.sub(pattern, '', content, flags=re.DOTALL)

        # self.persons = { ... } 뒤에 추가
        persons_pattern = r"(self\.persons = \{[^}]*\})"

        def add_wiki_data(match):
            original = match.group(1)
            return f"{original}\n        \n        {new_code}"

        content = re.sub(persons_pattern, add_wiki_data, content, count=1)

        # 파일 저장
        with open(convert_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"\n[완료] {convert_file} 업데이트 완료")

    def add_refs_to_xml(self, xml_file: str, persons_json: str):
        """XML 파일에 위키피디아 참조 추가"""
        from lxml import etree

        # JSON 로드
        with open(persons_json, 'r', encoding='utf-8') as f:
            persons = json.load(f)

        # XML 파일 로드
        parser = etree.XMLParser(remove_blank_text=False)
        tree = etree.parse(xml_file, parser)
        root = tree.getroot()

        # 네임스페이스
        ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

        # persName 태그 찾아서 ref 추가
        pers_names = root.findall('.//tei:persName', ns)

        added_count = 0
        for pers_name in pers_names:
            name = pers_name.text

            if not name:
                continue

            # persons 데이터에서 검색
            person_info = persons.get(name)

            if not person_info:
                continue

            wiki_info = person_info.get('wikipedia')

            if not wiki_info or not wiki_info.get('url'):
                continue

            # 이미 ref 속성이 있으면 스킵
            if pers_name.get('ref'):
                continue

            # ref 속성 추가
            wiki_url = wiki_info['url']
            pers_name.set('ref', wiki_url)
            added_count += 1

        # XML 저장
        tree.write(xml_file, encoding='utf-8', xml_declaration=True, pretty_print=True)

        print(f"\n[완료] XML 파일 업데이트")
        print(f"- 총 persName 태그: {len(pers_names)}개")
        print(f"- 위키피디아 ref 추가: {added_count}개")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='위키피디아 정보 추가')
    parser.add_argument('--mode', choices=['json', 'xml', 'both'], default='both',
                        help='작업 모드: json(JSON만), xml(XML만), both(둘 다)')
    parser.add_argument('--input-json', default='enriched_persons_from_list_api.json',
                        help='입력 JSON 파일')
    parser.add_argument('--output-json', default='enriched_persons_with_wikipedia.json',
                        help='출력 JSON 파일')
    parser.add_argument('--xml-file', default=None,
                        help='XML 파일 경로')
    args = parser.parse_args()

    enricher = WikipediaEnricher()

    if args.mode in ['json', 'both']:
        print("=== 위키피디아 정보 수집 ===\n")
        enricher.enrich_persons_json(args.input_json, args.output_json)
        enricher.update_convert_to_xml(args.output_json)

    if args.mode in ['xml', 'both'] and args.xml_file:
        print("\n=== XML 파일 업데이트 ===\n")
        enricher.add_refs_to_xml(args.xml_file, args.output_json)

    print("\n완료!")
