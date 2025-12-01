#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XML 파일의 태그 오류 수정 스크립트
"""
import re

def fix_xml_tags(xml_file):
    """XML 파일의 태그 불일치 수정"""
    with open(xml_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 패턴 1: 「...」가 <title>...</title>로 변환되지 않은 경우
    # 「xxx</title> 형태를 <title level="a">xxx</title>로 수정
    content = re.sub(r'「([^」]+)</title>', r'<title level="a">\1</title>', content)

    # 패턴 2: 『...』가 <title>...</title>로 변환되지 않은 경우
    # 『xxx</title> 형태를 <title level="m">xxx</title>로 수정
    content = re.sub(r'『([^』]+)</title>', r'<title level="m">\1</title>', content)

    # 패턴 3: 《...》가 <title>...</title>로 변환되지 않은 경우
    # 《xxx</title> 형태를 <title level="j">xxx</title>로 수정
    content = re.sub(r'《([^》]+)</title>', r'<title level="j">\1</title>', content)

    # 패턴 4: <title level="x">가 </s>나 </p> 전에 닫히지 않은 경우
    # <title level="a">xxx로 시작하고 </title>이 없으면 다음 <나 </s> 전에 </title> 추가
    def close_unclosed_title_a(match):
        text_before_end = match.group(1)
        # 이미 </title>이 있으면 그대로 반환
        if '</title>' in text_before_end:
            return match.group(0)
        # </title>이 없으면 </s> 바로 앞에 추가
        return f'<title level="a">{text_before_end}</title></s>'

    content = re.sub(r'<title level="a">([^<]+)</s>', close_unclosed_title_a, content)

    # level="m"도 동일하게 처리
    def close_unclosed_title_m(match):
        text_before_end = match.group(1)
        if '</title>' in text_before_end:
            return match.group(0)
        return f'<title level="m">{text_before_end}</title></s>'

    content = re.sub(r'<title level="m">([^<]+)</s>', close_unclosed_title_m, content)

    # level="j"도 동일하게 처리
    def close_unclosed_title_j(match):
        text_before_end = match.group(1)
        if '</title>' in text_before_end:
            return match.group(0)
        return f'<title level="j">{text_before_end}</title></s>'

    content = re.sub(r'<title level="j">([^<]+)</s>', close_unclosed_title_j, content)

    # 패턴 5: <note> 태그 안의 잘못된 태그 수정
    # 「xxx</title> 형태를 <title level="a">xxx</title>로 수정
    def fix_title_in_note(match):
        before = match.group(1)
        middle = match.group(2)
        after = match.group(3)
        return f'{before}<title level="a">{middle}</title>{after}'

    content = re.sub(r'(<note[^>]*>[^「]*)「([^」]+)</title>([^<]*</note>)', fix_title_in_note, content)

    # 파일 저장
    with open(xml_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f'태그 수정 완료: {xml_file}')

if __name__ == '__main__':
    xml_file = r'C:\Users\bj363\OneDrive\문서\대학원 공부\xml데이터 구축\claude\data\김우창_궁핍한시대의시인_451-467쪽.xml'
    fix_xml_tags(xml_file)
