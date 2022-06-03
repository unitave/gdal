.. _rfc-52:

=======================================================================================
RFC 52: 엄격한 OGR SQL 인용
=======================================================================================

저자: 이벤 루올

연락처: even.rouault@spatialys.com

상태: 승인, GDAL 2.0버전에 구현

요약
----

이 RFC는 OGR SQL이 SQL 리터럴(literal) 및 식별자에 대해 엄격한 인용 규칙을 강제할 것을 제안합니다.

상세 사항
---------

현재 OGR SQL 엔진은 작은따옴표 문자(')와 큰따옴표 문자(")가 두 가지 서로 다른 맥락에서 사용될 수 있는데도 이 둘을 구분하지 않고 처리합니다:

-  문자열 리터럴 지정
-  열 또는 테이블 이름 지정 (인용이 필요한 경우)

SQL-92는 문자열 리터럴은 작은따옴표 문자로 감싸야 하는 반면 인용된 식별자(열 이름, 테이블 이름)은 큰따옴표 문자로 감싸야 한다고 규정합니다.

`https://github.com/ronsavage/SQL/blob/master/sql-92.bnf <https://github.com/ronsavage/SQL/blob/master/sql-92.bnf>`_ 에서:

::

   <delimited identifier>     ::= <double quote> <delimited identifier body> <double quote>
   <character string literal> ::= <quote> [ <character representation> ... ] <quote>

현재 OGR 습성은 SELECT 선언문 또는 WHERE 표현식에서 열을 지정하는 일부 상황을 제외하면 일반적으로 문제가 없습니다. OGR SQL 엔진은 다음 규칙으로 의도를 판단하려 시도합니다:

   -  인용된 문자열이 열 이름과 일치하는 경우 열 식별자로 가정하고, 일치하지 않으면 문자열 리터럴로 가정합니다. 그러나 가끔 (`https://trac.osgeo.org/gdal/ticket/5428 <https://trac.osgeo.org/gdal/ticket/5428>`_ 참조) ``"MyField" = 'MYFIELD'`` 같은 필터가 필요한 상황이 있으며, 현재로서는 항상 이런 필터들을 TRUE로 평가합니다.

모호함을 방지하고 SQL을 좀 더 준수하려면, 문자열 리터럴을 작은따옴표로 인용하고 식별자(열 이름, 테이블 이름)를 인용 처리하지 않거나 또는 예약된 키워드와 충돌하는 경우 큰따옴표 문자로 감싸야 합니다.

구현
----

이벤 루올(`Spatialys <http://www.spatialys.com>`_)이 이 RFC를 구현할 것입니다.

제안한 구현은 `"rfc52_stricter_sql" 브랜치 <https://github.com/rouault/gdal2/tree/rfc52_stricter_sql>`_ 저장소에 있습니다.

`변경 사항 목록 <https://github.com/rouault/gdal2/compare/rfc52_stricter_sql>`_

호환성
------

이 변경 사항은 현재의 관용적인 습성에 의존하는 사용자가 자신의 SQL 표현식을 수정해야 한다는 점에서 호환성에 영향을 미칩니다. 사용자가 수정하지 않는다고 해도 항상 명백한 런타임 실패를 발생시키지 않을 것이기 때문에 탐지하기가 아주 까다로울 수도 있습니다.
예를 들어 ``SELECT 'i_thought_this_would_be_interpreted_as_a_column_name_but_now_it_is_a_string_litteral' FROM a_table`` 이 오류 없이 실행될 것이지만 예전에 기대했던 결과물을 생성하지 않을 것입니다. 따라서 응용 프로그램이 어떻게 SQL 필터(SetAttributeFilter())와 표현식(ExecuteSQL())을 작성하는지 살펴봐야 할 것입니다.

이 엄격한 규칙을 준수하도록 수정된 표현식은 예전 GDAL 버전과도 작동할 것입니다.

습성이 변경되었음을 알리기 위해 OGR SQL 문서 페이지 상에도 눈에 띄는 경고를 넣어야 합니다.

논의
----

SQLite로 수행된 테스트는 SQLite가 인용 문자의 오용에 관대할 때도 있지만, 현재 OGR과는 반대의 방식으로 관대하다는 사실을 보여줍니다. 즉 ``SELECT "non_existing_column" FROM 'a_table'`` 을 받아들여 ``SELECT 'non_existing_column' FROM "a_table"`` 로 해석할 것입니다.
이와는 반대로, PostgreSQL은 ``SELECT "non_existing_column" FROM 'a_table'`` 을 받아들이지 않을 것입니다.
인용 규칙을 단순하고 이해하기 쉽게 유지하기 위해 PostgreSQL의 더 엄격한 접근법을 따를 것을 제안합니다:

.. quote::

   문자열 리터럴을 작은따옴표로 인용하고, 식별자(열 이름, 테이블 이름)를 인용 처리하지 않거나 또는 큰따옴표 문자로 감싸야 합니다.

테스트
------

파이썬 자동 테스트 스위트가 계속 통과하도록 수정할 것입니다.

투표 이력
---------

-  유카 라흐코넨 +1
-  세케레시 터마시 +1
-  대니얼 모리셋 +1
-  이벤 루올 +1

