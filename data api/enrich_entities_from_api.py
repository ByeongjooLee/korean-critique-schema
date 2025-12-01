#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
한국민족문화대백과 API를 활용한 엔티티 데이터베이스 자동 확장 스크립트
"""
import requests
import json
import re
import time
from typing import Dict, List, Optional

class AKSAPIEnricher:
    def __init__(self, api_key: str):
        """
        Args:
            api_key: 한국민족문화대백과 API 인증키
        """
        self.api_key = api_key
        self.base_url = "https://devin.aks.ac.kr:8080/v1"
        self.headers = {'X-API-Key': api_key}
        self.cache = {}  # 중복 API 호출 방지

        # 스키마 role 매핑
        self.role_mapping = {
            # 문학 관련
            '시인': 'poet',
            '소설가': 'novelist',
            '작가': 'novelist',
            '극작가': 'playwright',
            '수필가': 'essayist',
            '아동문학가': 'childrenauthor',
            '번역가': 'translator',

            # 학술 관련
            '비평가': 'critic',
            '문학평론가': 'critic',
            '학자': 'scholar',
            '연구자': 'scholar',
            '교수': 'scholar',
            '철학자': 'scholar',
            '역사학자': 'scholar',
            '사회학자': 'scholar',

            # 기타
            '외국인': 'foreigner',
        }

    def search_article(self, keyword: str, field: str = None) -> Optional[Dict]:
        """API로 항목 검색"""
        # 캐시 확인
        cache_key = f"{keyword}_{field}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        try:
            # API 호출
            if field:
                url = f"{self.base_url}/Articles/Search?keyword={keyword}&field={field}&page=1"
            else:
                url = f"{self.base_url}/Articles/Search?keyword={keyword}&page=1"

            response = requests.get(url, headers=self.headers, timeout=10)

            if response.status_code == 200:
                data = response.json()

                # 결과가 있으면 첫 번째 항목 반환
                if data.get('ArticleCount', 0) > 0:
                    # 첫 번째 항목의 상세 정보 가져오기
                    first_item = data.get('items', [{}])[0]
                    eid = first_item.get('eid')

                    if eid:
                        article = self.get_article_detail(eid)
                        self.cache[cache_key] = article
                        return article

            # 요청 제한 방지 (1초 대기)
            time.sleep(1)

        except Exception as e:
            print(f"[오류] {keyword} 검색 중 오류 발생: {e}")

        self.cache[cache_key] = None
        return None

    def get_article_detail(self, eid: str) -> Optional[Dict]:
        """항목 상세 정보 가져오기"""
        try:
            url = f"{self.base_url}/Article/{eid}"
            response = requests.get(url, headers=self.headers, timeout=10)

            if response.status_code == 200:
                return response.json()

            time.sleep(1)

        except Exception as e:
            print(f"[오류] 항목 {eid} 조회 중 오류 발생: {e}")

        return None

    def map_role(self, article_data: Dict) -> str:
        """API 데이터에서 role 추출 및 매핑"""
        # contentsType (유형) 확인
        contents_type = article_data.get('contentsType', '')
        if contents_type == '인물':
            # attributes에서 직업 정보 찾기
            attributes = article_data.get('attributes', [])

            roles = []
            for attr in attributes:
                attr_name = attr.get('attrName', '')
                attr_value = attr.get('attrValue', '')

                if attr_name in ['직업', '활동분야', '분야']:
                    # 직업에서 role 매핑
                    for key, value in self.role_mapping.items():
                        if key in attr_value:
                            roles.append(value)

            # 중복 제거 및 반환
            if roles:
                return ' '.join(sorted(set(roles)))

            # field(분야)로도 추측
            field = article_data.get('field', '')
            if '문학' in field:
                return 'scholar'

        return 'other'

    def extract_person_candidates(self, text: str) -> List[str]:
        """텍스트에서 인명 후보 추출"""
        # 한글 이름 패턴 (2-4글자)
        korean_names = re.findall(r'[가-힣]{2,4}', text)

        # 빈도 기반 필터링 (2회 이상 등장한 이름만)
        from collections import Counter
        name_counts = Counter(korean_names)
        candidates = [name for name, count in name_counts.items() if count >= 2 and len(name) >= 2]

        return list(set(candidates))

    def enrich_from_text(self, text_file: str, output_file: str = 'enriched_persons.json'):
        """텍스트 파일에서 인명을 추출하고 API로 확장"""
        print(f"[시작] {text_file}에서 인명 추출 중...")

        # 텍스트 읽기
        with open(text_file, 'r', encoding='utf-8') as f:
            text = f.read()

        # 인명 후보 추출
        candidates = self.extract_person_candidates(text)
        print(f"[정보] {len(candidates)}개의 인명 후보 추출됨")

        # API로 검증 및 정보 수집
        enriched_persons = {}

        for i, name in enumerate(candidates, 1):
            print(f"[{i}/{len(candidates)}] {name} 검색 중...", end=' ')

            # '문학' 분야에서 먼저 검색
            article = self.search_article(name, field='문학')

            # 문학 분야에 없으면 전체 검색
            if not article:
                article = self.search_article(name)

            if article:
                contents_type = article.get('contentsType', '')

                if contents_type == '인물':
                    role = self.map_role(article)
                    era = article.get('era', '')
                    definition = article.get('definition', '')

                    enriched_persons[name] = {
                        'role': role,
                        'era': era,
                        'definition': definition[:100] if definition else '',
                        'eid': article.get('eid', ''),
                        'url': article.get('url', '')
                    }
                    print(f"[OK] role: {role}")
                else:
                    print(f"[SKIP] type: {contents_type}")
            else:
                print("[SKIP] not found")

        # 결과 저장
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(enriched_persons, f, ensure_ascii=False, indent=2)

        print(f"\n[완료] {len(enriched_persons)}명의 인물 정보가 {output_file}에 저장되었습니다.")
        return enriched_persons

    def search_organizations(self, keywords: List[str], output_file: str = 'enriched_orgs.json'):
        """기관명 검색 및 확장"""
        print(f"[시작] {len(keywords)}개의 기관명 검색 중...")

        enriched_orgs = {}

        for i, keyword in enumerate(keywords, 1):
            print(f"[{i}/{len(keywords)}] {keyword} 검색 중...", end=' ')

            article = self.search_article(keyword)

            if article:
                contents_type = article.get('contentsType', '')

                if contents_type == '단체':
                    enriched_orgs[keyword] = {
                        'type': '단체',
                        'definition': article.get('definition', '')[:100],
                        'eid': article.get('eid', ''),
                        'url': article.get('url', '')
                    }
                    print(f"[OK]")
                else:
                    print(f"[SKIP] type: {contents_type}")
            else:
                print("[SKIP]")

        # 결과 저장
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(enriched_orgs, f, ensure_ascii=False, indent=2)

        print(f"\n[완료] {len(enriched_orgs)}개의 기관 정보가 {output_file}에 저장되었습니다.")
        return enriched_orgs

    def generate_python_code(self, persons_file: str = 'enriched_persons.json'):
        """JSON 파일에서 Python 딕셔너리 코드 생성"""
        with open(persons_file, 'r', encoding='utf-8') as f:
            persons = json.load(f)

        print("\n# 확장된 인명 데이터베이스 (convert_to_xml.py에 추가)")
        print("self.persons.update({")

        for name, info in persons.items():
            role = info.get('role', 'other')
            era = info.get('era', '')
            comment = f"# {era}" if era else ""

            print(f"    '{name}': {{'role': '{role}'}},  {comment}")

        print("})")


def main():
    # API 키 입력
    api_key = input("한국민족문화대백과 API 키를 입력하세요: ").strip()

    if not api_key:
        print("[오류] API 키가 필요합니다.")
        return

    enricher = AKSAPIEnricher(api_key)

    print("\n=== 한국민족문화대백과 API 엔티티 확장 도구 ===\n")
    print("1. 텍스트 파일에서 인명 자동 추출 및 확장")
    print("2. 특정 인명 리스트 검색")
    print("3. 기관명 검색")
    print("4. JSON을 Python 코드로 변환")

    choice = input("\n선택 (1-4): ").strip()

    if choice == '1':
        text_file = input("텍스트 파일 경로: ").strip()
        enricher.enrich_from_text(text_file)

    elif choice == '2':
        names_input = input("인명을 쉼표로 구분하여 입력: ").strip()
        names = [n.strip() for n in names_input.split(',')]

        results = {}
        for name in names:
            article = enricher.search_article(name, field='문학')
            if article and article.get('contentsType') == '인물':
                role = enricher.map_role(article)
                results[name] = {'role': role}
                print(f"{name}: {role}")

        output = input("\n결과를 저장할 파일명 (엔터: 저장 안 함): ").strip()
        if output:
            with open(output, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"저장 완료: {output}")

    elif choice == '3':
        orgs_input = input("기관명을 쉼표로 구분하여 입력: ").strip()
        orgs = [o.strip() for o in orgs_input.split(',')]
        enricher.search_organizations(orgs)

    elif choice == '4':
        json_file = input("JSON 파일 경로: ").strip()
        enricher.generate_python_code(json_file)


if __name__ == '__main__':
    main()
