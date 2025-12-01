#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API 최종 체크 - 모든 엔드포인트 테스트
"""
import requests
import json
from urllib.parse import quote
import sys
import io

# Windows 콘솔 UTF-8 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

api_key = "1CD432FC-7D68-4F57-9B14-4D1BFED8B7E4"
base_url = "https://devin.aks.ac.kr:8080/v1"
headers = {'X-API-Key': api_key}

print("=== Korean Encyclopedia API Final Check ===\n")

tests = [
    {
        'name': '1. Articles List (page 1)',
        'url': f"{base_url}/Articles?pageNo=1"
    },
    {
        'name': '2. Articles by Field (Literature)',
        'url': f"{base_url}/Articles/Field/{quote('문학')}?pageNo=1"
    },
    {
        'name': '3. Search Person: Kim Woochang',
        'url': f"{base_url}/Articles/Search?keyword={quote('김우창')}&page=1"
    },
    {
        'name': '4. Search Person in Literature: Kim Hyeon',
        'url': f"{base_url}/Articles/Search?keyword={quote('김현')}&field={quote('문학')}&page=1"
    },
    {
        'name': '5. Field List',
        'url': f"{base_url}/Category/Field"
    },
    {
        'name': '6. Specific Article by EID',
        'url': f"{base_url}/Article/AKS_KH_0000000001"
    }
]

for test in tests:
    print(f"\n{'='*60}")
    print(test['name'])
    print(f"URL: {test['url']}")
    print('-'*60)

    try:
        response = requests.get(test['url'], headers=headers, timeout=15)
        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            try:
                data = response.json()

                # Response structure analysis
                if isinstance(data, dict):
                    print(f"Response Type: dict")
                    print(f"Keys: {list(data.keys())[:10]}")

                    # Check pagination and counts
                    for key in ['totalPage', 'pageNo', 'pageSize', 'articleCount', 'mediaCount']:
                        if key in data:
                            print(f"  {key}: {data[key]}")

                    # Check articles
                    if 'articles' in data:
                        articles = data['articles']
                        print(f"  articles: {len(articles)} items")
                        if articles:
                            print(f"\n  First article:")
                            first = articles[0]
                            for k, v in list(first.items())[:5]:
                                print(f"    {k}: {str(v)[:50]}")

                    # Check field list
                    if 'field' in data:
                        fields = data['field']
                        print(f"  field count: {len(fields)} items")
                        if fields:
                            field_names = [f.get('name') for f in fields[:5]]
                            print(f"  First 5 fields: {field_names}")

                elif isinstance(data, list):
                    print(f"Response Type: list (length: {len(data)})")
                    if data:
                        print(f"First item: {str(data[0])[:200]}")

                else:
                    print(f"Response Type: {type(data)}")
                    print(f"Content: {str(data)[:500]}")

            except json.JSONDecodeError as je:
                print(f"JSON Decode Error: {je}")
                print(f"Response Text: {response.text[:500]}")

        elif response.status_code == 404:
            print("404 Not Found")

        elif response.status_code == 400:
            print("400 Bad Request")
            print(f"Response: {response.text[:200]}")

        elif response.status_code == 500:
            print("500 Server Error")
            print(f"Response: {response.text[:200]}")

        else:
            print(f"Other Error")
            print(f"Response: {response.text[:200]}")

    except requests.Timeout:
        print("Timeout (15s exceeded)")

    except Exception as e:
        print(f"Exception: {e}")

print(f"\n{'='*60}")
print("Test Complete")
