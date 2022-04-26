.. _ogr_sql_dialect:

================================================================================
OGR SQL 방언
================================================================================

.. highlight:: sql

GDALDataset은 :cpp:func:`GDALDataset::ExecuteSQL` 메소드를 통해 데이터소스를 대상으로 하는 명령어 실행을 지원합니다. 이론적으로는 어떤 유형의 명령어든 이 방식으로 처리할 수 있지만, 실제로는 응용 프로그램에 SQL SELECT 케이퍼빌리티의 부분 집합을 제공하기 위해 이 메커니즘을 사용합니다. 이 문서에서는 OGR 내부에 구현된 일반 SQL 구현 및 드라이버 특화 SQL 지원이 가지는 문제점을 논의합니다.

OGR SQL 방언 대신 대체 "방언"인 SQLite 방언을 사용할 수 있습니다. 자세한 내용은 :ref:`sql_sqlite_dialect` 문서를 참조하십시오.

OGRLayer 클래스도 :cpp:func:`OGRLayer::SetAttributeFilter()` 메소드를 사용해서 반환되는 객체에 속성 쿼리 필터를 적용할 수 있습니다. 속성 필터의 문법은 OGR SQL SELECT 선언문의 WHERE 절의 문법과 동일합니다. 즉 이 문서에서 WHERE 절과 관련된 모든 것은 ``SetAttributeFilter()`` 메소드의 맥락에서 적용됩니다.

SELECT
------

SELECT 선언문을 사용해서 임시 객체 레이어로 표현되는 쿼리 결과물을 가진 (RDBMS의 테이블 행과 유사한) 레이어 객체를 가져옵니다. 데이터소스의 레이어는 RDBMS에 있는 테이블과 유사하며 객체 속성은 열의 값과 유사합니다. OGR SQL SELECT 문의 가장 단순한 형식은 다음과 같습니다:

.. code-block::

    SELECT * FROM polylayer

이 경우 "polylayer"라는 레이어로부터 모든 객체를 가져오고, 이 객체들의 모든 속성을 반환합니다. 레이어에 직접 접근하는 것과 본질적으로 동등합니다. 이 예시에서 "\*"는 레이어로부터 가져올 필드들의 목록이며, 이때 "\*"는 모든 필드를 가져와야 한다는 뜻입니다.

다음 예시는 조금 더 복잡한 형식으로, 레이어로부터 모든 객체를 가져오지만 스키마는 도형 열과 EAS_ID 및 PROP_VALUE 속성만 담게 될 것입니다. OGR SQL 방언을 사용하면 언제나 결과물에 도형 열을 포함시키기 때문에 SQL 문에 따로 작성할 필요가 없습니다:

.. code-block::

    SELECT eas_id, prop_value FROM polylayer


다음은 WHERE 절로 가져오는 객체를 제약하고 결과물을 정렬시키는 좀 더 복잡한 SELECT 문의 예시입니다:

.. code-block::

    SELECT * from polylayer WHERE prop_value > 220000.0 ORDER BY prop_value DESC

다음 SELECT 문은 객체 하나만 가진 테이블을 생성합니다. 이 객체는 도형 및 EAS_ID 속성의 개별 값 여러 개를 담고 있는 ("count_eas_id" 같은 이름을 가진) 속성 하나를 가집니다:

.. code-block::

    SELECT COUNT(DISTINCT eas_id) FROM polylayer

일반 문법
++++++++++++++

SELECT 문의 일반 문법은 다음과 같습니다:

.. code-block::

    SELECT [fields] FROM layer_name [JOIN ...] [WHERE ...] [ORDER BY ...] [LIMIT ...] [OFFSET ...]

목록 연산자
++++++++++++++

'fields' 목록은 소스 레이어로부터 산출 객체로 옮겨지는 필드들을 쉼표로 구분한 목록입니다. 이 필드들은 산출 객체에 필드 목록에서의 순서대로 나타나기 때문에, 필드 목록을 필드들을 재정렬하기 위해 사용할 수도 있습니다.

