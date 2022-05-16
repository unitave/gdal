.. _rfc-21:

================================================================================
RFC 21: OGR SQL 유형 캐스트 및 필드 이름 별명
================================================================================

저자: 세케레시 터마시

연락처: szekerest@gmail.com

상태: 승인

요약
----

이 RFC는 OGR SQL 'select' 목록에 있는 열 이름 및 열 유형을 변경하기 위한 지원을 제안합니다.

이런 변경의 주요 동기는 OGR_STYLE 특수 필드를 각 데이터소스로부터 다른 데이터소스로 전송할 때 더 잘 제어할 수 있도록 해주기 위한 것입니다. 예를 들면 ogr2ogr 유틸리티를 다음 명령줄처럼 사용하면 이 목적을 달성할 수 있습니다:

::

   ogr2ogr -f "ESRI Shapefile" -sql "select *, OGR_STYLE from rivers" rivers.shp rivers.tab

Shapefile 드라이버는 기본적으로 OGR_STYLE 필드를 실제 값을 담기에 충분하지 않을 수도 있는 문자 80개 길이로 절단(truncate)할 것입니다. 따라서 이 문제점을 해결하려면 'select' 목록에 다음과 같이 원하는 길이를 지정해줘야 할 수도 있습니다:

::

   ogr2ogr -f "ESRI Shapefile" -sql "select *, CAST(OGR_STYLE AS character(255)) from rivers" rivers.shp rivers.tab

대상 데이터소스에 있는 필드의 이름을 변경하는 것이 유용할 경우도 있습니다:

::

   ogr2ogr -f "ESRI Shapefile" -sql "select *, CAST(OGR_STYLE AS character(255)) AS 'STYLE' from rivers" rivers.shp rivers.tab

주요 개념
---------

이 새 기능을 지원하기 위해 현재 OGR SQL 문법을 확장할 것입니다. 이 추가 제안은 SQL92 사양을 준수하는 문법을 유지할 것입니다:

::

   SELECT <field-list> FROM <table_def>
        [LEFT JOIN <table_def> 
         ON [<table_ref>.]<key_field> = [<table_ref>.].<key_field>]*
        [WHERE <where-expr>] 
        [ORDER BY <sort specification list>]

   <field-list> ::= <column-spec> [ { , <column-spec> }... ]

   <column-spec> ::= <field-spec> [ <as clause> ]
                    | CAST ( <field-spec> AS <data type> ) [ <as clause> ]

   <field-spec> ::= [DISTINCT] <field_ref>
                    | <field_func> ( [DISTINCT] <field-ref> )
                    | Count(*)

   <as clause> ::= [ AS ] <column_name>

   <data type> ::= character [ ( field_length ) ]
                   | float [ ( field_length ) ]
                   | numeric [ ( field_length [, field_precision ] ) ]
                   | integer [ ( field_length ) ]
                   | date [ ( field_length ) ]
                   | time [ ( field_length ) ]
                   | timestamp [ ( field_length ) ]

   <field-func> ::= AVG | MAX | MIN | SUM | COUNT

   <field_ref>  ::= [<table_ref>.]field_name

   <sort specification list> ::=
                 <sort specification> [ { <comma> <sort specification> }... ]

   <sort specification> ::= <sort key> [ <ordering specification> ]

   <sort key> ::=  <field_ref>

   <ordering specification> ::= ASC | DESC

   <table_def> ::= ['<datasource name>'.]table_name [table_alias]

   <table_ref> ::= table_name | table_alias

이 RFC는 '정수형 목록', '더블형 목록' 및 '문자열 목록' OGR 데이터 유형으로의 변환을 구현하자고 제안하지 않습니다. 이런 유형들이 SQL92 사양을 준수하지 않으며, OGR 코드에 이런 변환에 필요한 루틴이 없기 때문입니다.

구현
----

이 제안을 구현하려면 OGR 코드베이스에 다음과 같은 변경 사항들을 적용해야 합니다:

1. :file:`ogr_swq.h` 에 있는 ``swq_col_def`` 에 'field_alias', 'target_type', 'field_length', 그리고 'field_precision'을 담을 필드 4개를 추가해야 할 것입니다.

2. :file:`ogr_swq.h` 에 있는 ``swq_field_type`` 열거형에 SWQ_DATE, SWQ_TIME, 그리고 SWQ_TIMESTAMP를 추가할 것입니다.

3. :file:`swq.c` 에 있는 ``swq_select_preparse`` 가 필드 별명 및 CAST 사양을 처리할 수 있도록 변경해야 할 것입니다.

4. 지원 유형 이름들을 파싱할 수 있도록 새 함수(``swq_parse_typename``)를 추가할 것입니다.

5. :file:`ogr_gensql.cpp` 에 있는 :cpp:class:`OGRGenSQLResultsLayer` 의 ``.ctor`` 가 대상 데이터소스에 필드 이름 및 길이를 설정할 수 있도록 변경할 것입니다.

6. 유형을 지정하는 경우 :file:`ogr_gensql.cpp` 에 있는 :cpp:func:`TranslateFeature` 가 유형 변경을 처리할 수 있도록 변경할 것입니다.

하위 호환성
-----------

현재 SQL 문법의 하위 호환성은 유지될 것입니다. 이 새 기능을 위해 OGR C 및 SWIG API를 변경할 필요는 없습니다.

문서화
------

이 새 기능을 반영해서 OGR SQL 문서를 업데이트할 것입니다. OGR 스타일 문서에 데이터소스들 간의 스타일 전송 지원 내용을 업데이트할 것입니다.

구현 인력
---------

세케레시 터마시가 GDAL/OGR 개발 버전에 이 RFC를 구현할 것입니다.

프랑크 바르메르담이 이 새 기능에 따라 회귀 테스트 스크립트를 구현할 것입니다.

참조
----

-  이 기능에 대한 버그 추적(제안 코드 변경 사항을 모두 담고 있습니다): #2171

투표 이력
---------

-  프랑크 바르메르담(Frank Warmerdam) +1
-  대니얼 모리셋(Daniel Morissette) +1
-  하워드 버틀러(Howard Butler) +1
-  이벤 루올(Even Rouault) +1
-  세케레시 터마시(Szekeres Tamás) +1
-  안드레이 키셀레프(Andrey Kiselev) +0

