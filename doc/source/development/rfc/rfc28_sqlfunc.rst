.. _rfc-28:

================================================================================
RFC 28: OGR SQL 일반화 표현식
================================================================================

저자: 프랑크 바르메르담

연락처: warmerdam@pobox.com

상태: 승인, 구현

요약
----

OGR SQL 평가 엔진은 현재 SELECT 문에서 열에 일반 목적 함수를 적용하지 못 합니다. 몇몇 특수 목적 함수들을 (예: CAST, COUNT, AVG, MAX, MIN, 및 SUM) 지원하지만 좀 더 일반적인 표현식들의 일부로서 지원하는 것은 아니며, 일반적으로 매우 제한된 준비가 필요합니다. 이 작업 항목의 목적은 OGR SQL SELECT 문의 산출 필드 목록에서 일반 목적 표현식 평가를 상당하게 지원할 수 있도록 OGR SQL 엔진을 확장하고, 표준 SQL과 호환되는 방식으로 몇몇 예비 처리 함수를 구현하는 것입니다. 마찬가지로 WHERE 절에 사용되는 표현식도 산술 및 함수 같은 비논리 연산의 평가를 지원하도록 일반화할 것입니다.
예를 들면 구현 이후 다음과 같은 SQL 문도 평가할 수 있게 하려 합니다:

::

   SELECT CONCAT(first_name, ' ', last_name) AS full_name FROM customers
   SELECT id, "Regional Road" AS roadtypename FROM roads where roadtype=3
   SELECT (subtotal+salestax) as totalcost from invoice_info where 100 <= (subtotal+salestax)

`https://svn.osgeo.org/gdal/sandbox/warmerdam/gdal-rfc28/ <https://svn.osgeo.org/gdal/sandbox/warmerdam/gdal-rfc28/>`_ 에서 구현 프로토타입을 살펴볼 수 있습니다.

기술적 접근
-----------

현재 논리 표현식은 기반 요소가 <constant_value> 형식이어야 하는 매우 제한된 서식을 입력받습니다. 일반화 작업의 일환으로, 비논리 표현식을 지원하고 연산자의 왼쪽 및 오른쪽도 동일하게 취급할 것입니다. 현재 OGR SQL 파서(parser)는 그때그때 즉석에서(ad hoc) 처리하기 때문에 이렇게 일반화된 형식의 표현식으로 실질적으로 확장할 수 없습니다. 그렇기 때문에 이 지점에서 표현식을 위한 Yacc/bison 기반 파서 문법으로 넘어갈 것입니다.

SELECT 문의 일부가 표현식인 경우 기존 즉석(ad hoc) SELECT 파싱을 계속해서 사용하는 것은 별로 실용적이지 않기 때문에, SELECT 문 전체를 파싱하는 데 Yacc/bison 기반 파서도 사용할 것입니다.

현재 표현식 노드가 (함수의 인자에 대해) 0개에서 n개 사이의(0-n) 하위 노드를 가지도록, 그리고 필드 참조 및 상수값을 연산을 정의하는 노드에 내장하는 대신 개별 리프(leaf) 노드로 취급하도록 일반화할 것입니다.

이에 따른 부작용으로 WHERE 절도 논리 비교뿐만이 아니라 좀 더 일반적인 표현식을 지원할 것입니다. 다음은 그 예시입니다:

::

   SELECT * WHERE (subtotal+salestax) > 100.0

새 함수
-------

-  산술: ``+``, ``-``, ``*``, ``/``, ``**``
-  문자열: CONCAT, SUBSTR

SELECT 규칙
-----------

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
                    | <cumm-field-func> ( [DISTINCT] <field-ref> )
                    | <field-expr>
                    | Count(*)

   <field-expr> ::= <field_ref>
                    | <constant-value>
                    | <field-expr> <field-operator> <field-expr>
                    | <field-func> ( <field-expr-list> )
                    | ( <field-expr> )

   <field-expr-list> ::= field-expr
                    |  field-expr , field-expr-list
                    |  <empty>

   <as clause> ::= [ AS ] <column_name>

   <data type> ::= character [ ( field_length ) ]
                   | float [ ( field_length ) ]
                   | numeric [ ( field_length [, field_precision ] ) ]
                   | integer [ ( field_length ) ]
                   | date [ ( field_length ) ]
                   | time [ ( field_length ) ]
                   | timestamp [ ( field_length ) ]

   <cumm-field-func> ::= AVG | MAX | MIN | SUM | COUNT

   <field-operator> ::= '+' | '-' | '/' | '*' | '||'

   <field-func> ::= CONCAT | SUBSTR

   <field_ref>  ::= [<table_ref>.]field_name

특별 메모
---------

기존 CAST, 그리고 열 요약 함수 COUNT, AVG, MIN, MAX 및 SUM을 거의 함수처럼 취급할 것이지만, 열 정의에 대한 루트 연산(root operation)으로 제한되며 (여전히) 특수 사례로 취급할 것입니다.

호환성에 미치는 영향
--------------------

예전에는 따옴표 없는 필드 이름으로 사용할 수 있었던 몇몇 식별자를 이제는 따옴표로 감싸야 할 것입니다. 이 문법에서 식별자가 키워드일 것이기 때문입니다. 이 키워드 집합은 다음과 같습니다:

-  IN
-  LIKE
-  NULL
-  IS
-  SELECT
-  LEFT
-  JOIN
-  WHERE
-  ON
-  ORDER
-  BY
-  FROM
-  AS
-  ASC
-  DESC
-  DISTINCT
-  CAST

예전 구현은 C로 작성되었고, OGDI 라이브러리의 WHERE 절 평가자를 포함하는 다른 맥락에서 쉽게 사용할 수 있도록 GDAL/OGR 서비스를 하나도 사용하지 않았습니다. 이 업데이트 이후 C++로 코드를 작성하고, CPL 오류 및 다른 서비스들을 직접 사용하도록 통합합니다. 즉 GDAL과 OGDI가 사용하는 구현이 갈라질 것이라는 의미입니다.

대부분의 경우 예전에는 오류를 발생시켰을 몇몇 OGR SQL 선언문이 작동하게 될 것입니다.

성능에 미치는 영향
------------------

단순 SELECT 문의 경우 평가 속도가 크게 달라지지 않을 것으로 기대하지만, 각 산출 필드를 (아마도 필드로부터 나온 값을 가진 노드가 하나 있는) 표현식으로 평가해야 할 것입니다.

구현 계획
---------

프랑크 바르메르담이 GDAL/OGR 1.8버전 배포판에 맞춰 이 RFC를 구현, 테스트 및 문서화할 것입니다.

테스트
------

기존 OGR SQL 테스트 스위트의 모든 테스트를 통과할 것입니다.
새 기능을 테스트하기 위해 새로운 :file:`autotest/ogr/ogr_sql_rfc28.py` 스크립트를 도입할 것입니다.

문서화
------

새 기능을 설명하기 위해 :ref:`OGR SQL <ogr_sql_dialect>` 문서를 업데이트할 것입니다.

