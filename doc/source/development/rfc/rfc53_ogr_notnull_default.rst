.. _rfc-53:

=======================================================================================
RFC 53: OGR의 NULL이 아님 제약 조건과 기본값
=======================================================================================

저자: 이벤 루올

연락처: even.rouault@spatialys.com

상태: 승인, GDAL 2.0버전에 구현

요약
----

이 RFC는 OGR 필드에 대한 NULL이 아님(NOT NULL) 제약 조건 및 DEFAULT 값의 처리에 대해 제안합니다. NOT NULL 제약 조건은 기본 데이터 무결성(integrity)을 유지하는 데 유용하며, SQL을 지원하는 드라이버 대부분이 (전부가?) 처리합니다. 피처를 레이어로 삽입할 때 필드 값이 제공되지 않는 경우 필드에 할당해야만 하는 값을 지정하기 위해, NOT NULL 제약 조건에 보완적으로 또는 독립적으로 기본 필드 값을 사용할 수도 있습니다.

NOT NULL 제약 조건
---------------------

지금까지 OGR 필드에는 NOT NULL 제약 조건이 없었습니다. 예를 들어 지금까지는 레이어/테이블에 있는 필드를 피처/레코드의 필드가 설정되지 않을 수도 있다는 (즉 NULL 값을 가질 수도 있다는) 가능성과 함께 생성했습니다. 이것은 여전히 기본 습성일 것입니다. 즉 향후에도 필드가 NULL일 수 있다고 가정합니다.
:cpp:class:`OGRFieldDefn` 클래스에 기본값이 TRUE이고 NOT NULL 제약 조건을 표현하기 위해 FALSE로 설정할 수 있는 'bNullable' 불(boolean) 속성을 추가합니다. (이중 부정 혼동을 피하기 위해 'bNotNullable'보다 'bNullable'을 선호했습니다.)
자신의 저장소에서 NOT NULL 제약 조건을 해석(translate)할 수 있는 드라이버는 해당 속성을 사용해서 필드 정의가 NOT NULL 제약 조건을 포함해야만 하는지를 판단할 것입니다. 데이터소스를 여는 경우 데이터소스의 메타데이터를 조사해서 NULL 값을 가질 수 있는 속성을 제대로 설정할 것이기 때문에, 이 미봉책(roundtrip)이 작동합니다.

:cpp:class:`OGRFieldDefn` 클래스에 다음 메소드들을 추가합니다:

::

       int                 IsNullable() const { return bNullable; }

   /**
    * \brief 이 필드가 NULL 값을 받아들일 수 있는지 여부를 반환합니다.
    *
    * 기본적으로, 필드는 NULL 값을 가질 수 있습니다.
    *
    * 이 메소드가 FALSE를 반환하더라도 (NULL 값을 가질 수 없는 필드일지라도)
    * OGRFeature::IsFieldSet()이 반드시 TRUE를 반환할 것이라는 뜻은 아닙니다.
    * 필드를 임시로 설정하지 않을 수 있고 일반적으로 OGRLayer::CreateFeature()
    * 또는 SetFeature()를 호출했을 때 NULL/NOT NULL 검증을 수행하기 때문입니다.
    *
    * 이 메소드는 OGR_Fld_IsNullable() C 함수와 동일합니다.
    *
    * @return 필드가 NULL일 수 있다고 승인된 경우 TRUE를 반환합니다.
    * @since GDAL 2.0
    */

       void                SetNullable( int bNullableIn ) { bNullable = bNullableIn; }

   /**
    * \brief 이 필드가 NULL 값을 받아들일 수 있는지 여부를 설정합니다.
    *
    * 기본적으로, 필드는 NULL 값을 가질 수 있기 때문에 일반적으로 NOT NULL
    * 제약 조건을 설정하는 FALSE로 이 메소드를 호출합니다.
    *
    * NOT NULL 제약 조건 작성을 지원하는 드라이버는 GDAL_DCAP_NOTNULL_FIELDS
    * 드라이버 메타데이터 항목을 노출시킬 것입니다.
    *
    * 이 메소드는 OGR_Fld_SetNullable() C 함수와 동일합니다.
    *
    * @param bNullableIn 필드가 NOT NULL 제약 조건을 가져야만 하는 경우
    *                    FALSE를 반환합니다.
    * @since GDAL 2.0
    */

