#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
김우창 '궁핍한 시대의 시인' 텍스트를 TEI XML로 변환하는 스크립트
"""

import re
from datetime import datetime

class TextToXMLConverter:
    def __init__(self):
        # 인명 데이터베이스 - 대폭 확장
        self.persons = {
            # 한국 비평가/학자
            '김우창': {'id': 'kim-woochang', 'role': 'critic scholar'}
        
        # API + Wikipedia로부터 자동 수집된 인물 데이터
self.persons.update({
    '가군': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%80%EA%B5%B0'},  # 고대/삼국 - 삼국시대 때, 고구려 장안성 축성의 책임을 맡았던 관리. | Wiki: 환의 선형 작용이 주어진 아벨 군
    '가귀': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B7%80%EB%A9%B8%EC%9D%98_%EC%B9%BC%EB%82%A0'},  # 고대/삼국 - 삼국시대 때, 신라에서 『화엄경의강』, 『심원장』 등을 저술한 승려. | Wiki: 일본의 만화
    '가라포고이': {'role': 'other foreigner', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%80%EB%9D%BC%ED%8F%AC%EA%B3%A0%EC%9D%B4'},  # 고대/삼국 - 삼국시대 때, 일본에 귀화한 신라의 유민.
    '가루': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%80%EB%A3%A8'},  # 고대/삼국 - 삼국시대 때, 대상(大相) 등을 역임하다 고구려 멸망 후 부흥운동에 참여한 고구려의 귀족.
    '가마': {'role': 'other foreigner', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%80%EB%A7%88'},  # 고대/삼국 - 삼국시대 때, 백제에서 일본으로 파견된 사신. | Wiki: 사람의 힘을 이용하는 운송 수단
    '가서일': {'role': 'other foreigner', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%80%EC%84%9C%EC%9D%BC'},  # 고대/삼국 - 삼국시대 때, 일본에서 활약한 고구려 출신의 화가.
    '가실': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%80%EC%8B%A4'},  # 고대/남북국 - 삼국시대 때, 신라의 사량부 출신으로 변방에서 복무한 군인. | Wiki: 신라의 군인
    '가실왕': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%80%EC%8B%A4%EC%99%95'},  # 고대/삼국/가야 - 가야의 제7대(재위: 421년~451년) 왕.
    '각가': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%81%EA%B0%80'},  # 고대/삼국 - 삼국시대 때, 백제의 좌평 등을 역임한 귀족. | Wiki: 백제의 귀족이자, 관료이다
    '각굉': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B5%89'},  # 고려 - 고려 후기에, 『나옹화상어록』, 『나옹화상행장』 등을 저술한 승려. | Wiki: 위키미디어 동음이의어 문서
    '각덕': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%81%EB%8D%95'},  # 고대/삼국/신라 - 삼국시대 때, 양나라에 유학한 신라의 승려.
    '각민': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%BA%90%EB%82%98%EB%8B%A4'},  # 조선 - 조선 후기에, 청허계 정관문파로 『해의』 등을 저술한 승려. | Wiki: 북아메리카의 국가
    '각복모': {'role': 'other foreigner', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%81%EB%B3%B5%EB%AA%A8'},  # 고대/삼국 - 삼국시대 때, 백제의 멸망 후 일본으로 망명한 귀족. | Wiki: 백제의 귀족 (?–?)
    '각성': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%81%EC%84%B1'},  # 조선 - 조선시대 때, 판선교도총섭, 팔도도총섭, 규정도총섭 등을 역임한 승려. | Wiki: 자극에 반응을 보이는 생리적, 심리적 상태
    '각안': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EB%AC%B8%EA%B4%91_(%EC%8A%B9%EB%A0%A4)'},  # 조선/조선 후기 - 조선 후기에, 『동사열전』, 『범해선사유고』 등을 저술한 승려.
    '각우': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%95%BC%EC%9A%B4'},  # 고려 - 고려 후기에, 『자경문』을 저술한 승려. | Wiki: 고려 말의 고승
    '각운': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%95%95%EC%9A%B4'},  # 고려 - 고려 후기에, 『경덕전등록』을 중간한 승려.
    '각웅': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%9E%A5%EC%98%81%EC%8B%A4'},  # 고려/고려 후기 - 고려 후기에, 나옹 혜근의 제자로 서기의 직무를 담당한 승려. | Wiki: 조선의 과학자 (?–?)
    '각유': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%9C%A0_(%EC%84%B1%EC%94%A8)'},  # 고려 - 고려 후기에, 경주 기림사 주지, 대선사 등을 역임한 승려. | Wiki: 한국의 성씨
    '각절왕': {'role': 'other foreigner', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EB%AC%B4%EA%B5%90%EC%A0%88'},  # 고대/삼국 - 삼국시대 때, 일본의 『신찬성씨록』에 전하는 신라의 왕.
    '각종': {'role': 'other foreigner', 'wikipedia': 'https://ko.wikipedia.org/wiki/%ED%95%9C%ED%95%9C%EB%A0%B9'},  # 고대/삼국 - 삼국시대 때, 백제의 사비성 함락 사실을 일본 야마토 조정에 보고한 승려. | Wiki: 중국인들이 한국과 관련된 한류 컨텐츠를 제한하는 것 외
    '각훈': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%ED%95%B4%EB%8F%99%EA%B3%A0%EC%8A%B9%EC%A0%84'},  # 고려 - 고려 후기에, 『해동고승전』을 저술한 승려. | Wiki: 삼국 시대에 활약했던 승려들의 열전을 모아 놓은 책
    '간왕': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%84%EC%99%95_(%EB%B0%9C%ED%95%B4)'},  # 고대/남북국/발해 - 발해의 제9대(재위: 817년~818년) 왕. | Wiki: 발해의 제9대 국왕 (?~818)
    '간위거': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EB%A7%88%EC%97%AC%EC%99%95'},  # 고대/초기국가 - 부여의 제10대(재위: 2세기~3세기) 왕.
    '간진': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EB%AA%A8%EB%A6%AC%EC%85%94%EC%8A%A4'},  # 고대/남북국/통일신라 - 신라 진평왕대 곡물 수송을 담당한 왕경 출신의 관리. | Wiki: 아프리카의 섬 나라
    '갈로맹광': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%88%EB%A7%8C%EB%A1%9C'},  # 고대/삼국 - 삼국시대 때, 고구려 원정군의 사령관으로 활약한 장수. | Wiki: 고구려의 장수 (?–?)
    '갈홍기': {'role': 'other foreigner', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%88%ED%99%8D%EA%B8%B0'},  # 근대/일제강점기 - 일제강점기 때, 일본기독교 조선감리교단 연성국장, 일본기독교 조선교단의 종교교육국장 등으로 | Wiki: 일제강점기, 대한민국의 목회자 (1906–1989)
    '감경인': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%ED%98%95%EC%9D%98_%EA%B0%90%EA%B2%BD'},  # 조선 - 조선시대 때, 여도만호, 내금위, 정략장군 등을 역임한 무신.
    '강감찬': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EA%B0%90%EC%B0%AC'},  # 고려 전기에, 서북면행영도통사, 상원수대장군, 문하시중 등을 역임한 문신. | Wiki: 고려의 문인 (948-1031)
    '강거효': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%98%88%EC%A2%85%EC%8B%A4%EB%A1%9D'},  # 조선/조선 전기 - 조선 전기에, 예문관검열, 가예조좌랑, 통훈대부 등을 역임한 문신. | Wiki: 조선 예종 시대의 역사를 기록한 실록
    '강견': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%8B%A0%EC%96%B8%ED%98%B8'},  # 조선/조선 전기 - 조선 전기에, 서인들의 사주를 받아 기축옥사 때 최영경이 정여립과 연루되어 있다고 무고한 
    '강겸': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EB%B3%B4%EA%B2%B8'},  # 조선 - 조선 전기에, 예조좌랑, 병조정랑, 장령 등을 역임한 문신. | Wiki: 한국의 유튜버 및 아프리카TV BJ
    '강경대': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EA%B2%BD%EB%8C%80'},  # 현대/대한민국 - 대한민국의 학생운동가, 시민운동가. | Wiki: 대한민국의 학생운동가
    '강경서': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EA%B2%BD%EC%9D%8D'},  # 조선 - 조선 전기에, 사헌부집의, 대사간 등을 역임한 문신. | Wiki: 충청남도 논산시의 하위행정구역
    '강경선': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EA%B2%BD%EC%84%A0'},  # 근대/일제강점기 - 일제강점기 때, 대한적십자회 상의원, 대한민국임시정부 교민단 총무, 한국유일독립당 집행위원 | Wiki: 논산시의 채운역과 연무대역을 잇는 한국철도공사의 철도 
    '강경애': {'role': 'novelist', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EA%B2%BD%EC%95%A0'},  # 근대 - 일제강점기 때, 「소금」, 「인간 문제」, 「해고」 등을 저술한 소설가. | Wiki: 한국의 문학가, 인권 운동가 (1906–1944)
    '강계식': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EA%B3%84%EC%8B%9D'},  # 현대/대한민국 - 해방 이후 「붉은 장갑」, 「원술랑」, 「한강은 흐른다」 등에 출연한 배우. | Wiki: 대한민국의 배우 (1917–2000)
    '강고': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EB%95%85%EA%B0%95%EC%95%84%EC%A7%80'},  # 고대/남북국 - 남북국시대 때, 통일신라의 분황사 약사여래상을 주조한 장인. | Wiki: 땅강아지과 땅강아지속의 곤충
    '강곤': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%95%84%EC%9D%B4%ED%85%9C_(%EB%93%9C%EB%9D%BC%EB%A7%88)'},  # 조선/조선 전기 - 조선 전기에, 인수부윤, 충청도도절제사, 영안남도절도사 등을 역임한 무신.
    '강공훤': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%ED%83%9C%EC%A1%B0_(%EA%B3%A0%EB%A0%A4)'},  # 고대/삼국 - 남북국시대 때, 시중, 대장군, 대상 등을 역임한 무신. | Wiki: 고려의 초대 임금 (877–943)
    '강구려': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EA%B5%AC%ED%95%AD'},  # 고대/삼국 - 삼국시대 때, 왜에 억류된 신라 왕족 미사흔의 환국을 호송했던 박제상을 보좌한 신라의 관리
    '강구손': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EA%B7%80%EC%86%90'},  # 조선/조선 전기 - 조선 전기에, 도승지, 경기도관찰사, 우의정 등을 역임한 문신. | Wiki: 조선 초기의 문신
    '강국승': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%9D%B4%EC%8A%B9%EB%A7%8C'},  # 고려/고려 후기 - 고려 후기, 무오정변을 통해 최씨 무신정권을 붕괴시켜 위사보좌공신에 책록된 공신이자 무신. | Wiki: 대한민국의 제1·2·3대 대통령, 독립운동가, 교육가 
    '강국진': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EA%B5%AD%EC%A7%84'},  # 현대/대한민국 - 「비닐우산과 촛불이 있는 해프닝」, 「한강변의 타살」, 「역사의 빛」 등의 작품을 그린 화 | Wiki: 위키미디어 동음이의어 문서
    '강궁진': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EA%B6%81%EC%A7%84'},  # 고려/고려 전기 - 고려 전기, 강감찬의 아버지이자 금주 일대의 토착세력으로, 고려 태조 왕건을 섬겼던 호족  | Wiki: 후삼국 시대의 호족
    '강귀례': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%A7%84%EC%A3%BC%EA%B2%80%EB%AC%B4'},  # 현대 - 「진주 검무」의 전승자로 지정된 예능 보유자. | Wiki: 晋州劍舞
    '강규찬': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EA%B7%9C%EC%B0%AC'},  # 근대 - 일제강점기 때, 105인 사건 등과 관련된 목사.
    '강규환': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%95%A0%EB%B9%84%EA%B7%9C%ED%99%98'},  # 조선/조선 후기 - 조선 후기 경종~영종대 활동한 노론-호론계 출신의 학자이자 영남안무사 종사관, 장릉참봉 등 | Wiki: 2020년 영화
    '강극성': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%95%88%EC%82%B0%ED%96%A5%EA%B5%90%EC%A7%80'},  # 조선/조선 전기 - 조선 전기에, 지평, 부교리, 교리 등을 역임한 문신.
    '강근호': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EA%B7%BC%ED%98%B8'},  # 근대/일제강점기 - 일제강점기, 청산리 대첩에 참전한 독립운동가. | Wiki: 한국의 독립운동가 (1888–1960)
    '강기덕': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EA%B8%B0%EB%8D%95'},  # 근대 - 일제강점기 때, 3·1운동의 기획과 실행에 가담한 민족대표 48인 중 한 사람으로, 학생  | Wiki: 한국의 독립운동가
    '강기동': {'role': 'other foreigner', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EA%B8%B0%EB%8F%99'},  # 근대/대한제국기 - 대한제국기 때, 일본헌병보조원으로 위장 귀순하여 포로의병들을 석방하고 무기를 탈취해 항일의 | Wiki: 구한말의 의병장
    '강기운': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EA%B8%B0%EC%9A%B4'},  # 근대 - 일제강점기 때, 국민회에서 활동하며 독립군과 군자금 모집 및 밀정색출 작업을 전개한 독립운 | Wiki: 한국의 독립운동가
    '강기찬': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EA%B8%B0%EC%B0%AC'},  # 근대 - 일제강점기 때, 제주에서 독서회를 조직하고 일인상품불매운동을 전개하는 등 항일계몽운동을 전 | Wiki: 위키미디어 동음이의어 문서
    '강난형': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%ED%98%95%EC%A1%B0'},  # 조선 - 조선 후기에, 형조판서, 한성부판윤, 황해도관찰사 등을 역임한 문신.
    '강남중': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EB%82%A8%EC%A4%91%ED%95%99%EA%B5%90_(%EC%84%9C%EC%9A%B8)'},  # 근대/일제강점기 - 일제강점기 때, 김창환과 박유전의 제자로 원각사와 광무대에서 활약한 남도소리의 명창. | Wiki: 서울 동작구에 위치한 중학교
    '강달영': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EB%8B%AC%EC%98%81'},  # 근대/일제강점기 - 일제강점기 때, 조선노농총동맹 중앙위원, 제2차 조선공산당 책임비서 등을 역임한 사회주의  | Wiki: 일제강점기의 공산주의자
    '강달주': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%A1%B0%EC%84%A0%EA%B3%B5%EC%82%B0%EB%8B%B9'},  # 근대 - 대한제국기 때, 심남일 의진에서 후군장으로 활약하다 투옥되었으며, 출감 후 나주군의 독립운 | Wiki: 한국의 독립운동 단체이자 공산주의 정당
    '강대성': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EB%8C%80%EC%84%B1'},  # 근대 - 1890∼1954. 갱정유도(更定儒道)의 제1대 교조. | Wiki: 위키미디어 동음이의어 문서
    '강대수': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EB%8D%B0%EB%8B%88%EC%8A%A4_%EA%B0%95'},  # 조선/조선 후기 - 조선 후기에, 호조좌랑, 예조정랑, 병조참의 등을 역임한 문신. | Wiki: 캐나다의 한국계 이종 격투기 선수
    '강대적': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 병자호란 당시 청군에 대적해서 싸운 의병장.
    '강덕룡': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%82%AC%EC%B2%9C%EC%8B%9C'},  # 조선 - 조선시대 때, 함창현감, 장기현감 등을 역임한 무신. | Wiki: 대한민국의 경상남도 도시
    '강도근': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EB%8F%84%EA%B7%BC'},  # 현대/대한민국 - 판소리의 전승자로 지정된 예능 보유자. | Wiki: 판소리 인간문화재
    '강도순절인': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B9%80%EA%B2%BD%EC%A7%95'},  # 조선/조선 후기 - 조선 후기에, 병자호란으로 강화가 함락되자 순절한 관리. | Wiki: 조선 후기의 무신
    '강도영': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%ED%92%80'},  # 근대 - 개항기 때, 우리나라에서 3번째로 사제 서품을 받은 신부. | Wiki: 대한민국의 웹툰 작가
    '강동진': {'role': 'scholar foreigner', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EB%8F%99%EC%A7%84'},  # 근대 - 「일본의 조선지배정책사 연구」, 「한국노동조합운동사」 등을 저술한 역사학자. | Wiki: 위키미디어 동음이의어 문서
    '강두안': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%A0%95%EB%AA%BD%EC%A3%BC'},  # 근대/일제강점기 - 일제강점기 때, 대구사범학교에서 항일비밀결사인 문예부를 조직해 기관잡지인 『학생』, 『반딧 | Wiki: 고려 말의 문신
    '강로': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EB%A1%9C'},  # 근대 - 조선 후기에, 사간원대사간, 병조판서, 좌의정 등을 역임한 문신. | Wiki: 조선 말기의 문신
    '강린': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/He'story'},  # 조선/조선 전기 - 조선 전기에, 교리, 부수찬, 함경도어사 등을 역임한 문신.
    '강매': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EB%A7%A4'},  # 근대/일제강점기 - 일제강점기 때, 『조선문법제요』, 『잘 뽑은 조선말과 글의 본』 등을 저술한 국어학자.
    '강맹경': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EB%A7%B9%EA%B2%BD'},  # 조선/조선 전기 - 조선 전기에, 예문관제학, 의정부우참찬, 좌찬성 등을 역임한 문신. | Wiki: 조선의 문신
    '강명규': {'role': 'other foreigner', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EB%B0%98%EB%AF%BC%EC%A1%B1%ED%96%89%EC%9C%84%ED%8A%B9%EB%B3%84%EC%A1%B0%EC%82%AC%EC%9C%84%EC%9B%90%ED%9A%8C'},  # 근대/일제강점기 - 일제강점기 중국 만주에서 활약한 독립운동가. | Wiki: 반민특위
    '강명길': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%A0%95%EC%A1%B0'},  # 조선/조선 후기 - 조선 후기에, 내의원수의, 양주목사, 지중추부사 등을 역임한 의관. | Wiki: 조선의 제22대 임금 (1752–1800)
    '강명준': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%9A%A9%EC%9D%B8%EC%8B%9C_%EB%B9%A0%EB%94%B0%ED%98%95_%EB%8F%85%EB%A6%BD%EC%95%BC%EA%B5%AC%EB%8B%A8'},  # 근대 - 개항기 때, 임오군란 당시의 군인.
    '강무경': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%A7%84%EC%A3%BC_%EA%B0%95%EC%94%A8_%EC%84%B8%EA%B3%84%EB%8F%84'},  # 근대/개항기 - 대한제국기 때, 심남일 의진에서 선봉장으로 활약한 의병.
    '강문규': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EB%AC%B8%EA%B7%9C'},  # 조선/조선 후기 - 조선 후기에, 희릉참봉, 의영고봉사 등을 역임한 문신.
    '강문봉': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EB%AC%B8%EB%B4%89'},  # 현대 - 김창룡 육군 특무부대장 암살사건 당시의 군인 · 외교관. | Wiki: 대한민국의 군인, 외교관, 정치가
    '강문수': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EB%AC%B8%EC%88%98'},  # 근대/일제강점기 - 일제강점기 때, 조선공산당 만주부 조직 책임, 대한민국 특무부대 장교 등을 역임한 사회주의
    '강문진': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%ED%95%9C%EA%B5%AD%EA%B0%9C%ED%98%81%EC%A3%BC%EC%9D%98%EC%84%A4%EA%B5%90%EC%97%B0%EA%B5%AC%EC%9B%90'},  # 근대 - 일제강점기 때, 대동단에 입단하여 군자금을 모금하여 임시정부에 조달하는 활동을 전개한 독립
    '강문형': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/TV%EC%87%BC_%EC%A7%84%ED%92%88%EB%AA%85%ED%92%88'},  # 근대 - 조선 후기에, 예방승지, 협판교섭통상사무, 이조참판 등을 역임한 문신. | Wiki: KBS 1TV에서 방송되는 골동품 감정 프로그램
    '강문회': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%9D%BC%EC%88%9C'},  # 조선/조선 전기 - 조선 전기에, 예문관 검열을 역임하고, 성균관에서 후학을 지도한 문신.
    '강민저': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%B4%88%EB%81%88_%EC%9D%B4%EB%A1%A0'},  # 조선 - 조선 후기에, 희빈장씨를 옹호하던 남구만을 규탄한 죄로 유배되었다가 벼슬을 단념하였고, 이 | Wiki: 끈이론에 초대칭성을 도입한 물리학 이론
    '강민첨': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EB%AF%BC%EC%B2%A8'},  # 고려/고려 전기 - 고려 전기에, 안찰사, 내사사인, 지중추사 병부상서 등을 역임하였으며, 동여진과 거란의 친 | Wiki: 고려의 문신 (963–1021)
    '강박': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EB%B0%95%EC%9E%A5%EC%95%A0'},  # 조선/조선 후기 - 조선 후기 부교리, 수찬, 필선 등을 역임한 문신. | Wiki: 질병의 종류
    '강백': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EB%B0%B1'},  # 조선/조선 후기 - 조선 후기에, 승문원박사, 정산현감, 한성부우윤 등을 역임한 문신.
    '강백규': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%9D%B4%EA%B4%84'},  # 근대/일제강점기 - 일제강점기 때, 대한국민회, 간도청년회, 대한청년단 등에서 활동하며 항일투쟁을 전개한 독립
    '강백년': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%84%B8%ED%99%A9'},  # 조선/조선 후기 - 조선 후기 관각문학을 대표하는 문한(文翰)이자 청렴한 관직 생활로 청백리에 녹선된 문신. | Wiki: 조선의 화가 (1713~1791)
    '강백진': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EB%B0%B1'},  # 조선/조선 전기 - 조선 전기에, 함안군수, 사헌부장령, 사간원사간 등을 역임한 문신.
    '강백천': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B9%80%EB%8F%99%EC%A7%84_(%EA%B5%AD%EC%95%85%EC%9D%B8)'},  # 근대 - 「대금 산조」를 전승한 예능 보유자. | Wiki: 대한민국의 국악인
    '강변칠우': {'role': 'novelist', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%84%EC%B6%95%EC%98%A5%EC%82%AC'},  # 조선/조선 후기 - 조선 후기에, 북한강변에서 시와 술로 세월을 보낸 박응서 등 일곱 명의 문인들.
    '강병두': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B5%AD%EB%AF%BC%EB%8C%80%ED%95%99%EA%B5%90'},  # 현대/대한민국 - 국가재건최고회의 헌법심의위원회 전문위원, 행정계획조사위원회 위원 등으로 활동하였으며, 『신 | Wiki: 대한민국 서울특별시의 사립 종합대학
    '강병일': {'role': 'other foreigner', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EB%B3%91%EC%9D%BC'},  # 근대/일제강점기 - 일제강점기 중국 만주에서 항일투쟁을 한 독립운동가.
    '강병주': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EB%B3%91%EC%A3%BC'},  # 근대 - 일제강점기 때, 『큰 사전』 편찬 전문위원, 내명학교 교장, 경안중학교 교장 등을 역임한  | Wiki: 위키미디어 동음이의어 문서
    '강보': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EB%B3%B4'},  # 고려/고려 후기 - 고려 후기 판서운관사를 역임한 과학기술자. | Wiki: 고려 말의 문신
    '강복성': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EB%B3%B5%EC%8B%A0'},  # 조선/조선 후기 - 조선 후기에, 평산부사, 전주부윤, 청송부사 등을 역임한 문신. | Wiki: 한국의 체육인 (1916–1944)
    '강복중': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%8B%A0%EC%B2%9C_%EA%B0%95%EC%94%A8'},  # 조선/조선 후기 - 조선 후기에, 「수월정청흥가」, 「위군위친통곡가」, 「분산회복사은가」 등의 작품을 남긴 문
    '강봉수': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EB%B4%89%EC%88%98'},  # 조선/조선 전기 - 조선 전기에, 평창군수, 참판 등을 역임한 문신. | Wiki: 위키미디어 동음이의어 문서
    '강봉우': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B4%91%EC%A3%BC%EC%A0%9C%EC%9D%BC%EA%B3%A0%EB%93%B1%ED%95%99%EA%B5%90'},  # 근대 - 일제강점기 때, 105인사건으로 옥고를 치렀으며, 간도에서 3·1운동을 주도한 독립운동가. | Wiki: 대한민국의 공립고등학교
    '강사덕': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%A7%84%EC%A3%BC_%EA%B0%95%EC%94%A8_(%EA%B0%95%EC%9D%B4%EC%8B%9D)'},  # 조선/조선 전기 - 조선 전기에, 우군도총제, 전라도병마도절제사, 판승녕부사 등을 역임한 무신.
    '강사상': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%82%AC%EC%83%81'},  # 조선/조선 전기 - 조선 전기에, 병조판서, 형조판서, 이조판서 등을 역임한 문신. | Wiki: 조선의 문신, 정치가
    '강사필': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%ED%99%A9%ED%98%84%ED%95%84'},  # 조선/조선 전기 - 조선 전기에, 병조참의, 사헌부대사헌, 승문원부제조 등을 역임한 문신.
    '강삼': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%82%BC%EC%9D%BC'},  # 조선/조선 전기 - 조선 전기에, 동부승지, 우부승지, 우승지 등을 역임한 문신. | Wiki: 대한민국의 축구 선수
    '강상국': {'role': 'scholar'},  # 조선 - 조선 후기에, 『능호집』 등을 저술한 학자.
    '강상모': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EB%B4%89%EC%98%A4%EB%8F%99_%EC%A0%84%ED%88%AC'},  # 근대 - 일제강점기 때, 홍범도가 이끄는 대한독립군에서 활동한 독립운동가.
    '강상인': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%83%81%EC%9D%B8'},  # 조선/조선 전기 - 조선 전기에, 병조참판을 역임한 무신.
    '강상주': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%83%81%EC%A3%BC'},  # 근대 - 일제강점기 때, 제5군부설 체카 특별부 전권위원, 연해주 소비에트 집행위원회 감시관 등을  | Wiki: 위키미디어 동음이의어 문서
    '강상호': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%83%81%ED%98%B8'},  # 현대/대한민국 - 북한에서, 내무성 부상, 인민군 총정치국장 등을 역임하다가 김일성 독재를 규탄하며 소련으로 | Wiki: 위키미디어 동음이의어 문서
    '강서': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%84%9C'},  # 조선/조선 전기 - 조선 전기에, 수원부사, 우승지, 좌승지 등을 역임한 문신. | Wiki: 위키미디어 동음이의어 문서
    '강서룡': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%84%9C%EB%A3%A1'},  # 현대/대한민국 - 내무부 치안국장, 국방부차관, 교통부장관 등을 역임한 법조인 · 관료. | Wiki: 대한민국의 법조인 겸 관료
    '강석': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%84%9D_(1952%EB%85%84)'},  # 고려/고려 후기 - 고려 후기에, 동지밀직사사, 교주강릉도도순문 겸 병마사, 삼재 등을 역임한 무신.
    '강석구': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%84%9D%EA%B5%AC'},  # 조선 - 조선 후기에, 헌납, 사간, 집의 등을 역임한 문신. | Wiki: 위키미디어 동음이의어 문서
    '강석기': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%84%9D%EA%B8%B0'},  # 조선/조선 후기 - 조선 후기에, 대사간, 대사성, 도승지, 이조판서 등을 역임한 문신. | Wiki: 조선 중기의 문신
    '강석덕': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%ED%9D%AC%EB%A7%B9'},  # 조선/조선 전기 - 조선 전기에, 우부승지, 호조참판, 대사헌 등을 역임한 문신. | Wiki: 조선 초기 문신
    '강석봉': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%84%9D%EB%B4%89'},  # 근대/일제강점기 - 일제강점기 때, 조선청년총동맹 중앙집행위원, 건국준비위원회 전남지부 부위원장 등을 역임한  | Wiki: 한국의 독립운동가
    '강석빈': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%86%90%EC%84%9D%ED%9D%AC'},  # 조선 - 조선 후기에, 충청도암행어사, 이조좌랑, 경기도수군절도사 등을 역임한 문신. | Wiki: 대한민국의 언론인
    '강석숭': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%A1%B0%EC%84%A0%EB%AF%BC%EC%A3%BC%EC%A3%BC%EC%9D%98%EC%9D%B8%EB%AF%BC%EA%B3%B5%ED%99%94%EA%B5%AD_%EB%82%B4%EB%AC%B4%EC%84%B1'},  # 현대/대한민국 - 북한에서, 당 중앙위원, 최고인민회의 대의원, 당 역사연구소장 등을 역임한 관료.
    '강석연': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EB%B9%85%ED%84%B0%EB%A0%88%EC%BD%94%EB%93%9C%ED%9A%8C%EC%82%AC'},  # 근대/일제강점기 - 일제강점기 「모란등기」 · 「모반의 혈」 · 「대장안」 등에 출연한 배우. 가수.
    '강석창': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%ED%8F%AC%EC%BB%A4%EC%8A%A4_%EC%9D%B8_%EC%A0%9C%EC%A3%BC'},  # 조선 - 조선 후기에, 고산찰방, 종성부사 등을 역임한 문신.
    '강석호': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%84%9D%ED%98%B8'},  # 근대/개항기 - 조선 후기~대한제국기에 국왕 고종의 총애를 받으며 정치에 관여하였던 내시. | Wiki: 위키미디어 동음이의어 문서
    '강선': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%84%A0'},  # 조선/조선 후기 - 조선 후기에, 강원도관찰사, 형조참판, 도승지 등을 역임한 문신.
    '강선여': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%84%A0'},  # 조선/조선 후기 - 조선 후기에, 공조좌랑, 예조좌랑, 병조좌랑 등을 역임한 문신.
    '강선힐': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%84%A0%ED%9E%90'},  # 고대/남북국 - 남북국시대 때, 태봉국의 왕건이 나주지방으로의 출정을 도운 장수.
    '강섬': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%84%AC%EB%AA%A8%EC%B6%A9%EC%86%8D'},  # 조선/조선 전기 - 조선 전기에, 함경도어사, 사간원헌납, 도승지 등을 역임한 문신.
    '강성산': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%84%B1%EC%82%B0'},  # 현대/대한민국 - 북한에서, 노동당 중앙위원, 최고인민회의 대의원, 정무원 총리 등을 역임한 관료. | Wiki: 조선민주주의인민공화국의 정치인
    '강성삼': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%ED%95%9C%EA%B5%AD%ED%8E%AB%EA%B3%A0%EB%93%B1%ED%95%99%EA%B5%90'},  # 근대 - 개항기 때, 우리나라에서 첫 번째로 사제서품을 받은 신부. | Wiki: 대한민국의 사립고등학교
    '강성좌': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EB%AC%B8_(%EC%84%B1%EC%94%A8)'},  # 조선 - 조선 후기에, 오위도총부도사, 훈련원정, 영변부사 등을 역임한 무신. | Wiki: 한국의 성씨
    '강성태': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%84%B1%ED%83%9C'},  # 현대 - 대한테니스협회 회장, 대한손해보험협회 이사장, 상공부장관, 민의원 의원 등을 역임한 실업가 | Wiki: 위키미디어 동음이의어 문서
    '강세': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%84%B8'},  # 고대/삼국 - 삼국시대 때, 신라의 이벌찬 등을 역임한 관리.
    '강세구': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%95%88%EC%A0%95%EB%B3%B5'},  # 조선/조선 후기 - 조선 후기에, 호조참의, 충청도관찰사, 대사간 등을 역임한 문신. | Wiki: 조선 후기의 실학자 (1712–1791)
    '강세규': {'role': 'other'},  # 조선 - 조선 후기에, 지평, 정언, 기주관 등을 역임한 문신.
    '강세윤': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%95%88%EB%8F%99_%EA%B0%95%EC%94%A8'},  # 조선 - 조선 후기에, 승정원주서, 이천부사 등을 역임한 문신.
    '강세황': {'role': 'critic', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%84%B8%ED%99%A9'},  # 조선/조선 후기 - 조선후기 시, 서, 화 삼절(三絶)로 일컬어진 화가. 문관, 평론가. | Wiki: 조선의 화가 (1713~1791)
    '강소천': {'role': 'childrenauthor', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%86%8C%EC%B2%9C'},  # 근대/일제강점기 - 일제강점기 때, 「길가에 얼음판」, 「얼굴 모르는 동무에게」, 「호박꽃과 반딧불」 등을 저 | Wiki: 한국의 작가 (1915–1963)
    '강소춘': {'role': 'other'},  # 근대 - 조선 후기에, 원각사 및 협률사의 창극 공연에 참가한 판소리의 명창.
    '강수': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%88%98'},  # 조선 - 조선 후기에, 예조좌랑, 장악원첨정, 장령 등을 역임한 문신. | Wiki: 수증기가 응축하여 땅에 내리는 것
    '강수곤': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%88%98'},  # 조선 - 조선 중기에, 공조좌랑, 고창현감, 괴산군수 등을 역임한 문신. | Wiki: 수증기가 응축하여 땅에 내리는 것
    '강수남': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%84%9C%EC%9A%B8%ED%8A%B9%EB%B3%84%EC%8B%9C'},  # 조선/조선 전기 - 조선 전기에, 예조좌랑, 병조정랑, 이조참판 등을 역임한 문신. | Wiki: 대한민국의 수도
    '강수형': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%86%8C%EA%B5%B0_%EC%99%95%EC%84%9C'},  # 고려 - 고려 후기에, 북경동지, 동경총관, 찬성사 등을 역임한 역관.
    '강숙경': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%ED%94%BC%EC%A7%80%EC%BB%AC%3A_100'},  # 조선/조선 전기 - 조선 전기에, 밀양도호부사, 강원도사, 함안군수 등을 역임한 문신. | Wiki: 서바이벌 게임 예능
    '강숙돌': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B8%88%EC%B2%9C_%EA%B0%95%EC%94%A8'},  # 조선/조선 전기 - 조선 전기에, 의금부도사, 사헌부지평, 사간원사간 등을 역임한 문신.
    '강순': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%88%9C'},  # 근대/일제강점기 - 일제강점기 때, 대한민국임시의정원 의원 등을 역임하였으며, 해방 이후 북한에서, 최고인민회
    '강순룡': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%9C%A4%EC%84%B1'},  # 고려/고려 후기 - 고려 후기에, 지밀직사, 찬성사, 재령백 등을 역임한 무신.
    '강순의': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EB%82%A8%EC%9D%B4%EC%9D%98_%EC%98%A5'},  # 고려/고려 후기 - 고려 후기에, 어사중승, 섭대장군, 초토처치병마우도사 등을 역임한 무신.
    '강순필': {'role': 'other foreigner', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EB%B3%91%EC%88%98'},  # 근대/일제강점기 - 일제강점기 때, 대한광복회를 결성하여 활동하다가 일본경찰에게 발각되어 처형당한 독립운동가.
    '강승우': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%8A%B9%EC%9A%B0'},  # 현대 - 한국전쟁 때, 강원도 철원의 백마고지 전투에 참전한 군인.
    '강시': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%8B%9C'},  # 고려/고려 후기 - 고려 후기에, 삼사좌윤, 군기판관, 강릉도안찰사 등을 역임한 문신.
    '강시경': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%8B%9C'},  # 조선/조선 후기 - 조선 후기에, 장령, 지평, 정언 등을 역임한 문신.
    '강시만': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%8B%9C'},  # 근대/일제강점기 - 일제강점기 때, 경상남도 합천군 독립만세시위로 체포된 구금자의 석방을 위해 결사대를 조직하
    '강시영': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%9D%98%EC%82%AC%EC%9A%94%ED%95%9C'},  # 조선/조선 후기 - 조선 후기에, 형조판서, 대사헌, 예조판서 등을 역임한 문신. | Wiki: 대한민국의 드라마
    '강시원': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%8B%9C%EC%9B%90'},  # 근대 - 개항기 때, 차도주를 역임한 천도교인.
    '강시환': {'role': 'other'},  # 조선 - 조선 후기에, 양양부사, 장령, 헌납 등을 역임한 문신.
    '강신': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%8B%A0'},  # 조선 - 조선 중기에, 강원도관찰사, 경기도관찰사, 좌참찬 등을 역임한 문신.
    '강신명': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%8B%A0%EB%AA%85'},  # 현대/대한민국 - 해방 이후, 숭실대학교 이사장, 대한기독교교육협회(大韓基督敎敎育協會) 회장, 서울장로회신학 | Wiki: 위키미디어 동음이의어 문서
    '강신재': {'role': 'novelist', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%8B%A0%EC%9E%AC'},  # 현대/대한민국 - 해방 이후 「얼굴」 · 「젊은 느티나무」 · 「표선생 수난기」 등을 저술한 소설가. | Wiki: 대한민국의 소설가 (1924–2001)
    '강신호': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%8B%A0%ED%98%B8'},  # 근대 - 일제강점기 「의자」, 「작품제9」, 「진주풍경」 등을 그린 화가. 서양화가. | Wiki: 대한민국의 기업인 (1927–2023)
    '강심': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%BA%A1%EC%82%AC%EC%9D%B4%EC%8B%A0'},  # 고대/삼국/신라 - 삼국시대 때, 신라의 통일전쟁에 참여한 이동혜 지방의 촌주.
    '강양공': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%96%91%EA%B3%B5'},  # 고려 - 고려의 제25대 왕, 충렬왕의 첫째 왕자. | Wiki: 고려의 왕족
    '강언룡': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95_(%EC%84%B1%EC%94%A8)'},  # 조선/조선 전기 - 조선 전기에, 유곡도찰방, 좌승지 등을 역임한 무신. | Wiki: 한국의 성씨
    '강여재': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%98%A8%EB%8B%AC_%EC%99%95%EC%9E%90%EB%93%A4'},  # 조선 - 조선 후기에, 장령, 세자시강원 보덕 등을 역임한 문신.
    '강여호': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/10%EA%B0%80%EC%A7%80_%EC%9E%AC%EC%95%99'},  # 조선/조선 후기 - 조선 후기에, 사간원정언, 사헌부장령, 종성부사 등을 역임한 문신. | Wiki: 출애굽기에 이집트에 내렸다고 기록된 10가지 재앙
    '강연': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%9D%98'},  # 조선 - 조선 중기에, 인천부사, 첨지중추부사, 한성부판윤 등을 역임한 문신. | Wiki: 대학교에서 이루어지는 구술 프레젠테이션
    '강영': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%98%81%EC%95%84'},  # 고려/고려 후기 - 고려 후기에, 강계만호, 조전원수 등을 역임한 무신 · 공신.
    '강영각': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%9D%B4%EC%9A%A9%EC%A7%81_(1894%EB%85%84)'},  # 근대/일제강점기 - 일제강점기 때, 하와이로 노동 이민하여 임시정부후원회 이사부원, 재미한족연합위원회 의사부  | Wiki: 한국의 기독교 지도자
    '강영선': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%ED%99%A9%EA%B8%88%EC%96%B4%EC%9E%A5_%EB%9D%BC%EB%94%94%EC%98%A4%EC%8A%A4%ED%83%80'},  # 현대/대한민국 - 한국자연보존협회 회장, 한국생물과학협회 회장 등을 역임한 유전학자. | Wiki: 수요일 밤 10시 30분에 방송되는 예능
    '강영소': {'role': 'other foreigner', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%96%91%EC%9A%B0%EC%A1%B0'},  # 근대/일제강점기 - 일제강점기 때, 미국으로 노동 이민하여 흥사단을 조직하고, 대한인국민회 북미지방 총회장, 
    '강영준': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%98%81%EC%A4%80'},  # 고려/고려 전기 - 고려 전기에, 내시 위위주부, 좌상시 등을 역임한 문신.
    '강영지': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%98%81%EC%A7%80'},  # 조선 - 조선 후기에, 『수재집』, 「심학집략」 등을 저술한 학자. | Wiki: 구멍장이버섯목 불로초과에 속하는 버섯의 한 종류
    '강옥경': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EB%AA%85%ED%83%90%EC%A0%95_%EC%BD%94%EB%82%9C%3A_%EC%B9%A0%ED%9D%91%EC%9D%98_%EC%B6%94%EC%A0%81%EC%9E%90'},  # 현대 - 해방 이후 「진주검무」 전승자로 지정된 기예능보유자.
    '강완숙': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%99%84%EC%88%99'},  # 조선 - 조선 후기에, 신유박해 당시의 순교자. | Wiki: 신유박해 때 순교한 천주교 순교자
    '강왕': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%99%95'},  # 발해의 제6대(재위: 795년~809년) 왕. | Wiki: 위키미디어 동음이의어 문서
    '강용구': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95_%EB%AF%B8%ED%95%98%EC%9D%BC'},  # 근대 - 원로원 참의, 삼일원 대덕, 대일각 전교 등을 역임한 대종교인.
    '강용환': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%9A%A9%ED%99%98'},  # 근대 - 대한제국기 때, 이날치의 제자로 김창환 협률사에서 활동한 판소리의 명창.
    '강용흘': {'role': 'novelist', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%9A%A9%ED%9D%98'},  # 근대/일제강점기 - 일제강점기 때, 「행복한 숲」, 「동양인이 본 서양」, 「초당」 등을 저술한 소설가. | Wiki: 대한민국의 소설가
    '강우': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EB%B9%84_(%EB%82%A0%EC%94%A8)'},  # 근대 - 일제강점기 때, 『종리문답』, 『천산도설』, 『제천혈고사』 등을 저술한 대종교인. | Wiki: 대기권의 수증기가 응축되어 물방울의 형태로 지상에 떨어
    '강우규': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%9A%B0%EA%B7%9C'},  # 근대/일제강점기 - 대한국민노인동맹단 라오허현 지부장으로 사이토 마코토 총독 처단 투탄 의거를 일으킨 독립운동 | Wiki: 일제 강점기의 한의사 겸 독립운동가 (1855-1920
    '강우성': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%A7%80%ED%9B%84'},  # 조선/조선 후기 - 조선시대 때, 부산훈도이자 『첩해신어』를 저술한 역관. | Wiki: 대한민국 배우
    '강우형': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%A7%84%EC%A3%BC_%EA%B0%95%EC%94%A8_(%EA%B0%95%EC%9D%B4%EC%8B%9D)'},  # 조선/조선 후기 - 조선 후기에, 중추원의관, 장례원소경, 봉상사제조 등을 역임한 문신.
    '강욱': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%9A%B1'},  # 조선/조선 전기 - 조선 전기에, 도승지, 예조참의, 강원도관찰사 등을 역임한 문신. | Wiki: 위키미디어 동음이의어 문서
    '강운': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%9A%B4'},  # 조선/조선 후기 - 조선 후기 영남 남인 출신의 학자이자 전적, 지평, 이조좌랑 등을 역임한 문신.
    '강운경': {'role': 'other'},  # 현대/대한민국 - 서울대학교 교수, 한국듀오피아노협회 회장 등을 역임한 음악가.
    '강원': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%9B%90%EB%8F%84'},  # 조선/조선 전기 - 조선 전기에, 전의현감, 공주목사, 청주목사 등을 역임한 문신. | Wiki: 한국의 도
    '강원보': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%8B%A0%EB%8F%88_(%EB%93%9C%EB%9D%BC%EB%A7%88)'},  # 고려/고려 후기 - 고려 후기에, 종부부령, 판소부시사 등을 역임한 문신.
    '강원영': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EB%A5%98%ED%98%84%EA%B2%BD'},  # 근대/개항기 - 대한제국기 때, 대한의학교 교관, 육군 3등 군의관 등을 역임한 의관. | Wiki: 대한민국의 배우
    '강원용': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%9B%90%EC%9A%A9'},  # 현대/대한민국 - 해방 이후 아시아종교인평화회의 의장, 세계종교인평화회의 공동의장 등을 역임한 목사. 교육자
    '강원형': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/KUH-1_%EC%88%98%EB%A6%AC%EC%98%A8'},  # 근대 - 대한제국기 때, 십삼도유생연명소의 소수로 상소를 올린 민족운동가. | Wiki: 대한민국의 다목적 헬리콥터
    '강위': {'role': 'poet', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%9C%84'},  # 근대/개항기 - 개항기 때, 『경위합벽』, 『손무자주』, 『동문자모분해』 등을 저술한 시인 · 개화사상가. | Wiki: 조선의 유학자, 철학자, 시인, 외교관
    '강위빙': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%9D%B8%EC%B2%9C_%EC%B6%A9%EB%A0%AC%EC%82%AC'},  # 조선/조선 후기 - 조선 후기에, 희릉참봉, 종묘서봉사, 순안현령 등을 역임한 문신.
    '강유': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%9C%A0'},  # 조선 - 조선 후기에, 황해감사, 경기수군절도사, 호조참의 등을 역임한 문신.
    '강유선': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EB%B2%88%EA%B0%9C%EB%A7%A8%EC%9D%98_%EB%B9%84%EB%B0%80'},  # 조선 - 조선 전기에, 『주천집』을 저술한 유생.
    '강유정': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%9C%A0%EC%A0%95_(%ED%8F%89%EB%A1%A0%EA%B0%80)'},  # 현대 - 해방 이후 여인극장 대표, 한국연극협회 이사 등을 역임한 연출가. | Wiki: 대한민국의 평론가 겸 이재명 대통령 대변인
    '강유후': {'role': 'other'},  # 조선 - 조선 후기에, 정주목사, 강계부사, 의주부윤 등을 역임한 문신.
    '강윤': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%9C%A4'},  # 근대/일제강점기|현대 - 일제강점기 때, 태화기독교사회관을 신축한 건축가. | Wiki: 위키미디어 동음이의어 문서
    '강윤국': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%9C%A4%EA%B5%AD'},  # 근대/일제강점기 - 일제강점기 때, 대한애국청년당을 결성하여 부민관 투탄 의거를 전개한 독립운동가. | Wiki: 한국의 독립운동가 (1926–2009)
    '강윤명': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%9C%A4%EB%AA%85%ED%98%81'},  # 고려 - 고려 충렬왕 때, 영월에서 민란을 일으킨 주모자.
    '강윤소': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%9E%84%EC%8A%B9%EB%8C%80'},  # 고려 - 고려 후기에, 원종폐립사건 당시의 관리. | Wiki: 대한민국의 배우
    '강윤충': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%9C%A4%EC%B6%A9'},  # 고려 - 고려 후기에, 찬성사, 판삼사사 등을 역임한 문신 · 공신. | Wiki: 백제의 장군 (?–?)
    '강윤형': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%84%9C%EC%9A%B8_%EC%9E%90%EA%B0%80%EC%97%90_%EB%8C%80%EA%B8%B0%EC%97%85_%EB%8B%A4%EB%8B%88%EB%8A%94_%EA%B9%80_%EB%B6%80%EC%9E%A5_%EC%9D%B4%EC%95%BC%EA%B8%B0'},  # 조선/조선 후기 - 조선 후기에, 만경현령, 동부승지, 승지 등을 역임한 문신.
    '강윤희': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%9C%A4%ED%9D%AC'},  # 근대/개항기 - 대한제국기 경기도 가평 출신으로, 관동창의진(關東倡義陣)과 13도창의군에서 활동한 의병장.
    '강융': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%9C%B5'},  # 고려 - 고려 후기에, 만호, 찬성사, 첨의좌정승판삼사사 등을 역임한 문신.
    '강은': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EB%A9%B4%EC%A0%81%EC%88%9C_%EB%82%98%EB%9D%BC_%EB%AA%A9%EB%A1%9D'},  # 조선/조선 전기 - 조선 전기에, 검열, 예빈시참봉, 전적 등을 역임한 문신. | Wiki: 위키미디어 목록 항목
    '강응정': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%A0%95%EC%9D%B8%EC%84%A0'},  # 조선 - 조선 전기에, 김용석, 신종호 등과 향약을 만들고, 『소학』을 강론한 문신.
    '강응철': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%8B%A0%EC%B2%9C_%EA%B0%95%EC%94%A8'},  # 조선 - 조선 중기에, 찰방 등을 역임하였으며, 임진왜란이 발발하자 의병을 일으켜 항쟁한 의병장.
    '강응태': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%ED%83%9C%EC%A1%B0_(%EC%A1%B0%EC%84%A0)'},  # 조선/조선 전기 - 조선 전기에, 성균관전적, 사헌부지평, 순천도호부사 등을 역임한 문신. | Wiki: 조선의 초대 임금 (1335–1408)
    '강응환': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%88%98%EC%82%AC%EA%B3%B5%EA%B0%95%EC%9D%91%ED%99%98%EA%B0%80%EC%A0%84%EC%9C%A0%EB%AC%BC'},  # 조선/조선 후기 - 조선 후기에, 고령진첨사, 창성부사, 동래부사 등을 역임한 무신.
    '강이문': {'role': 'critic', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%9D%98%EC%82%AC%EC%9A%94%ED%95%9C'},  # 현대 - 해방 이후 부산여자대학교 무용과 교수, 한국춤평론가회 회장 등을 역임한 평론가. 춤평론가. | Wiki: 대한민국의 드라마
    '강이봉': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B8%88%EA%B0%95'},  # 근대 - 대한제국기 때, 문태수 의진에서 항일의병투쟁을 전개한 의병. | Wiki: 대한민국 충청권ㆍ전라북도의 강
    '강이상': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%A0%95%EC%86%8C%EB%AF%BC'},  # 조선 - 조선 후기에, 정언, 지평, 양덕현감 등을 역임한 문신. | Wiki: 대한민국의 배우
    '강이식': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%9D%B4%EC%8B%9D'},  # 고대/삼국/고구려 - 삼국시대 때, 고구려 임유관전투에 참전한 장수. | Wiki: 고구려의 장수 (?–?)
    '강이오': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%9D%B4%EC%98%A4_%EC%B4%88%EC%83%81'},  # 조선/조선 후기 - 조선 후기에, 「강안주유도」, 「송하망폭도」 등의 작품을 그린 화가.
    '강이원': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%A0%95%EC%95%BD%EC%9A%A9'},  # 조선 - 조선 후기, 이승훈, 정약용 등과 함께 천주교리를 강습한 일에 대하여 유생들이 상소를 올려 | Wiki: 조선의 실학자, 철학자 (1762–1836)
    '강이천': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B9%80%EB%A0%A4'},  # 조선 - 조선 후기에, 신유박해와 관련된 천주교인.
    '강익': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%ED%95%A8%EC%96%91_%EB%82%A8%EA%B3%84%EC%84%9C%EC%9B%90'},  # 조선 - 조선 전기에, 남계서원을 건립하여 정여창을 제향하였으며, 『개암집』을 저술한 학자.
    '강익록': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%ED%95%AD'},  # 근대/일제강점기 - 일제강점기 독립운동 자금을 모금하고, 일제의 경찰 주재소 습격으로 무기징역을 선고받고 옥고 | Wiki: 조선 중기의 문신 (1567~1618)
    '강익문': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%ED%95%A8%EC%96%91_%EB%82%A8%EA%B3%84%EC%84%9C%EC%9B%90'},  # 조선/조선 후기 - 조선 후기에, 예조좌랑, 충원현감, 제용감정 등을 역임한 문신.
    '강인': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%9D%B8_(%EA%B0%80%EC%88%98)'},  # 조선 - 조선 중기에, 공조좌랑, 한성부좌윤, 상주목사 등을 역임한 문신. | Wiki: 대한민국의 가수
    '강인부': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%9D%B8_(%EA%B0%80%EC%88%98)'},  # 고려 - 조선 전기에, 상의중추원사를 역임한 환관. | Wiki: 대한민국의 가수
    '강인수': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%9D%B8%EC%88%98'},  # 근대/일제강점기 - 일제강점기 때, 의열단, 조선의용군, 조선민족혁명당 특파원 등으로 활동하였으며 해방 이후, | Wiki: 위키미디어 동음이의어 문서
    '강인식': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%B6%A9%ED%9B%88%EA%B3%A0%EB%93%B1%ED%95%99%EA%B5%90'},  # 조선 - 조선 후기에, 대오전악, 집사악사 등을 역임한 거문고 명인. | Wiki: 대한민국의 공립고등학교
    '강인유': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%95%88%EB%B9%84_%EA%B0%95%EC%94%A8'},  # 고려 - 고려 후기에, 찬성사, 계품사 등을 역임한 문신.
    '강인희': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%9D%B8%ED%9D%AC'},  # 현대/대한민국 - 해방 이후 공주사범대학 가정과 교수, 명지대 가정학과 교수, 양정학원 이사 등을 역임한 교 | Wiki: 위키미디어 동음이의어 문서
    '강일순': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%9D%BC%EC%88%9C'},  # 근대 - 대한제국기 때, 증산사상을 개시한 종교 창시자.
    '강자평': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B2%BD%EC%8B%A0%EC%98%B9%EC%A3%BC'},  # 조선/조선 전기 - 조선 전기에, 승정원동부승지, 우부승지, 형조참의 등을 역임한 문신. | Wiki: 조선의 옹주
    '강장원': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%9E%A5%EC%9B%90'},  # 근대 - 일제강점기 때, 김창환의 제자로 국립국악원 국악사로 활동한 판소리의 명창.
    '강재구': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%9E%AC%EA%B5%AC'},  # 현대/대한민국 - 수도사단 제1연대 소대장, 1군 하사관학교 수류탄 교관 등을 역임한 군인. | Wiki: 대한민국의 군인 (1937–1965)
    '강재만': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%9E%AC%EB%A7%8C'},  # 근대 - 조선 후기에, 동편제의 법통을 이은 판소리의 명창.
    '강재천': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B9%80%EA%B5%AC'},  # 근대 - 일제강점기 때, 의병으로 활동하다가 만주로 망명하였고, 북로군정서에 가입해 항일무장투쟁을  | Wiki: 대한민국의 정치인, 교육자, 독립운동가 (1876–19
    '강재항': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%9E%AC%ED%95%AD'},  # 조선/조선 후기 - 조선 후기, 선공감역, 한성주부, 회인현감 등을 역임한 문신.
    '강정택': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%A0%95%ED%83%9D'},  # 근대/일제강점기 - 일제하의 농정학자이자 해방 후 경성대학 교수, 농림부 차관 등을 역임한 농업 정책학자.
    '강정환': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%9D%B8%EC%B2%9C%EC%A0%95%EA%B0%81%EC%B4%88%EB%93%B1%ED%95%99%EA%B5%90'},  # 조선 - 조선 후기에, 『전암문집』 등을 저술한 학자.
    '강제': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%A0%9C'},  # 조선 - 조선 전기에, 영덕현감, 이조정랑 등을 역임한 문신.
    '강제억': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EB%B0%95%EA%B8%B0%EC%96%91'},  # 근대/일제강점기 - 일제강점기 1919년 평안북도 창성에서 3·1운동에 참여하고, 1920년 1월 대한민국임시 | Wiki: 조선 말기의 관료, 일제강점기의 조선귀족 (1856–1
    '강제원': {'role': 'scholar'},  # 현대/대한민국 - 『한국동식물도감』 해조류편을 저술한 생물학자.
    '강제하': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%ED%99%80%EB%A1%9C%EC%BD%94%EC%8A%A4%ED%8A%B8'},  # 근대 - 일제강점기 때, 대한민국임시정부 파견원, 대한통의부 교통위원장 등을 역임하여 만세시위 계획 | Wiki: 나치 독일의 유럽 유대인 학살
    '강제희': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%ED%95%AB%EB%8F%84%EA%B7%B8_TV'},  # 근대/일제강점기 - 일제강점기 때, 평안북도 창성의 독립만세시위를 주도하였고, 대한민국임시정부 평안북도창성군 
    '강조': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%A1%B0'},  # 고려/고려 전기 - 고려 전기, 서북면도순검사, 중대사, 이부상서 · 참지정사, 행영도통사 등을 역임한 권신. | Wiki: 고려의 관리
    '강조원': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EB%B3%84%EB%82%9C_%EC%B2%AD%EC%B6%98'},  # 근대/일제강점기 - 일제강점기 개성 남부교회, 경기도 파주구읍교회, 개풍군 풍덕교회 등에서 목회한 목사.
    '강종': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%A2%85_(%EA%B3%A0%EB%A0%A4)'},  # 고려 - 고려의 제22대(재위: 1211~1213) 왕. | Wiki: 고려의 제22대 임금 (1152–1213)
    '강종경': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%A0%95%EC%84%9D%EA%B5%B0'},  # 조선 - 조선 전기에, 예문관검열, 성균관학유 등을 역임한 문신.
    '강주': {'role': 'novelist', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%A3%BC'},  # 조선/조선 후기 - 조선 후기 문신이자 문인. | Wiki: 위키미디어 동음이의어 문서
    '강주룡': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%A3%BC%EB%A3%A1'},  # 일제강점기 평양 소재 평원(平元)고무공장 여공으로 1931년 동맹파업을 벌인 항일노동운동가 | Wiki: 일제강점기 조선의 노동운동가
    '강주진': {'role': 'scholar foreigner', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EB%B0%95_(%EC%84%B1%EC%94%A8)'},  # 현대/대한민국 - 『정치학개론』, 『근대외교사』, 『미국정당 정치연구』 등을 저술한 서지학자. | Wiki: 한국의 성씨(朴)
    '강주호': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%A3%BC%ED%98%B8'},  # 조선 - 조선 후기에, 서숙을 열어 후진 양성에 전념하였으며, 『유금강산록』, 『유태백산록』, 『유 | Wiki: 대한민국의 축구 선수
    '강준호': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%A4%80%ED%98%B8'},  # 현대 - 멕시코 올림픽대회 등에서 지도자로 활약한 체육인. | Wiki: 위키미디어 동음이의어 문서
    '강준흠': {'role': 'novelist', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%A7%84%EC%A3%BC_%EA%B0%95%EC%94%A8_(%EA%B0%95%EC%9D%B4%EC%8B%9D)'},  # 조선/조선 후기 - 조선 후기 정언, 지평, 부수찬, 수안현감 등을 역임한 문신이며 문인.
    '강중경': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%9A%A9%EA%B0%95%EC%A4%91%ED%95%99%EA%B5%90_(%EC%84%9C%EC%9A%B8)'},  # 고려 - 고려 후기에, 동지밀직사사, 서북면병마사 등을 역임한 무신 · 공신.
    '강중상': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%9A%A9%EA%B0%95%EC%A4%91%ED%95%99%EA%B5%90_(%EC%84%9C%EC%9A%B8)'},  # 고려 - 고려 후기에, 경상도도순문진변사, 판개성부사, 경상도도순문사 등을 역임한 문신.
    '강중진': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%A7%84%EB%82%98%EB%9D%BC'},  # 조선/조선 전기 - 조선 전기에, 성균관전적, 형조좌랑, 승문원판교 등을 역임한 문신. | Wiki: 중국 최초의 통일 왕조
    '강증': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%98%81%EA%B0%95_%EA%B0%95%EC%94%A8'},  # 고려 - 고려 전기에, 수사공 참지정사판상서형부사, 중서시랑평장사 등을 역임한 문신.
    '강진': {'role': 'other foreigner', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%A7%84%EA%B5%B0'},  # 근대 - 일제강점기 때, 러시아 및 간도 등지에서 공산주의 활동을 하다가 해방 이후 조선인민공화국에 | Wiki: 대한민국의 행정 구역
    '강진구': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%9E%A5%EC%A7%84%EA%B5%AC_(%EC%B6%A9%EC%B9%AD%EC%8B%9C)'},  # 현대/대한민국 - 1973년 삼성전자에 상무를 시작으로 2000년까지 삼성그룹 전문경영인으로 활약한 기업인.
    '강진규': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%A7%84%EA%B7%9C'},  # 조선 - 조선 후기에, 성균관박사, 사헌부장령, 예조참판 등을 역임하였으며, 「영남만인소」를 지어  | Wiki: 위키미디어 동음이의어 문서
    '강진원': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%A7%84%EC%9B%90'},  # 근대 - 대한제국기 때, 의병 부대를 편성하여 여수의 원포리전투에 참전한 의병장. | Wiki: 대한민국의 관료 겸 지방자치단체장
    '강진철': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%A7%84%EC%B2%A0'},  # 현대/대한민국 - 「고려 초기의 군인전」, 「고려 토지 제도사 연구」 등을 저술한 역사학자.
    '강진해': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%A7%84%EA%B5%B0'},  # 근대 - 일제강점기 때, 만주에서 정의부 서란총관, 한국독립군 별동대장 등으로 활동하며 항일투쟁을  | Wiki: 대한민국의 행정 구역
    '강진휘': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%A7%84%EA%B5%B0'},  # 조선 - 조선 중기에, 사포서별제, 참봉, 선전관 등을 역임한 문신. | Wiki: 대한민국의 행정 구역
    '강진희': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%A7%84%ED%9D%AC'},  # 근대/개항기 | 근대/일제강점기 - 일제강점기 때, 서화미술회 교수, 서화협회 발기인 등을 역임한 서화가.
    '강징': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%A7%95_%EC%84%A0%EC%83%9D_%EB%AC%98_%EB%B0%8F_%EC%8B%A0%EB%8F%84%EB%B9%84'},  # 조선/조선 전기 - 조선 전기에, 지중추부사, 경주부윤, 예조참판 등을 역임한 문신.
    '강찬': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%B0%AC'},  # 근대 - 조선 후기에, 사헌부대사헌, 이조참판, 봉상사제조 등을 역임한 문신.
    '강창규': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%96%B4%EB%93%B1%EC%B4%88%EB%93%B1%ED%95%99%EA%B5%90'},  # 근대/일제강점기 | 현대 - 해방 이후 「건칠반」을 제작한 공예가. 건칠공예가.
    '강창제': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%B0%BD%EA%B5%90'},  # 근대/일제강점기 - 일제강점기 때, 독립신문사 기자, 임시정부 경무국장서리, 조선혁명당 중앙감찰위원 등을 역임 | Wiki: 위키미디어 동음이의어 문서
    '강철구': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%B2%A0%EA%B5%AC'},  # 근대 - 일제강점기 때, 만주에서 천영학교 교사, 북로군정서 총재비서로 활동하며 민족교육과 독립운동
    '강첨': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EB%8C%80%EC%82%AC%ED%97%8C'},  # 조선 - 조선 중기에, 병조좌랑, 이조참의, 경상도관찰사 등을 역임한 문신.
    '강춘삼': {'role': 'other'},  # 근대 - 대한제국기 때, 의병 부대를 편성하여 황해도 해주의 쟈라기벌판전투에 참전한 의병장.
    '강충': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%B6%A9'},  # 고대/남북국 - 삼국시대 때, 신라의 상사찬 등을 역임한 호족. | Wiki: 신라시대 말기의 문신, 호족
    '강치성': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EB%A7%88%EC%9D%B8_(1957%EB%85%84_%EC%98%81%ED%99%94)'},  # 조선/조선 전기 - 조선 전기에, 검열, 홍문관저작, 춘추관기사관 등을 역임한 문신. | Wiki: 대한민국의 영화
    '강태국': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%ED%83%9C%EA%B5%AD'},  # 현대/대한민국 - 해방 이후 한국성서대학교를 설립한 목사. 교육가.
    '강태동': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%9D%B4%EC%9A%B4%ED%98%95'},  # 근대/일제강점기 - 일제강점기 때, 대한민국임시정부의 내무차장과 비밀항일결사인 대동단의 단장 등으로 활동하며  | Wiki: 일제강점기의 독립운동가 (1891–1972)
    '강태성': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%84%B1%EB%AF%BC_(%EB%B0%B0%EC%9A%B0)'},  # 근대/일제강점기 - 일제강점기 때, 수원의 독립만세시위를 주도하다가 제암리 학살사건에 의해 사망한 독립운동가. | Wiki: 대한민국의 배우
    '강태수': {'role': 'novelist', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%ED%83%9C%EC%88%98'},  # 현대 - 소련에서 카자흐공화국으로 강제이주를 당하였으며, 「나의 가르노」, 「밭 갈던 아씨에게」 등 | Wiki: 대한민국의 프로게임단 지도자
    '강태홍': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%ED%83%9C%ED%99%8D'},  # 근대 - 일제강점기 때, 김창조의 제자로 조선성악연구회에서 활동한 가야금 산조 명인. | Wiki: 위키미디어 동음이의어 문서
    '강택진': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B9%80%EC%95%BD%EA%B5%AD%EC%9D%98_%EB%94%B8%EB%93%A4'},  # 근대/일제강점기 - 일제강점기 때, 조선13도총간부 교섭부장, 조선노농대회준비회 발기인 등을 역임한 사회주의  | Wiki: 박경리의 장편소설
    '강필경': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%ED%95%84'},  # 조선 - 조선 후기에, 집의, 첨지중추부사, 오위장 등을 역임한 문신. | Wiki: 위키미디어 동음이의어 문서
    '강필로': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%ED%95%84'},  # 조선 - 조선 후기에, 회양부사, 대사간, 병조참의 등을 역임한 문신. | Wiki: 위키미디어 동음이의어 문서
    '강필리': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%ED%95%84%EB%A6%AC'},  # 조선/조선 후기 - 조선 후기에, 동래부사, 승정원동부승지, 대사간 등을 역임한 문신.
    '강필방': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%84%B1%EB%8F%99%EC%9D%BC'},  # 조선/조선 후기 - 조선 후기에, 제주도에서 양재해의 반란에 가담한 호족. | Wiki: 대한민국의 배우
    '강필성': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%ED%95%84%EC%84%B1'},  # 근대 - 일제강점기 때, 풍산군수, 중추원참의, 황해도지사 등을 역임한 관료 · 친일반민족행위자.
    '강필신': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%ED%9D%94%EB%93%A4%EB%A6%AC%EC%A7%80%EB%A7%88'},  # 조선/조선 후기 - 조선 후기에, 예조좌랑, 병조좌랑, 안주현감 등을 역임한 문신.
    '강필주': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%ED%95%84%EC%A3%BC'},  # 근대/일제강점기 - 일제강점기 때, 서화미술회 교수를 역임한 화가.
    '강필효': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%9D%B4%EC%83%81%ED%98%B8_(1702%EB%85%84)'},  # 조선 - 조선 후기에, 『사유록』, 『경서고이』, 『해은유고』 등을 저술한 학자.
    '강학년': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%9D%B4%EC%B0%BD%EC%84%AD_(%EA%B0%80%EC%88%98)'},  # 조선/조선 후기 - 조선 후기에, 지평, 장령, 대사헌 등을 역임한 문신. | Wiki: 대한민국의 가수이자 비투비 멤버
    '강한수': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%ED%95%9C%EC%88%98'},  # 근대 - 일제강점기 때, 학생비밀결사 무등회를 조직하여 항일운동을 전개하다 옥사한 독립운동가. | Wiki: 위키미디어 동음이의어 문서
    '강항': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%ED%95%AD'},  # 조선 - 조선 중기에, 교서관박사, 공조좌랑, 형조좌랑 등을 역임한 문신. | Wiki: 조선 중기의 문신 (1567~1618)
    '강헌지': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EB%A9%B4%EC%A0%81%EC%88%9C_%EB%82%98%EB%9D%BC_%EB%AA%A9%EB%A1%9D'},  # 조선 - 조선 후기에, 개녕현감, 성균관전적, 춘추관기주관 등을 역임한 문신. | Wiki: 위키미디어 목록 항목
    '강현': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%ED%98%84'},  # 조선/조선 후기 - 조선 후기에, 이조참의, 예조참판, 대제학 등을 역임한 문신.
    '강형': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%ED%9A%A8%EC%9C%A8%EC%A0%81_%EC%8B%9C%EC%9E%A5_%EA%B0%80%EC%84%A4'},  # 조선/조선 전기 - 조선 전기에, 지평, 장령, 대사간 등을 역임한 문신. | Wiki: 시장에 관한 가설의 하나
    '강혜원': {'role': 'other foreigner', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%ED%98%9C%EC%9B%90'},  # 근대/일제강점기 - 일제강점기 때, 미국으로 노동 이민하여 신한부인회 총무, 대한여자애국단 초대 총단장, 흥사 | Wiki: 대한민국의 가수
    '강호': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%ED%98%B8'},  # 근대/일제강점기|현대 - 일제강점기 때, 인쇄미술 및 상업미술, 영화감독, 연극공연의 무대장치 제작 등 3개 분야에 | Wiki: 위키미디어 동음이의어 문서
    '강호문': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%ED%98%B8%EB%AC%B8'},  # 고려/고려 후기 - 고려 후기 판전교시사를 역임한 문신.
    '강호보': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%ED%98%B8%EB%B3%B4'},  # 조선/조선 후기 - 조선 후기 전적, 찰방, 지중추부사 등을 역임한 문신.
    '강혼': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%ED%98%95%EC%A1%B0'},  # 조선/조선 전기 - 조선 전기에, 우찬성, 판중추부사 등을 역임한 문신.
    '강홍대': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EC%98%81%EA%B7%A0_(%EA%B4%80%EB%A3%8C)'},  # 조선/조선 후기 - 조선 후기에, 비서원승, 중추원의관, 육군삼등군의장 등을 역임한 의관.
    '강홍립': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%ED%99%8D%EB%A6%BD'},  # 조선 후기에, 한성부우윤, 순검사, 오도원수 등을 역임한 문신. | Wiki: 조선의 문관, 군인
    '강홍식': {'role': 'novelist', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%ED%99%8D%EC%8B%9D'},  # 일제강점기 「복지만리」, 「집 없는 천사」, 「망루의 결사대」 등에 출연한 배우. 시나리오 | Wiki: 조선민주주의인민공화국의 영화인, 가수 (1902–197
    '강홍중': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%95%88%EB%82%A8%EC%B4%88%EB%93%B1%ED%95%99%EA%B5%90_(%EB%B6%80%EC%82%B0)'},  # 조선/조선 후기 - 조선 후기에, 청송부사, 동지의금부사, 성천부사 등을 역임한 문신.
    '강회계': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%ED%9A%8C%EA%B4%80%ED%99%94'},  # 고려 - 고려 후기에, 고공좌랑, 진원군 등을 역임한 문신.
    '강회백': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%ED%83%9C%EC%A1%B0_(%EC%A1%B0%EC%84%A0)'},  # 고려 - 고려 후기에, 밀직부사, 판밀직사사, 이조판서 등을 역임하였으며, 조선 건국 후에는 동북면 | Wiki: 조선의 초대 임금 (1335–1408)
    '강효동': {'role': 'other foreigner', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%84%B8%EC%A2%85'},  # 조선/조선 전기 - 조선 전기에, 중국으로부터의 채색무역문제에 관해 진언한 도화서의 화가. | Wiki: 조선의 제4대 임금 (1397–1450)
    '강효문': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%8B%A0%EC%B2%9C_%EA%B0%95%EC%94%A8'},  # 조선/조선 전기 - 조선 전기에, 예조참판, 함길도관찰사, 함길도병마절도사 등을 역임한 문신.
    '강효실': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%ED%9A%A8%EC%8B%A4'},  # 현대/대한민국 - 「죄와 벌」, 「한강은 흐른다」, 「울어도 부끄럽지 않다」 등에 출연한 배우. | Wiki: 대한민국의 배우 (1932–1996)
    '강효원': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%ED%94%BC%EB%8F%85'},  # 조선/조선 후기 - 조선 후기 병자호란 후 소현세자를 따라 심양에 간 시강원 서리.
    '강흡': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%95%84%EC%8B%9C%EC%95%84'},  # 조선/조선 후기 - 조선 후기에, 성현찰방, 산음현감 등을 역임한 문신. | Wiki: 지구에서 가장 넓고, 인구가 많은 대륙
    '강흥업': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%9D%B8%EC%B2%9C_%EC%B6%A9%EB%A0%AC%EC%82%AC'},  # 조선 - 조선 후기에, 병자호란과 관련된 무신.
    '강희맹': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%ED%9D%AC%EB%A7%B9'},  # 조선/조선 전기 - 조선 전기에, 예조정랑, 이조참의, 진헌부사 등을 역임한 문신. | Wiki: 조선 초기 문신
    '강희보': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%ED%9D%AC%EB%B3%B4'},  # 조선 - 조선 중기에, 임진왜란이 발발하자 금산전투, 진주성전투 등에 참전한 의병.
    '강희안': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%ED%9D%AC%EC%95%88'},  # 조선 - 조선 전기에, 호조참의, 황해도관찰사 등을 역임한 문신.
    '강희언': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%ED%9D%AC%EC%96%B8'},  # 조선/조선 후기 - 조선 후기에, 「인왕산도」, 「석공도」, 「사인삼경도」 등의 작품을 그린 화가. | Wiki: 조선 후기의 화가
    '강희열': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%ED%8C%8C%EC%9D%BC%EB%9F%BF_(%EC%98%81%ED%99%94)'},  # 조선 - 조선 중기에, 임진왜란이 발발하자 금산전투, 진주성전투 등에 참전한 의병. | Wiki: 2024년 김한결 감독의 영화
    '강희중': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%ED%9D%AC%EC%A4%91'},  # 현대/대한민국 - 한국전쟁 때, 경북 경주의 기계 · 안강전투에 참전한 군인.
    '강희헌': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%ED%9D%AC'},  # 근대/일제강점기 - 일제강점기, 북간도에서 활동한 민족운동가. | Wiki: 청나라의 연호
    '개로왕': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%9C%EB%A1%9C%EC%99%95'},  # 고대/삼국/백제 - 백제의 제21대(재위: 455년~475년) 왕. | Wiki: 백제의 제21대 국왕 (?~475)
    '개루왕': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%9C%EB%A3%A8%EC%99%95'},  # 고대/삼국/백제 - 백제의 제4대(재위: 128년~166년) 왕. | Wiki: 백제의 제4대 국왕 (?~166)
    '개지문': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EB%B2%84%EB%93%9C%EB%82%98%EB%AC%B4'},  # 고대/삼국 - 신라의 제29대 왕 태종 무열왕의 서자인 왕자. | Wiki: 식물의 종
    '개청': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%98%81%EC%9B%94%EA%B5%90%EB%8F%84%EC%86%8C'},  # 고대/삼국시대 - 삼국시대 때, 신라의 보현사 주지 등을 역임한 승려.
    '갱세': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%B1%EC%84%B8'},  # 고대/남북국 - 남북국시대 때, 통일신라의 급찬관등을 역임한 관리.
    '거관': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%A4%91%EC%B6%94%EC%9B%90_(%EC%A1%B0%EC%84%A0)'},  # 조선 - 조선 후기에, 설악산 신흥사로 출가하여 정업에게서 구족계를 받은 승려.
    '거도': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B1%B0%EB%8F%84'},  # 고대/삼국 - 신라 탈해이사금 때, 우시산국과 거칠산국을 병합한 장수.
    '거득공': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%83%81%EC%88%98%EB%A6%AC_%EC%A0%9C%EB%8F%84'},  # 고대/삼국 - 삼국시대 때, 신라 태종무열왕의 서자로 총재를 역임한 관리.
    '거등왕': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B1%B0%EB%93%B1%EC%99%95'},  # 고대/삼국/가야 - 금관가야의 제2대(재위: 199년~253년) 왕. | Wiki: 금관가야의 제2대 국왕 (?~253)
    '거시지': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%9E%90%EC%A0%84%EA%B1%B0'},  # 고대/남북국 - 삼국시대 때, 신라의 현령 등을 역임한 지방관. | Wiki: 일반적으로 바퀴 두 개로 구성되어 사람의 힘으로 움직일
    '거연': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%9D%B4%EA%B1%B0%EC%97%B0'},  # 근대 - 개항기 때, 남한총섭, 북한총섭 등을 역임한 승려.
    '거연당': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%9D%B4%EA%B1%B0%EC%97%B0'},  # 조선/조선 후기 - 조선 후기에, 「관동팔경도 병풍」, 「산수도 병풍」 등의 작품을 그린 화가.
    '거열랑': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B1%B0%EC%97%B4'},  # 고대/삼국 - 삼국시대 때, 신라의 「혜성가」와 관련된 화랑. | Wiki: 죄인의 사지, 머리를 말이나 소에 묶어 달리게 하여 사
    '거진': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B1%B0%EC%A7%84'},  # 고대/삼국 - 삼국시대 때, 무산성 · 감물성 · 동잠성전투에 참전한 신라의 장수.
    '거질미왕': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B1%B0%EC%A7%88%EB%AF%B8%EC%99%95'},  # 고대/삼국/가야 - 금관가야의 제4대(재위: 291년~346년) 왕. | Wiki: 금관가야의 제4대 국왕 (?~346)
    '거천': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%ED%8C%94%EA%B1%B0%EC%B2%9C'},  # 고려/고려 전기 - 고려 전기에, 경주호장을 역임한 호족.
    '거칠부': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B1%B0%EC%B9%A0%EB%B6%80'},  # 삼국시대 신라의 파진찬 · 상대등 등을 역임한 장수. | Wiki: 삼국시대 신라의 파진찬, 상대등 등을 역임한 관리. 장
    '건품': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B1%B4%ED%92%88'},  # 고대/삼국/신라 - 삼국시대 백제 무왕의 아막성 침공 당시의 신라 장수. | Wiki: 건품(乾品): 삼국시대 백제 무왕의 아막성 침공 당시의
    '걸걸중상': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B1%B8%EA%B1%B8%EC%A4%91%EC%83%81'},  # 고대/남북국/발해 - 발해의 제1대 고왕 대조영의 아버지로, 고구려 유민을 이끌고 당나라군과 싸우다 전사한 왕족 | Wiki: 고구려의 장수이자 부흥을 이끈 지도자 (629~698)
    '걸숙': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%84%9D%EA%B1%B8%EC%88%99'},  # 고대/삼국/신라 - 삼국시대, 신라의 석씨 왕족.
    '걸승': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%ED%95%98%EC%9C%A4%EA%B2%BD'},  # 고려 - 고려 후기에, 양양 낙산사의 노비. | Wiki: 대한민국의 배우
    '검군': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B2%80%EA%B5%B0'},  # 고대/삼국 - 삼국시대 때, 신라의 화랑 · 근랑의 낭도 출신으로 사량궁 사인 등을 역임한 관리. | Wiki: 신라의 관리로, 낭도 출신이자 사량궁 소속 사인
    '검모잠': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B2%80%EB%AA%A8%EC%9E%A0'},  # 고대/삼국/고구려 - 삼국시대 때, 고구려 부흥 운동을 전개한 지도자. | Wiki: 고구려의 부흥운동가 (?~670)
    '견권': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B2%AC%EA%B6%8C'},  # 고려 - 고려 전기에, 말갈과 후백제와의 전투에서 공을 세운 장수 · 공신.
    '견금': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B2%AC%EC%84%AC%EC%9C%A0'},  # 고려 - 고려 전기에, 본주의 영군장군을 역임한 호족. | Wiki: 누에 고치에서 얻은 천연 단백질 섬유
    '견등': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%A0%80%EB%A8%BC_%EC%85%B0%ED%8D%BC%EB%93%9C'},  # 고대/삼국 - 삼국시대 때, 신라의 『화엄일승성불묘의』, 『대승기신론동현장』 등을 저술한 승려. | Wiki: 독일의 견종
    '견성군': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B2%AC%EC%84%B1%EA%B5%B0'},  # 조선 - 조선의 제9대 왕, 성종의 서자인 왕자. | Wiki: 조선전기 제9대 성종의 서자인 왕자
    '견우옹': {'role': 'novelist', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EB%B6%88%ED%9B%84%EC%9D%98_%EB%AA%85%EA%B3%A1%EC%9D%98_%EC%97%90%ED%94%BC%EC%86%8C%EB%93%9C_%EB%AA%A9%EB%A1%9D'},  # 고대/남북국 - 삼국시대 때, 신라의 「헌화가」를 지은 작가. | Wiki: 위키미디어 목록 항목
    '견훤': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B2%AC%ED%9B%A4'},  # 고대/남북국 - 남북국시대 때, 후백제를 건국한 시조. | Wiki: 후백제의 초대 국왕 (867–936)
    '결응': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%98%81%EC%A3%BC_%EB%B6%80%EC%84%9D%EC%82%AC_%EC%9B%90%EC%9C%B5%EA%B5%AD%EC%82%AC%EB%B9%84'},  # 고려 - 고려 전기에, 승통, 왕사, 국사 등을 역임한 승려.
    '겸용': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%84%9C%EC%9A%B8%EA%B5%90%ED%86%B5%EA%B3%B5%EC%82%AC_4000%ED%98%B8%EB%8C%80_VVVF_%EC%A0%84%EB%8F%99%EC%B0%A8'},  # 고대/남북국 - 삼국시대 때, 신라의 태수 등을 역임한 관리. | Wiki: 수도권 전철 4호선에서 운행 중인 서울교통공사 소속 통
    '겸익': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B2%B8%EC%9D%B5'},  # 고대/삼국/백제 - 백제시대, 인도에 유학을 다녀온 승려. | Wiki: 백제의 승려
    '겸지왕': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B2%B8%EC%A7%80%EC%99%95'},  # 고대/삼국/가야 - 금관가야의 제9대(재위: 492년~521년) 왕. | Wiki: 금관가야의 제9대 국왕 (?~521)
    '경': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B2%BD'},  # 고대/삼국 - 삼국시대 때, 고구려 평양성 내 낙랑동사 주지 등을 역임한 승려. | Wiki: 위키미디어 동음이의어 문서
    '경강대왕': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EB%A0%A4_%EC%9D%98%EC%A1%B0'},  # 고려/고려 전기 - 고려의 제1대 왕, 태조 왕건의 조부인 왕족. | Wiki: 고려 태조의 할아버지
    '경구': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B2%BD%EA%B5%AC_%ED%88%AC%EC%97%AC'},  # 조선/조선 후기 - 조선 후기에, 내의원수의 · 지중추부사 등을 역임한 의관. | Wiki: 입을 통해 물질을 투여하는 경로
    '경녕군': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B2%BD%EB%85%95%EA%B5%B0'},  # 조선/조선 전기 - 조선의 제3대 왕, 태종의 서자인 왕자.
    '경대승': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B2%BD%EB%8C%80%EC%8A%B9'},  # 고려 - 고려 후기에, 교위, 사심관, 장군 등을 역임한 무신. | Wiki: 고려 중기의 장군, 독재자 (1154~1183)
    '경덕왕': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B2%BD%EB%8D%95%EC%99%95'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 제35대 왕. | Wiki: 신라의 제35대 국왕 (?~765)
    '경명군': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B2%BD%EB%AA%85%EA%B5%B0'},  # 조선 - 조선의 제9대 왕, 성종의 서자인 왕자. | Wiki: 조선 성종의 서남
    '경명왕': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B2%BD%EB%AA%85%EC%99%95'},  # 고대/남북국 - 통일신라의 제54대(재위: 917년~924년) 왕. | Wiki: 신라의 제54대 국왕 (?~924)
    '경목현비': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B2%BD%EB%AA%A9%ED%98%84%EB%B9%84'},  # 고려 - 고려 전기, 제9대 왕 덕종의 왕비. | Wiki: 고려 덕종의 왕후
    '경문왕': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B2%BD%EB%AC%B8%EC%99%95'},  # 고대/남북국/통일신라 - 통일신라의 제48대(재위: 861년~875년) 왕. | Wiki: 신라의 제48대 국왕 (?~875)
    '경보': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B2%BD%EB%B3%B4'},  # 고려 - 후백제의 견훤과 고려 초 국왕들의 공경을 받았던 승려. | Wiki: 위키미디어 동음이의어 문서
    '경복흥': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B2%BD%EB%B3%B5%ED%9D%A5'},  # 고려 - 고려 후기에, 수시중, 수성도통사, 청원부원군 등을 역임한 문신.
    '경봉': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B2%BD%EB%B4%89'},  # 현대/대한민국 - 일제강점기 통도사 불교전문강원 원장, 통도사 주지 등을 역임한 승려.
    '경빈 박씨': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B2%BD%EB%B9%88_%EB%B0%95%EC%94%A8_(%EC%A4%91%EC%A2%85)'},  # 조선/조선 전기 - 조선 전기 제11대 국왕 중종의 후궁.
    '경사만': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B2%BD%EC%82%AC_%ED%95%98%EA%B0%95%EB%B2%95'},  # 고려/고려 후기 - 고려 후기 우대언(右代言)을 역임한 충숙왕 측근 문신.
    '경산': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B2%BD%EC%82%B0'},  # 근대 - 일제강점기 때, 동래에서 범어사 주지, 임시정부 고문 등을 역임한 승려. | Wiki: 위키미디어 동음이의어 문서
    '경선': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B2%BD%EC%84%A0'},  # 현대/대한민국 - 수덕사 주지를 역임한 승려.
    '경선행': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EB%AF%B8%EC%BC%88%EB%9E%80%EC%A0%A4%EB%A1%9C_%EB%B6%80%EC%98%A4%EB%82%98%EB%A1%9C%ED%8B%B0'},  # 조선 - 조선 후기에, 『묵사집』 등을 저술한 수학자. | Wiki: 르네상스 시대 이탈리아의 예술가
    '경섬': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B2%BD%EC%84%AC'},  # 조선 - 조선 중기에, 장례원행판결사, 부제학, 호조참판 등을 역임한 문신. | Wiki: 조선의 문신
    '경성왕후': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B2%BD%EC%84%B1%EC%99%95%ED%9B%84'},  # 고려 - 고려의 제9대 왕, 덕종의 왕비. | Wiki: 고려 덕종의 왕후
    '경세인': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B2%BD%EC%84%B8%EC%9D%B8'},  # 조선/조선 전기 - 조선 전기에, 『경재유고』, 『경연강독록』 등을 저술한 문신.
    '경세창': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%B2%AD%EC%A3%BC_%EA%B2%BD%EC%94%A8'},  # 조선 - 조선 전기에, 도승지, 황해도관찰사, 호조참판 등을 역임한 문신.
    '경순': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B2%BD%EC%88%9C%EC%99%95'},  # 조선/조선 후기 - 조선 후기에, 통도사, 송광사, 해인사 등에서 선을 지도한 승려. | Wiki: 신라의 제56대 국왕 (897~978)
    '경순공주': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B2%BD%EC%88%9C%EA%B3%B5%EC%A3%BC'},  # 조선/조선 전기 - 조선의 제1대 왕, 태조의 셋째 공주. | Wiki: 조선 태조의 왕녀
    '경순왕': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B2%BD%EC%88%9C%EC%99%95'},  # 통일신라의 제56대(재위: 927년~935년) 왕. | Wiki: 신라의 제56대 국왕 (897~978)
    '경식': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B2%BD%EC%8B%9D'},  # 근대 - 개항기 때, 해인사 완허의 제자로 평신에게 선교를 배운 승려.
    '경신': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B2%BD%EC%8B%A0'},  # 조선 - 조선후기 송광사(松廣寺)의 내원선원에서 선교를 지도한 승려.
    '경신공주': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B2%BD%EC%8B%A0%EA%B3%B5%EC%A3%BC'},  # 조선/조선 전기 - 조선전기 제1대 태조의 첫째 딸인 공주. | Wiki: 조선 태조의 왕녀
    '경애왕': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B2%BD%EC%95%A0%EC%99%95'},  # 고대/남북국 - 통일신라의 제55대(재위: 924년~927년) 왕. | Wiki: 신라의 제55대 국왕 (?~927)
    '경언': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EB%82%98%EA%B2%BD%EC%96%B8'},  # 조선/조선 후기 - 조선 후기에, 가지산 보림사 당우를 신축한 건축가.
    '경연': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B2%BD%EC%97%B0'},  # 조선/조선 전기 - 조선 전기에, 사재감주부, 이산현감 등을 역임한 문신.
    '경열': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B2%BD%EC%97%B4%EB%A1%9C'},  # 조선 - 조선시대 때, 태능으로부터 선법을 계승한 승려.
    '경욱': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B2%BD%EC%9A%B1'},  # 현대/대한민국 - 일제강점기 통도사(通度寺) 혜봉의 제자로 정혜사 만공의 법맥을 계승한 승려. | Wiki: 위키미디어 동음이의어 문서
    '경운': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B2%BD%EC%9A%B4'},  # 근대 - 일제강점기 때, 조선불교선교양종교무원 교정을 역임한 승려. | Wiki: 위키미디어 동음이의어 문서
    '경원공': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B2%BD%EC%9B%90%EA%B3%B5'},  # 고려 - 고려의 제21대 왕, 희종의 셋째 왕자. | Wiki: 고려의 왕족, 희종의 셋째아들
    '경유': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B2%BD%EC%9C%A0'},  # 고대/남북국/통일신라 - 남북국시대 때, 태조의 왕사를 역임한 승려. | Wiki: 원유나 콜타르를 분류하여 얻은 기름
    '경유공': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%9D%B4%EC%83%81%ED%95%9C_%EB%B3%80%ED%98%B8%EC%82%AC_%EC%9A%B0%EC%98%81%EC%9A%B0'},  # 조선/조선 전기 - 조선 전기에, 경상도병마절도사, 첨지중추부사 등을 역임한 무신. | Wiki: 2022년 대한민국 텔레비전 시리즈
    '경응순': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%ED%83%9C%EC%9D%B8_%EA%B2%BD%EC%94%A8'},  # 조선 - 조선 중기에, 왜학통사를 역임하였으며, 임진왜란이 발발하자 왜장 고니시에게 포로로 잡혀 결
    '경의': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B2%BD%EC%9D%98'},  # 고려 - 고려 후기에, 밀직부사, 계림원수 등을 역임하였으며, 위화도회군 이후 이성계의 집권과정에서
    '경조': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B2%BD%EC%A1%B0'},  # 고려/고려 후기 - 고려 후기에, 삼중대사를 역임한 승려.
    '경종': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B2%BD%EC%A2%85_(%EC%A1%B0%EC%84%A0)'},  # 조선/조선 후기 - 조선 제20대 왕. | Wiki: 조선의 제20대 임금 (1688–1724)
    '경주': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B2%BD%EC%A3%BC%EC%8B%9C'},  # 근대 - 일제강점기 때, 명정학교 교장, 중앙불교전문학교 교장서리 등을 역임한 승려. | Wiki: 대한민국의 경상북도 시단위 행정구역
    '경준': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B2%BD%EC%A4%80'},  # 조선/조선 전기 - 조선 전기에, 좌부승지, 첨지중추부사 등을 역임한 문신. | Wiki: 조선의 문신
    '경질': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B2%BD%EC%A7%88%EC%9E%90%EA%B8%B0'},  # 고대/남북국 - 남북국시대 때, 통일신라의 봉림산파 2대조 심희의 문하생인 승려. | Wiki: 도자기의 한 종류
    '경찬': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B2%BD%EC%B0%AC'},  # 조선 - 조선 후기에, 용흥사 주지, 용흥사 수호총섭 등을 역임한 승려. | Wiki: 위키미디어 동음이의어 문서
    '경창군': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B2%BD%EC%B0%BD%EA%B5%B0'},  # 조선/조선 후기 - 조선 제14대 임금 선조의 서(庶) 9남. | Wiki: 조선 중기의 왕족, 선조의 서자
    '경창궁주': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B2%BD%EC%B0%BD%EA%B6%81%EC%A3%BC'},  # 고려 - 고려의 제24대 왕, 원종의 왕비. | Wiki: 고려 원종의 왕후
    '경최': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%B2%AD%EC%A3%BC_%EA%B2%BD%EC%94%A8'},  # 조선 - 조선 후기에, 도승지, 판결사 등을 역임한 문신.
    '경한': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B2%BD%ED%95%9C'},  # 고려 - 고려후기 신광사 주지, 흥성사 주지, 공부선 시관 등을 역임한 승려. | Wiki: 위키미디어 동음이의어 문서
    '경헌': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B9%80%EC%82%AC%EB%AA%A9'},  # 조선 - 조선시대 때, 『제월당집』을 저술한 승려. | Wiki: 조선 후기의 문신
    '경호': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B2%BD%ED%98%B8'},  # 근대 - 개항기 때, 벽송사 · 동학사 등에서 불교 경전을 깊이 연구한 승려.
    '경혼': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B2%BD%ED%98%BC'},  # 조선/조선 전기 - 조선 전기에, 홍문관부제학, 충청도관찰사, 좌부승지 등을 역임한 문신.
    '경화': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B2%BD%ED%99%94'},  # 근대 - 대한제국기 때, 부안 내소사에 선원을 개설하여 후학을 양성한 승려. | Wiki: 위키미디어 동음이의어 문서
    '경화공주': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B2%BD%ED%99%94%EA%B3%B5%EC%A3%BC'},  # 고려 - 고려, 제27대 충숙왕의 왕비. | Wiki: 고려 충숙왕의 왕후
    '경화궁부인': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B2%BD%ED%99%94%EA%B6%81%EB%B6%80%EC%9D%B8'},  # 고려 - 고려의 제4대 왕, 광종의 왕비.
    '경화왕후': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B2%BD%ED%99%94%EC%99%95%ED%9B%84'},  # 고려/고려 전기 - 고려의 제16대 왕, 예종의 왕비. | Wiki: 고려 예종의 왕후
    '경흥': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B2%BD%ED%9D%A5'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 『삼미륵경소』 · 『금광명경최승왕경약찬』 등을 저술한 승려. | Wiki: 위키미디어 동음이의어 문서
    '계강': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%A0%9C%EC%9D%B4%EC%8A%A8_%EC%9A%B0'},  # 고대/남북국 - 남북국시대 때, 통일신라의 아찬으로 시중, 상대등 등을 역임한 관리.
    '계고': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%84%EA%B3%A0'},  # 고대/삼국 - 삼국시대 신라의 제24대 진흥왕 때의 가야국의 음악가 우륵에게 가야금을 배운 신라인. | Wiki: 위키미디어 동음이의어 문서
    '계광순': {'role': 'other foreigner', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%84%EA%B4%91%EC%88%9C'},  # 현대/대한민국 - 일제강점기 때, 일본 척무성 사무관 등을 역임하였으며, 해방 이후 제 4·5대 민의원 등을 | Wiki: 일제강점기의 관료, 대한민국의 정치인
    '계국대장공주': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%84%EA%B5%AD%EB%8C%80%EC%9E%A5%EA%B3%B5%EC%A3%BC'},  # 고려/고려 후기 - 고려, 제26대 충선왕의 왕비. | Wiki: 고려 충선왕의 왕후
    '계덕해': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%84%EB%8D%95%ED%95%B4'},  # 조선 - 조선 후기에, 성균관전적, 예조좌랑 등을 역임한 문신.
    '계백': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%84%EB%B0%B1'},  # 고대/삼국/백제 - 삼국시대 때, 황산벌전투에 참전한 백제의 장수. | Wiki: 백제의 장군 (?–660)
    '계병호': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%98%81%EB%9D%BD%EC%A4%91%ED%95%99%EA%B5%90'},  # 현대/대한민국 - 일제강점기 선천YMCA 총무, 중앙YMCA 간사 및 이사 등을 역임한 사회운동가.
    '계봉우': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%84%EB%B4%89%EC%9A%B0'},  # 근대/일제강점기 - 일제강점기 때, 임시의정원, 고려공산당에서 활동하며 국외 항일운동을 전개한 역사학자 · 독 | Wiki: 한글학자, 역사학자, 독립운동가
    '계선': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%84%EC%84%A0%EB%B6%80%ED%91%9C'},  # 조선 - 조선 후기에, 대흥사 주지로 『양악문집』을 저술한 승려.
    '계수': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%84%EC%88%98'},  # 고대/삼국 - 고구려의 제8대 왕, 신대왕의 5번째 왕자. | Wiki: 변수에 일정하게 곱해진 상수
    '계아태후': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%ED%9A%A8%EA%B3%B5%EC%99%95'},  # 고대/남북국 - 신라의 제56대 왕, 경순왕의 어머니로, 경순왕 즉위 후에 왕태후로 추존된 왕족. | Wiki: 신라의 제52대 국왕 (885–912)
    '계양군': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%84%EC%96%91%EA%B5%B0'},  # 조선 - 조선의 제4대 왕, 세종의 서자인 왕자. | Wiki: 조선 세종의 서자
    '계오': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%B9%A0%EA%B0%81%EC%A7%80'},  # 조선 - 조선 후기에, 『가산집』 등을 저술한 승려.
    '계오부인': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%9B%90%EC%84%B1%EC%99%95'},  # 고대/남북국 - 신라의 제38대 왕, 원성왕의 어머니로, 원성왕 즉위 후에 소문태후로 추봉된 왕족. | Wiki: 신라의 제38대 국왕 (?–798)
    '계왕': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%84%EC%99%95'},  # 고대/삼국/백제 - 백제의 제12대(재위: 344년~346년) 왕. | Wiki: 백제의 제12대 국왕 (?~346)
    '계용묵': {'role': 'novelist', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%84%EC%9A%A9%EB%AC%B5'},  # 근대 - 일제강점기 때, 『병풍에 그린 닭이』, 『백치 아다다』 등을 저술한 소설가. | Wiki: 대한민국의 작가 (1904–1961)
    '계원': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%84%EC%9B%90'},  # 고대/삼국/신라 - 삼국시대 때, 이찬 관등에 임명된 신라의 관리.
    '계유명': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%84%EC%9C%A0%EB%AA%85%EC%82%BC%EC%A1%B4%EC%B2%9C%EB%B6%88%EB%B9%84%EC%83%81'},  # 조선 - 조선 후기에, 효행으로 선교랑 사포서별제를 제수받은 효자. | Wiki: 불상과 글이 새겨진 비석 모양의 석상
    '계응': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%86%A1%ED%95%9C%ED%95%84'},  # 고려/고려 전기 - 고려 전기에, 대각국사 의천의 화엄종을 계승한 승려.
    '계응태': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%84%EC%9D%91%ED%83%9C'},  # 현대/대한민국 - 북한에서, 당 중앙위원회 위원, 부총리 겸 무역부장, 당 중앙위원회 공안담당 비서 등을 역 | Wiki: 조선민주주의인민공화국의 정치인
    '계정': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%84%EC%A0%95'},  # 근대 - 조선 후기에, 보제, 월화 등 5대 강사로부터 경전을 배운 승려.
    '계정식': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%84%EC%A0%95%EC%8B%9D'},  # 일제강점기 때, 이화여자전문학교 음악과 과장, 조선음악회 이사 등을 역임한 지휘자 · 친일
    '계지문': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%88%98%EC%95%88_%EA%B3%84%EC%94%A8'},  # 조선 - 조선 후기에, 정묘호란이 발발하자 아들과 함께 의병을 모집하여 항쟁한 의병장.
    '계홍': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%ED%83%9C%EC%A1%B0_(%EC%A1%B0%EC%84%A0)'},  # 고대/남북국/통일신라 - 남북국시대 때, 통일신라의 아찬, 진두 등을 역임한 관리. | Wiki: 조선의 초대 임금 (1335–1408)
    '계화': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%84%ED%99%94'},  # 근대 - 일제강점기 때, 만주에서 대한군정서를 조직하여 군자금 모금활동을 전개한 독립운동가. | Wiki: 위키미디어 동음이의어 문서
    '계화부인': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%86%8C%EC%84%B1%EC%99%95'},  # 고대/남북국/통일신라 - 신라의 제39대 왕, 소성왕의 왕비. | Wiki: 신라의 제39대 국왕 (?–800)
    '계훈제': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%84%ED%9B%88%EC%A0%9C'},  # 현대 - 민족수호협의회 운영위원, 민주헌법쟁취 국민운동본부 상임공동대표 등을 역임한 사회운동가. | Wiki: 대한민국의 사회 운동가 (1921–1999)
    '고경리': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B2%BD%EB%A6%AC'},  # 조선 - 조선 중기에, 임진왜란 당시 선조를 호종하지 않았다는 이유로 곤경에 빠진 정철과 성혼을 두 | Wiki: 위키미디어 동음이의어 문서
    '고경명': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EA%B2%BD%EB%AA%85'},  # 조선 - 조선 중기에, 임진왜란이 발발하자 전라좌도 의병대장에 추대되었으며, 금산전투를 이끌다 전사 | Wiki: 조선 중기의 문신·의병장 (1533–1592)
    '고경조': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EA%B2%BD%EC%A1%B0'},  # 조선 - 조선 전기에, 해미현감, 임천군수, 광주목사 등을 역임한 문신.
    '고경허': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EA%B2%BD%EB%A9%B4'},  # 조선 - 조선 전기에, 승지, 전주부윤 등을 역임한 문신.
    '고공의': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EA%B3%B5%EC%9D%98'},  # 고대/삼국 - 삼국시대 때, 고구려 멸망 후, 유민 집단을 이끈 지도자. | Wiki: 고구려 멸망 후 고구러 유민들을 이끈 지도자
    '고광만': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EA%B4%91%EB%A7%8C'},  # 현대 - 해방 이후 문교부차관, 문교부장관 등을 역임한 관료. 교육자. | Wiki: 대한민국의 교육인, 관료 (1904–1994)
    '고광수': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EA%B4%91%EC%88%98'},  # 근대/일제강점기 - 일제강점기 고려공산청년회 책임비서를 지낸 사회주의운동가, 독립운동가. | Wiki: 재일교포 야구 선수
    '고광순': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EA%B4%91%EC%88%9C'},  # 근대 - 개항기 때, 을미사변이 일어나자 기우만과 함께 의병을 모집하여 좌도의병대장으로 활약한 의병 | Wiki: 조선 말기의 의병장
    '고광채': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%A1%B0%EC%9D%B8%EC%84%B1_(%EB%B0%B0%EC%9A%B0)'},  # 근대 - 개항기 때, 을미사변이 일어나자 고광순 의진에서 참모 겸 우익장으로 활약한 의병장. | Wiki: 대한민국의 배우
    '고광훈': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%9A%A9%ED%9D%AC'},  # 근대 - 대한제국기 때, 형 고광순 의진에서 참모부장으로 활약한 의병. | Wiki: 김정일의 네번째 배우자
    '고구': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EA%B5%AC'},  # 고대/삼국 - 삼국시대 때, 고구려 장수왕의 측근으로 활동한 장수. | Wiki: 위키미디어 동음이의어 문서
    '고국양왕': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EA%B5%AD%EC%96%91%EC%99%95'},  # 고대/삼국/고구려 - 고구려의 제18대(재위: 384년~391년) 왕. | Wiki: 고구려의 제18대 국왕 (?~391)
    '고국원왕': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EA%B5%AD%EC%9B%90%EC%99%95'},  # 고대/삼국/고구려 - 삼국시대 고구려 제16대 왕. | Wiki: 고구려의 제16대 국왕 (?~371)
    '고국천왕': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EA%B5%AD%EC%B2%9C%EC%99%95'},  # 고대/삼국/고구려 - 고구려의 제9대(재위: 179년~197년) 왕. | Wiki: 고구려의 제9대 국왕 (176~197)
    '고기승': {'role': 'other'},  # 조선 - 조선 후기에, 사간원헌납, 성균관전적 등을 역임한 문신.
    '고기준': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%9D%B4%EA%B4%91%EC%88%98_(%EB%B0%B0%EC%9A%B0)'},  # 현대/대한민국 - 해방 이후 북한의 조선기독교도연맹 서기장을 역임한 목사. | Wiki: 대한민국의 배우, 방송인
    '고길덕': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EA%B8%B8%EB%8D%95'},  # 고대/남북국 - 남북국시대 때, 발해의 대부승으로서 고려에 파견된 사신. | Wiki: 발해의 대부승으로서 고려에 파견된 사신
    '고노자': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EB%85%B8%EC%9E%90'},  # 고대/삼국/고구려 - 삼국시대 고구려 신성태수를 지낸 관리. | Wiki: 고구려의 장수
    '고달': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EB%8B%AC'},  # 고대/삼국 - 삼국시대 때, 백제의 행건위장군 광양태수 겸 장사로서 남제에 파견된 사신.
    '고대선': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%ED%95%9C%EA%B5%AD%EC%9D%98_%EC%84%A0%EA%B5%90'},  # 근대/일제강점기 - 일제강점기 때, 강원도 양양의 독립만세시위에 참여했다가 순국한 독립운동가.
    '고대수': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EB%8C%80%EC%88%98'},  # 근대/개항기 - 개항기 때, 갑신정변 당시의 궁녀. | Wiki: 《수호전》의 등장인물
    '고덕린': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/2025%EB%85%84'},  # 근대/일제강점기 - 일제강점기 때, 평안남도 대동군 금제면 원장리와 강서군 반석면 상사리 사천시장 일대의 독립 | Wiki: 연도
    '고덕무': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EB%8D%95%EB%AC%B4'},  # 고대/삼국/고구려 - 고구려 제28대 보장왕의 아들로, 요동지역의 고구려 유민을 통치한 왕자. | Wiki: 고구려의 왕자 (?~?)
    '고두환': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD_%EB%8F%85%EB%A6%BD%EC%9C%A0%EA%B3%B5%EC%9E%90'},  # 근대 - 일제강점기 때, 대한독립단에 가입하였고, 구월산대를 조직하여 군자금 모금활동 및 친일파 처
    '고득뢰': {'role': 'other'},  # 조선 - 조선 중기에, 임진왜란이 발발하자 의병장 최경회 휘하의 부장이 되었으며, 진주성전투에 참전
    '고득종': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EB%93%9D%EC%A2%85'},  # 조선/조선 전기 - 조선 전기에, 중추원부사, 동지중추원사, 한성부판윤 등을 역임한 문신.
    '고량': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EB%9F%89%EC%A3%BC'},  # 고대/삼국 - 삼국시대 때, 고구려 위두대형, 책성도독, 대상 등을 역임한 귀족.
    '고려복신': {'role': 'other foreigner', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B7%80%EC%8B%A4%EB%B3%B5%EC%8B%A0'},  # 고대/삼국 - 삼국시대 고구려 멸망 후 일본에서 여러 관직을 역임한 유민. 일본관리.
    '고련': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EB%A0%A8'},  # 고대/삼국 - 삼국시대 때, 당나라에서 안동도호 등을 역임한 장수.
    '고로': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EB%A1%9C'},  # 고대/삼국 - 삼국시대 때, 고구려와 말갈 연합의 백제 한성 침공에 가담했던 고구려의 장수. | Wiki: 고로 시작하는 단어
    '고맹영': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EB%A7%B9%EC%98%81'},  # 조선/조선 전기 - 조선 전기에, 사헌부지평, 옥천군수, 호조참의 등을 역임한 문신. | Wiki: 조선 중기의 문신, 관료 (1502–1565)
    '고명달': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%ED%8F%89%EC%96%91%EB%83%89%EB%A9%B4'},  # 현대/대한민국 - 해방 이후 「양주별산대놀이」의 전승자로 지정된 예능보유자. | Wiki: 평양시의 향토 음식
    '고명자': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%9D%B4%ED%98%9C%EB%A6%AC_(1967%EB%85%84)'},  # 근대/일제강점기 - 해방 이후 조선부녀총동맹 총무부위원, 근로인민당 중앙위원으로 활동한 사회주의운동가. 독립운 | Wiki: 대한민국의 가수 (1967년)
    '고모한': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EB%AA%A8%ED%95%9C'},  # 고대/남북국/발해 - 고려 전기에, 요나라에서 개부의동삼사, 중대성좌상 등을 역임한 발해의 유민.
    '고무': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EB%AC%B4'},  # 고대/삼국 - 고구려의 제15대 왕, 미천왕의 아들인 왕자.
    '고문간': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EB%AC%B8%EA%B0%84'},  # 고대/삼국 - 삼국시대 때, 고구려 멸망 후 몽고고원의 돌궐로 이주한 유민. | Wiki: 고구려가 멸망하자 돌궐과 당나라로 이주한 유민
    '고병간': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EB%B3%91%EA%B0%84'},  # 근대/일제강점기|현대 - 세브란스의학전문학교 교수, 연세대학교 총장, 세브란스병원 원장 등을 역임한 의사.
    '고병국': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EB%B3%91%EA%B5%AD'},  # 현대 - 헌법제정 전문위원, 법전편찬위원회 위원 등을 역임한 법학자. | Wiki: 대한민국의 법학자 (1909–1976)
    '고병익': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EB%B3%91%EC%9D%B5'},  # 현대/대한민국 - 해방 이후 『완전 동양사』, 『아시아의 역사상』, 『동아교섭사의 연구』 등을 저술한 학자. | Wiki: 대한민국의 역사가 (1924–2004)
    '고병희': {'role': 'other foreigner', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EB%B3%91%ED%9D%AC_(%EA%B0%80%EC%88%98)'},  # 근대 - 일제강점기 때, 일본에서 흑우회에 가입해 활동하다가 귀향하여 독서회를 조직한 독립운동가.
    '고보원': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EB%B3%B4%EC%9B%90'},  # 고대/삼국/고구려 - 고구려의 제28대 보장왕의 손자로, 좌응양위 대장군에 임명된 왕족. | Wiki: 고구려의 왕족
    '고보준': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EB%B3%B4%EC%A4%80'},  # 고려 - 고려 전기에, 이자겸 일파를 제거하려다 실패한 관리. | Wiki: 고려의 관료이다
    '고복남': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EB%B3%B5%EB%82%A8'},  # 고대/삼국/고구려 - 고구려 시대 보장왕의 태자. | Wiki: 위키미디어 동음이의어 문서
    '고복수': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EB%B3%B5%EC%88%98'},  # 근대 - 일제강점기 때, 「타향살이」, 「짝사랑」, 「사막의 한」 등을 부른 가수. | Wiki: 대한민국의 가수 (1911–1972)
    '고복장': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EB%B3%B5%EC%9E%A5'},  # 고대/삼국 - 삼국시대 때, 고구려 우보 등을 역임한 관리. | Wiki: 고구려의 관리
    '고봉': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%B6%A9%EB%8B%AC'},  # 근대 | 현대 - 해인사, 은해사 등에서 강사로 후학을 지도한 승려.
    '고봉기': {'role': 'other foreigner', 'wikipedia': 'https://ko.wikipedia.org/wiki/6%EC%9B%94_%EB%B4%89%EA%B8%B0'},  # 현대/대한민국 - 일제강점기 때, 중국으로 건너가 항일투쟁을 벌였으며, 해방 이후 북한에서, 중앙당 기요과장
    '고봉례': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EB%B4%89%EB%A1%80'},  # 조선 - 조선 전기에, 우군동지총제, 제주안무사 등을 역임한 무신. | Wiki: 조선 초기의 무신
    '고부천': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EB%B6%80%EC%B2%9C'},  # 조선 - 조선 후기에, 교서관정자, 지제교, 사헌부장령 등을 역임한 문신.
    '고비': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EB%B9%84_%EC%82%AC%EB%A7%89'},  # 고대/남북국/후백제|고려/고려 전기 - 후백제의 제1대 왕, 견훤의 후궁으로, 견훤의 첫째 아들 신검에 의해 금산사에 유폐되었을  | Wiki: 중국 북부의 내몽골 자치구에서 몽골에 걸쳐 펼쳐지는 사
    '고사경': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%9C%EC%84%B1_%EA%B3%A0%EC%94%A8'},  # 조선 - 조선 전기에, 동지중추부사 등을 역임하였으며, 『대명률직해』를 저술한 학자. | Wiki: 한국의 성씨 중 하나
    '고사계': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%82%AC%EA%B3%84'},  # 고대/삼국 - 남북국시대 때, 당나라에서 사진교장을 역임한 장수.
    '고사훈': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%82%AC%ED%9B%88'},  # 근대 - 대한제국기 때, 김석윤 대장의 참모 및 모병책으로 활약하며 항일의병투쟁을 전개한 의병.
    '고상돈': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%83%81%EB%8F%88'},  # 현대 - 한국에서 최초로 에베레스트산을 등정한 산악인. | Wiki: 대한민국의 산악인 (1948–1979)
    '고상안': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%9C%EC%84%B1_%EA%B3%A0%EC%94%A8'},  # 조선 - 조선 중기에, 함창현감, 풍기군수 등을 역임하였으며, 임진왜란이 발발하자 함창에서 의병 대 | Wiki: 한국의 성씨 중 하나
    '고석': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%84%9D'},  # 근대/일제강점기 - 일제강점기 「정오의 우사」 · 「정원」 · 「모자」 등을 그린 화가. 유화가. | Wiki: 위키미디어 동음이의어
    '고석규': {'role': 'poet critic', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%84%9D%EA%B7%9C'},  # 현대/대한민국 - 「윤동주의 정신적 소묘」, 「비평가의 교양」, 「현대시의 형이상성」 등을 저술한 시인 · 
    '고석진': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%84%9D%EC%A7%84'},  # 근대/대한제국기 - 대한제국기 때, 최익현의 태인의거에 참모로서 가담하였으며, 임병찬 의진에서 참모관으로 활약
    '고선지': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%84%A0%EC%A7%80'},  # 고대/삼국 - 남북국시대 때, 당나라에서 사진절도사, 안서절도사 등을 역임한 장수. | Wiki: 고구려 유민의 후손으로 당나라의 장군
    '고설봉': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%84%A4%EB%B4%89'},  # 현대 - 해방 이후 「여명」 · 「사랑의 가족」 등에 출연한 배우. | Wiki: 대한민국의 배우 (1913–2001)
    '고성겸': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EB%82%A8_(%EC%84%B1%EC%94%A8)'},  # 조선 - 조선 후기에, 「한성악부」, 『녹리문집』 등을 저술한 학자. | Wiki: 성씨
    '고성후': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%9C%A0%ED%92%8D_(%EA%B3%A0%EC%84%B1%ED%9B%84)'},  # 조선/조선 전기 - 조선 전기에, 감찰, 군수, 예조참의 등을 역임한 문신.
    '고세': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%BD%94%EC%84%B8'},  # 고려 - 고려 후기에, 판밀직사사, 자의밀직사사, 도첨의참리 등을 역임한 무신. | Wiki: 일본의 화장품 기업
    '고세보': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%B5%9C%EC%84%B8%EB%B3%B4'},  # 조선/조선 전기 - 조선 전기에, 자헌, 중추부 2품직 등을 역임한 의관.
    '고수': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%88%98'},  # 고대/삼국 - 삼국시대 때, 위사좌평 등을 역임한 백제의 관리. | Wiki: 위키미디어 동음이의어 문서
    '고수겸': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%A0%95%EA%B5%AD%EA%B3%B5%EC%8B%A0'},  # 고려/고려 후기 - 고려후기 최우암살미수사건과 관련된 관리. 무신.
    '고수관': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%88%98%EA%B4%80'},  # 조선 - 조선 후기에, 더늠 「자진사랑가」를 지은 판소리 명창. | Wiki: 조선 후기의 판소리 명창
    '고숙수': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EB%8C%80%EB%A0%B9%EC%88%99%EC%88%98'},  # 고대/삼국 - 삼국시대 때, 당나라에서 조청대부심택령 등을 역임한 관리. | Wiki: 조선시대 궁중의 남자 조리사
    '고순': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%88%9C'},  # 고대/삼국/신라 - 삼국시대 때, 고구려 옹산성 침공에 가담한 신라의 장수.
    '고순흠': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%B2%AD%EC%B6%98%EC%9B%94%EB%8B%B4'},  # 근대/일제강점기 - 일제강점기 때, 조선일보 사카이지국장, 재일거류민단 제2대 단장 등을 역임한 노동운동가. | Wiki: 드라마 2023
    '고숭덕': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%88%AD%EB%8D%95%EC%A0%9C'},  # 고대/삼국 - 삼국시대 때, 당나라에서 좌표도위익부랑장 등을 역임한 무신. | Wiki: 청나라의 제2대 황제
    '고승': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%8A%B9'},  # 고대/삼국/고구려 - 고구려 영양왕대의 장군. | Wiki: 위키미디어 동음이의어 문서
    '고승제': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%8A%B9%EC%A0%9C'},  # 현대 - 『경제학입문』, 『한국경제론』, 『한국사회 경제사론』 등을 저술한 경제학자 · 친일반민족행 | Wiki: 대한민국의 경제학자 (1917–1995)
    '고시복': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%8B%9C%EB%B3%B5'},  # 근대 - 일제강점기 때, 한인애국단 비밀단원, 한국광복군 총사령부 전령 장교, 임시정부 내무부 총무
    '고시언': {'role': 'poet', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%8B%9C%EC%96%B8'},  # 조선 - 조선 후기에, 『소대풍요』, 『성재집』 등을 저술한 시인. | Wiki: 조선의 시인·역관
    '고식': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/GOSICK_-%EA%B3%A0%EC%8B%9D-'},  # 고대/삼국 - 삼국시대 때, 막리지 등을 역임한 고구려의 관리. | Wiki: 일본 라이트 노벨 시리즈
    '고안무': {'role': 'scholar foreigner', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%95%88%EB%AC%B4'},  # 고대/삼국 - 삼국시대 때, 오경박사로서 일본에 파견된 백제의 학자. | Wiki: 삼국시대 백제에서 일본에 건너가 문화전파에 공헌한 학자
    '고앙주': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%95%99%EC%A3%BC'},  # 근대/일제강점기 - 일제강점기 때, 경상남도 창원의 삼진 만세운동에 참여했다가 순국한 독립운동가.
    '고약해': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%95%BD'},  # 조선/조선 전기 - 조선 전기에, 형조참판, 개성부유수 등을 역임한 문신. | Wiki: 의약품의 종류
    '고언백': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%96%B8%EB%B0%B1'},  # 조선/조선 후기 - 조선 후기에, 경상좌도병마사, 경기방어사 등을 역임한 무신. | Wiki: 조선 중기의 무신
    '고여': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%97%AC'},  # 고려/고려 후기 - 고려 후기에, 이성계의 휘하 산원으로 활동하였으며, 이방원의 명으로 정몽주를 격살하고 이성
    '고여림': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%97%AC%EB%A6%BC'},  # 고려 - 고려 후기에, 야별초지유, 장군 등을 역임한 무신. | Wiki: 고려 후기의 무신
    '고연무': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%97%B0%EB%AC%B4'},  # 고대/삼국/고구려 - 고구려 말기의 장군. | Wiki: 고구려 말기의 군인으로 고구려 부흥 운동을 전개했던 인
    '고연수': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%97%B0%EC%88%98'},  # 고대/삼국 - 삼국시대 때, 고구려 안시성전투에 참전한 장수. | Wiki: 고구려 말의 관리
    '고연휘': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%A0%9C%ED%9C%98'},  # 고려/고려 후기 - 고려 후기에, 「동경산수도」, 「하경산수도」 등의 작품을 그린 화가.
    '고열': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EB%B0%9C%EC%97%B4'},  # 고려/고려 전기 - 고려 전기에, 중대광, 섭병부상서, 수사공상서좌복야 등을 역임한 무신. | Wiki: 정상 체온인 36.5~37.5°C 이상으로 체온이 올라
    '고영근': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%98%81%EA%B7%BC'},  # 근대/개항기 - 개항기 때, 만민공동회와 독립협회에서 활동하며 정부에게 개혁을 요구하는 개혁개방운동을 전개 | Wiki: 대한제국의 군인이자, 개화파 정치인 (1853–1923
    '고영기': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%98%81%EA%B8%B0'},  # 고려/고려 전기 - 고려 전기에, 감찰어사, 중군판관, 호부원외랑 등을 역임한 무신. | Wiki: 재일 한국인 2세 언론인
    '고영문': {'role': 'other'},  # 근대 - 조선 후기에, 고종에게 「시무7조」 상소문을 올린 개화사상가.
    '고영부': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%98%81%EB%B6%80'},  # 고려 - 고려 전기에, 위위소경, 보문각직각, 어사중승 등을 역임한 문신. | Wiki: 위키미디어 동음이의어 문서
    '고영석': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EB%8B%B9%EC%A7%84%EA%B5%B0_(1988%EB%85%84_%EC%84%A0%EA%B1%B0%EA%B5%AC)'},  # 근대/개항기 - 김옥균의 상노로 갑신정변 당시 통신 및 정찰 임무를 수행하였던 개화당원. | Wiki: 대한민국의 옛 국회의원 선거구(1988~2012)
    '고영신': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%ED%95%9C%EA%B5%AD%EB%B0%A9%EC%86%A1%EA%B3%B5%EC%82%AC'},  # 고려/고려 전기 - 고려 전기에, 서북면병마사, 이부상서지추밀원사, 검교사공참지정사 등을 역임한 문신. | Wiki: 대한민국의 지상파 방송사
    '고영중': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%98%81%EC%A4%91'},  # 고려/고려 후기 - 고려 후기 무신집권기에 활동한 문신 관료로 은퇴한 후 해동기로회를 결성하여 활동한 인물. | Wiki: 고려의 문신
    '고영창': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%98%81%EC%B0%BD'},  # 고려/고려 전기 - 고려 전기, 요나라에서 발해 광복운동을 벌인 발해의 유민.
    '고영철': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%A3%BC%EC%9B%90'},  # 근대/일제강점기 - 개항기 때, 통리아문박문국 주사를 역임한 언론인. | Wiki: 대한민국의 배우
    '고영희': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%98%81%ED%9D%AC'},  # 근대/개항기 | 근대/일제강점기 - 일제강점기 때, 주일 특명전권공사, 탁지부 대신 등을 역임한 관료 · 친일반민족행위자. | Wiki: 위키미디어 동음이의어 문서
    '고예진': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%ED%91%9C%EC%98%88%EC%A7%84'},  # 근대 - 일제강점기 때, 의병 및 독립의군부 총무국 서기관으로 활동하며 항일운동을 전개하였고, 파리 | Wiki: 대한민국의 배우
    '고왕': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%99%95'},  # 고대/남북국/발해 - 발해의 제1대(재위: 698년~719년) 왕. | Wiki: 발해의 초대 국왕 (?–719)
    '고욕': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%9A%95'},  # 고대/남북국/발해 - 남북국시대 거란의 요주에서 발해부흥운동을 일으키고 스스로 대왕이라 칭한 발해의 유민.
    '고용보': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%9A%A9%EB%B3%B4'},  # 고려/고려 후기 - 고려 후기 원나라 황실에서 활동한 고려 출신 환관. | Wiki: 고려 후기의 환관
    '고용지': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%9A%A9%EC%A7%80%EB%8F%99'},  # 고려 - 고려 후기에, 도지병마사, 남로착적병마사, 공부상서 등을 역임한 무신.
    '고용진': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%9A%A9%EC%A7%84'},  # 근대 - 일제강점기 때, 의병 및 독립의군부 회계총관으로 활동하며 항일운동을 전개하였고, 파리장서 
    '고용현': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%9A%A9%ED%98%84'},  # 고려 - 고려 후기에, 대사성, 개성윤, 전라도진변사 등을 역임한 문신.
    '고용후': {'role': 'novelist', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%9A%A9'},  # 조선/조선 후기 - 조선 후기의 문인. | Wiki: 고용주가 노무에 대하여 보수를 근로자에게 지급할 것을 
    '고우루': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%9A%B0%EB%A3%A8'},  # 고대/삼국 - 삼국시대 때, 고구려의 을파소에 이어 죽을 때까지 국상을 역임한 관리. | Wiki: 고구려의 관료 (?–230)
    '고우영': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%9A%B0%EC%98%81'},  # 현대/대한민국 - 1970~1980년대 스포츠신문 지면을 통해 성인을 위한 만화를 연재한 만화가.
    '고운': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%9A%B4'},  # 조선/조선 전기 - 조선 전기에, 「백액대호」를 그린 화가. | Wiki: 위키미디어 동음이의어 문서
    '고원증': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%9B%90%EC%A6%9D'},  # 현대/대한민국 - 해방 이후 중앙고등군법회의 재판장, 서울지구 계엄민사부장, 법무차감 등을 역임한 군인. 관
    '고원훈': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%9B%90%ED%9B%88'},  # 근대 - 일제강점기 때, 보성전문학교 교수, 조선체육회 초대 이사장, 중추원 참의 등을 역임한 관료 | Wiki: 일제 강점기의 관료이며 기업인
    '고유': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%9C%A0'},  # 조선/조선 후기 - 조선 후기에, 승지, 안주목사 등을 역임한 문신. | Wiki: 중국 후한 말기 ~ 조위의 관료, 자는 문혜(文惠)
    '고유방': {'role': 'other'},  # 고려/고려 후기 - 고려의 제19대 왕, 명종의 총애를 받았던 도화원의 화가.
    '고유섭': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%9C%A0%EC%84%AD'},  # 근대 - 일제강점기 때, 『조선회화집성』, 『조선탑파의 연구』, 『한국미술문화사논총』 등을 저술한  | Wiki: 일제강점기의 미술 사학자
    '고윤식': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%9C%A4%EC%8B%9D'},  # 조선 - 조선 후기에, 「문심경」, 『태려문집』 등을 저술한 학자. | Wiki: 대한민국의 정치인, 경제학자 (1939–2023)
    '고을나': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%9D%84%EB%82%98'},  # 고대/초기국가 - 초기국가시대 때, 탐라국의 삼성혈 신화에 전해지는 건국 시조. | Wiki: 삼성혈 신화에 등장하는 탐라국 3시조신 중 하나
    '고응관': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EB%AA%A8%EB%82%98%EB%A6%AC%EC%9E%90'},  # 조선 - 조선 후기에, 예조좌랑, 사헌부장령 등을 역임한 문신. | Wiki: 16세기 르네상스 시대에 레오나르도 다 빈치가 그린 초
    '고응량': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%81%EC%9A%B4%EB%8F%99%EB%9F%89'},  # 조선/조선 후기 - 조선 후기에, 발생한 이인좌의 난과 관련된 관리. | Wiki: 어떤 원점에 대해 선운동량이 돌고 있는 정도를 나타내는
    '고응척': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EB%82%99%EB%B4%89%EC%84%9C%EC%9B%90'},  # 조선 - 조선 중기에, 함흥교수, 풍기군수, 회덕현감, 경주부윤 등을 역임하였으며, 「임인제야시」,
    '고의화': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%9D%98%ED%99%94'},  # 고려 - 고려 전기에, 수사공 상서좌복야 판병부사, 위사공신 등을 역임한 무신 · 공신. | Wiki: 고려의 무신
    '고이만년': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%9D%B4%EB%A7%8C%EB%85%84'},  # 고대/삼국 - 삼국시대 때, 고구려 장수왕이 감행한 백제 침공에서 공을 세운 장수. | Wiki: 삼국시대 고구려 장수왕의 백제 침공 당시의 장수
    '고이왕': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%9D%B4%EC%99%95'},  # 백제의 제8대(재위: 234년~286년) 왕. | Wiki: 백제의 제8대 국왕 (?–286)
    '고익': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%9D%B5'},  # 고대/삼국 - 삼국시대 때, 고구려 장사 등을 역임하며 동진에 사신으로 파견된 관리. | Wiki: 위키미디어 동음이의어 문서
    '고익진': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%82%BC%EB%A1%A0%EC%A2%85'},  # 현대/대한민국 - 동국대학교 불교학과 교수, 한국불교전서 편찬실장 등을 역임하였으며, 『한역불교근본경전』, 
    '고인계': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%88%98%EC%9B%90%EC%8B%9C'},  # 조선/조선 후기 - 조선 후기에, 형조정랑, 충청도도사, 예안현감 등을 역임한 문신. | Wiki: 대한민국 경기도의 도청 소재지이자 특례시
    '고인단': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%9D%B4%EC%9E%AC%EC%9A%A9'},  # 고려 - 고려후기 탐라 성주, 총관행서부사 등을 역임한 인물. | Wiki: 대한민국의 기업인
    '고인덕': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%9D%B8%EB%8D%95'},  # 근대 - 일제강점기 때, 만주에서 의열단을 조직하여 항일무장투쟁을 벌이다가 체포되어 옥사한 독립운동
    '고인재': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%B8%A1%EC%B2%9C%EB%AC%B4%ED%9B%84'},  # 근대 - 일제강점기 때, 경기도 안성군 원곡면과 양성면 일대의 독립만세시위에 참여한 독립운동가. | Wiki: 당 고종의 황후이자 무주의 여제
    '고인후': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%9D%B8%ED%9B%84'},  # 조선/조선 전기 - 조선 전기에, 승문원정자, 예조참의 등을 역임한 문신. | Wiki: 조선 중기의 문신, 의병장 (1561–1592)
    '고임무': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%9E%84%EB%AC%B4'},  # 고대/삼국/고구려 - 삼국시대 고구려의 제28대 보장왕의 둘째 아들인 왕자. | Wiki: 고구려 보장왕의 둘째 아들이자, 고구려의 막리지이다
    '고자': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%9E%90'},  # 고대/삼국 - 삼국시대 때, 당나라에서 장무장군 등을 역임한 장수. | Wiki: 위키미디어 동음이의어 문서
    '고장환': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%9E%A5%ED%99%98'},  # 근대/일제강점기 - 일제강점기 때, 조선소년연맹 중앙집행위원을 역임한 소년 운동가. | Wiki: 대한민국의 희극인
    '고재욱': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%9E%AC%EC%9A%B1'},  # 근대 - 한국신문연구소 이사장, 국제신문협회 한국위원장 등을 역임한 언론인. | Wiki: 대한민국의 축구 지도자
    '고재필': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%9E%AC%ED%95%84'},  # 현대/대한민국 - 일제강점기 때, 만주국 국무원 총무청 고등관 시보 등을 역임하였으며 해방 이후, 국방부 비 | Wiki: 대한민국의 정치인 (1913–2005)
    '고재호': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%9E%AC%ED%98%B8'},  # 현대 - 대구고등법원장, 대법관 등을 역임한 법조인. | Wiki: 위키미디어 동음이의어 문서
    '고적': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%84%B8%EC%A2%85%EC%8B%A4%EB%A1%9D_%EC%A7%80%EB%A6%AC%EC%A7%80'},  # 고려 - 고려 후기에, 유총관을 역임한 문신.
    '고정봉': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%A0%95%EB%B4%89'},  # 조선/조선 후기 - 조선 후기 홍문관교리, 돈녕부도정 등을 지낸 문신.
    '고정사': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%A0%95%EA%B4%80%EB%85%90'},  # 고대/남북국/발해 - 남북국시대 후발해의 사신으로 후당에 입조하여 관직을 받은 발해의 유민. | Wiki: 상황이 바뀌어도 당사자가 그 생각 또는 관념을 수정하지
    '고정옥': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%98%A5%EC%9E%90%EC%97%B0'},  # 근대/일제강점기 - 서울대학교 사범대학 교수를 재임하며 우리어문학회 회원으로 활동하였고, 『조선민요연구』, 『 | Wiki: 대한민국의 배우 (1988)
    '고정의': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%A0%95%EC%9D%98'},  # 고대/삼국 - 삼국시대 때, 여당전쟁 시기 고구려의 관직인 대로 등을 역임한 관리. | Wiki: 고구려의 관료 (?–?)
    '고정훈': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%A0%95%ED%9B%88'},  # 현대/대한민국 - 광복 이후 육군본부 정보국차장, 조선일보 논설위원 등을 역임한 정치인. 언론인. | Wiki: 위키미디어 동음이의어 문서
    '고정희': {'role': 'poet', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%A0%95%ED%9D%AC'},  # 현대 - 해방 이후 『지리산의 봄』, 『저 무덤에 푸른 잔디』, 『아름다운 사람 하나』 등을 저술한 | Wiki: 대한민국의 시인 (1948–1991)
    '고제남': {'role': 'other foreigner', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%A7%80%EB%82%9C%EC%8B%9C'},  # 근대 - 대한제국기 때, 전남 장성에서 창의포고문을 살포하고 정읍에서 일본군을 습격하는 등 항일의병 | Wiki: 중국 산둥성의 성도
    '고제덕': {'role': 'other foreigner', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%A0%9C%EB%8D%95'},  # 고대/남북국 - 남북국시대 때, 발해의 수령이자 일본에 사신으로 파견된 관리. | Wiki: 발해의 관료 (?–?)
    '고제량': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD_%EB%8F%85%EB%A6%BD%EC%9C%A0%EA%B3%B5%EC%9E%90'},  # 근대 - 대한제국기 때, 고광순 의진에서 부장으로 활동한 의병.
    '고제신': {'role': 'other foreigner', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%A0%9C%EC%8B%A0'},  # 근대 - 일제강점기 때, 일본 고관 총살단을 조직하였으나 실행에 실패하고, 임시정부에 조달할 군자금 | Wiki: 상나라의 제31대 왕으로 마지막 군주
    '고조기': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%A1%B0%EA%B8%B0'},  # 고려 - 고려 전기에, 서북면병마판사, 상서좌복야, 중서시랑평장사 등을 역임한 문신. | Wiki: 고려전기 서북면병마판사, 상서좌복야, 중서시랑평장사 등
    '고조다': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%A1%B0%EB%8B%A4'},  # 고대/삼국 - 고구려의 제20대 왕, 장수왕의 아들인 왕자. | Wiki: 고구려의 태자이자 장수왕의 장남
    '고종': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%A2%85_(%EB%8C%80%ED%95%9C%EC%A0%9C%EA%B5%AD)'},  # 근대/개항기|근대/대한제국기 - 조선의 제26대(재위: 1863년~1907년) 왕. | Wiki: 조선의 제26대 임금, 대한제국의 초대 황제 (1852
    '고종수': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%A2%85%EC%88%98'},  # 고려 - 고려 후기에, 왕경등처관군만호부만호, 삼주호부 등을 역임한 무신. | Wiki: 대한민국의 축구 지도자
    '고종후': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%A2%85%ED%9B%84'},  # 조선 - 조선 중기에, 감찰, 예조좌랑, 임피현령 등을 역임한 문신. | Wiki: 임진왜란 당시의 의병장
    '고주옥': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%A3%BC%EC%98%A5'},  # 현대/대한민국 - 남해안별신굿의 기예능보유자인 무녀. | Wiki: 위키미디어 동음이의어 문서
    '고죽리': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%A3%BD%EB%A6%AC'},  # 고대/삼국 - 삼국시대 때, 고구려의 안시성전투 당시, 연개소문에 의해 보내진 첩자. | Wiki: 위키미디어 동음이의어 문서
    '고준택': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%A1%B0%EC%84%A0%EB%AF%BC%EC%A3%BC%EC%A3%BC%EC%9D%98%EC%9D%B8%EB%AF%BC%EA%B3%B5%ED%99%94%EA%B5%AD_%EB%A6%BC%EC%97%85%EC%84%B1'},  # 현대/대한민국 - 일제강점기 때, 반일투쟁 혐의로 약 7년여간 복역하었으며, 해방 이후 북한에서, 최고인민회
    '고지연': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%ED%95%9C%ED%95%9C%EB%A0%B9'},  # 조선 - 조선 후기에, 『주암집』 등을 저술한 학자. | Wiki: 중국인들이 한국과 관련된 한류 컨텐츠를 제한하는 것 외
    '고지형': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%A7%80%ED%98%95%ED%95%99'},  # 근대/일제강점기 - 일제강점기 때, 평안남도 대동군 금제면 원장리와 강서군 반석면 상사리 사천시장 일대의 독립 | Wiki: 자연지리학 및 지구과학의 한 분야
    '고진': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%A7%84'},  # 고대/남북국 - 삼국시대 때, 당나라에 귀화한 고구려의 왕족.
    '고진상': {'role': 'other'},  # 고대/남북국 - 고려 전기에, 고려로 귀화한 발해제군판관 출신의 발해 유민.
    '고진승': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%A7%84%EC%8A%B9'},  # 조선/조선 후기 | 근대/개항기 - 조선후기 도화서 화원으로 헌종의 국장도감 등에 참여한 화가.
    '고질': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%A7%88'},  # 고대/삼국/고구려 - 고구려 말기와 멸망 이후, 고구려 유민 출신으로 당나라에서 주로 활동한 무관.
    '고찬보': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/5%EC%B1%84%EB%84%90'},  # 근대 - 남조선신민당 중앙위원회 선전부장, 남조선노동당 중앙상무위원 등을 역임한 사회주의 운동가. | Wiki: 일본의 익명 커뮤니티 사이트
    '고찬익': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%8B%A0%EC%B0%AC%EC%9D%B5'},  # 근대/개항기 - 대한제국기 연동교회 초대 장로, 장로회공의회 전도위원 등으로 활동한 개신교인. 사회운동가.
    '고창일': {'role': 'other foreigner', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%B0%BD%EC%9D%BC'},  # 근대/일제강점기 - 일제강점기 때, 대한국민의회 대표로서 파리강화회의에 파견되었으며, 중국 하얼빈에서 독립운동 | Wiki: 대한민국 외무부 차관 겸 장관 직무대행 서리 직을 지낸
    '고채주': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%B1%84%EC%A3%BC'},  # 근대 - 일제강점기 때, 경상남도 통영 부도정시장의 독립만세시위를 주도한 독립운동가.
    '고천백': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%B8%A1%EC%B2%9C%EB%AC%B4%ED%9B%84'},  # 고려/고려 후기 - 고려 후기에, 장군, 하정사 등을 역임한 무신. | Wiki: 당 고종의 황후이자 무주의 여제
    '고추안': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%B6%94%EC%95%88'},  # 고대/삼국 - 고구려의 제7대 왕, 차대왕의 태자인 왕자.
    '고춘자': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%B6%98%EC%9E%90'},  # 현대 - 백민악극단, 태평양가극단, 백조가극단 등에서 활동한 연극인.
    '고타소랑': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%ED%83%80%EC%86%8C%EB%9E%91'},  # 고대/삼국/신라 - 신라의 제29대 태종 무열왕의 딸로, 백제의 대야성전투에서 살해된 왕족. | Wiki: 신라의 공주 (?–642)
    '고태문': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%ED%83%9C%EB%AC%B8'},  # 현대 - 한국전쟁 때, 소대장, 중대장 등을 역임한 군인. | Wiki: 대한민국의 군인
    '고태필': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%A0%9C%EC%A3%BC_%EA%B3%A0%EC%94%A8'},  # 조선/조선 전기 - 조선 전기에, 한성부좌윤, 유수 등을 역임한 문신. | Wiki: 제주도를 본관으로 하는 한국의 성씨
    '고판례': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%ED%8C%90%EB%A1%80'},  # 현대/대한민국 - 일제강점기 증산교 최초의 교파인 선도교를 창립한 종교창시자. | Wiki: 한국의 종교인 (1980–1935)
    '고평': {'role': 'other foreigner', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B9%8C%EC%98%A4%EB%B0%A9'},  # 근대/일제강점기 - 대한제국기 검사를 지냈으나, 일제강점기 중국으로 망명하여 광복단, 대한국민회 등에서 활동한 | Wiki: 까오방성의 행정 구역
    '고한승': {'role': 'childrenauthor', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%ED%95%9C%EC%8A%B9'},  # 근대/일제강점기 - 일제강점기 때, 희곡 「장구한 밤」 등을 저술한 연극인 · 아동문학가.
    '고한우': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%ED%95%9C%EC%9A%B0'},  # 고려/고려 후기 - 고려후기 대호군, 찰방사 등을 역임한 관리. 무신.
    '고현': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%ED%98%84'},  # 조선 - 조선 중기에, 성주판관을 역임하던 중 임진왜란이 발발하자 도피하여 탄핵당하였으나, 의주까지 | Wiki: 위키미디어 동음이의어 문서
    '고형림': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%83%B4%ED%91%B8'},  # 근대 - 일제강점기 때, 만주에서 사진관을 경영하다가 광복군 제5지대에 입대하여 항일투쟁을 전개한  | Wiki: 머리카락과 두피 — 계면활성제의 액체 비누
    '고형산': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%ED%98%95%EC%82%B0'},  # 조선/조선 전기 - 조선 전기에, 우찬성, 강원도관찰사 등을 역임한 문신. | Wiki: 조선 전기의 훈구파 문신
    '고혜진': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%ED%98%9C%EC%A7%84'},  # 고대/삼국 - 삼국시대 때, 고구려 안시성전투에 참전한 장수.
    '고홍건': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%ED%99%8D%EA%B1%B4'},  # 조선 - 조선시대 때, 오위도총부도총관, 지중추부사 등을 역임한 무신. | Wiki: 고홍건(高弘建): 조선시대 오위도총부도총관, 지중추부사
    '고홍달': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B8%88%EB%82%98%EB%9D%BC'},  # 조선 - 조선 후기에, 인목대비 폐비 논의가 이루어지자 성균관을 떠났으며, 인조반정 이후에 참봉으로 | Wiki: 여진족이 화북을 정복하여 세운 왕조
    '고황경': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%ED%99%A9%EA%B2%BD'},  # 근대/개항기|근대/일제강점기 - 해방 이후 이화여자대학교 교수, 서울여자대학교 초대총장 등을 역임한 교육자. 여성운동가 · | Wiki: 한국의 사회학자 (1909–2000)
    '고효충': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%9D%B4%EC%88%9C%EC%8B%A0'},  # 고려 - 고려 예종 때, 국학생으로 「감이녀시」를 지어 풍자한 문신. | Wiki: 조선의 무관 (1545–1598)
    '고흘': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%ED%9D%98'},  # 고대/삼국 - 삼국시대 때, 돌궐의 고구려 신성 침공 시, 돌궐을 격퇴했다고 전해지는 고구려의 장수. | Wiki: 고구려의 장수
    '고흥': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%ED%9D%A5'},  # 고대/삼국 - 삼국시대 때, 박사를 역임하여 『서기』를 저술한 백제의 학자. | Wiki: 백제의 학자, 역사가
    '고흥문': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%ED%9D%A5%EB%AC%B8'},  # 현대/대한민국 - 제6·7·8·9·10대 국회의원을 역임한 정치인. | Wiki: 대한민국 정치인 (1921–1998)
    '고희': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%ED%9D%AC'},  # 조선 - 조선 중기에, 군기시판관, 유원첨사, 픙천부사 등을 역임한 무신 · 공신. | Wiki: 조선시대 호성공신 3등에 책록된 공신
    '고희경': {'role': 'other foreigner', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%ED%9D%AC%EA%B2%BD'},  # 근대/개항기 | 근대/일제강점기 - 일제강점기 때, 주차영국공사관, 이왕직사무관 등을 역임한 관료 · 친일반민족행위자. | Wiki: 위키미디어 동음이의어 문서
    '고희동': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%ED%9D%AC%EB%8F%99'},  # 일제강점기 「정자관을 쓴 자화상」, 「부채를 든 자화상」, 「금강산진주담폭포」, 「탐승」  | Wiki: 한국의 화가 (1886–1965)
    '곡나진수': {'role': 'other foreigner', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A1%EB%82%98%EC%A7%84%EC%88%98'},  # 고대/삼국 - 삼국시대 때, 백제 부흥을 위해 항전하다 주류성이 함락되자 일본으로 망명한 백제의 유민. | Wiki: 백제의 유민
    '곤우': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A4%EC%9A%B0%EC%B9%98%EC%88%98'},  # 고대/삼국 - 삼국시대 때, 백제 고목성에서 벌어진 말갈족과의 전투에 참전한 장수.
    '곤지': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A4%EC%A7%80'},  # 고대/삼국/백제 - 삼국시대 백제 제22대 문주왕(文周王)의 아우. | Wiki: 백제의 왕족 (?–477)
    '골번': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A8%EB%B2%88'},  # 고대/삼국 - 삼국시대 때, 신라의 『삼국사기』 강수전에 나오는 문장가.
    '공규': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%B5%EA%B7%9C'},  # 조선 - 조선 전기에, 예문관봉교, 정언, 전적 등을 역임한 문신.
    '공대일': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EB%B2%84%EC%A7%80%EB%8B%88%EC%95%84_%EA%B3%B5%EB%8C%80_%EC%B4%9D%EA%B8%B0_%EB%82%9C%EC%82%AC_%EC%82%AC%EA%B1%B4'},  # 현대/대한민국 - 해방 이후 광주호남 국악원, 전남미술예술학원, 남도국악학원 등에서 소리선생으로 활동한 판소 | Wiki: 버지니아주 블랙스버그 총기난사 사건
    '공덕귀': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%B5%EB%8D%95%EA%B7%80'},  # 현대/대한민국 - 한국교회여성연합회 대표, 방림방적체불임금대책위원회 위원장 등을 역임한 사회운동가. | Wiki: 대한민국의 4대 대통령 영부인 (1911–1997)
    '공덕흡': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%B5%EB%8D%95%EB%8F%99'},  # 근대/일제강점기 - 일제강점기 간도 용정촌에서 전개된 독립만세시위를 주도하는 과정에서 순국한 독립운동가.
    '공민왕': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%B5%EB%AF%BC%EC%99%95'},  # 고려/고려 후기 - 고려 후기 제31대 국왕. | Wiki: 고려의 제31대 임금 (1330–1374)
    '공병우': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%B5%EB%B3%91%EC%9A%B0'},  # 근대/일제강점기|현대 - 일제강점기 때, 『신소안과학』, 『소안과학』 등을 저술한 의사. | Wiki: 일제강점기와 대한민국의 안과 의사이자 국어학자
    '공부': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%ED%95%99%EC%8A%B5'},  # 고려 - 조선 전기에, 전의부령, 예조총랑, 집현전태학사 등을 역임한 문신. | Wiki: 직간접적 경험, 훈련에 의해 지속적으로 자각, 인지, 
    '공서린': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A1%EB%B6%80_%EA%B3%B5%EC%94%A8'},  # 조선/조선 전기 - 조선 전기에, 황해도관찰사, 대사헌, 동지중추부사 등을 역임한 문신. | Wiki: 동이족에서 유래한 한국의 성씨
    '공성학': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%B5%EC%84%B1%ED%95%99'},  # 근대/일제강점기 - 일제강점기 때, 개성삼업주식회사 사장, 개성인삼조합 조합장 등을 역임한 실업가.
    '공소': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%B5%EC%86%8C'},  # 고려 - 고려 후기에, 한림학사, 문하시랑평장사, 창원백 등을 역임한 문신. | Wiki: 위키미디어 동음이의어 문서
    '공양왕': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%B5%EC%96%91%EC%99%95'},  # 고려/고려 후기 - 고려시대, 제34대(재위: 1389~1392) 왕. | Wiki: 고려의 제34대 임금 (1345–1394)
    '공예태후': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EB%AA%85%EC%A2%85_(%EA%B3%A0%EB%A0%A4)'},  # 고려/고려 전기 - 고려, 제17대 왕이며 인종의 왕비. | Wiki: 고려의 제19대 임금 (1131–1202)
    '공유': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%B5%EC%9C%A0_(%EB%B0%B0%EC%9A%B0)'},  # 고려 - 고려 후기에, 부지밀직사사, 동판밀직사, 판삼사사 등을 역임한 무신. | Wiki: 대한민국의 배우
    '공윤택': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EB%83%84%EC%83%88%EB%8A%94_%EB%82%9C%EB%8B%A4'},  # 현대/대한민국 - 인천 출신으로 한국의 대표적인 제과 제빵 장인.
    '공윤항': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A1%EB%B6%80_%EA%B3%B5%EC%94%A8'},  # 조선 - 조선 후기에, 정언, 병조좌랑 등을 역임한 문신. | Wiki: 동이족에서 유래한 한국의 성씨
    '공은': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%B5'},  # 고려/고려 후기 - 고려 후기 척불소를 올렸던 문신.
    '공인': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%B5%EC%9D%B8'},  # 조선 - 음악을 전업으로 삼던 음악인. | Wiki: 위키미디어 동음이의어 문서
    '공재규': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A1%EB%B6%80_%EA%B3%B5%EC%94%A8'},  # 근대/일제강점기 - 일제강점기 때, 경상남도 합천군 삼가장터의 독립만세시위를 주도하는 과정에서 순국한 독립운동 | Wiki: 동이족에서 유래한 한국의 성씨
    '공재웅': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%95%88%EB%85%95%ED%95%98%EC%84%B8%EC%9A%94_(2022%EB%85%84_%EC%98%81%ED%99%94)'},  # 현대 - 해방 이후 「양주별산대놀이」 전승자로 지정된 기예능보유자.
    '공중인': {'role': 'poet', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%9C%A1%EA%B5%B0%EC%82%AC%EA%B4%80%ED%95%99%EA%B5%90_(%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD)'},  # 현대/대한민국 - 『무지개』, 『조국』 등을 저술한 시인. | Wiki: 대한민국의 육군 장교를 육성하는 기관
    '공직': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EB%B0%95%EC%99%84%EC%88%98'},  # 고려/고려 전기 - 고려 초, 태조 왕건에게 귀부한 호족. | Wiki: 대한민국의 정치인 (1955년~)
    '공진원': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%A0%EC%9A%B4%EA%B8%B0_(%EB%8F%85%EB%A6%BD%EC%9A%B4%EB%8F%99%EA%B0%80)'},  # 근대 - 일제강점기 때, 한국독립당 감찰위원장, 한국광복군 총사령부 참모 등을 역임한 독립운동가. | Wiki: 한국의 독립운동가 (1907–1943)
    '공진항': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%B5%EC%A7%84%ED%95%AD'},  # 근대/일제강점기 - 일제강점기 때, 만주 진출을 위해 만몽산업주식회사를 설립하였으며, 해방 이후 고려인삼흥업사
    '공진형': {'role': 'novelist', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%B5%EB%AA%85'},  # 근대/일제강점기|현대 - 해방 이후 국전의 추천작가를 역임한 화가. 서양화가. | Wiki: 특정 진동수에서 진동하는 현상
    '공천원': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%B5_(%EC%84%B1%EC%94%A8)'},  # 고려 - 고려 후기에, 지문하성사, 이부상서, 참지정사 등을 역임한 문신. | Wiki: 한국의 성씨
    '공학원': {'role': 'scholar foreigner', 'wikipedia': 'https://ko.wikipedia.org/wiki/%ED%99%94%ED%8C%90_%EB%8C%80%ED%95%99'},  # 근대 - 대한제국기 때, 유림의 대표로 성토문을 지어 일본의 만행을 꾸짖었으며, 말년에는 집 근처에 | Wiki: 대만의 사립 대학
    '공한': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EB%B0%98%EC%95%BC%EC%8B%AC%EA%B2%BD'},  # 고대/삼국 - 신라의 제17대 왕, 내물마립간의 손자인 왕족. | Wiki: 대승 불교의 불전
    '공해동': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%B5%ED%95%B4_(%EB%B0%94%EB%8B%A4)'},  # 현대 - 한국전쟁 때, 강원도 화천의 금성지역 수도고지 전투에 참전한 군인. | Wiki: 영유권이나 배타권이 특정 국가에 속하지 않는 바다
    '공혜왕후': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%B5%ED%98%9C%EC%99%95%ED%9B%84'},  # 조선/조선 전기 - 조선의 제9대 왕, 성종의 왕비. | Wiki: 조선 성종의 왕비
    '곽간': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%BD%EB%B2%94'},  # 조선 - 조선 전기에, 성균관사성, 공주목사, 강릉부사 등을 역임한 문신. | Wiki: 대한민국의 희극 배우
    '곽경렬': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%B9%A0%EA%B3%A1%EA%B5%B0%EC%88%98'},  # 근대/일제강점기 - 대한민국임시정부 독립운동자금 모금 활동을 전개한 독립운동가.
    '곽공의': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%84%B8%EA%B3%84_%EA%B5%90%ED%9A%8C_%ED%98%91%EC%9D%98%ED%9A%8C'},  # 고려/고려 후기 - 고려 후기에, 양광도안찰사, 지병마사, 위위경 등을 역임한 문신.
    '곽규석': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%BD%EA%B7%9C%EC%84%9D'},  # 현대/대한민국 - 해방 이후 코미디 연기와 무대, 방송, TV 등의 사회자로 활약한 방송인이자 코미디언. | Wiki: 대한민국의 희극인, 미국 이민 개신교 목회자 (1928
    '곽기락': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%97%B0%EC%95%A0_(%EC%98%81%ED%99%94)'},  # 근대 - 조선 후기에, 채서, 동도서기론을 주장한 문신.
    '곽기수': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%BD_(%EC%84%B1%EC%94%A8)'},  # 조선/조선 전기 - 조선 전기에 예조좌랑, 부안현감 등을 지낸 문신. | Wiki: 한국의 성씨
    '곽낙원': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%BD%EB%82%99%EC%9B%90'},  # 근대/일제강점기 - 일제강점기 때, 아들 김구의 임시정부 활동과 독립운동을 지원한 독립운동가.
    '곽린': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%BD%EB%A6%B0'},  # 고려 - 고려 후기에, 문한서, 서장관 등을 역임한 문신.
    '곽복산': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%84%9C%EC%9A%B8%EC%8B%A0%EB%AC%B8%ED%95%99%EC%9B%90'},  # 근대 - 한국신문학회 초대 회장, 한국신문연구소 이사 등을 역임한 언론인.
    '곽상': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%BD%EC%83%81'},  # 고려 - 고려 전기에, 형부상서, 상서우복야 참지정사, 수사공 등을 역임한 문신. | Wiki: 위키미디어 동음이의어 문서
    '곽상훈': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%BD%EC%83%81%ED%9B%88'},  # 현대/대한민국 - 일제강점기 때, 동래 3·1운동 및 신간회 활동 등 독립운동을 하다가 해방 이후, 국회의장 | Wiki: 대한민국의 정치인 (1896–1980)
    '곽선': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%BD%EC%84%A0'},  # 고려 - 고려 후기에, 양광, 전라도체찰사 등을 역임한 문신.
    '곽성구': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%ED%95%B4%EB%AF%B8_%EA%B3%BD%EC%94%A8'},  # 조선/조선 후기 - 조선 후기에, 지평, 장령, 필선 등을 역임한 문신.
    '곽세건': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%9D%B4%EC%B1%84%EC%9D%80_(2004%EB%85%84)'},  # 조선 - 조선 후기에, 공조정랑, 봉직랑, 익산군수 등을 역임한 문신.
    '곽수강': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%A7%84%EB%A7%88%EC%82%AC_%EC%82%AC%EC%83%81%EB%B3%B5%EB%A7%88'},  # 조선 - 조선 후기에, 「천인감응」, 『매헌문집』 등을 저술한 유생.
    '곽순': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%BD%EC%88%9C'},  # 조선/조선 전기 - 조선 전기에, 교리, 봉상시정, 사간 등을 역임한 문신.
    '곽승우': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%BD%EC%8A%B9%EC%9A%B0'},  # 조선/조선 전기 - 조선 전기에, 이번절제사, 중군총제, 전라도처치사 등을 역임한 무신.
    '곽시': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%BD%EC%8B%9C'},  # 조선/조선 전기 - 조선 전기에, 홍문관정자를 역임한 문신.
    '곽시징': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%B2%AD%EC%A3%BC_%EA%B3%BD%EC%94%A8'},  # 조선 - 조선 후기에, 목릉참봉, 왕자사부, 이인찰방 등을 역임한 학자.
    '곽여': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%BD%EC%97%AC'},  # 고려/고려 전기 - 고려 전기에, 합문지후, 홍주사, 예부원외랑 등을 역임한 관리. | Wiki: 고려의 문신
    '곽여필': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%9C%84%EB%AC%B8%EA%B0%9C'},  # 고려 - 고려 후기에, 국학대사성, 전법판서, 전라도계점사 등을 역임한 문신.
    '곽연성': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%BD%EC%97%B0%EC%84%B1'},  # 조선/조선 전기 - 조선 전기에, 이조참판, 경상도절제사 등을 역임한 무신. | Wiki: 조선 전기의 무신
    '곽영': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%BD%EC%98%81'},  # 조선 - 조선시대 때, 전라도병마절도사, 행호군 등을 역임한 무신. | Wiki: 조선 중기 선조 치세 시대의 무신
    '곽영준': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%BD%EC%98%81%EC%A4%80'},  # 근대/일제강점기 - 일제강점기 때, 경기도 양평군 양근리시장의 독립만세시위에 참여한 독립운동가.
    '곽예': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%BD%EC%98%88'},  # 고려 - 고려 후기에, 국자감대사성, 문한학사, 감찰대부 등을 역임한 문신.
    '곽예순': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%9B%90_%ED%83%9C%EC%A0%95%EC%A0%9C'},  # 현대/대한민국 - 해방 이후 댁에서 곽외과의원을 개업한 의료인. 의사. | Wiki: 몽골 제국의 제 10대 카안
    '곽원': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%BD%EC%9B%90'},  # 고려 - 고려 전기에, 서북면행영부도통, 추성문리공신상주국, 참지정사 등을 역임한 문신 · 공신. | Wiki: 위키미디어 동음이의어 문서
    '곽원진': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%ED%98%84%ED%92%8D_%EA%B3%BD%EC%94%A8'},  # 고려 - 고려 후기에, 총랑, 좌대언, 성균좨주진현관제학 등을 역임한 문신.
    '곽월': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%BD%EC%9B%94'},  # 조선/조선 전기 - 조선 전기에, 제주목사, 청송부사, 남원부사 등을 역임한 문신. | Wiki: 조선시대 중기의 문신
    '곽유번': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B9%80%EA%B4%91%EA%B7%9C_(%EB%B0%B0%EC%9A%B0)'},  # 조선 - 조선 후기에, 『오암문집』 등을 저술한 학자.
    '곽율': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%BD%EC%9C%A8'},  # 조선 - 조선 중기에, 예천군수, 예빈시부정, 초계군수 등을 역임한 문신.
    '곽은': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%BD%ED%8A%9C%EB%B8%8C'},  # 조선/조선 전기 - 조선 전기에, 담양부사, 승지 등을 역임한 문신. | Wiki: 대한민국의 유튜버
    '곽의영': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B3%BD%EC%9D%98%EC%98%81'},  # 현대/대한민국 - 제2, 3, 4대 국회의원, 체신부장관 등을 역임한 정치인 · 실업인. | Wiki: 대한민국 정치인 (1911–1992)
    '곽인식': {'role': 'scholar'},  # 현대/대한민국 - 「작품」, 「천(성)」, 「무제」 등의 작품을 그린 화가.
    '곽자방': {'role': 'other'},  # 조선 - 조선 중기에, 훈련원봉사를 역임하였고, 임진왜란이 발발하자 의병으로 싸워 청주성을 탈환하였
    '곽재겸': {'role': 'other'},  # 조선 - 조선 중기에, 임진왜란이 발발하자 사촌동생인 곽재우와 함께 의병을 이끌고 화왕산성전투에서 
    '곽재구': {'role': 'other'},  # 근대 - 대한제국기 때, 심남일 의진에서 항일의병투쟁을 전개한 의병.
    '곽재기': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 만주에서 의열단을 조직하여 총독부 고관 살해 및 일제 기관 파괴 활동을 계
    '곽재우': {'role': 'other'},  # 조선/조선 후기 - 조선 중기에, 임진왜란이 발발하자 1차 진주성전투를 지원하고, 화왕산성전투에서 활약하며 홍
    '곽제화': {'role': 'scholar'},  # 조선/조선 후기 - 조선 후기 사간원과 사헌부에서 언관으로 활동한 문신, 학자.
    '곽존중': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 예조참판, 중군동지총제, 경창부윤 등을 역임한 문신.
    '곽종석': {'role': 'scholar'},  # 근대/대한제국기 - 대한제국기 때, 을사조약이 강제로 체결되자 오적 처단을 상소하였고, 파리강화회의에 독립청원
    '곽종원': {'role': 'critic'},  # 현대/대한민국 - 해방 이후 『신인간형의 탐구』, 『사색과 행동의 세월』, 『사색의 반려』 등을 저술한 평론
    '곽준': {'role': 'other'},  # 조선 - 조선 중기에, 자여도찰방, 안음현감 등을 역임한 문신.
    '곽중규': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 대한민국임시정부 비서장, 임시의정원 의원 등으로 활동한 독립운동가.
    '곽지운': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 이조좌랑 등을 역임한 문신.
    '곽지원': {'role': 'other'},  # 조선 - 조선시대 때, 하정사 오상을 수행하여 명나라에 다녀온 역관.
    '곽지흠': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 장령, 사간, 집의 등을 역임한 문신.
    '곽진': {'role': 'scholar'},  # 조선 - 임진왜란 때 의병을 모집하여 화왕산성전투에 참전한 후, 학문에만 전념하며 『단곡문집』 등을
    '곽천호': {'role': 'other'},  # 조선 - 조선 후기에, 교리, 예조정랑 등을 역임한 문신.
    '곽충보': {'role': 'other'},  # 고려 - 조선 전기에, 상의중추원사, 도총제 등을 역임한 무신.
    '곽충수': {'role': 'other'},  # 고려 - 고려 후기에, 지평, 형부시랑, 통헌대부 등을 역임한 문신.
    '곽태진': {'role': 'other'},  # 현대/대한민국 - 일제강점기 때, 비밀결사 호의단을 조직하여 항일투쟁을 전개하였으며 해방 이후, 민의원, 민
    '곽학송': {'role': 'novelist'},  # 현대/대한민국 - 「제주도」, 「낯설은 골짜기」, 「모란봉에서 한라산까지」 등을 저술한 작가.
    '곽한일': {'role': 'other'},  # 근대/대한제국기 - 대한제국기 때, 민종식 의진에서 돌격장, 소모장으로 활동한 의병장.
    '곽해룡': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 지중추부사로 『통문관지』를 편찬한 역관.
    '곽현': {'role': 'scholar'},  # 조선 - 조선 후기에, 「만언소」, 『삼안당유고』 등을 저술한 학자.
    '곽홍지': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 전라도사, 예조정랑 등을 역임한 문신.
    '곽휘승': {'role': 'scholar'},  # 근대 - 대한제국기 때, 스승인 곽종석의 학문과 사상에 영향을 받아 성리학을 연구하며 『염와집』을 
    '곽희태': {'role': 'other'},  # 조선 - 조선 후기에, 동지중추부사 등을 역임한 문신.
    '관기': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라 포산에 은거하며 수행한 승려.
    '관나부인': {'role': 'other'},  # 고대/삼국/고구려 - 삼국시대 고구려 제12대 중천왕의 후궁.
    '관례': {'role': 'other'},  # 조선 - 조선 후기에, 구체사 주지를 역임한 승려.
    '관륵': {'role': 'other foreigner'},  # 고대/삼국/백제 - 삼국시대 때, 백제에서 일본으로 불교를 전파하고 승정에 오른 승려.
    '관승': {'role': 'other'},  # 고려 - 고려 전기에, 광명사 주지를 역임한 승려.
    '관영': {'role': 'other'},  # 근대/개항기 - 개항기 때, 대종장을 역임한 승려.
    '관오': {'role': 'other'},  # 고려/고려 전기 - 고려 전기, 자은종 현화사의 승통 상지에게 출가한 후 승계가 수좌에 오른 승려.
    '관준': {'role': 'other'},  # 근대 - 대한제국기 때, 팔도승풍규정원장, 관동도교정 등을 역임한 승려.
    '관지': {'role': 'scholar'},  # 고대/삼국 - 삼국시대 때, 『열반경요간』, 『아비달마식신족론소』 등을 저술한 신라의 승려.
    '관징': {'role': 'other'},  # 조선 - 조선시대 때, 회암 · 낙암 · 환성 · 쌍운 · 대적 등의 지도를 받은 승려.
    '관창': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 황산벌 싸움에서 활약한 신라의 화랑.
    '관혜': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 때, 통일신라의 해인사에서 활동하였던 화엄종의 승려.
    '관홍': {'role': 'other'},  # 조선 - 조선 후기에, 지리산 철불사 아자방선원에서 수도한 승려.
    '관흔': {'role': 'other'},  # 고대/남북국 - 남북국시대 때, 후백제의 시조 견훤의 명을 받아 양산성을 축조한 장수.
    '광개토왕': {'role': 'other'},  # 고대/삼국/고구려 - 고구려의 제19대(재위: 391년~413년) 왕.
    '광기': {'role': 'other'},  # 고려 - 고려 전기에, 손필 등과 거짓 음양서로 유배형을 받은 승려.
    '광덕': {'role': 'other'},  # 고대/남북국 - 삼국시대 때, 신라의 10구체 향가 「원왕생가」 등을 지은 승려.
    '광명부인': {'role': 'other'},  # 고대/삼국/신라 - 신라의 제13대 왕, 미추이사금의 왕비.
    '광언': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 직지사 조실, 조선불교선리참구원 상임이사 등을 역임한 승려.
    '광열': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 대흥사 편양파의 법손으로 대흥사 제2대 강사를 역임한 승려.
    '광정태후': {'role': 'other'},  # 고려 - 고려의 제19대 왕, 명종의 왕비.
    '광제': {'role': 'other'},  # 고려/고려 전기 - 고려전기 승통을 역임한 승려.
    '광종': {'role': 'other'},  # 고려/고려 전기 - 고려 전기, 제4대 왕.
    '광주원부인': {'role': 'other'},  # 고려/고려 전기 - 고려 전기, 제1대 왕 태조의 제15 왕비.
    '광준': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 총섭, 자헌대부 등을 역임한 승려.
    '광평대군': {'role': 'other'},  # 조선/조선 전기 - 조선의 제4대 왕, 세종의 5번째 왕자.
    '광학': {'role': 'other'},  # 고려 - 고려 전기에, 적리녀의 아들로 신인종에 귀의하여 대덕을 역임한 승려.
    '광해군': {'role': 'other'},  # 조선/조선 후기 - 조선의 제15대 국왕.
    '광화부인': {'role': 'other'},  # 고대/남북국 - 통일신라의 제48대 왕, 경문왕의 어머니로, 광의왕태후로 봉해진 왕족.
    '괴유': {'role': 'other'},  # 고대/삼국 - 고구려 대무신왕 때, 부여 정벌에 자원하여 전공을 세운 장수.
    '굉연': {'role': 'poet'},  # 고려/고려 후기 - 고려후기 나옹 혜근의 제자로 선원사 5대 주지를 역임한 승려. 시인.
    '굉활': {'role': 'other'},  # 조선 - 조선 후기에, 대흥사 제3대 종사 도안의 문하에서 수도한 승려.
    '교기': {'role': 'other foreigner'},  # 고대/삼국/백제 - 백제의 제31대 의자왕의 조카로, 섬으로 추방되어 일본으로 건너간 종실.
    '교대': {'role': 'other foreigner'},  # 고대/삼국 - 삼국시대 때, 일본에 화현했던 미륵보살의 화신으로 알려진 승려.
    '교웅': {'role': 'other'},  # 고려 - 고려 전기에, 삼중대사, 선사, 대선사 등을 역임한 승려.
    '교필': {'role': 'other'},  # 고대/남북국 - 남북국시대 때, 통일신라의 김해지방에서 세력을 떨쳤던 호족.
    '구강': {'role': 'other'},  # 조선 - 조선 후기에, 시강원보덕, 첨지사, 함경도암행어사 등을 역임한 문신.
    '구겸': {'role': 'other'},  # 조선/조선 전기 - 조선전기 경상우도병마절도사, 의주목사 등을 역임한 무신.
    '구공신': {'role': 'other'},  # 고려 - 고려의 제34대 왕인 공양왕을 즉위시킨 9인의 공신.
    '구굉': {'role': 'other'},  # 조선 - 조선시대 때, 형조판서, 공조판서, 병조판서 등을 역임한 무신.
    '구근': {'role': 'other'},  # 고대/남북국 - 남북국시대 때, 통일신라에서 사찬을 역임한 장수.
    '구기': {'role': 'other'},  # 고대/남북국 - 남북국시대 때, 통일신라에서 술간을 역임한 장수.
    '구낙서': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 때, 서울에서 전개된 야간 독립만세시위에 참여했다가 미행하던 일본 경찰에 의해 
    '구덕': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 당나라에서 불경을 가지고 온 통일신라의 승려.
    '구덕환': {'role': 'other'},  # 현대/대한민국 - 일제강점기 때, 임시정부에서 활동하다가 고향으로 돌아와 의사로 재직 중에 독립운동을 벌였고
    '구도': {'role': 'other'},  # 고대/삼국/고구려 - 삼국시대 때, 고구려에서 비류부장 등을 역임한 관리.
    '구도갈문왕': {'role': 'other'},  # 고대/삼국 - 신라의 제13대 왕, 미추이사금의 아버지로, 좌군주를 역임하여 소문국을 정벌한 왕족.
    '구례마': {'role': 'other'},  # 고대/삼국 - 삼국시대 신라 무산대수촌의 촌장.
    '구륜공': {'role': 'other'},  # 고대/삼국 - 신라의 제24대 진흥왕의 셋째 아들이자 후백제 견훤의 고조부로 『이제가기』에 기록된 왕족.
    '구리내': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 일리촌(一利村)의 지방세력가. 촌주.
    '구마기': {'role': 'other foreigner'},  # 고대/삼국 - 삼국시대 때, 탐라국에서 일본으로 파견된 탐라국의 왕자.
    '구만리': {'role': 'other'},  # 조선 - 조선 후기에, 사서, 지평, 장령 등을 역임한 문신.
    '구명겸': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 좌포도대장, 삼도수군통제사 등을 역임한 문신.
    '구문신': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 경상우도병마도절제사 등을 역임한 무신.
    '구문유': {'role': 'other'},  # 조선 - 조선 후기에, 현풍현감, 고령현감, 익찬 등을 역임한 문신.
    '구문치': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 통제사, 어영대장, 포도대장 등을 역임한 무신.
    '구변': {'role': 'other'},  # 조선 - 조선 전기에, 이조좌랑, 진주목사 등을 역임한 문신.
    '구본웅': {'role': 'scholar'},  # 근대 - 일제강점기 때, 「얼굴 습작」, 「비파와 포도」, 「여인」 등의 작품을 그린 화가.
    '구봉령': {'role': 'other'},  # 조선 - 조선 전기에, 대사헌, 병조참판, 형조참판 등을 역임한 문신.
    '구봉서': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 호조참의, 평안도관찰사 등을 역임한 문신.
    '구봉창': {'role': 'other'},  # 조선 - 조선 후기에, 충청도수사, 충청병사, 평안병사 등을 역임한 무신.
    '구사나왕': {'role': 'other foreigner'},  # 고대/삼국 - 삼국시대 때, 고구려 멸망 후 일본으로 망명한 고구려의 왕족.
    '구사맹': {'role': 'other'},  # 조선 - 조선 중기에, 좌부승지, 이조판서, 좌찬성 등을 역임한 문신.
    '구사안': {'role': 'other'},  # 조선 - 조선 전기에, 위사원종공신일등에 책록된 문신.
    '구상': {'role': 'poet'},  # 현대/대한민국 - 해방 이후 「여명도」, 「길」, 「초토의 시」 등을 저술한 시인.
    '구선복': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 병조판서, 의금부판사 등을 역임한 무신.
    '구선행': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 판의금부사, 병조판서 등을 역임한 무신.
    '구성': {'role': 'other'},  # 조선 - 조선 중기에, 호조참판, 해주목사 등을 역임한 문신.
    '구성량': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 충청도병마도절제사, 판안동대도호부사 등을 역임한 무신.
    '구성로': {'role': 'other'},  # 고려 - 고려 후기에, 대호군, 강원도부원수, 경상도부원수 등을 역임한 무신.
    '구성우': {'role': 'other'},  # 고려 - 고려 후기에, 간관, 문하부낭사, 형조판서 등을 역임한 문신.
    '구성임': {'role': 'other'},  # 조선 - 조선 후기에, 형조판서, 판의금부사, 판돈령부사 등을 역임한 무신.
    '구수담': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 부제학, 전라감사, 대사헌 등을 역임한 문신.
    '구수복': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 수찬, 이조좌랑, 구례현감 등을 역임한 문신.
    '구수암': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 경상남도 동래군 기장읍의 독립만세시위를 주도한 혐의로 체포되어 순국한 독립
    '구수영': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 오위도총관, 장악원제조 등을 역임한 무신.
    '구수왕': {'role': 'other'},  # 고대/삼국 - 백제의 제6대(재위: 214년~234년) 왕.
    '구수혜': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 신라의 일길찬 등을 역임한 관리.
    '구수훈': {'role': 'other'},  # 조선 - 조선 후기에, 경기도수군절도사, 수원부사, 좌포도대장 등을 역임한 무신.
    '구여순': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 의령에서 만세시위를 주도하였으며, 의열단에서 항일무장투쟁을 계획한 독립운동
    '구연영': {'role': 'other'},  # 근대 - 개항기 때, 민승천 의진 중군장, 독립협회 회원으로 활동하며 항일투쟁을 전개한 의병 · 독
    '구연해': {'role': 'scholar'},  # 조선 - 조선 후기에, 『연역설』, 『강초유고』 등을 저술한 학자.
    '구연흠': {'role': 'other'},  # 근대 - 일제강점기 때, 전조선민중운동자대회 준비위원, 국제모쁠 제2차조선대표 등을 역임한 사회주의
    '구영': {'role': 'other'},  # 조선 - 조선 후기에, 별좌, 감찰, 회인현감 등을 역임한 문신.
    '구영검': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 면천군, 전리판서 등을 역임한 문신.
    '구영숙': {'role': 'other'},  # 근대/일제강점기|현대 - 보건부장관, 세계보건기구 한국수석대표, 한국적십자사 총재 등을 역임한 의사 · 관료.
    '구완희': {'role': 'other'},  # 근대 - 대한제국기 때, 육군참령, 육군법원 이사, 경무사 등을 역임한 관료.
    '구용': {'role': 'other'},  # 조선 - 조선 중기에, 김화현감 등을 역임한 문신.
    '구용서': {'role': 'other'},  # 현대/대한민국 - 한국은행 초대 총재, 대한석탄공사 총재, 상공부장관 등을 역임한 금융인 · 관료.
    '구용징': {'role': 'scholar'},  # 조선 - 조선 후기에, 『경타재문집』 등을 저술한 학자.
    '구용현': {'role': 'other'},  # 현대/대한민국 - 문교부 장학실장, 부산직할시교육위원회 교육감, 국회의원 등을 역임한 교육자.
    '구원일': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 병자호란 당시 강화도 갑곶에서 순절한 무관.
    '구윤명': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 이조를 제외한 육조의 판서 등을 역임한 문신.
    '구윤옥': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 병조판서, 호조판서, 판중추부사 도승지, 병조판서, 의금부판사 등을 역임한 문신
    '구율': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 사찬으로 사천원전투에 참전한 관리.
    '구은': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에 활동했던, 아호에 은(隱)자가 붙은 9인의 문신들.
    '구음': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 사간, 승지, 간성군수 등을 역임한 문신.
    '구의강': {'role': 'other'},  # 조선 - 조선 후기에, 대사간, 대사성 등을 역임한 문신.
    '구이신왕': {'role': 'other'},  # 고대/삼국/백제 - 백제의 제19대(재위: 420년~427년) 왕.
    '구익': {'role': 'other'},  # 조선 - 조선 후기에, 판서, 지돈령부사 등을 역임한 문신.
    '구인기': {'role': 'other'},  # 조선 - 조선 후기에, 공조판서, 영의정 등을 역임한 문신.
    '구인문': {'role': 'other'},  # 조선 - 조선 전기에, 청주판관, 집현전교리, 좌정언 등을 역임한 문신.
    '구인회': {'role': 'other'},  # 현대 - 금성사 사장, 호남정유 대표, 한국경제인협회 부회장 등을 역임한 실업가.
    '구인후': {'role': 'other'},  # 조선 - 조선시대 때, 판의금부사, 홍청도병마절도사, 우의정 등을 역임한 무신.
    '구일': {'role': 'other'},  # 조선 - 조선 후기에, 한성판윤, 총융사, 지돈령부사 등을 역임한 무신.
    '구자균': {'role': 'scholar'},  # 현대/대한민국 - 고려대학교 문과대학의 교수 등을 역임하였으며, 『국문학사』, 『국역파한집 · 용재총화』, 
    '구자운': {'role': 'poet'},  # 현대 - 『처녀승천』, 『청자수병』 등을 저술한 시인.
    '구자춘': {'role': 'other'},  # 현대 - 서울특별시 경찰국장, 서울특별시장, 내무부장관 등을 역임한 군인 · 정치인.
    '구저': {'role': 'other foreigner'},  # 고대/삼국 - 삼국시대 때, 여러 차례 일본에 사신으로 파견된 백제의 관리.
    '구정래': {'role': 'scholar'},  # 조선 - 조선 후기에, 광릉참봉 등을 역임하였으며, 『연포당유고』를 저술한 학자.
    '구정훈': {'role': 'other'},  # 조선 - 조선 후기에, 빙고별제, 배천군수 등을 역임한 문신.
    '구족달': {'role': 'other'},  # 고려/고려 전기 - 고려 전기에, 「강릉보현사낭원대사오진탑비」, 「충주정토사법경대사자등탑비」 등의 글을 쓴 서
    '구족왕후': {'role': 'other'},  # 고대/남북국/통일신라 - 신라의 제37대 왕, 선덕왕의 왕비.
    '구종수': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 순금사사직, 선공감부정 등을 역임한 문신.
    '구종지': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 형조의랑, 호조참의, 호조참판 등을 역임한 문신.
    '구종직': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 행첨지중추부사, 지경연사, 좌찬성 등을 역임한 문신.
    '구준원': {'role': 'scholar'},  # 조선/조선 후기 - 조선 후기에, 『신임기년제요』 등을 저술한 문신.
    '구중회': {'role': 'other'},  # 현대/대한민국 - 해방 이후 국회의원, 미군정청 경남고문 등을 역임한 정치인. 교육자.
    '구지정': {'role': 'other'},  # 조선 - 조선 후기에, 공주목사, 황주목사 등을 역임한 문신.
    '구진': {'role': 'other'},  # 고려 - 고려 전기에, 시중, 나주도대행대시중 등을 역임한 문신.
    '구진주': {'role': 'scholar'},  # 조선 - 조선 후기에, 천연두를 앓다가 두 눈을 실명하였으나, 그 뒤에도 더욱 학문에 정진하여 역사
    '구진천': {'role': 'other'},  # 고대/남북국 - 남북국시대 때, 신라의 사찬이자 쇠뇌의 명수인 관리.
    '구찬회': {'role': 'other'},  # 근대 - 일제강점기 때, 신민회 회원으로 활동하였으며, 독립사상을 고취하는 문서를 배포하다가 체포되
    '구참공': {'role': 'other'},  # 고대/삼국 - 신라 진평왕 때의 화랑.
    '구철우': {'role': 'novelist'},  # 근대/일제강점기 | 현대 - 해방 이후 국전 추천작가, 서예부 심사위원 및 심사위원장 등을 역임한 서화가.
    '구춘선': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 북만주에서 활동한 독립운동가.
    '구치곤': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 우승지, 한성부우윤 등을 역임한 문신.
    '구치관': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 우찬성, 우의정, 영의정 등을 역임한 문신.
    '구치용': {'role': 'scholar'},  # 조선 - 조선 후기에, 『우교당유고』, 『주서연의』 등을 저술한 학자.
    '구치홍': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 판돈령부사, 동지중추부사, 지훈련원사 등을 역임한 무신.
    '구칠': {'role': 'other foreigner'},  # 고대/남북국 - 남북국시대 때, 김대세와 함께 신선이 되려고 중국의 오월로 건너간 신라의 도교인.
    '구태': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 『주서』 백제전, 『수서』 동이전 백제조, 『한원』 등에 기록된 백제의 시조
    '구택규': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 공조참판, 형조참판, 한성부판윤 등을 역임한 문신.
    '구파해': {'role': 'other'},  # 고대/삼국 - 초기국가시대 때, 백제에 귀화한 남옥저의 유민.
    '구한': {'role': 'other'},  # 조선 - 조선 전기에, 중종의 딸 숙정옹주와 결혼하여 능창위에 봉해진 문신.
    '구항': {'role': 'other'},  # 조선 - 조선 중기에, 임진왜란이 발발하자 금산전투에 참전한 의병장.
    '구형왕': {'role': 'other'},  # 고대/삼국/가야 - 금관가야의 제10대(재위: 521년~532년) 왕.
    '구혜': {'role': 'other'},  # 조선 - 조선 중기에, 호조좌랑, 정언 등을 역임한 문신.
    '구홍': {'role': 'other'},  # 고려 - 고려 후기에, 밀직부사, 우정승 등을 역임한 문신.
    '구희': {'role': 'scholar'},  # 조선 - 조선 중기에, 임진왜란이 발발하자 금산전투와 진주성전투에서 활약하다가 진주성이 함락되자 자
    '국경인': {'role': 'other'},  # 조선 - 조선시대 임진왜란 때, 경성부민을 선동해 반란을 일으킨 주모자.
    '국대부인': {'role': 'other'},  # 고대/남북국 - 후백제의 왕, 견훤의 딸인 공주.
    '국융': {'role': 'other'},  # 조선 - 조선 전기에, 애완유영(哀婉悠永) 미조(美調)의 범패로 유명한 범패승.
    '국지모': {'role': 'other foreigner'},  # 고대/삼국 - 삼국시대 때, 백제에서 중국 수나라로 파견된 관리.
    '국채표': {'role': 'scholar'},  # 현대 - 중앙관상대장, 기상학회장 등을 역임하며 한국의 후진 기상전문가 양성에 힘쓴 기상학자.
    '국침': {'role': 'scholar'},  # 조선 - 조선 후기에, 『송만문집』 등을 저술한 학자.
    '궁예': {'role': 'other'},  # 고대/남북국/고려·마진·태봉 - 태봉국의 제1대(재위:901년~918년) 왕.
    '권감': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 도승지, 의정부좌참찬, 병조판서 등을 역임한 문신.
    '권강': {'role': 'scholar'},  # 조선 - 조선 중기에, 『방담문집』 등을 저술한 학자.
    '권개': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 관찰사, 중추원부사 등을 역임한 문신.
    '권건': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 예조참판, 호조참판 등을 역임한 문신.
    '권격': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 병조정랑, 강릉부사 등을 역임한 문신.
    '권겸': {'role': 'other'},  # 고려 - 고려 후기에, 찬성사, 판삼사사, 태부감태감 등을 역임한 문신.
    '권겹': {'role': 'other'},  # 조선 - 조선 중기에, 종부시주부 등을 역임한 문신.
    '권경': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 동지중추원사, 경상좌도병마절도사 등을 역임한 문신.
    '권경완': {'role': 'poet'},  # 근대/일제강점기 - 일제강점기 『자화상』, 『윤리』, 『동결』 등을 저술한 시인.
    '권경우': {'role': 'other'},  # 조선 - 조선 중기에, 정언, 헌납, 장령 등을 역임한 문신.
    '권경유': {'role': 'other'},  # 조선 - 조선 전기에, 홍문관정자, 제천현감 등을 역임한 문신.
    '권경중': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 상서예부시랑지제고를 역임한 문신.
    '권경희': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 예조참판, 대사헌 등을 역임한 문신.
    '권고': {'role': 'other'},  # 고려/고려 후기 - 고려 후기 검교시중을 역임한 문신.
    '권공': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 사은사, 경상좌도병마절제사 등을 역임하면서 세조의 신임을 받았던 무신 · 공
    '권굉': {'role': 'other'},  # 조선 - 조선 후기에, 상의원별좌, 별제, 동궁의부수 등을 역임한 문신.
    '권구': {'role': 'scholar'},  # 조선 - 조선 후기에, 「여사휘찬의의」, 『내정편』, 『병곡집』 등을 저술한 학자.
    '권구현': {'role': 'poet'},  # 근대 - 일제강점기 때, 『흑방의 선물』을 저술한 시인 · 미술가.
    '권규': {'role': 'other'},  # 조선 - 조선 후기에, 대사간, 대사헌, 공조참판 등을 역임한 문신.
    '권균': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 이조판서, 영경연사, 우의정 등을 역임한 문신.
    '권극량': {'role': 'scholar'},  # 조선 - 조선 후기에, 『동산문집』 등을 저술한 학자.
    '권극례': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 대사헌, 예조판서 등을 역임한 문신.
    '권극상': {'role': 'other'},  # 조선 - 조선 후기에, 천총, 훈련원첨정 등을 역임한 무신.
    '권극중': {'role': 'other'},  # 조선/조선 후기 - 조선후기 평해군수, 곡산부사, 삼척영장 등을 역임한 무신.
    '권극지': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 형조참판, 동지경연, 예조판서 등을 역임한 문신.
    '권극화': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 충청도관찰사, 중추원부사, 행지중추원사 등을 역임한 문신.
    '권근': {'role': 'scholar'},  # 조선/조선 전기 - 조선 전기에, 중추원사, 정당문학, 대사헌 등을 역임한 문신.
    '권기': {'role': 'scholar'},  # 조선 - 조선 중기에, 『용만문집』, 『영가지』 등을 저술한 학자.
    '권기옥': {'role': 'other'},  # 일제강점기 때, 남경 국민정부 항공서 부비항원, 의열단 여자부 연락원으로 활동한 한국 최초
    '권기일': {'role': 'other foreigner'},  # 근대 - 일제강점기 때, 서로군정서 외무담당과 어사부장으로 활동하다가 일본군의 습격으로 순국한 독립
    '권길': {'role': 'other'},  # 조선/조선 전기 - 조선시대 임진왜란 때 상주판관으로 상주 북천전투에서 순절한 문신.
    '권단': {'role': 'other'},  # 고려 - 고려 후기에, 밀직제학, 지첨의부사, 찬성사 등을 역임한 문신.
    '권달수': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 이조좌랑, 대교, 부교리 등을 역임한 문신.
    '권담': {'role': 'other'},  # 고려 - 조선 전기에, 공주목사, 황해도관찰사, 전주부윤 등을 역임한 문신.
    '권대림': {'role': 'other'},  # 조선 - 조선 후기에, 성균관직강, 자인현감, 만경현감 등을 역임한 문신.
    '권대운': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 예조판서, 병조판서, 영의정 등을 역임한 문신.
    '권대재': {'role': 'other'},  # 조선 - 조선 후기에, 전라감사, 홍문관제학, 호조판서 등을 역임한 문신.
    '권대항': {'role': 'other'},  # 조선 - 조선 후기에, 금군청부총관을 역임한 무신.
    '권대형': {'role': 'other'},  # 근대 - 일제강점기 때, 조선공산당재건설동맹 중앙집행위원, 조선공산주의자협의회 책임자 등을 역임한 
    '권덕규': {'role': 'scholar'},  # 근대 | 현대 - 일제강점기 때, 「한글맞춤법통일안」의 원안을 작성한 국어학자.
    '권덕린': {'role': 'other'},  # 조선 - 조선 전기에, 좌랑, 합천군수 등을 역임한 문신.
    '권덕수': {'role': 'scholar'},  # 조선 - 조선 후기에, 『몽구』, 『포헌집』 등을 저술한 학자.
    '권덕여': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 부제학, 대사간 등을 역임한 문신.
    '권덕형': {'role': 'scholar'},  # 조선 - 조선 후기에, 『경림당유집』 등을 저술한 학자.
    '권도': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 판서, 참찬 등을 역임한 문신.
    '권돈': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 선전관, 경주통판, 밀양부사 등을 역임한 무신.
    '권돈례': {'role': 'scholar'},  # 고려 - 고려 후기에, 어사 등을 역임하였으며, 무신의 난 이후 지방으로 피신하여 은거한 학자.
    '권돈인': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 우의정, 좌의정, 영의정 등을 역임한 문신.
    '권동보': {'role': 'other'},  # 조선 - 조선 전기에, 헌릉참봉, 사섬시직장 등을 역임한 문신.
    '권동수': {'role': 'other foreigner'},  # 근대 - 갑신정변 이후, 김옥균 등의 암살 목적으로 일본에 밀파된 문신.
    '권동진': {'role': 'other'},  # 근대/일제강점기 - 천도교 지도자이자 민족 대표의 한 사람으로서 「3·1독립선언서」에 서명한 독립운동가.
    '권두경': {'role': 'other'},  # 조선 - 조선 후기에, 형조좌랑, 전라도사, 사간원정언 등을 역임한 문신.
    '권두기': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 해운판관, 지평, 정언 등을 역임한 문신.
    '권두문': {'role': 'other'},  # 조선 - 조선 중기에, 내자시정, 통례원좌통례 등을 역임한 문신.
    '권득경': {'role': 'other'},  # 조선 - 조선 중기에, 형조좌랑, 평양판관 등을 역임한 문신.
    '권득기': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 예조좌랑, 공조참판 등을 역임한 문신.
    '권득수': {'role': 'other'},  # 근대/대한제국기 - 대한제국기 때, 경기도 지평, 이천, 양근, 양주 등지에서 항일의병투쟁을 전개한 의병장.
    '권람': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 의정부우찬성, 좌찬성, 우의정 등을 역임한 문신.
    '권렴': {'role': 'other'},  # 고려 - 고려 후기에, 정순대부좌상시, 광정대부첨의찬성사 등을 역임한 문신.
    '권령': {'role': 'other'},  # 조선 - 조선 후기에, 승지, 한성부좌우윤 등을 역임한 문신.
    '권륜': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 대사성, 예조참의, 강원도관찰사 등을 역임한 문신.
    '권만': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 병조정랑, 이조참의 등을 역임한 문신.
    '권만두': {'role': 'other'},  # 조선 - 조선 후기에, 공조정랑, 장수현감 등을 역임한 문신.
    '권만전': {'role': 'scholar'},  # 조선 - 조선 후기에, 『근계문집』 등을 저술한 학자.
    '권맹손': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 이조판서, 중추원사 등을 역임한 문신.
    '권맹희': {'role': 'other'},  # 조선 - 조선 전기에, 도승지, 함길남도절도사, 경기관찰사 등을 역임한 문신.
    '권명덕': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 「자화상」 · 「모란대」 등을 그린 화가. 유화가.
    '권명희': {'role': 'scholar'},  # 조선 - 조선 후기에, 『삼외재문집』 등을 저술한 학자.
    '권목': {'role': 'other'},  # 조선 - 조선 후기에, 함흥판관, 호조정랑 등을 역임한 문신.
    '권무중': {'role': 'other'},  # 조선 - 조선 후기에, 문음(門蔭)으로 선전관을 제수받았으나 사양하고 낙향한 문신.
    '권문해': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 좌부승지, 사간 등을 역임한 문신.
    '권민수': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 대사헌, 동지중추부사 등을 역임한 문신.
    '권반': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 관찰사, 형조판서 등을 역임한 문신.
    '권벌': {'role': 'other'},  # 조선 - 조선 전기에, 의정부좌참찬, 의정부우찬성, 원상 등을 역임한 문신.
    '권벽': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 관찰사, 승문원제조 등을 역임한 문신.
    '권변': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 대사헌, 부수찬, 대사간 등을 역임한 문신.
    '권병노': {'role': 'other'},  # 현대/대한민국 - 제헌국회의원, 제2대 국회의원을 역임하였으며, 정계 은퇴 후 고향에서 의사로 활동한 정치인
    '권병덕': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 독립선언서에 서명한 민족대표 33인 중 한 사람으로, 천도교 전제관장, 보
    '권보': {'role': 'scholar'},  # 조선 - 조선 후기에, 『성포일고』 등를 저술한 학자.
    '권복': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 중추원부사, 강계도호부사, 절제사 등을 역임한 무신.
    '권복흥': {'role': 'other'},  # 조선 - 조선 중기에, 임진왜란이 발발하자 의병을 일으켜 항쟁한 의병장.
    '권봉수': {'role': 'poet'},  # 근대 - 일제강점기 때, 「용호정」을 저술한 시인.
    '권봉희': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 사간, 정언, 홍문관수찬 등을 역임한 문신.
    '권부': {'role': 'other'},  # 고려 - 고려 후기에, 우정언, 시강학사, 삼중대광 등을 역임한 문신.
    '권사공': {'role': 'other'},  # 조선 - 조선 후기에, 예조좌랑, 예조정랑 등을 역임한 문신.
    '권산해': {'role': 'other'},  # 조선 - 조선 전기에, 종부시첨정을 역임하였으나 세조 즉위 후 조정에 나가지 않았던 관리.
    '권삼득': {'role': 'other'},  # 조선 - 조선 후기에, 「판소리 설렁제」라는 소리제를 낸 것으로 유명한 판소리의 명창.
    '권삼현': {'role': 'scholar'},  # 근대 - 일제강점기 때, 『각재문집』 등을 저술한 학자.
    '권상': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 문소전참봉, 용강현령, 선공감정 등을 역임한 문신.
    '권상구': {'role': 'other'},  # 조선 - 조선 후기에, 동부승지, 여주목사, 공조참의 등을 역임한 문신.
    '권상길': {'role': 'scholar'},  # 조선 - 조선 후기에, 『남곡선생문집』 등을 저술한 학자.
    '권상로': {'role': 'scholar'},  # 현대/대한민국 - 일제강점기 때, 문경 대승사 주지, 불교조계종원로회 원장, 불교사상사 사장 등을 역임한 불
    '권상룡': {'role': 'scholar'},  # 조선 - 조선 후기에, 『긍재유고』 등을 저술한 학자.
    '권상신': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 병조판서, 광주유수 등을 역임한 문신.
    '권상연': {'role': 'other'},  # 조선 - 조선 후기에, 조상의 제사를 지내지 않은 일로 윤지충과 함께 체포되어 참수당한 순교자.
    '권상유': {'role': 'other'},  # 조선 - 조선 후기에, 대사간, 도승지, 이조판서 등을 역임한 문신.
    '권상익': {'role': 'other'},  # 근대 - 일제강점기 때, 파리강화회의에 전달할 독립청원서의 서명 운동과 발송에 가담하였으며, 군자금
    '권상일': {'role': 'other'},  # 조선 - 조선 후기에, 대사간, 홍문관부제학, 대사헌 등을 역임한 문신.
    '권상임': {'role': 'other'},  # 조선 - 조선 후기에, 풍기군수, 승문원판교, 춘추관편수관 등을 역임한 문신.
    '권상중': {'role': 'other'},  # 근대 - 대한제국기 때, 항일의병투쟁을 벌이며 청송일대에서 모병 및 군자금 모금 활동을 전개한 의병
    '권상하': {'role': 'scholar'},  # 조선 - 조선 후기에, 송시열의 수제자로서 기호학파의 정통 계승자이며, 『한수재집』, 『삼서집의』 
    '권석도': {'role': 'other'},  # 근대 - 대한제국기 때. 지리산 일대에서 항일의병투쟁을 전개한 의병장.
    '권석장': {'role': 'scholar'},  # 조선 - 조선 후기에, 「심성설」, 「이기호발설」, 『외암문집』 등을 저술한 학자.
    '권섭': {'role': 'novelist'},  # 조선/조선 후기 - 조선 후기에, 「황강구곡가」, 「도통가」, 『옥소집』 등을 저술한 문인.
    '권성': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 충청도관찰사, 형조판서 등을 역임한 문신.
    '권성구': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 병조정랑, 직강, 병조좌랑 등을 역임한 문신.
    '권성오': {'role': 'other'},  # 조선 - 조선 후기에, 공조정랑, 보령현감 등을 역임한 문신.
    '권성원': {'role': 'other'},  # 조선 - 조선 후기에, 여산군수, 선산부사 등을 역임한 문신.
    '권성익': {'role': 'scholar'},  # 조선 - 조선 후기에, 「성지위천명」, 「성리설변」, 『연곡유집』 등을 저술한 학자.
    '권성제': {'role': 'scholar'},  # 조선 - 조선 후기에, 『반구재유고』 등을 저술한 학자.
    '권성징': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 시약청어의, 내의원수의 등을 역임한 의관.
    '권세경': {'role': 'other'},  # 조선 - 조선 후기에, 회양부사, 청주목사 등을 역임한 문신.
    '권세숙': {'role': 'other'},  # 조선 - 조선 후기에, 정언, 홍문록, 교리 등을 역임한 문신.
    '권세연': {'role': 'other'},  # 근대/개항기 - 개항기 때, 경상북도 안동에서 항일의병투쟁을 전개한 의병장.
    '권세항': {'role': 'other'},  # 조선 - 조선 후기에, 승지, 경주부윤 등을 역임한 문신.
    '권세후': {'role': 'other'},  # 고려/고려 후기 - 고려후기 방호별감으로 양산성전투에 참전한 관리. 무신.
    '권수': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 장령, 동래부사 등을 역임한 문신.
    '권수평': {'role': 'other'},  # 고려 - 고려 후기에, 대정, 추밀원부사 등을 역임한 문신.
    '권순': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 사산감역, 양주목사, 동지중추부사 등을 역임한 문신.
    '권순명': {'role': 'other'},  # 근대/대한제국기 - 대한제국기 때, 김춘쇠 의병부대에서 포군으로 활동한 의병.
    '권순장': {'role': 'other'},  # 조선 - 조선시대 병자호란 때, 검찰사 김경징 등과 의병을 일으킨 문신.
    '권순창': {'role': 'other'},  # 조선 - 조선 후기에, 첨지중추부사, 돈녕부도정, 동지중추부사 등을 역임한 문신.
    '권승렬': {'role': 'other'},  # 현대/대한민국 - 일제강점기 때, 광주학생운동 및 여운형 · 안창호 검거 사건 등을 변론한 법조인.
    '권시': {'role': 'other'},  # 조선 - 조선 후기에, 승지, 찬선, 한성부우윤 등을 역임한 문신.
    '권시경': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 강원도관찰사, 예조판서, 판돈녕부사 등을 역임한 문신.
    '권신': {'role': 'other'},  # 고려 - 고려 전기에, 고려 건국에 대한 공으로 이등공신에 책록된 관리 · 공신.
    '권심규': {'role': 'scholar'},  # 조선 - 조선 후기에, 『송하집』 등을 저술한 학자.
    '권애라': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 경기도 개성군 송도면의 독립만세시위를 주도하였으며, 상하이로 건너가 애국부
    '권양': {'role': 'novelist'},  # 조선/조선 후기 - 조선  후기, 자녀교육의 지침서인 『영가가훈』을 저술한 문인.
    '권양성': {'role': 'other'},  # 조선 - 조선 후기에, 한성부서윤, 배천현감, 첨지중추부사 등을 역임한 문신.
    '권언': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 수양대군의 심복으로 활약하여 진위 겸 진향부사 등을 역임한 무신 · 공신.
    '권엄': {'role': 'other'},  # 조선 - 조선 후기에 병조판서 · 지중추부사 · 한성판윤 등을 역임한 문신.
    '권업': {'role': 'other'},  # 조선 - 조선 후기에, 형조판서, 대사헌, 참찬 등을 역임한 문신.
    '권연하': {'role': 'other'},  # 조선 - 조선 후기에, 선공감역, 돈녕부도정, 용양위호군 등을 역임한 문신.
    '권엽': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 군수, 오위도총부부총관 등을 역임한 문신.
    '권영': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 승지, 사직 등을 역임한 문신.
    '권영대': {'role': 'scholar'},  # 현대/대한민국 - 서울대학교 교수를 역임하며 광학 교육과 연구에 힘썼으며, 『자연과학개론』, 『일반물리학』,
    '권영만': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 때, 대한광복회를 조직하여 군자금을 모금하고 일본 고관 암살을 계획하는 등 항일
    '권영우': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「바닷가의 환상」, 「섬으로 가는 길」, 「무제」 등을 그린 화가.
    '권영준': {'role': 'other'},  # 근대 - 일제강점기 때, 정교, 전리, 경의원 참의 등을 역임한 대종교인.
    '권영태': {'role': 'other'},  # 현대/대한민국 - 일제강점기 공산주의자그룹을 결성하고자 했던 사회주의운동가.
    '권영하': {'role': 'other'},  # 현대/대한민국 - 해방 이후 강릉단오제 「관노가면극」 전승자로 지정된 기예능보유자.
    '권영회': {'role': 'other'},  # 근대/대한제국기 - 대한제국기 때, 박민홍 의병부대에서 참모장으로 활동한 의병장.
    '권예': {'role': 'other'},  # 조선 - 조선 전기에, 대사헌, 이조판서, 우참찬 등을 역임한 문신.
    '권오기': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 경상좌도군적경차관, 사도시부정, 좌통례 등을 역임한 문신.
    '권오돈': {'role': 'other'},  # 근대 - 일제강점기 때, 무정부주의 비밀결사인 문예운동사를 조직하여 독립운동을 전개한 독립운동가.
    '권오병': {'role': 'other'},  # 현대/대한민국 - 광주지검 검사장, 법무부장관, 문교부장관 등을 역임한 법조인 · 정치인.
    '권오복': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 수찬, 교리 등을 역임한 문신.
    '권오설': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 고려공산청년회 책임비서를 지낸 사회주의운동가, 독립운동가.
    '권오익': {'role': 'scholar'},  # 현대/대한민국 - 성균관대학교 총장, 유네스코 한국위원회 위원 등을 역임하였고, 『상업경제학』, 『국제협력에
    '권오일': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「세일즈맨의 죽음」, 「욕망이라는 이름의 전차」, 「느릅나무 그늘의 욕망」 등을
    '권오직': {'role': 'other'},  # 현대/대한민국 - 북한 인민위원회 외무성 부수상, 북한 주중공 대사 등을 역임한 정치인 · 사회주의 운동가.
    '권오훈': {'role': 'other'},  # 현대/대한민국 - 일제강점기 때, 임시정부와 광복군을 지원하였으며, 해방 이후 호국군 106연대 부연대장, 
    '권옥연': {'role': 'other'},  # 근대/일제강점기 | 현대 - 해방 이후 「고향」 · 「부인상」 · 「꿈」 등을 그린 화가. 서양화가.
    '권완': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 행돈녕부판관 등을 역임하였으며, 단종복위운동에 가담했다는 죄로 처형된 문신.
    '권용': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 응교, 전한, 직제학 등을 역임한 문신.
    '권용일': {'role': 'other'},  # 근대 - 대한제국기 때, 이강년 의진에서 안동의 재산전투 등에 참전하며 항일의병투쟁을 전개한 의병.
    '권용정': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 「보부상」을 그린 화가.
    '권우': {'role': 'other'},  # 조선 - 조선 후기에, 도승지, 한성부좌윤 등을 역임한 문신.
    '권위': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 시랑, 판태복시사, 한림학사 등을 역임한 문신.
    '권유': {'role': 'other'},  # 조선 - 조선 후기에, 공조판서, 좌참찬, 대사헌 등을 역임한 문신.
    '권율': {'role': 'other'},  # 조선 중기에, 의주목사, 도원수 등을 역임한 문신.
    '권응생': {'role': 'other'},  # 조선 - 조선 후기에, 북부주부, 진천현감 등을 역임한 문신.
    '권응선': {'role': 'other'},  # 근대 - 조선 후기에, 사헌부대사헌, 봉상사제조, 강원도관찰사 등을 역임한 문신.
    '권응수': {'role': 'other'},  # 조선 - 조선 중기에, 경상도병마좌별장, 충청도방어사, 경상도방어사 등을 역임한 무신 · 의병장.
    '권응시': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 호조좌랑, 군위현감 등을 역임한 문신.
    '권응심': {'role': 'other'},  # 조선/조선 후기 - 조선시대 임진왜란 의병장으로 호분위 좌부장, 경상좌도 병마우후를 역임한 무신.
    '권응인': {'role': 'novelist'},  # 조선 - 조선 전기에, 『송계집』, 『송계만록』 등을 저술한 문인.
    '권응정': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 경주부윤, 안동부사, 동지중추부사 등을 역임한 문신.
    '권응창': {'role': 'other'},  # 조선 - 조선 전기에, 남양부사, 동지중추부사 등을 역임한 문신.
    '권의': {'role': 'other'},  # 고려 - 고려 후기에, 감찰시사, 판도총량 등을 역임한 관리.
    '권이복': {'role': 'scholar'},  # 조선 - 조선 후기에, 『만주문집』 등을 저술한 학자.
    '권이중': {'role': 'other'},  # 조선 - 조선 후기에, 종묘서직장, 장원서별제, 감찰 등을 역임한 문신.
    '권이진': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 판서, 평안도관찰사 등을 역임한 문신.
    '권익경': {'role': 'other'},  # 조선 - 조선 후기에, 안동부현감, 감찰 등을 역임한 문신.
    '권익관': {'role': 'other'},  # 조선 - 조선 후기에, 충청감사, 공조참의, 함경감사 등을 역임한 문신.
    '권인규': {'role': 'other'},  # 근대 - 대한제국기 때, 관동구군도창의소를 설치하여 관동방면의 의진을 규합한 의병장.
    '권일송': {'role': 'poet'},  # 현대/대한민국 - 해방 이후 『이 땅은 나를 술 마시게 한다』, 『바다의 여자』, 『비비추의 사랑』 등을 저
    '권일신': {'role': 'scholar'},  # 조선 - 조선 후기에, 추조적발사건, 진산사건과 관련된 학자 · 천주교인.
    '권일형': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 의주 부윤, 승지, 병조참판 등을 역임한 문신.
    '권자신': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 좌부승지, 우승지, 호조참판 등을 역임한 문신.
    '권장': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 홍문박사, 검열 등을 역임한 문신.
    '권장수': {'role': 'other'},  # 고려 - 고려 후기에, 판사재시사, 교주도병마사, 밀직부사 등을 역임한 관리 · 공신.
    '권재수': {'role': 'other'},  # 근대 - 조선 후기에, 박영효 암살미수사건과 관련된 정객.
    '권적': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 판서, 판의금부사, 우빈객 등을 역임한 문신.
    '권전': {'role': 'other'},  # 조선 - 조선 전기에, 정언, 이조좌랑, 수찬 등을 역임한 문신.
    '권절': {'role': 'other'},  # 조선 - 조선 전기에, 통정대부, 위장 등을 역임한 문신.
    '권절평': {'role': 'other'},  # 고려 - 고려 후기에, 좌승선, 추밀원사, 참지정사판호부사 등을 역임한 무신.
    '권정생': {'role': 'childrenauthor'},  # 현대/대한민국 - 해방 이후 『강아지똥』, 『몽실언니』 등을 저술한 아동문학가.
    '권정선': {'role': 'scholar'},  # 조선/조선 후기 | 근대/개항기 - 대한제국기 때, 『정음종훈』, 『음경』 등을 저술한 국어학자.
    '권정침': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 세자시강원설서 등을 역임한 문신.
    '권정필': {'role': 'other'},  # 근대/일제강점기 - 일제강점기에 의열단에 입단하여 항일 독립 투쟁을 전개한 독립운동가.
    '권제': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 좌참찬, 우찬성, 문형 등을 역임한 문신.
    '권종': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 개령현감, 금산군수 등을 역임한 문신.
    '권종록': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 사헌부집의, 부사직, 정위 등을 역임한 문신.
    '권종해': {'role': 'other'},  # 근대/대한제국기 | 근대/일제강점기 - 대한제국과 일제강점기에 의병운동과 민족운동을 펼친 독립운동가.
    '권주': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 성균관전적, 공주목사, 성주목사 등을 역임한 문신.
    '권주욱': {'role': 'scholar'},  # 조선 - 조선 후기에, 『동감』, 『포암문집』 등을 저술한 학자.
    '권준': {'role': 'other'},  # 근대 - 대한제국기 때, 경기북부 지역에서 항일의병투쟁을 전개한 의병장.
    '권중경': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 함경도관찰사, 형조참의, 호조참의 등을 역임한 문신.
    '권중도': {'role': 'scholar'},  # 조선 - 조선 후기에, 『퇴암집』, 『금양기선록』, 『노산자경록』 등을 저술한 학자.
    '권중돈': {'role': 'other'},  # 현대/대한민국 - 국방부장관, 민권당 고문 등을 역임한 정치인.
    '권중석': {'role': 'other'},  # 근대 - 정교, 대형호, 원로원 참의 등을 역임한 대종교인.
    '권중원': {'role': 'other'},  # 의병 활동을 적극 지원한 공적으로 2019년 대통령표창을 추서한 독립운동가 · 독립유공자.
    '권중집': {'role': 'other'},  # 조선 - 조선 후기에, 돈령부참봉, 진산군수 등을 역임한 문신.
    '권중현': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 농상공부대신, 법부대신, 군부대신, 자작, 중추원 고문 등을 역임한 관료 
    '권중화': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 판문하부사, 우의정, 영의정부사 등을 역임한 문신 · 의원.
    '권지': {'role': 'other'},  # 조선 - 조선 후기에, 장령, 서장관, 좌부승지 등을 역임한 문신.
    '권진': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 한성판윤, 우참찬, 병조판서 등을 역임한 문신.
    '권진규': {'role': 'scholar'},  # 현대 - 「자각상」, 「소녀의 얼굴」, 「여인상」 등의 작품을 낸 조각가.
    '권진응': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 자의 등을 역임한 문신.
    '권진인': {'role': 'other'},  # 고려 - 고려 전기에, 단학 설화에 나오는 도교인.
    '권질': {'role': 'other'},  # 조선 - 조선 전기에, 집경전, 순릉, 후릉참봉, 광흥창봉사 등을 역임한 문신.
    '권집': {'role': 'other'},  # 조선 - 조선 후기에, 대동찰방, 한성부서윤, 하동부사 등을 역임한 문신.
    '권징': {'role': 'other'},  # 조선 - 조선 중기에, 병조판서, 경기관찰사 등을 역임한 문신.
    '권찬': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 지중추부사, 정헌대부, 호조판서 등을 역임한 문신.
    '권창식': {'role': 'scholar'},  # 조선 - 조선 후기에, 『잠계문집』 등을 저술한 학자.
    '권창진': {'role': 'scholar'},  # 조선 - 조선 후기에, 『아맹일고』 등을 저술한 학자.
    '권채': {'role': 'other'},  # 조선 - 조선 전기에, 대사성, 우승지 등을 역임한 문신.
    '권채근': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 경상남도 진주의 독립만세시위를 주도한 혐의로 체포되어 옥중에서 순국한 독립
    '권척': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 호조좌랑, 예조좌랑, 예문관봉교 등을 역임한 문신.
    '권철': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 우의정, 좌의정, 영의정 등을 역임한 문신.
    '권철신': {'role': 'scholar'},  # 조선/조선 후기 - 조선 후기에, 『시칭』, 『대학설』 등을 저술한 학자 · 천주교인.
    '권첨': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 대사간, 전라도관찰사, 충청도관찰사 등을 역임한 문신.
    '권첩': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 형조참판, 경주부윤 등을 역임한 문신.
    '권총': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 세자익위사의 위솔, 익찬, 지중추부사 등을 역임한 문신.
    '권축': {'role': 'scholar'},  # 근대 - 조선 후기에, 홍문관수찬, 시강원 겸 문학, 이조정랑 등을 역임한 문신.
    '권춘란': {'role': 'other'},  # 조선 - 조선 중기에, 성균관사성, 청송부사, 홍문관수찬 등을 역임한 문신.
    '권충': {'role': 'other'},  # 조선 - 조선 전기에, 우군동지총제, 공조판서, 의정부찬성사 등을 역임한 문신.
    '권치문': {'role': 'other'},  # 근대 - 개항기 때, 약현천주교회를 기공한 천주교인.
    '권칭': {'role': 'other'},  # 조선 - 조선 후기에, 성균관사예 등을 역임한 문신.
    '권쾌복': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 대구사범학교 학생의 항일 비밀결사인 다혁당 당수로 활동한 독립운동가.
    '권태석': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 조선민흥회와 신간회, 조선공산당 등에서 활동한 사회주의운동가, 독립운동가, 정치
    '권태시': {'role': 'other'},  # 조선 - 조선 후기에, 장악원주부, 회덕현감 등을 역임한 문신.
    '권태양': {'role': 'other'},  # 현대/대한민국 - 해방 이후 좌우합작위원회 서무부장, 민족자주연맹 비서처 총무, 중앙집행위원 등을 역임한 정
    '권태완': {'role': 'scholar'},  # 현대/대한민국 - 국내 식품 과학 연구를 국제적 수준으로 발전시킨 학자.
    '권태욱': {'role': 'other'},  # 현대/대한민국 - 제헌국회의원, 제2대 국회의원을 역임한 정치인.
    '권태일': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 형조참판 등을 역임한 문신.
    '권태하': {'role': 'other'},  # 현대 - 조선마라톤보급회 위원장, 대한육상경기연맹 회장 등을 역임한 체육인.
    '권태호': {'role': 'other foreigner'},  # 근대/일제강점기 - 1930년 3월 일본 니혼[日本]음악학교를 졸업한 테너 성악가로 일제강점기 「봄나들이」, 
    '권태훈': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 『민족비전 정신수련법』 · 『천부경의 비밀과 백두산족 문화』 등을 저술하며 단학
    '권태희': {'role': 'other'},  # 현대/대한민국 - 제헌국회의원, 문교사회분과위원장 등을 역임한 정치인 · 종교인.
    '권필': {'role': 'poet'},  # 조선 - 조선 중기의 시인.
    '권필칭': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 선전관, 장기현감, 삭주부사, 평안도방어사, 경상좌도수군절도사 등을 지낸 무관.
    '권한공': {'role': 'other'},  # 고려 - 고려 후기에, 찬성사, 도첨의정승, 태자좌찬선 등을 역임한 문신.
    '권한성': {'role': 'other'},  # 조선 - 조선 후기에, 사헌부지평, 이조정랑, 대동찰방 등을 역임한 문신.
    '권해': {'role': 'other'},  # 조선 - 조선 후기에, 대사헌, 호조참의, 평양부윤 등을 역임한 문신.
    '권행': {'role': 'other'},  # 고려 - 고려 전기에, 고려와 후백제의 고창전투에서 고려군에 가담하여 공을 세워, 태조 왕건으로부터
    '권헌': {'role': 'other'},  # 조선 - 조선 전기에, 사섬시직장, 장악원직장, 지평 등을 역임한 문신.
    '권혁': {'role': 'other'},  # 조선 - 조선 후기에, 함경도관찰사, 대사헌, 이조판서 등을 역임한 문신.
    '권현룡': {'role': 'other'},  # 고려 - 고려 후기에, 밀직부사, 강릉도부원수, 판덕창부사 등을 역임한 무신.
    '권협': {'role': 'other'},  # 조선 - 조선 중기에, 대사헌, 전라도감사, 예조판서 등을 역임한 문신.
    '권형': {'role': 'other'},  # 조선 - 조선 중기에, 장악원첨정, 세자시강원필선, 예빈시부정 등을 역임한 문신.
    '권호문': {'role': 'novelist'},  # 조선/조선 전기 - 조선 전기에, 「독락팔곡」, 「한거십팔곡」, 『송암집』 등을 저술한 문인.
    '권호윤': {'role': 'scholar'},  # 조선 - 조선 후기에, 『동빈만록』 등을 저술한 학자.
    '권홍': {'role': 'other'},  # 고려 - 조선 전기에, 판돈령부사, 예조판서, 영돈령부사 등을 역임한 문신.
    '권화': {'role': 'other'},  # 고려 - 조선 전기에, 도성제조, 삼사우복야 등을 역임한 문신.
    '권확': {'role': 'other'},  # 조선 - 조선 후기에, 여주목사, 좌부승지, 동부승지 등을 역임한 문신.
    '권환': {'role': 'poet'},  # 근대 - 일제강점기 때, 『자화상』, 『윤리』 등을 저술한 시인.
    '권황': {'role': 'other'},  # 조선 - 조선 후기에, 고양군수, 마전군수, 지중추부사 등을 역임한 문신.
    '권흠': {'role': 'other'},  # 조선 - 조선 후기에, 대사성, 이조참의, 승지 등을 역임한 문신.
    '권희': {'role': 'other'},  # 조선 - 조선 중기에, 도승지, 한성부좌윤, 형조참판 등을 역임한 문신.
    '권희맹': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 나주목사, 장악원정, 강원도관찰사 등을 역임한 문신.
    '권희인': {'role': 'other'},  # 조선 - 조선시대 때, 서천포만호, 옥천군수 등을 역임한 무신.
    '권희학': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 곤양군수, 운산군수, 장연부사 등을 역임한 무신 · 공신.
    '궤홍': {'role': 'other'},  # 조선 - 조선 후기에, 보월사 해원의 제자가 되어 법맥을 계승한 승려.
    '귀금': {'role': 'other'},  # 고대/남북국 - 신라 헌강왕 때 거문고의 명인.
    '귀보부인': {'role': 'other'},  # 고대/남북국/통일신라 - 신라의 제44대 왕, 민애왕의 어머니로, 선의태후로 추봉된 왕족.
    '귀산': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 신라의 아막성전투에 참전한 장수.
    '귀승부인': {'role': 'other'},  # 고대/남북국/통일신라 - 신라의 제41대 왕, 헌덕왕의 왕비.
    '귀실집사': {'role': 'other foreigner'},  # 고대/삼국/백제 - 남북국시대 때, 일본에 망명한 백제의 유민.
    '귀실집신': {'role': 'other foreigner'},  # 고대/삼국 - 삼국시대 때, 일본에서 활동한 백제의 의원.
    '귀지': {'role': 'other foreigner'},  # 고대/삼국 - 삼국시대 때, 백제의 사신으로 일본에 구원병을 요청한 부흥운동가.
    '귀진': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 신라의 법왕사를 창건한 관리.
    '균여': {'role': 'scholar'},  # 고려전기 「보현십원가(普賢十願歌)」, 『수현방궤기(搜玄方軌記)』, 『공목장기(孔目章記)』 
    '극상': {'role': 'other'},  # 고대/남북국 - 통일신라 효공왕 때, 아버지인 안장에게 거문고 비법을 전수받은 거문고 명인.
    '극정': {'role': 'other'},  # 고대/남북국 - 남북국시대 때, 통일 신라의 사찬을 역임한 장수.
    '극종': {'role': 'other'},  # 고대/남북국 - 남북국시대 때, 통일 신라에서 아버지인 안장에게 「표풍」 등을 전수받은 거문고 명인.
    '극현': {'role': 'other'},  # 조선 - 조선 후기에, 대흥사 신월선사의 제자가 되어 법맥을 계승한 승려.
    '근구수왕': {'role': 'other'},  # 고대/삼국 - 백제의 제14대(재위:375년~384년) 왕.
    '근랑': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 이찬 관등이었던 대일의 아들로, 많은 낭도들을 거느린 신라의 화랑.
    '근비': {'role': 'other'},  # 고려 - 고려의 제32대 왕, 우왕의 왕비.
    '근적': {'role': 'other'},  # 조선 - 조선 후기에, 대흥사 주지가 되어 가선대부의 품계를 받은 승려.
    '근종': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 때, 신라의 이찬 관등을 역임한 귀족, 반란자.
    '근초고왕': {'role': 'other'},  # 백제의 제13대(재위:346년~375년) 왕.
    '근헌': {'role': 'other'},  # 근대 - 개항기 때, 취암의 제자이자 초의로부터 보살계를 받은 승려.
    '금강': {'role': 'other'},  # 고대/남북국 - 남북국시대 때, 후백제의 시조인 견훤의 넷째 왕자.
    '금관후': {'role': 'other'},  # 고려/고려 전기 - 고려 전기, 제11대 왕 문종의 아들인 왕자.
    '금기철': {'role': 'other'},  # 근대 - 대한제국기 때, 경상북도와 영동지역에서 항일의병투쟁을 전개한 의병장.
    '금난수': {'role': 'other'},  # 조선 - 조선 중기에, 직장, 장례원사평, 봉화현감 등을 역임하였으며, 정유재란이 발발하자 의병을 
    '금능인': {'role': 'other'},  # 근대 - 일제강점기 「타향살이」, 「휘파람」, 「사막의 한」 등을 작사한 음악인.
    '금달연': {'role': 'other'},  # 근대 - 대한제국기 때, 경상북도 영주에서 의병을 조직하였다가, 이강년 의병부대에 들어가 별초종사,
    '금룡': {'role': 'other'},  # 현대/대한민국 - 운문사 주지를 역임한 승려.
    '금보': {'role': 'scholar'},  # 조선 - 조선 전기에, 『사서질의』, 『심근강의』, 『매헌집』 등을 저술한 학자.
    '금사': {'role': 'other'},  # 고대/남북국 - 남북국시대 때, 당나라에서 유학하여 대승과 소승의 경전을 공부한 승려.
    '금석주': {'role': 'other'},  # 근대 - 개항기 때, 경상북도 봉화에서 의병을 조직하였다가, 유인석 의진에 들어가 소토장으로 활동한
    '금선자': {'role': 'other'},  # 조선 - 조선 선조 때, 전란의 조짐을 보고 전쟁 발발을 예언한 도교인.
    '금성규': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 진사, 전적, 사예 등을 역임한 문신 · 서예가.
    '금성대군': {'role': 'other'},  # 조선/조선 전기 - 조선의 제4대 왕, 세종의 여섯번째 왕자.
    '금수현': {'role': 'other'},  # 현대/대한민국 - 오페라 「피리와 칼」, 「그네」 등을 작곡한 음악가.
    '금시양': {'role': 'scholar'},  # 조선 - 조선 후기에, 『가례부해』, 『삼기당문집』 등을 저술한 학자.
    '금식': {'role': 'other'},  # 고대/남북국 - 남북국시대 때, 태봉국의 사화진(沙火鎭)전투(戰鬪)에 참전한 장수.
    '금와': {'role': 'other'},  # 고대/초기국가 - 부여의 제4대(재위: BCE.60~BCE.20) 왕.
    '금용': {'role': 'other'},  # 고대/남북국 - 남북국시대 때, 평양에서 평양성주장군으로 세력을 떨친 호족.
    '금원 김씨': {'role': 'poet'},  # 조선 - 조선후기 『죽서시집』 발문, 『호동서락기』 등을 저술한 시인.
    '금원군': {'role': 'other'},  # 조선 - 조선의 제11대 왕, 중종의 서자인 왕자.
    '금월': {'role': 'other'},  # 조선 - 조선후기 사교과와 『화엄경』, 『사분율』, 『범망경』 등을 공부한 승려.
    '금윤선': {'role': 'other'},  # 조선 - 조선 중기에, 의서습독관, 훈련원정 등을 역임하였으며, 임진왜란 때 의병장으로 활약한 무신
    '금응협': {'role': 'other'},  # 조선 - 조선 중기에, 집경전참봉, 하양현감 등을 역임한 문신.
    '금응훈': {'role': 'other'},  # 조선 - 조선 중기에, 영춘현감, 양천현감, 의흥현감 등을 역임한 문신.
    '금의': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 풍기군수, 청송부사 등을 역임한 문신.
    '금이영': {'role': 'other'},  # 조선 - 조선 전기에, 승문원부교리, 청주판관, 승문원교리 등을 역임한 문신.
    '금일': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 때, 신라의 대야성전투 당시 사지 등을 역임했던 관리.
    '금주리': {'role': 'other foreigner'},  # 고대/삼국/백제 - 삼국시대 때, 일본 와카야마현 구마모토시에 있는 우전팔번신사 소장 인물화상경을 제작한 백제
    '금훈': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 각문부사, 초유사 등을 역임한 문신.
    '금휘': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 동북면병마사, 대장군 등을 역임한 무신.
    '급리': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 때, 신라의 아찬으로 내외병마사를 담당한 관리.
    '긍법': {'role': 'other'},  # 근대/개항기 - 대한제국기 봉원사 대웅전 극락구품도, 불암사 대웅전 아미타불도 등의 불화를 제작한 승려. 
    '긍선': {'role': 'other'},  # 조선 - 19세기에, 초의 의순(草衣意恂)과 선 논쟁을 펼친 것으로 유명한 호남의 선승.
    '긍양': {'role': 'other'},  # 고려 - 삼국시대 신라의 구산선문 중 희양산문(曦陽山門)을 대표하는 승려.
    '긍엽': {'role': 'other'},  # 근대/개항기 - 대한제국기 영지사 「지장보살도」 · 「신중도」 등을 그린 화가. 승려.
    '긍척': {'role': 'other'},  # 조선/조선 후기 - 조선후기 흥국사 응진전 석가모니불도, 흥국사 관음전 관음보살도, 송광사 오십전 53불도 등
    '긍탄': {'role': 'other'},  # 현대/대한민국 - 일제강점기 때, 보문사 주지를 역임한 승려.
    '기건': {'role': 'other'},  # 조선 - 조선 전기에, 인순부윤, 평안도관찰사, 판중추원사 등을 역임한 문신.
    '기대승': {'role': 'other'},  # 조선 - 조선 전기에, 성균관대사성, 대사간, 공조참의 등을 역임한 문신.
    '기대정': {'role': 'other'},  # 조선 - 조선 중기에, 지평, 장령 등을 역임한 문신.
    '기대항': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 이조참판, 한성부판윤 등을 역임한 문신.
    '기루왕': {'role': 'other'},  # 고대/삼국 - 백제의 제3대(재위: 77년~128년) 왕.
    '기륜': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에 삼사좌사 · 찬성사 · 덕산부원군 등을 역임하였으며, 동생인 기황후의 권세를 
    '기림이사금': {'role': 'other'},  # 고대/삼국 - 신라의 제15대(재위: 298년~310년) 왕.
    '기마차': {'role': 'other'},  # 고대/삼국 - 백제 6세기 인물로 왜(倭)의 궁중에 파견된 악사(樂師).
    '기만헌': {'role': 'other'},  # 조선 - 조선 후기에, 정언, 지평, 부사 등을 역임한 문신.
    '기보갈문왕': {'role': 'other'},  # 고대/삼국 - 신라의 제19대 왕, 눌지마립간의 동생이자 제22대 지증왕의 아버지로, 습보와 동일인으로 
    '기본한기': {'role': 'other'},  # 고대/삼국/가야 - 대가야의 왕.
    '기산도': {'role': 'other'},  # 근대/대한제국기 - 대한제국기 때, 을사조약이 강제 체결되자 결사대를 조직하여 을사오적 암살을 계획한 독립운동
    '기삼만': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 원나라 기황후의 족제(族弟)인 권신.
    '기삼연': {'role': 'other'},  # 근대 - 대한제국기 때, 호남창의맹소의 대장으로 활약하며 항일의병투쟁을 전개한 의병장.
    '기새인티무르': {'role': 'other'},  # 고려 - 고려 후기에, 권신이었던 기철(奇轍)의 아들로 태어나 원나라 평장 등을 역임한 관리.
    '기석복': {'role': 'other'},  # 현대/대한민국 - 해방 이후 북한에서 공산당 중앙위원 등을 역임한 정치인. 공산주의자.
    '기수발': {'role': 'other'},  # 조선 - 조선 후기에, 홍문관정자, 예조좌랑, 정언 등을 역임한 문신.
    '기순격': {'role': 'other'},  # 조선 - 조선 후기에, 해남현감, 장흥부사 등을 역임한 문신.
    '기양연': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 사복시정, 부교리, 부수찬 등을 역임한 문신.
    '기언정': {'role': 'other'},  # 조선 - 조선 후기에, 대사간, 대사헌, 공조판서 등을 역임한 문신.
    '기연': {'role': 'other'},  # 조선/조선 후기 - 조선후기 송광사 천자암 지장시왕도, 흥국사 극락암 칠성도 등의 불화를 제작한 승려. 화승(
    '기오공': {'role': 'other'},  # 고대/삼국 - 신라 진지왕의 비, 지도부인의 부친인 귀족.
    '기온': {'role': 'other'},  # 고려/고려 후기 - 고려 후기 국왕 원종의 측근 세력으로 활약한 무신.
    '기용숙': {'role': 'scholar'},  # 현대 - 서울대학교 의과대학 미생물학 교수를 역임한 미생물학자.
    '기우만': {'role': 'other'},  # 근대 - 개항기 때, 호남지방에서 기삼연과 합세하여 호남창의 총수로 활약한 의병장.
    '기원': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 한림학사, 원사 등을 역임하였으며, 동생인 기황후의 권세를 믿고 횡포를 일삼
    '기윤숙': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 문하시랑 동중서문하평장사, 문하시랑평장사 등을 역임한 무신.
    '기윤위': {'role': 'other'},  # 고려 - 고려 후기에, 지유, 대장군, 가발병마사 등을 역임한 무신.
    '기윤헌': {'role': 'scholar'},  # 조선 - 조선 후기에, 세자시강원문학, 장령, 안악군수 등을 역임한 문신.
    '기의헌': {'role': 'scholar'},  # 조선 - 조선 후기에, 『기은유고』 등을 저술하였으며, 정묘호란과 병자호란이 발발하자 의병을 일으켜
    '기익헌': {'role': 'other'},  # 조선 - 조선시대 때, 이괄의 난에 가담한 장수.
    '기인보': {'role': 'other'},  # 고려/고려 후기 - 고려후기 거란유종의 침입 당시의 관리. 무신.
    '기자오': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 산원, 총부산랑, 영안왕 등을 역임한 무신.
    '기자헌': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 좌승지, 강원도관찰사, 좌의정 등을 역임한 문신.
    '기재': {'role': 'scholar'},  # 조선 - 조선 후기에, 『식재집』 등을 저술한 학자.
    '기전': {'role': 'other'},  # 조선/조선 후기 - 개항기 합천 해인사 대광전 삼신불도, 부산 범어사 석가26보살도 등의 불화를 제작한 승려.
    '기전해': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 가야연맹 반피국의 상수위를 역임한 귀족.
    '기정룡': {'role': 'scholar'},  # 조선 - 조선 후기에, 『낙암유고』 등을 저술한 학자.
    '기정진': {'role': 'scholar'},  # 조선/조선 후기 - 조선 후기에, 「정자설」, 「이통설」, 『노사집』, 『답문유편』 등 중요한 성리학 저술을 
    '기존정': {'role': 'other'},  # 고려 - 고려 후기에, 연주에서 김취려와 군사를 이끌고 거란군을 물리쳐 대승을 거둔 무신.
    '기종': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 신라의 사찬으로 감문주군주를 역임한 지방관.
    '기준': {'role': 'other'},  # 조선 - 조선 전기에, 장령, 시강관, 응교 등을 역임한 문신.
    '기준격': {'role': 'other'},  # 조선 - 조선 후기에, 정언, 병조좌랑, 예조좌랑 등을 역임한 문신.
    '기철': {'role': 'other'},  # 고려/고려 후기 - 고려 후기 요양행성 평장정사를 역임한 부원세력.
    '기탁성': {'role': 'other'},  # 고려 - 고려 후기에, 판병부사, 문하시랑평장사 판이부사 등을 역임한 무신.
    '기학경': {'role': 'other'},  # 조선 - 조선 후기에, 사간원정언, 무장현감, 홍문관수찬 등을 역임한 문신.
    '기현': {'role': 'other'},  # 고려 - 고려 후기에, 신돈의 심복이 되어 횡포를 부린 권신.
    '기협': {'role': 'other'},  # 조선 - 조선 후기에, 황해도관찰사, 선천부사 등을 역임한 문신.
    '기형도': {'role': 'poet'},  # 해방 이후 「안개」, 『입 속의 검은 잎』 등을 저술한 시인.
    '기홍': {'role': 'other'},  # 조선 - 조선후기 월출산 장선을 은사로 득도하고 성옥의 법맥을 계승한 승려.
    '기홍석': {'role': 'other'},  # 고려 - 고려후기 군부판서 응양군상장군, 밀직부사, 동지밀직사 감찰제헌 등을 역임한 무신.
    '기홍수': {'role': 'other'},  # 고려/고려 후기 - 고려후기 문하시랑 동중서문하 평장사, 벽상삼한삼중대광 문하시랑 동중서문하평장사 판이부사 등
    '기홍연': {'role': 'scholar'},  # 조선 - 조선 후기에, 『주서표기』, 『용산유고』 등을 저술한 학자.
    '기화': {'role': 'other'},  # 조선/조선 전기 - 조선 초기 불교계를 대표하는 선승이자 학승으로 호불 논서  『현정론』의 저자.
    '기황후': {'role': 'other'},  # 고려/고려 후기 - 고려 후기, 몽골제국 제14대 카안 순제 토곤테무르의 황후.
    '기효간': {'role': 'scholar'},  # 조선 - 조선 중기에, 벼슬에 오르지 않고 학문과 후진 양성에 전념하여 호남의 은덕군자로 불린 학자
    '기효근': {'role': 'other'},  # 조선 - 조선시대 남해현령, 통정대부 등을 역임한 무신.
    '기효증': {'role': 'scholar'},  # 조선 - 조선 중기에, 형조정랑, 군기시첨정 등을 역임하였으며, 임진왜란이 발발하자 의병을 일으켜 
    '기훤': {'role': 'other'},  # 고대/남북국 - 남북국시대 통일신라의 조정에 반기를 들어 죽주에서 반란을 일으킨 호족. 반란자.
    '길나': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라 중대의 장수.
    '길달': {'role': 'other'},  # 고대/삼국 - 삼국시대 신라의 진평왕 때 도깨비가 인간으로 나타난 전설의 인물로 집사를 담당한 관리.
    '길문': {'role': 'other'},  # 고대/삼국 - 삼국시대 신라의 아찬, 파진찬 등을 역임한 관리.
    '길삼봉': {'role': 'other'},  # 조선/조선 전기 - 조선 전기 선조대 정여립 사건의 연루자 심문 과정에서 언급되었던 가상의 인물.
    '길선': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 아찬으로 모반에 실패해 백제로 건너간 관리.
    '길선주': {'role': 'other'},  # 근대 - 일제강점기 장대현교회에서 시무한 목사.
    '길숙': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 신문왕 납비 때 시비를 궁내로 모셔오는 임무를 수행한 관리.
    '길영수': {'role': 'other'},  # 근대 - 개항기 과천군수, 한성부판윤 등을 역임한 관리.
    '길영희': {'role': 'other'},  # 현대/대한민국 - 해방 이후 인천중학교 교장, 제물포고등학교 교장 등을 역임한 교육자.
    '길옥윤': {'role': 'other'},  # 해방 이후 「서울의 찬가」, 「사랑은 영원히」, 「당신은 모르실거야」 등을 발표한 작곡가.
    '길운절': {'role': 'other'},  # 조선/조선 후기 - 조선후기 정여립의 모반군에 모사로 참여한 주모자.
    '길원': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 아찬(阿飡) 관등의 관리.
    '길의': {'role': 'scholar'},  # 고대/남북국/통일신라 - 남북국시대 『추일어장왕택연신라객』, 『종가길야궁』 등을 저술한 통일신라의 승려. 의관.
    '길인': {'role': 'other'},  # 고려/고려 후기 - 고려 후기, 상장군으로 최충헌의 정변에 저항하였던 이의민 계의 무신.
    '길인화': {'role': 'other'},  # 조선 - 조선 후기에, 상서원직장, 사축서별제, 통례원인의 등을 역임한 문신.
    '길재': {'role': 'scholar'},  # 조선/조선 전기 - 조선 전기에, 『야은집』, 『야은속집』, 『야은언행습유록』 등을 저술하였으며, 이색, 정몽
    '길재호': {'role': 'other'},  # 현대/대한민국 - 해방 이후 5, 16군사정변 당시의 군인. 정치인.
    '길진섭': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 「옹진바다 전망」 · 「농촌의 모녀상 」 · 「바닷가 풍경」 등의 작품을 그린 
    '길진형': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 신성학교 교사를 역임한 교육자.
    '길회': {'role': 'other'},  # 조선 - 조선 중기에, 직강, 헌납, 장령 등을 역임한 문신.
    '김가기': {'role': 'other'},  # 고대/남북국 - 삼국시대 신라에 도교를 전한 최초의 도교인. 문장가.
    '김가진': {'role': 'other'},  # 근대 - 개항기 농상공부대신, 중추원의장 등을 역임한 관리.
    '김각': {'role': 'other'},  # 조선 - 조선 중기에, 용궁현감, 온성판관 등을 역임한 문신.
    '김각현': {'role': 'other'},  # 근대 - 조선 후기에, 제실회계심사국장, 대원왕대원비원침천봉시검찰당상 등을 역임한 문신.
    '김간': {'role': 'other'},  # 조선 - 조선 후기에, 청나라에서 내무부주사, 사고전서관부총재 등을 역임한 문신.
    '김감': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 경상도 도사 등의 관직을 역임한 문신.
    '김감불': {'role': 'other'},  # 조선/조선 전기 - 조선전기 단천연은법을 개발한 기술자.
    '김갑': {'role': 'other'},  # 근대 - 일제강점기 때, 임시정부에서 법무총장 대리, 노동총판, 국무위원 등을 역임한 독립운동가.
    '김갑수': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 내무부 차관, 대법원 대법관, 경성대학교 법문학부 교수 등을 역임한 법조인. 정
    '김갑순': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 중추원참의, 유성온천주식회사 사장, 조선임전보국단 이사 등을 역임한 기업인. 정
    '김갑우': {'role': 'other'},  # 고려 - 고려후기 천우위대장군, 대호군 등을 역임한 무신.
    '김갑태': {'role': 'other'},  # 현대/대한민국 - 한국전쟁 당시 강원도 김화의 748고지전투(피의 능선전투)에 참전한 군인.
    '김강': {'role': 'other foreigner'},  # 근대 - 일제강점기 때, 간민회 일본조사부원, 동제회 평의원, 대한국민회 중부경호부장 등을 역임한 
    '김개': {'role': 'other'},  # 조선 - 조선 후기에, 승지, 좌윤 등을 역임한 문신.
    '김개국': {'role': 'other'},  # 조선 - 조선 중기에, 정랑, 군수 등을 역임한 문신.
    '김개남': {'role': 'other'},  # 근대/개항기 - 19세기 후반 동학농민운동 당시 호남창의소 총관령 등을 역임한 동학교단의 호남 대접주.
    '김개물': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 감찰사, 사헌지평, 전부시승 등을 역임한 문신.
    '김개시': {'role': 'other'},  # 조선/조선 후기 - 조선후기 제15대 광해군의 총애를 받아 권세를 누린 궁녀.
    '김개원': {'role': 'other'},  # 고대/남북국 - 삼국시대 신라 제29대 태종무열왕의 일곱째 아들인 왕자.
    '김거공': {'role': 'other'},  # 고려 - 고려 전기에, 판삼사사, 지문하성사, 호부상서 등을 역임한 문신.
    '김거두': {'role': 'other'},  # 고려 - 조선 전기에, 『삼국사기』의 발문을 작성한 문신.
    '김거복': {'role': 'other'},  # 근대/대한제국기 - 조선후기 「수궁가」 중 용왕탄식대목에 뛰어났던 판소리의 명창.
    '김거실': {'role': 'scholar'},  # 고려 - 고려 전기에, 내시 대부소경 태자문학, 태자궁의 행궁별감 등을 역임한 문신.
    '김거웅': {'role': 'other'},  # 고려/고려 전기 - 고려전기 거돈사지의 「거돈사원공국사승묘탑비문」을 쓴 서예가.
    '김건': {'role': 'playwright novelist'},  # 근대 - 해방 이후 「눈물의 38선」 · 「한강물은 흐른다」 · 「직공」 등의 작품을 낸 극작가.
    '김건수': {'role': 'other'},  # 조선 - 조선 후기에, 홍문관응교, 김해부사, 승정원우부승지 등을 역임한 문신.
    '김건순': {'role': 'scholar'},  # 조선 - 조선후기 『천당지옥론』 · 『성교전서』 등을 저술한 천주교인.
    '김건안': {'role': 'other foreigner'},  # 남북국시대 통일신라의 일길찬으로 일본에 파견된 관리.
    '김건종': {'role': 'other'},  # 조선/조선 후기 - 조선후기 「호리건곤도」를 그린 화가.
    '김견수': {'role': 'other'},  # 조선/조선 전기 - 조선전기 평안도절도사, 전주부윤 등을 역임한 무신.
    '김겸': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 공안부윤, 정헌대부, 경상도관찰사 등을 역임한 문신.
    '김겸광': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 예조판서, 경상도관찰사, 평안도절도사 등을 역임한 문신.
    '김경': {'role': 'other'},  # 고려/고려 후기 - 고려후기 무진정변과 관련된 환관.
    '김경구': {'role': 'other'},  # 조선/조선 후기 - 조선후기 첨지중추부사를 역임한 의관. 화가.
    '김경근': {'role': 'other'},  # 조선 - 조선 중기에, 왜적의 침입을 예측하고 산성 수축을 건의하였다가 투옥되었으며, 임진왜란이 발
    '김경남': {'role': 'other'},  # 근대 - 조선후기 거문고 삼절 중 하나인 거문고명인.
    '김경로': {'role': 'other'},  # 조선/조선 후기 - 조선후기 경성판관, 김해부사, 첨지중추부사 등을 역임한 무신.
    '김경문': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 조선과 청나라 간의 외교적 사안을 담당한 역관.
    '김경배': {'role': 'other'},  # 현대/대한민국 - 일제강점기 때, 반일투쟁 혐의로 2년간 복역하였으며 한국전쟁 때 납북되어 북한에서, 재북평
    '김경복': {'role': 'other'},  # 조선 - 조선시대 군수, 부사 등을 역임한 무신.
    '김경부': {'role': 'other'},  # 고려 - 고려후기 김사미와 효심의 난과 관련된 무신.
    '김경서': {'role': 'other'},  # 조선 - 조선시대 전라도병마절도사, 정주목사, 평안도병마절도사 등을 역임한 무신.
    '김경석': {'role': 'other'},  # 조선 - 조선시대 전라도수군도절제사, 전라우도방어사 등을 역임한 무신.
    '김경선': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 우참찬, 판의금부사 등을 역임한 문신.
    '김경손': {'role': 'other'},  # 고려/고려 후기 - 고려 후기, 전라도지휘사 · 추밀원지주사 · 추밀원부사 등을 역임한 무신.
    '김경수': {'role': 'other'},  # 조선 - 조선 중기에, 장악원주부, 예조좌랑, 군자감정 등을 역임하였으며, 임진왜란이 발발하자 의병
    '김경숙': {'role': 'other'},  # 현대/대한민국 - 대한민국의 노동운동가로, 1970년대 YH무역 노동조합에서 민주노조운동을 전개한 인물.
    '김경승': {'role': 'scholar'},  # 근대/일제강점기|현대 - 해방 이후 「충무공 이순신장군상」 · 「안중근의사상」 · 「세종대왕상」 등의 작품을 낸 조
    '김경여': {'role': 'other'},  # 조선 - 조선 후기에, 대사간, 충청도관찰사 등을 역임한 문신.
    '김경용': {'role': 'other'},  # 고려 - 고려 전기에, 문하시중, 수태부 판상서이부사 등을 역임한 문신.
    '김경운': {'role': 'other'},  # 근대 - 대한제국기 때, 박래병 의병군으로 활동하며 군자금 모금 및 무장투쟁을 전개한 의병.
    '김경원': {'role': 'other'},  # 근대/일제강점기 | 현대 - 해방 이후 대한민국미술전람회 심사위원을 역임한 화가.
    '김경유': {'role': 'scholar'},  # 조선 - 조선 후기에, 동지중추부사, 오위장 등을 역임하였으며, 『노은유고』를 저술한 문신.
    '김경장': {'role': 'scholar'},  # 조선 - 조선 후기에, 『예원집설』, 「천문성상도」, 『구암문집』 등을 저술한 학자.
    '김경재': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 독립신문 기자, 신한독립당 비서과장, 조선지광 기자 등을 역임한 언론인. 사회주
    '김경제': {'role': 'other'},  # 고려 - 고려후기 홍건적의 난 당시의 무신.
    '김경지': {'role': 'other'},  # 조선 - 조선 후기에, 병조정랑, 강원도도사, 개성경력 등을 역임한 문신.
    '김경직': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 낭천현감, 병조좌랑, 사도시정 등을 역임한 문신.
    '김경징': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 도승지, 한성부판윤, 강도검찰사 등을 역임한 문신.
    '김경탁': {'role': 'scholar foreigner'},  # 현대/대한민국 - 고려대학교 철학과 교수로 재임해 동양철학학풍을 이끈 중국철학 분야의 개척자로, 『유교철학사
    '김경태': {'role': 'other'},  # 근대 - 일제강점기 때, 대한제국 군인 출신으로, 의병으로 활동하다가 대한광복회에서 군자금 모집 활
    '김경희': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 숭의여학교 교사로 근무하면서 비밀결사인 송죽회를 조직하고, 평양 만세시위를
    '김계': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 병조참지, 승문원부제조, 이조참판 등을 역임한 문신.
    '김계광': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 성균관직강, 춘추관편수관, 풍기군수 등을 역임한 문신.
    '김계금': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 지평, 의성현령, 집현전권지학유 등을 역임한 문신.
    '김계락': {'role': 'other'},  # 조선 - 조선 후기에, 형조판서, 예조판서, 우참찬 등을 역임한 문신.
    '김계명': {'role': 'other'},  # 고대/남북국/통일신라 - 통일신라의 제48대 경문왕의 아버지로, 파진찬에 임명되어 집사성시중 등을 역임한 왕족.
    '김계봉': {'role': 'other'},  # 고려 - 고려후기 명주부사를 역임한 무신.
    '김계부': {'role': 'other'},  # 고려/고려 전기 - 고려전기 좌우기군장군, 병부시랑 등을 역임한 관리. 무신.
    '김계선': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 이왕직 아악수를 역임한 음악인. 대금명인.
    '김계숙': {'role': 'scholar'},  # 현대/대한민국 - 서울대학교 문리과대학과 사범대학 교수로 재임하였으며, 『근세문화사』, 『근세철학사』, 『헤
    '김계우': {'role': 'other'},  # 조선 - 조선 전기에, 참상판관, 청도군수, 공조참판 등을 역임한 문신.
    '김계종': {'role': 'other'},  # 조선/조선 전기 - 조선전기 영안남도병마절도사, 동지중추부사, 겸사복장 등을 역임한 무신.
    '김계지': {'role': 'other'},  # 조선/조선 전기 - 조선전기 판해주목사, 강원도병마도절제사 등을 역임한 무신.
    '김계창': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 우승지, 도승지, 이조참판 등을 역임한 문신.
    '김계하': {'role': 'other'},  # 조선 - 조선 후기에, 의주부윤, 개성유수, 함경도관찰사 등을 역임한 문신.
    '김계행': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 고령현감, 홍문관부수찬, 대사간 등을 역임한 문신.
    '김계휘': {'role': 'other'},  # 조선 - 조선 전기에, 동지의금부사, 평안도관찰사, 예조참판 등을 역임한 문신.
    '김고': {'role': 'other'},  # 고려 - 고려 전기에, 지추밀원사, 중서시랑평장사 등을 역임한 문신.
    '김곡': {'role': 'scholar'},  # 고대/남북국/통일신라 - 남북국시대 때, 숙위학생으로 당나라에서 유학한 통일신라의 학자.
    '김곤': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 선전관, 부령부사, 경원부사 등을 역임한 문신.
    '김공량': {'role': 'other'},  # 조선 - 조선 중기에, 내수사별좌 등을 역임한 문신.
    '김공망': {'role': 'other'},  # 조선 - 조선 전기에, 사간원, 병조좌랑, 해주목사 등을 역임한 문신.
    '김공석': {'role': 'other'},  # 고려 - 고려 후기 중랑장, 분도장군 등을 역임한 무신.
    '김공정': {'role': 'other'},  # 고려 - 고려 전기, 묘청의 난에 가담한 의관.
    '김공천': {'role': 'poet'},  # 현대/대한민국 - 해방 이후 『한라의 바람노래』를 저술한 시인.
    '김관': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 동지중추부사, 전주부윤, 전라도관찰사 등을 역임한 문신.
    '김관석': {'role': 'other'},  # 현대/대한민국 - 해방 이후 한국기독교 교회협의회 총무, 기독교방송 사장 등을 역임한 목사. 사회운동가, 민
    '김관성': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 광한단, 모험대 등을 조직해 항일투쟁을 전개하였으며, 대한통의부 검무감 등
    '김관식': {'role': 'poet'},  # 현대/대한민국 - 해방 이후 「귀양가는 길」 · 「다시 광야에」 · 「춘잠에게」 등을 저술한 시인.
    '김관오': {'role': 'other'},  # 근대 - 일제강점기 때, 한국독립당 충칭지구당부위원장, 임시정부 경위대 대장 등을 역임한 독립운동가
    '김관의': {'role': 'scholar'},  # 고려 - 고려 후기에, 검교군기감 등을 역임하였으며, 『편년통록』을 저술한 관리.
    '김관장': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 대아찬, 총관 등을 역임한 관리.
    '김관주': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 이조판서, 광주유수, 우의정 등을 역임한 문신.
    '김관준': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 서도소리 명창으로 「배뱅이굿」의 창시자인 서도소리의 명창.
    '김관택': {'role': 'other'},  # 현대/대한민국 - 일제강점기, 성모학원 교사와 해성학교 교장 등을 역임한 교육자. 천주교 전교사 및 총회장을
    '김관현': {'role': 'other'},  # 근대/개항기 | 근대/일제강점기 - 일제강점기 충청남도지사, 함경남도지사, 중추원 참의 등을 역임한 관료. 군인 · 친일반민족
    '김관호': {'role': 'scholar'},  # 근대 - 일제강점기 「해질녘」 · 「호수」 · 「친구의 초상」 등의 작품을 그린 화가.
    '김광': {'role': 'other'},  # 조선 - 조선 전기에, 정난공신들을 따라 일한 공으로 세조 때 녹훈되어 장교를 역임한 천인 출신의 
    '김광국': {'role': 'other'},  # 조선/조선 후기 - 조선후기 수의, 가선대부, 동지중추부사 등을 역임한 의관. 서화수집가.
    '김광균': {'role': 'poet'},  # 해방 이후 『기항지』, 『황혼가』 등을 저술한 시인. 실업가.
    '김광두': {'role': 'other foreigner'},  # 조선/조선 후기 - 조선 후기 임진왜란 때 함창 황령사에서 창의(倡義)하여 일본군을 격퇴한 의병장.
    '김광률': {'role': 'other'},  # 현대/대한민국 - 해방 이후 올빼미부대 대침투작전 당시의 군인.
    '김광부': {'role': 'other'},  # 고려 - 고려후기 수어간, 계림윤, 합포도순문사 등을 역임한 무신.
    '김광서': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 만주와 연해주에서 무장 항일운동을 한 독립운동가.
    '김광선': {'role': 'other'},  # 근대 - 일제강점기 영산서무부장, 원평교무, 총부순교무 등을 역임한 원불교인.
    '김광섭': {'role': 'poet'},  # 근대 - 광복 이후 『마음』, 『성북동 비둘기』, 『김광섭시전집』 등을 저술한 시인. 독립운동가.
    '김광세': {'role': 'other'},  # 조선 - 조선 후기에, 병조참판, 강화유수, 대사헌 등을 역임한 문신.
    '김광수': {'role': 'novelist'},  # 조선/조선 후기 - 조선후기 문인들에게 고동 서화 수집에 대한 가치를 일깨운 수장가.
    '김광식': {'role': 'other'},  # 현대/대한민국 - 해방 이후 서울시립국악관현악단 악장 등을 역임한 대금명인.
    '김광악': {'role': 'other'},  # 조선 - 조선 후기에, 황해도도사, 현릉령, 흡곡현령 등을 역임한 문신.
    '김광엽': {'role': 'other'},  # 조선 - 조선 중기에, 흥해군수, 이조정랑, 성균관사성 등을 역임한 문신.
    '김광옥': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 만주에서 조선혁명군 유격대장, 보위대장, 총사령 부관 등을 역임한 독립운동
    '김광우': {'role': 'other'},  # 현대/대한민국 - 해방 이후 자교교회목사, 기독교대한감리회 중부연회 연회장, 배화학원 이사장 등을 역임한 목
    '김광욱': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 양서관향사, 우참찬 등을 역임한 문신.
    '김광원': {'role': 'scholar'},  # 조선 - 조선 전기에, 이문습독관을 역임하다가 안처겸의 옥사애 연루되어 유배된 학자.
    '김광익': {'role': 'poet'},  # 조선 - 조선후기 『반포유고』를 저술한 여항시인.
    '김광재': {'role': 'other'},  # 고려 - 고려 후기에, 첨의평리, 삼사우사, 전리판서 등을 역임한 문신.
    '김광제': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 국채보상운동과 노동운동에 참여한 독립운동가.
    '김광조': {'role': 'other'},  # 고려 - 고려 후기에, 군부판서, 밀직사, 동북면도순위사 등을 역임한 관리 · 공신.
    '김광주': {'role': 'novelist'},  # 근대 - 해방 이후 「태양은 누구를 위하여」, 「석방인」 등을 저술한 작가. 소설가.
    '김광준': {'role': 'other'},  # 현대/대한민국 - 헌법기초위원, 고시사법행정 양과위원, 국회의원 등을 역임한 법조인 · 정치인.
    '김광중': {'role': 'other'},  # 고려 - 고려 전기에, 간의대부, 비서감, 상서우승 등을 역임한 문신.
    '김광진': {'role': 'other'},  # 근대 - 일제강점기 때, 정의부의용대 제1대장 등을 역임하면서 항일무장투쟁을 전개한 독립운동가.
    '김광찬': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 청풍군수, 파주목사, 동지중추부사 등을 역임한 문신.
    '김광철': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 동지중추부사, 전라도관찰사 등을 역임한 문신.
    '김광혁': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 광주목사, 예문관응교, 동부승지 등을 역임한 문신.
    '김광현': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 부제학, 청주목사 등을 역임한 문신.
    '김괴': {'role': 'other'},  # 조선 - 조선 전기에, 이조좌랑, 정언, 헌납 등을 역임한 문신.
    '김굉': {'role': 'scholar'},  # 조선 - 조선 후기에, 단양군수, 세자시강원문학, 예조참판 등을 역임한 문신.
    '김굉필': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 사헌부감찰, 형조좌랑 등을 역임하였으며, 김종직의 제자로 무오사화와 갑자사화
    '김교': {'role': 'other'},  # 조선/조선 전기 - 조선전기 공조판서, 평안도병마절도사, 평안도관찰사 등을 역임한 무신.
    '김교락': {'role': 'other'},  # 근대 - 일제강점기 때, 전라남도 나주 등지에서 군자금 모금 활동을 전개한 독립운동가.
    '김교만': {'role': 'other'},  # 현대/대한민국 - 해방 이후 서울대학교 미술대학 교수를 역임한 교육자. 산업디자이너.
    '김교성': {'role': 'other'},  # 근대 - 해방 이후 「자명고 사랑」 · 「울고 넘는 박달재」 · 「고향역」 등을 만든 작곡가.
    '김교신': {'role': 'other'},  # 근대 - 일제강점기 무교회주의를 제창한 교육자. 종교인.
    '김교제': {'role': 'novelist'},  # 근대/일제강점기 - 일제강점기 「목단화」, 「비행선」, 「현미경」 등을 저술한 소설가. 번역, 번안작가.
    '김교준': {'role': 'other'},  # 현대/대한민국 - 일제강점기 근대 양의학계의 선구자로 알려진 의사. 종교인.
    '김교중': {'role': 'other'},  # 현대/대한민국 - 국회의원을 역임하며 전라남도 일대 민정조사반, 교통체신위원회 등에서 활동한 정치인.
    '김교창': {'role': 'other'},  # 근대 - 일제강점기 때, 수원군 송산면 사강리의 독립만세시위에 참여한 독립운동가.
    '김교헌': {'role': 'other'},  # 근대 - 일제강점기 대종교 제2대 교주.
    '김구': {'role': 'other'},  # 일제강점기 때, 임시정부 주석 등을 역임하였으며, 한인애국단을 조직해 이봉창과 윤봉길의 의
    '김구경': {'role': 'scholar'},  # 근대/일제강점기 - 일제강점기, 『교간당사본능가사자기(校刊唐寫本楞伽師資記)』를 발간하여 초기 선종사 연구의 발
    '김구년': {'role': 'other'},  # 고려 - 고려 후기에, 동지밀직사사, 밀직부사상의, 절일사 등을 역임한 문신.
    '김구덕': {'role': 'other'},  # 조선 - 조선 전기에, 한성부윤, 지돈녕부사, 판돈녕부사 등을 역임한 문신.
    '김구명': {'role': 'other'},  # 조선 - 조선 후기에, 동지중추원사 등을 역임한 문신.
    '김구상': {'role': 'other'},  # 조선/조선 후기 - 조선시대 내의원주부, 상의원판관, 지평현감 등을 역임한 의관.
    '김구용': {'role': 'other'},  # 고려 - 고려 후기에, 삼사좌윤, 성균관대사성, 판전교시사 등을 역임한 문신.
    '김구응': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 충청남도 천안의 아우내 독립만세시위를 주도하는 과정에서 순국한 교육자 · 
    '김구익': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 『조선무산오운육기론』, 『동의사상임해지남』 등을 저술한 학자. 의학자.
    '김구정': {'role': 'other'},  # 현대/대한민국 - 해방 이후 군산여자고등학교 교감, 군산대학교 교수 등을 역임한 교육자. 천주교회사가, 언론
    '김구주': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 강원감사, 승지, 공조참판 등을 역임한 문신.
    '김구현': {'role': 'other'},  # 근대 - 조선 후기에, 공조판서, 중추원일등의관, 궁내부특진관 등을 역임한 문신.
    '김국광': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 동지중추원사, 병조판서, 영중추부사 등을 역임한 문신.
    '김국연': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라에서 당나라에 사신으로 파견된 관리.
    '김국태': {'role': 'novelist'},  # 현대/대한민국 - 해방 이후 「우리교실의 전설」, 「귀는 왜 줄창 열려 있나」 등을 저술한 소설가.
    '김군관': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 신라 김흠돌의 반란 당시의 장수. 대신.
    '김군수': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 일본인과 함께 브라질로 이민한 교민.
    '김군승': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 아찬을 역임한 장수.
    '김군정': {'role': 'other'},  # 고려 - 고려 후기에, 원외랑, 전의부령, 좌대언 등을 역임한 문신.
    '김권': {'role': 'other'},  # 조선 - 조선 중기에, 연안부사, 사복시첨정, 호조참판 등을 역임한 문신.
    '김권수': {'role': 'other'},  # 근대/개항기 | 근대/일제강점기 - 일제강점기 「유하미인」 · 「청조」 · 「춘규」 등을 그린 화가.
    '김궤': {'role': 'other'},  # 고려 - 고려 후기에, 예부시랑, 좌간의대부, 판비서성사 등을 역임한 문신.
    '김귀': {'role': 'other'},  # 고려 - 고려후기 전리판서, 동북면병마사, 첨의평리 등을 역임한 무신.
    '김귀수': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「수영야류」 할미 역 전승자로 인정된 예능보유자.
    '김귀영': {'role': 'other'},  # 조선 - 조선 중기에, 예조판서, 병조판서, 우의정 등을 역임한 문신.
    '김귀희': {'role': 'other'},  # 조선 - 조선 중기에, 장사군관, 수군절도사 등을 역임한 관리 · 공신.
    '김규': {'role': 'other'},  # 조선 - 조선 전기에, 지평, 이조정랑, 전한 등을 역임한 문신.
    '김규동': {'role': 'poet'},  # 근대/일제강점기 | 현대 - 해방 이후 『나비와 광장』 · 『죽음 속의 영웅』 · 『느릅나무에게』 등을 저술한 시인.
    '김규면': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 만주에서 독립운동 활동을 한 사회주의운동가.
    '김규서': {'role': 'other'},  # 조선 - 조선 후기에, 동부승지 등을 역임한 문신.
    '김규식': {'role': 'scholar'},  # 일제강점기 때, 파리강화회의에서 대한민국임시정부 대표 명의의 탄원서를 제출하였고, 해방 이
    '김규열': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 조선공산당 제3차대회 코민테른 파견 대표, 조선공산당재건설준비위원회 중앙간부 등
    '김규오': {'role': 'scholar'},  # 조선 - 조선 후기에, 『최와집』 등을 저술한 학자.
    '김규진': {'role': 'other'},  # 근대 - 일제강점기에 최초의 근대적 영업 화랑을 개설한 서화가. 사진가.
    '김규철': {'role': 'other'},  # 근대/대한제국기 - 대한제국기 때, 단양, 죽령, 청풍 등지에서 의병대장으로 활약하였고, 국권 피탈 이후 군자
    '김규택': {'role': 'scholar'},  # 근대/일제강점기 | 현대 - 일제강점기 망부석, 억지 춘향전 등의 작품을 그린 만화가. 삽화가.
    '김규하': {'role': 'other'},  # 조선 - 조선 후기에, 지평, 정악원정, 장령 등을 역임한 문신.
    '김규홍': {'role': 'other'},  # 근대 - 조선 후기에, 장례원경, 시종원경, 귀족원경 등을 역임한 문신.
    '김규환': {'role': 'scholar'},  # 현대 - 해방 이후 한국방송윤리위원회 위원장, 한국신문학회 회장 등을 역임한 언론인. 학자.
    '김규희': {'role': 'other'},  # 근대 - 조선 후기에, 중추원외랑, 내부참서관, 한성부판윤 등을 역임한 문신.
    '김균': {'role': 'other'},  # 조선 - 조선 전기에, 중추원부사, 보국숭록좌찬성 등을 역임한 문신.
    '김균정': {'role': 'other'},  # 고대/남북국/통일신라 - 통일신라의 제38대 원성왕의 손자로, 대아찬에 임명되어 시중, 상대등 등을 역임하였으며, 
    '김극개': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 경기관찰사, 형조참판 등을 역임한 문신.
    '김극검': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 호조참판, 동지중추부사, 지중추부사 등을 역임한 문신.
    '김극기': {'role': 'scholar'},  # 조선 - 조선 전기에, 『지월당유고』 등을 저술한 문신.
    '김극성': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 예조판서, 우의정 등을 역임한 문신.
    '김극일': {'role': 'other'},  # 조선 - 조선 전기에, 밀양부사, 내자시정, 사헌부장령 등을 역임한 문신.
    '김극종': {'role': 'other'},  # 고려 - 고려전기 간천대장군을 역임한 무신.
    '김극핍': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 이조판서, 호조판서, 좌찬성 등을 역임한 문신.
    '김극해': {'role': 'other'},  # 고려 - 고려 전기에, 중상서영, 분사대부시승, 검교군기감 등을 역임한 문신.
    '김근': {'role': 'scholar'},  # 조선 - 조선 후기에, 『오우당집』 등을 저술한 학자.
    '김근배': {'role': 'other'},  # 근대 - 조선 후기에, 성균관박사 등을 역임한 문신.
    '김근사': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 우의정, 좌의정, 영의정 등을 역임한 문신.
    '김근순': {'role': 'other'},  # 조선 - 조선 후기에, 부제학, 대사성, 직제학 등을 역임한 문신.
    '김근태': {'role': 'other'},  # 현대/대한민국 - 대한민국의 인권과 민주주의를 위해 헌신한 사회운동가이자 정치가.
    '김근행': {'role': 'other'},  # 조선 - 조선 후기에, 태자익위사세마, 김포군수 등을 역임한 문신.
    '김긍률': {'role': 'other'},  # 고려 - 고려전기 제2대 혜종의 비 청주원부인과 제3대 정종의 비 청주남원부인의 부친으로 원보를 역
    '김기': {'role': 'scholar'},  # 조선 - 조선 중기에, 임진왜란이 발발하자 의병을 일으켜 화왕산성전투에 참전하였고, 『북애문집』 등
    '김기대': {'role': 'other'},  # 조선 - 조선 후기에, 경기도관찰사, 함경도관찰사, 예조판서 등을 역임한 문신.
    '김기덕': {'role': 'other'},  # 현대/대한민국 - 대한민국의 영화감독.
    '김기동': {'role': 'scholar'},  # 현대 - 동국대학교 국어국문학과 교수를 역임하였으며, 『국문학개론』, 『한국고대소설개론』, 『한국문
    '김기두': {'role': 'scholar'},  # 현대/대한민국 - 서울대학교 법과대학 학장, 법무부 정책자문위원 등을 역임한 법학자.
    '김기득': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 의열단의 단원으로 밀양폭탄사건에 가담하였으며, 신간회, 조선공산당 재조직 
    '김기련': {'role': 'other foreigner'},  # 현대/대한민국 - 해방 이후 프랑스리모주국제칠보비엔날레 금상, 민속예술상 등을 수상한 공예가. 칠보공예가.
    '김기례': {'role': 'scholar'},  # 조선 - 조선 후기에, 역학에 주력하여 「팔괘성정물상」, 「역요선의강목」, 『묵천집』 등을 저술한 
    '김기림': {'role': 'poet critic'},  # 근대 - 일제강점기 『기상도』, 『태양의 풍속』 등을 저술한 시인. 문학평론가.
    '김기범': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 경상남도 합천군 삼가장터의 독립만세시위를 주도하는 과정에서 순국한 독립운동
    '김기서': {'role': 'other'},  # 조선/조선 후기 - 조선후기 「단발령도」를 그린 화가.
    '김기석': {'role': 'scholar'},  # 현대/대한민국 - 서울대학교 사범대학 교수 및 학장, 한국교육학회 초대회장 등을 역임하였으며, 『철학개론』,
    '김기선': {'role': 'scholar'},  # 조선 - 조선 후기에, 『기서문집』 등을 저술한 학자.
    '김기성': {'role': 'other'},  # 조선 - 조선 후기에, 서사관, 광은부위 등을 역임한 문신.
    '김기손': {'role': 'other'},  # 고려 - 고려 후기에, 문하시랑동중서문하평장사, 문하시랑평장사 등을 역임한 문신.
    '김기수': {'role': 'other'},  # 현대 - 해방 이후 한국사상 처음으로 복싱동양챔피언 타이틀을 획득한 체육인.
    '김기영': {'role': 'scholar'},  # 현대 - 해방 이후 「봉선화」 · 「하녀」 등의 작품에 관여한 영화인. 영화감독.
    '김기용': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 대구에서 활약한 독립운동가.
    '김기웅': {'role': 'scholar'},  # 현대/대한민국 - 『조선반도의 벽화고분』, 『고분유물』 등을 저술하며 초창기 고고학 발전에 기여한 고고학자.
    '김기전': {'role': 'other'},  # 현대/대한민국 - 일제강점기 때, 잡지 『개벽』의 주필을 역임하였고, 방정환 등과 함께 천도교소년회를 조직하
    '김기종': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 당상관, 호조판서 등을 역임한 문신.
    '김기중': {'role': 'scholar'},  # 근대/일제강점기 - 일제강점기 서울의 중앙학교, 보성전문학교 등을 운영한 육영사업가.
    '김기진': {'role': 'poet critic'},  # 근대/일제강점기 - 일제강점기 「가련아」 · 「님의 부르심을 받들고서」 · 「나도 가겠습니다」 등을 저술한 시
    '김기찬': {'role': 'other'},  # 조선 - 조선 후기에, 대사간, 이조참의, 이조참판 등을 역임한 문신.
    '김기창': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 신민회, 흥사단 등에서 항일투쟁을 전개한 독립운동가.
    '김기천': {'role': 'other'},  # 근대 - 일제강점기 영광지부장, 총부서무부장, 선원교무 등을 역임한 원불교인.
    '김기철': {'role': 'other'},  # 현대/대한민국 - 제헌의원, 민주동지회 대표간사, 제5대 국회의원 등을 역임한 정치인.
    '김기추': {'role': 'other'},  # 현대/대한민국 - 일제강점기 때, 학교에서 교육투쟁을 전개하였고, 청년동맹 위원장을 역임하였으며, 해방 이후
    '김기풍': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 임천군수, 평양서윤, 충주목사 등을 역임한 문신.
    '김기하': {'role': 'other'},  # 조선 - 조선 후기에, 후릉참봉 등을 역임한 문신.
    '김기한': {'role': 'other'},  # 근대 - 일제강점기 때, 대한독립단을 조직하여 국내지단 결성과 군자금 모금 활동을 전개한 독립운동가
    '김기형': {'role': 'scholar'},  # 현대/대한민국 - 1967년부터 1971년까지, 과학기술처 초대 장관을 역임한 과학자이자 정치가.
    '김기호': {'role': 'scholar'},  # 조선 - 조선 후기, 『구령요의』, 『소원신종』, 『봉교자술』 등을 저술한 천주교 지도자.
    '김기홍': {'role': 'scholar'},  # 현대 - 한양대학교 의과대학 원장, 대한의학협회 부회장 등을 역임하며, 국내 의학의 임상병리 검사기
    '김기후': {'role': 'other'},  # 조선 - 조선 후기에, 지돈녕부사, 도총관, 한성부판윤 등을 역임한 문신.
    '김길임': {'role': 'other'},  # 근대 - 해방 이후 「강강술래」의 전승자로 지정된 예능보유자.
    '김길창': {'role': 'other foreigner'},  # 근대 - 일제강점기, 일본기독교 조선장로교단 및 조선교단 경남 교구장으로서 적극적으로 부일협력 활동
    '김길통': {'role': 'other'},  # 조선 - 조선 전기에, 지중추부사가, 한성부판윤, 호조판서 등을 역임한 문신.
    '김길호': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 내의로 근무하던 중 치료하던 문종이 사망하여 직첩을 환수당하였다가 복귀한 의
    '김낙': {'role': 'other'},  # 고려 - 고려 전기에, 이부시랑 등을 역임하였으며, 자신을 신라 원성왕의 먼 자손이라 사칭하였던 경
    '김낙선': {'role': 'other'},  # 근대 - 대한제국기 때, 이용서 의진에서 선봉장으로 활약한 의병.
    '김낙수': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 경상남도 울산군 언양읍의 독립만세시위를 주도한 혐의로 체포되어 옥중에서 순
    '김낙철': {'role': 'other'},  # 근대/개항기 | 근대/대한제국기 - 19세기 후반~20세기 초 동학농민운동과 천도교 활동에 참여한 천도교인.
    '김낙풍': {'role': 'other'},  # 조선 - 조선 후기에, 종부시정 겸 편수관, 병조참의 등을 역임한 문신.
    '김낙행': {'role': 'scholar'},  # 조선 - 조선 후기에, 『기법질의』, 『강록간보고의』, 『구사당집』 등을 저술한 학자.
    '김난상': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 응교, 직제학, 대사성 등을 역임한 문신.
    '김난섭': {'role': 'other'},  # 근대 - 일제강점기 때, 대한독립단에서 군자금 모금 활동을 전개한 독립운동가.
    '김난손': {'role': 'other foreigner'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 사찬으로서 일본에 파견된 사신.
    '김난순': {'role': 'other'},  # 조선 - 조선후기 대사헌, 우참찬, 이조판서 등을 역임한 문신. 서예가.
    '김남극': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 만주에 동창학교와 북일학교를 설립하여 민족의식을 고취하였고, 경신참변에 의
    '김남득': {'role': 'other'},  # 고려/고려 후기 - 고려 후기 상주목사, 서해도관찰사, 문하평리 등을 역임한 문신.
    '김남수': {'role': 'other'},  # 조선/조선 전기 - 조선전기 판사복시사, 공조판서, 판좌군도총제부사 등을 역임한 무신.
    '김남일': {'role': 'other'},  # 조선 - 조선 후기에, 상의원별제, 홍산현감, 괴산군수 등을 역임한 문신.
    '김남주': {'role': 'poet'},  # 현대/대한민국 - 해방 이후 『진혼가』, 『나의 칼 나의 피』, 『조국은 하나다』 등을 저술한 시인.
    '김남중': {'role': 'essayist'},  # 현대 - 해방 이후 『전남일보』사장, 한국신문협회 부회장 등을 역임한 언론인. 수필가.
    '김남천': {'role': 'novelist critic'},  # 근대 - 일제강점기 「대하」, 「물」, 「생의 고민」 등을 저술한 소설가. 문학비평가..
    '김내범': {'role': 'other'},  # 근대 - 일제강점기 간도노회초대노회장, 국민회 분회장 등을 역임한 목사. 독립운동가.
    '김내성': {'role': 'novelist'},  # 근대 - 일제강점기, 『마인』, 『백가면』, 「백사도」 등을 저술한 탐정소설가.
    '김녕': {'role': 'other'},  # 조선 - 조선 후기에, 전적, 사예, 예안현감 등을 역임한 문신.
    '김노겸': {'role': 'other'},  # 조선 - 조선 후기에, 홍산현감 등을 역임한 문신.
    '김노경': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 광주부유수, 지돈녕부사, 판의금부사 등을 역임한 문신.
    '김노선': {'role': 'scholar'},  # 조선 - 조선 후기에, 향교의 교장이 되어 어린 학생을 가르치는 교안 「유의」를 만들었으며, 『기계
    '김노응': {'role': 'other'},  # 조선 - 조선 후기에, 형조판서, 한성판윤, 병조판서 등을 역임한 문신.
    '김노진': {'role': 'other'},  # 조선 - 조선 후기에, 형조판서, 우참찬 등을 역임한 문신.
    '김노차': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라 제29대 태종무열왕의 넷째 아들인 왕자.
    '김녹연': {'role': 'other'},  # 고려 - 고려 후기에, 경상주도안찰사, 우간의대부 등을 역임한 문신.
    '김녹영': {'role': 'other'},  # 현대/대한민국 - 신민당 상무위원, 제12대 국회부의장 등을 역임한 정치인.
    '김녹주': {'role': 'other'},  # 근대 - 일제강점기 김정문의 제자로 송만갑협률사에서 활동한 판소리의 명창.
    '김뉴': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 이조참판 등을 역임한 문신.
    '김능유': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 때, 사신으로 당에 파견되었다가 귀국길에 익사한 통일신라의 왕족.
    '김니': {'role': 'scholar'},  # 조선 - 조선 중기에, 『유당집』 등을 저술한 문신.
    '김다수': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 사신으로 당과 왜에 파견된 관리.
    '김단': {'role': 'other'},  # 고려 - 고려전기 장주방어사, 시어사 겸 동로병마사 등을 역임한 무신.
    '김단갈단': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 하정사로 당나라에 파견되어 위위소경의 관직을 받은 관리.
    '김단야': {'role': 'other'},  # 근대 - 일제강점기 고려공산청년당 책임비서, 전조선민중운동자대회 준비위원 등을 역임한 사회주의운동가
    '김달복': {'role': 'other'},  # 고대/남북국 - 남북국시대 신라의 제17대 내물마립간의 7세손으로 잡찬 관등의 귀족.
    '김달상': {'role': 'other'},  # 고려 - 고려 후기에, 밀직부사, 한양윤, 양광도도순문사 등을 역임한 문신 · 공신.
    '김달순': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 우의정 등을 역임한 문신.
    '김달진': {'role': 'poet scholar'},  # 현대/대한민국 - 해방 이후 『올빼미의 노래』, 『큰 연꽃 한 송이 피기까지』 등을 저술한 시인. 한학자.
    '김달현': {'role': 'other'},  # 현대/대한민국 - 일제강점기 때, 무산자동지회를 설립하는 등 사회주의운동을 벌였고, 해방 이후 북한에서, 최
    '김달호': {'role': 'other'},  # 현대/대한민국 - 서울고등검찰청 차장검사, 사회대중당 중앙집행위원장, 제5대 민의원 등을 역임한 정치인 · 
    '김담': {'role': 'other'},  # 조선 - 조선 후기에, 판결사 등을 역임한 문신.
    '김담수': {'role': 'scholar'},  # 조선 - 조선 중기에, 『서계일고』 등을 저술한 학자.
    '김당': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 좌찬성 등을 역임한 문신.
    '김대건': {'role': 'other'},  # 조선/조선 후기 - 1846년 병오박해 때 서울 새남터에서 처형된 신부로 한국인 최초의 사제.
    '김대규': {'role': 'other'},  # 근대 - 대한제국기 때, 경상도, 강원도에서 항일의병투쟁을 전개한 의병장.
    '김대근': {'role': 'other'},  # 조선 - 조선 후기에, 이조판서, 좌찬성, 우찬성 등을 역임한 문신.
    '김대금': {'role': 'other'},  # 고대/남북국 - 남북국시대 태봉국 궁예(弓裔)의 부하로 신라의 명주(溟州) 침공 당시의 장수.
    '김대덕': {'role': 'other'},  # 조선 - 조선 후기에, 동지의금부사, 부총관, 형조참판 등을 역임한 문신.
    '김대래': {'role': 'other'},  # 조선 - 조선 중기에, 홍문관부응교, 사인, 직제학 등을 역임한 문신.
    '김대례': {'role': 'other'},  # 근대 - 해방 이후 「진도씻김굿」 전승자로 지정된 예능보유자. 무속인.
    '김대명': {'role': 'other'},  # 조선 - 조선 중기에, 풍기군수 등을 역임한 문신.
    '김대문': {'role': 'other'},  # 고대/남북국/통일신라 - 신라 성덕왕 때 활약한 진골 출신 관료.
    '김대봉': {'role': 'poet'},  # 현대/대한민국 - 일제강점기 『맥』, 『무심』 등을 저술한 시인. 의사.
    '김대비': {'role': 'other foreigner'},  # 고대/남북국 - 남북국시대 통일신라에서 중국 선종의 육조인 혜능의 목을 훔쳐 하동군 쌍계사에 봉안하였다고 
    '김대섭': {'role': 'other'},  # 조선 - 조선 중기에, 의금부도사, 조지서별제 등을 역임한 문신.
    '김대성': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 때, 중시 등을 역임하였으며, 불국사를 창건한 통일신라의 귀족 · 관리.
    '김대우': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 학무국 사회교육과장, 참여관, 전라북도지사 등을 역임한 관료. 친일반민족행위자.
    '김대유': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 정언, 칠원현감, 전적 등을 역임한 문신.
    '김대인': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 임진왜란 당시 해상 및 육상에서 활약하였던 무관.
    '김대재': {'role': 'other'},  # 고려 - 고려후기 무오정변, 임연의 정변 등과 관련된 무신.
    '김대정': {'role': 'other'},  # 조선 - 조선시대 임진왜란 때, 연안부사로 연안성을 굳게 지킨 문신.
    '김대중': {'role': 'other'},  # 현대/대한민국 - 대한민국 제15대 대통령을 지내고 노벨평화상을 수상한 정치인.
    '김대지': {'role': 'other'},  # 근대 - 일제강점기 때, 임시정부 내무위원, 국내조사원 등을 역임하고 의열단의 주요간부로 활약한 독
    '김대현': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「자장가」 · 「들국화」 · 「고향의 노래」 등을 만든 작곡가.
    '김대흥': {'role': 'other'},  # 근대/개항기 - 개항기 갑신정변, 한성조약 등과 관련된 의사(義士).
    '김대희': {'role': 'scholar'},  # 근대 - 대한제국기 때, 보성전문학교 강사, 광신상업학교 교사 등을 역임한 교육자 · 경제학자.
    '김덕겸': {'role': 'other'},  # 조선 - 조선 중기에, 북청판관, 충청도사동지중추부사 등을 역임한 문신.
    '김덕기': {'role': 'other'},  # 조선 - 조선 후기에, 동래부사, 황해도관찰사, 호조참판 등을 역임한 문신.
    '김덕련': {'role': 'scholar'},  # 조선 - 일제강점기 때, 『고헌집』 등을 저술한 학자.
    '김덕령': {'role': 'other'},  # 조선/조선 후기 - 조선 중기에, 임진왜란이 발발하자 의병으로 활약하여 형조좌랑에 임명된 의병장.
    '김덕룡': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「두석장(豆錫匠) 전승자로 지정된 기능보유자.
    '김덕명': {'role': 'other'},  # 고려/고려 후기 - 고려후기 개경 승도의 난, 최우암살모의 등과 관련된 주모자.
    '김덕목': {'role': 'other'},  # 근대 - 일제강점기 때, 학생항일구국회 간부, 한국광복군 총사령부 참모 등을 역임한 독립운동가.
    '김덕방': {'role': 'other foreigner'},  # 조선/조선 후기 - 조선후기 일본인 나가타에게 침구의 비법을 전해준 의관.
    '김덕보': {'role': 'scholar'},  # 조선/조선 후기 - 조선 후기 임진왜란과 정묘호란 때 의병을 일으킨 의병장이자 학자.
    '김덕부': {'role': 'other'},  # 고려 - 고려 전기에, 상서좌복야, 수사공 상서좌복야 등을 역임한 문신.
    '김덕생': {'role': 'other'},  # 고려/고려 후기 - 고려후기 전옥서영, 낭장, 동지중추원사(추증) 등을 역임한 무신.
    '김덕성': {'role': 'scholar'},  # 조선/조선 후기 - 조선후기 「쌍마도」 · 「선객도」 · 「뇌공도」 등의 작품을 그린 화가.
    '김덕수': {'role': 'scholar'},  # 조선/조선 후기 - 조선 전기에 기묘사화로 화를 입은 김식의 아들로 사면된 이후 후학 양성에 힘쓴 학자.
    '김덕순': {'role': 'other foreigner'},  # 근대 - 대한제국기 때, 항일의병투쟁과 군자금 모금, 일본인 처단 활동 등을 전개한 의병.
    '김덕승': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 사복시정, 목사 등을 역임한 문신.
    '김덕열': {'role': 'other'},  # 현대/대한민국 - 미군정청 관재처 감찰관, 제헌국회의원 등을 역임한 정치인.
    '김덕오': {'role': 'scholar'},  # 조선 - 조선 후기에, 『기연의변』, 『사학의변』, 『치헌집』 등을 저술한 학자.
    '김덕용': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 수원의 독립만세시위를 주도하다가 제암리 학살사건에 의해 사망한 독립운동가.
    '김덕원': {'role': 'other'},  # 조선 - 조선 후기에, 사헌부장령, 형조참판, 예조판서 등을 역임한 문신.
    '김덕제': {'role': 'other'},  # 근대 - 대한제국기 때, 원주진위대 정위 등을 역임하였으며, 항일의병활동을 전개한 의병장.
    '김덕준': {'role': 'other'},  # 현대 - 해방 이후 우리나라 최초의 국제 심판으로 국제심판 공로상을 받은 체육인.
    '김덕지': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 제56대 경순왕의 왕자.
    '김덕진': {'role': 'other'},  # 근대/대한제국기 - 을사조약에 반대하여 일어난 의병운동에 참여한 의병장.
    '김덕하': {'role': 'other'},  # 조선/조선 후기 - 조선후기 「사계산수도권」을 그린 화가.
    '김덕한': {'role': 'other'},  # 근대/개항기 | 근대/일제강점기 - 일제강점기 봉상사 제조, 종묘서 제조, 의효전 제조 등을 역임한 관료. 친일반민족행위자.
    '김덕함': {'role': 'other'},  # 조선 - 조선 중기에, 공조좌랑, 호조정랑 등을 역임한 문신.
    '김덕현': {'role': 'other'},  # 근대 - 일제강점기 때, 학성학교 교장, 북로군정서 군정회의원 등을 역임한 독립운동가.
    '김덕흥': {'role': 'other'},  # 근대 - 대한제국기 때, 강원도 양구 일대에서 항일의병투쟁을 전개한 의병장.
    '김도': {'role': 'other'},  # 고려 - 고려 후기에, 좌부대언, 지신사, 밀직제학 등을 역임한 문신.
    '김도규': {'role': 'other'},  # 근대/대한제국기 - 대한제국기 전라남도 보성일대에서 활약한 의병장.
    '김도나': {'role': 'other foreigner'},  # 고대/남북국 - 남북국시대 통일신라에서 일본에 사신으로 파견된 관리.
    '김도명': {'role': 'scholar'},  # 조선 - 조선 후기에, 『외암문집』 등을 저술한 학자.
    '김도산': {'role': 'scholar'},  # 근대/일제강점기 - 일제강점기 「의리적 구투」, 「시우정」, 「형사고심」 등의 작품에 관여한 영화인. 연극인.
    '김도삼': {'role': 'other'},  # 근대 - 대한제국기 상쇠와 진법놀이에 능해 정읍농악을 널리 알린 음악인. 상쇠.
    '김도성': {'role': 'poet scholar'},  # 현대/대한민국 - 해방 이후 『고란초』, 『갈대』 등을 저술한 시인. 영문학자.
    '김도수': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 예빈시주부, 경양찰방 등을 역임한 서얼 문사.
    '김도숙': {'role': 'other'},  # 근대/대한제국기 - 대한제국기 심남일 의진에서 도통장으로 활약한 의병장.
    '김도언': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 의금부도사, 병조좌랑, 음죽현감 등을 역임한 문신.
    '김도연': {'role': 'other'},  # 현대/대한민국 - 일제강점기 때, 2·8독립선언과 조선어학회 사건으로 옥고를 치렀으며, 해방 이후, 국회의원
    '김도원': {'role': 'other'},  # 근대 - 일제강점기 때, 대한독립보합단에서 군자금 모금 활동을 전개한 독립운동가.
    '김도주': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 경상북도 안동군 임하면의 독립만세시위에 참여했다가 순국한 독립운동가.
    '김도태': {'role': 'other'},  # 근대 - 3.1운동 당시 48인의 한 사람으로 활약한 교육자.
    '김도행': {'role': 'scholar'},  # 조선 - 조선 후기에, 『우고문집』 등을 저술한 학자.
    '김도혁': {'role': 'scholar'},  # 조선 - 조선 후기에, 「망해도법」, 「측량법」, 『암당문집』 등을 저술한 학자.
    '김도현': {'role': 'other'},  # 근대/개항기 | 근대/대한제국기 - 을미사변 이후 대한제국 강제 병합 이전까지 의병 활동을 전개한 의병장.
    '김도화': {'role': 'scholar'},  # 근대/개항기 - 개항기 때, 의금부도사 등을 역임하였으며, 안동에서 의병을 일으켜 항쟁한 학자 · 의병장.
    '김도희': {'role': 'other'},  # 조선 - 조선 후기에, 판서, 우의정, 좌의정 등을 역임한 문신.
    '김돈': {'role': 'other'},  # 조선 - 조선 전기에, 인순부윤, 도승지 등을 역임한 문신.
    '김돈시': {'role': 'other'},  # 고려/고려 전기 - 고려 전기 의종의 측근으로, 정중부의 난 당시 살해된 문신.
    '김돈중': {'role': 'other'},  # 고려 - 고려 전기에, 호부원외랑, 시랑, 좌승선 등을 역임한 문신.
    '김돈희': {'role': 'scholar'},  # 근대/일제강점기 - 일제강점기 「출사표」, 「장진주」 등의 작품을 낸 서예가.
    '김동건': {'role': 'other'},  # 조선 - 조선 후기에, 동지 겸 사은부사, 우참찬 등을 역임한 문신.
    '김동권': {'role': 'other'},  # 조선 - 조선후기 효행으로 정려를 하사 받고, 중학교 교관으로 추증된 효자.
    '김동리': {'role': 'novelist'},  # 해방 이후 『무녀도』, 『황토기』, 『등신불』 등을 저술한 문학작가.
    '김동명': {'role': 'other'},  # 근대 - 일제강점기 신흥청년동맹 상무집행위원장, 고려공산청년회 만주총국 책임자 등을 역임한 사회주의
    '김동삼': {'role': 'other'},  # 근대/일제강점기 - 1910년대에 만주에 망명하여 1920년대까지 서간도 독립운동 단체의 지도자로 활약하였던 
    '김동석': {'role': 'poet critic'},  # 근대 - 해방 이후 『길』, 『해변의 시』 등을 저술한 시인. 비평가.
    '김동성': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 서울대교수, 공보부장관 등을 역임한 학자. 정치인.
    '김동수': {'role': 'other'},  # 근대/개항기 - 대한제국기 전라남도 광주 출신으로, 양진여 의진에 참여하여 활동한 의병장.
    '김동식': {'role': 'other'},  # 근대 - 일제강점기 때, 평안남도 중화군 상원면의 독립만세시위를 주도한 천도교인 · 독립운동가.
    '김동신': {'role': 'other'},  # 근대/대한제국기 - 을사조약 이후 민종식 의진에서 선봉장으로 활약한 의병장.
    '김동엄': {'role': 'other foreigner'},  # 고대/남북국 - 남북국시대 통일신라의 급찬으로서 일본에 사신으로 파견된 관리.
    '김동연': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 장령, 사간, 집의 등을 역임한 문신.
    '김동엽': {'role': 'other'},  # 현대 - 해방 이후 프로야구 해태타이거즈 창단감독, 서울방송 전속야구해설위원 등을 역임한 체육인.
    '김동영': {'role': 'other'},  # 현대/대한민국 - 제9대, 10대, 12대, 13대 국회의원, 정무제1장관 등을 역임한 정치인.
    '김동욱': {'role': 'scholar'},  # 현대/대한민국 - 민속학회 이사, 한국비교문학회 회장, 한국복식학회 부회장 등을 역임하였으며, 『국문학개설』
    '김동원': {'role': 'other'},  # 현대 - 해방 이후 「자명고」, 「마의태자」, 「별」 등에 출연한 배우. 영화배우, 연극배우.
    '김동은': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 광주에서 학생항일비밀결사인 독서회를 조직하여 항일투쟁을 전개한 독립운동가.
    '김동익': {'role': 'scholar'},  # 근대/일제강점기 | 현대 - 서울대학교 의과대학 교수, 동국대학교 총장 등을 역임한 의학자.
    '김동인': {'role': 'novelist'},  # 근대/일제강점기 - 일제강점기 「배따라기」 · 「감자」 · 「발가락이 닮았다」 등을 저술한 소설가. 친일반민족
    '김동일': {'role': 'scholar'},  # 현대/대한민국 - 서울대학교 공과대학 초대 학장, 한국원자력원의 초대 상임위원 등을 역임하였으며, 『한국자기
    '김동조': {'role': 'other foreigner'},  # 현대/대한민국 - 주일본 대사, 외무부장관 등을 역임한 외교관 · 정치인.
    '김동준': {'role': 'other'},  # 현대/대한민국 - 해방 이후 판소리 고법의 전승자로 지정된 예능보유자. 고수.
    '김동철': {'role': 'other'},  # 현대/대한민국 - 덕원면속구 소속으로 해방 이후 평양대목구로 파견되어 안주본당, 비현본당에서 사목한 신부.
    '김동필': {'role': 'other'},  # 근대 - 대한제국기 때, 일제의 침략을 규탄하는 상소운동 및 을사조약 반대투쟁 등을 전개한 독립운동
    '김동하': {'role': 'other'},  # 현대/대한민국 - 해방 이후 제1상륙 사단장, 해병중장, 국가재건최고회의최고위원 등을 역임한 군인. 체육인.
    '김동한': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 우리나라 최초의 사교무용학원인 조선예술학원을 설립한 무용가.
    '김동화': {'role': 'scholar'},  # 현대/대한민국 - 동국대학교 교수로 재임하여 세계적인 불교학의 연구를 학계에 정착시켰으며, 『불교학개론』, 
    '김동환': {'role': 'poet'},  # 근대/일제강점기 - 일제강점기 『국경의 밤』 · 『해당화』 · 『돌아온 날개』 등을 저술한 시인. 언론인 · 
    '김동훈': {'role': 'other'},  # 현대 - 해방 이후 「아들을 위하여」, 「심판」, 「롤러스케이트를 타는 오뚝이」 등에 출연한 배우.
    '김동휘': {'role': 'other'},  # 현대/대한민국 - 해방 이후 주독대사관 부영사, 외무부 차관, 상공부 장관 등을 역임한 관료. 외교관.
    '김두달': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 호군 등을 역임하였으며, 신돈의 세력으로 활동하다 신돈의 반역모의사건에 가담
    '김두량': {'role': 'scholar'},  # 조선/조선 후기 - 조선후기 「월야산수도」 · 「춘하도리원호흥도권」 · 「흑구도」 등의 작품을 그린 화가.
    '김두룡': {'role': 'scholar'},  # 조선 - 조선 후기에, 『낙선당집』 등을 저술한 학자.
    '김두만': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 대한청년단연합회 교제부장, 광복군참리부 외무사장 등을 역임한 독립운동가.
    '김두명': {'role': 'other'},  # 조선 - 조선 후기에, 사간, 승지, 병조참의 등을 역임한 문신.
    '김두봉': {'role': 'scholar'},  # 일제강점기 때, 임시의정원 의원, 한국민족혁명당 중앙집행위원, 조선독립동맹 주석 등을 역임
    '김두용': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 고려공산청년회 일본부기관지 출판위원, 조선신문사 편집국원 등을 역임한 사회주의운
    '김두종': {'role': 'scholar'},  # 근대/일제강점기 | 현대 - 서울대학교 의과대학 교수, 숙명여자대학교 총장 등을 역임하였으며, 『한국의학사』, 『한국고
    '김두징': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 갑인예송으로 곤경에 처한 송시열을 변호하는 상소를 올리는 데 참여한 유생.
    '김두한': {'role': 'other'},  # 현대/대한민국 - 대한청년당의 감찰부장, 제3대, 6대 국회의원 등을 역임하였으며, 국회오물투척사건을 일으킨
    '김두헌': {'role': 'scholar'},  # 현대 - 해방 이후 『조선가족제도연구』 · 『현대의 가족』 등을 저술한 학자. 교육자.
    '김두환': {'role': 'other'},  # 근대/일제강점기|현대 - 해방 이후 제1회 국전에서 「향원정」 으로 입선한 화가. 유화가.
    '김둔산': {'role': 'other'},  # 고대/남북국 - 남북국시대 평양성전투에서 큰공을 세워 사찬을 제수받은 관리.
    '김득경': {'role': 'other'},  # 고려 - 고려후기 북청주만호를 역임한 무신.
    '김득배': {'role': 'scholar'},  # 고려 - 고려 후기에, 서북면도병마사, 수충보절정원공신, 정당문학 등을 역임한 문신 · 공신.
    '김득복': {'role': 'other'},  # 조선 - 조선 중기에, 임진왜란이 발발하자 불국산에서 의병을 일으켜 항쟁하였고, 이순신의 휘하에서 
    '김득상': {'role': 'other'},  # 조선 - 조선 중기에, 임진왜란이 발발하자 형 김득복을 따라 의병활동을 전개하다가 전사한 의병.
    '김득수': {'role': 'other'},  # 현대/대한민국 - 해방 이후 판소리 고법의 전승자로 지정된 예능보유자. 고수.
    '김득신': {'role': 'scholar'},  # 조선/조선 후기 - 조선후기 「파적도」, 「긍재풍속화첩」, 「풍속팔곡병」 등의 작품을 그린 화가.
    '김득연': {'role': 'scholar'},  # 조선 - 조선 후기에, 「청량산유록」, 『지수정가』, 『갈봉유고』 등을 저술한 학자.
    '김득인': {'role': 'other'},  # 조선 - 조선후기 장례원사의를 역임한 무신.
    '김득제': {'role': 'other'},  # 고려 - 고려후기 대장군, 의주원수, 삼사우사 등을 역임한 무신.
    '김득진': {'role': 'other'},  # 조선 - 조선 후기에, 용강부사, 자산군수 등을 역임한 무신 · 공신.
    '김득추': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 용양위부사직, 가선대부 등을 역임한 무신 · 공신.
    '김락': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 예안군에서 전개된 독립만세운동에 참여한 독립운동가.
    '김란': {'role': 'other'},  # 고려 - 고려 후기에, 밀직부사, 서북면도체찰사, 참지문하부사 등을 역임한 문신.
    '김려': {'role': 'other'},  # 조선 - 조선 후기에, 연산현감, 함양군수 등을 역임한 문신.
    '김련': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 추밀원사, 지문하성사, 참지정사 등을 역임한 문신.
    '김령': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 승문원관원, 주서 등을 역임한 문신.
    '김례': {'role': 'other'},  # 고려 - 고려후기 이장대의 난과 관련된 무신. 반란자.
    '김례삼': {'role': 'novelist'},  # 근대 | 현대 - 해방 이후 연변문학연합회 주비위원회 비서장, 조선족민속학회 이사 등을 역임한 작가.
    '김로': {'role': 'other'},  # 조선 - 조선 후기에, 판의금부사, 호조판서, 대사헌 등을 역임한 문신.
    '김룡': {'role': 'other'},  # 고려 - 고려후기 만호, 판사 등을 역임한 무신.
    '김류': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 형조좌랑, 전주판관, 병조판서 등을 역임한 문신.
    '김륜': {'role': 'other'},  # 고려 - 고려 후기에, 경상 · 전라도도순문사, 벽상공신, 좌정승 등을 역임한 문신 · 공신.
    '김률': {'role': 'other'},  # 고대/남북국 - 남북국시대 통일신라의 아찬 관등을 역임한 관리.
    '김륭': {'role': 'scholar'},  # 조선 - 조선 전기에, 『물암집』, 『삼서강록』 등을 저술한 학자.
    '김륵': {'role': 'other'},  # 조선 - 조선 중기에, 경상우도관찰사, 충청도관찰사, 안동부사 등을 역임한 문신.
    '김림': {'role': 'other'},  # 고려 - 고려 후기에, 권신인 정세운과 함께 홍건적의 난을 평정함으로써 왕의 신임을 얻었으나, 정세
    '김립': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 만주에서 활약한 사회주의운동가.
    '김마리아': {'role': 'other foreigner'},  # 근대/일제강점기 - 고려혁명군으로 활동하고 중국 중앙군관학교 서북북교의 러시아어 교관을 역임한 독립운동가.
    '김막인': {'role': 'other'},  # 현대 - 해방 이후 조선무용예술협회 현대무용부의 임원을 역임한 무용가.
    '김만': {'role': 'scholar'},  # 조선/조선 후기 - 조선 후기에, 농정개혁과 환곡의 폐단을 상소한 학자.
    '김만겸': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 대한국민의회 간부를 지내며 독립운동을 한 사회주의운동가.
    '김만균': {'role': 'other'},  # 조선 - 조선 후기에, 사인, 보덕, 승지 등을 역임한 문신.
    '김만기': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에 영돈녕부사 · 총융사 등을 역임한 문신.
    '김만길': {'role': 'other'},  # 조선 - 조선 후기에, 부제학, 전라도관찰사, 이조참의 등을 역임한 문신.
    '김만덕': {'role': 'other'},  # 조선후기 1795년 흉년과 관련된 상인.
    '김만물': {'role': 'other foreigner'},  # 고대/삼국/신라 - 남북국시대 통일신라의 사찬으로 일본에 파견된 관리.
    '김만삼': {'role': 'other'},  # 현대/대한민국 - 소련에서 카자흐공화국으로 강제이주를 당하여 아들 김홍빈과 함께 선봉 콜호즈를 세웠으며, 벼
    '김만선': {'role': 'novelist'},  # 근대 - 해방 이후 「절룸바리 돌쇠」, 「압록강」, 「해방의 노래」 등을 저술한 작가. 소설가.
    '김만수': {'role': 'other foreigner'},  # 근대 - 일제강점기 때, 서로군정서에서 일본 총영사 및 일본경찰 처단 활동을 전개한 독립운동가.
    '김만술': {'role': 'scholar'},  # 근대/일제강점기 | 현대 - 해방 이후 「해방」, 「역사(力士) I」, 「역사(力士) II」 등의 작품을 낸 조각가.
    '김만식': {'role': 'other'},  # 근대 - 조선 후기에, 동부승지, 공조참의, 예조판서, 평안도관찰사 등을 역임한 문신.
    '김만옥': {'role': 'poet'},  # 현대/대한민국 - 해방 이후 『슬픈 계절의』, 『오늘 죽지 않고 오늘 살아 있다』 등을 저술한 시인.
    '김만와': {'role': 'other'},  # 근대 - 일제강점기 때, 철혈광복단, 대한독립단, 고려혁명당, 정의부 등에서 항일투쟁을 전개한 독립
    '김만중': {'role': 'scholar'},  # 조선 후기에, 『사씨남정기』, 『구운몽』 등을 저술한 문신.
    '김만증': {'role': 'scholar'},  # 조선 - 조선 후기에, 지중추부사, 임피현령 등을 역임하였으며, 『돈촌집』을 저술한 학자.
    '김만채': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 강원도관찰사, 개성부유수, 경기도관찰사 등을 역임한 문신.
    '김만형': {'role': 'scholar'},  # 근대/일제강점기 | 현대 - 해방 이후 「연봉」, 「쇳물을 붓는 사람들」 등의 작품을 그린 화가.
    '김만흥': {'role': 'other'},  # 현대 - 해방 이후 종묘제례악 해금의 전승자로 지정된 예능보유자.
    '김말': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 예문제학, 중추원부사, 판중추원사 등을 역임한 문신.
    '김말봉': {'role': 'novelist'},  # 근대 - 일제강점기 「찔레꽃」, 「망명녀」, 「밀림」 등을 저술한 소설가.
    '김매순': {'role': 'other'},  # 조선 - 조선 후기에, 예조참판, 강화부유수 등을 역임한 문신.
    '김맹': {'role': 'other'},  # 조선 - 조선 전기에, 오위도총부경력 등을 역임한 문신 · 공신.
    '김맹경': {'role': 'other'},  # 조선 - 조선전기 하정사 유자광을 수행하여 연경에 다녀온 역관.
    '김맹권': {'role': 'scholar'},  # 조선 - 조선 전기에, 집현전학사 등을 역임한 학자.
    '김맹도리': {'role': 'other'},  # 근대/대한제국기 - 대한제국기 때, 양한규 의진에서 항일의병투쟁을 전개한 의병.
    '김맹성': {'role': 'other'},  # 조선 - 조선 전기에, 이조정랑, 수찬 등을 역임한 문신.
    '김면': {'role': 'scholar'},  # 조선 - 조선 중기에, 임진왜란이 발발하자 의병을 일으켜 활약한 공으로 합천군수, 첨지사, 경상우도
    '김면호': {'role': 'other'},  # 조선 - 조선후기 병인박해 당시의 순교자.
    '김명국': {'role': 'scholar'},  # 조선 - 조선후기 「설중귀려도」, 「달마도」, 「은사도」 등의 작품을 그린 화가.
    '김명권': {'role': 'other'},  # 근대 - 일제강점기 때, 대한청년단에서 군자금 모금 활동을 전개한 독립운동가.
    '김명규': {'role': 'other'},  # 근대 - 일제강점기 때, 동래고등보통학교의 독립만세시위를 주도하였으며, 군자금 모금 활동을 전개한 
    '김명균': {'role': 'other'},  # 근대 - 개항기 통리군국사무아문 감공사주사, 기기국방판 등을 역임한 관료.
    '김명동': {'role': 'other'},  # 근대 - 일제강점기 때, 신간회 중앙집행위원 등으로 활동하였고, 해방 이후, 국회의원을 역임한 정치
    '김명립': {'role': 'other'},  # 근대/대한제국기 - 대한제국기 때, 이강년 의진에서 활약하였고, 군자금 모금 활동을 전개한 의병 · 독립운동가
    '김명복': {'role': 'scholar'},  # 근대 - 경희대학교 체육대학장, 교육대학원장, 부총장 등을 역임하였으며, 『체육지도서』, 『체육개론
    '김명선': {'role': 'other'},  # 근대/일제강점기 | 현대 - 해방 이후 대한의학협회 부회회장, 대한가족계획협회 회장 등을 역임한 의사.
    '김명수': {'role': 'other foreigner'},  # 현대/대한민국 - 일제강점기 때, 일본 우베일일신문사 기자, 편집국장을 역임하였으며, 해방 이후 국회의원을 
    '김명순': {'role': 'poet novelist'},  # 근대 - 일제강점기 「동경」, 「옛날의 노래여」, 「언니 오시는 길에」 등을 저술한 시인. 소설가.
    '김명시': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 때, 상해한인청년동맹 부인부 책임, 중국공산당 한인지부 선전부 책임, 조선의용대
    '김명식': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 활동한 사회주의 운동가, 민족운동가.
    '김명언': {'role': 'other'},  # 조선 - 조선 전기에, 호조정랑, 김제군수, 상주목사 등을 역임한 문신.
    '김명원': {'role': 'other'},  # 조선 - 조선 중기에, 이조판서, 우의정, 좌의정 등을 역임한 문신.
    '김명윤': {'role': 'other'},  # 조선 - 조선 전기에, 의정부좌찬성, 지경연사, 판돈녕부사 등을 역임한 문신.
    '김명제': {'role': 'other'},  # 근대 - 일제강점기 때, 수원군 송산면 사강리의 독립만세시위에 참여한 독립운동가.
    '김명진': {'role': 'other'},  # 근대 - 조선 후기에, 경기관찰사, 경상도관찰사, 이조참판 등을 역임한 문신.
    '김명하': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 평안북도 강계군 강계면의 독립만세시위를 주도한 혐의로 체포된 독립운동가.
    '김명환': {'role': 'other'},  # 현대/대한민국 - 해방 이후 판소리 고법의 전승자로 지정된 예능보유자. 고수.
    '김명희': {'role': 'other'},  # 조선/조선 후기 - 조선후기 홍문관직제학, 강동현령을 역임한 서예가.
    '김몽호': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 사헌부장령, 공조참의 등을 역임한 문신.
    '김무': {'role': 'other'},  # 고대/삼국 - 삼국시대 신라의 파진찬을 역임한 의관.
    '김무규': {'role': 'other'},  # 현대/대한민국 - 해방 이후 구례향제줄풍류에서 단소의 전승자로 지정된 예능보유자. 단소, 거문고명인.
    '김무력': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 관산성전투에 참전한 장수.
    '김무림': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 소판 관등의 귀족.
    '김무석': {'role': 'other'},  # 현대/대한민국 - 해방 이후 맹호5호작전 당시의 군인.
    '김무선': {'role': 'scholar'},  # 고대/남북국/통일신라 - 남북국시대 때, 숙위학생으로 당나라에서 유학하여 빈공과에 급제한 통일신라의 학자.
    '김무알': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 제19대 눌지마립간 때 고구려에 질자로 간 복호(卜好)를 보좌한 관리.
    '김무정': {'role': 'other'},  # 근대 - 일제강점기 팔로군 포병단 단장, 조선의용군 총사령 등을 역임한 사회주의운동가.
    '김무체': {'role': 'scholar'},  # 고려 - 고려 전기에, 복야 등을 역임하였으며, 고려시대 사학(私學) 12도 중 하나인 서원도를 열
    '김무훈': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라에서 당나라에 파견된 사신.
    '김문': {'role': 'other'},  # 조선 - 조선 전기에, 집현전수찬, 집현전부교리, 집현전직제학 등을 역임한 문신 · 공신.
    '김문귀': {'role': 'other'},  # 고려 - 고려 후기에, 호군, 밀직부사 등을 역임한 문신.
    '김문근': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 영돈녕부사, 총융사, 훈련대장 등을 역임한 문신.
    '김문기': {'role': 'other'},  # 조선 전기에, 예문관검열, 병조참의, 형조참판 등을 역임한 문신.
    '김문길': {'role': 'other'},  # 현대/대한민국 - 해방 이후 제25사단 항공대 조종사 중위를 역임한 군인.
    '김문달': {'role': 'other'},  # 현대/대한민국 - 해방 이후 이리농악 전승자로 지정된 기예능보유자.
    '김문량': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 아찬으로 중시를 역임한 관리.
    '김문발': {'role': 'other'},  # 조선/조선 전기 - 조선전기 충청전라도수군도체찰추포사, 전라도수군절제사 등을 역임한 무신.
    '김문보': {'role': 'other foreigner'},  # 현대 - 중국공산당 연변지방위원회 위원 , 연변조선족자치주위원회 서기처 서기 등을 역임한 조선족 출
    '김문비': {'role': 'other'},  # 고려 - 고려후기 상장군, 삼익군 우군사, 군부판사 등을 역임한 무신.
    '김문빈': {'role': 'other'},  # 근대/대한제국기 - 대한제국기 때, 신경칠 의진의 참모장 및 중군장으로 활약한 의병.
    '김문상': {'role': 'scholar'},  # 현대/대한민국 - 서울대학교 섬유공학과 교수, 한국섬유공학회 회장, 한국표준심의위원회 위원장 등을 역임한 공
    '김문세': {'role': 'other'},  # 근대/일제강점기 - 대한민국임시정부 기관지인 독립신문의 기자로 활동한 독립운동가.
    '김문순': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 이조판서, 선혜청당상, 우참찬 등을 역임한 문신.
    '김문연': {'role': 'other'},  # 고려 - 고려 후기에, 좌우위산원, 첨의시랑찬성사, 첨의중호 등을 역임한 문신.
    '김문영': {'role': 'other'},  # 고대/남북국 - 삼국시대 나당연합군의 백제 정벌 당시의 장수.
    '김문왕': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라 제29대 태종무열왕의 셋째 아들인 왕자.
    '김문울': {'role': 'scholar'},  # 고대/남북국/통일신라 - 남북국시대 때, 당나라 빈공과에 급제하여 공부원외랑, 기왕부자의참군 등을 역임한 통일신라의
    '김문정': {'role': 'other'},  # 고려 - 고려 후기에, 국학학정, 사헌규정 등을 역임한 문신.
    '김문제': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 이조참의, 좌참찬, 경연관 등을 역임한 문신.
    '김문집': {'role': 'critic'},  # 근대/일제강점기 - 일제강점기 『비평문학』 · 『아리랑고개』 등을 저술한 평론가. 친일반민족행위자.
    '김문평': {'role': 'other'},  # 현대/대한민국 - 일제강점기 때, 한성은행 본정지점 지배인 대리, 동아일보 여수지국장 등을 역임하였으며, 해
    '김문현': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 형조판서, 예조판서, 전라도관찰사 등을 역임한 문신.
    '김문호': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 한국광복군으로 활동한 독립운동가.
    '김문희': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 임시정부 연통제 장서, 임시의정원 의원 등을 역임한 독립운동가.
    '김물유': {'role': 'other foreigner'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 대나마로 일본에 파견된 관리.
    '김미': {'role': 'other'},  # 조선 - 조선 전기에, 정주별선위사, 우승지, 첨지중추부사 등을 역임한 문신.
    '김미하일': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 한인사회당 부회장, 노보에쿠스코예의 구역당서기 등을 역임한 사회주의운동가.
    '김미향': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「영해별신굿놀이」 전승자로 지정된 예능보유자. 무속인.
    '김민선': {'role': 'other'},  # 조선 - 조선 전기에, 집의, 헌남, 인천부사 등을 역임한 문신.
    '김민순': {'role': 'poet'},  # 조선/조선 후기 - 조선후기 지평현감을 역임한 시인.
    '김민자': {'role': 'other'},  # 현대 - 해방 이후 최승희의 제자이며, 예그린악단의 안무가로 활동한 무용가.
    '김민재': {'role': 'scholar'},  # 조선 - 조선후기 담양군수, 제천군수 등을 역임한 문신. 학자.
    '김민주': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 대감을 역임한 장수.
    '김민택': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 남학교수, 실록청낭관, 지제교 등을 역임한 문신.
    '김민환': {'role': 'scholar foreigner'},  # 조선 - 조선 후기에, 「통사문답」, 「중국학통」, 『용암집』 등을 저술한 학자.
    '김반': {'role': 'other'},  # 조선 - 조선 후기에, 대사성, 대사간, 대사헌 등을 역임한 문신.
    '김반굴': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 황산벌전투에 참전한 장수.
    '김방걸': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 승지, 대사간, 대사성 등을 역임한 문신.
    '김방경': {'role': 'other foreigner'},  # 고려/고려 후기 - 고려 후기 삼별초의 난을 진압하고 몽골군과 함께 일본 정벌을 지휘했던 무신.
    '김방두': {'role': 'other'},  # 조선 - 조선시대 「죽지쌍금도」를 그린 화가.
    '김방서': {'role': 'other'},  # 근대 - 개항기 봉성 대접주, 금구의 접주 등을 역임한 천도교인.
    '김방행': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 평안도사, 대사성 등을 역임한 문신.
    '김백겸': {'role': 'other'},  # 조선/조선 전기 - 조선전기 겸사복장, 첨지중추부사, 평안도절도사 등을 역임한 무신.
    '김백균': {'role': 'other'},  # 고려 - 고려후기 삼사사, 밀직부사, 동지밀직사사 등을 역임한 무신.
    '김백만': {'role': 'other'},  # 근대 - 일제강점기 밀산반일유격대 대장을 역임한 사회주의운동가.
    '김백선': {'role': 'other'},  # 근대 - 개항기 때, 유인석 의진에서 선봉장으로 활약하였으나, 군기문란죄로 처형된 의병.
    '김백순': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 인산진첨사, 의주목사, 승지 등을 역임한 문신.
    '김백안': {'role': 'other'},  # 고려 - 고려후기 낭장, 대성, 평장사 등을 역임한 문신. 반란자.
    '김백일': {'role': 'other'},  # 근대/일제강점기 - 해방 이후 여순항쟁, 옹진반도전투에 참전한 군인. 친일반민족행위자.
    '김백흥': {'role': 'other'},  # 고려 - 고려후기 조전원수, 한양윤 등을 역임한 무신.
    '김번': {'role': 'scholar'},  # 조선 - 조선 전기에, 제용감첨정, 평양서윤, 시강원문학 등을 역임한 문신.
    '김범문': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 고달산에서 반란을 일으킨 주모자.
    '김범부': {'role': 'scholar'},  # 현대/대한민국 - 『화랑외사』, 『풍류정신』 등을 저술하며 불교철학, 동양철학 연구에 전념한 철학자.
    '김범우': {'role': 'other'},  # 조선 - 조선 후기, 을사추조적발사건과 관련된 천주교인.
    '김범이': {'role': 'other'},  # 근대/대한제국기 - 대한제국기 때, 어윤성 의진에 가담하여 군자금 모금 활동을 전개한 의병.
    '김범주': {'role': 'scholar'},  # 조선 - 조선 후기에, 『익와집』 등을 저술한 학자.
    '김범청': {'role': 'other'},  # 고대/남북국 - 남북국시대 통일신라의 김헌창의 난 당시의 귀족.
    '김법린': {'role': 'scholar'},  # 현대/대한민국 - 일제강점기 때, 만당, 조선청년동맹 등을 조직하여 항일투쟁을 전개하였으며, 해방 이후, 문
    '김법선': {'role': 'other'},  # 고대/삼국/신라 - 남북국시대 통일신라의 현성대왕으로 추봉된 신라의 귀족.
    '김변': {'role': 'other'},  # 고려 - 고려 후기에, 첨의참리, 집현전대학사, 동수국사 등을 역임한 문신.
    '김변광': {'role': 'other'},  # 조선 - 조선 후기에, 병조정랑, 용강현령, 공조참의 등을 역임한 문신.
    '김병걸': {'role': 'critic'},  # 현대/대한민국 - 해방 이후 『리얼리즘문학론』, 『민중문학과 민족현실』, 『실패한 인생 실패한 문학』 등을 
    '김병관': {'role': 'scholar'},  # 조선 - 조선 후기에, 『정산유고』 등을 저술한 학자.
    '김병교': {'role': 'other'},  # 조선 - 조선 후기에, 형조판서, 판의금부사, 상호군 등을 역임한 문신.
    '김병국': {'role': 'other'},  # 근대 - 개항기 때, 총리군국사무, 영돈녕부사 등을 역임한 문신.
    '김병기': {'role': 'other'},  # 조선 - 조선 후기에, 삼정이정청의 구관당상, 이조판서 등을 역임한 문신.
    '김병덕': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 우의정, 좌의정, 총리군국사무 등을 역임한 문신.
    '김병로': {'role': 'other'},  # 해방 이후 남조선과도정부 사법부 부장, 대법원장 등을 역임한 법조인. 정치인.
    '김병록': {'role': 'other'},  # 근대 - 일제강점기 때, 친일파 이완용 암살을 계획한 혐의로 체포된 독립운동가.
    '김병삼': {'role': 'other'},  # 현대/대한민국 - 해방 이후 육군헌병사령관, 육군본부 일반참모부 비서실장, 육군소장 등을 역임한 군인. 공무
    '김병서': {'role': 'other'},  # 현대/대한민국 - 일제강점기 농민복음학교 교장, 해주 구세요양원 부원장 등을 역임한 사회운동가. 의료인.
    '김병수': {'role': 'scholar'},  # 조선 - 조선 후기에, 『계미유고』 등을 저술한 학자.
    '김병시': {'role': 'other'},  # 근대/개항기 - 개항기 때, 예문관제학, 독판군국사무, 의정부의정 등을 역임한 문신.
    '김병연': {'role': 'poet'},  # 조선/조선 후기 - 조선 후기, ‘김삿갓’ 혹은 ‘김립(金笠)으로 널리 알려진 시인.
    '김병영': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 간도 용정촌에서 전개된 독립만세시위를 주도하다가 순국한 독립운동가.
    '김병욱': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 장악원주부, 연풍현감, 돈녕부정 등을 역임한 문신.
    '김병운': {'role': 'other'},  # 근대/일제강점기|현대 - 일제강점기 경성방직 기술책임자를 역임한 기술자.
    '김병익': {'role': 'other'},  # 근대 - 일제강점기 대사성, 궁내부 특진관, 조선귀족(남작) 등을 역임한 관료. 친일반민족행위자.
    '김병제': {'role': 'scholar'},  # 해방 이후 『조선어문법: 어음론 · 형태론』, 『조선어학사』 등을 저술한 학자. 국어학자.
    '김병조': {'role': 'other'},  # 근대 - 일제강점기 때, 한국독립당 동북의용군 사령, 중한연합군 부사령 등을 역임한 독립운동가.
    '김병종': {'role': 'scholar'},  # 조선 - 조선 후기에, 『성학속도』, 『학림통록』, 『문소가례』 등을 저술한 학자.
    '김병주': {'role': 'other'},  # 근대 - 조선 후기에, 한성부판윤, 경상도관찰사, 의정부좌참 등을 역임한 문신.
    '김병준': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 함경남도 이원의 천도교구장으로서 독립만세시위를 주도하였고, 대한민국임시정부
    '김병지': {'role': 'other'},  # 근대 - 조선 후기에, 공조판서, 형조판서, 함경도감사 등을 역임한 문신.
    '김병찬': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 평안북도 강계군 강계면의 독립만세시위에 참여했다가 순국한 독립운동가.
    '김병태': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 의열단에서 활동하며 조선혁명간부학교 군사교관, 김원봉 비서 등을 역임한 독
    '김병필': {'role': 'other'},  # 조선 - 조선 후기에, 좌의정, 홍문관부제학, 예조판서 등을 역임한 문신.
    '김병학': {'role': 'other'},  # 근대 - 일제강점기 때, 광복군에 입대하여 학병탈출공작과 정보 수집 활동을 전개한 독립운동가.
    '김병호': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 김창조의 제자로 조선창극단, 임방울창극단에서 활동한 가야금산조의 명창.
    '김병화': {'role': 'other'},  # 현대/대한민국 - 소련에서 소련군 장교, 공산당 당원으로 지내다가 우즈베키스탄으로 강제이주를 당하여 북극성 
    '김병환': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 의열단에서 무장투쟁을 전개하였으며, 밀양청년회 문화부장, 신간회 밀양지회 
    '김병회': {'role': 'other'},  # 현대/대한민국 - 조선일보사 목포지국장, 제헌국회의원 등을 역임하였으며, 국회프락치사건으로 복역하다가 한국전
    '김보': {'role': 'other'},  # 고려 - 고려 후기에, 중서문하시랑평장사판밀직, 도첨의찬성사, 수시중 등을 역임한 문신.
    '김보가': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 대감으로 나당연합군의 고구려 원정 시 당나라에 파견된 관리.
    '김보근': {'role': 'other'},  # 조선 - 조선 후기에, 좌참찬, 예문관제학, 광주유수 등을 역임한 문신.
    '김보남': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 아악수, 아악수장, 아악사 등을 역임한 음악인. 무용가.
    '김보당': {'role': 'other'},  # 고려 - 고려 후기에, 우간의, 공부시랑, 간의대부 겸 동북면병마사 등을 역임한 문신.
    '김보생': {'role': 'other'},  # 고려 - 고려 후기에, 정조사, 판도판서, 지밀직 등을 역임한 문신.
    '김보연': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 대한민국임시정부 임시의정원 황해도 의원이자 임시정부 경제후원회의 준비위원으로 임
    '김보정': {'role': 'other'},  # 고려 - 고려 후기에, 추밀원사, 지문하성사, 이부상서 등을 역임한 무신.
    '김보택': {'role': 'scholar'},  # 조선/조선 후기 - 조선 후기에, 문학, 보덕, 전라도관찰사 등을 역임한 문신.
    '김보현': {'role': 'other'},  # 현대/대한민국 - 해방 이후 농림부장관, 체신부장관, 전라남도지사 등을 역임한 관료.
    '김보형': {'role': 'other'},  # 근대 - 일제강점기 때, 만주에서 군자금 모금 및 의용군 조직책으로 활동하였으며, 정의부, 고려혁명
    '김복근': {'role': 'other'},  # 조선/조선 전기 - 조선전기 예조판서 성현 등과 『악학궤범』 편찬에 참여한 음악인.
    '김복대': {'role': 'other foreigner'},  # 고려/고려 후기 - 고려후기 삼별초 토벌, 여몽연합군 일본 정벌 등과 관련된 무신.
    '김복윤': {'role': 'other'},  # 고려/고려 전기 - 고려 전기에, 황주목서기, 동경유수판관, 행대영령 등을 역임한 문신.
    '김복일': {'role': 'other'},  # 조선 - 조선 전기에, 사예, 사성, 풍기군수 등을 역임한 문신.
    '김복진': {'role': 'scholar'},  # 근대/일제강점기 - 일제강점기 「백화」, 「소년」, 「다산선생상」 등의 작품을 낸 조각가. 독립운동가.
    '김복택': {'role': 'other'},  # 조선 - 조선 후기에, 영휘전참봉 등을 역임한 문신.
    '김복한': {'role': 'other'},  # 근대 - 개항기 때, 승정원승지, 형조참의 등을 역임하다가 을미사변 이후 의병활동을 전개하였으며, 
    '김복호': {'role': 'other foreigner'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 사찬으로 일본에 사신으로 간 관리.
    '김복흥': {'role': 'scholar'},  # 조선 - 조선시대 별제, 직장, 의금부도사 등을 역임한 문신. 학자.
    '김봉': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 평안도관찰사, 대사헌, 예조참판 등을 역임한 문신.
    '김봉관': {'role': 'other'},  # 근대/일제강점기 - 함경남도 갑산군 동인면 일대의 주재소, 면사무소 등을 습격한 독립운동가.
    '김봉국': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 고려혁명위원회를 조직하였고, 고려혁명당 간부 등을 역임한 독립운동가.
    '김봉규': {'role': 'other'},  # 근대 - 대한제국기 때, 기삼연 중심의 호남창의맹소에서 중군장으로 활약하였고, 기삼연 사후에 잔병을
    '김봉균': {'role': 'other'},  # 근대/개항기 - 개항기 갑신정변과 관련된 정객.
    '김봉남': {'role': 'other'},  # 근대 - 일제강점기 물법계 종교단체를 설립한 종교창시자.
    '김봉득': {'role': 'other'},  # 근대/개항기 - 개항기 동학운동에 참여한 천도교인.
    '김봉룡': {'role': 'other'},  # 현대 - 해방 이후 「나전장」 전승자로 지정된 기능보유자.
    '김봉모': {'role': 'other'},  # 고려 - 고려 후기에, 판합문사, 추밀원부사, 중서문하평장사 태자태부 등을 역임한 문신.
    '김봉문': {'role': 'other'},  # 근대 - 일제강점기 박기홍의 제자로 동편제 소리의 진수를 발휘한 판소리의 명창.
    '김봉수': {'role': 'other'},  # 근대 - 일제강점기 때, 정의부에서 군자금 모금 및 밀정 처단 활동을 전개한 독립운동가.
    '김봉식': {'role': 'other'},  # 근대 - 일제강점기 때, 만주에서 대한통의부 독립결사대에 가입하여 군자금 모금 활동을 전개한 독립운
    '김봉원': {'role': 'other'},  # 근대 - 일제강점기 때, 국내에서 군자금 모금 활동을 전개해 임시정부를 지원하였으며, 강동경찰서에 
    '김봉재': {'role': 'other'},  # 현대 - 해방 이후 대한유리공업주식회사 대표이사, 중소기업진흥재단 이사장 등을 역임한 실업가. 정치
    '김봉조': {'role': 'other'},  # 현대/대한민국 - 일제강점기 때, 영남상업고등학교 교장 등을 역임하였으며 해방 이후, 제헌국회의원, 제2대 
    '김봉학': {'role': 'other'},  # 근대 - 일제강점기 명창 김창환의 아들로 김창환협률사에 참가한 판소리의 명창.
    '김봉현': {'role': 'other'},  # 근대 - 일제강점기 때, 경기도 안성군 원곡면과 양성면 일대의 독립만세시위에 참여한 독립운동가.
    '김봉휴': {'role': 'other'},  # 고대/남북국/통일신라 - 후삼국시대 신라의 시랑으로 국서를 가지고 고려 태조에게 항복을 청하러 파견된 문신.
    '김부': {'role': 'other'},  # 고려 - 고려후기 낭장, 장군 겸 예부시랑 등을 역임한 무신.
    '김부륜': {'role': 'scholar'},  # 조선 - 조선 중기에, 동복현감 등을 역임하였으며, 『설월당집』 등을 저술한 학자.
    '김부식': {'role': 'scholar novelist'},  # 고려전기 직한림, 추밀원부사, 중서시랑평장사 등을 역임한 문신. 학자, 문인.
    '김부윤': {'role': 'other'},  # 고려 - 고려 후기에, 밀직부사, 서북면도지휘사, 도첨의찬성사 등을 역임한 무신.
    '김부의': {'role': 'other'},  # 고려 - 고려 전기에, 한림학사승지, 좌군수, 지추밀원사 등을 역임한 문신.
    '김부인': {'role': 'scholar'},  # 조선 - 조선전기 첨지중추부사, 창성부사 등을 역임한 무신. 학자.
    '김부일': {'role': 'other'},  # 고려 - 고려 전기에, 직한림원, 예부낭중, 보문각대제, 중서시랑 동중서문하평장사 등을 역임한 문신
    '김부필': {'role': 'other'},  # 고려 - 고려 전기에, 병마판관 등을 역임한 문신.
    '김북원': {'role': 'poet critic'},  # 근대 - 해방 이후 『조국』, 『운로봉』, 『대지의 아침』 등을 저술한 시인. 평론가.
    '김북향': {'role': 'novelist'},  # 현대/대한민국 - 해방 이후 북한에서 『로동의 나날』 · 『횃불을 찾아서』 · 『실바킹』 등을 저술한 작가.
    '김불': {'role': 'other'},  # 후삼국시대 신라의 집사시랑으로 후당에 파견된 관리.
    '김붕구': {'role': 'scholar novelist'},  # 현대 - 한국불어불문학회 회장을 역임하였으며, 『불문학 산고』, 『현실과 문학의 비원』, 『작가와 
    '김붕준': {'role': 'other'},  # 현대/대한민국 - 일제강점기 때, 임시정부의 수립과 운영에 참여하며 국무위원, 제15대 임시의정원 의장 등을
    '김붕해': {'role': 'scholar'},  # 조선 - 조선 후기에, 『운당집』 등을 저술한 학자.
    '김빙': {'role': 'other'},  # 조선 - 조선 중기에, 형조좌랑 등을 역임하였으며, 정여립의 모반사건에 대한 추국을 맡았으나 역적을
    '김사걸': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 평안북도 정주군의 독립만세시위에 참여했다가 순국한 독립운동가.
    '김사공': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 중시, 상대등, 장군 등을 역임한 관리. 장수.
    '김사국': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 3·1운동에 참가하고 고려공산동맹을 이끈 사회주의운동가, 독립운동가.
    '김사란': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 때, 당나라에 건너가 태복원외경을 역임하였으며, 당 현종의 명으로 귀국하여 성덕
    '김사량': {'role': 'novelist'},  # 근대/일제강점기 - 일제강점기 「물오리섬」, 「빛속에서」, 「태백산맥」 등을 저술한 소설가.
    '김사렴': {'role': 'other'},  # 고려 - 고려 후기에, 안렴사 등을 역임한 문신.
    '김사림': {'role': 'poet'},  # 현대/대한민국 - 해방 이후 『바람의 비밀』, 『송짓골 우화』, 『수몰지구』 등을 저술한 시인.
    '김사목': {'role': 'other'},  # 조선 - 조선 후기에, 황해도관찰사, 예조판서, 우의정 등을 역임한 문신.
    '김사묵': {'role': 'other'},  # 조선/조선 후기 - 조선후기 중추원찬의, 경상남도관찰사, 경기도관찰사 등을 역임한 관리.
    '김사미': {'role': 'other'},  # 고려/고려 후기 - 고려후기 경상북도 청도에서 농민들을 모아 반란을 일으킨 주모자.
    '김사신': {'role': 'other'},  # 남북국시대 통일신라에서 당나라에 사신으로 파견된 관리.
    '김사안': {'role': 'other'},  # 고려 - 고려 후기에, 동지밀직사사, 전라도관찰사 등을 역임한 문신.
    '김사양': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 아찬으로 당나라에 사신으로 파견된 관리.
    '김사엽': {'role': 'scholar foreigner'},  # 현대 - 『조선문학사』, 『이조시대의 가요연구』, 『일본의 만엽집』 등을 저술하였으며, 오사카외국어
    '김사용': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 3·1운동, 계몽운동과 대동청년단 · 의열단의 항일투쟁에 참여한 독립유공자.
    '김사우': {'role': 'other'},  # 조선/조선 전기 - 조선전기 병조판서, 평안도도절제사, 동지중추원사 등을 역임한 무신.
    '김사원': {'role': 'other'},  # 조선 - 조선시대 임진왜란 때, 의병을 규합하여 정제장으로 추대된 문신.
    '김사인': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 때, 신라 무열왕의 4세손으로, 장군, 상대등 등을 역임한 통일신라의 종실.
    '김사정': {'role': 'scholar'},  # 조선 - 조선 중기에, 임진왜란이 발발하자 곽재우 의진에 들어가 화왕산성전투에서 활약하였으며, 『계
    '김사종': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 제31대 신문왕의 아들인 왕자.
    '김사준': {'role': 'other'},  # 근대 - 조선 후기에, 궁내부특진관, 규장각지후관, 중추원참의 등을 역임한 문신.
    '김사철': {'role': 'other'},  # 근대 - 일제강점기 중추원 찬의, 규장각 제학, 조선귀족(남작) 등을 역임한 관료. 친일반민족행위자
    '김사행': {'role': 'other'},  # 고려 - 조선전기 겸판사헌부사, 판경흥부사 동판도평의사사 등을 역임한 환관.
    '김사혁': {'role': 'other'},  # 고려 - 고려후기 전리판서, 양광도상원수, 지문하사 등을 역임한 무신.
    '김사형': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 개성윤, 지문하부사 등을 역임하였으며, 이성계를 왕으로 추대해 조선 건국 이
    '김산': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 혁명행동 부주필, 북경시위원회 조직부장 등을 역임한 사회주의운동가.
    '김살유': {'role': 'other foreigner'},  # 고대/남북국 - 남북국시대 통일신라의 일길찬으로 일본에 사신으로 파견된 관리.
    '김삼개': {'role': 'other'},  # 고려 - 고려후기 김삼선과 동북면을 침략한 여진족의 관리.
    '김삼광': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 때, 파진찬, 이찬 관등에 임명된 통일신라의 귀족 · 관리.
    '김삼규': {'role': 'other'},  # 현대/대한민국 - 해방 이후 서울대학교 교수, 동아일보 편집국장 등을 역임한 언론인.
    '김삼룡': {'role': 'other'},  # 현대/대한민국 - 해방 이후 민주주의민족전선 상임위원, 남조선노동당 서울지도부 책임자 등을 역임한 사회주의운
    '김삼선': {'role': 'other'},  # 고려 - 고려후기 김삼개와 동북면을 침략한 여진족의 관리.
    '김삼성': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「통영오광대」 큰어미, 사자탈 역 전승자로 인정된 보유자.
    '김삼순': {'role': 'scholar'},  # 현대/대한민국 - 한국인 여성 최초의 농학 박사이자 과학자.
    '김삼조': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 아찬으로 집사성 시중을 역임한 관리.
    '김삼현': {'role': 'other'},  # 조선 - 조선후기 여항육인의 한 사람으로 은거한정을 노래한 음악인.
    '김상': {'role': 'other'},  # 고려/고려 후기 - 고려후기 무진정변과 관련된 노비.
    '김상갑': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 함경남도 단천의 독립만세시위를 주도하는 과정에서 순국한 독립운동가.
    '김상경': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 한산주소감을 역임한 장수.
    '김상구': {'role': 'other'},  # 조선 - 조선 후기에, 승지, 양천현감, 대사간 등을 역임한 문신.
    '김상규': {'role': 'other'},  # 조선 - 조선 후기에, 승지, 대사간 등을 역임한 문신.
    '김상기': {'role': 'scholar'},  # 근대 - 해방 이후 「동학과 동학란」, 「동방문화교류사논고」, 「고려시대사」 등을 저술한 학자. 역
    '김상길': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 대구상업학교 재학 중 항일 비밀결사인 태극단의 활동을 주도한 독립운동가.
    '김상덕': {'role': 'other'},  # 근대 - 조선 후기에, 인천부사 겸 감리인천항통상사무, 홍주부관찰사 등을 역임하였으며, 을사조약 이
    '김상돈': {'role': 'other'},  # 현대/대한민국 - 반민족행위특별조사위원회 부위원장, 제5대 민의원, 서울특별시장 등을 역임한 정치인.
    '김상로': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 병조판서, 예조참판, 영의정 등을 역임한 문신.
    '김상리': {'role': 'scholar'},  # 조선 - 조선 후기에, 선교랑, 돈녕부주부, 예빈시주부, 순릉참봉 등을 역임하였으며, 「경의」, 『
    '김상림': {'role': 'other foreigner'},  # 고대/남북국/통일신라 - 남북국시대 신라의 불교문화를 일본에 전한 귀족.
    '김상만': {'role': 'other'},  # 현대 - 해방 이후 동아일보 사장, 국제신문협회 본부이사 등을 역임한 언론인.
    '김상묵': {'role': 'other'},  # 조선/조선 후기 - 조선 후기, 정언, 교리, 헌납, 형조참의, 안동부사 등을 지낸 문신.
    '김상범': {'role': 'other'},  # 조선/조선 후기 - 조선후기 관상감관으로 시헌역법을 시행한 관료.
    '김상복': {'role': 'other'},  # 조선 - 조선 후기에, 홍문관제학, 우의정, 영의정 등을 역임한 문신.
    '김상석': {'role': 'other'},  # 조선 - 조선 후기에, 강화유수, 한성부우윤, 판돈녕부사 등을 역임한 문신.
    '김상성': {'role': 'other'},  # 조선 - 조선 후기에, 좌빈객, 판의금부사, 이조판서 등을 역임한 문신.
    '김상숙': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 사옹원주부, 공조정랑, 첨지중추부사 등을 역임한 문신.
    '김상순': {'role': 'other foreigner'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 급찬으로 일본에 파견된 관리.
    '김상신': {'role': 'other'},  # 근대/대한제국기 - 대한제국기 때, 이석용 의진에서 창의동맹의 도로부장으로 활약한 의병.
    '김상악': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 홍릉참봉, 첨지중추부사, 동지중추부사 등을 역임한 문신.
    '김상연': {'role': 'scholar'},  # 조선 - 조선 후기에, 『기기재집』 등을 저술한 학자.
    '김상열': {'role': 'novelist'},  # 현대/대한민국 - 해방 이후 「언챙이곡마단」, 「애니깽」, 「우린 나발을 불었다」 등의 작품을 낸 작가. 연
    '김상옥': {'role': 'poet'},  # 현대 - 해방 이후 『초적』, 『의상』, 『느티나무의 말』 등을 저술한 시인.
    '김상용': {'role': 'poet scholar'},  # 근대/일제강점기 - 일제강점기 『망향』을 저술한 시인. 영문학자, 교육자.
    '김상우': {'role': 'other'},  # 고려 - 고려 전기에 예부상서 · 이부상서 · 형부상서 등을 역임한 문신.
    '김상원': {'role': 'other'},  # 조선 - 조선 후기에, 강원도관찰사, 개성부유수, 대사간 등을 역임한 문신.
    '김상을': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 1945년 한국광복군 제2지대와 미국 전략정보국(OSS)이 함께 추진한 독수리작
    '김상익': {'role': 'other'},  # 조선 - 조선 후기에, 대사성, 부제학, 도승지 등을 역임한 문신.
    '김상일': {'role': 'scholar'},  # 조선 - 조선 후기에, 「문견록」, 『일엄유고』 등을 저술한 학자.
    '김상적': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 동지의금부사, 예조참판, 형조참판 등을 역임한 문신.
    '김상전': {'role': 'scholar'},  # 조선 - 조선 후기에, 『경의답문』, 『영은문집』 등을 저술한 학자.
    '김상정': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 의성현령, 승지, 대사간 등을 역임한 문신.
    '김상제': {'role': 'other'},  # 고려 - 고려 전기에, 판합문사를 역임한 문신.
    '김상준': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 한국광복군 인면전구공작대 대원으로 인도와 버마(지금의 미얀마) 국경지대인 임팔 
    '김상중': {'role': 'other'},  # 조선 - 조선 후기에, 도승지, 한성부부윤, 공조판서 등을 역임한 문신.
    '김상직': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 좌윤, 형조참판, 도승지 등을 역임한 문신.
    '김상진': {'role': 'other'},  # 현대/대한민국 - 대한민국의 민주화운동가로, 1975년 4월 11일 유신체제에 항거하여 할복 자살한 인물.
    '김상집': {'role': 'other'},  # 조선 - 조선 후기에, 공조판서, 예조판서, 우참찬 등을 역임한 문신.
    '김상채': {'role': 'poet'},  # 조선 - 조선후기 『창암집』을 저술한 시인.
    '김상철': {'role': 'other'},  # 조선 - 조선 후기에, 우의정, 좌의정, 영의정 등을 역임한 문신.
    '김상태': {'role': 'other'},  # 근대/대한제국기 - 대한제국기 때. 이강년 의진에서 중군장으로 활약하였으며, 경기도, 강원도, 경상도 일대에서
    '김상한': {'role': 'other'},  # 근대 - 대한제국기 때, 이강년 의진에서 좌익장으로 활약하다가 경상북도 의병장이 되어 항일의병투쟁을
    '김상헌': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 충청남도 천안의 아우내 독립만세시위에 참여했다가 순국한 독립운동가.
    '김상현': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 우참찬, 좌참찬, 판돈녕부사 등을 역임한 문신.
    '김상협': {'role': 'other'},  # 현대/대한민국 - 고려대학교 총장, 문교부장관, 국무총리, 대한적십자사 총재 등을 역임한 교육자 · 관료.
    '김상호': {'role': 'other'},  # 현대/대한민국 - 일제강점기 때, 임시정부를 지원하고 친일승려들을 규탄하는 등 불교계 중심인물이 되어 항일투
    '김상효': {'role': 'scholar'},  # 근대 - 조선 후기에, 『양사재기』, 『경재기』, 『경재유고』 등을 저술한 학자.
    '김상훈': {'role': 'poet critic'},  # 근대 - 해방 이후 「편복」, 「경부선」, 「전원애화」 등을 저술한 시인. 평론가.
    '김상휴': {'role': 'other'},  # 조선 - 조선 후기에, 판의금부사, 예문관제학, 이조판서 등을 역임한 문신.
    '김생': {'role': 'scholar'},  # 고대/삼국 - 남북국시대 통일신라에서 「태자사낭공대사백월서운탑비」, 「여산폭포시」, 「창림사비」 등의 작
    '김생려': {'role': 'other'},  # 현대/대한민국 - 해방 이후 서울시립교향악단의 초대지휘자, 남가주필하모닉 상임지휘자 등을 역임한 지휘자. 바
    '김서': {'role': 'other'},  # 고려 - 고려후기 서북면순문사, 동지밀직사사, 판밀직사사 등을 역임한 무신.
    '김서규': {'role': 'other'},  # 근대 - 일제강점기, 전라남도 지사, 경상북도 지사, 중추원 참의 등을 역임한 관료 · 친일반민족행
    '김서성': {'role': 'scholar'},  # 조선/조선 전기 - 조선 전기에, 문학, 필선, 사재감정 등을 역임한 문신.
    '김서일': {'role': 'scholar'},  # 조선 - 조선 후기에, 『전긍재집』 등을 저술한 학자.
    '김서정': {'role': 'other foreigner'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 사찬으로 일본에 파견된 관리.
    '김서종': {'role': 'other'},  # 근대 - 일제강점기 경의원참의, 총본사전강, 천전건축주비회 부위원장 등을 역임한 대종교인.
    '김서현': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 지방관 및 장군으로 활동한 김유신의 아버지.
    '김석': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 대한교민단의경대 간부, 상해 한인청년당 이사장, 임시정부 외교부장 비서장 
    '김석견': {'role': 'other'},  # 조선 - 조선 중기에, 임진왜란이 발발하자 세 아들을 이끌고 의병을 일으켜 창암전투에서 활약한 의병
    '김석관': {'role': 'other'},  # 현대/대한민국 - 해방 이후 교통부차관, 교통부장관 등을 역임한 관료.
    '김석규': {'role': 'other'},  # 근대 - 조선 후기에, 평리원판사, 한성재판소 수반판사, 형법교정관 등을 역임한 문신.
    '김석근': {'role': 'other'},  # 근대 - 개항기 때, 궁내부특진관, 경효전제조, 장례원경 등을 역임한 문신.
    '김석동': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 1940년 9월 한국광복군에 입대하여 제2지대 본부요원으로 활동하였고, 1943
    '김석문': {'role': 'scholar'},  # 조선/조선 후기 - 조선 후기에, 『역학도해』를 저술하였으며, 최초로 지전설을 주장한 학자.
    '김석신': {'role': 'scholar'},  # 조선/조선 후기 - 조선후기 「도봉도」, 「가고중류도」, 「좌수도해도」 등의 작품을 그린 화가.
    '김석연': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 강화유수, 어영대장, 형조판서 등을 역임한 문신.
    '김석옥': {'role': 'scholar'},  # 조선 - 조선 전기에, 생원이 된 후 벼슬을 지내지 않고 음률을 즐기며 은거하였으며, 호조참판에 추
    '김석운': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 평안북도 의주군 고령삭면 영산시장의 독립만세시위를 주도하는 과정에서 순국한
    '김석원': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 중일전쟁, 북어사건 당시의 군인. 교육자, 친일반민족행위자.
    '김석익': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 개성유수, 총융사, 한성좌윤 등을 역임한 문신.
    '김석일': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 지평, 정언, 동래부사 등을 역임한 문신.
    '김석주': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 이조좌랑, 우의정 등을 역임한 문신.
    '김석준': {'role': 'poet'},  # 근대 - 조선 후기부터 일제강점기 사이에, 활동한 역관. 시인. 서예가.
    '김석지': {'role': 'novelist'},  # 조선/조선 후기 - 조선 후기, 서북 지역 출신의 문인.
    '김석진': {'role': 'other'},  # 근대 - 조선 후기에, 홍문관장령, 삼도육군통어사, 판돈녕부사 등을 역임한 문신.
    '김석찬': {'role': 'other'},  # 현대/대한민국 - 해방 이후 염천교회를 설립하고, 문창교회에 부임 목회한 목사.
    '김석창': {'role': 'other'},  # 근대 - 일제강점기 때, 선천경찰서 투탄 의거를 지원한 목사 · 독립운동가.
    '김석철': {'role': 'other'},  # 조선/조선 전기 - 조선전기 공조참판, 병조참판, 동지중추부사 등을 역임한 무신.
    '김석출': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「동해안 별신굿」 전승자로 지정된 예능보유자.
    '김석항': {'role': 'other'},  # 근대/대한제국기 - 대한제국기 때, 궁내부 물품사 주사를 역임하였으며, 을사오적 암살을 계획하다 체포되어 순국
    '김석형': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 「리조병제사」, 「조선통사」, 「초기 조일관계 연구」 등을 저술한 학자. 역사학
    '김석황': {'role': 'other'},  # 근대 - 일제강점기 때, 2·8독립선언에 가담하였으며, 임시정부 특파원, 의용단 서무부장, 임시의정
    '김석희': {'role': 'scholar'},  # 조선 - 조선후기 성균관사성, 형조참지 등을 역임한 문신. 학자.
    '김선': {'role': 'other'},  # 조선 - 조선 후기에, 형조판서, 한성부판윤 등을 역임한 문신.
    '김선궁': {'role': 'other'},  # 고려 - 고려전기 삼중대광 문하시중을 역임한 장수.
    '김선기': {'role': 'scholar'},  # 근대/대한제국기 | 근대/일제강점기 | 현대 - 일제강점기 때, 조선어학회에서 활동하였으며, 해방 이후 문교부차관, 한글학회 이사 등을 역
    '김선두': {'role': 'other'},  # 근대 - 일제강점기, 조선예수교장로회 총회장으로서 평양 장로교계 3·1운동을 주동했던 목사.
    '김선량': {'role': 'other'},  # 근대 - 일제강점기 때, 동우회에 가입하여 기관지 『동광』을 발간하고 항일투쟁을 전개한 독립운동가.
    '김선봉': {'role': 'other'},  # 현대 - 해방 이후 봉산탈춤 전승자로 지정된 기예능보유자.
    '김선석': {'role': 'other'},  # 고려 - 고려 전기에, 추밀원사, 좌복야판호부사, 중서시랑평장사 등을 역임한 문신.
    '김선여': {'role': 'other'},  # 근대 - 대한제국기 때, 신보현 의진에서 선봉장으로 활약하다가 독자적으로 의진을 조직하여 항일의병투
    '김선영': {'role': 'other'},  # 현대 - 해방 이후 「자명고」, 「마의태자」, 「은하수」 등에 출연한 배우.
    '김선장': {'role': 'other'},  # 고려/고려 후기 - 고려후기 신궁건축 감독관, 청도군 지군사 등을 역임한 무신.
    '김선치': {'role': 'other'},  # 고려 - 고려후기 전리판서, 계림부윤 등을 역임한 무신.
    '김선태': {'role': 'other'},  # 현대/대한민국 - 일제강점기 전주지방법원 판사, 대전지방법원 청주지청 판사 등을 역임한 법조인. 정치인.
    '김선평': {'role': 'other'},  # 고려 - 고려전기 대광, 아보 등을 역임한 무신.
    '김선필': {'role': 'other'},  # 근대 - 개항기 지삼군부사, 대호군, 강화부유수 등을 역임한 무신.
    '김선행': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 대사헌, 좌윤 등을 역임한 문신.
    '김설': {'role': 'other'},  # 조선 - 조선 후기에, 검열, 대교, 예빈시정 등을 역임한 문신.
    '김섬': {'role': 'other'},  # 조선 - 조선시대 임진왜란 당시 의기(義妓)로 알려진 기생.
    '김성': {'role': 'other'},  # 고려 - 고려후기 제주부사 장윤화의 침학에 반란을 일으킨 주모자.
    '김성곤': {'role': 'other'},  # 현대 - 해방 이후 금성방직, 쌍용양회 등을 설립한 실업가. 언론인 · 정치인.
    '김성구': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 강원도관찰사, 병조참지, 호조참의 등을 역임한 문신.
    '김성규': {'role': 'other'},  # 조선 - 조선 후기에, 고창군수, 장성군수, 강원도순찰사 등을 역임한 문신.
    '김성균': {'role': 'scholar'},  # 근대 - 해방 이후 「국사강좌」, 「한국사입문」, 「세계문화사」 등을 저술한 학자. 역사학자.
    '김성근': {'role': 'other'},  # 근대 - 일제강점기 때, 임시의정원 함경도대표의원, 구국모험단 단장 등을 역임한 독립운동가.
    '김성기': {'role': 'other'},  # 현대/대한민국 - 서울지방검찰청 부장검사, 대검찰청 총무부 부장, 법무부장관 등을 역임하다가 박종철 고문치사
    '김성대': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「양주별산대놀이」 연희 및 가면 제작 전승자로 지정된 기능보유자.
    '김성도': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 광복군 제3지대에 입대하여 광복군 징모 공작을 전개한 독립운동가.
    '김성동': {'role': 'other'},  # 조선 - 조선 전기에, 당상관, 부평부사, 가선대부 등을 역임한 문신.
    '김성룡': {'role': 'other'},  # 현대/대한민국 - 해방 이후 공군사관학교 교장, 공군참모총장, 대장 등을 역임한 군인.
    '김성립': {'role': 'other'},  # 조선/조선 전기 - 조선 전기 승문원정자, 홍문관저작 등을 지냈고, 허난설헌의 남편이자 문장가인 문신.
    '김성무': {'role': 'other'},  # 근대 - 일제강점기 때, 조선여자기독교청년회연맹을 창설하고, 근우회 조직활동에 참여한 교육자 · 독
    '김성발': {'role': 'other'},  # 조선 - 조선 후기에, 원주목사, 종부시정, 금산군수 등을 역임한 문신.
    '김성배': {'role': 'other'},  # 현대/대한민국 - 해방 이후 건설부장관, 서울시장, 강원도지사 등을 역임한 관료.
    '김성범': {'role': 'other'},  # 근대 - 일제강점기 때, 천마단 사령부 오장으로 활동하며 항일무장투쟁을 전개한 독립운동가.
    '김성수': {'role': 'other'},  # 근대 - 일제강점기 때 의열단 · 남화한인청년연맹 등에서 활동하며 친일파 처단 등 항일무장투쟁을 전
    '김성숙': {'role': 'other'},  # 현대/대한민국 - 일제강점기 때, 조선의용대 정치부장, 임시정부 국무위원 등을 역임하였으며, 해방 이후, 혁
    '김성식': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 「대학사」, 「역사와 현실」 , 「내가 본 서양」 등을 저술한 학자. 역사학자.
    '김성업': {'role': 'other'},  # 근대 - 일제강점기 때, 동아일보 평양지국장, 조선물산장려회 이사장, 소년척후대 평안남도연맹 부이사
    '김성열': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 천도교 전교사로 활동하며 구국동지회에 가입하였고, 수원의 독립만세시위를 주
    '김성엽': {'role': 'other'},  # 근대 - 일제강점기 때, 광복군사령부 국내특파원으로 활동하며 친일파 숙청, 군자금 모금, 국내 조직
    '김성옥': {'role': 'other'},  # 조선 - 조선후기 진양조장단을 처음 판소리에 응용한 판소리의 명창.
    '김성원': {'role': 'scholar'},  # 조선 - 조선시대 제원도찰방, 동복현감 등을 역임한 문신. 학자.
    '김성은': {'role': 'other'},  # 현대/대한민국 - 해방 이후 해병교육단장, 해병대 부사령관, 해병대사령관 등을 역임한 군인. 관료.
    '김성응': {'role': 'other'},  # 조선/조선 후기 - 조선후기 판의금부사, 병조판서, 훈련대장 등을 역임한 무신.
    '김성익': {'role': 'other'},  # 조선 - 조선 후기에, 참봉, 시직, 부수 등을 역임한 문신.
    '김성일': {'role': 'other'},  # 조선 - 조선후기 도총부경력, 영원군수, 삭주도호부사 등을 역임한 무신.
    '김성적': {'role': 'other'},  # 조선 - 조선 후기에, 대사간, 이조참의, 충청도관찰사 등을 역임한 문신.
    '김성진': {'role': 'other'},  # 현대/대한민국 - 해방 이후 동양통신 정치부장 겸 편집부국장, 연합통신 사장 등을 역임한 언론인. 관료.
    '김성춘': {'role': 'scholar'},  # 근대 - 해방 이후 「자유만세」 · 「오발탄」 등의 작품에 관여한 영화인. 영화조명기사.
    '김성칠': {'role': 'scholar'},  # 현대 - 해방 이후 「조선역사」, 「동양사개설」 등을 저술한 학자. 역사학자.
    '김성탁': {'role': 'scholar'},  # 조선 - 조선후기 사간원정언, 홍문관수찬 등을 역임한 문신. 학자.
    '김성태': {'role': 'scholar'},  # 현대/대한민국 - 고려대학교 교수, 한국심리학 회장 등을 역임하였으며, 『실험연구의 방법』, 『발달심리학』 
    '김성택': {'role': 'other'},  # 근대/일제강점기 | 현대 - 해방 이후 북한에서 고려청자 제작기술을 재현하여 도자기를 제작한 공예가. 도자공예가.
    '김성하': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 병자호란 당시 남한산성에서 인조를 호종한 문신.
    '김성학': {'role': 'other'},  # 근대 - 일제강점기 용산 예수성심신학교, 평양성당 등에서 사목한 신부.
    '김성한': {'role': 'novelist'},  # 근대/일제강점기 | 현대 - 해방 이후 「오 분간」 · 「바비도」, 『임진왜란』 등을 저술한 소설가.
    '김성현': {'role': 'other'},  # 근대 - 일제강점기 때, 전라남도 곡성, 담양에서 군자금 모금 활동을 전개한 독립운동가.
    '김성호': {'role': 'other'},  # 근대 - 일제강점기 때, 대한정의군정서 사찰과 서기 등을 역임하였으며, 선천경찰서 투탄 의거에 가담
    '김성환': {'role': 'other'},  # 현대/대한민국 - 해방 이후 은행감독원 원장, 한국은행 총재 등을 역임한 금융인. 정치인.
    '김성후': {'role': 'scholar'},  # 조선 - 조선후기 풍기군수, 성균관사성, 사간원사간 등을 역임한 문신. 학자.
    '김성휘': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 상해청년연맹에서 항일투쟁을 전개한 독립운동가.
    '김세광': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 조선혁명간부학교 교관, 조선민족혁명당 중앙군사학 편찬위원, 조선의용대 제3
    '김세균': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 좌참찬, 수원유수 등을 역임한 문신.
    '김세기': {'role': 'other'},  # 근대 - 개항기 때, 비서원경, 시종원경, 전라남도관찰사 등을 역임한 문신.
    '김세덕': {'role': 'other'},  # 고려 - 고려 후기에, 친종호군 등을 역임한 무신 · 공신.
    '김세련': {'role': 'other'},  # 현대/대한민국 - 한국산업은행 총재, 재무부장관, 한국은행 총재, 국회의원 등을 역임한 금융인 · 정치인.
    '김세렴': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 도승지, 호조판서 등을 역임한 문신.
    '김세록': {'role': 'scholar'},  # 조선/조선 후기 - 조선후기 「신죽」 · 「통죽」 · 「죽보」 등의 작품을 그린 화가.
    '김세민': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 인순부윤, 전라도관찰사, 판돈녕부사 등을 역임한 문신.
    '김세연': {'role': 'other'},  # 근대/일제강점기 | 현대 - 해방 이후 조선건축기술단 초대단장, 조선토건협회 초대회장 등을 역임한 건축가.
    '김세열': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 항일단체인 구국동지회에 가입하였고, 수원의 독립만세시위에 참여했다가 고주리
    '김세용': {'role': 'other'},  # 근대 - 일제강점기 때, 광복군에서 활동하며 정보 수집과 초모공작을 전개한 독립운동가.
    '김세우': {'role': 'other'},  # 조선 - 조선 전기에, 전적, 적성현감 등을 역임한 문신.
    '김세익': {'role': 'other'},  # 조선 - 조선 후기에, 지평, 승지, 경상도관찰사 등을 역임한 문신.
    '김세일': {'role': 'novelist'},  # 현대/대한민국 - 해방 이후 레닌기치 기자를 역임한 작가. 언론인.
    '김세적': {'role': 'other'},  # 조선/조선 전기 - 조선전기 충청도관찰사, 형조참판, 행첨지중추부사 등을 역임한 무신.
    '김세정': {'role': 'other'},  # 조선 - 조선 후기에, 헌납, 집의, 우부승지 등을 역임한 문신.
    '김세종': {'role': 'other'},  # 조선 - 조선후기 신재효의 제자로 판소리 이론에 뛰어났던 판소리의 명창.
    '김세중': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 「십자가」, 「최후의 심판도」, 「충무공이순신장군상」 등의 작품을 낸 조각가.
    '김세지': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 대한애국부인회 재무부 부부장으로 활동한 개신교인. 전도부인.
    '김세진': {'role': 'other'},  # 현대/대한민국 - 대한민국의 학생운동가 · 반미운동가 · 반전운동가로, 1980년대 반미자주화운동을 선도한 
    '김세충': {'role': 'other'},  # 고려 - 고려 후기에, 야별초지유를 역임한 문신.
    '김세탁': {'role': 'other'},  # 근대 - 일제강점기 때, 105인 사건으로 복역하였으며, 출옥 후 만주로 망명하여 한족회에서 활동하
    '김세필': {'role': 'scholar'},  # 조선 - 조선전기 전라도관찰사, 대사헌, 이조참판 등을 역임한 문신. 학자.
    '김세행': {'role': 'other'},  # 조선 - 조선 후기에, 대동찰방을 역임한 문신.
    '김세형': {'role': 'other'},  # 현대/대한민국 - 일제강점기 「먼길」 · 「오텔로」 · 「뱃노래」 등을 만든 작곡가.
    '김세호': {'role': 'other'},  # 근대 - 조선 후기에, 경상도관찰사, 한성부판윤 등을 역임한 문신.
    '김세환': {'role': 'other'},  # 근대 - 일제강점기 때, 삼일남녀학교와 수원상업학교를 설립하여 후진교육에 힘쓴 교육자 · 독립운동가
    '김세흠': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 지평, 교리, 수찬 등을 역임한 문신.
    '김소': {'role': 'other'},  # 조선 - 조선 전기에, 성균관사성, 종학박사 등을 역임한 문신.
    '김소랑': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 신극 초창기 신파 배우.
    '김소모': {'role': 'other foreigner'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 살찬으로 일본에 사신으로 파견된 관리.
    '김소엽': {'role': 'poet novelist'},  # 근대 - 일제강점기 「배우에게」, 「흙 한 줌 쥐고」 등을 저술한 시인. 소설가.
    '김소운': {'role': 'poet essayist'},  # 근대/일제강점기 - 일제강점기 「신조」 등을 저술한 시인. 수필가 · 번역문학가.
    '김소월': {'role': 'poet'},  # 일제강점기 「금잔디」, 「첫치마」, 「엄마야 누나야」 등을 저술한 시인.
    '김소진': {'role': 'novelist'},  # 현대/대한민국 - 해방 이후 『열린사회와 그 적들』, 『자전거 도둑』, 『양파』 등을 저술한 소설가.
    '김소충': {'role': 'other foreigner'},  # 남북국시대 통일신라의 대통사로 일본에 파견된 관리.
    '김소희': {'role': 'other'},  # 현대/대한민국 - 해방 이후 판소리의 전승자로 지정된 예능보유자.
    '김속명': {'role': 'other'},  # 고려 - 고려 후기에, 첨의평리, 평양도도순문사, 대사헌 등을 역임한 문신.
    '김송': {'role': 'novelist'},  # 근대/일제강점기 - 일제강점기 「국경의 주막」, 「추계」, 「봉황금」 등을 저술한 작가. 소설가.
    '김수': {'role': 'other'},  # 조선 - 조선 중기에, 경상도관찰사, 한성판윤, 호조판서 등을 역임한 문신.
    '김수강': {'role': 'other'},  # 고려 - 고려 후기에, 직사관, 시어사, 중서사인 등을 역임한 문신.
    '김수경': {'role': 'other'},  # 조선 - 조선 전기에, 장단부사, 연안부사, 이천부사 등을 역임한 문신.
    '김수곡': {'role': 'other foreigner'},  # 근대 - 대한제국기 때, 정관직 의진에서 군자금 모금, 일본인 관리 처단 활동 등을 전개한 의병.
    '김수규': {'role': 'scholar'},  # 조선/조선 후기 - 조선후기 「사옹귀조도」 · 「기려도강도」 등의 작품을 그린 화가.
    '김수근': {'role': 'other'},  # 현대/대한민국 - 해방 이후 공간사옥, 마산성당 등을 신축한 건축가.
    '김수남': {'role': 'other'},  # 근대 - 일제강점기 때, 군산공립보통학교 방화사건을 주도한 독립운동가.
    '김수담': {'role': 'scholar'},  # 조선 - 조선후기 예조좌랑, 고령현감 등을 역임한 문신. 학자.
    '김수돈': {'role': 'poet'},  # 현대/대한민국 - 해방 이후 『소연가』, 『우수의 황제』 등을 저술한 시인.
    '김수동': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 경상남도 창원의 삼진 만세운동을 주도하는 과정에서 순국한 독립운동가.
    '김수렴': {'role': 'other'},  # 조선 - 조선 후기에, 사섬시부정, 절충장군, 첨지중추부사 등을 역임한 문신.
    '김수령': {'role': 'scholar'},  # 조선/조선 전기 - 조선전기 대사간, 참판 등을 역임한 문신. 학자.
    '김수만': {'role': 'other'},  # 고려 - 고려 후기에, 진원부원군 등을 역임한 환관 · 공신.
    '김수문': {'role': 'other'},  # 조선/조선 전기 - 조선전기 지중추부사, 한성판윤, 평안도병마절도사 등을 역임한 무신.
    '김수미산': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 사찬 관등의 귀족.
    '김수민': {'role': 'other'},  # 근대 - 대한제국기 때, 경기도 장단에서 의병을 일으켜 13도총도독으로 활약한 의병장.
    '김수산': {'role': 'other'},  # 현대/대한민국 - 해방 이후 브라질에서 한인교포사회의 경제적 기반을 만든 교민. 의류제조업자.
    '김수석': {'role': 'other'},  # 현대 - 해방 이후 「북청사자놀음」 전승자로 지정된 기예능보유자.
    '김수선': {'role': 'other'},  # 현대/대한민국 - 제헌국회의원, 제3대 국회의원 등을 역임한 정치인.
    '김수성': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 경기도관찰사, 황해도관찰사, 공조참의 등을 역임한 문신.
    '김수악': {'role': 'other'},  # 현대/대한민국 - 진주검무와 진주교방굿거리춤 예능보유자. 전통무용가.
    '김수영': {'role': 'poet'},  # 현대 - 해방 이후 「달나라의 장난」, 「헬리콥터」, 「폭포」 등을 저술한 시인.
    '김수온': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 지영천군사, 판중추부사, 호조판서 등을 역임한 문신.
    '김수익': {'role': 'other'},  # 조선 - 조선 후기에, 응교, 병조참의, 제주목사 등을 역임한 문신.
    '김수인': {'role': 'other'},  # 조선 - 조선후기 양주목사, 수원부사, 익산군수 등을 역임한 문신. 서예가.
    '김수자': {'role': 'other'},  # 고려 - 고려 전기에, 국학학유, 직사관, 예주방어사 등을 역임한 문신.
    '김수장': {'role': 'other'},  # 조선 - 조선후기 3대 시조집의 하나인 『해동가요』를 편찬한 음악인.
    '김수정': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 하규일의 제자로 여창가곡의 명창.
    '김수제': {'role': 'other'},  # 고려 - 고려후기 백주소복별감을 역임한 관리.
    '김수조': {'role': 'other'},  # 현대 - 해방 이후 브라질 농업이민을 태동시킨 교민.
    '김수증': {'role': 'scholar'},  # 조선/조선 후기 - 조선 후기에, 세마, 형조정랑, 공조정랑 등을 역임하였으며, 『곡운집』, 『곡운구곡도첩』 
    '김수창': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 병자호란 당시 남한산성에서 인조를 호종한 문신.
    '김수천': {'role': 'other'},  # 근대 - 일제강점기 아악에 정통한 음악인. 장구명인.
    '김수철': {'role': 'scholar'},  # 조선/조선 후기 - 조선후기 「송계한담도」 · 「자양화도」 등의 작품을 그린 화가.
    '김수충': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 제33대 성덕왕의 아들인 왕자.
    '김수학': {'role': 'other'},  # 현대/대한민국 - 상공은행 이사, 대한무진금융주식회사 사장, 상공부차관, 제2대 국회의원 등을 역임한 금융인
    '김수항': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 예조판서, 좌의정, 영의정 등을 역임한 문신.
    '김수현': {'role': 'other'},  # 현대/대한민국 - 해방 이후 선소리산타령의 전승자로 지정된 예능보유자.
    '김수홍': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 승지, 호조참판, 지돈녕부사 등을 역임한 문신.
    '김수환': {'role': 'other'},  # 현대/대한민국 - 해방 이후 한국천주교 주교회의 의장, 아시아 주교회의 공동의장 등에 서임된 사제. 추기경.
    '김수훈': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라에서 당에 파견한 숙위학생으로 빈공과에 합격한 문장가.
    '김수흥': {'role': 'scholar'},  # 조선 - 조선후기 도승지, 호조판서, 영의정 등을 역임한 문신. 학자.
    '김숙년': {'role': 'other'},  # 현대/대한민국 - 해방 이후, 서울 반가 음식을 계승해온 전통 요리 연구가.
    '김숙룡': {'role': 'other'},  # 고려 - 고려 후기에, 추밀원좌승선 공부상서 지이부사, 지추밀원사 병부상서 상장군 등을 역임한 문신
    '김숙명': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 대아찬 관등의 귀족.
    '김숙자': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「살풀이춤(경기도 도당굿 도살풀이)」의 전승자로 지정된 예능보유자. 전통무용가.
    '김숙정': {'role': 'scholar'},  # 고대/남북국/통일신라 - 남북국시대 때, 숙위학생으로 당나라에서 유학하여 빈공과에 급제한 통일신라의 학자.
    '김숙흘종': {'role': 'other'},  # 고대/삼국/신라 - 신라의 제24대 진흥왕의 동생이자 삼국통일을 이끈 김유신의 외할아버지인 왕족.
    '김숙흥': {'role': 'other'},  # 고려 - 고려 전기에, 거란의 침입으로부터 대항하다 전사한 무신 · 공신.
    '김순': {'role': 'other'},  # 조선 - 조선 후기에, 이천군수, 동지중추부사, 돈지돈녕부사 등을 역임한 문신.
    '김순고': {'role': 'other'},  # 조선/조선 전기 - 조선전기 포도대장, 지훈련원사, 비변사제조 등을 역임한 무신.
    '김순구': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 충청북도 옥천군 군서면의 독립만세시위를 주도한 혐의로 체포되어 옥중에서 순
    '김순남': {'role': 'other'},  # 근대 - 일제강점기로부터 대한민국 건국 초기에 활동한 월북 작곡가. 피아니스트. 지휘자. 음악이론가
    '김순명': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 의금부동지사, 황해도관찰사 등을 역임한 문신.
    '김순몽': {'role': 'other'},  # 조선/조선 전기 - 조선전기 내의원제조, 대비이어소 시약의원, 행부호군 등을 역임한 의관.
    '김순부': {'role': 'other'},  # 고려 - 고려 전기 묘청의 난 때, 평주판관 등을 역임하였으며, 반란군을 진압한 문신.
    '김순서': {'role': 'other'},  # 근대/일제강점기 - 일제강점기, 경기도 안성군 원곡면 · 양성면에서 일어난 독립만세운동을 주도한 독립운동가.
    '김순손': {'role': 'other'},  # 조선/조선 전기 - 조선전기 승선색, 상전 등을 역임한 환관.
    '김순식': {'role': 'scholar'},  # 근대/일제강점기|현대 - 일제강점기 때, 『은행부기강의안』, 『상업부기요의』 등을 저술하였으며, 해방 후에 고려대학
    '김순애': {'role': 'other'},  # 현대/대한민국 - 해방 이후 김순애가곡집, 김순애동요곡집 등을 발표한 작곡가.
    '김순원': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 대아찬으로 시중을 역임한 귀족.
    '김순이': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 경상남도 통영의 독립만세시위를 준비하다 체포된 독립운동가.
    '김순정': {'role': 'other'},  # 고대/남북국/통일신라 - 통일신라의 제35대 경덕왕의 장인으로, 이찬 관등에 임명된 귀족.
    '김순태': {'role': 'other'},  # 현대 - 해방 이후 「선소리산타령」의 전승자로 지정된 예능보유자.
    '김순하': {'role': 'other'},  # 근대/일제강점기|현대 - 해방 이후 대한건축사협회 이사장, 대한건축사협회 창립회장 등을 역임한 건축가.
    '김순흠': {'role': 'other'},  # 근대/개항기 - 개항기 때, 이강년 의진에서 활동하다가 국권 피탈 이후 단식을 감행하여 자결한 의병 · 열
    '김술종': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 대등, 삭주도독 등을 역임한 귀족.
    '김숭겸': {'role': 'poet'},  # 조선 - 조선후기 『관복암유고』을 저술한 시인.
    '김숭빈': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 때, 신라의 소성왕, 헌덕왕, 흥덕왕의 형제로, 시중, 상대등 등을 역임한 통일
    '김숭정': {'role': 'other'},  # 고려 - 고려 전기에, 안변도호부판관 등을 역임하였으며, 동여진 고지문의 습격에 원병이 도착한 것처
    '김숭조': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 사예, 사간, 나주목사 등을 역임한 문신.
    '김승': {'role': 'other'},  # 고려 - 고려 후기에, 승지를 역임한 문신.
    '김승경': {'role': 'other'},  # 조선 - 조선전기 예조참판, 대사헌 등을 역임한 문신.
    '김승곤': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 한국광복군 제1지대 본부 부관주임 겸 본부 구대장으로 활동한 독립운동가.
    '김승구': {'role': 'other'},  # 고려 - 고려 후기에, 전의령, 강릉도존무사, 경상도안렴사 등을 역임한 문신.
    '김승규': {'role': 'other'},  # 근대 - 조선 후기에, 군부협판, 육군연성학교장, 규장각제학 등을 역임한 문신.
    '김승득': {'role': 'other'},  # 고려 - 고려후기 집의, 좌부대언 등을 역임한 문신. 간신.
    '김승록': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 간도 용정촌에서 전개된 독립만세시위를 주도하는 과정에서 순국한 독립운동가.
    '김승만': {'role': 'other'},  # 근대 - 일제강점기 때, 독립단 의주지국평북총감, 광복군 참리부 협찬, 대한통의부 서무부장 등을 역
    '김승무': {'role': 'other'},  # 고려 - 고려 후기에, 사한, 시어사 등을 역임한 문신.
    '김승민': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 만주에서 광복단 조직에 참여하여 항일무장투쟁을 전개한 독립운동가.
    '김승빈': {'role': 'other'},  # 근대 - 일제강점기 때, 신흥무관학교 교관, 대한의용군 소대장, 고려혁명군정의회 장교 등을 역임한 
    '김승옥': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 전라북도 고창의 독립만세시위를 주도한 혐의로 체포되었으며, 출옥 이후 고창
    '김승용': {'role': 'other'},  # 고려 - 고려 후기에, 내부령, 밀직사 등을 역임한 문신.
    '김승원': {'role': 'other foreigner'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 대아찬으로 일본에 사신으로 파견된 관리.
    '김승위': {'role': 'other'},  # 고려 - 고려전기 대장군, 병부상서 등을 역임한 무신.
    '김승조': {'role': 'other'},  # 고려 - 고려 전기에, 내서랑으로 목종의 교육을 담당하여 사공에 추증된 관리 · 공신.
    '김승주': {'role': 'other'},  # 조선/조선 전기 - 조선전기 병조판서, 판중군도총제, 평양부원군 등을 역임한 무신.
    '김승준': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에 중낭장 · 차장군 등을 역임한 무신 · 공신.
    '김승택': {'role': 'other'},  # 고려 - 고려 후기에, 서연관, 찬성사, 중서평장사 등을 역임한 문신.
    '김승학': {'role': 'other'},  # 근대 - 일제강점기 때, 한국독립당과 군민의회를 조직하였으며, 임시의정원 평안도대표의원, 임시정부 
    '김승한': {'role': 'other'},  # 고려 - 고려 후기에, 밀직부사 등을 역임한 문신.
    '김승호': {'role': 'other'},  # 근대 - 해방 이후 「소」, 「무지개」, 「갈매기」 등에 출연한 배우. 영화배우.
    '김승환': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 북선상업은행 은행장을 역임한 실업가.
    '김시': {'role': 'scholar'},  # 조선 - 조선시대 「동자견려도」, 「한림제설도」, 「황우도」 등의 작품을 그린 화가.
    '김시걸': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 승지, 전라도관찰사, 대사간 등을 역임한 문신.
    '김시구': {'role': 'other'},  # 조선 - 조선 후기에, 장령, 전사관, 승지 등을 역임한 문신.
    '김시국': {'role': 'other'},  # 조선 - 조선 후기에, 제학, 대사성, 판의금부사 등을 역임한 문신.
    '김시권': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 강원도지사, 조선임전보국단 이사장 등을 역임한 관료.
    '김시묵': {'role': 'other'},  # 조선 - 조선 후기에, 판의금부사, 선혜청당상, 좌참찬 등을 역임한 문신.
    '김시민': {'role': 'scholar'},  # 조선 - 조선후기 의빈부도사, 진산군수, 낭천현감 등을 역임한 문신. 학자.
    '김시백': {'role': 'other'},  # 근대/대한제국기 - 대한제국기 때, 김상태 의진에서 영월의병장, 소모장 등으로 활동한 의병장.
    '김시번': {'role': 'other'},  # 조선 - 조선 후기에, 암행어사, 집의, 예조참의 등을 역임한 문신.
    '김시빈': {'role': 'other'},  # 조선 - 조선 후기에, 필선, 장령, 울산부사 등을 역임한 문신.
    '김시성': {'role': 'other'},  # 조선 - 조선후기 어영중군, 경상병사, 통제사 등을 역임한 무신.
    '김시습': {'role': 'scholar novelist'},  # 조선전기 『매월당집』 · 『금오신화』 · 『만복사저포기』 등을 저술한 학자. 문인.
    '김시약': {'role': 'other'},  # 조선 - 조선 후기에, 통영군관, 훈련원첨정 등을 역임한 무신 · 공신.
    '김시양': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 예조정랑, 도원수, 판중추부사 등을 역임한 문신.
    '김시연': {'role': 'other'},  # 근대 - 조선 후기에, 성균관대사성, 강원도관찰사, 전라도관찰사 등을 역임한 문신.
    '김시온': {'role': 'novelist'},  # 조선/조선 후기 - 조선 후기 경상북도 안동에서 학문과 후학 양성에 전념한 문인.
    '김시위': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 부교리, 승지, 영광군수 등을 역임한 문신.
    '김시유': {'role': 'other'},  # 조선 - 조선후기 청어(淸語)에 능통하고 외교적 활동이 뛰어났던 역관.
    '김시주': {'role': 'other'},  # 조선 - 조선 후기에, 승정원주서, 병부랑 등을 역임한 문신.
    '김시중': {'role': 'other'},  # 근대/대한제국기 - 대한제국기 때, 이경년 의진의 좌선봉장, 김상태 의진 중군장 등으로 활약한 의병장.
    '김시진': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 한성부좌윤, 수원부사, 호조참판 등을 역임한 문신.
    '김시찬': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 수찬, 대사간, 부제학 등을 역임한 문신.
    '김시창': {'role': 'other'},  # 조선 - 조선전기 효행으로 정려를 하사 받고, 현량과에 피천된 효자.
    '김시풍': {'role': 'other'},  # 근대 - 개항기 전주감영영장을 역임한 무신.
    '김시헌': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 동지춘추관사, 예조참판, 도승지 등을 역임한 문신.
    '김시혁': {'role': 'other'},  # 조선 - 조선 후기에, 호조참판, 대사헌, 판돈녕부사 등을 역임한 문신.
    '김시현': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 의열단에서 항일투쟁을 전개하였고 해방 이후, 국회의원을 역임하였으며, 이승
    '김시형': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 판의금부사, 판돈녕부사, 병조판서 등을 역임한 문신.
    '김시황': {'role': 'other'},  # 근대 - 일제강점기 때, 보합단을 조직하여 항일무장투쟁을 전개한 독립운동가.
    '김시회': {'role': 'other'},  # 조선 - 조선 전기에, 예문관대교, 부평부사 등을 역임한 문신.
    '김식': {'role': 'scholar'},  # 조선/조선 전기 - 조선시대 「고목우도」 · 「영모도」 등의 작품을 그린 화가.
    '김식재': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 최씨무인정권을 무너뜨리고 권력을 잡은 김준의 샛째 아들로, 전전승지동정 등을
    '김신': {'role': 'other'},  # 고려 - 고려전기 묘청의 난 과 관련된 관리. 역신.
    '김신겸': {'role': 'scholar'},  # 조선 - 조선 후기에, 「백육애음」, 『증소집』 등을 저술한 학자.
    '김신국': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 공조판서, 형조판서, 영중추부사 등을 역임한 문신.
    '김신련': {'role': 'other'},  # 고려/고려 전기 - 고려 전기 묘청의 난을 진압하는 데 참여한 문신.
    '김신망': {'role': 'scholar'},  # 조선/조선 후기 - 조선 후기 『가례기의』를 저술한 학자.
    '김신복': {'role': 'other foreigner'},  # 고대/남북국/통일신라 - 남북국시대 통일신라에서 일본에 사신으로 파견된 관리.
    '김신술': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 각간 관등의 귀족.
    '김신영': {'role': 'other'},  # 고려 - 고려후기 전주 죽동의 반란과 관련된 무신.
    '김신윤': {'role': 'other'},  # 고려 - 고려 후기에, 우간의대부, 좌간의대부, 판대부사 등을 역임한 문신.
    '김신재': {'role': 'other'},  # 현대 - 해방 이후 「낙조」 · 「뻐꾸기도 밤에 우는가」 등에 출연한 배우.
    '김실': {'role': 'other'},  # 고려 - 고려후기 수성원수, 문하찬성사 상의 등을 역임한 환관.
    '김심': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 부총관, 대사헌, 지중추부사 등을 역임한 문신.
    '김심백': {'role': 'other'},  # 고려 - 고려후기 7품, 5품 별장을 역임한 관리.
    '김심언': {'role': 'other'},  # 고려 - 고려 전기에, 예부상서, 내사시랑평장사, 서경유수 등을 역임한 문신.
    '김아파나시아르센지예비치': {'role': 'other'},  # 근대 - 일제강점기 공산당 연해주위원회 고려부장, 포시에트 구역당 제1비서 등을 역임한 사회주의운동
    '김악': {'role': 'other foreigner'},  # 고대/남북국/통일신라|고려/고려 전기 - 남북국시대 때, 신라의 사신으로서 중국을 내왕하던 중 후백제 측에 붙잡혀 관직을 가졌으며,
    '김안': {'role': 'other'},  # 고려/고려 전기 - 고려 전기 묘청, 정지상 일파로 활약한 문신.
    '김안국': {'role': 'scholar'},  # 조선/조선 전기 - 조선전기 수교리, 예조판서, 판중추부사 등을 역임한 문신. 학자.
    '김안로': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 이조판서, 도총관, 대제학, 좌의정 등을 역임한 문신.
    '김안정': {'role': 'other'},  # 조선 - 조선 전기에, 도승지, 개성유수 등을 역임한 문신.
    '김알렉산드라': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 하바로프스크시당 비서, 극동인민위원회 외무부장 등을 역임한 사회주의운동가.
    '김알지': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라 경주김씨의 시조.
    '김암': {'role': 'other'},  # 고대/남북국 - 남북국시대 통일신라의 양주, 강주, 한주태수, 집사시랑 등을 역임한 문신. 방술가(方術家)
    '김압실': {'role': 'other foreigner'},  # 고대/남북국/통일신라 - 남북국시대 통일신라에서 일본에 파견된 사신.
    '김애': {'role': 'other'},  # 고려 - 고려 후기에, 합문지후, 우부승선, 동지공거 등을 역임한 문신.
    '김애마': {'role': 'other'},  # 현대/대한민국 - 해방 이후 이화여자대학교 초대학장, 문교부 대학교육위원 등을 역임한 교육자.
    '김약': {'role': 'scholar'},  # 조선 - 조선 중기에, 임진왜란이 발발하자 스승 조헌과 함께 의병을 일으킨 학자.
    '김약련': {'role': 'other'},  # 조선 - 조선 후기에, 전적, 병조좌랑, 좌부승지 등을 역임한 문신.
    '김약로': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 좌의정, 약방도제조, 판중추부사 등을 역임한 문신.
    '김약묵': {'role': 'other'},  # 조선 - 조선 전기에, 내자시정, 양주목사 등을 역임한 문신.
    '김약선': {'role': 'other'},  # 고려 - 고려 후기에, 추밀부사 등을 역임한 문신.
    '김약수': {'role': 'other'},  # 현대/대한민국 - 일제강점기 조선노동공제회, 조선노동총동맹 창설에 참여한 노동운동가. 정치인.
    '김약슬': {'role': 'scholar'},  # 근대 - 해방 이후 『신라, 백제, 고구려나려예문지』를 편찬한 학자. 장서가.
    '김약시': {'role': 'other'},  # 고려 - 고려 후기에, 진현관직제학, 이조판서 등을 역임한 문신.
    '김약연': {'role': 'other'},  # 근대 - 일제강점기 때, 만주에 서전의숙, 명동서숙, 명동여학교 등을 설립하였으며, 간민회 회장 등
    '김약온': {'role': 'other'},  # 고려 - 고려 전기에, 검교사도 수사공 상주국, 문하시중 등을 역임한 문신.
    '김약진': {'role': 'other'},  # 고려/고려 후기 - 고려 후기 최충헌 등이 이의민을 제거할 때 공로를 세워 최충헌 정권에서 출세한 무신.
    '김약채': {'role': 'other'},  # 조선 - 조선 전기에, 대사헌, 충청도관찰사 등을 역임한 문신.
    '김약필': {'role': 'other foreigner'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 사찬으로서 일본에 파견된 사신.
    '김약항': {'role': 'other'},  # 고려 - 조선 전기에, 사헌집의, 판전교시사 등을 역임한 문신.
    '김양': {'role': 'other'},  # 고려 - 고려 전기에, 좌승선, 추밀원부사, 예부상서 등을 역임한 문신.
    '김양감': {'role': 'other'},  # 고려 - 고려 전기에, 판상서호부사, 수태위, 문하시랑 등을 역임한 문신.
    '김양검': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 대호군 등을 역임하였으며, 신돈 일파로 몰려 처형된 무신 · 공신.
    '김양경': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 개성부유수, 대사헌, 공조판서 등을 역임한 문신.
    '김양근': {'role': 'other'},  # 조선 - 조선 후기에, 현풍현감, 음죽현감, 형조참의 등을 역임한 문신.
    '김양기': {'role': 'scholar'},  # 조선/조선 후기 - 조선후기 「송하모정도」 · 「추경산수도」 · 「화조도」 등의 작품을 그린 화가.
    '김양도': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 나당연합군의 사비성 함락 당시의 장수. 문장가.
    '김양림': {'role': 'other foreigner'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 사찬 박강국 · 김충선 등과 일본에 사신으로 파견된 왕자.
    '김양선': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 평동중학교 교장, 기독교박물관관장 등을 역임한 목사. 고고학자.
    '김양수': {'role': 'other foreigner'},  # 근대 - 일제강점기 때, 미국에서 삼일신보 주필로 활동하였으며, 조선어학회에 참여하여 사전편찬을 재
    '김양순': {'role': 'other'},  # 조선 - 조선 후기에, 대사헌, 이조판서 등을 역임한 문신.
    '김양신': {'role': 'other'},  # 조선/조선 후기 - 조선후기 도화서 교수를 역임한 화가.
    '김양언': {'role': 'other'},  # 조선 - 조선 후기에, 이괄의 난을 진압하여 녹훈되었으나, 정묘호란 때 전사한 무신 · 공신.
    '김양연': {'role': 'other'},  # 조선 - 조선 후기에, 사헌부장령, 홍문관교리, 남포현감 등을 역임한 문신.
    '김양영': {'role': 'other'},  # 고려 - 고려 후기에, 사문박사 등을 역임한 문신.
    '김양원': {'role': 'other foreigner'},  # 고대/남북국/통일신라 - 남북국시대 통일신라에서 한나마로서 일본에 파견된 사신.
    '김양종': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 파진찬으로 집사부시중을 역임한 관리.
    '김양지': {'role': 'other'},  # 고려 - 고려 전기에, 급사중, 어사대부, 상서우복야 등을 역임한 문신.
    '김양진': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 형조참의, 대사간, 예조참의 등을 역임한 문신.
    '김양택': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 정조의 원손사부(元孫師傅)이며 대제학, 영의정을 역임한 문신.
    '김양품': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 각간 관등의 귀족.
    '김양행': {'role': 'scholar'},  # 조선 - 조선후기 직제학, 이조참의, 형조참판 등을 역임한 문신. 학자.
    '김양홍': {'role': 'other'},  # 근대 - 일제강점기 우리나라 최초의 교구장을 역임한 신부.
    '김어진': {'role': 'other'},  # 고려 - 고려후기 안주군민부만호를 역임한 무신.
    '김억': {'role': 'poet critic'},  # 근대/일제강점기 - 일제강점기 때, 『해파리의 노래』, 『금모래』, 『봄의 노래』 등을 저술한 시인 · 문학평
    '김억렴': {'role': 'other'},  # 고대/남북국/통일신라 - 통일신라의 제56대 경순왕의 큰아버지로, 지대야군사 등을 역임하였으며, 딸을 고려의 태조 
    '김억추': {'role': 'other'},  # 조선 - 조선시대 전라수군절도사, 제주목사 등을 역임한 무신.
    '김언': {'role': 'other'},  # 조선 - 조선 후기에, 장악원정, 영천군수, 성천부사 등을 역임한 문신.
    '김언건': {'role': 'scholar'},  # 조선 - 조선 전기에, 『운정유집』 등을 저술한 문신.
    '김언경': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 보림사보조선사창성탑비를 쓴 관리. 서예가.
    '김언공': {'role': 'other'},  # 조선 - 조선시대 순천부사, 고령진첨절제사, 혜산진첨절제사 등을 역임한 무신.
    '김언기': {'role': 'scholar'},  # 조선 - 조선 전기에, 『유일재집』 등을 저술하였으며, 안동지역의 학문 진흥을 이끈 학자.
    '김언수': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 정묘호란 때 안주성전투에서 순절한 무관.
    '김언평': {'role': 'other'},  # 조선 - 조선 전기에, 감찰, 장령, 강릉대도호부사 등을 역임한 문신.
    '김여': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 대아찬으로 시중을 역임한 관리.
    '김여건': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 정언, 수찬 등을 역임한 문신.
    '김여기': {'role': 'other'},  # 조선 - 조선후기 청성진첨절제사, 벽동군수, 선사포첨절제사 등을 역임한 무신.
    '김여란': {'role': 'other'},  # 현대/대한민국 - 해방 이후 판소리 「춘향가」의 전승자로 지정된 예능보유자.
    '김여량': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 김제군수, 창원부사, 승지 등을 역임한 문신.
    '김여로': {'role': 'other'},  # 조선 - 조선후기 별군직, 자산군수, 덕천군수 등을 역임한 무신.
    '김여물': {'role': 'other'},  # 조선 - 조선 전기에, 충주도사, 담양부사, 의주목사 등을 역임한 문신.
    '김여부': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 전한 등을 역임한 문신.
    '김여생': {'role': 'other'},  # 조선/조선 전기 - 조선  전기 임진왜란 당시 전라도의 의병장.
    '김여석': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 호조참판, 병조참판, 형조판서 등을 역임한 문신.
    '김여옥': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 판결사, 강화유수, 장례원판결사 등을 역임한 문신.
    '김여제': {'role': 'poet'},  # 근대/일제강점기 - 일제강점기 「한끗」, 「잘짜」, 「해에게서 소년에게」 등을 저술한 시인. 교육자.
    '김여준': {'role': 'other'},  # 조선 - 조선후기 김직재의 옥사사건과 관련된 무신.
    '김여지': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 대사헌, 판한성부사, 형조판서 등을 역임한 문신.
    '김역기': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라에서 당나라에 파견된 사신.
    '김연': {'role': 'other'},  # 조선/조선 전기 - 조선 전기 임진왜란 때 영천 출신의 의병장.
    '김연경': {'role': 'other'},  # 고려 - 고려전기 김치양의 난과 관련된 무신.
    '김연광': {'role': 'other'},  # 조선 - 조선 전기에, 부여현감, 평창군수, 회양부사 등을 역임한 문신.
    '김연국': {'role': 'other'},  # 근대/개항기 | 근대/대한제국기 | 근대/일제강점기 - 동학, 천도교, 시천교 지도자로 활약하다가 상제교를 창건한 종교인.
    '김연방': {'role': 'other'},  # 근대/일제강점기 - 일제강점기, 경기도 수원군 우정면에서 일어난 독립만세운동에 참여한 독립운동가.
    '김연수': {'role': 'other'},  # 근대 - 일제강점기부터 1970년대까지, 활동한 판소리 창자이며. 창극 배우 · 각색가 · 작창가.
    '김연실': {'role': 'other'},  # 현대 - 해방 이후 북한에서 「정찰병」, 「처녀 리발사」, 「아름다운 거리」 등에 출연한 배우. 영
    '김연조': {'role': 'other'},  # 조선 - 조선 후기에, 권지승문원부정자 등을 역임한 문신.
    '김연준': {'role': 'other'},  # 현대/대한민국 - 해방 이후 한양대학교 총장과 이사장을 역임한 교육자. 작곡가.
    '김연지': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 대사헌, 한성부윤, 지중추원사 등을 역임한 문신.
    '김열보': {'role': 'other'},  # 고려 - 고려 후기에, 장작승, 시각문지후, 전주목판관 등을 역임한 문신.
    '김영': {'role': 'scholar'},  # 조선 - 조선후기 「우후산수도」, 「산수십곡병풍」 등의 작품을 그린 화가.
    '김영건': {'role': 'critic scholar'},  # 현대/대한민국 - 해방 이후 「농촌계몽운동에서의 일제안」, 『어록』, 『문화와 평론』 등을 저술한 평론가. 
    '김영견': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 좌부승지, 이조참판, 동지중추부사 등을 역임한 문신.
    '김영고': {'role': 'other'},  # 고려 - 고려 후기에, 흥교도관역사, 합문지후 등을 역임한 문신.
    '김영곤': {'role': 'other'},  # 근대 - 해방 이후 「북청사자놀음」의 전승자로 지정된 예능보유자.
    '김영공': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 각간으로 시중을 역임한 귀족. 대신.
    '김영관': {'role': 'other'},  # 고려 - 고려 전기에, 감수국사 지서경유수사, 수사도 판국자감사 등을 역임한 문신.
    '김영근': {'role': 'poet scholar'},  # 일제강점기 때, 위정척사 사상을 바탕으로 민족운동을 모색하였으며, 저항시인으로 평가되는 학
    '김영기': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 경상남도 합천군 독립만세시위로 체포된 구금자의 석방을 위해 결사대를 조직하
    '김영덕': {'role': 'other'},  # 조선/조선 후기 - 조선후기 충청남도관찰사, 경상남도관찰사, 강원도관 등을 역임한 관료. 의사(義士).
    '김영돈': {'role': 'other'},  # 고려 - 고려 후기에, 강릉부녹사, 지공거, 정치도감판사 등을 역임한 문신.
    '김영동': {'role': 'other'},  # 현대/대한민국 - 일제강점기 때, 북간도, 연길, 용정, 연해주 일대에서 독립운동을 전개하였으며 해방 이후,
    '김영란': {'role': 'other'},  # 근대 - 일제강점기 때, 비밀결사 숭의단과 공성단 등을 조직하여 군자금 모금 및 친일파 처단 활동을
    '김영랑': {'role': 'poet'},  # 근대/일제강점기 - 일제강점기 「동백잎에 빛나는 마음」 · 「언덕에 바로 누워」 · 「독을 차고」 등을 저술한
    '김영렬': {'role': 'other'},  # 근대 - 일제강점기 때, 독립단에서 주재소와 면사무소를 습격하는 등 항일무장투쟁을 전개한 독립운동가
    '김영로': {'role': 'other'},  # 조선 - 조선 전기에, 거산찰방, 수성찰방, 고산찰방 등을 역임한 문신.
    '김영리': {'role': 'other'},  # 고려 - 고려 후기에, 존무사, 좌사의대부 등을 역임한 문신.
    '김영만': {'role': 'other'},  # 근대 - 일제강점기 사회주의자동맹 집행위원, 조선공산당재건설준비위원회 선전부 간부 등을 역임한 사회
    '김영면': {'role': 'scholar'},  # 조선/조선 후기 - 조선후기 「행려도」, 「강촌추사도」 등의 작품을 그린 화가.
    '김영목': {'role': 'other'},  # 근대 - 조선 후기에, 장례원경, 홍문관학사, 궁내부특진관 등을 역임한 문신.
    '김영배': {'role': 'other'},  # 근대 - 일제강점기, 황해도 참여관 겸 산업 부장, 전라남도 참여관 겸 산업 부장 등을 역임한 관료
    '김영백': {'role': 'other'},  # 근대/개항기 - 대한제국기 전라남도 장성군 출신의 평민 의병장.
    '김영보': {'role': 'playwright novelist'},  # 근대/일제강점기 - 일제강점기 「나의 세계로」 · 「연의 물결」 · 「구리십자가」 등의 작품을 낸 극작가. 언
    '김영부': {'role': 'other'},  # 고려 - 고려 전기에, 참지정사 판상서병부사, 중서시랑, 중서평장사 등을 역임한 문신.
    '김영삼': {'role': 'other'},  # 현대/대한민국 - 대한민국의 제14대 대통령을 지낸 정치인.
    '김영상': {'role': 'scholar foreigner'},  # 근대/일제강점기 - 조선 후기 일본 왕의 노인 은사금을 거절하여 수감 중 단식하여 순국한 유학자이자 독립운동가
    '김영서': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 대구3·1운동을 주도하여 옥고를 치른 독립유공자.
    '김영석': {'role': 'novelist critic'},  # 근대 - 해방 이후 「지하로 뚫린 길」, 「격랑」 등을 저술한 작가. 소설가, 평론가.
    '김영선': {'role': 'other foreigner'},  # 근대/일제강점기 - 대한제국기 1907년 신민회(新民會) 조직에 참여하고, 일제강점기 1919년 4월 중국 상
    '김영섭': {'role': 'other'},  # 근대 - 해방 이후 하와이 총영사, 서울 중앙교회 목사 등을 역임한 목사.
    '김영성': {'role': 'other'},  # 근대/대한제국기 - 대한제국기 때, 의병을 모집하며 항일의병활동을 전개하였고, 전남 여수의 돌산전투에 참전한 
    '김영소': {'role': 'other'},  # 고려/고려 전기 - 고려시대 수좌, 승통, 대선의 도청 등을 역임한 승려.
    '김영수': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「판소리 고법」 전승자로 지정된 예능보유자. 고수.
    '김영숙': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 대종교 총본사 서무부장, 대형 등을 역임하며 대종교를 통한 항일투쟁을 전개
    '김영순': {'role': 'other'},  # 조선 - 조선 후기에, 대사헌, 형조판서, 이조판서 등을 역임한 문신.
    '김영식': {'role': 'other'},  # 근대 - 일제강점기 신간회 목포지회 대의원, 조선공산당 재건설준비위원회 정치부위원 등을 역임한 사회
    '김영약': {'role': 'other'},  # 고려 - 고려 전기에, 우사간 등을 역임한 문신.
    '김영옥': {'role': 'other foreigner'},  # 현대/대한민국 - 한국계 미국인 2세로, 미국 육군 대령 출신의 군인.
    '김영완': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 전라북도 고창의 독립만세시위를 주도한 혐의로 체포되어 옥중에서 순국한 독립
    '김영원': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 전라북도 임실의 독립만세시위를 주도한 혐의로 체포되어 옥중에서 순국한 독립
    '김영유': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 행첨지중추부사, 수지중추부사, 동지중추부사 등을 역임한 문신.
    '김영윤': {'role': 'scholar'},  # 근대 - 해방 이후 『가야금교본』을 저술한 가야금명인.
    '김영의': {'role': 'other'},  # 현대/대한민국 - 해방 이후 이화여자대학교 이사장, 문교부 교육과정음악분과위원장 등을 역임한 교육자. 피아노
    '김영일': {'role': 'childrenauthor novelist'},  # 현대 - 해방 이후 한국문인협회 아동문학분과위원장, 한국아동문학회 회장 등을 역임한 아동문학가.
    '김영작': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 사헌부대사헌, 홍문관제학, 개성부유수 등을 역임한 문신.
    '김영재': {'role': 'other'},  # 근대 - 일제강점기 때, 윤봉길의 의거에 사용할 폭탄을 제작하였으며, 임시정부 주석 경호원, 비서 
    '김영적': {'role': 'other'},  # 근대 - 조선 후기에, 비서원승, 봉상사제조, 궁내부특진관 등을 역임한 문신.
    '김영전': {'role': 'other'},  # 근대 - 조선 후기에, 봉상사제조, 종묘서제조, 종묘전사 등을 역임한 문신.
    '김영정': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 지돈녕부사, 전라도관찰사 등을 역임한 문신.
    '김영제': {'role': 'other'},  # 근대 - 일제강점기 제3대 아악사장 등을 역임한 국악인. 가야금명인.
    '김영조': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 대사간, 부제학, 이조참판 등을 역임한 문신.
    '김영존': {'role': 'other'},  # 고려 - 고려후기 동지추밀원사, 지추밀원사, 평장사 등을 역임한 무신.
    '김영종의 난': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라에서 귀족 김영종이 일으킨 반란.
    '김영주': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 「검은 태양」 · 「신화시대」 등의 작품을 그린 화가.
    '김영준': {'role': 'other'},  # 현대/대한민국 - 해방 이후 농림부장관, 한국전력사장 등을 역임한 관료. 경제인.
    '김영진': {'role': 'other'},  # 근대 - 조선후기 내장원감독, 군부교육국장, 봉상사제조 등을 역임한 관리.
    '김영찬': {'role': 'other'},  # 현대/대한민국 - 해방 이후 한국은행 수석부총재, 산업은행 총재 등을 역임한 금융인. 관료.
    '김영철': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「줄타기」 전승자로 지정된 예능보유자. 줄타기명인.
    '김영태': {'role': 'poet critic'},  # 현대 - 해방 이후 『유태인이 사는 마을의 겨울』 · 『하늘 바람꽃이 핀다』 등을 저술한 시인. 무
    '김영팔': {'role': 'scholar'},  # 근대/일제강점기 - 일제강점기 「미쳐가는 처녀」, 「싸움」, 「그 후의 대학생」 등의 작품을 제작한 연극인.
    '김영하': {'role': 'other'},  # 근대 - 일제강점기 때, 전라남도 나주, 함평 등에서 군자금 모금 활동을 전개한 독립운동가.
    '김영학': {'role': 'other'},  # 근대 - 일제강점기 때, 철원애국단을 조직하여 군자금 모금 활동을 전개한 목사 · 독립운동가.
    '김영한': {'role': 'scholar'},  # 근대 - 대한제국기 때, 용인군수, 양근군수, 비서원승 등을 역임한 문신 · 학자.
    '김영행': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 우사어, 임천군수, 첨지중추부사 등을 역임한 문신.
    '김영현': {'role': 'other foreigner'},  # 근대 - 일제강점기 때, 중국에서 독립군에 가담하여 군자금 모금 활동을 전개한 독립운동가.
    '김영환': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 경상남도 창원의 삼진 만세운동에 참여했다가 순국한 독립운동가.
    '김영후': {'role': 'other'},  # 고려 - 고려 후기에, 좌정승, 우정승, 상락후 등을 역임한 문신.
    '김영훈': {'role': 'scholar'},  # 근대/일제강점기 | 현대 - 대한한의사협회 명예회장, 서울한의과대학 명예학장 등을 역임한 한의학자.
    '김영희': {'role': 'other'},  # 근대 - 일제강점기 때,경기도 안성군 원곡면과 양성면 일대의 독립만세시위에 참여한 독립운동가.
    '김예': {'role': 'other'},  # 고대/남북국/통일신라 - 통일신라의 제46대 문성왕의 사촌동생으로, 창림사 무구정찹 건립에 참여하였으며, 김현 등과
    '김예몽': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 강원도관찰사, 대사성, 공조판서 등을 역임한 문신.
    '김예영': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 제38대 원성왕의 셋째 아들인 왕자.
    '김예직': {'role': 'other'},  # 조선 - 조선시대 함경도병마절도사, 포도대장, 삼도수군통제사 등을 역임한 무신.
    '김예진': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 때, 일신청년단을 조직하여 군자금 모금, 일본기관 파괴 활동 등을 전개한 독립운
    '김예징': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 때, 민애왕을 타도하고 신무왕으로 즉위시키는데 공을 세워 상대등을 역임한 통일신
    '김오성': {'role': 'critic'},  # 근대 - 일제강점기 때, 문학, 철학 비평 분야에서 활약하였고, 해방 이후 조선인민당 선전부장, 민
    '김옥': {'role': 'other'},  # 조선 - 조선 후기에, 군수 등을 역임한 문신.
    '김옥균': {'role': 'other'},  # 근대/개항기 - 우리나라 개화운동의 대표적 인물이자 갑신정변의 주모자.
    '김옥길': {'role': 'other'},  # 현대/대한민국 - 해방 이후 이화여자대학교 총장, 문교부장관 등을 역임한 교육자. 여성운동가.
    '김옥심': {'role': 'other'},  # 현대/대한민국 - 해방 이후 활동한 대표적인 경기민요 명창.
    '김옥주': {'role': 'other'},  # 현대/대한민국 - 제헌국회의원을 역임하였으며, 국회프락치사건으로 복역하다가 한국전쟁 때 납북되어 북한에서, 
    '김온': {'role': 'other'},  # 고려 - 고려 후기에, 충숙왕과 대립하던 심양왕 왕고를 돕다가 세력을 잃고 유배된 관리.
    '김온주': {'role': 'other'},  # 고려 - 고려 후기에, 고애사, 좌간의대부 중군병마부사 등을 역임한 문신.
    '김옹': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 이찬으로 시중, 상상, 병부령 등을 지낸 관리.
    '김완': {'role': 'other'},  # 조선 - 조선 후기에, 소파아권관 겸 단련사, 선전관, 내금위장 등을 역임한 무신 · 공신.
    '김완규': {'role': 'other'},  # 근대/일제강점기 - 천도교를 대표한 민족 대표 33인의 한 사람으로 「3·1독립선언서」에 서명한 독립운동가.
    '김완손': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「양주별산대놀이」 해금의 전승자로 지정된 예능보유자.
    '김완수': {'role': 'other'},  # 근대 - 조선 후기에, 궁내부특진관, 봉상사제조, 예식원장례경 등을 역임한 문신.
    '김완자티무르': {'role': 'other foreigner'},  # 고려/고려 후기 - 고려 후기 중국 원나라의 예부상서를 역임한 고려인 출신의 환관.
    '김왕': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 양산도사, 충청도사, 함평현감 등을 역임한 문신.
    '김요립': {'role': 'other'},  # 조선 - 조선 전기에, 사성, 상의원정, 종부시정 등을 역임한 문신.
    '김요섭': {'role': 'poet childrenauthor'},  # 현대/대한민국 - 해방 이후 『체중』, 『달과 기계』, 『얼굴이 없는 얼굴』 등을 저술한 시인. 아동문학가.
    '김요의 난': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 때, 이찬 관등으로 한주에서 반란을 일으킨 통일신라의 왕족.
    '김용': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 소판으로 당나라에 파견된 관리.
    '김용겸': {'role': 'other'},  # 조선 - 조선 후기에, 우승지, 동지돈녕부사를 등을 역임한 문신.
    '김용경': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 승지, 개성부유수 등을 역임한 문신.
    '김용관': {'role': 'scholar'},  # 해방 이후 『치과 마취학』, 『구강 외과학』 등을 저술한 학자. 치의학자.
    '김용구': {'role': 'other'},  # 근대/대한제국기 - 대한제국기 때, 호남창의회맹소에서 도통령으로 활약한 의병장.
    '김용규': {'role': 'other'},  # 근대 - 조선 후기에, 궁내부특진관, 봉상사제조, 장례원부경 등을 역임한 문신.
    '김용근': {'role': 'other'},  # 근대 - 해방 이후 정읍에서 초산국악원을 개설한 거문고명인.
    '김용기': {'role': 'other'},  # 현대/대한민국 - 광복 이후, 기독교 농촌 지도자 교육에 힘쓴 개신교인.
    '김용대': {'role': 'other'},  # 근대 - 일제강점기 때, 대한독립단 비서, 대한광정단 국법과장, 정의부 중앙행정위원 등을 역임한 독
    '김용덕': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 「국사개설」, 「한국제도사연구」, 「신학국사의 탐국」 등을 저술한 학자. 역사학
    '김용래': {'role': 'other'},  # 현대/대한민국 - 해방 이후 서울시장, 총무처장관, 경기도지사 등을 역임한 관료.
    '김용만': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「해뜨는소리」 · 「대마루 댓바람」 · 「우헌도곡」 등을 만든 작곡가. 지휘자.
    '김용무': {'role': 'other'},  # 현대/대한민국 - 해방 이후 대법원장, 제2대 국회의원 등을 역임한 법조인. 정치인.
    '김용배': {'role': 'other'},  # 현대/대한민국 - 한국전쟁 당시 강원도 양구의 토평리지구전투에 참전한 군인.
    '김용성': {'role': 'other foreigner'},  # 근대 - 일제강점기 때, 미국에서 재미한족연합회 집행부위원, 임시정부 주미외교위원부 외교위원장 등을
    '김용수': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 「효귀」 · 「월야」 · 「선경」 등을 그린 화가. 수묵채색화가.
    '김용순': {'role': 'other'},  # 현대/대한민국 - 5·16군사정변에 가담하였으며, 경남지구 계엄사령관, 육군 군수기지사령부 사령관, 중앙정보
    '김용식': {'role': 'other'},  # 현대 - 한국전쟁 당시 경북 포항의 비학산전투에 참전한 군인.
    '김용언': {'role': 'scholar'},  # 조선 - 조선 후기에, 『송계유고』 등을 저술한 학자.
    '김용옥': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 『고린도전서』, 『신약개론』, 『데살로니가 전후서』 등을 저술한 신학자. 목사.
    '김용완': {'role': 'other'},  # 현대 - 해방 이후 경방주식회사 명예회장, 전국경제인연합회 회장 등을 역임한 기업인.
    '김용우': {'role': 'other'},  # 현대/대한민국 - 해방 이후 국방부장관, 민주공화당 정책위 의장, 대한올림픽위원회 위원장 등을 역임한 정치인
    '김용욱': {'role': 'other'},  # 근대/대한제국기 - 대한제국기 때, 신돌석 의진에서 중군장으로 활동하며 항일의병투쟁을 전개한 의병장.
    '김용원': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 대동단에서 활동하며 의친왕 망명 계획에 참여하였고, 임시정부 의정원 의원 
    '김용이': {'role': 'other'},  # 근대 - 일제강점기 때, 충청북도 옥천의 독립만세시위에 참여한 독립운동가.
    '김용익': {'role': 'other'},  # 현대 - 해방 이후 「봉산탈춤」의 전승자로 지정된 예능보유자.
    '김용재': {'role': 'other'},  # 고려/고려 후기 - 1258년(고종 45), 무오정변(戊午政變)에 참여하여 위사보좌공신(衛社輔佐功臣)에 이어 
    '김용제': {'role': 'poet critic'},  # 근대/일제강점기 - 일제강점기 「압록강」 · 「사랑하는 대륙이여」 등을 저술한 시인. 비평가 · 친일반민족행위
    '김용조': {'role': 'scholar'},  # 근대/일제강점기 - 일제강점기 「어머니의 상」, 「어선」, 「해경」 등의 작품을 그린 화가.
    '김용주': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 한국광복군에 입대하여 제2지대 총무조원 겸 공작조원으로 활동하였으며, 1945년
    '김용준': {'role': 'scholar'},  # 근대/일제강점기 | 현대 - 북한에서 평양미술대학 교수 등을 역임하였으며, 『조선미술대요』 등을 저술한 화가 · 미술인
    '김용중': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 때, 미국으로 이주하여 대한인국민회, 재미한족연합위원회 등에서 활동하였고, 영자
    '김용진': {'role': 'other'},  # 근대 - 일제강점기 때, 신민회 운영위원으로 활동하였으며, 황해도에서 임시정부 연통제를 조직하여 군
    '김용찬': {'role': 'scholar'},  # 조선 - 조선 후기에, 『경독재집』 등을 저술한 학자.
    '김용춘': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라 제25대 진지왕의 아들인 왕자.
    '김용태': {'role': 'other'},  # 현대/대한민국 - 5·16군사정변의 핵심 인물로, 국가재건최고회의 경제고문 등을 역임하였으며, 민주공화당의 
    '김용택': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 이이명의 천거로 벼슬길에 올랐으나, 이이명 추대 세력에 대한 목호룡의 고변으
    '김용하': {'role': 'other'},  # 현대 - 한국전쟁 당시 경북 문경의 이화령전투에 참전한 군인.
    '김용한': {'role': 'other'},  # 현대 - 해방 이후 물가정책국장, 과학기술처 차관 등을 역임한 관료.
    '김용행': {'role': 'scholar'},  # 고대/삼국/신라 - 삼국시대 신라의 대나마로「아도화상비」를 저술한 문장가.
    '김용현': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「강릉농악」 전승자로 지정된 예능보유자. 농악인.
    '김용호': {'role': 'poet'},  # 근대/일제강점기 - 일제강점기 『향연』 · 『해마다 피는 꽃』 등을 저술한 시인.
    '김용환': {'role': 'other'},  # 현대/대한민국 - 박정희 경제개발기에, 재무부와 농림부, 대통령비서실의 관료로서 경제개발에 투자 재원을 마련
    '김용휘': {'role': 'other'},  # 고려 - 고려후기 도안무사 겸 부원수, 서북면도순찰사 등을 역임한 무신.
    '김우': {'role': 'other'},  # 근대 - 대한제국기 때, 전남 장성에서 의병을 일으켜 200정의 총으로 무장한 부대를 이끈 의병장.
    '김우굉': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 대사간, 대사성, 승지 등을 역임한 문신.
    '김우규': {'role': 'scholar'},  # 조선/조선 후기 - 조선후기 『청구가요』 등에 주요 작품이 실려 있는 가객.
    '김우근': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 참의부 경무원, 조선혁명단 지방책임위원, 한중연합토일군 참모 등을 역임한 
    '김우명': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 영돈녕부사, 오위도총관, 호위대장 등을 역임한 문신.
    '김우문': {'role': 'other'},  # 고려/고려 후기 - 고려후기 수월관음도 제작을 주도한 화가.
    '김우번': {'role': 'other'},  # 고려 - 고려 전기에, 지제고, 동지공거, 판예빈성사 등을 역임한 문신.
    '김우범': {'role': 'novelist'},  # 근대/개항기 | 근대/일제강점기 - 일제강점기 「우후산수」 · 「난」 · 「매」 등을 그린 화가. 문인화가.
    '김우생': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 순천부사, 승지 등을 역임한 문신.
    '김우석': {'role': 'other'},  # 조선 - 조선 후기에, 개성유수, 한성부판윤, 형조판서 등을 역임한 문신.
    '김우식': {'role': 'other'},  # 현대/대한민국 - 한국민주당 경상북도 감찰위원장, 제헌국회의원 등을 역임하다가 한국전쟁 때 납북되어 북한에서
    '김우신': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 대호군, 호조참의, 첨지중추부사 등을 역임한 문신.
    '김우옹': {'role': 'scholar'},  # 조선 - 조선시대 병조참판, 예조참판, 이조참판 등을 역임한 문신. 학자.
    '김우윤': {'role': 'other'},  # 조선 - 조선 중기에, 문한관, 공조좌랑 등을 역임한 문신.
    '김우전': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 일본군 학병으로 동원되었으나, 중국에서 탈출한 후 한국광복군에 입대하여 활동한 
    '김우중': {'role': 'other'},  # 현대/대한민국 - 1967년, 섬유수출업체 대우실업 창업 이래 단기간에 국내 굴지의 재벌 대우그룹을 만들어 
    '김우진': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 1919년 3월 서울 3·1운동에 참가한 뒤 중국 상하이로 망명하여 대한민국임시
    '김우창': {'role': 'scholar'},  # 조선 - 개항기 때, 영주지방의 의병대장으로 활약하였으며, 『기사』, 『예설간요』 등을 저술한 학자
    '김우철': {'role': 'critic'},  # 근대/일제강점기 - 일제강점기 「아동문학에 관하야」, 「낭만적 인간탐조」 등을 저술한 평론가.
    '김우평': {'role': 'other'},  # 근대/일제강점기|현대 - 일제강점기 때, 동아일보 기자, 친일조직인 만주국 협화회 조선인민회 분회 상임감사 등을 역
    '김우항': {'role': 'other'},  # 조선 - 조선 후기에, 이조참판, 대사성, 이조판서, 우의정 등을 역임한 문신.
    '김우현': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 공조참의, 우부승지, 경흥도호부사 등을 역임한 문신.
    '김우형': {'role': 'other'},  # 조선 - 조선 후기에, 한성부판윤, 개성유수, 형조판서 등을 역임한 문신.
    '김우화': {'role': 'other'},  # 조선 - 조선 후기에, 황감별제, 전적, 봉상시정 등을 역임한 문신.
    '김운': {'role': 'other'},  # 고려 - 고려 후기에, 지첨의부사, 첨의참리, 도첨의참리 등을 역임한 문신.
    '김운경': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 선위부사를 역임한 관리.
    '김운공': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「영산재」 전승자로 지정된 예능보유자. 범패승.
    '김운서': {'role': 'other'},  # 근대/대한제국기 - 대한제국기 때, 이석용 의진에서 중군장으로 활약하였으며, 국권 피탈 이후 군자금 모금 활동
    '김운택': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 평안도감진어사, 부제학, 호조참판, 형조참판 등을 역임하였으나, 목호룡의 고
    '김운파': {'role': 'other'},  # 현대/대한민국 - 해방 이후 봉원사 주지를 역임한 승려.
    '김운학': {'role': 'critic scholar'},  # 현대/대한민국 - 해방 이후 『신라불교문학연구』, 『향가에 나타난 불교사상』 등을 저술한 승려. 불교학자, 
    '김울산': {'role': 'other'},  # 근대 - 일제강점기 순도학교, 복명학교, 희도국민학교 등을 설립한 여성 육영사업가.
    '김웅권': {'role': 'other'},  # 현대/대한민국 - 조선민족청년당 이사와 총무부장, 제헌국회의원, 국회 외무국방위원회 국방분과위원 등을 역임한
    '김웅렴': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 국상으로 고려에 원병을 요청하러 파견된 관리.
    '김웅원': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 김헌창의 난 당시의 장수.
    '김웅진': {'role': 'other'},  # 현대/대한민국 - 국회의원, 반민족행위특별조사위원회 검찰관 등을 역임하다가 한국전쟁 때 납북되어 북한에서, 
    '김원': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 「38선」 · 「설악산」 · 「한강」 등의 작품을 그린 화가.
    '김원구': {'role': 'other'},  # 고려 - 고려 후기에, 전법총랑 등을 역임한 문신.
    '김원국': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 중국 운남군관학교를 졸업한 후 만주로 건너가 정의부에서 무장투쟁을 전개한 독립운
    '김원규': {'role': 'other'},  # 현대/대한민국 - 해방 이후 경기중고등학교 교장, 서울사범학교 교장, 서울특별시 교육감 등을 역임한 교육자.
    '김원균': {'role': 'other'},  # 현대 - 해방 이후 북한에서 조선음악가동맹 중앙위원장, 조선민족음악위원장 등을 역임한 작곡가.
    '김원근': {'role': 'scholar'},  # 근대/개항기 | 근대/일제강점기 - 일제강점기 정신여학교 교사를 역임한 교육자. 한학자.
    '김원길': {'role': 'other'},  # 근대 - 해방 이후 국극단, 국악사 등에서 활동한 창극명인. 판소리명창.
    '김원량': {'role': 'other'},  # 조선 - 조선 후기에, 장례원사평, 공조좌랑, 지평 등을 역임한 문신 · 공신.
    '김원록': {'role': 'other'},  # 조선 - 조선 후기에, 병조좌랑, 돈녕도정, 동지돈녕부사 등을 역임한 문신.
    '김원룡': {'role': 'scholar novelist'},  # 현대/대한민국 - 서울대학교 고고미술사학과 교수, 한국고고학연구회 회장 등을 역임하였으며, 『신라토기의 연구
    '김원립': {'role': 'other'},  # 조선 - 조선 후기에, 부안현감, 능주목사, 종성부사 등을 역임한 문신.
    '김원만': {'role': 'other'},  # 현대 - 제4·5대 민의원, 내무부차관, 제7·8·9대 국회의원 등을 역임한 정치인.
    '김원망': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 장군 김유신의 다섯째 아들로 대아찬을 역임한 관리.
    '김원명': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 감찰집의, 판도판서 등을 역임한 문신 · 공신.
    '김원범': {'role': 'other'},  # 근대 - 대한제국기 때, 형 김원국과 함께 의병을 일으켰으며, 대동창의단을 조직하여 중군장으로 활약
    '김원벽': {'role': 'other'},  # 근대/일제강점기 - 1919년 3월 1일과 3월 5일 경성(지금의 서울특별시)에서 학생 만세 시위를 이끈 독립
    '김원복': {'role': 'other'},  # 해방 이후 서울대학교 음악대학교 교수를 역임한 교육자. 피아노연주자.
    '김원봉': {'role': 'other'},  # 일제강점기 때, 임시정부 군무부장, 광복군 부사령관 등을 역임하였고, 의열단과 조선의용대를
    '김원상': {'role': 'other'},  # 고려/고려 후기 - 고려 후기 충렬왕~충혜왕대에 활동한 문신이자 간신.
    '김원섭': {'role': 'other'},  # 조선 - 조선 후기에, 사헌부 · 사간원 · 홍문관의 청요직, 대사간 등을 역임한 문신.
    '김원술': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 석문전투에 참전한 장수.
    '김원식': {'role': 'other'},  # 근대/개항기 - 1907년 강원도 금강산 일대에서 의병을 일으킨 의병장.
    '김원영': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 중국 공군기지 중미혼합단 소속 장교(비행사)로, 웨양 · 헝양 등지에서 일본군 
    '김원용': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 때, 미국에서 하와이 대한인국민회 기관지의 주필, 주미 외교위원부 외교위원장 등
    '김원의': {'role': 'other'},  # 고려 - 고려후기 참지정사 판예부사, 문하시랑평장사 판병부사 등을 역임한 무신.
    '김원전': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 사은사로 당나라에 파견된 관리.
    '김원정': {'role': 'other'},  # 고려 - 고려 전기에, 서경유수사, 수태위문하시중 등을 역임한 문신.
    '김원조': {'role': 'other'},  # 근대 - 일제강점기 때, 대한군정부에서 군자금 모금 활동을 전개한 독립운동가.
    '김원충': {'role': 'other'},  # 고려 - 고려 전기에, 문하시랑평장사 판상서형부사, 수사도 문하시중 등을 역임한 문신.
    '김원태': {'role': 'other'},  # 현대 - 농림부차관, 재무부차관, 대한민국 헌정회 제9대 회장 등을 정치인 · 기업가.
    '김원필': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 집사부시랑을 역임한 관리.
    '김원행': {'role': 'scholar'},  # 조선 - 조선후기 종부시주부, 공조참의, 사성 등을 역임한 문신. 학자.
    '김원현': {'role': 'other'},  # 남북국시대 통일신라의 대신으로 당나라에 파견된 관리.
    '김원황': {'role': 'other'},  # 고려 - 고려 전기에, 중추원사, 중추원사 병부상서 등을 역임한 문신.
    '김원훈': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 아찬으로 중시를 역임한 귀족. 대신.
    '김월하': {'role': 'other'},  # 현대/대한민국 - 해방 이후 여창가곡의 전승자로 지정된 예능보유자.
    '김위': {'role': 'scholar'},  # 조선 - 조선후기 이조좌랑, 지평 등을 역임한 문신. 학자.
    '김위남': {'role': 'other'},  # 조선 - 조선 후기에, 공조좌랑, 병조좌랑, 통례 등을 역임한 문신.
    '김위량': {'role': 'other'},  # 고려 - 고려 후기에, 낭장, 장군 등을 역임한 무신 · 공신.
    '김위문': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 때, 신라 원성왕의 조부로, 중시 등을 역임한 통일신라의 귀족 · 관리.
    '김위제': {'role': 'other'},  # 고려 - 고려전기 위위승동정, 주부동정 등을 역임한 관리.
    '김위홍': {'role': 'other'},  # 고대/남북국/통일신라 - 통일신라의 제48대 신라 경문왕의 동생으로, 각간, 상대등, 병부령 등을 역임한 통일신라의
    '김유': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 찬수낭관, 대제학 등을 역임한 문신.
    '김유감': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「서울새남굿」의 전승자로 지정된 예능보유자.
    '김유경': {'role': 'other'},  # 조선 - 조선 후기에, 사헌, 형조참판, 좌참찬 등을 역임한 문신.
    '김유규': {'role': 'other'},  # 고려/고려 전기 - 고려 전기에, 대관령, 공역령, 상식직장 등을 역임한 문신.
    '김유근': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 병조판서, 이조판서, 판돈녕부사 등을 역임한 문신.
    '김유기': {'role': 'other'},  # 조선/조선 후기 - 조선후기 여항육인의 한 사람으로 태평성대의 평안한 삶을 노래한 음악인.
    '김유길': {'role': 'other foreigner'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 일길찬으로서 일본에 파견된 사신.
    '김유돈': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 대아찬으로서 웅진도독부에 파견된 관리.
    '김유렴': {'role': 'other'},  # 고대/남북국/통일신라 - 통일신라의 제56대 경순왕의 사촌동생으로, 대아찬에 임명되었으며, 시중 등을 역임한 종실.
    '김유립': {'role': 'other'},  # 고려 - 고려 전기에, 명주도감창전중내급사 등을 역임한 문신.
    '김유방': {'role': 'novelist'},  # 근대/일제강점기 - 일제강점기 때, 김동인 등과 함께 우리나라 최초의 순수문예동인지 『창조』를 창간하였으며, 
    '김유성': {'role': 'other'},  # 근대 - 조선 후기에, 중추원 일등의관, 궁내부특진관, 규장각전제관 등을 역임한 문신.
    '김유순': {'role': 'other'},  # 근대 - 일제강점기 평양 남산현교회, 서울 만리현교회 등에서 목회 활동을 한 목사.
    '김유신': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 1938년 한국청년전지공작대를 거쳐 한국광복군에서 활동한 독립운동가.
    '김유연': {'role': 'other'},  # 조선 - 조선 후기에, 이조판서, 우의정, 판중추부사 등을 역임한 문신.
    '김유영': {'role': 'scholar'},  # 근대 - 일제강점기 「유랑」, 「애련송」, 「수선화」 등의 작품에 관여한 영화인. 영화감독.
    '김유정': {'role': 'novelist'},  # 일제강점기 『동백꽃』, 「봄봄」, 「따라지」 등을 저술한 소설가.
    '김유지': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 『의방유취』 편찬에 참여한 의관 · 공신.
    '김유철': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 1930년 남화한인청년연맹에 가입하여 무정부주의 독립운동을 시작하여 한국청년전지
    '김유탁': {'role': 'other'},  # 근대/개항기 | 근대/일제강점기 - 일제강점기 때, 「화조사군자」, 「조안도」 등을 그린 서화가.
    '김유택': {'role': 'other'},  # 현대 - 한국은행 총재, 주일대사, 재무부장관 등을 역임한 은행가 · 외교관 · 정치인.
    '김유하': {'role': 'other'},  # 근대 - 해방 이후 문교부 체육과 장학위원, 올림픽위원회 위원 등을 역임한 체육인.
    '김유행': {'role': 'other'},  # 근대 - 조선 후기에, 대사간, 협판내무부사, 이조참의 등을 역임한 문신.
    '김육': {'role': 'scholar'},  # 조선/조선 후기 - 조선 후기에 형조참의 · 병조참판 · 우의정 · 좌의정 · 영의정 등을 역임하였으며, 『구
    '김육진': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 경주 무장사 아미타여래조상사적비의 비문을 쓴 서예가.
    '김윤': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 제48대 경문왕의 넷째 아들인 왕자.
    '김윤겸': {'role': 'scholar'},  # 조선/조선 후기 - 조선후기 「동산계정도」 · 「금강산화첩」 · 「영남명승기행사경첩」 등의 작품을 그린 화가.
    '김윤경': {'role': 'scholar'},  # 근대 | 현대 - 『조선문자급어학사』, 『나라말본』, 『중등말본』 등을 저술한 국어학자.
    '김윤구': {'role': 'other'},  # 근대/개항기 | 근대/일제강점기 - 일제강점기 창덕궁 대조전 등을 신축한 건축가.
    '김윤기': {'role': 'other'},  # 근대/일제강점기|현대 - 교통부장관, 건설부장관 등을 역임한 건축가 · 관료.
    '김윤덕': {'role': 'other'},  # 현대/대한민국 - 해방 이후 가야금산조 및 병창의 전승자로 지정된 예능보유자.
    '김윤면': {'role': 'other'},  # 근대/개항기 - 개항기 동양물산 사장을 역임한 실업가.
    '김윤명': {'role': 'scholar'},  # 조선 - 조선시대 호조참의, 의금부도사, 오위도총부부총관 등을 역임한 문신. 학자.
    '김윤문': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 발해 침공 당시의 장수.
    '김윤보': {'role': 'other'},  # 근대/개항기 | 근대/일제강점기 - 개항기 「산수도」, 「쌍마인물도」, 「설중방우도」 등을 그린 화가.
    '김윤부': {'role': 'scholar'},  # 고대/남북국/통일신라 - 남북국시대 때, 숙위학생으로 당나라에서 유학하여 빈공과에 급제한 통일신라의 학자.
    '김윤서': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 때, 신한민주당 재정부장, 중국 중앙대학 농과대학 교수 등을 역임한 교육자 · 
    '김윤수': {'role': 'other'},  # 조선 - 조선전기 지중추부사, 충청도처치사 등을 역임한 무신.
    '김윤승': {'role': 'other'},  # 고려/고려 후기 - 고려 후기 권신(權臣) 지윤의 심복이었던 문신.
    '김윤식': {'role': 'scholar'},  # 조선/조선 후기 - 조선후기 황실제도국총재, 강구회 회장, 흥사단 단장 등을 역임한 문신. 학자.
    '김윤신': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 지평, 평안도도사, 안변부사 등을 역임한 문신.
    '김윤안': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 대구부사, 대사간 등을 역임한 문신.
    '김윤은': {'role': 'other'},  # 조선/조선 전기 - 조선시대 사옹원주부, 가선대부 등을 역임한 의관.
    '김윤정': {'role': 'other'},  # 근대 - 일제강점기 국민정신총동원조선연맹 평의원, 국민총력조선연맹 평의원 등을 역임한 관료. 친일반
    '김윤제': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 제사묘직, 군기주부, 금오위녹사참군사 등을 역임한 문신.
    '김윤중': {'role': 'other'},  # 고대/남북국/통일신라 - 신라 중대에 중시(中侍)와 장군으로 활동한 김유신의 손자.
    '김윤충': {'role': 'scholar'},  # 조선 - 조선 전기에, 사마시에 합격하였으나, 벼슬을 지내지 않고 은거하며 문예에 열중한 학자.
    '김윤택': {'role': 'other'},  # 현대 - 해방 이후 「송파산대놀이」 첫 상좌역의 전승자로 지정된 예능보유자.
    '김윤환': {'role': 'other'},  # 현대/대한민국 - 대한민국의 언론인 출신으로, 국회의원, 정무1장관, 민주자유당 사무총장 등을 지낸 정치인.
    '김윤후': {'role': 'other'},  # 고려/고려 후기 - 고려 후기 대몽항쟁 때 처인성과 충주성의 전투에서 크게 활약한 승려 출신 무신.
    '김율': {'role': 'other'},  # 근대 - 대한제국기 때, 호남창의회맹소에 가담하였으며, 신덕순 의진, 유병기 의진 등에서 활동한 의
    '김은': {'role': 'scholar'},  # 조선 - 조선 후기에, 가난한 집안에서 아우와 함께 학문에 전념하였으며, 호조좌랑에 추증된 학자.
    '김은거': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 때, 이찬 관등으로 당나라에 파견되었으며, 시중 등을 역임한 통일신라의 관리.
    '김은배': {'role': 'other'},  # 현대 - 해방 이후 헬싱키올림픽대회 육상감독, 대한체육회 상무이사 등을 역임한 체육인.
    '김은부': {'role': 'other'},  # 고려 - 고려 전기에, 지중추사, 호부상서, 중추사상호군 등을 역임한 문신.
    '김은우': {'role': 'other'},  # 현대/대한민국 - 해방 이후 한국철학회 부회장, 배재학당 재단이사장 등을 역임한 교육자. 언론인.
    '김은하': {'role': 'other'},  # 현대/대한민국 - 인천시의회 의원, 국회의원, 국회부의장, 교통체신위원 등을 역임한 정치인.
    '김은호': {'role': 'other'},  # 현대/대한민국 - 해방 이후 대한변호사협회 회장, 법조원로회 회장 등을 역임한 법조인.
    '김은휘': {'role': 'other'},  # 조선 - 조선 중기에, 통례원상례, 광주목사, 첨지중추부사 등을 역임한 문신.
    '김을한': {'role': 'other'},  # 현대/대한민국 - 해방 이후 서울신문 동경특파원, 서울신문 이사 등을 역임한 언론인.
    '김을현': {'role': 'other'},  # 조선/조선 전기 - 조선전기 인수부윤, 동지중추원사, 중추원부사 등을 역임한 역관.
    '김응근': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 충청도관찰사, 공조판서, 형조판서 등을 역임한 문신.
    '김응기': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 좌의정, 영중추부사 등을 역임한 문신.
    '김응남': {'role': 'other'},  # 조선 - 조선 중기에, 한성판윤, 병조판서 겸 부제찰사 등을 역임한 문신 · 공신.
    '김응덕': {'role': 'other'},  # 고려 - 고려 후기에, 나주사록을 역임하여 삼별초의 난에 대항한 문신.
    '김응락': {'role': 'other'},  # 현대/대한민국 - 일제강점기 안동교회 장로, 베다니전도교회 건축위원 등으로 활동한 개신교인. 육영사업가, 순
    '김응명': {'role': 'other'},  # 조선 - 조선 후기에, 생원이 되었으나, 벼슬에 뜻이 없어 향리에서 학문에 전념한 유생.
    '김응문': {'role': 'other'},  # 고려 - 고려 후기에, 대부윤, 비서소윤, 판삼사사 등을 역임한 문신.
    '김응백': {'role': 'other foreigner'},  # 근대 - 대한제국기 때, 황영문 의진에서 일본인 사살과 군자금 모금 활동을 전개한 의병.
    '김응삼': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 한국광복군 제3징모처 위원으로 선임되어 초모 활동 및 대적 선전 활동을 전개한 
    '김응상': {'role': 'other'},  # 조선/조선 전기 - 조선 전기 종사관과 병마절도사를 역임한 무신.
    '김응생': {'role': 'scholar'},  # 조선 - 조선 전기에, 생원이 되었으나, 벼슬을 지내지 않고 향촌교육에 전념한 학자.
    '김응섭': {'role': 'other'},  # 근대 - 일제강점기 때, 임시정부 법무장관, 조선공산당 만주총국 간부 등을 역임한 법조인 · 독립운
    '김응순': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 한성부좌윤, 호조참판, 한성부우윤 등을 역임한 문신.
    '김응원': {'role': 'other'},  # 근대/일제강점기 - 조선후기 「석란도」를 그린 서화가.
    '김응인': {'role': 'other'},  # 고려 - 고려 전기 강조의 정변 당시에, 강조가 목종을 폐하고 현종을 왕으로 옹립할 수 있도록 도왔
    '김응정': {'role': 'novelist'},  # 조선 - 조선 중기에  「서산일락가」 · 『해암문집』 등을 저술한 문인.
    '김응조': {'role': 'other'},  # 현대/대한민국 - 해방 이후 예수교대한성결교회 및 성결대학교 창립자인 목사.
    '김응진': {'role': 'other'},  # 현대 - 해방 이후 「군자란」 · 「향원정」 · 「비원」 등을 그린 화가. 서양화가.
    '김응창': {'role': 'other'},  # 조선 - 조선 후기 임진왜란 때, 선조를 호종한 공으로 녹훈되었으나, 이괄의 난에 연루되어 처형된 
    '김응탁': {'role': 'other'},  # 조선/조선 후기 - 조선시대 내의원내의를 역임한 의관.
    '김응태': {'role': 'other'},  # 근대 - 일제강점기, 일제의 종교 정책에 협력한 감리교 목사.
    '김응표': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 「향상회관 뒤에서」, 「정물」, 「A목사의 댁」 등을 그린 화가. 서양화가.
    '김응하': {'role': 'other'},  # 조선 - 조선시대 후금정벌과 관련된 무신.
    '김응해': {'role': 'other'},  # 조선 - 조선시대 정주부사, 별장, 어영대장 등을 역임한 무신.
    '김응환': {'role': 'scholar'},  # 조선/조선 후기 - 조선후기 「금강산화첩」 · 「금강전도」 · 「강안청적도」 등의 작품을 그린 화가.
    '김의': {'role': 'other'},  # 고려/고려 후기 - 고려후기 밀직부사, 동지밀직사사 등을 역임한 무신.
    '김의관': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 신영대왕으로 추봉된 귀족.
    '김의광': {'role': 'other'},  # 고려/고려 후기 - 고려후기 신문색, 장군, 부지밀직사사 등을 역임한 환관. 문신.
    '김의복': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 백수성전투, 석문전투에 참전한 장수.
    '김의영': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라 제38대 원성왕의 둘째 아들인 왕자.
    '김의원': {'role': 'other'},  # 조선 - 조선 중기에, 보덕, 악정, 대사간 등을 역임한 문신.
    '김의정': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 공조좌랑, 훈련원부정, 종부시첨정 등을 역임한 문신.
    '김의종': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라 제42대 흥덕왕의 둘째 아들인 왕자.
    '김의준': {'role': 'other'},  # 현대/대한민국 - 서울고등법원 판사, 국회의원, 국회 법제사법위원장 등을 역임한 법조인 · 정치인.
    '김의진': {'role': 'scholar'},  # 고려 - 고려전기 지공거, 판상서병부사, 평장사 등을 역임한 문신. 학자.
    '김의충': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 시중, 이벌찬 등을 역임한 귀족. 대신.
    '김의택': {'role': 'other'},  # 현대/대한민국 - 충청북도 경찰국장, 신민당 수석부총재, 민권당 총재 등을 역임한 정치인.
    '김의한': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 임시정부 비서, 한국독립당 상무위원, 광복군총사령부 주계 등을 역임한 독립
    '김의행': {'role': 'poet'},  # 조선/조선 후기 - 조선 후기 교서관 서리를 지낸 경아전 출신으로, 『삼류재유고』를 저술한 여항시인.
    '김이': {'role': 'other'},  # 고려 - 고려 후기에, 사헌집의, 밀직부사, 첨의중찬 등을 역임한 문신.
    '김이건': {'role': 'other'},  # 조선 - 조선 후기에, 참봉, 청도군수, 청주목사 등을 역임한 문신.
    '김이걸': {'role': 'other'},  # 근대 - 일제강점기 때, 친일파 이완용과 이용구의 암살을 계획하였으며, 의용단에서 군자금 모금 활동
    '김이곤': {'role': 'scholar'},  # 조선 - 조선후기 동궁시직, 신계현령 등을 역임한 문신. 학자.
    '김이교': {'role': 'other'},  # 조선 - 조선 후기에, 공조판서, 예조판서, 우의정 등을 역임한 문신.
    '김이구': {'role': 'scholar'},  # 조선 - 조선 후기에, 경학과 예학에 주력하였으며, 호조참판에 추증된 학자.
    '김이도': {'role': 'other'},  # 조선 - 조선 후기에, 대사헌, 수원부유수 등을 역임한 문신.
    '김이련': {'role': 'other'},  # 근대 - 개항기 의주교회 창설에 공헌한 개신교인.
    '김이례': {'role': 'other'},  # 조선 - 조선 후기에, 군수, 첨지중추부사조사오위장 등을 역임한 문신.
    '김이만': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 집의, 통정대부, 첨지중추부사 등을 역임한 문신.
    '김이상': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 통례원통례, 덕천군수, 영원군수 등을 역임한 문신.
    '김이생': {'role': 'other'},  # 고려 - 고려후기 낭장, 자문지유, 상장군 동남도지휘사 등을 역임한 무신.
    '김이석': {'role': 'novelist'},  # 근대 - 해방 이후 「실비명」, 「동면 冬眠」, 「외뿔소」 등을 저술한 작가. 소설가.
    '김이섭': {'role': 'other foreigner'},  # 근대 - 일제강점기 때, 정의부에서 교육 · 선전활동과 군자금 모금, 친일파 처단, 일본관리 사살 
    '김이소': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 이조참판, 예조판서, 좌의정 등을 역임한 문신.
    '김이안': {'role': 'scholar'},  # 조선 - 조선 후기에, 『의례경전기의』, 『계몽기의』, 『삼산재집』 등을 저술한 문신.
    '김이양': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 홍문관제학, 판의금부사, 좌참찬 등을 역임한 문신.
    '김이어': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 숙위학생으로서 당나라 빈공과에 급제한 관리.
    '김이영': {'role': 'other'},  # 고려/고려 전기 - 고려 전기 의종의 동생 대령후(大寧侯) 왕경(王暻) 유배사건과 관련된 문신.
    '김이원': {'role': 'other'},  # 근대 - 일제강점기 때, 평안북도 의주의 독립만세시위를 주도한 독립운동가.
    '김이음': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 우사간, 강원도관찰사, 호조참판 등을 역임한 문신.
    '김이익': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 형조판서, 한성부판윤, 대호군 등을 역임한 문신.
    '김이재': {'role': 'other'},  # 조선 - 조선 후기에, 상호군, 공조판서, 이조판서 등을 역임한 문신.
    '김이주': {'role': 'other'},  # 조선 - 조선 후기에, 행부사직, 대사헌, 형조판서 등을 역임한 문신.
    '김이직': {'role': 'other'},  # 근대 - 일제강점기 때, 연해주에서 니콜라예프스크재류 한인민단의 초대단장을 역임하여 교육구제사업 및
    '김이혁': {'role': 'scholar'},  # 조선/조선 후기 - 조선후기 「고산구곡담총도」, 「산수도」 등의 작품을 그린 화가.
    '김이희': {'role': 'other'},  # 조선 - 조선 후기에, 대사간, 동지의금부사, 대사헌 등을 역임한 문신.
    '김익': {'role': 'other'},  # 조선 - 조선 후기에, 판중추부사, 동지사은사, 영의정 등을 역임한 문신.
    '김익겸': {'role': 'other'},  # 조선 - 조선시대 병자호란 때, 강화도에서 항전하여 영의정으로 추증된 문신.
    '김익경': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 대사헌, 이조참의, 예조참판 등을 역임한 문신.
    '김익곤': {'role': 'other'},  # 근대 - 일제강점기 때, 대한독립단과 광복군사령부에서 군자금 모금, 친일파 처단, 일제기관 파괴 등
    '김익기': {'role': 'other'},  # 현대/대한민국 - 국회의원, 국회 사회보건위원장 등을 역임한 정치인.
    '김익노': {'role': 'other'},  # 현대/대한민국 - 국회의원, 국회징계자격위원장 등을 역임하였으며, 발췌개헌, 사사오입 개헌 등 이승만의 정치
    '김익달': {'role': 'other'},  # 현대/대한민국 - 해방 이후 대양출판사를 설립하여 3,000여 종의 단행본을 발행한 출판인.
    '김익동': {'role': 'scholar'},  # 조선 - 조선 후기에, 『상제의집록』, 『직재문집』 등을 저술한 학자.
    '김익두': {'role': 'other'},  # 근대 - 일제강점기에, 개신교 부흥사로서 큰 업적을 남긴 평양신학교 출신의 개신교 목사.
    '김익문': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 광주부유수, 한성부판윤, 홍문관제학 등을 역임한 문신.
    '김익복': {'role': 'other'},  # 조선 - 조선 중기에, 도사, 영남군수 등을 역임한 문신.
    '김익상': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 의열단에 가입하여 조선총독부 투탄 의거를 전개하였고, 육군대장 다나카 암살
    '김익수': {'role': 'other'},  # 조선 - 조선 전기에, 병조참판, 관상감제조 등을 역임한 문신.
    '김익용': {'role': 'other'},  # 근대 - 조선후기 한성부판윤, 형조판서, 예문관제학 등을 역임한 관리.
    '김익정': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 재랑, 통정대부, 가선대부 등을 역임한 문신.
    '김익주': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 멕시코로 노동 이민하여 대한인국민회 탐피코지방회를 결성하였고, 식당 경영으
    '김익중': {'role': 'other'},  # 근대 - 대한제국기 때, 호남창의맹소에서 종사로 활약한 의병장.
    '김익진': {'role': 'other'},  # 현대/대한민국 - 해방 이후 순심중학교 교장, 성의중학교 교감, 근화여자중학교 교감 등을 역임한 교육자이자 
    '김익훈': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 광주부윤, 형조참판, 어영대장 등을 역임한 문신.
    '김익휴': {'role': 'other'},  # 조선 - 조선 후기에, 행호군, 공조판서, 이조판서 등을 역임한 문신.
    '김익희': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 대사성, 대사헌, 대제학 등을 역임한 문신.
    '김인': {'role': 'other'},  # 근대 - 일제강점기 때, 한국국민당 조직에 참여하였고, 한국국민당청년단의 기관지 『전고』, 『청년호
    '김인겸': {'role': 'novelist'},  # 조선/조선 후기 - 조선 후기에, 「일동장유가」, 『동사록』 등을 저술한 문인.
    '김인경': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 혜순옹주와 혼인하여 광천위에 봉해진 문신.
    '김인관': {'role': 'scholar'},  # 조선 - 조선시대 「어해도」, 「화훼도」, 「초충도」 등의 작품을 그린 화가.
    '김인광': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 지김해부 진례성 제군사 명의장군으로 불렸던 호족.
    '김인규': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 「새출발」, 「조선해협」, 「병정님」 등에 출연한 배우 · 미술인 · 친일
    '김인근': {'role': 'other'},  # 근대 - 일제강점기 때, 안창호의 지시를 받고 평양 특파원으로 파견되어 항일투쟁을 전개한 독립운동가
    '김인령': {'role': 'scholar'},  # 조선/조선 전기 - 조선 전기에, 예조좌랑, 문학, 지평 등을 역임한 문신.
    '김인문': {'role': 'other'},  # 고려/고려 후기 - 고려후기 문황의 김준암살미수사건과 관련된 관리. 무신.
    '김인서': {'role': 'other'},  # 근대 - 일제강점기 때, 함경북도 회령에 임시정부 연통제를 조직하여 정보 수집 및 군자금 모금 활동
    '김인석': {'role': 'other'},  # 고려 - 고려 전기에, 장주분도, 상서우승 등을 역임한 문신.
    '김인선': {'role': 'other'},  # 고려/고려 후기 - 고려후기 내전숭반을 역임한 환관.
    '김인섭': {'role': 'other'},  # 근대 - 조선 후기에, 장녕전별검, 사간원정언 등을 역임한 문신.
    '김인손': {'role': 'other'},  # 조선 - 조선 전기에, 평안도관찰사, 지중추부사, 지돈녕부사 등을 역임한 문신.
    '김인승': {'role': 'other'},  # 근대/일제강점기 | 현대 - 일제강점기 「나부」, 「아틀리에 」, 「가락」 등을 그린 화가. 서양화가, 친일반민족행위자
    '김인식': {'role': 'other'},  # 근대/일제강점기 - 한국 최초의 서양 음악가로 「학도가」 · 「표의」 · 「부모은덕가」 등 다수의  노래를 작
    '김인연': {'role': 'other'},  # 고려 - 고려 후기에, 지신사, 밀직사, 찬성사 등을 역임한 문신.
    '김인영': {'role': 'scholar'},  # 근대 - 일제강점기 감리교신학교교장, 기독교조선감리회연맹 이사 등을 역임한 목사. 신학자.
    '김인위': {'role': 'other'},  # 고려 - 고려전기 평장사, 상서좌복야 참지정사 주국 경조현 개국남 등을 역임한 문신.
    '김인전': {'role': 'other'},  # 근대 - 일제강점기 때, 임시정부 국무원 학무차장, 임시의정원 전원위원장, 의장, 대한적십자회 상의
    '김인존': {'role': 'other'},  # 고려 - 고려 전기에, 비서감, 병부, 예부, 호부상서, 익성동덕공신 등을 역임한 문신 · 공신.
    '김인찬': {'role': 'other'},  # 조선 - 조선전기 중추원사, 의흥친군위동지절제사 등을 역임한 무신. 무신.
    '김인태': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라 제29대 태종무열왕의 다섯째 아들인 왕자.
    '김인항': {'role': 'scholar'},  # 조선 - 조선 후기에, 『도촌유고』 등을 저술한 학자.
    '김인호': {'role': 'other'},  # 고려 - 고려 후기에, 밀직부사, 순성익찬보리공신도첨의참리, 찬성사 등을 역임한 문신 · 공신.
    '김인환': {'role': 'scholar'},  # 현대/대한민국 - 경북대학교 농학과 교수, 농촌진흥청장 등을 역임하였고, 통일벼의 보급확대에 힘쓴 농학자 ·
    '김인후': {'role': 'scholar'},  # 조선/조선 전기 - 조선전기 세자시강원설서, 홍문관부수찬, 제술관 등을 역임한 문신. 학자.
    '김일': {'role': 'other'},  # 고려 - 고려 후기에, 검교중랑장, 금적사, 보빙사 등을 역임한 문신.
    '김일경': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 정언, 동부승지, 이조판서 등을 역임한 문신.
    '김일곤': {'role': 'other'},  # 근대 - 일제강점기 때, 조선의용군 진서북지대 책임자, 화북조선독립동맹 진서북분맹 조직위원 등을 역
    '김일동': {'role': 'other'},  # 조선/조선 전기 - 조선전기 황해도 신계에서 반란을 일으킨 주모자.
    '김일두': {'role': 'other'},  # 근대 - 일제강점기 때, 임시정부 통신원으로 임명되어 군자금 모금 활동을 전개한 독립운동가.
    '김일봉': {'role': 'other'},  # 근대 - 일제강점기 때, 대한독립단에서 친일파 숙청, 일제기관 파괴, 군자금 모금 활동 등을 전개한
    '김일손': {'role': 'scholar'},  # 조선/조선 전기 - 조선 전기에, 『탁영집』 등을 저술한 문신.
    '김일수': {'role': 'other'},  # 근대 - 일제강점기 조공재건설준비위원회 책임비서, 공산주의자협의회 군사부책임자 등을 역임한 사회주의
    '김일엽': {'role': 'scholar'},  # 근대 - 해방 이후 『청춘을 불사르고』, 『행복과 불행의 갈피에서』 등을 저술한 승려.
    '김일원': {'role': 'other'},  # 근대 - 대한제국기 때, 정환직 의진에서 항일의병활동을 전개한 의병.
    '김일진': {'role': 'scholar'},  # 조선 - 조선 후기에, 변려체에 재능을 보였으며, 폐비된 인현왕후에게 예를 표하고, 과거에서의 부정
    '김일해': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 「춘풍」 · 「오몽녀」 · 「순정해협」 등에 출연한 배우. 영화배우.
    '김일환': {'role': 'other'},  # 근대/일제강점기 - 일제강점기인 1940년 한국광복군 창설 이후 제2지대 간부로 활동한 독립운동가.
    '김임상': {'role': 'other foreigner'},  # 남북국시대 통일신라의 부사로 일본에 파견된 관리.
    '김입견': {'role': 'other'},  # 고려 - 고려후기 판밀직사사 등을 역임한 무신.
    '김입지': {'role': 'scholar'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 숙위학생으로 당나라에서 유학한 학자. 문장가.
    '김잉석': {'role': 'scholar'},  # 현대/대한민국 - 동국대학교 불교대학장 등을 역임하였으며, 『불교학개론』, 『화엄학개론』 등을 저술한 불교학
    '김자': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 우대언, 대독관, 좌대언 등을 역임한 문신.
    '김자경': {'role': 'other'},  # 현대/대한민국 - 해방 이후 김자경오페라단 단장, 한국음악협회 부이사장 등을 역임한 음악인. 성악가.
    '김자류': {'role': 'other'},  # 고려/고려 전기 - 고려 전기 이자겸의 난으로 불탄 궁궐을 중수한 문신.
    '김자린': {'role': 'other'},  # 현대/대한민국 - 북한에서, 조선인민군 군단 부군단장, 민족보위성 부국장, 최고인민회의 대의원 등을 역임한 
    '김자림': {'role': 'playwright novelist'},  # 현대/대한민국 - 해방 이후 「돌개바람」, 「신들의 결혼」, 「이민선」 등의 작품을 낸 극작가.
    '김자수': {'role': 'other'},  # 고려 - 고려 후기에, 판전교시사, 충청도관찰사, 형조판서 등을 역임한 문신.
    '김자의': {'role': 'other'},  # 고려/고려 전기 - 고려 전기에, 동지공거, 우산기상시, 예부상서 등을 역임한 문신.
    '김자점': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 강화부윤, 우의정, 어영청도제조 등을 역임한 문신.
    '김자정': {'role': 'other'},  # 조선 - 조선 전기에, 황해도관찰사, 지의금부사, 한성부판윤 등을 역임한 문신.
    '김자지': {'role': 'other'},  # 고려 - 조선 전기에, 평안도관찰사, 형조판서, 개성부유후 등을 역임한 문신.
    '김자진': {'role': 'other'},  # 고려 - 고려전기 대장군 고문개 등의 역모와 관련된 무신.
    '김자환': {'role': 'other'},  # 조선/조선 전기 - 조선전기 여진에서 조선에 귀화한 유민.
    '김자희': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 강원도 홍천군 내촌면 물걸리의 독립만세시위에 참여했다가 순국한 독립운동가.
    '김작': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 병조판서, 수지중추부사, 형조판서 등을 역임한 문신.
    '김작빈': {'role': 'other'},  # 고려 - 고려 전기에, 어사중승, 상서우승, 대부경 등을 역임한 문신.
    '김잠': {'role': 'other'},  # 고려 - 고려 후기에, 송문중, 권근 등과 응거시에 합격한 문신.
    '김장': {'role': 'other'},  # 고려 - 고려 후기에, 대호군 등을 역임한 무신 · 공신.
    '김장렴': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 제41대 헌덕왕의 아들인 왕자.
    '김장생': {'role': 'scholar'},  # 조선/조선 후기 - 조선 후기에, 『상례비요』, 『가례집람』, 『근사록석의』 등을 저술한 문신.
    '김장손': {'role': 'other'},  # 근대/개항기 - 개항기 임오군란 당시의 주모자.
    '김장수': {'role': 'other'},  # 고려 - 고려후기 상장군 겸 만호, 교주도병마사, 상호군 등을 역임한 무신.
    '김장순': {'role': 'scholar'},  # 조선/조선 후기 - 조선 후기, 선종한과 함께 『감저신보』를 저술한 농학자.
    '김장언': {'role': 'other foreigner'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 급찬으로 일본에 파견된 관리.
    '김장여': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 파진찬으로 시중을 역임한 관리.
    '김장이': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 장군 김유신의 넷째 아들로 대아찬을 역임한 관리.
    '김장청': {'role': 'scholar'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 집사랑으로 김유신의 행록을 저술한 관리.
    '김장훈': {'role': 'other'},  # 현대/대한민국 - 해방 이후 해군함대 부사령관, 해군통제 부사령관, 해군중장 등을 역임한 군인. 관료.
    '김재계': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 전라남도 장흥의 3·1운동을 주도하고 1930년대 후반에 '멸왜기도'를 드리다가
    '김재관': {'role': 'scholar'},  # 현대/대한민국 - 철강, 자동차 등 우리나라 중공업의 발전 방안을 제시한 과학자이자 기술 관료.
    '김재광': {'role': 'other'},  # 현대/대한민국 - 서울시의회 의원, 제7·8·9·10·12대 국회의원, 통일민주당 상임고문 등을 역임한 정치
    '김재규': {'role': 'other'},  # 현대 - 해방 이후 10, 26 박정희 대통령 시해사건 당시의 군인. 정치인.
    '김재근': {'role': 'scholar'},  # 현대/대한민국 - 서울대학교 조선공학과 교수, 대한조선학회 회장 등을 역임하였으며, 『거북선의 신화』, 『한
    '김재덕': {'role': 'other'},  # 근대 - 일제강점기 때, 임시의정원 비서, 교하중학교 교장, 정의부 중앙상임대의원, 국민부 집행위원
    '김재로': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 병조판서, 판중추부사, 영의정 등을 역임한 문신.
    '김재룡': {'role': 'other'},  # 근대 - 일제강점기 때, 성진회, 옥과노동회에서 동맹휴교와 광주학생항일운동을 주도한 독립운동가.
    '김재명': {'role': 'other'},  # 현대/대한민국 - 해방 이후 육군 제1군단장, 합참본부장 겸 대간첩대책 본부장, 국방부 인력차관보 등을 역임
    '김재백': {'role': 'other foreigner'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 대나마로서 일본에 파견된 사신.
    '김재범': {'role': 'other'},  # 근대 - 일제강점기 동북항일연군 제2군 제6사 제7단에서 정치위원으로 활동한 사회주의운동가.
    '김재봉': {'role': 'other'},  # 근대/일제강점기 - 일제강점기, 조선공산당 초대 책임비서를 지낸 사회주의운동가 · 독립운동가.
    '김재석': {'role': 'other'},  # 현대/대한민국 - 해방 이후 조선미술가협회 위원, 조선공예가회 회장 등을 역임한 공예가. 도예가.
    '김재선': {'role': 'other'},  # 근대 - 해방 이후 대한국악원 이사, 전국국악인친목회 회장 등을 역임한 장구명인.
    '김재섭': {'role': 'other'},  # 현대/대한민국 - 해방 이후 주식회사 영창악기를 설립한 기업인.
    '김재수': {'role': 'other'},  # 조선 - 조선후기 효행으로 정려를 하사 받고, 동몽교관에 추증된 효자.
    '김재순': {'role': 'other'},  # 조선 - 조선 후기에, 대사간, 경상도관찰사, 대사헌 등을 역임한 문신.
    '김재욱': {'role': 'other'},  # 현대/대한민국 - 북한에서, 농업부 부장, 평남도당위원장 등을 역임하였으나, 8월 종파사건을 계기로 숙청된 
    '김재원': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「꼭두각시놀음」의 덜미 전승자로 지정된 기예능보유자.
    '김재익': {'role': 'scholar'},  # 현대/대한민국 - 경제기획원 기획국장, 제5공화국 대통령비서실 경제수석비서관 등을 역임한 경제학자 · 관료.
    '김재일': {'role': 'scholar'},  # 조선 - 조선후기 사헌부지평, 사간원정언, 이조정랑 등을 역임한 문신. 학자.
    '김재준': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 『낙수』, 『요한계시록 주석』, 『황야에 외치는 소리』 등을 저술한 신학자이자 
    '김재찬': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 평안도관찰사, 한성부판윤, 우의정 등을 역임한 문신.
    '김재창': {'role': 'other'},  # 근대 - 일제강점기 때, 대한광복회에서 군자금 모금 활동 등을 전개한 독립운동가.
    '김재철': {'role': 'scholar'},  # 근대/일제강점기 - 일제강점기 때, 최초의 한국 연극사 연구인 『조선연극사』를 저술한 국문학자.
    '김재학': {'role': 'other'},  # 현대 - 해방 이후 제헌의원, 삼성운수㈜대표이사 등을 역임한 정치인. 실업가.
    '김재항': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 안성군 삼죽면 덕산리의 독립만세시위에 참여했다가 순국한 독립운동가.
    '김재현': {'role': 'other'},  # 근대 - 조선 후기에, 경기도관찰사, 한성부판윤, 지중추부사 등을 역임한 문신.
    '김재호': {'role': 'other'},  # 현대 - 한국전쟁 당시 강원도 김화의 수도고지전투에 참전한 군인.
    '김재화': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 경상남도 진주의 독립만세시위를 주도한 혐의로 체포된 독립운동가.
    '김재훈': {'role': 'scholar'},  # 근대 - 일제강점기 경성음악전문학교 초대원장, 조선음악협회 이사 등을 역임한 음악인. 작곡가. 바이
    '김저': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 검열, 어사, 교리, 지평 등을 역임하다 을사사화에 관련되어 관직을 박탈당하
    '김적': {'role': 'other'},  # 고려 - 고려 후기에, 중랑장 등을 역임한 무신 · 공신.
    '김전': {'role': 'other'},  # 조선 - 조선 전기에, 공조판서, 한성부판윤, 영의정 등을 역임한 문신.
    '김점현': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 평안남도 대동군 금제면 원장리와 강서군 반석면 상사리 사천시장 일대의 독립
    '김정': {'role': 'scholar'},  # 조선 - 조선후기 강릉부사, 사간원정언, 제주목사 등을 역임한 문신. 학자.
    '김정견': {'role': 'scholar'},  # 조선/조선 후기 - 조선 후기에, 생원이 되었으나, 벼슬을 지내지 않고 향리에서 후진 양성에 힘쓴 학자.
    '김정경': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 공안부윤, 조군도총제, 개성부유후 등을 역임한 문신.
    '김정고': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 만파식적을 보관하던 천존고(天尊庫)의 창고지기로 근무한 관리.
    '김정구': {'role': 'other'},  # 현대/대한민국 - 일제강점기 「총각진정서」, 「왕서방 연서」, 「눈물 젖은 두만강」 등을 부른 가수.
    '김정국': {'role': 'scholar'},  # 조선 - 조선 전기에, 『사재집』, 『사재척언』, 『경민편』 등을 저술한 문신.
    '김정권': {'role': 'other foreigner'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 급찬으로서 일본에 파견된 사신.
    '김정균': {'role': 'other'},  # 조선 - 조선 후기에, 대사헌, 충청도관찰사 등을 역임한 문신.
    '김정근': {'role': 'other'},  # 근대 - 조선 후기에, 법부협판, 경위원총관, 경무사 등을 역임한 문신.
    '김정길': {'role': 'other'},  # 근대 - 대한제국기 박기홍의 제자로 김창환협률사등에서 활동한 판소리의 명창. 창극명인.
    '김정남': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 견당 청익승 엔닌[圓仁]의『입당구법순례행기』와 관련된 역관.
    '김정락': {'role': 'other foreigner'},  # 남북국시대 통일신라의 소판관으로 일본에 파견된 관리.
    '김정란': {'role': 'other'},  # 남북국시대 통일신라의 미인으로 『삼국유사』의 사미 묘정 설화와 관련된 주인공.
    '김정련': {'role': 'other'},  # 근대 - 일제강점기 때, 전라남도에서 군자금 모집 활동을 전개하다가 공명단에서 활동하며 독립군 비행
    '김정렬': {'role': 'other'},  # 현대 - 해방 이후 초대 공군참모총장, 국방부장관, 반공연맹 이사장 등을 역임한 군인. 정치인.
    '김정룡': {'role': 'other'},  # 조선 - 조선 중기에, 영월군수, 풍기군수, 이조정랑 등을 역임한 문신.
    '김정목': {'role': 'other'},  # 조선 - 조선 중기에, 사예, 내자시정, 장흥부사 등을 역임한 문신.
    '김정묵': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 1919년 대한민국임시정부 임시의정원 의원, 의열단 단원으로 활동한 독립운동가.
    '김정문': {'role': 'other'},  # 근대 - 일제강점기 송만갑의 제자로 동편제에 기초를 두고 서편제의 가락을 함께 구사한 판소리의 명창
    '김정범': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 통의부에서 군자금 모금 및 친일파 처단 등 항일무장투쟁을 전개한 독립운동가
    '김정수': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 서울대학교 공과대학 응용수학과 교수, 대한수학회 회장 등을 역임한 학자. 수학자
    '김정숙': {'role': 'other foreigner'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 대나마로 일본에 파견된 관리.
    '김정순': {'role': 'other'},  # 고려 - 고려 전기에, 참지정사, 상서우복야 서경유수사 겸 태자소부 등을 역임한 문신.
    '김정식': {'role': 'other'},  # 현대/대한민국 - 제2대 국회의원 · 자유당 문화부장 등을 역임한 정치인.
    '김정실': {'role': 'other'},  # 현대/대한민국 - 임시정부 산하 정치공작대의 총무, 단국대학교 재단설립 이사와 학장, 민의원 등을 역임한 교
    '김정언': {'role': 'scholar'},  # 고려 - 고려전기 태승, 한림학사, 내봉성령 등을 역임한 문신. 학자.
    '김정여': {'role': 'other'},  # 고려/고려 후기 - 고려후기 위사보좌공신에 책록된 공신. 무신.
    '김정연': {'role': 'other'},  # 현대 - 해방 이후 서도소리의 전승자로 지정된 예능보유자.
    '김정오': {'role': 'other'},  # 조선 - 조선 후기에, 사직서여, 형조정랑, 성현찰방 등을 역임한 문신.
    '김정원': {'role': 'other'},  # 근대 - 대한제국기 때, 경상북도 서북방 산간 지역에서 항일의병투쟁을 전개한 의병.
    '김정윤': {'role': 'other'},  # 조선 - 조선 후기에, 헌납, 공조참의 등을 역임한 문신.
    '김정익': {'role': 'other'},  # 근대 - 일제강점기 때, 친일파 이완용과 이용구의 암살을 계획한 혐의로 체포된 독립운동가.
    '김정일': {'role': 'other'},  # 현대/대한민국 - 북한에서, 김일성 사망 이후 권력을 승계한 제2대 통치자로, 국방위원장, 조선로동당 총비서
    '김정제': {'role': 'scholar'},  # 현대/대한민국 - 대한한의사협회 회장, 경희대학교 한의과대학 학장 등을 역임한 한의학자.
    '김정종': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 때, 이찬 관등으로 장군, 상대등 등을 역임한 통일신라의 관리.
    '김정주': {'role': 'scholar foreigner'},  # 현대/대한민국 - 해방 이후 「일본의 한국침략사」, 「구주와 한인」, 「일제통치사료」 등을 저술한 학자. 역
    '김정준': {'role': 'other'},  # 근대 - 해방 이후, 전국신학대학협의회 초대 회장, 한국신학대학 학장 등을 역임한 한국기독교장로회 
    '김정진': {'role': 'playwright novelist'},  # 근대/일제강점기 - 일제강점기 「찬웃음」, 「약수풍경」, 「꿈」 등의 작품을 낸 극작가. 언론인.
    '김정집': {'role': 'other'},  # 조선 - 조선 후기에, 동지성균관사, 대사헌, 평안도관찰사 등을 역임한 문신.
    '김정하': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 모스크바 동방노력자공산대학에서 조선민족부 교관을 지냈으며, 사회주의운동을 전개한
    '김정한': {'role': 'novelist'},  # 현대 - 해방 이후 「모래톱이야기」, 「수라도」, 「인간단지」 등을 저술한 작가. 소설가.
    '김정헌': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 제암리교회 지도자로 활동하였으며, 수원의 독립만세시위를 주도하다가 제암리 
    '김정현': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 「녹음」, 「귀로」, 「임」 등의 작품을 그린 화가.
    '김정혜': {'role': 'other'},  # 근대/대한제국기 - 대한제국기 정화여학교를 설립하고 여성을 위한 교육의 필요성을 역설한 교육자.
    '김정호': {'role': 'other'},  # 근대/개항기 | 근대/일제강점기 - 일제강점기 개성전기주식회사 대표이사, 개성상공회의소 회장 등을 역임한 기업인. 친일반민족행
    '김정환': {'role': 'other'},  # 근대/일제강점기 - 일제강점기, 충청북도 청원군에서 독립만세시위를 주도한 독립운동가.
    '김정후': {'role': 'other'},  # 조선 - 조선 후기에, 전적, 직강, 옹진군수 등을 역임한 문신.
    '김정희': {'role': 'scholar'},  # 조선 - 조선 후기에 조선 금석학파를 성립하고 추사체를 완성한 문신 · 학자 · 서화가.
    '김제': {'role': 'other'},  # 고려 - 고려 전기에, 이부상서 참지정사 겸 태자소보, 태자태보 등을 역임한 문신.
    '김제갑': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 정언, 층청도관찰사, 우승지 등을 역임한 문신.
    '김제겸': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 헌납, 집의, 예조참의, 승지 등을 역임하였으며, 목호룡의 고변으로 노론 4
    '김제공': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 제38대 원성왕 때 반란을 일으킨 주모자.
    '김제남': {'role': 'other'},  # 조선 - 조선 중기에, 이조좌랑, 돈녕부도정, 영돈령부사 등을 역임한 문신.
    '김제민': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 평안남도 대동군 금제면 원장리와 강서군 반석면 상사리 사천시장 일대의 독립
    '김제신': {'role': 'other'},  # 조선 - 조선 전기에, 정언, 집의, 좌승지, 예조참판 등을 역임한 문신.
    '김제안': {'role': 'other'},  # 고려 - 고려 후기에, 군부좌랑, 내서사인, 전교부령 등을 역임한 문신.
    '김제옹': {'role': 'other'},  # 고대/남북국/통일신라 - 통일신라의 제38대 원성왕의 손자로, 형 김언승(제41대 헌덕왕)과 난을 일으켜 애장왕을 
    '김제준': {'role': 'other'},  # 조선 - 조선후기 기해박해 당시의 순교자.
    '김제중': {'role': 'other'},  # 근대 - 일제강점기 때, 전라남도 곡성과 담양에서 임시정부의 군자금조달원으로 활동한 독립운동가.
    '김제철': {'role': 'other'},  # 조선 - 조선후기 8명창의 한 사람으로 「심청가」에 뛰어났던 판소리의 명창.
    '김제혜': {'role': 'other'},  # 근대 - 일제강점기 국제여성총회에 조선인 대표로 참석한 사회주의운동가.
    '김제환': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 제자들을 모아 배일사상을 고취하고 항일투쟁을 전개한 독립운동가.
    '김조': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 병조참판, 예조판서, 지중추원사 등을 역임한 문신.
    '김조규': {'role': 'poet'},  # 근대/일제강점기 - 일제강점기 「연심」, 「어버이 잃은 가슴이」, 「회향곡」 등을 저술한 시인.
    '김조근': {'role': 'other'},  # 조선/조선 후기 - 조선후기 어영대장, 영돈녕부사 등을 역임한 척신.
    '김조순': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 이조참의, 부제학, 이조판서 등을 역임한 문신.
    '김조이': {'role': 'other'},  # 근대 - 광복 이후 전조선민중운동자대회 준비위원, 민주주의민족전선 중앙위원 등을 역임한 사회주의운동
    '김존경': {'role': 'other'},  # 조선 - 조선 후기에, 강원도감사, 지중추부사, 경주부윤 등을 역임한 문신.
    '김존심': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 내시합문지후 등을 역임한 문신.
    '김존중': {'role': 'other'},  # 고려 - 고려 전기에, 첨사부녹사, 우정언, 우승선, 태자소보 등을 역임한 문신.
    '김종': {'role': 'scholar'},  # 조선 - 조선 전기에, 진사가 되었으나, 기묘사화가 일어나자 과거를 포기하고 은거하여 성리학적 예절
    '김종규': {'role': 'other'},  # 근대 - 조선후기 궁내부특진관, 경효전제조, 경상북도관찰사 등을 역임한 관리.
    '김종기': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 백낙준의 제자로 조선성악연구회에서 활동한 음악인. 거문고산조명인.
    '김종남': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 「풍경1」, 「호라」, 「물가」 등을 그린 화가. 서양화가.
    '김종덕': {'role': 'scholar'},  # 조선 - 조선 후기에, 『천사집』, 『석학정론』, 『초려문답』 등을 저술한 학자.
    '김종렬': {'role': 'other'},  # 현대 - 해방 이후 대한체육회 부회장, 서울올림픽대회조직위원회 위원 등을 역임한 체육인.
    '김종리': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 진산현감, 고부현감, 예문관직제학 등을 역임한 문신.
    '김종림': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 때, 미국으로 노동 이민하여 공립협회, 흥사단, 한인공동회, 대한인국민회 등에서
    '김종묵': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 간도 용정촌에서 전개된 독립만세시위를 주도하다가 순국한 독립운동가.
    '김종문': {'role': 'poet critic'},  # 현대/대한민국 - 해방 이후 『벽』, 『불안한 토요일』, 『시사시대』 등을 저술한 시인. 비평가.
    '김종민': {'role': 'other'},  # 조선 - 조선시대 미곶첨사를 역임한 무신.
    '김종발': {'role': 'scholar'},  # 조선 - 조선후기 승문원부정자, 사헌부지평, 장령 등을 역임한 문신. 학자.
    '김종범': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 조선노농총동맹과 북풍회에서 활동한 사회주의운동가, 독립운동가.
    '김종삼': {'role': 'poet'},  # 현대 - 해방 이후 『시인학교』, 『북치는 소년』, 『누군가 나에게 물었다』 등을 저술한 시인.
    '김종서': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 함길도도관찰사, 우의정, 좌의정 등을 역임한 문신.
    '김종석': {'role': 'scholar'},  # 한국광업진흥주식회사 상무이사, 대한광산학회 회장 등을 역임하였으며, 『자원개발통론』, 『한
    '김종선': {'role': 'other'},  # 현대/대한민국 - 일제강점기 때, 조선식산신탁회사 부사장, 서울 천도교 홍제소년군 단장 등을 역임하며 사회운
    '김종수': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 대제학, 이조판서, 우의정 등을 역임한 문신.
    '김종순': {'role': 'other'},  # 조선 - 조선 전기에, 판한성부사, 평안도관찰사, 지중추부사 등을 역임한 문신.
    '김종연': {'role': 'other'},  # 고려 - 고려후기 이성계 살해모의 당시의 장수.
    '김종영': {'role': 'scholar'},  # 현대 - 해방 이후 「3, 1운동 기념상」, 「가족」, 「전설」 등의 작품을 낸 조각가.
    '김종오': {'role': 'other'},  # 현대 - 한국전쟁 당시 강원도 철원의 백마고지전투에 참전한 군인.
    '김종우': {'role': 'other'},  # 근대 - 일제강점기, 한국교회의 초기 부흥사로 기독교조선감리회 3대 감독을 역임한 목사.
    '김종원': {'role': 'other'},  # 현대/대한민국 - 해방 이후 육군헌병총사령부 부사령관, 경남지구 계엄사령관 등을 역임한 군인. 경찰.
    '김종윤': {'role': 'other'},  # 조선 - 조선시대 어모장군, 행용양위부호군 등을 역임한 무신.
    '김종익': {'role': 'other'},  # 현대/대한민국 - 한국체육회 회장, 국회의원, 공화당 중앙위원회 부위원장 등을 역임한 정치인 · 교육자.
    '김종일': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 교리, 울산부사 등을 역임한 문신.
    '김종정': {'role': 'scholar'},  # 조선 - 조선후기 성균관대사성, 예조판서, 좌참찬 등을 역임한 문신. 학자.
    '김종직': {'role': 'scholar'},  # 조선/조선 전기 - 조선전기 병조참판, 홍문관제학, 공조참판 등을 역임한 문신. 학자.
    '김종진': {'role': 'other'},  # 근대 - 일제강점기 때, 한족총연합회 조직 선전 농무부 위원장 등을 역임한 독립운동가.
    '김종찬': {'role': 'scholar'},  # 근대/일제강점기 - 일제강점기 「산서」, 「진중의 A병단장」, 「몽고가족」 등의 작품을 그린 화가. 서양화가.
    '김종철': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 『교육계획론』, 『세계 안의 한국교육』, 『한국고등교육 연구』 등을 저술한 학자
    '김종태': {'role': 'scholar'},  # 근대 - 일제강점기 「아이」, 「포오즈」, 「낮잠」 등의 작품을 그린 화가.
    '김종표': {'role': 'other'},  # 근대 - 조선후기 대오전악, 집사악사 등을 역임한 가야금명인.
    '김종한': {'role': 'poet critic'},  # 근대/일제강점기 - 일제강점기 「귀로」 · 「고원의 시」 · 「할아버지」 등을 저술한 시인. 문학평론가 · 친
    '김종해': {'role': 'other'},  # 해방 이후 서울대학교 의과대학 교수, 화종신경정신과의원 원장 등을 역임한 의료인.
    '김종현': {'role': 'other'},  # 고려 - 고려 전기에, 예부원외랑, 우간의대부, 우산기상시 등을 역임한 문신.
    '김종호': {'role': 'other'},  # 현대/대한민국 - 해방 이후 주월군사참모장, 군수차관보, 육군소장 등을 역임한 군인. 경영인.
    '김종후': {'role': 'critic novelist'},  # 현대/대한민국 - 해방 이후 「작가의패기」, 「동양의 휴머니즘」, 「민족문학소론」 등을 저술한 평론가.
    '김종희': {'role': 'other'},  # 현대 - 해방 이후 제일화재해상보험 대표이사, 전국경제인연합회 부회장 등을 역임한 실업가.
    '김좌근': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 예조판서, 형조판서, 공조판서, 호조판서 등을 거쳐 영의정을 3번 연임한 문
    '김좌명': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 공조판서, 병조판서, 호조판서 등을 역임한 문신.
    '김좌진': {'role': 'other'},  # 근대/일제강점기 - 북로군정서를 이끌고 청산리 대첩을 승리로 이끈 독립운동가.
    '김주': {'role': 'other'},  # 조선 - 조선 후기에, 예조정랑, 춘추관기주관, 무안현감 등을 역임한 문신.
    '김주경': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 북한에서 「만경대」 · 「묘향산」 등의 작품을 그린 화가.
    '김주남': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 수원의 독립만세시위를 주도하다가 고주리 학살사건에 의해 사망한 독립운동가.
    '김주만': {'role': 'scholar'},  # 조선 - 조선 후기에, 『청헌집』 등을 저술한 학자.
    '김주신': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 영돈령부사, 호위대장 등을 역임한 문신.
    '김주업': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 수원의 독립만세시위에 참여했다가 고주리 학살사건에 의해 사망한 독립운동가.
    '김주열': {'role': 'other'},  # 현대/대한민국 - 대한민국의 의거 학생으로, 1960년, 3·15부정선거에 반대하는 마산 시위에 참가하였다가
    '김주우': {'role': 'other'},  # 조선/조선 후기 - 조선후기 정언, 지평, 경성판관 등을 역임한 문신. 서예가.
    '김주원': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 이찬으로 시중을 역임한 귀족. 재상.
    '김주정': {'role': 'other'},  # 고려 - 고려 후기에, 부성위, 진변만호, 응방도감사 등을 역임한 문신.
    '김주천': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 한찬 관등을 역임한 관리.
    '김주필': {'role': 'other'},  # 남북국시대 통일신라의 당나라에 사신으로 파견된 관리.
    '김주현': {'role': 'other'},  # 근대 - 개항기 봉상사제조, 장례원경 등을 역임한 관료.
    '김죽파': {'role': 'other'},  # 현대/대한민국 - 해방 이후 가야금산조 및 병창의 전승자로 지정된 예능보유자.
    '김준': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 의열단 간부학교 교관, 조선의용대 전방공작대원, 한국광복군 제1지대 제1구
    '김준거': {'role': 'other'},  # 고려 - 고려후기 무신정변과 관련된 무신.
    '김준근': {'role': 'scholar'},  # 개항기 「기산풍속도」 · 「텬로력뎡」 삽화 등의 작품을 그린 화가.
    '김준룡': {'role': 'other'},  # 조선 - 조선시대 김해부사, 경상도병마절도사 등을 역임한 무신.
    '김준민': {'role': 'other'},  # 조선/조선 후기 - 조선 전기 임진왜란 때 거제현령과 합천가장을 지낸 무신.
    '김준섭': {'role': 'other'},  # 근대 - 일제강점기 창극좌, 동일창극단 등에서 활동한 음악인. 창극명인, 판소리명창.
    '김준성': {'role': 'other'},  # 현대/대한민국 - 일제강점기 함흥 영생고등보통학교 훈육주임, 용정 은진중학교 교사 등을 역임한 교육자. 사회
    '김준승': {'role': 'other'},  # 근대 - 일제강점기 때, 통의부 국내파견 결사대원으로 군자금 모금 활동을 전개한 독립운동가.
    '김준업': {'role': 'other'},  # 조선 - 조선 후기에, 이괄의 난과 병자호란이 발발하자 의병을 일으켜 항쟁한 의병장.
    '김준연': {'role': 'other'},  # 현대/대한민국 - 일제강점기 때, 조선일보 모스크바 특파원, 동아일보 편집국장 등을 역임하였으며, 해방 이후
    '김준엽': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 학병 출신으로 일본 제국주의 군대를 탈출하여 한국광복군 제2지대에서 활동한 독립
    '김준영': {'role': 'other'},  # 현대/대한민국 - 일제강점기 「처녀총각」 · 「개나리 고개」 · 「홍도야 울지 마라」 등을 만든 작곡가.
    '김준태': {'role': 'other'},  # 현대/대한민국 - 대구지방검찰청 검사 · 국회의원 등을 역임한 법조인 · 정치인.
    '김준택': {'role': 'other'},  # 근대 - 일제강점기 때, 정의부 중앙집행위원, 조선혁명당 중앙집행위원, 조선혁명군 사령관 등을 역임
    '김준현': {'role': 'other'},  # 현대/대한민국 - 일제강점기 「평조회상」을 독주한 음악인. 피리명인.
    '김중건': {'role': 'other'},  # 근대/일제강점기 - 원종교를 창립하였으며, 대진단을 조직하고 대한국민단 지단장으로 활약한 독립운동가.
    '김중경': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 제33대 성덕왕의 첫째 아들인 왕자.
    '김중공': {'role': 'other'},  # 고대/남북국/통일신라 - 통일신라의 제41대 헌덕왕의 동생인 왕족.
    '김중구': {'role': 'other'},  # 고려 - 고려후기 지추밀원사, 지문하성사, 왕경유수병마사 등을 역임한 무신.
    '김중기': {'role': 'other'},  # 조선 - 조선후기 훈련대장, 총융사 등을 역임한 무신.
    '김중남': {'role': 'scholar'},  # 조선 - 조선후기 전적, 단성현감, 자인현감 등을 역임한 문신. 학자.
    '김중린': {'role': 'other'},  # 현대/대한민국 - 북한에서, 최고인민회의 대의원, 대남담당 당 비서 등을 역임한 관료.
    '김중명': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 효종대의 북벌과 관련한 무신.
    '김중문': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 형부낭중, 병부시랑, 판장작감사, 지삼사사 등을 역임한 문신.
    '김중보': {'role': 'scholar'},  # 조선/조선 전기 - 조선 전기에, 주사(朱砂)로 수은을 제조하는 방법을 개발한 학자.
    '김중서': {'role': 'other'},  # 현대/대한민국 - 해방 이후 대구고등법원장, 대법원 판사, 선거관리위원장 등을 역임한 법조인.
    '김중식': {'role': 'other'},  # 근대 - 일제강점기 때, 경기도 안성군 원곡면과 양성면 일대의 독립만세시위에 참여한 독립운동가.
    '김중업': {'role': 'other foreigner'},  # 현대 - 해방 이후 주한프랑스대사관, 올림픽공원 상징조형물 등을 신축한 건축가.
    '김중온': {'role': 'other'},  # 고려 - 고려후기 부방장군, 분도장군 등을 역임한 무신.
    '김중원': {'role': 'scholar'},  # 조선 - 조선 후기에, 이인좌의 난을 진압하기 위해 의병을 일으켰고, 『퇴장암유집』 등을 저술하며 
    '김중일': {'role': 'other'},  # 조선 - 조선후기 어영장, 훈련원판관 등을 역임한 무신.
    '김중청': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 정언, 신안현감, 승정원승지 등을 역임한 문신.
    '김중하': {'role': 'scholar'},  # 조선 - 조선 후기에, 돈령부도정, 형조참의 등에 임명되었으나, 벼슬에 뜻이 없어 모두 사양한 학자
    '김중현': {'role': 'scholar'},  # 현대/대한민국 - 일제강점기 「무녀도」 · 「농악놀이」 등의 작품을 그린 화가.
    '김중환': {'role': 'other'},  # 근대 - 조선후기 중추원의관, 개성부윤, 문부조사위원 등을 역임한 관리.
    '김증한': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 『법학통론』, 『민법총칙』, 『물권법』 등을 저술한 학자. 교육행정가.
    '김지': {'role': 'other'},  # 조선 - 조선 전기에, 공주목사 등을 역임한 문신.
    '김지겸': {'role': 'other'},  # 고려 - 고려 후기에, 밀직부사, 영해부사, 권정동성 등을 역임한 문신.
    '김지경': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 이조참의, 예문관부제학, 지중추부사 등을 역임한 문신.
    '김지남': {'role': 'scholar'},  # 조선/조선 후기 - 조선후기 지중추부사로 『신전자초방』, 『동사록』, 『통문관지』 등을 저술한 역관.
    '김지대': {'role': 'scholar'},  # 고려 - 고려 후기에, 정당문학이부상서, 중서시랑평장사 등을 역임한 문신.
    '김지량': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라에서 하정사로서 당나라에 파견된 사신.
    '김지렴': {'role': 'other'},  # 고대/남북국/통일신라 - 통일신라의 제33대 성덕왕의 조카로, 당나라에 사신으로 방문한 종실.
    '김지만': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 때, 당나라에 사신으로 방문하여 태복경에 임명된 통일신라의 왕족.
    '김지묵': {'role': 'other'},  # 조선 - 조선 후기에, 판돈령부사, 총융사 등을 역임한 문신.
    '김지복': {'role': 'other'},  # 조선 - 조선 후기에, 사예, 형조좌랑 등을 역임한 문신.
    '김지산': {'role': 'other foreigner'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 아찬으로서 일본에 파견된 사신.
    '김지상': {'role': 'other foreigner'},  # 고대/남북국/통일신라 - 남북국시대 통일신라에서 파진찬으로서 일본에 파견된 사신.
    '김지서': {'role': 'other'},  # 고려 - 고려 후기에, 병마사, 만호 등을 역임한 무신 · 공신.
    '김지석': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 제주부사 등을 역임한 문신.
    '김지섭': {'role': 'other foreigner'},  # 근대/일제강점기 - 의열단원으로서 일본 왕궁에 폭탄을 투척한 독립운동가.
    '김지성': {'role': 'other'},  # 고려 - 고려후기 후군지병마사, 대장군, 추밀원부사 등을 역임한 무신.
    '김지수': {'role': 'other'},  # 조선 - 조선 후기에, 보덕, 종성부사 등을 역임한 문신.
    '김지숙': {'role': 'other'},  # 고려 - 고려 후기에, 동지광정원사 참지기무, 도첨의찬성사 판감찰사사, 첨의중찬 등을 역임한 문신.
    '김지옥': {'role': 'other'},  # 현대 - 해방 이후 「강령탈춤」의 전승자로 지정된 예능보유자.
    '김지우': {'role': 'other'},  # 고려 - 고려 전기에, 선경부사인, 합문지후, 안서도호부판관 등을 역임한 문신.
    '김지웅': {'role': 'other'},  # 조선 - 조선후기 청성첨절제사, 별군직, 맹산현감 등을 역임한 무신.
    '김지원': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 때, 이찬 관등으로 시중을 역임한 통일신라의 관리.
    '김지저': {'role': 'other'},  # 고려 - 고려후기 임유무 제거, 삼별초의 난 등과 관련된 무신.
    '김지태': {'role': 'other'},  # 현대/대한민국 - 해방 이후 한국생사회 회장, 대한상공회의소 부회장 등을 역임한 실업가. 정치인, 언론인.
    '김지화': {'role': 'other'},  # 고려 - 고려 전기에, 좌복야 참지정사, 태자소사, 판병부사 등을 역임한 문신.
    '김지환': {'role': 'other'},  # 근대/일제강점기 - 3·1운동 당시 ｢독립의견서｣, ｢독립청원서｣ 등을 상하이의 현순에게 전달하는 임무를 맡았
    '김직량': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라에서 입조사로서 당나라에 파견된 사신.
    '김직손': {'role': 'other'},  # 조선 - 조선 전기에, 정언, 한산군수, 사도시첨정 등을 역임한 문신.
    '김직재': {'role': 'other'},  # 조선 - 조선 후기에, 대 · 소북파 사이의 정쟁에 휘말려 아들 김백함과 함께 역모를 꾸민다는 누명
    '김진': {'role': 'other'},  # 조선 - 조선 후기에, 정언, 정주절제사, 예안현감 등을 역임한 문신.
    '김진갑': {'role': 'other'},  # 근대/일제강점기 | 현대 - 해방 이후 조선나전칠기공예조합의 이사장, 대한공예협회 회장 등을 역임한 공예가. 사업가.
    '김진걸': {'role': 'other'},  # 현대/대한민국 - 해방 이후 한국무용협회 이사 및 고문, 국립무용단 초대 지도 위원, 한성대학교 교수 등을 
    '김진구': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 좌참찬, 판의금부사 등을 역임한 문신.
    '김진규': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 대사성, 예조판서, 좌참찬 등을 역임한 문신.
    '김진균': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 「노래의 날개 위에」, 「금잔디」, 「그리움」 등을 만든 작곡가. 음악학자.
    '김진만': {'role': 'other'},  # 현대/대한민국 - 국회의원, 민주공화당 원내총무, 국회부의장 등을 역임한 정치인.
    '김진명': {'role': 'other'},  # 현대/대한민국 - 해방 이후 북한에서 전통 창법인 서도소리를 전승한 음악인. 작곡가.
    '김진묵': {'role': 'other'},  # 근대/대한제국기 - 대한제국기 때, 황해도 일대에서 항일의병투쟁을 전개하였으며, 국권 피탈 이후 광복단, 국민
    '김진민': {'role': 'scholar'},  # 근대/일제강점기 | 현대 - 일제강점기 「유란부」, 「독서락」, 「누실명」 등의 작품을 낸 서예가.
    '김진상': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 대사성, 대사헌, 좌참찬 등을 역임한 문신.
    '김진섭': {'role': 'essayist scholar novelist'},  # 근대 - 해방 이후 『인생예찬』, 『생활인의 철학』 등을 저술한 작가. 수필가, 독문학자.
    '김진성': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 경기도 양주군 광적면의 독립만세시위를 주도하는 과정에서 순국한 독립운동가.
    '김진수': {'role': 'playwright novelist'},  # 현대 - 해방 이후 「코스모스」, 「불더미 속에서」, 「이 몸 조국에 바치리」 등의 작품을 낸 극작
    '김진양': {'role': 'other'},  # 고려 - 고려 후기에, 우산기상시, 좌상시, 간관 등을 역임한 문신.
    '김진여': {'role': 'scholar'},  # 조선/조선 후기 - 조선후기 「기사계첩」, 「성적도」 등의 작품을 그린 화가.
    '김진옥': {'role': 'other'},  # 현대 - 해방 이후 「봉산탈춤」의 전승자로 지정된 예능보유자.
    '김진우': {'role': 'other'},  # 근대/일제강점기 | 현대 - 일제강점기 때, 임시의정원 강원도대표의원 등을 역임하며 항일투쟁을 전개하였으며, 「묵죽도」
    '김진종': {'role': 'other'},  # 조선 - 조선 전기에, 부응교, 헌납, 전적 등을 역임한 문신.
    '김진주': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 백제정벌군을 지휘한 장수.
    '김진준': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 독립청년단을 조직하여 친일파 처단활동을 전개하였고, 대한광복군 내무부 기밀
    '김진초': {'role': 'scholar'},  # 근대/대한제국기 - 대한제국기 『과수재배법』, 『아국농업론』 등을 저술한 학자. 농촌계몽운동가.
    '김진태': {'role': 'other'},  # 조선 - 조선후기 「입춘가(立春歌)」, 「진선가(眞仙歌)」 등을 노래한 음악인.
    '김진표': {'role': 'other'},  # 조선 - 조선 후기에, 청풍군수, 공조참의, 돈녕부도정 등을 역임한 문신.
    '김진하': {'role': 'scholar'},  # 조선 - 조선후기 동지중추부사로 『삼역총해』, 『신역소아론』, 『팔세아』 등을 저술한 역관.
    '김진형': {'role': 'other'},  # 현대/대한민국 - 해방 이후 한국은행 총재, 한국개발금융주식회사 사장 등을 역임한 금융인.
    '김진호': {'role': 'other'},  # 근대 - 일제강점기 때, 흥업단 재무부장, 국민부 중앙집행위원, 조선혁명당 중앙위원 등을 역임한 대
    '김진화': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 능주목사 등을 역임한 문신.
    '김진후': {'role': 'other'},  # 조선 - 조선후기 신해박해 당시의 순교자.
    '김진흥': {'role': 'other'},  # 조선/조선 후기 - 조선후기 「대학장구」 · 「전해심경」 등을 전서로 쓴 역관이자 서예가.
    '김질': {'role': 'scholar'},  # 조선/조선 전기 - 조선 전기에, 효행으로 알려져 명종에게 표창을 받았으며, 『영모록』, 『육사자책설』 등을 
    '김질간': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 대사간, 이조참판 등을 역임한 문신.
    '김질엽': {'role': 'other'},  # 근대 - 조선후기 「수궁가」로 널리 알려졌던 판소리의 명창.
    '김질충': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 도승지 등을 역임한 문신.
    '김집': {'role': 'scholar'},  # 조선 - 조선시대 이조판서, 좌참찬, 판중추부사 등을 역임한 문신. 학자.
    '김징': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 동부승지, 전라도관찰사 등을 역임한 문신.
    '김징악': {'role': 'other'},  # 고려/고려 전기 - 고려전기 다방태의소감를 역임한 의관.
    '김찬': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 대한독립군비단 참모장, 대한국민단 군사부장 등을 역임한 독립운동가.
    '김찬규': {'role': 'other'},  # 근대 - 일제강점기 때, 대동단 결성에 참여하였으며, 경상도 지방에 의용단을 조직해 군자금 모금 활
    '김찬수': {'role': 'other'},  # 근대 - 일제강점기 때, 북로군정서에서 김좌진 휘하의 제3중대장을 역임한 독립운동가.
    '김찬순': {'role': 'other'},  # 근대 - 대한제국기 때, 전기홍 의진에서 도통장으로 활동한 의병.
    '김찬식': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 「작품」, 「정」, 「희」 등의 작품을 낸 조각가.
    '김찬업': {'role': 'other'},  # 근대 - 조선후기 박만순과 김세종의 제자로 흥선대원군의 아낌을 받았던 판소리의 명창.
    '김찬영': {'role': 'scholar'},  # 근대/일제강점기 - 일제강점기 「자화상」 · 「님프의 죽음」 등의 작품을 그린 화가. 문장가.
    '김창': {'role': 'other'},  # 고려 - 고려 후기에, 문하평장사, 수태사 문하시랑평장사 판이부사 등을 역임한 문신.
    '김창곤': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 광복단 국내파견원으로 활동하며 친일파 처단 및 군자금 모금 활동을 전개한 
    '김창균': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 대한독립단, 대한통의부 의용군에서 항일무장투쟁을 전개한 독립운동가.
    '김창근': {'role': 'other'},  # 현대 - 제6·7·8·10대 국회의원, 민추협 부의장, 교통부장관 등을 역임한 정치인.
    '김창남': {'role': 'other'},  # 남북국시대 때, 이찬 관등으로, 당나라에 사신으로 파견된 통일신라의 귀족 · 관리.
    '김창도': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 경종대에 목호룡의 고변으로 발생한 옥사 때에 죽임을 당한 인물.
    '김창락': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 「추경」 · 「사양」 등의 작품을 그린 화가.
    '김창록': {'role': 'other'},  # 근대 - 조선후기 「심청가」에 뛰어났던 판소리의 명창.
    '김창룡': {'role': 'other'},  # 1920~1956. 군인.
    '김창석': {'role': 'other'},  # 조선/조선 후기 - 조선후기 호남균전관을 역임한 관리.
    '김창섭': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 한국 서양화가 1세대이자 골동품 수장가. 서양화가.
    '김창수': {'role': 'scholar'},  # 조선/조선 후기 - 조선후기 「춘산만하도」, 「송천독경도」 등의 작품을 그린 화가.
    '김창숙': {'role': 'scholar'},  # 현대/대한민국 - 일제강점기 때, 파리만국평화회의에 한국의 독립을 호소하는 진정서를 제출하였으며, 서로군정서
    '김창술': {'role': 'poet'},  # 현대/대한민국 - 일제강점기 「여명의 설움」, 「아-지금은 첫겨울」, 「문열어라」 등을 저술한 시인.
    '김창시': {'role': 'other'},  # 조선/조선 후기 - 조선후기 홍경래의 난을 주동한 관리.
    '김창식': {'role': 'other'},  # 근대 - 일제강점기, 한국인 최초의 목사이자 한국 기독교 초기 전도인.
    '김창업': {'role': 'novelist'},  # 조선/조선 후기 - 조선후기 「추강만박도」 · 「우암송선생칠십사세진」 등의 작품을 그린 화가. 문인.
    '김창오': {'role': 'other'},  # 근대 - 대한제국기 때, 박기섭 의진에서 돌격장으로 활동한 의병장.
    '김창원': {'role': 'other'},  # 현대 - 해방 이후 주한튀니지 명예총영사, 신진학원 이사장 등을 역임한 경제인.
    '김창일': {'role': 'other'},  # 조선 - 조선 후기에, 동지중추부사 등을 역임한 문신.
    '김창조': {'role': 'other'},  # 조선/조선 후기 - 조선후기 「김창조가락 가야금산조」를 지은 거문고명인.
    '김창주': {'role': 'other'},  # 현대/대한민국 - 북한에서, 최고인민회의 대의원, 정무원 부총리 겸 농업위원장 등을 역임한 관료.
    '김창준': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「고성오광대」 전승자로 지정된 기예능보유자.
    '김창즙': {'role': 'scholar'},  # 조선 - 조선후기 왕자사부, 예빈시주부 등을 역임한 문신. 학자.
    '김창직': {'role': 'scholar'},  # 조선/조선 후기 - 조선 후기에, 사서, 문학 등을 역임한 문신.
    '김창집': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 우의정, 좌의정, 영의정 등을 역임한 문신.
    '김창하': {'role': 'other'},  # 조선/조선 후기 - 조선후기 가전악, 전악, 집박악사 등을 역임한 음악인.
    '김창학': {'role': 'other'},  # 현대 - 해방 이후 대한해협 해전 당시의 군인.
    '김창헌': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 통의부 헌병대장, 정의부 헌병대장, 조선혁명군 제4중대장 등을 역임한 군인
    '김창현': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 조선독립단 황해도 지부를 조직하여 동지규합, 군자금 모금 활동 등을 전개한
    '김창협': {'role': 'other'},  # 조선 - 조선 후기에, 병조참지, 예조참의, 대사간 등을 역임한 문신.
    '김창환': {'role': 'other'},  # 근대/개항기 | 근대/일제강점기 - 일제강점기 「송월학명」 · 「봉학도」 등을 그린 화가.
    '김창후': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「고성오광대」의 전승자로 인정된 예능보유자.
    '김창흡': {'role': 'scholar'},  # 조선 - 조선 후기에, 『삼연집』, 『심양일기』 등을 저술한 학자.
    '김창희': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 사헌부대사헌, 홍문관제학, 예문관제학 등을 역임한 문신.
    '김채만': {'role': 'other'},  # 근대 - 대한제국기 이날치의 제자로 창극단과 협률사에 참여한 판소리의 명창.
    '김채옥': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「진주검무」의 전승자로 지정된 예능보유자.
    '김처선': {'role': 'other'},  # 조선/조선 전기 - 조선전기 자헌대부를 역임한 환관.
    '김처암': {'role': 'other'},  # 조선 - 조선 후기에, 집의 등을 역임한 문신.
    '김처회': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 병부시랑, 납정절사 등을 역임한 관리.
    '김척명': {'role': 'novelist'},  # 고대/남북국/통일신라 - 남북국시대 통일신라에서 원광, 비허 등의 불교 사적을 정리한 문인.
    '김척후': {'role': 'other'},  # 고려 - 고려 후기에, 장군, 대장군, 초토처치병마중도사 등을 역임한 문신.
    '김천': {'role': 'other'},  # 고려/고려 후기 - 고려후기 몽고의 제6차 침입 당시 몽고군에게 포로로 잡혀간 모친을 구한 효자. 향리.
    '김천경': {'role': 'other'},  # 고려 - 고려 후기에, 중랑장 등을 역임한 무신 · 공신.
    '김천령': {'role': 'other'},  # 조선 - 조선 전기에, 집의 등을 역임한 문신.
    '김천록': {'role': 'other foreigner'},  # 고려 - 고려후기 삼별초의 난, 여몽연합군 일본정벌 등과 관련된 무신.
    '김천보': {'role': 'other'},  # 고려 - 고려 후기에, 동지밀직사사, 대사헌, 판도판서 등을 역임한 문신.
    '김천석': {'role': 'other'},  # 조선 - 조선 후기에, 군수 등을 역임한 문신.
    '김천성': {'role': 'other foreigner'},  # 근대 - 일제강점기 때, 중국에서 광복군 제5지대 간부 등을 역임하며 항일무장투쟁을 전개한 독립운동
    '김천수': {'role': 'other'},  # 근대 - 조선 후기에, 경주군수, 비서승, 규장각기주관 등을 역임한 문신.
    '김천애': {'role': 'other'},  # 현대/대한민국 - 해방 이후 경성음악학교 교수, 숙명여자대학교 성악과 교수 및 학장 등을 역임한 음악인. 성
    '김천익': {'role': 'other'},  # 근대 - 일제강점기 때, 만주에서 한족회, 대한독립군 등에 가담하여 항일무장투쟁을 전개한 독립운동가
    '김천일': {'role': 'other'},  # 조선 - 조선 중기에, 임진왜란이 발발하자 의병을 일으켜 군사활동을 전개하였으며, 수원부사, 장례원
    '김천존': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 삼국통일전쟁에 참전한 장수. 대신.
    '김천택': {'role': 'novelist'},  # 조선/조선 후기 - 조선후기 『청구영언』을 편찬한 가객. 시조작가.
    '김천흥': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 이왕직 아악부 아악수, 아악수장 등을 역임한 국악인.
    '김철': {'role': 'other'},  # 현대/대한민국 - 민족일보 논설위원, 통일사회당 대통령 후보 등을 역임한 정치인.
    '김철규': {'role': 'other'},  # 현대/대한민국 - 해방 이후 서울교구장 비서, 서울대교구 부주교(현 총대리) 등에 서임된 사제. 신부.
    '김철남': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 임시의정원 황해도 대표의원, 임시정부 교통부차장, 참모차장 등을 역임한 독
    '김철산': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 건설자동맹, 고려공산청년동맹 등에서 사회주의 운동을 전개하다가 제1차 간도
    '김철수': {'role': 'other'},  # 근대 - 일제강점기 때, 2·8독립선언을 주도하였으며, 조선청년회연합회 상무위원, 조선물산장려회 경
    '김철준': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 「한국고대사회 연구」, 「한국문화사론」, 「한국문화전통론」 등을 저술한 학자. 
    '김철훈': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 러시아공산당 한인지부 위원장, 전로한인공산당 위원장 등을 역임한 사회주의운동가.
    '김철희': {'role': 'other'},  # 근대 - 대한제국기 때, 경모궁제조, 궁내부특진관 등을 역임한 문신.
    '김첨': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 교리 등을 역임한 문신.
    '김첨경': {'role': 'other'},  # 조선 - 조선 전기에, 예조판서 등을 역임한 문신.
    '김첨수': {'role': 'other'},  # 고려 - 고려 후기에, 충혜왕이 원나라에 억류당했을 때 호종한 무신 · 공신.
    '김청': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 대사간 등을 역임하다 낙향하였으나 임진왜란이 발발하자 왕의 호위를 자청한 문
    '김청평': {'role': 'other foreigner'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 사찬으로 일본에 파견된 관리.
    '김체': {'role': 'other'},  # 고려 - 고려 후기에, 순안현령 등을 역임한 문신.
    '김체명': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 제39대 소성왕의 아들인 왕자.
    '김체신': {'role': 'other'},  # 고대/남북국/통일신라 - 신라 경덕왕, 혜공왕, 선덕왕 때 중앙 행정과 대일 외교 및 군사 분야에서 활약한 관료.
    '김초': {'role': 'other'},  # 고려 - 고려 후기에, 안동판관, 충청도안렴사, 성균박사 등을 역임한 문신.
    '김초정': {'role': 'other foreigner'},  # 고대/남북국/통일신라 - 남북국시대 통일신라에서 급찬으로서 일본에 파견된 사신.
    '김총': {'role': 'scholar'},  # 조선 - 조선후기 집의, 지제교, 옥구현감 등을 역임한 문신. 학자.
    '김최명': {'role': 'other foreigner'},  # 근대 - 일제강점기 때, 대한독립단과 광복군총영의 결사대원으로 활동하며 일제 기관 파괴 및 일본 고
    '김추월': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 이동백, 신금홍과 일본 와시표축음기에 춘향전 전집을 취입한 판소리의 명창.
    '김춘광': {'role': 'playwright novelist'},  # 근대/일제강점기 - 일제강점기 「검사와 여선생」, 「촌색시」 등의 작품을 낸 극작가.
    '김춘배': {'role': 'other'},  # 근대 - 일제강점기 때, 정의부에서 군자금 모금 활동을 전개한 독립운동가.
    '김춘수': {'role': 'novelist'},  # 해방 이후 『구름과 장미』, 『타령조 기타』, 『거울 속의 천사』 등을 저술한 문인.
    '김춘영': {'role': 'other'},  # 근대/개항기 - 개항기 임오군란 당시의 군인.
    '김춘지': {'role': 'other'},  # 현대 - 해방 이후 가야금산조 및 병창의 전승자로 지정된 예능보유자. 가야금연주자.
    '김춘질': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 신문왕이 감은사 창건 시 일관을 역임한 관리.
    '김춘택': {'role': 'scholar'},  # 조선/조선 후기 - 조선 후기에, 『북헌집』, 『만필』 등을 저술한 문신.
    '김춘희': {'role': 'other'},  # 근대/개항기 | 근대/일제강점기 - 일제강점기 성균관 대사성, 이조 참의, 이조 참판, 도승지, 황해도 관찰사 등을 역임한 관
    '김충': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 선공감정, 사성, 초계군수 등을 역임한 문신.
    '김충간': {'role': 'other'},  # 고려 - 고려 전기에, 병마녹사를 역임한 문신.
    '김충공': {'role': 'other'},  # 고대/남북국/통일신라 - 통일신라의 제44대 민애왕의 아버지로, 집사부시중, 상대등 등을 역임하였으며, 민애왕 즉위
    '김충렬': {'role': 'other'},  # 조선 - 조선시대 효행으로 정려와 예물을 하사받은 효자.
    '김충복': {'role': 'other'},  # 현대/대한민국 - 현대, 한국 제과 · 제빵업 발전에 기여한 공로자.
    '김충선': {'role': 'other'},  # 조선 - 조선시대 가선대부, 자헌대부, 정헌대부 등을 역임한 무신.
    '김충신': {'role': 'other'},  # 고대/남북국/통일신라 - 통일신라의 제33대 성덕왕의 사촌동생으로, 당나라에 사신으로 가서 발해 토벌을 요청하였으며
    '김충의': {'role': 'other'},  # 고려 - 고려후기 제26대 충선왕 때 악행으로 참형을 당한 관리.
    '김충찬': {'role': 'other'},  # 고려 - 고려 전기에, 우산기상시, 지충추원사 병부상서 등을 역임한 문신.
    '김충평': {'role': 'other foreigner'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 일길찬으로 일본에 파견된 관리.
    '김충현': {'role': 'scholar'},  # 현대 - 해방 이후 「윤봉길 열사 기의비」 · 「백범 김구 선생 묘비」 · 「사육신 묘비」 등의 작
    '김취기': {'role': 'other'},  # 고려 - 고려후기 호군, 군부판서 응양군 상호군 등을 역임한 무신.
    '김취려': {'role': 'other'},  # 고려/고려 후기 - 고려후기 평장사 판병부사, 평장사 판이부사, 문하시중 등을 역임한 무신.
    '김취로': {'role': 'other'},  # 조선 - 조선 후기에, 호조판서를 역임한 문신.
    '김취문': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 교리, 호조참의, 대사간 등을 역임한 문신.
    '김취성': {'role': 'scholar'},  # 조선 - 조선 전기에, 『진락당집』을 저술하였으며, 의학 연구를 통해 환자 치료에 힘쓴 학자.
    '김치': {'role': 'other'},  # 조선 - 조선 후기에, 경상도관찰사 등을 역임한 문신.
    '김치관': {'role': 'scholar'},  # 조선 - 조선 중기에, 벼슬에 뜻을 두지 않고 의성향교에서 후진 양성에 힘쓰며, 『역락재집』을 저술
    '김치룡': {'role': 'other'},  # 조선 - 조선 후기에, 승지 등을 역임한 문신.
    '김치만': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 동몽교관, 시직 등을 역임한 문신.
    '김치보': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 러시아 연해주 블라디보스토크로 망명하여 성명회, 권업회, 대한국민의회 등에서 활
    '김치선': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 서울대학교 법학연구소 소장, 서울대학교 법과대학 학장 등을 역임한 학자. 법학자
    '김치양': {'role': 'other'},  # 고려/고려 전기 - 고려 전기 목종대에 반란을 일으킨 권신.
    '김치열': {'role': 'other'},  # 현대/대한민국 - 검찰총장, 법무부장관, 중앙정보부 차장 등을 역임하며 박정희 정부에서 핵심 세력으로 활동한
    '김치영': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 『중학교 수학』, 『고교수학』, 『미분적분학』 등을 저술한 학자. 수학자.
    '김치운': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 장악원정, 봉상시정 등을 역임한 문신.
    '김치인': {'role': 'other'},  # 근대/개항기 - 개항기 일수 이복래를 교주로 추대하여 오방불교를 창립한 종교창시자.
    '김치정': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 재중국본부한인청년동맹, 무산자사, 노동계급사 등에서 활동한 사회주의운동가, 독립
    '김치홍': {'role': 'other'},  # 근대 - 대한제국기 때, 심남일 의진에서 기군장으로 활동한 의병.
    '김치후': {'role': 'other'},  # 조선 - 조선 후기에, 대사간, 정주목사 등을 역임한 문신.
    '김칠성': {'role': 'other'},  # 현대/대한민국 - 일제강점기 때, 김천청년연맹 집행위원, 부산청년동맹 집행부에서 활동하며 독립운동 자금 지원
    '김타업': {'role': 'other'},  # 현대/대한민국 - 국가무형문화유산 밀양 백중놀이의 상쇠 부문 보유자로 인정된 악사이자 밀양 지역의 상례 의식
    '김탄행': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 첨지중추부사를 역임한 문신.
    '김탕': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 파리강화회의에 참석하기 위해 대한민국임시정부 대표로 파견되어 외교활동을 벌
    '김태곤': {'role': 'scholar'},  # 현대/대한민국 - 원광대학교와 경희대학교의 교수로 재임하여 민속학연구소장 등을 역임하였으며, 『한국민간신앙연
    '김태균': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 간도 용정촌에서 전개된 독립만세시위를 주도하는 과정에서 순국한 독립운동가.
    '김태기': {'role': 'other'},  # 조선 - 조선 후기에, 영광군수를 역임한 문신.
    '김태동': {'role': 'other'},  # 현대/대한민국 - 경제기획원 차관, 체신부 · 보건사회부 장관 등을 역임한 관료 · 친일반민족행위자.
    '김태렴': {'role': 'other foreigner'},  # 고대/남북국/통일신라 - 통일신라 경덕왕 때, 대규모 사절단을 이끌고 일본에 방문한 왕족.
    '김태서': {'role': 'other'},  # 고려 - 고려 후기에, 한림학사, 문하시랑평장사 등을 역임한 문신.
    '김태석': {'role': 'other'},  # 근대/일제강점기 - 대한제국기 「승사인보」 · 「청유인보」 등을 제작한 서예가. 전각가.
    '김태선': {'role': 'other'},  # 현대/대한민국 - 해방 이후 내무부치안국장, 서울시장, 내무부장관 등을 역임한 관료.
    '김태섭': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「종묘제례악」 전승자로 지정된 기예능보유자.
    '김태수': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 및 8·15광복 후 충청북도 영동 지역애서 활동한 사회주의운동가.
    '김태숙': {'role': 'other'},  # 근대/일제강점기 | 현대 - 해방 이후 한국자수협회 회장을 역임한 공예가. 자수공예가.
    '김태식': {'role': 'other'},  # 근대 - 해방 이후 서울대학교 체육담당 교수, 대한수상경기연맹 부회장 등을 역임한 체육인. 교육자.
    '김태암': {'role': 'other'},  # 조선 - 조선 후기에. 찰방 등을 역임한 무신 · 공신.
    '김태연': {'role': 'other'},  # 근대 - 일제강점기 때, 대한통의부 국내파견 결사대장으로 활동하였고, 정의부, 신민부 등에서 항일투
    '김태영': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 국내에서 활동한 사회주의운동가.
    '김태오': {'role': 'poet childrenauthor scholar'},  # 현대/대한민국 - 일제강점기 「새벽」, 「소리소리 무슨 소리」, 「가을하늘 휘파람」 등을 저술한 시인. 아동
    '김태운': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 경기민요와 잡가로 활약한 경기소리의 명창.
    '김태원': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 때, 벽창의용단을 조직하여 군자금 모금, 일본경찰 및 밀정 처단 등의 항일투쟁을
    '김태일': {'role': 'scholar'},  # 조선 - 조선 후기에, 문학, 보덕, 사간 등을 역임한 문신.
    '김태정': {'role': 'other'},  # 조선 - 조선 전기에, 진사, 전라도관찰사 등을 역임한 문신.
    '김태제': {'role': 'other'},  # 근대 - 조선 후기에, 사직서제조, 비서원승, 태의원경 등을 역임한 문신.
    '김태준': {'role': 'scholar'},  # 근대 - 일제강점기 『조선한문학사』, 『조선소설사』, 『조선가요집성』 등을 저술한 학자. 사상가.
    '김태진': {'role': 'playwright novelist'},  # 근대/일제강점기 - 일제강점기 「개척자」, 「풍운아」, 「낙원을 찾는 무리들」 등에 출연한 배우. 극작가, 연
    '김태허': {'role': 'other'},  # 조선 - 조선 중기에, 밀양부사, 울산군수, 당상관, 지중추부사 등을 역임한 무신 · 공신.
    '김태현': {'role': 'other'},  # 고려 - 고려 후기에, 평장사, 상서우승, 첨의정승 등을 역임한 문신.
    '김태호': {'role': 'other'},  # 현대/대한민국 - 해방 이후 경기도지사, 국회의원 등을 역임한 정치인. 관료.
    '김태홍': {'role': 'poet'},  # 현대/대한민국 - 해방 이후 『땀과 장미와 시』ㆍ『공』ㆍ『훗날에도 가을에는』 등을 저술한 시인.
    '김태희': {'role': 'other'},  # 근대/일제강점기 | 현대 - 해방 이후 「칠장」 전승자로 지정된 기능보유자. 나전칠기명인.
    '김택': {'role': 'other'},  # 조선 - 조선 전기에, 학유, 박사, 감찰 등을 역임한 문신.
    '김택규': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 『동족부락의 생활구조연구』, 『한국민속문예론』 등을 저술한 학자. 문화인류학자.
    '김택룡': {'role': 'other'},  # 조선 - 조선 중기에, 전적, 도사 등을 역임한 문신.
    '김택수': {'role': 'other'},  # 현대/대한민국 - 해방 이후 국민체육진흥재단 이사장, 국제올림픽위원회 위원 등을 역임한 체육인. 정치인.
    '김택술': {'role': 'other'},  # 현대/대한민국 - 대한노총연맹 전라북도 부위원장, 제2·3대 국회의원 등을 역임한 정치인.
    '김택영': {'role': 'scholar'},  # 근대 - 조선 후기부터 일제강점기를, 살아가며 우리나라 역사 서술 및 한문학 유산 정리에 힘쓴 학자
    '김택현': {'role': 'other'},  # 현대/대한민국 - 해방 이후 대한변호사협회 회장, 공직자윤리위원회 위원 등을 역임한 법조인.
    '김토': {'role': 'other'},  # 조선/조선 전기 - 조선전기 전의주부, 전의감승 등을 역임한 의관.
    '김통': {'role': 'other'},  # 조선 - 조선 전기에, 정언, 성균관직강, 예조정랑 등을 역임한 문신.
    '김통정': {'role': 'other'},  # 고려/고려 후기 - 고려후기 진도의 삼별초의 항쟁과 관련된 무신.
    '김판술': {'role': 'other'},  # 현대/대한민국 - 농림부 농정과 과장, 농민부 차장, 민의원, 보건사회부장관, 국회의원 등을 역임한 정치인.
    '김팔원': {'role': 'other'},  # 조선 - 조선 전기에, 전적, 예조좌랑, 용궁현감 등을 역임한 문신.
    '김평': {'role': 'other'},  # 고려 - 고려 후기에, 국자대사성, 추밀원 부사, 추밀원사 등을 역임한 문신.
    '김평묵': {'role': 'scholar'},  # 근대 - 조선 후기에, 『중암선생문집』, 『구곡문답』, 『척양대의』 등을 저술한 학자.
    '김평손': {'role': 'novelist'},  # 조선 - 조선시대 강변칠우에 속한 문인.
    '김평식': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 대한독립단 총무부장, 의군부 정무총감 등을 역임한 독립운동가.
    '김포질': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라에서 사찬으로서 당나라에 파견된 사신.
    '김표석': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 때, 이찬 관등으로 당나라에 파견된 통일신라의 관리.
    '김품석': {'role': 'other'},  # 고대/삼국/신라 - 신라의 제29대 왕, 태종 무열왕의 사위로, 대야성군주를 역임하여 백제의 침입에 대응하고자
    '김풍나': {'role': 'other foreigner'},  # 고대/남북국/통일신라 - 남북국시대 통일신라에서 일본에 사신으로 다녀온 왕자 충원(忠元)의 호송원.
    '김풍익': {'role': 'other'},  # 현대 - 한국전쟁 당시 경기도 이천의 의정부지역전투에 참전한 군인.
    '김풍후': {'role': 'other'},  # 남북국시대 통일신라의 하정사로 당나라에 파견된 관리.
    '김풍훈': {'role': 'scholar'},  # 고대/남북국/통일신라 - 남북국시대 때, 숙위학생으로 당나라에서 유학하다가 아버지의 처형 소식을 듣고 당나라 군사의
    '김필': {'role': 'other foreigner'},  # 남북국시대 통일신라의 사찬으로 일본에 파견된 관리.
    '김필덕': {'role': 'other foreigner'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 일길찬으로 일본에 파견된 관리.
    '김필례': {'role': 'other'},  # 근대 - 해방 이후 정신여자중학교 교장, 정신학원 이사장 등을 역임한 교육자. 지도자.
    '김필순': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 만주에서 독립운동가 주치의로 활동하며 독립군을 치료하고, 병원 수입을 독립
    '김필월': {'role': 'novelist'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 「성덕대왕신종명」을 지은 문인.
    '김필진': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 평시서령, 원성현감 등을 역임한 문신.
    '김하': {'role': 'other'},  # 조선 - 조선 전기에, 공조판서를 역임한 문신.
    '김하건': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 일본의 미술문화협회 회원으로 활동한 화가. 서양화가.
    '김하구': {'role': 'scholar'},  # 근대 - 해방 이후 「고대문화사」, 「세계문화사」 등을 저술한 학자. 역사학자.
    '김하득': {'role': 'other'},  # 현대/대한민국 - 해방 이후 부산교육대학 초대학장, 부산시교육회 회장 등을 역임한 교육자.
    '김하락': {'role': 'other'},  # 근대/개항기 - 개항기 때, 이천에서 의병을 일으켜 각 군 도지휘, 군사 겸 지휘 등으로 활동한 의병.
    '김하명': {'role': 'other'},  # 조선 - 조선 후기에, 용양위부호군, 돈녕부도정 등을 역임한 문신.
    '김하석': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 대한국민의회의 군정부장, 임시고려혁명군정의회 의장 등을 역임한 사회주의운동가.
    '김하재': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 대사헌, 동지경연사, 이조참판 등을 역임한 문신.
    '김하정': {'role': 'scholar'},  # 조선 - 조선 후기에, 춘추관편수관, 예조정랑, 영해부사 등을 역임하였으며, 『제례질의』, 『선집록
    '김하종': {'role': 'scholar'},  # 조선 - 조선후기 「장안사」 · 「철종철인후가례도감의궤도」 등의 작품을 그린 화가.
    '김학규': {'role': 'other'},  # 근대 - 일제강점기 때, 조선혁명당 군사령부참모장, 조선민족혁명당 국민부장, 한국광복군 총사령참모 
    '김학기': {'role': 'other'},  # 조선 - 조선 전기에, 집의, 사옹원정, 대제학 등을 역임한 문신.
    '김학렬': {'role': 'other'},  # 현대/대한민국 - 해방 이후 재무부장관, 대통령수석정무비서관, 경제기획원 장관 등을 역임한 관료. 행정가, 
    '김학무': {'role': 'other'},  # 근대 - 일제강점기 때, 조선의용대 지도위원, 화북조선독립동맹 선전부 부장, 화북조선청년혁명학교 교
    '김학배': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 예조좌랑, 성균관교정관 등을 역임한 문신.
    '김학섭': {'role': 'other'},  # 근대 - 일제강점기 때, 대한독립군결사대를 조직하여 항일무장투쟁을 전개한 독립운동가.
    '김학성': {'role': 'scholar'},  # 근대 - 해방 이후 「새로운 맹세」 · 「오발탄」 · 「아리랑」 등의 작품에 관여한 영화인. 영화촬
    '김학수': {'role': 'other'},  # 근대/일제강점기 | 현대 - 해방 이후 「삼강행실도」 · 「능행도」 · 「한강전도」 등을 그린 화가. 한국화가 · 역사
    '김학순': {'role': 'other foreigner'},  # 현대/대한민국 - 대한민국의 여성운동가로, 1991년 일본군 위안부 피해 사실을 한국인 최초로 공개 증언한 
    '김학연': {'role': 'other'},  # 근대/일제강점기 - 일제강점기, 북간도 명동학교의 교원으로 활동한 교육자.
    '김학우': {'role': 'other'},  # 근대 - 개항기 전운서낭청, 내무부참의직, 법무아문대신서리 등을 역임한 관료.
    '김학준': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 「소녀」, 「하코네 풍경」, 「바다」 등을 그린 화가. 서양화가.
    '김학진': {'role': 'other'},  # 근대/개항기 | 근대/일제강점기 - 일제강점기 홍문관 학사, 궁내부 특진관, 시종원경 등을 역임한 관료. 친일반민족행위자.
    '김학철': {'role': 'novelist'},  # 현대 - 해방 이후 연변에서 『격정시』 · 『해란강아 말하라』 등을 저술한 소설가.
    '김한': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 상하이 대한민국임시정부 사법부장, 무산자동지회 상무위원 등을 역임한 사회주의운동
    '김한계': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 승문원교리, 승정원부승지, 정언 등을 역임한 문신.
    '김한구': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 영조의 장인으로 어영대장을 지낸 문신.
    '김한귀': {'role': 'other'},  # 고려 - 고려후기 동경도병마사, 감찰대부 등을 역임한 무신.
    '김한기': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 지중추부사 등을 역임한 문신.
    '김한동': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 대사간, 승지 등을 역임한 문신.
    '김한로': {'role': 'other'},  # 조선 - 조선 전기에, 판한성부사, 예조판서, 의정부찬성 등을 역임한 문신.
    '김한록': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 세자익위사세마를 역임한 문신.
    '김한룡': {'role': 'other'},  # 고려 - 고려 후기에, 전첨, 판전교시사 등을 역임한 문신 · 공신.
    '김한섭': {'role': 'scholar'},  # 조선 - 조선 후기에, 「통화변답, 「농정신서서조변」, 『오남문집』 등을 저술한 학자.
    '김한수': {'role': 'other'},  # 현대 - 해방 이후 중앙합성섬유주식회사, 한일합성섬유주식회사 등을 설립한 실업가.
    '김한신': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 오위도총부총관, 제용감제조 등을 역임한 문신.
    '김한종': {'role': 'other'},  # 근대 - 일제강점기 때, 대한광복회를 조직하여 군자금을 모금하고 친일파를 처단하는 등 항일무장투쟁을
    '김한진': {'role': 'other'},  # 고려 - 고려 후기에, 순성보절공신, 호종일등공신, 경성수복일등공신 등에 책록된 문신 · 공신.
    '김한철': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 함경도관찰사, 대사헌, 우참찬 등을 역임한 문신.
    '김한충': {'role': 'other'},  # 고려 - 고려 전기에, 중군병마사, 추밀원사, 상서좌복야 등을 역임한 문신.
    '김함': {'role': 'other'},  # 고려/고려 전기 - 고려 전기에, 어서검토관, 지호부사, 호부상서 등을 역임한 문신.
    '김항': {'role': 'scholar'},  # 근대 - 조선 후기에, 『주역』을 풀이하여 한국식으로 체계화한 역학의 대가로, 『정역』을 주창한 학
    '김항나': {'role': 'other foreigner'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 아찬으로서 일본에 파견된 사신.
    '김해': {'role': 'other'},  # 조선 - 조선 중기에, 승문원정자, 예문관검열 등을 역임하였으며, 임진왜란이 발발하자 영남의병대장으
    '김해강': {'role': 'poet'},  # 현대 - 해방 이후 『동방서곡』, 『기도하는 마음』 등을 저술한 시인.
    '김해랑': {'role': 'other'},  # 현대 - 해방 이후 한국무용예술인협회 초대 이사장 및 회장을 역임한 무용가. 한국무용가.
    '김해성': {'role': 'other foreigner'},  # 근대 - 일제강점기 때, 중국에서 한국청년전지공작대에 입대하여 정보 수집, 초모공작 등의 활동을 전
    '김해송': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 「연락선은 떠난다」 · 「잘있거라 단발령」 등을 부른 가수. 작곡가.
    '김해수': {'role': 'other'},  # 조선 - 조선 후기에, 제용감직장, 현감 등을 역임한 문신.
    '김해일': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 승지, 경주부윤 등을 역임한 문신.
    '김행': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 광주목사 등을 역임한 문신.
    '김행경': {'role': 'other'},  # 고려 - 고려 전기에, 판상서병부사, 문하시랑동중서문하평장사 등을 역임한 문신.
    '김행공': {'role': 'other'},  # 고려 - 고려 전기에, 거란 흥종의 즉위를 축하하는 사신으로 파견된 문신.
    '김행도': {'role': 'other'},  # 고려 - 고려 전기에, 광평시중, 동남도초토사, 지아주제군사 등을 역임한 문신.
    '김행파': {'role': 'other'},  # 고려 - 고려전기 대광을 역임한 호족.
    '김향': {'role': 'other'},  # 고려/고려 전기 - 고려 전기에, 검교태위수사공, 참지정사 등을 역임한 문신.
    '김헌경': {'role': 'other'},  # 근대 - 대한제국기 때, 관동의진에서 창의대장으로 활동한 의병장.
    '김헌기': {'role': 'scholar'},  # 조선 - 조선 후기에, 『논어설』, 『초암집』, 『충서설』 등을 저술한 학자.
    '김헌장': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 때, 진위사로 당나라에 파견된 통일신라의 왕족.
    '김헌정': {'role': 'other'},  # 고대/남북국/통일신라 - 통일신라의 제43대 희강왕의 아버지로, 시중, 국상, 병부령 겸 수성부령 등을 역임한 왕족
    '김헌창': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 시중, 청주도독, 웅주도독 등을 역임한 귀족. 반란자.
    '김헌충': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 때, 시비서감 등을 역임하였으며, 숙위로 당나라에 파견된 통일신라의 왕족.
    '김혁': {'role': 'other'},  # 근대 - 일제강점기에 만주에서 흥업단 부단장 · 대한독립군단 군사부장 · 신민부 중앙집행위원장 · 
    '김혁정': {'role': 'other'},  # 고려/고려 후기 - 고려후기 야별초지유, 충청도안찰사 등을 역임한 관리. 무신.
    '김현': {'role': 'critic scholar foreigner'},  # 현대/대한민국 - 해방 이후 『프랑스 비평사』, 『문학사회학』 등을 저술한 학자. 문학평론가.
    '김현구': {'role': 'poet'},  # 근대 - 일제강점기 「거룩한 봄과 슬픈 봄」, 「풀 우에 누워」, 「내마음 사는 곳」 등을 저술한 
    '김현기': {'role': 'other'},  # 현대/대한민국 - 제7~10대 국회의원, 신민당 중앙상임위원 등을 역임한 정치인.
    '김현도': {'role': 'other'},  # 조선 - 조선 중기에, 해주목사, 양재찰방 등을 역임한 문신.
    '김현배': {'role': 'other'},  # 현대/대한민국 - 1947년에서 1960년까지, 제3대 전주교구장으로 사목한 천주교 사제.
    '김현보': {'role': 'other'},  # 고려/고려 후기 - 고려후기 최우의 심복으로 상장군을 역임한 관리. 무신.
    '김현성': {'role': 'other'},  # 조선 - 조선시대 봉상시주부, 양주목사, 동지돈녕부사 등을 역임한 서화가.
    '김현숙': {'role': 'other'},  # 현대/대한민국 - 해방 이후 육군본부 여군부장, 여군훈련소 소장, 대령 등을 역임한 군인.
    '김현승': {'role': 'poet'},  # 현대/대한민국 - 광복 이후 『김현승시초』, 『옹호자의 노래』, 『견고한 고독』등을 저술한 시인.
    '김현옥': {'role': 'other'},  # 현대/대한민국 - 육군제3항만사령관, 서울시장, 내무부장관 등을 역임한 군인 · 정치인.
    '김현우': {'role': 'scholar'},  # 조선/조선 후기 - 조선후기 「연파고주도」, 「신선도」 등의 작품을 그린 화가.
    '김현일': {'role': 'other'},  # 현대/대한민국 - 해방 이후 고성지구 근접항공지원작전 당시의 군인.
    '김현준': {'role': 'scholar'},  # 근대/일제강점기 | 현대 - 한국의 첫 신문학 박사로, 성균관대학교 학장과 조선대학교 문리학부장 등을 역임하였으며, 『
    '김현철': {'role': 'other'},  # 현대/대한민국 - 재무부장관, 경제기획원장관, 주미대사 등을 역임한 관료 · 외교관.
    '김현태': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 『판례, 학설주석민법』, 『민법총칙』, 『불법행위론』 등을 저술한 학자. 법학자
    '김형규': {'role': 'scholar'},  # 해방 이후 『국어학개론』, 『국어사』, 『한국방언연구』 등을 저술한 학자. 국어학자.
    '김형근': {'role': 'other'},  # 현대 - 해방 이후 대검찰청검사, 서울지방검찰청 검사장, 중앙선거관리위원 헌법위원회 헌법위원 등을 
    '김형남': {'role': 'other'},  # 현대/대한민국 - 해방 이후 숭실대학교 초대 총장 , 이사장 등을 역임한 교육자.
    '김형래': {'role': 'other'},  # 현대/대한민국 - 일제강점기 「맹강녀」 · 「카추샤」 · 「가면무도회」 등을 만든 작곡가.
    '김형렬': {'role': 'other'},  # 근대 - 일제강점기 금산사에 미륵불교를 설립한 종교창시자.
    '김형빈': {'role': 'other foreigner'},  # 근대 - 일제강점기 때, 중국에서 독립단에 입단하여 군자금 모금 활동을 전개한 독립운동가.
    '김형선': {'role': 'other'},  # 근대 - 해방 이후 조선인민공화국 경제부장 대리, 남조선노동당 중앙감찰위원회 부위원장 등을 역임한 
    '김형섭': {'role': 'other'},  # 근대 - 대한제국기 혁명일심회 사건 당시의 군인.
    '김형순': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 미국에서 대한인국민회를 중심으로 독립운동을 후원한 기업인.
    '김형욱': {'role': 'other'},  # 국가재건최고회의 최고위원, 중앙정보부장 등을 역임하며 박정희 체제 유지에 결정적인 역할을 
    '김형원': {'role': 'poet'},  # 근대/일제강점기 - 일제강점기 「이향」, 「아 지금은 새벽 네시」, 「불순의 피」 등을 저술한 시인. 언론인.
    '김형익': {'role': 'other'},  # 근대/일제강점기 | 현대 - 해방 이후 대한적십자사 서울지사장, 대한나관리협회 이사 등을 역임한 의사.
    '김형일': {'role': 'other'},  # 현대/대한민국 - 연합참모본부장, 국방부장관 특별보좌관, 국회의원 등을 역임한 군인 · 정치인.
    '김형재': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 동흥학교 교원, 대동공보 하얼빈지국장 등을 역임하였으며, 안중근의 의거에 
    '김형준': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 「봉선화」 · 「저 구름의 탓」 · 「나물 캐는 처녀」 등을 작사한 음악인. 교
    '김형직': {'role': 'other'},  # 현대/대한민국 - 북한의 통치자 김일성의 아버지로 북한에서는 일제강점기 비밀결사단체인 조선국민회에 가입하여 
    '김혜손': {'role': 'scholar'},  # 조선/조선 전기 - 조선 전기에, 군수 등을 역임한 학자.
    '김호': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 만주와 러시아 연해주에서 활동하며 대한독립단, 광정단, 정의부 등에서 무장투쟁을
    '김호길': {'role': 'scholar'},  # 현대 - 포항공과대학의 설립을 주도하며 한국의 과학교육에 힘쓴 물리학자 · 교육자.
    '김호룡': {'role': 'scholar foreigner'},  # 근대/일제강점기 - 일제강점기 일본식 외광파(外光派)의 영향을 강하게 드러낸 작품을 그린 화가. 서양화가.
    '김호반': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 경상남도 지역을 기반으로 사회주의운동을 전개한 독립운동가.
    '김호석': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 만주에서 조선혁명군 총사령, 조선혁명군 정부 군사부 부장 등을 역임한 독립
    '김호식': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 『발효공학』, 『발효미생물학』 등을 저술한 학자. 교육자.생물학자.
    '김호준': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 경상남도 합천군 독립만세시위로 체포된 구금자의 석방을 위해 결사대를 조직하
    '김호직': {'role': 'scholar'},  # 현대 - 해방 이후 『소맥분 보강에 대한 연구』, 『콩단백에 관한 연구』 등을 저술한 학자. 교육자
    '김호현': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 경상남도 창원의 삼진 만세운동에 참여했다가 순국한 독립운동가.
    '김혼': {'role': 'other'},  # 고려/고려 후기 - 고려 후기, 찬성사 · 우중찬 · 판삼사사 등을 역임하고, 낙랑군, 계림부원군에 봉해진 문
    '김홍경': {'role': 'other'},  # 조선 - 조선 후기에, 청송부사, 진산군수, 오위의 호군 등을 역임한 문신.
    '김홍근': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 의정부좌참찬, 좌의정, 판중추부사 등을 역임한 문신.
    '김홍기': {'role': 'other'},  # 현대/대한민국 - 해방 이후 서울대학교병원 병원장, 인천길병원 병원장 등을 역임한 의료인.
    '김홍도': {'role': 'scholar'},  # 조선 - 조선후기 「군선도병」 · 「단원풍속화첩」 · 「무이귀도도」 등의 작품을 그린 화가.
    '김홍량': {'role': 'other'},  # 근대 - 대한제국기 양산중학교를 설립하여 교육구국운동을 지도한 교육자. 사회운동가.
    '김홍렬': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 전라북도 옥구의 독립만세시위를 주도한 혐의로 체포되었으며, 출옥 이후에도 
    '김홍륙': {'role': 'other foreigner'},  # 근대/대한제국기 - 대한제국기 러시아어 통역관을 역임한 관료. 역관.
    '김홍미': {'role': 'other'},  # 조선 - 조선 중기에, 승문원부제조, 청송부사, 강릉부사 등을 역임한 문신.
    '김홍민': {'role': 'other'},  # 조선 - 조선 중기에, 삼사, 이조좌랑, 전한 등을 역임한 문신.
    '김홍복': {'role': 'other'},  # 조선 - 조선 후기에, 예조참의, 여주목사, 대사간 등을 역임한 문신.
    '김홍빈': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 1919년 4월 1일 평안북도 창성군에서 일어난 만세 시위운동을 주도하고, 19
    '김홍서': {'role': 'other'},  # 근대/일제강점기 - 대한민국임시의정원 의원을 역임하고 한국독립당과 조선민족혁명당에서 활동한 독립운동가.
    '김홍석': {'role': 'other'},  # 조선 - 조선 후기에, 수찬, 부교리, 교리 등을 역임한 문신.
    '김홍섭': {'role': 'other'},  # 현대/대한민국 - 해방 이후 서울지방법원 판사, 지방법원장, 대법원 판사 등을 역임한 법조인.
    '김홍수': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 『노동법학』, 『행정법』, 『행정재판제도연구』 등을 저술한 학자. 법학자.
    '김홍술': {'role': 'other'},  # 고려/고려 전기 - 신라 말과 고려 초, 진보성 성주 및 의성부 성주를 역임한 장군.
    '김홍식': {'role': 'other'},  # 현대 - 해방 이후 사법위원, 법제처 차장, 무임소장관 등을 역임한 법조인. 관료.
    '김홍욱': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 황해도관찰사 등을 역임하였으며, 효종에게 소현세자의 부인인 민회빈 강씨의 억
    '김홍운': {'role': 'scholar'},  # 조선 - 조선 후기에, 「의로가」, 「안택사」, 『동곡집』 등을 저술한 학자.
    '김홍윤': {'role': 'other'},  # 조선 - 조선 전기에, 대사헌, 경기도관찰사 등을 역임한 문신.
    '김홍익': {'role': 'scholar'},  # 조선 - 조선시대 공조좌랑, 연산현감 등을 역임한 문신. 학자.
    '김홍일': {'role': 'other'},  # 일제강점기 때, 한국독립군, 국민혁명군 등에서 활동하였고, 이봉창과 윤봉길의 의거에 사용할
    '김홍집': {'role': 'other'},  # 개항기 당상경리사, 독판교섭통상사무, 좌의정 등을 역임한 관리. 정치인.
    '김홍취': {'role': 'other'},  # 고려/고려 후기 - 고려후기 출배도감 별감, 대장군, 상장군 등을 역임한 무신.
    '김화경': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「해와 초가」를 그린 화가.
    '김화랑': {'role': 'novelist'},  # 현대/대한민국 - 일제강점기 「드메」 · 「수선화」 · 「집없는 천사」 등의 작품을 낸 작가. 시나리오작가 
    '김화산': {'role': 'poet critic'},  # 근대 - 일제강점기 「뇌동성 문학론의 극복」, 「마르크스주의의 문학론 음미」 등을 저술한 평론가. 
    '김화숭': {'role': 'other'},  # 고려/고려 전기 - 고려 전기에, 동북면병마부사, 어사중승, 한림학사 등을 역임한 문신.
    '김화식': {'role': 'other'},  # 근대 - 일제강점기 안주 동부교회, 평양창동교회 등에서 목회활동을 한 목사. 정치인.
    '김화준': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 주서, 설서, 석성현감 등을 역임한 문신.
    '김화진': {'role': 'other'},  # 조선 - 조선 후기에, 사은사, 이조판서, 판중추부사 등을 역임한 문신.
    '김확': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 철원부사 등을 역임한 문신.
    '김환': {'role': 'other'},  # 조선 - 조선후기 기사환국과 관련된 무신.
    '김환기': {'role': 'scholar'},  # 「향(響)」, 「월광」, 「영원의 노래」, 「산월」, 「무제」, 「어디서 무엇이 되어 다시
    '김환식': {'role': 'other'},  # 현대/대한민국 - 전북특별자치도 고창 출신으로 한국의 대표적인 제과 제빵 장인.
    '김환태': {'role': 'critic'},  # 근대 - 일제강점기 「문예시평」, 「예술의 순수성」, 「문학의 성격과 시대」 등을 저술한 평론가.
    '김활란': {'role': 'other'},  # 일제강점기 대한여자기독교청년회연합회 재단이사장 · 대한기독교교육자협회 회장 등을 역임한 개
    '김황': {'role': 'scholar'},  # 현대/대한민국 - 일제강점기 때, 김창숙과 함께 파리장서사건을 도모하는 등 독립운동에 힘쓰며 도학 정립과 후
    '김황원': {'role': 'poet'},  # 고려 - 고려전기 예부시랑, 한림학사 등을 역임한 문신. 시인.
    '김회': {'role': 'scholar'},  # 조선 - 조선시대 성균관박사, 사헌부감찰 등을 역임한 문신. 학자.
    '김회련': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 검교한성윤 등을 역임한 문신 · 공신.
    '김회연': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 승지, 예조참의 등을 역임한 문신.
    '김회일': {'role': 'other'},  # 현대/대한민국 - 북한에서, 최초로 시작된 대중적 증산운동인 건국사상총동원운동의 상징으로 받아들여졌으며, 교
    '김효거': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 의주부사 등을 역임한 문신.
    '김효건': {'role': 'other'},  # 조선 - 조선 후기에, 여주목사, 양주목사, 한성부판윤 등을 역임한 문신.
    '김효대': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 공조판서 등을 역임한 문신.
    '김효방': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라 제37대 선덕왕의 부친인 귀족.
    '김효석': {'role': 'other'},  # 현대/대한민국 - 내무부장관, 평화통일촉진협의회 상무위원 등을 역임한 정치인.
    '김효성': {'role': 'other'},  # 조선 - 조선 후기에, 목사, 조사오위장 등을 역임한 문신.
    '김효손': {'role': 'other'},  # 조선 - 조선 전기에, 참판, 대사헌 등을 역임한 문신.
    '김효숙': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 한국광복군 제2지대에 종군하여 대일 심리전을 펼쳤던 독립운동가.
    '김효순': {'role': 'other'},  # 조선 - 조선시대 예빈참봉, 당상역관, 한성판윤 등을 역임한 역관.
    '김효양': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라 제38대 원성왕의 부친인 귀족.
    '김효원': {'role': 'other foreigner'},  # 남북국시대 통일신라의 고애사(告哀使)로 일본에 파견된 관리.
    '김효인': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 전중시어사, 상서좌승, 병부상서 등을 역임한 문신.
    '김효정': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 사헌부감찰, 이조판서 등을 역임한 문신.
    '김효종': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 집사성 시중을 역임한 화랑. 대신.
    '김후': {'role': 'other'},  # 조선 - 조선 후기에, 부수찬 겸 금위영종사, 대사간 등을 역임한 문신.
    '김후근': {'role': 'other'},  # 조선 - 조선 후기에, 개령현감 등을 역임한 문신.
    '김후신': {'role': 'scholar'},  # 조선/조선 후기 - 조선후기 「산수도」 · 「야압도」 등의 작품을 그린 화가.
    '김후직': {'role': 'other'},  # 고대/삼국/신라 - 신라의 제22대 지증왕의 증손으로, 이찬에 임명되었으며, 병부령 등을 역임한 종실.
    '김후진': {'role': 'scholar'},  # 조선 - 조선 중기에, 경학과 역학을 연구하였으며, 고종때 호조참판에 추증된 학자.
    '김훈': {'role': 'other'},  # 현대/대한민국 - 해방 이후 기획처장, 상공부장관 등을 역임한 관료.
    '김훈영': {'role': 'other'},  # 고대/남북국/통일신라 - 통일신라의 제46대 문성왕의 종숙으로, 문성왕이 창림사 무구정탑을 건립할 때 동감수조사로서
    '김훈입': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라 제38대 원성왕의 조부인 귀족.
    '김훤': {'role': 'scholar'},  # 고려/고려 후기 - 고려 후기, 정당문학 · 보문각 대학사 · 동수국사 등을 역임한 문신.
    '김휘': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 판서, 개성유수 등을 역임한 문신.
    '김휴': {'role': 'scholar'},  # 조선 - 조선 후기에, 강릉참봉 등을 역임하였으며, 『경와집』, 『해동문헌총록』 등을 저술한 학자.
    '김흔': {'role': 'other'},  # 조선 - 조선 전기에, 행부사과 등을 역임한 문신.
    '김흔질': {'role': 'other'},  # 고대/남북국/통일신라 - 통일신라의 제33대 성덕왕의 동생으로, 당나라에 입조사로 가서 낭장의 관직을 받은 왕족.
    '김흠': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 주류성 침공 당시의 장수.
    '김흠돌': {'role': 'other'},  # 고대/남북국/통일신라 - 신라 시대 문무왕대 활약한 진골 출신의 고위 관료로, 신문왕 때 반란을 일으켰다가 실패한 
    '김흠순': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 황산벌전투에 참전한 장수.
    '김흠운': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 낭당대감을 역임한 군인.
    '김흠조': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 장례원판결사 등을 역임한 문신.
    '김흡': {'role': 'other'},  # 조선 - 조선후기 우포도대장, 총융사, 어영대장 등을 역임한 무신.
    '김흥경': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 이조판서, 우의정, 영의정 등을 역임한 문신.
    '김흥교': {'role': 'other'},  # 현대/대한민국 - 해방 이후 효성여자대학교 음악과장, 서울대학교 국악과 조교수 등을 역임한 교육자. 콘트라바
    '김흥국': {'role': 'other'},  # 조선 - 조선 후기에, 북평사, 서장관, 형조정랑 등을 역임한 문신.
    '김흥근': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 이조판서, 좌의정, 영의정 등을 역임한 문신.
    '김흥락': {'role': 'scholar'},  # 조선/조선 후기 - 조선 후기에, 학자 · 의병 · 독립운동가 등 수많은 제자를 양성하였으며, 『서산집』, 『
    '김흥렬': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 수원교구 순회교사로 활동하며 항일단체인 구국동지회를 조직하였고, 수원의 독
    '김흥배': {'role': 'other'},  # 현대 - 해방 이후 한국외국어대학을 설립한 육영사업가. 실업인.
    '김흥복': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 수원의 독립만세시위에 참여했다가 고주리 학살사건에 의해 사망한 독립운동가.
    '김흥수': {'role': 'other'},  # 조선/조선 전기 - 조선전기 첨지중추부사, 내의원내의 등을 역임한 의관.
    '김흥식': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 서울에 거주하던 상인으로, 간도 용정에 방문했다가 그곳에서 전개된 독립만세시위에
    '김흥우': {'role': 'other'},  # 조선 - 조선 중기에, 강릉참봉 등을 역임한 문신.
    '김흥조': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 해주수령, 수원부사 등을 역임한 문신.
    '김희': {'role': 'other'},  # 조선 - 조선 후기에, 이조참판, 우의정, 영중추부사 등을 역임한 문신.
    '김희갑': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「팔도강산」, 「자유부인」, 「사랑방손님과 어머니」 등에 출연한 배우. 희극인.
    '김희겸': {'role': 'scholar'},  # 조선/조선 후기 - 조선후기 「와운누계창」 · 「석천한유」 · 「안음송대」 등의 작품을 그린 화가.
    '김희남': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 임시정부에서 활동한 독립운동가.
    '김희락': {'role': 'other'},  # 조선 - 조선 후기에, 정언, 흥양현감 등을 역임한 문신.
    '김희로': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 호조참판, 동지중추부사 등을 역임한 문신.
    '김희백': {'role': 'other'},  # 근대 - 일제강점기 때, 대한국민회, 대한독립군 등에서 활약하며 군자금 모금 활동을 전개한 독립운동
    '김희삼': {'role': 'scholar'},  # 조선 - 조선전기 병조좌랑, 옥당, 삼척부사 등을 역임한 문신. 학자.
    '김희상': {'role': 'scholar'},  # 근대/일제강점기 - 일제강점기 『조선어전』, 『울이글틀』 등을 저술한 학자. 국어학자.
    '김희선': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 육군무관학교 교장, 임시정부 군무부차장 등을 역임한 관료.
    '김희수': {'role': 'other'},  # 현대/대한민국 - 해방 이후 대종상 편집상, 조선일보 기술상 등을 수상한 영화인. 편집기사.
    '김희순': {'role': 'other'},  # 근대/일제강점기 | 현대 - 근⋅현대기 전주를 중심으로 활동한 서화가.
    '김희열': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 참판, 경주부윤 등을 역임한 문신.
    '김희제': {'role': 'other'},  # 고려 - 고려후기 의주분도장군, 서북면병마부사 등을 역임한 무신.
    '김희조': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「단소와 관현악을 위한 수상곡」 · 「창과 관현악 범피중류」 · 「대춘향전」 등
    '김희주': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 대사간, 안악군수 등을 역임한 문신.
    '김희채': {'role': 'other'},  # 조선 - 조선 후기에, 교리 등을 역임한 문신.
    '김희철': {'role': 'scholar'},  # 현대/대한민국 - 인하대학교 대학원장, 총장을 비롯하여 대한기계학회 회장, 대한자동차공학회 회장 등을 역임하
    '김희춘': {'role': 'other'},  # 현대 - 해방 이후 경기도청사, 한국정신문화연구원 등을 신축한 건축가.
    '김희취': {'role': 'other'},  # 고려 - 고려후기 삼별초의 난과 관련된 무신.
    '김희화': {'role': 'other'},  # 조선 - 조선 후기에, 공조판서 등을 역임한 문신.
    '나경적': {'role': 'scholar'},  # 조선/조선 후기 - 조선 후기에, 『석당유고』 등을 저술한 학자.
    '나계종': {'role': 'other'},  # 고려/고려 후기 - 고려 후기, 사헌부시사 · 전리좌랑 · 예문관제학 등을 역임한 문신.
    '나광만': {'role': 'other'},  # 고려 - 고려 후기에, 대호군 등을 역임한 무신 · 공신.
    '나급': {'role': 'other'},  # 조선 - 조선 중기에, 장령, 평산부사 등을 역임한 문신.
    '나기학': {'role': 'other'},  # 근대 - 일제강점기 상교, 정교, 대형 등을 역임한 대종교인.
    '나대용': {'role': 'other'},  # 조선 - 조선시대 임진왜란 당시 한산도해전, 명량해전 등과 관련된 무신.
    '나덕명': {'role': 'scholar'},  # 조선 - 조선 중기에, 정여립 사건에 연루되어 유배되었으며, 임진왜란 때 의병을 모아 국경인의 반란
    '나덕헌': {'role': 'other'},  # 조선 - 조선시대 창성부사, 의주부윤, 삼도통어사 등을 역임한 무신.
    '나도향': {'role': 'novelist'},  # 근대 - 일제강점기 「벙어리 삼룡이」, 「뽕」, 「물레방아」 등을 저술한 소설가.
    '나득황': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 판예빈성사, 추밀원부사, 형부상서 등을 역임한 문신.
    '나만갑': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 병자호란 당시 남한산성에서 인조를 호종한 문신.
    '나무송': {'role': 'other'},  # 조선 - 조선 후기에, 예안현감, 병조정랑 등을 역임한 문신.
    '나무춘': {'role': 'other'},  # 조선 - 조선 후기에, 성균관학록, 성균관학정, 감찰 등을 역임한 문신.
    '나백': {'role': 'other'},  # 조선 - 조선후기 춘파 쌍언(春坡雙彦)의 제자가 되어 법맥을 계승한 승려.
    '나병삼': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 대한독립청년단연합회 모험단에 참여하여 순사 총살, 독립운동문서 배포, 친일파 처
    '나상기': {'role': 'other'},  # 현대/대한민국 - 해방 이후 홍익대학교 교수, 한국건축가협회회장 등을 역임한 건축가.
    '나상목': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 「비류」 · 「장하강촌」 등의 작품을 그린 화가.
    '나상진': {'role': 'other'},  # 현대 - 해방 이후 새나라자동차 부평공장, 경기도청사 등을 신축한 건축가.
    '나석좌': {'role': 'scholar'},  # 조선 - 조선 후기에, 명왕조 부흥세력과 연합하여 북벌을 단행해 병자호란의 치욕을 설욕하자고 주장한
    '나석주': {'role': 'other'},  # 근대/일제강점기 - 조선식산은행과 동양척식주식회사에 폭탄을 던지며 의열 투쟁을 전개한 독립운동가.
    '나성두': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 호조좌랑, 봉산현감, 이산현감 등을 역임한 문신.
    '나성화': {'role': 'other'},  # 근대 - 대한제국기 때, 심남일 의진에서 후군장으로 활약한 의병.
    '나세': {'role': 'other'},  # 고려 - 조선전기 참찬문하, 연해등처병선조전절제사 등을 역임한 장수.
    '나세진': {'role': 'scholar'},  # 근대/일제강점기|현대 - 대한해부학회 회장, 대한체질인류학회 회장 등을 역임하였으며, 해부학과 체질인류학 분야의 학
    '나세찬': {'role': 'other'},  # 조선 - 조선 전기에, 대사간, 대사헌, 한성우윤 등을 역임한 문신.
    '나수연': {'role': 'other'},  # 근대/대한제국기 - 대한제국기 황성신문 총무원, 대한자강회 총무, 중추원 참의 등을 역임한 관료. 서화가.
    '나숙': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 직제학, 승지, 부제학 등을 역임한 문신.
    '나시운': {'role': 'other'},  # 근대/개항기 - 개항기 때, 안승우 의진에서 도령장으로 활동한 의병.
    '나식': {'role': 'scholar'},  # 조선 - 조선 전기에, 『장음정집』 등을 저술하였으며, 선릉참봉을 역임하다 을사사화 때 유배형에 처
    '나양좌': {'role': 'other'},  # 조선 - 조선 후기에, 종친부전부, 삭녕군수, 장령 등을 역임한 문신.
    '나열': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 함창현감과 의금부도사 등을 역임한 문신.
    '나용균': {'role': 'other'},  # 근대 - 일제강점기 때, 2·8독립선언에 참여하였으며, 임시의정원 법제위원, 정무조사 특별위원, 정
    '나용환': {'role': 'other'},  # 근대 - 일제강점기 때, 민족대표 33인 중 한 사람으로, 독립선언서에 서명한 천도교인 · 독립운동
    '나운규': {'role': 'scholar'},  # 근대 - 일제강점기 「아리랑」, 「풍운아」, 「벙어리 삼룡」 등의 작품에 관여한 영화인. 영화감독.
    '나운영': {'role': 'other'},  # 현대/대한민국 - 「고전풍의 첼로소나타」, 「아 가을인가」 등을 만든 작곡가.
    '나월환': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 때, 철혈단을 조직하였으며, 중국헌병학교 교수, 한국청년전지공작대 대장, 한국광
    '나위소': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 경주부윤, 동지중추부사 등을 역임한 문신.
    '나유': {'role': 'other'},  # 고려 - 고려후기 진도에서 원수 김방경을 따라 삼별초를 토벌하는 공을 세운 무신.
    '나윤명': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 교서별좌 등을 역임한 문신.
    '나이준': {'role': 'other'},  # 조선 - 조선 후기에, 부교리, 집의, 사간 등을 역임한 문신.
    '나익': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 설서, 적성현감 등을 역임한 문신.
    '나익남': {'role': 'other'},  # 조선 - 조선 후기에, 개성부유수, 창원부교수, 유학교수 등을 역임한 문신.
    '나익진': {'role': 'other'},  # 현대 - 동서통상주식회사 사장, 채신부차관, 한국산업은행 총재 등을 역임한 관료 · 기업인.
    '나익희': {'role': 'other'},  # 고려 - 고려후기 검교상호군, 상의평리, 첨의참리 등을 역임한 무신.
    '나인협': {'role': 'other'},  # 근대 - 일제강점기 때, 독립선언서에 서명한 민족대표 33인 중 한 사람으로, 천도교 도사를 역임하
    '나정구': {'role': 'other'},  # 근대 - 일제강점기 때, 대한청년단, 대한통의부 등에서 군자금 모금 활동을 전개한 독립운동가.
    '나정련': {'role': 'other'},  # 근대 - 일제강점기 시교원, 경의원참의 등을 역임한 대종교인. 순교자.
    '나정록': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 홍경래의 난을 진압하는 과정에서 살해된 의병.
    '나정문': {'role': 'other'},  # 근대 - 일제강점기 교적간행회 총무, 천전건축주비회 발기인 등을 역임한 대종교인. 순교자.
    '나주의 샛골나이': {'role': 'other'},  # 전라남도 나주시 다시면 동당리의 무명짜기 기능.
    '나중소': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 북로군정서를 조직하였고, 사관양성소 교성대장, 신민부 참모부 위원장 등을 
    '나창준': {'role': 'other'},  # 현대/대한민국 - 해방 이후 한국전쟁 당시의 군인.
    '나창헌': {'role': 'other'},  # 근대 - 일제강점기 때, 대동단에서 의친왕 망명 계획에 가담하였으며, 한국노병회 이사, 교민단의사회
    '나철': {'role': 'other'},  # 근대 - 대한제국 말기에 을사오적 암살을 계획하다 유배되었으며, 대종교를 창시해 독립정신을 고취한 
    '나태섭': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 한국국민당청년단 단장으로 활동하였고, 1940년 9월 17일 창설된 한국광복군의
    '나학천': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 병조참지 등을 역임한 문신.
    '나항윤': {'role': 'other'},  # 현대 - 해방 이후 전주지방법원장, 서울지방법원장, 대법관 등을 역임한 법조인.
    '나해륜': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 이괄의 난과 병자호란이 발발하자 의병을 모집한 의병장.
    '나해봉': {'role': 'novelist'},  # 조선/조선 후기 - 조선 후기에, 이괄의 난과 병자호란이 발발하자 의병을 모집하였고, 『남간집』, 『남간집선』
    '나현성': {'role': 'scholar'},  # 현대/대한민국 - 서울대학교 사범대학 교수, 대한체육회 선수강화위원회 및 훈련평가위원회 위원 등을 역임하였으
    '나혜석': {'role': 'scholar foreigner'},  # 일제강점기 「무희」, 「스페인해수욕장」 등의 작품을 그린 화가.
    '나홍좌': {'role': 'other'},  # 조선/조선 후기 - 조선후기 함경남도병마절도사, 삼도통제사, 수원방어사 등을 역임한 무신.
    '나화랑': {'role': 'other'},  # 근대 - 해방 이후 「열아홉 순정」, 「무너진 사랑탑」, 「이정표」 등을 만든 작곡가.
    '나흥유': {'role': 'other'},  # 고려 - 고려후기 영전도감판관, 사농소경, 판전객시사 등을 역임한 무신.
    '낙금': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 청해진대사 장보고 휘하의 장수.
    '낙랑공주': {'role': 'other'},  # 고려 - 고려전기 제1대 태조의 맏딸인 공주.
    '낙랑후': {'role': 'other'},  # 고려/고려 전기 - 고려의 제10대 왕, 정종의 아들로, 형제가 모두 죽어 장자와 다를 바 없었으나, 정종 사
    '낙사계': {'role': 'other'},  # 고대/남북국/발해 - 남북국시대 당나라에서 행좌우림군장군, 농우절도사, 경략대사 등을 역임한 관리. 장군.
    '낙선군': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 제16대 왕인 인조의 서(庶)2남.
    '낙안': {'role': 'other'},  # 조선 - 조선후기 보시행으로 이름높은 범어사의 승려.
    '낙진': {'role': 'other'},  # 고려 - 고려전기 승통, 귀법사 주지, 법수사 주지, 왕사 등을 역임한 승려.
    '낙현': {'role': 'other'},  # 조선 - 개항기 팔도대각등계보제존자도총섭에 추증된 승려.
    '난승': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 김유신이 삼국통일에 뜻을 품고 석굴에 들어가 기원할 때 나타난 선인(仙人)
    '난원': {'role': 'other'},  # 고려 - 고려전기 화엄종 도승통을 역임한 승려.
    '남간': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 예문직제학, 지사간원사, 대사헌 등을 역임한 문신.
    '남간부인': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라 신인종의 종조 명랑의 모친인 귀족.
    '남경우': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 병조판서 등을 역임한 문신.
    '남경조': {'role': 'scholar'},  # 조선 - 조선 후기에, 경학을 깊이 탐구하였으며, 『구고헌일고』 등을 저술한 학자.
    '남경희': {'role': 'other'},  # 조선 - 조선 후기에, 사헌부감찰, 병조좌랑, 사간원정언 등을 역임한 문신.
    '남계병': {'role': 'other'},  # 근대 - 일제강점기 때, 경상북도 영덕군 영해면 성내시장의 독립만세시위를 주도한 독립운동가.
    '남계영': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 봉상시주부 등을 역임한 문신.
    '남계우': {'role': 'scholar'},  # 조선 - 조선후기 「군접도」 · 「화접도대련」 · 「석화접도대련」 등의 작품을 그린 화가.
    '남계하': {'role': 'other'},  # 조선 - 조선 후기에, 의금부도사, 청하현감 등을 역임한 문신.
    '남곤': {'role': 'other'},  # 조선 - 조선 전기에, 심정 등과 함께 기묘사화를 일으켜 조광조 · 김정 등 신진 사림파를 숙청한 
    '남공선': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 『한족공보(韓族公報)』 주필과 고려공산청년회 집행위원을 역임한 사회주의운동가.
    '남공철': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 대제학, 우의정, 영의정 등을 역임한 문신.
    '남관': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 「동양의 풍경」, 「허물어진 제단」, 「역사의 흔적」 등의 작품을 그린 화가.
    '남광우': {'role': 'scholar'},  # 『고어사전』, 『조선한자음연구』, 『조선한자음연구』, 『고금한한자전』 등을 저술한 학자. 
    '남광원': {'role': 'other'},  # 근대 - 대한제국기 때, 고창, 부안 등지에서 군자금 모금 활동을 전개한 의병.
    '남구만': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 함경도관찰사, 형조판서, 영의정 등을 역임한 문신.
    '남구명': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 순천부사 등을 역임한 문신.
    '남궁경': {'role': 'other'},  # 조선 - 조선 후기에, 세자시강원필선, 검상, 사인 등을 역임한 문신.
    '남궁계': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 경주부윤, 중추원부사 등을 역임한 문신.
    '남궁두': {'role': 'other'},  # 조선 - 조선시대 단학파에 속한 도교인.
    '남궁민': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 정치관, 간의 등을 역임한 문신.
    '남궁벽': {'role': 'poet'},  # 근대 - 일제강점기 「고독은 너의 운명이다」, 「신비의 인연」, 「출생」 등을 저술한 시인.
    '남궁숙': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 함경도관찰사, 동지중추부사 등을 역임한 문신.
    '남궁신': {'role': 'other'},  # 고려 - 고려 후기에, 호군 등을 역임한 무신 · 공신.
    '남궁억': {'role': 'other'},  # 근대 - 대한제국기 때, 황성신문 사장, 대한협회 회장, 배화학당 교사 등을 역임하며 애국계몽운동을
    '남궁영': {'role': 'other'},  # 근대/개항기 | 근대/일제강점기 - 일제강점기 경상남도 참여관, 충청북도지사, 중추원 참의 등을 역임한 관료. 친일반민족행위자
    '남궁옥': {'role': 'other'},  # 조선/조선 후기 - 조선후기 승문원판교, 시정 등을 역임한 문신. 서예가.
    '남궁요열': {'role': 'other'},  # 현대 - 해방 이후, 고려교향악단 오보에 주자이자, 해군군악학교 초대 교장 및 해군본부 군악대장, 
    '남궁집': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 대사헌, 대사간 등을 역임한 문신.
    '남궁찬': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 강원도관찰사 등을 역임한 문신.
    '남궁침': {'role': 'other'},  # 조선 - 조선 전기에, 한성부판윤, 오우도총부부총관, 형조참판 등을 역임한 문신.
    '남궁혁': {'role': 'other'},  # 현대/대한민국 - 일제강점기 평양신학교 교수, 조선예수교장로회 총회장 등을 역임한 목사. 교육가.
    '남궁현': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 전라북도(현, 전북특별자치도) 전주의 독립만세시위를 주도하였으며, 출옥 후
    '남규희': {'role': 'other'},  # 근대 - 일제강점기 중추원 찬의, 중추원 참의 등을 역임한 관료. 친일반민족행위자.
    '남극관': {'role': 'novelist'},  # 조선/조선 후기 - 조선후기 『몽예집』을 저술한 문인.
    '남극표': {'role': 'other'},  # 조선 - 조선 후기에, 의금부도사 등을 역임한 문신.
    '남근': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 대사헌, 대사간 등을 역임한 문신.
    '남급': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 사옹원봉사, 종묘사직장 등을 역임한 문신.
    '남기만': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 승문원주서, 장릉별검, 정언 등을 역임한 문신.
    '남기제': {'role': 'scholar'},  # 조선/조선 후기 - 조선 후기에, 『아아록』 등을 저술한 학자.
    '남노명': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 좌랑, 거창현감 등을 역임한 문신.
    '남노성': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 청요직을 두루 역임한 문신.
    '남대관': {'role': 'other foreigner'},  # 근대/일제강점기 - 재일본조선노동총동맹 중앙집행위원으로 활동한 사회운동가.
    '남덕우': {'role': 'scholar'},  # 현대/대한민국 - 대한민국의 재무부 장관, 부총리 겸 경제기획원 장관, 제14대 국무총리 등을 역임한 경제관
    '남도진': {'role': 'scholar'},  # 조선 - 조선 후기에, 『낙은별곡』, 『봉래가』 등을 저술한 문신.
    '남두민': {'role': 'other'},  # 조선/조선 후기 - 조선후기 전의감(典醫監) 정(正)을 역임한 의관.
    '남두첨': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 호조참의 등을 역임한 문신.
    '남려': {'role': 'other'},  # 고대/초기국가/동예 - 초기국가시대 위만조선 말기 예족의 군장.
    '남만춘': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 합동민족부대 참모장, 고려공산당창립대회준비위원 등을 역임한 사회주의운동가.
    '남명학': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 참봉, 감찰, 평택현감, 공조좌랑 등을 역임한 함경도 출신의 문신.
    '남모': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라 청소년 조직의 수장인 원화(源花).
    '남몽뢰': {'role': 'scholar'},  # 조선 - 조선 후기에, 예조정랑, 진주목사 등을 역임하였으며, 『이게문집』 등을 저술한 문신.
    '남무성': {'role': 'other'},  # 조선 - 조선 후기에, 병자호란이 발발하자 충청도관찰사 정세규의 휘하에서 활약한 의병.
    '남벌': {'role': 'other'},  # 조선 - 조선 후기에, 장령, 삼척부사 등을 역임한 문신.
    '남병길': {'role': 'scholar'},  # 조선 - 조선후기 『칠정보법』 · 『태양출입표』 · 『산학정의』 등을 저술한 학자. 천문역법학자.
    '남병철': {'role': 'scholar'},  # 조선 - 조선후기 예조판서, 대제학 등을 역임한 문신. 천문학자 · 수학자.
    '남사고': {'role': 'scholar'},  # 조선 - 조선시대 『남사고비결』, 『남격암십승지론』 등을 저술한 학자. 도사(道士).
    '남상교': {'role': 'novelist'},  # 조선/조선 후기 - 조선후기 충주목사, 동지돈령부사 등을 역임한 문신. 문인 · 종교인.
    '남상국': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「고성오광대」의 전승자로 인정된 예능보유자.
    '남상덕': {'role': 'other foreigner'},  # 근대 - 대한제국기 대한제국군대 해산령 당시 일본군에 항전한 항일운동가.
    '남상목': {'role': 'other'},  # 근대 - 대한제국기 때, 용인에서 모병하여 구식총 40자루와 양총 10자루로 항일의병투쟁을 전개한 
    '남상문': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 군수 등을 역임한 문신.
    '남석인': {'role': 'other'},  # 근대 - 대한제국기 때, 정용기의 산남의진에서 청송지방 소모장으로 활동한 의병장.
    '남선': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 이조판서 등을 역임한 문신.
    '남세건': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 대사성, 호조참판 등을 역임한 문신.
    '남세주': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 지평, 부응교, 예문관응교 등을 역임한 문신.
    '남세준': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 경기감사, 예조참판, 이조참판 등을 역임한 문신.
    '남수문': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 집현전부수찬, 집현전응교, 집현전직제학 등을 역임한 문신.
    '남순민': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 첨지중추부사, 오위장 등을 역임한 문신.
    '남억우': {'role': 'other'},  # 현대/대한민국 - 해방 이후 한국교육개발원 부원장, 인천교원단체 연합회 회장 등을 역임한 교육자.
    '남언경': {'role': 'other'},  # 조선 - 조선시대 때, 양명학의 사상적 체계를 완성한 문신.
    '남언기': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 인심도심설을 토론하며 도학에 열중한 문신.
    '남언순': {'role': 'other'},  # 조선/조선 전기 - 조선전기 병조참의, 함경도병마절도사 등을 역임한 무신.
    '남연': {'role': 'other'},  # 조선 - 조선 후기에, 공조정랑, 성균관직강, 봉상시첨정 등을 역임한 문신.
    '남연년': {'role': 'other'},  # 조선/조선 후기 - 조선후기 이인좌의 난과 관련된 무신.
    '남영': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 선조~광해군 연간의 침의(鍼醫).
    '남영신': {'role': 'other'},  # 고려 - 고려 후기에, 사관 등을 역임한 문신.
    '남용익': {'role': 'scholar'},  # 조선/조선 후기 - 조선후기 좌참찬, 예문관제학 등을 역임한 문신. 학자.
    '남운룡': {'role': 'other'},  # 현대/대한민국 - 해방 이후 남사당놀이 중 「꼭두각시놀음」의 전승자로 지정된 예능보유자.
    '남위': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 학생 대표로서 3·1운동에 참가해 시위를 주도하다가 체포되어 고문 후유증으
    '남위언': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 중국 만주 북간도 민족교육기관인 명동중학교 교사를 역임한 교육자.
    '남유': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 서천군수와 부평부사를 역임하고 정유재란 때 노량해전에서 전사한 무신.
    '남유상': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 실록랑, 수찬, 이조정랑 등을 역임한 문신.
    '남유용': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 홍문관교리, 홍문관제학, 형조판서 등을 역임한 문신.
    '남윤구': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 조선노농총동맹 중앙위원 등을 역임하며 항일투쟁을 전개한 독립운동가.
    '남윤함': {'role': 'other'},  # 조선 - 조선시대 동지사 정경세를 수행하여 명나라에 다녀온 역관.
    '남은': {'role': 'other'},  # 고려 후기에, 삼척지군사, 밀직부사, 지문하부사 등을 역임한 문신.
    '남을진': {'role': 'other'},  # 고려/고려 후기 - 고려후기 참지문하부사, 사천백 등을 역임한 문신. 충신.
    '남응룡': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 공조참의 등을 역임한 문신.
    '남응운': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 승정원주서, 길주목사, 경기도관찰사 등을 역임한 문신.
    '남응중': {'role': 'other'},  # 조선/조선 후기 - 조선후기 은언군의 손자를 왕으로 추대하고자 반란을 모의한 주모자. 반역자.
    '남이': {'role': 'other'},  # 조선/조선 전기 - 조선전기 공조판서, 병조판서 등을 역임한 무신.
    '남이공': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 예조참의, 홍문관부제학, 병조참판 등을 역임한 문신.
    '남이성': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 예조판서 등을 역임한 문신.
    '남이신': {'role': 'other'},  # 조선 - 조선 중기에, 경기도관찰사, 안변부사, 대사간 등을 역임한 문신.
    '남이웅': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 이조판서, 우의정, 좌의정 등을 역임한 문신.
    '남이준': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 사간, 경성판관 등을 역임한 문신.
    '남이흥': {'role': 'other'},  # 조선 - 조선시대 선전관, 안주목사, 연안부사 등을 역임한 무신.
    '남익훈': {'role': 'other'},  # 조선 - 조선 후기에, 함경도관찰사 등을 역임한 문신.
    '남인수': {'role': 'other'},  # 근대 - 해방 이후 「가거라 삼팔선」, 「이별의 부산정거장」 등 다수의 곡을 발표한 가수.
    '남일우': {'role': 'other'},  # 근대 - 조선 후기에, 홍문관부제학, 경상도관찰사, 공조판서 등을 역임한 문신.
    '남자': {'role': 'scholar'},  # 조선 - 조선 후기에, 『중용차의』 등을 저술한 문신.
    '남자현': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 만주 서로군정서에서 활약하였고, 여성 계몽과 독립정신 고취에 힘쓰며 군자금
    '남재': {'role': 'other'},  # 조선 - 조선 전기에, 도병마사, 경기도관찰사, 좌의정 등을 역임한 문신.
    '남정각': {'role': 'other'},  # 근대 - 일제강점기 때, 의열단에서 활동하며 일제 기관 파괴를 계획하다 발각되어 체포된 독립운동가.
    '남정국': {'role': 'other'},  # 조선 - 조선 전기에, 공조정랑, 충훈부도사 등을 역임한 문신.
    '남정순': {'role': 'other'},  # 근대 - 조선 후기에, 함경도안무사, 공조판서, 이조판서 등을 역임한 문신.
    '남정임': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「유정」, 「까치소리」, 「분녀」 등에 출연한 배우. 영화배우.
    '남정중': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 능주목사 등을 역임한 문신.
    '남정철': {'role': 'other'},  # 근대 - 일제강점기 한성판윤, 내부대신 등을 역임한 관료. 친일반민족행위자.
    '남종삼': {'role': 'other'},  # 조선 - 조선후기 홍문관교리 · 영해현감 · 승지 등을 역임한 순교자.
    '남좌시': {'role': 'other'},  # 고려/고려 후기 - 고려후기 첨서밀직(簽書密直), 강릉도부원수(江陵道副元帥), 정당상의(政堂商議) 등을 역임한
    '남주헌': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 승지, 춘천부사 등을 역임한 문신.
    '남준표': {'role': 'other'},  # 근대 - 일제강점기 만주에서 조선인 공청운동에 참여한 사회주의운동가.
    '남중유': {'role': 'other'},  # 조선 - 조선 후기에, 사직서령, 대흥군수 등을 역임한 문신.
    '남지': {'role': 'other'},  # 조선 - 조선 전기에, 호조판서, 우의정, 좌의정 등을 역임한 문신.
    '남질': {'role': 'other'},  # 고려 - 고려 후기에, 경상도도순문사 등을 역임한 문신.
    '남창익': {'role': 'other'},  # 근대 - 일제강점기 동북인민혁명군 제2군 독립사 제3단 정치위원 등을 역임한 사회주의운동가.
    '남채': {'role': 'other'},  # 현대/대한민국 - 해방 이후 불교조계종 교무국장, 한국불교태고종 제5대총무원 등을 역임한 승려.
    '남천우': {'role': 'other foreigner'},  # 현대/대한민국 - 일제강점기 때, 대전제일교회 목사, 일본기독교 조선감리교단 상임위원 등을 역임하였으며, 해
    '남천한': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 호조참의 등을 역임한 문신.
    '남추': {'role': 'other'},  # 조선 - 조선 전기에, 성균관학유, 성균관전적 등을 역임한 문신.
    '남취명': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 병조참판, 지돈녕부사 등을 역임한 문신.
    '남치근': {'role': 'other'},  # 조선/조선 전기 - 조선전기에 전라도병마절도사 · 전라도순변사 · 한성부판윤 등을 역임한 무신.
    '남치리': {'role': 'scholar'},  # 조선 - 조선 전기에, 『비지문집』 등을 저술한 학자.
    '남치원': {'role': 'other'},  # 조선 - 조선전기 평시서제조, 훈련원첨정 등을 역임한 관리.
    '남치훈': {'role': 'other'},  # 조선 - 조선 후기에, 형조참판, 강원도관찰사 등을 역임한 문신.
    '남탁': {'role': 'other'},  # 조선 - 조선 후기에, 종부시정, 해미현감 등을 역임한 문신.
    '남태기': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 형조참판, 한성부좌우윤, 예조판서 등을 역임한 문신.
    '남태온': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 오위도총부부총관, 안변부사 등을 역임한 문신.
    '남태응': {'role': 'novelist'},  # 조선/조선 후기 - 조선 후기에, 『청죽만록』, 『청죽별지』, 「삼화가유평」 등을 저술한 문인.
    '남태저': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 병조참판, 한성부우윤 등을 역임한 문신.
    '남태제': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 경기감사, 홍문관제학, 이조판서 등을 역임한 문신.
    '남태징': {'role': 'other'},  # 조선/조선 후기 - 조선후기 이인좌의 난과 관련된 무신.
    '남태혁': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 사간, 승정원동부승지, 공조참판 등을 역임한 문신.
    '남태회': {'role': 'other'},  # 조선 - 조선 후기에, 형조판서, 동지의금부사 등을 역임한 문신.
    '남포': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 공조낭관, 홍문관직제학, 소격서령 등을 역임한 문신.
    '남하정': {'role': 'scholar'},  # 조선 - 조선 후기에, 「출사책」, 『사대춘추』, 『동소만록』 등을 저술한 학자.
    '남하행': {'role': 'scholar'},  # 조선 - 조선 후기에, 『와유록』, 『술선록』 등을 저술한 학자.
    '남한기': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 장례원판결사, 오위도총부부총관 등을 역임한 문신.
    '남한조': {'role': 'scholar'},  # 조선 - 조선 후기에, 「거습잠」, 『손재문집』 등을 저술한 학자.
    '남해준': {'role': 'scholar'},  # 조선 - 조선 후기에, 『사례질의』 등을 저술한 학자.
    '남해차차웅': {'role': 'other'},  # 고대/삼국 - 신라의 제2대(재위: 4년~24년) 왕.
    '남형우': {'role': 'other'},  # 근대/일제강점기 - 대한민국임시정부 법무총장과 교통총장을 역임한 독립운동가.
    '남효온': {'role': 'novelist'},  # 조선 - 조선 전기에, 김종직의 문인으로, 문종의 비, 현덕왕후의 능인 소릉의 복위를 상소한 일로 
    '남효의': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 대사헌, 형조판서 등을 역임한 문신.
    '남휘': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 판한성부사, 평양선위사, 황주선위사 등을 역임한 문신.
    '남흔': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 통정대부, 좌부승지, 우부승지 등을 역임한 문신.
    '낭오': {'role': 'other'},  # 조선 - 조선 후기, 불교의 수계 의식 전통을 복구한 승려.
    '낭지': {'role': 'other'},  # 고대/남북국/통일신라 - 삼국시대 신라의 삽량주 영취산에서 『법화경』을 강의했던 승려.
    '내례부인': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라 제8대 아달라이사금의 왕비.
    '내로': {'role': 'other'},  # 고대/삼국/신라 - 신라의 건국시조인 박혁거세의 손자인 왕족.
    '내물마립간': {'role': 'other'},  # 신라의 제17대(재위: 356년~402년) 왕.
    '내숙': {'role': 'other'},  # 고대/삼국/신라 - 신라의 제17대 왕, 내물마립간의 증손으로, 이벌찬에 임명된 종실.
    '내원': {'role': 'other'},  # 고려/고려 후기 - 고려후기 제28대 충혜왕의 왕사로 책봉된 승려.
    '내음': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라 제10대 내해이사금의 서자인 왕자. 재상.
    '내음갈문왕': {'role': 'other'},  # 고대/삼국/신라 - 신라의 제14대 왕, 유례이사금의 외조부로, 갈문왕에 책봉된 귀족.
    '내해이사금': {'role': 'other'},  # 고대/삼국 - 신라의 제10대(재위 196년~230년) 왕.
    '노개방': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 동래교수 등을 역임한 문신.
    '노경린': {'role': 'other'},  # 조선 - 조선 전기에, 사헌부지평, 성주목사, 숙천부사 등을 역임한 문신.
    '노경임': {'role': 'other'},  # 조선 - 조선 중기에, 지영해부사, 성주목사 등을 역임한 문신.
    '노경희': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「실낙원의 별」 · 「느티나무있는 언덕」 · 「어느 하늘 아래서」 등에 출연한 
    '노계원': {'role': 'scholar'},  # 조선 - 조선 후기에, 『오행설』, 『정성서의』, 『심의설』 등을 저술한 학자.
    '노계정': {'role': 'other'},  # 조선 - 조선후기 박천군수, 위원군수, 전라우수사 등을 역임한 무신.
    '노공일': {'role': 'other'},  # 근대 - 대한제국기 때, 창의군 의진에서 종사관으로 활동한 의병장.
    '노공필': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 우찬성, 영중추부사 등을 역임한 문신.
    '노관': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 이부원외랑, 이부낭중, 판사재사 등을 역임한 문신.
    '노광두': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 장령, 동부승지, 호조참판 등을 역임한 문신.
    '노구산': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 밀직제학, 좌군총제, 도총제 등을 역임한 문신.
    '노구영': {'role': 'other'},  # 근대/대한제국기 - 대한제국기 태의원전의보, 태의원전의 등을 역임한 관료. 의관.
    '노국대장공주': {'role': 'other'},  # 고려후기 제31대 공민왕의 왕비.
    '노극복': {'role': 'other'},  # 조선 - 조선 후기에, 이조정랑, 오수도찰방 등을 역임한 문신.
    '노극신': {'role': 'other'},  # 조선 - 조선 중기에, 양성, 김포 등지의 수령, 돈녕부첨정 등을 역임한 문신.
    '노극청': {'role': 'other'},  # 고려/고려 후기 - 고려후기 산관, 직장동정 등을 역임한 관리.
    '노극홍': {'role': 'scholar'},  # 조선 - 조선 중기에, 임진왜란이 발발하자 곽재우의 휘하에서 서기, 참모로 활동하였으며, 정유재란 
    '노긍': {'role': 'novelist'},  # 조선/조선 후기 - 조선 후기 『한원문집』을 저술한 문인.
    '노기남': {'role': 'other'},  # 현대/대한민국 - 한국인 최초의 주교이자 교구장.
    '노기용': {'role': 'other'},  # 근대 - 일제강점기 때, 대구에서 군사주비단에 가담하여 군자금 모금 활동을 전개한 독립운동가.
    '노단': {'role': 'other'},  # 고려/고려 전기 - 고려 전기에, 중추원사, 상서좌복야 참지정사 등을 역임한 문신.
    '노대하': {'role': 'other'},  # 조선 - 조선 중기에, 고부군수 등을 역임한 문신.
    '노덕술': {'role': 'other'},  # 현대/대한민국 - 일제강점기 육군본부 헌병대장, 부산 제2육군범죄수사단 대장 등을 역임한 군인. 친일반민족행
    '노도형': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 예천군수 등을 역임한 문신.
    '노류지': {'role': 'other foreigner'},  # 고대/삼국/고구려 - 삼국시대 일본에 파견된 고구려의 공예가.
    '노리부': {'role': 'other'},  # 고대/삼국/신라 - 신라 진평왕대에 상대등을 지낸 진골 귀족.
    '노리사치계': {'role': 'other foreigner'},  # 고대/삼국/백제 - 삼국시대 백제의 달솔로서 일본에 불교를 전수한 귀족.
    '노명석': {'role': 'novelist'},  # 현대 - 해방 이후 『문』, 『용사냥』, 『노들강변』 등을 저술한 소설가.
    '노무현': {'role': 'other'},  # 현대/대한민국 - 대한민국의 제16대 대통령.
    '노문천': {'role': 'poet'},  # 현대/대한민국 - 해방 이후 『미이라』, 『불멸의 연가』, 『Back mirror』 등을 저술한 시인.
    '노물재': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 유거감찰, 첨지중추부사, 동지돈녕부사 등을 역임한 문신.
    '노백린': {'role': 'other'},  # 근대/일제강점기 - 대한민국임시정부의 군무총장과 국무총리를 역임한 독립운동가.
    '노병대': {'role': 'other'},  # 근대 - 대한제국기 때, 속리산에서 의병을 모집하여 충청북도와 경상북도에서 항일의병투쟁을 전개한 의
    '노병선': {'role': 'other'},  # 근대/일제강점기 - 대한제국기 협성회 부회장, 웹윗청년회 창립위원 등으로 활동한 개신교인.
    '노병희': {'role': 'other'},  # 근대/대한제국기 - 대한제국기 때, 최익현과 의병활동을 모의하며 군자금 모금 운동을 전개하였고, 의진에서 의관
    '노복선': {'role': 'other'},  # 근대 - 일제강점기 때, 임시정부 군무부 군사특파단 청년공작원, 광복군 총사령부 부관 등을 역임한 
    '노부': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 거칠부 등과 고구려를 침공하여 한강 상류지역 10개군을 점령한 장수.
    '노사신': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 이조판서, 영중추부사, 영의정 등을 역임한 문신.
    '노사예': {'role': 'scholar'},  # 조선 - 조선시대 『경임안』, 『홍와유고』, 『사서찬요』 등을 저술한 학자. 의병참모.
    '노석빈': {'role': 'other'},  # 조선 - 조선 후기에, 공조좌랑, 창평현감, 직강 등을 역임한 문신.
    '노석숭': {'role': 'other'},  # 고려/고려 후기 - 고려후기 이의민 제거와 관련된 관리. 무신.
    '노석정': {'role': 'other'},  # 근대 - 일제강점기 때, 전라남도에서 군자금 모금 활동을 전개한 독립운동가.
    '노석중': {'role': 'other'},  # 근대 - 일제강점기 때, 전라남도에서 동지 포섭 및 군자금 모금 활동을 전개한 독립운동가.
    '노선': {'role': 'other'},  # 고려/고려 후기 - 고려 후기, 공민왕 때 자제위 소속 관리.
    '노선경': {'role': 'other'},  # 조선 - 조선 전기에, 함양군수, 고령현감 등을 역임한 문신.
    '노세후': {'role': 'scholar'},  # 조선 - 조선 중기에, 상수학 및 정전법에 정통했으며, 임진왜란 때 곽재우의 휘하에서 의병으로 싸운
    '노수': {'role': 'scholar'},  # 조선 - 조선 전기에, 『경신잠』, 『삼성잠』 등을 저술한 학자.
    '노수신': {'role': 'other'},  # 조선 - 조선 전기에, 우의정, 좌의정, 영의정 등을 역임한 문신.
    '노수현': {'role': 'other'},  # 현대/대한민국 - 해방 이후 서울대학교 미술대학 교수, 대한민국미술전람회 심사위원 등을 역임한 화가.
    '노숙': {'role': 'other'},  # 조선 - 조선시대 용양위부호군를 역임한 무신.
    '노숙동': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 대사헌, 형조참판, 동지중추원사 등을 역임한 문신.
    '노순': {'role': 'novelist'},  # 조선/조선 후기 - 조선 후기 조식의 문인으로, 임진왜란 때 삼가에서 창의한 의병장.
    '노숭': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 참판승추부사, 참찬의정부사, 검교우의정 등을 역임한 문신.
    '노약순': {'role': 'other'},  # 고려/고려 후기 - 고려후기 노약순, 한수도 반란기도사건 등과 관련된 관리.
    '노영': {'role': 'other'},  # 고려/고려 후기 - 고려후기 「아미타구존도」를 그린 화가.
    '노영거': {'role': 'other'},  # 고려/고려 전기 - 고려 전기에, 좌중군사, 공부시랑 등을 역임한 문신.
    '노영규': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「수영야류」 양반 역 전승자로 인정된 기예능보유자.
    '노영서': {'role': 'other'},  # 고려 - 고려후기 내승별감, 직성군 등을 역임한 관리.
    '노영손': {'role': 'other'},  # 조선/조선 전기 - 조선 전기, 중종반정 이후에 형성된 정국공신 중심 체제에 불만을 품었던 이과 등의 무리를 
    '노영수': {'role': 'other'},  # 고려 - 고려후기 서운부정, 대호군, 밀직사 등을 역임한 관리.
    '노영순': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 합문지후, 참지정사, 문하시랑평장사 등을 역임한 문신.
    '노영의': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 다봉 등을 역임한 문신.
    '노영재': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 중국에서 활동한 독립운동가.
    '노영희': {'role': 'other'},  # 고려 - 고려후기 삼별초의 난과 관련된 무신.
    '노우명': {'role': 'scholar'},  # 조선 - 조선 전기에, 음운학에 조예가 깊었으며, 현릉참봉을 역임하였으나 기묘사화에 연루되어 파직된
    '노원섭': {'role': 'other'},  # 근대/대한제국기 - 대한제국기 때, 공주 용당에서 의진을 결성하였으며, 국권 피탈 이후 고향에서 독립만세시위를
    '노원순': {'role': 'other'},  # 고려 - 고려후기 상장군, 중군병마사 등을 역임한 무신.
    '노을룡': {'role': 'other foreigner'},  # 근대 - 일제강점기 때, 중국의 국민혁명군으로 복무하며 의열단에서 활동하였고, 조선인 군관학교 교관
    '노응규': {'role': 'other foreigner'},  # 근대/개항기 - 개항기 때, 안의에서 의병을 일으켰고, 일본군 및 척후대 공격, 경부철도 파괴 활동 등을 
    '노응환': {'role': 'other'},  # 조선 - 조선 중기에, 임진왜란이 발발하자 의병에 자원하였으며, 금산전투에서 항전하다 전사한 의병.
    '노이형': {'role': 'other'},  # 조선 - 조선 후기에, 예조정랑, 춘추관기주관, 전적 등을 역임한 문신.
    '노인': {'role': 'other'},  # 조선 - 조선시대 황해수사, 진용교위 등을 역임한 장수.
    '노인수': {'role': 'other'},  # 고려 - 고려후기 분도장군, 상장군 등을 역임한 무신.
    '노인우': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 인주수령 등을 역임한 문신.
    '노임수': {'role': 'other'},  # 근대 - 대한제국기 때, 의병장 김동신의 휘하에서 활동하다가 직접 의병을 규합하여 항일의병투쟁을 전
    '노자영': {'role': 'poet essayist'},  # 근대 - 일제강점기 『처녀의 화환』, 『내 혼이 불탈 때』, 『백공작』 등을 저술한 시인. 수필가.
    '노자형': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 사성, 대사성, 첨지중추부사 등을 역임한 문신.
    '노장': {'role': 'other'},  # 「봉산탈춤」, 「강령탈춤」, 「송파산대놀이」, 「양주별산대놀이」에 등장하는 배역.
    '노재철': {'role': 'other'},  # 근대 - 일제강점기 때, 충남, 전북 등지에서 군자금 모금 활동을 전개한 독립운동가.
    '노전': {'role': 'other'},  # 고려/고려 전기 - 고려 전기에, 중추부사 상호군, 삼사사, 호부상서 등을 역임한 문신.
    '노정': {'role': 'other'},  # 고려 - 고려전기 어사중승, 행영도병마부사, 예빈경 등을 역임한 관리.
    '노정섭': {'role': 'scholar'},  # 근대 - 개항기 때, 개항에 반대하는 척화상소를 올렸으나 받아들여지지 않자, 학문에 전념하여 『연곡
    '노종': {'role': 'other'},  # 고대/삼국 - 삼국시대 금관가야 제10대 구형왕의 첫째 아들인 왕자.
    '노종균': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 한인애국단원으로 활동한 독립운동가.
    '노준': {'role': 'other'},  # 조선 - 조선 전기에, 동래부사, 파주목사, 관찰사 등을 역임한 문신.
    '노준명': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 홍원목사 등을 역임한 문신.
    '노중례': {'role': 'other'},  # 조선/조선 전기 - 조선전기 판전의감사, 첨지중추원사, 상호군 등을 역임한 의관.
    '노지': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 때, 이찬 관등으로 사량궁의 사신을 역임한 신라의 관리.
    '노지정': {'role': 'other'},  # 고려/고려 후기 - 고려 후기, 희종복위 참소사건에 연루되어 최우에게 죽임을 당한 무신.
    '노직': {'role': 'other'},  # 조선 - 조선 중기에, 병조판서, 판중추부사 등을 역임한 문신.
    '노진': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 대사헌, 예조판서 등을 역임한 문신.
    '노진규': {'role': 'other'},  # 현대 - 해방 이후 「동래야류」의 전승자로 지정된 예능보유자.
    '노진룡': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 임시정부 전라북도 총감독으로 임명되어 군자금 모금 활동을 전개한 독립운동가
    '노진설': {'role': 'other'},  # 현대 - 해방 이후 중앙선거관리위원장, 감찰위원장 등을 역임한 법조인.
    '노진의': {'role': 'other'},  # 고려 - 고려후기 낭장, 장군 등을 역임한 무신.
    '노창성': {'role': 'other'},  # 근대 - 일제강점기 경성방송국 제2방송부장, 서울중앙방송국 국장, 방송관리국 국장 등을 역임한 방송
    '노책': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 좌정승, 집현전학사 등을 역임하였으며, 딸이 원의 태자비가 되자 권세를 부리
    '노천명': {'role': 'poet'},  # 근대/일제강점기 - 일제강점기 『산호림』 · 『창변』 · 『별을 쳐다보며』 등을 저술한 시인. 친일반민족행위자
    '노춘근': {'role': 'other'},  # 조선 - 조선시대 임진왜란 당시 당포해전에 참전한 무신.
    '노탁유': {'role': 'other'},  # 고려 - 고려후기 서북면지병마사, 흥위위섭상장군, 용호군상장군 등을 역임한 무신.
    '노태준': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 한국광복군 간부로 활동한 독립운동가.
    '노필': {'role': 'other'},  # 조선 - 조선 전기에, 공조좌랑, 경상도도사 등을 역임한 문신.
    '노한': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 우찬성사, 대사헌, 우의정 등을 역임한 문신.
    '노한문': {'role': 'other'},  # 조선 - 조선 전기에, 사헌부지평, 교서관판교, 통례원좌통례 등을 역임한 문신.
    '노현용': {'role': 'other'},  # 고려 - 고려 전기에. 진사, 사신 등을 역임한 문신.
    '노협': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 정주목사 등을 역임한 문신.
    '노형규': {'role': 'other'},  # 근대 - 일제강점기 때, 임시정부 지원을 위해 군자금 모금 활동을 전개한 독립운동가.
    '노형하': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 승정원주서, 지평, 정언 등을 역임한 문신.
    '노홍기': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 익산군수 등을 역임한 문신.
    '노효돈': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 중낭장, 동지추밀원사, 문하시랑평장사 등을 역임한 문신.
    '노흠': {'role': 'scholar'},  # 조선 - 조선 중기에, 참봉, 봉사가 되었으나 낙향하여 학문과 수행에 전념하였으며, 『입재고』 등을
    '노힐부득': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 제33대 성덕왕 때 미륵불이 된 염불하는 승려.
    '녹진': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 집사부시랑을 역임한 관리.
    '논개': {'role': 'other'},  # 조선 - 조선시대 임진왜란 당시 의기(義妓)로 알려진 기생.
    '뇌음신': {'role': 'other'},  # 고대/삼국/고구려 - 삼국시대 고구려의 술천성 침공 당시의 장수.
    '뇌질주일': {'role': 'other'},  # 고대/삼국 - 삼국시대 대가야의 건국 시조.
    '뇌질청예': {'role': 'other'},  # 고대/삼국 - 삼국시대 금관가야의 건국 시조.
    '뇌학': {'role': 'other'},  # 조선 - 조선후기 명주사 자흠의 제자로 설송의 법맥을 계승한 승려.
    '누한': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 제17대(재위:356~402) 왕.
    '눌지마립간': {'role': 'other'},  # 신라의 제19대(재위: 417년~458년) 왕.
    '눌최': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 앵잠, 봉잠, 기현 3성전투에 참전한 장수.
    '능귀문': {'role': 'other foreigner'},  # 고대/삼국/백제 - 삼국시대 백제의 제27대 위덕왕 때 불교를보급하기 위하여 일본에 파견된 기술자.
    '능달': {'role': 'other'},  # 고려/고려 전기 - 고려전기 호족으로 왕경에 초치된 무신.
    '능문': {'role': 'other'},  # 고대/남북국/통일신라 - 고려전기 대광으로 후백제의 신라 침입을 방비하기 위하여 파견된 장수.
    '능범': {'role': 'other'},  # 고려 - 고려전기 내봉낭중, 내장 및 동궁 식읍의 심곡사 등을 역임한 관리.
    '능선': {'role': 'other'},  # 고려/고려 전기 - 고려전기 나주에서 유금필, 충질 등과 견훤의 고려 투항을 인솔한 관리.
    '능식': {'role': 'other'},  # 고려/고려 전기 - 고려 전기에, 순군낭중 등을 역임한 관리 · 공신.
    '능신': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 백수성전투에 참전한 장수.
    '능안': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 나마 긴주의 아들로 가야춤에 능했던 음악인.
    '능애': {'role': 'other'},  # 고대/남북국 - 후백제의 제1대 왕, 견훤의 동생인 왕족.
    '능여': {'role': 'other'},  # 고대/남북국 - 남북국시대 직지사를 중창한 승려.
    '능예': {'role': 'other'},  # 고대/남북국 - 남북국시대 후백제 견훤의 열째 아들인 왕자.
    '능예남': {'role': 'other'},  # 고대/남북국 - 남북국시대 후백제 견훤의 궁녀.
    '능준': {'role': 'other'},  # 고려 - 고려전기 수순군부경(守徇軍部卿), 내봉경 등을 역임한 관리.
    '능창': {'role': 'other'},  # 고대/남북국/후백제 - 후삼국 시기 서남해안 나주 압해도를 중심으로 해상 세력을 이끌었던 인물.
    '능현': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 매조성장군을 역임한 호족.
    '능혜': {'role': 'other'},  # 고려/고려 전기 - 고려전기 내군경을 역임한 관리.
    '능환': {'role': 'other'},  # 고대/남북국 - 남북국시대 때, 후백제의 왕인 견훤을 금산사에 유폐하고, 넷째 아들 금강을 살해한 관리.
    '다루왕': {'role': 'other'},  # 고대/삼국/백제 - 백제의 제2대(재위: 28년~77년) 왕.
    '다리': {'role': 'other'},  # 고대/삼국 - 삼국시대 백제의 무령왕릉에서 출토된 은팔찌를 제작한 공예가.
    '다미': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 나당연합군의 백제 정벌 당시의 장수.
    '다상': {'role': 'other foreigner'},  # 고대/삼국시대 - 삼국시대 백제에서 일본에 건너가 불교 전파에 공헌한 승려.
    '다식': {'role': 'other'},  # 고대/삼국/고구려 - 삼국시대 고구려 소형으로 고구려 부흥에 힘쓴 귀족. 부흥운동가.
    '다지': {'role': 'other'},  # 고려 - 고려후기 수졸, 낭장 등을 역임한 무신.
    '단경왕후': {'role': 'other'},  # 조선/조선 전기 - 조선전기 제11대 중종의 왕비.
    '단군': {'role': 'other'},  # 고대/초기국가/고조선 - 고조선의 제1대(재위:BCE.2333~BCE.1122) 왕.
    '단양이': {'role': 'scholar foreigner'},  # 고대/삼국/백제 - 삼국시대 때, 오경박사로서 일본에 파견된 백제의 학자.
    '단의왕후': {'role': 'other'},  # 조선/조선 후기 - 조선후기 제20대 경종의 왕비.
    '단의장옹주': {'role': 'other'},  # 고대/남북국/통일신라 - 통일신라의 제48대 경문왕의 누이로, 미륵불에 귀의하여 독실한 신자가 된 왕족.
    '단종': {'role': 'other'},  # 조선의 제6대(재위: 1452년~1455년) 왕.
    '달가': {'role': 'other'},  # 고대/삼국/고구려 - 고구려의 제13대 서천왕의 동생이자 제14대 봉상왕의 작은 아버지로, 안국군에 봉해져 군사
    '달공': {'role': 'scholar'},  # 고려 - 고려후기 『법어』을 저술한 승려.
    '달관': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 나당연합군의 고구려 정벌 당시의 장수.
    '달달박박': {'role': 'other'},  # 고대/남북국시대 - 남북국시대 통일신라의 제33대 성덕왕 때 아미타불로 화현한 염불하는 승려.
    '달사': {'role': 'other'},  # 고대/삼국/백제 - 삼국시대 백제의 고구려 도살성 함락 당시의 장수.
    '달선': {'role': 'other'},  # 조선/조선 후기 - 조선후기 유점사 승통, 보현사 수호총섭 등을 역임한 승려.
    '달자': {'role': 'other'},  # 고려/고려 후기 - 고려후기 개경 연복사를 중심으로 활동한 승려.
    '달전': {'role': 'poet'},  # 고려/고려 후기 - 고려후기 「연경 호천사의 9층대탑에 올라」 · 「이하의 장진주 운을 따라 짓다」 등을 저술
    '담릉': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 화랑 김원술을 보좌한 관리.
    '담수': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 「날현인」을 지은 승려.
    '담양군': {'role': 'other'},  # 조선/조선 전기 - 조선전기 제4대 세종의 서자인 왕자.
    '담욱': {'role': 'other'},  # 고대/삼국시대 - 삼국시대 백제의 계율을 확립시킨 승려.
    '담육': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 수나라 유학승으로 신라 불교에 큰 영향을 끼친 승려.
    '담진': {'role': 'other'},  # 고려 - 고려전기 예종의 국사로 활동한 승려.
    '담징': {'role': 'other foreigner'},  # 고대/삼국 - 삼국시대 일본 호류사금당벽화(사불정토도)를 그린 승려. 화가.
    '담혜': {'role': 'other foreigner'},  # 고대/삼국시대 - 삼국시대 백제에서 일본에 건너가 불교 전파에 공헌한 승려.
    '담휴': {'role': 'other'},  # 고려/고려 전기 - 고려전기 제16대 예종의 왕사로 추봉된 승려.
    '답본춘초': {'role': 'other'},  # 고대/삼국/백제 - 삼국시대 백제 멸망 후 왜국에서 대산하를 역임한 유민. 유신(遺臣).
    '당성': {'role': 'other'},  # 조선 - 조선 전기에, 개성부부유후, 공안부윤 등을 역임한 문신.
    '당원': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 때, 이찬 관등으로 중시를 역임한 통일신라의 관리.
    '당천': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 사찬을 역임한 장수.
    '대간지': {'role': 'other'},  # 고대/남북국 - 남북국시대 발해에서 산수화를 잘 그린 화가.
    '대건황': {'role': 'other'},  # 고대/남북국/발해 - 발해의 제12대(재위: 858년~871년) 왕.
    '대경한': {'role': 'other'},  # 고대/남북국/발해 - 남북국시대 흥요국의 관리였던 발해의 유민.
    '대고장': {'role': 'other'},  # 큰북［大鼓］을 제작하는 장인(匠人).
    '대곡': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 사도성 수복 당시의 장수.
    '대공': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 아찬 대렴과 함께 반란을 일으킨 관리.
    '대광현': {'role': 'other'},  # 고대/남북국/발해 - 고려 전기에, 발해에서 고려로 귀화한 왕족.
    '대굉림': {'role': 'other'},  # 고대/남북국/발해 - 남북국시대 발해의 제3대 문왕 대흠무의 아들인 왕자.
    '대구': {'role': 'scholar'},  # 고대/삼국 - 삼국시대 신라의 각간 위홍과 『삼대목』을 저술한 승려.
    '대당': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 일모산군 태수를 역임한 관리.
    '대도리경': {'role': 'other'},  # 고대/남북국/발해 - 고려전기 발해에서 고려로 귀화한 유민.
    '대도리행': {'role': 'other'},  # 고대/남북국/발해 - 남북국시대 발해의 제2대 무왕 대무예의 장남인 왕자.
    '대도수': {'role': 'other'},  # 고려/고려 전기 - 고려전기 중랑장, 장군 등을 역임한 관리. 무신.
    '대도행랑': {'role': 'other'},  # 고대/남북국/발해 - 고려전기 발해에서 고려로 귀화한 유민.
    '대렴': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 일길찬 대공과 함께 반란을 일으킨 관리.
    '대령후': {'role': 'other'},  # 고려/고려 전기 - 고려전기 제17대 인종의 둘째 아들인 왕자.
    '대륜': {'role': 'other'},  # 현대/대한민국 - 해방 이후 태고종 종정, 한국불교태고종 원로원장 등을 역임한 승려.
    '대명궁부인': {'role': 'other'},  # 고려 - 고려전기 제5대 경종의 제5왕비.
    '대명주원부인': {'role': 'other'},  # 고려 - 고려전기 제1대 태조의 제14왕비.
    '대목왕후': {'role': 'other'},  # 고려/고려 전기 - 고려전기 제4대 광종의 왕비.
    '대무신왕': {'role': 'other'},  # 고대/삼국/고구려 - 삼국시대 고구려 제3대(재위: 18~44) 왕.
    '대문': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라에서 대문의 난을 일으킨 고구려의 유민.
    '대문예': {'role': 'other'},  # 고대/남북국/발해 - 남북국시대 발해의 시조 대조영의 둘째 아들인 왕자.
    '대방공': {'role': 'other'},  # 고려/고려 전기 - 고려전기 제15대 숙종의 아들인 왕자.
    '대범': {'role': 'other'},  # 고대/남북국 - 삼국시대 신라에서 당나라와 인도로 건너가 유학하며 불법을 공부한 승려.
    '대복모': {'role': 'other'},  # 고대/남북국/발해 - 고려전기 발해에서 고려로 귀화한 유민.
    '대봉예': {'role': 'other'},  # 고대/남북국/발해 - 남북국시대 때, 하정사로 당나라에 방문했다가, 신라 사신과 발해 사신의 자리 다툼인 쟁장사
    '대서원부인': {'role': 'other'},  # 고려 - 고려전기 제1대 태조의 제19왕비.
    '대서지': {'role': 'other'},  # 고대/삼국/신라 - 신라의 제13대 왕, 미추이사금의 동생이자 제18대 실성이사금의 아버지로, 이찬에 임명된 
    '대세': {'role': 'other foreigner'},  # 고대/남북국 - 삼국시대 선술을 체득하기 위해 중국으로 건너간 신라 진평왕대의 귀족.
    '대소': {'role': 'other'},  # 고대/초기국가 - 부여의 제5대(재위:BCE.20~CE.22) 왕.
    '대승': {'role': 'other'},  # 고대/삼국 - 고구려 시대 낙랑군에 투항한 잠지락부의 족장.
    '대신덕': {'role': 'other'},  # 고대/남북국/발해 - 남북국시대 발해의 제10대 선왕의 아들인 왕자.
    '대심리': {'role': 'other'},  # 고대/남북국/발해 - 고려전기 발해에서 고려로 귀화한 유민.
    '대안': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 삼국 통일기 원효와 함께 활동했던 승려.
    '대야발': {'role': 'scholar'},  # 고대/남북국/발해 - 발해의 제1대 왕, 대조영의 동생으로, 『단기고사』를 저술한 왕족.
    '대양왕': {'role': 'other'},  # 고대/삼국/고구려 - 고구려의 마지막 왕, 보장왕의 아버지인 왕족.
    '대연': {'role': 'other'},  # 고려 - 남북국시대 삼중대사를 역임한 승려.
    '대연림': {'role': 'other'},  # 고대/남북국/발해 - 발해의 부흥국인 흥료국의 제1대 왕.
    '대연정': {'role': 'other'},  # 고대/남북국/발해 - 남북국시대 발해의 부흥국인 흥료국의 태사를 역임한 관리. 장수.
    '대우': {'role': 'scholar'},  # 조선 - 조선후기 『예수시왕생칠재의찬요』를 저술한 승려.
    '대운': {'role': 'other'},  # 조선 - 조선후기 도갑사 회성의 제자가 되어 법맥을 계승한 승려.
    '대원공': {'role': 'other'},  # 고려/고려 전기 - 고려전기 제15대 숙종의 다섯째 아들인 왕자.
    '대원균': {'role': 'other'},  # 고대/남북국/발해 - 고려전기 발해에서 고려로 귀화한 유민.
    '대원의': {'role': 'other'},  # 고대/남북국/발해 - 발해의 제4대(재위: 793년~794년) 왕.
    '대위해': {'role': 'other'},  # 고대/남북국/발해 - 발해의 제14대(재위: 894년~906년) 왕.
    '대유범': {'role': 'other'},  # 고대/남북국/발해 - 고려전기 발해에서 고려로 귀화한 유민.
    '대은': {'role': 'other'},  # 현대/대한민국 - 해방 이후 팔만대장경 번역위원회 위원, 동국역경원 역경위원 등을 역임한 승려. 포교사.
    '대의': {'role': 'other'},  # 현대/대한민국 - 해방 이후 대한불교총연합회 이사장, 한민족총회결성준비위원회 부회장 등을 역임한 승려.
    '대이진': {'role': 'other'},  # 고대/남북국/발해 - 발해의 제11대(재위: 830년~858년) 왕.
    '대인': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 고구려 낭비성 함락에 공헌한 장수.
    '대인선': {'role': 'other'},  # 발해의 제15대(재위: 906년~926년) 왕.
    '대일하': {'role': 'other'},  # 고대/남북국/발해 - 발해의 제2대 무왕 대무예의 사촌 형으로, 당과의 대립을 두려워하여 흑수말갈에 대한 선제공
    '대장': {'role': 'other'},  # 고대/남북국/통일신라 - 통일신라의 제29대 왕, 태종 무열왕의 후손으로, 이찬에 임명되어 중시 등을 역임한 종실.
    '대정': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 이찬으로 중시를 지낸 귀족.
    '대존': {'role': 'other'},  # 고대/남북국/통일신라 - 통일신라의 제54대 경명왕의 장인으로, 각간에서 성희대왕으로 추봉된 귀족.
    '대종': {'role': 'other'},  # 고려/고려 전기 - 고려의 제6대 왕, 성종의 아버지로, 예성선경대왕에 추존된 왕족.
    '대진림': {'role': 'other'},  # 고대/남북국/발해 - 남북국시대 때, 발해에서 조공사로 후당에 파견되었으나, 발해의 몰락으로 고려에 망명한 발해
    '대집성': {'role': 'other'},  # 고려/고려 후기 - 고려 후기, 대장군(大將軍), 어사대부(御史大夫), 수사공(守司空) 등을 역임한 관리이자 
    '대창발가': {'role': 'other'},  # 고대/남북국/발해 - 발해의 제2대 무왕 대무예의 동생으로, 당나라에 사신으로 가서 좌위위원외장군으로 임명된 발
    '대충': {'role': 'other'},  # 현대/대한민국 - 해방 이후 대한불교천태종 제2대 종정 등을 역임한 승려.
    '대토': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 아찬으로 당나라와 내통하려다 발각된 관리.
    '대통': {'role': 'other'},  # 고대/남북국 - 남북국시대 통일신라에서 당나라로 유학하며 불법을 공부한 승려.
    '대현': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 살찬으로 태대각간을 역임한 귀족.
    '대현석': {'role': 'other'},  # 고대/남북국/발해 - 발해의 제13대(재위: 871년~893년) 왕.
    '대화균': {'role': 'other'},  # 고대/남북국/발해 - 고려전기 발해에서 고려로 귀화한 유민.
    '대흔': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 때, 반란으로 왕위에 오른 신무왕이 죽고 문성왕이 즉위하자 이찬 김식과 함께 반
    '덕기': {'role': 'other'},  # 근대 - 일제강점기 범어사 주지, 임시정부 고문 등을 역임한 승려.
    '덕녕공주': {'role': 'other'},  # 고려/고려 후기 - 고려후기 제28대 충혜왕의 왕비.
    '덕래': {'role': 'other foreigner'},  # 고대/삼국/백제 - 삼국시대 일본조정에서 의약을 담당한 백제 출신의 의약인.
    '덕복': {'role': 'other'},  # 고대/남북국/통일신라 - 신라 문무왕 때 당에서 숙위로 활동하고, 귀국할 때 새로운 역법을 전한 인물.
    '덕비': {'role': 'other'},  # 고려 - 고려후기 제32대 우왕의 제7왕비.
    '덕소': {'role': 'other'},  # 고려 - 고려시대 선사, 대선사, 왕사 등을 역임한 승려.
    '덕안대군': {'role': 'other'},  # 조선/조선 전기 - 조선전기 제1대 태조의 여섯째 아들인 왕자.
    '덕양군': {'role': 'other'},  # 조선 - 조선전기 제11대 중종의 서자인 왕자.
    '덕양후': {'role': 'other'},  # 고려 - 고려후기 제20대 신종의 아들인 왕자.
    '덕연': {'role': 'other'},  # 고려/고려 전기 - 고려전기 제16대 예종의 왕사, 제17대 인종의 국사로 책봉된 승려.
    '덕원군': {'role': 'other'},  # 조선 - 조선전기 제7대 세조의 셋째 아들인 왕자.
    '덕자진': {'role': 'other foreigner'},  # 고대/삼국 - 삼국시대 일본왕 지토로부터 의박사 칭호를 받은 백제 출신의 의약인.
    '덕종': {'role': 'other'},  # 조선/조선 전기 - 조선 세조의 첫째 아들로, 왕세자로 책봉되었으나, 20세에 사망한 후 성종에 의해 추존된 
    '덕좌왕': {'role': 'other foreigner'},  # 고대/삼국/백제 - 삼국시대 일본 백제기의 시조.
    '덕지': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 삽량성전투에 참전한 장수.
    '덕진': {'role': 'other'},  # 근대 - 조선후기 경순(敬淳)과 더불어 당대의 뛰어난 선지식으로 불린 승려.
    '덕창': {'role': 'other'},  # 고려 - 고려전기 제16대 예종의 왕사를 역임한 승려.
    '덕혜옹주': {'role': 'other foreigner'},  # 근대 - 조선의 제26대 왕, 고종의 딸로, 일제에 의해 일본에서 교육을 받고, 대마도 번주의 아들
    '덕흥군': {'role': 'other'},  # 고려/고려 후기 - 고려 후기, 제26대 충선왕의 셋째 아들인 왕자.
    '도경유': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 금부도사, 평양서윤 등을 역임한 문신.
    '도금봉': {'role': 'other'},  # 현대 - 해방 이후 「상록수」, 「또순이」, 「토지」 등에 출연한 배우. 영화배우.
    '도길부': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 제조정방, 서북면도체찰사, 찬성사 등을 역임한 문신.
    '도대철': {'role': 'other'},  # 현대 - 한국전쟁 당시 강원도 양구의 949고지전투에 참전한 군인.
    '도도': {'role': 'other'},  # 고대/삼국/신라 - 신라 진흥왕대에 백제와 벌인 관산성전투 때 신라 편에 서서 활약한 지방 유력자.
    '도동음률': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라에 내항한 탐라국의 왕. 관리.
    '도두': {'role': 'other'},  # 고대/삼국/고구려 - 삼국시대 고구려 태조왕대 고구려에 투항한 갈사국의 왕족.
    '도등': {'role': 'other foreigner'},  # 고대/삼국/고구려 - 삼국시대 고구려에서 일본에 건너가 불교 전파에 공헌한 승려.
    '도령': {'role': 'other foreigner'},  # 고대/삼국/백제 - 삼국시대 백제에서 일본으로 건너가 불경을 공부한 승려.
    '도림': {'role': 'other'},  # 고대/삼국/고구려 - 삼국시대 고구려 밀사로 백제에 파견된 승려.
    '도모': {'role': 'other'},  # 고대/삼국/백제 - 삼국시대 백제의 시조.
    '도문': {'role': 'other'},  # 조선 - 조선후기 수호일품대승 칭호를 받고 개운사를 수호한 승려.
    '도미': {'role': 'other'},  # 고대/삼국/백제 - 삼국시대 백제 「도미설화」의 주인공.
    '도상봉': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 「한정」 · 「고궁」 · 「이조백자」 등의 작품을 그린 화가.
    '도생': {'role': 'other'},  # 고려 - 고려전기 법주사 주시, 승통, 금산사 주지 등을 역임한 승려.
    '도선': {'role': 'scholar'},  # 고대/남북국시대 - 남북국시대 통일신라의 『도선비기』, 『송악명당기』, 『도선답산가』 등을 저술한 승려.
    '도설지': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 급간지, 대등 등을 역임한 귀족.
    '도설지왕': {'role': 'other'},  # 고대/삼국/가야 - 대가야의 제3대(재위: ?~562년) 왕.
    '도성': {'role': 'other'},  # 고대/남북국 - 삼국시대 신라 『삼국유사』의 포산이성조와 관련된 승려.
    '도성기': {'role': 'other'},  # 고려/고려 후기 - 고려후기 낭장, 장군 등을 역임한 환관.
    '도성유': {'role': 'scholar'},  # 조선 - 조선 후기에, 『성리정학집』, 「체용각분도」, 「오경체용합일도」 등을 저술한 문신.
    '도신수': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 호조정랑, 함흥판관, 울산부사 등을 역임한 문신.
    '도신여': {'role': 'other'},  # 조선 - 조선 후기에, 용담현령, 예조정랑, 성균관사예 등을 역임한 문신.
    '도신징': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 강릉참봉, 용궁현감, 통훈대부 등을 역임한 문신.
    '도심': {'role': 'other foreigner'},  # 고대/삼국 - 삼국시대 백제에서 담혜 등과 일본으로 건너간 일본 최초의 승려.
    '도안': {'role': 'scholar'},  # 조선 - 조선 후기, 편양파의 주류 계보를 잇고 화엄학을 진흥시킨 학승으로 『월저당대사집』을 저술한
    '도엄': {'role': 'other foreigner'},  # 고대/삼국/백제 - 삼국시대 백제의 사신 은솔 수신 등과 일본에 파견된 승려.
    '도연': {'role': 'other'},  # 조선 - 조선후기 대둔사(大芚寺) 총오의 제자로 연담의 법맥을 계승한 승려.
    '도예종': {'role': 'other'},  # 현대/대한민국 - 대한민국 8·15광복 이후 민주화, 통일운동을 전개한 진보적 활동가.
    '도오': {'role': 'other'},  # 현대/대한민국 - 일제강점기 설곡의 검선일여비법을 전수받은 승려. 선무술가(禪武術家).
    '도옥': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 조천성전투에 참전한 최초의 호국 승려.
    '도원': {'role': 'other'},  # 고려 - 고려전기 우가승록을 역임한 승려.
    '도유호': {'role': 'scholar'},  # 현대 - 북한에서 함흥시립도서관장, 김일성종합대학의 교수와 고고학연구소장 등을 역임하였으며, 북한 
    '도육': {'role': 'other'},  # 고려 - 남북국시대 당나라로 유학가서 천태산을 순례한 승려.
    '도윤': {'role': 'other'},  # 고대/남북국 - 남북국시대 통일신라 사자산문의 승려.
    '도응': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 찬성사 등을 역임한 문신.
    '도응유': {'role': 'scholar'},  # 조선 - 조선 후기에, 이괄의 난이 발발하자 의병을 일으켰으며, 정묘호란 때 소모장으로 활동한 학자
    '도의': {'role': 'other foreigner'},  # 고대/남북국/통일신라 - 남북국시대 최초로 중국의 남종선을 신라에 전한 승려.
    '도인권': {'role': 'other foreigner'},  # 근대 - 일제강점기, 안악사건으로 옥고를 치르고 평양 3·1운동에 참여한 후 중국 상하이 대한민국 
    '도일': {'role': 'other'},  # 조선/조선 후기 - 조선후기 선암사 운수난야 지장시왕도, 선암사 선조암 신중도, 운주사 신중도 등을 그린 승려
    '도장': {'role': 'scholar foreigner'},  # 고대/삼국/백제 - 삼국시대 백제에서 일본으로 건너가 『성실론소』를 저술한 승려.
    '도절': {'role': 'other'},  # 고대/삼국/고구려 - 삼국시대 고구려 제2대 유리명왕의 첫째 태자.
    '도조': {'role': 'other'},  # 조선/조선 전기 - 조선의 제1대 왕, 태조의 조부로, 원나라에서 아버지의 천호 관직을 계승받았으며, 조선 건
    '도증': {'role': 'scholar'},  # 고대/남북국/통일신라 - 삼국시대 신라의 『금강반야경소』, 『인명입정리론소』 등을 저술한 승려.
    '도침': {'role': 'other'},  # 고대/삼국 - 삼국시대 백제의 재건을 주도하던 부흥운동가. 승려.
    '도한기': {'role': 'scholar'},  # 근대 - 조선 후기에, 『춘추의례』, 『사례절략』, 『심근강의』 등을 저술한 학자.
    '도현': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 승려로 견당사의 통역과 당나라 관공서와의 교섭 등을 담당한 역관.
    '도형': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 전적, 공조좌랑, 형조좌랑, 호조좌랑 등을 역임한 문신.
    '도화랑': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 때, 신라 진지왕의 혼령과 동침하여 아들 비형랑을 낳은 왕족.
    '도흔': {'role': 'other foreigner'},  # 고대/삼국/백제 - 삼국시대 백제 승려로, 오나라에서 백제로 오던 중 풍랑으로 표류하다 일본에 정착한 승려.
    '도흥': {'role': 'other'},  # 고려 - 고려후기 전라도도순문사, 원수, 양광도 상원수 등을 역임한 무신.
    '독고립': {'role': 'other'},  # 조선 - 조선후기 군자감판관, 호조참의 등을 역임한 무신.
    '독고성': {'role': 'other'},  # 조선/조선 후기 - 조선후기 병자호란 당시 의주성전투에 참전한 무신.
    '독고전': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 국경청년연맹 검사위원, 조공, 고려공산청년회 해외 연락원 등을 지낸 사회주의운동
    '독보': {'role': 'other'},  # 조선 - 조선후기 병자호란 때 명나라에 사신으로 파견된 승려.
    '돌고': {'role': 'other'},  # 고대/삼국/고구려 - 삼국시대 고구려 제13대 서천왕의 아들인 왕자.
    '동기달': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「강릉학산오독떼기」 전승자로 지정된 예능보유자.
    '동륜': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라 제24대 진흥왕의 첫째 아들인 왕자.
    '동명성왕': {'role': 'other'},  # 고대/삼국/고구려 - 고구려의 제1대(재위: BCE. 37~BCE. 19) 왕.
    '동산원부인': {'role': 'other'},  # 고려/고려 전기 - 고려전기 제1대 태조의 후비.
    '동석기': {'role': 'other'},  # 현대/대한민국 - 일제강점기 때, 함경남도 북청에서 최초의 그리스도 교회인 함전그리스도교회를 설립하였으며, 
    '동성왕': {'role': 'other'},  # 고대/삼국/백제 - 백제의 제24대(재위: 479년~501년) 왕.
    '동성자막고': {'role': 'other foreigner'},  # 고대/삼국/백제 - 삼국시대 백제의 덕솔로서 일본에 파견된 관리.
    '동소': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 주재성 성주를 역임한 장수.
    '동수': {'role': 'other'},  # 고대/삼국/고구려 - 삼국시대 모용부에서 고구려에 귀화한 유민.
    '동양원부인': {'role': 'other'},  # 고려/고려 전기 - 고려전기 제1대 태조의 제9왕비.
    '동완': {'role': 'scholar'},  # 한국외국어대학교와 고려대학교에서 교수 등을 역임하였으며, 『노한사전』, 『소련 청소년과 러
    '동천왕': {'role': 'other'},  # 고구려의 제11대(재위: 227년~247년) 왕.
    '동타천': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 북한산성 성주를 역임한 지방관.
    '동풍신': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 함경북도에서 전개된 독립만세운동에 참여한 독립운동가.
    '두경승': {'role': 'other'},  # 고려후기 서북면병마사, 평장사, 문하시중 등을 역임한 무신.
    '두로': {'role': 'other'},  # 고대/삼국/고구려 - 삼국시대 고구려 제5대 모본왕을 시해한 관리.
    '두방루': {'role': 'other'},  # 고대/삼국/고구려 - 삼국시대 고구려 적봉진전투에 참전한 장수.
    '두사지': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라에서 고구려 사절로 가는 김춘추에게 청포 300포를 준 관리.
    '두삼': {'role': 'other'},  # 근대/개항기 - 조선후기 백련사 괘불도, 남양주 흥국사 팔상도 등의 불화를 제작한 승려. 화승.
    '두선': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 아찬으로 석문전투에 참전한 관리. 장군.
    '두운': {'role': 'other'},  # 조선 - 조선후기 전평과 대흥사 만일암을 중창한 승려.
    '두질': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 군사(軍師)로 사비성전투에 참전한 관리.
    '두훈': {'role': 'other'},  # 조선/조선 후기 - 조선후기 법주사 괘불도, 통도사 괘불도 등을 그린 승려. 화승.
    '둔륜': {'role': 'scholar'},  # 고대/남북국 - 삼국시대 신라의 『승만경소』, 『금광명경약기』, 『아미타경소』 등을 저술한 승려.
    '득오': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 「모죽지랑가」를 지은 낭도.
    '득원': {'role': 'other'},  # 조선 - 조선후기 지리산 용수암에서 수년간 1일 1식으로 수행한 승려.
    '등린': {'role': 'other'},  # 조선 - 조선후기 석왕사 정연의 제자로 궤홍의 법맥을 계승한 승려.
    '류경채': {'role': 'scholar'},  # 서울대학교 서양화과 교수, 창작미술협회 회장 등을 역임하였으며, 「선(船)」, 「폐림지 근
    '류금렬': {'role': 'other'},  # 근대/일제강점기 | 현대 - 해방 이후 북한에서 원산필수품공장 미술가로 활동한 공예가. 염색공예가.
    '류방택': {'role': 'scholar'},  # 조선/조선 전기 - 고려 후기, 서운관(書雲觀)의 판사(判事)를 역임하고 조선 초기에 권근(權近)과 함께 천상
    '류시훈': {'role': 'other foreigner'},  # 근대 - 일제강점기 때, 중국에서 조선민족혁명당의 지하공작에 참여하였고, 광복군에서 대적선전공작, 
    '류인': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 「파란 Ⅰ」 · 「흙: 난지도」 · 「급행열차: 시대의 변(辯)」 등의 작품을 
    '류택윤': {'role': 'other'},  # 근대/일제강점기 | 현대 - 해방 이후 「개구리잉크단지」, 「강냉이탁상등」, 「포도잉크단지」 등을 제작한 공예가. 석공
    '류형기': {'role': 'other'},  # 현대/대한민국 - 일제강점기와 해방 후 1950년대에, 기독교교육운동, 문서선교운동, 교회 재건과 복구 운동
    '류홍': {'role': 'other'},  # 현대/대한민국 - 경성방직 도감독, 고려방직 이사, 유관순열사기념사업회 회장, 제2·4·6대 국회의원 등을 
    '리영희': {'role': 'other'},  # 현대/대한민국 - 대한민국의 언론인 겸 사회운동가.
    '마건': {'role': 'other'},  # 근대/일제강점기 - 일제강점기에 적기단 결성 및 조선공산당 만주총국에서 활동한 사회주의 운동가.
    '마군후': {'role': 'scholar'},  # 조선/조선 후기 - 조선후기 「촌녀채총도」, 「수하승려도」, 「묘도」 등의 작품을 그린 화가.
    '마나': {'role': 'other'},  # 고대/삼국/백제 - 삼국시대 백제의 사신으로 왜에 파견된 장수.
    '마라난타': {'role': 'other'},  # 고대/삼국/백제 - 삼국시대 백제에 불교를 최초로 전한 인도의 승려.
    '마려': {'role': 'other'},  # 고대/삼국/백제 - 삼국시대 때, 백제의 건국 시조인 온조왕을 보좌한 관리.
    '마로': {'role': 'other'},  # 고대/삼국/백제 - 삼국시대 백제의 중좌평을 역임한 장수.
    '마리': {'role': 'other'},  # 고대/삼국/고구려 - 삼국시대 고구려 건국 초기 오이, 협보와 함께 많은 공적을 세운 관리. 공로자.
    '마명': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 노동총동맹의 중앙집행위원, 북풍회 집행위원 등을 역임한 노동운동가.
    '마무': {'role': 'other'},  # 고대/삼국/백제 - 삼국시대 백제의 시덕, 나솔 등을 역임한 관리.
})
        
        # API + Wikipedia로부터 자동 수집된 인물 데이터
self.persons.update({
    '가군': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%80%EA%B5%B0'},  # 고대/삼국 - 삼국시대 때, 고구려 장안성 축성의 책임을 맡았던 관리. | Wiki: 환의 선형 작용이 주어진 아벨 군
    '가귀': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B7%80%EB%A9%B8%EC%9D%98_%EC%B9%BC%EB%82%A0'},  # 고대/삼국 - 삼국시대 때, 신라에서 『화엄경의강』, 『심원장』 등을 저술한 승려. | Wiki: 일본의 만화
    '가라포고이': {'role': 'other foreigner', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%80%EB%9D%BC%ED%8F%AC%EA%B3%A0%EC%9D%B4'},  # 고대/삼국 - 삼국시대 때, 일본에 귀화한 신라의 유민.
    '가루': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%80%EB%A3%A8'},  # 고대/삼국 - 삼국시대 때, 대상(大相) 등을 역임하다 고구려 멸망 후 부흥운동에 참여한 고구려의 귀족.
    '가마': {'role': 'other foreigner', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%80%EB%A7%88'},  # 고대/삼국 - 삼국시대 때, 백제에서 일본으로 파견된 사신. | Wiki: 사람의 힘을 이용하는 운송 수단
    '가서일': {'role': 'other foreigner', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%80%EC%84%9C%EC%9D%BC'},  # 고대/삼국 - 삼국시대 때, 일본에서 활약한 고구려 출신의 화가.
    '가실': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%80%EC%8B%A4'},  # 고대/남북국 - 삼국시대 때, 신라의 사량부 출신으로 변방에서 복무한 군인. | Wiki: 신라의 군인
    '가실왕': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%80%EC%8B%A4%EC%99%95'},  # 고대/삼국/가야 - 가야의 제7대(재위: 421년~451년) 왕.
    '각가': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%81%EA%B0%80'},  # 고대/삼국 - 삼국시대 때, 백제의 좌평 등을 역임한 귀족. | Wiki: 백제의 귀족이자, 관료이다
    '각굉': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B5%89'},  # 고려 - 고려 후기에, 『나옹화상어록』, 『나옹화상행장』 등을 저술한 승려. | Wiki: 위키미디어 동음이의어 문서
    '각덕': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%81%EB%8D%95'},  # 고대/삼국/신라 - 삼국시대 때, 양나라에 유학한 신라의 승려.
    '각민': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%BA%90%EB%82%98%EB%8B%A4'},  # 조선 - 조선 후기에, 청허계 정관문파로 『해의』 등을 저술한 승려. | Wiki: 북아메리카의 국가
    '각복모': {'role': 'other foreigner', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%81%EB%B3%B5%EB%AA%A8'},  # 고대/삼국 - 삼국시대 때, 백제의 멸망 후 일본으로 망명한 귀족. | Wiki: 백제의 귀족 (?–?)
    '각성': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%81%EC%84%B1'},  # 조선 - 조선시대 때, 판선교도총섭, 팔도도총섭, 규정도총섭 등을 역임한 승려. | Wiki: 자극에 반응을 보이는 생리적, 심리적 상태
    '각안': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EB%AC%B8%EA%B4%91_(%EC%8A%B9%EB%A0%A4)'},  # 조선/조선 후기 - 조선 후기에, 『동사열전』, 『범해선사유고』 등을 저술한 승려.
    '각우': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%95%BC%EC%9A%B4'},  # 고려 - 고려 후기에, 『자경문』을 저술한 승려. | Wiki: 고려 말의 고승
    '각운': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%95%95%EC%9A%B4'},  # 고려 - 고려 후기에, 『경덕전등록』을 중간한 승려.
    '각웅': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%9E%A5%EC%98%81%EC%8B%A4'},  # 고려/고려 후기 - 고려 후기에, 나옹 혜근의 제자로 서기의 직무를 담당한 승려. | Wiki: 조선의 과학자 (?–?)
    '각유': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%9C%A0_(%EC%84%B1%EC%94%A8)'},  # 고려 - 고려 후기에, 경주 기림사 주지, 대선사 등을 역임한 승려. | Wiki: 한국의 성씨
    '각절왕': {'role': 'other foreigner', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EB%AC%B4%EA%B5%90%EC%A0%88'},  # 고대/삼국 - 삼국시대 때, 일본의 『신찬성씨록』에 전하는 신라의 왕.
    '각종': {'role': 'other foreigner', 'wikipedia': 'https://ko.wikipedia.org/wiki/%ED%95%9C%ED%95%9C%EB%A0%B9'},  # 고대/삼국 - 삼국시대 때, 백제의 사비성 함락 사실을 일본 야마토 조정에 보고한 승려. | Wiki: 중국인들이 한국과 관련된 한류 컨텐츠를 제한하는 것 외
    '각훈': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%ED%95%B4%EB%8F%99%EA%B3%A0%EC%8A%B9%EC%A0%84'},  # 고려 - 고려 후기에, 『해동고승전』을 저술한 승려. | Wiki: 삼국 시대에 활약했던 승려들의 열전을 모아 놓은 책
    '간왕': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%84%EC%99%95_(%EB%B0%9C%ED%95%B4)'},  # 고대/남북국/발해 - 발해의 제9대(재위: 817년~818년) 왕. | Wiki: 발해의 제9대 국왕 (?~818)
    '간위거': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EB%A7%88%EC%97%AC%EC%99%95'},  # 고대/초기국가 - 부여의 제10대(재위: 2세기~3세기) 왕.
    '간진': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EB%AA%A8%EB%A6%AC%EC%85%94%EC%8A%A4'},  # 고대/남북국/통일신라 - 신라 진평왕대 곡물 수송을 담당한 왕경 출신의 관리. | Wiki: 아프리카의 섬 나라
    '갈로맹광': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%88%EB%A7%8C%EB%A1%9C'},  # 고대/삼국 - 삼국시대 때, 고구려 원정군의 사령관으로 활약한 장수. | Wiki: 고구려의 장수 (?–?)
    '갈홍기': {'role': 'other foreigner', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%88%ED%99%8D%EA%B8%B0'},  # 근대/일제강점기 - 일제강점기 때, 일본기독교 조선감리교단 연성국장, 일본기독교 조선교단의 종교교육국장 등으로 | Wiki: 일제강점기, 대한민국의 목회자 (1906–1989)
    '감경인': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%ED%98%95%EC%9D%98_%EA%B0%90%EA%B2%BD'},  # 조선 - 조선시대 때, 여도만호, 내금위, 정략장군 등을 역임한 무신.
    '강감찬': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EA%B0%90%EC%B0%AC'},  # 고려 전기에, 서북면행영도통사, 상원수대장군, 문하시중 등을 역임한 문신. | Wiki: 고려의 문인 (948-1031)
    '강거효': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%98%88%EC%A2%85%EC%8B%A4%EB%A1%9D'},  # 조선/조선 전기 - 조선 전기에, 예문관검열, 가예조좌랑, 통훈대부 등을 역임한 문신. | Wiki: 조선 예종 시대의 역사를 기록한 실록
    '강견': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%8B%A0%EC%96%B8%ED%98%B8'},  # 조선/조선 전기 - 조선 전기에, 서인들의 사주를 받아 기축옥사 때 최영경이 정여립과 연루되어 있다고 무고한 
    '강겸': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EB%B3%B4%EA%B2%B8'},  # 조선 - 조선 전기에, 예조좌랑, 병조정랑, 장령 등을 역임한 문신. | Wiki: 한국의 유튜버 및 아프리카TV BJ
    '강경대': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EA%B2%BD%EB%8C%80'},  # 현대/대한민국 - 대한민국의 학생운동가, 시민운동가. | Wiki: 대한민국의 학생운동가
    '강경서': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EA%B2%BD%EC%9D%8D'},  # 조선 - 조선 전기에, 사헌부집의, 대사간 등을 역임한 문신. | Wiki: 충청남도 논산시의 하위행정구역
    '강경선': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EA%B2%BD%EC%84%A0'},  # 근대/일제강점기 - 일제강점기 때, 대한적십자회 상의원, 대한민국임시정부 교민단 총무, 한국유일독립당 집행위원 | Wiki: 논산시의 채운역과 연무대역을 잇는 한국철도공사의 철도 
    '강경애': {'role': 'novelist', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EA%B2%BD%EC%95%A0'},  # 근대 - 일제강점기 때, 「소금」, 「인간 문제」, 「해고」 등을 저술한 소설가. | Wiki: 한국의 문학가, 인권 운동가 (1906–1944)
    '강계식': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EA%B3%84%EC%8B%9D'},  # 현대/대한민국 - 해방 이후 「붉은 장갑」, 「원술랑」, 「한강은 흐른다」 등에 출연한 배우. | Wiki: 대한민국의 배우 (1917–2000)
    '강고': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EB%95%85%EA%B0%95%EC%95%84%EC%A7%80'},  # 고대/남북국 - 남북국시대 때, 통일신라의 분황사 약사여래상을 주조한 장인. | Wiki: 땅강아지과 땅강아지속의 곤충
    '강곤': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%95%84%EC%9D%B4%ED%85%9C_(%EB%93%9C%EB%9D%BC%EB%A7%88)'},  # 조선/조선 전기 - 조선 전기에, 인수부윤, 충청도도절제사, 영안남도절도사 등을 역임한 무신.
    '강공훤': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%ED%83%9C%EC%A1%B0_(%EA%B3%A0%EB%A0%A4)'},  # 고대/삼국 - 남북국시대 때, 시중, 대장군, 대상 등을 역임한 무신. | Wiki: 고려의 초대 임금 (877–943)
    '강구려': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EA%B5%AC%ED%95%AD'},  # 고대/삼국 - 삼국시대 때, 왜에 억류된 신라 왕족 미사흔의 환국을 호송했던 박제상을 보좌한 신라의 관리
    '강구손': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EA%B7%80%EC%86%90'},  # 조선/조선 전기 - 조선 전기에, 도승지, 경기도관찰사, 우의정 등을 역임한 문신. | Wiki: 조선 초기의 문신
    '강국승': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%9D%B4%EC%8A%B9%EB%A7%8C'},  # 고려/고려 후기 - 고려 후기, 무오정변을 통해 최씨 무신정권을 붕괴시켜 위사보좌공신에 책록된 공신이자 무신. | Wiki: 대한민국의 제1·2·3대 대통령, 독립운동가, 교육가 
    '강국진': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EA%B5%AD%EC%A7%84'},  # 현대/대한민국 - 「비닐우산과 촛불이 있는 해프닝」, 「한강변의 타살」, 「역사의 빛」 등의 작품을 그린 화 | Wiki: 위키미디어 동음이의어 문서
    '강궁진': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EA%B6%81%EC%A7%84'},  # 고려/고려 전기 - 고려 전기, 강감찬의 아버지이자 금주 일대의 토착세력으로, 고려 태조 왕건을 섬겼던 호족  | Wiki: 후삼국 시대의 호족
    '강귀례': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%A7%84%EC%A3%BC%EA%B2%80%EB%AC%B4'},  # 현대 - 「진주 검무」의 전승자로 지정된 예능 보유자. | Wiki: 晋州劍舞
    '강규찬': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EA%B7%9C%EC%B0%AC'},  # 근대 - 일제강점기 때, 105인 사건 등과 관련된 목사.
    '강규환': {'role': 'scholar', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%95%A0%EB%B9%84%EA%B7%9C%ED%99%98'},  # 조선/조선 후기 - 조선 후기 경종~영종대 활동한 노론-호론계 출신의 학자이자 영남안무사 종사관, 장릉참봉 등 | Wiki: 2020년 영화
    '강극성': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EC%95%88%EC%82%B0%ED%96%A5%EA%B5%90%EC%A7%80'},  # 조선/조선 전기 - 조선 전기에, 지평, 부교리, 교리 등을 역임한 문신.
    '강근호': {'role': 'other', 'wikipedia': 'https://ko.wikipedia.org/wiki/%EA%B0%95%EA%B7%BC%ED%98%B8'},  # 근대/일제강점기 - 일제강점기, 청산리 대첩에 참전한 독립운동가. | Wiki: 한국의 독립운동가 (1888–1960)
})
        
        # API + Wikipedia로부터 자동 수집된 인물 데이터
self.persons.update({
    '가군': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 고구려 장안성 축성의 책임을 맡았던 관리.
    '가귀': {'role': 'scholar'},  # 고대/삼국 - 삼국시대 때, 신라에서 『화엄경의강』, 『심원장』 등을 저술한 승려.
    '가라포고이': {'role': 'other foreigner'},  # 고대/삼국 - 삼국시대 때, 일본에 귀화한 신라의 유민.
    '가루': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 대상(大相) 등을 역임하다 고구려 멸망 후 부흥운동에 참여한 고구려의 귀족.
    '가마': {'role': 'other foreigner'},  # 고대/삼국 - 삼국시대 때, 백제에서 일본으로 파견된 사신.
    '가서일': {'role': 'other foreigner'},  # 고대/삼국 - 삼국시대 때, 일본에서 활약한 고구려 출신의 화가.
    '가실': {'role': 'other'},  # 고대/남북국 - 삼국시대 때, 신라의 사량부 출신으로 변방에서 복무한 군인.
    '가실왕': {'role': 'other'},  # 고대/삼국/가야 - 가야의 제7대(재위: 421년~451년) 왕.
    '각가': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 백제의 좌평 등을 역임한 귀족.
    '각굉': {'role': 'scholar'},  # 고려 - 고려 후기에, 『나옹화상어록』, 『나옹화상행장』 등을 저술한 승려.
    '각덕': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 때, 양나라에 유학한 신라의 승려.
    '각민': {'role': 'scholar'},  # 조선 - 조선 후기에, 청허계 정관문파로 『해의』 등을 저술한 승려.
    '각복모': {'role': 'other foreigner'},  # 고대/삼국 - 삼국시대 때, 백제의 멸망 후 일본으로 망명한 귀족.
    '각성': {'role': 'other'},  # 조선 - 조선시대 때, 판선교도총섭, 팔도도총섭, 규정도총섭 등을 역임한 승려.
    '각안': {'role': 'scholar'},  # 조선/조선 후기 - 조선 후기에, 『동사열전』, 『범해선사유고』 등을 저술한 승려.
    '각우': {'role': 'scholar'},  # 고려 - 고려 후기에, 『자경문』을 저술한 승려.
    '각운': {'role': 'other'},  # 고려 - 고려 후기에, 『경덕전등록』을 중간한 승려.
    '각웅': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 나옹 혜근의 제자로 서기의 직무를 담당한 승려.
    '각유': {'role': 'other'},  # 고려 - 고려 후기에, 경주 기림사 주지, 대선사 등을 역임한 승려.
    '각절왕': {'role': 'other foreigner'},  # 고대/삼국 - 삼국시대 때, 일본의 『신찬성씨록』에 전하는 신라의 왕.
    '각종': {'role': 'other foreigner'},  # 고대/삼국 - 삼국시대 때, 백제의 사비성 함락 사실을 일본 야마토 조정에 보고한 승려.
    '각훈': {'role': 'scholar'},  # 고려 - 고려 후기에, 『해동고승전』을 저술한 승려.
    '간왕': {'role': 'other'},  # 고대/남북국/발해 - 발해의 제9대(재위: 817년~818년) 왕.
    '간위거': {'role': 'other'},  # 고대/초기국가 - 부여의 제10대(재위: 2세기~3세기) 왕.
    '간진': {'role': 'other'},  # 고대/남북국/통일신라 - 신라 진평왕대 곡물 수송을 담당한 왕경 출신의 관리.
    '갈로맹광': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 고구려 원정군의 사령관으로 활약한 장수.
    '갈홍기': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 때, 일본기독교 조선감리교단 연성국장, 일본기독교 조선교단의 종교교육국장 등으로
    '감경인': {'role': 'other'},  # 조선 - 조선시대 때, 여도만호, 내금위, 정략장군 등을 역임한 무신.
    '강감찬': {'role': 'other'},  # 고려 전기에, 서북면행영도통사, 상원수대장군, 문하시중 등을 역임한 문신.
    '강거효': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 예문관검열, 가예조좌랑, 통훈대부 등을 역임한 문신.
    '강견': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 서인들의 사주를 받아 기축옥사 때 최영경이 정여립과 연루되어 있다고 무고한 
    '강겸': {'role': 'other'},  # 조선 - 조선 전기에, 예조좌랑, 병조정랑, 장령 등을 역임한 문신.
    '강경대': {'role': 'other'},  # 현대/대한민국 - 대한민국의 학생운동가, 시민운동가.
    '강경서': {'role': 'other'},  # 조선 - 조선 전기에, 사헌부집의, 대사간 등을 역임한 문신.
    '강경선': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 대한적십자회 상의원, 대한민국임시정부 교민단 총무, 한국유일독립당 집행위원
    '강경애': {'role': 'novelist'},  # 근대 - 일제강점기 때, 「소금」, 「인간 문제」, 「해고」 등을 저술한 소설가.
    '강계식': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「붉은 장갑」, 「원술랑」, 「한강은 흐른다」 등에 출연한 배우.
    '강고': {'role': 'other'},  # 고대/남북국 - 남북국시대 때, 통일신라의 분황사 약사여래상을 주조한 장인.
    '강곤': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 인수부윤, 충청도도절제사, 영안남도절도사 등을 역임한 무신.
    '강공훤': {'role': 'other'},  # 고대/삼국 - 남북국시대 때, 시중, 대장군, 대상 등을 역임한 무신.
    '강구려': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 왜에 억류된 신라 왕족 미사흔의 환국을 호송했던 박제상을 보좌한 신라의 관리
    '강구손': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 도승지, 경기도관찰사, 우의정 등을 역임한 문신.
    '강국승': {'role': 'other'},  # 고려/고려 후기 - 고려 후기, 무오정변을 통해 최씨 무신정권을 붕괴시켜 위사보좌공신에 책록된 공신이자 무신.
    '강국진': {'role': 'scholar'},  # 현대/대한민국 - 「비닐우산과 촛불이 있는 해프닝」, 「한강변의 타살」, 「역사의 빛」 등의 작품을 그린 화
    '강궁진': {'role': 'other'},  # 고려/고려 전기 - 고려 전기, 강감찬의 아버지이자 금주 일대의 토착세력으로, 고려 태조 왕건을 섬겼던 호족 
    '강귀례': {'role': 'other'},  # 현대 - 「진주 검무」의 전승자로 지정된 예능 보유자.
    '강규찬': {'role': 'other'},  # 근대 - 일제강점기 때, 105인 사건 등과 관련된 목사.
    '강규환': {'role': 'scholar'},  # 조선/조선 후기 - 조선 후기 경종~영종대 활동한 노론-호론계 출신의 학자이자 영남안무사 종사관, 장릉참봉 등
    '강극성': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 지평, 부교리, 교리 등을 역임한 문신.
    '강근호': {'role': 'other'},  # 근대/일제강점기 - 일제강점기, 청산리 대첩에 참전한 독립운동가.
})
        
        # API로부터 자동 수집된 인물 데이터
self.persons.update({
    '가군': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 고구려 장안성 축성의 책임을 맡았던 관리.
    '가귀': {'role': 'scholar'},  # 고대/삼국 - 삼국시대 때, 신라에서 『화엄경의강』, 『심원장』 등을 저술한 승려.
    '가라포고이': {'role': 'other foreigner'},  # 고대/삼국 - 삼국시대 때, 일본에 귀화한 신라의 유민.
    '가루': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 대상(大相) 등을 역임하다 고구려 멸망 후 부흥운동에 참여한 고구려의 귀족.
    '가마': {'role': 'other foreigner'},  # 고대/삼국 - 삼국시대 때, 백제에서 일본으로 파견된 사신.
    '가서일': {'role': 'other foreigner'},  # 고대/삼국 - 삼국시대 때, 일본에서 활약한 고구려 출신의 화가.
    '가실': {'role': 'other'},  # 고대/남북국 - 삼국시대 때, 신라의 사량부 출신으로 변방에서 복무한 군인.
    '가실왕': {'role': 'other'},  # 고대/삼국/가야 - 가야의 제7대(재위: 421년~451년) 왕.
    '각가': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 백제의 좌평 등을 역임한 귀족.
    '각굉': {'role': 'scholar'},  # 고려 - 고려 후기에, 『나옹화상어록』, 『나옹화상행장』 등을 저술한 승려.
    '각덕': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 때, 양나라에 유학한 신라의 승려.
    '각민': {'role': 'scholar'},  # 조선 - 조선 후기에, 청허계 정관문파로 『해의』 등을 저술한 승려.
    '각복모': {'role': 'other foreigner'},  # 고대/삼국 - 삼국시대 때, 백제의 멸망 후 일본으로 망명한 귀족.
    '각성': {'role': 'other'},  # 조선 - 조선시대 때, 판선교도총섭, 팔도도총섭, 규정도총섭 등을 역임한 승려.
    '각안': {'role': 'scholar'},  # 조선/조선 후기 - 조선 후기에, 『동사열전』, 『범해선사유고』 등을 저술한 승려.
    '각우': {'role': 'scholar'},  # 고려 - 고려 후기에, 『자경문』을 저술한 승려.
    '각운': {'role': 'other'},  # 고려 - 고려 후기에, 『경덕전등록』을 중간한 승려.
    '각웅': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 나옹 혜근의 제자로 서기의 직무를 담당한 승려.
    '각유': {'role': 'other'},  # 고려 - 고려 후기에, 경주 기림사 주지, 대선사 등을 역임한 승려.
    '각절왕': {'role': 'other foreigner'},  # 고대/삼국 - 삼국시대 때, 일본의 『신찬성씨록』에 전하는 신라의 왕.
    '각종': {'role': 'other foreigner'},  # 고대/삼국 - 삼국시대 때, 백제의 사비성 함락 사실을 일본 야마토 조정에 보고한 승려.
    '각훈': {'role': 'scholar'},  # 고려 - 고려 후기에, 『해동고승전』을 저술한 승려.
    '간왕': {'role': 'other'},  # 고대/남북국/발해 - 발해의 제9대(재위: 817년~818년) 왕.
    '간위거': {'role': 'other'},  # 고대/초기국가 - 부여의 제10대(재위: 2세기~3세기) 왕.
    '간진': {'role': 'other'},  # 고대/남북국/통일신라 - 신라 진평왕대 곡물 수송을 담당한 왕경 출신의 관리.
    '갈로맹광': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 고구려 원정군의 사령관으로 활약한 장수.
    '갈홍기': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 때, 일본기독교 조선감리교단 연성국장, 일본기독교 조선교단의 종교교육국장 등으로 활동하면서 일본제국주...
    '감경인': {'role': 'other'},  # 조선 - 조선시대 때, 여도만호, 내금위, 정략장군 등을 역임한 무신.
    '강감찬': {'role': 'other'},  # 고려 전기에, 서북면행영도통사, 상원수대장군, 문하시중 등을 역임한 문신.
    '강거효': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 예문관검열, 가예조좌랑, 통훈대부 등을 역임한 문신.
    '강견': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 서인들의 사주를 받아 기축옥사 때 최영경이 정여립과 연루되어 있다고 무고한 유생.
    '강겸': {'role': 'other'},  # 조선 - 조선 전기에, 예조좌랑, 병조정랑, 장령 등을 역임한 문신.
    '강경대': {'role': 'other'},  # 현대/대한민국 - 대한민국의 학생운동가, 시민운동가.
    '강경서': {'role': 'other'},  # 조선 - 조선 전기에, 사헌부집의, 대사간 등을 역임한 문신.
    '강경선': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 대한적십자회 상의원, 대한민국임시정부 교민단 총무, 한국유일독립당 집행위원 등을 역임한 독립운동가.
    '강경애': {'role': 'novelist'},  # 근대 - 일제강점기 때, 「소금」, 「인간 문제」, 「해고」 등을 저술한 소설가.
    '강계식': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「붉은 장갑」, 「원술랑」, 「한강은 흐른다」 등에 출연한 배우.
    '강고': {'role': 'other'},  # 고대/남북국 - 남북국시대 때, 통일신라의 분황사 약사여래상을 주조한 장인.
    '강곤': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 인수부윤, 충청도도절제사, 영안남도절도사 등을 역임한 무신.
    '강공훤': {'role': 'other'},  # 고대/삼국 - 남북국시대 때, 시중, 대장군, 대상 등을 역임한 무신.
    '강구려': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 왜에 억류된 신라 왕족 미사흔의 환국을 호송했던 박제상을 보좌한 신라의 관리.
    '강구손': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 도승지, 경기도관찰사, 우의정 등을 역임한 문신.
    '강국승': {'role': 'other'},  # 고려/고려 후기 - 고려 후기, 무오정변을 통해 최씨 무신정권을 붕괴시켜 위사보좌공신에 책록된 공신이자 무신.
    '강국진': {'role': 'scholar'},  # 현대/대한민국 - 「비닐우산과 촛불이 있는 해프닝」, 「한강변의 타살」, 「역사의 빛」 등의 작품을 그린 화가.
    '강궁진': {'role': 'other'},  # 고려/고려 전기 - 고려 전기, 강감찬의 아버지이자 금주 일대의 토착세력으로, 고려 태조 왕건을 섬겼던 호족 · 공신.
    '강귀례': {'role': 'other'},  # 현대 - 「진주 검무」의 전승자로 지정된 예능 보유자.
    '강규찬': {'role': 'other'},  # 근대 - 일제강점기 때, 105인 사건 등과 관련된 목사.
    '강규환': {'role': 'scholar'},  # 조선/조선 후기 - 조선 후기 경종~영종대 활동한 노론-호론계 출신의 학자이자 영남안무사 종사관, 장릉참봉 등을 지낸 문신.
    '강극성': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 지평, 부교리, 교리 등을 역임한 문신.
    '강근호': {'role': 'other'},  # 근대/일제강점기 - 일제강점기, 청산리 대첩에 참전한 독립운동가.
    '강기덕': {'role': 'other'},  # 근대 - 일제강점기 때, 3·1운동의 기획과 실행에 가담한 민족대표 48인 중 한 사람으로, 학생 대표로서 서울 학생 제2차 독립만...
    '강기동': {'role': 'other foreigner'},  # 근대/대한제국기 - 대한제국기 때, 일본헌병보조원으로 위장 귀순하여 포로의병들을 석방하고 무기를 탈취해 항일의병투쟁을 전개한 의병장.
    '강기운': {'role': 'other'},  # 근대 - 일제강점기 때, 국민회에서 활동하며 독립군과 군자금 모집 및 밀정색출 작업을 전개한 독립운동가.
    '강기찬': {'role': 'other'},  # 근대 - 일제강점기 때, 제주에서 독서회를 조직하고 일인상품불매운동을 전개하는 등 항일계몽운동을 전개한 독립운동가.
    '강난형': {'role': 'other'},  # 조선 - 조선 후기에, 형조판서, 한성부판윤, 황해도관찰사 등을 역임한 문신.
    '강남중': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 김창환과 박유전의 제자로 원각사와 광무대에서 활약한 남도소리의 명창.
    '강달영': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 조선노농총동맹 중앙위원, 제2차 조선공산당 책임비서 등을 역임한 사회주의 운동가.
    '강달주': {'role': 'other'},  # 근대 - 대한제국기 때, 심남일 의진에서 후군장으로 활약하다 투옥되었으며, 출감 후 나주군의 독립운동에 은밀히 참여한 독립운동가.
    '강대성': {'role': 'other'},  # 근대 - 1890∼1954. 갱정유도(更定儒道)의 제1대 교조.
    '강대수': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 호조좌랑, 예조정랑, 병조참의 등을 역임한 문신.
    '강대적': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 병자호란 당시 청군에 대적해서 싸운 의병장.
    '강덕룡': {'role': 'other'},  # 조선 - 조선시대 때, 함창현감, 장기현감 등을 역임한 무신.
    '강도근': {'role': 'other'},  # 현대/대한민국 - 판소리의 전승자로 지정된 예능 보유자.
    '강도순절인': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 병자호란으로 강화가 함락되자 순절한 관리.
    '강도영': {'role': 'other'},  # 근대 - 개항기 때, 우리나라에서 3번째로 사제 서품을 받은 신부.
    '강동진': {'role': 'scholar foreigner'},  # 근대 - 「일본의 조선지배정책사 연구」, 「한국노동조합운동사」 등을 저술한 역사학자.
    '강두안': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 대구사범학교에서 항일비밀결사인 문예부를 조직해 기관잡지인 『학생』, 『반딧불』 등을 발간하였고,...
    '강로': {'role': 'other'},  # 근대 - 조선 후기에, 사간원대사간, 병조판서, 좌의정 등을 역임한 문신.
    '강린': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 교리, 부수찬, 함경도어사 등을 역임한 문신.
    '강매': {'role': 'scholar'},  # 근대/일제강점기 - 일제강점기 때, 『조선문법제요』, 『잘 뽑은 조선말과 글의 본』 등을 저술한 국어학자.
    '강맹경': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 예문관제학, 의정부우참찬, 좌찬성 등을 역임한 문신.
    '강명규': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 중국 만주에서 활약한 독립운동가.
    '강명길': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 내의원수의, 양주목사, 지중추부사 등을 역임한 의관.
    '강명준': {'role': 'other'},  # 근대 - 개항기 때, 임오군란 당시의 군인.
    '강무경': {'role': 'other'},  # 근대/개항기 - 대한제국기 때, 심남일 의진에서 선봉장으로 활약한 의병.
    '강문규': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 희릉참봉, 의영고봉사 등을 역임한 문신.
    '강문봉': {'role': 'other'},  # 현대 - 김창룡 육군 특무부대장 암살사건 당시의 군인 · 외교관.
    '강문수': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 조선공산당 만주부 조직 책임, 대한민국 특무부대 장교 등을 역임한 사회주의 운동가.
    '강문진': {'role': 'other'},  # 근대 - 일제강점기 때, 대동단에 입단하여 군자금을 모금하여 임시정부에 조달하는 활동을 전개한 독립운동가.
    '강문형': {'role': 'other'},  # 근대 - 조선 후기에, 예방승지, 협판교섭통상사무, 이조참판 등을 역임한 문신.
    '강문회': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 예문관 검열을 역임하고, 성균관에서 후학을 지도한 문신.
    '강민저': {'role': 'scholar'},  # 조선 - 조선 후기에, 희빈장씨를 옹호하던 남구만을 규탄한 죄로 유배되었다가 벼슬을 단념하였고, 이후 후학 양성에 힘쓰며 「상남상」...
    '강민첨': {'role': 'other'},  # 고려/고려 전기 - 고려 전기에, 안찰사, 내사사인, 지중추사 병부상서 등을 역임하였으며, 동여진과 거란의 친입을 격퇴한 장수 · 공신.
    '강박': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 부교리, 수찬, 필선 등을 역임한 문신.
    '강백': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 승문원박사, 정산현감, 한성부우윤 등을 역임한 문신.
    '강백규': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 대한국민회, 간도청년회, 대한청년단 등에서 활동하며 항일투쟁을 전개한 독립운동가.
    '강백년': {'role': 'scholar'},  # 조선/조선 후기 - 조선 후기 관각문학을 대표하는 문한(文翰)이자 청렴한 관직 생활로 청백리에 녹선된 문신.
    '강백진': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 함안군수, 사헌부장령, 사간원사간 등을 역임한 문신.
    '강백천': {'role': 'other'},  # 근대 - 「대금 산조」를 전승한 예능 보유자.
    '강변칠우': {'role': 'novelist'},  # 조선/조선 후기 - 조선 후기에, 북한강변에서 시와 술로 세월을 보낸 박응서 등 일곱 명의 문인들.
    '강병두': {'role': 'scholar'},  # 현대/대한민국 - 국가재건최고회의 헌법심의위원회 전문위원, 행정계획조사위원회 위원 등으로 활동하였으며, 『신헌법』, 『헌법강의』, ...
    '강병일': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 중국 만주에서 항일투쟁을 한 독립운동가.
    '강병주': {'role': 'scholar'},  # 근대 - 일제강점기 때, 『큰 사전』 편찬 전문위원, 내명학교 교장, 경안중학교 교장 등을 역임한 목사 · 한글학자.
    '강보': {'role': 'other'},  # 고려/고려 후기 - 고려 후기 판서운관사를 역임한 과학기술자.
    '강복성': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 평산부사, 전주부윤, 청송부사 등을 역임한 문신.
    '강복중': {'role': 'scholar'},  # 조선/조선 후기 - 조선 후기에, 「수월정청흥가」, 「위군위친통곡가」, 「분산회복사은가」 등의 작품을 남긴 문신.
    '강봉수': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 평창군수, 참판 등을 역임한 문신.
    '강봉우': {'role': 'other'},  # 근대 - 일제강점기 때, 105인사건으로 옥고를 치렀으며, 간도에서 3·1운동을 주도한 독립운동가.
    '강사덕': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 우군도총제, 전라도병마도절제사, 판승녕부사 등을 역임한 무신.
    '강사상': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 병조판서, 형조판서, 이조판서 등을 역임한 문신.
    '강사필': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 병조참의, 사헌부대사헌, 승문원부제조 등을 역임한 문신.
    '강삼': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 동부승지, 우부승지, 우승지 등을 역임한 문신.
    '강상국': {'role': 'scholar'},  # 조선 - 조선 후기에, 『능호집』 등을 저술한 학자.
    '강상모': {'role': 'other'},  # 근대 - 일제강점기 때, 홍범도가 이끄는 대한독립군에서 활동한 독립운동가.
    '강상인': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 병조참판을 역임한 무신.
    '강상주': {'role': 'other'},  # 근대 - 일제강점기 때, 제5군부설 체카 특별부 전권위원, 연해주 소비에트 집행위원회 감시관 등을 역임한 사회주의 운동가.
    '강상호': {'role': 'other'},  # 현대/대한민국 - 북한에서, 내무성 부상, 인민군 총정치국장 등을 역임하다가 김일성 독재를 규탄하며 소련으로 망명해 북한 체제 비판...
    '강서': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 수원부사, 우승지, 좌승지 등을 역임한 문신.
    '강서룡': {'role': 'other'},  # 현대/대한민국 - 내무부 치안국장, 국방부차관, 교통부장관 등을 역임한 법조인 · 관료.
    '강석': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 동지밀직사사, 교주강릉도도순문 겸 병마사, 삼재 등을 역임한 무신.
    '강석구': {'role': 'other'},  # 조선 - 조선 후기에, 헌납, 사간, 집의 등을 역임한 문신.
    '강석기': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 대사간, 대사성, 도승지, 이조판서 등을 역임한 문신.
    '강석덕': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 우부승지, 호조참판, 대사헌 등을 역임한 문신.
    '강석봉': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 조선청년총동맹 중앙집행위원, 건국준비위원회 전남지부 부위원장 등을 역임한 사회주의 운동가.
    '강석빈': {'role': 'other'},  # 조선 - 조선 후기에, 충청도암행어사, 이조좌랑, 경기도수군절도사 등을 역임한 문신.
    '강석숭': {'role': 'other'},  # 현대/대한민국 - 북한에서, 당 중앙위원, 최고인민회의 대의원, 당 역사연구소장 등을 역임한 관료.
    '강석연': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 「모란등기」 · 「모반의 혈」 · 「대장안」 등에 출연한 배우. 가수.
    '강석창': {'role': 'other'},  # 조선 - 조선 후기에, 고산찰방, 종성부사 등을 역임한 문신.
    '강석호': {'role': 'other'},  # 근대/개항기 - 조선 후기~대한제국기에 국왕 고종의 총애를 받으며 정치에 관여하였던 내시.
    '강선': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 강원도관찰사, 형조참판, 도승지 등을 역임한 문신.
    '강선여': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 공조좌랑, 예조좌랑, 병조좌랑 등을 역임한 문신.
    '강선힐': {'role': 'other'},  # 고대/남북국 - 남북국시대 때, 태봉국의 왕건이 나주지방으로의 출정을 도운 장수.
    '강섬': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 함경도어사, 사간원헌납, 도승지 등을 역임한 문신.
    '강성산': {'role': 'other'},  # 현대/대한민국 - 북한에서, 노동당 중앙위원, 최고인민회의 대의원, 정무원 총리 등을 역임한 관료.
    '강성삼': {'role': 'other'},  # 근대 - 개항기 때, 우리나라에서 첫 번째로 사제서품을 받은 신부.
    '강성좌': {'role': 'other'},  # 조선 - 조선 후기에, 오위도총부도사, 훈련원정, 영변부사 등을 역임한 무신.
    '강성태': {'role': 'other'},  # 현대 - 대한테니스협회 회장, 대한손해보험협회 이사장, 상공부장관, 민의원 의원 등을 역임한 실업가 · 정치인.
    '강세': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 신라의 이벌찬 등을 역임한 관리.
    '강세구': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 호조참의, 충청도관찰사, 대사간 등을 역임한 문신.
    '강세규': {'role': 'other'},  # 조선 - 조선 후기에, 지평, 정언, 기주관 등을 역임한 문신.
    '강세윤': {'role': 'other'},  # 조선 - 조선 후기에, 승정원주서, 이천부사 등을 역임한 문신.
    '강세황': {'role': 'critic'},  # 조선/조선 후기 - 조선후기 시, 서, 화 삼절(三絶)로 일컬어진 화가. 문관, 평론가.
    '강소천': {'role': 'childrenauthor'},  # 근대/일제강점기 - 일제강점기 때, 「길가에 얼음판」, 「얼굴 모르는 동무에게」, 「호박꽃과 반딧불」 등을 저술한 아동문학가.
    '강소춘': {'role': 'other'},  # 근대 - 조선 후기에, 원각사 및 협률사의 창극 공연에 참가한 판소리의 명창.
    '강수': {'role': 'other'},  # 조선 - 조선 후기에, 예조좌랑, 장악원첨정, 장령 등을 역임한 문신.
    '강수곤': {'role': 'other'},  # 조선 - 조선 중기에, 공조좌랑, 고창현감, 괴산군수 등을 역임한 문신.
    '강수남': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 예조좌랑, 병조정랑, 이조참판 등을 역임한 문신.
    '강수형': {'role': 'other'},  # 고려 - 고려 후기에, 북경동지, 동경총관, 찬성사 등을 역임한 역관.
    '강숙경': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 밀양도호부사, 강원도사, 함안군수 등을 역임한 문신.
    '강숙돌': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 의금부도사, 사헌부지평, 사간원사간 등을 역임한 문신.
    '강순': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 대한민국임시의정원 의원 등을 역임하였으며, 해방 이후 북한에서, 최고인민회의 대의원 등을 역임한...
    '강순룡': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 지밀직사, 찬성사, 재령백 등을 역임한 무신.
    '강순의': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 어사중승, 섭대장군, 초토처치병마우도사 등을 역임한 무신.
    '강순필': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 때, 대한광복회를 결성하여 활동하다가 일본경찰에게 발각되어 처형당한 독립운동가.
    '강승우': {'role': 'other'},  # 현대 - 한국전쟁 때, 강원도 철원의 백마고지 전투에 참전한 군인.
    '강시': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 삼사좌윤, 군기판관, 강릉도안찰사 등을 역임한 문신.
    '강시경': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 장령, 지평, 정언 등을 역임한 문신.
    '강시만': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 경상남도 합천군 독립만세시위로 체포된 구금자의 석방을 위해 결사대를 조직하여 시위를 전개하다가 ...
    '강시영': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 형조판서, 대사헌, 예조판서 등을 역임한 문신.
    '강시원': {'role': 'other'},  # 근대 - 개항기 때, 차도주를 역임한 천도교인.
    '강시환': {'role': 'other'},  # 조선 - 조선 후기에, 양양부사, 장령, 헌납 등을 역임한 문신.
    '강신': {'role': 'other'},  # 조선 - 조선 중기에, 강원도관찰사, 경기도관찰사, 좌참찬 등을 역임한 문신.
    '강신명': {'role': 'other'},  # 현대/대한민국 - 해방 이후, 숭실대학교 이사장, 대한기독교교육협회(大韓基督敎敎育協會) 회장, 서울장로회신학교 교장 등을 역임(歷任...
    '강신재': {'role': 'novelist'},  # 현대/대한민국 - 해방 이후 「얼굴」 · 「젊은 느티나무」 · 「표선생 수난기」 등을 저술한 소설가.
    '강신호': {'role': 'scholar'},  # 근대 - 일제강점기 「의자」, 「작품제9」, 「진주풍경」 등을 그린 화가. 서양화가.
    '강심': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 때, 신라의 통일전쟁에 참여한 이동혜 지방의 촌주.
    '강양공': {'role': 'other'},  # 고려 - 고려의 제25대 왕, 충렬왕의 첫째 왕자.
    '강언룡': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 유곡도찰방, 좌승지 등을 역임한 무신.
    '강여재': {'role': 'other'},  # 조선 - 조선 후기에, 장령, 세자시강원 보덕 등을 역임한 문신.
    '강여호': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 사간원정언, 사헌부장령, 종성부사 등을 역임한 문신.
    '강연': {'role': 'other'},  # 조선 - 조선 중기에, 인천부사, 첨지중추부사, 한성부판윤 등을 역임한 문신.
    '강영': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 강계만호, 조전원수 등을 역임한 무신 · 공신.
    '강영각': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 하와이로 노동 이민하여 임시정부후원회 이사부원, 재미한족연합위원회 의사부 국방위원 등을 역임한 ...
    '강영선': {'role': 'scholar'},  # 현대/대한민국 - 한국자연보존협회 회장, 한국생물과학협회 회장 등을 역임한 유전학자.
    '강영소': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 때, 미국으로 노동 이민하여 흥사단을 조직하고, 대한인국민회 북미지방 총회장, 독립신문사 하와이 지국...
    '강영준': {'role': 'other'},  # 고려/고려 전기 - 고려 전기에, 내시 위위주부, 좌상시 등을 역임한 문신.
    '강영지': {'role': 'scholar'},  # 조선 - 조선 후기에, 『수재집』, 「심학집략」 등을 저술한 학자.
    '강옥경': {'role': 'other'},  # 현대 - 해방 이후 「진주검무」 전승자로 지정된 기예능보유자.
    '강완숙': {'role': 'other'},  # 조선 - 조선 후기에, 신유박해 당시의 순교자.
    '강왕': {'role': 'other'},  # 발해의 제6대(재위: 795년~809년) 왕.
    '강용구': {'role': 'other'},  # 근대 - 원로원 참의, 삼일원 대덕, 대일각 전교 등을 역임한 대종교인.
    '강용환': {'role': 'other'},  # 근대 - 대한제국기 때, 이날치의 제자로 김창환 협률사에서 활동한 판소리의 명창.
    '강용흘': {'role': 'novelist'},  # 근대/일제강점기 - 일제강점기 때, 「행복한 숲」, 「동양인이 본 서양」, 「초당」 등을 저술한 소설가.
    '강우': {'role': 'scholar'},  # 근대 - 일제강점기 때, 『종리문답』, 『천산도설』, 『제천혈고사』 등을 저술한 대종교인.
    '강우규': {'role': 'other'},  # 근대/일제강점기 - 대한국민노인동맹단 라오허현 지부장으로 사이토 마코토 총독 처단 투탄 의거를 일으킨 독립운동가.
    '강우성': {'role': 'scholar'},  # 조선/조선 후기 - 조선시대 때, 부산훈도이자 『첩해신어』를 저술한 역관.
    '강우형': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 중추원의관, 장례원소경, 봉상사제조 등을 역임한 문신.
    '강욱': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 도승지, 예조참의, 강원도관찰사 등을 역임한 문신.
    '강운': {'role': 'scholar'},  # 조선/조선 후기 - 조선 후기 영남 남인 출신의 학자이자 전적, 지평, 이조좌랑 등을 역임한 문신.
    '강운경': {'role': 'other'},  # 현대/대한민국 - 서울대학교 교수, 한국듀오피아노협회 회장 등을 역임한 음악가.
    '강원': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 전의현감, 공주목사, 청주목사 등을 역임한 문신.
    '강원보': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 종부부령, 판소부시사 등을 역임한 문신.
    '강원영': {'role': 'other'},  # 근대/개항기 - 대한제국기 때, 대한의학교 교관, 육군 3등 군의관 등을 역임한 의관.
    '강원용': {'role': 'other'},  # 현대/대한민국 - 해방 이후 아시아종교인평화회의 의장, 세계종교인평화회의 공동의장 등을 역임한 목사. 교육자, 사회운동가.
    '강원형': {'role': 'other'},  # 근대 - 대한제국기 때, 십삼도유생연명소의 소수로 상소를 올린 민족운동가.
    '강위': {'role': 'poet'},  # 근대/개항기 - 개항기 때, 『경위합벽』, 『손무자주』, 『동문자모분해』 등을 저술한 시인 · 개화사상가.
    '강위빙': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 희릉참봉, 종묘서봉사, 순안현령 등을 역임한 문신.
    '강유': {'role': 'other'},  # 조선 - 조선 후기에, 황해감사, 경기수군절도사, 호조참의 등을 역임한 문신.
    '강유선': {'role': 'scholar'},  # 조선 - 조선 전기에, 『주천집』을 저술한 유생.
    '강유정': {'role': 'other'},  # 현대 - 해방 이후 여인극장 대표, 한국연극협회 이사 등을 역임한 연출가.
    '강유후': {'role': 'other'},  # 조선 - 조선 후기에, 정주목사, 강계부사, 의주부윤 등을 역임한 문신.
    '강윤': {'role': 'other'},  # 근대/일제강점기|현대 - 일제강점기 때, 태화기독교사회관을 신축한 건축가.
    '강윤국': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 대한애국청년당을 결성하여 부민관 투탄 의거를 전개한 독립운동가.
    '강윤명': {'role': 'other'},  # 고려 - 고려 충렬왕 때, 영월에서 민란을 일으킨 주모자.
    '강윤소': {'role': 'other'},  # 고려 - 고려 후기에, 원종폐립사건 당시의 관리.
    '강윤충': {'role': 'other'},  # 고려 - 고려 후기에, 찬성사, 판삼사사 등을 역임한 문신 · 공신.
    '강윤형': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 만경현령, 동부승지, 승지 등을 역임한 문신.
    '강윤희': {'role': 'other'},  # 근대/개항기 - 대한제국기 경기도 가평 출신으로, 관동창의진(關東倡義陣)과 13도창의군에서 활동한 의병장.
    '강융': {'role': 'other'},  # 고려 - 고려 후기에, 만호, 찬성사, 첨의좌정승판삼사사 등을 역임한 문신.
    '강은': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 검열, 예빈시참봉, 전적 등을 역임한 문신.
    '강응정': {'role': 'other'},  # 조선 - 조선 전기에, 김용석, 신종호 등과 향약을 만들고, 『소학』을 강론한 문신.
    '강응철': {'role': 'other'},  # 조선 - 조선 중기에, 찰방 등을 역임하였으며, 임진왜란이 발발하자 의병을 일으켜 항쟁한 의병장.
    '강응태': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 성균관전적, 사헌부지평, 순천도호부사 등을 역임한 문신.
    '강응환': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 고령진첨사, 창성부사, 동래부사 등을 역임한 무신.
    '강이문': {'role': 'critic'},  # 현대 - 해방 이후 부산여자대학교 무용과 교수, 한국춤평론가회 회장 등을 역임한 평론가. 춤평론가.
    '강이봉': {'role': 'other'},  # 근대 - 대한제국기 때, 문태수 의진에서 항일의병투쟁을 전개한 의병.
    '강이상': {'role': 'other'},  # 조선 - 조선 후기에, 정언, 지평, 양덕현감 등을 역임한 문신.
    '강이식': {'role': 'other'},  # 고대/삼국/고구려 - 삼국시대 때, 고구려 임유관전투에 참전한 장수.
    '강이오': {'role': 'scholar'},  # 조선/조선 후기 - 조선 후기에, 「강안주유도」, 「송하망폭도」 등의 작품을 그린 화가.
    '강이원': {'role': 'other'},  # 조선 - 조선 후기, 이승훈, 정약용 등과 함께 천주교리를 강습한 일에 대하여 유생들이 상소를 올려 천주교 탄압의 계기가 된 정미반...
    '강이천': {'role': 'other'},  # 조선 - 조선 후기에, 신유박해와 관련된 천주교인.
    '강익': {'role': 'scholar'},  # 조선 - 조선 전기에, 남계서원을 건립하여 정여창을 제향하였으며, 『개암집』을 저술한 학자.
    '강익록': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 독립운동 자금을 모금하고, 일제의 경찰 주재소 습격으로 무기징역을 선고받고 옥고를 치른 독립유공자.
    '강익문': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 예조좌랑, 충원현감, 제용감정 등을 역임한 문신.
    '강인': {'role': 'other'},  # 조선 - 조선 중기에, 공조좌랑, 한성부좌윤, 상주목사 등을 역임한 문신.
    '강인부': {'role': 'other'},  # 고려 - 조선 전기에, 상의중추원사를 역임한 환관.
    '강인수': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 의열단, 조선의용군, 조선민족혁명당 특파원 등으로 활동하였으며 해방 이후, 중국군 육군소장을 역...
    '강인식': {'role': 'other'},  # 조선 - 조선 후기에, 대오전악, 집사악사 등을 역임한 거문고 명인.
    '강인유': {'role': 'other'},  # 고려 - 고려 후기에, 찬성사, 계품사 등을 역임한 문신.
    '강인희': {'role': 'other'},  # 현대/대한민국 - 해방 이후 공주사범대학 가정과 교수, 명지대 가정학과 교수, 양정학원 이사 등을 역임한 교육자. 한국음식연구가.
    '강일순': {'role': 'other'},  # 근대 - 대한제국기 때, 증산사상을 개시한 종교 창시자.
    '강자평': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 승정원동부승지, 우부승지, 형조참의 등을 역임한 문신.
    '강장원': {'role': 'other'},  # 근대 - 일제강점기 때, 김창환의 제자로 국립국악원 국악사로 활동한 판소리의 명창.
    '강재구': {'role': 'other'},  # 현대/대한민국 - 수도사단 제1연대 소대장, 1군 하사관학교 수류탄 교관 등을 역임한 군인.
    '강재만': {'role': 'other'},  # 근대 - 조선 후기에, 동편제의 법통을 이은 판소리의 명창.
    '강재천': {'role': 'other'},  # 근대 - 일제강점기 때, 의병으로 활동하다가 만주로 망명하였고, 북로군정서에 가입해 항일무장투쟁을 전개한 의병 · 대종교인 · 독립...
    '강재항': {'role': 'other'},  # 조선/조선 후기 - 조선 후기, 선공감역, 한성주부, 회인현감 등을 역임한 문신.
    '강정택': {'role': 'scholar'},  # 근대/일제강점기 - 일제하의 농정학자이자 해방 후 경성대학 교수, 농림부 차관 등을 역임한 농업 정책학자.
    '강정환': {'role': 'scholar'},  # 조선 - 조선 후기에, 『전암문집』 등을 저술한 학자.
    '강제': {'role': 'other'},  # 조선 - 조선 전기에, 영덕현감, 이조정랑 등을 역임한 문신.
    '강제억': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 1919년 평안북도 창성에서 3·1운동에 참여하고, 1920년 1월 대한민국임시정부 연통제(聯通制)에...
    '강제원': {'role': 'scholar'},  # 현대/대한민국 - 『한국동식물도감』 해조류편을 저술한 생물학자.
    '강제하': {'role': 'other'},  # 근대 - 일제강점기 때, 대한민국임시정부 파견원, 대한통의부 교통위원장 등을 역임하여 만세시위 계획, 자금 및 독립군 모집과 같은 ...
    '강제희': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 평안북도 창성의 독립만세시위를 주도하였고, 대한민국임시정부 평안북도창성군 조사원을 역임하여 항일...
    '강조': {'role': 'other'},  # 고려/고려 전기 - 고려 전기, 서북면도순검사, 중대사, 이부상서 · 참지정사, 행영도통사 등을 역임한 권신.
    '강조원': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 개성 남부교회, 경기도 파주구읍교회, 개풍군 풍덕교회 등에서 목회한 목사.
    '강종': {'role': 'other'},  # 고려 - 고려의 제22대(재위: 1211~1213) 왕.
    '강종경': {'role': 'other'},  # 조선 - 조선 전기에, 예문관검열, 성균관학유 등을 역임한 문신.
    '강주': {'role': 'novelist'},  # 조선/조선 후기 - 조선 후기 문신이자 문인.
    '강주룡': {'role': 'other'},  # 일제강점기 평양 소재 평원(平元)고무공장 여공으로 1931년 동맹파업을 벌인 항일노동운동가.
    '강주진': {'role': 'scholar foreigner'},  # 현대/대한민국 - 『정치학개론』, 『근대외교사』, 『미국정당 정치연구』 등을 저술한 서지학자.
    '강주호': {'role': 'scholar'},  # 조선 - 조선 후기에, 서숙을 열어 후진 양성에 전념하였으며, 『유금강산록』, 『유태백산록』, 『유속리산록』 등을 저술한 학자.
    '강준호': {'role': 'other'},  # 현대 - 멕시코 올림픽대회 등에서 지도자로 활약한 체육인.
    '강준흠': {'role': 'novelist'},  # 조선/조선 후기 - 조선 후기 정언, 지평, 부수찬, 수안현감 등을 역임한 문신이며 문인.
    '강중경': {'role': 'other'},  # 고려 - 고려 후기에, 동지밀직사사, 서북면병마사 등을 역임한 무신 · 공신.
    '강중상': {'role': 'other'},  # 고려 - 고려 후기에, 경상도도순문진변사, 판개성부사, 경상도도순문사 등을 역임한 문신.
    '강중진': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 성균관전적, 형조좌랑, 승문원판교 등을 역임한 문신.
    '강증': {'role': 'other'},  # 고려 - 고려 전기에, 수사공 참지정사판상서형부사, 중서시랑평장사 등을 역임한 문신.
    '강진': {'role': 'other foreigner'},  # 근대 - 일제강점기 때, 러시아 및 간도 등지에서 공산주의 활동을 하다가 해방 이후 조선인민공화국에서 중앙인민위원회의 인민위원 및 ...
    '강진구': {'role': 'other'},  # 현대/대한민국 - 1973년 삼성전자에 상무를 시작으로 2000년까지 삼성그룹 전문경영인으로 활약한 기업인.
    '강진규': {'role': 'other'},  # 조선 - 조선 후기에, 성균관박사, 사헌부장령, 예조참판 등을 역임하였으며, 「영남만인소」를 지어 사학을 몰아낼 것을 주장하며 개화...
    '강진원': {'role': 'other'},  # 근대 - 대한제국기 때, 의병 부대를 편성하여 여수의 원포리전투에 참전한 의병장.
    '강진철': {'role': 'scholar'},  # 현대/대한민국 - 「고려 초기의 군인전」, 「고려 토지 제도사 연구」 등을 저술한 역사학자.
    '강진해': {'role': 'other'},  # 근대 - 일제강점기 때, 만주에서 정의부 서란총관, 한국독립군 별동대장 등으로 활동하며 항일투쟁을 전개하다가 일본군과의 전투에서 전...
    '강진휘': {'role': 'other'},  # 조선 - 조선 중기에, 사포서별제, 참봉, 선전관 등을 역임한 문신.
    '강진희': {'role': 'other'},  # 근대/개항기 | 근대/일제강점기 - 일제강점기 때, 서화미술회 교수, 서화협회 발기인 등을 역임한 서화가.
    '강징': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 지중추부사, 경주부윤, 예조참판 등을 역임한 문신.
    '강찬': {'role': 'other'},  # 근대 - 조선 후기에, 사헌부대사헌, 이조참판, 봉상사제조 등을 역임한 문신.
    '강창규': {'role': 'other'},  # 근대/일제강점기 | 현대 - 해방 이후 「건칠반」을 제작한 공예가. 건칠공예가.
    '강창제': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 독립신문사 기자, 임시정부 경무국장서리, 조선혁명당 중앙감찰위원 등을 역임하며 항일운동을 전개한...
    '강철구': {'role': 'other'},  # 근대 - 일제강점기 때, 만주에서 천영학교 교사, 북로군정서 총재비서로 활동하며 민족교육과 독립운동을 전개하다가 체포되어 순국한 독...
    '강첨': {'role': 'other'},  # 조선 - 조선 중기에, 병조좌랑, 이조참의, 경상도관찰사 등을 역임한 문신.
    '강춘삼': {'role': 'other'},  # 근대 - 대한제국기 때, 의병 부대를 편성하여 황해도 해주의 쟈라기벌판전투에 참전한 의병장.
    '강충': {'role': 'other'},  # 고대/남북국 - 삼국시대 때, 신라의 상사찬 등을 역임한 호족.
    '강치성': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 검열, 홍문관저작, 춘추관기사관 등을 역임한 문신.
    '강태국': {'role': 'other'},  # 현대/대한민국 - 해방 이후 한국성서대학교를 설립한 목사. 교육가.
    '강태동': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 대한민국임시정부의 내무차장과 비밀항일결사인 대동단의 단장 등으로 활동하며 항일운동을 전개한 독립...
    '강태성': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 수원의 독립만세시위를 주도하다가 제암리 학살사건에 의해 사망한 독립운동가.
    '강태수': {'role': 'novelist'},  # 현대 - 소련에서 카자흐공화국으로 강제이주를 당하였으며, 「나의 가르노」, 「밭 갈던 아씨에게」 등의 시, 단편, 수필을 저술한 고...
    '강태홍': {'role': 'other'},  # 근대 - 일제강점기 때, 김창조의 제자로 조선성악연구회에서 활동한 가야금 산조 명인.
    '강택진': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 조선13도총간부 교섭부장, 조선노농대회준비회 발기인 등을 역임한 사회주의 운동가.
    '강필경': {'role': 'other'},  # 조선 - 조선 후기에, 집의, 첨지중추부사, 오위장 등을 역임한 문신.
    '강필로': {'role': 'other'},  # 조선 - 조선 후기에, 회양부사, 대사간, 병조참의 등을 역임한 문신.
    '강필리': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 동래부사, 승정원동부승지, 대사간 등을 역임한 문신.
    '강필방': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 제주도에서 양재해의 반란에 가담한 호족.
    '강필성': {'role': 'other'},  # 근대 - 일제강점기 때, 풍산군수, 중추원참의, 황해도지사 등을 역임한 관료 · 친일반민족행위자.
    '강필신': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 예조좌랑, 병조좌랑, 안주현감 등을 역임한 문신.
    '강필주': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 서화미술회 교수를 역임한 화가.
    '강필효': {'role': 'scholar'},  # 조선 - 조선 후기에, 『사유록』, 『경서고이』, 『해은유고』 등을 저술한 학자.
    '강학년': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 지평, 장령, 대사헌 등을 역임한 문신.
    '강한수': {'role': 'other'},  # 근대 - 일제강점기 때, 학생비밀결사 무등회를 조직하여 항일운동을 전개하다 옥사한 독립운동가.
    '강항': {'role': 'other'},  # 조선 - 조선 중기에, 교서관박사, 공조좌랑, 형조좌랑 등을 역임한 문신.
    '강헌지': {'role': 'other'},  # 조선 - 조선 후기에, 개녕현감, 성균관전적, 춘추관기주관 등을 역임한 문신.
    '강현': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 이조참의, 예조참판, 대제학 등을 역임한 문신.
    '강형': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 지평, 장령, 대사간 등을 역임한 문신.
    '강혜원': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 때, 미국으로 노동 이민하여 신한부인회 총무, 대한여자애국단 초대 총단장, 흥사단원 등으로 활동한 독...
    '강호': {'role': 'other'},  # 근대/일제강점기|현대 - 일제강점기 때, 인쇄미술 및 상업미술, 영화감독, 연극공연의 무대장치 제작 등 3개 분야에 걸쳐 활동하였으...
    '강호문': {'role': 'other'},  # 고려/고려 후기 - 고려 후기 판전교시사를 역임한 문신.
    '강호보': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 전적, 찰방, 지중추부사 등을 역임한 문신.
    '강혼': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 우찬성, 판중추부사 등을 역임한 문신.
    '강홍대': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 비서원승, 중추원의관, 육군삼등군의장 등을 역임한 의관.
    '강홍립': {'role': 'other'},  # 조선 후기에, 한성부우윤, 순검사, 오도원수 등을 역임한 문신.
    '강홍식': {'role': 'novelist'},  # 일제강점기 「복지만리」, 「집 없는 천사」, 「망루의 결사대」 등에 출연한 배우. 시나리오작가.
    '강홍중': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 청송부사, 동지의금부사, 성천부사 등을 역임한 문신.
    '강회계': {'role': 'other'},  # 고려 - 고려 후기에, 고공좌랑, 진원군 등을 역임한 문신.
    '강회백': {'role': 'other'},  # 고려 - 고려 후기에, 밀직부사, 판밀직사사, 이조판서 등을 역임하였으며, 조선 건국 후에는 동북면도순문사를 역임한 문신 · 공신.
    '강효동': {'role': 'other foreigner'},  # 조선/조선 전기 - 조선 전기에, 중국으로부터의 채색무역문제에 관해 진언한 도화서의 화가.
    '강효문': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 예조참판, 함길도관찰사, 함길도병마절도사 등을 역임한 문신.
    '강효실': {'role': 'other'},  # 현대/대한민국 - 「죄와 벌」, 「한강은 흐른다」, 「울어도 부끄럽지 않다」 등에 출연한 배우.
    '강효원': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 병자호란 후 소현세자를 따라 심양에 간 시강원 서리.
    '강흡': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 성현찰방, 산음현감 등을 역임한 문신.
    '강흥업': {'role': 'other'},  # 조선 - 조선 후기에, 병자호란과 관련된 무신.
    '강희맹': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 예조정랑, 이조참의, 진헌부사 등을 역임한 문신.
    '강희보': {'role': 'other'},  # 조선 - 조선 중기에, 임진왜란이 발발하자 금산전투, 진주성전투 등에 참전한 의병.
    '강희안': {'role': 'other'},  # 조선 - 조선 전기에, 호조참의, 황해도관찰사 등을 역임한 문신.
    '강희언': {'role': 'scholar'},  # 조선/조선 후기 - 조선 후기에, 「인왕산도」, 「석공도」, 「사인삼경도」 등의 작품을 그린 화가.
    '강희열': {'role': 'other'},  # 조선 - 조선 중기에, 임진왜란이 발발하자 금산전투, 진주성전투 등에 참전한 의병.
    '강희중': {'role': 'other'},  # 현대/대한민국 - 한국전쟁 때, 경북 경주의 기계 · 안강전투에 참전한 군인.
    '강희헌': {'role': 'other'},  # 근대/일제강점기 - 일제강점기, 북간도에서 활동한 민족운동가.
    '개로왕': {'role': 'other'},  # 고대/삼국/백제 - 백제의 제21대(재위: 455년~475년) 왕.
    '개루왕': {'role': 'other'},  # 고대/삼국/백제 - 백제의 제4대(재위: 128년~166년) 왕.
    '개지문': {'role': 'other'},  # 고대/삼국 - 신라의 제29대 왕 태종 무열왕의 서자인 왕자.
    '개청': {'role': 'other'},  # 고대/삼국시대 - 삼국시대 때, 신라의 보현사 주지 등을 역임한 승려.
    '갱세': {'role': 'other'},  # 고대/남북국 - 남북국시대 때, 통일신라의 급찬관등을 역임한 관리.
    '거관': {'role': 'other'},  # 조선 - 조선 후기에, 설악산 신흥사로 출가하여 정업에게서 구족계를 받은 승려.
    '거도': {'role': 'other'},  # 고대/삼국 - 신라 탈해이사금 때, 우시산국과 거칠산국을 병합한 장수.
    '거득공': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 신라 태종무열왕의 서자로 총재를 역임한 관리.
    '거등왕': {'role': 'other'},  # 고대/삼국/가야 - 금관가야의 제2대(재위: 199년~253년) 왕.
    '거시지': {'role': 'other'},  # 고대/남북국 - 삼국시대 때, 신라의 현령 등을 역임한 지방관.
    '거연': {'role': 'other'},  # 근대 - 개항기 때, 남한총섭, 북한총섭 등을 역임한 승려.
    '거연당': {'role': 'scholar'},  # 조선/조선 후기 - 조선 후기에, 「관동팔경도 병풍」, 「산수도 병풍」 등의 작품을 그린 화가.
    '거열랑': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 신라의 「혜성가」와 관련된 화랑.
    '거진': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 무산성 · 감물성 · 동잠성전투에 참전한 신라의 장수.
    '거질미왕': {'role': 'other'},  # 고대/삼국/가야 - 금관가야의 제4대(재위: 291년~346년) 왕.
    '거천': {'role': 'other'},  # 고려/고려 전기 - 고려 전기에, 경주호장을 역임한 호족.
    '거칠부': {'role': 'other'},  # 삼국시대 신라의 파진찬 · 상대등 등을 역임한 장수.
    '건품': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 백제 무왕의 아막성 침공 당시의 신라 장수.
    '걸걸중상': {'role': 'other'},  # 고대/남북국/발해 - 발해의 제1대 고왕 대조영의 아버지로, 고구려 유민을 이끌고 당나라군과 싸우다 전사한 왕족.
    '걸숙': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대, 신라의 석씨 왕족.
    '걸승': {'role': 'other'},  # 고려 - 고려 후기에, 양양 낙산사의 노비.
    '검군': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 신라의 화랑 · 근랑의 낭도 출신으로 사량궁 사인 등을 역임한 관리.
    '검모잠': {'role': 'other'},  # 고대/삼국/고구려 - 삼국시대 때, 고구려 부흥 운동을 전개한 지도자.
    '견권': {'role': 'other'},  # 고려 - 고려 전기에, 말갈과 후백제와의 전투에서 공을 세운 장수 · 공신.
    '견금': {'role': 'other'},  # 고려 - 고려 전기에, 본주의 영군장군을 역임한 호족.
    '견등': {'role': 'scholar'},  # 고대/삼국 - 삼국시대 때, 신라의 『화엄일승성불묘의』, 『대승기신론동현장』 등을 저술한 승려.
    '견성군': {'role': 'other'},  # 조선 - 조선의 제9대 왕, 성종의 서자인 왕자.
    '견우옹': {'role': 'novelist'},  # 고대/남북국 - 삼국시대 때, 신라의 「헌화가」를 지은 작가.
    '견훤': {'role': 'other'},  # 고대/남북국 - 남북국시대 때, 후백제를 건국한 시조.
    '결응': {'role': 'other'},  # 고려 - 고려 전기에, 승통, 왕사, 국사 등을 역임한 승려.
    '겸용': {'role': 'other'},  # 고대/남북국 - 삼국시대 때, 신라의 태수 등을 역임한 관리.
    '겸익': {'role': 'other'},  # 고대/삼국/백제 - 백제시대, 인도에 유학을 다녀온 승려.
    '겸지왕': {'role': 'other'},  # 고대/삼국/가야 - 금관가야의 제9대(재위: 492년~521년) 왕.
    '경': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 고구려 평양성 내 낙랑동사 주지 등을 역임한 승려.
    '경강대왕': {'role': 'other'},  # 고려/고려 전기 - 고려의 제1대 왕, 태조 왕건의 조부인 왕족.
    '경구': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 내의원수의 · 지중추부사 등을 역임한 의관.
    '경녕군': {'role': 'other'},  # 조선/조선 전기 - 조선의 제3대 왕, 태종의 서자인 왕자.
    '경대승': {'role': 'other'},  # 고려 - 고려 후기에, 교위, 사심관, 장군 등을 역임한 무신.
    '경덕왕': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 제35대 왕.
    '경명군': {'role': 'other'},  # 조선 - 조선의 제9대 왕, 성종의 서자인 왕자.
    '경명왕': {'role': 'other'},  # 고대/남북국 - 통일신라의 제54대(재위: 917년~924년) 왕.
    '경목현비': {'role': 'other'},  # 고려 - 고려 전기, 제9대 왕 덕종의 왕비.
    '경문왕': {'role': 'other'},  # 고대/남북국/통일신라 - 통일신라의 제48대(재위: 861년~875년) 왕.
    '경보': {'role': 'other'},  # 고려 - 후백제의 견훤과 고려 초 국왕들의 공경을 받았던 승려.
    '경복흥': {'role': 'other'},  # 고려 - 고려 후기에, 수시중, 수성도통사, 청원부원군 등을 역임한 문신.
    '경봉': {'role': 'other'},  # 현대/대한민국 - 일제강점기 통도사 불교전문강원 원장, 통도사 주지 등을 역임한 승려.
    '경빈 박씨': {'role': 'other'},  # 조선/조선 전기 - 조선 전기 제11대 국왕 중종의 후궁.
    '경사만': {'role': 'other'},  # 고려/고려 후기 - 고려 후기 우대언(右代言)을 역임한 충숙왕 측근 문신.
    '경산': {'role': 'other'},  # 근대 - 일제강점기 때, 동래에서 범어사 주지, 임시정부 고문 등을 역임한 승려.
    '경선': {'role': 'other'},  # 현대/대한민국 - 수덕사 주지를 역임한 승려.
    '경선행': {'role': 'scholar'},  # 조선 - 조선 후기에, 『묵사집』 등을 저술한 수학자.
    '경섬': {'role': 'other'},  # 조선 - 조선 중기에, 장례원행판결사, 부제학, 호조참판 등을 역임한 문신.
    '경성왕후': {'role': 'other'},  # 고려 - 고려의 제9대 왕, 덕종의 왕비.
    '경세인': {'role': 'scholar'},  # 조선/조선 전기 - 조선 전기에, 『경재유고』, 『경연강독록』 등을 저술한 문신.
    '경세창': {'role': 'other'},  # 조선 - 조선 전기에, 도승지, 황해도관찰사, 호조참판 등을 역임한 문신.
    '경순': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 통도사, 송광사, 해인사 등에서 선을 지도한 승려.
    '경순공주': {'role': 'other'},  # 조선/조선 전기 - 조선의 제1대 왕, 태조의 셋째 공주.
    '경순왕': {'role': 'other'},  # 통일신라의 제56대(재위: 927년~935년) 왕.
    '경식': {'role': 'other'},  # 근대 - 개항기 때, 해인사 완허의 제자로 평신에게 선교를 배운 승려.
    '경신': {'role': 'other'},  # 조선 - 조선후기 송광사(松廣寺)의 내원선원에서 선교를 지도한 승려.
    '경신공주': {'role': 'other'},  # 조선/조선 전기 - 조선전기 제1대 태조의 첫째 딸인 공주.
    '경애왕': {'role': 'other'},  # 고대/남북국 - 통일신라의 제55대(재위: 924년~927년) 왕.
    '경언': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 가지산 보림사 당우를 신축한 건축가.
    '경연': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 사재감주부, 이산현감 등을 역임한 문신.
    '경열': {'role': 'other'},  # 조선 - 조선시대 때, 태능으로부터 선법을 계승한 승려.
    '경욱': {'role': 'other'},  # 현대/대한민국 - 일제강점기 통도사(通度寺) 혜봉의 제자로 정혜사 만공의 법맥을 계승한 승려.
    '경운': {'role': 'other'},  # 근대 - 일제강점기 때, 조선불교선교양종교무원 교정을 역임한 승려.
    '경원공': {'role': 'other'},  # 고려 - 고려의 제21대 왕, 희종의 셋째 왕자.
    '경유': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 때, 태조의 왕사를 역임한 승려.
    '경유공': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 경상도병마절도사, 첨지중추부사 등을 역임한 무신.
    '경응순': {'role': 'other'},  # 조선 - 조선 중기에, 왜학통사를 역임하였으며, 임진왜란이 발발하자 왜장 고니시에게 포로로 잡혀 결국 피살된 역관.
    '경의': {'role': 'other'},  # 고려 - 고려 후기에, 밀직부사, 계림원수 등을 역임하였으며, 위화도회군 이후 이성계의 집권과정에서 일시 소외되었다가, 태조 즉위 ...
    '경조': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 삼중대사를 역임한 승려.
    '경종': {'role': 'other'},  # 조선/조선 후기 - 조선 제20대 왕.
    '경주': {'role': 'scholar'},  # 근대 - 일제강점기 때, 명정학교 교장, 중앙불교전문학교 교장서리 등을 역임한 승려.
    '경준': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 좌부승지, 첨지중추부사 등을 역임한 문신.
    '경질': {'role': 'other'},  # 고대/남북국 - 남북국시대 때, 통일신라의 봉림산파 2대조 심희의 문하생인 승려.
    '경찬': {'role': 'other'},  # 조선 - 조선 후기에, 용흥사 주지, 용흥사 수호총섭 등을 역임한 승려.
    '경창군': {'role': 'other'},  # 조선/조선 후기 - 조선 제14대 임금 선조의 서(庶) 9남.
    '경창궁주': {'role': 'other'},  # 고려 - 고려의 제24대 왕, 원종의 왕비.
    '경최': {'role': 'other'},  # 조선 - 조선 후기에, 도승지, 판결사 등을 역임한 문신.
    '경한': {'role': 'other'},  # 고려 - 고려후기 신광사 주지, 흥성사 주지, 공부선 시관 등을 역임한 승려.
    '경헌': {'role': 'scholar'},  # 조선 - 조선시대 때, 『제월당집』을 저술한 승려.
    '경호': {'role': 'other'},  # 근대 - 개항기 때, 벽송사 · 동학사 등에서 불교 경전을 깊이 연구한 승려.
    '경혼': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 홍문관부제학, 충청도관찰사, 좌부승지 등을 역임한 문신.
    '경화': {'role': 'other'},  # 근대 - 대한제국기 때, 부안 내소사에 선원을 개설하여 후학을 양성한 승려.
    '경화공주': {'role': 'other'},  # 고려 - 고려, 제27대 충숙왕의 왕비.
    '경화궁부인': {'role': 'other'},  # 고려 - 고려의 제4대 왕, 광종의 왕비.
    '경화왕후': {'role': 'other'},  # 고려/고려 전기 - 고려의 제16대 왕, 예종의 왕비.
    '경흥': {'role': 'scholar'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 『삼미륵경소』 · 『금광명경최승왕경약찬』 등을 저술한 승려.
    '계강': {'role': 'other'},  # 고대/남북국 - 남북국시대 때, 통일신라의 아찬으로 시중, 상대등 등을 역임한 관리.
    '계고': {'role': 'other'},  # 고대/삼국 - 삼국시대 신라의 제24대 진흥왕 때의 가야국의 음악가 우륵에게 가야금을 배운 신라인.
    '계광순': {'role': 'other foreigner'},  # 현대/대한민국 - 일제강점기 때, 일본 척무성 사무관 등을 역임하였으며, 해방 이후 제 4·5대 민의원 등을 역임한 정치인 · 친일...
    '계국대장공주': {'role': 'other'},  # 고려/고려 후기 - 고려, 제26대 충선왕의 왕비.
    '계덕해': {'role': 'other'},  # 조선 - 조선 후기에, 성균관전적, 예조좌랑 등을 역임한 문신.
    '계백': {'role': 'other'},  # 고대/삼국/백제 - 삼국시대 때, 황산벌전투에 참전한 백제의 장수.
    '계병호': {'role': 'other'},  # 현대/대한민국 - 일제강점기 선천YMCA 총무, 중앙YMCA 간사 및 이사 등을 역임한 사회운동가.
    '계봉우': {'role': 'scholar'},  # 근대/일제강점기 - 일제강점기 때, 임시의정원, 고려공산당에서 활동하며 국외 항일운동을 전개한 역사학자 · 독립운동가.
    '계선': {'role': 'scholar'},  # 조선 - 조선 후기에, 대흥사 주지로 『양악문집』을 저술한 승려.
    '계수': {'role': 'other'},  # 고대/삼국 - 고구려의 제8대 왕, 신대왕의 5번째 왕자.
    '계아태후': {'role': 'other'},  # 고대/남북국 - 신라의 제56대 왕, 경순왕의 어머니로, 경순왕 즉위 후에 왕태후로 추존된 왕족.
    '계양군': {'role': 'other'},  # 조선 - 조선의 제4대 왕, 세종의 서자인 왕자.
    '계오': {'role': 'scholar'},  # 조선 - 조선 후기에, 『가산집』 등을 저술한 승려.
    '계오부인': {'role': 'other'},  # 고대/남북국 - 신라의 제38대 왕, 원성왕의 어머니로, 원성왕 즉위 후에 소문태후로 추봉된 왕족.
    '계왕': {'role': 'other'},  # 고대/삼국/백제 - 백제의 제12대(재위: 344년~346년) 왕.
    '계용묵': {'role': 'novelist'},  # 근대 - 일제강점기 때, 『병풍에 그린 닭이』, 『백치 아다다』 등을 저술한 소설가.
    '계원': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 때, 이찬 관등에 임명된 신라의 관리.
    '계유명': {'role': 'other'},  # 조선 - 조선 후기에, 효행으로 선교랑 사포서별제를 제수받은 효자.
    '계응': {'role': 'other'},  # 고려/고려 전기 - 고려 전기에, 대각국사 의천의 화엄종을 계승한 승려.
    '계응태': {'role': 'other'},  # 현대/대한민국 - 북한에서, 당 중앙위원회 위원, 부총리 겸 무역부장, 당 중앙위원회 공안담당 비서 등을 역임한 관료.
    '계정': {'role': 'other'},  # 근대 - 조선 후기에, 보제, 월화 등 5대 강사로부터 경전을 배운 승려.
    '계정식': {'role': 'scholar'},  # 일제강점기 때, 이화여자전문학교 음악과 과장, 조선음악회 이사 등을 역임한 지휘자 · 친일반민족행위자.
    '계지문': {'role': 'other'},  # 조선 - 조선 후기에, 정묘호란이 발발하자 아들과 함께 의병을 모집하여 항쟁한 의병장.
    '계홍': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 때, 통일신라의 아찬, 진두 등을 역임한 관리.
    '계화': {'role': 'other'},  # 근대 - 일제강점기 때, 만주에서 대한군정서를 조직하여 군자금 모금활동을 전개한 독립운동가.
    '계화부인': {'role': 'other'},  # 고대/남북국/통일신라 - 신라의 제39대 왕, 소성왕의 왕비.
    '계훈제': {'role': 'other'},  # 현대 - 민족수호협의회 운영위원, 민주헌법쟁취 국민운동본부 상임공동대표 등을 역임한 사회운동가.
    '고경리': {'role': 'other'},  # 조선 - 조선 중기에, 임진왜란 당시 선조를 호종하지 않았다는 이유로 곤경에 빠진 정철과 성혼을 두둔하는 상소에서 이언적을 제외하였...
    '고경명': {'role': 'other'},  # 조선 - 조선 중기에, 임진왜란이 발발하자 전라좌도 의병대장에 추대되었으며, 금산전투를 이끌다 전사한 문신 · 의병장.
    '고경조': {'role': 'other'},  # 조선 - 조선 전기에, 해미현감, 임천군수, 광주목사 등을 역임한 문신.
    '고경허': {'role': 'other'},  # 조선 - 조선 전기에, 승지, 전주부윤 등을 역임한 문신.
    '고공의': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 고구려 멸망 후, 유민 집단을 이끈 지도자.
    '고광만': {'role': 'other'},  # 현대 - 해방 이후 문교부차관, 문교부장관 등을 역임한 관료. 교육자.
    '고광수': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 고려공산청년회 책임비서를 지낸 사회주의운동가, 독립운동가.
    '고광순': {'role': 'other'},  # 근대 - 개항기 때, 을미사변이 일어나자 기우만과 함께 의병을 모집하여 좌도의병대장으로 활약한 의병장.
    '고광채': {'role': 'other'},  # 근대 - 개항기 때, 을미사변이 일어나자 고광순 의진에서 참모 겸 우익장으로 활약한 의병장.
    '고광훈': {'role': 'other'},  # 근대 - 대한제국기 때, 형 고광순 의진에서 참모부장으로 활약한 의병.
    '고구': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 고구려 장수왕의 측근으로 활동한 장수.
    '고국양왕': {'role': 'other'},  # 고대/삼국/고구려 - 고구려의 제18대(재위: 384년~391년) 왕.
    '고국원왕': {'role': 'other'},  # 고대/삼국/고구려 - 삼국시대 고구려 제16대 왕.
    '고국천왕': {'role': 'other'},  # 고대/삼국/고구려 - 고구려의 제9대(재위: 179년~197년) 왕.
    '고기승': {'role': 'other'},  # 조선 - 조선 후기에, 사간원헌납, 성균관전적 등을 역임한 문신.
    '고기준': {'role': 'other'},  # 현대/대한민국 - 해방 이후 북한의 조선기독교도연맹 서기장을 역임한 목사.
    '고길덕': {'role': 'other'},  # 고대/남북국 - 남북국시대 때, 발해의 대부승으로서 고려에 파견된 사신.
    '고노자': {'role': 'other'},  # 고대/삼국/고구려 - 삼국시대 고구려 신성태수를 지낸 관리.
    '고달': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 백제의 행건위장군 광양태수 겸 장사로서 남제에 파견된 사신.
    '고대선': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 강원도 양양의 독립만세시위에 참여했다가 순국한 독립운동가.
    '고대수': {'role': 'other'},  # 근대/개항기 - 개항기 때, 갑신정변 당시의 궁녀.
    '고덕린': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 평안남도 대동군 금제면 원장리와 강서군 반석면 상사리 사천시장 일대의 독립만세시위에 참여했다가 ...
    '고덕무': {'role': 'other'},  # 고대/삼국/고구려 - 고구려 제28대 보장왕의 아들로, 요동지역의 고구려 유민을 통치한 왕자.
    '고두환': {'role': 'other'},  # 근대 - 일제강점기 때, 대한독립단에 가입하였고, 구월산대를 조직하여 군자금 모금활동 및 친일파 처단 활동을 전개한 독립운동가.
    '고득뢰': {'role': 'other'},  # 조선 - 조선 중기에, 임진왜란이 발발하자 의병장 최경회 휘하의 부장이 되었으며, 진주성전투에 참전한 무신.
    '고득종': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 중추원부사, 동지중추원사, 한성부판윤 등을 역임한 문신.
    '고량': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 고구려 위두대형, 책성도독, 대상 등을 역임한 귀족.
    '고려복신': {'role': 'other foreigner'},  # 고대/삼국 - 삼국시대 고구려 멸망 후 일본에서 여러 관직을 역임한 유민. 일본관리.
    '고련': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 당나라에서 안동도호 등을 역임한 장수.
    '고로': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 고구려와 말갈 연합의 백제 한성 침공에 가담했던 고구려의 장수.
    '고맹영': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 사헌부지평, 옥천군수, 호조참의 등을 역임한 문신.
    '고명달': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「양주별산대놀이」의 전승자로 지정된 예능보유자.
    '고명자': {'role': 'other'},  # 근대/일제강점기 - 해방 이후 조선부녀총동맹 총무부위원, 근로인민당 중앙위원으로 활동한 사회주의운동가. 독립운동가.
    '고모한': {'role': 'other'},  # 고대/남북국/발해 - 고려 전기에, 요나라에서 개부의동삼사, 중대성좌상 등을 역임한 발해의 유민.
    '고무': {'role': 'other'},  # 고대/삼국 - 고구려의 제15대 왕, 미천왕의 아들인 왕자.
    '고문간': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 고구려 멸망 후 몽고고원의 돌궐로 이주한 유민.
    '고병간': {'role': 'scholar'},  # 근대/일제강점기|현대 - 세브란스의학전문학교 교수, 연세대학교 총장, 세브란스병원 원장 등을 역임한 의사.
    '고병국': {'role': 'scholar'},  # 현대 - 헌법제정 전문위원, 법전편찬위원회 위원 등을 역임한 법학자.
    '고병익': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 『완전 동양사』, 『아시아의 역사상』, 『동아교섭사의 연구』 등을 저술한 학자. 역사학자.
    '고병희': {'role': 'other foreigner'},  # 근대 - 일제강점기 때, 일본에서 흑우회에 가입해 활동하다가 귀향하여 독서회를 조직한 독립운동가.
    '고보원': {'role': 'other'},  # 고대/삼국/고구려 - 고구려의 제28대 보장왕의 손자로, 좌응양위 대장군에 임명된 왕족.
    '고보준': {'role': 'other'},  # 고려 - 고려 전기에, 이자겸 일파를 제거하려다 실패한 관리.
    '고복남': {'role': 'other'},  # 고대/삼국/고구려 - 고구려 시대 보장왕의 태자.
    '고복수': {'role': 'other'},  # 근대 - 일제강점기 때, 「타향살이」, 「짝사랑」, 「사막의 한」 등을 부른 가수.
    '고복장': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 고구려 우보 등을 역임한 관리.
    '고봉': {'role': 'other'},  # 근대 | 현대 - 해인사, 은해사 등에서 강사로 후학을 지도한 승려.
    '고봉기': {'role': 'other foreigner'},  # 현대/대한민국 - 일제강점기 때, 중국으로 건너가 항일투쟁을 벌였으며, 해방 이후 북한에서, 중앙당 기요과장, 외무성 부상 등을 역...
    '고봉례': {'role': 'other'},  # 조선 - 조선 전기에, 우군동지총제, 제주안무사 등을 역임한 무신.
    '고부천': {'role': 'other'},  # 조선 - 조선 후기에, 교서관정자, 지제교, 사헌부장령 등을 역임한 문신.
    '고비': {'role': 'other'},  # 고대/남북국/후백제|고려/고려 전기 - 후백제의 제1대 왕, 견훤의 후궁으로, 견훤의 첫째 아들 신검에 의해 금산사에 유폐되었을 때...
    '고사경': {'role': 'scholar'},  # 조선 - 조선 전기에, 동지중추부사 등을 역임하였으며, 『대명률직해』를 저술한 학자.
    '고사계': {'role': 'other'},  # 고대/삼국 - 남북국시대 때, 당나라에서 사진교장을 역임한 장수.
    '고사훈': {'role': 'other'},  # 근대 - 대한제국기 때, 김석윤 대장의 참모 및 모병책으로 활약하며 항일의병투쟁을 전개한 의병.
    '고상돈': {'role': 'other'},  # 현대 - 한국에서 최초로 에베레스트산을 등정한 산악인.
    '고상안': {'role': 'scholar'},  # 조선 - 조선 중기에, 함창현감, 풍기군수 등을 역임하였으며, 임진왜란이 발발하자 함창에서 의병 대장으로 활약하다가 벼슬을 그만두고...
    '고석': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 「정오의 우사」 · 「정원」 · 「모자」 등을 그린 화가. 유화가.
    '고석규': {'role': 'poet critic'},  # 현대/대한민국 - 「윤동주의 정신적 소묘」, 「비평가의 교양」, 「현대시의 형이상성」 등을 저술한 시인 · 평론가.
    '고석진': {'role': 'other'},  # 근대/대한제국기 - 대한제국기 때, 최익현의 태인의거에 참모로서 가담하였으며, 임병찬 의진에서 참모관으로 활약한 의병.
    '고선지': {'role': 'other'},  # 고대/삼국 - 남북국시대 때, 당나라에서 사진절도사, 안서절도사 등을 역임한 장수.
    '고설봉': {'role': 'other'},  # 현대 - 해방 이후 「여명」 · 「사랑의 가족」 등에 출연한 배우.
    '고성겸': {'role': 'scholar'},  # 조선 - 조선 후기에, 「한성악부」, 『녹리문집』 등을 저술한 학자.
    '고성후': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 감찰, 군수, 예조참의 등을 역임한 문신.
    '고세': {'role': 'other'},  # 고려 - 고려 후기에, 판밀직사사, 자의밀직사사, 도첨의참리 등을 역임한 무신.
    '고세보': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 자헌, 중추부 2품직 등을 역임한 의관.
    '고수': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 위사좌평 등을 역임한 백제의 관리.
    '고수겸': {'role': 'other'},  # 고려/고려 후기 - 고려후기 최우암살미수사건과 관련된 관리. 무신.
    '고수관': {'role': 'other'},  # 조선 - 조선 후기에, 더늠 「자진사랑가」를 지은 판소리 명창.
    '고숙수': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 당나라에서 조청대부심택령 등을 역임한 관리.
    '고순': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 때, 고구려 옹산성 침공에 가담한 신라의 장수.
    '고순흠': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 조선일보 사카이지국장, 재일거류민단 제2대 단장 등을 역임한 노동운동가.
    '고숭덕': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 당나라에서 좌표도위익부랑장 등을 역임한 무신.
    '고승': {'role': 'other'},  # 고대/삼국/고구려 - 고구려 영양왕대의 장군.
    '고승제': {'role': 'scholar'},  # 현대 - 『경제학입문』, 『한국경제론』, 『한국사회 경제사론』 등을 저술한 경제학자 · 친일반민족행위자.
    '고시복': {'role': 'other'},  # 근대 - 일제강점기 때, 한인애국단 비밀단원, 한국광복군 총사령부 전령 장교, 임시정부 내무부 총무과장 등을 역임한 군인 · 독립운동가.
    '고시언': {'role': 'poet'},  # 조선 - 조선 후기에, 『소대풍요』, 『성재집』 등을 저술한 시인.
    '고식': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 막리지 등을 역임한 고구려의 관리.
    '고안무': {'role': 'scholar foreigner'},  # 고대/삼국 - 삼국시대 때, 오경박사로서 일본에 파견된 백제의 학자.
    '고앙주': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 경상남도 창원의 삼진 만세운동에 참여했다가 순국한 독립운동가.
    '고약해': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 형조참판, 개성부유수 등을 역임한 문신.
    '고언백': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 경상좌도병마사, 경기방어사 등을 역임한 무신.
    '고여': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 이성계의 휘하 산원으로 활동하였으며, 이방원의 명으로 정몽주를 격살하고 이성계를 추대한 무신 · 공신.
    '고여림': {'role': 'other'},  # 고려 - 고려 후기에, 야별초지유, 장군 등을 역임한 무신.
    '고연무': {'role': 'other'},  # 고대/삼국/고구려 - 고구려 말기의 장군.
    '고연수': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 고구려 안시성전투에 참전한 장수.
    '고연휘': {'role': 'scholar'},  # 고려/고려 후기 - 고려 후기에, 「동경산수도」, 「하경산수도」 등의 작품을 그린 화가.
    '고열': {'role': 'other'},  # 고려/고려 전기 - 고려 전기에, 중대광, 섭병부상서, 수사공상서좌복야 등을 역임한 무신.
    '고영근': {'role': 'other'},  # 근대/개항기 - 개항기 때, 만민공동회와 독립협회에서 활동하며 정부에게 개혁을 요구하는 개혁개방운동을 전개한 관리 · 독립운동가.
    '고영기': {'role': 'other'},  # 고려/고려 전기 - 고려 전기에, 감찰어사, 중군판관, 호부원외랑 등을 역임한 무신.
    '고영문': {'role': 'other'},  # 근대 - 조선 후기에, 고종에게 「시무7조」 상소문을 올린 개화사상가.
    '고영부': {'role': 'other'},  # 고려 - 고려 전기에, 위위소경, 보문각직각, 어사중승 등을 역임한 문신.
    '고영석': {'role': 'other'},  # 근대/개항기 - 김옥균의 상노로 갑신정변 당시 통신 및 정찰 임무를 수행하였던 개화당원.
    '고영신': {'role': 'other'},  # 고려/고려 전기 - 고려 전기에, 서북면병마사, 이부상서지추밀원사, 검교사공참지정사 등을 역임한 문신.
    '고영중': {'role': 'other'},  # 고려/고려 후기 - 고려 후기 무신집권기에 활동한 문신 관료로 은퇴한 후 해동기로회를 결성하여 활동한 인물.
    '고영창': {'role': 'other'},  # 고려/고려 전기 - 고려 전기, 요나라에서 발해 광복운동을 벌인 발해의 유민.
    '고영철': {'role': 'other'},  # 근대/일제강점기 - 개항기 때, 통리아문박문국 주사를 역임한 언론인.
    '고영희': {'role': 'other'},  # 근대/개항기 | 근대/일제강점기 - 일제강점기 때, 주일 특명전권공사, 탁지부 대신 등을 역임한 관료 · 친일반민족행위자.
    '고예진': {'role': 'other'},  # 근대 - 일제강점기 때, 의병 및 독립의군부 총무국 서기관으로 활동하며 항일운동을 전개하였고, 파리장서에 서명한 의병 · 독립운동가.
    '고왕': {'role': 'other'},  # 고대/남북국/발해 - 발해의 제1대(재위: 698년~719년) 왕.
    '고욕': {'role': 'other'},  # 고대/남북국/발해 - 남북국시대 거란의 요주에서 발해부흥운동을 일으키고 스스로 대왕이라 칭한 발해의 유민.
    '고용보': {'role': 'other'},  # 고려/고려 후기 - 고려 후기 원나라 황실에서 활동한 고려 출신 환관.
    '고용지': {'role': 'other'},  # 고려 - 고려 후기에, 도지병마사, 남로착적병마사, 공부상서 등을 역임한 무신.
    '고용진': {'role': 'other'},  # 근대 - 일제강점기 때, 의병 및 독립의군부 회계총관으로 활동하며 항일운동을 전개하였고, 파리장서 서명운동에 가담한 의병 · 독립운동가.
    '고용현': {'role': 'other'},  # 고려 - 고려 후기에, 대사성, 개성윤, 전라도진변사 등을 역임한 문신.
    '고용후': {'role': 'novelist'},  # 조선/조선 후기 - 조선 후기의 문인.
    '고우루': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 고구려의 을파소에 이어 죽을 때까지 국상을 역임한 관리.
    '고우영': {'role': 'other'},  # 현대/대한민국 - 1970~1980년대 스포츠신문 지면을 통해 성인을 위한 만화를 연재한 만화가.
    '고운': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 「백액대호」를 그린 화가.
    '고원증': {'role': 'other'},  # 현대/대한민국 - 해방 이후 중앙고등군법회의 재판장, 서울지구 계엄민사부장, 법무차감 등을 역임한 군인. 관료.
    '고원훈': {'role': 'scholar'},  # 근대 - 일제강점기 때, 보성전문학교 교수, 조선체육회 초대 이사장, 중추원 참의 등을 역임한 관료 · 기업인 · 친일반민족행위자.
    '고유': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 승지, 안주목사 등을 역임한 문신.
    '고유방': {'role': 'other'},  # 고려/고려 후기 - 고려의 제19대 왕, 명종의 총애를 받았던 도화원의 화가.
    '고유섭': {'role': 'scholar'},  # 근대 - 일제강점기 때, 『조선회화집성』, 『조선탑파의 연구』, 『한국미술문화사논총』 등을 저술한 미술사학자.
    '고윤식': {'role': 'scholar'},  # 조선 - 조선 후기에, 「문심경」, 『태려문집』 등을 저술한 학자.
    '고을나': {'role': 'other'},  # 고대/초기국가 - 초기국가시대 때, 탐라국의 삼성혈 신화에 전해지는 건국 시조.
    '고응관': {'role': 'other'},  # 조선 - 조선 후기에, 예조좌랑, 사헌부장령 등을 역임한 문신.
    '고응량': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 발생한 이인좌의 난과 관련된 관리.
    '고응척': {'role': 'scholar'},  # 조선 - 조선 중기에, 함흥교수, 풍기군수, 회덕현감, 경주부윤 등을 역임하였으며, 「임인제야시」, 「탄시」, 「차기음」, 『두곡집...
    '고의화': {'role': 'other'},  # 고려 - 고려 전기에, 수사공 상서좌복야 판병부사, 위사공신 등을 역임한 무신 · 공신.
    '고이만년': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 고구려 장수왕이 감행한 백제 침공에서 공을 세운 장수.
    '고이왕': {'role': 'other'},  # 백제의 제8대(재위: 234년~286년) 왕.
    '고익': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 고구려 장사 등을 역임하며 동진에 사신으로 파견된 관리.
    '고익진': {'role': 'scholar'},  # 현대/대한민국 - 동국대학교 불교학과 교수, 한국불교전서 편찬실장 등을 역임하였으며, 『한역불교근본경전』, 『한글아함경』, 『한국의...
    '고인계': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 형조정랑, 충청도도사, 예안현감 등을 역임한 문신.
    '고인단': {'role': 'other'},  # 고려 - 고려후기 탐라 성주, 총관행서부사 등을 역임한 인물.
    '고인덕': {'role': 'other'},  # 근대 - 일제강점기 때, 만주에서 의열단을 조직하여 항일무장투쟁을 벌이다가 체포되어 옥사한 독립운동가.
    '고인재': {'role': 'other'},  # 근대 - 일제강점기 때, 경기도 안성군 원곡면과 양성면 일대의 독립만세시위에 참여한 독립운동가.
    '고인후': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 승문원정자, 예조참의 등을 역임한 문신.
    '고임무': {'role': 'other'},  # 고대/삼국/고구려 - 삼국시대 고구려의 제28대 보장왕의 둘째 아들인 왕자.
    '고자': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 당나라에서 장무장군 등을 역임한 장수.
    '고장환': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 조선소년연맹 중앙집행위원을 역임한 소년 운동가.
    '고재욱': {'role': 'other'},  # 근대 - 한국신문연구소 이사장, 국제신문협회 한국위원장 등을 역임한 언론인.
    '고재필': {'role': 'other'},  # 현대/대한민국 - 일제강점기 때, 만주국 국무원 총무청 고등관 시보 등을 역임하였으며 해방 이후, 국방부 비서실장, 육군 대령, 국...
    '고재호': {'role': 'other'},  # 현대 - 대구고등법원장, 대법관 등을 역임한 법조인.
    '고적': {'role': 'other'},  # 고려 - 고려 후기에, 유총관을 역임한 문신.
    '고정봉': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 홍문관교리, 돈녕부도정 등을 지낸 문신.
    '고정사': {'role': 'other'},  # 고대/남북국/발해 - 남북국시대 후발해의 사신으로 후당에 입조하여 관직을 받은 발해의 유민.
    '고정옥': {'role': 'scholar'},  # 근대/일제강점기 - 서울대학교 사범대학 교수를 재임하며 우리어문학회 회원으로 활동하였고, 『조선민요연구』, 『국어국문학요강』, 『국...
    '고정의': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 여당전쟁 시기 고구려의 관직인 대로 등을 역임한 관리.
    '고정훈': {'role': 'other'},  # 현대/대한민국 - 광복 이후 육군본부 정보국차장, 조선일보 논설위원 등을 역임한 정치인. 언론인.
    '고정희': {'role': 'poet'},  # 현대 - 해방 이후 『지리산의 봄』, 『저 무덤에 푸른 잔디』, 『아름다운 사람 하나』 등을 저술한 시인.
    '고제남': {'role': 'other foreigner'},  # 근대 - 대한제국기 때, 전남 장성에서 창의포고문을 살포하고 정읍에서 일본군을 습격하는 등 항일의병투쟁을 전개한 의병장.
    '고제덕': {'role': 'other foreigner'},  # 고대/남북국 - 남북국시대 때, 발해의 수령이자 일본에 사신으로 파견된 관리.
    '고제량': {'role': 'other'},  # 근대 - 대한제국기 때, 고광순 의진에서 부장으로 활동한 의병.
    '고제신': {'role': 'other foreigner'},  # 근대 - 일제강점기 때, 일본 고관 총살단을 조직하였으나 실행에 실패하고, 임시정부에 조달할 군자금 모금활동을 전개한 독립운동가.
    '고조기': {'role': 'other'},  # 고려 - 고려 전기에, 서북면병마판사, 상서좌복야, 중서시랑평장사 등을 역임한 문신.
    '고조다': {'role': 'other'},  # 고대/삼국 - 고구려의 제20대 왕, 장수왕의 아들인 왕자.
    '고종': {'role': 'other'},  # 근대/개항기|근대/대한제국기 - 조선의 제26대(재위: 1863년~1907년) 왕.
    '고종수': {'role': 'other'},  # 고려 - 고려 후기에, 왕경등처관군만호부만호, 삼주호부 등을 역임한 무신.
    '고종후': {'role': 'other'},  # 조선 - 조선 중기에, 감찰, 예조좌랑, 임피현령 등을 역임한 문신.
    '고주옥': {'role': 'other'},  # 현대/대한민국 - 남해안별신굿의 기예능보유자인 무녀.
    '고죽리': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 고구려의 안시성전투 당시, 연개소문에 의해 보내진 첩자.
    '고준택': {'role': 'other'},  # 현대/대한민국 - 일제강점기 때, 반일투쟁 혐의로 약 7년여간 복역하었으며, 해방 이후 북한에서, 최고인민회의 대의원 등을 역임한 ...
    '고지연': {'role': 'scholar'},  # 조선 - 조선 후기에, 『주암집』 등을 저술한 학자.
    '고지형': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 평안남도 대동군 금제면 원장리와 강서군 반석면 상사리 사천시장 일대의 독립만세시위를 주도한 기독...
    '고진': {'role': 'other'},  # 고대/남북국 - 삼국시대 때, 당나라에 귀화한 고구려의 왕족.
    '고진상': {'role': 'other'},  # 고대/남북국 - 고려 전기에, 고려로 귀화한 발해제군판관 출신의 발해 유민.
    '고진승': {'role': 'other'},  # 조선/조선 후기 | 근대/개항기 - 조선후기 도화서 화원으로 헌종의 국장도감 등에 참여한 화가.
    '고질': {'role': 'other'},  # 고대/삼국/고구려 - 고구려 말기와 멸망 이후, 고구려 유민 출신으로 당나라에서 주로 활동한 무관.
    '고찬보': {'role': 'other'},  # 근대 - 남조선신민당 중앙위원회 선전부장, 남조선노동당 중앙상무위원 등을 역임한 사회주의 운동가.
    '고찬익': {'role': 'other'},  # 근대/개항기 - 대한제국기 연동교회 초대 장로, 장로회공의회 전도위원 등으로 활동한 개신교인. 사회운동가.
    '고창일': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 때, 대한국민의회 대표로서 파리강화회의에 파견되었으며, 중국 하얼빈에서 독립운동을 지속하다가 해방 이...
    '고채주': {'role': 'other'},  # 근대 - 일제강점기 때, 경상남도 통영 부도정시장의 독립만세시위를 주도한 독립운동가.
    '고천백': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 장군, 하정사 등을 역임한 무신.
    '고추안': {'role': 'other'},  # 고대/삼국 - 고구려의 제7대 왕, 차대왕의 태자인 왕자.
    '고춘자': {'role': 'other'},  # 현대 - 백민악극단, 태평양가극단, 백조가극단 등에서 활동한 연극인.
    '고타소랑': {'role': 'other'},  # 고대/삼국/신라 - 신라의 제29대 태종 무열왕의 딸로, 백제의 대야성전투에서 살해된 왕족.
    '고태문': {'role': 'other'},  # 현대 - 한국전쟁 때, 소대장, 중대장 등을 역임한 군인.
    '고태필': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 한성부좌윤, 유수 등을 역임한 문신.
    '고판례': {'role': 'other'},  # 현대/대한민국 - 일제강점기 증산교 최초의 교파인 선도교를 창립한 종교창시자.
    '고평': {'role': 'other foreigner'},  # 근대/일제강점기 - 대한제국기 검사를 지냈으나, 일제강점기 중국으로 망명하여 광복단, 대한국민회 등에서 활동한 독립운동가.
    '고한승': {'role': 'childrenauthor'},  # 근대/일제강점기 - 일제강점기 때, 희곡 「장구한 밤」 등을 저술한 연극인 · 아동문학가.
    '고한우': {'role': 'other'},  # 고려/고려 후기 - 고려후기 대호군, 찰방사 등을 역임한 관리. 무신.
    '고현': {'role': 'other'},  # 조선 - 조선 중기에, 성주판관을 역임하던 중 임진왜란이 발발하자 도피하여 탄핵당하였으나, 의주까지 선조를 호종한 공으로 녹훈된 무...
    '고형림': {'role': 'other'},  # 근대 - 일제강점기 때, 만주에서 사진관을 경영하다가 광복군 제5지대에 입대하여 항일투쟁을 전개한 독립운동가.
    '고형산': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 우찬성, 강원도관찰사 등을 역임한 문신.
    '고혜진': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 고구려 안시성전투에 참전한 장수.
    '고홍건': {'role': 'other'},  # 조선 - 조선시대 때, 오위도총부도총관, 지중추부사 등을 역임한 무신.
    '고홍달': {'role': 'scholar'},  # 조선 - 조선 후기에, 인목대비 폐비 논의가 이루어지자 성균관을 떠났으며, 인조반정 이후에 참봉으로 임명되었으나 곧 물러나 은거한 학자.
    '고황경': {'role': 'other'},  # 근대/개항기|근대/일제강점기 - 해방 이후 이화여자대학교 교수, 서울여자대학교 초대총장 등을 역임한 교육자. 여성운동가 · 친일반민...
    '고효충': {'role': 'other'},  # 고려 - 고려 예종 때, 국학생으로 「감이녀시」를 지어 풍자한 문신.
    '고흘': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 돌궐의 고구려 신성 침공 시, 돌궐을 격퇴했다고 전해지는 고구려의 장수.
    '고흥': {'role': 'scholar'},  # 고대/삼국 - 삼국시대 때, 박사를 역임하여 『서기』를 저술한 백제의 학자.
    '고흥문': {'role': 'other'},  # 현대/대한민국 - 제6·7·8·9·10대 국회의원을 역임한 정치인.
    '고희': {'role': 'other'},  # 조선 - 조선 중기에, 군기시판관, 유원첨사, 픙천부사 등을 역임한 무신 · 공신.
    '고희경': {'role': 'other foreigner'},  # 근대/개항기 | 근대/일제강점기 - 일제강점기 때, 주차영국공사관, 이왕직사무관 등을 역임한 관료 · 친일반민족행위자.
    '고희동': {'role': 'scholar'},  # 일제강점기 「정자관을 쓴 자화상」, 「부채를 든 자화상」, 「금강산진주담폭포」, 「탐승」 등의 작품을 그린 화가.
    '곡나진수': {'role': 'other foreigner'},  # 고대/삼국 - 삼국시대 때, 백제 부흥을 위해 항전하다 주류성이 함락되자 일본으로 망명한 백제의 유민.
    '곤우': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 백제 고목성에서 벌어진 말갈족과의 전투에 참전한 장수.
    '곤지': {'role': 'other'},  # 고대/삼국/백제 - 삼국시대 백제 제22대 문주왕(文周王)의 아우.
    '골번': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 신라의 『삼국사기』 강수전에 나오는 문장가.
    '공규': {'role': 'other'},  # 조선 - 조선 전기에, 예문관봉교, 정언, 전적 등을 역임한 문신.
    '공대일': {'role': 'other'},  # 현대/대한민국 - 해방 이후 광주호남 국악원, 전남미술예술학원, 남도국악학원 등에서 소리선생으로 활동한 판소리의 명창.
    '공덕귀': {'role': 'other'},  # 현대/대한민국 - 한국교회여성연합회 대표, 방림방적체불임금대책위원회 위원장 등을 역임한 사회운동가.
    '공덕흡': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 간도 용정촌에서 전개된 독립만세시위를 주도하는 과정에서 순국한 독립운동가.
    '공민왕': {'role': 'other'},  # 고려/고려 후기 - 고려 후기 제31대 국왕.
    '공병우': {'role': 'scholar'},  # 근대/일제강점기|현대 - 일제강점기 때, 『신소안과학』, 『소안과학』 등을 저술한 의사.
    '공부': {'role': 'other'},  # 고려 - 조선 전기에, 전의부령, 예조총랑, 집현전태학사 등을 역임한 문신.
    '공서린': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 황해도관찰사, 대사헌, 동지중추부사 등을 역임한 문신.
    '공성학': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 개성삼업주식회사 사장, 개성인삼조합 조합장 등을 역임한 실업가.
    '공소': {'role': 'other'},  # 고려 - 고려 후기에, 한림학사, 문하시랑평장사, 창원백 등을 역임한 문신.
    '공양왕': {'role': 'other'},  # 고려/고려 후기 - 고려시대, 제34대(재위: 1389~1392) 왕.
    '공예태후': {'role': 'other'},  # 고려/고려 전기 - 고려, 제17대 왕이며 인종의 왕비.
    '공유': {'role': 'other'},  # 고려 - 고려 후기에, 부지밀직사사, 동판밀직사, 판삼사사 등을 역임한 무신.
    '공윤택': {'role': 'other'},  # 현대/대한민국 - 인천 출신으로 한국의 대표적인 제과 제빵 장인.
    '공윤항': {'role': 'other'},  # 조선 - 조선 후기에, 정언, 병조좌랑 등을 역임한 문신.
    '공은': {'role': 'other'},  # 고려/고려 후기 - 고려 후기 척불소를 올렸던 문신.
    '공인': {'role': 'other'},  # 조선 - 음악을 전업으로 삼던 음악인.
    '공재규': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 경상남도 합천군 삼가장터의 독립만세시위를 주도하는 과정에서 순국한 독립운동가.
    '공재웅': {'role': 'other'},  # 현대 - 해방 이후 「양주별산대놀이」 전승자로 지정된 기예능보유자.
    '공중인': {'role': 'poet'},  # 현대/대한민국 - 『무지개』, 『조국』 등을 저술한 시인.
    '공직': {'role': 'other'},  # 고려/고려 전기 - 고려 초, 태조 왕건에게 귀부한 호족.
    '공진원': {'role': 'other'},  # 근대 - 일제강점기 때, 한국독립당 감찰위원장, 한국광복군 총사령부 참모 등을 역임한 독립운동가.
    '공진항': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 만주 진출을 위해 만몽산업주식회사를 설립하였으며, 해방 이후 고려인삼흥업사장, 농림부장관, 농협...
    '공진형': {'role': 'novelist'},  # 근대/일제강점기|현대 - 해방 이후 국전의 추천작가를 역임한 화가. 서양화가.
    '공천원': {'role': 'other'},  # 고려 - 고려 후기에, 지문하성사, 이부상서, 참지정사 등을 역임한 문신.
    '공학원': {'role': 'scholar foreigner'},  # 근대 - 대한제국기 때, 유림의 대표로 성토문을 지어 일본의 만행을 꾸짖었으며, 말년에는 집 근처에 정사를 짓고 후학 양성을 위해 ...
    '공한': {'role': 'other'},  # 고대/삼국 - 신라의 제17대 왕, 내물마립간의 손자인 왕족.
    '공해동': {'role': 'other'},  # 현대 - 한국전쟁 때, 강원도 화천의 금성지역 수도고지 전투에 참전한 군인.
    '공혜왕후': {'role': 'other'},  # 조선/조선 전기 - 조선의 제9대 왕, 성종의 왕비.
    '곽간': {'role': 'other'},  # 조선 - 조선 전기에, 성균관사성, 공주목사, 강릉부사 등을 역임한 문신.
    '곽경렬': {'role': 'other'},  # 근대/일제강점기 - 대한민국임시정부 독립운동자금 모금 활동을 전개한 독립운동가.
    '곽공의': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 양광도안찰사, 지병마사, 위위경 등을 역임한 문신.
    '곽규석': {'role': 'other'},  # 현대/대한민국 - 해방 이후 코미디 연기와 무대, 방송, TV 등의 사회자로 활약한 방송인이자 코미디언.
    '곽기락': {'role': 'other'},  # 근대 - 조선 후기에, 채서, 동도서기론을 주장한 문신.
    '곽기수': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에 예조좌랑, 부안현감 등을 지낸 문신.
    '곽낙원': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 아들 김구의 임시정부 활동과 독립운동을 지원한 독립운동가.
    '곽린': {'role': 'other'},  # 고려 - 고려 후기에, 문한서, 서장관 등을 역임한 문신.
    '곽복산': {'role': 'scholar'},  # 근대 - 한국신문학회 초대 회장, 한국신문연구소 이사 등을 역임한 언론인.
    '곽상': {'role': 'other'},  # 고려 - 고려 전기에, 형부상서, 상서우복야 참지정사, 수사공 등을 역임한 문신.
    '곽상훈': {'role': 'other'},  # 현대/대한민국 - 일제강점기 때, 동래 3·1운동 및 신간회 활동 등 독립운동을 하다가 해방 이후, 국회의장, 대통령 권한대행 등을...
    '곽선': {'role': 'other'},  # 고려 - 고려 후기에, 양광, 전라도체찰사 등을 역임한 문신.
    '곽성구': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 지평, 장령, 필선 등을 역임한 문신.
    '곽세건': {'role': 'other'},  # 조선 - 조선 후기에, 공조정랑, 봉직랑, 익산군수 등을 역임한 문신.
    '곽수강': {'role': 'scholar'},  # 조선 - 조선 후기에, 「천인감응」, 『매헌문집』 등을 저술한 유생.
    '곽순': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 교리, 봉상시정, 사간 등을 역임한 문신.
    '곽승우': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 이번절제사, 중군총제, 전라도처치사 등을 역임한 무신.
    '곽시': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 홍문관정자를 역임한 문신.
    '곽시징': {'role': 'scholar'},  # 조선 - 조선 후기에, 목릉참봉, 왕자사부, 이인찰방 등을 역임한 학자.
    '곽여': {'role': 'other'},  # 고려/고려 전기 - 고려 전기에, 합문지후, 홍주사, 예부원외랑 등을 역임한 관리.
    '곽여필': {'role': 'other'},  # 고려 - 고려 후기에, 국학대사성, 전법판서, 전라도계점사 등을 역임한 문신.
    '곽연성': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 이조참판, 경상도절제사 등을 역임한 무신.
    '곽영': {'role': 'other'},  # 조선 - 조선시대 때, 전라도병마절도사, 행호군 등을 역임한 무신.
    '곽영준': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 경기도 양평군 양근리시장의 독립만세시위에 참여한 독립운동가.
    '곽예': {'role': 'other'},  # 고려 - 고려 후기에, 국자감대사성, 문한학사, 감찰대부 등을 역임한 문신.
    '곽예순': {'role': 'other'},  # 현대/대한민국 - 해방 이후 댁에서 곽외과의원을 개업한 의료인. 의사.
    '곽원': {'role': 'other'},  # 고려 - 고려 전기에, 서북면행영부도통, 추성문리공신상주국, 참지정사 등을 역임한 문신 · 공신.
    '곽원진': {'role': 'other'},  # 고려 - 고려 후기에, 총랑, 좌대언, 성균좨주진현관제학 등을 역임한 문신.
    '곽월': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 제주목사, 청송부사, 남원부사 등을 역임한 문신.
    '곽유번': {'role': 'scholar'},  # 조선 - 조선 후기에, 『오암문집』 등을 저술한 학자.
    '곽율': {'role': 'other'},  # 조선 - 조선 중기에, 예천군수, 예빈시부정, 초계군수 등을 역임한 문신.
    '곽은': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 담양부사, 승지 등을 역임한 문신.
    '곽의영': {'role': 'other'},  # 현대/대한민국 - 제2, 3, 4대 국회의원, 체신부장관 등을 역임한 정치인 · 실업인.
    '곽인식': {'role': 'scholar'},  # 현대/대한민국 - 「작품」, 「천(성)」, 「무제」 등의 작품을 그린 화가.
    '곽자방': {'role': 'other'},  # 조선 - 조선 중기에, 훈련원봉사를 역임하였고, 임진왜란이 발발하자 의병으로 싸워 청주성을 탈환하였으나 금산성전투에서 전사한 무신 ...
    '곽재겸': {'role': 'other'},  # 조선 - 조선 중기에, 임진왜란이 발발하자 사촌동생인 곽재우와 함께 의병을 이끌고 화왕산성전투에서 활약한 의병장.
    '곽재구': {'role': 'other'},  # 근대 - 대한제국기 때, 심남일 의진에서 항일의병투쟁을 전개한 의병.
    '곽재기': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 만주에서 의열단을 조직하여 총독부 고관 살해 및 일제 기관 파괴 활동을 계획하다 체포된 독립운동가.
    '곽재우': {'role': 'other'},  # 조선/조선 후기 - 조선 중기에, 임진왜란이 발발하자 1차 진주성전투를 지원하고, 화왕산성전투에서 활약하며 홍의장군이라 불린 의병장.
    '곽제화': {'role': 'scholar'},  # 조선/조선 후기 - 조선 후기 사간원과 사헌부에서 언관으로 활동한 문신, 학자.
    '곽존중': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 예조참판, 중군동지총제, 경창부윤 등을 역임한 문신.
    '곽종석': {'role': 'scholar'},  # 근대/대한제국기 - 대한제국기 때, 을사조약이 강제로 체결되자 오적 처단을 상소하였고, 파리강화회의에 독립청원서를 전달한 죄로 옥고...
    '곽종원': {'role': 'critic'},  # 현대/대한민국 - 해방 이후 『신인간형의 탐구』, 『사색과 행동의 세월』, 『사색의 반려』 등을 저술한 평론가. 문학평론가.
    '곽준': {'role': 'other'},  # 조선 - 조선 중기에, 자여도찰방, 안음현감 등을 역임한 문신.
    '곽중규': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 대한민국임시정부 비서장, 임시의정원 의원 등으로 활동한 독립운동가.
    '곽지운': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 이조좌랑 등을 역임한 문신.
    '곽지원': {'role': 'other'},  # 조선 - 조선시대 때, 하정사 오상을 수행하여 명나라에 다녀온 역관.
    '곽지흠': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 장령, 사간, 집의 등을 역임한 문신.
    '곽진': {'role': 'scholar'},  # 조선 - 임진왜란 때 의병을 모집하여 화왕산성전투에 참전한 후, 학문에만 전념하며 『단곡문집』 등을 저술한 학자.
    '곽천호': {'role': 'other'},  # 조선 - 조선 후기에, 교리, 예조정랑 등을 역임한 문신.
    '곽충보': {'role': 'other'},  # 고려 - 조선 전기에, 상의중추원사, 도총제 등을 역임한 무신.
    '곽충수': {'role': 'other'},  # 고려 - 고려 후기에, 지평, 형부시랑, 통헌대부 등을 역임한 문신.
    '곽태진': {'role': 'other'},  # 현대/대한민국 - 일제강점기 때, 비밀결사 호의단을 조직하여 항일투쟁을 전개하였으며 해방 이후, 민의원, 민권당 부총재 등을 역임한...
    '곽학송': {'role': 'novelist'},  # 현대/대한민국 - 「제주도」, 「낯설은 골짜기」, 「모란봉에서 한라산까지」 등을 저술한 작가.
    '곽한일': {'role': 'other'},  # 근대/대한제국기 - 대한제국기 때, 민종식 의진에서 돌격장, 소모장으로 활동한 의병장.
    '곽해룡': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 지중추부사로 『통문관지』를 편찬한 역관.
    '곽현': {'role': 'scholar'},  # 조선 - 조선 후기에, 「만언소」, 『삼안당유고』 등을 저술한 학자.
    '곽홍지': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 전라도사, 예조정랑 등을 역임한 문신.
    '곽휘승': {'role': 'scholar'},  # 근대 - 대한제국기 때, 스승인 곽종석의 학문과 사상에 영향을 받아 성리학을 연구하며 『염와집』을 저술한 학자.
    '곽희태': {'role': 'other'},  # 조선 - 조선 후기에, 동지중추부사 등을 역임한 문신.
    '관기': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라 포산에 은거하며 수행한 승려.
    '관나부인': {'role': 'other'},  # 고대/삼국/고구려 - 삼국시대 고구려 제12대 중천왕의 후궁.
    '관례': {'role': 'other'},  # 조선 - 조선 후기에, 구체사 주지를 역임한 승려.
    '관륵': {'role': 'other foreigner'},  # 고대/삼국/백제 - 삼국시대 때, 백제에서 일본으로 불교를 전파하고 승정에 오른 승려.
    '관승': {'role': 'other'},  # 고려 - 고려 전기에, 광명사 주지를 역임한 승려.
    '관영': {'role': 'other'},  # 근대/개항기 - 개항기 때, 대종장을 역임한 승려.
    '관오': {'role': 'other'},  # 고려/고려 전기 - 고려 전기, 자은종 현화사의 승통 상지에게 출가한 후 승계가 수좌에 오른 승려.
    '관준': {'role': 'other'},  # 근대 - 대한제국기 때, 팔도승풍규정원장, 관동도교정 등을 역임한 승려.
    '관지': {'role': 'scholar'},  # 고대/삼국 - 삼국시대 때, 『열반경요간』, 『아비달마식신족론소』 등을 저술한 신라의 승려.
    '관징': {'role': 'other'},  # 조선 - 조선시대 때, 회암 · 낙암 · 환성 · 쌍운 · 대적 등의 지도를 받은 승려.
    '관창': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 황산벌 싸움에서 활약한 신라의 화랑.
    '관혜': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 때, 통일신라의 해인사에서 활동하였던 화엄종의 승려.
    '관홍': {'role': 'other'},  # 조선 - 조선 후기에, 지리산 철불사 아자방선원에서 수도한 승려.
    '관흔': {'role': 'other'},  # 고대/남북국 - 남북국시대 때, 후백제의 시조 견훤의 명을 받아 양산성을 축조한 장수.
    '광개토왕': {'role': 'other'},  # 고대/삼국/고구려 - 고구려의 제19대(재위: 391년~413년) 왕.
    '광기': {'role': 'other'},  # 고려 - 고려 전기에, 손필 등과 거짓 음양서로 유배형을 받은 승려.
    '광덕': {'role': 'other'},  # 고대/남북국 - 삼국시대 때, 신라의 10구체 향가 「원왕생가」 등을 지은 승려.
    '광명부인': {'role': 'other'},  # 고대/삼국/신라 - 신라의 제13대 왕, 미추이사금의 왕비.
    '광언': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 직지사 조실, 조선불교선리참구원 상임이사 등을 역임한 승려.
    '광열': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 대흥사 편양파의 법손으로 대흥사 제2대 강사를 역임한 승려.
    '광정태후': {'role': 'other'},  # 고려 - 고려의 제19대 왕, 명종의 왕비.
    '광제': {'role': 'other'},  # 고려/고려 전기 - 고려전기 승통을 역임한 승려.
    '광종': {'role': 'other'},  # 고려/고려 전기 - 고려 전기, 제4대 왕.
    '광주원부인': {'role': 'other'},  # 고려/고려 전기 - 고려 전기, 제1대 왕 태조의 제15 왕비.
    '광준': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 총섭, 자헌대부 등을 역임한 승려.
    '광평대군': {'role': 'other'},  # 조선/조선 전기 - 조선의 제4대 왕, 세종의 5번째 왕자.
    '광학': {'role': 'other'},  # 고려 - 고려 전기에, 적리녀의 아들로 신인종에 귀의하여 대덕을 역임한 승려.
    '광해군': {'role': 'other'},  # 조선/조선 후기 - 조선의 제15대 국왕.
    '광화부인': {'role': 'other'},  # 고대/남북국 - 통일신라의 제48대 왕, 경문왕의 어머니로, 광의왕태후로 봉해진 왕족.
    '괴유': {'role': 'other'},  # 고대/삼국 - 고구려 대무신왕 때, 부여 정벌에 자원하여 전공을 세운 장수.
    '굉연': {'role': 'poet'},  # 고려/고려 후기 - 고려후기 나옹 혜근의 제자로 선원사 5대 주지를 역임한 승려. 시인.
    '굉활': {'role': 'other'},  # 조선 - 조선 후기에, 대흥사 제3대 종사 도안의 문하에서 수도한 승려.
    '교기': {'role': 'other foreigner'},  # 고대/삼국/백제 - 백제의 제31대 의자왕의 조카로, 섬으로 추방되어 일본으로 건너간 종실.
    '교대': {'role': 'other foreigner'},  # 고대/삼국 - 삼국시대 때, 일본에 화현했던 미륵보살의 화신으로 알려진 승려.
    '교웅': {'role': 'other'},  # 고려 - 고려 전기에, 삼중대사, 선사, 대선사 등을 역임한 승려.
    '교필': {'role': 'other'},  # 고대/남북국 - 남북국시대 때, 통일신라의 김해지방에서 세력을 떨쳤던 호족.
    '구강': {'role': 'other'},  # 조선 - 조선 후기에, 시강원보덕, 첨지사, 함경도암행어사 등을 역임한 문신.
    '구겸': {'role': 'other'},  # 조선/조선 전기 - 조선전기 경상우도병마절도사, 의주목사 등을 역임한 무신.
    '구공신': {'role': 'other'},  # 고려 - 고려의 제34대 왕인 공양왕을 즉위시킨 9인의 공신.
    '구굉': {'role': 'other'},  # 조선 - 조선시대 때, 형조판서, 공조판서, 병조판서 등을 역임한 무신.
    '구근': {'role': 'other'},  # 고대/남북국 - 남북국시대 때, 통일신라에서 사찬을 역임한 장수.
    '구기': {'role': 'other'},  # 고대/남북국 - 남북국시대 때, 통일신라에서 술간을 역임한 장수.
    '구낙서': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 때, 서울에서 전개된 야간 독립만세시위에 참여했다가 미행하던 일본 경찰에 의해 살해된 독립운동가.
    '구덕': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 당나라에서 불경을 가지고 온 통일신라의 승려.
    '구덕환': {'role': 'other'},  # 현대/대한민국 - 일제강점기 때, 임시정부에서 활동하다가 고향으로 돌아와 의사로 재직 중에 독립운동을 벌였고 해방 이후, 민의원에 ...
    '구도': {'role': 'other'},  # 고대/삼국/고구려 - 삼국시대 때, 고구려에서 비류부장 등을 역임한 관리.
    '구도갈문왕': {'role': 'other'},  # 고대/삼국 - 신라의 제13대 왕, 미추이사금의 아버지로, 좌군주를 역임하여 소문국을 정벌한 왕족.
    '구례마': {'role': 'other'},  # 고대/삼국 - 삼국시대 신라 무산대수촌의 촌장.
    '구륜공': {'role': 'other'},  # 고대/삼국 - 신라의 제24대 진흥왕의 셋째 아들이자 후백제 견훤의 고조부로 『이제가기』에 기록된 왕족.
    '구리내': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 일리촌(一利村)의 지방세력가. 촌주.
    '구마기': {'role': 'other foreigner'},  # 고대/삼국 - 삼국시대 때, 탐라국에서 일본으로 파견된 탐라국의 왕자.
    '구만리': {'role': 'other'},  # 조선 - 조선 후기에, 사서, 지평, 장령 등을 역임한 문신.
    '구명겸': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 좌포도대장, 삼도수군통제사 등을 역임한 문신.
    '구문신': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 경상우도병마도절제사 등을 역임한 무신.
    '구문유': {'role': 'other'},  # 조선 - 조선 후기에, 현풍현감, 고령현감, 익찬 등을 역임한 문신.
    '구문치': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 통제사, 어영대장, 포도대장 등을 역임한 무신.
    '구변': {'role': 'other'},  # 조선 - 조선 전기에, 이조좌랑, 진주목사 등을 역임한 문신.
    '구본웅': {'role': 'scholar'},  # 근대 - 일제강점기 때, 「얼굴 습작」, 「비파와 포도」, 「여인」 등의 작품을 그린 화가.
    '구봉령': {'role': 'other'},  # 조선 - 조선 전기에, 대사헌, 병조참판, 형조참판 등을 역임한 문신.
    '구봉서': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 호조참의, 평안도관찰사 등을 역임한 문신.
    '구봉창': {'role': 'other'},  # 조선 - 조선 후기에, 충청도수사, 충청병사, 평안병사 등을 역임한 무신.
    '구사나왕': {'role': 'other foreigner'},  # 고대/삼국 - 삼국시대 때, 고구려 멸망 후 일본으로 망명한 고구려의 왕족.
    '구사맹': {'role': 'other'},  # 조선 - 조선 중기에, 좌부승지, 이조판서, 좌찬성 등을 역임한 문신.
    '구사안': {'role': 'other'},  # 조선 - 조선 전기에, 위사원종공신일등에 책록된 문신.
    '구상': {'role': 'poet'},  # 현대/대한민국 - 해방 이후 「여명도」, 「길」, 「초토의 시」 등을 저술한 시인.
    '구선복': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 병조판서, 의금부판사 등을 역임한 무신.
    '구선행': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 판의금부사, 병조판서 등을 역임한 무신.
    '구성': {'role': 'other'},  # 조선 - 조선 중기에, 호조참판, 해주목사 등을 역임한 문신.
    '구성량': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 충청도병마도절제사, 판안동대도호부사 등을 역임한 무신.
    '구성로': {'role': 'other'},  # 고려 - 고려 후기에, 대호군, 강원도부원수, 경상도부원수 등을 역임한 무신.
    '구성우': {'role': 'other'},  # 고려 - 고려 후기에, 간관, 문하부낭사, 형조판서 등을 역임한 문신.
    '구성임': {'role': 'other'},  # 조선 - 조선 후기에, 형조판서, 판의금부사, 판돈령부사 등을 역임한 무신.
    '구수담': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 부제학, 전라감사, 대사헌 등을 역임한 문신.
    '구수복': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 수찬, 이조좌랑, 구례현감 등을 역임한 문신.
    '구수암': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 경상남도 동래군 기장읍의 독립만세시위를 주도한 혐의로 체포되어 순국한 독립운동가.
    '구수영': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 오위도총관, 장악원제조 등을 역임한 무신.
    '구수왕': {'role': 'other'},  # 고대/삼국 - 백제의 제6대(재위: 214년~234년) 왕.
    '구수혜': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 신라의 일길찬 등을 역임한 관리.
    '구수훈': {'role': 'other'},  # 조선 - 조선 후기에, 경기도수군절도사, 수원부사, 좌포도대장 등을 역임한 무신.
    '구여순': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 의령에서 만세시위를 주도하였으며, 의열단에서 항일무장투쟁을 계획한 독립운동가.
    '구연영': {'role': 'other'},  # 근대 - 개항기 때, 민승천 의진 중군장, 독립협회 회원으로 활동하며 항일투쟁을 전개한 의병 · 독립운동가.
    '구연해': {'role': 'scholar'},  # 조선 - 조선 후기에, 『연역설』, 『강초유고』 등을 저술한 학자.
    '구연흠': {'role': 'other'},  # 근대 - 일제강점기 때, 전조선민중운동자대회 준비위원, 국제모쁠 제2차조선대표 등을 역임한 사회주의 운동가.
    '구영': {'role': 'other'},  # 조선 - 조선 후기에, 별좌, 감찰, 회인현감 등을 역임한 문신.
    '구영검': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 면천군, 전리판서 등을 역임한 문신.
    '구영숙': {'role': 'other'},  # 근대/일제강점기|현대 - 보건부장관, 세계보건기구 한국수석대표, 한국적십자사 총재 등을 역임한 의사 · 관료.
    '구완희': {'role': 'other'},  # 근대 - 대한제국기 때, 육군참령, 육군법원 이사, 경무사 등을 역임한 관료.
    '구용': {'role': 'other'},  # 조선 - 조선 중기에, 김화현감 등을 역임한 문신.
    '구용서': {'role': 'other'},  # 현대/대한민국 - 한국은행 초대 총재, 대한석탄공사 총재, 상공부장관 등을 역임한 금융인 · 관료.
    '구용징': {'role': 'scholar'},  # 조선 - 조선 후기에, 『경타재문집』 등을 저술한 학자.
    '구용현': {'role': 'other'},  # 현대/대한민국 - 문교부 장학실장, 부산직할시교육위원회 교육감, 국회의원 등을 역임한 교육자.
    '구원일': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 병자호란 당시 강화도 갑곶에서 순절한 무관.
    '구윤명': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 이조를 제외한 육조의 판서 등을 역임한 문신.
    '구윤옥': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 병조판서, 호조판서, 판중추부사 도승지, 병조판서, 의금부판사 등을 역임한 문신.
    '구율': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 사찬으로 사천원전투에 참전한 관리.
    '구은': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에 활동했던, 아호에 은(隱)자가 붙은 9인의 문신들.
    '구음': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 사간, 승지, 간성군수 등을 역임한 문신.
    '구의강': {'role': 'other'},  # 조선 - 조선 후기에, 대사간, 대사성 등을 역임한 문신.
    '구이신왕': {'role': 'other'},  # 고대/삼국/백제 - 백제의 제19대(재위: 420년~427년) 왕.
    '구익': {'role': 'other'},  # 조선 - 조선 후기에, 판서, 지돈령부사 등을 역임한 문신.
    '구인기': {'role': 'other'},  # 조선 - 조선 후기에, 공조판서, 영의정 등을 역임한 문신.
    '구인문': {'role': 'other'},  # 조선 - 조선 전기에, 청주판관, 집현전교리, 좌정언 등을 역임한 문신.
    '구인회': {'role': 'other'},  # 현대 - 금성사 사장, 호남정유 대표, 한국경제인협회 부회장 등을 역임한 실업가.
    '구인후': {'role': 'other'},  # 조선 - 조선시대 때, 판의금부사, 홍청도병마절도사, 우의정 등을 역임한 무신.
    '구일': {'role': 'other'},  # 조선 - 조선 후기에, 한성판윤, 총융사, 지돈령부사 등을 역임한 무신.
    '구자균': {'role': 'scholar'},  # 현대/대한민국 - 고려대학교 문과대학의 교수 등을 역임하였으며, 『국문학사』, 『국역파한집 · 용재총화』, 『국문학논고』 등을 저술...
    '구자운': {'role': 'poet'},  # 현대 - 『처녀승천』, 『청자수병』 등을 저술한 시인.
    '구자춘': {'role': 'other'},  # 현대 - 서울특별시 경찰국장, 서울특별시장, 내무부장관 등을 역임한 군인 · 정치인.
    '구저': {'role': 'other foreigner'},  # 고대/삼국 - 삼국시대 때, 여러 차례 일본에 사신으로 파견된 백제의 관리.
    '구정래': {'role': 'scholar'},  # 조선 - 조선 후기에, 광릉참봉 등을 역임하였으며, 『연포당유고』를 저술한 학자.
    '구정훈': {'role': 'other'},  # 조선 - 조선 후기에, 빙고별제, 배천군수 등을 역임한 문신.
    '구족달': {'role': 'other'},  # 고려/고려 전기 - 고려 전기에, 「강릉보현사낭원대사오진탑비」, 「충주정토사법경대사자등탑비」 등의 글을 쓴 서예가.
    '구족왕후': {'role': 'other'},  # 고대/남북국/통일신라 - 신라의 제37대 왕, 선덕왕의 왕비.
    '구종수': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 순금사사직, 선공감부정 등을 역임한 문신.
    '구종지': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 형조의랑, 호조참의, 호조참판 등을 역임한 문신.
    '구종직': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 행첨지중추부사, 지경연사, 좌찬성 등을 역임한 문신.
    '구준원': {'role': 'scholar'},  # 조선/조선 후기 - 조선 후기에, 『신임기년제요』 등을 저술한 문신.
    '구중회': {'role': 'other'},  # 현대/대한민국 - 해방 이후 국회의원, 미군정청 경남고문 등을 역임한 정치인. 교육자.
    '구지정': {'role': 'other'},  # 조선 - 조선 후기에, 공주목사, 황주목사 등을 역임한 문신.
    '구진': {'role': 'other'},  # 고려 - 고려 전기에, 시중, 나주도대행대시중 등을 역임한 문신.
    '구진주': {'role': 'scholar'},  # 조선 - 조선 후기에, 천연두를 앓다가 두 눈을 실명하였으나, 그 뒤에도 더욱 학문에 정진하여 역사와 성리학에 뛰어났던 학자.
    '구진천': {'role': 'other'},  # 고대/남북국 - 남북국시대 때, 신라의 사찬이자 쇠뇌의 명수인 관리.
    '구찬회': {'role': 'other'},  # 근대 - 일제강점기 때, 신민회 회원으로 활동하였으며, 독립사상을 고취하는 문서를 배포하다가 체포되어 옥사한 독립운동가.
    '구참공': {'role': 'other'},  # 고대/삼국 - 신라 진평왕 때의 화랑.
    '구철우': {'role': 'novelist'},  # 근대/일제강점기 | 현대 - 해방 이후 국전 추천작가, 서예부 심사위원 및 심사위원장 등을 역임한 서화가.
    '구춘선': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 북만주에서 활동한 독립운동가.
    '구치곤': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 우승지, 한성부우윤 등을 역임한 문신.
    '구치관': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 우찬성, 우의정, 영의정 등을 역임한 문신.
    '구치용': {'role': 'scholar'},  # 조선 - 조선 후기에, 『우교당유고』, 『주서연의』 등을 저술한 학자.
    '구치홍': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 판돈령부사, 동지중추부사, 지훈련원사 등을 역임한 무신.
    '구칠': {'role': 'other foreigner'},  # 고대/남북국 - 남북국시대 때, 김대세와 함께 신선이 되려고 중국의 오월로 건너간 신라의 도교인.
    '구태': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 『주서』 백제전, 『수서』 동이전 백제조, 『한원』 등에 기록된 백제의 시조.
    '구택규': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 공조참판, 형조참판, 한성부판윤 등을 역임한 문신.
    '구파해': {'role': 'other'},  # 고대/삼국 - 초기국가시대 때, 백제에 귀화한 남옥저의 유민.
    '구한': {'role': 'other'},  # 조선 - 조선 전기에, 중종의 딸 숙정옹주와 결혼하여 능창위에 봉해진 문신.
    '구항': {'role': 'other'},  # 조선 - 조선 중기에, 임진왜란이 발발하자 금산전투에 참전한 의병장.
    '구형왕': {'role': 'other'},  # 고대/삼국/가야 - 금관가야의 제10대(재위: 521년~532년) 왕.
    '구혜': {'role': 'other'},  # 조선 - 조선 중기에, 호조좌랑, 정언 등을 역임한 문신.
    '구홍': {'role': 'other'},  # 고려 - 고려 후기에, 밀직부사, 우정승 등을 역임한 문신.
    '구희': {'role': 'scholar'},  # 조선 - 조선 중기에, 임진왜란이 발발하자 금산전투와 진주성전투에서 활약하다가 진주성이 함락되자 자결한 학자 · 의병.
    '국경인': {'role': 'other'},  # 조선 - 조선시대 임진왜란 때, 경성부민을 선동해 반란을 일으킨 주모자.
    '국대부인': {'role': 'other'},  # 고대/남북국 - 후백제의 왕, 견훤의 딸인 공주.
    '국융': {'role': 'other'},  # 조선 - 조선 전기에, 애완유영(哀婉悠永) 미조(美調)의 범패로 유명한 범패승.
    '국지모': {'role': 'other foreigner'},  # 고대/삼국 - 삼국시대 때, 백제에서 중국 수나라로 파견된 관리.
    '국채표': {'role': 'scholar'},  # 현대 - 중앙관상대장, 기상학회장 등을 역임하며 한국의 후진 기상전문가 양성에 힘쓴 기상학자.
    '국침': {'role': 'scholar'},  # 조선 - 조선 후기에, 『송만문집』 등을 저술한 학자.
    '궁예': {'role': 'other'},  # 고대/남북국/고려·마진·태봉 - 태봉국의 제1대(재위:901년~918년) 왕.
    '권감': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 도승지, 의정부좌참찬, 병조판서 등을 역임한 문신.
    '권강': {'role': 'scholar'},  # 조선 - 조선 중기에, 『방담문집』 등을 저술한 학자.
    '권개': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 관찰사, 중추원부사 등을 역임한 문신.
    '권건': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 예조참판, 호조참판 등을 역임한 문신.
    '권격': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 병조정랑, 강릉부사 등을 역임한 문신.
    '권겸': {'role': 'other'},  # 고려 - 고려 후기에, 찬성사, 판삼사사, 태부감태감 등을 역임한 문신.
    '권겹': {'role': 'other'},  # 조선 - 조선 중기에, 종부시주부 등을 역임한 문신.
    '권경': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 동지중추원사, 경상좌도병마절도사 등을 역임한 문신.
    '권경완': {'role': 'poet'},  # 근대/일제강점기 - 일제강점기 『자화상』, 『윤리』, 『동결』 등을 저술한 시인.
    '권경우': {'role': 'other'},  # 조선 - 조선 중기에, 정언, 헌납, 장령 등을 역임한 문신.
    '권경유': {'role': 'other'},  # 조선 - 조선 전기에, 홍문관정자, 제천현감 등을 역임한 문신.
    '권경중': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 상서예부시랑지제고를 역임한 문신.
    '권경희': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 예조참판, 대사헌 등을 역임한 문신.
    '권고': {'role': 'other'},  # 고려/고려 후기 - 고려 후기 검교시중을 역임한 문신.
    '권공': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 사은사, 경상좌도병마절제사 등을 역임하면서 세조의 신임을 받았던 무신 · 공신.
    '권굉': {'role': 'other'},  # 조선 - 조선 후기에, 상의원별좌, 별제, 동궁의부수 등을 역임한 문신.
    '권구': {'role': 'scholar'},  # 조선 - 조선 후기에, 「여사휘찬의의」, 『내정편』, 『병곡집』 등을 저술한 학자.
    '권구현': {'role': 'poet'},  # 근대 - 일제강점기 때, 『흑방의 선물』을 저술한 시인 · 미술가.
    '권규': {'role': 'other'},  # 조선 - 조선 후기에, 대사간, 대사헌, 공조참판 등을 역임한 문신.
    '권균': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 이조판서, 영경연사, 우의정 등을 역임한 문신.
    '권극량': {'role': 'scholar'},  # 조선 - 조선 후기에, 『동산문집』 등을 저술한 학자.
    '권극례': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 대사헌, 예조판서 등을 역임한 문신.
    '권극상': {'role': 'other'},  # 조선 - 조선 후기에, 천총, 훈련원첨정 등을 역임한 무신.
    '권극중': {'role': 'other'},  # 조선/조선 후기 - 조선후기 평해군수, 곡산부사, 삼척영장 등을 역임한 무신.
    '권극지': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 형조참판, 동지경연, 예조판서 등을 역임한 문신.
    '권극화': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 충청도관찰사, 중추원부사, 행지중추원사 등을 역임한 문신.
    '권근': {'role': 'scholar'},  # 조선/조선 전기 - 조선 전기에, 중추원사, 정당문학, 대사헌 등을 역임한 문신.
    '권기': {'role': 'scholar'},  # 조선 - 조선 중기에, 『용만문집』, 『영가지』 등을 저술한 학자.
    '권기옥': {'role': 'other'},  # 일제강점기 때, 남경 국민정부 항공서 부비항원, 의열단 여자부 연락원으로 활동한 한국 최초의 여성 비행사 · 독립운동가.
    '권기일': {'role': 'other foreigner'},  # 근대 - 일제강점기 때, 서로군정서 외무담당과 어사부장으로 활동하다가 일본군의 습격으로 순국한 독립운동가.
    '권길': {'role': 'other'},  # 조선/조선 전기 - 조선시대 임진왜란 때 상주판관으로 상주 북천전투에서 순절한 문신.
    '권단': {'role': 'other'},  # 고려 - 고려 후기에, 밀직제학, 지첨의부사, 찬성사 등을 역임한 문신.
    '권달수': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 이조좌랑, 대교, 부교리 등을 역임한 문신.
    '권담': {'role': 'other'},  # 고려 - 조선 전기에, 공주목사, 황해도관찰사, 전주부윤 등을 역임한 문신.
    '권대림': {'role': 'other'},  # 조선 - 조선 후기에, 성균관직강, 자인현감, 만경현감 등을 역임한 문신.
    '권대운': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 예조판서, 병조판서, 영의정 등을 역임한 문신.
    '권대재': {'role': 'other'},  # 조선 - 조선 후기에, 전라감사, 홍문관제학, 호조판서 등을 역임한 문신.
    '권대항': {'role': 'other'},  # 조선 - 조선 후기에, 금군청부총관을 역임한 무신.
    '권대형': {'role': 'other'},  # 근대 - 일제강점기 때, 조선공산당재건설동맹 중앙집행위원, 조선공산주의자협의회 책임자 등을 역임한 사회주의 운동가.
    '권덕규': {'role': 'scholar'},  # 근대 | 현대 - 일제강점기 때, 「한글맞춤법통일안」의 원안을 작성한 국어학자.
    '권덕린': {'role': 'other'},  # 조선 - 조선 전기에, 좌랑, 합천군수 등을 역임한 문신.
    '권덕수': {'role': 'scholar'},  # 조선 - 조선 후기에, 『몽구』, 『포헌집』 등을 저술한 학자.
    '권덕여': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 부제학, 대사간 등을 역임한 문신.
    '권덕형': {'role': 'scholar'},  # 조선 - 조선 후기에, 『경림당유집』 등을 저술한 학자.
    '권도': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 판서, 참찬 등을 역임한 문신.
    '권돈': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 선전관, 경주통판, 밀양부사 등을 역임한 무신.
    '권돈례': {'role': 'scholar'},  # 고려 - 고려 후기에, 어사 등을 역임하였으며, 무신의 난 이후 지방으로 피신하여 은거한 학자.
    '권돈인': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 우의정, 좌의정, 영의정 등을 역임한 문신.
    '권동보': {'role': 'other'},  # 조선 - 조선 전기에, 헌릉참봉, 사섬시직장 등을 역임한 문신.
    '권동수': {'role': 'other foreigner'},  # 근대 - 갑신정변 이후, 김옥균 등의 암살 목적으로 일본에 밀파된 문신.
    '권동진': {'role': 'other'},  # 근대/일제강점기 - 천도교 지도자이자 민족 대표의 한 사람으로서 「3·1독립선언서」에 서명한 독립운동가.
    '권두경': {'role': 'other'},  # 조선 - 조선 후기에, 형조좌랑, 전라도사, 사간원정언 등을 역임한 문신.
    '권두기': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 해운판관, 지평, 정언 등을 역임한 문신.
    '권두문': {'role': 'other'},  # 조선 - 조선 중기에, 내자시정, 통례원좌통례 등을 역임한 문신.
    '권득경': {'role': 'other'},  # 조선 - 조선 중기에, 형조좌랑, 평양판관 등을 역임한 문신.
    '권득기': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 예조좌랑, 공조참판 등을 역임한 문신.
    '권득수': {'role': 'other'},  # 근대/대한제국기 - 대한제국기 때, 경기도 지평, 이천, 양근, 양주 등지에서 항일의병투쟁을 전개한 의병장.
    '권람': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 의정부우찬성, 좌찬성, 우의정 등을 역임한 문신.
    '권렴': {'role': 'other'},  # 고려 - 고려 후기에, 정순대부좌상시, 광정대부첨의찬성사 등을 역임한 문신.
    '권령': {'role': 'other'},  # 조선 - 조선 후기에, 승지, 한성부좌우윤 등을 역임한 문신.
    '권륜': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 대사성, 예조참의, 강원도관찰사 등을 역임한 문신.
    '권만': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 병조정랑, 이조참의 등을 역임한 문신.
    '권만두': {'role': 'other'},  # 조선 - 조선 후기에, 공조정랑, 장수현감 등을 역임한 문신.
    '권만전': {'role': 'scholar'},  # 조선 - 조선 후기에, 『근계문집』 등을 저술한 학자.
    '권맹손': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 이조판서, 중추원사 등을 역임한 문신.
    '권맹희': {'role': 'other'},  # 조선 - 조선 전기에, 도승지, 함길남도절도사, 경기관찰사 등을 역임한 문신.
    '권명덕': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 「자화상」 · 「모란대」 등을 그린 화가. 유화가.
    '권명희': {'role': 'scholar'},  # 조선 - 조선 후기에, 『삼외재문집』 등을 저술한 학자.
    '권목': {'role': 'other'},  # 조선 - 조선 후기에, 함흥판관, 호조정랑 등을 역임한 문신.
    '권무중': {'role': 'other'},  # 조선 - 조선 후기에, 문음(門蔭)으로 선전관을 제수받았으나 사양하고 낙향한 문신.
    '권문해': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 좌부승지, 사간 등을 역임한 문신.
    '권민수': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 대사헌, 동지중추부사 등을 역임한 문신.
    '권반': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 관찰사, 형조판서 등을 역임한 문신.
    '권벌': {'role': 'other'},  # 조선 - 조선 전기에, 의정부좌참찬, 의정부우찬성, 원상 등을 역임한 문신.
    '권벽': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 관찰사, 승문원제조 등을 역임한 문신.
    '권변': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 대사헌, 부수찬, 대사간 등을 역임한 문신.
    '권병노': {'role': 'other'},  # 현대/대한민국 - 제헌국회의원, 제2대 국회의원을 역임하였으며, 정계 은퇴 후 고향에서 의사로 활동한 정치인 · 의사.
    '권병덕': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 독립선언서에 서명한 민족대표 33인 중 한 사람으로, 천도교 전제관장, 보문관장 등을 역임한 천...
    '권보': {'role': 'scholar'},  # 조선 - 조선 후기에, 『성포일고』 등를 저술한 학자.
    '권복': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 중추원부사, 강계도호부사, 절제사 등을 역임한 무신.
    '권복흥': {'role': 'other'},  # 조선 - 조선 중기에, 임진왜란이 발발하자 의병을 일으켜 항쟁한 의병장.
    '권봉수': {'role': 'poet'},  # 근대 - 일제강점기 때, 「용호정」을 저술한 시인.
    '권봉희': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 사간, 정언, 홍문관수찬 등을 역임한 문신.
    '권부': {'role': 'other'},  # 고려 - 고려 후기에, 우정언, 시강학사, 삼중대광 등을 역임한 문신.
    '권사공': {'role': 'other'},  # 조선 - 조선 후기에, 예조좌랑, 예조정랑 등을 역임한 문신.
    '권산해': {'role': 'other'},  # 조선 - 조선 전기에, 종부시첨정을 역임하였으나 세조 즉위 후 조정에 나가지 않았던 관리.
    '권삼득': {'role': 'other'},  # 조선 - 조선 후기에, 「판소리 설렁제」라는 소리제를 낸 것으로 유명한 판소리의 명창.
    '권삼현': {'role': 'scholar'},  # 근대 - 일제강점기 때, 『각재문집』 등을 저술한 학자.
    '권상': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 문소전참봉, 용강현령, 선공감정 등을 역임한 문신.
    '권상구': {'role': 'other'},  # 조선 - 조선 후기에, 동부승지, 여주목사, 공조참의 등을 역임한 문신.
    '권상길': {'role': 'scholar'},  # 조선 - 조선 후기에, 『남곡선생문집』 등을 저술한 학자.
    '권상로': {'role': 'scholar'},  # 현대/대한민국 - 일제강점기 때, 문경 대승사 주지, 불교조계종원로회 원장, 불교사상사 사장 등을 역임한 불교학자 · 친일반민족행위자.
    '권상룡': {'role': 'scholar'},  # 조선 - 조선 후기에, 『긍재유고』 등을 저술한 학자.
    '권상신': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 병조판서, 광주유수 등을 역임한 문신.
    '권상연': {'role': 'other'},  # 조선 - 조선 후기에, 조상의 제사를 지내지 않은 일로 윤지충과 함께 체포되어 참수당한 순교자.
    '권상유': {'role': 'other'},  # 조선 - 조선 후기에, 대사간, 도승지, 이조판서 등을 역임한 문신.
    '권상익': {'role': 'other'},  # 근대 - 일제강점기 때, 파리강화회의에 전달할 독립청원서의 서명 운동과 발송에 가담하였으며, 군자금을 제공하여 독립군기지 건설을 지...
    '권상일': {'role': 'other'},  # 조선 - 조선 후기에, 대사간, 홍문관부제학, 대사헌 등을 역임한 문신.
    '권상임': {'role': 'other'},  # 조선 - 조선 후기에, 풍기군수, 승문원판교, 춘추관편수관 등을 역임한 문신.
    '권상중': {'role': 'other'},  # 근대 - 대한제국기 때, 항일의병투쟁을 벌이며 청송일대에서 모병 및 군자금 모금 활동을 전개한 의병장.
    '권상하': {'role': 'scholar'},  # 조선 - 조선 후기에, 송시열의 수제자로서 기호학파의 정통 계승자이며, 『한수재집』, 『삼서집의』 등을 저술하였고, 호락논쟁의 계기...
    '권석도': {'role': 'other'},  # 근대 - 대한제국기 때. 지리산 일대에서 항일의병투쟁을 전개한 의병장.
    '권석장': {'role': 'scholar'},  # 조선 - 조선 후기에, 「심성설」, 「이기호발설」, 『외암문집』 등을 저술한 학자.
    '권섭': {'role': 'novelist'},  # 조선/조선 후기 - 조선 후기에, 「황강구곡가」, 「도통가」, 『옥소집』 등을 저술한 문인.
    '권성': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 충청도관찰사, 형조판서 등을 역임한 문신.
    '권성구': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 병조정랑, 직강, 병조좌랑 등을 역임한 문신.
    '권성오': {'role': 'other'},  # 조선 - 조선 후기에, 공조정랑, 보령현감 등을 역임한 문신.
    '권성원': {'role': 'other'},  # 조선 - 조선 후기에, 여산군수, 선산부사 등을 역임한 문신.
    '권성익': {'role': 'scholar'},  # 조선 - 조선 후기에, 「성지위천명」, 「성리설변」, 『연곡유집』 등을 저술한 학자.
    '권성제': {'role': 'scholar'},  # 조선 - 조선 후기에, 『반구재유고』 등을 저술한 학자.
    '권성징': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 시약청어의, 내의원수의 등을 역임한 의관.
    '권세경': {'role': 'other'},  # 조선 - 조선 후기에, 회양부사, 청주목사 등을 역임한 문신.
    '권세숙': {'role': 'other'},  # 조선 - 조선 후기에, 정언, 홍문록, 교리 등을 역임한 문신.
    '권세연': {'role': 'other'},  # 근대/개항기 - 개항기 때, 경상북도 안동에서 항일의병투쟁을 전개한 의병장.
    '권세항': {'role': 'other'},  # 조선 - 조선 후기에, 승지, 경주부윤 등을 역임한 문신.
    '권세후': {'role': 'other'},  # 고려/고려 후기 - 고려후기 방호별감으로 양산성전투에 참전한 관리. 무신.
    '권수': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 장령, 동래부사 등을 역임한 문신.
    '권수평': {'role': 'other'},  # 고려 - 고려 후기에, 대정, 추밀원부사 등을 역임한 문신.
    '권순': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 사산감역, 양주목사, 동지중추부사 등을 역임한 문신.
    '권순명': {'role': 'other'},  # 근대/대한제국기 - 대한제국기 때, 김춘쇠 의병부대에서 포군으로 활동한 의병.
    '권순장': {'role': 'other'},  # 조선 - 조선시대 병자호란 때, 검찰사 김경징 등과 의병을 일으킨 문신.
    '권순창': {'role': 'other'},  # 조선 - 조선 후기에, 첨지중추부사, 돈녕부도정, 동지중추부사 등을 역임한 문신.
    '권승렬': {'role': 'other'},  # 현대/대한민국 - 일제강점기 때, 광주학생운동 및 여운형 · 안창호 검거 사건 등을 변론한 법조인.
    '권시': {'role': 'other'},  # 조선 - 조선 후기에, 승지, 찬선, 한성부우윤 등을 역임한 문신.
    '권시경': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 강원도관찰사, 예조판서, 판돈녕부사 등을 역임한 문신.
    '권신': {'role': 'other'},  # 고려 - 고려 전기에, 고려 건국에 대한 공으로 이등공신에 책록된 관리 · 공신.
    '권심규': {'role': 'scholar'},  # 조선 - 조선 후기에, 『송하집』 등을 저술한 학자.
    '권애라': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 경기도 개성군 송도면의 독립만세시위를 주도하였으며, 상하이로 건너가 애국부인회 등에서 활약하며 ...
    '권양': {'role': 'novelist'},  # 조선/조선 후기 - 조선  후기, 자녀교육의 지침서인 『영가가훈』을 저술한 문인.
    '권양성': {'role': 'other'},  # 조선 - 조선 후기에, 한성부서윤, 배천현감, 첨지중추부사 등을 역임한 문신.
    '권언': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 수양대군의 심복으로 활약하여 진위 겸 진향부사 등을 역임한 무신 · 공신.
    '권엄': {'role': 'other'},  # 조선 - 조선 후기에 병조판서 · 지중추부사 · 한성판윤 등을 역임한 문신.
    '권업': {'role': 'other'},  # 조선 - 조선 후기에, 형조판서, 대사헌, 참찬 등을 역임한 문신.
    '권연하': {'role': 'other'},  # 조선 - 조선 후기에, 선공감역, 돈녕부도정, 용양위호군 등을 역임한 문신.
    '권엽': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 군수, 오위도총부부총관 등을 역임한 문신.
    '권영': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 승지, 사직 등을 역임한 문신.
    '권영대': {'role': 'scholar'},  # 현대/대한민국 - 서울대학교 교수를 역임하며 광학 교육과 연구에 힘썼으며, 『자연과학개론』, 『일반물리학』, 『현대물리학』 등을 저...
    '권영만': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 때, 대한광복회를 조직하여 군자금을 모금하고 일본 고관 암살을 계획하는 등 항일무장투쟁을 전개한 독립...
    '권영우': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「바닷가의 환상」, 「섬으로 가는 길」, 「무제」 등을 그린 화가.
    '권영준': {'role': 'other'},  # 근대 - 일제강점기 때, 정교, 전리, 경의원 참의 등을 역임한 대종교인.
    '권영태': {'role': 'other'},  # 현대/대한민국 - 일제강점기 공산주의자그룹을 결성하고자 했던 사회주의운동가.
    '권영하': {'role': 'other'},  # 현대/대한민국 - 해방 이후 강릉단오제 「관노가면극」 전승자로 지정된 기예능보유자.
    '권영회': {'role': 'other'},  # 근대/대한제국기 - 대한제국기 때, 박민홍 의병부대에서 참모장으로 활동한 의병장.
    '권예': {'role': 'other'},  # 조선 - 조선 전기에, 대사헌, 이조판서, 우참찬 등을 역임한 문신.
    '권오기': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 경상좌도군적경차관, 사도시부정, 좌통례 등을 역임한 문신.
    '권오돈': {'role': 'other'},  # 근대 - 일제강점기 때, 무정부주의 비밀결사인 문예운동사를 조직하여 독립운동을 전개한 독립운동가.
    '권오병': {'role': 'other'},  # 현대/대한민국 - 광주지검 검사장, 법무부장관, 문교부장관 등을 역임한 법조인 · 정치인.
    '권오복': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 수찬, 교리 등을 역임한 문신.
    '권오설': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 고려공산청년회 책임비서를 지낸 사회주의운동가, 독립운동가.
    '권오익': {'role': 'scholar'},  # 현대/대한민국 - 성균관대학교 총장, 유네스코 한국위원회 위원 등을 역임하였고, 『상업경제학』, 『국제협력에서의 새로운 방향』 등을...
    '권오일': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「세일즈맨의 죽음」, 「욕망이라는 이름의 전차」, 「느릅나무 그늘의 욕망」 등을 연출한 연출가. 연극연출가.
    '권오직': {'role': 'other'},  # 현대/대한민국 - 북한 인민위원회 외무성 부수상, 북한 주중공 대사 등을 역임한 정치인 · 사회주의 운동가.
    '권오훈': {'role': 'other'},  # 현대/대한민국 - 일제강점기 때, 임시정부와 광복군을 지원하였으며, 해방 이후 호국군 106연대 부연대장, 국회의원 등을 역임한 군...
    '권옥연': {'role': 'other'},  # 근대/일제강점기 | 현대 - 해방 이후 「고향」 · 「부인상」 · 「꿈」 등을 그린 화가. 서양화가.
    '권완': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 행돈녕부판관 등을 역임하였으며, 단종복위운동에 가담했다는 죄로 처형된 문신.
    '권용': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 응교, 전한, 직제학 등을 역임한 문신.
    '권용일': {'role': 'other'},  # 근대 - 대한제국기 때, 이강년 의진에서 안동의 재산전투 등에 참전하며 항일의병투쟁을 전개한 의병.
    '권용정': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 「보부상」을 그린 화가.
    '권우': {'role': 'other'},  # 조선 - 조선 후기에, 도승지, 한성부좌윤 등을 역임한 문신.
    '권위': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 시랑, 판태복시사, 한림학사 등을 역임한 문신.
    '권유': {'role': 'other'},  # 조선 - 조선 후기에, 공조판서, 좌참찬, 대사헌 등을 역임한 문신.
    '권율': {'role': 'other'},  # 조선 중기에, 의주목사, 도원수 등을 역임한 문신.
    '권응생': {'role': 'other'},  # 조선 - 조선 후기에, 북부주부, 진천현감 등을 역임한 문신.
    '권응선': {'role': 'other'},  # 근대 - 조선 후기에, 사헌부대사헌, 봉상사제조, 강원도관찰사 등을 역임한 문신.
    '권응수': {'role': 'other'},  # 조선 - 조선 중기에, 경상도병마좌별장, 충청도방어사, 경상도방어사 등을 역임한 무신 · 의병장.
    '권응시': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 호조좌랑, 군위현감 등을 역임한 문신.
    '권응심': {'role': 'other'},  # 조선/조선 후기 - 조선시대 임진왜란 의병장으로 호분위 좌부장, 경상좌도 병마우후를 역임한 무신.
    '권응인': {'role': 'novelist'},  # 조선 - 조선 전기에, 『송계집』, 『송계만록』 등을 저술한 문인.
    '권응정': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 경주부윤, 안동부사, 동지중추부사 등을 역임한 문신.
    '권응창': {'role': 'other'},  # 조선 - 조선 전기에, 남양부사, 동지중추부사 등을 역임한 문신.
    '권의': {'role': 'other'},  # 고려 - 고려 후기에, 감찰시사, 판도총량 등을 역임한 관리.
    '권이복': {'role': 'scholar'},  # 조선 - 조선 후기에, 『만주문집』 등을 저술한 학자.
    '권이중': {'role': 'other'},  # 조선 - 조선 후기에, 종묘서직장, 장원서별제, 감찰 등을 역임한 문신.
    '권이진': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 판서, 평안도관찰사 등을 역임한 문신.
    '권익경': {'role': 'other'},  # 조선 - 조선 후기에, 안동부현감, 감찰 등을 역임한 문신.
    '권익관': {'role': 'other'},  # 조선 - 조선 후기에, 충청감사, 공조참의, 함경감사 등을 역임한 문신.
    '권인규': {'role': 'other'},  # 근대 - 대한제국기 때, 관동구군도창의소를 설치하여 관동방면의 의진을 규합한 의병장.
    '권일송': {'role': 'poet'},  # 현대/대한민국 - 해방 이후 『이 땅은 나를 술 마시게 한다』, 『바다의 여자』, 『비비추의 사랑』 등을 저술한 시인.
    '권일신': {'role': 'scholar'},  # 조선 - 조선 후기에, 추조적발사건, 진산사건과 관련된 학자 · 천주교인.
    '권일형': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 의주 부윤, 승지, 병조참판 등을 역임한 문신.
    '권자신': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 좌부승지, 우승지, 호조참판 등을 역임한 문신.
    '권장': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 홍문박사, 검열 등을 역임한 문신.
    '권장수': {'role': 'other'},  # 고려 - 고려 후기에, 판사재시사, 교주도병마사, 밀직부사 등을 역임한 관리 · 공신.
    '권재수': {'role': 'other'},  # 근대 - 조선 후기에, 박영효 암살미수사건과 관련된 정객.
    '권적': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 판서, 판의금부사, 우빈객 등을 역임한 문신.
    '권전': {'role': 'other'},  # 조선 - 조선 전기에, 정언, 이조좌랑, 수찬 등을 역임한 문신.
    '권절': {'role': 'other'},  # 조선 - 조선 전기에, 통정대부, 위장 등을 역임한 문신.
    '권절평': {'role': 'other'},  # 고려 - 고려 후기에, 좌승선, 추밀원사, 참지정사판호부사 등을 역임한 무신.
    '권정생': {'role': 'childrenauthor'},  # 현대/대한민국 - 해방 이후 『강아지똥』, 『몽실언니』 등을 저술한 아동문학가.
    '권정선': {'role': 'scholar'},  # 조선/조선 후기 | 근대/개항기 - 대한제국기 때, 『정음종훈』, 『음경』 등을 저술한 국어학자.
    '권정침': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 세자시강원설서 등을 역임한 문신.
    '권정필': {'role': 'other'},  # 근대/일제강점기 - 일제강점기에 의열단에 입단하여 항일 독립 투쟁을 전개한 독립운동가.
    '권제': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 좌참찬, 우찬성, 문형 등을 역임한 문신.
    '권종': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 개령현감, 금산군수 등을 역임한 문신.
    '권종록': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 사헌부집의, 부사직, 정위 등을 역임한 문신.
    '권종해': {'role': 'other'},  # 근대/대한제국기 | 근대/일제강점기 - 대한제국과 일제강점기에 의병운동과 민족운동을 펼친 독립운동가.
    '권주': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 성균관전적, 공주목사, 성주목사 등을 역임한 문신.
    '권주욱': {'role': 'scholar'},  # 조선 - 조선 후기에, 『동감』, 『포암문집』 등을 저술한 학자.
    '권준': {'role': 'other'},  # 근대 - 대한제국기 때, 경기북부 지역에서 항일의병투쟁을 전개한 의병장.
    '권중경': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 함경도관찰사, 형조참의, 호조참의 등을 역임한 문신.
    '권중도': {'role': 'scholar'},  # 조선 - 조선 후기에, 『퇴암집』, 『금양기선록』, 『노산자경록』 등을 저술한 학자.
    '권중돈': {'role': 'other'},  # 현대/대한민국 - 국방부장관, 민권당 고문 등을 역임한 정치인.
    '권중석': {'role': 'other'},  # 근대 - 정교, 대형호, 원로원 참의 등을 역임한 대종교인.
    '권중원': {'role': 'other'},  # 의병 활동을 적극 지원한 공적으로 2019년 대통령표창을 추서한 독립운동가 · 독립유공자.
    '권중집': {'role': 'other'},  # 조선 - 조선 후기에, 돈령부참봉, 진산군수 등을 역임한 문신.
    '권중현': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 농상공부대신, 법부대신, 군부대신, 자작, 중추원 고문 등을 역임한 관료 · 친일반민족행위자 ·...
    '권중화': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 판문하부사, 우의정, 영의정부사 등을 역임한 문신 · 의원.
    '권지': {'role': 'other'},  # 조선 - 조선 후기에, 장령, 서장관, 좌부승지 등을 역임한 문신.
    '권진': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 한성판윤, 우참찬, 병조판서 등을 역임한 문신.
    '권진규': {'role': 'scholar'},  # 현대 - 「자각상」, 「소녀의 얼굴」, 「여인상」 등의 작품을 낸 조각가.
    '권진응': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 자의 등을 역임한 문신.
    '권진인': {'role': 'other'},  # 고려 - 고려 전기에, 단학 설화에 나오는 도교인.
    '권질': {'role': 'other'},  # 조선 - 조선 전기에, 집경전, 순릉, 후릉참봉, 광흥창봉사 등을 역임한 문신.
    '권집': {'role': 'other'},  # 조선 - 조선 후기에, 대동찰방, 한성부서윤, 하동부사 등을 역임한 문신.
    '권징': {'role': 'other'},  # 조선 - 조선 중기에, 병조판서, 경기관찰사 등을 역임한 문신.
    '권찬': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 지중추부사, 정헌대부, 호조판서 등을 역임한 문신.
    '권창식': {'role': 'scholar'},  # 조선 - 조선 후기에, 『잠계문집』 등을 저술한 학자.
    '권창진': {'role': 'scholar'},  # 조선 - 조선 후기에, 『아맹일고』 등을 저술한 학자.
    '권채': {'role': 'other'},  # 조선 - 조선 전기에, 대사성, 우승지 등을 역임한 문신.
    '권채근': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 경상남도 진주의 독립만세시위를 주도한 혐의로 체포되어 옥중에서 순국한 독립운동가.
    '권척': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 호조좌랑, 예조좌랑, 예문관봉교 등을 역임한 문신.
    '권철': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 우의정, 좌의정, 영의정 등을 역임한 문신.
    '권철신': {'role': 'scholar'},  # 조선/조선 후기 - 조선 후기에, 『시칭』, 『대학설』 등을 저술한 학자 · 천주교인.
    '권첨': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 대사간, 전라도관찰사, 충청도관찰사 등을 역임한 문신.
    '권첩': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 형조참판, 경주부윤 등을 역임한 문신.
    '권총': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 세자익위사의 위솔, 익찬, 지중추부사 등을 역임한 문신.
    '권축': {'role': 'scholar'},  # 근대 - 조선 후기에, 홍문관수찬, 시강원 겸 문학, 이조정랑 등을 역임한 문신.
    '권춘란': {'role': 'other'},  # 조선 - 조선 중기에, 성균관사성, 청송부사, 홍문관수찬 등을 역임한 문신.
    '권충': {'role': 'other'},  # 조선 - 조선 전기에, 우군동지총제, 공조판서, 의정부찬성사 등을 역임한 문신.
    '권치문': {'role': 'other'},  # 근대 - 개항기 때, 약현천주교회를 기공한 천주교인.
    '권칭': {'role': 'other'},  # 조선 - 조선 후기에, 성균관사예 등을 역임한 문신.
    '권쾌복': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 대구사범학교 학생의 항일 비밀결사인 다혁당 당수로 활동한 독립운동가.
    '권태석': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 조선민흥회와 신간회, 조선공산당 등에서 활동한 사회주의운동가, 독립운동가, 정치인.
    '권태시': {'role': 'other'},  # 조선 - 조선 후기에, 장악원주부, 회덕현감 등을 역임한 문신.
    '권태양': {'role': 'other'},  # 현대/대한민국 - 해방 이후 좌우합작위원회 서무부장, 민족자주연맹 비서처 총무, 중앙집행위원 등을 역임한 정치인.
    '권태완': {'role': 'scholar'},  # 현대/대한민국 - 국내 식품 과학 연구를 국제적 수준으로 발전시킨 학자.
    '권태욱': {'role': 'other'},  # 현대/대한민국 - 제헌국회의원, 제2대 국회의원을 역임한 정치인.
    '권태일': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 형조참판 등을 역임한 문신.
    '권태하': {'role': 'other'},  # 현대 - 조선마라톤보급회 위원장, 대한육상경기연맹 회장 등을 역임한 체육인.
    '권태호': {'role': 'other foreigner'},  # 근대/일제강점기 - 1930년 3월 일본 니혼[日本]음악학교를 졸업한 테너 성악가로 일제강점기 「봄나들이」, 「눈 · 꽃 · 새」,...
    '권태훈': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 『민족비전 정신수련법』 · 『천부경의 비밀과 백두산족 문화』 등을 저술하며 단학의 역사에 족적을 남긴 ...
    '권태희': {'role': 'other'},  # 현대/대한민국 - 제헌국회의원, 문교사회분과위원장 등을 역임한 정치인 · 종교인.
    '권필': {'role': 'poet'},  # 조선 - 조선 중기의 시인.
    '권필칭': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 선전관, 장기현감, 삭주부사, 평안도방어사, 경상좌도수군절도사 등을 지낸 무관.
    '권한공': {'role': 'other'},  # 고려 - 고려 후기에, 찬성사, 도첨의정승, 태자좌찬선 등을 역임한 문신.
    '권한성': {'role': 'other'},  # 조선 - 조선 후기에, 사헌부지평, 이조정랑, 대동찰방 등을 역임한 문신.
    '권해': {'role': 'other'},  # 조선 - 조선 후기에, 대사헌, 호조참의, 평양부윤 등을 역임한 문신.
    '권행': {'role': 'other'},  # 고려 - 고려 전기에, 고려와 후백제의 고창전투에서 고려군에 가담하여 공을 세워, 태조 왕건으로부터 권씨 성을 하사받았던 호족 · 공신.
    '권헌': {'role': 'other'},  # 조선 - 조선 전기에, 사섬시직장, 장악원직장, 지평 등을 역임한 문신.
    '권혁': {'role': 'other'},  # 조선 - 조선 후기에, 함경도관찰사, 대사헌, 이조판서 등을 역임한 문신.
    '권현룡': {'role': 'other'},  # 고려 - 고려 후기에, 밀직부사, 강릉도부원수, 판덕창부사 등을 역임한 무신.
    '권협': {'role': 'other'},  # 조선 - 조선 중기에, 대사헌, 전라도감사, 예조판서 등을 역임한 문신.
    '권형': {'role': 'other'},  # 조선 - 조선 중기에, 장악원첨정, 세자시강원필선, 예빈시부정 등을 역임한 문신.
    '권호문': {'role': 'novelist'},  # 조선/조선 전기 - 조선 전기에, 「독락팔곡」, 「한거십팔곡」, 『송암집』 등을 저술한 문인.
    '권호윤': {'role': 'scholar'},  # 조선 - 조선 후기에, 『동빈만록』 등을 저술한 학자.
    '권홍': {'role': 'other'},  # 고려 - 조선 전기에, 판돈령부사, 예조판서, 영돈령부사 등을 역임한 문신.
    '권화': {'role': 'other'},  # 고려 - 조선 전기에, 도성제조, 삼사우복야 등을 역임한 문신.
    '권확': {'role': 'other'},  # 조선 - 조선 후기에, 여주목사, 좌부승지, 동부승지 등을 역임한 문신.
    '권환': {'role': 'poet'},  # 근대 - 일제강점기 때, 『자화상』, 『윤리』 등을 저술한 시인.
    '권황': {'role': 'other'},  # 조선 - 조선 후기에, 고양군수, 마전군수, 지중추부사 등을 역임한 문신.
    '권흠': {'role': 'other'},  # 조선 - 조선 후기에, 대사성, 이조참의, 승지 등을 역임한 문신.
    '권희': {'role': 'other'},  # 조선 - 조선 중기에, 도승지, 한성부좌윤, 형조참판 등을 역임한 문신.
    '권희맹': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 나주목사, 장악원정, 강원도관찰사 등을 역임한 문신.
    '권희인': {'role': 'other'},  # 조선 - 조선시대 때, 서천포만호, 옥천군수 등을 역임한 무신.
    '권희학': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 곤양군수, 운산군수, 장연부사 등을 역임한 무신 · 공신.
    '궤홍': {'role': 'other'},  # 조선 - 조선 후기에, 보월사 해원의 제자가 되어 법맥을 계승한 승려.
    '귀금': {'role': 'other'},  # 고대/남북국 - 신라 헌강왕 때 거문고의 명인.
    '귀보부인': {'role': 'other'},  # 고대/남북국/통일신라 - 신라의 제44대 왕, 민애왕의 어머니로, 선의태후로 추봉된 왕족.
    '귀산': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 신라의 아막성전투에 참전한 장수.
    '귀승부인': {'role': 'other'},  # 고대/남북국/통일신라 - 신라의 제41대 왕, 헌덕왕의 왕비.
    '귀실집사': {'role': 'other foreigner'},  # 고대/삼국/백제 - 남북국시대 때, 일본에 망명한 백제의 유민.
    '귀실집신': {'role': 'other foreigner'},  # 고대/삼국 - 삼국시대 때, 일본에서 활동한 백제의 의원.
    '귀지': {'role': 'other foreigner'},  # 고대/삼국 - 삼국시대 때, 백제의 사신으로 일본에 구원병을 요청한 부흥운동가.
    '귀진': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 신라의 법왕사를 창건한 관리.
    '균여': {'role': 'scholar'},  # 고려전기 「보현십원가(普賢十願歌)」, 『수현방궤기(搜玄方軌記)』, 『공목장기(孔目章記)』 등을 저술한 승려.
    '극상': {'role': 'other'},  # 고대/남북국 - 통일신라 효공왕 때, 아버지인 안장에게 거문고 비법을 전수받은 거문고 명인.
    '극정': {'role': 'other'},  # 고대/남북국 - 남북국시대 때, 통일 신라의 사찬을 역임한 장수.
    '극종': {'role': 'other'},  # 고대/남북국 - 남북국시대 때, 통일 신라에서 아버지인 안장에게 「표풍」 등을 전수받은 거문고 명인.
    '극현': {'role': 'other'},  # 조선 - 조선 후기에, 대흥사 신월선사의 제자가 되어 법맥을 계승한 승려.
    '근구수왕': {'role': 'other'},  # 고대/삼국 - 백제의 제14대(재위:375년~384년) 왕.
    '근랑': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 이찬 관등이었던 대일의 아들로, 많은 낭도들을 거느린 신라의 화랑.
    '근비': {'role': 'other'},  # 고려 - 고려의 제32대 왕, 우왕의 왕비.
    '근적': {'role': 'other'},  # 조선 - 조선 후기에, 대흥사 주지가 되어 가선대부의 품계를 받은 승려.
    '근종': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 때, 신라의 이찬 관등을 역임한 귀족, 반란자.
    '근초고왕': {'role': 'other'},  # 백제의 제13대(재위:346년~375년) 왕.
    '근헌': {'role': 'other'},  # 근대 - 개항기 때, 취암의 제자이자 초의로부터 보살계를 받은 승려.
    '금강': {'role': 'other'},  # 고대/남북국 - 남북국시대 때, 후백제의 시조인 견훤의 넷째 왕자.
    '금관후': {'role': 'other'},  # 고려/고려 전기 - 고려 전기, 제11대 왕 문종의 아들인 왕자.
    '금기철': {'role': 'other'},  # 근대 - 대한제국기 때, 경상북도와 영동지역에서 항일의병투쟁을 전개한 의병장.
    '금난수': {'role': 'other'},  # 조선 - 조선 중기에, 직장, 장례원사평, 봉화현감 등을 역임하였으며, 정유재란이 발발하자 의병을 일으켜 항쟁한 문신 · 의병장.
    '금능인': {'role': 'other'},  # 근대 - 일제강점기 「타향살이」, 「휘파람」, 「사막의 한」 등을 작사한 음악인.
    '금달연': {'role': 'other'},  # 근대 - 대한제국기 때, 경상북도 영주에서 의병을 조직하였다가, 이강년 의병부대에 들어가 별초종사, 선봉장 등으로 활동한 의병장.
    '금룡': {'role': 'other'},  # 현대/대한민국 - 운문사 주지를 역임한 승려.
    '금보': {'role': 'scholar'},  # 조선 - 조선 전기에, 『사서질의』, 『심근강의』, 『매헌집』 등을 저술한 학자.
    '금사': {'role': 'other'},  # 고대/남북국 - 남북국시대 때, 당나라에서 유학하여 대승과 소승의 경전을 공부한 승려.
    '금석주': {'role': 'other'},  # 근대 - 개항기 때, 경상북도 봉화에서 의병을 조직하였다가, 유인석 의진에 들어가 소토장으로 활동한 의병장.
    '금선자': {'role': 'other'},  # 조선 - 조선 선조 때, 전란의 조짐을 보고 전쟁 발발을 예언한 도교인.
    '금성규': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 진사, 전적, 사예 등을 역임한 문신 · 서예가.
    '금성대군': {'role': 'other'},  # 조선/조선 전기 - 조선의 제4대 왕, 세종의 여섯번째 왕자.
    '금수현': {'role': 'other'},  # 현대/대한민국 - 오페라 「피리와 칼」, 「그네」 등을 작곡한 음악가.
    '금시양': {'role': 'scholar'},  # 조선 - 조선 후기에, 『가례부해』, 『삼기당문집』 등을 저술한 학자.
    '금식': {'role': 'other'},  # 고대/남북국 - 남북국시대 때, 태봉국의 사화진(沙火鎭)전투(戰鬪)에 참전한 장수.
    '금와': {'role': 'other'},  # 고대/초기국가 - 부여의 제4대(재위: BCE.60~BCE.20) 왕.
    '금용': {'role': 'other'},  # 고대/남북국 - 남북국시대 때, 평양에서 평양성주장군으로 세력을 떨친 호족.
    '금원 김씨': {'role': 'poet'},  # 조선 - 조선후기 『죽서시집』 발문, 『호동서락기』 등을 저술한 시인.
    '금원군': {'role': 'other'},  # 조선 - 조선의 제11대 왕, 중종의 서자인 왕자.
    '금월': {'role': 'other'},  # 조선 - 조선후기 사교과와 『화엄경』, 『사분율』, 『범망경』 등을 공부한 승려.
    '금윤선': {'role': 'other'},  # 조선 - 조선 중기에, 의서습독관, 훈련원정 등을 역임하였으며, 임진왜란 때 의병장으로 활약한 무신 · 공신.
    '금응협': {'role': 'other'},  # 조선 - 조선 중기에, 집경전참봉, 하양현감 등을 역임한 문신.
    '금응훈': {'role': 'other'},  # 조선 - 조선 중기에, 영춘현감, 양천현감, 의흥현감 등을 역임한 문신.
    '금의': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 풍기군수, 청송부사 등을 역임한 문신.
    '금이영': {'role': 'other'},  # 조선 - 조선 전기에, 승문원부교리, 청주판관, 승문원교리 등을 역임한 문신.
    '금일': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 때, 신라의 대야성전투 당시 사지 등을 역임했던 관리.
    '금주리': {'role': 'other foreigner'},  # 고대/삼국/백제 - 삼국시대 때, 일본 와카야마현 구마모토시에 있는 우전팔번신사 소장 인물화상경을 제작한 백제의 장인.
    '금훈': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 각문부사, 초유사 등을 역임한 문신.
    '금휘': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 동북면병마사, 대장군 등을 역임한 무신.
    '급리': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 때, 신라의 아찬으로 내외병마사를 담당한 관리.
    '긍법': {'role': 'other'},  # 근대/개항기 - 대한제국기 봉원사 대웅전 극락구품도, 불암사 대웅전 아미타불도 등의 불화를 제작한 승려. 화승.
    '긍선': {'role': 'other'},  # 조선 - 19세기에, 초의 의순(草衣意恂)과 선 논쟁을 펼친 것으로 유명한 호남의 선승.
    '긍양': {'role': 'other'},  # 고려 - 삼국시대 신라의 구산선문 중 희양산문(曦陽山門)을 대표하는 승려.
    '긍엽': {'role': 'other'},  # 근대/개항기 - 대한제국기 영지사 「지장보살도」 · 「신중도」 등을 그린 화가. 승려.
    '긍척': {'role': 'other'},  # 조선/조선 후기 - 조선후기 흥국사 응진전 석가모니불도, 흥국사 관음전 관음보살도, 송광사 오십전 53불도 등을 그린 승려. 화승.
    '긍탄': {'role': 'other'},  # 현대/대한민국 - 일제강점기 때, 보문사 주지를 역임한 승려.
    '기건': {'role': 'other'},  # 조선 - 조선 전기에, 인순부윤, 평안도관찰사, 판중추원사 등을 역임한 문신.
    '기대승': {'role': 'other'},  # 조선 - 조선 전기에, 성균관대사성, 대사간, 공조참의 등을 역임한 문신.
    '기대정': {'role': 'other'},  # 조선 - 조선 중기에, 지평, 장령 등을 역임한 문신.
    '기대항': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 이조참판, 한성부판윤 등을 역임한 문신.
    '기루왕': {'role': 'other'},  # 고대/삼국 - 백제의 제3대(재위: 77년~128년) 왕.
    '기륜': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에 삼사좌사 · 찬성사 · 덕산부원군 등을 역임하였으며, 동생인 기황후의 권세를 믿고 횡포를 일삼다가 ...
    '기림이사금': {'role': 'other'},  # 고대/삼국 - 신라의 제15대(재위: 298년~310년) 왕.
    '기마차': {'role': 'other'},  # 고대/삼국 - 백제 6세기 인물로 왜(倭)의 궁중에 파견된 악사(樂師).
    '기만헌': {'role': 'other'},  # 조선 - 조선 후기에, 정언, 지평, 부사 등을 역임한 문신.
    '기보갈문왕': {'role': 'other'},  # 고대/삼국 - 신라의 제19대 왕, 눌지마립간의 동생이자 제22대 지증왕의 아버지로, 습보와 동일인으로 추정되는 왕족.
    '기본한기': {'role': 'other'},  # 고대/삼국/가야 - 대가야의 왕.
    '기산도': {'role': 'other'},  # 근대/대한제국기 - 대한제국기 때, 을사조약이 강제 체결되자 결사대를 조직하여 을사오적 암살을 계획한 독립운동가.
    '기삼만': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 원나라 기황후의 족제(族弟)인 권신.
    '기삼연': {'role': 'other'},  # 근대 - 대한제국기 때, 호남창의맹소의 대장으로 활약하며 항일의병투쟁을 전개한 의병장.
    '기새인티무르': {'role': 'other'},  # 고려 - 고려 후기에, 권신이었던 기철(奇轍)의 아들로 태어나 원나라 평장 등을 역임한 관리.
    '기석복': {'role': 'other'},  # 현대/대한민국 - 해방 이후 북한에서 공산당 중앙위원 등을 역임한 정치인. 공산주의자.
    '기수발': {'role': 'other'},  # 조선 - 조선 후기에, 홍문관정자, 예조좌랑, 정언 등을 역임한 문신.
    '기순격': {'role': 'other'},  # 조선 - 조선 후기에, 해남현감, 장흥부사 등을 역임한 문신.
    '기양연': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 사복시정, 부교리, 부수찬 등을 역임한 문신.
    '기언정': {'role': 'other'},  # 조선 - 조선 후기에, 대사간, 대사헌, 공조판서 등을 역임한 문신.
    '기연': {'role': 'other'},  # 조선/조선 후기 - 조선후기 송광사 천자암 지장시왕도, 흥국사 극락암 칠성도 등의 불화를 제작한 승려. 화승(畵僧).
    '기오공': {'role': 'other'},  # 고대/삼국 - 신라 진지왕의 비, 지도부인의 부친인 귀족.
    '기온': {'role': 'other'},  # 고려/고려 후기 - 고려 후기 국왕 원종의 측근 세력으로 활약한 무신.
    '기용숙': {'role': 'scholar'},  # 현대 - 서울대학교 의과대학 미생물학 교수를 역임한 미생물학자.
    '기우만': {'role': 'other'},  # 근대 - 개항기 때, 호남지방에서 기삼연과 합세하여 호남창의 총수로 활약한 의병장.
    '기원': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 한림학사, 원사 등을 역임하였으며, 동생인 기황후의 권세를 믿고 횡포를 일삼다가 공민왕에 의해 숙...
    '기윤숙': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 문하시랑 동중서문하평장사, 문하시랑평장사 등을 역임한 무신.
    '기윤위': {'role': 'other'},  # 고려 - 고려 후기에, 지유, 대장군, 가발병마사 등을 역임한 무신.
    '기윤헌': {'role': 'scholar'},  # 조선 - 조선 후기에, 세자시강원문학, 장령, 안악군수 등을 역임한 문신.
    '기의헌': {'role': 'scholar'},  # 조선 - 조선 후기에, 『기은유고』 등을 저술하였으며, 정묘호란과 병자호란이 발발하자 의병을 일으켜 항쟁한 학자 · 의병.
    '기익헌': {'role': 'other'},  # 조선 - 조선시대 때, 이괄의 난에 가담한 장수.
    '기인보': {'role': 'other'},  # 고려/고려 후기 - 고려후기 거란유종의 침입 당시의 관리. 무신.
    '기자오': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 산원, 총부산랑, 영안왕 등을 역임한 무신.
    '기자헌': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 좌승지, 강원도관찰사, 좌의정 등을 역임한 문신.
    '기재': {'role': 'scholar'},  # 조선 - 조선 후기에, 『식재집』 등을 저술한 학자.
    '기전': {'role': 'other'},  # 조선/조선 후기 - 개항기 합천 해인사 대광전 삼신불도, 부산 범어사 석가26보살도 등의 불화를 제작한 승려. 화승(畵僧).
    '기전해': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 가야연맹 반피국의 상수위를 역임한 귀족.
    '기정룡': {'role': 'scholar'},  # 조선 - 조선 후기에, 『낙암유고』 등을 저술한 학자.
    '기정진': {'role': 'scholar'},  # 조선/조선 후기 - 조선 후기에, 「정자설」, 「이통설」, 『노사집』, 『답문유편』 등 중요한 성리학 저술을 남긴 학자.
    '기존정': {'role': 'other'},  # 고려 - 고려 후기에, 연주에서 김취려와 군사를 이끌고 거란군을 물리쳐 대승을 거둔 무신.
    '기종': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 신라의 사찬으로 감문주군주를 역임한 지방관.
    '기준': {'role': 'other'},  # 조선 - 조선 전기에, 장령, 시강관, 응교 등을 역임한 문신.
    '기준격': {'role': 'other'},  # 조선 - 조선 후기에, 정언, 병조좌랑, 예조좌랑 등을 역임한 문신.
    '기철': {'role': 'other'},  # 고려/고려 후기 - 고려 후기 요양행성 평장정사를 역임한 부원세력.
    '기탁성': {'role': 'other'},  # 고려 - 고려 후기에, 판병부사, 문하시랑평장사 판이부사 등을 역임한 무신.
    '기학경': {'role': 'other'},  # 조선 - 조선 후기에, 사간원정언, 무장현감, 홍문관수찬 등을 역임한 문신.
    '기현': {'role': 'other'},  # 고려 - 고려 후기에, 신돈의 심복이 되어 횡포를 부린 권신.
    '기협': {'role': 'other'},  # 조선 - 조선 후기에, 황해도관찰사, 선천부사 등을 역임한 문신.
    '기형도': {'role': 'poet'},  # 해방 이후 「안개」, 『입 속의 검은 잎』 등을 저술한 시인.
    '기홍': {'role': 'other'},  # 조선 - 조선후기 월출산 장선을 은사로 득도하고 성옥의 법맥을 계승한 승려.
    '기홍석': {'role': 'other'},  # 고려 - 고려후기 군부판서 응양군상장군, 밀직부사, 동지밀직사 감찰제헌 등을 역임한 무신.
    '기홍수': {'role': 'other'},  # 고려/고려 후기 - 고려후기 문하시랑 동중서문하 평장사, 벽상삼한삼중대광 문하시랑 동중서문하평장사 판이부사 등을 역임한 무신.
    '기홍연': {'role': 'scholar'},  # 조선 - 조선 후기에, 『주서표기』, 『용산유고』 등을 저술한 학자.
    '기화': {'role': 'other'},  # 조선/조선 전기 - 조선 초기 불교계를 대표하는 선승이자 학승으로 호불 논서  『현정론』의 저자.
    '기황후': {'role': 'other'},  # 고려/고려 후기 - 고려 후기, 몽골제국 제14대 카안 순제 토곤테무르의 황후.
    '기효간': {'role': 'scholar'},  # 조선 - 조선 중기에, 벼슬에 오르지 않고 학문과 후진 양성에 전념하여 호남의 은덕군자로 불린 학자.
    '기효근': {'role': 'other'},  # 조선 - 조선시대 남해현령, 통정대부 등을 역임한 무신.
    '기효증': {'role': 'scholar'},  # 조선 - 조선 중기에, 형조정랑, 군기시첨정 등을 역임하였으며, 임진왜란이 발발하자 의병을 일으켜 항쟁한 학자 · 의병장.
    '기훤': {'role': 'other'},  # 고대/남북국 - 남북국시대 통일신라의 조정에 반기를 들어 죽주에서 반란을 일으킨 호족. 반란자.
    '길나': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라 중대의 장수.
    '길달': {'role': 'other'},  # 고대/삼국 - 삼국시대 신라의 진평왕 때 도깨비가 인간으로 나타난 전설의 인물로 집사를 담당한 관리.
    '길문': {'role': 'other'},  # 고대/삼국 - 삼국시대 신라의 아찬, 파진찬 등을 역임한 관리.
    '길삼봉': {'role': 'other'},  # 조선/조선 전기 - 조선 전기 선조대 정여립 사건의 연루자 심문 과정에서 언급되었던 가상의 인물.
    '길선': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 아찬으로 모반에 실패해 백제로 건너간 관리.
    '길선주': {'role': 'other'},  # 근대 - 일제강점기 장대현교회에서 시무한 목사.
    '길숙': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 신문왕 납비 때 시비를 궁내로 모셔오는 임무를 수행한 관리.
    '길영수': {'role': 'other'},  # 근대 - 개항기 과천군수, 한성부판윤 등을 역임한 관리.
    '길영희': {'role': 'other'},  # 현대/대한민국 - 해방 이후 인천중학교 교장, 제물포고등학교 교장 등을 역임한 교육자.
    '길옥윤': {'role': 'other'},  # 해방 이후 「서울의 찬가」, 「사랑은 영원히」, 「당신은 모르실거야」 등을 발표한 작곡가.
    '길운절': {'role': 'other'},  # 조선/조선 후기 - 조선후기 정여립의 모반군에 모사로 참여한 주모자.
    '길원': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 아찬(阿飡) 관등의 관리.
    '길의': {'role': 'scholar'},  # 고대/남북국/통일신라 - 남북국시대 『추일어장왕택연신라객』, 『종가길야궁』 등을 저술한 통일신라의 승려. 의관.
    '길인': {'role': 'other'},  # 고려/고려 후기 - 고려 후기, 상장군으로 최충헌의 정변에 저항하였던 이의민 계의 무신.
    '길인화': {'role': 'other'},  # 조선 - 조선 후기에, 상서원직장, 사축서별제, 통례원인의 등을 역임한 문신.
    '길재': {'role': 'scholar'},  # 조선/조선 전기 - 조선 전기에, 『야은집』, 『야은속집』, 『야은언행습유록』 등을 저술하였으며, 이색, 정몽주와 함께 고려의 삼은...
    '길재호': {'role': 'other'},  # 현대/대한민국 - 해방 이후 5, 16군사정변 당시의 군인. 정치인.
    '길진섭': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 「옹진바다 전망」 · 「농촌의 모녀상 」 · 「바닷가 풍경」 등의 작품을 그린 화가.
    '길진형': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 신성학교 교사를 역임한 교육자.
    '길회': {'role': 'other'},  # 조선 - 조선 중기에, 직강, 헌납, 장령 등을 역임한 문신.
    '김가기': {'role': 'other'},  # 고대/남북국 - 삼국시대 신라에 도교를 전한 최초의 도교인. 문장가.
    '김가진': {'role': 'other'},  # 근대 - 개항기 농상공부대신, 중추원의장 등을 역임한 관리.
    '김각': {'role': 'other'},  # 조선 - 조선 중기에, 용궁현감, 온성판관 등을 역임한 문신.
    '김각현': {'role': 'other'},  # 근대 - 조선 후기에, 제실회계심사국장, 대원왕대원비원침천봉시검찰당상 등을 역임한 문신.
    '김간': {'role': 'other'},  # 조선 - 조선 후기에, 청나라에서 내무부주사, 사고전서관부총재 등을 역임한 문신.
    '김감': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 경상도 도사 등의 관직을 역임한 문신.
    '김감불': {'role': 'other'},  # 조선/조선 전기 - 조선전기 단천연은법을 개발한 기술자.
    '김갑': {'role': 'other'},  # 근대 - 일제강점기 때, 임시정부에서 법무총장 대리, 노동총판, 국무위원 등을 역임한 독립운동가.
    '김갑수': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 내무부 차관, 대법원 대법관, 경성대학교 법문학부 교수 등을 역임한 법조인. 정치인.
    '김갑순': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 중추원참의, 유성온천주식회사 사장, 조선임전보국단 이사 등을 역임한 기업인. 정치인, 친일반민족행위자.
    '김갑우': {'role': 'other'},  # 고려 - 고려후기 천우위대장군, 대호군 등을 역임한 무신.
    '김갑태': {'role': 'other'},  # 현대/대한민국 - 한국전쟁 당시 강원도 김화의 748고지전투(피의 능선전투)에 참전한 군인.
    '김강': {'role': 'other foreigner'},  # 근대 - 일제강점기 때, 간민회 일본조사부원, 동제회 평의원, 대한국민회 중부경호부장 등을 역임한 독립운동가.
    '김개': {'role': 'other'},  # 조선 - 조선 후기에, 승지, 좌윤 등을 역임한 문신.
    '김개국': {'role': 'other'},  # 조선 - 조선 중기에, 정랑, 군수 등을 역임한 문신.
    '김개남': {'role': 'other'},  # 근대/개항기 - 19세기 후반 동학농민운동 당시 호남창의소 총관령 등을 역임한 동학교단의 호남 대접주.
    '김개물': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 감찰사, 사헌지평, 전부시승 등을 역임한 문신.
    '김개시': {'role': 'other'},  # 조선/조선 후기 - 조선후기 제15대 광해군의 총애를 받아 권세를 누린 궁녀.
    '김개원': {'role': 'other'},  # 고대/남북국 - 삼국시대 신라 제29대 태종무열왕의 일곱째 아들인 왕자.
    '김거공': {'role': 'other'},  # 고려 - 고려 전기에, 판삼사사, 지문하성사, 호부상서 등을 역임한 문신.
    '김거두': {'role': 'other'},  # 고려 - 조선 전기에, 『삼국사기』의 발문을 작성한 문신.
    '김거복': {'role': 'other'},  # 근대/대한제국기 - 조선후기 「수궁가」 중 용왕탄식대목에 뛰어났던 판소리의 명창.
    '김거실': {'role': 'scholar'},  # 고려 - 고려 전기에, 내시 대부소경 태자문학, 태자궁의 행궁별감 등을 역임한 문신.
    '김거웅': {'role': 'other'},  # 고려/고려 전기 - 고려전기 거돈사지의 「거돈사원공국사승묘탑비문」을 쓴 서예가.
    '김건': {'role': 'playwright novelist'},  # 근대 - 해방 이후 「눈물의 38선」 · 「한강물은 흐른다」 · 「직공」 등의 작품을 낸 극작가.
    '김건수': {'role': 'other'},  # 조선 - 조선 후기에, 홍문관응교, 김해부사, 승정원우부승지 등을 역임한 문신.
    '김건순': {'role': 'scholar'},  # 조선 - 조선후기 『천당지옥론』 · 『성교전서』 등을 저술한 천주교인.
    '김건안': {'role': 'other foreigner'},  # 남북국시대 통일신라의 일길찬으로 일본에 파견된 관리.
    '김건종': {'role': 'other'},  # 조선/조선 후기 - 조선후기 「호리건곤도」를 그린 화가.
    '김견수': {'role': 'other'},  # 조선/조선 전기 - 조선전기 평안도절도사, 전주부윤 등을 역임한 무신.
    '김겸': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 공안부윤, 정헌대부, 경상도관찰사 등을 역임한 문신.
    '김겸광': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 예조판서, 경상도관찰사, 평안도절도사 등을 역임한 문신.
    '김경': {'role': 'other'},  # 고려/고려 후기 - 고려후기 무진정변과 관련된 환관.
    '김경구': {'role': 'other'},  # 조선/조선 후기 - 조선후기 첨지중추부사를 역임한 의관. 화가.
    '김경근': {'role': 'other'},  # 조선 - 조선 중기에, 왜적의 침입을 예측하고 산성 수축을 건의하였다가 투옥되었으며, 임진왜란이 발발하자 의병을 일으켜 항쟁한 의병.
    '김경남': {'role': 'other'},  # 근대 - 조선후기 거문고 삼절 중 하나인 거문고명인.
    '김경로': {'role': 'other'},  # 조선/조선 후기 - 조선후기 경성판관, 김해부사, 첨지중추부사 등을 역임한 무신.
    '김경문': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 조선과 청나라 간의 외교적 사안을 담당한 역관.
    '김경배': {'role': 'other'},  # 현대/대한민국 - 일제강점기 때, 반일투쟁 혐의로 2년간 복역하였으며 한국전쟁 때 납북되어 북한에서, 재북평화통일촉진협의회 중앙집행...
    '김경복': {'role': 'other'},  # 조선 - 조선시대 군수, 부사 등을 역임한 무신.
    '김경부': {'role': 'other'},  # 고려 - 고려후기 김사미와 효심의 난과 관련된 무신.
    '김경서': {'role': 'other'},  # 조선 - 조선시대 전라도병마절도사, 정주목사, 평안도병마절도사 등을 역임한 무신.
    '김경석': {'role': 'other'},  # 조선 - 조선시대 전라도수군도절제사, 전라우도방어사 등을 역임한 무신.
    '김경선': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 우참찬, 판의금부사 등을 역임한 문신.
    '김경손': {'role': 'other'},  # 고려/고려 후기 - 고려 후기, 전라도지휘사 · 추밀원지주사 · 추밀원부사 등을 역임한 무신.
    '김경수': {'role': 'other'},  # 조선 - 조선 중기에, 장악원주부, 예조좌랑, 군자감정 등을 역임하였으며, 임진왜란이 발발하자 의병을 일으켜 항쟁한 의병.
    '김경숙': {'role': 'other'},  # 현대/대한민국 - 대한민국의 노동운동가로, 1970년대 YH무역 노동조합에서 민주노조운동을 전개한 인물.
    '김경승': {'role': 'scholar'},  # 근대/일제강점기|현대 - 해방 이후 「충무공 이순신장군상」 · 「안중근의사상」 · 「세종대왕상」 등의 작품을 낸 조각가.
    '김경여': {'role': 'other'},  # 조선 - 조선 후기에, 대사간, 충청도관찰사 등을 역임한 문신.
    '김경용': {'role': 'other'},  # 고려 - 고려 전기에, 문하시중, 수태부 판상서이부사 등을 역임한 문신.
    '김경운': {'role': 'other'},  # 근대 - 대한제국기 때, 박래병 의병군으로 활동하며 군자금 모금 및 무장투쟁을 전개한 의병.
    '김경원': {'role': 'other'},  # 근대/일제강점기 | 현대 - 해방 이후 대한민국미술전람회 심사위원을 역임한 화가.
    '김경유': {'role': 'scholar'},  # 조선 - 조선 후기에, 동지중추부사, 오위장 등을 역임하였으며, 『노은유고』를 저술한 문신.
    '김경장': {'role': 'scholar'},  # 조선 - 조선 후기에, 『예원집설』, 「천문성상도」, 『구암문집』 등을 저술한 학자.
    '김경재': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 독립신문 기자, 신한독립당 비서과장, 조선지광 기자 등을 역임한 언론인. 사회주의운동가.
    '김경제': {'role': 'other'},  # 고려 - 고려후기 홍건적의 난 당시의 무신.
    '김경지': {'role': 'other'},  # 조선 - 조선 후기에, 병조정랑, 강원도도사, 개성경력 등을 역임한 문신.
    '김경직': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 낭천현감, 병조좌랑, 사도시정 등을 역임한 문신.
    '김경징': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 도승지, 한성부판윤, 강도검찰사 등을 역임한 문신.
    '김경탁': {'role': 'scholar foreigner'},  # 현대/대한민국 - 고려대학교 철학과 교수로 재임해 동양철학학풍을 이끈 중국철학 분야의 개척자로, 『유교철학사상개요』, 『중국철학개론...
    '김경태': {'role': 'other'},  # 근대 - 일제강점기 때, 대한제국 군인 출신으로, 의병으로 활동하다가 대한광복회에서 군자금 모집 활동을 전개한 독립운동가.
    '김경희': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 숭의여학교 교사로 근무하면서 비밀결사인 송죽회를 조직하고, 평양 만세시위를 주도하였으며, 임시정...
    '김계': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 병조참지, 승문원부제조, 이조참판 등을 역임한 문신.
    '김계광': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 성균관직강, 춘추관편수관, 풍기군수 등을 역임한 문신.
    '김계금': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 지평, 의성현령, 집현전권지학유 등을 역임한 문신.
    '김계락': {'role': 'other'},  # 조선 - 조선 후기에, 형조판서, 예조판서, 우참찬 등을 역임한 문신.
    '김계명': {'role': 'other'},  # 고대/남북국/통일신라 - 통일신라의 제48대 경문왕의 아버지로, 파진찬에 임명되어 집사성시중 등을 역임한 왕족.
    '김계봉': {'role': 'other'},  # 고려 - 고려후기 명주부사를 역임한 무신.
    '김계부': {'role': 'other'},  # 고려/고려 전기 - 고려전기 좌우기군장군, 병부시랑 등을 역임한 관리. 무신.
    '김계선': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 이왕직 아악수를 역임한 음악인. 대금명인.
    '김계숙': {'role': 'scholar'},  # 현대/대한민국 - 서울대학교 문리과대학과 사범대학 교수로 재임하였으며, 『근세문화사』, 『근세철학사』, 『헤겔연구』 등을 저술한 철학자.
    '김계우': {'role': 'other'},  # 조선 - 조선 전기에, 참상판관, 청도군수, 공조참판 등을 역임한 문신.
    '김계종': {'role': 'other'},  # 조선/조선 전기 - 조선전기 영안남도병마절도사, 동지중추부사, 겸사복장 등을 역임한 무신.
    '김계지': {'role': 'other'},  # 조선/조선 전기 - 조선전기 판해주목사, 강원도병마도절제사 등을 역임한 무신.
    '김계창': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 우승지, 도승지, 이조참판 등을 역임한 문신.
    '김계하': {'role': 'other'},  # 조선 - 조선 후기에, 의주부윤, 개성유수, 함경도관찰사 등을 역임한 문신.
    '김계행': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 고령현감, 홍문관부수찬, 대사간 등을 역임한 문신.
    '김계휘': {'role': 'other'},  # 조선 - 조선 전기에, 동지의금부사, 평안도관찰사, 예조참판 등을 역임한 문신.
    '김고': {'role': 'other'},  # 고려 - 고려 전기에, 지추밀원사, 중서시랑평장사 등을 역임한 문신.
    '김곡': {'role': 'scholar'},  # 고대/남북국/통일신라 - 남북국시대 때, 숙위학생으로 당나라에서 유학한 통일신라의 학자.
    '김곤': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 선전관, 부령부사, 경원부사 등을 역임한 문신.
    '김공량': {'role': 'other'},  # 조선 - 조선 중기에, 내수사별좌 등을 역임한 문신.
    '김공망': {'role': 'other'},  # 조선 - 조선 전기에, 사간원, 병조좌랑, 해주목사 등을 역임한 문신.
    '김공석': {'role': 'other'},  # 고려 - 고려 후기 중랑장, 분도장군 등을 역임한 무신.
    '김공정': {'role': 'other'},  # 고려 - 고려 전기, 묘청의 난에 가담한 의관.
    '김공천': {'role': 'poet'},  # 현대/대한민국 - 해방 이후 『한라의 바람노래』를 저술한 시인.
    '김관': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 동지중추부사, 전주부윤, 전라도관찰사 등을 역임한 문신.
    '김관석': {'role': 'other'},  # 현대/대한민국 - 해방 이후 한국기독교 교회협의회 총무, 기독교방송 사장 등을 역임한 목사. 사회운동가, 민주화 운동가, 에큐메니컬...
    '김관성': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 광한단, 모험대 등을 조직해 항일투쟁을 전개하였으며, 대한통의부 검무감 등을 역임한 독립운동가.
    '김관식': {'role': 'poet'},  # 현대/대한민국 - 해방 이후 「귀양가는 길」 · 「다시 광야에」 · 「춘잠에게」 등을 저술한 시인.
    '김관오': {'role': 'other'},  # 근대 - 일제강점기 때, 한국독립당 충칭지구당부위원장, 임시정부 경위대 대장 등을 역임한 독립운동가.
    '김관의': {'role': 'scholar'},  # 고려 - 고려 후기에, 검교군기감 등을 역임하였으며, 『편년통록』을 저술한 관리.
    '김관장': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 대아찬, 총관 등을 역임한 관리.
    '김관주': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 이조판서, 광주유수, 우의정 등을 역임한 문신.
    '김관준': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 서도소리 명창으로 「배뱅이굿」의 창시자인 서도소리의 명창.
    '김관택': {'role': 'other'},  # 현대/대한민국 - 일제강점기, 성모학원 교사와 해성학교 교장 등을 역임한 교육자. 천주교 전교사 및 총회장을 지낸 민족운동가.
    '김관현': {'role': 'other'},  # 근대/개항기 | 근대/일제강점기 - 일제강점기 충청남도지사, 함경남도지사, 중추원 참의 등을 역임한 관료. 군인 · 친일반민족행위자.
    '김관호': {'role': 'scholar'},  # 근대 - 일제강점기 「해질녘」 · 「호수」 · 「친구의 초상」 등의 작품을 그린 화가.
    '김광': {'role': 'other'},  # 조선 - 조선 전기에, 정난공신들을 따라 일한 공으로 세조 때 녹훈되어 장교를 역임한 천인 출신의 관리 · 공신.
    '김광국': {'role': 'other'},  # 조선/조선 후기 - 조선후기 수의, 가선대부, 동지중추부사 등을 역임한 의관. 서화수집가.
    '김광균': {'role': 'poet'},  # 해방 이후 『기항지』, 『황혼가』 등을 저술한 시인. 실업가.
    '김광두': {'role': 'other foreigner'},  # 조선/조선 후기 - 조선 후기 임진왜란 때 함창 황령사에서 창의(倡義)하여 일본군을 격퇴한 의병장.
    '김광률': {'role': 'other'},  # 현대/대한민국 - 해방 이후 올빼미부대 대침투작전 당시의 군인.
    '김광부': {'role': 'other'},  # 고려 - 고려후기 수어간, 계림윤, 합포도순문사 등을 역임한 무신.
    '김광서': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 만주와 연해주에서 무장 항일운동을 한 독립운동가.
    '김광선': {'role': 'other'},  # 근대 - 일제강점기 영산서무부장, 원평교무, 총부순교무 등을 역임한 원불교인.
    '김광섭': {'role': 'poet'},  # 근대 - 광복 이후 『마음』, 『성북동 비둘기』, 『김광섭시전집』 등을 저술한 시인. 독립운동가.
    '김광세': {'role': 'other'},  # 조선 - 조선 후기에, 병조참판, 강화유수, 대사헌 등을 역임한 문신.
    '김광수': {'role': 'novelist'},  # 조선/조선 후기 - 조선후기 문인들에게 고동 서화 수집에 대한 가치를 일깨운 수장가.
    '김광식': {'role': 'other'},  # 현대/대한민국 - 해방 이후 서울시립국악관현악단 악장 등을 역임한 대금명인.
    '김광악': {'role': 'other'},  # 조선 - 조선 후기에, 황해도도사, 현릉령, 흡곡현령 등을 역임한 문신.
    '김광엽': {'role': 'other'},  # 조선 - 조선 중기에, 흥해군수, 이조정랑, 성균관사성 등을 역임한 문신.
    '김광옥': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 만주에서 조선혁명군 유격대장, 보위대장, 총사령 부관 등을 역임한 독립운동가.
    '김광우': {'role': 'other'},  # 현대/대한민국 - 해방 이후 자교교회목사, 기독교대한감리회 중부연회 연회장, 배화학원 이사장 등을 역임한 목사. 교육가.
    '김광욱': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 양서관향사, 우참찬 등을 역임한 문신.
    '김광원': {'role': 'scholar'},  # 조선 - 조선 전기에, 이문습독관을 역임하다가 안처겸의 옥사애 연루되어 유배된 학자.
    '김광익': {'role': 'poet'},  # 조선 - 조선후기 『반포유고』를 저술한 여항시인.
    '김광재': {'role': 'other'},  # 고려 - 고려 후기에, 첨의평리, 삼사우사, 전리판서 등을 역임한 문신.
    '김광제': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 국채보상운동과 노동운동에 참여한 독립운동가.
    '김광조': {'role': 'other'},  # 고려 - 고려 후기에, 군부판서, 밀직사, 동북면도순위사 등을 역임한 관리 · 공신.
    '김광주': {'role': 'novelist'},  # 근대 - 해방 이후 「태양은 누구를 위하여」, 「석방인」 등을 저술한 작가. 소설가.
    '김광준': {'role': 'other'},  # 현대/대한민국 - 헌법기초위원, 고시사법행정 양과위원, 국회의원 등을 역임한 법조인 · 정치인.
    '김광중': {'role': 'other'},  # 고려 - 고려 전기에, 간의대부, 비서감, 상서우승 등을 역임한 문신.
    '김광진': {'role': 'other'},  # 근대 - 일제강점기 때, 정의부의용대 제1대장 등을 역임하면서 항일무장투쟁을 전개한 독립운동가.
    '김광찬': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 청풍군수, 파주목사, 동지중추부사 등을 역임한 문신.
    '김광철': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 동지중추부사, 전라도관찰사 등을 역임한 문신.
    '김광혁': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 광주목사, 예문관응교, 동부승지 등을 역임한 문신.
    '김광현': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 부제학, 청주목사 등을 역임한 문신.
    '김괴': {'role': 'other'},  # 조선 - 조선 전기에, 이조좌랑, 정언, 헌납 등을 역임한 문신.
    '김굉': {'role': 'scholar'},  # 조선 - 조선 후기에, 단양군수, 세자시강원문학, 예조참판 등을 역임한 문신.
    '김굉필': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 사헌부감찰, 형조좌랑 등을 역임하였으며, 김종직의 제자로 무오사화와 갑자사화에 연루되어 처형된 문신.
    '김교': {'role': 'other'},  # 조선/조선 전기 - 조선전기 공조판서, 평안도병마절도사, 평안도관찰사 등을 역임한 무신.
    '김교락': {'role': 'other'},  # 근대 - 일제강점기 때, 전라남도 나주 등지에서 군자금 모금 활동을 전개한 독립운동가.
    '김교만': {'role': 'other'},  # 현대/대한민국 - 해방 이후 서울대학교 미술대학 교수를 역임한 교육자. 산업디자이너.
    '김교성': {'role': 'other'},  # 근대 - 해방 이후 「자명고 사랑」 · 「울고 넘는 박달재」 · 「고향역」 등을 만든 작곡가.
    '김교신': {'role': 'other'},  # 근대 - 일제강점기 무교회주의를 제창한 교육자. 종교인.
    '김교제': {'role': 'novelist'},  # 근대/일제강점기 - 일제강점기 「목단화」, 「비행선」, 「현미경」 등을 저술한 소설가. 번역, 번안작가.
    '김교준': {'role': 'other'},  # 현대/대한민국 - 일제강점기 근대 양의학계의 선구자로 알려진 의사. 종교인.
    '김교중': {'role': 'other'},  # 현대/대한민국 - 국회의원을 역임하며 전라남도 일대 민정조사반, 교통체신위원회 등에서 활동한 정치인.
    '김교창': {'role': 'other'},  # 근대 - 일제강점기 때, 수원군 송산면 사강리의 독립만세시위에 참여한 독립운동가.
    '김교헌': {'role': 'other'},  # 근대 - 일제강점기 대종교 제2대 교주.
    '김구': {'role': 'other'},  # 일제강점기 때, 임시정부 주석 등을 역임하였으며, 한인애국단을 조직해 이봉창과 윤봉길의 의거를 주도하고, 신민회, 한국광복군 등에서...
    '김구경': {'role': 'scholar'},  # 근대/일제강점기 - 일제강점기, 『교간당사본능가사자기(校刊唐寫本楞伽師資記)』를 발간하여 초기 선종사 연구의 발판을 마련한 불교학자.
    '김구년': {'role': 'other'},  # 고려 - 고려 후기에, 동지밀직사사, 밀직부사상의, 절일사 등을 역임한 문신.
    '김구덕': {'role': 'other'},  # 조선 - 조선 전기에, 한성부윤, 지돈녕부사, 판돈녕부사 등을 역임한 문신.
    '김구명': {'role': 'other'},  # 조선 - 조선 후기에, 동지중추원사 등을 역임한 문신.
    '김구상': {'role': 'other'},  # 조선/조선 후기 - 조선시대 내의원주부, 상의원판관, 지평현감 등을 역임한 의관.
    '김구용': {'role': 'other'},  # 고려 - 고려 후기에, 삼사좌윤, 성균관대사성, 판전교시사 등을 역임한 문신.
    '김구응': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 충청남도 천안의 아우내 독립만세시위를 주도하는 과정에서 순국한 교육자 · 독립운동가.
    '김구익': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 『조선무산오운육기론』, 『동의사상임해지남』 등을 저술한 학자. 의학자.
    '김구정': {'role': 'other'},  # 현대/대한민국 - 해방 이후 군산여자고등학교 교감, 군산대학교 교수 등을 역임한 교육자. 천주교회사가, 언론인.
    '김구주': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 강원감사, 승지, 공조참판 등을 역임한 문신.
    '김구현': {'role': 'other'},  # 근대 - 조선 후기에, 공조판서, 중추원일등의관, 궁내부특진관 등을 역임한 문신.
    '김국광': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 동지중추원사, 병조판서, 영중추부사 등을 역임한 문신.
    '김국연': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라에서 당나라에 사신으로 파견된 관리.
    '김국태': {'role': 'novelist'},  # 현대/대한민국 - 해방 이후 「우리교실의 전설」, 「귀는 왜 줄창 열려 있나」 등을 저술한 소설가.
    '김군관': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 신라 김흠돌의 반란 당시의 장수. 대신.
    '김군수': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 일본인과 함께 브라질로 이민한 교민.
    '김군승': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 아찬을 역임한 장수.
    '김군정': {'role': 'other'},  # 고려 - 고려 후기에, 원외랑, 전의부령, 좌대언 등을 역임한 문신.
    '김권': {'role': 'other'},  # 조선 - 조선 중기에, 연안부사, 사복시첨정, 호조참판 등을 역임한 문신.
    '김권수': {'role': 'other'},  # 근대/개항기 | 근대/일제강점기 - 일제강점기 「유하미인」 · 「청조」 · 「춘규」 등을 그린 화가.
    '김궤': {'role': 'other'},  # 고려 - 고려 후기에, 예부시랑, 좌간의대부, 판비서성사 등을 역임한 문신.
    '김귀': {'role': 'other'},  # 고려 - 고려후기 전리판서, 동북면병마사, 첨의평리 등을 역임한 무신.
    '김귀수': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「수영야류」 할미 역 전승자로 인정된 예능보유자.
    '김귀영': {'role': 'other'},  # 조선 - 조선 중기에, 예조판서, 병조판서, 우의정 등을 역임한 문신.
    '김귀희': {'role': 'other'},  # 조선 - 조선 중기에, 장사군관, 수군절도사 등을 역임한 관리 · 공신.
    '김규': {'role': 'other'},  # 조선 - 조선 전기에, 지평, 이조정랑, 전한 등을 역임한 문신.
    '김규동': {'role': 'poet'},  # 근대/일제강점기 | 현대 - 해방 이후 『나비와 광장』 · 『죽음 속의 영웅』 · 『느릅나무에게』 등을 저술한 시인.
    '김규면': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 만주에서 독립운동 활동을 한 사회주의운동가.
    '김규서': {'role': 'other'},  # 조선 - 조선 후기에, 동부승지 등을 역임한 문신.
    '김규식': {'role': 'scholar'},  # 일제강점기 때, 파리강화회의에서 대한민국임시정부 대표 명의의 탄원서를 제출하였고, 해방 이후 이승만의 남한단독정부수립안에 반대하며 ...
    '김규열': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 조선공산당 제3차대회 코민테른 파견 대표, 조선공산당재건설준비위원회 중앙간부 등을 역임한 사회주의운동가.
    '김규오': {'role': 'scholar'},  # 조선 - 조선 후기에, 『최와집』 등을 저술한 학자.
    '김규진': {'role': 'other'},  # 근대 - 일제강점기에 최초의 근대적 영업 화랑을 개설한 서화가. 사진가.
    '김규철': {'role': 'other'},  # 근대/대한제국기 - 대한제국기 때, 단양, 죽령, 청풍 등지에서 의병대장으로 활약하였고, 국권 피탈 이후 군자금 모금 활동을 전개한...
    '김규택': {'role': 'scholar'},  # 근대/일제강점기 | 현대 - 일제강점기 망부석, 억지 춘향전 등의 작품을 그린 만화가. 삽화가.
    '김규하': {'role': 'other'},  # 조선 - 조선 후기에, 지평, 정악원정, 장령 등을 역임한 문신.
    '김규홍': {'role': 'other'},  # 근대 - 조선 후기에, 장례원경, 시종원경, 귀족원경 등을 역임한 문신.
    '김규환': {'role': 'scholar'},  # 현대 - 해방 이후 한국방송윤리위원회 위원장, 한국신문학회 회장 등을 역임한 언론인. 학자.
    '김규희': {'role': 'other'},  # 근대 - 조선 후기에, 중추원외랑, 내부참서관, 한성부판윤 등을 역임한 문신.
    '김균': {'role': 'other'},  # 조선 - 조선 전기에, 중추원부사, 보국숭록좌찬성 등을 역임한 문신.
    '김균정': {'role': 'other'},  # 고대/남북국/통일신라 - 통일신라의 제38대 원성왕의 손자로, 대아찬에 임명되어 시중, 상대등 등을 역임하였으며, 흥덕왕 사후에 왕...
    '김극개': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 경기관찰사, 형조참판 등을 역임한 문신.
    '김극검': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 호조참판, 동지중추부사, 지중추부사 등을 역임한 문신.
    '김극기': {'role': 'scholar'},  # 조선 - 조선 전기에, 『지월당유고』 등을 저술한 문신.
    '김극성': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 예조판서, 우의정 등을 역임한 문신.
    '김극일': {'role': 'other'},  # 조선 - 조선 전기에, 밀양부사, 내자시정, 사헌부장령 등을 역임한 문신.
    '김극종': {'role': 'other'},  # 고려 - 고려전기 간천대장군을 역임한 무신.
    '김극핍': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 이조판서, 호조판서, 좌찬성 등을 역임한 문신.
    '김극해': {'role': 'other'},  # 고려 - 고려 전기에, 중상서영, 분사대부시승, 검교군기감 등을 역임한 문신.
    '김근': {'role': 'scholar'},  # 조선 - 조선 후기에, 『오우당집』 등을 저술한 학자.
    '김근배': {'role': 'other'},  # 근대 - 조선 후기에, 성균관박사 등을 역임한 문신.
    '김근사': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 우의정, 좌의정, 영의정 등을 역임한 문신.
    '김근순': {'role': 'other'},  # 조선 - 조선 후기에, 부제학, 대사성, 직제학 등을 역임한 문신.
    '김근태': {'role': 'other'},  # 현대/대한민국 - 대한민국의 인권과 민주주의를 위해 헌신한 사회운동가이자 정치가.
    '김근행': {'role': 'other'},  # 조선 - 조선 후기에, 태자익위사세마, 김포군수 등을 역임한 문신.
    '김긍률': {'role': 'other'},  # 고려 - 고려전기 제2대 혜종의 비 청주원부인과 제3대 정종의 비 청주남원부인의 부친으로 원보를 역임한 척신.
    '김기': {'role': 'scholar'},  # 조선 - 조선 중기에, 임진왜란이 발발하자 의병을 일으켜 화왕산성전투에 참전하였고, 『북애문집』 등을 저술하며 후진 양성과 고을의 ...
    '김기대': {'role': 'other'},  # 조선 - 조선 후기에, 경기도관찰사, 함경도관찰사, 예조판서 등을 역임한 문신.
    '김기덕': {'role': 'other'},  # 현대/대한민국 - 대한민국의 영화감독.
    '김기동': {'role': 'scholar'},  # 현대 - 동국대학교 국어국문학과 교수를 역임하였으며, 『국문학개론』, 『한국고대소설개론』, 『한국문헌설화전집』 등을 저술하여 고소설...
    '김기두': {'role': 'scholar'},  # 현대/대한민국 - 서울대학교 법과대학 학장, 법무부 정책자문위원 등을 역임한 법학자.
    '김기득': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 의열단의 단원으로 밀양폭탄사건에 가담하였으며, 신간회, 조선공산당 재조직 준비위원회 등에서 활동...
    '김기련': {'role': 'other foreigner'},  # 현대/대한민국 - 해방 이후 프랑스리모주국제칠보비엔날레 금상, 민속예술상 등을 수상한 공예가. 칠보공예가.
    '김기례': {'role': 'scholar'},  # 조선 - 조선 후기에, 역학에 주력하여 「팔괘성정물상」, 「역요선의강목」, 『묵천집』 등을 저술한 학자.
    '김기림': {'role': 'poet critic'},  # 근대 - 일제강점기 『기상도』, 『태양의 풍속』 등을 저술한 시인. 문학평론가.
    '김기범': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 경상남도 합천군 삼가장터의 독립만세시위를 주도하는 과정에서 순국한 독립운동가.
    '김기서': {'role': 'other'},  # 조선/조선 후기 - 조선후기 「단발령도」를 그린 화가.
    '김기석': {'role': 'scholar'},  # 현대/대한민국 - 서울대학교 사범대학 교수 및 학장, 한국교육학회 초대회장 등을 역임하였으며, 『철학개론』, 『현대정신사』, 『윤리...
    '김기선': {'role': 'scholar'},  # 조선 - 조선 후기에, 『기서문집』 등을 저술한 학자.
    '김기성': {'role': 'other'},  # 조선 - 조선 후기에, 서사관, 광은부위 등을 역임한 문신.
    '김기손': {'role': 'other'},  # 고려 - 고려 후기에, 문하시랑동중서문하평장사, 문하시랑평장사 등을 역임한 문신.
    '김기수': {'role': 'other'},  # 현대 - 해방 이후 한국사상 처음으로 복싱동양챔피언 타이틀을 획득한 체육인.
    '김기영': {'role': 'scholar'},  # 현대 - 해방 이후 「봉선화」 · 「하녀」 등의 작품에 관여한 영화인. 영화감독.
    '김기용': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 대구에서 활약한 독립운동가.
    '김기웅': {'role': 'scholar'},  # 현대/대한민국 - 『조선반도의 벽화고분』, 『고분유물』 등을 저술하며 초창기 고고학 발전에 기여한 고고학자.
    '김기전': {'role': 'other'},  # 현대/대한민국 - 일제강점기 때, 잡지 『개벽』의 주필을 역임하였고, 방정환 등과 함께 천도교소년회를 조직하여 소년운동을 전개한 언...
    '김기종': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 당상관, 호조판서 등을 역임한 문신.
    '김기중': {'role': 'scholar'},  # 근대/일제강점기 - 일제강점기 서울의 중앙학교, 보성전문학교 등을 운영한 육영사업가.
    '김기진': {'role': 'poet critic'},  # 근대/일제강점기 - 일제강점기 「가련아」 · 「님의 부르심을 받들고서」 · 「나도 가겠습니다」 등을 저술한 시인. 평론가.
    '김기찬': {'role': 'other'},  # 조선 - 조선 후기에, 대사간, 이조참의, 이조참판 등을 역임한 문신.
    '김기창': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 신민회, 흥사단 등에서 항일투쟁을 전개한 독립운동가.
    '김기천': {'role': 'other'},  # 근대 - 일제강점기 영광지부장, 총부서무부장, 선원교무 등을 역임한 원불교인.
    '김기철': {'role': 'other'},  # 현대/대한민국 - 제헌의원, 민주동지회 대표간사, 제5대 국회의원 등을 역임한 정치인.
    '김기추': {'role': 'other'},  # 현대/대한민국 - 일제강점기 때, 학교에서 교육투쟁을 전개하였고, 청년동맹 위원장을 역임하였으며, 해방 이후, 조선건국준비위원회 간...
    '김기풍': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 임천군수, 평양서윤, 충주목사 등을 역임한 문신.
    '김기하': {'role': 'other'},  # 조선 - 조선 후기에, 후릉참봉 등을 역임한 문신.
    '김기한': {'role': 'other'},  # 근대 - 일제강점기 때, 대한독립단을 조직하여 국내지단 결성과 군자금 모금 활동을 전개한 독립운동가.
    '김기형': {'role': 'scholar'},  # 현대/대한민국 - 1967년부터 1971년까지, 과학기술처 초대 장관을 역임한 과학자이자 정치가.
    '김기호': {'role': 'scholar'},  # 조선 - 조선 후기, 『구령요의』, 『소원신종』, 『봉교자술』 등을 저술한 천주교 지도자.
    '김기홍': {'role': 'scholar'},  # 현대 - 한양대학교 의과대학 원장, 대한의학협회 부회장 등을 역임하며, 국내 의학의 임상병리 검사기술 전문화에 기여한 의학자.
    '김기후': {'role': 'other'},  # 조선 - 조선 후기에, 지돈녕부사, 도총관, 한성부판윤 등을 역임한 문신.
    '김길임': {'role': 'other'},  # 근대 - 해방 이후 「강강술래」의 전승자로 지정된 예능보유자.
    '김길창': {'role': 'other foreigner'},  # 근대 - 일제강점기, 일본기독교 조선장로교단 및 조선교단 경남 교구장으로서 적극적으로 부일협력 활동을 한 장로교 목사.
    '김길통': {'role': 'other'},  # 조선 - 조선 전기에, 지중추부사가, 한성부판윤, 호조판서 등을 역임한 문신.
    '김길호': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 내의로 근무하던 중 치료하던 문종이 사망하여 직첩을 환수당하였다가 복귀한 의관 · 공신.
    '김낙': {'role': 'other'},  # 고려 - 고려 전기에, 이부시랑 등을 역임하였으며, 자신을 신라 원성왕의 먼 자손이라 사칭하였던 경주인 김융대에게 뇌물을 받았다는 ...
    '김낙선': {'role': 'other'},  # 근대 - 대한제국기 때, 이용서 의진에서 선봉장으로 활약한 의병.
    '김낙수': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 경상남도 울산군 언양읍의 독립만세시위를 주도한 혐의로 체포되어 옥중에서 순국한 독립운동가.
    '김낙철': {'role': 'other'},  # 근대/개항기 | 근대/대한제국기 - 19세기 후반~20세기 초 동학농민운동과 천도교 활동에 참여한 천도교인.
    '김낙풍': {'role': 'other'},  # 조선 - 조선 후기에, 종부시정 겸 편수관, 병조참의 등을 역임한 문신.
    '김낙행': {'role': 'scholar'},  # 조선 - 조선 후기에, 『기법질의』, 『강록간보고의』, 『구사당집』 등을 저술한 학자.
    '김난상': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 응교, 직제학, 대사성 등을 역임한 문신.
    '김난섭': {'role': 'other'},  # 근대 - 일제강점기 때, 대한독립단에서 군자금 모금 활동을 전개한 독립운동가.
    '김난손': {'role': 'other foreigner'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 사찬으로서 일본에 파견된 사신.
    '김난순': {'role': 'other'},  # 조선 - 조선후기 대사헌, 우참찬, 이조판서 등을 역임한 문신. 서예가.
    '김남극': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 만주에 동창학교와 북일학교를 설립하여 민족의식을 고취하였고, 경신참변에 의해 사망한 교육자 · ...
    '김남득': {'role': 'other'},  # 고려/고려 후기 - 고려 후기 상주목사, 서해도관찰사, 문하평리 등을 역임한 문신.
    '김남수': {'role': 'other'},  # 조선/조선 전기 - 조선전기 판사복시사, 공조판서, 판좌군도총제부사 등을 역임한 무신.
    '김남일': {'role': 'other'},  # 조선 - 조선 후기에, 상의원별제, 홍산현감, 괴산군수 등을 역임한 문신.
    '김남주': {'role': 'poet'},  # 현대/대한민국 - 해방 이후 『진혼가』, 『나의 칼 나의 피』, 『조국은 하나다』 등을 저술한 시인.
    '김남중': {'role': 'essayist'},  # 현대 - 해방 이후 『전남일보』사장, 한국신문협회 부회장 등을 역임한 언론인. 수필가.
    '김남천': {'role': 'novelist critic'},  # 근대 - 일제강점기 「대하」, 「물」, 「생의 고민」 등을 저술한 소설가. 문학비평가..
    '김내범': {'role': 'other'},  # 근대 - 일제강점기 간도노회초대노회장, 국민회 분회장 등을 역임한 목사. 독립운동가.
    '김내성': {'role': 'novelist'},  # 근대 - 일제강점기, 『마인』, 『백가면』, 「백사도」 등을 저술한 탐정소설가.
    '김녕': {'role': 'other'},  # 조선 - 조선 후기에, 전적, 사예, 예안현감 등을 역임한 문신.
    '김노겸': {'role': 'other'},  # 조선 - 조선 후기에, 홍산현감 등을 역임한 문신.
    '김노경': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 광주부유수, 지돈녕부사, 판의금부사 등을 역임한 문신.
    '김노선': {'role': 'scholar'},  # 조선 - 조선 후기에, 향교의 교장이 되어 어린 학생을 가르치는 교안 「유의」를 만들었으며, 『기계문집』 등을 저술한 학자.
    '김노응': {'role': 'other'},  # 조선 - 조선 후기에, 형조판서, 한성판윤, 병조판서 등을 역임한 문신.
    '김노진': {'role': 'other'},  # 조선 - 조선 후기에, 형조판서, 우참찬 등을 역임한 문신.
    '김노차': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라 제29대 태종무열왕의 넷째 아들인 왕자.
    '김녹연': {'role': 'other'},  # 고려 - 고려 후기에, 경상주도안찰사, 우간의대부 등을 역임한 문신.
    '김녹영': {'role': 'other'},  # 현대/대한민국 - 신민당 상무위원, 제12대 국회부의장 등을 역임한 정치인.
    '김녹주': {'role': 'other'},  # 근대 - 일제강점기 김정문의 제자로 송만갑협률사에서 활동한 판소리의 명창.
    '김뉴': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 이조참판 등을 역임한 문신.
    '김능유': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 때, 사신으로 당에 파견되었다가 귀국길에 익사한 통일신라의 왕족.
    '김니': {'role': 'scholar'},  # 조선 - 조선 중기에, 『유당집』 등을 저술한 문신.
    '김다수': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 사신으로 당과 왜에 파견된 관리.
    '김단': {'role': 'other'},  # 고려 - 고려전기 장주방어사, 시어사 겸 동로병마사 등을 역임한 무신.
    '김단갈단': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 하정사로 당나라에 파견되어 위위소경의 관직을 받은 관리.
    '김단야': {'role': 'other'},  # 근대 - 일제강점기 고려공산청년당 책임비서, 전조선민중운동자대회 준비위원 등을 역임한 사회주의운동가.
    '김달복': {'role': 'other'},  # 고대/남북국 - 남북국시대 신라의 제17대 내물마립간의 7세손으로 잡찬 관등의 귀족.
    '김달상': {'role': 'other'},  # 고려 - 고려 후기에, 밀직부사, 한양윤, 양광도도순문사 등을 역임한 문신 · 공신.
    '김달순': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 우의정 등을 역임한 문신.
    '김달진': {'role': 'poet scholar'},  # 현대/대한민국 - 해방 이후 『올빼미의 노래』, 『큰 연꽃 한 송이 피기까지』 등을 저술한 시인. 한학자.
    '김달현': {'role': 'other'},  # 현대/대한민국 - 일제강점기 때, 무산자동지회를 설립하는 등 사회주의운동을 벌였고, 해방 이후 북한에서, 최고인민회의 대의원 등을 ...
    '김달호': {'role': 'other'},  # 현대/대한민국 - 서울고등검찰청 차장검사, 사회대중당 중앙집행위원장, 제5대 민의원 등을 역임한 정치인 · 법조인.
    '김담': {'role': 'other'},  # 조선 - 조선 후기에, 판결사 등을 역임한 문신.
    '김담수': {'role': 'scholar'},  # 조선 - 조선 중기에, 『서계일고』 등을 저술한 학자.
    '김당': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 좌찬성 등을 역임한 문신.
    '김대건': {'role': 'other'},  # 조선/조선 후기 - 1846년 병오박해 때 서울 새남터에서 처형된 신부로 한국인 최초의 사제.
    '김대규': {'role': 'other'},  # 근대 - 대한제국기 때, 경상도, 강원도에서 항일의병투쟁을 전개한 의병장.
    '김대근': {'role': 'other'},  # 조선 - 조선 후기에, 이조판서, 좌찬성, 우찬성 등을 역임한 문신.
    '김대금': {'role': 'other'},  # 고대/남북국 - 남북국시대 태봉국 궁예(弓裔)의 부하로 신라의 명주(溟州) 침공 당시의 장수.
    '김대덕': {'role': 'other'},  # 조선 - 조선 후기에, 동지의금부사, 부총관, 형조참판 등을 역임한 문신.
    '김대래': {'role': 'other'},  # 조선 - 조선 중기에, 홍문관부응교, 사인, 직제학 등을 역임한 문신.
    '김대례': {'role': 'other'},  # 근대 - 해방 이후 「진도씻김굿」 전승자로 지정된 예능보유자. 무속인.
    '김대명': {'role': 'other'},  # 조선 - 조선 중기에, 풍기군수 등을 역임한 문신.
    '김대문': {'role': 'other'},  # 고대/남북국/통일신라 - 신라 성덕왕 때 활약한 진골 출신 관료.
    '김대봉': {'role': 'poet'},  # 현대/대한민국 - 일제강점기 『맥』, 『무심』 등을 저술한 시인. 의사.
    '김대비': {'role': 'other foreigner'},  # 고대/남북국 - 남북국시대 통일신라에서 중국 선종의 육조인 혜능의 목을 훔쳐 하동군 쌍계사에 봉안하였다고 하는 승려.
    '김대섭': {'role': 'other'},  # 조선 - 조선 중기에, 의금부도사, 조지서별제 등을 역임한 문신.
    '김대성': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 때, 중시 등을 역임하였으며, 불국사를 창건한 통일신라의 귀족 · 관리.
    '김대우': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 학무국 사회교육과장, 참여관, 전라북도지사 등을 역임한 관료. 친일반민족행위자.
    '김대유': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 정언, 칠원현감, 전적 등을 역임한 문신.
    '김대인': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 임진왜란 당시 해상 및 육상에서 활약하였던 무관.
    '김대재': {'role': 'other'},  # 고려 - 고려후기 무오정변, 임연의 정변 등과 관련된 무신.
    '김대정': {'role': 'other'},  # 조선 - 조선시대 임진왜란 때, 연안부사로 연안성을 굳게 지킨 문신.
    '김대중': {'role': 'other'},  # 현대/대한민국 - 대한민국 제15대 대통령을 지내고 노벨평화상을 수상한 정치인.
    '김대지': {'role': 'other'},  # 근대 - 일제강점기 때, 임시정부 내무위원, 국내조사원 등을 역임하고 의열단의 주요간부로 활약한 독립운동가.
    '김대현': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「자장가」 · 「들국화」 · 「고향의 노래」 등을 만든 작곡가.
    '김대흥': {'role': 'other'},  # 근대/개항기 - 개항기 갑신정변, 한성조약 등과 관련된 의사(義士).
    '김대희': {'role': 'scholar'},  # 근대 - 대한제국기 때, 보성전문학교 강사, 광신상업학교 교사 등을 역임한 교육자 · 경제학자.
    '김덕겸': {'role': 'other'},  # 조선 - 조선 중기에, 북청판관, 충청도사동지중추부사 등을 역임한 문신.
    '김덕기': {'role': 'other'},  # 조선 - 조선 후기에, 동래부사, 황해도관찰사, 호조참판 등을 역임한 문신.
    '김덕련': {'role': 'scholar'},  # 조선 - 일제강점기 때, 『고헌집』 등을 저술한 학자.
    '김덕령': {'role': 'other'},  # 조선/조선 후기 - 조선 중기에, 임진왜란이 발발하자 의병으로 활약하여 형조좌랑에 임명된 의병장.
    '김덕룡': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「두석장(豆錫匠) 전승자로 지정된 기능보유자.
    '김덕명': {'role': 'other'},  # 고려/고려 후기 - 고려후기 개경 승도의 난, 최우암살모의 등과 관련된 주모자.
    '김덕목': {'role': 'other'},  # 근대 - 일제강점기 때, 학생항일구국회 간부, 한국광복군 총사령부 참모 등을 역임한 독립운동가.
    '김덕방': {'role': 'other foreigner'},  # 조선/조선 후기 - 조선후기 일본인 나가타에게 침구의 비법을 전해준 의관.
    '김덕보': {'role': 'scholar'},  # 조선/조선 후기 - 조선 후기 임진왜란과 정묘호란 때 의병을 일으킨 의병장이자 학자.
    '김덕부': {'role': 'other'},  # 고려 - 고려 전기에, 상서좌복야, 수사공 상서좌복야 등을 역임한 문신.
    '김덕생': {'role': 'other'},  # 고려/고려 후기 - 고려후기 전옥서영, 낭장, 동지중추원사(추증) 등을 역임한 무신.
    '김덕성': {'role': 'scholar'},  # 조선/조선 후기 - 조선후기 「쌍마도」 · 「선객도」 · 「뇌공도」 등의 작품을 그린 화가.
    '김덕수': {'role': 'scholar'},  # 조선/조선 후기 - 조선 전기에 기묘사화로 화를 입은 김식의 아들로 사면된 이후 후학 양성에 힘쓴 학자.
    '김덕순': {'role': 'other foreigner'},  # 근대 - 대한제국기 때, 항일의병투쟁과 군자금 모금, 일본인 처단 활동 등을 전개한 의병.
    '김덕승': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 사복시정, 목사 등을 역임한 문신.
    '김덕열': {'role': 'other'},  # 현대/대한민국 - 미군정청 관재처 감찰관, 제헌국회의원 등을 역임한 정치인.
    '김덕오': {'role': 'scholar'},  # 조선 - 조선 후기에, 『기연의변』, 『사학의변』, 『치헌집』 등을 저술한 학자.
    '김덕용': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 수원의 독립만세시위를 주도하다가 제암리 학살사건에 의해 사망한 독립운동가.
    '김덕원': {'role': 'other'},  # 조선 - 조선 후기에, 사헌부장령, 형조참판, 예조판서 등을 역임한 문신.
    '김덕제': {'role': 'other'},  # 근대 - 대한제국기 때, 원주진위대 정위 등을 역임하였으며, 항일의병활동을 전개한 의병장.
    '김덕준': {'role': 'other'},  # 현대 - 해방 이후 우리나라 최초의 국제 심판으로 국제심판 공로상을 받은 체육인.
    '김덕지': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 제56대 경순왕의 왕자.
    '김덕진': {'role': 'other'},  # 근대/대한제국기 - 을사조약에 반대하여 일어난 의병운동에 참여한 의병장.
    '김덕하': {'role': 'other'},  # 조선/조선 후기 - 조선후기 「사계산수도권」을 그린 화가.
    '김덕한': {'role': 'other'},  # 근대/개항기 | 근대/일제강점기 - 일제강점기 봉상사 제조, 종묘서 제조, 의효전 제조 등을 역임한 관료. 친일반민족행위자.
    '김덕함': {'role': 'other'},  # 조선 - 조선 중기에, 공조좌랑, 호조정랑 등을 역임한 문신.
    '김덕현': {'role': 'other'},  # 근대 - 일제강점기 때, 학성학교 교장, 북로군정서 군정회의원 등을 역임한 독립운동가.
    '김덕흥': {'role': 'other'},  # 근대 - 대한제국기 때, 강원도 양구 일대에서 항일의병투쟁을 전개한 의병장.
    '김도': {'role': 'other'},  # 고려 - 고려 후기에, 좌부대언, 지신사, 밀직제학 등을 역임한 문신.
    '김도규': {'role': 'other'},  # 근대/대한제국기 - 대한제국기 전라남도 보성일대에서 활약한 의병장.
    '김도나': {'role': 'other foreigner'},  # 고대/남북국 - 남북국시대 통일신라에서 일본에 사신으로 파견된 관리.
    '김도명': {'role': 'scholar'},  # 조선 - 조선 후기에, 『외암문집』 등을 저술한 학자.
    '김도산': {'role': 'scholar'},  # 근대/일제강점기 - 일제강점기 「의리적 구투」, 「시우정」, 「형사고심」 등의 작품에 관여한 영화인. 연극인.
    '김도삼': {'role': 'other'},  # 근대 - 대한제국기 상쇠와 진법놀이에 능해 정읍농악을 널리 알린 음악인. 상쇠.
    '김도성': {'role': 'poet scholar'},  # 현대/대한민국 - 해방 이후 『고란초』, 『갈대』 등을 저술한 시인. 영문학자.
    '김도수': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 예빈시주부, 경양찰방 등을 역임한 서얼 문사.
    '김도숙': {'role': 'other'},  # 근대/대한제국기 - 대한제국기 심남일 의진에서 도통장으로 활약한 의병장.
    '김도언': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 의금부도사, 병조좌랑, 음죽현감 등을 역임한 문신.
    '김도연': {'role': 'other'},  # 현대/대한민국 - 일제강점기 때, 2·8독립선언과 조선어학회 사건으로 옥고를 치렀으며, 해방 이후, 국회의원, 초대 재무부장관 등을...
    '김도원': {'role': 'other'},  # 근대 - 일제강점기 때, 대한독립보합단에서 군자금 모금 활동을 전개한 독립운동가.
    '김도주': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 경상북도 안동군 임하면의 독립만세시위에 참여했다가 순국한 독립운동가.
    '김도태': {'role': 'other'},  # 근대 - 3.1운동 당시 48인의 한 사람으로 활약한 교육자.
    '김도행': {'role': 'scholar'},  # 조선 - 조선 후기에, 『우고문집』 등을 저술한 학자.
    '김도혁': {'role': 'scholar'},  # 조선 - 조선 후기에, 「망해도법」, 「측량법」, 『암당문집』 등을 저술한 학자.
    '김도현': {'role': 'other'},  # 근대/개항기 | 근대/대한제국기 - 을미사변 이후 대한제국 강제 병합 이전까지 의병 활동을 전개한 의병장.
    '김도화': {'role': 'scholar'},  # 근대/개항기 - 개항기 때, 의금부도사 등을 역임하였으며, 안동에서 의병을 일으켜 항쟁한 학자 · 의병장.
    '김도희': {'role': 'other'},  # 조선 - 조선 후기에, 판서, 우의정, 좌의정 등을 역임한 문신.
    '김돈': {'role': 'other'},  # 조선 - 조선 전기에, 인순부윤, 도승지 등을 역임한 문신.
    '김돈시': {'role': 'other'},  # 고려/고려 전기 - 고려 전기 의종의 측근으로, 정중부의 난 당시 살해된 문신.
    '김돈중': {'role': 'other'},  # 고려 - 고려 전기에, 호부원외랑, 시랑, 좌승선 등을 역임한 문신.
    '김돈희': {'role': 'scholar'},  # 근대/일제강점기 - 일제강점기 「출사표」, 「장진주」 등의 작품을 낸 서예가.
    '김동건': {'role': 'other'},  # 조선 - 조선 후기에, 동지 겸 사은부사, 우참찬 등을 역임한 문신.
    '김동권': {'role': 'other'},  # 조선 - 조선후기 효행으로 정려를 하사 받고, 중학교 교관으로 추증된 효자.
    '김동리': {'role': 'novelist'},  # 해방 이후 『무녀도』, 『황토기』, 『등신불』 등을 저술한 문학작가.
    '김동명': {'role': 'other'},  # 근대 - 일제강점기 신흥청년동맹 상무집행위원장, 고려공산청년회 만주총국 책임자 등을 역임한 사회주의운동가.
    '김동삼': {'role': 'other'},  # 근대/일제강점기 - 1910년대에 만주에 망명하여 1920년대까지 서간도 독립운동 단체의 지도자로 활약하였던 독립운동가.
    '김동석': {'role': 'poet critic'},  # 근대 - 해방 이후 『길』, 『해변의 시』 등을 저술한 시인. 비평가.
    '김동성': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 서울대교수, 공보부장관 등을 역임한 학자. 정치인.
    '김동수': {'role': 'other'},  # 근대/개항기 - 대한제국기 전라남도 광주 출신으로, 양진여 의진에 참여하여 활동한 의병장.
    '김동식': {'role': 'other'},  # 근대 - 일제강점기 때, 평안남도 중화군 상원면의 독립만세시위를 주도한 천도교인 · 독립운동가.
    '김동신': {'role': 'other'},  # 근대/대한제국기 - 을사조약 이후 민종식 의진에서 선봉장으로 활약한 의병장.
    '김동엄': {'role': 'other foreigner'},  # 고대/남북국 - 남북국시대 통일신라의 급찬으로서 일본에 사신으로 파견된 관리.
    '김동연': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 장령, 사간, 집의 등을 역임한 문신.
    '김동엽': {'role': 'other'},  # 현대 - 해방 이후 프로야구 해태타이거즈 창단감독, 서울방송 전속야구해설위원 등을 역임한 체육인.
    '김동영': {'role': 'other'},  # 현대/대한민국 - 제9대, 10대, 12대, 13대 국회의원, 정무제1장관 등을 역임한 정치인.
    '김동욱': {'role': 'scholar'},  # 현대/대한민국 - 민속학회 이사, 한국비교문학회 회장, 한국복식학회 부회장 등을 역임하였으며, 『국문학개설』, 『한국가요의 연구』,...
    '김동원': {'role': 'other'},  # 현대 - 해방 이후 「자명고」, 「마의태자」, 「별」 등에 출연한 배우. 영화배우, 연극배우.
    '김동은': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 광주에서 학생항일비밀결사인 독서회를 조직하여 항일투쟁을 전개한 독립운동가.
    '김동익': {'role': 'scholar'},  # 근대/일제강점기 | 현대 - 서울대학교 의과대학 교수, 동국대학교 총장 등을 역임한 의학자.
    '김동인': {'role': 'novelist'},  # 근대/일제강점기 - 일제강점기 「배따라기」 · 「감자」 · 「발가락이 닮았다」 등을 저술한 소설가. 친일반민족행위자.
    '김동일': {'role': 'scholar'},  # 현대/대한민국 - 서울대학교 공과대학 초대 학장, 한국원자력원의 초대 상임위원 등을 역임하였으며, 『한국자기공업론』, 『한국화학공업...
    '김동조': {'role': 'other foreigner'},  # 현대/대한민국 - 주일본 대사, 외무부장관 등을 역임한 외교관 · 정치인.
    '김동준': {'role': 'other'},  # 현대/대한민국 - 해방 이후 판소리 고법의 전승자로 지정된 예능보유자. 고수.
    '김동철': {'role': 'other'},  # 현대/대한민국 - 덕원면속구 소속으로 해방 이후 평양대목구로 파견되어 안주본당, 비현본당에서 사목한 신부.
    '김동필': {'role': 'other'},  # 근대 - 대한제국기 때, 일제의 침략을 규탄하는 상소운동 및 을사조약 반대투쟁 등을 전개한 독립운동가.
    '김동하': {'role': 'other'},  # 현대/대한민국 - 해방 이후 제1상륙 사단장, 해병중장, 국가재건최고회의최고위원 등을 역임한 군인. 체육인.
    '김동한': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 우리나라 최초의 사교무용학원인 조선예술학원을 설립한 무용가.
    '김동화': {'role': 'scholar'},  # 현대/대한민국 - 동국대학교 교수로 재임하여 세계적인 불교학의 연구를 학계에 정착시켰으며, 『불교학개론』, 『삼국시대의 불교사상』,...
    '김동환': {'role': 'poet'},  # 근대/일제강점기 - 일제강점기 『국경의 밤』 · 『해당화』 · 『돌아온 날개』 등을 저술한 시인. 언론인 · 친일반민족행위자.
    '김동훈': {'role': 'other'},  # 현대 - 해방 이후 「아들을 위하여」, 「심판」, 「롤러스케이트를 타는 오뚝이」 등에 출연한 배우.
    '김동휘': {'role': 'other'},  # 현대/대한민국 - 해방 이후 주독대사관 부영사, 외무부 차관, 상공부 장관 등을 역임한 관료. 외교관.
    '김두달': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 호군 등을 역임하였으며, 신돈의 세력으로 활동하다 신돈의 반역모의사건에 가담했다는 죄목으로 죽임을...
    '김두량': {'role': 'scholar'},  # 조선/조선 후기 - 조선후기 「월야산수도」 · 「춘하도리원호흥도권」 · 「흑구도」 등의 작품을 그린 화가.
    '김두룡': {'role': 'scholar'},  # 조선 - 조선 후기에, 『낙선당집』 등을 저술한 학자.
    '김두만': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 대한청년단연합회 교제부장, 광복군참리부 외무사장 등을 역임한 독립운동가.
    '김두명': {'role': 'other'},  # 조선 - 조선 후기에, 사간, 승지, 병조참의 등을 역임한 문신.
    '김두봉': {'role': 'scholar'},  # 일제강점기 때, 임시의정원 의원, 한국민족혁명당 중앙집행위원, 조선독립동맹 주석 등을 역임한 한글학자 · 정치인 · 독립운동가.
    '김두용': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 고려공산청년회 일본부기관지 출판위원, 조선신문사 편집국원 등을 역임한 사회주의운동가.
    '김두종': {'role': 'scholar'},  # 근대/일제강점기 | 현대 - 서울대학교 의과대학 교수, 숙명여자대학교 총장 등을 역임하였으며, 『한국의학사』, 『한국고인쇄기술사』 ...
    '김두징': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 갑인예송으로 곤경에 처한 송시열을 변호하는 상소를 올리는 데 참여한 유생.
    '김두한': {'role': 'other'},  # 현대/대한민국 - 대한청년당의 감찰부장, 제3대, 6대 국회의원 등을 역임하였으며, 국회오물투척사건을 일으킨 정치인.
    '김두헌': {'role': 'scholar'},  # 현대 - 해방 이후 『조선가족제도연구』 · 『현대의 가족』 등을 저술한 학자. 교육자.
    '김두환': {'role': 'other'},  # 근대/일제강점기|현대 - 해방 이후 제1회 국전에서 「향원정」 으로 입선한 화가. 유화가.
    '김둔산': {'role': 'other'},  # 고대/남북국 - 남북국시대 평양성전투에서 큰공을 세워 사찬을 제수받은 관리.
    '김득경': {'role': 'other'},  # 고려 - 고려후기 북청주만호를 역임한 무신.
    '김득배': {'role': 'scholar'},  # 고려 - 고려 후기에, 서북면도병마사, 수충보절정원공신, 정당문학 등을 역임한 문신 · 공신.
    '김득복': {'role': 'other'},  # 조선 - 조선 중기에, 임진왜란이 발발하자 불국산에서 의병을 일으켜 항쟁하였고, 이순신의 휘하에서 활약하며 절충장군에 임명된 의병장.
    '김득상': {'role': 'other'},  # 조선 - 조선 중기에, 임진왜란이 발발하자 형 김득복을 따라 의병활동을 전개하다가 전사한 의병.
    '김득수': {'role': 'other'},  # 현대/대한민국 - 해방 이후 판소리 고법의 전승자로 지정된 예능보유자. 고수.
    '김득신': {'role': 'scholar'},  # 조선/조선 후기 - 조선후기 「파적도」, 「긍재풍속화첩」, 「풍속팔곡병」 등의 작품을 그린 화가.
    '김득연': {'role': 'scholar'},  # 조선 - 조선 후기에, 「청량산유록」, 『지수정가』, 『갈봉유고』 등을 저술한 학자.
    '김득인': {'role': 'other'},  # 조선 - 조선후기 장례원사의를 역임한 무신.
    '김득제': {'role': 'other'},  # 고려 - 고려후기 대장군, 의주원수, 삼사우사 등을 역임한 무신.
    '김득진': {'role': 'other'},  # 조선 - 조선 후기에, 용강부사, 자산군수 등을 역임한 무신 · 공신.
    '김득추': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 용양위부사직, 가선대부 등을 역임한 무신 · 공신.
    '김락': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 예안군에서 전개된 독립만세운동에 참여한 독립운동가.
    '김란': {'role': 'other'},  # 고려 - 고려 후기에, 밀직부사, 서북면도체찰사, 참지문하부사 등을 역임한 문신.
    '김려': {'role': 'other'},  # 조선 - 조선 후기에, 연산현감, 함양군수 등을 역임한 문신.
    '김련': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 추밀원사, 지문하성사, 참지정사 등을 역임한 문신.
    '김령': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 승문원관원, 주서 등을 역임한 문신.
    '김례': {'role': 'other'},  # 고려 - 고려후기 이장대의 난과 관련된 무신. 반란자.
    '김례삼': {'role': 'novelist'},  # 근대 | 현대 - 해방 이후 연변문학연합회 주비위원회 비서장, 조선족민속학회 이사 등을 역임한 작가.
    '김로': {'role': 'other'},  # 조선 - 조선 후기에, 판의금부사, 호조판서, 대사헌 등을 역임한 문신.
    '김룡': {'role': 'other'},  # 고려 - 고려후기 만호, 판사 등을 역임한 무신.
    '김류': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 형조좌랑, 전주판관, 병조판서 등을 역임한 문신.
    '김륜': {'role': 'other'},  # 고려 - 고려 후기에, 경상 · 전라도도순문사, 벽상공신, 좌정승 등을 역임한 문신 · 공신.
    '김률': {'role': 'other'},  # 고대/남북국 - 남북국시대 통일신라의 아찬 관등을 역임한 관리.
    '김륭': {'role': 'scholar'},  # 조선 - 조선 전기에, 『물암집』, 『삼서강록』 등을 저술한 학자.
    '김륵': {'role': 'other'},  # 조선 - 조선 중기에, 경상우도관찰사, 충청도관찰사, 안동부사 등을 역임한 문신.
    '김림': {'role': 'other'},  # 고려 - 고려 후기에, 권신인 정세운과 함께 홍건적의 난을 평정함으로써 왕의 신임을 얻었으나, 정세운과 권력을 다투던 김용의 간계에...
    '김립': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 만주에서 활약한 사회주의운동가.
    '김마리아': {'role': 'other foreigner'},  # 근대/일제강점기 - 고려혁명군으로 활동하고 중국 중앙군관학교 서북북교의 러시아어 교관을 역임한 독립운동가.
    '김막인': {'role': 'other'},  # 현대 - 해방 이후 조선무용예술협회 현대무용부의 임원을 역임한 무용가.
    '김만': {'role': 'scholar'},  # 조선/조선 후기 - 조선 후기에, 농정개혁과 환곡의 폐단을 상소한 학자.
    '김만겸': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 대한국민의회 간부를 지내며 독립운동을 한 사회주의운동가.
    '김만균': {'role': 'other'},  # 조선 - 조선 후기에, 사인, 보덕, 승지 등을 역임한 문신.
    '김만기': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에 영돈녕부사 · 총융사 등을 역임한 문신.
    '김만길': {'role': 'other'},  # 조선 - 조선 후기에, 부제학, 전라도관찰사, 이조참의 등을 역임한 문신.
    '김만덕': {'role': 'other'},  # 조선후기 1795년 흉년과 관련된 상인.
    '김만물': {'role': 'other foreigner'},  # 고대/삼국/신라 - 남북국시대 통일신라의 사찬으로 일본에 파견된 관리.
    '김만삼': {'role': 'other'},  # 현대/대한민국 - 소련에서 카자흐공화국으로 강제이주를 당하여 아들 김홍빈과 함께 선봉 콜호즈를 세웠으며, 벼농사 확산 및 품종 개발...
    '김만선': {'role': 'novelist'},  # 근대 - 해방 이후 「절룸바리 돌쇠」, 「압록강」, 「해방의 노래」 등을 저술한 작가. 소설가.
    '김만수': {'role': 'other foreigner'},  # 근대 - 일제강점기 때, 서로군정서에서 일본 총영사 및 일본경찰 처단 활동을 전개한 독립운동가.
    '김만술': {'role': 'scholar'},  # 근대/일제강점기 | 현대 - 해방 이후 「해방」, 「역사(力士) I」, 「역사(力士) II」 등의 작품을 낸 조각가.
    '김만식': {'role': 'other'},  # 근대 - 조선 후기에, 동부승지, 공조참의, 예조판서, 평안도관찰사 등을 역임한 문신.
    '김만옥': {'role': 'poet'},  # 현대/대한민국 - 해방 이후 『슬픈 계절의』, 『오늘 죽지 않고 오늘 살아 있다』 등을 저술한 시인.
    '김만와': {'role': 'other'},  # 근대 - 일제강점기 때, 철혈광복단, 대한독립단, 고려혁명당, 정의부 등에서 항일투쟁을 전개한 독립운동가.
    '김만중': {'role': 'scholar'},  # 조선 후기에, 『사씨남정기』, 『구운몽』 등을 저술한 문신.
    '김만증': {'role': 'scholar'},  # 조선 - 조선 후기에, 지중추부사, 임피현령 등을 역임하였으며, 『돈촌집』을 저술한 학자.
    '김만채': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 강원도관찰사, 개성부유수, 경기도관찰사 등을 역임한 문신.
    '김만형': {'role': 'scholar'},  # 근대/일제강점기 | 현대 - 해방 이후 「연봉」, 「쇳물을 붓는 사람들」 등의 작품을 그린 화가.
    '김만흥': {'role': 'other'},  # 현대 - 해방 이후 종묘제례악 해금의 전승자로 지정된 예능보유자.
    '김말': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 예문제학, 중추원부사, 판중추원사 등을 역임한 문신.
    '김말봉': {'role': 'novelist'},  # 근대 - 일제강점기 「찔레꽃」, 「망명녀」, 「밀림」 등을 저술한 소설가.
    '김매순': {'role': 'other'},  # 조선 - 조선 후기에, 예조참판, 강화부유수 등을 역임한 문신.
    '김맹': {'role': 'other'},  # 조선 - 조선 전기에, 오위도총부경력 등을 역임한 문신 · 공신.
    '김맹경': {'role': 'other'},  # 조선 - 조선전기 하정사 유자광을 수행하여 연경에 다녀온 역관.
    '김맹권': {'role': 'scholar'},  # 조선 - 조선 전기에, 집현전학사 등을 역임한 학자.
    '김맹도리': {'role': 'other'},  # 근대/대한제국기 - 대한제국기 때, 양한규 의진에서 항일의병투쟁을 전개한 의병.
    '김맹성': {'role': 'other'},  # 조선 - 조선 전기에, 이조정랑, 수찬 등을 역임한 문신.
    '김면': {'role': 'scholar'},  # 조선 - 조선 중기에, 임진왜란이 발발하자 의병을 일으켜 활약한 공으로 합천군수, 첨지사, 경상우도병마절도사 등을 역임한 학자 · ...
    '김면호': {'role': 'other'},  # 조선 - 조선후기 병인박해 당시의 순교자.
    '김명국': {'role': 'scholar'},  # 조선 - 조선후기 「설중귀려도」, 「달마도」, 「은사도」 등의 작품을 그린 화가.
    '김명권': {'role': 'other'},  # 근대 - 일제강점기 때, 대한청년단에서 군자금 모금 활동을 전개한 독립운동가.
    '김명규': {'role': 'other'},  # 근대 - 일제강점기 때, 동래고등보통학교의 독립만세시위를 주도하였으며, 군자금 모금 활동을 전개한 독립운동가.
    '김명균': {'role': 'other'},  # 근대 - 개항기 통리군국사무아문 감공사주사, 기기국방판 등을 역임한 관료.
    '김명동': {'role': 'other'},  # 근대 - 일제강점기 때, 신간회 중앙집행위원 등으로 활동하였고, 해방 이후, 국회의원을 역임한 정치인 · 독립운동가.
    '김명립': {'role': 'other'},  # 근대/대한제국기 - 대한제국기 때, 이강년 의진에서 활약하였고, 군자금 모금 활동을 전개한 의병 · 독립운동가.
    '김명복': {'role': 'scholar'},  # 근대 - 경희대학교 체육대학장, 교육대학원장, 부총장 등을 역임하였으며, 『체육지도서』, 『체육개론』 등을 저술하여 우리나라의 체육...
    '김명선': {'role': 'other'},  # 근대/일제강점기 | 현대 - 해방 이후 대한의학협회 부회회장, 대한가족계획협회 회장 등을 역임한 의사.
    '김명수': {'role': 'other foreigner'},  # 현대/대한민국 - 일제강점기 때, 일본 우베일일신문사 기자, 편집국장을 역임하였으며, 해방 이후 국회의원을 역임한 언론인 · 정치인.
    '김명순': {'role': 'poet novelist'},  # 근대 - 일제강점기 「동경」, 「옛날의 노래여」, 「언니 오시는 길에」 등을 저술한 시인. 소설가.
    '김명시': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 때, 상해한인청년동맹 부인부 책임, 중국공산당 한인지부 선전부 책임, 조선의용대 부녀복무대 지휘관 등...
    '김명식': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 활동한 사회주의 운동가, 민족운동가.
    '김명언': {'role': 'other'},  # 조선 - 조선 전기에, 호조정랑, 김제군수, 상주목사 등을 역임한 문신.
    '김명원': {'role': 'other'},  # 조선 - 조선 중기에, 이조판서, 우의정, 좌의정 등을 역임한 문신.
    '김명윤': {'role': 'other'},  # 조선 - 조선 전기에, 의정부좌찬성, 지경연사, 판돈녕부사 등을 역임한 문신.
    '김명제': {'role': 'other'},  # 근대 - 일제강점기 때, 수원군 송산면 사강리의 독립만세시위에 참여한 독립운동가.
    '김명진': {'role': 'other'},  # 근대 - 조선 후기에, 경기관찰사, 경상도관찰사, 이조참판 등을 역임한 문신.
    '김명하': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 평안북도 강계군 강계면의 독립만세시위를 주도한 혐의로 체포된 독립운동가.
    '김명환': {'role': 'other'},  # 현대/대한민국 - 해방 이후 판소리 고법의 전승자로 지정된 예능보유자. 고수.
    '김명희': {'role': 'other'},  # 조선/조선 후기 - 조선후기 홍문관직제학, 강동현령을 역임한 서예가.
    '김몽호': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 사헌부장령, 공조참의 등을 역임한 문신.
    '김무': {'role': 'other'},  # 고대/삼국 - 삼국시대 신라의 파진찬을 역임한 의관.
    '김무규': {'role': 'other'},  # 현대/대한민국 - 해방 이후 구례향제줄풍류에서 단소의 전승자로 지정된 예능보유자. 단소, 거문고명인.
    '김무력': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 관산성전투에 참전한 장수.
    '김무림': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 소판 관등의 귀족.
    '김무석': {'role': 'other'},  # 현대/대한민국 - 해방 이후 맹호5호작전 당시의 군인.
    '김무선': {'role': 'scholar'},  # 고대/남북국/통일신라 - 남북국시대 때, 숙위학생으로 당나라에서 유학하여 빈공과에 급제한 통일신라의 학자.
    '김무알': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 제19대 눌지마립간 때 고구려에 질자로 간 복호(卜好)를 보좌한 관리.
    '김무정': {'role': 'other'},  # 근대 - 일제강점기 팔로군 포병단 단장, 조선의용군 총사령 등을 역임한 사회주의운동가.
    '김무체': {'role': 'scholar'},  # 고려 - 고려 전기에, 복야 등을 역임하였으며, 고려시대 사학(私學) 12도 중 하나인 서원도를 열어 후진 양성에 힘쓴 학자.
    '김무훈': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라에서 당나라에 파견된 사신.
    '김문': {'role': 'other'},  # 조선 - 조선 전기에, 집현전수찬, 집현전부교리, 집현전직제학 등을 역임한 문신 · 공신.
    '김문귀': {'role': 'other'},  # 고려 - 고려 후기에, 호군, 밀직부사 등을 역임한 문신.
    '김문근': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 영돈녕부사, 총융사, 훈련대장 등을 역임한 문신.
    '김문기': {'role': 'other'},  # 조선 전기에, 예문관검열, 병조참의, 형조참판 등을 역임한 문신.
    '김문길': {'role': 'other'},  # 현대/대한민국 - 해방 이후 제25사단 항공대 조종사 중위를 역임한 군인.
    '김문달': {'role': 'other'},  # 현대/대한민국 - 해방 이후 이리농악 전승자로 지정된 기예능보유자.
    '김문량': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 아찬으로 중시를 역임한 관리.
    '김문발': {'role': 'other'},  # 조선/조선 전기 - 조선전기 충청전라도수군도체찰추포사, 전라도수군절제사 등을 역임한 무신.
    '김문보': {'role': 'other foreigner'},  # 현대 - 중국공산당 연변지방위원회 위원 , 연변조선족자치주위원회 서기처 서기 등을 역임한 조선족 출신의 정치인 · 교육가.
    '김문비': {'role': 'other'},  # 고려 - 고려후기 상장군, 삼익군 우군사, 군부판사 등을 역임한 무신.
    '김문빈': {'role': 'other'},  # 근대/대한제국기 - 대한제국기 때, 신경칠 의진의 참모장 및 중군장으로 활약한 의병.
    '김문상': {'role': 'scholar'},  # 현대/대한민국 - 서울대학교 섬유공학과 교수, 한국섬유공학회 회장, 한국표준심의위원회 위원장 등을 역임한 공학자.
    '김문세': {'role': 'other'},  # 근대/일제강점기 - 대한민국임시정부 기관지인 독립신문의 기자로 활동한 독립운동가.
    '김문순': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 이조판서, 선혜청당상, 우참찬 등을 역임한 문신.
    '김문연': {'role': 'other'},  # 고려 - 고려 후기에, 좌우위산원, 첨의시랑찬성사, 첨의중호 등을 역임한 문신.
    '김문영': {'role': 'other'},  # 고대/남북국 - 삼국시대 나당연합군의 백제 정벌 당시의 장수.
    '김문왕': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라 제29대 태종무열왕의 셋째 아들인 왕자.
    '김문울': {'role': 'scholar'},  # 고대/남북국/통일신라 - 남북국시대 때, 당나라 빈공과에 급제하여 공부원외랑, 기왕부자의참군 등을 역임한 통일신라의 학자.
    '김문정': {'role': 'other'},  # 고려 - 고려 후기에, 국학학정, 사헌규정 등을 역임한 문신.
    '김문제': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 이조참의, 좌참찬, 경연관 등을 역임한 문신.
    '김문집': {'role': 'critic'},  # 근대/일제강점기 - 일제강점기 『비평문학』 · 『아리랑고개』 등을 저술한 평론가. 친일반민족행위자.
    '김문평': {'role': 'other'},  # 현대/대한민국 - 일제강점기 때, 한성은행 본정지점 지배인 대리, 동아일보 여수지국장 등을 역임하였으며, 해방 이후 조선건국준비위원...
    '김문현': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 형조판서, 예조판서, 전라도관찰사 등을 역임한 문신.
    '김문호': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 한국광복군으로 활동한 독립운동가.
    '김문희': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 임시정부 연통제 장서, 임시의정원 의원 등을 역임한 독립운동가.
    '김물유': {'role': 'other foreigner'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 대나마로 일본에 파견된 관리.
    '김미': {'role': 'other'},  # 조선 - 조선 전기에, 정주별선위사, 우승지, 첨지중추부사 등을 역임한 문신.
    '김미하일': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 한인사회당 부회장, 노보에쿠스코예의 구역당서기 등을 역임한 사회주의운동가.
    '김미향': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「영해별신굿놀이」 전승자로 지정된 예능보유자. 무속인.
    '김민선': {'role': 'other'},  # 조선 - 조선 전기에, 집의, 헌남, 인천부사 등을 역임한 문신.
    '김민순': {'role': 'poet'},  # 조선/조선 후기 - 조선후기 지평현감을 역임한 시인.
    '김민자': {'role': 'other'},  # 현대 - 해방 이후 최승희의 제자이며, 예그린악단의 안무가로 활동한 무용가.
    '김민재': {'role': 'scholar'},  # 조선 - 조선후기 담양군수, 제천군수 등을 역임한 문신. 학자.
    '김민주': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 대감을 역임한 장수.
    '김민택': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 남학교수, 실록청낭관, 지제교 등을 역임한 문신.
    '김민환': {'role': 'scholar foreigner'},  # 조선 - 조선 후기에, 「통사문답」, 「중국학통」, 『용암집』 등을 저술한 학자.
    '김반': {'role': 'other'},  # 조선 - 조선 후기에, 대사성, 대사간, 대사헌 등을 역임한 문신.
    '김반굴': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 황산벌전투에 참전한 장수.
    '김방걸': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 승지, 대사간, 대사성 등을 역임한 문신.
    '김방경': {'role': 'other foreigner'},  # 고려/고려 후기 - 고려 후기 삼별초의 난을 진압하고 몽골군과 함께 일본 정벌을 지휘했던 무신.
    '김방두': {'role': 'other'},  # 조선 - 조선시대 「죽지쌍금도」를 그린 화가.
    '김방서': {'role': 'other'},  # 근대 - 개항기 봉성 대접주, 금구의 접주 등을 역임한 천도교인.
    '김방행': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 평안도사, 대사성 등을 역임한 문신.
    '김백겸': {'role': 'other'},  # 조선/조선 전기 - 조선전기 겸사복장, 첨지중추부사, 평안도절도사 등을 역임한 무신.
    '김백균': {'role': 'other'},  # 고려 - 고려후기 삼사사, 밀직부사, 동지밀직사사 등을 역임한 무신.
    '김백만': {'role': 'other'},  # 근대 - 일제강점기 밀산반일유격대 대장을 역임한 사회주의운동가.
    '김백선': {'role': 'other'},  # 근대 - 개항기 때, 유인석 의진에서 선봉장으로 활약하였으나, 군기문란죄로 처형된 의병.
    '김백순': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 인산진첨사, 의주목사, 승지 등을 역임한 문신.
    '김백안': {'role': 'other'},  # 고려 - 고려후기 낭장, 대성, 평장사 등을 역임한 문신. 반란자.
    '김백일': {'role': 'other'},  # 근대/일제강점기 - 해방 이후 여순항쟁, 옹진반도전투에 참전한 군인. 친일반민족행위자.
    '김백흥': {'role': 'other'},  # 고려 - 고려후기 조전원수, 한양윤 등을 역임한 무신.
    '김번': {'role': 'scholar'},  # 조선 - 조선 전기에, 제용감첨정, 평양서윤, 시강원문학 등을 역임한 문신.
    '김범문': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 고달산에서 반란을 일으킨 주모자.
    '김범부': {'role': 'scholar'},  # 현대/대한민국 - 『화랑외사』, 『풍류정신』 등을 저술하며 불교철학, 동양철학 연구에 전념한 철학자.
    '김범우': {'role': 'other'},  # 조선 - 조선 후기, 을사추조적발사건과 관련된 천주교인.
    '김범이': {'role': 'other'},  # 근대/대한제국기 - 대한제국기 때, 어윤성 의진에 가담하여 군자금 모금 활동을 전개한 의병.
    '김범주': {'role': 'scholar'},  # 조선 - 조선 후기에, 『익와집』 등을 저술한 학자.
    '김범청': {'role': 'other'},  # 고대/남북국 - 남북국시대 통일신라의 김헌창의 난 당시의 귀족.
    '김법린': {'role': 'scholar'},  # 현대/대한민국 - 일제강점기 때, 만당, 조선청년동맹 등을 조직하여 항일투쟁을 전개하였으며, 해방 이후, 문교부장관, 민의원, 동국...
    '김법선': {'role': 'other'},  # 고대/삼국/신라 - 남북국시대 통일신라의 현성대왕으로 추봉된 신라의 귀족.
    '김변': {'role': 'other'},  # 고려 - 고려 후기에, 첨의참리, 집현전대학사, 동수국사 등을 역임한 문신.
    '김변광': {'role': 'other'},  # 조선 - 조선 후기에, 병조정랑, 용강현령, 공조참의 등을 역임한 문신.
    '김병걸': {'role': 'critic'},  # 현대/대한민국 - 해방 이후 『리얼리즘문학론』, 『민중문학과 민족현실』, 『실패한 인생 실패한 문학』 등을 저술한 평론가. 문학평론가.
    '김병관': {'role': 'scholar'},  # 조선 - 조선 후기에, 『정산유고』 등을 저술한 학자.
    '김병교': {'role': 'other'},  # 조선 - 조선 후기에, 형조판서, 판의금부사, 상호군 등을 역임한 문신.
    '김병국': {'role': 'other'},  # 근대 - 개항기 때, 총리군국사무, 영돈녕부사 등을 역임한 문신.
    '김병기': {'role': 'other'},  # 조선 - 조선 후기에, 삼정이정청의 구관당상, 이조판서 등을 역임한 문신.
    '김병덕': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 우의정, 좌의정, 총리군국사무 등을 역임한 문신.
    '김병로': {'role': 'other'},  # 해방 이후 남조선과도정부 사법부 부장, 대법원장 등을 역임한 법조인. 정치인.
    '김병록': {'role': 'other'},  # 근대 - 일제강점기 때, 친일파 이완용 암살을 계획한 혐의로 체포된 독립운동가.
    '김병삼': {'role': 'other'},  # 현대/대한민국 - 해방 이후 육군헌병사령관, 육군본부 일반참모부 비서실장, 육군소장 등을 역임한 군인. 공무원.
    '김병서': {'role': 'other'},  # 현대/대한민국 - 일제강점기 농민복음학교 교장, 해주 구세요양원 부원장 등을 역임한 사회운동가. 의료인.
    '김병수': {'role': 'scholar'},  # 조선 - 조선 후기에, 『계미유고』 등을 저술한 학자.
    '김병시': {'role': 'other'},  # 근대/개항기 - 개항기 때, 예문관제학, 독판군국사무, 의정부의정 등을 역임한 문신.
    '김병연': {'role': 'poet'},  # 조선/조선 후기 - 조선 후기, ‘김삿갓’ 혹은 ‘김립(金笠)으로 널리 알려진 시인.
    '김병영': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 간도 용정촌에서 전개된 독립만세시위를 주도하다가 순국한 독립운동가.
    '김병욱': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 장악원주부, 연풍현감, 돈녕부정 등을 역임한 문신.
    '김병운': {'role': 'other'},  # 근대/일제강점기|현대 - 일제강점기 경성방직 기술책임자를 역임한 기술자.
    '김병익': {'role': 'other'},  # 근대 - 일제강점기 대사성, 궁내부 특진관, 조선귀족(남작) 등을 역임한 관료. 친일반민족행위자.
    '김병제': {'role': 'scholar'},  # 해방 이후 『조선어문법: 어음론 · 형태론』, 『조선어학사』 등을 저술한 학자. 국어학자.
    '김병조': {'role': 'other'},  # 근대 - 일제강점기 때, 한국독립당 동북의용군 사령, 중한연합군 부사령 등을 역임한 독립운동가.
    '김병종': {'role': 'scholar'},  # 조선 - 조선 후기에, 『성학속도』, 『학림통록』, 『문소가례』 등을 저술한 학자.
    '김병주': {'role': 'other'},  # 근대 - 조선 후기에, 한성부판윤, 경상도관찰사, 의정부좌참 등을 역임한 문신.
    '김병준': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 함경남도 이원의 천도교구장으로서 독립만세시위를 주도하였고, 대한민국임시정부의 이원 참사 등으로 ...
    '김병지': {'role': 'other'},  # 근대 - 조선 후기에, 공조판서, 형조판서, 함경도감사 등을 역임한 문신.
    '김병찬': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 평안북도 강계군 강계면의 독립만세시위에 참여했다가 순국한 독립운동가.
    '김병태': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 의열단에서 활동하며 조선혁명간부학교 군사교관, 김원봉 비서 등을 역임한 독립운동가.
    '김병필': {'role': 'other'},  # 조선 - 조선 후기에, 좌의정, 홍문관부제학, 예조판서 등을 역임한 문신.
    '김병학': {'role': 'other'},  # 근대 - 일제강점기 때, 광복군에 입대하여 학병탈출공작과 정보 수집 활동을 전개한 독립운동가.
    '김병호': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 김창조의 제자로 조선창극단, 임방울창극단에서 활동한 가야금산조의 명창.
    '김병화': {'role': 'other'},  # 현대/대한민국 - 소련에서 소련군 장교, 공산당 당원으로 지내다가 우즈베키스탄으로 강제이주를 당하여 북극성 집단농장 지도자로 활동한...
    '김병환': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 의열단에서 무장투쟁을 전개하였으며, 밀양청년회 문화부장, 신간회 밀양지회 부회장 등을 역임한 독...
    '김병회': {'role': 'other'},  # 현대/대한민국 - 조선일보사 목포지국장, 제헌국회의원 등을 역임하였으며, 국회프락치사건으로 복역하다가 한국전쟁 때 월북하여 북한에서...
    '김보': {'role': 'other'},  # 고려 - 고려 후기에, 중서문하시랑평장사판밀직, 도첨의찬성사, 수시중 등을 역임한 문신.
    '김보가': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 대감으로 나당연합군의 고구려 원정 시 당나라에 파견된 관리.
    '김보근': {'role': 'other'},  # 조선 - 조선 후기에, 좌참찬, 예문관제학, 광주유수 등을 역임한 문신.
    '김보남': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 아악수, 아악수장, 아악사 등을 역임한 음악인. 무용가.
    '김보당': {'role': 'other'},  # 고려 - 고려 후기에, 우간의, 공부시랑, 간의대부 겸 동북면병마사 등을 역임한 문신.
    '김보생': {'role': 'other'},  # 고려 - 고려 후기에, 정조사, 판도판서, 지밀직 등을 역임한 문신.
    '김보연': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 대한민국임시정부 임시의정원 황해도 의원이자 임시정부 경제후원회의 준비위원으로 임시정부 활동 자금 조달...
    '김보정': {'role': 'other'},  # 고려 - 고려 후기에, 추밀원사, 지문하성사, 이부상서 등을 역임한 무신.
    '김보택': {'role': 'scholar'},  # 조선/조선 후기 - 조선 후기에, 문학, 보덕, 전라도관찰사 등을 역임한 문신.
    '김보현': {'role': 'other'},  # 현대/대한민국 - 해방 이후 농림부장관, 체신부장관, 전라남도지사 등을 역임한 관료.
    '김보형': {'role': 'other'},  # 근대 - 일제강점기 때, 만주에서 군자금 모금 및 의용군 조직책으로 활동하였으며, 정의부, 고려혁명군 등에서 항일투쟁을 전개한 독립...
    '김복근': {'role': 'other'},  # 조선/조선 전기 - 조선전기 예조판서 성현 등과 『악학궤범』 편찬에 참여한 음악인.
    '김복대': {'role': 'other foreigner'},  # 고려/고려 후기 - 고려후기 삼별초 토벌, 여몽연합군 일본 정벌 등과 관련된 무신.
    '김복윤': {'role': 'other'},  # 고려/고려 전기 - 고려 전기에, 황주목서기, 동경유수판관, 행대영령 등을 역임한 문신.
    '김복일': {'role': 'other'},  # 조선 - 조선 전기에, 사예, 사성, 풍기군수 등을 역임한 문신.
    '김복진': {'role': 'scholar'},  # 근대/일제강점기 - 일제강점기 「백화」, 「소년」, 「다산선생상」 등의 작품을 낸 조각가. 독립운동가.
    '김복택': {'role': 'other'},  # 조선 - 조선 후기에, 영휘전참봉 등을 역임한 문신.
    '김복한': {'role': 'other'},  # 근대 - 개항기 때, 승정원승지, 형조참의 등을 역임하다가 을미사변 이후 의병활동을 전개하였으며, 국권 피탈 이후 파리장서 서명운동...
    '김복호': {'role': 'other foreigner'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 사찬으로 일본에 사신으로 간 관리.
    '김복흥': {'role': 'scholar'},  # 조선 - 조선시대 별제, 직장, 의금부도사 등을 역임한 문신. 학자.
    '김봉': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 평안도관찰사, 대사헌, 예조참판 등을 역임한 문신.
    '김봉관': {'role': 'other'},  # 근대/일제강점기 - 함경남도 갑산군 동인면 일대의 주재소, 면사무소 등을 습격한 독립운동가.
    '김봉국': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 고려혁명위원회를 조직하였고, 고려혁명당 간부 등을 역임한 독립운동가.
    '김봉규': {'role': 'other'},  # 근대 - 대한제국기 때, 기삼연 중심의 호남창의맹소에서 중군장으로 활약하였고, 기삼연 사후에 잔병을 수습하여 항일의병투쟁을 전개한 ...
    '김봉균': {'role': 'other'},  # 근대/개항기 - 개항기 갑신정변과 관련된 정객.
    '김봉남': {'role': 'other'},  # 근대 - 일제강점기 물법계 종교단체를 설립한 종교창시자.
    '김봉득': {'role': 'other'},  # 근대/개항기 - 개항기 동학운동에 참여한 천도교인.
    '김봉룡': {'role': 'other'},  # 현대 - 해방 이후 「나전장」 전승자로 지정된 기능보유자.
    '김봉모': {'role': 'other'},  # 고려 - 고려 후기에, 판합문사, 추밀원부사, 중서문하평장사 태자태부 등을 역임한 문신.
    '김봉문': {'role': 'other'},  # 근대 - 일제강점기 박기홍의 제자로 동편제 소리의 진수를 발휘한 판소리의 명창.
    '김봉수': {'role': 'other'},  # 근대 - 일제강점기 때, 정의부에서 군자금 모금 및 밀정 처단 활동을 전개한 독립운동가.
    '김봉식': {'role': 'other'},  # 근대 - 일제강점기 때, 만주에서 대한통의부 독립결사대에 가입하여 군자금 모금 활동을 전개한 독립운동가.
    '김봉원': {'role': 'other'},  # 근대 - 일제강점기 때, 국내에서 군자금 모금 활동을 전개해 임시정부를 지원하였으며, 강동경찰서에 폭탄을 던진 독립운동가.
    '김봉재': {'role': 'other'},  # 현대 - 해방 이후 대한유리공업주식회사 대표이사, 중소기업진흥재단 이사장 등을 역임한 실업가. 정치인.
    '김봉조': {'role': 'other'},  # 현대/대한민국 - 일제강점기 때, 영남상업고등학교 교장 등을 역임하였으며 해방 이후, 제헌국회의원, 제2대 국회의원 등을 역임한 교...
    '김봉학': {'role': 'other'},  # 근대 - 일제강점기 명창 김창환의 아들로 김창환협률사에 참가한 판소리의 명창.
    '김봉현': {'role': 'other'},  # 근대 - 일제강점기 때, 경기도 안성군 원곡면과 양성면 일대의 독립만세시위에 참여한 독립운동가.
    '김봉휴': {'role': 'other'},  # 고대/남북국/통일신라 - 후삼국시대 신라의 시랑으로 국서를 가지고 고려 태조에게 항복을 청하러 파견된 문신.
    '김부': {'role': 'other'},  # 고려 - 고려후기 낭장, 장군 겸 예부시랑 등을 역임한 무신.
    '김부륜': {'role': 'scholar'},  # 조선 - 조선 중기에, 동복현감 등을 역임하였으며, 『설월당집』 등을 저술한 학자.
    '김부식': {'role': 'scholar novelist'},  # 고려전기 직한림, 추밀원부사, 중서시랑평장사 등을 역임한 문신. 학자, 문인.
    '김부윤': {'role': 'other'},  # 고려 - 고려 후기에, 밀직부사, 서북면도지휘사, 도첨의찬성사 등을 역임한 무신.
    '김부의': {'role': 'other'},  # 고려 - 고려 전기에, 한림학사승지, 좌군수, 지추밀원사 등을 역임한 문신.
    '김부인': {'role': 'scholar'},  # 조선 - 조선전기 첨지중추부사, 창성부사 등을 역임한 무신. 학자.
    '김부일': {'role': 'other'},  # 고려 - 고려 전기에, 직한림원, 예부낭중, 보문각대제, 중서시랑 동중서문하평장사 등을 역임한 문신.
    '김부필': {'role': 'other'},  # 고려 - 고려 전기에, 병마판관 등을 역임한 문신.
    '김북원': {'role': 'poet critic'},  # 근대 - 해방 이후 『조국』, 『운로봉』, 『대지의 아침』 등을 저술한 시인. 평론가.
    '김북향': {'role': 'novelist'},  # 현대/대한민국 - 해방 이후 북한에서 『로동의 나날』 · 『횃불을 찾아서』 · 『실바킹』 등을 저술한 작가.
    '김불': {'role': 'other'},  # 후삼국시대 신라의 집사시랑으로 후당에 파견된 관리.
    '김붕구': {'role': 'scholar novelist'},  # 현대 - 한국불어불문학회 회장을 역임하였으며, 『불문학 산고』, 『현실과 문학의 비원』, 『작가와 사회』 등을 저술한 불문학자.
    '김붕준': {'role': 'other'},  # 현대/대한민국 - 일제강점기 때, 임시정부의 수립과 운영에 참여하며 국무위원, 제15대 임시의정원 의장 등을 역임하였고, 해방 이후...
    '김붕해': {'role': 'scholar'},  # 조선 - 조선 후기에, 『운당집』 등을 저술한 학자.
    '김빙': {'role': 'other'},  # 조선 - 조선 중기에, 형조좌랑 등을 역임하였으며, 정여립의 모반사건에 대한 추국을 맡았으나 역적을 동정한다는 누명을 쓰고 처형된 문신.
    '김사걸': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 평안북도 정주군의 독립만세시위에 참여했다가 순국한 독립운동가.
    '김사공': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 중시, 상대등, 장군 등을 역임한 관리. 장수.
    '김사국': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 3·1운동에 참가하고 고려공산동맹을 이끈 사회주의운동가, 독립운동가.
    '김사란': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 때, 당나라에 건너가 태복원외경을 역임하였으며, 당 현종의 명으로 귀국하여 성덕왕에게 원군을 요...
    '김사량': {'role': 'novelist'},  # 근대/일제강점기 - 일제강점기 「물오리섬」, 「빛속에서」, 「태백산맥」 등을 저술한 소설가.
    '김사렴': {'role': 'other'},  # 고려 - 고려 후기에, 안렴사 등을 역임한 문신.
    '김사림': {'role': 'poet'},  # 현대/대한민국 - 해방 이후 『바람의 비밀』, 『송짓골 우화』, 『수몰지구』 등을 저술한 시인.
    '김사목': {'role': 'other'},  # 조선 - 조선 후기에, 황해도관찰사, 예조판서, 우의정 등을 역임한 문신.
    '김사묵': {'role': 'other'},  # 조선/조선 후기 - 조선후기 중추원찬의, 경상남도관찰사, 경기도관찰사 등을 역임한 관리.
    '김사미': {'role': 'other'},  # 고려/고려 후기 - 고려후기 경상북도 청도에서 농민들을 모아 반란을 일으킨 주모자.
    '김사신': {'role': 'other'},  # 남북국시대 통일신라에서 당나라에 사신으로 파견된 관리.
    '김사안': {'role': 'other'},  # 고려 - 고려 후기에, 동지밀직사사, 전라도관찰사 등을 역임한 문신.
    '김사양': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 아찬으로 당나라에 사신으로 파견된 관리.
    '김사엽': {'role': 'scholar foreigner'},  # 현대 - 『조선문학사』, 『이조시대의 가요연구』, 『일본의 만엽집』 등을 저술하였으며, 오사카외국어대학에서 20년 간 재직하여 한국...
    '김사용': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 3·1운동, 계몽운동과 대동청년단 · 의열단의 항일투쟁에 참여한 독립유공자.
    '김사우': {'role': 'other'},  # 조선/조선 전기 - 조선전기 병조판서, 평안도도절제사, 동지중추원사 등을 역임한 무신.
    '김사원': {'role': 'other'},  # 조선 - 조선시대 임진왜란 때, 의병을 규합하여 정제장으로 추대된 문신.
    '김사인': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 때, 신라 무열왕의 4세손으로, 장군, 상대등 등을 역임한 통일신라의 종실.
    '김사정': {'role': 'scholar'},  # 조선 - 조선 중기에, 임진왜란이 발발하자 곽재우 의진에 들어가 화왕산성전투에서 활약하였으며, 『계문예설』, 『후송재문집』 등을 저...
    '김사종': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 제31대 신문왕의 아들인 왕자.
    '김사준': {'role': 'other'},  # 근대 - 조선 후기에, 궁내부특진관, 규장각지후관, 중추원참의 등을 역임한 문신.
    '김사철': {'role': 'other'},  # 근대 - 일제강점기 중추원 찬의, 규장각 제학, 조선귀족(남작) 등을 역임한 관료. 친일반민족행위자.
    '김사행': {'role': 'other'},  # 고려 - 조선전기 겸판사헌부사, 판경흥부사 동판도평의사사 등을 역임한 환관.
    '김사혁': {'role': 'other'},  # 고려 - 고려후기 전리판서, 양광도상원수, 지문하사 등을 역임한 무신.
    '김사형': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 개성윤, 지문하부사 등을 역임하였으며, 이성계를 왕으로 추대해 조선 건국 이후에는 판문하부사, 좌...
    '김산': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 혁명행동 부주필, 북경시위원회 조직부장 등을 역임한 사회주의운동가.
    '김살유': {'role': 'other foreigner'},  # 고대/남북국 - 남북국시대 통일신라의 일길찬으로 일본에 사신으로 파견된 관리.
    '김삼개': {'role': 'other'},  # 고려 - 고려후기 김삼선과 동북면을 침략한 여진족의 관리.
    '김삼광': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 때, 파진찬, 이찬 관등에 임명된 통일신라의 귀족 · 관리.
    '김삼규': {'role': 'other'},  # 현대/대한민국 - 해방 이후 서울대학교 교수, 동아일보 편집국장 등을 역임한 언론인.
    '김삼룡': {'role': 'other'},  # 현대/대한민국 - 해방 이후 민주주의민족전선 상임위원, 남조선노동당 서울지도부 책임자 등을 역임한 사회주의운동가.
    '김삼선': {'role': 'other'},  # 고려 - 고려후기 김삼개와 동북면을 침략한 여진족의 관리.
    '김삼성': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「통영오광대」 큰어미, 사자탈 역 전승자로 인정된 보유자.
    '김삼순': {'role': 'scholar'},  # 현대/대한민국 - 한국인 여성 최초의 농학 박사이자 과학자.
    '김삼조': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 아찬으로 집사성 시중을 역임한 관리.
    '김삼현': {'role': 'other'},  # 조선 - 조선후기 여항육인의 한 사람으로 은거한정을 노래한 음악인.
    '김상': {'role': 'other'},  # 고려/고려 후기 - 고려후기 무진정변과 관련된 노비.
    '김상갑': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 함경남도 단천의 독립만세시위를 주도하는 과정에서 순국한 독립운동가.
    '김상경': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 한산주소감을 역임한 장수.
    '김상구': {'role': 'other'},  # 조선 - 조선 후기에, 승지, 양천현감, 대사간 등을 역임한 문신.
    '김상규': {'role': 'other'},  # 조선 - 조선 후기에, 승지, 대사간 등을 역임한 문신.
    '김상기': {'role': 'scholar'},  # 근대 - 해방 이후 「동학과 동학란」, 「동방문화교류사논고」, 「고려시대사」 등을 저술한 학자. 역사학자.
    '김상길': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 대구상업학교 재학 중 항일 비밀결사인 태극단의 활동을 주도한 독립운동가.
    '김상덕': {'role': 'other'},  # 근대 - 조선 후기에, 인천부사 겸 감리인천항통상사무, 홍주부관찰사 등을 역임하였으며, 을사조약 이후 민종식 의진에서 항일의병투쟁을...
    '김상돈': {'role': 'other'},  # 현대/대한민국 - 반민족행위특별조사위원회 부위원장, 제5대 민의원, 서울특별시장 등을 역임한 정치인.
    '김상로': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 병조판서, 예조참판, 영의정 등을 역임한 문신.
    '김상리': {'role': 'scholar'},  # 조선 - 조선 후기에, 선교랑, 돈녕부주부, 예빈시주부, 순릉참봉 등을 역임하였으며, 「경의」, 『송와집』 등을 저술한 학자.
    '김상림': {'role': 'other foreigner'},  # 고대/남북국/통일신라 - 남북국시대 신라의 불교문화를 일본에 전한 귀족.
    '김상만': {'role': 'other'},  # 현대 - 해방 이후 동아일보 사장, 국제신문협회 본부이사 등을 역임한 언론인.
    '김상묵': {'role': 'other'},  # 조선/조선 후기 - 조선 후기, 정언, 교리, 헌납, 형조참의, 안동부사 등을 지낸 문신.
    '김상범': {'role': 'other'},  # 조선/조선 후기 - 조선후기 관상감관으로 시헌역법을 시행한 관료.
    '김상복': {'role': 'other'},  # 조선 - 조선 후기에, 홍문관제학, 우의정, 영의정 등을 역임한 문신.
    '김상석': {'role': 'other'},  # 조선 - 조선 후기에, 강화유수, 한성부우윤, 판돈녕부사 등을 역임한 문신.
    '김상성': {'role': 'other'},  # 조선 - 조선 후기에, 좌빈객, 판의금부사, 이조판서 등을 역임한 문신.
    '김상숙': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 사옹원주부, 공조정랑, 첨지중추부사 등을 역임한 문신.
    '김상순': {'role': 'other foreigner'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 급찬으로 일본에 파견된 관리.
    '김상신': {'role': 'other'},  # 근대/대한제국기 - 대한제국기 때, 이석용 의진에서 창의동맹의 도로부장으로 활약한 의병.
    '김상악': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 홍릉참봉, 첨지중추부사, 동지중추부사 등을 역임한 문신.
    '김상연': {'role': 'scholar'},  # 조선 - 조선 후기에, 『기기재집』 등을 저술한 학자.
    '김상열': {'role': 'novelist'},  # 현대/대한민국 - 해방 이후 「언챙이곡마단」, 「애니깽」, 「우린 나발을 불었다」 등의 작품을 낸 작가. 연출가, 극단대표, 방송작가.
    '김상옥': {'role': 'poet'},  # 현대 - 해방 이후 『초적』, 『의상』, 『느티나무의 말』 등을 저술한 시인.
    '김상용': {'role': 'poet scholar'},  # 근대/일제강점기 - 일제강점기 『망향』을 저술한 시인. 영문학자, 교육자.
    '김상우': {'role': 'other'},  # 고려 - 고려 전기에 예부상서 · 이부상서 · 형부상서 등을 역임한 문신.
    '김상원': {'role': 'other'},  # 조선 - 조선 후기에, 강원도관찰사, 개성부유수, 대사간 등을 역임한 문신.
    '김상을': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 1945년 한국광복군 제2지대와 미국 전략정보국(OSS)이 함께 추진한 독수리작전에 참여한 독립운동가.
    '김상익': {'role': 'other'},  # 조선 - 조선 후기에, 대사성, 부제학, 도승지 등을 역임한 문신.
    '김상일': {'role': 'scholar'},  # 조선 - 조선 후기에, 「문견록」, 『일엄유고』 등을 저술한 학자.
    '김상적': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 동지의금부사, 예조참판, 형조참판 등을 역임한 문신.
    '김상전': {'role': 'scholar'},  # 조선 - 조선 후기에, 『경의답문』, 『영은문집』 등을 저술한 학자.
    '김상정': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 의성현령, 승지, 대사간 등을 역임한 문신.
    '김상제': {'role': 'other'},  # 고려 - 고려 전기에, 판합문사를 역임한 문신.
    '김상준': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 한국광복군 인면전구공작대 대원으로 인도와 버마(지금의 미얀마) 국경지대인 임팔 전선에 투입되어 대일 ...
    '김상중': {'role': 'other'},  # 조선 - 조선 후기에, 도승지, 한성부부윤, 공조판서 등을 역임한 문신.
    '김상직': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 좌윤, 형조참판, 도승지 등을 역임한 문신.
    '김상진': {'role': 'other'},  # 현대/대한민국 - 대한민국의 민주화운동가로, 1975년 4월 11일 유신체제에 항거하여 할복 자살한 인물.
    '김상집': {'role': 'other'},  # 조선 - 조선 후기에, 공조판서, 예조판서, 우참찬 등을 역임한 문신.
    '김상채': {'role': 'poet'},  # 조선 - 조선후기 『창암집』을 저술한 시인.
    '김상철': {'role': 'other'},  # 조선 - 조선 후기에, 우의정, 좌의정, 영의정 등을 역임한 문신.
    '김상태': {'role': 'other'},  # 근대/대한제국기 - 대한제국기 때. 이강년 의진에서 중군장으로 활약하였으며, 경기도, 강원도, 경상도 일대에서 항일의병투쟁을 전개한...
    '김상한': {'role': 'other'},  # 근대 - 대한제국기 때, 이강년 의진에서 좌익장으로 활약하다가 경상북도 의병장이 되어 항일의병투쟁을 전개한 의병장.
    '김상헌': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 충청남도 천안의 아우내 독립만세시위에 참여했다가 순국한 독립운동가.
    '김상현': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 우참찬, 좌참찬, 판돈녕부사 등을 역임한 문신.
    '김상협': {'role': 'other'},  # 현대/대한민국 - 고려대학교 총장, 문교부장관, 국무총리, 대한적십자사 총재 등을 역임한 교육자 · 관료.
    '김상호': {'role': 'other'},  # 현대/대한민국 - 일제강점기 때, 임시정부를 지원하고 친일승려들을 규탄하는 등 불교계 중심인물이 되어 항일투쟁을 전개한 승려 · 독...
    '김상효': {'role': 'scholar'},  # 근대 - 조선 후기에, 『양사재기』, 『경재기』, 『경재유고』 등을 저술한 학자.
    '김상훈': {'role': 'poet critic'},  # 근대 - 해방 이후 「편복」, 「경부선」, 「전원애화」 등을 저술한 시인. 평론가.
    '김상휴': {'role': 'other'},  # 조선 - 조선 후기에, 판의금부사, 예문관제학, 이조판서 등을 역임한 문신.
    '김생': {'role': 'scholar'},  # 고대/삼국 - 남북국시대 통일신라에서 「태자사낭공대사백월서운탑비」, 「여산폭포시」, 「창림사비」 등의 작품을 낸 서예가.
    '김생려': {'role': 'other'},  # 현대/대한민국 - 해방 이후 서울시립교향악단의 초대지휘자, 남가주필하모닉 상임지휘자 등을 역임한 지휘자. 바이올린연주자.
    '김서': {'role': 'other'},  # 고려 - 고려후기 서북면순문사, 동지밀직사사, 판밀직사사 등을 역임한 무신.
    '김서규': {'role': 'other'},  # 근대 - 일제강점기, 전라남도 지사, 경상북도 지사, 중추원 참의 등을 역임한 관료 · 친일반민족행위자.
    '김서성': {'role': 'scholar'},  # 조선/조선 전기 - 조선 전기에, 문학, 필선, 사재감정 등을 역임한 문신.
    '김서일': {'role': 'scholar'},  # 조선 - 조선 후기에, 『전긍재집』 등을 저술한 학자.
    '김서정': {'role': 'other foreigner'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 사찬으로 일본에 파견된 관리.
    '김서종': {'role': 'other'},  # 근대 - 일제강점기 경의원참의, 총본사전강, 천전건축주비회 부위원장 등을 역임한 대종교인.
    '김서현': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 지방관 및 장군으로 활동한 김유신의 아버지.
    '김석': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 대한교민단의경대 간부, 상해 한인청년당 이사장, 임시정부 외교부장 비서장 등을 역임한 독립운동가.
    '김석견': {'role': 'other'},  # 조선 - 조선 중기에, 임진왜란이 발발하자 세 아들을 이끌고 의병을 일으켜 창암전투에서 활약한 의병장.
    '김석관': {'role': 'other'},  # 현대/대한민국 - 해방 이후 교통부차관, 교통부장관 등을 역임한 관료.
    '김석규': {'role': 'other'},  # 근대 - 조선 후기에, 평리원판사, 한성재판소 수반판사, 형법교정관 등을 역임한 문신.
    '김석근': {'role': 'other'},  # 근대 - 개항기 때, 궁내부특진관, 경효전제조, 장례원경 등을 역임한 문신.
    '김석동': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 1940년 9월 한국광복군에 입대하여 제2지대 본부요원으로 활동하였고, 1943년 6월  『독립신문』...
    '김석문': {'role': 'scholar'},  # 조선/조선 후기 - 조선 후기에, 『역학도해』를 저술하였으며, 최초로 지전설을 주장한 학자.
    '김석신': {'role': 'scholar'},  # 조선/조선 후기 - 조선후기 「도봉도」, 「가고중류도」, 「좌수도해도」 등의 작품을 그린 화가.
    '김석연': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 강화유수, 어영대장, 형조판서 등을 역임한 문신.
    '김석옥': {'role': 'scholar'},  # 조선 - 조선 전기에, 생원이 된 후 벼슬을 지내지 않고 음률을 즐기며 은거하였으며, 호조참판에 추증된 학자.
    '김석운': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 평안북도 의주군 고령삭면 영산시장의 독립만세시위를 주도하는 과정에서 순국한 독립운동가.
    '김석원': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 중일전쟁, 북어사건 당시의 군인. 교육자, 친일반민족행위자.
    '김석익': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 개성유수, 총융사, 한성좌윤 등을 역임한 문신.
    '김석일': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 지평, 정언, 동래부사 등을 역임한 문신.
    '김석주': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 이조좌랑, 우의정 등을 역임한 문신.
    '김석준': {'role': 'poet'},  # 근대 - 조선 후기부터 일제강점기 사이에, 활동한 역관. 시인. 서예가.
    '김석지': {'role': 'novelist'},  # 조선/조선 후기 - 조선 후기, 서북 지역 출신의 문인.
    '김석진': {'role': 'other'},  # 근대 - 조선 후기에, 홍문관장령, 삼도육군통어사, 판돈녕부사 등을 역임한 문신.
    '김석찬': {'role': 'other'},  # 현대/대한민국 - 해방 이후 염천교회를 설립하고, 문창교회에 부임 목회한 목사.
    '김석창': {'role': 'other'},  # 근대 - 일제강점기 때, 선천경찰서 투탄 의거를 지원한 목사 · 독립운동가.
    '김석철': {'role': 'other'},  # 조선/조선 전기 - 조선전기 공조참판, 병조참판, 동지중추부사 등을 역임한 무신.
    '김석출': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「동해안 별신굿」 전승자로 지정된 예능보유자.
    '김석항': {'role': 'other'},  # 근대/대한제국기 - 대한제국기 때, 궁내부 물품사 주사를 역임하였으며, 을사오적 암살을 계획하다 체포되어 순국한 독립운동가.
    '김석형': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 「리조병제사」, 「조선통사」, 「초기 조일관계 연구」 등을 저술한 학자. 역사학자.
    '김석황': {'role': 'other'},  # 근대 - 일제강점기 때, 2·8독립선언에 가담하였으며, 임시정부 특파원, 의용단 서무부장, 임시의정원 황해도대의원 등을 역임한 독립...
    '김석희': {'role': 'scholar'},  # 조선 - 조선후기 성균관사성, 형조참지 등을 역임한 문신. 학자.
    '김선': {'role': 'other'},  # 조선 - 조선 후기에, 형조판서, 한성부판윤 등을 역임한 문신.
    '김선궁': {'role': 'other'},  # 고려 - 고려전기 삼중대광 문하시중을 역임한 장수.
    '김선기': {'role': 'scholar'},  # 근대/대한제국기 | 근대/일제강점기 | 현대 - 일제강점기 때, 조선어학회에서 활동하였으며, 해방 이후 문교부차관, 한글학회 이사 ...
    '김선두': {'role': 'other'},  # 근대 - 일제강점기, 조선예수교장로회 총회장으로서 평양 장로교계 3·1운동을 주동했던 목사.
    '김선량': {'role': 'other'},  # 근대 - 일제강점기 때, 동우회에 가입하여 기관지 『동광』을 발간하고 항일투쟁을 전개한 독립운동가.
    '김선봉': {'role': 'other'},  # 현대 - 해방 이후 봉산탈춤 전승자로 지정된 기예능보유자.
    '김선석': {'role': 'other'},  # 고려 - 고려 전기에, 추밀원사, 좌복야판호부사, 중서시랑평장사 등을 역임한 문신.
    '김선여': {'role': 'other'},  # 근대 - 대한제국기 때, 신보현 의진에서 선봉장으로 활약하다가 독자적으로 의진을 조직하여 항일의병투쟁을 전개한 의병장.
    '김선영': {'role': 'other'},  # 현대 - 해방 이후 「자명고」, 「마의태자」, 「은하수」 등에 출연한 배우.
    '김선장': {'role': 'other'},  # 고려/고려 후기 - 고려후기 신궁건축 감독관, 청도군 지군사 등을 역임한 무신.
    '김선치': {'role': 'other'},  # 고려 - 고려후기 전리판서, 계림부윤 등을 역임한 무신.
    '김선태': {'role': 'other'},  # 현대/대한민국 - 일제강점기 전주지방법원 판사, 대전지방법원 청주지청 판사 등을 역임한 법조인. 정치인.
    '김선평': {'role': 'other'},  # 고려 - 고려전기 대광, 아보 등을 역임한 무신.
    '김선필': {'role': 'other'},  # 근대 - 개항기 지삼군부사, 대호군, 강화부유수 등을 역임한 무신.
    '김선행': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 대사헌, 좌윤 등을 역임한 문신.
    '김설': {'role': 'other'},  # 조선 - 조선 후기에, 검열, 대교, 예빈시정 등을 역임한 문신.
    '김섬': {'role': 'other'},  # 조선 - 조선시대 임진왜란 당시 의기(義妓)로 알려진 기생.
    '김성': {'role': 'other'},  # 고려 - 고려후기 제주부사 장윤화의 침학에 반란을 일으킨 주모자.
    '김성곤': {'role': 'other'},  # 현대 - 해방 이후 금성방직, 쌍용양회 등을 설립한 실업가. 언론인 · 정치인.
    '김성구': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 강원도관찰사, 병조참지, 호조참의 등을 역임한 문신.
    '김성규': {'role': 'other'},  # 조선 - 조선 후기에, 고창군수, 장성군수, 강원도순찰사 등을 역임한 문신.
    '김성균': {'role': 'scholar'},  # 근대 - 해방 이후 「국사강좌」, 「한국사입문」, 「세계문화사」 등을 저술한 학자. 역사학자.
    '김성근': {'role': 'other'},  # 근대 - 일제강점기 때, 임시의정원 함경도대표의원, 구국모험단 단장 등을 역임한 독립운동가.
    '김성기': {'role': 'other'},  # 현대/대한민국 - 서울지방검찰청 부장검사, 대검찰청 총무부 부장, 법무부장관 등을 역임하다가 박종철 고문치사 사건으로 경질된 법조인...
    '김성대': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「양주별산대놀이」 연희 및 가면 제작 전승자로 지정된 기능보유자.
    '김성도': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 광복군 제3지대에 입대하여 광복군 징모 공작을 전개한 독립운동가.
    '김성동': {'role': 'other'},  # 조선 - 조선 전기에, 당상관, 부평부사, 가선대부 등을 역임한 문신.
    '김성룡': {'role': 'other'},  # 현대/대한민국 - 해방 이후 공군사관학교 교장, 공군참모총장, 대장 등을 역임한 군인.
    '김성립': {'role': 'other'},  # 조선/조선 전기 - 조선 전기 승문원정자, 홍문관저작 등을 지냈고, 허난설헌의 남편이자 문장가인 문신.
    '김성무': {'role': 'other'},  # 근대 - 일제강점기 때, 조선여자기독교청년회연맹을 창설하고, 근우회 조직활동에 참여한 교육자 · 독립운동가.
    '김성발': {'role': 'other'},  # 조선 - 조선 후기에, 원주목사, 종부시정, 금산군수 등을 역임한 문신.
    '김성배': {'role': 'other'},  # 현대/대한민국 - 해방 이후 건설부장관, 서울시장, 강원도지사 등을 역임한 관료.
    '김성범': {'role': 'other'},  # 근대 - 일제강점기 때, 천마단 사령부 오장으로 활동하며 항일무장투쟁을 전개한 독립운동가.
    '김성수': {'role': 'other'},  # 근대 - 일제강점기 때 의열단 · 남화한인청년연맹 등에서 활동하며 친일파 처단 등 항일무장투쟁을 전개한 독립운동가.
    '김성숙': {'role': 'other'},  # 현대/대한민국 - 일제강점기 때, 조선의용대 정치부장, 임시정부 국무위원 등을 역임하였으며, 해방 이후, 혁신정당의 지도자로 활동한...
    '김성식': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 「대학사」, 「역사와 현실」 , 「내가 본 서양」 등을 저술한 학자. 역사학자.
    '김성업': {'role': 'other'},  # 근대 - 일제강점기 때, 동아일보 평양지국장, 조선물산장려회 이사장, 소년척후대 평안남도연맹 부이사장 등을 역임한 독립운동가.
    '김성열': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 천도교 전교사로 활동하며 구국동지회에 가입하였고, 수원의 독립만세시위를 주도하다가 고주리 학살사...
    '김성엽': {'role': 'other'},  # 근대 - 일제강점기 때, 광복군사령부 국내특파원으로 활동하며 친일파 숙청, 군자금 모금, 국내 조직확대 등을 전개한 독립운동가.
    '김성옥': {'role': 'other'},  # 조선 - 조선후기 진양조장단을 처음 판소리에 응용한 판소리의 명창.
    '김성원': {'role': 'scholar'},  # 조선 - 조선시대 제원도찰방, 동복현감 등을 역임한 문신. 학자.
    '김성은': {'role': 'other'},  # 현대/대한민국 - 해방 이후 해병교육단장, 해병대 부사령관, 해병대사령관 등을 역임한 군인. 관료.
    '김성응': {'role': 'other'},  # 조선/조선 후기 - 조선후기 판의금부사, 병조판서, 훈련대장 등을 역임한 무신.
    '김성익': {'role': 'other'},  # 조선 - 조선 후기에, 참봉, 시직, 부수 등을 역임한 문신.
    '김성일': {'role': 'other'},  # 조선 - 조선후기 도총부경력, 영원군수, 삭주도호부사 등을 역임한 무신.
    '김성적': {'role': 'other'},  # 조선 - 조선 후기에, 대사간, 이조참의, 충청도관찰사 등을 역임한 문신.
    '김성진': {'role': 'other'},  # 현대/대한민국 - 해방 이후 동양통신 정치부장 겸 편집부국장, 연합통신 사장 등을 역임한 언론인. 관료.
    '김성춘': {'role': 'scholar'},  # 근대 - 해방 이후 「자유만세」 · 「오발탄」 등의 작품에 관여한 영화인. 영화조명기사.
    '김성칠': {'role': 'scholar'},  # 현대 - 해방 이후 「조선역사」, 「동양사개설」 등을 저술한 학자. 역사학자.
    '김성탁': {'role': 'scholar'},  # 조선 - 조선후기 사간원정언, 홍문관수찬 등을 역임한 문신. 학자.
    '김성태': {'role': 'scholar'},  # 현대/대한민국 - 고려대학교 교수, 한국심리학 회장 등을 역임하였으며, 『실험연구의 방법』, 『발달심리학』 등을 저술한 심리학자.
    '김성택': {'role': 'other'},  # 근대/일제강점기 | 현대 - 해방 이후 북한에서 고려청자 제작기술을 재현하여 도자기를 제작한 공예가. 도자공예가.
    '김성하': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 병자호란 당시 남한산성에서 인조를 호종한 문신.
    '김성학': {'role': 'other'},  # 근대 - 일제강점기 용산 예수성심신학교, 평양성당 등에서 사목한 신부.
    '김성한': {'role': 'novelist'},  # 근대/일제강점기 | 현대 - 해방 이후 「오 분간」 · 「바비도」, 『임진왜란』 등을 저술한 소설가.
    '김성현': {'role': 'other'},  # 근대 - 일제강점기 때, 전라남도 곡성, 담양에서 군자금 모금 활동을 전개한 독립운동가.
    '김성호': {'role': 'other'},  # 근대 - 일제강점기 때, 대한정의군정서 사찰과 서기 등을 역임하였으며, 선천경찰서 투탄 의거에 가담한 독립운동가.
    '김성환': {'role': 'other'},  # 현대/대한민국 - 해방 이후 은행감독원 원장, 한국은행 총재 등을 역임한 금융인. 정치인.
    '김성후': {'role': 'scholar'},  # 조선 - 조선후기 풍기군수, 성균관사성, 사간원사간 등을 역임한 문신. 학자.
    '김성휘': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 상해청년연맹에서 항일투쟁을 전개한 독립운동가.
    '김세광': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 조선혁명간부학교 교관, 조선민족혁명당 중앙군사학 편찬위원, 조선의용대 제3지대장 등을 역임한 군...
    '김세균': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 좌참찬, 수원유수 등을 역임한 문신.
    '김세기': {'role': 'other'},  # 근대 - 개항기 때, 비서원경, 시종원경, 전라남도관찰사 등을 역임한 문신.
    '김세덕': {'role': 'other'},  # 고려 - 고려 후기에, 친종호군 등을 역임한 무신 · 공신.
    '김세련': {'role': 'other'},  # 현대/대한민국 - 한국산업은행 총재, 재무부장관, 한국은행 총재, 국회의원 등을 역임한 금융인 · 정치인.
    '김세렴': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 도승지, 호조판서 등을 역임한 문신.
    '김세록': {'role': 'scholar'},  # 조선/조선 후기 - 조선후기 「신죽」 · 「통죽」 · 「죽보」 등의 작품을 그린 화가.
    '김세민': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 인순부윤, 전라도관찰사, 판돈녕부사 등을 역임한 문신.
    '김세연': {'role': 'other'},  # 근대/일제강점기 | 현대 - 해방 이후 조선건축기술단 초대단장, 조선토건협회 초대회장 등을 역임한 건축가.
    '김세열': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 항일단체인 구국동지회에 가입하였고, 수원의 독립만세시위에 참여했다가 고주리 학살사건에 의해 사망...
    '김세용': {'role': 'other'},  # 근대 - 일제강점기 때, 광복군에서 활동하며 정보 수집과 초모공작을 전개한 독립운동가.
    '김세우': {'role': 'other'},  # 조선 - 조선 전기에, 전적, 적성현감 등을 역임한 문신.
    '김세익': {'role': 'other'},  # 조선 - 조선 후기에, 지평, 승지, 경상도관찰사 등을 역임한 문신.
    '김세일': {'role': 'novelist'},  # 현대/대한민국 - 해방 이후 레닌기치 기자를 역임한 작가. 언론인.
    '김세적': {'role': 'other'},  # 조선/조선 전기 - 조선전기 충청도관찰사, 형조참판, 행첨지중추부사 등을 역임한 무신.
    '김세정': {'role': 'other'},  # 조선 - 조선 후기에, 헌납, 집의, 우부승지 등을 역임한 문신.
    '김세종': {'role': 'other'},  # 조선 - 조선후기 신재효의 제자로 판소리 이론에 뛰어났던 판소리의 명창.
    '김세중': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 「십자가」, 「최후의 심판도」, 「충무공이순신장군상」 등의 작품을 낸 조각가.
    '김세지': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 대한애국부인회 재무부 부부장으로 활동한 개신교인. 전도부인.
    '김세진': {'role': 'other'},  # 현대/대한민국 - 대한민국의 학생운동가 · 반미운동가 · 반전운동가로, 1980년대 반미자주화운동을 선도한 인물.
    '김세충': {'role': 'other'},  # 고려 - 고려 후기에, 야별초지유를 역임한 문신.
    '김세탁': {'role': 'other'},  # 근대 - 일제강점기 때, 105인 사건으로 복역하였으며, 출옥 후 만주로 망명하여 한족회에서 활동하다가 일본군의 만주대학살에 의해 ...
    '김세필': {'role': 'scholar'},  # 조선 - 조선전기 전라도관찰사, 대사헌, 이조참판 등을 역임한 문신. 학자.
    '김세행': {'role': 'other'},  # 조선 - 조선 후기에, 대동찰방을 역임한 문신.
    '김세형': {'role': 'other'},  # 현대/대한민국 - 일제강점기 「먼길」 · 「오텔로」 · 「뱃노래」 등을 만든 작곡가.
    '김세호': {'role': 'other'},  # 근대 - 조선 후기에, 경상도관찰사, 한성부판윤 등을 역임한 문신.
    '김세환': {'role': 'other'},  # 근대 - 일제강점기 때, 삼일남녀학교와 수원상업학교를 설립하여 후진교육에 힘쓴 교육자 · 독립운동가.
    '김세흠': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 지평, 교리, 수찬 등을 역임한 문신.
    '김소': {'role': 'other'},  # 조선 - 조선 전기에, 성균관사성, 종학박사 등을 역임한 문신.
    '김소랑': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 신극 초창기 신파 배우.
    '김소모': {'role': 'other foreigner'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 살찬으로 일본에 사신으로 파견된 관리.
    '김소엽': {'role': 'poet novelist'},  # 근대 - 일제강점기 「배우에게」, 「흙 한 줌 쥐고」 등을 저술한 시인. 소설가.
    '김소운': {'role': 'poet essayist'},  # 근대/일제강점기 - 일제강점기 「신조」 등을 저술한 시인. 수필가 · 번역문학가.
    '김소월': {'role': 'poet'},  # 일제강점기 「금잔디」, 「첫치마」, 「엄마야 누나야」 등을 저술한 시인.
    '김소진': {'role': 'novelist'},  # 현대/대한민국 - 해방 이후 『열린사회와 그 적들』, 『자전거 도둑』, 『양파』 등을 저술한 소설가.
    '김소충': {'role': 'other foreigner'},  # 남북국시대 통일신라의 대통사로 일본에 파견된 관리.
    '김소희': {'role': 'other'},  # 현대/대한민국 - 해방 이후 판소리의 전승자로 지정된 예능보유자.
    '김속명': {'role': 'other'},  # 고려 - 고려 후기에, 첨의평리, 평양도도순문사, 대사헌 등을 역임한 문신.
    '김송': {'role': 'novelist'},  # 근대/일제강점기 - 일제강점기 「국경의 주막」, 「추계」, 「봉황금」 등을 저술한 작가. 소설가.
    '김수': {'role': 'other'},  # 조선 - 조선 중기에, 경상도관찰사, 한성판윤, 호조판서 등을 역임한 문신.
    '김수강': {'role': 'other'},  # 고려 - 고려 후기에, 직사관, 시어사, 중서사인 등을 역임한 문신.
    '김수경': {'role': 'other'},  # 조선 - 조선 전기에, 장단부사, 연안부사, 이천부사 등을 역임한 문신.
    '김수곡': {'role': 'other foreigner'},  # 근대 - 대한제국기 때, 정관직 의진에서 군자금 모금, 일본인 관리 처단 활동 등을 전개한 의병.
    '김수규': {'role': 'scholar'},  # 조선/조선 후기 - 조선후기 「사옹귀조도」 · 「기려도강도」 등의 작품을 그린 화가.
    '김수근': {'role': 'other'},  # 현대/대한민국 - 해방 이후 공간사옥, 마산성당 등을 신축한 건축가.
    '김수남': {'role': 'other'},  # 근대 - 일제강점기 때, 군산공립보통학교 방화사건을 주도한 독립운동가.
    '김수담': {'role': 'scholar'},  # 조선 - 조선후기 예조좌랑, 고령현감 등을 역임한 문신. 학자.
    '김수돈': {'role': 'poet'},  # 현대/대한민국 - 해방 이후 『소연가』, 『우수의 황제』 등을 저술한 시인.
    '김수동': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 경상남도 창원의 삼진 만세운동을 주도하는 과정에서 순국한 독립운동가.
    '김수렴': {'role': 'other'},  # 조선 - 조선 후기에, 사섬시부정, 절충장군, 첨지중추부사 등을 역임한 문신.
    '김수령': {'role': 'scholar'},  # 조선/조선 전기 - 조선전기 대사간, 참판 등을 역임한 문신. 학자.
    '김수만': {'role': 'other'},  # 고려 - 고려 후기에, 진원부원군 등을 역임한 환관 · 공신.
    '김수문': {'role': 'other'},  # 조선/조선 전기 - 조선전기 지중추부사, 한성판윤, 평안도병마절도사 등을 역임한 무신.
    '김수미산': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 사찬 관등의 귀족.
    '김수민': {'role': 'other'},  # 근대 - 대한제국기 때, 경기도 장단에서 의병을 일으켜 13도총도독으로 활약한 의병장.
    '김수산': {'role': 'other'},  # 현대/대한민국 - 해방 이후 브라질에서 한인교포사회의 경제적 기반을 만든 교민. 의류제조업자.
    '김수석': {'role': 'other'},  # 현대 - 해방 이후 「북청사자놀음」 전승자로 지정된 기예능보유자.
    '김수선': {'role': 'other'},  # 현대/대한민국 - 제헌국회의원, 제3대 국회의원 등을 역임한 정치인.
    '김수성': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 경기도관찰사, 황해도관찰사, 공조참의 등을 역임한 문신.
    '김수악': {'role': 'other'},  # 현대/대한민국 - 진주검무와 진주교방굿거리춤 예능보유자. 전통무용가.
    '김수영': {'role': 'poet'},  # 현대 - 해방 이후 「달나라의 장난」, 「헬리콥터」, 「폭포」 등을 저술한 시인.
    '김수온': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 지영천군사, 판중추부사, 호조판서 등을 역임한 문신.
    '김수익': {'role': 'other'},  # 조선 - 조선 후기에, 응교, 병조참의, 제주목사 등을 역임한 문신.
    '김수인': {'role': 'other'},  # 조선 - 조선후기 양주목사, 수원부사, 익산군수 등을 역임한 문신. 서예가.
    '김수자': {'role': 'other'},  # 고려 - 고려 전기에, 국학학유, 직사관, 예주방어사 등을 역임한 문신.
    '김수장': {'role': 'other'},  # 조선 - 조선후기 3대 시조집의 하나인 『해동가요』를 편찬한 음악인.
    '김수정': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 하규일의 제자로 여창가곡의 명창.
    '김수제': {'role': 'other'},  # 고려 - 고려후기 백주소복별감을 역임한 관리.
    '김수조': {'role': 'other'},  # 현대 - 해방 이후 브라질 농업이민을 태동시킨 교민.
    '김수증': {'role': 'scholar'},  # 조선/조선 후기 - 조선 후기에, 세마, 형조정랑, 공조정랑 등을 역임하였으며, 『곡운집』, 『곡운구곡도첩』 등을 저술한 문신.
    '김수창': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 병자호란 당시 남한산성에서 인조를 호종한 문신.
    '김수천': {'role': 'other'},  # 근대 - 일제강점기 아악에 정통한 음악인. 장구명인.
    '김수철': {'role': 'scholar'},  # 조선/조선 후기 - 조선후기 「송계한담도」 · 「자양화도」 등의 작품을 그린 화가.
    '김수충': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 제33대 성덕왕의 아들인 왕자.
    '김수학': {'role': 'other'},  # 현대/대한민국 - 상공은행 이사, 대한무진금융주식회사 사장, 상공부차관, 제2대 국회의원 등을 역임한 금융인 · 정치인.
    '김수항': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 예조판서, 좌의정, 영의정 등을 역임한 문신.
    '김수현': {'role': 'other'},  # 현대/대한민국 - 해방 이후 선소리산타령의 전승자로 지정된 예능보유자.
    '김수홍': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 승지, 호조참판, 지돈녕부사 등을 역임한 문신.
    '김수환': {'role': 'other'},  # 현대/대한민국 - 해방 이후 한국천주교 주교회의 의장, 아시아 주교회의 공동의장 등에 서임된 사제. 추기경.
    '김수훈': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라에서 당에 파견한 숙위학생으로 빈공과에 합격한 문장가.
    '김수흥': {'role': 'scholar'},  # 조선 - 조선후기 도승지, 호조판서, 영의정 등을 역임한 문신. 학자.
    '김숙년': {'role': 'other'},  # 현대/대한민국 - 해방 이후, 서울 반가 음식을 계승해온 전통 요리 연구가.
    '김숙룡': {'role': 'other'},  # 고려 - 고려 후기에, 추밀원좌승선 공부상서 지이부사, 지추밀원사 병부상서 상장군 등을 역임한 문신.
    '김숙명': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 대아찬 관등의 귀족.
    '김숙자': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「살풀이춤(경기도 도당굿 도살풀이)」의 전승자로 지정된 예능보유자. 전통무용가.
    '김숙정': {'role': 'scholar'},  # 고대/남북국/통일신라 - 남북국시대 때, 숙위학생으로 당나라에서 유학하여 빈공과에 급제한 통일신라의 학자.
    '김숙흘종': {'role': 'other'},  # 고대/삼국/신라 - 신라의 제24대 진흥왕의 동생이자 삼국통일을 이끈 김유신의 외할아버지인 왕족.
    '김숙흥': {'role': 'other'},  # 고려 - 고려 전기에, 거란의 침입으로부터 대항하다 전사한 무신 · 공신.
    '김순': {'role': 'other'},  # 조선 - 조선 후기에, 이천군수, 동지중추부사, 돈지돈녕부사 등을 역임한 문신.
    '김순고': {'role': 'other'},  # 조선/조선 전기 - 조선전기 포도대장, 지훈련원사, 비변사제조 등을 역임한 무신.
    '김순구': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 충청북도 옥천군 군서면의 독립만세시위를 주도한 혐의로 체포되어 옥중에서 순국한 독립운동가.
    '김순남': {'role': 'other'},  # 근대 - 일제강점기로부터 대한민국 건국 초기에 활동한 월북 작곡가. 피아니스트. 지휘자. 음악이론가.
    '김순명': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 의금부동지사, 황해도관찰사 등을 역임한 문신.
    '김순몽': {'role': 'other'},  # 조선/조선 전기 - 조선전기 내의원제조, 대비이어소 시약의원, 행부호군 등을 역임한 의관.
    '김순부': {'role': 'other'},  # 고려 - 고려 전기 묘청의 난 때, 평주판관 등을 역임하였으며, 반란군을 진압한 문신.
    '김순서': {'role': 'other'},  # 근대/일제강점기 - 일제강점기, 경기도 안성군 원곡면 · 양성면에서 일어난 독립만세운동을 주도한 독립운동가.
    '김순손': {'role': 'other'},  # 조선/조선 전기 - 조선전기 승선색, 상전 등을 역임한 환관.
    '김순식': {'role': 'scholar'},  # 근대/일제강점기|현대 - 일제강점기 때, 『은행부기강의안』, 『상업부기요의』 등을 저술하였으며, 해방 후에 고려대학교 교수, 부산대...
    '김순애': {'role': 'other'},  # 현대/대한민국 - 해방 이후 김순애가곡집, 김순애동요곡집 등을 발표한 작곡가.
    '김순원': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 대아찬으로 시중을 역임한 귀족.
    '김순이': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 경상남도 통영의 독립만세시위를 준비하다 체포된 독립운동가.
    '김순정': {'role': 'other'},  # 고대/남북국/통일신라 - 통일신라의 제35대 경덕왕의 장인으로, 이찬 관등에 임명된 귀족.
    '김순태': {'role': 'other'},  # 현대 - 해방 이후 「선소리산타령」의 전승자로 지정된 예능보유자.
    '김순하': {'role': 'other'},  # 근대/일제강점기|현대 - 해방 이후 대한건축사협회 이사장, 대한건축사협회 창립회장 등을 역임한 건축가.
    '김순흠': {'role': 'other'},  # 근대/개항기 - 개항기 때, 이강년 의진에서 활동하다가 국권 피탈 이후 단식을 감행하여 자결한 의병 · 열사.
    '김술종': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 대등, 삭주도독 등을 역임한 귀족.
    '김숭겸': {'role': 'poet'},  # 조선 - 조선후기 『관복암유고』을 저술한 시인.
    '김숭빈': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 때, 신라의 소성왕, 헌덕왕, 흥덕왕의 형제로, 시중, 상대등 등을 역임한 통일신라의 귀족 · 관리.
    '김숭정': {'role': 'other'},  # 고려 - 고려 전기에, 안변도호부판관 등을 역임하였으며, 동여진 고지문의 습격에 원병이 도착한 것처럼 대응하여 적을 물리친 문신.
    '김숭조': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 사예, 사간, 나주목사 등을 역임한 문신.
    '김승': {'role': 'other'},  # 고려 - 고려 후기에, 승지를 역임한 문신.
    '김승경': {'role': 'other'},  # 조선 - 조선전기 예조참판, 대사헌 등을 역임한 문신.
    '김승곤': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 한국광복군 제1지대 본부 부관주임 겸 본부 구대장으로 활동한 독립운동가.
    '김승구': {'role': 'other'},  # 고려 - 고려 후기에, 전의령, 강릉도존무사, 경상도안렴사 등을 역임한 문신.
    '김승규': {'role': 'other'},  # 근대 - 조선 후기에, 군부협판, 육군연성학교장, 규장각제학 등을 역임한 문신.
    '김승득': {'role': 'other'},  # 고려 - 고려후기 집의, 좌부대언 등을 역임한 문신. 간신.
    '김승록': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 간도 용정촌에서 전개된 독립만세시위를 주도하는 과정에서 순국한 독립운동가.
    '김승만': {'role': 'other'},  # 근대 - 일제강점기 때, 독립단 의주지국평북총감, 광복군 참리부 협찬, 대한통의부 서무부장 등을 역임한 독립운동가.
    '김승무': {'role': 'other'},  # 고려 - 고려 후기에, 사한, 시어사 등을 역임한 문신.
    '김승민': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 만주에서 광복단 조직에 참여하여 항일무장투쟁을 전개한 독립운동가.
    '김승빈': {'role': 'other'},  # 근대 - 일제강점기 때, 신흥무관학교 교관, 대한의용군 소대장, 고려혁명군정의회 장교 등을 역임한 군인 · 교육자 · 독립운동가.
    '김승옥': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 전라북도 고창의 독립만세시위를 주도한 혐의로 체포되었으며, 출옥 이후 고창군 청년회장으로 활약하...
    '김승용': {'role': 'other'},  # 고려 - 고려 후기에, 내부령, 밀직사 등을 역임한 문신.
    '김승원': {'role': 'other foreigner'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 대아찬으로 일본에 사신으로 파견된 관리.
    '김승위': {'role': 'other'},  # 고려 - 고려전기 대장군, 병부상서 등을 역임한 무신.
    '김승조': {'role': 'other'},  # 고려 - 고려 전기에, 내서랑으로 목종의 교육을 담당하여 사공에 추증된 관리 · 공신.
    '김승주': {'role': 'other'},  # 조선/조선 전기 - 조선전기 병조판서, 판중군도총제, 평양부원군 등을 역임한 무신.
    '김승준': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에 중낭장 · 차장군 등을 역임한 무신 · 공신.
    '김승택': {'role': 'other'},  # 고려 - 고려 후기에, 서연관, 찬성사, 중서평장사 등을 역임한 문신.
    '김승학': {'role': 'other'},  # 근대 - 일제강점기 때, 한국독립당과 군민의회를 조직하였으며, 임시의정원 평안도대표의원, 임시정부 학무부차장 등을 역임한 독립운동가.
    '김승한': {'role': 'other'},  # 고려 - 고려 후기에, 밀직부사 등을 역임한 문신.
    '김승호': {'role': 'other'},  # 근대 - 해방 이후 「소」, 「무지개」, 「갈매기」 등에 출연한 배우. 영화배우.
    '김승환': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 북선상업은행 은행장을 역임한 실업가.
    '김시': {'role': 'scholar'},  # 조선 - 조선시대 「동자견려도」, 「한림제설도」, 「황우도」 등의 작품을 그린 화가.
    '김시걸': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 승지, 전라도관찰사, 대사간 등을 역임한 문신.
    '김시구': {'role': 'other'},  # 조선 - 조선 후기에, 장령, 전사관, 승지 등을 역임한 문신.
    '김시국': {'role': 'other'},  # 조선 - 조선 후기에, 제학, 대사성, 판의금부사 등을 역임한 문신.
    '김시권': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 강원도지사, 조선임전보국단 이사장 등을 역임한 관료.
    '김시묵': {'role': 'other'},  # 조선 - 조선 후기에, 판의금부사, 선혜청당상, 좌참찬 등을 역임한 문신.
    '김시민': {'role': 'scholar'},  # 조선 - 조선후기 의빈부도사, 진산군수, 낭천현감 등을 역임한 문신. 학자.
    '김시백': {'role': 'other'},  # 근대/대한제국기 - 대한제국기 때, 김상태 의진에서 영월의병장, 소모장 등으로 활동한 의병장.
    '김시번': {'role': 'other'},  # 조선 - 조선 후기에, 암행어사, 집의, 예조참의 등을 역임한 문신.
    '김시빈': {'role': 'other'},  # 조선 - 조선 후기에, 필선, 장령, 울산부사 등을 역임한 문신.
    '김시성': {'role': 'other'},  # 조선 - 조선후기 어영중군, 경상병사, 통제사 등을 역임한 무신.
    '김시습': {'role': 'scholar novelist'},  # 조선전기 『매월당집』 · 『금오신화』 · 『만복사저포기』 등을 저술한 학자. 문인.
    '김시약': {'role': 'other'},  # 조선 - 조선 후기에, 통영군관, 훈련원첨정 등을 역임한 무신 · 공신.
    '김시양': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 예조정랑, 도원수, 판중추부사 등을 역임한 문신.
    '김시연': {'role': 'other'},  # 근대 - 조선 후기에, 성균관대사성, 강원도관찰사, 전라도관찰사 등을 역임한 문신.
    '김시온': {'role': 'novelist'},  # 조선/조선 후기 - 조선 후기 경상북도 안동에서 학문과 후학 양성에 전념한 문인.
    '김시위': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 부교리, 승지, 영광군수 등을 역임한 문신.
    '김시유': {'role': 'other'},  # 조선 - 조선후기 청어(淸語)에 능통하고 외교적 활동이 뛰어났던 역관.
    '김시주': {'role': 'other'},  # 조선 - 조선 후기에, 승정원주서, 병부랑 등을 역임한 문신.
    '김시중': {'role': 'other'},  # 근대/대한제국기 - 대한제국기 때, 이경년 의진의 좌선봉장, 김상태 의진 중군장 등으로 활약한 의병장.
    '김시진': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 한성부좌윤, 수원부사, 호조참판 등을 역임한 문신.
    '김시찬': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 수찬, 대사간, 부제학 등을 역임한 문신.
    '김시창': {'role': 'other'},  # 조선 - 조선전기 효행으로 정려를 하사 받고, 현량과에 피천된 효자.
    '김시풍': {'role': 'other'},  # 근대 - 개항기 전주감영영장을 역임한 무신.
    '김시헌': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 동지춘추관사, 예조참판, 도승지 등을 역임한 문신.
    '김시혁': {'role': 'other'},  # 조선 - 조선 후기에, 호조참판, 대사헌, 판돈녕부사 등을 역임한 문신.
    '김시현': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 의열단에서 항일투쟁을 전개하였고 해방 이후, 국회의원을 역임하였으며, 이승만의 독재정권에 불만을...
    '김시형': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 판의금부사, 판돈녕부사, 병조판서 등을 역임한 문신.
    '김시황': {'role': 'other'},  # 근대 - 일제강점기 때, 보합단을 조직하여 항일무장투쟁을 전개한 독립운동가.
    '김시회': {'role': 'other'},  # 조선 - 조선 전기에, 예문관대교, 부평부사 등을 역임한 문신.
    '김식': {'role': 'scholar'},  # 조선/조선 전기 - 조선시대 「고목우도」 · 「영모도」 등의 작품을 그린 화가.
    '김식재': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 최씨무인정권을 무너뜨리고 권력을 잡은 김준의 샛째 아들로, 전전승지동정 등을 역임한 무신 · 공신.
    '김신': {'role': 'other'},  # 고려 - 고려전기 묘청의 난 과 관련된 관리. 역신.
    '김신겸': {'role': 'scholar'},  # 조선 - 조선 후기에, 「백육애음」, 『증소집』 등을 저술한 학자.
    '김신국': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 공조판서, 형조판서, 영중추부사 등을 역임한 문신.
    '김신련': {'role': 'other'},  # 고려/고려 전기 - 고려 전기 묘청의 난을 진압하는 데 참여한 문신.
    '김신망': {'role': 'scholar'},  # 조선/조선 후기 - 조선 후기 『가례기의』를 저술한 학자.
    '김신복': {'role': 'other foreigner'},  # 고대/남북국/통일신라 - 남북국시대 통일신라에서 일본에 사신으로 파견된 관리.
    '김신술': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 각간 관등의 귀족.
    '김신영': {'role': 'other'},  # 고려 - 고려후기 전주 죽동의 반란과 관련된 무신.
    '김신윤': {'role': 'other'},  # 고려 - 고려 후기에, 우간의대부, 좌간의대부, 판대부사 등을 역임한 문신.
    '김신재': {'role': 'other'},  # 현대 - 해방 이후 「낙조」 · 「뻐꾸기도 밤에 우는가」 등에 출연한 배우.
    '김실': {'role': 'other'},  # 고려 - 고려후기 수성원수, 문하찬성사 상의 등을 역임한 환관.
    '김심': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 부총관, 대사헌, 지중추부사 등을 역임한 문신.
    '김심백': {'role': 'other'},  # 고려 - 고려후기 7품, 5품 별장을 역임한 관리.
    '김심언': {'role': 'other'},  # 고려 - 고려 전기에, 예부상서, 내사시랑평장사, 서경유수 등을 역임한 문신.
    '김아파나시아르센지예비치': {'role': 'other'},  # 근대 - 일제강점기 공산당 연해주위원회 고려부장, 포시에트 구역당 제1비서 등을 역임한 사회주의운동가.
    '김악': {'role': 'other foreigner'},  # 고대/남북국/통일신라|고려/고려 전기 - 남북국시대 때, 신라의 사신으로서 중국을 내왕하던 중 후백제 측에 붙잡혀 관직을 가졌으며,...
    '김안': {'role': 'other'},  # 고려/고려 전기 - 고려 전기 묘청, 정지상 일파로 활약한 문신.
    '김안국': {'role': 'scholar'},  # 조선/조선 전기 - 조선전기 수교리, 예조판서, 판중추부사 등을 역임한 문신. 학자.
    '김안로': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 이조판서, 도총관, 대제학, 좌의정 등을 역임한 문신.
    '김안정': {'role': 'other'},  # 조선 - 조선 전기에, 도승지, 개성유수 등을 역임한 문신.
    '김알렉산드라': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 하바로프스크시당 비서, 극동인민위원회 외무부장 등을 역임한 사회주의운동가.
    '김알지': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라 경주김씨의 시조.
    '김암': {'role': 'other'},  # 고대/남북국 - 남북국시대 통일신라의 양주, 강주, 한주태수, 집사시랑 등을 역임한 문신. 방술가(方術家).
    '김압실': {'role': 'other foreigner'},  # 고대/남북국/통일신라 - 남북국시대 통일신라에서 일본에 파견된 사신.
    '김애': {'role': 'other'},  # 고려 - 고려 후기에, 합문지후, 우부승선, 동지공거 등을 역임한 문신.
    '김애마': {'role': 'other'},  # 현대/대한민국 - 해방 이후 이화여자대학교 초대학장, 문교부 대학교육위원 등을 역임한 교육자.
    '김약': {'role': 'scholar'},  # 조선 - 조선 중기에, 임진왜란이 발발하자 스승 조헌과 함께 의병을 일으킨 학자.
    '김약련': {'role': 'other'},  # 조선 - 조선 후기에, 전적, 병조좌랑, 좌부승지 등을 역임한 문신.
    '김약로': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 좌의정, 약방도제조, 판중추부사 등을 역임한 문신.
    '김약묵': {'role': 'other'},  # 조선 - 조선 전기에, 내자시정, 양주목사 등을 역임한 문신.
    '김약선': {'role': 'other'},  # 고려 - 고려 후기에, 추밀부사 등을 역임한 문신.
    '김약수': {'role': 'other'},  # 현대/대한민국 - 일제강점기 조선노동공제회, 조선노동총동맹 창설에 참여한 노동운동가. 정치인.
    '김약슬': {'role': 'scholar'},  # 근대 - 해방 이후 『신라, 백제, 고구려나려예문지』를 편찬한 학자. 장서가.
    '김약시': {'role': 'other'},  # 고려 - 고려 후기에, 진현관직제학, 이조판서 등을 역임한 문신.
    '김약연': {'role': 'other'},  # 근대 - 일제강점기 때, 만주에 서전의숙, 명동서숙, 명동여학교 등을 설립하였으며, 간민회 회장 등을 역임한 교육자 · 독립운동가.
    '김약온': {'role': 'other'},  # 고려 - 고려 전기에, 검교사도 수사공 상주국, 문하시중 등을 역임한 문신.
    '김약진': {'role': 'other'},  # 고려/고려 후기 - 고려 후기 최충헌 등이 이의민을 제거할 때 공로를 세워 최충헌 정권에서 출세한 무신.
    '김약채': {'role': 'other'},  # 조선 - 조선 전기에, 대사헌, 충청도관찰사 등을 역임한 문신.
    '김약필': {'role': 'other foreigner'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 사찬으로서 일본에 파견된 사신.
    '김약항': {'role': 'other'},  # 고려 - 조선 전기에, 사헌집의, 판전교시사 등을 역임한 문신.
    '김양': {'role': 'other'},  # 고려 - 고려 전기에, 좌승선, 추밀원부사, 예부상서 등을 역임한 문신.
    '김양감': {'role': 'other'},  # 고려 - 고려 전기에, 판상서호부사, 수태위, 문하시랑 등을 역임한 문신.
    '김양검': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 대호군 등을 역임하였으며, 신돈 일파로 몰려 처형된 무신 · 공신.
    '김양경': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 개성부유수, 대사헌, 공조판서 등을 역임한 문신.
    '김양근': {'role': 'other'},  # 조선 - 조선 후기에, 현풍현감, 음죽현감, 형조참의 등을 역임한 문신.
    '김양기': {'role': 'scholar'},  # 조선/조선 후기 - 조선후기 「송하모정도」 · 「추경산수도」 · 「화조도」 등의 작품을 그린 화가.
    '김양도': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 나당연합군의 사비성 함락 당시의 장수. 문장가.
    '김양림': {'role': 'other foreigner'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 사찬 박강국 · 김충선 등과 일본에 사신으로 파견된 왕자.
    '김양선': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 평동중학교 교장, 기독교박물관관장 등을 역임한 목사. 고고학자.
    '김양수': {'role': 'other foreigner'},  # 근대 - 일제강점기 때, 미국에서 삼일신보 주필로 활동하였으며, 조선어학회에 참여하여 사전편찬을 재정적으로 지원한 정치인 · 독립운동가.
    '김양순': {'role': 'other'},  # 조선 - 조선 후기에, 대사헌, 이조판서 등을 역임한 문신.
    '김양신': {'role': 'other'},  # 조선/조선 후기 - 조선후기 도화서 교수를 역임한 화가.
    '김양언': {'role': 'other'},  # 조선 - 조선 후기에, 이괄의 난을 진압하여 녹훈되었으나, 정묘호란 때 전사한 무신 · 공신.
    '김양연': {'role': 'other'},  # 조선 - 조선 후기에, 사헌부장령, 홍문관교리, 남포현감 등을 역임한 문신.
    '김양영': {'role': 'other'},  # 고려 - 고려 후기에, 사문박사 등을 역임한 문신.
    '김양원': {'role': 'other foreigner'},  # 고대/남북국/통일신라 - 남북국시대 통일신라에서 한나마로서 일본에 파견된 사신.
    '김양종': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 파진찬으로 집사부시중을 역임한 관리.
    '김양지': {'role': 'other'},  # 고려 - 고려 전기에, 급사중, 어사대부, 상서우복야 등을 역임한 문신.
    '김양진': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 형조참의, 대사간, 예조참의 등을 역임한 문신.
    '김양택': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 정조의 원손사부(元孫師傅)이며 대제학, 영의정을 역임한 문신.
    '김양품': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 각간 관등의 귀족.
    '김양행': {'role': 'scholar'},  # 조선 - 조선후기 직제학, 이조참의, 형조참판 등을 역임한 문신. 학자.
    '김양홍': {'role': 'other'},  # 근대 - 일제강점기 우리나라 최초의 교구장을 역임한 신부.
    '김어진': {'role': 'other'},  # 고려 - 고려후기 안주군민부만호를 역임한 무신.
    '김억': {'role': 'poet critic'},  # 근대/일제강점기 - 일제강점기 때, 『해파리의 노래』, 『금모래』, 『봄의 노래』 등을 저술한 시인 · 문학평론가 · 친일반민족행위자.
    '김억렴': {'role': 'other'},  # 고대/남북국/통일신라 - 통일신라의 제56대 경순왕의 큰아버지로, 지대야군사 등을 역임하였으며, 딸을 고려의 태조 왕건과 혼인시킨 종실.
    '김억추': {'role': 'other'},  # 조선 - 조선시대 전라수군절도사, 제주목사 등을 역임한 무신.
    '김언': {'role': 'other'},  # 조선 - 조선 후기에, 장악원정, 영천군수, 성천부사 등을 역임한 문신.
    '김언건': {'role': 'scholar'},  # 조선 - 조선 전기에, 『운정유집』 등을 저술한 문신.
    '김언경': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 보림사보조선사창성탑비를 쓴 관리. 서예가.
    '김언공': {'role': 'other'},  # 조선 - 조선시대 순천부사, 고령진첨절제사, 혜산진첨절제사 등을 역임한 무신.
    '김언기': {'role': 'scholar'},  # 조선 - 조선 전기에, 『유일재집』 등을 저술하였으며, 안동지역의 학문 진흥을 이끈 학자.
    '김언수': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 정묘호란 때 안주성전투에서 순절한 무관.
    '김언평': {'role': 'other'},  # 조선 - 조선 전기에, 감찰, 장령, 강릉대도호부사 등을 역임한 문신.
    '김여': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 대아찬으로 시중을 역임한 관리.
    '김여건': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 정언, 수찬 등을 역임한 문신.
    '김여기': {'role': 'other'},  # 조선 - 조선후기 청성진첨절제사, 벽동군수, 선사포첨절제사 등을 역임한 무신.
    '김여란': {'role': 'other'},  # 현대/대한민국 - 해방 이후 판소리 「춘향가」의 전승자로 지정된 예능보유자.
    '김여량': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 김제군수, 창원부사, 승지 등을 역임한 문신.
    '김여로': {'role': 'other'},  # 조선 - 조선후기 별군직, 자산군수, 덕천군수 등을 역임한 무신.
    '김여물': {'role': 'other'},  # 조선 - 조선 전기에, 충주도사, 담양부사, 의주목사 등을 역임한 문신.
    '김여부': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 전한 등을 역임한 문신.
    '김여생': {'role': 'other'},  # 조선/조선 전기 - 조선  전기 임진왜란 당시 전라도의 의병장.
    '김여석': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 호조참판, 병조참판, 형조판서 등을 역임한 문신.
    '김여옥': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 판결사, 강화유수, 장례원판결사 등을 역임한 문신.
    '김여제': {'role': 'poet'},  # 근대/일제강점기 - 일제강점기 「한끗」, 「잘짜」, 「해에게서 소년에게」 등을 저술한 시인. 교육자.
    '김여준': {'role': 'other'},  # 조선 - 조선후기 김직재의 옥사사건과 관련된 무신.
    '김여지': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 대사헌, 판한성부사, 형조판서 등을 역임한 문신.
    '김역기': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라에서 당나라에 파견된 사신.
    '김연': {'role': 'other'},  # 조선/조선 전기 - 조선 전기 임진왜란 때 영천 출신의 의병장.
    '김연경': {'role': 'other'},  # 고려 - 고려전기 김치양의 난과 관련된 무신.
    '김연광': {'role': 'other'},  # 조선 - 조선 전기에, 부여현감, 평창군수, 회양부사 등을 역임한 문신.
    '김연국': {'role': 'other'},  # 근대/개항기 | 근대/대한제국기 | 근대/일제강점기 - 동학, 천도교, 시천교 지도자로 활약하다가 상제교를 창건한 종교인.
    '김연방': {'role': 'other'},  # 근대/일제강점기 - 일제강점기, 경기도 수원군 우정면에서 일어난 독립만세운동에 참여한 독립운동가.
    '김연수': {'role': 'other'},  # 근대 - 일제강점기부터 1970년대까지, 활동한 판소리 창자이며. 창극 배우 · 각색가 · 작창가.
    '김연실': {'role': 'other'},  # 현대 - 해방 이후 북한에서 「정찰병」, 「처녀 리발사」, 「아름다운 거리」 등에 출연한 배우. 영화배우, 연극배우, 가수.
    '김연조': {'role': 'other'},  # 조선 - 조선 후기에, 권지승문원부정자 등을 역임한 문신.
    '김연준': {'role': 'other'},  # 현대/대한민국 - 해방 이후 한양대학교 총장과 이사장을 역임한 교육자. 작곡가.
    '김연지': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 대사헌, 한성부윤, 지중추원사 등을 역임한 문신.
    '김열보': {'role': 'other'},  # 고려 - 고려 후기에, 장작승, 시각문지후, 전주목판관 등을 역임한 문신.
    '김영': {'role': 'scholar'},  # 조선 - 조선후기 「우후산수도」, 「산수십곡병풍」 등의 작품을 그린 화가.
    '김영건': {'role': 'critic scholar'},  # 현대/대한민국 - 해방 이후 「농촌계몽운동에서의 일제안」, 『어록』, 『문화와 평론』 등을 저술한 평론가. 문학평론가, 역사학자.
    '김영견': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 좌부승지, 이조참판, 동지중추부사 등을 역임한 문신.
    '김영고': {'role': 'other'},  # 고려 - 고려 후기에, 흥교도관역사, 합문지후 등을 역임한 문신.
    '김영곤': {'role': 'other'},  # 근대 - 해방 이후 「북청사자놀음」의 전승자로 지정된 예능보유자.
    '김영공': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 각간으로 시중을 역임한 귀족. 대신.
    '김영관': {'role': 'other'},  # 고려 - 고려 전기에, 감수국사 지서경유수사, 수사도 판국자감사 등을 역임한 문신.
    '김영근': {'role': 'poet scholar'},  # 일제강점기 때, 위정척사 사상을 바탕으로 민족운동을 모색하였으며, 저항시인으로 평가되는 학자 · 시인 · 독립운동가.
    '김영기': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 경상남도 합천군 독립만세시위로 체포된 구금자의 석방을 위해 결사대를 조직하여 시위를 전개하다가 ...
    '김영덕': {'role': 'other'},  # 조선/조선 후기 - 조선후기 충청남도관찰사, 경상남도관찰사, 강원도관 등을 역임한 관료. 의사(義士).
    '김영돈': {'role': 'other'},  # 고려 - 고려 후기에, 강릉부녹사, 지공거, 정치도감판사 등을 역임한 문신.
    '김영동': {'role': 'other'},  # 현대/대한민국 - 일제강점기 때, 북간도, 연길, 용정, 연해주 일대에서 독립운동을 전개하였으며 해방 이후, 조선전화사 사장, 국회...
    '김영란': {'role': 'other'},  # 근대 - 일제강점기 때, 비밀결사 숭의단과 공성단 등을 조직하여 군자금 모금 및 친일파 처단 활동을 전개한 독립운동가.
    '김영랑': {'role': 'poet'},  # 근대/일제강점기 - 일제강점기 「동백잎에 빛나는 마음」 · 「언덕에 바로 누워」 · 「독을 차고」 등을 저술한 시인.
    '김영렬': {'role': 'other'},  # 근대 - 일제강점기 때, 독립단에서 주재소와 면사무소를 습격하는 등 항일무장투쟁을 전개한 독립운동가.
    '김영로': {'role': 'other'},  # 조선 - 조선 전기에, 거산찰방, 수성찰방, 고산찰방 등을 역임한 문신.
    '김영리': {'role': 'other'},  # 고려 - 고려 후기에, 존무사, 좌사의대부 등을 역임한 문신.
    '김영만': {'role': 'other'},  # 근대 - 일제강점기 사회주의자동맹 집행위원, 조선공산당재건설준비위원회 선전부 간부 등을 역임한 사회주의운동가. 독립운동가.
    '김영면': {'role': 'scholar'},  # 조선/조선 후기 - 조선후기 「행려도」, 「강촌추사도」 등의 작품을 그린 화가.
    '김영목': {'role': 'other'},  # 근대 - 조선 후기에, 장례원경, 홍문관학사, 궁내부특진관 등을 역임한 문신.
    '김영배': {'role': 'other'},  # 근대 - 일제강점기, 황해도 참여관 겸 산업 부장, 전라남도 참여관 겸 산업 부장 등을 역임한 관료 · 친일반민족행위자.
    '김영백': {'role': 'other'},  # 근대/개항기 - 대한제국기 전라남도 장성군 출신의 평민 의병장.
    '김영보': {'role': 'playwright novelist'},  # 근대/일제강점기 - 일제강점기 「나의 세계로」 · 「연의 물결」 · 「구리십자가」 등의 작품을 낸 극작가. 언론인.
    '김영부': {'role': 'other'},  # 고려 - 고려 전기에, 참지정사 판상서병부사, 중서시랑, 중서평장사 등을 역임한 문신.
    '김영삼': {'role': 'other'},  # 현대/대한민국 - 대한민국의 제14대 대통령을 지낸 정치인.
    '김영상': {'role': 'scholar foreigner'},  # 근대/일제강점기 - 조선 후기 일본 왕의 노인 은사금을 거절하여 수감 중 단식하여 순국한 유학자이자 독립운동가.
    '김영서': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 대구3·1운동을 주도하여 옥고를 치른 독립유공자.
    '김영석': {'role': 'novelist critic'},  # 근대 - 해방 이후 「지하로 뚫린 길」, 「격랑」 등을 저술한 작가. 소설가, 평론가.
    '김영선': {'role': 'other foreigner'},  # 근대/일제강점기 - 대한제국기 1907년 신민회(新民會) 조직에 참여하고, 일제강점기 1919년 4월 중국 상하이 대한민국임시정부 ...
    '김영섭': {'role': 'other'},  # 근대 - 해방 이후 하와이 총영사, 서울 중앙교회 목사 등을 역임한 목사.
    '김영성': {'role': 'other'},  # 근대/대한제국기 - 대한제국기 때, 의병을 모집하며 항일의병활동을 전개하였고, 전남 여수의 돌산전투에 참전한 의병장.
    '김영소': {'role': 'other'},  # 고려/고려 전기 - 고려시대 수좌, 승통, 대선의 도청 등을 역임한 승려.
    '김영수': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「판소리 고법」 전승자로 지정된 예능보유자. 고수.
    '김영숙': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 대종교 총본사 서무부장, 대형 등을 역임하며 대종교를 통한 항일투쟁을 전개한 대종교인 · 독립운동가.
    '김영순': {'role': 'other'},  # 조선 - 조선 후기에, 대사헌, 형조판서, 이조판서 등을 역임한 문신.
    '김영식': {'role': 'other'},  # 근대 - 일제강점기 신간회 목포지회 대의원, 조선공산당 재건설준비위원회 정치부위원 등을 역임한 사회주의운동가.
    '김영약': {'role': 'other'},  # 고려 - 고려 전기에, 우사간 등을 역임한 문신.
    '김영옥': {'role': 'other foreigner'},  # 현대/대한민국 - 한국계 미국인 2세로, 미국 육군 대령 출신의 군인.
    '김영완': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 전라북도 고창의 독립만세시위를 주도한 혐의로 체포되어 옥중에서 순국한 독립운동가.
    '김영원': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 전라북도 임실의 독립만세시위를 주도한 혐의로 체포되어 옥중에서 순국한 독립운동가.
    '김영유': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 행첨지중추부사, 수지중추부사, 동지중추부사 등을 역임한 문신.
    '김영윤': {'role': 'scholar'},  # 근대 - 해방 이후 『가야금교본』을 저술한 가야금명인.
    '김영의': {'role': 'other'},  # 현대/대한민국 - 해방 이후 이화여자대학교 이사장, 문교부 교육과정음악분과위원장 등을 역임한 교육자. 피아노연주자.
    '김영일': {'role': 'childrenauthor novelist'},  # 현대 - 해방 이후 한국문인협회 아동문학분과위원장, 한국아동문학회 회장 등을 역임한 아동문학가.
    '김영작': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 사헌부대사헌, 홍문관제학, 개성부유수 등을 역임한 문신.
    '김영재': {'role': 'other'},  # 근대 - 일제강점기 때, 윤봉길의 의거에 사용할 폭탄을 제작하였으며, 임시정부 주석 경호원, 비서 등을 역임한 독립운동가.
    '김영적': {'role': 'other'},  # 근대 - 조선 후기에, 비서원승, 봉상사제조, 궁내부특진관 등을 역임한 문신.
    '김영전': {'role': 'other'},  # 근대 - 조선 후기에, 봉상사제조, 종묘서제조, 종묘전사 등을 역임한 문신.
    '김영정': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 지돈녕부사, 전라도관찰사 등을 역임한 문신.
    '김영제': {'role': 'other'},  # 근대 - 일제강점기 제3대 아악사장 등을 역임한 국악인. 가야금명인.
    '김영조': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 대사간, 부제학, 이조참판 등을 역임한 문신.
    '김영존': {'role': 'other'},  # 고려 - 고려후기 동지추밀원사, 지추밀원사, 평장사 등을 역임한 무신.
    '김영종의 난': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라에서 귀족 김영종이 일으킨 반란.
    '김영주': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 「검은 태양」 · 「신화시대」 등의 작품을 그린 화가.
    '김영준': {'role': 'other'},  # 현대/대한민국 - 해방 이후 농림부장관, 한국전력사장 등을 역임한 관료. 경제인.
    '김영진': {'role': 'other'},  # 근대 - 조선후기 내장원감독, 군부교육국장, 봉상사제조 등을 역임한 관리.
    '김영찬': {'role': 'other'},  # 현대/대한민국 - 해방 이후 한국은행 수석부총재, 산업은행 총재 등을 역임한 금융인. 관료.
    '김영철': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「줄타기」 전승자로 지정된 예능보유자. 줄타기명인.
    '김영태': {'role': 'poet critic'},  # 현대 - 해방 이후 『유태인이 사는 마을의 겨울』 · 『하늘 바람꽃이 핀다』 등을 저술한 시인. 무용평론가ㆍ서양화가.
    '김영팔': {'role': 'scholar'},  # 근대/일제강점기 - 일제강점기 「미쳐가는 처녀」, 「싸움」, 「그 후의 대학생」 등의 작품을 제작한 연극인.
    '김영하': {'role': 'other'},  # 근대 - 일제강점기 때, 전라남도 나주, 함평 등에서 군자금 모금 활동을 전개한 독립운동가.
    '김영학': {'role': 'other'},  # 근대 - 일제강점기 때, 철원애국단을 조직하여 군자금 모금 활동을 전개한 목사 · 독립운동가.
    '김영한': {'role': 'scholar'},  # 근대 - 대한제국기 때, 용인군수, 양근군수, 비서원승 등을 역임한 문신 · 학자.
    '김영행': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 우사어, 임천군수, 첨지중추부사 등을 역임한 문신.
    '김영현': {'role': 'other foreigner'},  # 근대 - 일제강점기 때, 중국에서 독립군에 가담하여 군자금 모금 활동을 전개한 독립운동가.
    '김영환': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 경상남도 창원의 삼진 만세운동에 참여했다가 순국한 독립운동가.
    '김영후': {'role': 'other'},  # 고려 - 고려 후기에, 좌정승, 우정승, 상락후 등을 역임한 문신.
    '김영훈': {'role': 'scholar'},  # 근대/일제강점기 | 현대 - 대한한의사협회 명예회장, 서울한의과대학 명예학장 등을 역임한 한의학자.
    '김영희': {'role': 'other'},  # 근대 - 일제강점기 때,경기도 안성군 원곡면과 양성면 일대의 독립만세시위에 참여한 독립운동가.
    '김예': {'role': 'other'},  # 고대/남북국/통일신라 - 통일신라의 제46대 문성왕의 사촌동생으로, 창림사 무구정찹 건립에 참여하였으며, 김현 등과 모반을 꾀하다 ...
    '김예몽': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 강원도관찰사, 대사성, 공조판서 등을 역임한 문신.
    '김예영': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 제38대 원성왕의 셋째 아들인 왕자.
    '김예직': {'role': 'other'},  # 조선 - 조선시대 함경도병마절도사, 포도대장, 삼도수군통제사 등을 역임한 무신.
    '김예진': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 때, 일신청년단을 조직하여 군자금 모금, 일본기관 파괴 활동 등을 전개한 독립운동가.
    '김예징': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 때, 민애왕을 타도하고 신무왕으로 즉위시키는데 공을 세워 상대등을 역임한 통일신라의 귀족 · 관리.
    '김오성': {'role': 'critic'},  # 근대 - 일제강점기 때, 문학, 철학 비평 분야에서 활약하였고, 해방 이후 조선인민당 선전부장, 민주주의민족전선 상임위원 등을 역임...
    '김옥': {'role': 'other'},  # 조선 - 조선 후기에, 군수 등을 역임한 문신.
    '김옥균': {'role': 'other'},  # 근대/개항기 - 우리나라 개화운동의 대표적 인물이자 갑신정변의 주모자.
    '김옥길': {'role': 'other'},  # 현대/대한민국 - 해방 이후 이화여자대학교 총장, 문교부장관 등을 역임한 교육자. 여성운동가.
    '김옥심': {'role': 'other'},  # 현대/대한민국 - 해방 이후 활동한 대표적인 경기민요 명창.
    '김옥주': {'role': 'other'},  # 현대/대한민국 - 제헌국회의원을 역임하였으며, 국회프락치사건으로 복역하다가 한국전쟁 때 납북되어 북한에서, 재북평화통일촉진협의회 간...
    '김온': {'role': 'other'},  # 고려 - 고려 후기에, 충숙왕과 대립하던 심양왕 왕고를 돕다가 세력을 잃고 유배된 관리.
    '김온주': {'role': 'other'},  # 고려 - 고려 후기에, 고애사, 좌간의대부 중군병마부사 등을 역임한 문신.
    '김옹': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 이찬으로 시중, 상상, 병부령 등을 지낸 관리.
    '김완': {'role': 'other'},  # 조선 - 조선 후기에, 소파아권관 겸 단련사, 선전관, 내금위장 등을 역임한 무신 · 공신.
    '김완규': {'role': 'other'},  # 근대/일제강점기 - 천도교를 대표한 민족 대표 33인의 한 사람으로 「3·1독립선언서」에 서명한 독립운동가.
    '김완손': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「양주별산대놀이」 해금의 전승자로 지정된 예능보유자.
    '김완수': {'role': 'other'},  # 근대 - 조선 후기에, 궁내부특진관, 봉상사제조, 예식원장례경 등을 역임한 문신.
    '김완자티무르': {'role': 'other foreigner'},  # 고려/고려 후기 - 고려 후기 중국 원나라의 예부상서를 역임한 고려인 출신의 환관.
    '김왕': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 양산도사, 충청도사, 함평현감 등을 역임한 문신.
    '김요립': {'role': 'other'},  # 조선 - 조선 전기에, 사성, 상의원정, 종부시정 등을 역임한 문신.
    '김요섭': {'role': 'poet childrenauthor'},  # 현대/대한민국 - 해방 이후 『체중』, 『달과 기계』, 『얼굴이 없는 얼굴』 등을 저술한 시인. 아동문학가.
    '김요의 난': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 때, 이찬 관등으로 한주에서 반란을 일으킨 통일신라의 왕족.
    '김용': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 소판으로 당나라에 파견된 관리.
    '김용겸': {'role': 'other'},  # 조선 - 조선 후기에, 우승지, 동지돈녕부사를 등을 역임한 문신.
    '김용경': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 승지, 개성부유수 등을 역임한 문신.
    '김용관': {'role': 'scholar'},  # 해방 이후 『치과 마취학』, 『구강 외과학』 등을 저술한 학자. 치의학자.
    '김용구': {'role': 'other'},  # 근대/대한제국기 - 대한제국기 때, 호남창의회맹소에서 도통령으로 활약한 의병장.
    '김용규': {'role': 'other'},  # 근대 - 조선 후기에, 궁내부특진관, 봉상사제조, 장례원부경 등을 역임한 문신.
    '김용근': {'role': 'other'},  # 근대 - 해방 이후 정읍에서 초산국악원을 개설한 거문고명인.
    '김용기': {'role': 'other'},  # 현대/대한민국 - 광복 이후, 기독교 농촌 지도자 교육에 힘쓴 개신교인.
    '김용대': {'role': 'other'},  # 근대 - 일제강점기 때, 대한독립단 비서, 대한광정단 국법과장, 정의부 중앙행정위원 등을 역임한 독립운동가.
    '김용덕': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 「국사개설」, 「한국제도사연구」, 「신학국사의 탐국」 등을 저술한 학자. 역사학자.
    '김용래': {'role': 'other'},  # 현대/대한민국 - 해방 이후 서울시장, 총무처장관, 경기도지사 등을 역임한 관료.
    '김용만': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「해뜨는소리」 · 「대마루 댓바람」 · 「우헌도곡」 등을 만든 작곡가. 지휘자.
    '김용무': {'role': 'other'},  # 현대/대한민국 - 해방 이후 대법원장, 제2대 국회의원 등을 역임한 법조인. 정치인.
    '김용배': {'role': 'other'},  # 현대/대한민국 - 한국전쟁 당시 강원도 양구의 토평리지구전투에 참전한 군인.
    '김용성': {'role': 'other foreigner'},  # 근대 - 일제강점기 때, 미국에서 재미한족연합회 집행부위원, 임시정부 주미외교위원부 외교위원장 등을 역임한 의사 · 독립운동가.
    '김용수': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 「효귀」 · 「월야」 · 「선경」 등을 그린 화가. 수묵채색화가.
    '김용순': {'role': 'other'},  # 현대/대한민국 - 5·16군사정변에 가담하였으며, 경남지구 계엄사령관, 육군 군수기지사령부 사령관, 중앙정보부장, 국회의원 등을 역...
    '김용식': {'role': 'other'},  # 현대 - 한국전쟁 당시 경북 포항의 비학산전투에 참전한 군인.
    '김용언': {'role': 'scholar'},  # 조선 - 조선 후기에, 『송계유고』 등을 저술한 학자.
    '김용옥': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 『고린도전서』, 『신약개론』, 『데살로니가 전후서』 등을 저술한 신학자. 목사.
    '김용완': {'role': 'other'},  # 현대 - 해방 이후 경방주식회사 명예회장, 전국경제인연합회 회장 등을 역임한 기업인.
    '김용우': {'role': 'other'},  # 현대/대한민국 - 해방 이후 국방부장관, 민주공화당 정책위 의장, 대한올림픽위원회 위원장 등을 역임한 정치인. 체육인.
    '김용욱': {'role': 'other'},  # 근대/대한제국기 - 대한제국기 때, 신돌석 의진에서 중군장으로 활동하며 항일의병투쟁을 전개한 의병장.
    '김용원': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 대동단에서 활동하며 의친왕 망명 계획에 참여하였고, 임시정부 의정원 의원 등을 역임하고 군자금 ...
    '김용이': {'role': 'other'},  # 근대 - 일제강점기 때, 충청북도 옥천의 독립만세시위에 참여한 독립운동가.
    '김용익': {'role': 'other'},  # 현대 - 해방 이후 「봉산탈춤」의 전승자로 지정된 예능보유자.
    '김용재': {'role': 'other'},  # 고려/고려 후기 - 1258년(고종 45), 무오정변(戊午政變)에 참여하여 위사보좌공신(衛社輔佐功臣)에 이어 위사공신(衛社功臣)에 ...
    '김용제': {'role': 'poet critic'},  # 근대/일제강점기 - 일제강점기 「압록강」 · 「사랑하는 대륙이여」 등을 저술한 시인. 비평가 · 친일반민족행위자.
    '김용조': {'role': 'scholar'},  # 근대/일제강점기 - 일제강점기 「어머니의 상」, 「어선」, 「해경」 등의 작품을 그린 화가.
    '김용주': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 한국광복군에 입대하여 제2지대 총무조원 겸 공작조원으로 활동하였으며, 1945년 독수리작전의 국내 정...
    '김용준': {'role': 'scholar'},  # 근대/일제강점기 | 현대 - 북한에서 평양미술대학 교수 등을 역임하였으며, 『조선미술대요』 등을 저술한 화가 · 미술인.
    '김용중': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 때, 미국으로 이주하여 대한인국민회, 재미한족연합위원회 등에서 활동하였고, 영자지 『한국의 소리(Th...
    '김용진': {'role': 'other'},  # 근대 - 일제강점기 때, 신민회 운영위원으로 활동하였으며, 황해도에서 임시정부 연통제를 조직하여 군자금 모금 활동 등을 전개한 독립...
    '김용찬': {'role': 'scholar'},  # 조선 - 조선 후기에, 『경독재집』 등을 저술한 학자.
    '김용춘': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라 제25대 진지왕의 아들인 왕자.
    '김용태': {'role': 'other'},  # 현대/대한민국 - 5·16군사정변의 핵심 인물로, 국가재건최고회의 경제고문 등을 역임하였으며, 민주공화당의 주류인 김종필계의 대표적...
    '김용택': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 이이명의 천거로 벼슬길에 올랐으나, 이이명 추대 세력에 대한 목호룡의 고변으로 인해 처형된 문신.
    '김용하': {'role': 'other'},  # 현대 - 한국전쟁 당시 경북 문경의 이화령전투에 참전한 군인.
    '김용한': {'role': 'other'},  # 현대 - 해방 이후 물가정책국장, 과학기술처 차관 등을 역임한 관료.
    '김용행': {'role': 'scholar'},  # 고대/삼국/신라 - 삼국시대 신라의 대나마로「아도화상비」를 저술한 문장가.
    '김용현': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「강릉농악」 전승자로 지정된 예능보유자. 농악인.
    '김용호': {'role': 'poet'},  # 근대/일제강점기 - 일제강점기 『향연』 · 『해마다 피는 꽃』 등을 저술한 시인.
    '김용환': {'role': 'other'},  # 현대/대한민국 - 박정희 경제개발기에, 재무부와 농림부, 대통령비서실의 관료로서 경제개발에 투자 재원을 마련하며 경제위기를 수습한 인물.
    '김용휘': {'role': 'other'},  # 고려 - 고려후기 도안무사 겸 부원수, 서북면도순찰사 등을 역임한 무신.
    '김우': {'role': 'other'},  # 근대 - 대한제국기 때, 전남 장성에서 의병을 일으켜 200정의 총으로 무장한 부대를 이끈 의병장.
    '김우굉': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 대사간, 대사성, 승지 등을 역임한 문신.
    '김우규': {'role': 'scholar'},  # 조선/조선 후기 - 조선후기 『청구가요』 등에 주요 작품이 실려 있는 가객.
    '김우근': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 참의부 경무원, 조선혁명단 지방책임위원, 한중연합토일군 참모 등을 역임한 독립운동가.
    '김우명': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 영돈녕부사, 오위도총관, 호위대장 등을 역임한 문신.
    '김우문': {'role': 'other'},  # 고려/고려 후기 - 고려후기 수월관음도 제작을 주도한 화가.
    '김우번': {'role': 'other'},  # 고려 - 고려 전기에, 지제고, 동지공거, 판예빈성사 등을 역임한 문신.
    '김우범': {'role': 'novelist'},  # 근대/개항기 | 근대/일제강점기 - 일제강점기 「우후산수」 · 「난」 · 「매」 등을 그린 화가. 문인화가.
    '김우생': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 순천부사, 승지 등을 역임한 문신.
    '김우석': {'role': 'other'},  # 조선 - 조선 후기에, 개성유수, 한성부판윤, 형조판서 등을 역임한 문신.
    '김우식': {'role': 'other'},  # 현대/대한민국 - 한국민주당 경상북도 감찰위원장, 제헌국회의원 등을 역임하다가 한국전쟁 때 납북되어 북한에서, 평화통일위원회 중앙위...
    '김우신': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 대호군, 호조참의, 첨지중추부사 등을 역임한 문신.
    '김우옹': {'role': 'scholar'},  # 조선 - 조선시대 병조참판, 예조참판, 이조참판 등을 역임한 문신. 학자.
    '김우윤': {'role': 'other'},  # 조선 - 조선 중기에, 문한관, 공조좌랑 등을 역임한 문신.
    '김우전': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 일본군 학병으로 동원되었으나, 중국에서 탈출한 후 한국광복군에 입대하여 활동한 독립운동가.
    '김우중': {'role': 'other'},  # 현대/대한민국 - 1967년, 섬유수출업체 대우실업 창업 이래 단기간에 국내 굴지의 재벌 대우그룹을 만들어 낸 기업가.
    '김우진': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 1919년 3월 서울 3·1운동에 참가한 뒤 중국 상하이로 망명하여 대한민국임시정부 임시의정원 의원 ...
    '김우창': {'role': 'scholar'},  # 조선 - 개항기 때, 영주지방의 의병대장으로 활약하였으며, 『기사』, 『예설간요』 등을 저술한 학자 · 의병장.
    '김우철': {'role': 'critic'},  # 근대/일제강점기 - 일제강점기 「아동문학에 관하야」, 「낭만적 인간탐조」 등을 저술한 평론가.
    '김우평': {'role': 'other'},  # 근대/일제강점기|현대 - 일제강점기 때, 동아일보 기자, 친일조직인 만주국 협화회 조선인민회 분회 상임감사 등을 역임하였으며 해방 ...
    '김우항': {'role': 'other'},  # 조선 - 조선 후기에, 이조참판, 대사성, 이조판서, 우의정 등을 역임한 문신.
    '김우현': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 공조참의, 우부승지, 경흥도호부사 등을 역임한 문신.
    '김우형': {'role': 'other'},  # 조선 - 조선 후기에, 한성부판윤, 개성유수, 형조판서 등을 역임한 문신.
    '김우화': {'role': 'other'},  # 조선 - 조선 후기에, 황감별제, 전적, 봉상시정 등을 역임한 문신.
    '김운': {'role': 'other'},  # 고려 - 고려 후기에, 지첨의부사, 첨의참리, 도첨의참리 등을 역임한 문신.
    '김운경': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 선위부사를 역임한 관리.
    '김운공': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「영산재」 전승자로 지정된 예능보유자. 범패승.
    '김운서': {'role': 'other'},  # 근대/대한제국기 - 대한제국기 때, 이석용 의진에서 중군장으로 활약하였으며, 국권 피탈 이후 군자금 모금 활동을 전개한 의병 · 독...
    '김운택': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 평안도감진어사, 부제학, 호조참판, 형조참판 등을 역임하였으나, 목호룡의 고변으로 반역을 도모한다...
    '김운파': {'role': 'other'},  # 현대/대한민국 - 해방 이후 봉원사 주지를 역임한 승려.
    '김운학': {'role': 'critic scholar'},  # 현대/대한민국 - 해방 이후 『신라불교문학연구』, 『향가에 나타난 불교사상』 등을 저술한 승려. 불교학자, 평론가.
    '김울산': {'role': 'other'},  # 근대 - 일제강점기 순도학교, 복명학교, 희도국민학교 등을 설립한 여성 육영사업가.
    '김웅권': {'role': 'other'},  # 현대/대한민국 - 조선민족청년당 이사와 총무부장, 제헌국회의원, 국회 외무국방위원회 국방분과위원 등을 역임한 정치인.
    '김웅렴': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 국상으로 고려에 원병을 요청하러 파견된 관리.
    '김웅원': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 김헌창의 난 당시의 장수.
    '김웅진': {'role': 'other'},  # 현대/대한민국 - 국회의원, 반민족행위특별조사위원회 검찰관 등을 역임하다가 한국전쟁 때 납북되어 북한에서, 평화통일협의회 중앙위원을...
    '김원': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 「38선」 · 「설악산」 · 「한강」 등의 작품을 그린 화가.
    '김원구': {'role': 'other'},  # 고려 - 고려 후기에, 전법총랑 등을 역임한 문신.
    '김원국': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 중국 운남군관학교를 졸업한 후 만주로 건너가 정의부에서 무장투쟁을 전개한 독립운동가.
    '김원규': {'role': 'other'},  # 현대/대한민국 - 해방 이후 경기중고등학교 교장, 서울사범학교 교장, 서울특별시 교육감 등을 역임한 교육자.
    '김원균': {'role': 'other'},  # 현대 - 해방 이후 북한에서 조선음악가동맹 중앙위원장, 조선민족음악위원장 등을 역임한 작곡가.
    '김원근': {'role': 'scholar'},  # 근대/개항기 | 근대/일제강점기 - 일제강점기 정신여학교 교사를 역임한 교육자. 한학자.
    '김원길': {'role': 'other'},  # 근대 - 해방 이후 국극단, 국악사 등에서 활동한 창극명인. 판소리명창.
    '김원량': {'role': 'other'},  # 조선 - 조선 후기에, 장례원사평, 공조좌랑, 지평 등을 역임한 문신 · 공신.
    '김원록': {'role': 'other'},  # 조선 - 조선 후기에, 병조좌랑, 돈녕도정, 동지돈녕부사 등을 역임한 문신.
    '김원룡': {'role': 'scholar novelist'},  # 현대/대한민국 - 서울대학교 고고미술사학과 교수, 한국고고학연구회 회장 등을 역임하였으며, 『신라토기의 연구』, 『한국미술사연구』 ...
    '김원립': {'role': 'other'},  # 조선 - 조선 후기에, 부안현감, 능주목사, 종성부사 등을 역임한 문신.
    '김원만': {'role': 'other'},  # 현대 - 제4·5대 민의원, 내무부차관, 제7·8·9대 국회의원 등을 역임한 정치인.
    '김원망': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 장군 김유신의 다섯째 아들로 대아찬을 역임한 관리.
    '김원명': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 감찰집의, 판도판서 등을 역임한 문신 · 공신.
    '김원범': {'role': 'other'},  # 근대 - 대한제국기 때, 형 김원국과 함께 의병을 일으켰으며, 대동창의단을 조직하여 중군장으로 활약한 의병.
    '김원벽': {'role': 'other'},  # 근대/일제강점기 - 1919년 3월 1일과 3월 5일 경성(지금의 서울특별시)에서 학생 만세 시위를 이끈 독립운동가.
    '김원복': {'role': 'other'},  # 해방 이후 서울대학교 음악대학교 교수를 역임한 교육자. 피아노연주자.
    '김원봉': {'role': 'other'},  # 일제강점기 때, 임시정부 군무부장, 광복군 부사령관 등을 역임하였고, 의열단과 조선의용대를 이끌며 항일무장투쟁을 전개한 정치인 · ...
    '김원상': {'role': 'other'},  # 고려/고려 후기 - 고려 후기 충렬왕~충혜왕대에 활동한 문신이자 간신.
    '김원섭': {'role': 'other'},  # 조선 - 조선 후기에, 사헌부 · 사간원 · 홍문관의 청요직, 대사간 등을 역임한 문신.
    '김원술': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 석문전투에 참전한 장수.
    '김원식': {'role': 'other'},  # 근대/개항기 - 1907년 강원도 금강산 일대에서 의병을 일으킨 의병장.
    '김원영': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 중국 공군기지 중미혼합단 소속 장교(비행사)로, 웨양 · 헝양 등지에서 일본군 운수부대를 소탕하는 등...
    '김원용': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 때, 미국에서 하와이 대한인국민회 기관지의 주필, 주미 외교위원부 외교위원장 등으로 활동하며 민족운동...
    '김원의': {'role': 'other'},  # 고려 - 고려후기 참지정사 판예부사, 문하시랑평장사 판병부사 등을 역임한 무신.
    '김원전': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 사은사로 당나라에 파견된 관리.
    '김원정': {'role': 'other'},  # 고려 - 고려 전기에, 서경유수사, 수태위문하시중 등을 역임한 문신.
    '김원조': {'role': 'other'},  # 근대 - 일제강점기 때, 대한군정부에서 군자금 모금 활동을 전개한 독립운동가.
    '김원충': {'role': 'other'},  # 고려 - 고려 전기에, 문하시랑평장사 판상서형부사, 수사도 문하시중 등을 역임한 문신.
    '김원태': {'role': 'other'},  # 현대 - 농림부차관, 재무부차관, 대한민국 헌정회 제9대 회장 등을 정치인 · 기업가.
    '김원필': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 집사부시랑을 역임한 관리.
    '김원행': {'role': 'scholar'},  # 조선 - 조선후기 종부시주부, 공조참의, 사성 등을 역임한 문신. 학자.
    '김원현': {'role': 'other'},  # 남북국시대 통일신라의 대신으로 당나라에 파견된 관리.
    '김원황': {'role': 'other'},  # 고려 - 고려 전기에, 중추원사, 중추원사 병부상서 등을 역임한 문신.
    '김원훈': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 아찬으로 중시를 역임한 귀족. 대신.
    '김월하': {'role': 'other'},  # 현대/대한민국 - 해방 이후 여창가곡의 전승자로 지정된 예능보유자.
    '김위': {'role': 'scholar'},  # 조선 - 조선후기 이조좌랑, 지평 등을 역임한 문신. 학자.
    '김위남': {'role': 'other'},  # 조선 - 조선 후기에, 공조좌랑, 병조좌랑, 통례 등을 역임한 문신.
    '김위량': {'role': 'other'},  # 고려 - 고려 후기에, 낭장, 장군 등을 역임한 무신 · 공신.
    '김위문': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 때, 신라 원성왕의 조부로, 중시 등을 역임한 통일신라의 귀족 · 관리.
    '김위제': {'role': 'other'},  # 고려 - 고려전기 위위승동정, 주부동정 등을 역임한 관리.
    '김위홍': {'role': 'other'},  # 고대/남북국/통일신라 - 통일신라의 제48대 신라 경문왕의 동생으로, 각간, 상대등, 병부령 등을 역임한 통일신라의 왕족.
    '김유': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 찬수낭관, 대제학 등을 역임한 문신.
    '김유감': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「서울새남굿」의 전승자로 지정된 예능보유자.
    '김유경': {'role': 'other'},  # 조선 - 조선 후기에, 사헌, 형조참판, 좌참찬 등을 역임한 문신.
    '김유규': {'role': 'other'},  # 고려/고려 전기 - 고려 전기에, 대관령, 공역령, 상식직장 등을 역임한 문신.
    '김유근': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 병조판서, 이조판서, 판돈녕부사 등을 역임한 문신.
    '김유기': {'role': 'other'},  # 조선/조선 후기 - 조선후기 여항육인의 한 사람으로 태평성대의 평안한 삶을 노래한 음악인.
    '김유길': {'role': 'other foreigner'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 일길찬으로서 일본에 파견된 사신.
    '김유돈': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 대아찬으로서 웅진도독부에 파견된 관리.
    '김유렴': {'role': 'other'},  # 고대/남북국/통일신라 - 통일신라의 제56대 경순왕의 사촌동생으로, 대아찬에 임명되었으며, 시중 등을 역임한 종실.
    '김유립': {'role': 'other'},  # 고려 - 고려 전기에, 명주도감창전중내급사 등을 역임한 문신.
    '김유방': {'role': 'novelist'},  # 근대/일제강점기 - 일제강점기 때, 김동인 등과 함께 우리나라 최초의 순수문예동인지 『창조』를 창간하였으며, 「배교자」, 「삼천오백...
    '김유성': {'role': 'other'},  # 근대 - 조선 후기에, 중추원 일등의관, 궁내부특진관, 규장각전제관 등을 역임한 문신.
    '김유순': {'role': 'other'},  # 근대 - 일제강점기 평양 남산현교회, 서울 만리현교회 등에서 목회 활동을 한 목사.
    '김유신': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 1938년 한국청년전지공작대를 거쳐 한국광복군에서 활동한 독립운동가.
    '김유연': {'role': 'other'},  # 조선 - 조선 후기에, 이조판서, 우의정, 판중추부사 등을 역임한 문신.
    '김유영': {'role': 'scholar'},  # 근대 - 일제강점기 「유랑」, 「애련송」, 「수선화」 등의 작품에 관여한 영화인. 영화감독.
    '김유정': {'role': 'novelist'},  # 일제강점기 『동백꽃』, 「봄봄」, 「따라지」 등을 저술한 소설가.
    '김유지': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 『의방유취』 편찬에 참여한 의관 · 공신.
    '김유철': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 1930년 남화한인청년연맹에 가입하여 무정부주의 독립운동을 시작하여 한국청년전지공작대를 거쳐 한국광복...
    '김유탁': {'role': 'other'},  # 근대/개항기 | 근대/일제강점기 - 일제강점기 때, 「화조사군자」, 「조안도」 등을 그린 서화가.
    '김유택': {'role': 'other'},  # 현대 - 한국은행 총재, 주일대사, 재무부장관 등을 역임한 은행가 · 외교관 · 정치인.
    '김유하': {'role': 'other'},  # 근대 - 해방 이후 문교부 체육과 장학위원, 올림픽위원회 위원 등을 역임한 체육인.
    '김유행': {'role': 'other'},  # 근대 - 조선 후기에, 대사간, 협판내무부사, 이조참의 등을 역임한 문신.
    '김육': {'role': 'scholar'},  # 조선/조선 후기 - 조선 후기에 형조참의 · 병조참판 · 우의정 · 좌의정 · 영의정 등을 역임하였으며, 『구황촬요』 · 『종덕신편...
    '김육진': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 경주 무장사 아미타여래조상사적비의 비문을 쓴 서예가.
    '김윤': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 제48대 경문왕의 넷째 아들인 왕자.
    '김윤겸': {'role': 'scholar'},  # 조선/조선 후기 - 조선후기 「동산계정도」 · 「금강산화첩」 · 「영남명승기행사경첩」 등의 작품을 그린 화가.
    '김윤경': {'role': 'scholar'},  # 근대 | 현대 - 『조선문자급어학사』, 『나라말본』, 『중등말본』 등을 저술한 국어학자.
    '김윤구': {'role': 'other'},  # 근대/개항기 | 근대/일제강점기 - 일제강점기 창덕궁 대조전 등을 신축한 건축가.
    '김윤기': {'role': 'other'},  # 근대/일제강점기|현대 - 교통부장관, 건설부장관 등을 역임한 건축가 · 관료.
    '김윤덕': {'role': 'other'},  # 현대/대한민국 - 해방 이후 가야금산조 및 병창의 전승자로 지정된 예능보유자.
    '김윤면': {'role': 'other'},  # 근대/개항기 - 개항기 동양물산 사장을 역임한 실업가.
    '김윤명': {'role': 'scholar'},  # 조선 - 조선시대 호조참의, 의금부도사, 오위도총부부총관 등을 역임한 문신. 학자.
    '김윤문': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 발해 침공 당시의 장수.
    '김윤보': {'role': 'other'},  # 근대/개항기 | 근대/일제강점기 - 개항기 「산수도」, 「쌍마인물도」, 「설중방우도」 등을 그린 화가.
    '김윤부': {'role': 'scholar'},  # 고대/남북국/통일신라 - 남북국시대 때, 숙위학생으로 당나라에서 유학하여 빈공과에 급제한 통일신라의 학자.
    '김윤서': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 때, 신한민주당 재정부장, 중국 중앙대학 농과대학 교수 등을 역임한 교육자 · 독립운동가.
    '김윤수': {'role': 'other'},  # 조선 - 조선전기 지중추부사, 충청도처치사 등을 역임한 무신.
    '김윤승': {'role': 'other'},  # 고려/고려 후기 - 고려 후기 권신(權臣) 지윤의 심복이었던 문신.
    '김윤식': {'role': 'scholar'},  # 조선/조선 후기 - 조선후기 황실제도국총재, 강구회 회장, 흥사단 단장 등을 역임한 문신. 학자.
    '김윤신': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 지평, 평안도도사, 안변부사 등을 역임한 문신.
    '김윤안': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 대구부사, 대사간 등을 역임한 문신.
    '김윤은': {'role': 'other'},  # 조선/조선 전기 - 조선시대 사옹원주부, 가선대부 등을 역임한 의관.
    '김윤정': {'role': 'other'},  # 근대 - 일제강점기 국민정신총동원조선연맹 평의원, 국민총력조선연맹 평의원 등을 역임한 관료. 친일반민족행위자.
    '김윤제': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 제사묘직, 군기주부, 금오위녹사참군사 등을 역임한 문신.
    '김윤중': {'role': 'other'},  # 고대/남북국/통일신라 - 신라 중대에 중시(中侍)와 장군으로 활동한 김유신의 손자.
    '김윤충': {'role': 'scholar'},  # 조선 - 조선 전기에, 사마시에 합격하였으나, 벼슬을 지내지 않고 은거하며 문예에 열중한 학자.
    '김윤택': {'role': 'other'},  # 현대 - 해방 이후 「송파산대놀이」 첫 상좌역의 전승자로 지정된 예능보유자.
    '김윤환': {'role': 'other'},  # 현대/대한민국 - 대한민국의 언론인 출신으로, 국회의원, 정무1장관, 민주자유당 사무총장 등을 지낸 정치인.
    '김윤후': {'role': 'other'},  # 고려/고려 후기 - 고려 후기 대몽항쟁 때 처인성과 충주성의 전투에서 크게 활약한 승려 출신 무신.
    '김율': {'role': 'other'},  # 근대 - 대한제국기 때, 호남창의회맹소에 가담하였으며, 신덕순 의진, 유병기 의진 등에서 활동한 의병장.
    '김은': {'role': 'scholar'},  # 조선 - 조선 후기에, 가난한 집안에서 아우와 함께 학문에 전념하였으며, 호조좌랑에 추증된 학자.
    '김은거': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 때, 이찬 관등으로 당나라에 파견되었으며, 시중 등을 역임한 통일신라의 관리.
    '김은배': {'role': 'other'},  # 현대 - 해방 이후 헬싱키올림픽대회 육상감독, 대한체육회 상무이사 등을 역임한 체육인.
    '김은부': {'role': 'other'},  # 고려 - 고려 전기에, 지중추사, 호부상서, 중추사상호군 등을 역임한 문신.
    '김은우': {'role': 'other'},  # 현대/대한민국 - 해방 이후 한국철학회 부회장, 배재학당 재단이사장 등을 역임한 교육자. 언론인.
    '김은하': {'role': 'other'},  # 현대/대한민국 - 인천시의회 의원, 국회의원, 국회부의장, 교통체신위원 등을 역임한 정치인.
    '김은호': {'role': 'other'},  # 현대/대한민국 - 해방 이후 대한변호사협회 회장, 법조원로회 회장 등을 역임한 법조인.
    '김은휘': {'role': 'other'},  # 조선 - 조선 중기에, 통례원상례, 광주목사, 첨지중추부사 등을 역임한 문신.
    '김을한': {'role': 'other'},  # 현대/대한민국 - 해방 이후 서울신문 동경특파원, 서울신문 이사 등을 역임한 언론인.
    '김을현': {'role': 'other'},  # 조선/조선 전기 - 조선전기 인수부윤, 동지중추원사, 중추원부사 등을 역임한 역관.
    '김응근': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 충청도관찰사, 공조판서, 형조판서 등을 역임한 문신.
    '김응기': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 좌의정, 영중추부사 등을 역임한 문신.
    '김응남': {'role': 'other'},  # 조선 - 조선 중기에, 한성판윤, 병조판서 겸 부제찰사 등을 역임한 문신 · 공신.
    '김응덕': {'role': 'other'},  # 고려 - 고려 후기에, 나주사록을 역임하여 삼별초의 난에 대항한 문신.
    '김응락': {'role': 'other'},  # 현대/대한민국 - 일제강점기 안동교회 장로, 베다니전도교회 건축위원 등으로 활동한 개신교인. 육영사업가, 순교자.
    '김응명': {'role': 'other'},  # 조선 - 조선 후기에, 생원이 되었으나, 벼슬에 뜻이 없어 향리에서 학문에 전념한 유생.
    '김응문': {'role': 'other'},  # 고려 - 고려 후기에, 대부윤, 비서소윤, 판삼사사 등을 역임한 문신.
    '김응백': {'role': 'other foreigner'},  # 근대 - 대한제국기 때, 황영문 의진에서 일본인 사살과 군자금 모금 활동을 전개한 의병.
    '김응삼': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 한국광복군 제3징모처 위원으로 선임되어 초모 활동 및 대적 선전 활동을 전개한 독립운동가.
    '김응상': {'role': 'other'},  # 조선/조선 전기 - 조선 전기 종사관과 병마절도사를 역임한 무신.
    '김응생': {'role': 'scholar'},  # 조선 - 조선 전기에, 생원이 되었으나, 벼슬을 지내지 않고 향촌교육에 전념한 학자.
    '김응섭': {'role': 'other'},  # 근대 - 일제강점기 때, 임시정부 법무장관, 조선공산당 만주총국 간부 등을 역임한 법조인 · 독립운동가.
    '김응순': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 한성부좌윤, 호조참판, 한성부우윤 등을 역임한 문신.
    '김응원': {'role': 'other'},  # 근대/일제강점기 - 조선후기 「석란도」를 그린 서화가.
    '김응인': {'role': 'other'},  # 고려 - 고려 전기 강조의 정변 당시에, 강조가 목종을 폐하고 현종을 왕으로 옹립할 수 있도록 도왔으며, 이후 거란의 침입에도 끝까...
    '김응정': {'role': 'novelist'},  # 조선 - 조선 중기에  「서산일락가」 · 『해암문집』 등을 저술한 문인.
    '김응조': {'role': 'other'},  # 현대/대한민국 - 해방 이후 예수교대한성결교회 및 성결대학교 창립자인 목사.
    '김응진': {'role': 'other'},  # 현대 - 해방 이후 「군자란」 · 「향원정」 · 「비원」 등을 그린 화가. 서양화가.
    '김응창': {'role': 'other'},  # 조선 - 조선 후기 임진왜란 때, 선조를 호종한 공으로 녹훈되었으나, 이괄의 난에 연루되어 처형된 환관 · 공신.
    '김응탁': {'role': 'other'},  # 조선/조선 후기 - 조선시대 내의원내의를 역임한 의관.
    '김응태': {'role': 'other'},  # 근대 - 일제강점기, 일제의 종교 정책에 협력한 감리교 목사.
    '김응표': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 「향상회관 뒤에서」, 「정물」, 「A목사의 댁」 등을 그린 화가. 서양화가.
    '김응하': {'role': 'other'},  # 조선 - 조선시대 후금정벌과 관련된 무신.
    '김응해': {'role': 'other'},  # 조선 - 조선시대 정주부사, 별장, 어영대장 등을 역임한 무신.
    '김응환': {'role': 'scholar'},  # 조선/조선 후기 - 조선후기 「금강산화첩」 · 「금강전도」 · 「강안청적도」 등의 작품을 그린 화가.
    '김의': {'role': 'other'},  # 고려/고려 후기 - 고려후기 밀직부사, 동지밀직사사 등을 역임한 무신.
    '김의관': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 신영대왕으로 추봉된 귀족.
    '김의광': {'role': 'other'},  # 고려/고려 후기 - 고려후기 신문색, 장군, 부지밀직사사 등을 역임한 환관. 문신.
    '김의복': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 백수성전투, 석문전투에 참전한 장수.
    '김의영': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라 제38대 원성왕의 둘째 아들인 왕자.
    '김의원': {'role': 'other'},  # 조선 - 조선 중기에, 보덕, 악정, 대사간 등을 역임한 문신.
    '김의정': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 공조좌랑, 훈련원부정, 종부시첨정 등을 역임한 문신.
    '김의종': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라 제42대 흥덕왕의 둘째 아들인 왕자.
    '김의준': {'role': 'other'},  # 현대/대한민국 - 서울고등법원 판사, 국회의원, 국회 법제사법위원장 등을 역임한 법조인 · 정치인.
    '김의진': {'role': 'scholar'},  # 고려 - 고려전기 지공거, 판상서병부사, 평장사 등을 역임한 문신. 학자.
    '김의충': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 시중, 이벌찬 등을 역임한 귀족. 대신.
    '김의택': {'role': 'other'},  # 현대/대한민국 - 충청북도 경찰국장, 신민당 수석부총재, 민권당 총재 등을 역임한 정치인.
    '김의한': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 임시정부 비서, 한국독립당 상무위원, 광복군총사령부 주계 등을 역임한 독립운동가.
    '김의행': {'role': 'poet'},  # 조선/조선 후기 - 조선 후기 교서관 서리를 지낸 경아전 출신으로, 『삼류재유고』를 저술한 여항시인.
    '김이': {'role': 'other'},  # 고려 - 고려 후기에, 사헌집의, 밀직부사, 첨의중찬 등을 역임한 문신.
    '김이건': {'role': 'other'},  # 조선 - 조선 후기에, 참봉, 청도군수, 청주목사 등을 역임한 문신.
    '김이걸': {'role': 'other'},  # 근대 - 일제강점기 때, 친일파 이완용과 이용구의 암살을 계획하였으며, 의용단에서 군자금 모금 활동을 전개한 독립운동가.
    '김이곤': {'role': 'scholar'},  # 조선 - 조선후기 동궁시직, 신계현령 등을 역임한 문신. 학자.
    '김이교': {'role': 'other'},  # 조선 - 조선 후기에, 공조판서, 예조판서, 우의정 등을 역임한 문신.
    '김이구': {'role': 'scholar'},  # 조선 - 조선 후기에, 경학과 예학에 주력하였으며, 호조참판에 추증된 학자.
    '김이도': {'role': 'other'},  # 조선 - 조선 후기에, 대사헌, 수원부유수 등을 역임한 문신.
    '김이련': {'role': 'other'},  # 근대 - 개항기 의주교회 창설에 공헌한 개신교인.
    '김이례': {'role': 'other'},  # 조선 - 조선 후기에, 군수, 첨지중추부사조사오위장 등을 역임한 문신.
    '김이만': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 집의, 통정대부, 첨지중추부사 등을 역임한 문신.
    '김이상': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 통례원통례, 덕천군수, 영원군수 등을 역임한 문신.
    '김이생': {'role': 'other'},  # 고려 - 고려후기 낭장, 자문지유, 상장군 동남도지휘사 등을 역임한 무신.
    '김이석': {'role': 'novelist'},  # 근대 - 해방 이후 「실비명」, 「동면 冬眠」, 「외뿔소」 등을 저술한 작가. 소설가.
    '김이섭': {'role': 'other foreigner'},  # 근대 - 일제강점기 때, 정의부에서 교육 · 선전활동과 군자금 모금, 친일파 처단, 일본관리 사살 등 항일무장투쟁을 전개한 독립운동가.
    '김이소': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 이조참판, 예조판서, 좌의정 등을 역임한 문신.
    '김이안': {'role': 'scholar'},  # 조선 - 조선 후기에, 『의례경전기의』, 『계몽기의』, 『삼산재집』 등을 저술한 문신.
    '김이양': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 홍문관제학, 판의금부사, 좌참찬 등을 역임한 문신.
    '김이어': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 숙위학생으로서 당나라 빈공과에 급제한 관리.
    '김이영': {'role': 'other'},  # 고려/고려 전기 - 고려 전기 의종의 동생 대령후(大寧侯) 왕경(王暻) 유배사건과 관련된 문신.
    '김이원': {'role': 'other'},  # 근대 - 일제강점기 때, 평안북도 의주의 독립만세시위를 주도한 독립운동가.
    '김이음': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 우사간, 강원도관찰사, 호조참판 등을 역임한 문신.
    '김이익': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 형조판서, 한성부판윤, 대호군 등을 역임한 문신.
    '김이재': {'role': 'other'},  # 조선 - 조선 후기에, 상호군, 공조판서, 이조판서 등을 역임한 문신.
    '김이주': {'role': 'other'},  # 조선 - 조선 후기에, 행부사직, 대사헌, 형조판서 등을 역임한 문신.
    '김이직': {'role': 'other'},  # 근대 - 일제강점기 때, 연해주에서 니콜라예프스크재류 한인민단의 초대단장을 역임하여 교육구제사업 및 민족사상 고취에 힘쓴 독립운동가.
    '김이혁': {'role': 'scholar'},  # 조선/조선 후기 - 조선후기 「고산구곡담총도」, 「산수도」 등의 작품을 그린 화가.
    '김이희': {'role': 'other'},  # 조선 - 조선 후기에, 대사간, 동지의금부사, 대사헌 등을 역임한 문신.
    '김익': {'role': 'other'},  # 조선 - 조선 후기에, 판중추부사, 동지사은사, 영의정 등을 역임한 문신.
    '김익겸': {'role': 'other'},  # 조선 - 조선시대 병자호란 때, 강화도에서 항전하여 영의정으로 추증된 문신.
    '김익경': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 대사헌, 이조참의, 예조참판 등을 역임한 문신.
    '김익곤': {'role': 'other'},  # 근대 - 일제강점기 때, 대한독립단과 광복군사령부에서 군자금 모금, 친일파 처단, 일제기관 파괴 등 항일무장투쟁을 전개한 독립운동가.
    '김익기': {'role': 'other'},  # 현대/대한민국 - 국회의원, 국회 사회보건위원장 등을 역임한 정치인.
    '김익노': {'role': 'other'},  # 현대/대한민국 - 국회의원, 국회징계자격위원장 등을 역임하였으며, 발췌개헌, 사사오입 개헌 등 이승만의 정치권력을 강화하는 활동에 ...
    '김익달': {'role': 'other'},  # 현대/대한민국 - 해방 이후 대양출판사를 설립하여 3,000여 종의 단행본을 발행한 출판인.
    '김익동': {'role': 'scholar'},  # 조선 - 조선 후기에, 『상제의집록』, 『직재문집』 등을 저술한 학자.
    '김익두': {'role': 'other'},  # 근대 - 일제강점기에, 개신교 부흥사로서 큰 업적을 남긴 평양신학교 출신의 개신교 목사.
    '김익문': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 광주부유수, 한성부판윤, 홍문관제학 등을 역임한 문신.
    '김익복': {'role': 'other'},  # 조선 - 조선 중기에, 도사, 영남군수 등을 역임한 문신.
    '김익상': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 의열단에 가입하여 조선총독부 투탄 의거를 전개하였고, 육군대장 다나카 암살을 시도했으나 실패한 ...
    '김익수': {'role': 'other'},  # 조선 - 조선 전기에, 병조참판, 관상감제조 등을 역임한 문신.
    '김익용': {'role': 'other'},  # 근대 - 조선후기 한성부판윤, 형조판서, 예문관제학 등을 역임한 관리.
    '김익정': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 재랑, 통정대부, 가선대부 등을 역임한 문신.
    '김익주': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 멕시코로 노동 이민하여 대한인국민회 탐피코지방회를 결성하였고, 식당 경영으로 번 수입을 기부하며...
    '김익중': {'role': 'other'},  # 근대 - 대한제국기 때, 호남창의맹소에서 종사로 활약한 의병장.
    '김익진': {'role': 'other'},  # 현대/대한민국 - 해방 이후 순심중학교 교장, 성의중학교 교감, 근화여자중학교 교감 등을 역임한 교육자이자 문필가.
    '김익훈': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 광주부윤, 형조참판, 어영대장 등을 역임한 문신.
    '김익휴': {'role': 'other'},  # 조선 - 조선 후기에, 행호군, 공조판서, 이조판서 등을 역임한 문신.
    '김익희': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 대사성, 대사헌, 대제학 등을 역임한 문신.
    '김인': {'role': 'other'},  # 근대 - 일제강점기 때, 한국국민당 조직에 참여하였고, 한국국민당청년단의 기관지 『전고』, 『청년호성』 등을 발간한 독립운동가.
    '김인겸': {'role': 'novelist'},  # 조선/조선 후기 - 조선 후기에, 「일동장유가」, 『동사록』 등을 저술한 문인.
    '김인경': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 혜순옹주와 혼인하여 광천위에 봉해진 문신.
    '김인관': {'role': 'scholar'},  # 조선 - 조선시대 「어해도」, 「화훼도」, 「초충도」 등의 작품을 그린 화가.
    '김인광': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 지김해부 진례성 제군사 명의장군으로 불렸던 호족.
    '김인규': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 「새출발」, 「조선해협」, 「병정님」 등에 출연한 배우 · 미술인 · 친일반민족행위자.
    '김인근': {'role': 'other'},  # 근대 - 일제강점기 때, 안창호의 지시를 받고 평양 특파원으로 파견되어 항일투쟁을 전개한 독립운동가.
    '김인령': {'role': 'scholar'},  # 조선/조선 전기 - 조선 전기에, 예조좌랑, 문학, 지평 등을 역임한 문신.
    '김인문': {'role': 'other'},  # 고려/고려 후기 - 고려후기 문황의 김준암살미수사건과 관련된 관리. 무신.
    '김인서': {'role': 'other'},  # 근대 - 일제강점기 때, 함경북도 회령에 임시정부 연통제를 조직하여 정보 수집 및 군자금 모금 활동을 전개한 독립운동가.
    '김인석': {'role': 'other'},  # 고려 - 고려 전기에, 장주분도, 상서우승 등을 역임한 문신.
    '김인선': {'role': 'other'},  # 고려/고려 후기 - 고려후기 내전숭반을 역임한 환관.
    '김인섭': {'role': 'other'},  # 근대 - 조선 후기에, 장녕전별검, 사간원정언 등을 역임한 문신.
    '김인손': {'role': 'other'},  # 조선 - 조선 전기에, 평안도관찰사, 지중추부사, 지돈녕부사 등을 역임한 문신.
    '김인승': {'role': 'other'},  # 근대/일제강점기 | 현대 - 일제강점기 「나부」, 「아틀리에 」, 「가락」 등을 그린 화가. 서양화가, 친일반민족행위자.
    '김인식': {'role': 'other'},  # 근대/일제강점기 - 한국 최초의 서양 음악가로 「학도가」 · 「표의」 · 「부모은덕가」 등 다수의  노래를 작곡한 작곡가.
    '김인연': {'role': 'other'},  # 고려 - 고려 후기에, 지신사, 밀직사, 찬성사 등을 역임한 문신.
    '김인영': {'role': 'scholar'},  # 근대 - 일제강점기 감리교신학교교장, 기독교조선감리회연맹 이사 등을 역임한 목사. 신학자.
    '김인위': {'role': 'other'},  # 고려 - 고려전기 평장사, 상서좌복야 참지정사 주국 경조현 개국남 등을 역임한 문신.
    '김인전': {'role': 'other'},  # 근대 - 일제강점기 때, 임시정부 국무원 학무차장, 임시의정원 전원위원장, 의장, 대한적십자회 상의원 등을 역임한 독립운동가.
    '김인존': {'role': 'other'},  # 고려 - 고려 전기에, 비서감, 병부, 예부, 호부상서, 익성동덕공신 등을 역임한 문신 · 공신.
    '김인찬': {'role': 'other'},  # 조선 - 조선전기 중추원사, 의흥친군위동지절제사 등을 역임한 무신. 무신.
    '김인태': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라 제29대 태종무열왕의 다섯째 아들인 왕자.
    '김인항': {'role': 'scholar'},  # 조선 - 조선 후기에, 『도촌유고』 등을 저술한 학자.
    '김인호': {'role': 'other'},  # 고려 - 고려 후기에, 밀직부사, 순성익찬보리공신도첨의참리, 찬성사 등을 역임한 문신 · 공신.
    '김인환': {'role': 'scholar'},  # 현대/대한민국 - 경북대학교 농학과 교수, 농촌진흥청장 등을 역임하였고, 통일벼의 보급확대에 힘쓴 농학자 · 관료.
    '김인후': {'role': 'scholar'},  # 조선/조선 전기 - 조선전기 세자시강원설서, 홍문관부수찬, 제술관 등을 역임한 문신. 학자.
    '김일': {'role': 'other'},  # 고려 - 고려 후기에, 검교중랑장, 금적사, 보빙사 등을 역임한 문신.
    '김일경': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 정언, 동부승지, 이조판서 등을 역임한 문신.
    '김일곤': {'role': 'other'},  # 근대 - 일제강점기 때, 조선의용군 진서북지대 책임자, 화북조선독립동맹 진서북분맹 조직위원 등을 역임한 독립운동가.
    '김일동': {'role': 'other'},  # 조선/조선 전기 - 조선전기 황해도 신계에서 반란을 일으킨 주모자.
    '김일두': {'role': 'other'},  # 근대 - 일제강점기 때, 임시정부 통신원으로 임명되어 군자금 모금 활동을 전개한 독립운동가.
    '김일봉': {'role': 'other'},  # 근대 - 일제강점기 때, 대한독립단에서 친일파 숙청, 일제기관 파괴, 군자금 모금 활동 등을 전개한 독립운동가.
    '김일손': {'role': 'scholar'},  # 조선/조선 전기 - 조선 전기에, 『탁영집』 등을 저술한 문신.
    '김일수': {'role': 'other'},  # 근대 - 일제강점기 조공재건설준비위원회 책임비서, 공산주의자협의회 군사부책임자 등을 역임한 사회주의운동가.
    '김일엽': {'role': 'scholar'},  # 근대 - 해방 이후 『청춘을 불사르고』, 『행복과 불행의 갈피에서』 등을 저술한 승려.
    '김일원': {'role': 'other'},  # 근대 - 대한제국기 때, 정환직 의진에서 항일의병활동을 전개한 의병.
    '김일진': {'role': 'scholar'},  # 조선 - 조선 후기에, 변려체에 재능을 보였으며, 폐비된 인현왕후에게 예를 표하고, 과거에서의 부정을 비판하는 상소를 올렸다가 남인...
    '김일해': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 「춘풍」 · 「오몽녀」 · 「순정해협」 등에 출연한 배우. 영화배우.
    '김일환': {'role': 'other'},  # 근대/일제강점기 - 일제강점기인 1940년 한국광복군 창설 이후 제2지대 간부로 활동한 독립운동가.
    '김임상': {'role': 'other foreigner'},  # 남북국시대 통일신라의 부사로 일본에 파견된 관리.
    '김입견': {'role': 'other'},  # 고려 - 고려후기 판밀직사사 등을 역임한 무신.
    '김입지': {'role': 'scholar'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 숙위학생으로 당나라에서 유학한 학자. 문장가.
    '김잉석': {'role': 'scholar'},  # 현대/대한민국 - 동국대학교 불교대학장 등을 역임하였으며, 『불교학개론』, 『화엄학개론』 등을 저술한 불교학자.
    '김자': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 우대언, 대독관, 좌대언 등을 역임한 문신.
    '김자경': {'role': 'other'},  # 현대/대한민국 - 해방 이후 김자경오페라단 단장, 한국음악협회 부이사장 등을 역임한 음악인. 성악가.
    '김자류': {'role': 'other'},  # 고려/고려 전기 - 고려 전기 이자겸의 난으로 불탄 궁궐을 중수한 문신.
    '김자린': {'role': 'other'},  # 현대/대한민국 - 북한에서, 조선인민군 군단 부군단장, 민족보위성 부국장, 최고인민회의 대의원 등을 역임한 군인 · 관료.
    '김자림': {'role': 'playwright novelist'},  # 현대/대한민국 - 해방 이후 「돌개바람」, 「신들의 결혼」, 「이민선」 등의 작품을 낸 극작가.
    '김자수': {'role': 'other'},  # 고려 - 고려 후기에, 판전교시사, 충청도관찰사, 형조판서 등을 역임한 문신.
    '김자의': {'role': 'other'},  # 고려/고려 전기 - 고려 전기에, 동지공거, 우산기상시, 예부상서 등을 역임한 문신.
    '김자점': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 강화부윤, 우의정, 어영청도제조 등을 역임한 문신.
    '김자정': {'role': 'other'},  # 조선 - 조선 전기에, 황해도관찰사, 지의금부사, 한성부판윤 등을 역임한 문신.
    '김자지': {'role': 'other'},  # 고려 - 조선 전기에, 평안도관찰사, 형조판서, 개성부유후 등을 역임한 문신.
    '김자진': {'role': 'other'},  # 고려 - 고려전기 대장군 고문개 등의 역모와 관련된 무신.
    '김자환': {'role': 'other'},  # 조선/조선 전기 - 조선전기 여진에서 조선에 귀화한 유민.
    '김자희': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 강원도 홍천군 내촌면 물걸리의 독립만세시위에 참여했다가 순국한 독립운동가.
    '김작': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 병조판서, 수지중추부사, 형조판서 등을 역임한 문신.
    '김작빈': {'role': 'other'},  # 고려 - 고려 전기에, 어사중승, 상서우승, 대부경 등을 역임한 문신.
    '김잠': {'role': 'other'},  # 고려 - 고려 후기에, 송문중, 권근 등과 응거시에 합격한 문신.
    '김장': {'role': 'other'},  # 고려 - 고려 후기에, 대호군 등을 역임한 무신 · 공신.
    '김장렴': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 제41대 헌덕왕의 아들인 왕자.
    '김장생': {'role': 'scholar'},  # 조선/조선 후기 - 조선 후기에, 『상례비요』, 『가례집람』, 『근사록석의』 등을 저술한 문신.
    '김장손': {'role': 'other'},  # 근대/개항기 - 개항기 임오군란 당시의 주모자.
    '김장수': {'role': 'other'},  # 고려 - 고려후기 상장군 겸 만호, 교주도병마사, 상호군 등을 역임한 무신.
    '김장순': {'role': 'scholar'},  # 조선/조선 후기 - 조선 후기, 선종한과 함께 『감저신보』를 저술한 농학자.
    '김장언': {'role': 'other foreigner'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 급찬으로 일본에 파견된 관리.
    '김장여': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 파진찬으로 시중을 역임한 관리.
    '김장이': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 장군 김유신의 넷째 아들로 대아찬을 역임한 관리.
    '김장청': {'role': 'scholar'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 집사랑으로 김유신의 행록을 저술한 관리.
    '김장훈': {'role': 'other'},  # 현대/대한민국 - 해방 이후 해군함대 부사령관, 해군통제 부사령관, 해군중장 등을 역임한 군인. 관료.
    '김재계': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 전라남도 장흥의 3·1운동을 주도하고 1930년대 후반에 '멸왜기도'를 드리다가 체포되어 옥고를 치른...
    '김재관': {'role': 'scholar'},  # 현대/대한민국 - 철강, 자동차 등 우리나라 중공업의 발전 방안을 제시한 과학자이자 기술 관료.
    '김재광': {'role': 'other'},  # 현대/대한민국 - 서울시의회 의원, 제7·8·9·10·12대 국회의원, 통일민주당 상임고문 등을 역임한 정치인.
    '김재규': {'role': 'other'},  # 현대 - 해방 이후 10, 26 박정희 대통령 시해사건 당시의 군인. 정치인.
    '김재근': {'role': 'scholar'},  # 현대/대한민국 - 서울대학교 조선공학과 교수, 대한조선학회 회장 등을 역임하였으며, 『거북선의 신화』, 『한국선박사연구』, 『한국의...
    '김재덕': {'role': 'other'},  # 근대 - 일제강점기 때, 임시의정원 비서, 교하중학교 교장, 정의부 중앙상임대의원, 국민부 집행위원 등을 역임한 독립운동가.
    '김재로': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 병조판서, 판중추부사, 영의정 등을 역임한 문신.
    '김재룡': {'role': 'other'},  # 근대 - 일제강점기 때, 성진회, 옥과노동회에서 동맹휴교와 광주학생항일운동을 주도한 독립운동가.
    '김재명': {'role': 'other'},  # 현대/대한민국 - 해방 이후 육군 제1군단장, 합참본부장 겸 대간첩대책 본부장, 국방부 인력차관보 등을 역임한 군인.
    '김재백': {'role': 'other foreigner'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 대나마로서 일본에 파견된 사신.
    '김재범': {'role': 'other'},  # 근대 - 일제강점기 동북항일연군 제2군 제6사 제7단에서 정치위원으로 활동한 사회주의운동가.
    '김재봉': {'role': 'other'},  # 근대/일제강점기 - 일제강점기, 조선공산당 초대 책임비서를 지낸 사회주의운동가 · 독립운동가.
    '김재석': {'role': 'other'},  # 현대/대한민국 - 해방 이후 조선미술가협회 위원, 조선공예가회 회장 등을 역임한 공예가. 도예가.
    '김재선': {'role': 'other'},  # 근대 - 해방 이후 대한국악원 이사, 전국국악인친목회 회장 등을 역임한 장구명인.
    '김재섭': {'role': 'other'},  # 현대/대한민국 - 해방 이후 주식회사 영창악기를 설립한 기업인.
    '김재수': {'role': 'other'},  # 조선 - 조선후기 효행으로 정려를 하사 받고, 동몽교관에 추증된 효자.
    '김재순': {'role': 'other'},  # 조선 - 조선 후기에, 대사간, 경상도관찰사, 대사헌 등을 역임한 문신.
    '김재욱': {'role': 'other'},  # 현대/대한민국 - 북한에서, 농업부 부장, 평남도당위원장 등을 역임하였으나, 8월 종파사건을 계기로 숙청된 관료.
    '김재원': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「꼭두각시놀음」의 덜미 전승자로 지정된 기예능보유자.
    '김재익': {'role': 'scholar'},  # 현대/대한민국 - 경제기획원 기획국장, 제5공화국 대통령비서실 경제수석비서관 등을 역임한 경제학자 · 관료.
    '김재일': {'role': 'scholar'},  # 조선 - 조선후기 사헌부지평, 사간원정언, 이조정랑 등을 역임한 문신. 학자.
    '김재준': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 『낙수』, 『요한계시록 주석』, 『황야에 외치는 소리』 등을 저술한 신학자이자 목사, 재야 민주화운동가.
    '김재찬': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 평안도관찰사, 한성부판윤, 우의정 등을 역임한 문신.
    '김재창': {'role': 'other'},  # 근대 - 일제강점기 때, 대한광복회에서 군자금 모금 활동 등을 전개한 독립운동가.
    '김재철': {'role': 'scholar'},  # 근대/일제강점기 - 일제강점기 때, 최초의 한국 연극사 연구인 『조선연극사』를 저술한 국문학자.
    '김재학': {'role': 'other'},  # 현대 - 해방 이후 제헌의원, 삼성운수㈜대표이사 등을 역임한 정치인. 실업가.
    '김재항': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 안성군 삼죽면 덕산리의 독립만세시위에 참여했다가 순국한 독립운동가.
    '김재현': {'role': 'other'},  # 근대 - 조선 후기에, 경기도관찰사, 한성부판윤, 지중추부사 등을 역임한 문신.
    '김재호': {'role': 'other'},  # 현대 - 한국전쟁 당시 강원도 김화의 수도고지전투에 참전한 군인.
    '김재화': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 경상남도 진주의 독립만세시위를 주도한 혐의로 체포된 독립운동가.
    '김재훈': {'role': 'scholar'},  # 근대 - 일제강점기 경성음악전문학교 초대원장, 조선음악협회 이사 등을 역임한 음악인. 작곡가. 바이올리니스트.
    '김저': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 검열, 어사, 교리, 지평 등을 역임하다 을사사화에 관련되어 관직을 박탈당하고 유배된 문신.
    '김적': {'role': 'other'},  # 고려 - 고려 후기에, 중랑장 등을 역임한 무신 · 공신.
    '김전': {'role': 'other'},  # 조선 - 조선 전기에, 공조판서, 한성부판윤, 영의정 등을 역임한 문신.
    '김점현': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 평안남도 대동군 금제면 원장리와 강서군 반석면 상사리 사천시장 일대의 독립만세시위에 참여했다가 ...
    '김정': {'role': 'scholar'},  # 조선 - 조선후기 강릉부사, 사간원정언, 제주목사 등을 역임한 문신. 학자.
    '김정견': {'role': 'scholar'},  # 조선/조선 후기 - 조선 후기에, 생원이 되었으나, 벼슬을 지내지 않고 향리에서 후진 양성에 힘쓴 학자.
    '김정경': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 공안부윤, 조군도총제, 개성부유후 등을 역임한 문신.
    '김정고': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 만파식적을 보관하던 천존고(天尊庫)의 창고지기로 근무한 관리.
    '김정구': {'role': 'other'},  # 현대/대한민국 - 일제강점기 「총각진정서」, 「왕서방 연서」, 「눈물 젖은 두만강」 등을 부른 가수.
    '김정국': {'role': 'scholar'},  # 조선 - 조선 전기에, 『사재집』, 『사재척언』, 『경민편』 등을 저술한 문신.
    '김정권': {'role': 'other foreigner'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 급찬으로서 일본에 파견된 사신.
    '김정균': {'role': 'other'},  # 조선 - 조선 후기에, 대사헌, 충청도관찰사 등을 역임한 문신.
    '김정근': {'role': 'other'},  # 근대 - 조선 후기에, 법부협판, 경위원총관, 경무사 등을 역임한 문신.
    '김정길': {'role': 'other'},  # 근대 - 대한제국기 박기홍의 제자로 김창환협률사등에서 활동한 판소리의 명창. 창극명인.
    '김정남': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 견당 청익승 엔닌[圓仁]의『입당구법순례행기』와 관련된 역관.
    '김정락': {'role': 'other foreigner'},  # 남북국시대 통일신라의 소판관으로 일본에 파견된 관리.
    '김정란': {'role': 'other'},  # 남북국시대 통일신라의 미인으로 『삼국유사』의 사미 묘정 설화와 관련된 주인공.
    '김정련': {'role': 'other'},  # 근대 - 일제강점기 때, 전라남도에서 군자금 모집 활동을 전개하다가 공명단에서 활동하며 독립군 비행사 양성을 위해 비행학교 설립을 ...
    '김정렬': {'role': 'other'},  # 현대 - 해방 이후 초대 공군참모총장, 국방부장관, 반공연맹 이사장 등을 역임한 군인. 정치인.
    '김정룡': {'role': 'other'},  # 조선 - 조선 중기에, 영월군수, 풍기군수, 이조정랑 등을 역임한 문신.
    '김정목': {'role': 'other'},  # 조선 - 조선 중기에, 사예, 내자시정, 장흥부사 등을 역임한 문신.
    '김정묵': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 1919년 대한민국임시정부 임시의정원 의원, 의열단 단원으로 활동한 독립운동가.
    '김정문': {'role': 'other'},  # 근대 - 일제강점기 송만갑의 제자로 동편제에 기초를 두고 서편제의 가락을 함께 구사한 판소리의 명창.
    '김정범': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 통의부에서 군자금 모금 및 친일파 처단 등 항일무장투쟁을 전개한 독립운동가.
    '김정수': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 서울대학교 공과대학 응용수학과 교수, 대한수학회 회장 등을 역임한 학자. 수학자.
    '김정숙': {'role': 'other foreigner'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 대나마로 일본에 파견된 관리.
    '김정순': {'role': 'other'},  # 고려 - 고려 전기에, 참지정사, 상서우복야 서경유수사 겸 태자소부 등을 역임한 문신.
    '김정식': {'role': 'other'},  # 현대/대한민국 - 제2대 국회의원 · 자유당 문화부장 등을 역임한 정치인.
    '김정실': {'role': 'other'},  # 현대/대한민국 - 임시정부 산하 정치공작대의 총무, 단국대학교 재단설립 이사와 학장, 민의원 등을 역임한 교육자 · 정치인.
    '김정언': {'role': 'scholar'},  # 고려 - 고려전기 태승, 한림학사, 내봉성령 등을 역임한 문신. 학자.
    '김정여': {'role': 'other'},  # 고려/고려 후기 - 고려후기 위사보좌공신에 책록된 공신. 무신.
    '김정연': {'role': 'other'},  # 현대 - 해방 이후 서도소리의 전승자로 지정된 예능보유자.
    '김정오': {'role': 'other'},  # 조선 - 조선 후기에, 사직서여, 형조정랑, 성현찰방 등을 역임한 문신.
    '김정원': {'role': 'other'},  # 근대 - 대한제국기 때, 경상북도 서북방 산간 지역에서 항일의병투쟁을 전개한 의병.
    '김정윤': {'role': 'other'},  # 조선 - 조선 후기에, 헌납, 공조참의 등을 역임한 문신.
    '김정익': {'role': 'other'},  # 근대 - 일제강점기 때, 친일파 이완용과 이용구의 암살을 계획한 혐의로 체포된 독립운동가.
    '김정일': {'role': 'other'},  # 현대/대한민국 - 북한에서, 김일성 사망 이후 권력을 승계한 제2대 통치자로, 국방위원장, 조선로동당 총비서, 조선인민군 최고사령관...
    '김정제': {'role': 'scholar'},  # 현대/대한민국 - 대한한의사협회 회장, 경희대학교 한의과대학 학장 등을 역임한 한의학자.
    '김정종': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 때, 이찬 관등으로 장군, 상대등 등을 역임한 통일신라의 관리.
    '김정주': {'role': 'scholar foreigner'},  # 현대/대한민국 - 해방 이후 「일본의 한국침략사」, 「구주와 한인」, 「일제통치사료」 등을 저술한 학자. 역사학자.
    '김정준': {'role': 'other'},  # 근대 - 해방 이후, 전국신학대학협의회 초대 회장, 한국신학대학 학장 등을 역임한 한국기독교장로회 소속의 목사.
    '김정진': {'role': 'playwright novelist'},  # 근대/일제강점기 - 일제강점기 「찬웃음」, 「약수풍경」, 「꿈」 등의 작품을 낸 극작가. 언론인.
    '김정집': {'role': 'other'},  # 조선 - 조선 후기에, 동지성균관사, 대사헌, 평안도관찰사 등을 역임한 문신.
    '김정하': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 모스크바 동방노력자공산대학에서 조선민족부 교관을 지냈으며, 사회주의운동을 전개한 독립운동가.
    '김정한': {'role': 'novelist'},  # 현대 - 해방 이후 「모래톱이야기」, 「수라도」, 「인간단지」 등을 저술한 작가. 소설가.
    '김정헌': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 제암리교회 지도자로 활동하였으며, 수원의 독립만세시위를 주도하다가 제암리 학살사건에 의해 사망한...
    '김정현': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 「녹음」, 「귀로」, 「임」 등의 작품을 그린 화가.
    '김정혜': {'role': 'other'},  # 근대/대한제국기 - 대한제국기 정화여학교를 설립하고 여성을 위한 교육의 필요성을 역설한 교육자.
    '김정호': {'role': 'other'},  # 근대/개항기 | 근대/일제강점기 - 일제강점기 개성전기주식회사 대표이사, 개성상공회의소 회장 등을 역임한 기업인. 친일반민족행위자.
    '김정환': {'role': 'other'},  # 근대/일제강점기 - 일제강점기, 충청북도 청원군에서 독립만세시위를 주도한 독립운동가.
    '김정후': {'role': 'other'},  # 조선 - 조선 후기에, 전적, 직강, 옹진군수 등을 역임한 문신.
    '김정희': {'role': 'scholar'},  # 조선 - 조선 후기에 조선 금석학파를 성립하고 추사체를 완성한 문신 · 학자 · 서화가.
    '김제': {'role': 'other'},  # 고려 - 고려 전기에, 이부상서 참지정사 겸 태자소보, 태자태보 등을 역임한 문신.
    '김제갑': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 정언, 층청도관찰사, 우승지 등을 역임한 문신.
    '김제겸': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 헌납, 집의, 예조참의, 승지 등을 역임하였으며, 목호룡의 고변으로 노론 4대신이었던 아버지가 사...
    '김제공': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 제38대 원성왕 때 반란을 일으킨 주모자.
    '김제남': {'role': 'other'},  # 조선 - 조선 중기에, 이조좌랑, 돈녕부도정, 영돈령부사 등을 역임한 문신.
    '김제민': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 평안남도 대동군 금제면 원장리와 강서군 반석면 상사리 사천시장 일대의 독립만세시위에 참여했다가 ...
    '김제신': {'role': 'other'},  # 조선 - 조선 전기에, 정언, 집의, 좌승지, 예조참판 등을 역임한 문신.
    '김제안': {'role': 'other'},  # 고려 - 고려 후기에, 군부좌랑, 내서사인, 전교부령 등을 역임한 문신.
    '김제옹': {'role': 'other'},  # 고대/남북국/통일신라 - 통일신라의 제38대 원성왕의 손자로, 형 김언승(제41대 헌덕왕)과 난을 일으켜 애장왕을 살해한 왕족.
    '김제준': {'role': 'other'},  # 조선 - 조선후기 기해박해 당시의 순교자.
    '김제중': {'role': 'other'},  # 근대 - 일제강점기 때, 전라남도 곡성과 담양에서 임시정부의 군자금조달원으로 활동한 독립운동가.
    '김제철': {'role': 'other'},  # 조선 - 조선후기 8명창의 한 사람으로 「심청가」에 뛰어났던 판소리의 명창.
    '김제혜': {'role': 'other'},  # 근대 - 일제강점기 국제여성총회에 조선인 대표로 참석한 사회주의운동가.
    '김제환': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 제자들을 모아 배일사상을 고취하고 항일투쟁을 전개한 독립운동가.
    '김조': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 병조참판, 예조판서, 지중추원사 등을 역임한 문신.
    '김조규': {'role': 'poet'},  # 근대/일제강점기 - 일제강점기 「연심」, 「어버이 잃은 가슴이」, 「회향곡」 등을 저술한 시인.
    '김조근': {'role': 'other'},  # 조선/조선 후기 - 조선후기 어영대장, 영돈녕부사 등을 역임한 척신.
    '김조순': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 이조참의, 부제학, 이조판서 등을 역임한 문신.
    '김조이': {'role': 'other'},  # 근대 - 광복 이후 전조선민중운동자대회 준비위원, 민주주의민족전선 중앙위원 등을 역임한 사회주의운동가. 독립운동가.
    '김존경': {'role': 'other'},  # 조선 - 조선 후기에, 강원도감사, 지중추부사, 경주부윤 등을 역임한 문신.
    '김존심': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 내시합문지후 등을 역임한 문신.
    '김존중': {'role': 'other'},  # 고려 - 고려 전기에, 첨사부녹사, 우정언, 우승선, 태자소보 등을 역임한 문신.
    '김종': {'role': 'scholar'},  # 조선 - 조선 전기에, 진사가 되었으나, 기묘사화가 일어나자 과거를 포기하고 은거하여 성리학적 예절을 탐구하고 실천한 학자.
    '김종규': {'role': 'other'},  # 근대 - 조선후기 궁내부특진관, 경효전제조, 경상북도관찰사 등을 역임한 관리.
    '김종기': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 백낙준의 제자로 조선성악연구회에서 활동한 음악인. 거문고산조명인.
    '김종남': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 「풍경1」, 「호라」, 「물가」 등을 그린 화가. 서양화가.
    '김종덕': {'role': 'scholar'},  # 조선 - 조선 후기에, 『천사집』, 『석학정론』, 『초려문답』 등을 저술한 학자.
    '김종렬': {'role': 'other'},  # 현대 - 해방 이후 대한체육회 부회장, 서울올림픽대회조직위원회 위원 등을 역임한 체육인.
    '김종리': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 진산현감, 고부현감, 예문관직제학 등을 역임한 문신.
    '김종림': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 때, 미국으로 노동 이민하여 공립협회, 흥사단, 한인공동회, 대한인국민회 등에서 활동하였고, 노동으로...
    '김종묵': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 간도 용정촌에서 전개된 독립만세시위를 주도하다가 순국한 독립운동가.
    '김종문': {'role': 'poet critic'},  # 현대/대한민국 - 해방 이후 『벽』, 『불안한 토요일』, 『시사시대』 등을 저술한 시인. 비평가.
    '김종민': {'role': 'other'},  # 조선 - 조선시대 미곶첨사를 역임한 무신.
    '김종발': {'role': 'scholar'},  # 조선 - 조선후기 승문원부정자, 사헌부지평, 장령 등을 역임한 문신. 학자.
    '김종범': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 조선노농총동맹과 북풍회에서 활동한 사회주의운동가, 독립운동가.
    '김종삼': {'role': 'poet'},  # 현대 - 해방 이후 『시인학교』, 『북치는 소년』, 『누군가 나에게 물었다』 등을 저술한 시인.
    '김종서': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 함길도도관찰사, 우의정, 좌의정 등을 역임한 문신.
    '김종석': {'role': 'scholar'},  # 한국광업진흥주식회사 상무이사, 대한광산학회 회장 등을 역임하였으며, 『자원개발통론』, 『한국광업개사』, 『탄성학』 등을 저술한 채광학자.
    '김종선': {'role': 'other'},  # 현대/대한민국 - 일제강점기 때, 조선식산신탁회사 부사장, 서울 천도교 홍제소년군 단장 등을 역임하며 사회운동과 빈민구제활동에 참여...
    '김종수': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 대제학, 이조판서, 우의정 등을 역임한 문신.
    '김종순': {'role': 'other'},  # 조선 - 조선 전기에, 판한성부사, 평안도관찰사, 지중추부사 등을 역임한 문신.
    '김종연': {'role': 'other'},  # 고려 - 고려후기 이성계 살해모의 당시의 장수.
    '김종영': {'role': 'scholar'},  # 현대 - 해방 이후 「3, 1운동 기념상」, 「가족」, 「전설」 등의 작품을 낸 조각가.
    '김종오': {'role': 'other'},  # 현대 - 한국전쟁 당시 강원도 철원의 백마고지전투에 참전한 군인.
    '김종우': {'role': 'other'},  # 근대 - 일제강점기, 한국교회의 초기 부흥사로 기독교조선감리회 3대 감독을 역임한 목사.
    '김종원': {'role': 'other'},  # 현대/대한민국 - 해방 이후 육군헌병총사령부 부사령관, 경남지구 계엄사령관 등을 역임한 군인. 경찰.
    '김종윤': {'role': 'other'},  # 조선 - 조선시대 어모장군, 행용양위부호군 등을 역임한 무신.
    '김종익': {'role': 'other'},  # 현대/대한민국 - 한국체육회 회장, 국회의원, 공화당 중앙위원회 부위원장 등을 역임한 정치인 · 교육자.
    '김종일': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 교리, 울산부사 등을 역임한 문신.
    '김종정': {'role': 'scholar'},  # 조선 - 조선후기 성균관대사성, 예조판서, 좌참찬 등을 역임한 문신. 학자.
    '김종직': {'role': 'scholar'},  # 조선/조선 전기 - 조선전기 병조참판, 홍문관제학, 공조참판 등을 역임한 문신. 학자.
    '김종진': {'role': 'other'},  # 근대 - 일제강점기 때, 한족총연합회 조직 선전 농무부 위원장 등을 역임한 독립운동가.
    '김종찬': {'role': 'scholar'},  # 근대/일제강점기 - 일제강점기 「산서」, 「진중의 A병단장」, 「몽고가족」 등의 작품을 그린 화가. 서양화가.
    '김종철': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 『교육계획론』, 『세계 안의 한국교육』, 『한국고등교육 연구』 등을 저술한 학자. 교육학자.
    '김종태': {'role': 'scholar'},  # 근대 - 일제강점기 「아이」, 「포오즈」, 「낮잠」 등의 작품을 그린 화가.
    '김종표': {'role': 'other'},  # 근대 - 조선후기 대오전악, 집사악사 등을 역임한 가야금명인.
    '김종한': {'role': 'poet critic'},  # 근대/일제강점기 - 일제강점기 「귀로」 · 「고원의 시」 · 「할아버지」 등을 저술한 시인. 문학평론가 · 친일반민족행위자.
    '김종해': {'role': 'other'},  # 해방 이후 서울대학교 의과대학 교수, 화종신경정신과의원 원장 등을 역임한 의료인.
    '김종현': {'role': 'other'},  # 고려 - 고려 전기에, 예부원외랑, 우간의대부, 우산기상시 등을 역임한 문신.
    '김종호': {'role': 'other'},  # 현대/대한민국 - 해방 이후 주월군사참모장, 군수차관보, 육군소장 등을 역임한 군인. 경영인.
    '김종후': {'role': 'critic novelist'},  # 현대/대한민국 - 해방 이후 「작가의패기」, 「동양의 휴머니즘」, 「민족문학소론」 등을 저술한 평론가.
    '김종희': {'role': 'other'},  # 현대 - 해방 이후 제일화재해상보험 대표이사, 전국경제인연합회 부회장 등을 역임한 실업가.
    '김좌근': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 예조판서, 형조판서, 공조판서, 호조판서 등을 거쳐 영의정을 3번 연임한 문신.
    '김좌명': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 공조판서, 병조판서, 호조판서 등을 역임한 문신.
    '김좌진': {'role': 'other'},  # 근대/일제강점기 - 북로군정서를 이끌고 청산리 대첩을 승리로 이끈 독립운동가.
    '김주': {'role': 'other'},  # 조선 - 조선 후기에, 예조정랑, 춘추관기주관, 무안현감 등을 역임한 문신.
    '김주경': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 북한에서 「만경대」 · 「묘향산」 등의 작품을 그린 화가.
    '김주남': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 수원의 독립만세시위를 주도하다가 고주리 학살사건에 의해 사망한 독립운동가.
    '김주만': {'role': 'scholar'},  # 조선 - 조선 후기에, 『청헌집』 등을 저술한 학자.
    '김주신': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 영돈령부사, 호위대장 등을 역임한 문신.
    '김주업': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 수원의 독립만세시위에 참여했다가 고주리 학살사건에 의해 사망한 독립운동가.
    '김주열': {'role': 'other'},  # 현대/대한민국 - 대한민국의 의거 학생으로, 1960년, 3·15부정선거에 반대하는 마산 시위에 참가하였다가 경찰이 쏜 최루탄에 희...
    '김주우': {'role': 'other'},  # 조선/조선 후기 - 조선후기 정언, 지평, 경성판관 등을 역임한 문신. 서예가.
    '김주원': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 이찬으로 시중을 역임한 귀족. 재상.
    '김주정': {'role': 'other'},  # 고려 - 고려 후기에, 부성위, 진변만호, 응방도감사 등을 역임한 문신.
    '김주천': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 한찬 관등을 역임한 관리.
    '김주필': {'role': 'other'},  # 남북국시대 통일신라의 당나라에 사신으로 파견된 관리.
    '김주현': {'role': 'other'},  # 근대 - 개항기 봉상사제조, 장례원경 등을 역임한 관료.
    '김죽파': {'role': 'other'},  # 현대/대한민국 - 해방 이후 가야금산조 및 병창의 전승자로 지정된 예능보유자.
    '김준': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 의열단 간부학교 교관, 조선의용대 전방공작대원, 한국광복군 제1지대 제1구대장 등을 역임한 독립...
    '김준거': {'role': 'other'},  # 고려 - 고려후기 무신정변과 관련된 무신.
    '김준근': {'role': 'scholar'},  # 개항기 「기산풍속도」 · 「텬로력뎡」 삽화 등의 작품을 그린 화가.
    '김준룡': {'role': 'other'},  # 조선 - 조선시대 김해부사, 경상도병마절도사 등을 역임한 무신.
    '김준민': {'role': 'other'},  # 조선/조선 후기 - 조선 전기 임진왜란 때 거제현령과 합천가장을 지낸 무신.
    '김준섭': {'role': 'other'},  # 근대 - 일제강점기 창극좌, 동일창극단 등에서 활동한 음악인. 창극명인, 판소리명창.
    '김준성': {'role': 'other'},  # 현대/대한민국 - 일제강점기 함흥 영생고등보통학교 훈육주임, 용정 은진중학교 교사 등을 역임한 교육자. 사회운동가.
    '김준승': {'role': 'other'},  # 근대 - 일제강점기 때, 통의부 국내파견 결사대원으로 군자금 모금 활동을 전개한 독립운동가.
    '김준업': {'role': 'other'},  # 조선 - 조선 후기에, 이괄의 난과 병자호란이 발발하자 의병을 일으켜 항쟁한 의병장.
    '김준연': {'role': 'other'},  # 현대/대한민국 - 일제강점기 때, 조선일보 모스크바 특파원, 동아일보 편집국장 등을 역임하였으며, 해방 이후, 법무부장관, 국회의원...
    '김준엽': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 학병 출신으로 일본 제국주의 군대를 탈출하여 한국광복군 제2지대에서 활동한 독립운동가.
    '김준영': {'role': 'other'},  # 현대/대한민국 - 일제강점기 「처녀총각」 · 「개나리 고개」 · 「홍도야 울지 마라」 등을 만든 작곡가.
    '김준태': {'role': 'other'},  # 현대/대한민국 - 대구지방검찰청 검사 · 국회의원 등을 역임한 법조인 · 정치인.
    '김준택': {'role': 'other'},  # 근대 - 일제강점기 때, 정의부 중앙집행위원, 조선혁명당 중앙집행위원, 조선혁명군 사령관 등을 역임한 독립운동가.
    '김준현': {'role': 'other'},  # 현대/대한민국 - 일제강점기 「평조회상」을 독주한 음악인. 피리명인.
    '김중건': {'role': 'other'},  # 근대/일제강점기 - 원종교를 창립하였으며, 대진단을 조직하고 대한국민단 지단장으로 활약한 독립운동가.
    '김중경': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 제33대 성덕왕의 첫째 아들인 왕자.
    '김중공': {'role': 'other'},  # 고대/남북국/통일신라 - 통일신라의 제41대 헌덕왕의 동생인 왕족.
    '김중구': {'role': 'other'},  # 고려 - 고려후기 지추밀원사, 지문하성사, 왕경유수병마사 등을 역임한 무신.
    '김중기': {'role': 'other'},  # 조선 - 조선후기 훈련대장, 총융사 등을 역임한 무신.
    '김중남': {'role': 'scholar'},  # 조선 - 조선후기 전적, 단성현감, 자인현감 등을 역임한 문신. 학자.
    '김중린': {'role': 'other'},  # 현대/대한민국 - 북한에서, 최고인민회의 대의원, 대남담당 당 비서 등을 역임한 관료.
    '김중명': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 효종대의 북벌과 관련한 무신.
    '김중문': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 형부낭중, 병부시랑, 판장작감사, 지삼사사 등을 역임한 문신.
    '김중보': {'role': 'scholar'},  # 조선/조선 전기 - 조선 전기에, 주사(朱砂)로 수은을 제조하는 방법을 개발한 학자.
    '김중서': {'role': 'other'},  # 현대/대한민국 - 해방 이후 대구고등법원장, 대법원 판사, 선거관리위원장 등을 역임한 법조인.
    '김중식': {'role': 'other'},  # 근대 - 일제강점기 때, 경기도 안성군 원곡면과 양성면 일대의 독립만세시위에 참여한 독립운동가.
    '김중업': {'role': 'other foreigner'},  # 현대 - 해방 이후 주한프랑스대사관, 올림픽공원 상징조형물 등을 신축한 건축가.
    '김중온': {'role': 'other'},  # 고려 - 고려후기 부방장군, 분도장군 등을 역임한 무신.
    '김중원': {'role': 'scholar'},  # 조선 - 조선 후기에, 이인좌의 난을 진압하기 위해 의병을 일으켰고, 『퇴장암유집』 등을 저술하며 후진양성에 힘쓴 학자 · 의병장.
    '김중일': {'role': 'other'},  # 조선 - 조선후기 어영장, 훈련원판관 등을 역임한 무신.
    '김중청': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 정언, 신안현감, 승정원승지 등을 역임한 문신.
    '김중하': {'role': 'scholar'},  # 조선 - 조선 후기에, 돈령부도정, 형조참의 등에 임명되었으나, 벼슬에 뜻이 없어 모두 사양한 학자.
    '김중현': {'role': 'scholar'},  # 현대/대한민국 - 일제강점기 「무녀도」 · 「농악놀이」 등의 작품을 그린 화가.
    '김중환': {'role': 'other'},  # 근대 - 조선후기 중추원의관, 개성부윤, 문부조사위원 등을 역임한 관리.
    '김증한': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 『법학통론』, 『민법총칙』, 『물권법』 등을 저술한 학자. 교육행정가.
    '김지': {'role': 'other'},  # 조선 - 조선 전기에, 공주목사 등을 역임한 문신.
    '김지겸': {'role': 'other'},  # 고려 - 고려 후기에, 밀직부사, 영해부사, 권정동성 등을 역임한 문신.
    '김지경': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 이조참의, 예문관부제학, 지중추부사 등을 역임한 문신.
    '김지남': {'role': 'scholar'},  # 조선/조선 후기 - 조선후기 지중추부사로 『신전자초방』, 『동사록』, 『통문관지』 등을 저술한 역관.
    '김지대': {'role': 'scholar'},  # 고려 - 고려 후기에, 정당문학이부상서, 중서시랑평장사 등을 역임한 문신.
    '김지량': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라에서 하정사로서 당나라에 파견된 사신.
    '김지렴': {'role': 'other'},  # 고대/남북국/통일신라 - 통일신라의 제33대 성덕왕의 조카로, 당나라에 사신으로 방문한 종실.
    '김지만': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 때, 당나라에 사신으로 방문하여 태복경에 임명된 통일신라의 왕족.
    '김지묵': {'role': 'other'},  # 조선 - 조선 후기에, 판돈령부사, 총융사 등을 역임한 문신.
    '김지복': {'role': 'other'},  # 조선 - 조선 후기에, 사예, 형조좌랑 등을 역임한 문신.
    '김지산': {'role': 'other foreigner'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 아찬으로서 일본에 파견된 사신.
    '김지상': {'role': 'other foreigner'},  # 고대/남북국/통일신라 - 남북국시대 통일신라에서 파진찬으로서 일본에 파견된 사신.
    '김지서': {'role': 'other'},  # 고려 - 고려 후기에, 병마사, 만호 등을 역임한 무신 · 공신.
    '김지석': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 제주부사 등을 역임한 문신.
    '김지섭': {'role': 'other foreigner'},  # 근대/일제강점기 - 의열단원으로서 일본 왕궁에 폭탄을 투척한 독립운동가.
    '김지성': {'role': 'other'},  # 고려 - 고려후기 후군지병마사, 대장군, 추밀원부사 등을 역임한 무신.
    '김지수': {'role': 'other'},  # 조선 - 조선 후기에, 보덕, 종성부사 등을 역임한 문신.
    '김지숙': {'role': 'other'},  # 고려 - 고려 후기에, 동지광정원사 참지기무, 도첨의찬성사 판감찰사사, 첨의중찬 등을 역임한 문신.
    '김지옥': {'role': 'other'},  # 현대 - 해방 이후 「강령탈춤」의 전승자로 지정된 예능보유자.
    '김지우': {'role': 'other'},  # 고려 - 고려 전기에, 선경부사인, 합문지후, 안서도호부판관 등을 역임한 문신.
    '김지웅': {'role': 'other'},  # 조선 - 조선후기 청성첨절제사, 별군직, 맹산현감 등을 역임한 무신.
    '김지원': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 때, 이찬 관등으로 시중을 역임한 통일신라의 관리.
    '김지저': {'role': 'other'},  # 고려 - 고려후기 임유무 제거, 삼별초의 난 등과 관련된 무신.
    '김지태': {'role': 'other'},  # 현대/대한민국 - 해방 이후 한국생사회 회장, 대한상공회의소 부회장 등을 역임한 실업가. 정치인, 언론인.
    '김지화': {'role': 'other'},  # 고려 - 고려 전기에, 좌복야 참지정사, 태자소사, 판병부사 등을 역임한 문신.
    '김지환': {'role': 'other'},  # 근대/일제강점기 - 3·1운동 당시 ｢독립의견서｣, ｢독립청원서｣ 등을 상하이의 현순에게 전달하는 임무를 맡았던 독립운동가.
    '김직량': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라에서 입조사로서 당나라에 파견된 사신.
    '김직손': {'role': 'other'},  # 조선 - 조선 전기에, 정언, 한산군수, 사도시첨정 등을 역임한 문신.
    '김직재': {'role': 'other'},  # 조선 - 조선 후기에, 대 · 소북파 사이의 정쟁에 휘말려 아들 김백함과 함께 역모를 꾸민다는 누명을 쓰고 처형된 문신.
    '김진': {'role': 'other'},  # 조선 - 조선 후기에, 정언, 정주절제사, 예안현감 등을 역임한 문신.
    '김진갑': {'role': 'other'},  # 근대/일제강점기 | 현대 - 해방 이후 조선나전칠기공예조합의 이사장, 대한공예협회 회장 등을 역임한 공예가. 사업가.
    '김진걸': {'role': 'other'},  # 현대/대한민국 - 해방 이후 한국무용협회 이사 및 고문, 국립무용단 초대 지도 위원, 한성대학교 교수 등을 역임한 무용가. 한국무용...
    '김진구': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 좌참찬, 판의금부사 등을 역임한 문신.
    '김진규': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 대사성, 예조판서, 좌참찬 등을 역임한 문신.
    '김진균': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 「노래의 날개 위에」, 「금잔디」, 「그리움」 등을 만든 작곡가. 음악학자.
    '김진만': {'role': 'other'},  # 현대/대한민국 - 국회의원, 민주공화당 원내총무, 국회부의장 등을 역임한 정치인.
    '김진명': {'role': 'other'},  # 현대/대한민국 - 해방 이후 북한에서 전통 창법인 서도소리를 전승한 음악인. 작곡가.
    '김진묵': {'role': 'other'},  # 근대/대한제국기 - 대한제국기 때, 황해도 일대에서 항일의병투쟁을 전개하였으며, 국권 피탈 이후 광복단, 국민부 등에서 활동한 의병...
    '김진민': {'role': 'scholar'},  # 근대/일제강점기 | 현대 - 일제강점기 「유란부」, 「독서락」, 「누실명」 등의 작품을 낸 서예가.
    '김진상': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 대사성, 대사헌, 좌참찬 등을 역임한 문신.
    '김진섭': {'role': 'essayist scholar novelist'},  # 근대 - 해방 이후 『인생예찬』, 『생활인의 철학』 등을 저술한 작가. 수필가, 독문학자.
    '김진성': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 경기도 양주군 광적면의 독립만세시위를 주도하는 과정에서 순국한 독립운동가.
    '김진수': {'role': 'playwright novelist'},  # 현대 - 해방 이후 「코스모스」, 「불더미 속에서」, 「이 몸 조국에 바치리」 등의 작품을 낸 극작가. 연극이론가.
    '김진양': {'role': 'other'},  # 고려 - 고려 후기에, 우산기상시, 좌상시, 간관 등을 역임한 문신.
    '김진여': {'role': 'scholar'},  # 조선/조선 후기 - 조선후기 「기사계첩」, 「성적도」 등의 작품을 그린 화가.
    '김진옥': {'role': 'other'},  # 현대 - 해방 이후 「봉산탈춤」의 전승자로 지정된 예능보유자.
    '김진우': {'role': 'other'},  # 근대/일제강점기 | 현대 - 일제강점기 때, 임시의정원 강원도대표의원 등을 역임하며 항일투쟁을 전개하였으며, 「묵죽도」 · 「죽석도...
    '김진종': {'role': 'other'},  # 조선 - 조선 전기에, 부응교, 헌납, 전적 등을 역임한 문신.
    '김진주': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 백제정벌군을 지휘한 장수.
    '김진준': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 독립청년단을 조직하여 친일파 처단활동을 전개하였고, 대한광복군 내무부 기밀과장을 역임한 독립운동가.
    '김진초': {'role': 'scholar'},  # 근대/대한제국기 - 대한제국기 『과수재배법』, 『아국농업론』 등을 저술한 학자. 농촌계몽운동가.
    '김진태': {'role': 'other'},  # 조선 - 조선후기 「입춘가(立春歌)」, 「진선가(眞仙歌)」 등을 노래한 음악인.
    '김진표': {'role': 'other'},  # 조선 - 조선 후기에, 청풍군수, 공조참의, 돈녕부도정 등을 역임한 문신.
    '김진하': {'role': 'scholar'},  # 조선 - 조선후기 동지중추부사로 『삼역총해』, 『신역소아론』, 『팔세아』 등을 저술한 역관.
    '김진형': {'role': 'other'},  # 현대/대한민국 - 해방 이후 한국은행 총재, 한국개발금융주식회사 사장 등을 역임한 금융인.
    '김진호': {'role': 'other'},  # 근대 - 일제강점기 때, 흥업단 재무부장, 국민부 중앙집행위원, 조선혁명당 중앙위원 등을 역임한 대종교인 · 독립운동가.
    '김진화': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 능주목사 등을 역임한 문신.
    '김진후': {'role': 'other'},  # 조선 - 조선후기 신해박해 당시의 순교자.
    '김진흥': {'role': 'other'},  # 조선/조선 후기 - 조선후기 「대학장구」 · 「전해심경」 등을 전서로 쓴 역관이자 서예가.
    '김질': {'role': 'scholar'},  # 조선/조선 전기 - 조선 전기에, 효행으로 알려져 명종에게 표창을 받았으며, 『영모록』, 『육사자책설』 등을 저술한 학자.
    '김질간': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 대사간, 이조참판 등을 역임한 문신.
    '김질엽': {'role': 'other'},  # 근대 - 조선후기 「수궁가」로 널리 알려졌던 판소리의 명창.
    '김질충': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 도승지 등을 역임한 문신.
    '김집': {'role': 'scholar'},  # 조선 - 조선시대 이조판서, 좌참찬, 판중추부사 등을 역임한 문신. 학자.
    '김징': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 동부승지, 전라도관찰사 등을 역임한 문신.
    '김징악': {'role': 'other'},  # 고려/고려 전기 - 고려전기 다방태의소감를 역임한 의관.
    '김찬': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 대한독립군비단 참모장, 대한국민단 군사부장 등을 역임한 독립운동가.
    '김찬규': {'role': 'other'},  # 근대 - 일제강점기 때, 대동단 결성에 참여하였으며, 경상도 지방에 의용단을 조직해 군자금 모금 활동을 전개한 독립운동가.
    '김찬수': {'role': 'other'},  # 근대 - 일제강점기 때, 북로군정서에서 김좌진 휘하의 제3중대장을 역임한 독립운동가.
    '김찬순': {'role': 'other'},  # 근대 - 대한제국기 때, 전기홍 의진에서 도통장으로 활동한 의병.
    '김찬식': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 「작품」, 「정」, 「희」 등의 작품을 낸 조각가.
    '김찬업': {'role': 'other'},  # 근대 - 조선후기 박만순과 김세종의 제자로 흥선대원군의 아낌을 받았던 판소리의 명창.
    '김찬영': {'role': 'scholar'},  # 근대/일제강점기 - 일제강점기 「자화상」 · 「님프의 죽음」 등의 작품을 그린 화가. 문장가.
    '김창': {'role': 'other'},  # 고려 - 고려 후기에, 문하평장사, 수태사 문하시랑평장사 판이부사 등을 역임한 문신.
    '김창곤': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 광복단 국내파견원으로 활동하며 친일파 처단 및 군자금 모금 활동을 전개한 독립운동가.
    '김창균': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 대한독립단, 대한통의부 의용군에서 항일무장투쟁을 전개한 독립운동가.
    '김창근': {'role': 'other'},  # 현대 - 제6·7·8·10대 국회의원, 민추협 부의장, 교통부장관 등을 역임한 정치인.
    '김창남': {'role': 'other'},  # 남북국시대 때, 이찬 관등으로, 당나라에 사신으로 파견된 통일신라의 귀족 · 관리.
    '김창도': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 경종대에 목호룡의 고변으로 발생한 옥사 때에 죽임을 당한 인물.
    '김창락': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 「추경」 · 「사양」 등의 작품을 그린 화가.
    '김창록': {'role': 'other'},  # 근대 - 조선후기 「심청가」에 뛰어났던 판소리의 명창.
    '김창룡': {'role': 'other'},  # 1920~1956. 군인.
    '김창석': {'role': 'other'},  # 조선/조선 후기 - 조선후기 호남균전관을 역임한 관리.
    '김창섭': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 한국 서양화가 1세대이자 골동품 수장가. 서양화가.
    '김창수': {'role': 'scholar'},  # 조선/조선 후기 - 조선후기 「춘산만하도」, 「송천독경도」 등의 작품을 그린 화가.
    '김창숙': {'role': 'scholar'},  # 현대/대한민국 - 일제강점기 때, 파리만국평화회의에 한국의 독립을 호소하는 진정서를 제출하였으며, 서로군정서를 조직하여 활동한 학자...
    '김창술': {'role': 'poet'},  # 현대/대한민국 - 일제강점기 「여명의 설움」, 「아-지금은 첫겨울」, 「문열어라」 등을 저술한 시인.
    '김창시': {'role': 'other'},  # 조선/조선 후기 - 조선후기 홍경래의 난을 주동한 관리.
    '김창식': {'role': 'other'},  # 근대 - 일제강점기, 한국인 최초의 목사이자 한국 기독교 초기 전도인.
    '김창업': {'role': 'novelist'},  # 조선/조선 후기 - 조선후기 「추강만박도」 · 「우암송선생칠십사세진」 등의 작품을 그린 화가. 문인.
    '김창오': {'role': 'other'},  # 근대 - 대한제국기 때, 박기섭 의진에서 돌격장으로 활동한 의병장.
    '김창원': {'role': 'other'},  # 현대 - 해방 이후 주한튀니지 명예총영사, 신진학원 이사장 등을 역임한 경제인.
    '김창일': {'role': 'other'},  # 조선 - 조선 후기에, 동지중추부사 등을 역임한 문신.
    '김창조': {'role': 'other'},  # 조선/조선 후기 - 조선후기 「김창조가락 가야금산조」를 지은 거문고명인.
    '김창주': {'role': 'other'},  # 현대/대한민국 - 북한에서, 최고인민회의 대의원, 정무원 부총리 겸 농업위원장 등을 역임한 관료.
    '김창준': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「고성오광대」 전승자로 지정된 기예능보유자.
    '김창즙': {'role': 'scholar'},  # 조선 - 조선후기 왕자사부, 예빈시주부 등을 역임한 문신. 학자.
    '김창직': {'role': 'scholar'},  # 조선/조선 후기 - 조선 후기에, 사서, 문학 등을 역임한 문신.
    '김창집': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 우의정, 좌의정, 영의정 등을 역임한 문신.
    '김창하': {'role': 'other'},  # 조선/조선 후기 - 조선후기 가전악, 전악, 집박악사 등을 역임한 음악인.
    '김창학': {'role': 'other'},  # 현대 - 해방 이후 대한해협 해전 당시의 군인.
    '김창헌': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 통의부 헌병대장, 정의부 헌병대장, 조선혁명군 제4중대장 등을 역임한 군인 · 독립운동가.
    '김창현': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 조선독립단 황해도 지부를 조직하여 동지규합, 군자금 모금 활동 등을 전개한 독립운동가.
    '김창협': {'role': 'other'},  # 조선 - 조선 후기에, 병조참지, 예조참의, 대사간 등을 역임한 문신.
    '김창환': {'role': 'other'},  # 근대/개항기 | 근대/일제강점기 - 일제강점기 「송월학명」 · 「봉학도」 등을 그린 화가.
    '김창후': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「고성오광대」의 전승자로 인정된 예능보유자.
    '김창흡': {'role': 'scholar'},  # 조선 - 조선 후기에, 『삼연집』, 『심양일기』 등을 저술한 학자.
    '김창희': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 사헌부대사헌, 홍문관제학, 예문관제학 등을 역임한 문신.
    '김채만': {'role': 'other'},  # 근대 - 대한제국기 이날치의 제자로 창극단과 협률사에 참여한 판소리의 명창.
    '김채옥': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「진주검무」의 전승자로 지정된 예능보유자.
    '김처선': {'role': 'other'},  # 조선/조선 전기 - 조선전기 자헌대부를 역임한 환관.
    '김처암': {'role': 'other'},  # 조선 - 조선 후기에, 집의 등을 역임한 문신.
    '김처회': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 병부시랑, 납정절사 등을 역임한 관리.
    '김척명': {'role': 'novelist'},  # 고대/남북국/통일신라 - 남북국시대 통일신라에서 원광, 비허 등의 불교 사적을 정리한 문인.
    '김척후': {'role': 'other'},  # 고려 - 고려 후기에, 장군, 대장군, 초토처치병마중도사 등을 역임한 문신.
    '김천': {'role': 'other'},  # 고려/고려 후기 - 고려후기 몽고의 제6차 침입 당시 몽고군에게 포로로 잡혀간 모친을 구한 효자. 향리.
    '김천경': {'role': 'other'},  # 고려 - 고려 후기에, 중랑장 등을 역임한 무신 · 공신.
    '김천령': {'role': 'other'},  # 조선 - 조선 전기에, 집의 등을 역임한 문신.
    '김천록': {'role': 'other foreigner'},  # 고려 - 고려후기 삼별초의 난, 여몽연합군 일본정벌 등과 관련된 무신.
    '김천보': {'role': 'other'},  # 고려 - 고려 후기에, 동지밀직사사, 대사헌, 판도판서 등을 역임한 문신.
    '김천석': {'role': 'other'},  # 조선 - 조선 후기에, 군수 등을 역임한 문신.
    '김천성': {'role': 'other foreigner'},  # 근대 - 일제강점기 때, 중국에서 광복군 제5지대 간부 등을 역임하며 항일무장투쟁을 전개한 독립운동가.
    '김천수': {'role': 'other'},  # 근대 - 조선 후기에, 경주군수, 비서승, 규장각기주관 등을 역임한 문신.
    '김천애': {'role': 'other'},  # 현대/대한민국 - 해방 이후 경성음악학교 교수, 숙명여자대학교 성악과 교수 및 학장 등을 역임한 음악인. 성악가.
    '김천익': {'role': 'other'},  # 근대 - 일제강점기 때, 만주에서 한족회, 대한독립군 등에 가담하여 항일무장투쟁을 전개한 독립운동가.
    '김천일': {'role': 'other'},  # 조선 - 조선 중기에, 임진왜란이 발발하자 의병을 일으켜 군사활동을 전개하였으며, 수원부사, 장례원판결사 등을 역임한 관리 · 의병장.
    '김천존': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 삼국통일전쟁에 참전한 장수. 대신.
    '김천택': {'role': 'novelist'},  # 조선/조선 후기 - 조선후기 『청구영언』을 편찬한 가객. 시조작가.
    '김천흥': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 이왕직 아악부 아악수, 아악수장 등을 역임한 국악인.
    '김철': {'role': 'other'},  # 현대/대한민국 - 민족일보 논설위원, 통일사회당 대통령 후보 등을 역임한 정치인.
    '김철규': {'role': 'other'},  # 현대/대한민국 - 해방 이후 서울교구장 비서, 서울대교구 부주교(현 총대리) 등에 서임된 사제. 신부.
    '김철남': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 임시의정원 황해도 대표의원, 임시정부 교통부차장, 참모차장 등을 역임한 독립운동가.
    '김철산': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 건설자동맹, 고려공산청년동맹 등에서 사회주의 운동을 전개하다가 제1차 간도공산당 검거사건으로 체...
    '김철수': {'role': 'other'},  # 근대 - 일제강점기 때, 2·8독립선언을 주도하였으며, 조선청년회연합회 상무위원, 조선물산장려회 경리부원 등을 역임한 독립운동가.
    '김철준': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 「한국고대사회 연구」, 「한국문화사론」, 「한국문화전통론」 등을 저술한 학자. 역사학자.
    '김철훈': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 러시아공산당 한인지부 위원장, 전로한인공산당 위원장 등을 역임한 사회주의운동가.
    '김철희': {'role': 'other'},  # 근대 - 대한제국기 때, 경모궁제조, 궁내부특진관 등을 역임한 문신.
    '김첨': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 교리 등을 역임한 문신.
    '김첨경': {'role': 'other'},  # 조선 - 조선 전기에, 예조판서 등을 역임한 문신.
    '김첨수': {'role': 'other'},  # 고려 - 고려 후기에, 충혜왕이 원나라에 억류당했을 때 호종한 무신 · 공신.
    '김청': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 대사간 등을 역임하다 낙향하였으나 임진왜란이 발발하자 왕의 호위를 자청한 문신.
    '김청평': {'role': 'other foreigner'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 사찬으로 일본에 파견된 관리.
    '김체': {'role': 'other'},  # 고려 - 고려 후기에, 순안현령 등을 역임한 문신.
    '김체명': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 제39대 소성왕의 아들인 왕자.
    '김체신': {'role': 'other'},  # 고대/남북국/통일신라 - 신라 경덕왕, 혜공왕, 선덕왕 때 중앙 행정과 대일 외교 및 군사 분야에서 활약한 관료.
    '김초': {'role': 'other'},  # 고려 - 고려 후기에, 안동판관, 충청도안렴사, 성균박사 등을 역임한 문신.
    '김초정': {'role': 'other foreigner'},  # 고대/남북국/통일신라 - 남북국시대 통일신라에서 급찬으로서 일본에 파견된 사신.
    '김총': {'role': 'scholar'},  # 조선 - 조선후기 집의, 지제교, 옥구현감 등을 역임한 문신. 학자.
    '김최명': {'role': 'other foreigner'},  # 근대 - 일제강점기 때, 대한독립단과 광복군총영의 결사대원으로 활동하며 일제 기관 파괴 및 일본 고관 처단 등을 계획한 독립운동가.
    '김추월': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 이동백, 신금홍과 일본 와시표축음기에 춘향전 전집을 취입한 판소리의 명창.
    '김춘광': {'role': 'playwright novelist'},  # 근대/일제강점기 - 일제강점기 「검사와 여선생」, 「촌색시」 등의 작품을 낸 극작가.
    '김춘배': {'role': 'other'},  # 근대 - 일제강점기 때, 정의부에서 군자금 모금 활동을 전개한 독립운동가.
    '김춘수': {'role': 'novelist'},  # 해방 이후 『구름과 장미』, 『타령조 기타』, 『거울 속의 천사』 등을 저술한 문인.
    '김춘영': {'role': 'other'},  # 근대/개항기 - 개항기 임오군란 당시의 군인.
    '김춘지': {'role': 'other'},  # 현대 - 해방 이후 가야금산조 및 병창의 전승자로 지정된 예능보유자. 가야금연주자.
    '김춘질': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 신문왕이 감은사 창건 시 일관을 역임한 관리.
    '김춘택': {'role': 'scholar'},  # 조선/조선 후기 - 조선 후기에, 『북헌집』, 『만필』 등을 저술한 문신.
    '김춘희': {'role': 'other'},  # 근대/개항기 | 근대/일제강점기 - 일제강점기 성균관 대사성, 이조 참의, 이조 참판, 도승지, 황해도 관찰사 등을 역임한 관료. ...
    '김충': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 선공감정, 사성, 초계군수 등을 역임한 문신.
    '김충간': {'role': 'other'},  # 고려 - 고려 전기에, 병마녹사를 역임한 문신.
    '김충공': {'role': 'other'},  # 고대/남북국/통일신라 - 통일신라의 제44대 민애왕의 아버지로, 집사부시중, 상대등 등을 역임하였으며, 민애왕 즉위 후 선강대왕으로...
    '김충렬': {'role': 'other'},  # 조선 - 조선시대 효행으로 정려와 예물을 하사받은 효자.
    '김충복': {'role': 'other'},  # 현대/대한민국 - 현대, 한국 제과 · 제빵업 발전에 기여한 공로자.
    '김충선': {'role': 'other'},  # 조선 - 조선시대 가선대부, 자헌대부, 정헌대부 등을 역임한 무신.
    '김충신': {'role': 'other'},  # 고대/남북국/통일신라 - 통일신라의 제33대 성덕왕의 사촌동생으로, 당나라에 사신으로 가서 발해 토벌을 요청하였으며, 당에서 좌령군...
    '김충의': {'role': 'other'},  # 고려 - 고려후기 제26대 충선왕 때 악행으로 참형을 당한 관리.
    '김충찬': {'role': 'other'},  # 고려 - 고려 전기에, 우산기상시, 지충추원사 병부상서 등을 역임한 문신.
    '김충평': {'role': 'other foreigner'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 일길찬으로 일본에 파견된 관리.
    '김충현': {'role': 'scholar'},  # 현대 - 해방 이후 「윤봉길 열사 기의비」 · 「백범 김구 선생 묘비」 · 「사육신 묘비」 등의 작품을 낸 서예가.
    '김취기': {'role': 'other'},  # 고려 - 고려후기 호군, 군부판서 응양군 상호군 등을 역임한 무신.
    '김취려': {'role': 'other'},  # 고려/고려 후기 - 고려후기 평장사 판병부사, 평장사 판이부사, 문하시중 등을 역임한 무신.
    '김취로': {'role': 'other'},  # 조선 - 조선 후기에, 호조판서를 역임한 문신.
    '김취문': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 교리, 호조참의, 대사간 등을 역임한 문신.
    '김취성': {'role': 'scholar'},  # 조선 - 조선 전기에, 『진락당집』을 저술하였으며, 의학 연구를 통해 환자 치료에 힘쓴 학자.
    '김치': {'role': 'other'},  # 조선 - 조선 후기에, 경상도관찰사 등을 역임한 문신.
    '김치관': {'role': 'scholar'},  # 조선 - 조선 중기에, 벼슬에 뜻을 두지 않고 의성향교에서 후진 양성에 힘쓰며, 『역락재집』을 저술한 학자.
    '김치룡': {'role': 'other'},  # 조선 - 조선 후기에, 승지 등을 역임한 문신.
    '김치만': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 동몽교관, 시직 등을 역임한 문신.
    '김치보': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 러시아 연해주 블라디보스토크로 망명하여 성명회, 권업회, 대한국민의회 등에서 활동한 독립운동가.
    '김치선': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 서울대학교 법학연구소 소장, 서울대학교 법과대학 학장 등을 역임한 학자. 법학자.
    '김치양': {'role': 'other'},  # 고려/고려 전기 - 고려 전기 목종대에 반란을 일으킨 권신.
    '김치열': {'role': 'other'},  # 현대/대한민국 - 검찰총장, 법무부장관, 중앙정보부 차장 등을 역임하며 박정희 정부에서 핵심 세력으로 활동한 법조인 · 정치인.
    '김치영': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 『중학교 수학』, 『고교수학』, 『미분적분학』 등을 저술한 학자. 수학자.
    '김치운': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 장악원정, 봉상시정 등을 역임한 문신.
    '김치인': {'role': 'other'},  # 근대/개항기 - 개항기 일수 이복래를 교주로 추대하여 오방불교를 창립한 종교창시자.
    '김치정': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 재중국본부한인청년동맹, 무산자사, 노동계급사 등에서 활동한 사회주의운동가, 독립운동가.
    '김치홍': {'role': 'other'},  # 근대 - 대한제국기 때, 심남일 의진에서 기군장으로 활동한 의병.
    '김치후': {'role': 'other'},  # 조선 - 조선 후기에, 대사간, 정주목사 등을 역임한 문신.
    '김칠성': {'role': 'other'},  # 현대/대한민국 - 일제강점기 때, 김천청년연맹 집행위원, 부산청년동맹 집행부에서 활동하며 독립운동 자금 지원 활동을 수행하였으며, ...
    '김타업': {'role': 'other'},  # 현대/대한민국 - 국가무형문화유산 밀양 백중놀이의 상쇠 부문 보유자로 인정된 악사이자 밀양 지역의 상례 의식춤인 휘쟁이춤을 전승한 ...
    '김탄행': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 첨지중추부사를 역임한 문신.
    '김탕': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 파리강화회의에 참석하기 위해 대한민국임시정부 대표로 파견되어 외교활동을 벌인 독립운동가 · 외교관.
    '김태곤': {'role': 'scholar'},  # 현대/대한민국 - 원광대학교와 경희대학교의 교수로 재임하여 민속학연구소장 등을 역임하였으며, 『한국민간신앙연구』, 『한국민속학원론』...
    '김태균': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 간도 용정촌에서 전개된 독립만세시위를 주도하는 과정에서 순국한 독립운동가.
    '김태기': {'role': 'other'},  # 조선 - 조선 후기에, 영광군수를 역임한 문신.
    '김태동': {'role': 'other'},  # 현대/대한민국 - 경제기획원 차관, 체신부 · 보건사회부 장관 등을 역임한 관료 · 친일반민족행위자.
    '김태렴': {'role': 'other foreigner'},  # 고대/남북국/통일신라 - 통일신라 경덕왕 때, 대규모 사절단을 이끌고 일본에 방문한 왕족.
    '김태서': {'role': 'other'},  # 고려 - 고려 후기에, 한림학사, 문하시랑평장사 등을 역임한 문신.
    '김태석': {'role': 'other'},  # 근대/일제강점기 - 대한제국기 「승사인보」 · 「청유인보」 등을 제작한 서예가. 전각가.
    '김태선': {'role': 'other'},  # 현대/대한민국 - 해방 이후 내무부치안국장, 서울시장, 내무부장관 등을 역임한 관료.
    '김태섭': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「종묘제례악」 전승자로 지정된 기예능보유자.
    '김태수': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 및 8·15광복 후 충청북도 영동 지역애서 활동한 사회주의운동가.
    '김태숙': {'role': 'other'},  # 근대/일제강점기 | 현대 - 해방 이후 한국자수협회 회장을 역임한 공예가. 자수공예가.
    '김태식': {'role': 'other'},  # 근대 - 해방 이후 서울대학교 체육담당 교수, 대한수상경기연맹 부회장 등을 역임한 체육인. 교육자.
    '김태암': {'role': 'other'},  # 조선 - 조선 후기에. 찰방 등을 역임한 무신 · 공신.
    '김태연': {'role': 'other'},  # 근대 - 일제강점기 때, 대한통의부 국내파견 결사대장으로 활동하였고, 정의부, 신민부 등에서 항일투쟁을 전개한 독립운동가.
    '김태영': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 국내에서 활동한 사회주의운동가.
    '김태오': {'role': 'poet childrenauthor scholar'},  # 현대/대한민국 - 일제강점기 「새벽」, 「소리소리 무슨 소리」, 「가을하늘 휘파람」 등을 저술한 시인. 아동문학가, 심리학자.
    '김태운': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 경기민요와 잡가로 활약한 경기소리의 명창.
    '김태원': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 때, 벽창의용단을 조직하여 군자금 모금, 일본경찰 및 밀정 처단 등의 항일투쟁을 전개한 독립운동가.
    '김태일': {'role': 'scholar'},  # 조선 - 조선 후기에, 문학, 보덕, 사간 등을 역임한 문신.
    '김태정': {'role': 'other'},  # 조선 - 조선 전기에, 진사, 전라도관찰사 등을 역임한 문신.
    '김태제': {'role': 'other'},  # 근대 - 조선 후기에, 사직서제조, 비서원승, 태의원경 등을 역임한 문신.
    '김태준': {'role': 'scholar'},  # 근대 - 일제강점기 『조선한문학사』, 『조선소설사』, 『조선가요집성』 등을 저술한 학자. 사상가.
    '김태진': {'role': 'playwright novelist'},  # 근대/일제강점기 - 일제강점기 「개척자」, 「풍운아」, 「낙원을 찾는 무리들」 등에 출연한 배우. 극작가, 연극연출가, 친일반민족행위자.
    '김태허': {'role': 'other'},  # 조선 - 조선 중기에, 밀양부사, 울산군수, 당상관, 지중추부사 등을 역임한 무신 · 공신.
    '김태현': {'role': 'other'},  # 고려 - 고려 후기에, 평장사, 상서우승, 첨의정승 등을 역임한 문신.
    '김태호': {'role': 'other'},  # 현대/대한민국 - 해방 이후 경기도지사, 국회의원 등을 역임한 정치인. 관료.
    '김태홍': {'role': 'poet'},  # 현대/대한민국 - 해방 이후 『땀과 장미와 시』ㆍ『공』ㆍ『훗날에도 가을에는』 등을 저술한 시인.
    '김태희': {'role': 'other'},  # 근대/일제강점기 | 현대 - 해방 이후 「칠장」 전승자로 지정된 기능보유자. 나전칠기명인.
    '김택': {'role': 'other'},  # 조선 - 조선 전기에, 학유, 박사, 감찰 등을 역임한 문신.
    '김택규': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 『동족부락의 생활구조연구』, 『한국민속문예론』 등을 저술한 학자. 문화인류학자.
    '김택룡': {'role': 'other'},  # 조선 - 조선 중기에, 전적, 도사 등을 역임한 문신.
    '김택수': {'role': 'other'},  # 현대/대한민국 - 해방 이후 국민체육진흥재단 이사장, 국제올림픽위원회 위원 등을 역임한 체육인. 정치인.
    '김택술': {'role': 'other'},  # 현대/대한민국 - 대한노총연맹 전라북도 부위원장, 제2·3대 국회의원 등을 역임한 정치인.
    '김택영': {'role': 'scholar'},  # 근대 - 조선 후기부터 일제강점기를, 살아가며 우리나라 역사 서술 및 한문학 유산 정리에 힘쓴 학자.
    '김택현': {'role': 'other'},  # 현대/대한민국 - 해방 이후 대한변호사협회 회장, 공직자윤리위원회 위원 등을 역임한 법조인.
    '김토': {'role': 'other'},  # 조선/조선 전기 - 조선전기 전의주부, 전의감승 등을 역임한 의관.
    '김통': {'role': 'other'},  # 조선 - 조선 전기에, 정언, 성균관직강, 예조정랑 등을 역임한 문신.
    '김통정': {'role': 'other'},  # 고려/고려 후기 - 고려후기 진도의 삼별초의 항쟁과 관련된 무신.
    '김판술': {'role': 'other'},  # 현대/대한민국 - 농림부 농정과 과장, 농민부 차장, 민의원, 보건사회부장관, 국회의원 등을 역임한 정치인.
    '김팔원': {'role': 'other'},  # 조선 - 조선 전기에, 전적, 예조좌랑, 용궁현감 등을 역임한 문신.
    '김평': {'role': 'other'},  # 고려 - 고려 후기에, 국자대사성, 추밀원 부사, 추밀원사 등을 역임한 문신.
    '김평묵': {'role': 'scholar'},  # 근대 - 조선 후기에, 『중암선생문집』, 『구곡문답』, 『척양대의』 등을 저술한 학자.
    '김평손': {'role': 'novelist'},  # 조선 - 조선시대 강변칠우에 속한 문인.
    '김평식': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 대한독립단 총무부장, 의군부 정무총감 등을 역임한 독립운동가.
    '김포질': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라에서 사찬으로서 당나라에 파견된 사신.
    '김표석': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 때, 이찬 관등으로 당나라에 파견된 통일신라의 관리.
    '김품석': {'role': 'other'},  # 고대/삼국/신라 - 신라의 제29대 왕, 태종 무열왕의 사위로, 대야성군주를 역임하여 백제의 침입에 대응하고자 하였으나, 부하 검일...
    '김풍나': {'role': 'other foreigner'},  # 고대/남북국/통일신라 - 남북국시대 통일신라에서 일본에 사신으로 다녀온 왕자 충원(忠元)의 호송원.
    '김풍익': {'role': 'other'},  # 현대 - 한국전쟁 당시 경기도 이천의 의정부지역전투에 참전한 군인.
    '김풍후': {'role': 'other'},  # 남북국시대 통일신라의 하정사로 당나라에 파견된 관리.
    '김풍훈': {'role': 'scholar'},  # 고대/남북국/통일신라 - 남북국시대 때, 숙위학생으로 당나라에서 유학하다가 아버지의 처형 소식을 듣고 당나라 군사의 향도가 되어 신...
    '김필': {'role': 'other foreigner'},  # 남북국시대 통일신라의 사찬으로 일본에 파견된 관리.
    '김필덕': {'role': 'other foreigner'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 일길찬으로 일본에 파견된 관리.
    '김필례': {'role': 'other'},  # 근대 - 해방 이후 정신여자중학교 교장, 정신학원 이사장 등을 역임한 교육자. 지도자.
    '김필순': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 만주에서 독립운동가 주치의로 활동하며 독립군을 치료하고, 병원 수입을 독립군의 군자금으로 기부한...
    '김필월': {'role': 'novelist'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 「성덕대왕신종명」을 지은 문인.
    '김필진': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 평시서령, 원성현감 등을 역임한 문신.
    '김하': {'role': 'other'},  # 조선 - 조선 전기에, 공조판서를 역임한 문신.
    '김하건': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 일본의 미술문화협회 회원으로 활동한 화가. 서양화가.
    '김하구': {'role': 'scholar'},  # 근대 - 해방 이후 「고대문화사」, 「세계문화사」 등을 저술한 학자. 역사학자.
    '김하득': {'role': 'other'},  # 현대/대한민국 - 해방 이후 부산교육대학 초대학장, 부산시교육회 회장 등을 역임한 교육자.
    '김하락': {'role': 'other'},  # 근대/개항기 - 개항기 때, 이천에서 의병을 일으켜 각 군 도지휘, 군사 겸 지휘 등으로 활동한 의병.
    '김하명': {'role': 'other'},  # 조선 - 조선 후기에, 용양위부호군, 돈녕부도정 등을 역임한 문신.
    '김하석': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 대한국민의회의 군정부장, 임시고려혁명군정의회 의장 등을 역임한 사회주의운동가.
    '김하재': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 대사헌, 동지경연사, 이조참판 등을 역임한 문신.
    '김하정': {'role': 'scholar'},  # 조선 - 조선 후기에, 춘추관편수관, 예조정랑, 영해부사 등을 역임하였으며, 『제례질의』, 『선집록』 등을 저술한 문신.
    '김하종': {'role': 'scholar'},  # 조선 - 조선후기 「장안사」 · 「철종철인후가례도감의궤도」 등의 작품을 그린 화가.
    '김학규': {'role': 'other'},  # 근대 - 일제강점기 때, 조선혁명당 군사령부참모장, 조선민족혁명당 국민부장, 한국광복군 총사령참모 등을 역임한 정치인 · 독립운동가.
    '김학기': {'role': 'other'},  # 조선 - 조선 전기에, 집의, 사옹원정, 대제학 등을 역임한 문신.
    '김학렬': {'role': 'other'},  # 현대/대한민국 - 해방 이후 재무부장관, 대통령수석정무비서관, 경제기획원 장관 등을 역임한 관료. 행정가, 경제관료.
    '김학무': {'role': 'other'},  # 근대 - 일제강점기 때, 조선의용대 지도위원, 화북조선독립동맹 선전부 부장, 화북조선청년혁명학교 교무주임 등을 역임한 독립운동가.
    '김학배': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 예조좌랑, 성균관교정관 등을 역임한 문신.
    '김학섭': {'role': 'other'},  # 근대 - 일제강점기 때, 대한독립군결사대를 조직하여 항일무장투쟁을 전개한 독립운동가.
    '김학성': {'role': 'scholar'},  # 근대 - 해방 이후 「새로운 맹세」 · 「오발탄」 · 「아리랑」 등의 작품에 관여한 영화인. 영화촬영감독.
    '김학수': {'role': 'other'},  # 근대/일제강점기 | 현대 - 해방 이후 「삼강행실도」 · 「능행도」 · 「한강전도」 등을 그린 화가. 한국화가 · 역사풍속화가.
    '김학순': {'role': 'other foreigner'},  # 현대/대한민국 - 대한민국의 여성운동가로, 1991년 일본군 위안부 피해 사실을 한국인 최초로 공개 증언한 인물.
    '김학연': {'role': 'other'},  # 근대/일제강점기 - 일제강점기, 북간도 명동학교의 교원으로 활동한 교육자.
    '김학우': {'role': 'other'},  # 근대 - 개항기 전운서낭청, 내무부참의직, 법무아문대신서리 등을 역임한 관료.
    '김학준': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 「소녀」, 「하코네 풍경」, 「바다」 등을 그린 화가. 서양화가.
    '김학진': {'role': 'other'},  # 근대/개항기 | 근대/일제강점기 - 일제강점기 홍문관 학사, 궁내부 특진관, 시종원경 등을 역임한 관료. 친일반민족행위자.
    '김학철': {'role': 'novelist'},  # 현대 - 해방 이후 연변에서 『격정시』 · 『해란강아 말하라』 등을 저술한 소설가.
    '김한': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 상하이 대한민국임시정부 사법부장, 무산자동지회 상무위원 등을 역임한 사회주의운동가, 독립운동가.
    '김한계': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 승문원교리, 승정원부승지, 정언 등을 역임한 문신.
    '김한구': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 영조의 장인으로 어영대장을 지낸 문신.
    '김한귀': {'role': 'other'},  # 고려 - 고려후기 동경도병마사, 감찰대부 등을 역임한 무신.
    '김한기': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 지중추부사 등을 역임한 문신.
    '김한동': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 대사간, 승지 등을 역임한 문신.
    '김한로': {'role': 'other'},  # 조선 - 조선 전기에, 판한성부사, 예조판서, 의정부찬성 등을 역임한 문신.
    '김한록': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 세자익위사세마를 역임한 문신.
    '김한룡': {'role': 'other'},  # 고려 - 고려 후기에, 전첨, 판전교시사 등을 역임한 문신 · 공신.
    '김한섭': {'role': 'scholar'},  # 조선 - 조선 후기에, 「통화변답, 「농정신서서조변」, 『오남문집』 등을 저술한 학자.
    '김한수': {'role': 'other'},  # 현대 - 해방 이후 중앙합성섬유주식회사, 한일합성섬유주식회사 등을 설립한 실업가.
    '김한신': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 오위도총부총관, 제용감제조 등을 역임한 문신.
    '김한종': {'role': 'other'},  # 근대 - 일제강점기 때, 대한광복회를 조직하여 군자금을 모금하고 친일파를 처단하는 등 항일무장투쟁을 전개한 독립운동가.
    '김한진': {'role': 'other'},  # 고려 - 고려 후기에, 순성보절공신, 호종일등공신, 경성수복일등공신 등에 책록된 문신 · 공신.
    '김한철': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 함경도관찰사, 대사헌, 우참찬 등을 역임한 문신.
    '김한충': {'role': 'other'},  # 고려 - 고려 전기에, 중군병마사, 추밀원사, 상서좌복야 등을 역임한 문신.
    '김함': {'role': 'other'},  # 고려/고려 전기 - 고려 전기에, 어서검토관, 지호부사, 호부상서 등을 역임한 문신.
    '김항': {'role': 'scholar'},  # 근대 - 조선 후기에, 『주역』을 풀이하여 한국식으로 체계화한 역학의 대가로, 『정역』을 주창한 학자.
    '김항나': {'role': 'other foreigner'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 아찬으로서 일본에 파견된 사신.
    '김해': {'role': 'other'},  # 조선 - 조선 중기에, 승문원정자, 예문관검열 등을 역임하였으며, 임진왜란이 발발하자 영남의병대장으로 추대되어 항쟁한 문신 · 의병장.
    '김해강': {'role': 'poet'},  # 현대 - 해방 이후 『동방서곡』, 『기도하는 마음』 등을 저술한 시인.
    '김해랑': {'role': 'other'},  # 현대 - 해방 이후 한국무용예술인협회 초대 이사장 및 회장을 역임한 무용가. 한국무용가.
    '김해성': {'role': 'other foreigner'},  # 근대 - 일제강점기 때, 중국에서 한국청년전지공작대에 입대하여 정보 수집, 초모공작 등의 활동을 전개한 독립운동가.
    '김해송': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 「연락선은 떠난다」 · 「잘있거라 단발령」 등을 부른 가수. 작곡가.
    '김해수': {'role': 'other'},  # 조선 - 조선 후기에, 제용감직장, 현감 등을 역임한 문신.
    '김해일': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 승지, 경주부윤 등을 역임한 문신.
    '김행': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 광주목사 등을 역임한 문신.
    '김행경': {'role': 'other'},  # 고려 - 고려 전기에, 판상서병부사, 문하시랑동중서문하평장사 등을 역임한 문신.
    '김행공': {'role': 'other'},  # 고려 - 고려 전기에, 거란 흥종의 즉위를 축하하는 사신으로 파견된 문신.
    '김행도': {'role': 'other'},  # 고려 - 고려 전기에, 광평시중, 동남도초토사, 지아주제군사 등을 역임한 문신.
    '김행파': {'role': 'other'},  # 고려 - 고려전기 대광을 역임한 호족.
    '김향': {'role': 'other'},  # 고려/고려 전기 - 고려 전기에, 검교태위수사공, 참지정사 등을 역임한 문신.
    '김헌경': {'role': 'other'},  # 근대 - 대한제국기 때, 관동의진에서 창의대장으로 활동한 의병장.
    '김헌기': {'role': 'scholar'},  # 조선 - 조선 후기에, 『논어설』, 『초암집』, 『충서설』 등을 저술한 학자.
    '김헌장': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 때, 진위사로 당나라에 파견된 통일신라의 왕족.
    '김헌정': {'role': 'other'},  # 고대/남북국/통일신라 - 통일신라의 제43대 희강왕의 아버지로, 시중, 국상, 병부령 겸 수성부령 등을 역임한 왕족.
    '김헌창': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 시중, 청주도독, 웅주도독 등을 역임한 귀족. 반란자.
    '김헌충': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 때, 시비서감 등을 역임하였으며, 숙위로 당나라에 파견된 통일신라의 왕족.
    '김혁': {'role': 'other'},  # 근대 - 일제강점기에 만주에서 흥업단 부단장 · 대한독립군단 군사부장 · 신민부 중앙집행위원장 · 성동사관학교 교장 등을 역임한 독...
    '김혁정': {'role': 'other'},  # 고려/고려 후기 - 고려후기 야별초지유, 충청도안찰사 등을 역임한 관리. 무신.
    '김현': {'role': 'critic scholar foreigner'},  # 현대/대한민국 - 해방 이후 『프랑스 비평사』, 『문학사회학』 등을 저술한 학자. 문학평론가.
    '김현구': {'role': 'poet'},  # 근대 - 일제강점기 「거룩한 봄과 슬픈 봄」, 「풀 우에 누워」, 「내마음 사는 곳」 등을 저술한 시인.
    '김현기': {'role': 'other'},  # 현대/대한민국 - 제7~10대 국회의원, 신민당 중앙상임위원 등을 역임한 정치인.
    '김현도': {'role': 'other'},  # 조선 - 조선 중기에, 해주목사, 양재찰방 등을 역임한 문신.
    '김현배': {'role': 'other'},  # 현대/대한민국 - 1947년에서 1960년까지, 제3대 전주교구장으로 사목한 천주교 사제.
    '김현보': {'role': 'other'},  # 고려/고려 후기 - 고려후기 최우의 심복으로 상장군을 역임한 관리. 무신.
    '김현성': {'role': 'other'},  # 조선 - 조선시대 봉상시주부, 양주목사, 동지돈녕부사 등을 역임한 서화가.
    '김현숙': {'role': 'other'},  # 현대/대한민국 - 해방 이후 육군본부 여군부장, 여군훈련소 소장, 대령 등을 역임한 군인.
    '김현승': {'role': 'poet'},  # 현대/대한민국 - 광복 이후 『김현승시초』, 『옹호자의 노래』, 『견고한 고독』등을 저술한 시인.
    '김현옥': {'role': 'other'},  # 현대/대한민국 - 육군제3항만사령관, 서울시장, 내무부장관 등을 역임한 군인 · 정치인.
    '김현우': {'role': 'scholar'},  # 조선/조선 후기 - 조선후기 「연파고주도」, 「신선도」 등의 작품을 그린 화가.
    '김현일': {'role': 'other'},  # 현대/대한민국 - 해방 이후 고성지구 근접항공지원작전 당시의 군인.
    '김현준': {'role': 'scholar'},  # 근대/일제강점기 | 현대 - 한국의 첫 신문학 박사로, 성균관대학교 학장과 조선대학교 문리학부장 등을 역임하였으며, 『사회학개론』 ...
    '김현철': {'role': 'other'},  # 현대/대한민국 - 재무부장관, 경제기획원장관, 주미대사 등을 역임한 관료 · 외교관.
    '김현태': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 『판례, 학설주석민법』, 『민법총칙』, 『불법행위론』 등을 저술한 학자. 법학자.
    '김형규': {'role': 'scholar'},  # 해방 이후 『국어학개론』, 『국어사』, 『한국방언연구』 등을 저술한 학자. 국어학자.
    '김형근': {'role': 'other'},  # 현대 - 해방 이후 대검찰청검사, 서울지방검찰청 검사장, 중앙선거관리위원 헌법위원회 헌법위원 등을 역임한 법조인. 관료.
    '김형남': {'role': 'other'},  # 현대/대한민국 - 해방 이후 숭실대학교 초대 총장 , 이사장 등을 역임한 교육자.
    '김형래': {'role': 'other'},  # 현대/대한민국 - 일제강점기 「맹강녀」 · 「카추샤」 · 「가면무도회」 등을 만든 작곡가.
    '김형렬': {'role': 'other'},  # 근대 - 일제강점기 금산사에 미륵불교를 설립한 종교창시자.
    '김형빈': {'role': 'other foreigner'},  # 근대 - 일제강점기 때, 중국에서 독립단에 입단하여 군자금 모금 활동을 전개한 독립운동가.
    '김형선': {'role': 'other'},  # 근대 - 해방 이후 조선인민공화국 경제부장 대리, 남조선노동당 중앙감찰위원회 부위원장 등을 역임한 사회주의운동가.
    '김형섭': {'role': 'other'},  # 근대 - 대한제국기 혁명일심회 사건 당시의 군인.
    '김형순': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 미국에서 대한인국민회를 중심으로 독립운동을 후원한 기업인.
    '김형욱': {'role': 'other'},  # 국가재건최고회의 최고위원, 중앙정보부장 등을 역임하며 박정희 체제 유지에 결정적인 역할을 하였으나, 유신체제 선포 이후 의원직을 상...
    '김형원': {'role': 'poet'},  # 근대/일제강점기 - 일제강점기 「이향」, 「아 지금은 새벽 네시」, 「불순의 피」 등을 저술한 시인. 언론인.
    '김형익': {'role': 'other'},  # 근대/일제강점기 | 현대 - 해방 이후 대한적십자사 서울지사장, 대한나관리협회 이사 등을 역임한 의사.
    '김형일': {'role': 'other'},  # 현대/대한민국 - 연합참모본부장, 국방부장관 특별보좌관, 국회의원 등을 역임한 군인 · 정치인.
    '김형재': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 동흥학교 교원, 대동공보 하얼빈지국장 등을 역임하였으며, 안중근의 의거에 가담한 독립운동가.
    '김형준': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 「봉선화」 · 「저 구름의 탓」 · 「나물 캐는 처녀」 등을 작사한 음악인. 교육자 · 관악연주자 ·...
    '김형직': {'role': 'other'},  # 현대/대한민국 - 북한의 통치자 김일성의 아버지로 북한에서는 일제강점기 비밀결사단체인 조선국민회에 가입하여 활동하였다고 선전하는 숭...
    '김혜손': {'role': 'scholar'},  # 조선/조선 전기 - 조선 전기에, 군수 등을 역임한 학자.
    '김호': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 만주와 러시아 연해주에서 활동하며 대한독립단, 광정단, 정의부 등에서 무장투쟁을 전개한 독립운동가.
    '김호길': {'role': 'scholar'},  # 현대 - 포항공과대학의 설립을 주도하며 한국의 과학교육에 힘쓴 물리학자 · 교육자.
    '김호룡': {'role': 'scholar foreigner'},  # 근대/일제강점기 - 일제강점기 일본식 외광파(外光派)의 영향을 강하게 드러낸 작품을 그린 화가. 서양화가.
    '김호반': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 경상남도 지역을 기반으로 사회주의운동을 전개한 독립운동가.
    '김호석': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 만주에서 조선혁명군 총사령, 조선혁명군 정부 군사부 부장 등을 역임한 독립운동가.
    '김호식': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 『발효공학』, 『발효미생물학』 등을 저술한 학자. 교육자.생물학자.
    '김호준': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 경상남도 합천군 독립만세시위로 체포된 구금자의 석방을 위해 결사대를 조직하여 시위를 전개하다가 ...
    '김호직': {'role': 'scholar'},  # 현대 - 해방 이후 『소맥분 보강에 대한 연구』, 『콩단백에 관한 연구』 등을 저술한 학자. 교육자.
    '김호현': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 경상남도 창원의 삼진 만세운동에 참여했다가 순국한 독립운동가.
    '김혼': {'role': 'other'},  # 고려/고려 후기 - 고려 후기, 찬성사 · 우중찬 · 판삼사사 등을 역임하고, 낙랑군, 계림부원군에 봉해진 문신.
    '김홍경': {'role': 'other'},  # 조선 - 조선 후기에, 청송부사, 진산군수, 오위의 호군 등을 역임한 문신.
    '김홍근': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 의정부좌참찬, 좌의정, 판중추부사 등을 역임한 문신.
    '김홍기': {'role': 'other'},  # 현대/대한민국 - 해방 이후 서울대학교병원 병원장, 인천길병원 병원장 등을 역임한 의료인.
    '김홍도': {'role': 'scholar'},  # 조선 - 조선후기 「군선도병」 · 「단원풍속화첩」 · 「무이귀도도」 등의 작품을 그린 화가.
    '김홍량': {'role': 'other'},  # 근대 - 대한제국기 양산중학교를 설립하여 교육구국운동을 지도한 교육자. 사회운동가.
    '김홍렬': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 전라북도 옥구의 독립만세시위를 주도한 혐의로 체포되었으며, 출옥 이후에도 비밀결사를 조직하여 항...
    '김홍륙': {'role': 'other foreigner'},  # 근대/대한제국기 - 대한제국기 러시아어 통역관을 역임한 관료. 역관.
    '김홍미': {'role': 'other'},  # 조선 - 조선 중기에, 승문원부제조, 청송부사, 강릉부사 등을 역임한 문신.
    '김홍민': {'role': 'other'},  # 조선 - 조선 중기에, 삼사, 이조좌랑, 전한 등을 역임한 문신.
    '김홍복': {'role': 'other'},  # 조선 - 조선 후기에, 예조참의, 여주목사, 대사간 등을 역임한 문신.
    '김홍빈': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 1919년 4월 1일 평안북도 창성군에서 일어난 만세 시위운동을 주도하고, 1920년 대한민국임시정부...
    '김홍서': {'role': 'other'},  # 근대/일제강점기 - 대한민국임시의정원 의원을 역임하고 한국독립당과 조선민족혁명당에서 활동한 독립운동가.
    '김홍석': {'role': 'other'},  # 조선 - 조선 후기에, 수찬, 부교리, 교리 등을 역임한 문신.
    '김홍섭': {'role': 'other'},  # 현대/대한민국 - 해방 이후 서울지방법원 판사, 지방법원장, 대법원 판사 등을 역임한 법조인.
    '김홍수': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 『노동법학』, 『행정법』, 『행정재판제도연구』 등을 저술한 학자. 법학자.
    '김홍술': {'role': 'other'},  # 고려/고려 전기 - 신라 말과 고려 초, 진보성 성주 및 의성부 성주를 역임한 장군.
    '김홍식': {'role': 'other'},  # 현대 - 해방 이후 사법위원, 법제처 차장, 무임소장관 등을 역임한 법조인. 관료.
    '김홍욱': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 황해도관찰사 등을 역임하였으며, 효종에게 소현세자의 부인인 민회빈 강씨의 억울함을 풀어줄 것을 상...
    '김홍운': {'role': 'scholar'},  # 조선 - 조선 후기에, 「의로가」, 「안택사」, 『동곡집』 등을 저술한 학자.
    '김홍윤': {'role': 'other'},  # 조선 - 조선 전기에, 대사헌, 경기도관찰사 등을 역임한 문신.
    '김홍익': {'role': 'scholar'},  # 조선 - 조선시대 공조좌랑, 연산현감 등을 역임한 문신. 학자.
    '김홍일': {'role': 'other'},  # 일제강점기 때, 한국독립군, 국민혁명군 등에서 활동하였고, 이봉창과 윤봉길의 의거에 사용할 폭탄을 제작하였으며, 해방 이후, 육군사...
    '김홍집': {'role': 'other'},  # 개항기 당상경리사, 독판교섭통상사무, 좌의정 등을 역임한 관리. 정치인.
    '김홍취': {'role': 'other'},  # 고려/고려 후기 - 고려후기 출배도감 별감, 대장군, 상장군 등을 역임한 무신.
    '김화경': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「해와 초가」를 그린 화가.
    '김화랑': {'role': 'novelist'},  # 현대/대한민국 - 일제강점기 「드메」 · 「수선화」 · 「집없는 천사」 등의 작품을 낸 작가. 시나리오작가 · 영화감독 · 방송작가...
    '김화산': {'role': 'poet critic'},  # 근대 - 일제강점기 「뇌동성 문학론의 극복」, 「마르크스주의의 문학론 음미」 등을 저술한 평론가. 시인.
    '김화숭': {'role': 'other'},  # 고려/고려 전기 - 고려 전기에, 동북면병마부사, 어사중승, 한림학사 등을 역임한 문신.
    '김화식': {'role': 'other'},  # 근대 - 일제강점기 안주 동부교회, 평양창동교회 등에서 목회활동을 한 목사. 정치인.
    '김화준': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 주서, 설서, 석성현감 등을 역임한 문신.
    '김화진': {'role': 'other'},  # 조선 - 조선 후기에, 사은사, 이조판서, 판중추부사 등을 역임한 문신.
    '김확': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 철원부사 등을 역임한 문신.
    '김환': {'role': 'other'},  # 조선 - 조선후기 기사환국과 관련된 무신.
    '김환기': {'role': 'scholar'},  # 「향(響)」, 「월광」, 「영원의 노래」, 「산월」, 「무제」, 「어디서 무엇이 되어 다시 만나랴」 등의 작품을 그린 화가.
    '김환식': {'role': 'other'},  # 현대/대한민국 - 전북특별자치도 고창 출신으로 한국의 대표적인 제과 제빵 장인.
    '김환태': {'role': 'critic'},  # 근대 - 일제강점기 「문예시평」, 「예술의 순수성」, 「문학의 성격과 시대」 등을 저술한 평론가.
    '김활란': {'role': 'other'},  # 일제강점기 대한여자기독교청년회연합회 재단이사장 · 대한기독교교육자협회 회장 등을 역임한 개신교인. 교육인 · 친일반민족행위자.
    '김황': {'role': 'scholar'},  # 현대/대한민국 - 일제강점기 때, 김창숙과 함께 파리장서사건을 도모하는 등 독립운동에 힘쓰며 도학 정립과 후진 양성에 전념한 학자 ...
    '김황원': {'role': 'poet'},  # 고려 - 고려전기 예부시랑, 한림학사 등을 역임한 문신. 시인.
    '김회': {'role': 'scholar'},  # 조선 - 조선시대 성균관박사, 사헌부감찰 등을 역임한 문신. 학자.
    '김회련': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 검교한성윤 등을 역임한 문신 · 공신.
    '김회연': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 승지, 예조참의 등을 역임한 문신.
    '김회일': {'role': 'other'},  # 현대/대한민국 - 북한에서, 최초로 시작된 대중적 증산운동인 건국사상총동원운동의 상징으로 받아들여졌으며, 교통상, 중앙인민위 경제정...
    '김효거': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 의주부사 등을 역임한 문신.
    '김효건': {'role': 'other'},  # 조선 - 조선 후기에, 여주목사, 양주목사, 한성부판윤 등을 역임한 문신.
    '김효대': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 공조판서 등을 역임한 문신.
    '김효방': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라 제37대 선덕왕의 부친인 귀족.
    '김효석': {'role': 'other'},  # 현대/대한민국 - 내무부장관, 평화통일촉진협의회 상무위원 등을 역임한 정치인.
    '김효성': {'role': 'other'},  # 조선 - 조선 후기에, 목사, 조사오위장 등을 역임한 문신.
    '김효손': {'role': 'other'},  # 조선 - 조선 전기에, 참판, 대사헌 등을 역임한 문신.
    '김효숙': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 한국광복군 제2지대에 종군하여 대일 심리전을 펼쳤던 독립운동가.
    '김효순': {'role': 'other'},  # 조선 - 조선시대 예빈참봉, 당상역관, 한성판윤 등을 역임한 역관.
    '김효양': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라 제38대 원성왕의 부친인 귀족.
    '김효원': {'role': 'other foreigner'},  # 남북국시대 통일신라의 고애사(告哀使)로 일본에 파견된 관리.
    '김효인': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 전중시어사, 상서좌승, 병부상서 등을 역임한 문신.
    '김효정': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 사헌부감찰, 이조판서 등을 역임한 문신.
    '김효종': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 집사성 시중을 역임한 화랑. 대신.
    '김후': {'role': 'other'},  # 조선 - 조선 후기에, 부수찬 겸 금위영종사, 대사간 등을 역임한 문신.
    '김후근': {'role': 'other'},  # 조선 - 조선 후기에, 개령현감 등을 역임한 문신.
    '김후신': {'role': 'scholar'},  # 조선/조선 후기 - 조선후기 「산수도」 · 「야압도」 등의 작품을 그린 화가.
    '김후직': {'role': 'other'},  # 고대/삼국/신라 - 신라의 제22대 지증왕의 증손으로, 이찬에 임명되었으며, 병부령 등을 역임한 종실.
    '김후진': {'role': 'scholar'},  # 조선 - 조선 중기에, 경학과 역학을 연구하였으며, 고종때 호조참판에 추증된 학자.
    '김훈': {'role': 'other'},  # 현대/대한민국 - 해방 이후 기획처장, 상공부장관 등을 역임한 관료.
    '김훈영': {'role': 'other'},  # 고대/남북국/통일신라 - 통일신라의 제46대 문성왕의 종숙으로, 문성왕이 창림사 무구정탑을 건립할 때 동감수조사로서 참여한 종실.
    '김훈입': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라 제38대 원성왕의 조부인 귀족.
    '김훤': {'role': 'scholar'},  # 고려/고려 후기 - 고려 후기, 정당문학 · 보문각 대학사 · 동수국사 등을 역임한 문신.
    '김휘': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 판서, 개성유수 등을 역임한 문신.
    '김휴': {'role': 'scholar'},  # 조선 - 조선 후기에, 강릉참봉 등을 역임하였으며, 『경와집』, 『해동문헌총록』 등을 저술한 학자.
    '김흔': {'role': 'other'},  # 조선 - 조선 전기에, 행부사과 등을 역임한 문신.
    '김흔질': {'role': 'other'},  # 고대/남북국/통일신라 - 통일신라의 제33대 성덕왕의 동생으로, 당나라에 입조사로 가서 낭장의 관직을 받은 왕족.
    '김흠': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 주류성 침공 당시의 장수.
    '김흠돌': {'role': 'other'},  # 고대/남북국/통일신라 - 신라 시대 문무왕대 활약한 진골 출신의 고위 관료로, 신문왕 때 반란을 일으켰다가 실패한 인물.
    '김흠순': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 황산벌전투에 참전한 장수.
    '김흠운': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 낭당대감을 역임한 군인.
    '김흠조': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 장례원판결사 등을 역임한 문신.
    '김흡': {'role': 'other'},  # 조선 - 조선후기 우포도대장, 총융사, 어영대장 등을 역임한 무신.
    '김흥경': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 이조판서, 우의정, 영의정 등을 역임한 문신.
    '김흥교': {'role': 'other'},  # 현대/대한민국 - 해방 이후 효성여자대학교 음악과장, 서울대학교 국악과 조교수 등을 역임한 교육자. 콘트라바스연주자.
    '김흥국': {'role': 'other'},  # 조선 - 조선 후기에, 북평사, 서장관, 형조정랑 등을 역임한 문신.
    '김흥근': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 이조판서, 좌의정, 영의정 등을 역임한 문신.
    '김흥락': {'role': 'scholar'},  # 조선/조선 후기 - 조선 후기에, 학자 · 의병 · 독립운동가 등 수많은 제자를 양성하였으며, 『서산집』, 『보인계첩』 등을 저술한...
    '김흥렬': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 수원교구 순회교사로 활동하며 항일단체인 구국동지회를 조직하였고, 수원의 독립만세시위를 주도하다가...
    '김흥배': {'role': 'other'},  # 현대 - 해방 이후 한국외국어대학을 설립한 육영사업가. 실업인.
    '김흥복': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 수원의 독립만세시위에 참여했다가 고주리 학살사건에 의해 사망한 독립운동가.
    '김흥수': {'role': 'other'},  # 조선/조선 전기 - 조선전기 첨지중추부사, 내의원내의 등을 역임한 의관.
    '김흥식': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 서울에 거주하던 상인으로, 간도 용정에 방문했다가 그곳에서 전개된 독립만세시위에 참여한 독립운동가.
    '김흥우': {'role': 'other'},  # 조선 - 조선 중기에, 강릉참봉 등을 역임한 문신.
    '김흥조': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 해주수령, 수원부사 등을 역임한 문신.
    '김희': {'role': 'other'},  # 조선 - 조선 후기에, 이조참판, 우의정, 영중추부사 등을 역임한 문신.
    '김희갑': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「팔도강산」, 「자유부인」, 「사랑방손님과 어머니」 등에 출연한 배우. 희극인.
    '김희겸': {'role': 'scholar'},  # 조선/조선 후기 - 조선후기 「와운누계창」 · 「석천한유」 · 「안음송대」 등의 작품을 그린 화가.
    '김희남': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 임시정부에서 활동한 독립운동가.
    '김희락': {'role': 'other'},  # 조선 - 조선 후기에, 정언, 흥양현감 등을 역임한 문신.
    '김희로': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 호조참판, 동지중추부사 등을 역임한 문신.
    '김희백': {'role': 'other'},  # 근대 - 일제강점기 때, 대한국민회, 대한독립군 등에서 활약하며 군자금 모금 활동을 전개한 독립운동가.
    '김희삼': {'role': 'scholar'},  # 조선 - 조선전기 병조좌랑, 옥당, 삼척부사 등을 역임한 문신. 학자.
    '김희상': {'role': 'scholar'},  # 근대/일제강점기 - 일제강점기 『조선어전』, 『울이글틀』 등을 저술한 학자. 국어학자.
    '김희선': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 육군무관학교 교장, 임시정부 군무부차장 등을 역임한 관료.
    '김희수': {'role': 'other'},  # 현대/대한민국 - 해방 이후 대종상 편집상, 조선일보 기술상 등을 수상한 영화인. 편집기사.
    '김희순': {'role': 'other'},  # 근대/일제강점기 | 현대 - 근⋅현대기 전주를 중심으로 활동한 서화가.
    '김희열': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 참판, 경주부윤 등을 역임한 문신.
    '김희제': {'role': 'other'},  # 고려 - 고려후기 의주분도장군, 서북면병마부사 등을 역임한 무신.
    '김희조': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「단소와 관현악을 위한 수상곡」 · 「창과 관현악 범피중류」 · 「대춘향전」 등을 만든 작곡가.
    '김희주': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 대사간, 안악군수 등을 역임한 문신.
    '김희채': {'role': 'other'},  # 조선 - 조선 후기에, 교리 등을 역임한 문신.
    '김희철': {'role': 'scholar'},  # 현대/대한민국 - 인하대학교 대학원장, 총장을 비롯하여 대한기계학회 회장, 대한자동차공학회 회장 등을 역임하였으며, 열역학, 내연기...
    '김희춘': {'role': 'other'},  # 현대 - 해방 이후 경기도청사, 한국정신문화연구원 등을 신축한 건축가.
    '김희취': {'role': 'other'},  # 고려 - 고려후기 삼별초의 난과 관련된 무신.
    '김희화': {'role': 'other'},  # 조선 - 조선 후기에, 공조판서 등을 역임한 문신.
    '나경적': {'role': 'scholar'},  # 조선/조선 후기 - 조선 후기에, 『석당유고』 등을 저술한 학자.
    '나계종': {'role': 'other'},  # 고려/고려 후기 - 고려 후기, 사헌부시사 · 전리좌랑 · 예문관제학 등을 역임한 문신.
    '나광만': {'role': 'other'},  # 고려 - 고려 후기에, 대호군 등을 역임한 무신 · 공신.
    '나급': {'role': 'other'},  # 조선 - 조선 중기에, 장령, 평산부사 등을 역임한 문신.
    '나기학': {'role': 'other'},  # 근대 - 일제강점기 상교, 정교, 대형 등을 역임한 대종교인.
    '나대용': {'role': 'other'},  # 조선 - 조선시대 임진왜란 당시 한산도해전, 명량해전 등과 관련된 무신.
    '나덕명': {'role': 'scholar'},  # 조선 - 조선 중기에, 정여립 사건에 연루되어 유배되었으며, 임진왜란 때 의병을 모아 국경인의 반란을 진압하는데 공을 세운 학자.
    '나덕헌': {'role': 'other'},  # 조선 - 조선시대 창성부사, 의주부윤, 삼도통어사 등을 역임한 무신.
    '나도향': {'role': 'novelist'},  # 근대 - 일제강점기 「벙어리 삼룡이」, 「뽕」, 「물레방아」 등을 저술한 소설가.
    '나득황': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 판예빈성사, 추밀원부사, 형부상서 등을 역임한 문신.
    '나만갑': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 병자호란 당시 남한산성에서 인조를 호종한 문신.
    '나무송': {'role': 'other'},  # 조선 - 조선 후기에, 예안현감, 병조정랑 등을 역임한 문신.
    '나무춘': {'role': 'other'},  # 조선 - 조선 후기에, 성균관학록, 성균관학정, 감찰 등을 역임한 문신.
    '나백': {'role': 'other'},  # 조선 - 조선후기 춘파 쌍언(春坡雙彦)의 제자가 되어 법맥을 계승한 승려.
    '나병삼': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 대한독립청년단연합회 모험단에 참여하여 순사 총살, 독립운동문서 배포, 친일파 처단과 군자금 모금에 주...
    '나상기': {'role': 'other'},  # 현대/대한민국 - 해방 이후 홍익대학교 교수, 한국건축가협회회장 등을 역임한 건축가.
    '나상목': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 「비류」 · 「장하강촌」 등의 작품을 그린 화가.
    '나상진': {'role': 'other'},  # 현대 - 해방 이후 새나라자동차 부평공장, 경기도청사 등을 신축한 건축가.
    '나석좌': {'role': 'scholar'},  # 조선 - 조선 후기에, 명왕조 부흥세력과 연합하여 북벌을 단행해 병자호란의 치욕을 설욕하자고 주장한 학자.
    '나석주': {'role': 'other'},  # 근대/일제강점기 - 조선식산은행과 동양척식주식회사에 폭탄을 던지며 의열 투쟁을 전개한 독립운동가.
    '나성두': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 호조좌랑, 봉산현감, 이산현감 등을 역임한 문신.
    '나성화': {'role': 'other'},  # 근대 - 대한제국기 때, 심남일 의진에서 후군장으로 활약한 의병.
    '나세': {'role': 'other'},  # 고려 - 조선전기 참찬문하, 연해등처병선조전절제사 등을 역임한 장수.
    '나세진': {'role': 'scholar'},  # 근대/일제강점기|현대 - 대한해부학회 회장, 대한체질인류학회 회장 등을 역임하였으며, 해부학과 체질인류학 분야의 학문개척과 연구발전...
    '나세찬': {'role': 'other'},  # 조선 - 조선 전기에, 대사간, 대사헌, 한성우윤 등을 역임한 문신.
    '나수연': {'role': 'other'},  # 근대/대한제국기 - 대한제국기 황성신문 총무원, 대한자강회 총무, 중추원 참의 등을 역임한 관료. 서화가.
    '나숙': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 직제학, 승지, 부제학 등을 역임한 문신.
    '나시운': {'role': 'other'},  # 근대/개항기 - 개항기 때, 안승우 의진에서 도령장으로 활동한 의병.
    '나식': {'role': 'scholar'},  # 조선 - 조선 전기에, 『장음정집』 등을 저술하였으며, 선릉참봉을 역임하다 을사사화 때 유배형에 처해져 사사된 학자.
    '나양좌': {'role': 'other'},  # 조선 - 조선 후기에, 종친부전부, 삭녕군수, 장령 등을 역임한 문신.
    '나열': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 함창현감과 의금부도사 등을 역임한 문신.
    '나용균': {'role': 'other'},  # 근대 - 일제강점기 때, 2·8독립선언에 참여하였으며, 임시의정원 법제위원, 정무조사 특별위원, 정치분과위원 등을 역임한 정치인 ·...
    '나용환': {'role': 'other'},  # 근대 - 일제강점기 때, 민족대표 33인 중 한 사람으로, 독립선언서에 서명한 천도교인 · 독립운동가.
    '나운규': {'role': 'scholar'},  # 근대 - 일제강점기 「아리랑」, 「풍운아」, 「벙어리 삼룡」 등의 작품에 관여한 영화인. 영화감독.
    '나운영': {'role': 'other'},  # 현대/대한민국 - 「고전풍의 첼로소나타」, 「아 가을인가」 등을 만든 작곡가.
    '나월환': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 때, 철혈단을 조직하였으며, 중국헌병학교 교수, 한국청년전지공작대 대장, 한국광복군 제5지대 지대장 ...
    '나위소': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 경주부윤, 동지중추부사 등을 역임한 문신.
    '나유': {'role': 'other'},  # 고려 - 고려후기 진도에서 원수 김방경을 따라 삼별초를 토벌하는 공을 세운 무신.
    '나윤명': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 교서별좌 등을 역임한 문신.
    '나이준': {'role': 'other'},  # 조선 - 조선 후기에, 부교리, 집의, 사간 등을 역임한 문신.
    '나익': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 설서, 적성현감 등을 역임한 문신.
    '나익남': {'role': 'other'},  # 조선 - 조선 후기에, 개성부유수, 창원부교수, 유학교수 등을 역임한 문신.
    '나익진': {'role': 'other'},  # 현대 - 동서통상주식회사 사장, 채신부차관, 한국산업은행 총재 등을 역임한 관료 · 기업인.
    '나익희': {'role': 'other'},  # 고려 - 고려후기 검교상호군, 상의평리, 첨의참리 등을 역임한 무신.
    '나인협': {'role': 'other'},  # 근대 - 일제강점기 때, 독립선언서에 서명한 민족대표 33인 중 한 사람으로, 천도교 도사를 역임하며 민중교화운동에 힘쓴 천도교인 ...
    '나정구': {'role': 'other'},  # 근대 - 일제강점기 때, 대한청년단, 대한통의부 등에서 군자금 모금 활동을 전개한 독립운동가.
    '나정련': {'role': 'other'},  # 근대 - 일제강점기 시교원, 경의원참의 등을 역임한 대종교인. 순교자.
    '나정록': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 홍경래의 난을 진압하는 과정에서 살해된 의병.
    '나정문': {'role': 'other'},  # 근대 - 일제강점기 교적간행회 총무, 천전건축주비회 발기인 등을 역임한 대종교인. 순교자.
    '나주의 샛골나이': {'role': 'other'},  # 전라남도 나주시 다시면 동당리의 무명짜기 기능.
    '나중소': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 북로군정서를 조직하였고, 사관양성소 교성대장, 신민부 참모부 위원장 등을 역임한 독립운동가.
    '나창준': {'role': 'other'},  # 현대/대한민국 - 해방 이후 한국전쟁 당시의 군인.
    '나창헌': {'role': 'other'},  # 근대 - 일제강점기 때, 대동단에서 의친왕 망명 계획에 가담하였으며, 한국노병회 이사, 교민단의사회 학무위원, 임시정부 경무국장 등...
    '나철': {'role': 'other'},  # 근대 - 대한제국 말기에 을사오적 암살을 계획하다 유배되었으며, 대종교를 창시해 독립정신을 고취한 대종교인 · 독립운동가.
    '나태섭': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 한국국민당청년단 단장으로 활동하였고, 1940년 9월 17일 창설된 한국광복군의 총사령부에서 간부로 ...
    '나학천': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 병조참지 등을 역임한 문신.
    '나항윤': {'role': 'other'},  # 현대 - 해방 이후 전주지방법원장, 서울지방법원장, 대법관 등을 역임한 법조인.
    '나해륜': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 이괄의 난과 병자호란이 발발하자 의병을 모집한 의병장.
    '나해봉': {'role': 'novelist'},  # 조선/조선 후기 - 조선 후기에, 이괄의 난과 병자호란이 발발하자 의병을 모집하였고, 『남간집』, 『남간집선』 등을 저술한 문인 ·...
    '나현성': {'role': 'scholar'},  # 현대/대한민국 - 서울대학교 사범대학 교수, 대한체육회 선수강화위원회 및 훈련평가위원회 위원 등을 역임하였으며, 『한국스포츠사』, ...
    '나혜석': {'role': 'scholar foreigner'},  # 일제강점기 「무희」, 「스페인해수욕장」 등의 작품을 그린 화가.
    '나홍좌': {'role': 'other'},  # 조선/조선 후기 - 조선후기 함경남도병마절도사, 삼도통제사, 수원방어사 등을 역임한 무신.
    '나화랑': {'role': 'other'},  # 근대 - 해방 이후 「열아홉 순정」, 「무너진 사랑탑」, 「이정표」 등을 만든 작곡가.
    '나흥유': {'role': 'other'},  # 고려 - 고려후기 영전도감판관, 사농소경, 판전객시사 등을 역임한 무신.
    '낙금': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 청해진대사 장보고 휘하의 장수.
    '낙랑공주': {'role': 'other'},  # 고려 - 고려전기 제1대 태조의 맏딸인 공주.
    '낙랑후': {'role': 'other'},  # 고려/고려 전기 - 고려의 제10대 왕, 정종의 아들로, 형제가 모두 죽어 장자와 다를 바 없었으나, 정종 사후에도 왕위에 오르지 ...
    '낙사계': {'role': 'other'},  # 고대/남북국/발해 - 남북국시대 당나라에서 행좌우림군장군, 농우절도사, 경략대사 등을 역임한 관리. 장군.
    '낙선군': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 제16대 왕인 인조의 서(庶)2남.
    '낙안': {'role': 'other'},  # 조선 - 조선후기 보시행으로 이름높은 범어사의 승려.
    '낙진': {'role': 'other'},  # 고려 - 고려전기 승통, 귀법사 주지, 법수사 주지, 왕사 등을 역임한 승려.
    '낙현': {'role': 'other'},  # 조선 - 개항기 팔도대각등계보제존자도총섭에 추증된 승려.
    '난승': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 김유신이 삼국통일에 뜻을 품고 석굴에 들어가 기원할 때 나타난 선인(仙人).
    '난원': {'role': 'other'},  # 고려 - 고려전기 화엄종 도승통을 역임한 승려.
    '남간': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 예문직제학, 지사간원사, 대사헌 등을 역임한 문신.
    '남간부인': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라 신인종의 종조 명랑의 모친인 귀족.
    '남경우': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 병조판서 등을 역임한 문신.
    '남경조': {'role': 'scholar'},  # 조선 - 조선 후기에, 경학을 깊이 탐구하였으며, 『구고헌일고』 등을 저술한 학자.
    '남경희': {'role': 'other'},  # 조선 - 조선 후기에, 사헌부감찰, 병조좌랑, 사간원정언 등을 역임한 문신.
    '남계병': {'role': 'other'},  # 근대 - 일제강점기 때, 경상북도 영덕군 영해면 성내시장의 독립만세시위를 주도한 독립운동가.
    '남계영': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 봉상시주부 등을 역임한 문신.
    '남계우': {'role': 'scholar'},  # 조선 - 조선후기 「군접도」 · 「화접도대련」 · 「석화접도대련」 등의 작품을 그린 화가.
    '남계하': {'role': 'other'},  # 조선 - 조선 후기에, 의금부도사, 청하현감 등을 역임한 문신.
    '남곤': {'role': 'other'},  # 조선 - 조선 전기에, 심정 등과 함께 기묘사화를 일으켜 조광조 · 김정 등 신진 사림파를 숙청한 후 좌의정 · 영의정 등을 역임한...
    '남공선': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 『한족공보(韓族公報)』 주필과 고려공산청년회 집행위원을 역임한 사회주의운동가.
    '남공철': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 대제학, 우의정, 영의정 등을 역임한 문신.
    '남관': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 「동양의 풍경」, 「허물어진 제단」, 「역사의 흔적」 등의 작품을 그린 화가.
    '남광우': {'role': 'scholar'},  # 『고어사전』, 『조선한자음연구』, 『조선한자음연구』, 『고금한한자전』 등을 저술한 학자. 국어학자.
    '남광원': {'role': 'other'},  # 근대 - 대한제국기 때, 고창, 부안 등지에서 군자금 모금 활동을 전개한 의병.
    '남구만': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 함경도관찰사, 형조판서, 영의정 등을 역임한 문신.
    '남구명': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 순천부사 등을 역임한 문신.
    '남궁경': {'role': 'other'},  # 조선 - 조선 후기에, 세자시강원필선, 검상, 사인 등을 역임한 문신.
    '남궁계': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 경주부윤, 중추원부사 등을 역임한 문신.
    '남궁두': {'role': 'other'},  # 조선 - 조선시대 단학파에 속한 도교인.
    '남궁민': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 정치관, 간의 등을 역임한 문신.
    '남궁벽': {'role': 'poet'},  # 근대 - 일제강점기 「고독은 너의 운명이다」, 「신비의 인연」, 「출생」 등을 저술한 시인.
    '남궁숙': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 함경도관찰사, 동지중추부사 등을 역임한 문신.
    '남궁신': {'role': 'other'},  # 고려 - 고려 후기에, 호군 등을 역임한 무신 · 공신.
    '남궁억': {'role': 'other'},  # 근대 - 대한제국기 때, 황성신문 사장, 대한협회 회장, 배화학당 교사 등을 역임하며 애국계몽운동을 전개한 언론인 · 교육자 · 독...
    '남궁영': {'role': 'other'},  # 근대/개항기 | 근대/일제강점기 - 일제강점기 경상남도 참여관, 충청북도지사, 중추원 참의 등을 역임한 관료. 친일반민족행위자.
    '남궁옥': {'role': 'other'},  # 조선/조선 후기 - 조선후기 승문원판교, 시정 등을 역임한 문신. 서예가.
    '남궁요열': {'role': 'other'},  # 현대 - 해방 이후, 고려교향악단 오보에 주자이자, 해군군악학교 초대 교장 및 해군본부 군악대장, 한국음악협회 이사장, 한국관악협회...
    '남궁집': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 대사헌, 대사간 등을 역임한 문신.
    '남궁찬': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 강원도관찰사 등을 역임한 문신.
    '남궁침': {'role': 'other'},  # 조선 - 조선 전기에, 한성부판윤, 오우도총부부총관, 형조참판 등을 역임한 문신.
    '남궁혁': {'role': 'other'},  # 현대/대한민국 - 일제강점기 평양신학교 교수, 조선예수교장로회 총회장 등을 역임한 목사. 교육가.
    '남궁현': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 전라북도(현, 전북특별자치도) 전주의 독립만세시위를 주도하였으며, 출옥 후 독립운동가 가족들의 ...
    '남규희': {'role': 'other'},  # 근대 - 일제강점기 중추원 찬의, 중추원 참의 등을 역임한 관료. 친일반민족행위자.
    '남극관': {'role': 'novelist'},  # 조선/조선 후기 - 조선후기 『몽예집』을 저술한 문인.
    '남극표': {'role': 'other'},  # 조선 - 조선 후기에, 의금부도사 등을 역임한 문신.
    '남근': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 대사헌, 대사간 등을 역임한 문신.
    '남급': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 사옹원봉사, 종묘사직장 등을 역임한 문신.
    '남기만': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 승문원주서, 장릉별검, 정언 등을 역임한 문신.
    '남기제': {'role': 'scholar'},  # 조선/조선 후기 - 조선 후기에, 『아아록』 등을 저술한 학자.
    '남노명': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 좌랑, 거창현감 등을 역임한 문신.
    '남노성': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 청요직을 두루 역임한 문신.
    '남대관': {'role': 'other foreigner'},  # 근대/일제강점기 - 재일본조선노동총동맹 중앙집행위원으로 활동한 사회운동가.
    '남덕우': {'role': 'scholar'},  # 현대/대한민국 - 대한민국의 재무부 장관, 부총리 겸 경제기획원 장관, 제14대 국무총리 등을 역임한 경제관료이자 경제학자.
    '남도진': {'role': 'scholar'},  # 조선 - 조선 후기에, 『낙은별곡』, 『봉래가』 등을 저술한 문신.
    '남두민': {'role': 'other'},  # 조선/조선 후기 - 조선후기 전의감(典醫監) 정(正)을 역임한 의관.
    '남두첨': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 호조참의 등을 역임한 문신.
    '남려': {'role': 'other'},  # 고대/초기국가/동예 - 초기국가시대 위만조선 말기 예족의 군장.
    '남만춘': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 합동민족부대 참모장, 고려공산당창립대회준비위원 등을 역임한 사회주의운동가.
    '남명학': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 참봉, 감찰, 평택현감, 공조좌랑 등을 역임한 함경도 출신의 문신.
    '남모': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라 청소년 조직의 수장인 원화(源花).
    '남몽뢰': {'role': 'scholar'},  # 조선 - 조선 후기에, 예조정랑, 진주목사 등을 역임하였으며, 『이게문집』 등을 저술한 문신.
    '남무성': {'role': 'other'},  # 조선 - 조선 후기에, 병자호란이 발발하자 충청도관찰사 정세규의 휘하에서 활약한 의병.
    '남벌': {'role': 'other'},  # 조선 - 조선 후기에, 장령, 삼척부사 등을 역임한 문신.
    '남병길': {'role': 'scholar'},  # 조선 - 조선후기 『칠정보법』 · 『태양출입표』 · 『산학정의』 등을 저술한 학자. 천문역법학자.
    '남병철': {'role': 'scholar'},  # 조선 - 조선후기 예조판서, 대제학 등을 역임한 문신. 천문학자 · 수학자.
    '남사고': {'role': 'scholar'},  # 조선 - 조선시대 『남사고비결』, 『남격암십승지론』 등을 저술한 학자. 도사(道士).
    '남상교': {'role': 'novelist'},  # 조선/조선 후기 - 조선후기 충주목사, 동지돈령부사 등을 역임한 문신. 문인 · 종교인.
    '남상국': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「고성오광대」의 전승자로 인정된 예능보유자.
    '남상덕': {'role': 'other foreigner'},  # 근대 - 대한제국기 대한제국군대 해산령 당시 일본군에 항전한 항일운동가.
    '남상목': {'role': 'other'},  # 근대 - 대한제국기 때, 용인에서 모병하여 구식총 40자루와 양총 10자루로 항일의병투쟁을 전개한 의병.
    '남상문': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 군수 등을 역임한 문신.
    '남석인': {'role': 'other'},  # 근대 - 대한제국기 때, 정용기의 산남의진에서 청송지방 소모장으로 활동한 의병장.
    '남선': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 이조판서 등을 역임한 문신.
    '남세건': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 대사성, 호조참판 등을 역임한 문신.
    '남세주': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 지평, 부응교, 예문관응교 등을 역임한 문신.
    '남세준': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 경기감사, 예조참판, 이조참판 등을 역임한 문신.
    '남수문': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 집현전부수찬, 집현전응교, 집현전직제학 등을 역임한 문신.
    '남순민': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 첨지중추부사, 오위장 등을 역임한 문신.
    '남억우': {'role': 'other'},  # 현대/대한민국 - 해방 이후 한국교육개발원 부원장, 인천교원단체 연합회 회장 등을 역임한 교육자.
    '남언경': {'role': 'other'},  # 조선 - 조선시대 때, 양명학의 사상적 체계를 완성한 문신.
    '남언기': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 인심도심설을 토론하며 도학에 열중한 문신.
    '남언순': {'role': 'other'},  # 조선/조선 전기 - 조선전기 병조참의, 함경도병마절도사 등을 역임한 무신.
    '남연': {'role': 'other'},  # 조선 - 조선 후기에, 공조정랑, 성균관직강, 봉상시첨정 등을 역임한 문신.
    '남연년': {'role': 'other'},  # 조선/조선 후기 - 조선후기 이인좌의 난과 관련된 무신.
    '남영': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 선조~광해군 연간의 침의(鍼醫).
    '남영신': {'role': 'other'},  # 고려 - 고려 후기에, 사관 등을 역임한 문신.
    '남용익': {'role': 'scholar'},  # 조선/조선 후기 - 조선후기 좌참찬, 예문관제학 등을 역임한 문신. 학자.
    '남운룡': {'role': 'other'},  # 현대/대한민국 - 해방 이후 남사당놀이 중 「꼭두각시놀음」의 전승자로 지정된 예능보유자.
    '남위': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 학생 대표로서 3·1운동에 참가해 시위를 주도하다가 체포되어 고문 후유증으로 순국한 독립운동가.
    '남위언': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 중국 만주 북간도 민족교육기관인 명동중학교 교사를 역임한 교육자.
    '남유': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 서천군수와 부평부사를 역임하고 정유재란 때 노량해전에서 전사한 무신.
    '남유상': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 실록랑, 수찬, 이조정랑 등을 역임한 문신.
    '남유용': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 홍문관교리, 홍문관제학, 형조판서 등을 역임한 문신.
    '남윤구': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 조선노농총동맹 중앙위원 등을 역임하며 항일투쟁을 전개한 독립운동가.
    '남윤함': {'role': 'other'},  # 조선 - 조선시대 동지사 정경세를 수행하여 명나라에 다녀온 역관.
    '남은': {'role': 'other'},  # 고려 후기에, 삼척지군사, 밀직부사, 지문하부사 등을 역임한 문신.
    '남을진': {'role': 'other'},  # 고려/고려 후기 - 고려후기 참지문하부사, 사천백 등을 역임한 문신. 충신.
    '남응룡': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 공조참의 등을 역임한 문신.
    '남응운': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 승정원주서, 길주목사, 경기도관찰사 등을 역임한 문신.
    '남응중': {'role': 'other'},  # 조선/조선 후기 - 조선후기 은언군의 손자를 왕으로 추대하고자 반란을 모의한 주모자. 반역자.
    '남이': {'role': 'other'},  # 조선/조선 전기 - 조선전기 공조판서, 병조판서 등을 역임한 무신.
    '남이공': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 예조참의, 홍문관부제학, 병조참판 등을 역임한 문신.
    '남이성': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 예조판서 등을 역임한 문신.
    '남이신': {'role': 'other'},  # 조선 - 조선 중기에, 경기도관찰사, 안변부사, 대사간 등을 역임한 문신.
    '남이웅': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 이조판서, 우의정, 좌의정 등을 역임한 문신.
    '남이준': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 사간, 경성판관 등을 역임한 문신.
    '남이흥': {'role': 'other'},  # 조선 - 조선시대 선전관, 안주목사, 연안부사 등을 역임한 무신.
    '남익훈': {'role': 'other'},  # 조선 - 조선 후기에, 함경도관찰사 등을 역임한 문신.
    '남인수': {'role': 'other'},  # 근대 - 해방 이후 「가거라 삼팔선」, 「이별의 부산정거장」 등 다수의 곡을 발표한 가수.
    '남일우': {'role': 'other'},  # 근대 - 조선 후기에, 홍문관부제학, 경상도관찰사, 공조판서 등을 역임한 문신.
    '남자': {'role': 'scholar'},  # 조선 - 조선 후기에, 『중용차의』 등을 저술한 문신.
    '남자현': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 만주 서로군정서에서 활약하였고, 여성 계몽과 독립정신 고취에 힘쓰며 군자금 모금 및 일본 고관 ...
    '남재': {'role': 'other'},  # 조선 - 조선 전기에, 도병마사, 경기도관찰사, 좌의정 등을 역임한 문신.
    '남정각': {'role': 'other'},  # 근대 - 일제강점기 때, 의열단에서 활동하며 일제 기관 파괴를 계획하다 발각되어 체포된 독립운동가.
    '남정국': {'role': 'other'},  # 조선 - 조선 전기에, 공조정랑, 충훈부도사 등을 역임한 문신.
    '남정순': {'role': 'other'},  # 근대 - 조선 후기에, 함경도안무사, 공조판서, 이조판서 등을 역임한 문신.
    '남정임': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「유정」, 「까치소리」, 「분녀」 등에 출연한 배우. 영화배우.
    '남정중': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 능주목사 등을 역임한 문신.
    '남정철': {'role': 'other'},  # 근대 - 일제강점기 한성판윤, 내부대신 등을 역임한 관료. 친일반민족행위자.
    '남종삼': {'role': 'other'},  # 조선 - 조선후기 홍문관교리 · 영해현감 · 승지 등을 역임한 순교자.
    '남좌시': {'role': 'other'},  # 고려/고려 후기 - 고려후기 첨서밀직(簽書密直), 강릉도부원수(江陵道副元帥), 정당상의(政堂商議) 등을 역임한 무신. 의성군(宜城君).
    '남주헌': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 승지, 춘천부사 등을 역임한 문신.
    '남준표': {'role': 'other'},  # 근대 - 일제강점기 만주에서 조선인 공청운동에 참여한 사회주의운동가.
    '남중유': {'role': 'other'},  # 조선 - 조선 후기에, 사직서령, 대흥군수 등을 역임한 문신.
    '남지': {'role': 'other'},  # 조선 - 조선 전기에, 호조판서, 우의정, 좌의정 등을 역임한 문신.
    '남질': {'role': 'other'},  # 고려 - 고려 후기에, 경상도도순문사 등을 역임한 문신.
    '남창익': {'role': 'other'},  # 근대 - 일제강점기 동북인민혁명군 제2군 독립사 제3단 정치위원 등을 역임한 사회주의운동가.
    '남채': {'role': 'other'},  # 현대/대한민국 - 해방 이후 불교조계종 교무국장, 한국불교태고종 제5대총무원 등을 역임한 승려.
    '남천우': {'role': 'other foreigner'},  # 현대/대한민국 - 일제강점기 때, 대전제일교회 목사, 일본기독교 조선감리교단 상임위원 등을 역임하였으며, 해방 이후 독립촉성국민회 ...
    '남천한': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 호조참의 등을 역임한 문신.
    '남추': {'role': 'other'},  # 조선 - 조선 전기에, 성균관학유, 성균관전적 등을 역임한 문신.
    '남취명': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 병조참판, 지돈녕부사 등을 역임한 문신.
    '남치근': {'role': 'other'},  # 조선/조선 전기 - 조선전기에 전라도병마절도사 · 전라도순변사 · 한성부판윤 등을 역임한 무신.
    '남치리': {'role': 'scholar'},  # 조선 - 조선 전기에, 『비지문집』 등을 저술한 학자.
    '남치원': {'role': 'other'},  # 조선 - 조선전기 평시서제조, 훈련원첨정 등을 역임한 관리.
    '남치훈': {'role': 'other'},  # 조선 - 조선 후기에, 형조참판, 강원도관찰사 등을 역임한 문신.
    '남탁': {'role': 'other'},  # 조선 - 조선 후기에, 종부시정, 해미현감 등을 역임한 문신.
    '남태기': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 형조참판, 한성부좌우윤, 예조판서 등을 역임한 문신.
    '남태온': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 오위도총부부총관, 안변부사 등을 역임한 문신.
    '남태응': {'role': 'novelist'},  # 조선/조선 후기 - 조선 후기에, 『청죽만록』, 『청죽별지』, 「삼화가유평」 등을 저술한 문인.
    '남태저': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 병조참판, 한성부우윤 등을 역임한 문신.
    '남태제': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 경기감사, 홍문관제학, 이조판서 등을 역임한 문신.
    '남태징': {'role': 'other'},  # 조선/조선 후기 - 조선후기 이인좌의 난과 관련된 무신.
    '남태혁': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 사간, 승정원동부승지, 공조참판 등을 역임한 문신.
    '남태회': {'role': 'other'},  # 조선 - 조선 후기에, 형조판서, 동지의금부사 등을 역임한 문신.
    '남포': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 공조낭관, 홍문관직제학, 소격서령 등을 역임한 문신.
    '남하정': {'role': 'scholar'},  # 조선 - 조선 후기에, 「출사책」, 『사대춘추』, 『동소만록』 등을 저술한 학자.
    '남하행': {'role': 'scholar'},  # 조선 - 조선 후기에, 『와유록』, 『술선록』 등을 저술한 학자.
    '남한기': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 장례원판결사, 오위도총부부총관 등을 역임한 문신.
    '남한조': {'role': 'scholar'},  # 조선 - 조선 후기에, 「거습잠」, 『손재문집』 등을 저술한 학자.
    '남해준': {'role': 'scholar'},  # 조선 - 조선 후기에, 『사례질의』 등을 저술한 학자.
    '남해차차웅': {'role': 'other'},  # 고대/삼국 - 신라의 제2대(재위: 4년~24년) 왕.
    '남형우': {'role': 'other'},  # 근대/일제강점기 - 대한민국임시정부 법무총장과 교통총장을 역임한 독립운동가.
    '남효온': {'role': 'novelist'},  # 조선 - 조선 전기에, 김종직의 문인으로, 문종의 비, 현덕왕후의 능인 소릉의 복위를 상소한 일로 박해받은 문신 · 생육신.
    '남효의': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 대사헌, 형조판서 등을 역임한 문신.
    '남휘': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 판한성부사, 평양선위사, 황주선위사 등을 역임한 문신.
    '남흔': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 통정대부, 좌부승지, 우부승지 등을 역임한 문신.
    '낭오': {'role': 'other'},  # 조선 - 조선 후기, 불교의 수계 의식 전통을 복구한 승려.
    '낭지': {'role': 'other'},  # 고대/남북국/통일신라 - 삼국시대 신라의 삽량주 영취산에서 『법화경』을 강의했던 승려.
    '내례부인': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라 제8대 아달라이사금의 왕비.
    '내로': {'role': 'other'},  # 고대/삼국/신라 - 신라의 건국시조인 박혁거세의 손자인 왕족.
    '내물마립간': {'role': 'other'},  # 신라의 제17대(재위: 356년~402년) 왕.
    '내숙': {'role': 'other'},  # 고대/삼국/신라 - 신라의 제17대 왕, 내물마립간의 증손으로, 이벌찬에 임명된 종실.
    '내원': {'role': 'other'},  # 고려/고려 후기 - 고려후기 제28대 충혜왕의 왕사로 책봉된 승려.
    '내음': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라 제10대 내해이사금의 서자인 왕자. 재상.
    '내음갈문왕': {'role': 'other'},  # 고대/삼국/신라 - 신라의 제14대 왕, 유례이사금의 외조부로, 갈문왕에 책봉된 귀족.
    '내해이사금': {'role': 'other'},  # 고대/삼국 - 신라의 제10대(재위 196년~230년) 왕.
    '노개방': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 동래교수 등을 역임한 문신.
    '노경린': {'role': 'other'},  # 조선 - 조선 전기에, 사헌부지평, 성주목사, 숙천부사 등을 역임한 문신.
    '노경임': {'role': 'other'},  # 조선 - 조선 중기에, 지영해부사, 성주목사 등을 역임한 문신.
    '노경희': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「실낙원의 별」 · 「느티나무있는 언덕」 · 「어느 하늘 아래서」 등에 출연한 배우. 영화배우.
    '노계원': {'role': 'scholar'},  # 조선 - 조선 후기에, 『오행설』, 『정성서의』, 『심의설』 등을 저술한 학자.
    '노계정': {'role': 'other'},  # 조선 - 조선후기 박천군수, 위원군수, 전라우수사 등을 역임한 무신.
    '노공일': {'role': 'other'},  # 근대 - 대한제국기 때, 창의군 의진에서 종사관으로 활동한 의병장.
    '노공필': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 우찬성, 영중추부사 등을 역임한 문신.
    '노관': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 이부원외랑, 이부낭중, 판사재사 등을 역임한 문신.
    '노광두': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 장령, 동부승지, 호조참판 등을 역임한 문신.
    '노구산': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 밀직제학, 좌군총제, 도총제 등을 역임한 문신.
    '노구영': {'role': 'other'},  # 근대/대한제국기 - 대한제국기 태의원전의보, 태의원전의 등을 역임한 관료. 의관.
    '노국대장공주': {'role': 'other'},  # 고려후기 제31대 공민왕의 왕비.
    '노극복': {'role': 'other'},  # 조선 - 조선 후기에, 이조정랑, 오수도찰방 등을 역임한 문신.
    '노극신': {'role': 'other'},  # 조선 - 조선 중기에, 양성, 김포 등지의 수령, 돈녕부첨정 등을 역임한 문신.
    '노극청': {'role': 'other'},  # 고려/고려 후기 - 고려후기 산관, 직장동정 등을 역임한 관리.
    '노극홍': {'role': 'scholar'},  # 조선 - 조선 중기에, 임진왜란이 발발하자 곽재우의 휘하에서 서기, 참모로 활동하였으며, 정유재란 때 화왕산성 전투에서 활약한 학자...
    '노긍': {'role': 'novelist'},  # 조선/조선 후기 - 조선 후기 『한원문집』을 저술한 문인.
    '노기남': {'role': 'other'},  # 현대/대한민국 - 한국인 최초의 주교이자 교구장.
    '노기용': {'role': 'other'},  # 근대 - 일제강점기 때, 대구에서 군사주비단에 가담하여 군자금 모금 활동을 전개한 독립운동가.
    '노단': {'role': 'other'},  # 고려/고려 전기 - 고려 전기에, 중추원사, 상서좌복야 참지정사 등을 역임한 문신.
    '노대하': {'role': 'other'},  # 조선 - 조선 중기에, 고부군수 등을 역임한 문신.
    '노덕술': {'role': 'other'},  # 현대/대한민국 - 일제강점기 육군본부 헌병대장, 부산 제2육군범죄수사단 대장 등을 역임한 군인. 친일반민족행위자.
    '노도형': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 예천군수 등을 역임한 문신.
    '노류지': {'role': 'other foreigner'},  # 고대/삼국/고구려 - 삼국시대 일본에 파견된 고구려의 공예가.
    '노리부': {'role': 'other'},  # 고대/삼국/신라 - 신라 진평왕대에 상대등을 지낸 진골 귀족.
    '노리사치계': {'role': 'other foreigner'},  # 고대/삼국/백제 - 삼국시대 백제의 달솔로서 일본에 불교를 전수한 귀족.
    '노명석': {'role': 'novelist'},  # 현대 - 해방 이후 『문』, 『용사냥』, 『노들강변』 등을 저술한 소설가.
    '노무현': {'role': 'other'},  # 현대/대한민국 - 대한민국의 제16대 대통령.
    '노문천': {'role': 'poet'},  # 현대/대한민국 - 해방 이후 『미이라』, 『불멸의 연가』, 『Back mirror』 등을 저술한 시인.
    '노물재': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 유거감찰, 첨지중추부사, 동지돈녕부사 등을 역임한 문신.
    '노백린': {'role': 'other'},  # 근대/일제강점기 - 대한민국임시정부의 군무총장과 국무총리를 역임한 독립운동가.
    '노병대': {'role': 'other'},  # 근대 - 대한제국기 때, 속리산에서 의병을 모집하여 충청북도와 경상북도에서 항일의병투쟁을 전개한 의병장.
    '노병선': {'role': 'other'},  # 근대/일제강점기 - 대한제국기 협성회 부회장, 웹윗청년회 창립위원 등으로 활동한 개신교인.
    '노병희': {'role': 'other'},  # 근대/대한제국기 - 대한제국기 때, 최익현과 의병활동을 모의하며 군자금 모금 운동을 전개하였고, 의진에서 의관으로 활약한 의사 · 의병.
    '노복선': {'role': 'other'},  # 근대 - 일제강점기 때, 임시정부 군무부 군사특파단 청년공작원, 광복군 총사령부 부관 등을 역임한 독립운동가.
    '노부': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 거칠부 등과 고구려를 침공하여 한강 상류지역 10개군을 점령한 장수.
    '노사신': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 이조판서, 영중추부사, 영의정 등을 역임한 문신.
    '노사예': {'role': 'scholar'},  # 조선 - 조선시대 『경임안』, 『홍와유고』, 『사서찬요』 등을 저술한 학자. 의병참모.
    '노석빈': {'role': 'other'},  # 조선 - 조선 후기에, 공조좌랑, 창평현감, 직강 등을 역임한 문신.
    '노석숭': {'role': 'other'},  # 고려/고려 후기 - 고려후기 이의민 제거와 관련된 관리. 무신.
    '노석정': {'role': 'other'},  # 근대 - 일제강점기 때, 전라남도에서 군자금 모금 활동을 전개한 독립운동가.
    '노석중': {'role': 'other'},  # 근대 - 일제강점기 때, 전라남도에서 동지 포섭 및 군자금 모금 활동을 전개한 독립운동가.
    '노선': {'role': 'other'},  # 고려/고려 후기 - 고려 후기, 공민왕 때 자제위 소속 관리.
    '노선경': {'role': 'other'},  # 조선 - 조선 전기에, 함양군수, 고령현감 등을 역임한 문신.
    '노세후': {'role': 'scholar'},  # 조선 - 조선 중기에, 상수학 및 정전법에 정통했으며, 임진왜란 때 곽재우의 휘하에서 의병으로 싸운 학자.
    '노수': {'role': 'scholar'},  # 조선 - 조선 전기에, 『경신잠』, 『삼성잠』 등을 저술한 학자.
    '노수신': {'role': 'other'},  # 조선 - 조선 전기에, 우의정, 좌의정, 영의정 등을 역임한 문신.
    '노수현': {'role': 'other'},  # 현대/대한민국 - 해방 이후 서울대학교 미술대학 교수, 대한민국미술전람회 심사위원 등을 역임한 화가.
    '노숙': {'role': 'other'},  # 조선 - 조선시대 용양위부호군를 역임한 무신.
    '노숙동': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 대사헌, 형조참판, 동지중추원사 등을 역임한 문신.
    '노순': {'role': 'novelist'},  # 조선/조선 후기 - 조선 후기 조식의 문인으로, 임진왜란 때 삼가에서 창의한 의병장.
    '노숭': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 참판승추부사, 참찬의정부사, 검교우의정 등을 역임한 문신.
    '노약순': {'role': 'other'},  # 고려/고려 후기 - 고려후기 노약순, 한수도 반란기도사건 등과 관련된 관리.
    '노영': {'role': 'other'},  # 고려/고려 후기 - 고려후기 「아미타구존도」를 그린 화가.
    '노영거': {'role': 'other'},  # 고려/고려 전기 - 고려 전기에, 좌중군사, 공부시랑 등을 역임한 문신.
    '노영규': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「수영야류」 양반 역 전승자로 인정된 기예능보유자.
    '노영서': {'role': 'other'},  # 고려 - 고려후기 내승별감, 직성군 등을 역임한 관리.
    '노영손': {'role': 'other'},  # 조선/조선 전기 - 조선 전기, 중종반정 이후에 형성된 정국공신 중심 체제에 불만을 품었던 이과 등의 무리를 역모죄로 무고하였던 문...
    '노영수': {'role': 'other'},  # 고려 - 고려후기 서운부정, 대호군, 밀직사 등을 역임한 관리.
    '노영순': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 합문지후, 참지정사, 문하시랑평장사 등을 역임한 문신.
    '노영의': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 다봉 등을 역임한 문신.
    '노영재': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 중국에서 활동한 독립운동가.
    '노영희': {'role': 'other'},  # 고려 - 고려후기 삼별초의 난과 관련된 무신.
    '노우명': {'role': 'scholar'},  # 조선 - 조선 전기에, 음운학에 조예가 깊었으며, 현릉참봉을 역임하였으나 기묘사화에 연루되어 파직된 학자.
    '노원섭': {'role': 'other'},  # 근대/대한제국기 - 대한제국기 때, 공주 용당에서 의진을 결성하였으며, 국권 피탈 이후 고향에서 독립만세시위를 전개한 의병장 · 독...
    '노원순': {'role': 'other'},  # 고려 - 고려후기 상장군, 중군병마사 등을 역임한 무신.
    '노을룡': {'role': 'other foreigner'},  # 근대 - 일제강점기 때, 중국의 국민혁명군으로 복무하며 의열단에서 활동하였고, 조선인 군관학교 교관을 역임하며 친일파 및 밀정 처단...
    '노응규': {'role': 'other foreigner'},  # 근대/개항기 - 개항기 때, 안의에서 의병을 일으켰고, 일본군 및 척후대 공격, 경부철도 파괴 활동 등을 전개한 의병장.
    '노응환': {'role': 'other'},  # 조선 - 조선 중기에, 임진왜란이 발발하자 의병에 자원하였으며, 금산전투에서 항전하다 전사한 의병.
    '노이형': {'role': 'other'},  # 조선 - 조선 후기에, 예조정랑, 춘추관기주관, 전적 등을 역임한 문신.
    '노인': {'role': 'other'},  # 조선 - 조선시대 황해수사, 진용교위 등을 역임한 장수.
    '노인수': {'role': 'other'},  # 고려 - 고려후기 분도장군, 상장군 등을 역임한 무신.
    '노인우': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 인주수령 등을 역임한 문신.
    '노임수': {'role': 'other'},  # 근대 - 대한제국기 때, 의병장 김동신의 휘하에서 활동하다가 직접 의병을 규합하여 항일의병투쟁을 전개한 의병장.
    '노자영': {'role': 'poet essayist'},  # 근대 - 일제강점기 『처녀의 화환』, 『내 혼이 불탈 때』, 『백공작』 등을 저술한 시인. 수필가.
    '노자형': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 사성, 대사성, 첨지중추부사 등을 역임한 문신.
    '노장': {'role': 'other'},  # 「봉산탈춤」, 「강령탈춤」, 「송파산대놀이」, 「양주별산대놀이」에 등장하는 배역.
    '노재철': {'role': 'other'},  # 근대 - 일제강점기 때, 충남, 전북 등지에서 군자금 모금 활동을 전개한 독립운동가.
    '노전': {'role': 'other'},  # 고려/고려 전기 - 고려 전기에, 중추부사 상호군, 삼사사, 호부상서 등을 역임한 문신.
    '노정': {'role': 'other'},  # 고려 - 고려전기 어사중승, 행영도병마부사, 예빈경 등을 역임한 관리.
    '노정섭': {'role': 'scholar'},  # 근대 - 개항기 때, 개항에 반대하는 척화상소를 올렸으나 받아들여지지 않자, 학문에 전념하여 『연곡집』을 저술한 학자.
    '노종': {'role': 'other'},  # 고대/삼국 - 삼국시대 금관가야 제10대 구형왕의 첫째 아들인 왕자.
    '노종균': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 한인애국단원으로 활동한 독립운동가.
    '노준': {'role': 'other'},  # 조선 - 조선 전기에, 동래부사, 파주목사, 관찰사 등을 역임한 문신.
    '노준명': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 홍원목사 등을 역임한 문신.
    '노중례': {'role': 'other'},  # 조선/조선 전기 - 조선전기 판전의감사, 첨지중추원사, 상호군 등을 역임한 의관.
    '노지': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 때, 이찬 관등으로 사량궁의 사신을 역임한 신라의 관리.
    '노지정': {'role': 'other'},  # 고려/고려 후기 - 고려 후기, 희종복위 참소사건에 연루되어 최우에게 죽임을 당한 무신.
    '노직': {'role': 'other'},  # 조선 - 조선 중기에, 병조판서, 판중추부사 등을 역임한 문신.
    '노진': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 대사헌, 예조판서 등을 역임한 문신.
    '노진규': {'role': 'other'},  # 현대 - 해방 이후 「동래야류」의 전승자로 지정된 예능보유자.
    '노진룡': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 임시정부 전라북도 총감독으로 임명되어 군자금 모금 활동을 전개한 독립운동가.
    '노진설': {'role': 'other'},  # 현대 - 해방 이후 중앙선거관리위원장, 감찰위원장 등을 역임한 법조인.
    '노진의': {'role': 'other'},  # 고려 - 고려후기 낭장, 장군 등을 역임한 무신.
    '노창성': {'role': 'other'},  # 근대 - 일제강점기 경성방송국 제2방송부장, 서울중앙방송국 국장, 방송관리국 국장 등을 역임한 방송인. 친일반민족행위자.
    '노책': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 좌정승, 집현전학사 등을 역임하였으며, 딸이 원의 태자비가 되자 권세를 부리다가 기철 등과의 역모...
    '노천명': {'role': 'poet'},  # 근대/일제강점기 - 일제강점기 『산호림』 · 『창변』 · 『별을 쳐다보며』 등을 저술한 시인. 친일반민족행위자.
    '노춘근': {'role': 'other'},  # 조선 - 조선시대 임진왜란 당시 당포해전에 참전한 무신.
    '노탁유': {'role': 'other'},  # 고려 - 고려후기 서북면지병마사, 흥위위섭상장군, 용호군상장군 등을 역임한 무신.
    '노태준': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 한국광복군 간부로 활동한 독립운동가.
    '노필': {'role': 'other'},  # 조선 - 조선 전기에, 공조좌랑, 경상도도사 등을 역임한 문신.
    '노한': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 우찬성사, 대사헌, 우의정 등을 역임한 문신.
    '노한문': {'role': 'other'},  # 조선 - 조선 전기에, 사헌부지평, 교서관판교, 통례원좌통례 등을 역임한 문신.
    '노현용': {'role': 'other'},  # 고려 - 고려 전기에. 진사, 사신 등을 역임한 문신.
    '노협': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 정주목사 등을 역임한 문신.
    '노형규': {'role': 'other'},  # 근대 - 일제강점기 때, 임시정부 지원을 위해 군자금 모금 활동을 전개한 독립운동가.
    '노형하': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 승정원주서, 지평, 정언 등을 역임한 문신.
    '노홍기': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 익산군수 등을 역임한 문신.
    '노효돈': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 중낭장, 동지추밀원사, 문하시랑평장사 등을 역임한 문신.
    '노흠': {'role': 'scholar'},  # 조선 - 조선 중기에, 참봉, 봉사가 되었으나 낙향하여 학문과 수행에 전념하였으며, 『입재고』 등을 저술한 학자.
    '노힐부득': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 제33대 성덕왕 때 미륵불이 된 염불하는 승려.
    '녹진': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 집사부시랑을 역임한 관리.
    '논개': {'role': 'other'},  # 조선 - 조선시대 임진왜란 당시 의기(義妓)로 알려진 기생.
    '뇌음신': {'role': 'other'},  # 고대/삼국/고구려 - 삼국시대 고구려의 술천성 침공 당시의 장수.
    '뇌질주일': {'role': 'other'},  # 고대/삼국 - 삼국시대 대가야의 건국 시조.
    '뇌질청예': {'role': 'other'},  # 고대/삼국 - 삼국시대 금관가야의 건국 시조.
    '뇌학': {'role': 'other'},  # 조선 - 조선후기 명주사 자흠의 제자로 설송의 법맥을 계승한 승려.
    '누한': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 제17대(재위:356~402) 왕.
    '눌지마립간': {'role': 'other'},  # 신라의 제19대(재위: 417년~458년) 왕.
    '눌최': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 앵잠, 봉잠, 기현 3성전투에 참전한 장수.
    '능귀문': {'role': 'other foreigner'},  # 고대/삼국/백제 - 삼국시대 백제의 제27대 위덕왕 때 불교를보급하기 위하여 일본에 파견된 기술자.
    '능달': {'role': 'other'},  # 고려/고려 전기 - 고려전기 호족으로 왕경에 초치된 무신.
    '능문': {'role': 'other'},  # 고대/남북국/통일신라 - 고려전기 대광으로 후백제의 신라 침입을 방비하기 위하여 파견된 장수.
    '능범': {'role': 'other'},  # 고려 - 고려전기 내봉낭중, 내장 및 동궁 식읍의 심곡사 등을 역임한 관리.
    '능선': {'role': 'other'},  # 고려/고려 전기 - 고려전기 나주에서 유금필, 충질 등과 견훤의 고려 투항을 인솔한 관리.
    '능식': {'role': 'other'},  # 고려/고려 전기 - 고려 전기에, 순군낭중 등을 역임한 관리 · 공신.
    '능신': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 백수성전투에 참전한 장수.
    '능안': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 나마 긴주의 아들로 가야춤에 능했던 음악인.
    '능애': {'role': 'other'},  # 고대/남북국 - 후백제의 제1대 왕, 견훤의 동생인 왕족.
    '능여': {'role': 'other'},  # 고대/남북국 - 남북국시대 직지사를 중창한 승려.
    '능예': {'role': 'other'},  # 고대/남북국 - 남북국시대 후백제 견훤의 열째 아들인 왕자.
    '능예남': {'role': 'other'},  # 고대/남북국 - 남북국시대 후백제 견훤의 궁녀.
    '능준': {'role': 'other'},  # 고려 - 고려전기 수순군부경(守徇軍部卿), 내봉경 등을 역임한 관리.
    '능창': {'role': 'other'},  # 고대/남북국/후백제 - 후삼국 시기 서남해안 나주 압해도를 중심으로 해상 세력을 이끌었던 인물.
    '능현': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 매조성장군을 역임한 호족.
    '능혜': {'role': 'other'},  # 고려/고려 전기 - 고려전기 내군경을 역임한 관리.
    '능환': {'role': 'other'},  # 고대/남북국 - 남북국시대 때, 후백제의 왕인 견훤을 금산사에 유폐하고, 넷째 아들 금강을 살해한 관리.
    '다루왕': {'role': 'other'},  # 고대/삼국/백제 - 백제의 제2대(재위: 28년~77년) 왕.
    '다리': {'role': 'other'},  # 고대/삼국 - 삼국시대 백제의 무령왕릉에서 출토된 은팔찌를 제작한 공예가.
    '다미': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 나당연합군의 백제 정벌 당시의 장수.
    '다상': {'role': 'other foreigner'},  # 고대/삼국시대 - 삼국시대 백제에서 일본에 건너가 불교 전파에 공헌한 승려.
    '다식': {'role': 'other'},  # 고대/삼국/고구려 - 삼국시대 고구려 소형으로 고구려 부흥에 힘쓴 귀족. 부흥운동가.
    '다지': {'role': 'other'},  # 고려 - 고려후기 수졸, 낭장 등을 역임한 무신.
    '단경왕후': {'role': 'other'},  # 조선/조선 전기 - 조선전기 제11대 중종의 왕비.
    '단군': {'role': 'other'},  # 고대/초기국가/고조선 - 고조선의 제1대(재위:BCE.2333~BCE.1122) 왕.
    '단양이': {'role': 'scholar foreigner'},  # 고대/삼국/백제 - 삼국시대 때, 오경박사로서 일본에 파견된 백제의 학자.
    '단의왕후': {'role': 'other'},  # 조선/조선 후기 - 조선후기 제20대 경종의 왕비.
    '단의장옹주': {'role': 'other'},  # 고대/남북국/통일신라 - 통일신라의 제48대 경문왕의 누이로, 미륵불에 귀의하여 독실한 신자가 된 왕족.
    '단종': {'role': 'other'},  # 조선의 제6대(재위: 1452년~1455년) 왕.
    '달가': {'role': 'other'},  # 고대/삼국/고구려 - 고구려의 제13대 서천왕의 동생이자 제14대 봉상왕의 작은 아버지로, 안국군에 봉해져 군사업무를 관장하였으나,...
    '달공': {'role': 'scholar'},  # 고려 - 고려후기 『법어』을 저술한 승려.
    '달관': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 나당연합군의 고구려 정벌 당시의 장수.
    '달달박박': {'role': 'other'},  # 고대/남북국시대 - 남북국시대 통일신라의 제33대 성덕왕 때 아미타불로 화현한 염불하는 승려.
    '달사': {'role': 'other'},  # 고대/삼국/백제 - 삼국시대 백제의 고구려 도살성 함락 당시의 장수.
    '달선': {'role': 'other'},  # 조선/조선 후기 - 조선후기 유점사 승통, 보현사 수호총섭 등을 역임한 승려.
    '달자': {'role': 'other'},  # 고려/고려 후기 - 고려후기 개경 연복사를 중심으로 활동한 승려.
    '달전': {'role': 'poet'},  # 고려/고려 후기 - 고려후기 「연경 호천사의 9층대탑에 올라」 · 「이하의 장진주 운을 따라 짓다」 등을 저술한 승려. 시인.
    '담릉': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 화랑 김원술을 보좌한 관리.
    '담수': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 「날현인」을 지은 승려.
    '담양군': {'role': 'other'},  # 조선/조선 전기 - 조선전기 제4대 세종의 서자인 왕자.
    '담욱': {'role': 'other'},  # 고대/삼국시대 - 삼국시대 백제의 계율을 확립시킨 승려.
    '담육': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 수나라 유학승으로 신라 불교에 큰 영향을 끼친 승려.
    '담진': {'role': 'other'},  # 고려 - 고려전기 예종의 국사로 활동한 승려.
    '담징': {'role': 'other foreigner'},  # 고대/삼국 - 삼국시대 일본 호류사금당벽화(사불정토도)를 그린 승려. 화가.
    '담혜': {'role': 'other foreigner'},  # 고대/삼국시대 - 삼국시대 백제에서 일본에 건너가 불교 전파에 공헌한 승려.
    '담휴': {'role': 'other'},  # 고려/고려 전기 - 고려전기 제16대 예종의 왕사로 추봉된 승려.
    '답본춘초': {'role': 'other'},  # 고대/삼국/백제 - 삼국시대 백제 멸망 후 왜국에서 대산하를 역임한 유민. 유신(遺臣).
    '당성': {'role': 'other'},  # 조선 - 조선 전기에, 개성부부유후, 공안부윤 등을 역임한 문신.
    '당원': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 때, 이찬 관등으로 중시를 역임한 통일신라의 관리.
    '당천': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 사찬을 역임한 장수.
    '대간지': {'role': 'other'},  # 고대/남북국 - 남북국시대 발해에서 산수화를 잘 그린 화가.
    '대건황': {'role': 'other'},  # 고대/남북국/발해 - 발해의 제12대(재위: 858년~871년) 왕.
    '대경한': {'role': 'other'},  # 고대/남북국/발해 - 남북국시대 흥요국의 관리였던 발해의 유민.
    '대고장': {'role': 'other'},  # 큰북［大鼓］을 제작하는 장인(匠人).
    '대곡': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 사도성 수복 당시의 장수.
    '대공': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 아찬 대렴과 함께 반란을 일으킨 관리.
    '대광현': {'role': 'other'},  # 고대/남북국/발해 - 고려 전기에, 발해에서 고려로 귀화한 왕족.
    '대굉림': {'role': 'other'},  # 고대/남북국/발해 - 남북국시대 발해의 제3대 문왕 대흠무의 아들인 왕자.
    '대구': {'role': 'scholar'},  # 고대/삼국 - 삼국시대 신라의 각간 위홍과 『삼대목』을 저술한 승려.
    '대당': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 일모산군 태수를 역임한 관리.
    '대도리경': {'role': 'other'},  # 고대/남북국/발해 - 고려전기 발해에서 고려로 귀화한 유민.
    '대도리행': {'role': 'other'},  # 고대/남북국/발해 - 남북국시대 발해의 제2대 무왕 대무예의 장남인 왕자.
    '대도수': {'role': 'other'},  # 고려/고려 전기 - 고려전기 중랑장, 장군 등을 역임한 관리. 무신.
    '대도행랑': {'role': 'other'},  # 고대/남북국/발해 - 고려전기 발해에서 고려로 귀화한 유민.
    '대렴': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 일길찬 대공과 함께 반란을 일으킨 관리.
    '대령후': {'role': 'other'},  # 고려/고려 전기 - 고려전기 제17대 인종의 둘째 아들인 왕자.
    '대륜': {'role': 'other'},  # 현대/대한민국 - 해방 이후 태고종 종정, 한국불교태고종 원로원장 등을 역임한 승려.
    '대명궁부인': {'role': 'other'},  # 고려 - 고려전기 제5대 경종의 제5왕비.
    '대명주원부인': {'role': 'other'},  # 고려 - 고려전기 제1대 태조의 제14왕비.
    '대목왕후': {'role': 'other'},  # 고려/고려 전기 - 고려전기 제4대 광종의 왕비.
    '대무신왕': {'role': 'other'},  # 고대/삼국/고구려 - 삼국시대 고구려 제3대(재위: 18~44) 왕.
    '대문': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라에서 대문의 난을 일으킨 고구려의 유민.
    '대문예': {'role': 'other'},  # 고대/남북국/발해 - 남북국시대 발해의 시조 대조영의 둘째 아들인 왕자.
    '대방공': {'role': 'other'},  # 고려/고려 전기 - 고려전기 제15대 숙종의 아들인 왕자.
    '대범': {'role': 'other'},  # 고대/남북국 - 삼국시대 신라에서 당나라와 인도로 건너가 유학하며 불법을 공부한 승려.
    '대복모': {'role': 'other'},  # 고대/남북국/발해 - 고려전기 발해에서 고려로 귀화한 유민.
    '대봉예': {'role': 'other'},  # 고대/남북국/발해 - 남북국시대 때, 하정사로 당나라에 방문했다가, 신라 사신과 발해 사신의 자리 다툼인 쟁장사건에 연루된 발해의 왕족.
    '대서원부인': {'role': 'other'},  # 고려 - 고려전기 제1대 태조의 제19왕비.
    '대서지': {'role': 'other'},  # 고대/삼국/신라 - 신라의 제13대 왕, 미추이사금의 동생이자 제18대 실성이사금의 아버지로, 이찬에 임명된 왕족.
    '대세': {'role': 'other foreigner'},  # 고대/남북국 - 삼국시대 선술을 체득하기 위해 중국으로 건너간 신라 진평왕대의 귀족.
    '대소': {'role': 'other'},  # 고대/초기국가 - 부여의 제5대(재위:BCE.20~CE.22) 왕.
    '대승': {'role': 'other'},  # 고대/삼국 - 고구려 시대 낙랑군에 투항한 잠지락부의 족장.
    '대신덕': {'role': 'other'},  # 고대/남북국/발해 - 남북국시대 발해의 제10대 선왕의 아들인 왕자.
    '대심리': {'role': 'other'},  # 고대/남북국/발해 - 고려전기 발해에서 고려로 귀화한 유민.
    '대안': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 삼국 통일기 원효와 함께 활동했던 승려.
    '대야발': {'role': 'scholar'},  # 고대/남북국/발해 - 발해의 제1대 왕, 대조영의 동생으로, 『단기고사』를 저술한 왕족.
    '대양왕': {'role': 'other'},  # 고대/삼국/고구려 - 고구려의 마지막 왕, 보장왕의 아버지인 왕족.
    '대연': {'role': 'other'},  # 고려 - 남북국시대 삼중대사를 역임한 승려.
    '대연림': {'role': 'other'},  # 고대/남북국/발해 - 발해의 부흥국인 흥료국의 제1대 왕.
    '대연정': {'role': 'other'},  # 고대/남북국/발해 - 남북국시대 발해의 부흥국인 흥료국의 태사를 역임한 관리. 장수.
    '대우': {'role': 'scholar'},  # 조선 - 조선후기 『예수시왕생칠재의찬요』를 저술한 승려.
    '대운': {'role': 'other'},  # 조선 - 조선후기 도갑사 회성의 제자가 되어 법맥을 계승한 승려.
    '대원공': {'role': 'other'},  # 고려/고려 전기 - 고려전기 제15대 숙종의 다섯째 아들인 왕자.
    '대원균': {'role': 'other'},  # 고대/남북국/발해 - 고려전기 발해에서 고려로 귀화한 유민.
    '대원의': {'role': 'other'},  # 고대/남북국/발해 - 발해의 제4대(재위: 793년~794년) 왕.
    '대위해': {'role': 'other'},  # 고대/남북국/발해 - 발해의 제14대(재위: 894년~906년) 왕.
    '대유범': {'role': 'other'},  # 고대/남북국/발해 - 고려전기 발해에서 고려로 귀화한 유민.
    '대은': {'role': 'other'},  # 현대/대한민국 - 해방 이후 팔만대장경 번역위원회 위원, 동국역경원 역경위원 등을 역임한 승려. 포교사.
    '대의': {'role': 'other'},  # 현대/대한민국 - 해방 이후 대한불교총연합회 이사장, 한민족총회결성준비위원회 부회장 등을 역임한 승려.
    '대이진': {'role': 'other'},  # 고대/남북국/발해 - 발해의 제11대(재위: 830년~858년) 왕.
    '대인': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 고구려 낭비성 함락에 공헌한 장수.
    '대인선': {'role': 'other'},  # 발해의 제15대(재위: 906년~926년) 왕.
    '대일하': {'role': 'other'},  # 고대/남북국/발해 - 발해의 제2대 무왕 대무예의 사촌 형으로, 당과의 대립을 두려워하여 흑수말갈에 대한 선제공격을 거절한 무왕의 ...
    '대장': {'role': 'other'},  # 고대/남북국/통일신라 - 통일신라의 제29대 왕, 태종 무열왕의 후손으로, 이찬에 임명되어 중시 등을 역임한 종실.
    '대정': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 이찬으로 중시를 지낸 귀족.
    '대존': {'role': 'other'},  # 고대/남북국/통일신라 - 통일신라의 제54대 경명왕의 장인으로, 각간에서 성희대왕으로 추봉된 귀족.
    '대종': {'role': 'other'},  # 고려/고려 전기 - 고려의 제6대 왕, 성종의 아버지로, 예성선경대왕에 추존된 왕족.
    '대진림': {'role': 'other'},  # 고대/남북국/발해 - 남북국시대 때, 발해에서 조공사로 후당에 파견되었으나, 발해의 몰락으로 고려에 망명한 발해의 왕족.
    '대집성': {'role': 'other'},  # 고려/고려 후기 - 고려 후기, 대장군(大將軍), 어사대부(御史大夫), 수사공(守司空) 등을 역임한 관리이자 무신.
    '대창발가': {'role': 'other'},  # 고대/남북국/발해 - 발해의 제2대 무왕 대무예의 동생으로, 당나라에 사신으로 가서 좌위위원외장군으로 임명된 발해의 왕족.
    '대충': {'role': 'other'},  # 현대/대한민국 - 해방 이후 대한불교천태종 제2대 종정 등을 역임한 승려.
    '대토': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 아찬으로 당나라와 내통하려다 발각된 관리.
    '대통': {'role': 'other'},  # 고대/남북국 - 남북국시대 통일신라에서 당나라로 유학하며 불법을 공부한 승려.
    '대현': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 살찬으로 태대각간을 역임한 귀족.
    '대현석': {'role': 'other'},  # 고대/남북국/발해 - 발해의 제13대(재위: 871년~893년) 왕.
    '대화균': {'role': 'other'},  # 고대/남북국/발해 - 고려전기 발해에서 고려로 귀화한 유민.
    '대흔': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 때, 반란으로 왕위에 오른 신무왕이 죽고 문성왕이 즉위하자 이찬 김식과 함께 반역을 꾀한 통일신...
    '덕기': {'role': 'other'},  # 근대 - 일제강점기 범어사 주지, 임시정부 고문 등을 역임한 승려.
    '덕녕공주': {'role': 'other'},  # 고려/고려 후기 - 고려후기 제28대 충혜왕의 왕비.
    '덕래': {'role': 'other foreigner'},  # 고대/삼국/백제 - 삼국시대 일본조정에서 의약을 담당한 백제 출신의 의약인.
    '덕복': {'role': 'other'},  # 고대/남북국/통일신라 - 신라 문무왕 때 당에서 숙위로 활동하고, 귀국할 때 새로운 역법을 전한 인물.
    '덕비': {'role': 'other'},  # 고려 - 고려후기 제32대 우왕의 제7왕비.
    '덕소': {'role': 'other'},  # 고려 - 고려시대 선사, 대선사, 왕사 등을 역임한 승려.
    '덕안대군': {'role': 'other'},  # 조선/조선 전기 - 조선전기 제1대 태조의 여섯째 아들인 왕자.
    '덕양군': {'role': 'other'},  # 조선 - 조선전기 제11대 중종의 서자인 왕자.
    '덕양후': {'role': 'other'},  # 고려 - 고려후기 제20대 신종의 아들인 왕자.
    '덕연': {'role': 'other'},  # 고려/고려 전기 - 고려전기 제16대 예종의 왕사, 제17대 인종의 국사로 책봉된 승려.
    '덕원군': {'role': 'other'},  # 조선 - 조선전기 제7대 세조의 셋째 아들인 왕자.
    '덕자진': {'role': 'other foreigner'},  # 고대/삼국 - 삼국시대 일본왕 지토로부터 의박사 칭호를 받은 백제 출신의 의약인.
    '덕종': {'role': 'other'},  # 조선/조선 전기 - 조선 세조의 첫째 아들로, 왕세자로 책봉되었으나, 20세에 사망한 후 성종에 의해 추존된 왕.
    '덕좌왕': {'role': 'other foreigner'},  # 고대/삼국/백제 - 삼국시대 일본 백제기의 시조.
    '덕지': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 삽량성전투에 참전한 장수.
    '덕진': {'role': 'other'},  # 근대 - 조선후기 경순(敬淳)과 더불어 당대의 뛰어난 선지식으로 불린 승려.
    '덕창': {'role': 'other'},  # 고려 - 고려전기 제16대 예종의 왕사를 역임한 승려.
    '덕혜옹주': {'role': 'other foreigner'},  # 근대 - 조선의 제26대 왕, 고종의 딸로, 일제에 의해 일본에서 교육을 받고, 대마도 번주의 아들과 정략결혼을 한 왕족.
    '덕흥군': {'role': 'other'},  # 고려/고려 후기 - 고려 후기, 제26대 충선왕의 셋째 아들인 왕자.
    '도경유': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 금부도사, 평양서윤 등을 역임한 문신.
    '도금봉': {'role': 'other'},  # 현대 - 해방 이후 「상록수」, 「또순이」, 「토지」 등에 출연한 배우. 영화배우.
    '도길부': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 제조정방, 서북면도체찰사, 찬성사 등을 역임한 문신.
    '도대철': {'role': 'other'},  # 현대 - 한국전쟁 당시 강원도 양구의 949고지전투에 참전한 군인.
    '도도': {'role': 'other'},  # 고대/삼국/신라 - 신라 진흥왕대에 백제와 벌인 관산성전투 때 신라 편에 서서 활약한 지방 유력자.
    '도동음률': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라에 내항한 탐라국의 왕. 관리.
    '도두': {'role': 'other'},  # 고대/삼국/고구려 - 삼국시대 고구려 태조왕대 고구려에 투항한 갈사국의 왕족.
    '도등': {'role': 'other foreigner'},  # 고대/삼국/고구려 - 삼국시대 고구려에서 일본에 건너가 불교 전파에 공헌한 승려.
    '도령': {'role': 'other foreigner'},  # 고대/삼국/백제 - 삼국시대 백제에서 일본으로 건너가 불경을 공부한 승려.
    '도림': {'role': 'other'},  # 고대/삼국/고구려 - 삼국시대 고구려 밀사로 백제에 파견된 승려.
    '도모': {'role': 'other'},  # 고대/삼국/백제 - 삼국시대 백제의 시조.
    '도문': {'role': 'other'},  # 조선 - 조선후기 수호일품대승 칭호를 받고 개운사를 수호한 승려.
    '도미': {'role': 'other'},  # 고대/삼국/백제 - 삼국시대 백제 「도미설화」의 주인공.
    '도상봉': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 「한정」 · 「고궁」 · 「이조백자」 등의 작품을 그린 화가.
    '도생': {'role': 'other'},  # 고려 - 고려전기 법주사 주시, 승통, 금산사 주지 등을 역임한 승려.
    '도선': {'role': 'scholar'},  # 고대/남북국시대 - 남북국시대 통일신라의 『도선비기』, 『송악명당기』, 『도선답산가』 등을 저술한 승려.
    '도설지': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 급간지, 대등 등을 역임한 귀족.
    '도설지왕': {'role': 'other'},  # 고대/삼국/가야 - 대가야의 제3대(재위: ?~562년) 왕.
    '도성': {'role': 'other'},  # 고대/남북국 - 삼국시대 신라 『삼국유사』의 포산이성조와 관련된 승려.
    '도성기': {'role': 'other'},  # 고려/고려 후기 - 고려후기 낭장, 장군 등을 역임한 환관.
    '도성유': {'role': 'scholar'},  # 조선 - 조선 후기에, 『성리정학집』, 「체용각분도」, 「오경체용합일도」 등을 저술한 문신.
    '도신수': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 호조정랑, 함흥판관, 울산부사 등을 역임한 문신.
    '도신여': {'role': 'other'},  # 조선 - 조선 후기에, 용담현령, 예조정랑, 성균관사예 등을 역임한 문신.
    '도신징': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 강릉참봉, 용궁현감, 통훈대부 등을 역임한 문신.
    '도심': {'role': 'other foreigner'},  # 고대/삼국 - 삼국시대 백제에서 담혜 등과 일본으로 건너간 일본 최초의 승려.
    '도안': {'role': 'scholar'},  # 조선 - 조선 후기, 편양파의 주류 계보를 잇고 화엄학을 진흥시킨 학승으로 『월저당대사집』을 저술한 승려.
    '도엄': {'role': 'other foreigner'},  # 고대/삼국/백제 - 삼국시대 백제의 사신 은솔 수신 등과 일본에 파견된 승려.
    '도연': {'role': 'other'},  # 조선 - 조선후기 대둔사(大芚寺) 총오의 제자로 연담의 법맥을 계승한 승려.
    '도예종': {'role': 'other'},  # 현대/대한민국 - 대한민국 8·15광복 이후 민주화, 통일운동을 전개한 진보적 활동가.
    '도오': {'role': 'other'},  # 현대/대한민국 - 일제강점기 설곡의 검선일여비법을 전수받은 승려. 선무술가(禪武術家).
    '도옥': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 조천성전투에 참전한 최초의 호국 승려.
    '도원': {'role': 'other'},  # 고려 - 고려전기 우가승록을 역임한 승려.
    '도유호': {'role': 'scholar'},  # 현대 - 북한에서 함흥시립도서관장, 김일성종합대학의 교수와 고고학연구소장 등을 역임하였으며, 북한 고고학 발전에 공을 세운 고고학자.
    '도육': {'role': 'other'},  # 고려 - 남북국시대 당나라로 유학가서 천태산을 순례한 승려.
    '도윤': {'role': 'other'},  # 고대/남북국 - 남북국시대 통일신라 사자산문의 승려.
    '도응': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 찬성사 등을 역임한 문신.
    '도응유': {'role': 'scholar'},  # 조선 - 조선 후기에, 이괄의 난이 발발하자 의병을 일으켰으며, 정묘호란 때 소모장으로 활동한 학자 · 의병장.
    '도의': {'role': 'other foreigner'},  # 고대/남북국/통일신라 - 남북국시대 최초로 중국의 남종선을 신라에 전한 승려.
    '도인권': {'role': 'other foreigner'},  # 근대 - 일제강점기, 안악사건으로 옥고를 치르고 평양 3·1운동에 참여한 후 중국 상하이 대한민국 임시정부 군무부 군사 국장, 무관...
    '도일': {'role': 'other'},  # 조선/조선 후기 - 조선후기 선암사 운수난야 지장시왕도, 선암사 선조암 신중도, 운주사 신중도 등을 그린 승려. 화승.
    '도장': {'role': 'scholar foreigner'},  # 고대/삼국/백제 - 삼국시대 백제에서 일본으로 건너가 『성실론소』를 저술한 승려.
    '도절': {'role': 'other'},  # 고대/삼국/고구려 - 삼국시대 고구려 제2대 유리명왕의 첫째 태자.
    '도조': {'role': 'other'},  # 조선/조선 전기 - 조선의 제1대 왕, 태조의 조부로, 원나라에서 아버지의 천호 관직을 계승받았으며, 조선 건국 후에 추존된 왕족.
    '도증': {'role': 'scholar'},  # 고대/남북국/통일신라 - 삼국시대 신라의 『금강반야경소』, 『인명입정리론소』 등을 저술한 승려.
    '도침': {'role': 'other'},  # 고대/삼국 - 삼국시대 백제의 재건을 주도하던 부흥운동가. 승려.
    '도한기': {'role': 'scholar'},  # 근대 - 조선 후기에, 『춘추의례』, 『사례절략』, 『심근강의』 등을 저술한 학자.
    '도현': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 승려로 견당사의 통역과 당나라 관공서와의 교섭 등을 담당한 역관.
    '도형': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 전적, 공조좌랑, 형조좌랑, 호조좌랑 등을 역임한 문신.
    '도화랑': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 때, 신라 진지왕의 혼령과 동침하여 아들 비형랑을 낳은 왕족.
    '도흔': {'role': 'other foreigner'},  # 고대/삼국/백제 - 삼국시대 백제 승려로, 오나라에서 백제로 오던 중 풍랑으로 표류하다 일본에 정착한 승려.
    '도흥': {'role': 'other'},  # 고려 - 고려후기 전라도도순문사, 원수, 양광도 상원수 등을 역임한 무신.
    '독고립': {'role': 'other'},  # 조선 - 조선후기 군자감판관, 호조참의 등을 역임한 무신.
    '독고성': {'role': 'other'},  # 조선/조선 후기 - 조선후기 병자호란 당시 의주성전투에 참전한 무신.
    '독고전': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 국경청년연맹 검사위원, 조공, 고려공산청년회 해외 연락원 등을 지낸 사회주의운동가.
    '독보': {'role': 'other'},  # 조선 - 조선후기 병자호란 때 명나라에 사신으로 파견된 승려.
    '돌고': {'role': 'other'},  # 고대/삼국/고구려 - 삼국시대 고구려 제13대 서천왕의 아들인 왕자.
    '동기달': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「강릉학산오독떼기」 전승자로 지정된 예능보유자.
    '동륜': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라 제24대 진흥왕의 첫째 아들인 왕자.
    '동명성왕': {'role': 'other'},  # 고대/삼국/고구려 - 고구려의 제1대(재위: BCE. 37~BCE. 19) 왕.
    '동산원부인': {'role': 'other'},  # 고려/고려 전기 - 고려전기 제1대 태조의 후비.
    '동석기': {'role': 'other'},  # 현대/대한민국 - 일제강점기 때, 함경남도 북청에서 최초의 그리스도 교회인 함전그리스도교회를 설립하였으며, 교인들의 민족의식을 고취...
    '동성왕': {'role': 'other'},  # 고대/삼국/백제 - 백제의 제24대(재위: 479년~501년) 왕.
    '동성자막고': {'role': 'other foreigner'},  # 고대/삼국/백제 - 삼국시대 백제의 덕솔로서 일본에 파견된 관리.
    '동소': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 주재성 성주를 역임한 장수.
    '동수': {'role': 'other'},  # 고대/삼국/고구려 - 삼국시대 모용부에서 고구려에 귀화한 유민.
    '동양원부인': {'role': 'other'},  # 고려/고려 전기 - 고려전기 제1대 태조의 제9왕비.
    '동완': {'role': 'scholar'},  # 한국외국어대학교와 고려대학교에서 교수 등을 역임하였으며, 『노한사전』, 『소련 청소년과 러시아문학』 등을 저술하며 한국의 러시아문학...
    '동천왕': {'role': 'other'},  # 고구려의 제11대(재위: 227년~247년) 왕.
    '동타천': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 북한산성 성주를 역임한 지방관.
    '동풍신': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 함경북도에서 전개된 독립만세운동에 참여한 독립운동가.
    '두경승': {'role': 'other'},  # 고려후기 서북면병마사, 평장사, 문하시중 등을 역임한 무신.
    '두로': {'role': 'other'},  # 고대/삼국/고구려 - 삼국시대 고구려 제5대 모본왕을 시해한 관리.
    '두방루': {'role': 'other'},  # 고대/삼국/고구려 - 삼국시대 고구려 적봉진전투에 참전한 장수.
    '두사지': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라에서 고구려 사절로 가는 김춘추에게 청포 300포를 준 관리.
    '두삼': {'role': 'other'},  # 근대/개항기 - 조선후기 백련사 괘불도, 남양주 흥국사 팔상도 등의 불화를 제작한 승려. 화승.
    '두선': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 아찬으로 석문전투에 참전한 관리. 장군.
    '두운': {'role': 'other'},  # 조선 - 조선후기 전평과 대흥사 만일암을 중창한 승려.
    '두질': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 신라의 군사(軍師)로 사비성전투에 참전한 관리.
    '두훈': {'role': 'other'},  # 조선/조선 후기 - 조선후기 법주사 괘불도, 통도사 괘불도 등을 그린 승려. 화승.
    '둔륜': {'role': 'scholar'},  # 고대/남북국 - 삼국시대 신라의 『승만경소』, 『금광명경약기』, 『아미타경소』 등을 저술한 승려.
    '득오': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 「모죽지랑가」를 지은 낭도.
    '득원': {'role': 'other'},  # 조선 - 조선후기 지리산 용수암에서 수년간 1일 1식으로 수행한 승려.
    '등린': {'role': 'other'},  # 조선 - 조선후기 석왕사 정연의 제자로 궤홍의 법맥을 계승한 승려.
    '류경채': {'role': 'scholar'},  # 서울대학교 서양화과 교수, 창작미술협회 회장 등을 역임하였으며, 「선(船)」, 「폐림지 근방」, 「뒷산」 등의 작품을 그린 화가 ·...
    '류금렬': {'role': 'other'},  # 근대/일제강점기 | 현대 - 해방 이후 북한에서 원산필수품공장 미술가로 활동한 공예가. 염색공예가.
    '류방택': {'role': 'scholar'},  # 조선/조선 전기 - 고려 후기, 서운관(書雲觀)의 판사(判事)를 역임하고 조선 초기에 권근(權近)과 함께 천상열차분야지도(天象列次分...
    '류시훈': {'role': 'other foreigner'},  # 근대 - 일제강점기 때, 중국에서 조선민족혁명당의 지하공작에 참여하였고, 광복군에서 대적선전공작, 초모공작활동을 전개한 독립운동가.
    '류인': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 「파란 Ⅰ」 · 「흙: 난지도」 · 「급행열차: 시대의 변(辯)」 등의 작품을 낸 조각가.
    '류택윤': {'role': 'other'},  # 근대/일제강점기 | 현대 - 해방 이후 「개구리잉크단지」, 「강냉이탁상등」, 「포도잉크단지」 등을 제작한 공예가. 석공예가.
    '류형기': {'role': 'other'},  # 현대/대한민국 - 일제강점기와 해방 후 1950년대에, 기독교교육운동, 문서선교운동, 교회 재건과 복구 운동을 전개한 기독교대한감리...
    '류홍': {'role': 'other'},  # 현대/대한민국 - 경성방직 도감독, 고려방직 이사, 유관순열사기념사업회 회장, 제2·4·6대 국회의원 등을 역임한 정치인 · 기업인.
    '리영희': {'role': 'other'},  # 현대/대한민국 - 대한민국의 언론인 겸 사회운동가.
    '마건': {'role': 'other'},  # 근대/일제강점기 - 일제강점기에 적기단 결성 및 조선공산당 만주총국에서 활동한 사회주의 운동가.
    '마군후': {'role': 'scholar'},  # 조선/조선 후기 - 조선후기 「촌녀채총도」, 「수하승려도」, 「묘도」 등의 작품을 그린 화가.
    '마나': {'role': 'other'},  # 고대/삼국/백제 - 삼국시대 백제의 사신으로 왜에 파견된 장수.
    '마라난타': {'role': 'other'},  # 고대/삼국/백제 - 삼국시대 백제에 불교를 최초로 전한 인도의 승려.
    '마려': {'role': 'other'},  # 고대/삼국/백제 - 삼국시대 때, 백제의 건국 시조인 온조왕을 보좌한 관리.
    '마로': {'role': 'other'},  # 고대/삼국/백제 - 삼국시대 백제의 중좌평을 역임한 장수.
    '마리': {'role': 'other'},  # 고대/삼국/고구려 - 삼국시대 고구려 건국 초기 오이, 협보와 함께 많은 공적을 세운 관리. 공로자.
    '마명': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 노동총동맹의 중앙집행위원, 북풍회 집행위원 등을 역임한 노동운동가.
    '마무': {'role': 'other'},  # 고대/삼국/백제 - 삼국시대 백제의 시덕, 나솔 등을 역임한 관리.
})
        
        # API로부터 자동 수집된 인물 데이터
self.persons.update({
    '가군': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 고구려 장안성 축성의 책임을 맡았던 관리.
    '가귀': {'role': 'scholar'},  # 고대/삼국 - 삼국시대 때, 신라에서 『화엄경의강』, 『심원장』 등을 저술한 승려.
    '가라포고이': {'role': 'other foreigner'},  # 고대/삼국 - 삼국시대 때, 일본에 귀화한 신라의 유민.
    '가루': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 대상(大相) 등을 역임하다 고구려 멸망 후 부흥운동에 참여한 고구려의 귀족.
    '가마': {'role': 'other foreigner'},  # 고대/삼국 - 삼국시대 때, 백제에서 일본으로 파견된 사신.
    '가서일': {'role': 'other foreigner'},  # 고대/삼국 - 삼국시대 때, 일본에서 활약한 고구려 출신의 화가.
    '가실': {'role': 'other'},  # 고대/남북국 - 삼국시대 때, 신라의 사량부 출신으로 변방에서 복무한 군인.
    '가실왕': {'role': 'other'},  # 고대/삼국/가야 - 가야의 제7대(재위: 421년~451년) 왕.
    '각가': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 백제의 좌평 등을 역임한 귀족.
    '각굉': {'role': 'scholar'},  # 고려 - 고려 후기에, 『나옹화상어록』, 『나옹화상행장』 등을 저술한 승려.
    '각덕': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 때, 양나라에 유학한 신라의 승려.
    '각민': {'role': 'scholar'},  # 조선 - 조선 후기에, 청허계 정관문파로 『해의』 등을 저술한 승려.
    '각복모': {'role': 'other foreigner'},  # 고대/삼국 - 삼국시대 때, 백제의 멸망 후 일본으로 망명한 귀족.
    '각성': {'role': 'other'},  # 조선 - 조선시대 때, 판선교도총섭, 팔도도총섭, 규정도총섭 등을 역임한 승려.
    '각안': {'role': 'scholar'},  # 조선/조선 후기 - 조선 후기에, 『동사열전』, 『범해선사유고』 등을 저술한 승려.
    '각우': {'role': 'scholar'},  # 고려 - 고려 후기에, 『자경문』을 저술한 승려.
    '각운': {'role': 'other'},  # 고려 - 고려 후기에, 『경덕전등록』을 중간한 승려.
    '각웅': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 나옹 혜근의 제자로 서기의 직무를 담당한 승려.
    '각유': {'role': 'other'},  # 고려 - 고려 후기에, 경주 기림사 주지, 대선사 등을 역임한 승려.
    '각절왕': {'role': 'other foreigner'},  # 고대/삼국 - 삼국시대 때, 일본의 『신찬성씨록』에 전하는 신라의 왕.
    '각종': {'role': 'other foreigner'},  # 고대/삼국 - 삼국시대 때, 백제의 사비성 함락 사실을 일본 야마토 조정에 보고한 승려.
    '각훈': {'role': 'scholar'},  # 고려 - 고려 후기에, 『해동고승전』을 저술한 승려.
    '간왕': {'role': 'other'},  # 고대/남북국/발해 - 발해의 제9대(재위: 817년~818년) 왕.
    '간위거': {'role': 'other'},  # 고대/초기국가 - 부여의 제10대(재위: 2세기~3세기) 왕.
    '간진': {'role': 'other'},  # 고대/남북국/통일신라 - 신라 진평왕대 곡물 수송을 담당한 왕경 출신의 관리.
    '갈로맹광': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 고구려 원정군의 사령관으로 활약한 장수.
    '갈홍기': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 때, 일본기독교 조선감리교단 연성국장, 일본기독교 조선교단의 종교교육국장 등으로 활동하면서 일본제국주...
    '감경인': {'role': 'other'},  # 조선 - 조선시대 때, 여도만호, 내금위, 정략장군 등을 역임한 무신.
    '강감찬': {'role': 'other'},  # 고려 전기에, 서북면행영도통사, 상원수대장군, 문하시중 등을 역임한 문신.
    '강거효': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 예문관검열, 가예조좌랑, 통훈대부 등을 역임한 문신.
    '강견': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 서인들의 사주를 받아 기축옥사 때 최영경이 정여립과 연루되어 있다고 무고한 유생.
    '강겸': {'role': 'other'},  # 조선 - 조선 전기에, 예조좌랑, 병조정랑, 장령 등을 역임한 문신.
    '강경대': {'role': 'other'},  # 현대/대한민국 - 대한민국의 학생운동가, 시민운동가.
    '강경서': {'role': 'other'},  # 조선 - 조선 전기에, 사헌부집의, 대사간 등을 역임한 문신.
    '강경선': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 대한적십자회 상의원, 대한민국임시정부 교민단 총무, 한국유일독립당 집행위원 등을 역임한 독립운동가.
    '강경애': {'role': 'novelist'},  # 근대 - 일제강점기 때, 「소금」, 「인간 문제」, 「해고」 등을 저술한 소설가.
    '강계식': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「붉은 장갑」, 「원술랑」, 「한강은 흐른다」 등에 출연한 배우.
    '강고': {'role': 'other'},  # 고대/남북국 - 남북국시대 때, 통일신라의 분황사 약사여래상을 주조한 장인.
    '강곤': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 인수부윤, 충청도도절제사, 영안남도절도사 등을 역임한 무신.
    '강공훤': {'role': 'other'},  # 고대/삼국 - 남북국시대 때, 시중, 대장군, 대상 등을 역임한 무신.
    '강구려': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 왜에 억류된 신라 왕족 미사흔의 환국을 호송했던 박제상을 보좌한 신라의 관리.
    '강구손': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 도승지, 경기도관찰사, 우의정 등을 역임한 문신.
    '강국승': {'role': 'other'},  # 고려/고려 후기 - 고려 후기, 무오정변을 통해 최씨 무신정권을 붕괴시켜 위사보좌공신에 책록된 공신이자 무신.
    '강국진': {'role': 'scholar'},  # 현대/대한민국 - 「비닐우산과 촛불이 있는 해프닝」, 「한강변의 타살」, 「역사의 빛」 등의 작품을 그린 화가.
    '강궁진': {'role': 'other'},  # 고려/고려 전기 - 고려 전기, 강감찬의 아버지이자 금주 일대의 토착세력으로, 고려 태조 왕건을 섬겼던 호족 · 공신.
    '강귀례': {'role': 'other'},  # 현대 - 「진주 검무」의 전승자로 지정된 예능 보유자.
    '강규찬': {'role': 'other'},  # 근대 - 일제강점기 때, 105인 사건 등과 관련된 목사.
    '강규환': {'role': 'scholar'},  # 조선/조선 후기 - 조선 후기 경종~영종대 활동한 노론-호론계 출신의 학자이자 영남안무사 종사관, 장릉참봉 등을 지낸 문신.
    '강극성': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 지평, 부교리, 교리 등을 역임한 문신.
    '강근호': {'role': 'other'},  # 근대/일제강점기 - 일제강점기, 청산리 대첩에 참전한 독립운동가.
    '강기덕': {'role': 'other'},  # 근대 - 일제강점기 때, 3·1운동의 기획과 실행에 가담한 민족대표 48인 중 한 사람으로, 학생 대표로서 서울 학생 제2차 독립만...
    '강기동': {'role': 'other foreigner'},  # 근대/대한제국기 - 대한제국기 때, 일본헌병보조원으로 위장 귀순하여 포로의병들을 석방하고 무기를 탈취해 항일의병투쟁을 전개한 의병장.
    '강기운': {'role': 'other'},  # 근대 - 일제강점기 때, 국민회에서 활동하며 독립군과 군자금 모집 및 밀정색출 작업을 전개한 독립운동가.
    '강기찬': {'role': 'other'},  # 근대 - 일제강점기 때, 제주에서 독서회를 조직하고 일인상품불매운동을 전개하는 등 항일계몽운동을 전개한 독립운동가.
    '강난형': {'role': 'other'},  # 조선 - 조선 후기에, 형조판서, 한성부판윤, 황해도관찰사 등을 역임한 문신.
    '강남중': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 김창환과 박유전의 제자로 원각사와 광무대에서 활약한 남도소리의 명창.
    '강달영': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 조선노농총동맹 중앙위원, 제2차 조선공산당 책임비서 등을 역임한 사회주의 운동가.
    '강달주': {'role': 'other'},  # 근대 - 대한제국기 때, 심남일 의진에서 후군장으로 활약하다 투옥되었으며, 출감 후 나주군의 독립운동에 은밀히 참여한 독립운동가.
    '강대성': {'role': 'other'},  # 근대 - 1890∼1954. 갱정유도(更定儒道)의 제1대 교조.
    '강대수': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 호조좌랑, 예조정랑, 병조참의 등을 역임한 문신.
    '강대적': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 병자호란 당시 청군에 대적해서 싸운 의병장.
    '강덕룡': {'role': 'other'},  # 조선 - 조선시대 때, 함창현감, 장기현감 등을 역임한 무신.
    '강도근': {'role': 'other'},  # 현대/대한민국 - 판소리의 전승자로 지정된 예능 보유자.
    '강도순절인': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 병자호란으로 강화가 함락되자 순절한 관리.
    '강도영': {'role': 'other'},  # 근대 - 개항기 때, 우리나라에서 3번째로 사제 서품을 받은 신부.
    '강동진': {'role': 'scholar foreigner'},  # 근대 - 「일본의 조선지배정책사 연구」, 「한국노동조합운동사」 등을 저술한 역사학자.
    '강두안': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 대구사범학교에서 항일비밀결사인 문예부를 조직해 기관잡지인 『학생』, 『반딧불』 등을 발간하였고,...
    '강로': {'role': 'other'},  # 근대 - 조선 후기에, 사간원대사간, 병조판서, 좌의정 등을 역임한 문신.
    '강린': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 교리, 부수찬, 함경도어사 등을 역임한 문신.
    '강매': {'role': 'scholar'},  # 근대/일제강점기 - 일제강점기 때, 『조선문법제요』, 『잘 뽑은 조선말과 글의 본』 등을 저술한 국어학자.
    '강맹경': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 예문관제학, 의정부우참찬, 좌찬성 등을 역임한 문신.
    '강명규': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 중국 만주에서 활약한 독립운동가.
    '강명길': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 내의원수의, 양주목사, 지중추부사 등을 역임한 의관.
    '강명준': {'role': 'other'},  # 근대 - 개항기 때, 임오군란 당시의 군인.
    '강무경': {'role': 'other'},  # 근대/개항기 - 대한제국기 때, 심남일 의진에서 선봉장으로 활약한 의병.
    '강문규': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 희릉참봉, 의영고봉사 등을 역임한 문신.
    '강문봉': {'role': 'other'},  # 현대 - 김창룡 육군 특무부대장 암살사건 당시의 군인 · 외교관.
    '강문수': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 조선공산당 만주부 조직 책임, 대한민국 특무부대 장교 등을 역임한 사회주의 운동가.
    '강문진': {'role': 'other'},  # 근대 - 일제강점기 때, 대동단에 입단하여 군자금을 모금하여 임시정부에 조달하는 활동을 전개한 독립운동가.
    '강문형': {'role': 'other'},  # 근대 - 조선 후기에, 예방승지, 협판교섭통상사무, 이조참판 등을 역임한 문신.
    '강문회': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 예문관 검열을 역임하고, 성균관에서 후학을 지도한 문신.
    '강민저': {'role': 'scholar'},  # 조선 - 조선 후기에, 희빈장씨를 옹호하던 남구만을 규탄한 죄로 유배되었다가 벼슬을 단념하였고, 이후 후학 양성에 힘쓰며 「상남상」...
    '강민첨': {'role': 'other'},  # 고려/고려 전기 - 고려 전기에, 안찰사, 내사사인, 지중추사 병부상서 등을 역임하였으며, 동여진과 거란의 친입을 격퇴한 장수 · 공신.
    '강박': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 부교리, 수찬, 필선 등을 역임한 문신.
    '강백': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 승문원박사, 정산현감, 한성부우윤 등을 역임한 문신.
    '강백규': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 대한국민회, 간도청년회, 대한청년단 등에서 활동하며 항일투쟁을 전개한 독립운동가.
    '강백년': {'role': 'scholar'},  # 조선/조선 후기 - 조선 후기 관각문학을 대표하는 문한(文翰)이자 청렴한 관직 생활로 청백리에 녹선된 문신.
    '강백진': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 함안군수, 사헌부장령, 사간원사간 등을 역임한 문신.
    '강백천': {'role': 'other'},  # 근대 - 「대금 산조」를 전승한 예능 보유자.
    '강변칠우': {'role': 'novelist'},  # 조선/조선 후기 - 조선 후기에, 북한강변에서 시와 술로 세월을 보낸 박응서 등 일곱 명의 문인들.
    '강병두': {'role': 'scholar'},  # 현대/대한민국 - 국가재건최고회의 헌법심의위원회 전문위원, 행정계획조사위원회 위원 등으로 활동하였으며, 『신헌법』, 『헌법강의』, ...
    '강병일': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 중국 만주에서 항일투쟁을 한 독립운동가.
    '강병주': {'role': 'scholar'},  # 근대 - 일제강점기 때, 『큰 사전』 편찬 전문위원, 내명학교 교장, 경안중학교 교장 등을 역임한 목사 · 한글학자.
    '강보': {'role': 'other'},  # 고려/고려 후기 - 고려 후기 판서운관사를 역임한 과학기술자.
    '강복성': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 평산부사, 전주부윤, 청송부사 등을 역임한 문신.
    '강복중': {'role': 'scholar'},  # 조선/조선 후기 - 조선 후기에, 「수월정청흥가」, 「위군위친통곡가」, 「분산회복사은가」 등의 작품을 남긴 문신.
    '강봉수': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 평창군수, 참판 등을 역임한 문신.
    '강봉우': {'role': 'other'},  # 근대 - 일제강점기 때, 105인사건으로 옥고를 치렀으며, 간도에서 3·1운동을 주도한 독립운동가.
    '강사덕': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 우군도총제, 전라도병마도절제사, 판승녕부사 등을 역임한 무신.
    '강사상': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 병조판서, 형조판서, 이조판서 등을 역임한 문신.
    '강사필': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 병조참의, 사헌부대사헌, 승문원부제조 등을 역임한 문신.
    '강삼': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 동부승지, 우부승지, 우승지 등을 역임한 문신.
    '강상국': {'role': 'scholar'},  # 조선 - 조선 후기에, 『능호집』 등을 저술한 학자.
    '강상모': {'role': 'other'},  # 근대 - 일제강점기 때, 홍범도가 이끄는 대한독립군에서 활동한 독립운동가.
    '강상인': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 병조참판을 역임한 무신.
    '강상주': {'role': 'other'},  # 근대 - 일제강점기 때, 제5군부설 체카 특별부 전권위원, 연해주 소비에트 집행위원회 감시관 등을 역임한 사회주의 운동가.
    '강상호': {'role': 'other'},  # 현대/대한민국 - 북한에서, 내무성 부상, 인민군 총정치국장 등을 역임하다가 김일성 독재를 규탄하며 소련으로 망명해 북한 체제 비판...
    '강서': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 수원부사, 우승지, 좌승지 등을 역임한 문신.
    '강서룡': {'role': 'other'},  # 현대/대한민국 - 내무부 치안국장, 국방부차관, 교통부장관 등을 역임한 법조인 · 관료.
    '강석': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 동지밀직사사, 교주강릉도도순문 겸 병마사, 삼재 등을 역임한 무신.
    '강석구': {'role': 'other'},  # 조선 - 조선 후기에, 헌납, 사간, 집의 등을 역임한 문신.
    '강석기': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 대사간, 대사성, 도승지, 이조판서 등을 역임한 문신.
    '강석덕': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 우부승지, 호조참판, 대사헌 등을 역임한 문신.
    '강석봉': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 조선청년총동맹 중앙집행위원, 건국준비위원회 전남지부 부위원장 등을 역임한 사회주의 운동가.
    '강석빈': {'role': 'other'},  # 조선 - 조선 후기에, 충청도암행어사, 이조좌랑, 경기도수군절도사 등을 역임한 문신.
    '강석숭': {'role': 'other'},  # 현대/대한민국 - 북한에서, 당 중앙위원, 최고인민회의 대의원, 당 역사연구소장 등을 역임한 관료.
    '강석연': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 「모란등기」 · 「모반의 혈」 · 「대장안」 등에 출연한 배우. 가수.
    '강석창': {'role': 'other'},  # 조선 - 조선 후기에, 고산찰방, 종성부사 등을 역임한 문신.
    '강석호': {'role': 'other'},  # 근대/개항기 - 조선 후기~대한제국기에 국왕 고종의 총애를 받으며 정치에 관여하였던 내시.
    '강선': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 강원도관찰사, 형조참판, 도승지 등을 역임한 문신.
    '강선여': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 공조좌랑, 예조좌랑, 병조좌랑 등을 역임한 문신.
    '강선힐': {'role': 'other'},  # 고대/남북국 - 남북국시대 때, 태봉국의 왕건이 나주지방으로의 출정을 도운 장수.
    '강섬': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 함경도어사, 사간원헌납, 도승지 등을 역임한 문신.
    '강성산': {'role': 'other'},  # 현대/대한민국 - 북한에서, 노동당 중앙위원, 최고인민회의 대의원, 정무원 총리 등을 역임한 관료.
    '강성삼': {'role': 'other'},  # 근대 - 개항기 때, 우리나라에서 첫 번째로 사제서품을 받은 신부.
    '강성좌': {'role': 'other'},  # 조선 - 조선 후기에, 오위도총부도사, 훈련원정, 영변부사 등을 역임한 무신.
    '강성태': {'role': 'other'},  # 현대 - 대한테니스협회 회장, 대한손해보험협회 이사장, 상공부장관, 민의원 의원 등을 역임한 실업가 · 정치인.
    '강세': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 신라의 이벌찬 등을 역임한 관리.
    '강세구': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 호조참의, 충청도관찰사, 대사간 등을 역임한 문신.
    '강세규': {'role': 'other'},  # 조선 - 조선 후기에, 지평, 정언, 기주관 등을 역임한 문신.
    '강세윤': {'role': 'other'},  # 조선 - 조선 후기에, 승정원주서, 이천부사 등을 역임한 문신.
    '강세황': {'role': 'critic'},  # 조선/조선 후기 - 조선후기 시, 서, 화 삼절(三絶)로 일컬어진 화가. 문관, 평론가.
    '강소천': {'role': 'childrenauthor'},  # 근대/일제강점기 - 일제강점기 때, 「길가에 얼음판」, 「얼굴 모르는 동무에게」, 「호박꽃과 반딧불」 등을 저술한 아동문학가.
    '강소춘': {'role': 'other'},  # 근대 - 조선 후기에, 원각사 및 협률사의 창극 공연에 참가한 판소리의 명창.
    '강수': {'role': 'other'},  # 조선 - 조선 후기에, 예조좌랑, 장악원첨정, 장령 등을 역임한 문신.
    '강수곤': {'role': 'other'},  # 조선 - 조선 중기에, 공조좌랑, 고창현감, 괴산군수 등을 역임한 문신.
    '강수남': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 예조좌랑, 병조정랑, 이조참판 등을 역임한 문신.
    '강수형': {'role': 'other'},  # 고려 - 고려 후기에, 북경동지, 동경총관, 찬성사 등을 역임한 역관.
    '강숙경': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 밀양도호부사, 강원도사, 함안군수 등을 역임한 문신.
    '강숙돌': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 의금부도사, 사헌부지평, 사간원사간 등을 역임한 문신.
    '강순': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 대한민국임시의정원 의원 등을 역임하였으며, 해방 이후 북한에서, 최고인민회의 대의원 등을 역임한...
    '강순룡': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 지밀직사, 찬성사, 재령백 등을 역임한 무신.
    '강순의': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 어사중승, 섭대장군, 초토처치병마우도사 등을 역임한 무신.
    '강순필': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 때, 대한광복회를 결성하여 활동하다가 일본경찰에게 발각되어 처형당한 독립운동가.
    '강승우': {'role': 'other'},  # 현대 - 한국전쟁 때, 강원도 철원의 백마고지 전투에 참전한 군인.
    '강시': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 삼사좌윤, 군기판관, 강릉도안찰사 등을 역임한 문신.
    '강시경': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 장령, 지평, 정언 등을 역임한 문신.
    '강시만': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 경상남도 합천군 독립만세시위로 체포된 구금자의 석방을 위해 결사대를 조직하여 시위를 전개하다가 ...
    '강시영': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 형조판서, 대사헌, 예조판서 등을 역임한 문신.
    '강시원': {'role': 'other'},  # 근대 - 개항기 때, 차도주를 역임한 천도교인.
    '강시환': {'role': 'other'},  # 조선 - 조선 후기에, 양양부사, 장령, 헌납 등을 역임한 문신.
    '강신': {'role': 'other'},  # 조선 - 조선 중기에, 강원도관찰사, 경기도관찰사, 좌참찬 등을 역임한 문신.
    '강신명': {'role': 'other'},  # 현대/대한민국 - 해방 이후, 숭실대학교 이사장, 대한기독교교육협회(大韓基督敎敎育協會) 회장, 서울장로회신학교 교장 등을 역임(歷任...
    '강신재': {'role': 'novelist'},  # 현대/대한민국 - 해방 이후 「얼굴」 · 「젊은 느티나무」 · 「표선생 수난기」 등을 저술한 소설가.
    '강신호': {'role': 'scholar'},  # 근대 - 일제강점기 「의자」, 「작품제9」, 「진주풍경」 등을 그린 화가. 서양화가.
    '강심': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 때, 신라의 통일전쟁에 참여한 이동혜 지방의 촌주.
    '강양공': {'role': 'other'},  # 고려 - 고려의 제25대 왕, 충렬왕의 첫째 왕자.
    '강언룡': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 유곡도찰방, 좌승지 등을 역임한 무신.
    '강여재': {'role': 'other'},  # 조선 - 조선 후기에, 장령, 세자시강원 보덕 등을 역임한 문신.
    '강여호': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 사간원정언, 사헌부장령, 종성부사 등을 역임한 문신.
    '강연': {'role': 'other'},  # 조선 - 조선 중기에, 인천부사, 첨지중추부사, 한성부판윤 등을 역임한 문신.
    '강영': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 강계만호, 조전원수 등을 역임한 무신 · 공신.
    '강영각': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 하와이로 노동 이민하여 임시정부후원회 이사부원, 재미한족연합위원회 의사부 국방위원 등을 역임한 ...
    '강영선': {'role': 'scholar'},  # 현대/대한민국 - 한국자연보존협회 회장, 한국생물과학협회 회장 등을 역임한 유전학자.
    '강영소': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 때, 미국으로 노동 이민하여 흥사단을 조직하고, 대한인국민회 북미지방 총회장, 독립신문사 하와이 지국...
    '강영준': {'role': 'other'},  # 고려/고려 전기 - 고려 전기에, 내시 위위주부, 좌상시 등을 역임한 문신.
    '강영지': {'role': 'scholar'},  # 조선 - 조선 후기에, 『수재집』, 「심학집략」 등을 저술한 학자.
    '강옥경': {'role': 'other'},  # 현대 - 해방 이후 「진주검무」 전승자로 지정된 기예능보유자.
    '강완숙': {'role': 'other'},  # 조선 - 조선 후기에, 신유박해 당시의 순교자.
    '강왕': {'role': 'other'},  # 발해의 제6대(재위: 795년~809년) 왕.
    '강용구': {'role': 'other'},  # 근대 - 원로원 참의, 삼일원 대덕, 대일각 전교 등을 역임한 대종교인.
    '강용환': {'role': 'other'},  # 근대 - 대한제국기 때, 이날치의 제자로 김창환 협률사에서 활동한 판소리의 명창.
    '강용흘': {'role': 'novelist'},  # 근대/일제강점기 - 일제강점기 때, 「행복한 숲」, 「동양인이 본 서양」, 「초당」 등을 저술한 소설가.
    '강우': {'role': 'scholar'},  # 근대 - 일제강점기 때, 『종리문답』, 『천산도설』, 『제천혈고사』 등을 저술한 대종교인.
    '강우규': {'role': 'other'},  # 근대/일제강점기 - 대한국민노인동맹단 라오허현 지부장으로 사이토 마코토 총독 처단 투탄 의거를 일으킨 독립운동가.
    '강우성': {'role': 'scholar'},  # 조선/조선 후기 - 조선시대 때, 부산훈도이자 『첩해신어』를 저술한 역관.
    '강우형': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 중추원의관, 장례원소경, 봉상사제조 등을 역임한 문신.
    '강욱': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 도승지, 예조참의, 강원도관찰사 등을 역임한 문신.
    '강운': {'role': 'scholar'},  # 조선/조선 후기 - 조선 후기 영남 남인 출신의 학자이자 전적, 지평, 이조좌랑 등을 역임한 문신.
    '강운경': {'role': 'other'},  # 현대/대한민국 - 서울대학교 교수, 한국듀오피아노협회 회장 등을 역임한 음악가.
    '강원': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 전의현감, 공주목사, 청주목사 등을 역임한 문신.
    '강원보': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 종부부령, 판소부시사 등을 역임한 문신.
    '강원영': {'role': 'other'},  # 근대/개항기 - 대한제국기 때, 대한의학교 교관, 육군 3등 군의관 등을 역임한 의관.
    '강원용': {'role': 'other'},  # 현대/대한민국 - 해방 이후 아시아종교인평화회의 의장, 세계종교인평화회의 공동의장 등을 역임한 목사. 교육자, 사회운동가.
    '강원형': {'role': 'other'},  # 근대 - 대한제국기 때, 십삼도유생연명소의 소수로 상소를 올린 민족운동가.
    '강위': {'role': 'poet'},  # 근대/개항기 - 개항기 때, 『경위합벽』, 『손무자주』, 『동문자모분해』 등을 저술한 시인 · 개화사상가.
    '강위빙': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 희릉참봉, 종묘서봉사, 순안현령 등을 역임한 문신.
    '강유': {'role': 'other'},  # 조선 - 조선 후기에, 황해감사, 경기수군절도사, 호조참의 등을 역임한 문신.
    '강유선': {'role': 'scholar'},  # 조선 - 조선 전기에, 『주천집』을 저술한 유생.
    '강유정': {'role': 'other'},  # 현대 - 해방 이후 여인극장 대표, 한국연극협회 이사 등을 역임한 연출가.
    '강유후': {'role': 'other'},  # 조선 - 조선 후기에, 정주목사, 강계부사, 의주부윤 등을 역임한 문신.
    '강윤': {'role': 'other'},  # 근대/일제강점기|현대 - 일제강점기 때, 태화기독교사회관을 신축한 건축가.
    '강윤국': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 대한애국청년당을 결성하여 부민관 투탄 의거를 전개한 독립운동가.
    '강윤명': {'role': 'other'},  # 고려 - 고려 충렬왕 때, 영월에서 민란을 일으킨 주모자.
    '강윤소': {'role': 'other'},  # 고려 - 고려 후기에, 원종폐립사건 당시의 관리.
    '강윤충': {'role': 'other'},  # 고려 - 고려 후기에, 찬성사, 판삼사사 등을 역임한 문신 · 공신.
    '강윤형': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 만경현령, 동부승지, 승지 등을 역임한 문신.
    '강윤희': {'role': 'other'},  # 근대/개항기 - 대한제국기 경기도 가평 출신으로, 관동창의진(關東倡義陣)과 13도창의군에서 활동한 의병장.
    '강융': {'role': 'other'},  # 고려 - 고려 후기에, 만호, 찬성사, 첨의좌정승판삼사사 등을 역임한 문신.
    '강은': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 검열, 예빈시참봉, 전적 등을 역임한 문신.
    '강응정': {'role': 'other'},  # 조선 - 조선 전기에, 김용석, 신종호 등과 향약을 만들고, 『소학』을 강론한 문신.
    '강응철': {'role': 'other'},  # 조선 - 조선 중기에, 찰방 등을 역임하였으며, 임진왜란이 발발하자 의병을 일으켜 항쟁한 의병장.
    '강응태': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 성균관전적, 사헌부지평, 순천도호부사 등을 역임한 문신.
    '강응환': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 고령진첨사, 창성부사, 동래부사 등을 역임한 무신.
    '강이문': {'role': 'critic'},  # 현대 - 해방 이후 부산여자대학교 무용과 교수, 한국춤평론가회 회장 등을 역임한 평론가. 춤평론가.
    '강이봉': {'role': 'other'},  # 근대 - 대한제국기 때, 문태수 의진에서 항일의병투쟁을 전개한 의병.
    '강이상': {'role': 'other'},  # 조선 - 조선 후기에, 정언, 지평, 양덕현감 등을 역임한 문신.
    '강이식': {'role': 'other'},  # 고대/삼국/고구려 - 삼국시대 때, 고구려 임유관전투에 참전한 장수.
    '강이오': {'role': 'scholar'},  # 조선/조선 후기 - 조선 후기에, 「강안주유도」, 「송하망폭도」 등의 작품을 그린 화가.
    '강이원': {'role': 'other'},  # 조선 - 조선 후기, 이승훈, 정약용 등과 함께 천주교리를 강습한 일에 대하여 유생들이 상소를 올려 천주교 탄압의 계기가 된 정미반...
    '강이천': {'role': 'other'},  # 조선 - 조선 후기에, 신유박해와 관련된 천주교인.
    '강익': {'role': 'scholar'},  # 조선 - 조선 전기에, 남계서원을 건립하여 정여창을 제향하였으며, 『개암집』을 저술한 학자.
    '강익록': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 독립운동 자금을 모금하고, 일제의 경찰 주재소 습격으로 무기징역을 선고받고 옥고를 치른 독립유공자.
    '강익문': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 예조좌랑, 충원현감, 제용감정 등을 역임한 문신.
    '강인': {'role': 'other'},  # 조선 - 조선 중기에, 공조좌랑, 한성부좌윤, 상주목사 등을 역임한 문신.
    '강인부': {'role': 'other'},  # 고려 - 조선 전기에, 상의중추원사를 역임한 환관.
    '강인수': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 의열단, 조선의용군, 조선민족혁명당 특파원 등으로 활동하였으며 해방 이후, 중국군 육군소장을 역...
    '강인식': {'role': 'other'},  # 조선 - 조선 후기에, 대오전악, 집사악사 등을 역임한 거문고 명인.
    '강인유': {'role': 'other'},  # 고려 - 고려 후기에, 찬성사, 계품사 등을 역임한 문신.
    '강인희': {'role': 'other'},  # 현대/대한민국 - 해방 이후 공주사범대학 가정과 교수, 명지대 가정학과 교수, 양정학원 이사 등을 역임한 교육자. 한국음식연구가.
    '강일순': {'role': 'other'},  # 근대 - 대한제국기 때, 증산사상을 개시한 종교 창시자.
    '강자평': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 승정원동부승지, 우부승지, 형조참의 등을 역임한 문신.
    '강장원': {'role': 'other'},  # 근대 - 일제강점기 때, 김창환의 제자로 국립국악원 국악사로 활동한 판소리의 명창.
    '강재구': {'role': 'other'},  # 현대/대한민국 - 수도사단 제1연대 소대장, 1군 하사관학교 수류탄 교관 등을 역임한 군인.
    '강재만': {'role': 'other'},  # 근대 - 조선 후기에, 동편제의 법통을 이은 판소리의 명창.
    '강재천': {'role': 'other'},  # 근대 - 일제강점기 때, 의병으로 활동하다가 만주로 망명하였고, 북로군정서에 가입해 항일무장투쟁을 전개한 의병 · 대종교인 · 독립...
    '강재항': {'role': 'other'},  # 조선/조선 후기 - 조선 후기, 선공감역, 한성주부, 회인현감 등을 역임한 문신.
    '강정택': {'role': 'scholar'},  # 근대/일제강점기 - 일제하의 농정학자이자 해방 후 경성대학 교수, 농림부 차관 등을 역임한 농업 정책학자.
    '강정환': {'role': 'scholar'},  # 조선 - 조선 후기에, 『전암문집』 등을 저술한 학자.
    '강제': {'role': 'other'},  # 조선 - 조선 전기에, 영덕현감, 이조정랑 등을 역임한 문신.
    '강제억': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 1919년 평안북도 창성에서 3·1운동에 참여하고, 1920년 1월 대한민국임시정부 연통제(聯通制)에...
    '강제원': {'role': 'scholar'},  # 현대/대한민국 - 『한국동식물도감』 해조류편을 저술한 생물학자.
    '강제하': {'role': 'other'},  # 근대 - 일제강점기 때, 대한민국임시정부 파견원, 대한통의부 교통위원장 등을 역임하여 만세시위 계획, 자금 및 독립군 모집과 같은 ...
    '강제희': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 평안북도 창성의 독립만세시위를 주도하였고, 대한민국임시정부 평안북도창성군 조사원을 역임하여 항일...
    '강조': {'role': 'other'},  # 고려/고려 전기 - 고려 전기, 서북면도순검사, 중대사, 이부상서 · 참지정사, 행영도통사 등을 역임한 권신.
    '강조원': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 개성 남부교회, 경기도 파주구읍교회, 개풍군 풍덕교회 등에서 목회한 목사.
    '강종': {'role': 'other'},  # 고려 - 고려의 제22대(재위: 1211~1213) 왕.
    '강종경': {'role': 'other'},  # 조선 - 조선 전기에, 예문관검열, 성균관학유 등을 역임한 문신.
    '강주': {'role': 'novelist'},  # 조선/조선 후기 - 조선 후기 문신이자 문인.
    '강주룡': {'role': 'other'},  # 일제강점기 평양 소재 평원(平元)고무공장 여공으로 1931년 동맹파업을 벌인 항일노동운동가.
    '강주진': {'role': 'scholar foreigner'},  # 현대/대한민국 - 『정치학개론』, 『근대외교사』, 『미국정당 정치연구』 등을 저술한 서지학자.
    '강주호': {'role': 'scholar'},  # 조선 - 조선 후기에, 서숙을 열어 후진 양성에 전념하였으며, 『유금강산록』, 『유태백산록』, 『유속리산록』 등을 저술한 학자.
    '강준호': {'role': 'other'},  # 현대 - 멕시코 올림픽대회 등에서 지도자로 활약한 체육인.
    '강준흠': {'role': 'novelist'},  # 조선/조선 후기 - 조선 후기 정언, 지평, 부수찬, 수안현감 등을 역임한 문신이며 문인.
    '강중경': {'role': 'other'},  # 고려 - 고려 후기에, 동지밀직사사, 서북면병마사 등을 역임한 무신 · 공신.
    '강중상': {'role': 'other'},  # 고려 - 고려 후기에, 경상도도순문진변사, 판개성부사, 경상도도순문사 등을 역임한 문신.
    '강중진': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 성균관전적, 형조좌랑, 승문원판교 등을 역임한 문신.
    '강증': {'role': 'other'},  # 고려 - 고려 전기에, 수사공 참지정사판상서형부사, 중서시랑평장사 등을 역임한 문신.
    '강진': {'role': 'other foreigner'},  # 근대 - 일제강점기 때, 러시아 및 간도 등지에서 공산주의 활동을 하다가 해방 이후 조선인민공화국에서 중앙인민위원회의 인민위원 및 ...
    '강진구': {'role': 'other'},  # 현대/대한민국 - 1973년 삼성전자에 상무를 시작으로 2000년까지 삼성그룹 전문경영인으로 활약한 기업인.
    '강진규': {'role': 'other'},  # 조선 - 조선 후기에, 성균관박사, 사헌부장령, 예조참판 등을 역임하였으며, 「영남만인소」를 지어 사학을 몰아낼 것을 주장하며 개화...
    '강진원': {'role': 'other'},  # 근대 - 대한제국기 때, 의병 부대를 편성하여 여수의 원포리전투에 참전한 의병장.
    '강진철': {'role': 'scholar'},  # 현대/대한민국 - 「고려 초기의 군인전」, 「고려 토지 제도사 연구」 등을 저술한 역사학자.
    '강진해': {'role': 'other'},  # 근대 - 일제강점기 때, 만주에서 정의부 서란총관, 한국독립군 별동대장 등으로 활동하며 항일투쟁을 전개하다가 일본군과의 전투에서 전...
    '강진휘': {'role': 'other'},  # 조선 - 조선 중기에, 사포서별제, 참봉, 선전관 등을 역임한 문신.
    '강진희': {'role': 'other'},  # 근대/개항기 | 근대/일제강점기 - 일제강점기 때, 서화미술회 교수, 서화협회 발기인 등을 역임한 서화가.
    '강징': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 지중추부사, 경주부윤, 예조참판 등을 역임한 문신.
    '강찬': {'role': 'other'},  # 근대 - 조선 후기에, 사헌부대사헌, 이조참판, 봉상사제조 등을 역임한 문신.
    '강창규': {'role': 'other'},  # 근대/일제강점기 | 현대 - 해방 이후 「건칠반」을 제작한 공예가. 건칠공예가.
    '강창제': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 독립신문사 기자, 임시정부 경무국장서리, 조선혁명당 중앙감찰위원 등을 역임하며 항일운동을 전개한...
    '강철구': {'role': 'other'},  # 근대 - 일제강점기 때, 만주에서 천영학교 교사, 북로군정서 총재비서로 활동하며 민족교육과 독립운동을 전개하다가 체포되어 순국한 독...
    '강첨': {'role': 'other'},  # 조선 - 조선 중기에, 병조좌랑, 이조참의, 경상도관찰사 등을 역임한 문신.
    '강춘삼': {'role': 'other'},  # 근대 - 대한제국기 때, 의병 부대를 편성하여 황해도 해주의 쟈라기벌판전투에 참전한 의병장.
    '강충': {'role': 'other'},  # 고대/남북국 - 삼국시대 때, 신라의 상사찬 등을 역임한 호족.
    '강치성': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 검열, 홍문관저작, 춘추관기사관 등을 역임한 문신.
    '강태국': {'role': 'other'},  # 현대/대한민국 - 해방 이후 한국성서대학교를 설립한 목사. 교육가.
    '강태동': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 대한민국임시정부의 내무차장과 비밀항일결사인 대동단의 단장 등으로 활동하며 항일운동을 전개한 독립...
    '강태성': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 수원의 독립만세시위를 주도하다가 제암리 학살사건에 의해 사망한 독립운동가.
    '강태수': {'role': 'novelist'},  # 현대 - 소련에서 카자흐공화국으로 강제이주를 당하였으며, 「나의 가르노」, 「밭 갈던 아씨에게」 등의 시, 단편, 수필을 저술한 고...
    '강태홍': {'role': 'other'},  # 근대 - 일제강점기 때, 김창조의 제자로 조선성악연구회에서 활동한 가야금 산조 명인.
    '강택진': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 조선13도총간부 교섭부장, 조선노농대회준비회 발기인 등을 역임한 사회주의 운동가.
    '강필경': {'role': 'other'},  # 조선 - 조선 후기에, 집의, 첨지중추부사, 오위장 등을 역임한 문신.
    '강필로': {'role': 'other'},  # 조선 - 조선 후기에, 회양부사, 대사간, 병조참의 등을 역임한 문신.
    '강필리': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 동래부사, 승정원동부승지, 대사간 등을 역임한 문신.
    '강필방': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 제주도에서 양재해의 반란에 가담한 호족.
    '강필성': {'role': 'other'},  # 근대 - 일제강점기 때, 풍산군수, 중추원참의, 황해도지사 등을 역임한 관료 · 친일반민족행위자.
    '강필신': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 예조좌랑, 병조좌랑, 안주현감 등을 역임한 문신.
    '강필주': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 서화미술회 교수를 역임한 화가.
    '강필효': {'role': 'scholar'},  # 조선 - 조선 후기에, 『사유록』, 『경서고이』, 『해은유고』 등을 저술한 학자.
    '강학년': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 지평, 장령, 대사헌 등을 역임한 문신.
    '강한수': {'role': 'other'},  # 근대 - 일제강점기 때, 학생비밀결사 무등회를 조직하여 항일운동을 전개하다 옥사한 독립운동가.
    '강항': {'role': 'other'},  # 조선 - 조선 중기에, 교서관박사, 공조좌랑, 형조좌랑 등을 역임한 문신.
    '강헌지': {'role': 'other'},  # 조선 - 조선 후기에, 개녕현감, 성균관전적, 춘추관기주관 등을 역임한 문신.
    '강현': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 이조참의, 예조참판, 대제학 등을 역임한 문신.
    '강형': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 지평, 장령, 대사간 등을 역임한 문신.
    '강혜원': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 때, 미국으로 노동 이민하여 신한부인회 총무, 대한여자애국단 초대 총단장, 흥사단원 등으로 활동한 독...
    '강호': {'role': 'other'},  # 근대/일제강점기|현대 - 일제강점기 때, 인쇄미술 및 상업미술, 영화감독, 연극공연의 무대장치 제작 등 3개 분야에 걸쳐 활동하였으...
    '강호문': {'role': 'other'},  # 고려/고려 후기 - 고려 후기 판전교시사를 역임한 문신.
    '강호보': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 전적, 찰방, 지중추부사 등을 역임한 문신.
    '강혼': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 우찬성, 판중추부사 등을 역임한 문신.
    '강홍대': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 비서원승, 중추원의관, 육군삼등군의장 등을 역임한 의관.
    '강홍립': {'role': 'other'},  # 조선 후기에, 한성부우윤, 순검사, 오도원수 등을 역임한 문신.
    '강홍식': {'role': 'novelist'},  # 일제강점기 「복지만리」, 「집 없는 천사」, 「망루의 결사대」 등에 출연한 배우. 시나리오작가.
    '강홍중': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 청송부사, 동지의금부사, 성천부사 등을 역임한 문신.
    '강회계': {'role': 'other'},  # 고려 - 고려 후기에, 고공좌랑, 진원군 등을 역임한 문신.
    '강회백': {'role': 'other'},  # 고려 - 고려 후기에, 밀직부사, 판밀직사사, 이조판서 등을 역임하였으며, 조선 건국 후에는 동북면도순문사를 역임한 문신 · 공신.
    '강효동': {'role': 'other foreigner'},  # 조선/조선 전기 - 조선 전기에, 중국으로부터의 채색무역문제에 관해 진언한 도화서의 화가.
    '강효문': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 예조참판, 함길도관찰사, 함길도병마절도사 등을 역임한 문신.
    '강효실': {'role': 'other'},  # 현대/대한민국 - 「죄와 벌」, 「한강은 흐른다」, 「울어도 부끄럽지 않다」 등에 출연한 배우.
    '강효원': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 병자호란 후 소현세자를 따라 심양에 간 시강원 서리.
    '강흡': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 성현찰방, 산음현감 등을 역임한 문신.
    '강흥업': {'role': 'other'},  # 조선 - 조선 후기에, 병자호란과 관련된 무신.
    '강희맹': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 예조정랑, 이조참의, 진헌부사 등을 역임한 문신.
    '강희보': {'role': 'other'},  # 조선 - 조선 중기에, 임진왜란이 발발하자 금산전투, 진주성전투 등에 참전한 의병.
    '강희안': {'role': 'other'},  # 조선 - 조선 전기에, 호조참의, 황해도관찰사 등을 역임한 문신.
    '강희언': {'role': 'scholar'},  # 조선/조선 후기 - 조선 후기에, 「인왕산도」, 「석공도」, 「사인삼경도」 등의 작품을 그린 화가.
    '강희열': {'role': 'other'},  # 조선 - 조선 중기에, 임진왜란이 발발하자 금산전투, 진주성전투 등에 참전한 의병.
    '강희중': {'role': 'other'},  # 현대/대한민국 - 한국전쟁 때, 경북 경주의 기계 · 안강전투에 참전한 군인.
    '강희헌': {'role': 'other'},  # 근대/일제강점기 - 일제강점기, 북간도에서 활동한 민족운동가.
    '개로왕': {'role': 'other'},  # 고대/삼국/백제 - 백제의 제21대(재위: 455년~475년) 왕.
    '개루왕': {'role': 'other'},  # 고대/삼국/백제 - 백제의 제4대(재위: 128년~166년) 왕.
    '개지문': {'role': 'other'},  # 고대/삼국 - 신라의 제29대 왕 태종 무열왕의 서자인 왕자.
    '개청': {'role': 'other'},  # 고대/삼국시대 - 삼국시대 때, 신라의 보현사 주지 등을 역임한 승려.
    '갱세': {'role': 'other'},  # 고대/남북국 - 남북국시대 때, 통일신라의 급찬관등을 역임한 관리.
    '거관': {'role': 'other'},  # 조선 - 조선 후기에, 설악산 신흥사로 출가하여 정업에게서 구족계를 받은 승려.
    '거도': {'role': 'other'},  # 고대/삼국 - 신라 탈해이사금 때, 우시산국과 거칠산국을 병합한 장수.
    '거득공': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 신라 태종무열왕의 서자로 총재를 역임한 관리.
    '거등왕': {'role': 'other'},  # 고대/삼국/가야 - 금관가야의 제2대(재위: 199년~253년) 왕.
    '거시지': {'role': 'other'},  # 고대/남북국 - 삼국시대 때, 신라의 현령 등을 역임한 지방관.
    '거연': {'role': 'other'},  # 근대 - 개항기 때, 남한총섭, 북한총섭 등을 역임한 승려.
    '거연당': {'role': 'scholar'},  # 조선/조선 후기 - 조선 후기에, 「관동팔경도 병풍」, 「산수도 병풍」 등의 작품을 그린 화가.
    '거열랑': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 신라의 「혜성가」와 관련된 화랑.
    '거진': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 무산성 · 감물성 · 동잠성전투에 참전한 신라의 장수.
    '거질미왕': {'role': 'other'},  # 고대/삼국/가야 - 금관가야의 제4대(재위: 291년~346년) 왕.
    '거천': {'role': 'other'},  # 고려/고려 전기 - 고려 전기에, 경주호장을 역임한 호족.
    '거칠부': {'role': 'other'},  # 삼국시대 신라의 파진찬 · 상대등 등을 역임한 장수.
    '건품': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 백제 무왕의 아막성 침공 당시의 신라 장수.
    '걸걸중상': {'role': 'other'},  # 고대/남북국/발해 - 발해의 제1대 고왕 대조영의 아버지로, 고구려 유민을 이끌고 당나라군과 싸우다 전사한 왕족.
    '걸숙': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대, 신라의 석씨 왕족.
    '걸승': {'role': 'other'},  # 고려 - 고려 후기에, 양양 낙산사의 노비.
    '검군': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 신라의 화랑 · 근랑의 낭도 출신으로 사량궁 사인 등을 역임한 관리.
    '검모잠': {'role': 'other'},  # 고대/삼국/고구려 - 삼국시대 때, 고구려 부흥 운동을 전개한 지도자.
    '견권': {'role': 'other'},  # 고려 - 고려 전기에, 말갈과 후백제와의 전투에서 공을 세운 장수 · 공신.
    '견금': {'role': 'other'},  # 고려 - 고려 전기에, 본주의 영군장군을 역임한 호족.
    '견등': {'role': 'scholar'},  # 고대/삼국 - 삼국시대 때, 신라의 『화엄일승성불묘의』, 『대승기신론동현장』 등을 저술한 승려.
    '견성군': {'role': 'other'},  # 조선 - 조선의 제9대 왕, 성종의 서자인 왕자.
    '견우옹': {'role': 'novelist'},  # 고대/남북국 - 삼국시대 때, 신라의 「헌화가」를 지은 작가.
    '견훤': {'role': 'other'},  # 고대/남북국 - 남북국시대 때, 후백제를 건국한 시조.
    '결응': {'role': 'other'},  # 고려 - 고려 전기에, 승통, 왕사, 국사 등을 역임한 승려.
    '겸용': {'role': 'other'},  # 고대/남북국 - 삼국시대 때, 신라의 태수 등을 역임한 관리.
    '겸익': {'role': 'other'},  # 고대/삼국/백제 - 백제시대, 인도에 유학을 다녀온 승려.
    '겸지왕': {'role': 'other'},  # 고대/삼국/가야 - 금관가야의 제9대(재위: 492년~521년) 왕.
    '경': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 고구려 평양성 내 낙랑동사 주지 등을 역임한 승려.
    '경강대왕': {'role': 'other'},  # 고려/고려 전기 - 고려의 제1대 왕, 태조 왕건의 조부인 왕족.
    '경구': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 내의원수의 · 지중추부사 등을 역임한 의관.
    '경녕군': {'role': 'other'},  # 조선/조선 전기 - 조선의 제3대 왕, 태종의 서자인 왕자.
    '경대승': {'role': 'other'},  # 고려 - 고려 후기에, 교위, 사심관, 장군 등을 역임한 무신.
    '경덕왕': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 제35대 왕.
    '경명군': {'role': 'other'},  # 조선 - 조선의 제9대 왕, 성종의 서자인 왕자.
    '경명왕': {'role': 'other'},  # 고대/남북국 - 통일신라의 제54대(재위: 917년~924년) 왕.
    '경목현비': {'role': 'other'},  # 고려 - 고려 전기, 제9대 왕 덕종의 왕비.
    '경문왕': {'role': 'other'},  # 고대/남북국/통일신라 - 통일신라의 제48대(재위: 861년~875년) 왕.
    '경보': {'role': 'other'},  # 고려 - 후백제의 견훤과 고려 초 국왕들의 공경을 받았던 승려.
    '경복흥': {'role': 'other'},  # 고려 - 고려 후기에, 수시중, 수성도통사, 청원부원군 등을 역임한 문신.
    '경봉': {'role': 'other'},  # 현대/대한민국 - 일제강점기 통도사 불교전문강원 원장, 통도사 주지 등을 역임한 승려.
    '경빈 박씨': {'role': 'other'},  # 조선/조선 전기 - 조선 전기 제11대 국왕 중종의 후궁.
    '경사만': {'role': 'other'},  # 고려/고려 후기 - 고려 후기 우대언(右代言)을 역임한 충숙왕 측근 문신.
    '경산': {'role': 'other'},  # 근대 - 일제강점기 때, 동래에서 범어사 주지, 임시정부 고문 등을 역임한 승려.
    '경선': {'role': 'other'},  # 현대/대한민국 - 수덕사 주지를 역임한 승려.
    '경선행': {'role': 'scholar'},  # 조선 - 조선 후기에, 『묵사집』 등을 저술한 수학자.
    '경섬': {'role': 'other'},  # 조선 - 조선 중기에, 장례원행판결사, 부제학, 호조참판 등을 역임한 문신.
    '경성왕후': {'role': 'other'},  # 고려 - 고려의 제9대 왕, 덕종의 왕비.
    '경세인': {'role': 'scholar'},  # 조선/조선 전기 - 조선 전기에, 『경재유고』, 『경연강독록』 등을 저술한 문신.
    '경세창': {'role': 'other'},  # 조선 - 조선 전기에, 도승지, 황해도관찰사, 호조참판 등을 역임한 문신.
    '경순': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 통도사, 송광사, 해인사 등에서 선을 지도한 승려.
    '경순공주': {'role': 'other'},  # 조선/조선 전기 - 조선의 제1대 왕, 태조의 셋째 공주.
    '경순왕': {'role': 'other'},  # 통일신라의 제56대(재위: 927년~935년) 왕.
    '경식': {'role': 'other'},  # 근대 - 개항기 때, 해인사 완허의 제자로 평신에게 선교를 배운 승려.
    '경신': {'role': 'other'},  # 조선 - 조선후기 송광사(松廣寺)의 내원선원에서 선교를 지도한 승려.
    '경신공주': {'role': 'other'},  # 조선/조선 전기 - 조선전기 제1대 태조의 첫째 딸인 공주.
    '경애왕': {'role': 'other'},  # 고대/남북국 - 통일신라의 제55대(재위: 924년~927년) 왕.
    '경언': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 가지산 보림사 당우를 신축한 건축가.
    '경연': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 사재감주부, 이산현감 등을 역임한 문신.
    '경열': {'role': 'other'},  # 조선 - 조선시대 때, 태능으로부터 선법을 계승한 승려.
    '경욱': {'role': 'other'},  # 현대/대한민국 - 일제강점기 통도사(通度寺) 혜봉의 제자로 정혜사 만공의 법맥을 계승한 승려.
    '경운': {'role': 'other'},  # 근대 - 일제강점기 때, 조선불교선교양종교무원 교정을 역임한 승려.
    '경원공': {'role': 'other'},  # 고려 - 고려의 제21대 왕, 희종의 셋째 왕자.
    '경유': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 때, 태조의 왕사를 역임한 승려.
    '경유공': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 경상도병마절도사, 첨지중추부사 등을 역임한 무신.
    '경응순': {'role': 'other'},  # 조선 - 조선 중기에, 왜학통사를 역임하였으며, 임진왜란이 발발하자 왜장 고니시에게 포로로 잡혀 결국 피살된 역관.
    '경의': {'role': 'other'},  # 고려 - 고려 후기에, 밀직부사, 계림원수 등을 역임하였으며, 위화도회군 이후 이성계의 집권과정에서 일시 소외되었다가, 태조 즉위 ...
    '경조': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 삼중대사를 역임한 승려.
    '경종': {'role': 'other'},  # 조선/조선 후기 - 조선 제20대 왕.
    '경주': {'role': 'scholar'},  # 근대 - 일제강점기 때, 명정학교 교장, 중앙불교전문학교 교장서리 등을 역임한 승려.
    '경준': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 좌부승지, 첨지중추부사 등을 역임한 문신.
    '경질': {'role': 'other'},  # 고대/남북국 - 남북국시대 때, 통일신라의 봉림산파 2대조 심희의 문하생인 승려.
    '경찬': {'role': 'other'},  # 조선 - 조선 후기에, 용흥사 주지, 용흥사 수호총섭 등을 역임한 승려.
    '경창군': {'role': 'other'},  # 조선/조선 후기 - 조선 제14대 임금 선조의 서(庶) 9남.
    '경창궁주': {'role': 'other'},  # 고려 - 고려의 제24대 왕, 원종의 왕비.
    '경최': {'role': 'other'},  # 조선 - 조선 후기에, 도승지, 판결사 등을 역임한 문신.
    '경한': {'role': 'other'},  # 고려 - 고려후기 신광사 주지, 흥성사 주지, 공부선 시관 등을 역임한 승려.
    '경헌': {'role': 'scholar'},  # 조선 - 조선시대 때, 『제월당집』을 저술한 승려.
    '경호': {'role': 'other'},  # 근대 - 개항기 때, 벽송사 · 동학사 등에서 불교 경전을 깊이 연구한 승려.
    '경혼': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 홍문관부제학, 충청도관찰사, 좌부승지 등을 역임한 문신.
    '경화': {'role': 'other'},  # 근대 - 대한제국기 때, 부안 내소사에 선원을 개설하여 후학을 양성한 승려.
    '경화공주': {'role': 'other'},  # 고려 - 고려, 제27대 충숙왕의 왕비.
    '경화궁부인': {'role': 'other'},  # 고려 - 고려의 제4대 왕, 광종의 왕비.
    '경화왕후': {'role': 'other'},  # 고려/고려 전기 - 고려의 제16대 왕, 예종의 왕비.
    '경흥': {'role': 'scholar'},  # 고대/남북국/통일신라 - 남북국시대 통일신라의 『삼미륵경소』 · 『금광명경최승왕경약찬』 등을 저술한 승려.
    '계강': {'role': 'other'},  # 고대/남북국 - 남북국시대 때, 통일신라의 아찬으로 시중, 상대등 등을 역임한 관리.
    '계고': {'role': 'other'},  # 고대/삼국 - 삼국시대 신라의 제24대 진흥왕 때의 가야국의 음악가 우륵에게 가야금을 배운 신라인.
    '계광순': {'role': 'other foreigner'},  # 현대/대한민국 - 일제강점기 때, 일본 척무성 사무관 등을 역임하였으며, 해방 이후 제 4·5대 민의원 등을 역임한 정치인 · 친일...
    '계국대장공주': {'role': 'other'},  # 고려/고려 후기 - 고려, 제26대 충선왕의 왕비.
    '계덕해': {'role': 'other'},  # 조선 - 조선 후기에, 성균관전적, 예조좌랑 등을 역임한 문신.
    '계백': {'role': 'other'},  # 고대/삼국/백제 - 삼국시대 때, 황산벌전투에 참전한 백제의 장수.
    '계병호': {'role': 'other'},  # 현대/대한민국 - 일제강점기 선천YMCA 총무, 중앙YMCA 간사 및 이사 등을 역임한 사회운동가.
    '계봉우': {'role': 'scholar'},  # 근대/일제강점기 - 일제강점기 때, 임시의정원, 고려공산당에서 활동하며 국외 항일운동을 전개한 역사학자 · 독립운동가.
    '계선': {'role': 'scholar'},  # 조선 - 조선 후기에, 대흥사 주지로 『양악문집』을 저술한 승려.
    '계수': {'role': 'other'},  # 고대/삼국 - 고구려의 제8대 왕, 신대왕의 5번째 왕자.
    '계아태후': {'role': 'other'},  # 고대/남북국 - 신라의 제56대 왕, 경순왕의 어머니로, 경순왕 즉위 후에 왕태후로 추존된 왕족.
    '계양군': {'role': 'other'},  # 조선 - 조선의 제4대 왕, 세종의 서자인 왕자.
    '계오': {'role': 'scholar'},  # 조선 - 조선 후기에, 『가산집』 등을 저술한 승려.
    '계오부인': {'role': 'other'},  # 고대/남북국 - 신라의 제38대 왕, 원성왕의 어머니로, 원성왕 즉위 후에 소문태후로 추봉된 왕족.
    '계왕': {'role': 'other'},  # 고대/삼국/백제 - 백제의 제12대(재위: 344년~346년) 왕.
    '계용묵': {'role': 'novelist'},  # 근대 - 일제강점기 때, 『병풍에 그린 닭이』, 『백치 아다다』 등을 저술한 소설가.
    '계원': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 때, 이찬 관등에 임명된 신라의 관리.
    '계유명': {'role': 'other'},  # 조선 - 조선 후기에, 효행으로 선교랑 사포서별제를 제수받은 효자.
    '계응': {'role': 'other'},  # 고려/고려 전기 - 고려 전기에, 대각국사 의천의 화엄종을 계승한 승려.
    '계응태': {'role': 'other'},  # 현대/대한민국 - 북한에서, 당 중앙위원회 위원, 부총리 겸 무역부장, 당 중앙위원회 공안담당 비서 등을 역임한 관료.
    '계정': {'role': 'other'},  # 근대 - 조선 후기에, 보제, 월화 등 5대 강사로부터 경전을 배운 승려.
    '계정식': {'role': 'scholar'},  # 일제강점기 때, 이화여자전문학교 음악과 과장, 조선음악회 이사 등을 역임한 지휘자 · 친일반민족행위자.
    '계지문': {'role': 'other'},  # 조선 - 조선 후기에, 정묘호란이 발발하자 아들과 함께 의병을 모집하여 항쟁한 의병장.
    '계홍': {'role': 'other'},  # 고대/남북국/통일신라 - 남북국시대 때, 통일신라의 아찬, 진두 등을 역임한 관리.
    '계화': {'role': 'other'},  # 근대 - 일제강점기 때, 만주에서 대한군정서를 조직하여 군자금 모금활동을 전개한 독립운동가.
    '계화부인': {'role': 'other'},  # 고대/남북국/통일신라 - 신라의 제39대 왕, 소성왕의 왕비.
    '계훈제': {'role': 'other'},  # 현대 - 민족수호협의회 운영위원, 민주헌법쟁취 국민운동본부 상임공동대표 등을 역임한 사회운동가.
    '고경리': {'role': 'other'},  # 조선 - 조선 중기에, 임진왜란 당시 선조를 호종하지 않았다는 이유로 곤경에 빠진 정철과 성혼을 두둔하는 상소에서 이언적을 제외하였...
    '고경명': {'role': 'other'},  # 조선 - 조선 중기에, 임진왜란이 발발하자 전라좌도 의병대장에 추대되었으며, 금산전투를 이끌다 전사한 문신 · 의병장.
    '고경조': {'role': 'other'},  # 조선 - 조선 전기에, 해미현감, 임천군수, 광주목사 등을 역임한 문신.
    '고경허': {'role': 'other'},  # 조선 - 조선 전기에, 승지, 전주부윤 등을 역임한 문신.
    '고공의': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 고구려 멸망 후, 유민 집단을 이끈 지도자.
    '고광만': {'role': 'other'},  # 현대 - 해방 이후 문교부차관, 문교부장관 등을 역임한 관료. 교육자.
    '고광수': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 고려공산청년회 책임비서를 지낸 사회주의운동가, 독립운동가.
    '고광순': {'role': 'other'},  # 근대 - 개항기 때, 을미사변이 일어나자 기우만과 함께 의병을 모집하여 좌도의병대장으로 활약한 의병장.
    '고광채': {'role': 'other'},  # 근대 - 개항기 때, 을미사변이 일어나자 고광순 의진에서 참모 겸 우익장으로 활약한 의병장.
    '고광훈': {'role': 'other'},  # 근대 - 대한제국기 때, 형 고광순 의진에서 참모부장으로 활약한 의병.
    '고구': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 고구려 장수왕의 측근으로 활동한 장수.
    '고국양왕': {'role': 'other'},  # 고대/삼국/고구려 - 고구려의 제18대(재위: 384년~391년) 왕.
    '고국원왕': {'role': 'other'},  # 고대/삼국/고구려 - 삼국시대 고구려 제16대 왕.
    '고국천왕': {'role': 'other'},  # 고대/삼국/고구려 - 고구려의 제9대(재위: 179년~197년) 왕.
    '고기승': {'role': 'other'},  # 조선 - 조선 후기에, 사간원헌납, 성균관전적 등을 역임한 문신.
    '고기준': {'role': 'other'},  # 현대/대한민국 - 해방 이후 북한의 조선기독교도연맹 서기장을 역임한 목사.
    '고길덕': {'role': 'other'},  # 고대/남북국 - 남북국시대 때, 발해의 대부승으로서 고려에 파견된 사신.
    '고노자': {'role': 'other'},  # 고대/삼국/고구려 - 삼국시대 고구려 신성태수를 지낸 관리.
    '고달': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 백제의 행건위장군 광양태수 겸 장사로서 남제에 파견된 사신.
    '고대선': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 강원도 양양의 독립만세시위에 참여했다가 순국한 독립운동가.
    '고대수': {'role': 'other'},  # 근대/개항기 - 개항기 때, 갑신정변 당시의 궁녀.
    '고덕린': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 평안남도 대동군 금제면 원장리와 강서군 반석면 상사리 사천시장 일대의 독립만세시위에 참여했다가 ...
    '고덕무': {'role': 'other'},  # 고대/삼국/고구려 - 고구려 제28대 보장왕의 아들로, 요동지역의 고구려 유민을 통치한 왕자.
    '고두환': {'role': 'other'},  # 근대 - 일제강점기 때, 대한독립단에 가입하였고, 구월산대를 조직하여 군자금 모금활동 및 친일파 처단 활동을 전개한 독립운동가.
    '고득뢰': {'role': 'other'},  # 조선 - 조선 중기에, 임진왜란이 발발하자 의병장 최경회 휘하의 부장이 되었으며, 진주성전투에 참전한 무신.
    '고득종': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 중추원부사, 동지중추원사, 한성부판윤 등을 역임한 문신.
    '고량': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 고구려 위두대형, 책성도독, 대상 등을 역임한 귀족.
    '고려복신': {'role': 'other foreigner'},  # 고대/삼국 - 삼국시대 고구려 멸망 후 일본에서 여러 관직을 역임한 유민. 일본관리.
    '고련': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 당나라에서 안동도호 등을 역임한 장수.
    '고로': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 고구려와 말갈 연합의 백제 한성 침공에 가담했던 고구려의 장수.
    '고맹영': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 사헌부지평, 옥천군수, 호조참의 등을 역임한 문신.
    '고명달': {'role': 'other'},  # 현대/대한민국 - 해방 이후 「양주별산대놀이」의 전승자로 지정된 예능보유자.
    '고명자': {'role': 'other'},  # 근대/일제강점기 - 해방 이후 조선부녀총동맹 총무부위원, 근로인민당 중앙위원으로 활동한 사회주의운동가. 독립운동가.
    '고모한': {'role': 'other'},  # 고대/남북국/발해 - 고려 전기에, 요나라에서 개부의동삼사, 중대성좌상 등을 역임한 발해의 유민.
    '고무': {'role': 'other'},  # 고대/삼국 - 고구려의 제15대 왕, 미천왕의 아들인 왕자.
    '고문간': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 고구려 멸망 후 몽고고원의 돌궐로 이주한 유민.
    '고병간': {'role': 'scholar'},  # 근대/일제강점기|현대 - 세브란스의학전문학교 교수, 연세대학교 총장, 세브란스병원 원장 등을 역임한 의사.
    '고병국': {'role': 'scholar'},  # 현대 - 헌법제정 전문위원, 법전편찬위원회 위원 등을 역임한 법학자.
    '고병익': {'role': 'scholar'},  # 현대/대한민국 - 해방 이후 『완전 동양사』, 『아시아의 역사상』, 『동아교섭사의 연구』 등을 저술한 학자. 역사학자.
    '고병희': {'role': 'other foreigner'},  # 근대 - 일제강점기 때, 일본에서 흑우회에 가입해 활동하다가 귀향하여 독서회를 조직한 독립운동가.
    '고보원': {'role': 'other'},  # 고대/삼국/고구려 - 고구려의 제28대 보장왕의 손자로, 좌응양위 대장군에 임명된 왕족.
    '고보준': {'role': 'other'},  # 고려 - 고려 전기에, 이자겸 일파를 제거하려다 실패한 관리.
    '고복남': {'role': 'other'},  # 고대/삼국/고구려 - 고구려 시대 보장왕의 태자.
    '고복수': {'role': 'other'},  # 근대 - 일제강점기 때, 「타향살이」, 「짝사랑」, 「사막의 한」 등을 부른 가수.
    '고복장': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 고구려 우보 등을 역임한 관리.
    '고봉': {'role': 'other'},  # 근대 | 현대 - 해인사, 은해사 등에서 강사로 후학을 지도한 승려.
    '고봉기': {'role': 'other foreigner'},  # 현대/대한민국 - 일제강점기 때, 중국으로 건너가 항일투쟁을 벌였으며, 해방 이후 북한에서, 중앙당 기요과장, 외무성 부상 등을 역...
    '고봉례': {'role': 'other'},  # 조선 - 조선 전기에, 우군동지총제, 제주안무사 등을 역임한 무신.
    '고부천': {'role': 'other'},  # 조선 - 조선 후기에, 교서관정자, 지제교, 사헌부장령 등을 역임한 문신.
    '고비': {'role': 'other'},  # 고대/남북국/후백제|고려/고려 전기 - 후백제의 제1대 왕, 견훤의 후궁으로, 견훤의 첫째 아들 신검에 의해 금산사에 유폐되었을 때...
    '고사경': {'role': 'scholar'},  # 조선 - 조선 전기에, 동지중추부사 등을 역임하였으며, 『대명률직해』를 저술한 학자.
    '고사계': {'role': 'other'},  # 고대/삼국 - 남북국시대 때, 당나라에서 사진교장을 역임한 장수.
    '고사훈': {'role': 'other'},  # 근대 - 대한제국기 때, 김석윤 대장의 참모 및 모병책으로 활약하며 항일의병투쟁을 전개한 의병.
    '고상돈': {'role': 'other'},  # 현대 - 한국에서 최초로 에베레스트산을 등정한 산악인.
    '고상안': {'role': 'scholar'},  # 조선 - 조선 중기에, 함창현감, 풍기군수 등을 역임하였으며, 임진왜란이 발발하자 함창에서 의병 대장으로 활약하다가 벼슬을 그만두고...
    '고석': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 「정오의 우사」 · 「정원」 · 「모자」 등을 그린 화가. 유화가.
    '고석규': {'role': 'poet critic'},  # 현대/대한민국 - 「윤동주의 정신적 소묘」, 「비평가의 교양」, 「현대시의 형이상성」 등을 저술한 시인 · 평론가.
    '고석진': {'role': 'other'},  # 근대/대한제국기 - 대한제국기 때, 최익현의 태인의거에 참모로서 가담하였으며, 임병찬 의진에서 참모관으로 활약한 의병.
    '고선지': {'role': 'other'},  # 고대/삼국 - 남북국시대 때, 당나라에서 사진절도사, 안서절도사 등을 역임한 장수.
    '고설봉': {'role': 'other'},  # 현대 - 해방 이후 「여명」 · 「사랑의 가족」 등에 출연한 배우.
    '고성겸': {'role': 'scholar'},  # 조선 - 조선 후기에, 「한성악부」, 『녹리문집』 등을 저술한 학자.
    '고성후': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 감찰, 군수, 예조참의 등을 역임한 문신.
    '고세': {'role': 'other'},  # 고려 - 고려 후기에, 판밀직사사, 자의밀직사사, 도첨의참리 등을 역임한 무신.
    '고세보': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 자헌, 중추부 2품직 등을 역임한 의관.
    '고수': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 위사좌평 등을 역임한 백제의 관리.
    '고수겸': {'role': 'other'},  # 고려/고려 후기 - 고려후기 최우암살미수사건과 관련된 관리. 무신.
    '고수관': {'role': 'other'},  # 조선 - 조선 후기에, 더늠 「자진사랑가」를 지은 판소리 명창.
    '고숙수': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 당나라에서 조청대부심택령 등을 역임한 관리.
    '고순': {'role': 'other'},  # 고대/삼국/신라 - 삼국시대 때, 고구려 옹산성 침공에 가담한 신라의 장수.
    '고순흠': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 조선일보 사카이지국장, 재일거류민단 제2대 단장 등을 역임한 노동운동가.
    '고숭덕': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 당나라에서 좌표도위익부랑장 등을 역임한 무신.
    '고승': {'role': 'other'},  # 고대/삼국/고구려 - 고구려 영양왕대의 장군.
    '고승제': {'role': 'scholar'},  # 현대 - 『경제학입문』, 『한국경제론』, 『한국사회 경제사론』 등을 저술한 경제학자 · 친일반민족행위자.
    '고시복': {'role': 'other'},  # 근대 - 일제강점기 때, 한인애국단 비밀단원, 한국광복군 총사령부 전령 장교, 임시정부 내무부 총무과장 등을 역임한 군인 · 독립운동가.
    '고시언': {'role': 'poet'},  # 조선 - 조선 후기에, 『소대풍요』, 『성재집』 등을 저술한 시인.
    '고식': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 막리지 등을 역임한 고구려의 관리.
    '고안무': {'role': 'scholar foreigner'},  # 고대/삼국 - 삼국시대 때, 오경박사로서 일본에 파견된 백제의 학자.
    '고앙주': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 경상남도 창원의 삼진 만세운동에 참여했다가 순국한 독립운동가.
    '고약해': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 형조참판, 개성부유수 등을 역임한 문신.
    '고언백': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 경상좌도병마사, 경기방어사 등을 역임한 무신.
    '고여': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 이성계의 휘하 산원으로 활동하였으며, 이방원의 명으로 정몽주를 격살하고 이성계를 추대한 무신 · 공신.
    '고여림': {'role': 'other'},  # 고려 - 고려 후기에, 야별초지유, 장군 등을 역임한 무신.
    '고연무': {'role': 'other'},  # 고대/삼국/고구려 - 고구려 말기의 장군.
    '고연수': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 고구려 안시성전투에 참전한 장수.
    '고연휘': {'role': 'scholar'},  # 고려/고려 후기 - 고려 후기에, 「동경산수도」, 「하경산수도」 등의 작품을 그린 화가.
    '고열': {'role': 'other'},  # 고려/고려 전기 - 고려 전기에, 중대광, 섭병부상서, 수사공상서좌복야 등을 역임한 무신.
    '고영근': {'role': 'other'},  # 근대/개항기 - 개항기 때, 만민공동회와 독립협회에서 활동하며 정부에게 개혁을 요구하는 개혁개방운동을 전개한 관리 · 독립운동가.
    '고영기': {'role': 'other'},  # 고려/고려 전기 - 고려 전기에, 감찰어사, 중군판관, 호부원외랑 등을 역임한 무신.
    '고영문': {'role': 'other'},  # 근대 - 조선 후기에, 고종에게 「시무7조」 상소문을 올린 개화사상가.
    '고영부': {'role': 'other'},  # 고려 - 고려 전기에, 위위소경, 보문각직각, 어사중승 등을 역임한 문신.
    '고영석': {'role': 'other'},  # 근대/개항기 - 김옥균의 상노로 갑신정변 당시 통신 및 정찰 임무를 수행하였던 개화당원.
    '고영신': {'role': 'other'},  # 고려/고려 전기 - 고려 전기에, 서북면병마사, 이부상서지추밀원사, 검교사공참지정사 등을 역임한 문신.
    '고영중': {'role': 'other'},  # 고려/고려 후기 - 고려 후기 무신집권기에 활동한 문신 관료로 은퇴한 후 해동기로회를 결성하여 활동한 인물.
    '고영창': {'role': 'other'},  # 고려/고려 전기 - 고려 전기, 요나라에서 발해 광복운동을 벌인 발해의 유민.
    '고영철': {'role': 'other'},  # 근대/일제강점기 - 개항기 때, 통리아문박문국 주사를 역임한 언론인.
    '고영희': {'role': 'other'},  # 근대/개항기 | 근대/일제강점기 - 일제강점기 때, 주일 특명전권공사, 탁지부 대신 등을 역임한 관료 · 친일반민족행위자.
    '고예진': {'role': 'other'},  # 근대 - 일제강점기 때, 의병 및 독립의군부 총무국 서기관으로 활동하며 항일운동을 전개하였고, 파리장서에 서명한 의병 · 독립운동가.
    '고왕': {'role': 'other'},  # 고대/남북국/발해 - 발해의 제1대(재위: 698년~719년) 왕.
    '고욕': {'role': 'other'},  # 고대/남북국/발해 - 남북국시대 거란의 요주에서 발해부흥운동을 일으키고 스스로 대왕이라 칭한 발해의 유민.
    '고용보': {'role': 'other'},  # 고려/고려 후기 - 고려 후기 원나라 황실에서 활동한 고려 출신 환관.
    '고용지': {'role': 'other'},  # 고려 - 고려 후기에, 도지병마사, 남로착적병마사, 공부상서 등을 역임한 무신.
    '고용진': {'role': 'other'},  # 근대 - 일제강점기 때, 의병 및 독립의군부 회계총관으로 활동하며 항일운동을 전개하였고, 파리장서 서명운동에 가담한 의병 · 독립운동가.
    '고용현': {'role': 'other'},  # 고려 - 고려 후기에, 대사성, 개성윤, 전라도진변사 등을 역임한 문신.
    '고용후': {'role': 'novelist'},  # 조선/조선 후기 - 조선 후기의 문인.
    '고우루': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 고구려의 을파소에 이어 죽을 때까지 국상을 역임한 관리.
    '고우영': {'role': 'other'},  # 현대/대한민국 - 1970~1980년대 스포츠신문 지면을 통해 성인을 위한 만화를 연재한 만화가.
    '고운': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 「백액대호」를 그린 화가.
    '고원증': {'role': 'other'},  # 현대/대한민국 - 해방 이후 중앙고등군법회의 재판장, 서울지구 계엄민사부장, 법무차감 등을 역임한 군인. 관료.
    '고원훈': {'role': 'scholar'},  # 근대 - 일제강점기 때, 보성전문학교 교수, 조선체육회 초대 이사장, 중추원 참의 등을 역임한 관료 · 기업인 · 친일반민족행위자.
    '고유': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 승지, 안주목사 등을 역임한 문신.
    '고유방': {'role': 'other'},  # 고려/고려 후기 - 고려의 제19대 왕, 명종의 총애를 받았던 도화원의 화가.
    '고유섭': {'role': 'scholar'},  # 근대 - 일제강점기 때, 『조선회화집성』, 『조선탑파의 연구』, 『한국미술문화사논총』 등을 저술한 미술사학자.
    '고윤식': {'role': 'scholar'},  # 조선 - 조선 후기에, 「문심경」, 『태려문집』 등을 저술한 학자.
    '고을나': {'role': 'other'},  # 고대/초기국가 - 초기국가시대 때, 탐라국의 삼성혈 신화에 전해지는 건국 시조.
    '고응관': {'role': 'other'},  # 조선 - 조선 후기에, 예조좌랑, 사헌부장령 등을 역임한 문신.
    '고응량': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 발생한 이인좌의 난과 관련된 관리.
    '고응척': {'role': 'scholar'},  # 조선 - 조선 중기에, 함흥교수, 풍기군수, 회덕현감, 경주부윤 등을 역임하였으며, 「임인제야시」, 「탄시」, 「차기음」, 『두곡집...
    '고의화': {'role': 'other'},  # 고려 - 고려 전기에, 수사공 상서좌복야 판병부사, 위사공신 등을 역임한 무신 · 공신.
    '고이만년': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 고구려 장수왕이 감행한 백제 침공에서 공을 세운 장수.
    '고이왕': {'role': 'other'},  # 백제의 제8대(재위: 234년~286년) 왕.
    '고익': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 고구려 장사 등을 역임하며 동진에 사신으로 파견된 관리.
    '고익진': {'role': 'scholar'},  # 현대/대한민국 - 동국대학교 불교학과 교수, 한국불교전서 편찬실장 등을 역임하였으며, 『한역불교근본경전』, 『한글아함경』, 『한국의...
    '고인계': {'role': 'other'},  # 조선/조선 후기 - 조선 후기에, 형조정랑, 충청도도사, 예안현감 등을 역임한 문신.
    '고인단': {'role': 'other'},  # 고려 - 고려후기 탐라 성주, 총관행서부사 등을 역임한 인물.
    '고인덕': {'role': 'other'},  # 근대 - 일제강점기 때, 만주에서 의열단을 조직하여 항일무장투쟁을 벌이다가 체포되어 옥사한 독립운동가.
    '고인재': {'role': 'other'},  # 근대 - 일제강점기 때, 경기도 안성군 원곡면과 양성면 일대의 독립만세시위에 참여한 독립운동가.
    '고인후': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 승문원정자, 예조참의 등을 역임한 문신.
    '고임무': {'role': 'other'},  # 고대/삼국/고구려 - 삼국시대 고구려의 제28대 보장왕의 둘째 아들인 왕자.
    '고자': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 당나라에서 장무장군 등을 역임한 장수.
    '고장환': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 조선소년연맹 중앙집행위원을 역임한 소년 운동가.
    '고재욱': {'role': 'other'},  # 근대 - 한국신문연구소 이사장, 국제신문협회 한국위원장 등을 역임한 언론인.
    '고재필': {'role': 'other'},  # 현대/대한민국 - 일제강점기 때, 만주국 국무원 총무청 고등관 시보 등을 역임하였으며 해방 이후, 국방부 비서실장, 육군 대령, 국...
    '고재호': {'role': 'other'},  # 현대 - 대구고등법원장, 대법관 등을 역임한 법조인.
    '고적': {'role': 'other'},  # 고려 - 고려 후기에, 유총관을 역임한 문신.
    '고정봉': {'role': 'other'},  # 조선/조선 후기 - 조선 후기 홍문관교리, 돈녕부도정 등을 지낸 문신.
    '고정사': {'role': 'other'},  # 고대/남북국/발해 - 남북국시대 후발해의 사신으로 후당에 입조하여 관직을 받은 발해의 유민.
    '고정옥': {'role': 'scholar'},  # 근대/일제강점기 - 서울대학교 사범대학 교수를 재임하며 우리어문학회 회원으로 활동하였고, 『조선민요연구』, 『국어국문학요강』, 『국...
    '고정의': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 여당전쟁 시기 고구려의 관직인 대로 등을 역임한 관리.
    '고정훈': {'role': 'other'},  # 현대/대한민국 - 광복 이후 육군본부 정보국차장, 조선일보 논설위원 등을 역임한 정치인. 언론인.
    '고정희': {'role': 'poet'},  # 현대 - 해방 이후 『지리산의 봄』, 『저 무덤에 푸른 잔디』, 『아름다운 사람 하나』 등을 저술한 시인.
    '고제남': {'role': 'other foreigner'},  # 근대 - 대한제국기 때, 전남 장성에서 창의포고문을 살포하고 정읍에서 일본군을 습격하는 등 항일의병투쟁을 전개한 의병장.
    '고제덕': {'role': 'other foreigner'},  # 고대/남북국 - 남북국시대 때, 발해의 수령이자 일본에 사신으로 파견된 관리.
    '고제량': {'role': 'other'},  # 근대 - 대한제국기 때, 고광순 의진에서 부장으로 활동한 의병.
    '고제신': {'role': 'other foreigner'},  # 근대 - 일제강점기 때, 일본 고관 총살단을 조직하였으나 실행에 실패하고, 임시정부에 조달할 군자금 모금활동을 전개한 독립운동가.
    '고조기': {'role': 'other'},  # 고려 - 고려 전기에, 서북면병마판사, 상서좌복야, 중서시랑평장사 등을 역임한 문신.
    '고조다': {'role': 'other'},  # 고대/삼국 - 고구려의 제20대 왕, 장수왕의 아들인 왕자.
    '고종': {'role': 'other'},  # 근대/개항기|근대/대한제국기 - 조선의 제26대(재위: 1863년~1907년) 왕.
    '고종수': {'role': 'other'},  # 고려 - 고려 후기에, 왕경등처관군만호부만호, 삼주호부 등을 역임한 무신.
    '고종후': {'role': 'other'},  # 조선 - 조선 중기에, 감찰, 예조좌랑, 임피현령 등을 역임한 문신.
    '고주옥': {'role': 'other'},  # 현대/대한민국 - 남해안별신굿의 기예능보유자인 무녀.
    '고죽리': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 고구려의 안시성전투 당시, 연개소문에 의해 보내진 첩자.
    '고준택': {'role': 'other'},  # 현대/대한민국 - 일제강점기 때, 반일투쟁 혐의로 약 7년여간 복역하었으며, 해방 이후 북한에서, 최고인민회의 대의원 등을 역임한 ...
    '고지연': {'role': 'scholar'},  # 조선 - 조선 후기에, 『주암집』 등을 저술한 학자.
    '고지형': {'role': 'other'},  # 근대/일제강점기 - 일제강점기 때, 평안남도 대동군 금제면 원장리와 강서군 반석면 상사리 사천시장 일대의 독립만세시위를 주도한 기독...
    '고진': {'role': 'other'},  # 고대/남북국 - 삼국시대 때, 당나라에 귀화한 고구려의 왕족.
    '고진상': {'role': 'other'},  # 고대/남북국 - 고려 전기에, 고려로 귀화한 발해제군판관 출신의 발해 유민.
    '고진승': {'role': 'other'},  # 조선/조선 후기 | 근대/개항기 - 조선후기 도화서 화원으로 헌종의 국장도감 등에 참여한 화가.
    '고질': {'role': 'other'},  # 고대/삼국/고구려 - 고구려 말기와 멸망 이후, 고구려 유민 출신으로 당나라에서 주로 활동한 무관.
    '고찬보': {'role': 'other'},  # 근대 - 남조선신민당 중앙위원회 선전부장, 남조선노동당 중앙상무위원 등을 역임한 사회주의 운동가.
    '고찬익': {'role': 'other'},  # 근대/개항기 - 대한제국기 연동교회 초대 장로, 장로회공의회 전도위원 등으로 활동한 개신교인. 사회운동가.
    '고창일': {'role': 'other foreigner'},  # 근대/일제강점기 - 일제강점기 때, 대한국민의회 대표로서 파리강화회의에 파견되었으며, 중국 하얼빈에서 독립운동을 지속하다가 해방 이...
    '고채주': {'role': 'other'},  # 근대 - 일제강점기 때, 경상남도 통영 부도정시장의 독립만세시위를 주도한 독립운동가.
    '고천백': {'role': 'other'},  # 고려/고려 후기 - 고려 후기에, 장군, 하정사 등을 역임한 무신.
    '고추안': {'role': 'other'},  # 고대/삼국 - 고구려의 제7대 왕, 차대왕의 태자인 왕자.
    '고춘자': {'role': 'other'},  # 현대 - 백민악극단, 태평양가극단, 백조가극단 등에서 활동한 연극인.
    '고타소랑': {'role': 'other'},  # 고대/삼국/신라 - 신라의 제29대 태종 무열왕의 딸로, 백제의 대야성전투에서 살해된 왕족.
    '고태문': {'role': 'other'},  # 현대 - 한국전쟁 때, 소대장, 중대장 등을 역임한 군인.
    '고태필': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 한성부좌윤, 유수 등을 역임한 문신.
    '고판례': {'role': 'other'},  # 현대/대한민국 - 일제강점기 증산교 최초의 교파인 선도교를 창립한 종교창시자.
    '고평': {'role': 'other foreigner'},  # 근대/일제강점기 - 대한제국기 검사를 지냈으나, 일제강점기 중국으로 망명하여 광복단, 대한국민회 등에서 활동한 독립운동가.
    '고한승': {'role': 'childrenauthor'},  # 근대/일제강점기 - 일제강점기 때, 희곡 「장구한 밤」 등을 저술한 연극인 · 아동문학가.
    '고한우': {'role': 'other'},  # 고려/고려 후기 - 고려후기 대호군, 찰방사 등을 역임한 관리. 무신.
    '고현': {'role': 'other'},  # 조선 - 조선 중기에, 성주판관을 역임하던 중 임진왜란이 발발하자 도피하여 탄핵당하였으나, 의주까지 선조를 호종한 공으로 녹훈된 무...
    '고형림': {'role': 'other'},  # 근대 - 일제강점기 때, 만주에서 사진관을 경영하다가 광복군 제5지대에 입대하여 항일투쟁을 전개한 독립운동가.
    '고형산': {'role': 'other'},  # 조선/조선 전기 - 조선 전기에, 우찬성, 강원도관찰사 등을 역임한 문신.
    '고혜진': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 고구려 안시성전투에 참전한 장수.
    '고홍건': {'role': 'other'},  # 조선 - 조선시대 때, 오위도총부도총관, 지중추부사 등을 역임한 무신.
    '고홍달': {'role': 'scholar'},  # 조선 - 조선 후기에, 인목대비 폐비 논의가 이루어지자 성균관을 떠났으며, 인조반정 이후에 참봉으로 임명되었으나 곧 물러나 은거한 학자.
    '고황경': {'role': 'other'},  # 근대/개항기|근대/일제강점기 - 해방 이후 이화여자대학교 교수, 서울여자대학교 초대총장 등을 역임한 교육자. 여성운동가 · 친일반민...
    '고효충': {'role': 'other'},  # 고려 - 고려 예종 때, 국학생으로 「감이녀시」를 지어 풍자한 문신.
    '고흘': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 돌궐의 고구려 신성 침공 시, 돌궐을 격퇴했다고 전해지는 고구려의 장수.
    '고흥': {'role': 'scholar'},  # 고대/삼국 - 삼국시대 때, 박사를 역임하여 『서기』를 저술한 백제의 학자.
    '고흥문': {'role': 'other'},  # 현대/대한민국 - 제6·7·8·9·10대 국회의원을 역임한 정치인.
    '고희': {'role': 'other'},  # 조선 - 조선 중기에, 군기시판관, 유원첨사, 픙천부사 등을 역임한 무신 · 공신.
    '고희경': {'role': 'other foreigner'},  # 근대/개항기 | 근대/일제강점기 - 일제강점기 때, 주차영국공사관, 이왕직사무관 등을 역임한 관료 · 친일반민족행위자.
    '고희동': {'role': 'scholar'},  # 일제강점기 「정자관을 쓴 자화상」, 「부채를 든 자화상」, 「금강산진주담폭포」, 「탐승」 등의 작품을 그린 화가.
    '곡나진수': {'role': 'other foreigner'},  # 고대/삼국 - 삼국시대 때, 백제 부흥을 위해 항전하다 주류성이 함락되자 일본으로 망명한 백제의 유민.
    '곤우': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 백제 고목성에서 벌어진 말갈족과의 전투에 참전한 장수.
    '곤지': {'role': 'other'},  # 고대/삼국/백제 - 삼국시대 백제 제22대 문주왕(文周王)의 아우.
    '골번': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 신라의 『삼국사기』 강수전에 나오는 문장가.
})
        
        # API로부터 자동 수집된 인물 데이터
self.persons.update({
    '가군': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 고구려 장안성 축성의 책임을 맡았던 관리.
    '가귀': {'role': 'scholar'},  # 고대/삼국 - 삼국시대 때, 신라에서 『화엄경의강』, 『심원장』 등을 저술한 승려.
    '가라포고이': {'role': 'other foreigner'},  # 고대/삼국 - 삼국시대 때, 일본에 귀화한 신라의 유민.
    '가루': {'role': 'other'},  # 고대/삼국 - 삼국시대 때, 대상(大相) 등을 역임하다 고구려 멸망 후 부흥운동에 참여한 고구려의 귀족.
    '가마': {'role': 'other foreigner'},  # 고대/삼국 - 삼국시대 때, 백제에서 일본으로 파견된 사신.
    '가서일': {'role': 'other foreigner'},  # 고대/삼국 - 삼국시대 때, 일본에서 활약한 고구려 출신의 화가.
    '가실': {'role': 'other'},  # 고대/남북국 - 삼국시대 때, 신라의 사량부 출신으로 변방에서 복무한 군인.
    '가실왕': {'role': 'other'},  # 고대/삼국/가야 - 가야의 제7대(재위: 421년~451년) 왕.
}),
            '김윤식': {'role': 'critic scholar'},
            '유종호': {'role': 'critic'},
            '김종길': {'role': 'poet critic'},
            '문광훈': {'role': 'scholar'},
            '류한형': {'role': 'scholar'},
            '천춘화': {'role': 'scholar'},
            '박향우': {'role': 'scholar'},
            '신새벽': {'role': 'scholar'},
            '신동해': {'role': 'scholar'},
            '김경은': {'role': 'scholar'},
            '허선애': {'role': 'scholar'},
            '허윤': {'role': 'scholar'},
            '노민혜': {'role': 'scholar'},
            '김은하': {'role': 'scholar'},
            '남선영': {'role': 'scholar'},
            '이남숙': {'role': 'scholar'},
            '김남희': {'role': 'scholar'},
            '박상미': {'role': 'scholar'},
            '김정미': {'role': 'scholar'},

            # 한국 시인
            '최남선': {'role': 'poet'},
            '서정주': {'role': 'poet'},
            '한용운': {'role': 'poet'},
            '윤동주': {'role': 'poet'},
            '신동엽': {'role': 'poet'},
            '김수영': {'role': 'poet critic'},
            '정현종': {'role': 'poet'},
            '김소월': {'role': 'poet'},
            '이상': {'role': 'poet novelist'},
            '백석': {'role': 'poet'},
            '정지용': {'role': 'poet'},
            '서정주': {'role': 'poet'},

            # 한국 소설가
            '이광수': {'role': 'novelist'},
            '안수길': {'role': 'novelist'},
            '최인훈': {'role': 'novelist'},
            '황순원': {'role': 'novelist'},
            '김동리': {'role': 'novelist'},
            '박경리': {'role': 'novelist'},

            # 한국 수필가
            '피천득': {'role': 'essayist'},

            # 서양 철학자 (고대-근대) - 스키마에 맞춰 scholar foreigner 사용
            '소크라테스': {'role': 'scholar foreigner'},
            '플라톤': {'role': 'scholar foreigner'},
            '아리스토텔레스': {'role': 'scholar foreigner'},
            '아우구스티누스': {'role': 'scholar foreigner'},
            '토마스 아퀴나스': {'role': 'scholar foreigner'},
            '데카르트': {'role': 'scholar foreigner'},
            '스피노자': {'role': 'scholar foreigner'},
            '라이프니츠': {'role': 'scholar foreigner'},
            '로크': {'role': 'scholar foreigner'},
            '흄': {'role': 'scholar foreigner'},
            '칸트': {'role': 'scholar foreigner'},
            '헤겔': {'role': 'scholar foreigner'},
            '마르크스': {'role': 'scholar foreigner'},
            '니체': {'role': 'scholar foreigner'},
            '키에르케고르': {'role': 'scholar foreigner'},

            # 현대 철학자 (20세기)
            '하이데거': {'role': 'scholar foreigner'},
            '사르트르': {'role': 'scholar foreigner'},
            '메를로퐁티': {'role': 'scholar foreigner'},
            '카뮈': {'role': 'novelist foreigner'},
            '레비나스': {'role': 'scholar foreigner'},
            '푸코': {'role': 'scholar foreigner'},
            '데리다': {'role': 'scholar foreigner'},
            '들뢰즈': {'role': 'scholar foreigner'},
            '리쾨르': {'role': 'scholar foreigner'},
            '가다머': {'role': 'scholar foreigner'},
            '아렌트': {'role': 'scholar foreigner'},
            '한나 아렌트': {'role': 'scholar foreigner'},

            # 프랑크푸르트 학파
            '하버마스': {'role': 'scholar foreigner'},
            '위르겐 하버마스': {'role': 'scholar foreigner'},
            '호르크하이머': {'role': 'scholar foreigner'},
            '막스 호르크하이머': {'role': 'scholar foreigner'},
            '아도르노': {'role': 'scholar foreigner'},
            '테오도어 아도르노': {'role': 'scholar foreigner'},
            '마르쿠제': {'role': 'scholar foreigner'},
            '헤르베르트 마르쿠제': {'role': 'scholar foreigner'},
            '에리히 프롬': {'role': 'scholar foreigner'},
            '발터 벤야민': {'role': 'critic foreigner'},

            # 사회학자/역사가
            '베버': {'role': 'scholar foreigner'},
            '막스 베버': {'role': 'scholar foreigner'},
            '뒤르켐': {'role': 'scholar foreigner'},
            '짐멜': {'role': 'scholar foreigner'},
            '조지프 레븐슨': {'role': 'scholar foreigner'},
            '게오르게 리히트하임': {'role': 'scholar foreigner'},

            # 심리학자
            '프로이트': {'role': 'scholar foreigner'},
            '지그문트 프로이트': {'role': 'scholar foreigner'},
            '융': {'role': 'scholar foreigner'},
            '칼 융': {'role': 'scholar foreigner'},

            # 미국 철학자
            '찰스 퍼스': {'role': 'scholar foreigner'},
            '존 듀이': {'role': 'scholar foreigner'},
            '윌리엄 제임스': {'role': 'scholar foreigner'},

            # 영미 문학
            '셰익스피어': {'role': 'playwright foreigner'},
            '밀턴': {'role': 'poet foreigner'},
            '워즈워스': {'role': 'poet foreigner'},
            '콜리지': {'role': 'poet critic foreigner'},
            '바이런': {'role': 'poet foreigner'},
            '셸리': {'role': 'poet foreigner'},
            '키츠': {'role': 'poet foreigner'},
            '엘리엇': {'role': 'poet critic foreigner'},
            '예이츠': {'role': 'poet foreigner'},
            '조이스': {'role': 'novelist foreigner'},
            '울프': {'role': 'novelist foreigner'},
            '버지니아 울프': {'role': 'novelist foreigner'},
            '로렌스': {'role': 'novelist foreigner'},

            # 프랑스 문학
            '보들레르': {'role': 'poet critic foreigner'},
            '랭보': {'role': 'poet foreigner'},
            '말라르메': {'role': 'poet foreigner'},
            '발레리': {'role': 'poet foreigner'},
            '프루스트': {'role': 'novelist foreigner'},
            '지드': {'role': 'novelist foreigner'},
            '말로': {'role': 'novelist foreigner'},

            # 독일 문학
            '괴테': {'role': 'poet novelist foreigner'},
            '실러': {'role': 'poet playwright foreigner'},
            '횔덜린': {'role': 'poet foreigner'},
            '릴케': {'role': 'poet foreigner'},
            '토마스 만': {'role': 'novelist foreigner'},
            '카프카': {'role': 'novelist foreigner'},
            '브레히트': {'role': 'playwright poet foreigner'},

            # 러시아 문학
            '톨스토이': {'role': 'novelist foreigner'},
            '도스토예프스키': {'role': 'novelist foreigner'},
            '체호프': {'role': 'playwright novelist foreigner'},
            '투르게네프': {'role': 'novelist foreigner'},

            # 정치사상가
            '홉스': {'role': 'scholar foreigner'},
            '마키아벨리': {'role': 'scholar foreigner'},
            '토머스 모어': {'role': 'scholar foreigner'},
            '루소': {'role': 'scholar foreigner'},
            '몽테스키외': {'role': 'scholar foreigner'},
        }

        # 기관명 데이터베이스
        self.organizations = [
            '민음사', '창비', '문학과지성사', '열린책들', '을유문화사',
            '서울대학교', '고려대학교', '연세대학교', '이화여대',
            '국어국문학과', '철학과', '사회학과',
            '프랑크푸르트 사회 연구소', '프랑크푸르트학파'
        ]

        # 학술/비평 용어 - 대폭 확장
        self.terms = [
            # 철학 용어
            '형이상학', '존재론', '인식론', '현상학', '해석학', '변증법',
            '실존주의', '구조주의', '후기구조주의', '포스트모더니즘',
            '실증주의', '경험주의', '합리주의', '관념론', '유물론',
            '에피스테메', '패러다임', '이데올로기', '헤게모니',
            '주체성', '객관성', '간주관성', '초월성', '내재성',
            '소외', '물화', '자본주의', '역사유물론', '계급투쟁',

            # 문학 이론
            '모더니즘', '리얼리즘', '낭만주의', '고전주의', '상징주의',
            '다다이즘', '초현실주의', '표현주의', '미래주의',
            '신비평', '형식주의', '수용이론', '독자반응비평',
            '탈식민주의', '페미니즘', '마르크스주의 비평',
            '텍스트', '담론', '서사', '시학', '수사학',
            '알레고리', '아이러니', '패러디', '풍자',

            # 사회과학 용어
            '프랑크푸르트학파', '비판이론', '계몽', '이성',
            '공공영역', '의사소통', '합리성', '정당성',
            '억압', '해방', '실천', '혁명', '저항',

            # 정신분석 용어
            '무의식', '억압', '승화', '전이', '리비도', '에로스',
        ]

        # ID가 이미 사용되었는지 추적
        self.used_ids = set()

    def markup_persons(self, text):
        """인명 마크업 - 이미 태그된 영역 내부는 건드리지 않음"""
        # 긴 이름부터 처리 (중복 방지)
        sorted_persons = sorted(self.persons.keys(), key=len, reverse=True)

        for person in sorted_persons:
            if person not in text:
                continue

            info = self.persons[person]

            # 이미 <persName> 태그 안에 있으면 스킵
            if f'<persName' in text and f'>{person}<' in text:
                continue

            # 태그 생성
            attrs = []
            # ID는 한 번만 사용, 이후에는 ref로 참조
            if 'id' in info:
                person_id = info['id']
                if person_id not in self.used_ids:
                    attrs.append(f'xml:id="{person_id}"')
                    self.used_ids.add(person_id)
                else:
                    attrs.append(f'ref="#{person_id}"')

            if 'role' in info:
                attrs.append(f'role="{info["role"]}"')

            attr_str = ' ' + ' '.join(attrs) if attrs else ''
            replacement = f'<persName{attr_str}>{person}</persName>'

            # 안전하게 태그 밖의 것만 치환
            # XML 태그를 분리해서 처리
            parts = re.split(r'(<persName[^>]*>.*?</persName>)', text)
            result = []
            for part in parts:
                if part.startswith('<persName'):
                    # 이미 태그된 부분은 그대로
                    result.append(part)
                else:
                    # 태그되지 않은 부분만 단어 경계에서 치환
                    part = re.sub(r'\b' + re.escape(person) + r'\b', replacement, part)
                    result.append(part)
            text = ''.join(result)

        return text

    def markup_titles(self, text):
        """작품명/서명 마크업"""
        # 『』 괄호 안의 텍스트 (단행본)
        text = re.sub(r'『([^』]+)』', r'<title level="m">\1</title>', text)
        # 「」 괄호 안의 텍스트 (수록작품)
        text = re.sub(r'「([^」]+)」', r'<title level="a">\1</title>', text)
        # 《》 괄호 안의 텍스트 (잡지/신문)
        text = re.sub(r'《([^》]+)》', r'<title level="j">\1</title>', text)
        return text

    def markup_orgs(self, text):
        """기관명 마크업"""
        for org in sorted(self.organizations, key=len, reverse=True):
            if org in text and f'<orgName>{org}</orgName>' not in text:
                text = text.replace(org, f'<orgName>{org}</orgName>')
        return text

    def markup_terms(self, text):
        """전문용어 마크업"""
        for term in sorted(self.terms, key=len, reverse=True):
            if term in text:
                # 이미 태그 안에 있지 않은 경우만
                if f'<term>{term}</term>' not in text:
                    text = text.replace(term, f'<term>{term}</term>')
        return text

    def split_sentences(self, paragraph):
        """문단을 문장으로 분리"""
        if not paragraph.strip():
            return []

        # 마침표, 느낌표, 물음표 뒤 공백으로 문장 분리
        sentences = re.split(r'([.!?])\s+', paragraph)

        result = []
        i = 0
        while i < len(sentences):
            if i + 1 < len(sentences) and sentences[i+1] in '.!?':
                sent = sentences[i] + sentences[i+1]
                result.append(sent.strip())
                i += 2
            else:
                if sentences[i].strip():
                    result.append(sentences[i].strip())
                i += 1

        return [s for s in result if s and len(s) > 1]

    def markup_footnotes(self, text):
        """각주 마크업 - 숫자로 시작하는 각주를 <note> 태그로 감싸기"""
        # 패턴: 공백 + 숫자 + 공백 + 한글/영문으로 시작하는 긴 텍스트
        # 예: " 1 조지프 레븐슨은..."
        pattern = r'\s+(\d+)\s+([가-힣a-zA-Z][^.!?]{20,}[.!?])'

        def replace_footnote(match):
            content = match.group(2)
            return f'<note type="footnote">{content}</note>'

        text = re.sub(pattern, replace_footnote, text)
        return text

    def markup_inline_elements(self, text):
        """모든 인라인 요소 마크업"""
        text = self.markup_footnotes(text)  # 각주를 먼저 처리
        text = self.markup_titles(text)      # title을 먼저 (중첩 방지)
        text = self.markup_persons(text)
        text = self.markup_orgs(text)
        # terms는 마지막에 - 이미 태그된 영역 내부는 건드리지 않음
        text = self.markup_terms_safe(text)
        return text

    def markup_terms_safe(self, text):
        """전문용어 마크업 - 이미 태그된 영역 내부는 건드리지 않음"""
        for term in sorted(self.terms, key=len, reverse=True):
            if term not in text:
                continue

            # 이미 <term>으로 태그된 것은 건너뛰기
            if f'<term>{term}</term>' in text:
                continue

            # title, persName, orgName 등의 태그 안에 있는 것은 건드리지 않음
            # XML 요소들을 분리해서 처리
            parts = re.split(r'(<(?:title|persName|orgName|note)[^>]*>.*?</(?:title|persName|orgName|note)>)', text, flags=re.DOTALL)
            result = []
            for i, part in enumerate(parts):
                if i % 2 == 0:  # 태그 밖의 일반 텍스트
                    # 여기서만 term 치환
                    part = part.replace(term, f'<term>{term}</term>')
                else:  # 태그 안의 내용
                    # 그대로 유지
                    pass
                result.append(part)
            text = ''.join(result)
        return text

    def paragraph_to_xml(self, paragraph):
        """문단을 XML로 변환"""
        if not paragraph.strip():
            return ''

        # 인라인 마크업
        marked = self.markup_inline_elements(paragraph)

        # 문장 분리
        sentences = self.split_sentences(marked)

        if not sentences:
            return ''

        xml = '        <p>\n'
        for sent in sentences:
            # XML 특수문자 이스케이프 (이미 태그로 변환된 부분 제외)
            xml += f'          <s>{sent}</s>\n'
        xml += '        </p>\n'

        return xml

    def detect_section_type(self, line):
        """섹션 타입 감지"""
        line = line.strip()

        if '간행의 말' in line:
            return 'introduction', '간행의 말'
        elif '일러두기' in line:
            return 'notes', '일러두기'
        elif '머리말' in line or '서문' in line:
            return 'introduction', line
        elif re.match(r'^\d+부', line):
            return 'section', line
        elif '출간에 즈음하여' in line:
            return 'introduction', line

        return None, None

    def generate_xml_header(self):
        """TEI XML 헤더 생성"""
        # 헤더에서 kim-woochang ID를 사용하므로 used_ids에 추가
        self.used_ids.add('kim-woochang')

        return f'''<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0"
     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
     xsi:schemaLocation="http://www.tei-c.org/ns/1.0 ../korean-critique-schema.xsd">

  <teiHeader>
    <fileDesc>
      <titleStmt>
        <title>궁핍한 시대의 시인 - 현대 문학과 사회에 관한 에세이</title>
        <author>
          <persName xml:id="kim-woochang" role="critic scholar">김우창</persName>
        </author>
        <respStmt>
          <resp>XML 인코딩</resp>
          <name>Claude AI (자동 변환)</name>
        </respStmt>
      </titleStmt>

      <publicationStmt>
        <p>이 파일은 김우창의 궁핍한 시대의 시인을 TEI XML 형식으로 인코딩한 것입니다. (작성일: {datetime.now().strftime('%Y-%m-%d')})</p>
      </publicationStmt>

      <sourceDesc>
        <bibl>원본: 김우창, 궁핍한 시대의 시인 (김우창 전집 I), 민음사, 2015년 12월</bibl>
      </sourceDesc>
    </fileDesc>

    <encodingDesc>
      <editorialDecl>
        <p>본 텍스트는 한글 워드 파일(.docx)에서 자동 추출하여 TEI XML 형식으로 변환하였습니다. 원문의 단락 구분과 편집 형식을 최대한 보존하였으며, 인명·작품명·용어 등은 TEI 태그로 마크업하였습니다.</p>
      </editorialDecl>
      <tagsDecl>
        <namespace>
          <tagUsage gi="div" occurs="다수"/>
          <tagUsage gi="p" occurs="다수"/>
          <tagUsage gi="s" occurs="다수"/>
          <tagUsage gi="persName" occurs="다수"/>
          <tagUsage gi="title" occurs="다수"/>
        </namespace>
      </tagsDecl>
      <classDecl>
        <taxonomy xml:id="text-types">
          <category xml:id="critique">
            <catDesc>문학 비평</catDesc>
          </category>
        </taxonomy>
      </classDecl>
    </encodingDesc>

  </teiHeader>

'''

    def convert_file(self, input_file, output_file):
        """전체 파일 변환"""
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        xml_output = self.generate_xml_header()
        xml_output += '  <text>\n'
        xml_output += '    <body>\n'

        current_div = None
        current_head = None
        paragraph_buffer = []

        for i, line in enumerate(lines):
            line = line.strip()

            # 빈 줄은 문단 구분
            if not line:
                if paragraph_buffer:
                    para_text = ' '.join(paragraph_buffer)
                    xml_output += self.paragraph_to_xml(para_text)
                    paragraph_buffer = []
                continue

            # 섹션 감지
            section_type, section_title = self.detect_section_type(line)

            if section_type:
                # 이전 div 닫기
                if current_div:
                    if paragraph_buffer:
                        para_text = ' '.join(paragraph_buffer)
                        xml_output += self.paragraph_to_xml(para_text)
                        paragraph_buffer = []
                    xml_output += '      </div>\n'

                # 새 div 시작 - ID는 숫자로 시작할 수 없으므로 'div-' 접두사 추가
                div_id = 'div-' + section_title.replace(' ', '-').replace(':', '').replace('/', '-')
                # 한글이 포함된 경우 로마자로 변환하거나 단순화
                import re
                # 숫자로 시작하는 경우 처리
                if div_id[4].isdigit():
                    div_id = 'section-' + div_id[4:]

                xml_output += f'      <div type="{section_type}" xml:id="{div_id}">\n'
                xml_output += f'        <head>{section_title}</head>\n'
                current_div = section_type
                current_head = section_title
                continue

            # 일반 텍스트는 버퍼에 추가
            paragraph_buffer.append(line)

        # div가 한 번도 열리지 않았다면 기본 div 추가
        if current_div is None:
            xml_output += '      <div type="section" xml:id="section-main">\n'
            xml_output += '        <head>본문</head>\n'

        # 마지막 문단 처리
        if paragraph_buffer:
            para_text = ' '.join(paragraph_buffer)
            xml_output += self.paragraph_to_xml(para_text)

        # div 닫기
        xml_output += '      </div>\n'

        xml_output += '    </body>\n'
        xml_output += '  </text>\n'
        xml_output += '</TEI>\n'

        # 파일 저장
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(xml_output)

        print(f'변환 완료: {output_file}')
        return xml_output


if __name__ == '__main__':
    converter = TextToXMLConverter()

    input_file = r'C:\Users\bj363\OneDrive\문서\대학원 공부\xml데이터 구축\claude\data\김우창_궁핍한시대의시인_451-467쪽.txt'
    output_file = r'C:\Users\bj363\OneDrive\문서\대학원 공부\xml데이터 구축\claude\data\김우창_궁핍한시대의시인_451-467쪽.xml'

    converter.convert_file(input_file, output_file)