DISTINCT 키워드를 사용하는 특수 형식의 필드 목록이 있습니다. 이 특수 목록은 지정된 속성의 모든 개별 값들의 목록을 반환합니다. DISTINCT 키워드를 사용하는 경우, 필드 목록에 단 하나의 속성만 나타날 수도 있습니다. DISTINCT 키워드는 모든 유형의 필드에 사용할 수 있습니다. 현재 OGR SQL에서 문자열 값을 대상으로 테스트된 개별성(distinctness)은 대소문자를 구분하지 않습니다. DISTINCT 키워드를 사용한 SELECT 문의 결과물은 (작업한 필드와 같은 이름을 가진) 열 1개를 가진 레이어로, 개별 값 하나 당 객체 하나를 가집니다. 도형은 폐기합니다. 개별 값들을 메모리로 불러오기 때문에, 수많은 개수의 개별 값을 가진 데이터셋의 경우 메모리를 많이 차지할 수도 있습니다.

.. code-block::

    SELECT DISTINCT areacode FROM polylayer

열에 적용할 수도 있는 요약(summarization) 연산자도 몇 개 있습니다. 어떤 필드에 요약 연산자를 적용하는 경우, 모든 필드에 요약 연산자를 적용해야만 합니다. 이런 요약 연산자로는 COUNT(인스턴스의 개수), AVG(숫자 평균), SUM(숫자 합), MIN(어휘 또는 숫자 최소값), 그리고 MAX(어휘 또는 숫자 최대값)가 있습니다. 다음은 행정 구역 속성값에 관한 다양한 요약 정보를 생성하는 예시입니다:

.. code-block::

    SELECT MIN(prop_value), MAX(prop_value), AVG(prop_value), SUM(prop_value),
        COUNT(prop_value) FROM polylayer WHERE prov_name = 'Ontario'

SELECT 문의 DISTINCT 키워드에 COUNT() 연산자를 적용하면 개별 값들의 개수도 수집할 수 있습니다. 다음은 그 예시입니다:

.. code-block::

    SELECT COUNT(DISTINCT areacode) FROM polylayer

특수 사용례로, COUNT() 연산자에 필드명 대신 모든 레코드를 세도록 하기 위한 단축 형식인 "\*" 인자를 지정할 수도 있습니다:

.. code-block::

    SELECT COUNT(*) FROM polylayer

필드명 앞에 테이블명을 접두어로 붙일 수도 있지만, 결합(join)을 수행하는 경우에만 의미가 있습니다. JOIN 단락에서 자세히 설명하겠습니다.

필드 정의가 산술 및 함수 연산자를 사용하는 복잡 표현식일 수도 있습니다. 하지만 DISTINCT 키워드와 MIN, MAX, AVG 및 SUM 같은 요약 연산자는 표현식 필드에 적용되지 못 할 수도 있습니다. 불(boolean) 값을 산출하는 (비교 및 논리 연산자) 표현식도 사용할 수 있습니다:

.. code-block::

    SELECT cost+tax from invoice

또는

.. code-block::

    SELECT CONCAT(owner_first_name,' ',owner_last_name) from properties

함수
*********

SUBSTR 함수를 사용해서 문자열로부터 하위 문자열을 추출할 수 있습니다. 그 문법은 다음과 같습니다:

::

   SUBSTR(string_expr, start_offset [, length])

이 명령어는 string_expr로부터 start_offset 오프셋에서 시작하는 (start_offset=1이면 string_expr의 첫 번째 문자, start_offset=2면 두 번째 문자, ...) 하위 문자열을 추출합니다. start_offset이 음의 값인 경우, 문자열의 끝으로부터 (start_offset=-1이면 문자열의 마지막 문자, start_offset=-2이면 마지막 문자 바로 앞의 문자, ...) 하위 문자열을 추출합니다. 'length'를 지정하면 문자열로부터 해당 개수만큼의 문자들을 추출합니다. 지정하지 않으면 문자열의 끝까지 추출합니다.

주의: 당분간은 문자를 바이트와 동등한 것으로 간주합니다. 이는 UTF-8처럼 문자 하나를 바이트 여러 개로 표현하는 인코딩에는 적절하지 않을 수도 있습니다.

