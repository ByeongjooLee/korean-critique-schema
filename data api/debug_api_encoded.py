#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API 디버깅 - URL 인코딩 버전
"""
import requests
import json
from urllib.parse import quote

api_key = "1CD432FC-7D68-4F57-9B14-4D1BFED8B7E4"
base_url = "https://devin.aks.ac.kr:8080/v1"
headers = {'X-API-Key': api_key}

# 테스트: 김우창 검색 (URL 인코딩)
print("=== API 응답 디버깅 (URL 인코딩) ===\n")

keyword = "김우창"
keyword_encoded = quote(keyword)

print(f"1. '{keyword}' 검색 (문학 분야)")
print(f"인코딩된 키워드: {keyword_encoded}\n")

url = f"{base_url}/Articles/Search?keyword={keyword_encoded}&field={quote('문학')}&page=1"
print(f"URL: {url}\n")

try:
    response = requests.get(url, headers=headers, timeout=10)
    print(f"상태 코드: {response.status_code}\n")

    if response.status_code == 200:
        data = response.json()
        print(f"성공!")
        print(json.dumps(data, ensure_ascii=False, indent=2)[:2000])
    else:
        print(f"오류 응답: {response.text}")

except Exception as e:
    print(f"예외 발생: {e}")

# 분야 없이 검색
print("\n\n2. 분야 없이 검색")
url2 = f"{base_url}/Articles/Search?keyword={keyword_encoded}&page=1"
print(f"URL: {url2}\n")

try:
    response2 = requests.get(url2, headers=headers, timeout=10)
    print(f"상태 코드: {response2.status_code}\n")

    if response2.status_code == 200:
        data2 = response2.json()
        print(f"성공!")
        print(json.dumps(data2, ensure_ascii=False, indent=2)[:2000])
    else:
        print(f"오류 응답: {response2.text}")

except Exception as e:
    print(f"예외 발생: {e}")

# 분야 목록 가져오기
print("\n\n3. 분야 목록 조회")
url3 = f"{base_url}/Category/Field"
print(f"URL: {url3}\n")

try:
    response3 = requests.get(url3, headers=headers, timeout=10)
    print(f"상태 코드: {response3.status_code}\n")

    if response3.status_code == 200:
        data3 = response3.json()
        print(f"성공!")
        print(json.dumps(data3, ensure_ascii=False, indent=2))
    else:
        print(f"오류 응답: {response3.text}")

except Exception as e:
    print(f"예외 발생: {e}")
