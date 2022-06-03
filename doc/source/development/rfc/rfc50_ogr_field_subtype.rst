.. _rfc-50:

=======================================================================================
RFC 50: OGR 필드 하위 유형
=======================================================================================

저자: 이벤 루올

연락처: even.rouault@spatialys.com

상태: 승인, GDAL 2.0버전에 구현

요약
-------

이 RFC의 목적은 OGR 필드에 불(boolean), 16비트 정수형 또는 32비트 부동소수점형 값 같은 하위 유형들을 지정하는 케이퍼빌리티를 추가하는 것입니다. 필드 정의 하위 유형은 주요 유형들에 힌트 또는 제약 조건을 지정하는 추가적인 속성입니다. 이런 하위 유형을 어떻게 처리하는지 알고 있는 응용 프로그램 및 드라이버가 하위 유형을 사용할 수 있으며, 알지 못 하는 응용 프로그램 및 드라이버는 일반적으로 안전하게 무시할 수 있습니다.

핵심 변경 사항
--------------

필드 하위 유형
~~~~~~~~~~~~~~

OGRFieldSubType 열거형을 추가합니다:

::

   /**
    * 필드 하위 유형 목록입니다. 하위 유형은 주요 유형의 굳이 참고할 필요는 없는
    * 힌트, 제약 조건을 표현합니다.
    * 이 목록은 향후 확장될 가능성이 큽니다. 모든 필드 유형을 알 수 있다는 가정을
    * 기반으로 응용 프로그램을 코딩하지 마십시오.
    * 하위 유형 대부분은 주요 유형들의 제한된 집합에 대해서만 의미가 있습니다.
    * @since GDAL 2.0
    */
   typedef enum
   {
       /** 하위 유형 없음. 기본값입니다. */                OFSTNone = 0,
       /** 불 정수형입니다. OFTInteger 및 OFTIntegerList에 대해서만 무결합니다. */
                                                           OFSTBoolean = 1,
       /** 부호 있는 16비트 정수형입니다. OFTInteger 및 OFTIntegerList에 대해서만 무결합니다. */
                                                           OFSTInt16 = 2,
       /** 단정밀도 (32비트) 부동소수점형입니다. OFTReal 및 OFTRealList에 대해서만 무결합니다. */
                                                           OFSTFloat32 = 3,
                                                           OFSTMaxSubType = 3
   } OGRFieldSubType;

새로운 속성 및 메소드
~~~~~~~~~~~~~~~~~~~~~

-  :cpp:class:`OGRFieldDefn` 클래스에 다음을 추가합니다:

::

       OGRFieldSubType     eSubType;

       OGRFieldSubType     GetSubType() { return eSubType; }
       void                SetSubType( OGRFieldSubType eSubTypeIn );
       static const char  *GetFieldSubTypeName( OGRFieldSubType );

:cpp:func:`OGRFeature::SetField` 가 전송된 값이 불 및 16비트 정수형 하위 유형의 허용 범위 안에 들어가는지 확인할 것입니다. 들어가지 않는 경우, 경고를 발하고 하위 유형에 맞게 값을 수정/고정할 것입니다.

C API 변경 사항
~~~~~~~~~~~~~~~

다음 내용만 추가합니다:

::

   OGRFieldSubType CPL_DLL OGR_Fld_GetSubType( OGRFieldDefnH );
   void   CPL_DLL OGR_Fld_SetSubType( OGRFieldDefnH, OGRFieldSubType );
   const char CPL_DLL *OGR_GetFieldSubTypeName( OGRFieldSubType );
   int CPL_DLL OGR_AreTypeSubTypeCompatible( OGRFieldType eType,
                                             OGRFieldSubType eSubType );

OGR SQL 변경 사항
-----------------

-  SELECT의 필드 목록에 필드명(또는 "\*")을 지정한 경우 하위 유형을 보전합니다.

-  이제 ``CAST(xxx AS BOOLEAN)`` 및 ``CAST(xxx AS SMALLINT)`` 을 지원합니다.

