.. _rfc-31:

================================================================================
RFC 31: OGR 64비트 정수형 필드 및 FID
================================================================================

저자: 프랑크 바르메르담, 이벤 루올

연락처: warmerdam@pobox.com, even dot rouault at spatialys.com

상태: 승인, GDAL 2.0버전에 구현

요약
----

이 RFC는 OGR가 64비트 정수형 필드 및 피처ID를 지원하도록 업그레이드하기 위한 단계를 제시합니다. 피처 데이터 포맷 다수가 확장 정수형(wide integer)을 지원하는데, OGR를 통해 이를 변환할 수 없기 때문에 발생하는 문제들이 늘어나고 있습니다.

.. _64bit-fid-feature-index-and-feature-count:

64비트 FID, 피처 색인 및 피처 개수
----------------------------------

내부적으로 피처ID를 "long"이 아니라 "GIntBig" 유형으로 처리할 것입니다. :cpp:class:`OGRFeature` 의 nFID 필드도 마찬가지입니다. :cpp:class:`OGRFeature` 에 있는 기존 GetFID() 및 SetFID() 메소드는 "long" 유형을 사용하는데, 대신 "GIntBig" 유형을 반환하도록 (그리고 입력받도록) 변경합니다. GetFID()의 반환 유형을 변경하려면 (예를 들어 printf 같은 표현식에 GetFID()를 사용하는 경우) 잠재적인 문제점을 피하도록 응용 프로그램 코드를 조심해서 조정해야 할 것입니다. SetFID() 변경은 대부분 직관적일 것입니다. 따라서 :cpp:class:`OGRFeature` 클래스의 변경 사항은 다음과 같습니다:

.. code-block:: cpp

     GIntBig  GetFID();
     OGRErr   SetFID(GIntBig nFID );

C API 수준에서는 다음과 같습니다:

.. code-block:: c

     GIntBig CPL_DLL OGR_F_GetFID( OGRFeatureH );
     OGRErr CPL_DLL OGR_F_SetFID( OGRFeatureH, GIntBig );

"long" 유형을 사용하는 예전 인터페이스가 (64비트 빌드 상에서도 "long" 유형이 32비트인 윈도우 대상 컴파일러를 제외한) 64비트 운영 체제 상에서 이미 64비트라는 사실을 기억하십시오. 따라서 응용 프로그램이 64비트 운영 체제 상에서 이런 인터페이스를 계속 사용해도 괜찮습니다.

64비트 FID를 가진 피처를 담고 있다는 사실을 비교적 리소스가 들지 않는 방식으로 발견할 수 있는 레이어는 OLMD_FID64 메타데이터 항목을 YES로 노출시켜야 ogr2ogr가 FID64 생성 옵션을 지원하는 드라이버에 FID64를 전송할 수 있습니다.


:cpp:class:`OGRLayer` 클래스는 몇 가지 FID 기반 작업을 할 수 있습니다. 이런 작업들의 서명(signature)을 '수정'해서 "long" 대신 "GIntBig" 유형을 입력받게 할 것입니다. "long"을 손실 없이 "GIntBig"으로 변환할 수 있기 때문에, 이론적으로는 응용 프로그램 코드를 하나도 변경하지 않아도 될 것입니다. 하지만 모든 기존 OGR 드라이버는 물론 상용 드라이버도 변경해야 합니다. 이렇게 되면 C ABI에 하위 호환되지 않는 변경 사항이 생기게 됩니다. 
하는 김에, (현재 32비트 정수형을 반환하는) :cpp:func:`GetFeatureCount` 가 20억개 이상의 레코드를 반환할 수 있게, 즉 "GIntBig" 유형을 반환하도록 하고자 합니다. 마찬가지로 GetFID()에도 이런 반환 유형 변경을 적용하는 경우 응용 프로그램 코드에 주의를 기울여야 합니다.

따라서 :cpp:class:`OGRLayer` 클래스 수준에서 다음과 같이 변경하고:

.. code-block:: cpp

       virtual OGRFeature *GetFeature( GIntBig nFID );
       virtual OGRErr      DeleteFeature( GIntBig nFID );
       virtual OGRErr      SetNextByIndex( GIntBig nIndex );
       virtual GIntBig     GetFeatureCount( int bForce = TRUE );

C API 수준에서는 다음과 같이 변경합니다:

.. code-block:: c

     OGRFeatureH CPL_DLL OGR_L_GetFeature( OGRLayerH, GIntBig );
     OGRErr CPL_DLL OGR_L_DeleteFeature( OGRLayerH, GIntBig );
     OGRErr CPL_DLL OGR_L_SetNextByIndex( OGRLayerH, GIntBig );
     GIntBig CPL_DLL OGR_L_GetFeatureCount( OGRLayerH, int );

.. _64bit-fields:

64비트 필드
-----------

64비트 정수형을 위한 새 필드 유형을 도입할 것입니다:

.. code-block:: cpp

      OFTInteger64 = 12
      OFTInteger64List = 13

:cpp:class:`OGRField` 합집합(union)이 다음을 포함하도록 확장할 것입니다:

.. code-block:: cpp

       GIntBig     Integer64;
       struct {
           int nCount;
           GIntBig *paList;
       } Integer64List;

:cpp:class:`OGRFeature` 클래스를 다음 새 메소드들로 확장할 것입니다:

.. code-block:: cpp

       GIntBig             GetFieldAsInteger64( int i );
       GIntBig             GetFieldAsInteger64( const char *pszFName );
       const int          *GetFieldAsInteger64List( const char *pszFName,
                                                  int *pnCount );
       const int          *GetFieldAsInteger64List( int i, int *pnCount );

       void                SetField( int i, GIntBig nValue );
       void                SetField( int i, int nCount, const GIntBig * panValues );
       void                SetField( const char *pszFName, GIntBig nValue )
       void                SetField( const char *pszFName, int nCount,
                                     const GIntBig * panValues )

C 수준에서는, 다음 함수들을 추가합니다:

.. code-block:: c

       GIntBig CPL_DLL OGR_F_GetFieldAsInteger64( OGRFeatureH, int );
       const GIntBig CPL_DLL *OGR_F_GetFieldAsInteger64List( OGRFeatureH, int, int * );
       void   CPL_DLL OGR_F_SetFieldInteger64( OGRFeatureH, int, GIntBig );
       void   CPL_DLL OGR_F_SetFieldInteger64List( OGRFeatureH, int, int, const GIntBig * );

뿐만 아니라 새 인터페이스는 내부적으로 정수형 필드 설정하기/가져오기를 지원하고 정수형 필드 메소드는 64비트 정수형 필드 가져오기/설정하기를 지원할 것이기 때문에 ("Integer64List" 유형 필드에서만 작업할 수 있는 :cpp:func:`GetFieldAsInteger64List` 를 제외하고) 편리한 경우 두 필드 유형에 하나의 유형을 사용할 수 있습니다.

``GDAL_DMD_CREATIONFIELDDATATYPES = "DMD_CREATIONFIELDDATATYPES"`` 드라이버 메타데이터 항목을 추가해서 드라이버가 생성 작업 시 지원하는 필드 유형을 -- 예를 들어 "Integer Integer64 Real String Date DateTime Time IntegerList Integer64List RealList StringList Binary"처럼 -- 선언할 수 있게 합니다. 자주 쓰이는 드라이버들이 이렇게 선언할 수 있도록 업데이트할 것입니다.

OGR SQL
-------

"SWQ_INTEGER64" 내부 유형을 추가해서 "OFTInteger64" 유형 필드를 매핑할 수 있고 매핑될 수 있게 합니다. 'swq_expr_node' 클래스의 'int_value' 멤버를 "int"로부터 "GIntBig" 유형으로 확장합니다. (따라서 SWQ_INTEGER 및 SWQ_INTEGER64 둘 다 해당 멤버를 참조합니다.)

.. _python--java--c--perl-changes:

파이썬 / 자바 / C# / 펄 변경 사항
---------------------------------

다음과 같이 변경했습니다:

-  GetFID(), GetFeatureCount()가 64비트 정수형을 반환하도록 변경했습니다.
-  SetFID(), GetFeature(), DeleteFeature(), SetNextByIndex()가 64비트 정수형을 인자로 입력받을 수 있도록 변경했습니다.
-  GetFieldAsInteger64() 및 SetFieldInteger64()를 추가했습니다.
-  파이썬에서, GetField(), SetField()가 64비트 값을 입력받고 반환할 수 있습니다.
-  GetFieldAsInteger64List() 및 SetFieldInteger64List()를 추가했습니다.
   (다른 언어에 대한 유형 매핑(typemap)이 부족하기 때문에 파이썬만 해당하지만, 다른 언어에 대해서도 가능하긴 합니다.)

