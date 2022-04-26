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

OGR SQL은 일대일 JOIN의 제한된 형식을 지원합니다. 일대일 JOIN은 쿼리 중인 기본 테이블과 부 테이블 사이의 공유 키를 기반으로 부 테이블에서 레코드를 검색할 수 있게 해줍니다. 예를 들면 "city" 테이블이 국가 이름을 가져오기 위해 "nation" 부 테이블을 가리키는 참조로 사용할 수 있는 "nation_id" 열을 포함하고 있을 수도 있습니다. 다음은 결합 쿼리의 예시입니다:

.. code-block::

    SELECT city.*, nation.name FROM city
        LEFT JOIN nation ON city.nation_id = nation.id

이 쿼리는 "city" 테이블의 모든 필드와 "nation" 테이블에서 "city.nation_id" 필드 값과 동일한 "id" 필드 값을 가진 레코드를 검색해서 나온 국가 이름을 가지고 있는 추가 "nation.name" 필드를 가진 테이블을 산출할 것입니다.

JOIN은 여러 가지 추가적인 문제점을 발생시킵니다. 그 중 하나는 필드 이름에 대한 테이블 검증자(qualifier)라는 개념입니다. 예를 들어 "nation_id" 필드가 "city" 레이어에 속해 있다는 것을 나타내기 위해 그냥 "nation_id" 대신 "city.nation_id"로 참조하는 것입니다. 이 테이블 이름 검증자는 필드 목록에서만, 그리고 JOIN의 ``ON`` 절 안에서만 사용될 수도 있습니다.

와일드카드 문자도 좀 더 포함될 수 있습니다. 일반적인 ``*`` 와일드카드 문자를 사용해서 기본 테이블의 (이 경우 "city" 테이블의) 모든 필드와 부 테이블의 (이 경우 "nation" 테이블의) 모든 필드를 선택할 수도 있습니다. 하지만 테이블 이름 앞에 ``*`` 와일드카드 문자를 붙이면 기본 또는 부 테이블 가운데 하나만의 필드를 모두 선택할 수도 있습니다.

필드 목록에 테이블 이름을 검증자로 지정한 경우 산출 쿼리 레이어에 있는 필드 이름들을 테이블 이름으로 검증할 것입니다. 또한 필드 이름이 이전 필드와 충돌할 경우에도 필드 이름을 테이블 이름으로 검증할 것입니다.예를 들어 "city" 및 "nation" 테이블 둘 다 "nation_id" 및 "name" 필드명을 가지고 있다면, 다음 예시 SELECT 문은 "name", "nation_id", "nation.nation_id" 및 "nation.name" 필드를 가진 결과물을 산출할 것입니다:

.. code-block::

    SELECT * FROM city LEFT JOIN nation ON city.nation_id = nation.nation_id

반면 "nation" 테이블이 "continent_id" 필드를 가졌지만 "city" 테이블에는 없는 경우, 결과물에서 해당 필드를 검증할 필요는 없을 것입니다. 하지만 다음 예시 SELECT 문처럼 필드를 선택한다면 모든 산출 필드를 테이블 이름으로 검증할 것입니다:

.. code-block::

    SELECT city.*, nation.* FROM city
        LEFT JOIN nation ON city.nation_id = nation.nation_id

이 두 예시에서 "city" 테이블과 "nation" 테이블은 동일한 데이터소스에 있습니다. 하지만 OGR JOIN은 서로 다른 데이터소스에 있는, 서로 다른 포맷일 수도 있는 테이블에 대해 JOIN을 사용할 수 있는 기능을 지원합니다. 부 테이블 이름을 데이터소스 이름으로 검증하면 됩니다. 이 경우 일반 OGR 구문을 이용해서 부 데이터소스를 열고 쿼리 결과물이 더 이상 필요하지 않을 때까지 부 테이블에 접근을 유지합니다:

.. code-block::

    SELECT * FROM city
    LEFT JOIN '/usr2/data/nation.dbf'.nation ON city.nation_id = nation.nation_id

그렇게 꼭 유용한 것은 아니지만, 어떤 SELECT 문을 단순화하기 위해 테이블 별명을 도입할 수도 있습니다. 서로 다른 데이터소스들로부터 동일한 이름을 가진 두 테이블을 사용하는 경우 상황을 분명히 구분하는 데에도 유용할 수 있습니다. 예를 들어 실제 테이블 이름이 지저분한 경우 다음 예시처럼 단순화하고 싶을 수도 있습니다:

.. code-block::

    SELECT c.name, n.name FROM project_615_city c
    LEFT JOIN '/usr2/data/project_615_nation.dbf'.project_615_nation n
                ON c.nation_id = n.nation_id

단일 쿼리에 JOIN을 여러 번 사용할 수도 있습니다:

