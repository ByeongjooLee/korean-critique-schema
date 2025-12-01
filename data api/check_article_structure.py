#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API 응답 구조 확인 - 항목 필드명 분석
"""
import requests
import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

api_key = "1CD432FC-7D68-4F57-9B14-4D1BFED8B7E4"
base_url = "https://devin.aks.ac.kr:8080/v1"
headers = {'X-API-Key': api_key}

print("=== 문학 분야 항목 구조 분석 ===\n")

url = f"{base_url}/Articles/Field/문학?pageNo=1"
response = requests.get(url, headers=headers, timeout=10)

if response.status_code == 200:
    data = response.json()
    articles = data.get('articles', [])

    if articles:
        print(f"총 {len(articles)}개 항목 확인\n")

        # 첫 5개 항목의 전체 구조 출력
        for i, article in enumerate(articles[:5], 1):
            print(f"\n{'='*60}")
            print(f"항목 {i}:")
            print(json.dumps(article, ensure_ascii=False, indent=2))

        # 모든 필드 수집
        all_keys = set()
        content_types = set()

        for article in articles:
            all_keys.update(article.keys())
            if 'contentsType' in article:
                content_types.add(article['contentsType'])

        print(f"\n{'='*60}")
        print(f"\n전체 필드 목록:")
        for key in sorted(all_keys):
            print(f"  - {key}")

        print(f"\n콘텐츠 타입 목록:")
        for ct in sorted(content_types):
            # 각 타입별 개수
            count = sum(1 for a in articles if a.get('contentsType') == ct)
            print(f"  - {ct}: {count}개")

else:
    print(f"API 호출 실패: {response.status_code}")