.. code-block::

    SELECT SUBSTR('abcdef',1,2) FROM xxx   --> 'ab'
    SELECT SUBSTR('abcdef',4)   FROM xxx   --> 'def'
    SELECT SUBSTR('abcdef',-2)  FROM xxx   --> 'ef'

``hstore_get_value()`` 함수를 사용하면 HSTORE 문자열로부터 키와 관련된 값을 ``key=>value,other_key=>other_value,...`` 같은 서식으로 추출할 수 있습니다:

.. code-block::

    SELECT hstore_get_value('a => b, "key with space"=> "value with space"', 'key with space') FROM xxx --> 'value with space'

필드 이름 별명 사용하기
**************************

OGR SQL은 다음 예시와 같은 문법으로 AS 키워드를 이용해서 필드명이 SQL92 사양을 준수하도록 재명명할 수 있습니다:

.. code-block::

    SELECT *, OGR_STYLE AS STYLE FROM polylayer

열 지정 작업에서 이 필드 이름 별명을 마지막 작업으로 사용할 수 있습니다. 따라서 연산자 안에서 필드를 재명명할 수 없지만, 전체 열 표현식을 다음 두 예시처럼 재명명할 수는 있습니다:

.. code-block::

    SELECT COUNT(areacode) AS "count" FROM polylayer
    SELECT dollars/100.0 AS cents FROM polylayer

필드 유형 변경하기
*******************************

OGR SQL은 다음 예시와 같은 문법으로 SQL92 사양을 준수하는 CAST 연산자를 이용해서 열 유형을 변경할 수 있습니다:

.. code-block::

    SELECT *, CAST(OGR_STYLE AS character(255)) FROM rivers

현재 다음 대상 유형들로 캐스트할 수 있습니다:

- boolean
- character(field_length): field_length의 기본값은 1입니다.
- float(field_length)
- numeric(field_length, field_precision)
- smallint(field_length): 부호 있는 16비트 정수형
- integer(field_length)
- bigint(field_length): 64비트 정수형으로, SQL92 사양의 확장 사양입니다.
- date(field_length)
- time(field_length)
- timestamp(field_length)
- geometry, geometry(geometry_type), geometry(geometry_type,epsg_code)

field_length 그리고/또는 field_precision 지정은 선택적 옵션입니다. character() 유형의 길이를 명확하게 0으로 지정하면 가변 길이(variable width)를 사용할 수 있습니다. 'integer list', 'double list' 및 'string list' OGR 데이터 유형으로의 변환은 지원하지 않습니다. 이 유형들은 SQL92 사양을 준수하지 않기 때문입니다.

CAST 연산자는 WHERE 절 안을 포함해서 표현식 안 어디에나 넣을 수 있지만, CAST 연산자가 필드 정의 목록에 있는 필드에 대한 "가장 바깥쪽에 있는" 연산자인 경우에만 산출 필드 유형을 세밀하게 제어할 수 있습니다. CAST가 "가장 바깥쪽에 있는" 연산자가 아닌 경우에도 숫자형, 문자열 및 날짜 데이터 유형들을 서로 변환하는 데 유용한 연산자입니다.

WKT 문자열을 도형으로 캐스트할 수 있습니다. 이때 geometry_type은 POINT[Z], LINESTRING[Z], POLYGON[Z], MULTIPOINT[Z], MULTILINESTRING[Z], MULTIPOLYGON[Z], GEOMETRYCOLLECTION[Z] 또는 GEOMETRY[Z] 가운데 하나일 수 있습니다.

문자열 직역 및 식별자 인용
***************************************

SQL92 규칙은 문자열 직역(string literals) 및 식별자 인용이라는 측면에서 엄격하게 적용됩니다.

문자열 직역(상수)을 작은따옴표 문자로 감싸야만 합니다:

::

   WHERE a_field = 'a_value'

식별자가 특수 문자를 포함하고 있지 않거나 SQL 예약 키워드가 아닌 경우 (열 이름 및 테이블 이름의) 식별자를 인용 부호 없이 사용할 수 있습니다. 하지만 그렇다면 반드시 큰따옴표 문자로 감싸야만 합니다:

::

   WHERE "from" = 5

WHERE
+++++

WHERE 절에 들어가는 인자는 소스 레이어로부터 레코드를 선택하기 위해 사용되는 논리 표현식입니다. WHERE 문 안에서의 쓰임뿐만 아니라, WHERE 절이 처리하는 이 표현식은 :cpp:func:`OGRLayer::SetAttributeFilter` 메소드를 통해 정규 레이어에 대한 OGR 속성 쿼리에도 사용됩니다.

WHERE 절 맥락에서는 SELECT 문의 필드 선택 절에 있는 표현식에 사용할 수 있는 산술 및 기타 함수 연산자뿐만 아니라, 논리 연산자도 사용할 수 있으며 표현식의 평가된 값은 논리적(참 또는 거짓)이어야 합니다.

다음 논리 연산자를 사용할 수 있습니다:

- ``=``
- ``!=``
- ``<>``
- ``<``
- ``>``
- ``<=``
- ``>=``
- ``LIKE`` 및 ``ILIKE``
- ``BETWEEN`` 및 ``IN``

대부분의 연산자는 따로 설명이 필요없지만, ``!=`` 와 ``<>`` 연산자는 동등하고 문자열 동등 비교는 대소문자를 구분하지 않지만 ``<``, ``>``, ``<=`` 그리고 ``>=`` 연산자는 대소문자를 구분한다는 사실은 기억해둘 만합니다.

GDAL 3.1버전부터 ``LIKE`` 연산자는 대소문자를 구분하고 ``ILIKE`` 연산자는 대소문자를 구분하지 않습니다. 이전 버전들에서는 ``LIKE`` 연산자도 대소문자를 구분하지 않았습니다. GDAL 3.1버전에서 예전 습성을 사용하고 싶다면 :decl_configoption:`OGR_SQL_LIKE_AS_ILIKE` 환경설정 옵션을 YES로 설정해주면 됩니다.

``LIKE`` 및 ``ILIKE`` 연산자에 들어가는 값 인자는 값 문자열이 일치하는지 판단하기 위한 패턴입니다. 이 패턴에서 백분율('%') 문자는 어떤 개수의 문자와도 일치하며, 언더바('_') 문자는 문자 1개와 일치합니다. 선택적인 ESCAPE escape_char 절을 추가해서 앞에 escape_char 문자가 붙는 백분율 또는 언더바 문자를 정규 문자로 검색할 수 있습니다.

.. list-table:: Pattern Arguments of LIKE and ILIKE operators
   :header-rows: 1

   * - 문자열
     - 패턴
     - 일치 여부
   * - Alberta
     - ALB%
     - Ｏ
   * - Alberta
     - _lberta
     - Ｏ
   * - St. Alberta
     - _lberta
     - Ｘ
   * - St. Alberta
     - %lberta
     - Ｏ
   * - Robarts St.
     - %Robarts%
     - Ｏ
   * - 12345
     - 123%45
     - Ｏ
   * - 123.45
     - 12?45
     - Ｘ
   * - N0N 1P0
     - %N0N%
     - Ｏ
   * - L4C 5E2
     - %N0N%
     - Ｘ

``IN`` 연산자는 값들의 목록을 인자로 입력받으며 입력 목록에 있는 속성 값들의 멤버십을 테스트합니다.

.. list-table:: Logics of IN operator
   :header-rows: 1

   * - 값
     - 값 목록
     - 일치 여부
   * - 321
     - IN (456,123)
     - Ｘ
   * - 'Ontario'
     - IN ('Ontario','BC')
     - Ｏ
   * - 'Ont'
     - IN ('Ontario','BC')
     - Ｘ
   * - 1
     - IN (0,2,4,6)
     - Ｘ

``BETWEEN`` 연산자의 문법은 다음과 같으며:

::

   field_name BETWEEN value1 AND value2

이 표현식은 다음과 동등합니다:

::

   field_name >= value1 AND field_name <= value2