.. code-block::

    SELECT city.name, prov.name, nation.name FROM city
    LEFT JOIN province ON city.prov_id = province.id
    LEFT JOIN nation ON city.nation_id = nation.id

ON 뒤에 오는 표현식은 일반적으로 다음과 같은 형식이며:

::

   {primary_table}.{field_name} = {secondary_table}.{field_name}

이 순서 그대로입니다.

비교 연산자를 여러 개 포함하는 더 복잡한 불(boolean) 표현식을 사용할 수도 있지만, 다음 "JOIN 제한 사항" 단락에서 설명하는 제약 조건들이 적용됩니다. 특히 (테이블 3개 이상을 대상으로) JOIN을 여러 번 사용하는 경우 JOIN 절 안에서 비교되는 필드들이 반드시 (FROM 다음에 오는) 기본 테이블과 활성 JOIN의 테이블에 속해 있어야만 합니다.

JOIN 제한 사항
++++++++++++++++

- 부 테이블이 사용 중인 키 필드에 대해 색인되어 있지 않은 경우 JOIN 작업의 부하량이 매우 커질 수 있습니다.

- 현재 WHERE 절 또는 ORDER BY 절에서 결합된 필드를 사용하지 못 할 수도 있습니다. JOIN 작업이 본질적으로 모든 기본 테이블 부분 집합 작업이 완료되고 ORDER BY 처리가 끝난 다음에야 평가되기 때문입니다.

- 결합된 필드를 다음 결합에서 키로 사용하지 못 할 수도 있습니다. 즉 "city" 테이블에서 "province" 레코드를 검색하기 위해 "province_id"를 사용한 다음, "province_id"로부터 나온 "nation_id"를 사용해서 "nation" 레코드를 검색할 수 없다는 뜻입니다. 결합된 필드를 다음 결합에서 키로 사용할 수 있도록 구현하기를 바라는 것이 당연하겠지만, 현재로서는 지원하지 않습니다.

- 결합된 테이블들의 데이터소스 이름을 기본 데이터소스를 가리키는 경로가 아니라 현재 작업 중인 디렉터리에 상대적으로 평가합니다.

- RDBMS 관점에서 LEFT 또는 RIGHT 결합은 말이 되지 않습니다. 결합 키에 대해 부 레코드가 존재하느냐에 상관없이 결과물에 기본 레코드의 복사본 하나만 반환합니다. 부 레코드를 찾을 수 없는 경우 파생된 부 필드는 NULL일 것입니다. 일치하는 부 필드를 하나 이상 찾은 경우 첫 번째 필드만 사용할 것입니다.

UNION ALL
+++++++++

SQL 엔진은 UNION ALL과 결합된 SELECT 문 여러 개를 처리할 수 있습니다. UNION ALL은 RIGHT SELECT 문이 반환하는 행들을 LEFT SELECT 문이 반환하는 행들에 연결(concatenate)시킵니다.

.. code-block::

    [(] SELECT field_list FROM first_layer [WHERE where_expr] [)]
    UNION ALL [(] SELECT field_list FROM second_layer [WHERE where_expr] [)]
    [UNION ALL [(] SELECT field_list FROM third_layer [WHERE where_expr] [)]]*

UNION ALL 제약 조건
++++++++++++++++++++++

OGR에서의 UNION ALL 처리 과정은 SELECT 문 여러 개로부터 동일하지 않은 열들을 입력받는다는 점에서 SQL 표준과 다릅니다. 이런 경우, 각 SELECT 문이 반환하는 모든 필드들의 총집합을 반환할 것입니다.

UNION의 결과물 수준에 대해서가 아니라 각 SELECT에 대해서만 ORDER BY를 지정할 수 있다는 제약 조건도 있습니다.

특수 필드
--------------

OGR SQL 처리기(processor)는 객체의 일부 속성을 다른 필드들과 마찬가지로 SQL 문에서 사용할 수 있는 내장 특수 필드로 취급합니다. 이런 특수 필드를 각각 선택 목록, WHERE 절, 그리고 ORDER BY 절에 넣을 수 있습니다. 기본적으로 특수 필드는 결과물에 포함되지 않지만, 특수 필드를 선택 목록에 추가해서 명확하게 포함시킬 수도 있습니다.

필드 값에 접근하는 경우 특수 필드가 데이터소스에 있는 같은 이름을 가진 다른 필드들보다 우선합니다.

FID
+++

객체ID는 일반적으로 객체의 특수 속성(property)으로, 객체 속성(attribute)으로 취급되지 않습니다. 쿼리에 객체ID를 활용해서 결과물을 정규 필드로 산출할 수 있다면 편리한 경우가 있습니다. 이렇게 하려면 ``FID`` 라는 이름을 사용하십시오. 필드 와일드카드 확장 사양은 객체ID를 포함하지 않지만, 다음과 같은 문법을 사용해서 명확하게 포함시킬 수도 있습니다:

.. code-block::

    SELECT FID, * FROM nation

도형 필드
++++++++++++++

OGR SQL 방언은 기본적으로 결과물에 데이터소스의 도형 필드를 추가합니다. 사용자가 도형 필드를 명확하게 선택할 필요는 없지만 그래도 선택할 수는 있습니다. 흔한 사용례는 도형 필드만 필요한 경우입니다. 이런 경우 SQL 문에 :cpp:func:`OGRLayer::GetGeometryColumn` 메소드가 반환하는 이름을 도형 필드의 이름으로 사용합니다. 이 메소드가 빈 문자열을 반환하는 경우 특수 이름 "_ogr_geometry_"를 사용해야만 합니다. 이름이 언더바로 시작하기 때문에 SQL 문법에 따라 이 이름을 큰따옴표로 감싸야만 합니다. 뿐만 아니라 명령줄 해석기가 큰따옴표를 이스케이프 처리할 것을 요구할 수도 있기 때문에, 최종 SELECT 문은 다음과 같이 보일 것입니다:

.. code-block::

    SELECT "_ogr_geometry_" FROM nation
    
OGR_GEOMETRY
++++++++++++

(MapInfo 탭 같은) 일부 데이터소스는 동일 레이어 안에서 서로 다른 유형의 도형을 처리할 수 있습니다. ``OGR_GEOMETRY`` 특수 필드가 :cpp:func:`OGRGeometry::getGeometryName` 메소드가 반환하는 도형 유형을 표현하고 다양한 도형 유형을 구별하는 데 사용될 수 있습니다. 이 필드를 이용하면 다음과 같이 특정 유형을 선택할 수 있습니다:

.. code-block::

    SELECT * FROM nation WHERE OGR_GEOMETRY='POINT' OR OGR_GEOMETRY='POLYGON'

OGR_GEOM_WKT
++++++++++++

도형의 WKT(Well Known Text) 표현을 특수 필드로도 사용할 수 있습니다. 도형의 WKT를 선택하려면 다음과 같이 선택 목록에 ``OGR_GEOM_WKT`` 를 포함시킬 수도 있습니다:

.. code-block::

    SELECT OGR_GEOM_WKT, * FROM nation

WHERE 절에 이 필드와 ``LIKE`` 연산자를 사용하면 OGR_GEOMETRY를 사용하는 것과 비슷한 결과를 얻을 수 있습니다:

.. code-block::

    SELECT OGR_GEOM_WKT, * FROM nation WHERE OGR_GEOM_WKT
    LIKE 'POINT%' OR OGR_GEOM_WKT LIKE 'POLYGON%'

OGR_GEOM_AREA
+++++++++++++

``OGR_GEOM_AREA`` 특수 필드는 :cpp:func:`OGRSurface::get_Area` 메소드가 계산한 객체의 도형 면적을 반환합니다. OGRGeometryCollection 및 OGRMultiPolygon 유형의 경우 해당 유형의 모든 멤버의 면적을 합한 값을 반환합니다. 면이 아닌 도형의 경우 반환되는 면적이 0.0입니다.

다음은 지정한 면적을 초과하는 폴리곤 객체만 선택하는 예시입니다:

.. code-block::

    SELECT * FROM nation WHERE OGR_GEOM_AREA > 10000000

OGR_STYLE
+++++++++

``OGR_STYLE`` 특수 필드는 :cpp:func:`OGRFeature::GetStyleString` 메소드가 반환하는 객체의 스타일 문자열을 표현합니다. 이 필드와 ``LIKE`` 연산자를 사용하면 쿼리 결과물을 스타일로 필터링할 수 있습니다. 다음은 주석 객체를 선택하는 예시입니다:

.. code-block::

    SELECT * FROM nation WHERE OGR_STYLE LIKE 'LABEL%'

CREATE INDEX
------------

몇몇 OGR SQL 드라이버는 속성 색인 생성을 지원합니다. 현재 Shapefile 드라이버가 이에 포함됩니다. 색인은 "fieldname = value" 형식의 아주 단순한 속성 쿼리의 속도를 향상시킵니다. ``JOIN`` 케이퍼빌리티가 이 색인을 사용합니다. "nation" 테이블의 "nation_id" 필드에 속성 색인을 생성하려면 다음과 같은 명령어를 사용할 것입니다:

.. code-block::

    CREATE INDEX ON nation USING nation_id

색인 제한 사항
+++++++++++++++++

- 레이어에 새 객체를 추가하거나 레이어로부터 객체를 제거할 때 색인을 동적으로 유지/관리하지 않습니다.

- 아주 긴 (문자 256개 길이를 넘는?) 문자열은 현재 색인 작업을 할 수 없습니다.

