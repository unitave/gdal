.. _rfc-67:

=======================================================================================
RFC 67 : OGR의 NULL 값
=======================================================================================

저자: 이벤 루올

연락처: even.rouault@spatialys.com

상태: 승인, GDAL 2.2버전에 구현

요약
----

이 RFC는 기존의 설정되지 않은 상태에 추가로 피처의 필드에 대한 NULL 값이라는 개념을 구현할 것을 제안합니다.

근거
----

현재 OGR는 필드 값이 누락되었는 사실을 나타내는 데 설정되지 않은(unset) 필드라는 하나의 단일 개념을 지원합니다.

따라서 각각 속성이 ``{ "foo": "bar" }`` 및 ``{ "foo": "bar", "other_field": null }`` 인 피처 2개를 가진 JSon 피처 선택 집합이 있다고 할 때, OGR는 현재 두 경우 모두 other_field가 설정되지 않은 상태라고 반환합니다.

여기에서 제안하는 것은 "other_field" 키워드가 완전히 생략된 첫 번째 경우 현재의 설정되지 않은 필드라는 개념을 사용하고, 두 번째 경우 NULL 필드라는 새로운 개념을 추가하자는 것입니다.

두 개념을 이렇게 구분하는 것은 모든 GeoJSON 기반 포맷 및 프로토콜에 적용되기 때문에, GeoJSON, ElasticSearch, MongoDB, CouchDB, Cloudant 드라이버에 영향을 미칩니다.

이 변경 사항은 GML에도 적용되어 누락된 요소라는 의미 체계는 설정되지 않은 필드에 매핑되고 ``xsi:nil="true"`` 속성을 가진 요소는 NULL 필드에 매핑될 것입니다.

변경 사항
---------

OGRField
~~~~~~~~

"raw field" 합집합에 있는 Set 구조를 수정해서 세 번째 마커를 추가합니다:

::

       struct {
           int     nMarker1;
           int     nMarker2;
           int     nMarker3;
       } Set;

이 수정 사항은 이 RFC와 직접적인 관련은 없지만 세 번째 마커가 실제 값이 설정되지 않은 상태 또는 NULL로 잘못 해석될 가능성을 줄여줍니다. 이 구조는 이미 최소 12바이트 용량이기 때문에 세 번째 마커를 추가해도 구조의 용량이 늘어나지는 않습니다.

이제 설정되지 않은 필드에 대해 마커 3개에 OGRUnsetMarker = -21121이라는 특수값이 설정될 것입니다. (현재로서는 처음 마커 2개에 설정되어 있습니다.)

새로운 NULL 상태에 대해서도 비슷하게 마커 3개에 OGRNullMarker = -21122라는 새 값이 설정될 것입니다.

OGRFeature
~~~~~~~~~~

``int IsFieldNull( int nFieldIdx )`` 과 ``void SetNullField( int nFieldIdx )`` 메소드를 추가합니다.

GetFieldXXXX() 접근자들이 설정되지 않은 필드에 대해 호출되는 경우와 동일한 방식으로 NULL인 경우를 고려하도록 수정합니다. 즉 숫자 필드 유형에 대해 0을, 문자열 필드 유형에 대해 비어 있는 문자열을, 날짜&시간 필드 유형에 대해 FALSE를, 그리고 목록 기반 필드 유형에 대해 NULL을 반환하도록 수정합니다.

:cpp:func:`OGRFeature::IsFieldSetAndNotNull` 편이(convenience) 메소드를 추가해서 예전에 IsFieldSet()을 사용했고 설정되지 않은 상태와 NULL 상태를 구분할 필요가 없는 기존 코드의 포팅을 쉽게 수행할 수 있도록 합니다.

C API
-----

다음 함수들을 추가할 것입니다:

::


   int    CPL_DLL OGR_F_IsFieldNull( OGRFeatureH, int );
   void   CPL_DLL OGR_F_SetFieldNull( OGRFeatureH, int );

   int    CPL_DLL OGR_F_IsFieldSetAndNotNull( OGRFeatureH, int );

마커를 직접 테스트/설정하는 대신 (대부분 GDAL 코어 및 몇몇 드러이버에서 사용하기 위해) "raw field" 합집합을 직접 조작하기 위한 저수준 함수들을 추가할 것입니다:

::

   int    CPL_DLL OGR_RawField_IsUnset( OGRField* );
   int    CPL_DLL OGR_RawField_IsNull( OGRField* );
   void   CPL_DLL OGR_RawField_SetUnset( OGRField* );
   void   CPL_DLL OGR_RawField_SetNull( OGRField* );

