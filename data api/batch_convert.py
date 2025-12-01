#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
일괄 변환 스크립트 - 여러 페이지 범위를 자동으로 변환
"""
import sys
import subprocess
from docx import Document

def extract_pages(doc_path, start_page, end_page, output_path):
    """워드 문서에서 특정 페이지 범위 추출"""
    doc = Document(doc_path)
    all_paras = [p.text for p in doc.paragraphs]
    full_text = '\n'.join(all_paras)
    total_chars = len(full_text)

    # 페이지당 문자 수 계산 (전체 467쪽 기준)
    start_idx = int(total_chars * start_page / 467)
    end_idx = int(total_chars * end_page / 467)

    pages_text = full_text[start_idx:end_idx]

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(pages_text)

    print(f'{start_page}-{end_page}쪽 추출 완료: {len(pages_text)} 문자')
    return len(pages_text)

def update_script_paths(start_page, end_page):
    """스크립트 파일들의 경로를 업데이트"""
    base_path = r'C:\Users\bj363\OneDrive\문서\대학원 공부\xml데이터 구축\claude\data\김우창_궁핍한시대의시인'

    # convert_to_xml.py 업데이트
    with open('convert_to_xml.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # input_file과 output_file 경로 교체
    import re
    new_input = f"input_file = r'{base_path}_{start_page}-{end_page}쪽.txt'"
    new_output = f"output_file = r'{base_path}_{start_page}-{end_page}쪽.xml'"

    content = re.sub(
        r"input_file = r'[^']*'",
        new_input.replace('\\', '\\\\'),
        content
    )
    content = re.sub(
        r"output_file = r'[^']*'",
        new_output.replace('\\', '\\\\'),
        content
    )

    with open('convert_to_xml.py', 'w', encoding='utf-8') as f:
        f.write(content)

    # fix_xml_tags.py 업데이트
    with open('fix_xml_tags.py', 'r', encoding='utf-8') as f:
        content = f.read()

    new_xml = f"xml_file = r'{base_path}_{start_page}-{end_page}쪽.xml'"
    content = re.sub(
        r"xml_file = r'[^']*'",
        new_xml.replace('\\', '\\\\'),
        content
    )

    with open('fix_xml_tags.py', 'w', encoding='utf-8') as f:
        f.write(content)

    # validate_xml.py 업데이트
    with open('validate_xml.py', 'r', encoding='utf-8') as f:
        content = f.read()

    content = re.sub(
        r"xml_file = r'C:[^']*\.xml'",
        new_xml.replace('\\', '\\\\'),
        content
    )

    with open('validate_xml.py', 'w', encoding='utf-8') as f:
        f.write(content)

def convert_range(doc_path, start_page, end_page):
    """특정 페이지 범위 변환"""
    print(f'\n=== {start_page}-{end_page}쪽 변환 시작 ===')

    base_path = r'C:\Users\bj363\OneDrive\문서\대학원 공부\xml데이터 구축\claude\data\김우창_궁핍한시대의시인'
    txt_path = f'{base_path}_{start_page}-{end_page}쪽.txt'

    # 1. 페이지 추출
    extract_pages(doc_path, start_page, end_page, txt_path)

    # 2. 스크립트 경로 업데이트
    update_script_paths(start_page, end_page)

    # 3. 변환 실행
    print('변환 중...')
    subprocess.run(['python', 'convert_to_xml.py'], check=True)

    # 4. 태그 수정
    print('태그 수정 중...')
    subprocess.run(['python', 'fix_xml_tags.py'], check=True)

    # 5. 검증
    print('검증 중...')
    result = subprocess.run(['python', 'validate_xml.py'], capture_output=True, text=True)

    if '[OK]' in result.stdout:
        print(f'[OK] {start_page}-{end_page}쪽 변환 완료!')
        return True
    else:
        print(f'[FAIL] {start_page}-{end_page}쪽 검증 실패')
        print(result.stdout)
        return False

if __name__ == '__main__':
    doc_path = r'C:\Users\bj363\OneDrive\문서\대학원 공부\xml데이터 구축\claude\김우창 궁핍한시대의 시인 1권.docx'

    # 변환할 페이지 범위 목록
    ranges = [
        (201, 250),
        (251, 300),
        (301, 350),
        (351, 400),
        (401, 450),
        (451, 467),  # 마지막 페이지
    ]

    success_count = 0
    fail_count = 0

    for start, end in ranges:
        try:
            if convert_range(doc_path, start, end):
                success_count += 1
            else:
                fail_count += 1
        except Exception as e:
            print(f'[ERROR] {start}-{end}쪽 변환 중 오류: {e}')
            fail_count += 1

    print(f'\n=== 변환 완료 ===')
    print(f'성공: {success_count}개')
    print(f'실패: {fail_count}개')