앞의 이항 연산자들뿐만 아니라, 필드가 NULL인지 여부를 테스트하기 위한 추가 연산자들이 있습니다. 바로 ``IS NULL`` 과 ``IS NOT NULL`` 연산자입니다.

``AND``, ``OR`` 및 단항 ``NOT`` 을 포함하는 논리 연산자들을 이용하는 좀 더 복잡한 표현식에 이런 기본 필드 테스트를 결합시킬 수 있습니다. 이런 하위 표현식은 우선 순위를 명확하게 하기 위해 괄호로 묶어야 합니다. 다음은 이런 복잡한 표현식의 예시입니다:

.. code-block::

    SELECT * FROM poly WHERE (prop_value >= 100000) AND (prop_value < 200000)
    SELECT * FROM poly WHERE NOT (area_code LIKE 'N0N%')
    SELECT * FROM poly WHERE (prop_value IS NOT NULL) AND (prop_value < 100000)

WHERE 제한 사항
+++++++++++++++++

- (FROM 절에 목록화된) 기본 테이블에서 모든 필드를 가져와야만 합니다.

- ``<``, ``>``, ``<=`` 및 ``>=`` 연산자를 제외한 모든 문자열 비교는 대소문자를 구분하지 않습니다.

ORDER BY
++++++++

``ORDER BY`` 절은 반환된 객체들을 하나 이상의 필드에 대해 정렬 순서에 따라 (오름차순 또는 내림차순) 강제로 재정렬합니다. ASC 또는 DESC 키워드를 둘 다 지정하지 않는 경우 기본값은 (증가하는) 오름차순입니다. 다음은 그 예시입니다:

.. code-block::

    SELECT * FROM property WHERE class_code = 7 ORDER BY prop_value DESC
    SELECT * FROM property ORDER BY prop_value
    SELECT * FROM property ORDER BY prop_value ASC
    SELECT DISTINCT zip_code FROM property ORDER BY zip_code
    SELECT * FROM property ORDER BY prop_value ASC, another_field DESC

ORDER BY 절이 객체 집합을 두 번 처리한다는 사실을 기억하십시오. 첫 번째는 객체ID에 대응하는 필드 값들을 가진 인메모리 테이블을 작성하고, 두 번째는 객체ID를 이용해서 정렬 순서대로 객체를 가져옵니다. 객체ID를 이용해서 객체를 효율적으로 임의 읽기할 수 없는 포맷의 경우 이 작업이 아주 오래 걸릴 수 있습니다.

대소문자를 구분하지 않는 다른 대부분의 OGR SQL 경우와는 달리, 문자열 필드 값을 정렬하는 작업은 대소문자를 구분합니다.

LIMIT 및 OFFSET
++++++++++++++++

GDAL 2.2버전부터, ``LIMIT`` 절을 사용해서 반환되는 객체들의 개수를 제한할 수 있습니다. 다음은 그 예시입니다:

.. code-block::

    SELECT * FROM poly LIMIT 5

``OFFSET`` 절을 사용하면 결과물 집합에서 처음 객체들을 건너뛸 수 있습니다. OFFSET 뒤에 오는 값이 건너뛸 객체 개수입니다. 예를 들어 결과물 집합에서 처음 3개의 객체를 건너뛰려면:

.. code-block::

    SELECT * FROM poly OFFSET 3

이 두 절을 결합할 수 있습니다:

.. code-block::

    SELECT * FROM poly LIMIT 5 OFFSET 3

JOIN
+++++

OGR SQL supports a limited form of one to one JOIN.  This allows records from
a secondary table to be looked up based on a shared key between it and the
primary table being queried.  For instance, a table of city locations might
include a **nation_id** column that can be used as a reference into a
secondary **nation** table to fetch a nation name.  A joined query might
look like:

.. code-block::

    SELECT city.*, nation.name FROM city
        LEFT JOIN nation ON city.nation_id = nation.id

This query would result in a table with all the fields from the city table,
and an additional "nation.name" field with the nation name pulled from the
nation table by looking for the record in the nation table that has the "id"
field with the same value as the city.nation_id field.

