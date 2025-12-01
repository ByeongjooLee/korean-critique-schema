#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XML 파일을 스키마에 대해 검증하는 스크립트
"""
from lxml import etree
import sys

def validate_xml(xml_file, schema_file):
    """XML 파일을 스키마에 대해 검증"""
    try:
        # 스키마 로드
        schema_doc = etree.parse(schema_file)
        schema = etree.XMLSchema(schema_doc)

        # XML 파일 로드
        doc = etree.parse(xml_file)

        # 검증
        is_valid = schema.validate(doc)

        if is_valid:
            print(f"[OK] 검증 성공: {xml_file}")

            # 통계 정보
            root = doc.getroot()
            ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

            divs = root.findall('.//tei:div', ns)
            paras = root.findall('.//tei:p', ns)
            sents = root.findall('.//tei:s', ns)
            persons = root.findall('.//tei:persName', ns)
            titles = root.findall('.//tei:title', ns)
            orgs = root.findall('.//tei:orgName', ns)
            terms = root.findall('.//tei:term', ns)

            print(f"\n통계:")
            print(f"  - div 섹션: {len(divs)}개")
            print(f"  - 문단: {len(paras)}개")
            print(f"  - 문장: {len(sents)}개")
            print(f"  - 태그된 엔티티: {len(persons) + len(titles) + len(orgs) + len(terms)}개")
            print(f"    * persName: {len(persons)}개")
            print(f"    * title: {len(titles)}개")
            print(f"    * orgName: {len(orgs)}개")
            print(f"    * term: {len(terms)}개")

            # 파일 크기
            import os
            size = os.path.getsize(xml_file)
            print(f"  - 파일 크기: {size:,} bytes ({size/1024:.1f} KB)")

            return True
        else:
            print(f"[FAIL] 검증 실패: {xml_file}\n")
            for i, error in enumerate(schema.error_log, 1):
                print(f"오류 {i}: 라인 {error.line} - {error.message}")
            return False

    except Exception as e:
        print(f"오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    schema_file = r'C:\Users\bj363\OneDrive\문서\대학원 공부\xml데이터 구축\claude\korean-critique-schema.xsd'
    xml_file = r'C:\Users\bj363\OneDrive\문서\대학원 공부\xml데이터 구축\claude\data\김우창_궁핍한시대의시인_451-467쪽.xml'

    if len(sys.argv) > 1:
        xml_file = sys.argv[1]

    validate_xml(xml_file, schema_file)
