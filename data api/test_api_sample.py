#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API 샘플 테스트 - 몇 명만 빠르게 테스트
"""
from enrich_entities_from_api import AKSAPIEnricher

# API 키
api_key = "1CD432FC-7D68-4F57-9B14-4D1BFED8B7E4"

enricher = AKSAPIEnricher(api_key)

print("=== 한국민족문화대백과 API 샘플 테스트 ===\n")

# 테스트할 인명 리스트 (문학 관련 인물)
test_names = [
    '김우창',
    '김윤식',
    '유종호',
    '김현',
    '김춘수',
    '조지훈',
    '김동리',
    '박경리',
    '이청준',
    '황석영'
]

print(f"총 {len(test_names)}명의 인물을 테스트합니다...\n")

results = {}
for i, name in enumerate(test_names, 1):
    print(f"[{i}/{len(test_names)}] {name} 검색 중...", end=' ')

    article = enricher.search_article(name, field='문학')

    if article and article.get('contentsType') == '인물':
        role = enricher.map_role(article)
        era = article.get('era', '')
        definition = article.get('definition', '')[:50]

        results[name] = {
            'role': role,
            'era': era,
            'definition': definition
        }
        print(f"[OK] role={role}, era={era}")
    else:
        print("[SKIP]")

print(f"\n검증 완료: {len(results)}명 확인됨")

# Python 코드 생성
if results:
    print("\n" + "="*60)
    print("# convert_to_xml.py에 추가할 코드:")
    print("self.persons.update({")
    for name, info in results.items():
        role = info.get('role', 'scholar')
        era = info.get('era', '')
        comment = f"  # {era} - {info.get('definition', '')}" if era else ""
        print(f"    '{name}': {{'role': '{role}'}},{comment}")
    print("})")