SWIG 바인딩 (파이썬 / 자바 / C# / 펄) 변경 사항
-----------------------------------------------

SWIG에 새 메소드들을 매핑할 것입니다.

드라이버
--------

다음 드라이버들이 설정되지 않은 상태와 NULL 상태를 개별적인 상태로 연산에 넣도록 수정할 것입니다:

   -  GeoJSON
   -  ElasticSearch
   -  MongoDB
   -  CouchDB
   -  Cloudant
   -  GML
   -  GMLAS
   -  WFS

주의: GMLAS 드라이버와 관련해서, xxxx가 NULL로 설정할 수 있는 선택적인 XML 요소인 경우 xxxx 및 xxxx_nil 필드를 둘 다 가질 수 있는 예전 습성을 기본적으로 보전합니다. (:file:`gmlasconf.xml` 파일에 있는 환경설정을 통해 변경할 수 있습니다.) 그 근거는 GMLAS 드라이버가 설정되지 않은 상태와 NULL 상태를 구분하지 못 하는 SQL 지원 포맷으로 변환시키는 데 주로 사용되기 때문에 전용 필드 2개가 필요하다는 사실입니다.

EMPTY_STRING_AS_NULL 열기 옵션이 지정된 경우 CSV 드라이버가 새로운 NULL 상태를 사용하도록 수정할 것입니다.

쓰기 쪽에서 소스 피처가 설정되지 않은 필드를 가지고 있는지 테스트하는 모든 드라이버가 필드가 NULL인지도 테스트할 것입니다.

SQL 기반 (PG, PGDump, Carto, MySQL, OCI, SQLite, GPKG) 드라이버의 경우 읽기 시 SQL NULL 값을 새로운 NULL 상태로 매핑할 것입니다.
쓰기 시, 대응하는 INSERT 또는 UPDATE 문에서 설정되지 않은 필드를 언급하지 않는 반면 NULL 필드는 언급하고 NULL로 설정할 것입니다.
삽입 시, 필드 상에 기본값을 정의하지 않는 이상 일반적으로 습성에 차이점은 없을 것입니다. 필드 상에 기본값이 정의되었다면 데이터베이스가 설정되지 않은 상태에 값을 설정하기 위해 기본값을 사용할 것입니다.
업데이트 시, 설정되지 않은 필드가 데이터베이스가 업데이트하는 자신의 내용을 인식하지 못 하는 반면 NULL로 설정된 필드는 NULL로 업데이트될 것입니다.

유틸리티
--------

직접적인 변경 사항은 없지만, :cpp:func:`OGRFeature::DumpReadable` 메소드가 피처의 설정되지 않은 필드를 더 이상 표시하지 않도록 수정하기 때문에 ogrinfo의 산출물이 영향을 받을 것입니다.

문서화
------

새 메소드 및 함수를 모두 문서화합니다.

테스트 스위트
-------------

GDAL 코어 변경 사항 및 업데이트된 드라이버들을 테스트할 것입니다.

호환성 문제점
-------------

GDAL 소스 코드와 GDAL이 호출하는 외부 코드에서 현재 OGRFeature::IsFieldSet() / OGR_F_IsFieldSet()를 사용하는 모든 코드도 설정되지 않은 상태인 경우와 정확하게 일치하게 동작하도록 또는 새로운 적절한 습성을 추가하도록 IsFieldNull() / OGR_F_IsFieldNull()을 사용하게 업데이트해야 합니다.
기존 코드의 포팅을 쉽게 해주는 OGRFeature::IsFieldSetAndNotNull() / OGR_F_IsFieldSetAndNotNull() 편이 메소드 및 함수를 추가합니다.

이렇게 하는 데 실패한다면, 기존 코드가 숫자 필드 유형에 대해 0을, 문자열 필드 유형에 대해 비어 있는 문자열을, 날짜&시간 필드 유형에 대해 FALSE를, 그리고 목록 기반 필드 유형에 대해 NULL을 보게 될 것입니다.

GDAL 2.1 이전 버전들에서 GeoJSON 드라이버의 경우 쓰기 쪽에서는 설정되지 않은 필드를 ``field_name: null`` 로 작성했습니다. GDAL 2.2버전부터, OGR_F_SetFieldNull()로 명확하게 NULL로 설정된 필드만 NULL 값으로 작성할 것입니다. 피처의 설정되지 않은 필드에 대응하는 JSon 피처 요소는 존재하지 않을 것입니다.

이런 호환성 문제점들을 논의하기 위해 :file:`MIGRATION_GUIDE.TXT` 를 업데이트합니다.

관련 티켓
---------

없음

구현
----

이벤 루올(`Spatialys <http://spatialys.com>`_)이 `세이프 소프트웨어 <https://www.safe.com/>`_ 의 후원을 받아 이 RFC를 구현할 것입니다.

제안한 구현은 `"rfc67" 브랜치 <https://github.com/rouault/gdal2/tree/rfc67>`_ 에 있습니다.


투표 이력
---------

-  유카 라흐코넨 +1
-  대니얼 모리셋 +1
-  하워드 버틀러 +1
-  이벤 루올 +1

