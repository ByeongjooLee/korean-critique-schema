#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API 디버깅 - 응답 내용 확인
"""
import requests
import json

api_key = "1CD432FC-7D68-4F57-9B14-4D1BFED8B7E4"
base_url = "https://devin.aks.ac.kr:8080/v1"
headers = {'X-API-Key': api_key}

# 테스트: 김우창 검색
print("=== API 응답 디버깅 ===\n")
print("1. 김우창 검색 (문학 분야)")

url = f"{base_url}/Articles/Search?keyword=김우창&field=문학&page=1"
print(f"URL: {url}\n")

try:
    response = requests.get(url, headers=headers, timeout=10)
    print(f"상태 코드: {response.status_code}")
    print(f"응답 헤더: {dict(response.headers)}\n")

    if response.status_code == 200:
        data = response.json()
        print(f"응답 데이터:")
        print(json.dumps(data, ensure_ascii=False, indent=2)[:1000])
    else:
        print(f"오류 응답: {response.text[:500]}")

except Exception as e:
    print(f"예외 발생: {e}")
    import traceback
    traceback.print_exc()

print("\n\n2. 전체 항목 리스트 (첫 페이지)")
url2 = f"{base_url}/Articles?pageNo=1"
print(f"URL: {url2}\n")

try:
    response2 = requests.get(url2, headers=headers, timeout=10)
    print(f"상태 코드: {response2.status_code}")

    if response2.status_code == 200:
        data2 = response2.json()
        print(f"TotalPage: {data2.get('TotalPage')}")
        print(f"ArticleCount: {data2.get('ArticleCount')}")
        if data2.get('items'):
            print(f"\n첫 번째 항목:")
            print(json.dumps(data2['items'][0], ensure_ascii=False, indent=2)[:500])
    else:
        print(f"오류 응답: {response2.text[:500]}")

except Exception as e:
    print(f"예외 발생: {e}")