Joins introduce a number of additional issues.  One is the concept of table
qualifiers on field names.  For instance, referring to city.nation_id instead
of just nation_id to indicate the nation_id field from the city layer.  The
table name qualifiers may only be used in the field list, and within the
``ON`` clause of the join.

Wildcards are also somewhat more involved.  All fields from the primary table
(**city** in this case) and the secondary table (**nation** in this
case) may be selected using the usual ``*`` wildcard.  But the fields of
just one of the primary or secondary table may be selected by prefixing the
asterix with the table name.

The field names in the resulting query layer will be qualified by the table
name, if the table name is given as a qualifier in the field list.  In addition
field names will be qualified with a table name if they would conflict with
earlier fields.  For instance, the following select would result might result
in a results set with a **name, nation_id, nation.nation_id** and **
nation.name** field if the city and nation tables both have the
**nation_id** and **name** fieldnames.

.. code-block::

    SELECT * FROM city LEFT JOIN nation ON city.nation_id = nation.nation_id

On the other hand if the nation table had a **continent_id** field, but
the city table did not, then that field would not need to be qualified in
the result set.  However, if the selected instead looked like the following
statement, all result fields would be qualified by the table name.

.. code-block::

    SELECT city.*, nation.* FROM city
        LEFT JOIN nation ON city.nation_id = nation.nation_id

In the above examples, the **nation** table was found in the same
datasource as the **city** table.   However, the OGR join support
includes the ability to join against a table in a different data source,
potentially of a different format.  This is indicated by qualifying the
secondary table name with a datasource name.  In this case the secondary
datasource is opened using normal OGR semantics and utilized to access the
secondary table until the query result is no longer needed.

.. code-block::

    SELECT * FROM city
    LEFT JOIN '/usr2/data/nation.dbf'.nation ON city.nation_id = nation.nation_id

While not necessarily very useful, it is also possible to introduce table
aliases to simplify some SELECT statements.  This can also be useful to
disambiguate situations where tables of the same name are being used from
different data sources.  For instance, if the actual
tables names were messy we might want to do something like:

.. code-block::

    SELECT c.name, n.name FROM project_615_city c
    LEFT JOIN '/usr2/data/project_615_nation.dbf'.project_615_nation n
                ON c.nation_id = n.nation_id

It is possible to do multiple joins in a single query.

.. code-block::

    SELECT city.name, prov.name, nation.name FROM city
    LEFT JOIN province ON city.prov_id = province.id
    LEFT JOIN nation ON city.nation_id = nation.id

The expression after ON is typically of the form
"{primary_table}.{field_name} = {secondary_table}.{field_name}", and in that
order.
It is also possible to use a more complex boolean expression,
involving multiple comparison operators, but with the restrictions mentioned
in the below "JOIN limitations" section. In particular, in case of multiple joins (3 tables
or more) the fields compared in a JOIN must belong to the primary table (the one
after FROM) and the table of the active JOIN.

JOIN 제한 사
++++++++++++++++

- Joins can be very expensive operations if the secondary table is not indexed on the key field being used.
- Joined fields may not be used in WHERE clauses, or ORDER BY clauses at this time.  The join is essentially evaluated after all primary table subsetting is complete, and after the ORDER BY pass.
- Joined fields may not be used as keys in later joins.  So you could not use the province id in a city to lookup the province record, and then use a nation id from the province id to lookup the nation record.  This is a sensible thing to want and could be implemented, but is not currently supported.
- Datasource names for joined tables are evaluated relative to the current processes working directory, not the path to the primary datasource.
- These are not true LEFT or RIGHT joins in the RDBMS sense.  Whether or not a secondary record exists for the join key or not, one and only one copy of the primary record is returned in the result set.  If a secondary record cannot be found, the secondary derived fields will be NULL.  If more than one matching secondary field is found only the first will be used.

UNION ALL
+++++++++

The SQL engine can deal with several SELECT combined with
UNION ALL. The effect of UNION ALL is to concatenate the rows returned by the right SELECT
statement to the rows returned by the left SELECT statement.