- 색인을 재생성하려면 레이어 상에 있는 모든 색인을 삭제한 다음 모든 색인을 재생성해야 합니다.

- 어떤 복잡 쿼리에서도 색인을 사용하지 않습니다. 현재 단순한 "field = value" 쿼리만 속도가 향상될 것입니다.

DROP INDEX
----------

OGR SQL DROP INDEX 명령어를 사용해서 특정 테이블에 있는 모든 색인을, 또는 특정 열의 색인만 삭제할 수 있습니다:

.. code-block::

    DROP INDEX ON nation USING nation_id
    DROP INDEX ON nation

ALTER TABLE
-----------

다음 OGR SQL ALTER TABLE 명령어들을 사용할 수 있습니다:

- ::

      ALTER TABLE tablename ADD [COLUMN] columnname columntype

  새 필드를 추가합니다. 레이어가 OLCCreateField 케이퍼빌리티를 선언하는 경우 지원합니다.

- ::

      ALTER TABLE tablename RENAME [COLUMN] oldcolumnname TO newcolumnname

  기존 필드를 재명명합니다. 레이어가 OLCAlterFieldDefn 케이퍼빌리티를 선언하는 경우 지원합니다.

- ::

      ALTER TABLE tablename ALTER [COLUMN] columnname TYPE columntype

  기존 필드의 유형을 변경합니다. 레이어가 OLCAlterFieldDefn 케이퍼빌리티를 선언하는 경우 지원합니다.

- ::

      ALTER TABLE tablename DROP [COLUMN] columnname

  기존 필드를 삭제합니다. 레이어가 OLCDeleteField 케이퍼빌리티를 선언하는 경우 지원합니다.

열 유형 값은 앞에서 설명한 CAST 연산자가 지원하는 유형들의 문법을 따릅니다:

.. code-block::

    ALTER TABLE nation ADD COLUMN myfield integer
    ALTER TABLE nation RENAME COLUMN myfield TO myfield2
    ALTER TABLE nation ALTER COLUMN myfield2 TYPE character(15)
    ALTER TABLE nation DROP COLUMN myfield2

DROP TABLE
----------

OGR SQL DROP TABLE 명령어를 사용해서 테이블을 삭제할 수 있습니다. ODsCDeleteLayer 케이퍼빌리티를 선언하는 데이터소스 상에서만 지원합니다.

.. code-block::

    DROP TABLE nation

ExecuteSQL()
------------

SQL은 특정 레이어가 아니라 GDALDataset을 대상으로 실행됩니다. 다음은 ExecuteSQL() 호출의 예시입니다:

.. code-block:: cpp

    OGRLayer * GDALDataset::ExecuteSQL( const char *pszSQLCommand,
                                        OGRGeometry *poSpatialFilter,
                                        const char *pszDialect );

``pszDialect`` 인자의 목적은 이론적으로 제공자에 대해 다른 명령어 언어를 지원할 수 있게 해주는 것이지만, 현재로서는 응용 프로그램이 기본 방언을 얻으려면 항상 비어 있는 (NULL이 아닌) 문자열을 전송해야 합니다.

``poSpatialFilter`` 인자는 :cpp:func:`OGRLayer::SetSpatialFilter` 메소드와 비슷한 방식으로 반환되는 객체의 경계 직사각형을 선택하기 위해 사용됩니다. 특수 공간 제약 조건이 없는 경우 경계 상자가 NULL일 수도 있습니다.

ExecuteSQL() 호출의 결과물은 일반적으로 SQL 선언문의 결과물을 표현하는 임시 OGRLayer입니다. 예를 들면 SELECT 문이 임시 OGRLayer를 반환합니다. 이 반환된 임시 레이어가 더 이상 필요없는 경우 :cpp:func:`GDALDataset::ReleaseResultsSet` 메소드로 해제해줘야 합니다. 데이터소스를 삭제하기 전에 임시 레이어를 해제하는 데 실패하면 크래시를 일으킬 수도 있습니다.

OGR가 아닌 SQL
--------------

데이터베이스 시스템 용 모든 OGR 드라이버는 -- :ref:`vector.mysql`, :ref:`vector.pg`, :ref:`vector.oci`, :ref:`vector.sqlite`, :ref:`vector.odbc`, :ref:`vector.pgeo`, :ref:`vector.hana` 및 :ref:`vector.mssqlspatial` 는 -- 전용 구현으로 :cpp:func:`GDALDataset::ExecuteSQL` 함수를 대체하고, 기본적으로 기저 RDBMS에 SQL 선언문을 직접 전송합니다.
이런 경우 SQL 문법이 몇 가지 세부 사항에서 OGR SQL과 달라집니다. 또한 SQL에서 가능한 모든 작업을 이런 특정 데이터베이스에 대해서도 할 수 있습니다. SQL WHERE 문의 결과물만 레이어로 반환할 것입니다.