이 내용이 도형 필드에 대해 참이기 때문에, :cpp:class:`OGRGeometryFieldDefn` 클래스에도 이 메소드 2개를 추가합니다.

필드에 DEFAULT 값이 연결되어 있지 않는 이상 일반적으로 비어 있지 않은 레이어 상에 NOT NULL 제약 조건을 가진 필드를 추가할 수 없다는 사실을 기억하십시오.

:cpp:`class:`OGRFeature` 클래스에 다음 메소드를 추가합니다:

::

       int                 Validate( int nValidateFlags, int bEmitError );

   /**
    * \brief 피처가 자신의 스키마의 제약 조건을 만족시키는지 검증합니다.
    *
    * nValidateFlags 파라미터가 이 테스트의 범위를 지정합니다.
    *
    * OGR_F_VAL_WIDTH와 관련해서, 문자열 길이를 UTF-8 문자의 개수로 해석해야만
    * 한다는 가정 하에 테스트를 수행합니다. 일부 드라이버들은 문자열 길이를
    * 바이트 수로 대신 해석할 수도 있습니다. 따라서 이 테스트는 보수적인 편입니다.
    * (테스트가 실패하는 경우, 모든 해석에 대해 실패할 것입니다.)
    *
    * 이 함수는 OGR_F_Validate() C 함수와 동일합니다.
    *
    * @param nValidateFlags OGR_F_VAL_ALL 또는 OGR_F_VAL_NULL, OGR_F_VAL_GEOM_TYPE,
    *                       OGR_F_VAL_WIDTH, OGR_F_VAL_ALLOW_NULL_WHEN_DEFAULT를
    *                       '|' 연산자로 조합한 값입니다.
    * @param bEmitError 검증이 실패했을 때 CPLError()를 호출해야만 하는 경우
    *                   TRUE입니다.
    * @return 활성화된 모든 검증 테스트를 통과한 경우 TRUE를 반환합니다.
    * @since GDAL 2.0
    */

이때 nValidateFlags는 다음의 조합입니다:

::

   /** 필드가 NOT NULL 제약 조건을 준수하는지 검증합니다.
    * OGR_F_Validate()가 사용합니다.
    * @since GDAL 2.0
    */
   #define OGR_F_VAL_NULL           0x00000001

   /** 도형이 도형 열 유형을 준수하는지 검증합니다.
    * OGR_F_Validate()가 사용합니다.
    * @since GDAL 2.0
    */
   #define OGR_F_VAL_GEOM_TYPE      0x00000002

   /** (문자열) 필드가 필드 길이를 준수하는지 검증합니다.
    * OGR_F_Validate()가 사용합니다.
    * @since GDAL 2.0
    */
   #define OGR_F_VAL_WIDTH          0x00000004

   /** 연결된 기본값이 있는 경우 필드가 NULL 값을 가질 수 있도록 허용합니다.
    * 저수준 레이어가 필드 값을 연결된 기본값으로 자동 설정하는 드라이버의
    * 경우 이 플래그가 유용할 수 있습니다.
    * 이 플래그는 OGR_F_VAL_NULL도 설정된 경우에만 의미가 있습니다.
    * OGR_F_Validate()가 사용합니다.
    * @since GDAL 2.0
    */
   #define OGR_F_VAL_ALLOW_NULL_WHEN_DEFAULT       0x00000008

   /** 모든 검증 테스트를 활성화합니다.
    * OGR_F_Validate()가 사용합니다.
    * @since GDAL 2.0
    */
   #define OGR_F_VAL_ALL            0xFFFFFFFF

NOT NULL 제약 조건의 검증은 일반적으로 드라이버 저수준 레이어에 전달되기 때문에, :cpp:func:`OGRFeature::Validate` 는 몇 가지 경우에만 (이런 경우 가운데 하나가 GML 드라이버입니다) 유용합니다.

(NULL / NOT-NULL 제약 조건을 구현한 드라이버의 경우) :cpp:func:`OGRLayer::AlterFieldDefn` 에 전송해서 NULL / NOT-NULL 제약 조건을 설정하거나 설정 해제할 수 있는 새 ``ALTER_NULLABLE_FLAG = 0x8`` 플래그를 추가합니다.

정규 속성 필드에 대해 NOT NULL 제약 조건을 처리하는 드라이버는 새로운 GDAL_DCAP_NOTNULL_FIELDS 그리고/또는 GDAL_DCAP_NOTNULL_GEOMFIELDS 드라이버 메타데이터 항목을 노출시켜야 합니다.

:cpp:func:`OGRLayer::CreateGeomField` 인터페이스를 구현하지 않지만 (예를 들어 단일 도형 필드를 지원하는 드라이버) 도형 필드에 NOT NULL 제약 조건이 적용된 레이어를 생성할 수 있는 드라이버는 GEOMETRY_NULLABLE=YES/NO 레이어 생성 옵션을 노출시킬 수 있습니다.

주의: 흔히 작성되는 방식 때문에, NOT NULL 제약 조건을 지원하지 않는 드라이버의 CreateField() 구현은 일반적으로 NULL 값을 사용할 수 있는 플래그의 값을 복사할 것입니다. 이때 플래그의 값을 추가한 직후 필드 정의를 쿼리하는 경우 오해의 소지가 조금 있을 수도 있습니다. (이것은 길이/정밀도에 대해서도 참입니다.)

앞의 모든 메소드들을 C API로 매핑합니다:

::

     int    CPL_DLL OGR_Fld_IsNullable( OGRFieldDefnH hDefn );
     void   CPL_DLL OGR_Fld_SetNullable( OGRFieldDefnH hDefn, int );

   int                  CPL_DLL OGR_GFld_IsNullable( OGRGeomFieldDefnH hDefn );
   void                 CPL_DLL OGR_GFld_SetNullable( OGRGeomFieldDefnH hDefn, int );

   int    CPL_DLL OGR_F_Validate( OGRFeatureH, int nValidateFlags, int bEmitError );

기본 필드 값
------------

NOT NULL 제약 조건을 가진 필드가 무결성을 유지하면서 모든 필드를 채우지 않고 새 피처를 생성할 수 있도록 DEFAULT 절이 수반되는 경우가 있습니다. NULL 값을 사용할 수 있는 필드 상에도 DEFAULT 값을 설정할 수 있지만 이후에 설명할 이유들로 인해 그러지 않을 것을 권장합니다.

자신의 저장소에서 NOT NULL 제약 조건을 해석(translate)할 수 있는 드라이버는 해당 속성을 사용해서 필드 정의가 NOT NULL 제약 조건을 포함해야만 하는지를 판단할 것입니다. 데이터소스를 여는 경우 데이터소스의 메타데이터를 조사해서 NULL 값을 가질 수 있는 속성을 제대로 설정할 것이기 때문에, 이 미봉책(roundtrip)이 작동합니다.

GDAL 1.x버전에는 기본값에 대한 초기 지원이 있었지만 :cpp:class:`OGRFieldDefn` 의 게터/세터(getter/setter) 메소드를 넘어서서 구현되는 일은 없었습니다. 기본값에 대한 초기 지원은 'OGRField uDefault' 멤버에 의존했습니다. :cpp:class:`OGRField` 를 선택한 이유는 기본값을 필드 유형으로 표현하도록 제약하기 위해서지만, 문자열이 아닌 필드에 표현식 또는 특수 키워드를 할당할 수 있기를 바라는 상황이 있을 수도 있습니다. 예를 들어 SQL 표준은 날짜/시간 필드에 대해 CURRENT_TIMESTAMP를 정의합니다. 일반화시키기 위해 이 'uDefault' 멤버를 제거하고 ``char* pszDefault`` 문자열로 대체했습니다.

기본값으로 설정할 수 있는 값은 다음과 같습니다:

-  작은따옴표 문자로 감싸여 있고 적절하게 이스케이프 처리된 다음과 같은 리터럴 문자열 값:
   ``'Nice weather. Isn''t it ?'``

-  숫자형 값 (인용되지 않음)

-  예약된 키워드 (인용되지 않음):
   
   -  CURRENT_TIMESTAMP
   -  CURRENT_DATE
   -  CURRENT_TIME
   -  NULL

-  작은따옴표 문자로 감싸여 있고, 다음과 같이 정의된 서식을 따르는 날짜/시간 리터럴 값:
   'YYYY/MM/DD HH:MM:SS[.sss]'

-  다른 모든 드라이버 특화 표현식. 예를 들어 SQLite의 경우:
   (strftime('%Y-%m-%dT%H:%M:%fZ','now'))

:cpp:class:`OGRFieldDefn` 클래스에 다음 메소드들을 추가/수정합니다:

::

       void                SetDefault( const char* );

   /**
    * \brief 기본 필드 값을 설정합니다.
    *
    * 기본 필드 값을 지원하는 (일반적으로 SQL 인터페이스를 가진) 드라이버가
    * 필드를 생성할 때 기본 필드 값을 연산에 넣습니다. OGRFeature::CreateFeature()
    * 또는 OGRFeature::SetFeature() 호출 시 OGR는 일반적으로 NULL 필드에 스스로
    * 기본 필드 값을 자동 설정하지 않을 것이지만, 저수준 레이어가 그렇게 하도록
    * 허용할 것입니다. 따라서 레이어로부터 피처를 가져오는 것을 권장합니다.
    *
    * 허용되는 값은 NULL, 숫자값, 작은따옴표 문자로 감싸인 (그리고 작은따옴표
    * 문자를 반복해서 내부의 작은따옴표 문자를 이스케이프시킨) 리터럴 값,
    * CURRENT_TIMESTAMP, CURRENT_TIME, CURRENT_DATE 또는 (다른 드라이버는 무시할
    * 수도 있는) 드라이버 특화 표현식입니다.
    * 날짜/시간 리터럴 값의 경우 'YYYY/MM/DD HH:MM:SS[.sss]' 서식이어야 합니다.
    * (UTC 시간으로 간주합니다.)
    *
    * DEFAULT 절 작성을 지원하는 드라이버는 GDAL_DCAP_DEFAULT_FIELDS 환경설정
    * 옵션을 노출시킬 것입니다.
    *
    * 이 메소드는 OGR_Fld_SetDefault() C 함수와 동일합니다.
    *
    * @param pszDefault 새 기본 필드 값 또는 NULL 포인터입니다.
    *
    * @since GDAL 2.0
    */


       const char         *GetDefault() const;

   /**
    * \brief 기본 필드 값을 가져옵니다.
    *
    * 이 메소드는 OGR_Fld_GetDefault() C 함수와 동일합니다.
    *
    * @return 기본 필드 값 또는 NULL을 반환합니다.
    * @since GDAL 2.0
    */


       int                 IsDefaultDriverSpecific() const;

   /**
    * \brief 기본 필드 값이 드라이버 특화 값인지 여부를 반환합니다.
    *
    * 드라이버 특화 기본 필드 값은 NULL이 '아닌' 기본 필드 값, 숫자값,
    * 작은따옴표 문자로 감싸인 리터럴 값, CURRENT_TIMESTAMP,
    * CURRENT_TIME, CURRENT_DATE 또는 날짜/시간 리터럴 값입니다.
    *
    * 이 메소드는 OGR_Fld_IsDefaultDriverSpecific() C 함수와 동일합니다.
    *
    * @return 기본 필드 값이 드라이버 특화 값인 경우 TRUE를 반환합니다.
    * @since GDAL 2.0
    */

SetDefault()는 작은따옴표 문자(')로 시작하는 문자열 리터럴이 제대로 이스케이프 처리되었는지 검증합니다.

IsDefaultDriverSpecific()은 설정된 값이 앞의 열거형에 있는 4개의 글머리 기호(bullet) 가운데 하나에 속하지 않는 경우 TRUE를 반환합니다. 드라이버가 기본값을 처리할 수 있는지 없는지 판단하기 위해 이 메소드를 사용합니다.

드라이버는 한 드라이버에서 또다른 드라이버로 기본값을 전파할 수 있도록 앞의 표준 서식 4개로 된 기본 값을 해석하고 재서식화하기 위한 노력을 기울여야 합니다.

:cpp:class:`OGRFeature` 클래스에 다음 메소드를 추가합니다:

::

       void                FillUnsetWithDefault(int bNotNullableOnly,
                                                char** papszOptions );
   /**
    * \brief 설정되지 않은 필드를 정의될 수도 있는 기본값으로 채웁니다.
    *
    * 이 메소드는 OGR_F_FillUnsetWithDefault() C 함수와 동일합니다.
    *
    * @param bNotNullableOnly 설정되지 않은 필드만 NULL이 아닌
    *                         상수로 채워야 하는 경우
    * @param papszOptions 현재 사용하지 않습니다. NULL로 설정해야만 합니다.
    * @since GDAL 2.0
    */

이 메소드는 피처의 설정되지 않는 필드를 기본 필드 값으로 대체할 것이지만, 드라이버 대부분이 저수준 레이어에서 자동으로 대체 작업을 수행하기 때문에 거의 사용할 일이 없을 것입니다. CreateFeature() 메소드가 전송된 :cpp:class:`OGRFeature` 객체를 수정해서 설정되지 않은 필드를 기본 필드 값으로 자동 설정할 것이라고 신뢰해서는 안 됩니다. 이를 위해서는, 데이터베이스에 저장된 대로 레코드를 가져오기 위해 GetFeature()를 명확하게 호출해야 합니다.

(기본 필드 값을 구현한 드라이버의 경우) :cpp:func:`OGRLayer::AlterFieldDefn` 에 전송해서 기본 필드 값을 설정하거나 설정 해제하거나 수정할 수 있는 새 ``ALTER_DEFAULT_FLAG = 0x8`` 플래그를 추가합니다.

기본 필드 값을 처리하는 드라이버는 새로운 GDAL_DCAP_DEFAULT_FIELDS 드라이버 메타데이터 항목을 노출시켜야 합니다.

주의: 흔히 작성되는 방식 때문에, 기본 필드 값을 지원하지 않는 드라이버의 CreateField() 구현은 일반적으로 기본 필드 값 문자열의 값을 복사할 것입니다. 이때 값을 추가한 직후 필드 정의를 쿼리하는 경우 오해의 소지가 조금 있을 수도 있습니다.

앞의 모든 메소드들을 C API로 매핑합니다:

::

   const char CPL_DLL *OGR_Fld_GetDefault( OGRFieldDefnH hDefn );
   void   CPL_DLL OGR_Fld_SetDefault( OGRFieldDefnH hDefn, const char* );
   int    CPL_DLL OGR_Fld_IsDefaultDriverSpecific( OGRFieldDefnH hDefn );

   void   CPL_DLL OGR_F_FillUnsetWithDefault( OGRFeatureH hFeat,
                                              int bNotNullableOnly,
                                              char** papszOptions );

SWIG 바인딩 (파이썬 / 자바 / C# / 펄) 변경 사항
-----------------------------------------------

다음 변경 사항을 적용했습니다:

-  FieldDefn 클래스에 SetNullable(), IsNullable() 추가
-  GeomFieldDefn 클래스에 SetNullable(), IsNullable() 추가
-  Feature 클래스에 Validate() 추가
-  FieldDefn 클래스 상에서 SetDefault(), GetDefault(), IsDefaultDriverSpecific() 사용 가능
-  Feature 클래스에 FillUnsetWithDefault() 추가

유틸리티
--------

ogrinfo가 NOT NULL 제약 조건 및 DEFAULT 값을 출력하도록 업데이트했습니다. 다음은 그 예시입니다:

::

   Geometry Column 1 NOT NULL = WKT
   Geometry Column 2 NOT NULL = geom2
   id: Integer (0.0) NOT NULL DEFAULT 1234567
   dbl: Real (0.0) NOT NULL DEFAULT 1.456
   str: String (0.0) NOT NULL DEFAULT 'a'
   d: Date (0.0) NOT NULL DEFAULT CURRENT_DATE
   t: Time (0.0) NOT NULL DEFAULT CURRENT_TIME
   dt: DateTime (0.0) NOT NULL DEFAULT CURRENT_TIMESTAMP
   dt2: DateTime (0.0) NOT NULL DEFAULT '2013/12/11 01:23:45'

ogr2ogr에 새 옵션 2개를 추가했습니다:

-  "-forceNullable":
   NOT NULL 제약 조건을 제거합니다. (NOT NULL 제약 조건은 기본적으로 소스로부터 대상 레이어로 전파됩니다.)

-  "-unsetDefault":
   DEFAULT 값을 제거합니다. (DEFAULT 값은 기본적으로 소스로부터 대상 레이어로 전파됩니다.)

명확하게 지정하지 않는 이상, 소스 레이어의 첫 번째 도형 필드에 NOT NULL 제약 조건이 설정된 경우 ogr2ogr는 NOT NULL 제약 조건을 지원하는 대상 레이어에 GEOMETRY_NULLABLE=NO 생성 옵션도 자동 설정할 것입니다.

문서화
------

새로운/수정된 API를 문서화합니다.

파일 포맷
---------

새 인터페이스를 지원하도록 다음 OGR 드라이버들을 업데이트했습니다:

-  PG:
   생성/읽기 시 (속성 필드 및 다중 도형 필드에 대해) NOT NULL 제약 조건 및 DEFAULT 값을 지원합니다. AlterFieldDefn() 구현이 ALTER_NULLABLE_FLAG 및 ALTER_DEFAULT_FLAG를 지원하도록 수정했습니다.

-  PGDump:
   생성 시 (속성 필드 및 다중 도형 필드에 대해) NOT NULL 제약 조건 및 DEFAULT 값을 지원합니다.

-  CartoDB:
   생성 시 (속성 필드 및 다중 도형 필드에 대해) NOT NULL 제약 조건 및 DEFAULT 값을 지원합니다. 인증 로그인 시에만 읽기 시 DEFAULT 값을 지원합니다. (PostgreSQL 시스템 테이블에 대한 쿼리에 의존합니다.)

-  GPKG:
   생성/읽기 시 (속성 필드 및 단일 도형 필드에 대해) NOT NULL 제약 조건 및 DEFAULT 값을 지원합니다. GEOMETRY_NULLABLE 레이어 생성 옵션을 추가했습니다.

-  SQLite:
   생성/읽기 시 (속성 필드 및 다중 도형 필드에 대해) NOT NULL 제약 조건(다중 도형 필드에 대한 지원은 #5494 티켓에 따라 최근 추가되었습니다) 및 DEFAULT 값을 지원합니다. AlterFieldDefn() 구현이 ALTER_NULLABLE_FLAG 및 ALTER_DEFAULT_FLAG를 지원하도록 수정했습니다.

-  MySQL:
   생성/읽기 시 (속성 필드에 대해서만) NOT NULL 제약 조건 및 DEFAULT 값을 지원합니다.

-  OCI:
   생성/읽기 시 (속성 필드 및 단일 도형 필드에 대해) NOT NULL 제약 조건 및 DEFAULT 값을 지원합니다. GEOMETRY_NULLABLE 레이어 생성 옵션을 추가했습니다.

-  VRT:
   읽기 시 새로운 "nullable" 및 "default" 속성을 통해 (속성 필드 및 다중 도형 필드에 대해) NOT NULL 제약 조건 및 DEFAULT 값을 지원합니다. (드라이버 문서 및 :file:`data/ogrvrt.xsd` 를 업데이트했습니다.)

-  GML:
   생성/읽기 시 (속성 필드 및 다중 도형 필드에 대해) NOT NULL 제약 조건을 지원합니다. DEFAULT 값은 실제로는 지원하지 않습니다. (.xsd AFAIK에 DEFAULT 값을 표현할 방법이 없습니다.) 그러나 생성 시 무결한 XML을 생성할 수 있도록 FillUnsetWithDefault()을 이용해서 설정되지 않은 필드를 NOT NULL 제약 조건 및 DEFAULT 값으로 채울 것입니다.

-  WFS:
   읽기 시 (속성 필드에 대해서만) NOT NULL 제약 조건을 지원합니다.

-  FileGDB:
   읽기/쓰기 시 (속성 필드 및 단일 도형 필드에 대해) NOT NULL 제약 조건을 지원합니다. GEOMETRY_NULLABLE 레이어 생성 옵션을 추가했습니다. 생성/읽기 시 문자열, 정수, 실수 유형 필드에 대해 DEFAULT 값을 지원합니다. (이때 FileGDB SDK 및 ESRI 도구에서 어떤 버그 또는 이상한 습성이 관찰됩니다. 문제가 있는 경우 OpenFileGDB 드라이버라는 미봉책을 사용할 수 있습니다.) 읽기 시 날짜/시간 유형에 대해 DEFAULT 값을 지원하지만, FileGDB SDK에 있는 버그로 인해 생성 시에는 지원하지 않습니다.

-  OpenFileGDB:
   읽기 시 (속성 필드 및 단일 도형 필드에 대해) NOT NULL 제약 조건 및 DEFAULT 값을 지원합니다.

MSSQLSpatial 드라이버도 아마도 NOT NULL 제약 조건 및 DEFAULT 값을 지원할 수 있겠지만, 이 작업의 일부로서 업데이트하지는 않았습니다.

테스트 스위트
-------------

다음을 테스트할 수 있도록 테스트 스위트를 확장했습니다:

-  :file:`ogr_feature.py` 에 :cpp:class:`OGRFieldDefn`, :cpp:class:`OGRGeomFieldDefn` 및 :cpp:class:`OGRFeature` 의 모든 새로운 메소드들에 대한 테스트를 추가했습니다.

-  업데이트된 드라이버:

   -  PG
   -  PGDump
   -  CartoDB
   -  GPKG
   -  SQLite
   -  MySQL
   -  OCI
   -  VRT
   -  GML
   -  FileGDB
   -  OpenFileGDB

-  ogr2ogr의 새 옵션들, 그리고 NOT NULL 제약 조건 및 DEFAULT 값 전파의 기본 습성

호환성 문제점
-------------

이 RFC는 몇몇 호환성 문제점을 발생시킬 것입니다.

API와 관련해서, 기존 :cpp:func:`OGRFieldDefn::SetDefault` 를 변경하고 GetDefaultRef()를 제거했습니다. 어떤 드라이버도 이 메소드를 사용하지 않았기 때문에 미치는 영향은 적을 것이며, 향후 제거될 가능성이 크다고 문서화되어 있었기 때문에 응용 프로그램에서도 사용되었을 가능성이 낮습니다. (C 바인딩이 없습니다.)

새 API를 사용하지 않는 경우, GDAL이 생성한 레이어에 대해 작업할 때 GDAL 1.x버전 관련 습성은 그대로 유지될 것입니다. 다른 도구가 생성한 레이어를 읽어오는 경우, NOT NULL 제약 조건 그리고/또는 DEFAULT 값을 읽어올 수 있으며 전파할 수 있습니다. NOT NULL 제약 조건 및 DEFAULT 값의 전파가 어떤 상황에서 문제를 일으킬 수 있다는 점을 배제할 수는 없습니다. 이런 경우 ogr2ogr의 새 옵션들은 GDAL 1.x버전 시대의 습성으로 되돌아갈 것입니다.

이 RFC의 범위를 벗어나는 관련 주제
----------------------------------

설정되지 않은 필드와 NULL로 설정된 필드 사이에 모호성이 존재할 수도 있습니다. 현재 OGR에서는 이 두 개념을 구분하지 않지만, 대부분의 RDBMS에서는 구분할 수 있습니다.

다음과 같은 2개의 선언문이 있을 때:

::

   INSERT INTO mytable (COL1) VALUES (5)
   INSERT INTO mytable (COL1, COL2) VALUES (5, NULL)

COL2가 기본 필드 값을 가진 경우 두 선언문은 동등하지 않습니다.

이 RFC가 수정한 드라이버의 습성은 필드가 설정되지 않은 경우 CreateFeature() 시 NULL을 발행하지 '않는' 것이기 때문에, 기본 필드 값이 존재하는 경우 드라이버의 저수준 레이어가 설정되지 않은 필드를 기본 필드 값으로 대체할 수 있습니다. 이것이 일반적으로 바라는 습성입니다.

명확하게 NULL을 삽입하려는 경우, 드라이버가 지원한다면 (일부 드라이버는 UPDATE 선언문을 작성할 때 설정되지 않은 OGR 필드를 NULL로 강제하지 않을 가능성이 큽니다) 삽입한 후 SetFeature()를 사용해야 할 수도 있습니다. 지원하지 않는다면 삽입한 후 SQL UPDATE 선언문을 직접 전송해야 할 수도 있습니다.

사실, 설정되지 않은 필드 또는 NULL 값을 가진 필드 사이의 이런 혼동은 필드가 NULL을 사용할 수 있고 DEFAULT 값을 가진 경우에만 문제가 됩니다. DEFAULT 값이 항상 NOT NULL 제약 조건과 연동되도록 확인한다면 데이터베이스가 명확한 NULL 값을 거부하기 때문에 문제가 되지 않습니다.

이런 혼동을 해결하려면 설정되지 않은 필드와 NULL 값을 가진 필드를 명확하게 구분하려면 피처 안에 있는 인스턴스화된 필드에 새로운 상태를 추가해야 할 텐데, 이렇게 하면 드라이버와 응용 프로그램의 코드에 심한 영향을 미칠 것입니다.

구현
----

이벤 루올(`Spatialys <http://spatialys.com>`_)이 `LINZ(Land Information New Zealand) <https://www.linz.govt.nz/>`_ 의 후원을 받아 이 RFC를 구현할 것입니다.

제안한 구현은 `"rfc53_ogr_notnull_default" 브랜치 <https://github.com/rouault/gdal2/tree/rfc53_ogr_notnull_default>`_ 저장소에 있습니다.

`변경 사항 목록 <https://github.com/rouault/gdal2/compare/rfc53_ogr_notnull_default>`_

투표 이력
---------

-  유카 라흐코넨 +1
-  대니얼 모리셋 +1
-  이벤 루올 +1