.. code-block::

    [(] SELECT field_list FROM first_layer [WHERE where_expr] [)]
    UNION ALL [(] SELECT field_list FROM second_layer [WHERE where_expr] [)]
    [UNION ALL [(] SELECT field_list FROM third_layer [WHERE where_expr] [)]]*

UNION ALL 제약 조건
++++++++++++++++++++++

The processing of UNION ALL in OGR differs from the SQL standard, in which it accepts
that the columns from the various SELECT are not identical. In that case, it will return
a super-set of all the fields from each SELECT statement.

There is also a restriction : ORDER BY can only be specified for each SELECT, and
not at the level of the result of the union.

SPECIAL FIELDS
--------------

The OGR SQL query processor treats some of the attributes of the features as
built-in special fields can be used in the SQL statements likewise the
other fields. These fields can be placed in the select list, the WHERE clause
and the ORDER BY clause respectively. The special field will not be included
in the result by default but it may be explicitly included by adding it to
the select list.
When accessing the field values the special fields will take precedence over
the other fields with the same names in the data source.

FID
+++

Normally the feature id is a special property of a feature and not treated
as an attribute of the feature.  In some cases it is convenient to be able to
utilize the feature id in queries and result sets as a regular field.  To do
so use the name ``FID``.  The field wildcard expansions will not include
the feature id, but it may be explicitly included using a syntax like:

.. code-block::

    SELECT FID, * FROM nation

도형 필드
++++++++++++++

The OGR SQL dialect adds the geometry field of the datasource to the result set
by default. Users do not need to select the geometry explicitly but it is still
possible to do so. Common use case is when geometry is the only field that is needed.
In this case the name of the geometry field to be used in the SQL statement is the
name returned by :cpp:func:`OGRLayer::GetGeometryColumn`. If the method returns
an empty string then a special name "_ogr_geometry_" must be used. The name begins
with an underscore and SQL syntax requires that it must appear between double quotes.
In addition the command line interpreter may require that double quotes are escaped
and the final SELECT statement could look like:

.. code-block::

    SELECT "_ogr_geometry_" FROM nation
    
OGR_GEOMETRY
++++++++++++

Some of the data sources (like MapInfo tab) can handle geometries of different
types within the same layer. The ``OGR_GEOMETRY`` special field represents
the geometry type returned by :cpp:func:`OGRGeometry::getGeometryName` and can be used to
distinguish the various types. By using this field one can select particular
types of the geometries like:

.. code-block::

    SELECT * FROM nation WHERE OGR_GEOMETRY='POINT' OR OGR_GEOMETRY='POLYGON'

OGR_GEOM_WKT
++++++++++++

The Well Known Text representation of the geometry can also be used as
a special field. To select the WKT of the geometry ``OGR_GEOM_WKT``
might be included in the select list, like:

.. code-block::

    SELECT OGR_GEOM_WKT, * FROM nation

Using the ``OGR_GEOM_WKT`` and the ``LIKE`` operator in the WHERE
clause we can get similar effect as using OGR_GEOMETRY:

.. code-block::

    SELECT OGR_GEOM_WKT, * FROM nation WHERE OGR_GEOM_WKT
    LIKE 'POINT%' OR OGR_GEOM_WKT LIKE 'POLYGON%'

OGR_GEOM_AREA
+++++++++++++

The ``OGR_GEOM_AREA`` special field returns the area of the feature's
geometry computed by the OGRSurface::get_Area() method. For
OGRGeometryCollection and OGRMultiPolygon the value is the sum of the
areas of its members. For non-surface geometries the returned area is 0.0.

For example, to select only polygon features larger than a given area:

.. code-block::

    SELECT * FROM nation WHERE OGR_GEOM_AREA > 10000000

OGR_STYLE
+++++++++

The ``OGR_STYLE`` special field represents the style string of the feature
returned by OGRFeature::GetStyleString(). By using this field and the
``LIKE`` operator the result of the query can be filtered by the style.
For example we can select the annotation features as:

.. code-block::

    SELECT * FROM nation WHERE OGR_STYLE LIKE 'LABEL%'

CREATE INDEX
------------

