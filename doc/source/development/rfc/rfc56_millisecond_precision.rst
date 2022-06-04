.. _rfc-56:

=======================================================================================
RFC 56: OFTTime/OFTDateTime 밀리초 정확도
=======================================================================================

저자: 이벤 루올

연락처: even.rouault@spatialys.com

상태: 승인, GDAL 2.0버전에 구현

요약
----

이 RFC의 목적은 OFTTime 및 OFTDateTime 필드에 다수의 포맷이 명확하게 또는 암묵적으로 지원하는 밀리초 정확도를 추가하는 것입니다:

   -  MapInfo
   -  GPX
   -  Atom (GeoRSS 드라이버)
   -  GeoPackage
   -  SQLite
   -  PostgreSQL
   -  CSV
   -  GeoJSON
   -  ODS
   -  XLSX
   -  KML (잠재적으로 GML도)
   -  ...

핵심 변경 사항
--------------

OGRField 열거형(enumeration)을 다음과 같이 수정합니다:

::

   typedef union {
       [... 변경 사항 없음 ... ]

       struct {
           GInt16  Year;
           GByte   Month;
           GByte   Day;
           GByte   Hour;
           GByte   Minute;
           GByte   TZFlag; /* 0=알 수 없음, 1=현지시(모호함),
                              100=GMT, 104=GMT+1, 80=GMT-5 등등 */
           GByte   Reserved; /* 0으로 설정해야만 합니다. */
           float   Second; /* 밀리초 정확도입니다. 구조의 마지막에 있는 이유는
                              32비트 시스템 상에서 12바이트를 유지하기 위해서입니다. */
       } Date;
   } OGRField;

즉 "GByte Second" 필드를 제거하고 향후 사용할 가능성 때문에 예약된 완충(padding) Byte 유형으로 대체합니다. "float Second" 필드를 추가합니다.

32비트 빌드 상에서, OGRField의 용량은 이제 8바이트가 아니라 12바이트입니다. 64비트 빌드 상에서는 16바이트로 유지됩니다.

새로운/수정된 메소드
~~~~~~~~~~~~~~~~~~~~

"int nSecond"를 입력받았던 :cpp:func:`OGRFeature::SetFieldAsDateTime` 메소드가 이제 "float fSecond" 파라미터를 입력받습니다. "int\* pnSecond"를 입력받던 GetFieldAsDateTime()은 그대로 유지하고, "float\* pfSecond" 를 입력받는 새 GetFieldAsDateTime() 메소드를 추가합니다.

-  :cpp:class:`OGRFeature` 클래스에서:

::

       int                 GetFieldAsDateTime( int i, 
                                        int *pnYear, int *pnMonth, int *pnDay,
                                        int *pnHour, int *pnMinute, int *pnSecond, 
                                        int *pnTZFlag ); /* GDAL 1.x버전과 동일 */
       int                 GetFieldAsDateTime( int i, 
                                        int *pnYear, int *pnMonth, int *pnDay,
                                        int *pnHour, int *pnMinute, float *pfSecond, 
                                        int *pnTZFlag ); /* 새 메소드 */
       void                SetField( int i, int nYear, int nMonth, int nDay,
                                     int nHour=0, int nMinute=0, float fSecond=0.f, 
                                     int nTZFlag = 0 ); /* 수정됨 */
       void                SetField( const char *pszFName, 
                                     int nYear, int nMonth, int nDay,
                                     int nHour=0, int nMinute=0, float fSecond=0.f, 
                                     int nTZFlag = 0 ); /* 수정됨 */

OGRField.Date의 'Second' 멤버가 정수가 아닌 경우 :cpp:func:`OGRFeature::GetFieldAsString` 이 밀리초를 산출하도록 수정합니다.

OGRParseDate()가 초를 부동소수점형 숫자로 파싱하도록 수정합니다.

다음 유틸리티 함수들의 서명이 (연, 월, 일, 시, 분, 초, TZFlag를 완전히 분해하는 대신) OGRField를 입력받도록 그리고 십진수 초를 입력/산출할 수 있도록 수정합니다:

::

   int CPL_DLL OGRParseXMLDateTime( const char* pszXMLDateTime,
                                    OGRField* psField );
   int CPL_DLL OGRParseRFC822DateTime( const char* pszRFC822DateTime,
                                       OGRField* psField );
   char CPL_DLL * OGRGetRFC822DateTime(const OGRField* psField);
   char CPL_DLL * OGRGetXMLDateTime(const OGRField* psField);

C API 변경 사항
~~~~~~~~~~~~~~~

다음 함수만 추가합니다:

::

   int   CPL_DLL OGR_F_GetFieldAsDateTimeEx( OGRFeatureH hFeat, int iField,
                                   int *pnYear, int *pnMonth, int *pnDay,
                                   int *pnHour, int *pnMinute, float *pfSecond,
                                   int *pnTZFlag );
   void   CPL_DLL OGR_F_SetFieldDateTimeEx( OGRFeatureH, int, 
                                          int, int, int, int, int, float, int );

드라이버 변경 사항
------------------

다음 드라이버들이 이제 밀리초를 입력받거나 산출할 수 있습니다:

-  GeoJSON
-  CSV
-  PG
-  PGDump (산출만)
-  CartoDB
-  GeoPackage
-  SQLite
-  MapInfo .tab 및 .mif
-  LIBKML
-  ODS
-  XLSX
-  GeoRSS (Atom 포맷)
-  GPX

SWIG 바인딩 변경 사항
---------------------

Feature.GetFieldAsDateTime() 및 Feature.SetFieldAsDateTime()이 이제 초에 대해 부동소수점형 숫자를 입력받고 반환합니다.

호환성
------

이 RFC는 C/C++ API 및 ABI를 수정합니다.

날짜&시간/시간 유형 필드가 해당 정밀도를 가진 경우, 앞에서 언급한 드라이버들의 산출물이 이제 밀리초를 포함할 것입니다.

관련 티켓
---------

이 RFC의 필요성은 MapInfo 드라이버에 대한 `#2680 티켓 <https://trac.osgeo.org/gdal/ticket/2680>`_ 으로부터 비롯되었습니다.

문서화
------

새로운/수정된 메소드를 모두 문서화합니다.
:file:`MIGRATION_GUIDE.TXT` 에 이 RFC에 대한 단락을 새로 추가합니다.

테스트
------

이 RFC의 다양한 측면을 테스트합니다:

-  핵심 변경 사항
-  드라이버 변경 사항

구현
----

이벤 루올(`Spatialys <http://spatialys.com>`_)이 이 RFC를 구현할 것입니다.

제안한 구현은 `"subsecond_accuracy" 브랜치 <https://github.com/rouault/gdal2/tree/subsecond_accuracy>`_ 저장소에 있습니다.

`변경 사항 목록 <https://github.com/rouault/gdal2/compare/subsecond_accuracy>`_

투표 이력
---------

-  대니얼 모리셋 +1
-  유카 라흐코넨 +1
-  이벤 루올 +1

