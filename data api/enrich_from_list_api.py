#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
한국민족문화대백과 List API를 활용한 인명 데이터베이스 확장
검색 API는 500 오류가 발생하므로, List API로 전체 데이터를 수집
"""
import requests
import json
import time
from typing import Dict, List
import sys
import io

# Windows 콘솔 UTF-8 설정 및 버퍼링 비활성화
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)

class ListAPIEnricher:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://devin.aks.ac.kr:8080/v1"
        self.headers = {'X-API-Key': api_key}

        # 역할 매핑 (한국민족문화대백과 → XML 스키마)
        self.role_mapping = {
            '시인': 'poet',
            '소설가': 'novelist',
            '비평가': 'critic',
            '평론가': 'critic',
            '수필가': 'essayist',
            '극작가': 'playwright',
            '아동문학가': 'childrenauthor',
            '번역가': 'translator',
            '학자': 'scholar',
            '문학평론가': 'critic',
            '문학비평가': 'critic',
            '작가': 'novelist',
            '문인': 'novelist',
        }

    def get_all_articles(self, max_pages: int = None, field: str = None) -> List[Dict]:
        """전체 항목 또는 특정 분야 항목 리스트 수집"""
        all_articles = []

        # URL 결정
        if field:
            from urllib.parse import quote
            base_api_url = f"{self.base_url}/Articles/Field/{quote(field)}"
            print(f"{field} 분야 데이터 수집 중...")
        else:
            base_api_url = f"{self.base_url}/Articles"
            print("전체 데이터 수집 중...")

        # 첫 페이지로 전체 페이지 수 확인
        url = f"{base_api_url}?pageNo=1"
        response = requests.get(url, headers=self.headers, timeout=10)

        if response.status_code != 200:
            print(f"[ERROR] API 호출 실패: {response.status_code}")
            return []

        data = response.json()
        total_pages = data.get('totalPage', 0)

        if max_pages:
            total_pages = min(total_pages, max_pages)

        print(f"총 {total_pages}페이지 수집 예정 (약 {total_pages * 50}개 항목)")

        # 모든 페이지 순회
        for page in range(1, total_pages + 1):
            url = f"{base_api_url}?pageNo={page}"

            try:
                response = requests.get(url, headers=self.headers, timeout=10)

                if response.status_code == 200:
                    data = response.json()
                    articles = data.get('articles', [])
                    all_articles.extend(articles)

                    print(f"[{page}/{total_pages}] {len(articles)}개 항목 수집 완료", end='\r', flush=True)
                else:
                    print(f"\n[WARN] 페이지 {page} 호출 실패: {response.status_code}")

                # API 부하 방지
                time.sleep(0.1)

            except Exception as e:
                print(f"\n[ERROR] 페이지 {page} 처리 중 오류: {e}")
                continue

        print(f"\n\n총 {len(all_articles)}개 항목 수집 완료")
        return all_articles

    def extract_persons(self, articles: List[Dict]) -> Dict[str, Dict]:
        """항목에서 인물 정보만 추출"""
        persons = {}

        print("\n인물 데이터 추출 중...")
        person_count = 0

        for article in articles:
            contents_type = article.get('contentsType', '')

            # 인물 타입 확인 (API는 "인물/전통 인물" 또는 "인물/현대 인물" 등으로 반환)
            if not contents_type.startswith('인물'):
                continue

            person_count += 1
            headword = article.get('headword', '').strip()

            if not headword:
                continue

            # 역할 추출 및 매핑
            definition = article.get('definition', '')
            era = article.get('era', '')

            role = self.infer_role(definition, era)

            # 한국인인지 외국인인지 판단
            is_foreign = self.is_foreign_person(headword, definition)

            if is_foreign and 'foreigner' not in role:
                role = role + ' foreigner' if role else 'foreigner'

            persons[headword] = {
                'role': role.strip(),
                'era': era,
                'definition': definition[:100],
                'eid': article.get('eid', ''),
                'url': article.get('url', ''),
                'field': article.get('field', '')
            }

            if person_count % 10 == 0:  # 10명마다 출력
                print(f"[{person_count}] {headword} - {role}", flush=True)

        print(f"\n\n총 {len(persons)}명의 인물 정보 추출 완료")
        return persons

    def infer_role(self, definition: str, era: str) -> str:
        """정의와 시대 정보로부터 역할 추론"""
        roles = []

        for keyword, role in self.role_mapping.items():
            if keyword in definition:
                if role not in roles:
                    roles.append(role)

        # 역할을 찾지 못한 경우 기본값
        if not roles:
            if any(word in definition for word in ['문학', '작품', '저술', '저서']):
                roles.append('scholar')
            else:
                roles.append('other')

        return ' '.join(roles)

    def is_foreign_person(self, name: str, definition: str) -> bool:
        """외국인 인물 판단"""
        # 영어 알파벳이 포함된 경우
        if any(c.isalpha() and ord(c) < 128 for c in name):
            return True

        # 정의에 국가명이 포함된 경우
        foreign_countries = [
            '영국', '미국', '프랑스', '독일', '러시아', '일본', '중국',
            '이탈리아', '스페인', '오스트리아', '네덜란드', '벨기에',
            '스위스', '폴란드', '체코', '헝가리', '아일랜드', '스웨덴'
        ]

        for country in foreign_countries:
            if country in definition[:50]:  # 정의 앞부분에 국가명이 있으면
                return True

        return False

    def save_to_json(self, persons: Dict, output_file: str):
        """JSON 파일로 저장"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(persons, f, ensure_ascii=False, indent=2)
        print(f"\n[저장 완료] {output_file}")

    def generate_python_code(self, persons: Dict) -> str:
        """convert_to_xml.py에 추가할 Python 코드 생성"""
        lines = []
        lines.append("# API로부터 자동 수집된 인물 데이터")
        lines.append("self.persons.update({")

        for name, info in sorted(persons.items()):
            role = info.get('role', 'scholar')
            era = info.get('era', '')
            definition = info.get('definition', '')

            comment = f"  # {era} - {definition}" if era else f"  # {definition}"
            if len(comment) > 80:
                comment = comment[:77] + "..."

            lines.append(f"    '{name}': {{'role': '{role}'}},{comment}")

        lines.append("})")

        return '\n'.join(lines)

    def update_convert_to_xml(self, persons: Dict, convert_file: str = 'convert_to_xml.py'):
        """convert_to_xml.py 파일 업데이트"""
        print(f"\n{convert_file} 업데이트 중...")

        # 기존 파일 읽기
        with open(convert_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 새로운 인물 데이터 코드 생성
        new_code = self.generate_python_code(persons)

        # self.persons = { ... } 부분 찾기
        import re

        # persons 딕셔너리 끝 부분 찾기 (닫는 괄호 찾기)
        # self.persons = { 로 시작하고 }로 끝나는 부분
        pattern = r"(self\.persons = \{[^}]*\})"

        # 기존 persons 딕셔너리 뒤에 update 추가
        def add_update(match):
            original = match.group(1)
            return f"{original}\n        \n        {new_code}"

        # 이미 API 데이터가 추가되어 있는지 확인
        if "# API로부터 자동 수집된 인물 데이터" in content:
            print("[INFO] 이미 API 데이터가 추가되어 있습니다. 기존 데이터를 교체합니다.")
            # 기존 API 데이터 제거
            api_pattern = r"\n\s*# API로부터 자동 수집된 인물 데이터\n\s*self\.persons\.update\(\{[^}]*\}\)"
            content = re.sub(api_pattern, '', content, flags=re.DOTALL)

        # 새 데이터 추가
        content = re.sub(pattern, add_update, content, count=1)

        # 파일 저장
        with open(convert_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"[완료] {len(persons)}명의 인물이 {convert_file}에 추가되었습니다.")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='한국민족문화대백과 API로부터 인물 데이터 수집')
    parser.add_argument('--mode', choices=['all', 'literature', 'test'], default='test',
                        help='수집 모드: all(전체), literature(문학), test(10페이지)')
    parser.add_argument('--pages', type=int, default=None,
                        help='수집할 최대 페이지 수 (기본값: mode에 따라 다름)')
    args = parser.parse_args()

    api_key = "1CD432FC-7D68-4F57-9B14-4D1BFED8B7E4"
    enricher = ListAPIEnricher(api_key)

    print("=== 한국민족문화대백과 List API 인물 데이터 수집 ===\n")

    field = None
    max_pages = args.pages

    if args.mode == 'all':
        field = None
        if max_pages is None:
            max_pages = 1507  # 전체
        print(f"전체 항목에서 인물 수집 ({max_pages}페이지)...")
    elif args.mode == 'literature':
        field = '문학'
        if max_pages is None:
            max_pages = 97  # 문학 전체
        print(f"문학 분야 수집 ({max_pages}페이지)...")
    elif args.mode == 'test':
        field = None
        max_pages = 10
        print("테스트 모드: 10페이지만 수집...")

    # 1. 항목 수집
    articles = enricher.get_all_articles(max_pages=max_pages, field=field)

    if not articles:
        print("[ERROR] 데이터 수집 실패")
        sys.exit(1)

    # 2. 인물 정보 추출
    persons = enricher.extract_persons(articles)

    if not persons:
        print("[ERROR] 인물 정보 추출 실패")
        sys.exit(1)

    # 3. JSON 저장
    output_json = 'enriched_persons_from_list_api.json'
    enricher.save_to_json(persons, output_json)

    # 4. convert_to_xml.py 업데이트
    enricher.update_convert_to_xml(persons)

    print("\n" + "="*60)
    print("완료!")
    print(f"- 수집된 인물: {len(persons)}명")
    print(f"- JSON 파일: {output_json}")
    print(f"- convert_to_xml.py 업데이트 완료")
    print("="*60)