Some OGR SQL drivers support creating of attribute indexes.  Currently
this includes the Shapefile driver.  An index accelerates very simple
attribute queries of the form **fieldname = value**, which is what
is used by the ``JOIN`` capability.  To create an attribute index on
the nation_id field of the nation table a command like this would be used:

.. code-block::

    CREATE INDEX ON nation USING nation_id

색인 제한 사항
+++++++++++++++++

- Indexes are not maintained dynamically when new features are added to or removed from a layer.
- Very long strings (longer than 256 characters?) cannot currently be indexed.
- To recreate an index it is necessary to drop all indexes on a layer and then recreate all the indexes.
- Indexes are not used in any complex queries.   Currently the only query the will accelerate is a simple "field = value" query.

DROP INDEX
----------

The OGR SQL DROP INDEX command can be used to drop all indexes on a particular
table, or just the index for a particular column.

.. code-block::

    DROP INDEX ON nation USING nation_id
    DROP INDEX ON nation

ALTER TABLE
-----------

The following OGR SQL ALTER TABLE commands can be used.

- ::

      ALTER TABLE tablename ADD [COLUMN] columnname columntype

새 필드를 추가합니다. 레이어가 OLCCreateField 케이퍼빌리티를 선언하는 경우 지원합니다.

- "ALTER TABLE tablename RENAME [COLUMN] oldcolumnname TO newcolumnname" to rename an existing field. Supported if the layer declares the OLCAlterFieldDefn capability.

- "ALTER TABLE tablename ALTER [COLUMN] columnname TYPE columntype" to change the type of an existing field. Supported if the layer declares the OLCAlterFieldDefn capability.

- "ALTER TABLE tablename DROP [COLUMN] columnname" to delete an existing field. Supported if the layer declares the OLCDeleteField capability.

The columntype value follows the syntax of the types supported by the CAST operator described above.

.. code-block::

    ALTER TABLE nation ADD COLUMN myfield integer
    ALTER TABLE nation RENAME COLUMN myfield TO myfield2
    ALTER TABLE nation ALTER COLUMN myfield2 TYPE character(15)
    ALTER TABLE nation DROP COLUMN myfield2

DROP TABLE
----------

The OGR SQL DROP TABLE command can be used to delete a table. This is only
supported on datasources that declare the ODsCDeleteLayer capability.

.. code-block::

    DROP TABLE nation

ExecuteSQL()
------------

SQL is executed against an GDALDataset, not against a specific layer.  The
call looks like this:

.. code-block:: cpp

    OGRLayer * GDALDataset::ExecuteSQL( const char *pszSQLCommand,
                                        OGRGeometry *poSpatialFilter,
                                        const char *pszDialect );

The ``pszDialect`` argument is in theory intended to allow for support of
different command languages against a provider, but for now applications
should always pass an empty (not NULL) string to get the default dialect.

The ``poSpatialFilter`` argument is a geometry used to select a bounding rectangle
for features to be returned in a manner similar to the
:cpp:func:`OGRLayer::SetSpatialFilter` method.  It may be NULL for no special spatial
restriction.

The result of an ExecuteSQL() call is usually a temporary OGRLayer representing
the results set from the statement.  This is the case for a SELECT statement
for instance.  The returned temporary layer should be released with
:cpp:func:`GDALDataset::ReleaseResultsSet` method when no longer needed.  Failure
to release it before the datasource is destroyed may result in a crash.

OGR가 아닌 SQL
--------------

All OGR drivers for database systems: :ref:`vector.mysql`, :ref:`vector.pg`,
:ref:`vector.oci`, :ref:`vector.sqlite`, :ref:`vector.odbc`, :ref:`vector.pgeo`,
:ref:`vector.hana` and :ref:`vector.mssqlspatial`,
override the :cpp:func:`GDALDataset::ExecuteSQL` function with dedicated implementation
and, by default, pass the SQL statements directly to the underlying RDBMS.
In these cases the SQL syntax varies in some particulars from OGR SQL.
Also, anything possible in SQL can then be accomplished for these particular
databases.  Only the result of SQL WHERE statements will be returned as
layers.

