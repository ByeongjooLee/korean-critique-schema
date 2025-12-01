#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API 테스트 스크립트 - 자동 실행
"""
from enrich_entities_from_api import AKSAPIEnricher

# API 키
api_key = "1CD432FC-7D68-4F57-9B14-4D1BFED8B7E4"

enricher = AKSAPIEnricher(api_key)

# 451-467쪽 텍스트에서 인명 추출 및 확장
print("=== 한국민족문화대백과 API 테스트 ===\n")
print("451-467쪽 텍스트에서 인명을 추출하고 API로 검증합니다...\n")

text_file = r'C:\Users\bj363\OneDrive\문서\대학원 공부\xml데이터 구축\claude\data\김우창_궁핍한시대의시인_451-467쪽.txt'
output_file = 'enriched_persons_451-467.json'

enriched = enricher.enrich_from_text(text_file, output_file)

print(f"\n검증 완료: {len(enriched)}명의 인물이 한국민족문화대백과에서 확인되었습니다.")

# Python 코드 생성
if enriched:
    print("\n" + "="*60)
    enricher.generate_python_code(output_file)