GetFID() 및 GetFeatureCount() 의 반환 유형을 변경했기 때문에 몇몇 언어에서 컴파일 작업 시 경고를 발할 수도 있습니다. (자바에서는 경고를 발하고, 파이썬은 관련없으며, 펄/C#에서는 불확실합니다.)
자바 바이트코드의 경우 기존 메소드의 모든 변경 사항들이 ABI에 적용될 것입니다.

유틸리티
--------

ogr2ogr 및 ogrinfo가 새로운 64비트 인터페이스를 지원하도록 업데이트합니다.

ogr2ogr에 새 옵션 ``-mapFieldType`` 을 추가합니다. ``-mapFieldType Integer64=Integer,Date=String`` 처럼 사용할 수 있습니다. 소스 레이어의 "Integer64" 유형 필드를 "Integer" 유형으로, 그리고 "Date" 유형 필드를 "String" 유형으로 생성해야 한다는 의미입니다. ogr2ogr는 GDAL_DMD_CREATIONFIELDDATATYPES 메타데이터 항목에 필요한 필드 유형이 지정되지 않았다는 사실을 노출시키는 산출 드라이버에서 필드를 생성하려 시도하는 경우에도 경고를 발할 것입니다. "Integer64" 유형 필드의 경우 GDAL_DMD_CREATIONFIELDDATATYPES 메타데이터 항목에 필요한 필드 유형이 지정되지 않았다면 또는 GDAL_DMD_CREATIONFIELDDATATYPES 메타데이터 항목이 생략되었다면 기본적으로 경고를 발하면서 "Real" 유형으로 변환합니다. ogr2ogr는 OLMD_FID64 메타데이터 항목이 선언되었는지 그리고 산출 드라이버가 FID64 레이어 생성 옵션을 가지고 있는지를 확인하기 위해 소스 레이어도 쿼리할 것입니다. 소스 레이어에 OLMD_FID64 메타데이터 항목이 선언되어 있고 산출 드라이버가 FID64 레이어 생성 옵션을 가지고 있다면 해당 옵션을 설정할 것입니다.

문서화
------

새로운 또는 수정된 API를 문서화합니다. 드라이버에 새로운 옵션 또는 습성으로 업데이트된 사항도 문서화합니다. :file:`MIGRATION_GUIDE.TXT` 에 이 RFC와 관련된 부분을 추가하고 OGR API를 업데이트합니다.

파일 포맷
---------

적절한 경우, 기존 OGR 드라이버가 새로운 또는 업데이트된 인터페이스를 지원할 수 있도록 업데이트했습니다. 특히 64비트 정수형 열을 피처ID로 사용할 수 있게 지원할 수 있도록 몇몇 데이터베이스 드라이버를 업데이트하는 데 노력을 기울였지만, 이 드라이버들은 기본적으로 새 레이어 생성 시 FID 열을 항상 64비트로 생성하지 않습니다. 다른 응용 프로그램들과 호환성 문제를 일으킬 수도 있기 때문입니다.

다음은 인터페이스 변경으로 인한 기계적인 변경 사항을 제외한 변경 사항들의 상세 목록입니다:

-  Shapefile:
   분명하게 "OFTInteger"로 읽을 수 있도록 "OFTInteger" 유형 필드를 문자 9개 길이로 생성합니다. (문자 10개 또는 11개 길이가 필요한 정수형을 지정하는 경우 몇몇 버전들부터 관리하는 대로 필드가 동적으로 확장됩니다.) 분명하게 "OFTInteger64"로 읽을 수 있도록 "OFTInteger64" 유형 필드를 문자 18개 길이로 생성하고, 필요한 경우 19개 또는 20개 길이로 확장합니다. 정수형 필드의 길이가 문자 10개에서 18개 사이인 경우 "OFTInteger64" 유형으로 읽을 것입니다. 필드 길이가 문자 19개 이상이라면 "OFTReal" 유형으로 취급할 것입니다.
   예전 GDAL 버전들에서는 정수형 필드를 문자 10개 기본값 길이로 생성했기 때문에, 이제는 "OFTInteger64" 유형으로 읽을 것입니다. OGR가 DBF 파일을 전체 스캔해서 길이가 문자 10개 또는 11개인 정수형 필드가 32비트 값을 담고 있는지 64비트 값을 담고 있는지 확인하고 그에 따라 유형을 조정하게 하려면 ADJUST_TYPE 열기 옵션을 YES로 지정하면 됩니다. (길이가 문자 19개 또는 20개인 정수형 필드에 대해서도 동일합니다. 64비트 정수형의 오버플로가 발생한다면 "OFTReal" 유형을 선택합니다.)

-  PG:
   "OFTInteger64" 유형을 "INT8"로 그리고 "OFTInteger64List" 유형을 "bigint[]"로 읽고 생성하도록 업데이트합니다. 64비트 FID를 지원합니다. 기본적으로 레이어 생성 시 호환성 문제점을 피하기 위해 FID 필드를 SERIAL(32비트 정수형)로 생성합니다. FID 필드를 SERIAL 대신 BIGSERIAL로 생성하려면 ``FID64=YES`` 생성 옵션을 전송하면 됩니다. 필요한 경우, 드라이버가 스키마를 동적으로 수정해서 32비트 정수형 FID 필드를 64비트 정수형으로 확장할 것입니다.
   GetFeatureCount() 메소드가 64비트 값을 반환하도록 수정합니다. FID 열이 64비트인 경우 즉시 ``OLMD_FID64 = "YES"`` 를 노출시킵니다.

-  PGDump:
   읽기/쓰기 작업 시 "Integer64", "Integer64List" 유형 및 64비트 FID를 지원하도록 업데이트합니다. ``FID64=YES`` 생성 옵션을 사용할 수 있습니다.

-  GeoJSON:
   읽기/쓰기 작업 시 "Integer64", "Integer64List" 유형 및 64비트 FID를 지원하도록 업데이트합니다. 필요한 경우에만 64비트 변이형을 리포트하고, 그렇지 않은 경우 "OFTInteger"/"OFTIntegerList" 유형을 사용합니다. 필요한 경우 ``OLMD_FID64 = "YES"`` 를 노출시킵니다.

-  CSV:
   읽기/쓰기 작업 시 "Integer64" 유형을 지원하도록 업데이트합니다. 필드 유형 자동탐지 기능을 추가합니다.

-  GPKG:
   읽기/쓰기 작업 시 "Integer64" 유형 및 64비트 FID를 지원하도록 업데이트합니다. 지오패키지 사양을 준수하여 "INT" 또는 "INTEGER" 유형 열을 64비트로 간주하지만 "MEDIUMINT" 유형은 32비트로 간주합니다.
   "MAX(fid_column)" 유형이 64비트인 경우 즉시 ``OLMD_FID64 = "YES"`` 를 노출시킵니다.
   GetFeatureCount() 메소드가 64비트 값을 반환하도록 수정합니다.

-  SQLite:
   읽기/쓰기 작업 시 "Integer64" 유형 및 64비트 FID를 지원하도록 업데이트합니다. 쓰기 작업의 경우 "Integer64" 유형을 "BIGINT"로 생성하고 읽기 작업의 경우 "BIGINT" 또는 "INT8"를 "Integer64" 유형으로 간주합니다. 하지만 다른 도구로 생성한 데이터베이스가 "INTEGER" 유형으로 생성되었지만 64비트 값을 담고 있을 가능성도 있습니다. 이런 경우 OGR가 64비트 값을 탐지하지 못 할 것입니다. 이 문제점을 피하려면 ``OGR_PROMOTE_TO_INTEGER64=YES`` 환경설정 옵션을 전송하면 됩니다.
   "MAX(fid_column)" 유형이 64비트인 경우 즉시 ``OLMD_FID64 = "YES"`` 를 노출시킵니다.
   GetFeatureCount() 메소드가 64비트 값을 반환하도록 수정합니다.

-  MySQL:
   읽기/쓰기 작업 시 "Integer64" 유형 및 64비트 FID를 지원하도록 업데이트합니다. PG 드라이버와 마찬가지로 FID64 생성 옵션을 YES로 지정하지 않는 이상 기본적으로 FID 열을 32비트로 생성합니다.
   FID 열이 64비트인 경우 즉시 ``OLMD_FID64 = "YES"`` 를 노출시킵니다.
   GetFeatureCount() 메소드가 64비트 값을 반환하도록 수정합니다.

-  OCI:
   읽기/쓰기 작업 시 "Integer64" 유형 및 64비트 FID를 지원하도록 업데이트합니다. 읽기 작업 시 "Integer"/"Integer64" 유형을 탐지하는 것이 어려울 수도 있습니다. 필드 길이에 "NUMBER" SQL 유형만 사용하기 때문입니다. 길이가 문자 9개 이하 또는 지정되지 않은 값(38)인 경우 "Integer" 유형으로 간주합니다. 생성 작업 시 OGR가 "OFTInteger64" 유형을 문자 20개 길이로 설정할 것이기 때문에, 소수점 이하 부분이 없고 길이가 문자 20개인 "NUMBER"를 "Integer64" 유형으로 간주할 것입니다.

-  MEM:
   읽기/쓰기 작업 시 "Integer64" 유형 및 64비트 FID를 지원하도록 업데이트합니다.
   GetFeatureCount() 메소드가 64비트 값을 반환하도록 수정합니다.

-  VRT:
   읽기/쓰기 작업 시 "Integer64", "Integer64List" 유형 및 64비트 FID를 지원하도록 업데이트합니다.
   GetFeatureCount() 메소드가 64비트 값을 반환하도록 수정합니다.

-  JML:
   생성 작업 시 "Integer64" 유형을 ("OBJECT"로 생성해서) 지원합니다. 읽기 작업 시 "String" 유형으로 반환합니다.

-  GML:
   읽기/쓰기 작업 시 "Integer64", "Integer64List" 유형 및 64비트 FID를 지원하도록 업데이트합니다.
   GetFeatureCount() 메소드가 64비트 값을 반환하도록 수정합니다.

-  WFS:
   읽기/쓰기 작업 시 "Integer64", "Integer64List" 유형 및 64비트 FID를 지원하도록 업데이트합니다.
   GetFeatureCount() 메소드가 64비트 값을 반환하도록 수정합니다.

-  CartoDB:
   생성 작업 시 "Integer64" 유형을 지원하도록 업데이트합니다. 읽기 작업 시 "Real" 유형으로 반환합니다. (CartoDB 드라이버는 "Number" 유형만 노출시킵니다.)
   GetFeatureCount() 메소드가 64비트 값을 반환하도록 수정합니다.

-  XLSX:
   읽기/쓰기 작업 시 "Integer64" 유형을 지원하도록 업데이트합니다.

-  ODS:
   읽기/쓰기 작업 시 "Integer64" 유형을 지원하도록 업데이트합니다.

-  MSSQLSpatial:
   GetFeatureCount() 메소드가 64비트 값을 반환하도록 수정합니다. 가능하긴 하지만 "Integer64" 유형 지원을 구현하지 않습니다.

-  OSM:
   이제 ``sizeof(long) != 8`` 인 경우에도 항상 FID를 설정하도록 업데이트합니다.

-  LIBKML:
   KML "uint" 유형을 "Integer64" 유형으로 노출시키도록 업데이트합니다.

-  MITAB:
   완전한 64비트 길이의 ID를 사용해서 MITAB 드라이버가 보다 강력하고 임의 개수의 피처로 이루어진 임의 개수의 색인 테이블을 입력받을 수 있도록 심리스(seamless) 테이블의 FID 생성 방식을 변경합니다.

테스트 스위트
-------------

다음과 같은 새로운 케이퍼빌리티를 테스트할 수 있도록 테스트 스위트를 확장합니다:

-  핵심 SetField()/GetField() 메소드

-  업데이트된 드라이버들:
   
   *  Shapefile
   *  PG
   *  GeoJSON
   *  CSV
   *  GPKG
   *  SQLite
   *  MySQL
   *  VRT
   *  GML
   *  XLSX
   *  ODS
   *  MITAB

-  OGR SQL

-  ogr2ogr의 ``-mapFieldType`` 옵션

호환성 문제점
-------------

드라이버 코드 변경
~~~~~~~~~~~~~~~~~~

-  SetNextByIndex(), DeleteFeature(), GetFeature(), GetFeatureCount()를 구현하는 모든 드라이버의 프로토타입을 변경하고 약간의 변경 사항을 적용해야 할 것입니다.

-  CreateField()를 지원하는 드라이버는 달리 사용할 수 있는 것이 없는 경우 (그리고 'bApproxOK'가 TRUE인 경우) "OFTInteger64" 유형을 정수형/실수형/문자열 필드로 지원하도록 확장해야 합니다.
   "Integer64" 지원이 노출되지 않는다면 ogr2ogr 유틸리티가 "Integer64" 유형을 "Real" 유형으로 변환할 것입니다.

-  Debug 선언문, printf를 통해 FID를 리포트하는 또는 sprintf 같은 선언문을 사용해서 산출물에 FID를 서식화시키는 드라이버들을 CPL_FRMT_GIB을 사용해서 FID를 서식화하도록 업데이트했습니다. 이런 변경 사항을 적용하는 데 실패하는 경우 코드 충돌이 발생할 수도 있습니다.
   CPL 함수에서 printf() 계열 서식화 문법을 알리기 위해 GCC 주석을 사용하기 때문에, (컴파일 검증이 불가능한 SDE, IDB, INGRES, ArcObjects 같은 일부 독점 드라이버들을 제외하고) 인트리(in-tree) 드라이버들에 필요한 변경 사항을 적용했다고 합리적으로 확신합니다.
   GetFeatureCount() 메소드의 경우에도 동일하게 적용합니다.

응용 프로그램 코드
~~~~~~~~~~~~~~~~~~

-  다운캐스트(downcast) 관련 경고를 피하려면 FID 및 피처 개수에 "GIntBig" 유형을 사용하도록 응용 프로그램 코드를 업데이트해야 할 수도 있습니다.

-  printf 계열 기능을 사용해서 FID 또는 피처 개수를 서식화하는 응용 프로그램 코드도 명확하게 다운캐스트하도록 또는 CPL_FRMT_GIB을 사용하도록 변경해야 할 수도 있습니다.

-  확장 필드(wide field)를 사용할 수 있게 하려면 응용 프로그램 코드에 "Integer64" 유형 처리 작업을 추가해야 할 수도 있습니다.

습성 변경
~~~~~~~~~

-  Shapefile 드라이버가 예전에 "Real" 또는 "Integer" 유형으로 취급했던 확장 정수형 필드를 이제 "Integer64" 유형으로 취급할 것이기 때문에, 일부 응용 프로그램과 작동하지 않을 수도 있고 다른 포맷으로의 변환이 실패할 수도 있습니다.

관련 티켓
---------

-  `#3747 OGR FID는 64비트여야 한다. <http://trac.osgeo.org/gdal/ticket/3747>`_
-  `#3615 Shapefile: 10자릿수 값이 꼭 32비트 정수형에 맞아야 할 필요는 없다. <http://trac.osgeo.org/gdal/ticket/3615>`_
-  `#3150 OGR/OCI 드라이버 상에서 숫자형의 정밀도 문제 <http://trac.osgeo.org/gdal/ticket/3150>`_

이 RFC의 범위를 벗어난 관련 주제
--------------------------------

일치하는 SQL 유형, 예를 들면 임의 개수의 유효 자릿수를 가진 십진수에 대응하는 "Numeric" 유형을 가질 가능성이 고려되었습니다. OGR에서 "Numeric" 유형을 "Integer", "Integer64" 등등 같은 완전한 유형으로 구현할 수 있고, 또는 "String"의 하위 유형으로 구현할 수도 있습니다. (`RFC 50: OGR 필드 하위 유형 <./rfc50_ogr_field_subtype>`_ 을 참조하십시오.)
후자의 경우 더 구현하기 쉽고 데이터베이스 드라이버들 (및 Shapefile 드라이버) 간의 비손실 변환에 가장 유용할 것입니다.
전자의 경우 더 많은 작업이 필요하고, 이상적으로는 임의 길이의 산술을 지원해야 하는 OGR SQL 지원을 수반할 것입니다.
지금으로서는 이런 숫자형 유형의 사용례가 미미한 것으로 판단하기 때문에 "Numeric" 유형 구현은 미루어두는 것으로 결정했습니다.

구현
----

-  이벤 루올(`Spatialys <http://spatialys.com>`_)이 `LINZ(Land Information New Zealand) <https://www.linz.govt.nz/>`_ 의 후원을 받아 구현을 수행할 것입니다.

-  제안된 구현은 깃허브 저장소의 `rfc31_64bit <https://github.com/rouault/gdal2/tree/rfc31_64bit>`_ 브랜치에 있습니다.

-  변경 사항 목록:
   `https://github.com/rouault/gdal2/compare/rfc31_64bit <https://github.com/rouault/gdal2/compare/rfc31_64bit>`_

투표 이력
---------

-  유카 라흐코넨(Jukka Rahkonen) +1
-  대니얼 모리셋(Daniel Morissette) +1
-  세케레시 터마시(Szekeres Tamás) +1
-  하워드 버틀러(Howard Butler) +1
-  이벤 루올(Even Rouault) +1

