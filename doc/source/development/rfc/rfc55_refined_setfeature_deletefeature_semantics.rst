.. _rfc-55:

=======================================================================================
RFC 55: SetFeature() 및 DeleteFeature() 의미 체계 개선
=======================================================================================

저자: 이벤 루올

연락처: even.rouault@spatialys.com

상태: 승인, GDAL 2.0버전에 구현

요약
----

이 RFC는 존재하지 않는 피처를 업데이트/삭제하려 시도하는 명목상의 경우와 존재하는 피처의 업데이트/삭제 실패를 구분할 수 있도록 SetFeature() 및 DeleteFeature() 의미 체계를 개선합니다.

근거
----

현재 드라이버에 따라 존재하지 않는 피처에 대해 SetFeature() 또는 DeleteFeature()를 호출하면 성공할 수도 있고 실패할 수도 있습니다. 대부분의 상황에서 이 함수들이 OGRERR_NONE 코드를 반환하는 것이 잘못된 입력이라는 신호일 수도 있기 때문에 일반적으로 바람직하지 않습니다. 따라서 드라이버가 호출 코드에 존재하지 않는 피처를 업데이트하거나 삭제하려고 시도했다는 사실을 알려줄 수 있도록 OGRERR_NON_EXISTING_FEATURE 반환 코드를 도입합니다.

변경 사항
---------

:file:`ogr_core.h` 에 ``#define OGRERR_NON_EXISTING_FEATURE 9`` 를 추가합니다.

업데이트된 드라이버
~~~~~~~~~~~~~~~~~~~

다음 드라이버들이 새로운 의미 체계를 구현하도록 업데이트합니다:

   -  PostgreSQL
   -  CartoDB
   -  SQLite
   -  GPKG
   -  MySQL
   -  OCI
   -  FileGDB
   -  Shapefile
   -  MITAB

메모: MSSQL 드라이버도 업데이트할 수 있습니다.

주의할 점
~~~~~~~~~

Shapefile 드라이버의 습성은 SetFeature() 구현이 삭제되었던 피처를 재생성하도록 허용한다는 점에서 조금 특별합니다. (그리고 이 드라이버의 CreateFeature() 구현은 새 피처를 추가하기 위해 전송된 피처에 설정된 모든 FID를 무시합니다.)
따라서 FID가 음의 값이거나 최대 피처 개수 이상인 경우에만 OGRERR_NON_EXISTING_FEATURE를 효과적으로 반환할 것입니다.

SWIG 바인딩 (파이썬 / 자바 / C# / 펄) 변경 사항
-----------------------------------------------

OGRERR_NON_EXISTING_FEATURE를 추가합니다.
파이썬 바인딩에 모든 ``OGRERR_xxxx`` 상수를 노출시킵니다.

유틸리티
--------

영향 없음.

문서화
------

SetFeature() 및 DeleteFeature() 문서에 새로운 오류 코드를 추가합니다.
:file:`MIGRATION_GUIDE.TXT` 에 다음 호환성 문제점 단락에 대한 언급을 추가합니다.

테스트 스위트
-------------

수정된 드라이버를 테스트하도록 테스트 스위트를 확장합니다.
:file:`test_ogrsf` 가 존재하지 않는 피처를 업데이트/삭제하는 드라이버의 습성도 테스트합니다.

호환성 문제점
-------------

존재하지 않는 피처를 업데이트 또는 삭제할 때 성공할 것으로 예상되는 코드를 업데이트해야 할 것입니다.

구현
----

이벤 루올(`Spatialys <http://spatialys.com>`_)이 `LINZ(Land Information New Zealand) <https://www.linz.govt.nz/>`_ 의 후원을 받아 이 RFC를 구현할 것입니다.

제안한 구현은 `"rfc55_refined_setfeature_deletefeature_semantics" 브랜치 <https://github.com/rouault/gdal2/tree/rfc55_refined_setfeature_deletefeature_semantics>`_ 저장소에 있습니다.
repository.

`변경 사항 목록 <https://github.com/rouault/gdal2/compare/rfc55_refined_setfeature_deletefeature_semantics>`_

투표 이력
---------

-  대니얼 모리셋 +1
-  하워드 버틀러 +1
-  유카 라흐코넨 +1
-  이벤 루올 +1

