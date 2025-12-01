#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API 리스트 방식 테스트
"""
import requests
import json

api_key = "1CD432FC-7D68-4F57-9B14-4D1BFED8B7E4"
base_url = "https://devin.aks.ac.kr:8080/v1"
headers = {'X-API-Key': api_key}

print("=== 한국민족문화대백과 API - 리스트 방식 테스트 ===\n")

# 문학 분야 항목 리스트
print("1. 문학 분야 항목 리스트 (첫 페이지)")
url = f"{base_url}/Articles/Field/문학?pageNo=1"

try:
    from urllib.parse import quote
    url_encoded = f"{base_url}/Articles/Field/{quote('문학')}?pageNo=1"
    print(f"URL: {url_encoded}\n")

    response = requests.get(url_encoded, headers=headers, timeout=10)
    print(f"상태 코드: {response.status_code}\n")

    if response.status_code == 200:
        data = response.json()
        print(f"TotalPage: {data.get('TotalPage')}")
        print(f"pageNo: {data.get('pageNo')}")
        print(f"pageSize: {data.get('pageSize')}")
        print(f"ArticleCount: {data.get('ArticleCount')}\n")

        if data.get('items'):
            print(f"첫 5개 항목:")
            for i, item in enumerate(data['items'][:5], 1):
                print(f"{i}. {item.get('headword')} ({item.get('contentsType')})")
                print(f"   - definition: {item.get('definition', '')[:50]}")
                print(f"   - eid: {item.get('eid')}")
                print()
        else:
            print("항목이 없습니다.")
    else:
        print(f"오류: {response.text}")

except Exception as e:
    print(f"예외 발생: {e}")
    import traceback
    traceback.print_exc()