-  SELECT의 필드 목록이 이제 ``SELECT x IS NULL, x >= 5 FROM foo`` 같은 불 표현식을 받아들일 수 있습니다.

-  SELECT의 WHERE 절이 이제 ``SELECT * FROM foo WHERE a_boolean_field`` 처럼 불 필드를 받아들일 수 있습니다.

드라이버 변경 사항
------------------

-  GeoJSON: OFSTBoolean을 읽고 쓸 수 있습니다.

-  GML: OFSTBoolean, OFSTInt16 및 OFSTFloat32를 읽고 쓸 수 있습니다.

-  CSV: (명확하게 CSVT로 또는 자동 탐지로) OFSTBoolean, (명확하게 CSVT로) OFSTInt16 및 OFSTFloat32를 읽고 쓸 수 있습니다.

-  PG: OFSTBoolean, OFSTInt16 및 OFSTFloat32를 읽고 쓸 수 있습니다.

-  PGDump: OFSTBoolean, OFSTInt16 및 OFSTFloat32를 쓸 수 있습니다.

-  GeoPackage: OFSTBoolean, OFSTInt16 및 OFSTFloat32를 읽고 쓸 수 있습니다.

-  SQLite: OFSTBoolean and OFSTInt16를 읽고 쓸 수 있습니다.

-  SQLite 방언: OFSTBoolean, OFSTInt16 및 OFSTFloat32를 읽고 쓸 수 있습니다.

-  FileGDB: OFSTInt16 및 OFSTFloat32를 읽고 쓸 수 있습니다.

-  OpenFileGDB: OFSTInt16 및 OFSTFloat32를 읽을 수 있습니다.

-  VRT: 모든 하위 유형을 처리할 수 있도록 'subtype' 속성을 추가했습니다.

유틸리티 변경 사항
------------------

-  ogrinfo:
   하위 유형이 존재하는 경우 ogrinfo의 산출물이 약간 수정됩니다. 기본값이 아닌 하위 유형을 가진 필드를 "field_type(field_subtype)"으로 서술할 것입니다. 다음은 그 예시입니다.

::

   Had to open data source read-only.
   INFO: Open of `out.gml'
         using driver `GML' successful.

   Layer name: test
   Geometry: None
   Feature Count: 2
   Layer SRS WKT:
   (unknown)
   short: Integer(Int16) (0.0)
   b: Integer(Boolean) (0.0)
   OGRFeature(test):0
     short (Integer(Int16)) = -32768
     b (Integer(Boolean)) = 1

SWIG 바인딩 변경 사항
---------------------

다음을 추가합니다:

-  ogr.OFSTNone, ogr.OFSTBoolean, ogr.OFSTInt16 및 ogr.OFSTFloat32
-  ogr.GetFieldSubTypeName()
-  FieldDefn.GetSubType()
-  FieldDefn.SetSubType()

호환성
------

이 변경 사항들은 응용 프로그램이 수행하는 읽기 전용 작업에 어떤 영향도 미치지 않습니다.
하위 유형의 범위를 벗어나는 값을 작성하는 경우 업데이트 작업이 영향을 받을 수 있습니다. (그러나 이런 습성은 아마도 벌써 백엔드가 무시하거나 경고를 발하는 문제점을 발생시켰을 것입니다.)

문서화
------

새로운 메소드들을 모두 문서화합니다.
필요한 경우 드라이버 문서를 업데이트합니다.

테스트
------

이 RFC의 여러 측면을 테스트합니다:

-  핵심 변경 사항
-  OGR SQL 변경 사항
-  드라이버 변경 사항

구현
----

이벤 루올이 `CartoDB <https://cartodb.com>`_ 의 후원을 받아 이 RFC를 구현할 것입니다.

제안한 구현은 `"ogr_field_subtype" 브랜치 <https://github.com/rouault/gdal2/tree/ogr_field_subtype>`_ 저장소에 있습니다.

`변경 사항 목록 <https://github.com/rouault/gdal2/compare/ogr_field_subtype>`_

투표 이력
---------

-  유카 라흐코넨 +1
-  세케레시 터마시 +1
-  프랑크 바르메르담 +1
-  이벤 루올 +1

