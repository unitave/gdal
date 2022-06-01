.. _rfc-46:

=======================================================================================
RFC 46: GDAL/OGR 통합
=======================================================================================

저자: 이벤 루올

연락처: even.rouault@spatialys.com

상태: 승인, GDAL 2.0버전에 구현

요약
----

GDAL/OGR 1.x버전에서, GDAL/래스터 및 OGR/벡터 두 쪽이 서로 달라야 할 뚜렷한 이유가 없는 분야에서도, 특히 드라이버의 구조를 포함하는 몇몇 측면에서 상당히 다릅니다. 이 RFC의 목적은 OGR 드라이버 구조를 GDAL 드라이버 구조와 통합하는 것입니다. GDAL 드라이버 구조를 사용하는 경우의 주요 장점은 다음과 같습니다:

-  메타데이터 케이퍼빌리티:
   드라이버 설명, 확장 사양, 생성 옵션, 가상 I/O 케이퍼빌리티, ...

-  효율적인 드라이버 식별 및 열기

마찬가지로, OGR 데이터소스 및 레이어에도 대응하는 GDAL 데이터셋 및 래스터 밴드 클래스들이 제공하는 메타데이터 메커니즘이 부족합니다.

또다른 측면은 GDAL "데이터셋"과 OGR "데이터소스"를 구분하는 것이 인위적인 경우가 있다는 것입니다. 다양한 데이터 컨테이너들이 두 데이터 유형을 모두 받아들일 수 있습니다. 다음은 GDAL 쪽과 OGR 쪽을 둘 다 가진 드라이버들의 목록입니다:

   -  SDTS
   -  PDS
   -  GRASS
   -  KML
   -  Spatialite/Rasterlite
   -  GeoPackage (래스터 쪽은 아직 구현되지 않았습니다)
   -  PostGIS/PostGIS Raster
   -  PDF
   -  PCIDSK
   -  FileGDB (래스터 쪽은 아직 구현되지 않았습니다)

두 데이터 유형 모두에 관심이 있는 응용 프로그램의 경우, 현재 상황은 파일을 서로 다른 API로 두 번 열어야 한다는 뜻입니다. 그리고 파일 기반 드라이버의 업데이트 모드의 경우, 업데이트 모드에서 파일을 동시에 두 번 열어서 서로 충돌하는 변경 사항들을 적용하는 일을 피하도록 업데이트를 순차적으로 수행해야만 합니다.

관련 RFC
--------

예전 RFC 가운데 승인되지는 않았지만 RFC 46와 밀접한 관련이 있는 RFC가 몇 가지 있습니다:

-  `RFC 10: OGR 열기 파라미터 <./rfc10_ogropen>`_:
   RFC 10에서 설명하는 모든 기능이, 특히 새 GDALOpenEx() API가 RFC 46에 포함됩니다.

-  `RFC 25: 빨리 열기 <./rfc25_fast_open>`_:
   RFC 25에서 열려 있는 파일에 형제 파일(sibling file)을 시스템적으로 목록화하는 일을 피해야 한다고 언급했습니다. :cpp:func:`GDALOpenInfo::GetSiblingFiles` 를 이용해서 지연 불러오기(lazy loading)를 하면 RFC 46에서 이를 달성할 수 있습니다. 적어도 Identify()가 GetSiblingFiles()를 촉발해서는 안 됩니다.

-  `RFC 36: GDALOpen 상에서 의도한 드라이버 지정 허용 <./rfc36_open_by_drivername>`_:
   새로운 GDALOpenEx()는 RFC 36에서 제안한 대로 탐지해야만 하는 드라이버 부분 집합 목록을 입력받습니다. 유틸리티에 새로운 옵션을 도입하면 명령줄 상에서 드라이버를 쉽게 지정할 수 있을 테지만, 이는 RFC 46의 범위에서 벗어납니다.

-  `RFC 38: OGR 더 빨리 열기 <./rfc38_ogr_faster_open>`_:
   OGR 드라이버에서 ``Open(GDALOpenInfo*)`` 를 사용한다는 가능성을 통해 RFC 38이 RFC 46에 완전히 포함됩니다.

스스로 부여한 개발 제약 조건
----------------------------

변경 사항들이 기존 GDAL/OGR 코드베이스에, 특히 드라이버에 있는 GDAL/OGR 코드 대부분에 큰 영향을 미쳐서는 안 됩니다. 사용자들이 새로 제공되는 케이퍼빌리티를 사용해야 할 필요가 없는 경우, 변경 사항들은 GDAL/OGR API의 기존 사용자들에게도 큰 영향을 미쳐서는 안 됩니다.

핵심 변경 사항: 요약
--------------------

-  :cpp:class:`OGRSFDriver` 가 :cpp:class:`GDALDriver` 를 확장합니다.
-  벡터 드라이버를 :cpp:class:`GDALDriver` 로 구현할 수 있습니다.
-  :cpp:class:`OGRSFDriverRegistrar` 는 레거시 :cpp:class:`OGRSFDriver` 를 위해 :cpp:class:`GDALDriverManager` 를 감싸는 호환성 래퍼(wrapper)입니다.
-  :cpp:class:`OGRDataSource` 가 :cpp:class:`GDALDataset` 을 확장합니다.
-  "혼합" 데이터셋을 열 수 있도록 GDALOpenEx() API를 추가합니다.
-  :cpp:class:`OGRLayer` 가 :cpp:class:`GDALMajorObject` 를 확장합니다. 즉 메타데이터 케이퍼빌리티를 추가합니다.
-  :cpp:class:`OGRDataSource` 의 레이어 관련 메소드들을 :cpp:class:`GDALDataset` 으로 이동시켜 래스터와 벡터를 모두 처리할 수 있는 컨테이너로 만듭니다.
-  GDALOpenInfo() 메커니즘의 성능을 개선합니다.
-  열기 옵션을 설명하는 (예: 환경설정 옵션의 사용을 퇴출시킨다고 설명하는) 새 드라이버 메타데이터 항목을 추가합니다.
-  레이어 생성 옵션을 설명하는 새 드라이버 메타데이터 항목을 추가합니다.

핵심 변경 사항: 상세
--------------------

드라이버 및 드라이버 등록
~~~~~~~~~~~~~~~~~~~~~~~~~

-  이제 :cpp:class:`OGRSFDriver` 가 :cpp:class:`GDALDriver` 를 확장하고 벡터 드라이버를 구현하는 레거시 방식이 됩니다. :cpp:class:`OGRSFDriver` 를 유지하는 주된 이유는 현재 구현에서 모든 드라이버가 "순수" :cpp:class:`GDALDriver` 로 마이그레이션되지는 않기 때문입니다. CopyDataSource() 가상 메소드를 제거한 이유는 어떤 인트리(in-tree) 드라이버도 이를 구현하지 않기 때문입니다. :cpp:class:`GDALDriver` 로의 상속은 :cpp:class:`GDALDriver` 가 :cpp:class:`GDALDriverManager` 를 이용해서 벡터 드라이버를 관리할 수 있게 해주기 때문에, 벡터 드라이버에 메타데이터를 추가하고 드라이버의 긴 이름을 문서화하고 문서, 파일 확장자, 데이터소스 생성 옵션을 기존 ``GDAL_DMD_*`` 메타데이터 항목들과 링크시킬 수 있습니다.

-  (:cpp:class:`OGRSFDriver` 로부터 상속받는 드라이버들과는 반대로) :cpp:class:`GDALDriver` 로부터 직접 상속받는 드라이버들은:

   -  ``SetMetadataItem(GDAL_DCAP_VECTOR, "YES")`` 를 선언해야 합니다 - 데이터셋 열기를 위해 pfnOpen()을 구현합니다.
   -  선택적으로, 데이터셋 생성을 위해 pfnCreate()를 구현해야 합니다. 벡터 드라이버의 경우 Create()의 'nBands' 파라미터를 0으로 전송해야 합니다.
   -  선택적으로, 데이터셋 삭제를 위해 pfnDelete()를 구현해야 합니다.

-  *C* OGR 드라이버 API는 "순수" :cpp:class:`GDALDriver` 로 변환된 드라이버들과 계속 작동할 것입니다. (C++ OGR 드라이버 API의 경우는 그렇지 않습니다.) 예를 들어 OGR_Dr_GetName()은 :cpp:func:`GDALDriver::GetDescription` 을 호출하고, OGR_Dr_CreateDatasource()는 :cpp:func:`GDALDriver::Create` 를 호출하며, ...

-  :cpp:class:`GDALDriver` 의 C++ 정의에 다음 함수 포인터들을 추가해서 레거시 :cpp:class:`OGRSFDriver` 와 작동할 수 있도록 확장합니다.

::

       /* 레거시 OGR 드라이버 용 */
       GDALDataset         *(*pfnOpenWithDriverArg)( GDALDriver*, GDALOpenInfo * );
       GDALDataset         *(*pfnCreateVectorOnly)( GDALDriver*,
                                                    const char * pszName,
                                                    char ** papszOptions );
       CPLErr              (*pfnDeleteDataSource)( GDALDriver*,
                                                    const char * pszName );


'pfnOpen', 'pfnCreate' 또는 'pfnDelete' 포인터가 NULL인 경우 GDALOpenEx(), :cpp:func:`GDALDriver::Create` 및 :cpp:func:`GDALDriver::Delete` 가 이 함수 포인터들을 사용합니다. :cpp:class:`OGRSFDriverRegistrar` 클래스에 레거시 C++ :cpp:func:`OGRSFDriver::Open`, :cpp:func:`OGRSFDriver::CreateDataSource` 및 :cpp:func:`OGRSFDriver::DeleteDataSource` 가상 메소드를 호출하는 이 함수 포인터들을 구현합니다.

-  벡터 지원 드라이버의 경우 :cpp:func:`GDALDriver::Create` 가 ``nBands == 0`` 을 입력받을 수 있습니다.

-  벡터 지원 드라이버의 경우 :cpp:func:`GDALDriver::DefaultCreateCopy` 는 밴드가 0개인 데이터셋을 입력받을 수 있으며, 산출 데이터셋이 레이어 생성 케이퍼빌리티를 가지고 있고 소스 데이터셋이 레이어를 가지고 있다면 소스 데이터셋으로부터 대상 데이터셋으로 레이어를 복사합니다.

-  :cpp:func:`GDALDriver::Identify` 는 이제 모든 종류의 드라이버들을 반복합니다. Identify()를 구현한 드라이버들에 대해 첫 번째 패스(pass)를 수행하도록 수정했습니다. 일치하는 드라이버를 찾지 못 한 경우 더 느릴 가능성이 있는 Open()을 식별 메소드로 사용해서 모든 드라이버에 대해 두 번째 패스를 수행합니다.

-  앞의 요점과 관련해서, 전송된 GDALOpenInfo가 드라이버와 일치하는지를 나타내는 불(boolean) 값을 반환하는 데 사용되는 GDALDriver::pfnIdentify 함수 포인터를 구현합니다. 일부 드라이버의 경우 이 포인터 구현이 Identify()를 구현할 수 있을 정도로 너무 제한적이었습니다. 예를 들면 탐지 로직이 "네, 해당 파일을 분명하게 인식합니다", "아니오, 일치하지 않습니다" 또는 "인식하기에는 GDALOpenInfo에 있는 요소들이 충분하지 않습니다"를 반환할 수 있는 경우입니다. 이제 마지막 선언을 음의 반환값으로 나타낼 수 있습니다.

-  :cpp:class:`OGRSFDriverRegistrar` 를 주로 :cpp:class:`GDALDriverManager` 를 감싸는 래퍼(wrapper)로 줄였습니다. 특히, :cpp:class:`OGRSFDriverRegistrar` 클래스는 이제 더 이상 드라이버 목록을 담지 않으며 Open(), OpenShared(), ReleaseDataSource(), DeregisterDriver() 그리고 AutoLoadDrivers() 메소드들을 제거했습니다.
   이 변경으로 인해 C++ 코드에 영향이 갈 수도 있습니다. 이 변경 사항들에 맞춰 OGR 유틸리티를 몇 군데 조정했습니다.
   레거시 OGR 드라이버를 위해 RegisterDriver() API를 유지했는데 이 API는 ``SetMetadataItem(GDAL_DCAP_VECTOR, "YES")`` 를 자동으로 설정합니다. GetDriverCount(), GetDriver() 및 GetDriverByName() 메소드를 :cpp:class:`GDALDriverManager` 로 위임하고 GDAL_DCAP_VECTOR 케이퍼빌리티를 가진 드라이버들만 고려하도록 합니다.
   드라이버가 GDAL 또는 OGR 드라이버와 동일한 이름을 가지고 있는 경우, 내부적으로 OGR 변이형에 ``OGR_`` 접두어를 붙이고 GetDriverByName()이 ``OGR_`` 변이형을 먼저 시도할 것입니다.
   참고로, MapServer도 QGIS도 이 함수들을 사용하지 않습니다.

-  OGRRegisterAll()은 이제 GDALAllRegister()의 별명입니다. 이제 예전 OGRRegisterAll()을 OGRRegisterAllInternal()로 재명명하고 GDALAllRegister()가 이를 호출합니다. 즉, GDALAllRegister()와 OGRRegisterAll()이 이제 동등하며 모든 드라이버를 등록합니다.

-  :cpp:class:`GDALDriverManager` 에 몇 가지 변경 사항들을 적용했습니다:

   -  GetDriverByName()의 속도를 높이기 위해 드라이버 이름으로부터 드라이버 객체로의 매핑을 사용합니다.

   -  하위 호환성을 위해 OGR_SKIP 및 OGR_DRIVER_PATH 환경설정 옵션을 받아들입니다.

   -  GDAL_SKIP 환경설정 옵션에서 드라이버 이름의 추천 구분자가 이제 (OGR_SKIP과 마찬가지로) 공백이 아니라 쉼표입니다. 이는 GDAL_SKIP에서 "ESRI Shapefile" 또는 "MapInfo File"처럼 이름에 공백이 포함된 OGR 드라이버 이름을 정의할 수 있게 하기 위해서입니다. (하위 호환성을 위해) GDAL_SKIP 값에 쉼표가 없을 경우 공백 구분자로 가정합니다.

   -  플러그인 검색 디렉터리의 대안 경로를 정의하는 것으로 보이는 GetHome()/SetHome() 메소드를 제거합니다. 이 메소드들은 오직 C++ 수준에서만 존재했는데, GDAL_DRIVER_PATH 환경설정 옵션으로 인해 쓸모가 없어졌기 때문입니다.

-  래스터 지원 드라이버가 ``SetMetadataItem(GDAL_DCAP_RASTER, "YES")`` 를 선언해야 합니다. 모든 인트리 GDAL 드라이버가 이를 선언하도록 패치했습니다. 그러나 등록 코드가 드라이버가 GDAL_DCAP_RASTER 또는 GDAL_DCAP_VECTOR 둘 다 선언하지 않는지를 탐지하고, 둘 다 선언하지 않는 경우 GDAL_DCAP_RASTER를 명확하게 설정할 것을 제안하는 디버그 메시지와 함께 패치되지 않은 드라이버를 대신해서 GDAL_DCAP_RASTER를 선언합니다.

-  새 메타데이터 항목들:

   -  GDAL_DCAP_RASTER=YES / GDAL_DCAP_VECTOR=YES: 드라이버 수준.
      드라이버가 래스터/벡터 케이퍼빌리티를 가지고 있다고 선언하기 위한 항목입니다. 드라이버가 둘 다 선언할 수 있습니다.

   -  GDAL_DMD_EXTENSIONS: (끝에 S가 붙습니다) 드라이버 수준.
      이 항목은 GDAL_DMD_EXTENSION의 진화형으로, 값 문자열에 확장자 여러 개를 지정할 수 있습니다. 확장자를 공백으로 구분합니다. 예를 들면 "shp dbf", "tab mif mid" 등등처럼 구분합니다. 좀 더 쉽게 사용할 수 있도록, GDAL_DMD_EXTENSIONS이 아직 설정되지 않은 경우 ``GDALDriver::SetMetadataItem(GDAL_DMD_EXTENSION)`` 도 전송된 값을 GDAL_DMD_EXTENSIONS로 설정합니다. 따라서 새로운 코드가 항상 GDAL_DMD_EXTENSIONS를 사용할 수 있습니다.

   -  GDAL_DMD_OPENOPTIONLIST: 드라이버 수준.
      이 항목의 값은 생성 옵션과 비슷한 서식을 가진 XML 조각(snippet)입니다. GDALOpenEx()가 Identify()를 이용해서 드라이버가 파일을 입력받는다는 사실을 식별하고 나면 인증된 열기 옵션 목록으로 전송된 열기 옵션 목록을 검증할 것입니다. 다음은 S57 드라이버에서의 이런 인증된 열기 옵션 목록의 예시입니다.

::

   <OpenOptionList>
     <Option name="UPDATES" type="string-select"
       description="Should update files be incorporated into the base data on the fly" default="APPLY">
       <Value>APPLY</Value>
       <Value>IGNORE</Value>
     </Option>
     <Option name="SPLIT_MULTIPOINT" type="boolean"
       description="Should multipoint soundings be split into many single point "
                   "sounding features" default="NO" />
     <Option name="ADD_SOUNDG_DEPTH" type="boolean"
       description="Should a DEPTH attribute be added on SOUNDG features and "
                   "assign the depth of the sounding" default="NO" />
     <Option name="RETURN_PRIMITIVES" type="boolean"
       description="Should all the low level geometry primitives be returned as "
                   "special IsolatedNode, ConnectedNode, Edge and Face layers" default="NO" />
     <Option name="PRESERVE_EMPTY_NUMBERS" type="boolean"
       description="If enabled, numeric attributes assigned an empty string as a "
                   "value will be preserved as a special numeric value" default="NO" />
     <Option name="LNAM_REFS" type="boolean"
       description="Should LNAM and LNAM_REFS fields be attached to features "
                   "capturing the feature to feature relationships in the FFPT "
                   "group of the S-57 file" default="YES" />
     <Option name="RETURN_LINKAGES" type="boolean"
       description="Should additional attributes relating features to their underlying "
                   "geometric primtives be attached" default="NO" />
     <Option name="RECODE_BY_DSSI" type="boolean"
       description="Should attribute values be recoded to UTF-8 from the character "
                   "encoding specified in the S57 DSSI record." default="NO" />
   </OpenOptionList>

-  GDAL_DS_LAYER_CREATIONOPTIONLIST: 데이터셋 수준.
   그러나 실제로는 드라이버 수준에서도 설정할 수 있습니다. 레이어 생성 옵션이 데이터셋 인스턴스에 의존하지 않기 때문입니다. 이 항목의 값은 데이터셋 생성 옵션과 비슷한 서식을 가진 XML 조각(snippet)입니다. 이 항목을 지정하는 경우 인증된 생성 옵션 목록으로 CreateLayer()에 전송된 생성 옵션을 검증합니다. 다음은 Shapefile 드라이버에서의 이런 인증된 생성 옵션 목록의 예시입니다.

::

   <LayerCreationOptionList>
     <Option name="SHPT" type="string-select" description="type of shape" default="automatically detected">
       <Value>POINT</Value>
       <Value>ARC</Value>
       <Value>POLYGON</Value>
       <Value>MULTIPOINT</Value>
       <Value>POINTZ</Value>
       <Value>ARCZ</Value>
       <Value>POLYGONZ</Value>
       <Value>MULTIPOINTZ</Value>
       <Value>NONE</Value>
       <Value>NULL</Value>
     </Option>
     <Option name="2GB_LIMIT" type="boolean" description="Restrict .shp and .dbf to 2GB" default="NO" />
     <Option name="ENCODING" type="string" description="DBF encoding" default="LDID/87" />
     <Option name="RESIZE" type="boolean" description="To resize fields to their optimal size." default="NO" />
   </LayerCreationOptionList>

.. _datasets--datasources:

데이터셋 / 데이터소스
~~~~~~~~~~~~~~~~~~~~~

-  :cpp:class:`OGRDataSource` 클래스의 주요 메소드들을 :cpp:class:`GDALDataset` 클래스로 이동시킵니다:

::

       virtual int         GetLayerCount() { return 0; }
       virtual OGRLayer    *GetLayer(int) { return NULL; }
       virtual OGRLayer    *GetLayerByName(const char *);
       virtual OGRErr      DeleteLayer(int);

       virtual int         TestCapability( const char * ) { return FALSE; }

       virtual OGRLayer   *CreateLayer( const char *pszName, 
                                        OGRSpatialReference *poSpatialRef = NULL,
                                        OGRwkbGeometryType eGType = wkbUnknown,
                                        char ** papszOptions = NULL );
       virtual OGRLayer   *CopyLayer( OGRLayer *poSrcLayer, 
                                      const char *pszNewName, 
                                      char **papszOptions = NULL );

       virtual OGRStyleTable *GetStyleTable();
       virtual void        SetStyleTableDirectly( OGRStyleTable *poStyleTable );
                               
       virtual void        SetStyleTable(OGRStyleTable *poStyleTable);

       virtual OGRLayer *  ExecuteSQL( const char *pszStatement,
                                       OGRGeometry *poSpatialFilter,
                                       const char *pszDialect );
       virtual void        ReleaseResultSet( OGRLayer * poResultsSet );

       int                 GetRefCount() const;
       int                 GetSummaryRefCount() const;
       OGRErr              Release();

-  다음 일치하는 C API를 사용할 수 있습니다:

::

   int    CPL_DLL GDALDatasetGetLayerCount( GDALDatasetH );
   OGRLayerH CPL_DLL GDALDatasetGetLayer( GDALDatasetH, int );
   OGRLayerH CPL_DLL GDALDatasetGetLayerByName( GDALDatasetH, const char * );
   OGRErr    CPL_DLL GDALDatasetDeleteLayer( GDALDatasetH, int );
   OGRLayerH CPL_DLL GDALDatasetCreateLayer( GDALDatasetH, const char *, 
                                         OGRSpatialReferenceH, OGRwkbGeometryType,
                                         char ** );
   OGRLayerH CPL_DLL GDALDatasetCopyLayer( GDALDatasetH, OGRLayerH, const char *,
                                           char ** );
   int    CPL_DLL GDALDatasetTestCapability( GDALDatasetH, const char * );
   OGRLayerH CPL_DLL GDALDatasetExecuteSQL( GDALDatasetH, const char *,
                                        OGRGeometryH, const char * );
   void   CPL_DLL GDALDatasetReleaseResultSet( GDALDatasetH, OGRLayerH );
   OGRStyleTableH CPL_DLL GDALDatasetGetStyleTable( GDALDatasetH );
   void   CPL_DLL GDALDatasetSetStyleTableDirectly( GDALDatasetH, OGRStyleTableH );
   void   CPL_DLL GDALDatasetSetStyleTable( GDALDatasetH, OGRStyleTableH );

-  OGRDataSource 정의를 이제 다음과 같이 줄입니다:

::

   class CPL_DLL OGRDataSource : public GDALDataset
   {
   public:
                           OGRDataSource();

       virtual const char  *GetName() = 0;

       static void         DestroyDataSource( OGRDataSource * );
   };

-  기존 ``OGR_DS_*`` API를 보전합니다. 이 함수들의 구현은 ``GDALDataset*`` 을 가리키는 OGRDataSourceH 불투명 포인터(opaque pointer)를 캐스트하기 때문에, C API 관점에서 GDALDatasetH와 OGRDataSourceH가 동등하다고 간주할 수 있습니다. 현재 C++ 수준에서는 그렇지 않다는 사실을 기억하십시오!

-  :cpp:func:`OGRDataSource::SyncToDisk` 를 제거했습니다. 기존 FlushCache()에 동등한 기능을 구현해야 합니다.
   :cpp:class:`GDALDataset::FlushCache` 는 이제 예를 들어 모든 레이어를 반복한 다음 레이어들에 대해 SyncToDisk()를 호출하는 것 같은 :cpp:class:`OGRDataSource::SyncToDisk` 의 예전 일반 구현의 작업을 수행합니다.

-  :cpp:class:`GDALDataset` 은 이제 보호된(protected) ICreateLayer() 메소드를 가집니다.

::

       virtual OGRLayer   *ICreateLayer( const char *pszName, 
                                        OGRSpatialReference *poSpatialRef = NULL,
                                        OGRwkbGeometryType eGType = wkbUnknown,
                                        char ** papszOptions = NULL );

예전 CreateLayer()이었던 메소드입니다. 즉 드라이버에서 CreateLayer() 특수 구현을 ICreateLayer()로 재명명해야 합니다. CreateLayer()는 :cpp:class:`GDALDataset` 수준으로 유지되지만, 그 구현은 ICreateLayer()를 호출하기 전에 선택적인 승인된 생성 옵션 목록(GDAL_DS_LAYER_CREATIONOPTIONLIST)으로 전송된 생성 옵션 목록을 사전 검증합니다. (이는 RasterIO() / IRasterIO()와 유사합니다.) CreateLayer()를 ICreateLayer()로 재명명하기 위해 모든 인트리 OGR 드라이버에 대해 전체 수준에서 훑었습니다.

-  래스터 전용, 벡터 전용, 또는 래스터-벡터 데이터셋을 열기 위한 GDALOpenEx()를 추가했습니다. 이 메소드는 읽기 전용/업데이트 모드, 공유/비공유 모드를 허용합니다.
   잠재적 후보 드라이버 목록을 전송할 수 있습니다. 이 목록이 NULL인 경우 모든 트라이버를 탐지합니다. (NAME=VALUE 문법의) 열기 옵션 목록을 전송할 수 있습니다. 형제(sibling) 파일 목록이 이미 확정되었다면 이 목록도 전송할 수 있습니다. 확정되지 않았다면 :cpp:class:`GDALOpenInfo` 가 형제 파일 목록을 확정할 것입니다.

::

   GDALDatasetH CPL_STDCALL GDALOpenEx( const char* pszFilename,
                                    unsigned int nOpenFlags,
                                    const char* const* papszAllowedDrivers,
                                    const char* const* papszOpenOptions,
                                    const char* const* papszSiblingFiles );

'nOpenFlags' 인자는 다음 값들의 'OR 가능(or-able)' 조합입니다:

::

   /* Note: GDAL_OF_READONLY 및 GDAL_OF_UPDATE를 의도적으로 정의합니다 */
   /* GA_ReadOnly 및 GA_Update와 동일합니다 */

   /** 읽기 전용 모드로 열기 */
   #define     GDAL_OF_READONLY        0x00
   /** 업데이트 모드로 열기 */
   #define     GDAL_OF_UPDATE          0x01

   /** 래스터 및 벡터 드라이버 허용 */
   #define     GDAL_OF_ALL             0x00

   /** 래스터 드라이버 허용 */
   #define     GDAL_OF_RASTER          0x02
   /** 벡터 드라이버 허용 */
   #define     GDAL_OF_VECTOR          0x04
   /* GDAL 3.0의 새로운 유형을 위해 예약 ;-) */
   /*#define     GDAL_OF_OTHER_KIND1   0x08 */
   /*#define     GDAL_OF_OTHER_KIND2   0x10 */

   /** 공유 모드로 열기 */
   #define     GDAL_OF_SHARED          0x20

   /** 열기 실패 시 오류 메시지 생성 */
   #define     GDAL_OF_VERBOSE_ERROR   0x40

기존 GDALOpen(), GDALOpenShared(), OGROpen(), OGROpenShared(), OGR_Dr_Open()은 그저 적절한 열기 플래그를 가진 GDALOpenEx()의 래퍼일 뿐입니다. 사용자 시점에서는 이들의 습성이 기존 습성과 동일합니다. 예를 들어 GDALOpen() 계열은 선언된 래스터 케이퍼빌리티를 가진 드라이버의 데이터셋만 반환하고, 이는 OGROpen() 계열도 벡터에 대해 마찬가지입니다.

-  :cpp:class:`GDALOpenInfo` 클래스에 다음 변경 사항들을 적용합니다:

   -  구성자의 두 번째 인자가 이제 GDALAccess가 아니라 GDALOpenEx()와 동일하게 'nOpenFlags'입니다. :cpp:class:`GDALOpenInfo` 는 읽기 전용/업데이트 비트를 사용해서 기존 드라이버에서 많이 사용되는 eAccess 플래그를 "계산"합니다.
      래스터와 벡터를 둘 다 지원하는 드라이버는 GDAL_OF_VECTOR/GDAL_OF_RASTER 비트를 사용해서 호출자의 의도를 판단할 수 있습니다. 예를 들어 호출자가 GDAL_OF_RASTER만 가지고 데이터셋을 열었는데 데이터셋이 벡터 데이터만 담고 있는 경우, 드라이버가 데이터셋을 열기 않기로 결정할 수도 있습니다. (해당 드라이버가 읽기 전용 드라이버인 경우입니다. 업데이트 케이퍼빌리티를 가진 드라이버라면 읽기 전용 모드로 열기를 수행한 경우에만 이렇게 해야 합니다.)

   -  드라이버가 열기 옵션을 사용할 수 있도록 :cpp:class:`GDALOpenInfo` 의 'papszOpenOptions' 멤버에 GDALOpenEx()로 전송된 열기 옵션을 저장합니다.

   -  "FILE\* fp" 멤버를 "VSILFILE\* fpL"로 변환합니다. 이렇게 변경하는 이유는 가장 유명한 드라이버들이 이제 파일을 다시 열어야 할 필요없이 'fpL' 멤버를 직접 사용할 수 있도록 VSI 가상 파일 API를 사용하기 때문입니다. 'fp'를 사용했던 모든 인트리 GDAL 드라이버에 대해 전체 수준에서 훑었습니다.

   -  예전에는 전송된 파일의 특성을 판단하기 위해 VSIStatExL()을 실행했습니다. 이제, 대부분의 사용례에서 전송된 파일명이 파일이라고 가정하고 낙관적으로 VSIFOpenL()을 실행합니다. 열기가 실패하는 경우, 파일명의 특성을 판단하기 위해 VSIStatExL()을 실행합니다.

   -  업데이트 모드로 접근을 요청한 경우, "rb+" 권한을 직접 사용할 수 있도록 VSIFOpenL()로 파일을 엽니다.

   -  'papszSiblingFiles'가 이제 비공개(private) 멤버입니다. 요청 시 ReadDir()를 실행하는 GetSiblingFiles() 메소드가 이 멤버에 접근합니다. 이렇게 하면 일반적으로 형제 파일을 알아야 할 필요가 없는 Identify() 메소드의 속도를 높일 수 있습니다.

   -  파일의 처음 1,024바이트 이상을 읽어오는 새 TryToIngest() 메소드를 추가합니다. 파일을 식별하려면 몇 바이트를 더 가져와야만 하는 GML 또는 NAS 같은 몇몇 벡터 드라이버에 유용합니다.

레이어
~~~~~~

-  :cpp:class:`OGRLayer` 가 :cpp:class:`GDALMajorObject` 를 확장합니다. 드라이버가 이제 일반적인 GetMetadata()/GetMetadateItem() API로 가져올 수 있는 레이어 메타데이터 항목들을 정의할 수 있습니다.

-  GetInfo() 메소드를 제거했습니다. 이 메소드는 어떤 인트리 드라이버에도 구현된 적이 없으며 오래 전에 퇴출되었기 때문입니다.

기타
~~~~

-  퇴출되어 사용되지 않는 GDALProjDefH 및 GDALOptionDefinition 유형을 :file:`gdal.h` 로부터 제거했습니다.

-  GDALGeneralCmdLineProcessor()가 이제 'nOptions'(GDAL_OF_RASTER와 GDAL_OF_VECTOR의 조합) 인자를 "--formats" 옵션으로 출력해야 하는 드라이버 유형으로 해석합니다. 0으로 설정하는 경우, GDAL_OF_RASTER라고 가정합니다.

-  GDAL 유틸리티의 "--formats" 옵션이 드라이버가 래스터 그리고/또는 벡터 케이퍼빌리티를 가지고 있는지 여부를 출력합니다.

-  GDAL 유틸리티의 "--formats" 옵션은 GDAL_DMD_EXTENSIONS, GDAL_DMD_OPENOPTIONLIST, DAL_DS_LAYER_CREATIONOPTIONLIST 를 출력합니다.

-  OGRGeneralCmdLineProcessor()가 벡터 지원 드라이버가 "--formats" 옵션을 사용하지 못 하게 하는 GDALGeneralCmdLineProcessor() 구현을 사용합니다.

드라이버 변경 사항
------------------

-  OGR PCIDSK 드라이버를 GDAL PCIDSK 드라이버로 병합했습니다.

-  OGR PDF 드라이버를 GDAL PDF 드라이버로 병합했습니다.

-  파일을 인식하는지 판단하기 위해 파일을 열어봐야만 하는 모든 인트리 OGR 드라이버를 전체 수준에서 훑었습니다. 이 드라이버들이 GDALOpenInfo 인자를 입력받을 수 있도록 :cpp:class:`GDALDriver` 로 변환했기 때문에 이제 'pabyHeader' 필드를 사용해서 파일의 처음 바이트들을 검사합니다.
   GDAL 1.11버전에서, OGR 드라이버가 파일을 인식하지 못 하는지 판단하기 위한 파일 접근 (열기/통계) 관련 시스템 호출의 개수가 46개에서 1개로 줄었습니다. 변환된 드라이버들은 다음과 같습니다:

   -  AeronavFAA
   -  ArcGEN
   -  AVCBin
   -  AVCE00
   -  BNA
   -  CSV
   -  DGN
   -  EDIGEO
   -  ESRI
   -  Shapefile
   -  GeoJSON
   -  GeoRSS
   -  GML
   -  GPKG
   -  GPSBabel
   -  GPX
   -  GTM
   -  HTF
   -  ILI1
   -  ILI2
   -  KML
   -  LIBKML
   -  MapInfo File
   -  MySQL
   -  NAS
   -  NTF
   -  OpenAIR
   -  OSM
   -  PDS
   -  REC
   -  S57
   -  SDTS
   -  SEGUKOOA
   -  SEGY
   -  SOSI
   -  SQLite
   -  SUA
   -  SVG
   -  TIGER
   -  VFK
   -  VRT
   -  WFS

-  대부분의 OGR 드라이버에 대해 드라이버의 긴 설명을 설정했습니다.

-  :cpp:class:`OGRLayer` 로부터 파생된 모든 클래스가 ``GetName()/poFeatureDefn->GetName()`` 값으로 SetDescription()을 호출하도록 수정했습니다. ``test_ogrsf`` 가 이 변경 사항이 제대로 설정되었는지 테스트합니다.

-  다음 드라이버들은 :cpp:class:`OGRSFDriver` 로 유지되지만, 이 드라이버들의 Open() 메소드는 데이터소스 객체가 인스턴스화되지 않도록 사전에 확장자/접두어 테스트를 수행합니다:

   -  CartoDB
   -  CouchDB
   -  DXF
   -  EDIGEO
   -  GeoConcept
   -  GFT
   -  GME
   -  IDRISI
   -  OGDI
   -  PCIDSK
   -  PG
   -  XPlane

-  다음 드라이버들에 Identify()를 구현했습니다:

   -  CSV
   -  DGN
   -  DXF
   -  EDIGEO
   -  GeoJSON
   -  GML
   -  KML
   -  LIBKML
   -  MapInfo File
   -  NAS
   -  OpenFileGDB
   -  OSM
   -  S57
   -  Shape
   -  SQLite
   -  VFK
   -  VRT

-  다음 드라이버들에 GDAL_DMD_EXTENSION/GDAL_DMD_EXTENSIONS를 설정했습니다:

   -  AVCE00
   -  BNA
   -  CSV
   -  DGN
   -  DWG
   -  DXF
   -  EDIGEO
   -  FileGDB
   -  Geoconcept
   -  GeoJSON
   -  Geomedia
   -  GML
   -  GMT
   -  GPKG
   -  GPX
   -  GPSTrackMaker
   -  IDRISI Vector
   -  Interlis 1
   -  Interlis 2
   -  KML
   -  LIBKML
   -  MDB
   -  MapInfo File
   -  NAS
   -  ODS
   -  OpenFileGDB
   -  OSM
   -  PGDump
   -  PGeo
   -  REC
   -  S57
   -  ESRI Shapefile
   -  SQLite
   -  SVG
   -  WaSP
   -  XLS
   -  XLSX
   -  XPlane

-  다음 드라이버의 데이터셋 및 레이어 생성 옵션들을 GDAL_DMD_CREATIONOPTIONLIST / GDAL_DS_LAYER_CREATIONOPTIONLIST로 문서화했습니다:

   -  BNA
   -  DGN
   -  FileGDB
   -  GeoConccept
   -  GeoJSON
   -  GeoRSS
   -  GML
   -  GPKG
   -  KML
   -  LIBKML
   -  PG
   -  PGDump
   -  ESRI Shapefile

-  다음 드라이버에 열기 옵션을 추가했습니다:

   -  AAIGRID
   -  PDF
   -  S57
   -  ESRI Shapefile

-  다음 드라이버에 GetFileList()를 구현했습니다:

   -  OpenFileGDB
   -  ESRI Shapefile
   -  OGR VRT

-  다음 드라이버에 대해 데이터소스 SyncToDisk()를 FlushCache()로 재명명했습니다:

   -  LIBKML
   -  OCI
   -  ODS
   -  XLSX

-  쓸모없는 파일 다시 열기를 방지하기 위해 다음 드라이버에서 ``poOpenInfo->fpL`` 을 사용하도록 수정했습니다:

   -  GTiff
   -  PNG
   -  JPEG
   -  GIF
   -  VRT
   -  NITF
   -  DTED

-  HTTP 드라이버:
   GDAL_DCAP_RASTER 및 GDAL_DCAP_VECTOR 드라이버로 선언합니다.

-  RIK 드라이버:
   Identify()를 구현했습니다.

-  주의 사항:
   다음 (대부분 독점) OGR 드라이버들이 컴파일되는지 그리고 제대로 작동하는지를 테스트하지 못 했습니다.

   -  ArcObjects
   -  DWG
   -  DODS
   -  SDE
   -  FME
   -  GRASS
   -  IDB
   -  OCI
   -  MSSQLSpatial (컴파일 확인, 그러나 런타임 테스트하지 못 함)

유틸리티 변경 사항
------------------

-  gdalinfo가 열기 옵션을 정의하는 "-oo" 옵션을 받아들입니다.
-  ogrinfo가열기 옵션을 정의하는 "-oo" 옵션을 받아들입니다.
-  ogr2ogr가 입력 데이터셋 열기 옵션을 정의하는 "-oo" 옵션을, 그리고 대상 데이터셋 열기 옵션을 정의하는 "-doo" 옵션을 받아들입니다.

SWIG 바인딩 변경 사항
---------------------

-  파이썬 및 자바 바인딩:

   -  :cpp:class:`OGRDataSource` 로부터 가져온 새로운 :cpp:class:`GDALDataset` 메소드를 추가합니다:

      -  CreateLayer()
      -  CopyLayer()
      -  DeleteLayer()
      -  GetLayerCount()
      -  GetLayerByIndex()
      -  GetLayerByName()
      -  TestCapability()
      -  ExecuteSQL()
      -  ReleaseResultSet()
      -  GetStyleTable()
      -  SetStyleTable()

   -  MajorObject로부터 OGR Driver, OGRMajorObjectDataSource 및 Layer 객체를 파생시킵니다.

-  펄(Perl) 및 C#:
   새 케이퍼빌리티를 사용할 수 있으려면 각각의 유지/관리자가 일부 작업을 수행해야 할 것입니다. 여전히 컴파일되는지 확인하십시오.

이 RFC에 포함되지 '않은' 잠재적인 변경 사항들
---------------------------------------------

현재 RFC의 "자연스러운" 진화:

-  GDAL MEM 및 OGR 메모리 드라이버들의 통합
-  GDAL VRT 및 OGR VRT 드라이버들의 통합

심화 통합 단계:

-  소스 트리 변경:
   OGR 드라이버를 :file:`ogr/ogrsf_frmts/` 로부터 :file:`frmts/` 로 이동시키고, :file:`ogr/ogrsf_frmts/generic/*` 를 :file:`gcore/*` 로 이동시키고, ...

-  문서 통합 (드라이버 목록 페이지 등등)

-  OGR 이름공간의 흔적을 제거하기 위해 재명명:
   OGRLayer를 GDALLayer로, ...

-  "--without-ogr" 컴파일 옵션을 제거해야 하는지? 현재 편의상 :file:`ogr/ogrsf_frmts/generic` 및 :file:`ogr/ogrsf_frmts/mitab` 을 내장하고 있기는 하지만 작동 상태로 유지되고 있습니다.

-  일부 유티리티들의 통합:
   모든 종류의 데이터셋에 대해 작동할 "gdal info XXX", "gdal convert XXX"

하위 호환성
-----------

:cpp:func:`GDALDriverManager::GetDriverCount`, :cpp:func:`GDALDriverManager::GetDriver` 가 이제 GDAL 드라이버는 물론 OGR 드라이버도 반환합니다.

GDAL 데이터셋의 참조 횟수 계산 방식(reference counting)과 GDAL 1.X OGR 데이터소스의 참조 횟수 계산 방식은 조금 다릅니다. GDAL 데이터셋의 경우 1에서 시작하고 OGR 데이터소스의 경우 0에서 시작합니다.
이제 :cpp:class:`OGRDataSource` 가 기본적으로 :cpp:class:`GDALDataset` 이기 때문에, 두 경우 모두 1에서 시작합니다. OGR_DS_GetRefCount() API 사용자가 몇 없기를 바랍니다. 필요하다고 판단되는 경우 C API의 예전 습성을 복원할 수도 있지만 C++ 수준에서는 불가능합니다. 참고로 MapServer 또는 QGIS 모두 OGR_DS_GetRefCount()를 사용하지 않습니다.

문서화
------

모든 새 메소드들이 제대로 문서화되었는지 확인하기 위해 문서를 한 번 훑어야 합니다. 변경 사항들을 반영하도록 OGR 일반 문서를 (특히 C++ API 읽기/쓰기 예제, 드라이버 구현 예제 및 OGR 아키텍처 문서를) 업데이트해야 합니다.

테스트
------

기존 자동 테스트 스위트가 계속 통과하도록 거의 변경하지 않았습니다.
GDALOpenEx() API 및 :cpp:class:`OGRDataSource` 로부터 :cpp:class:`GDALDataset` 으로 "가져온" 메소드들에 대한 테스트를 추가했습니다.

버전 번호 매기기
----------------

앞에서 변경 사항들이 C API의 기존 응용 프로그램들에 거의 영향을 미치지 않아야 한다고 설명했지만, 몇몇 습성 변경, C++ 수준 변경 사항들 및 개념 변경은 2.0버전 번호를 매겨도 될 정도라고 생각됩니다.

구현
----

이벤 루올이 구현할 것입니다.

`"통합" 브랜치 <https://github.com/rouault/gdal2/tree/unification>`_ 저장소에 제안한 구현이 있습니다.

변경 사항 목록: `https://github.com/rouault/gdal2/compare/unification <https://github.com/rouault/gdal2/compare/unification>`_

투표 이력
---------

-  유카 라흐코넨 +1
-  프랑크 바르메르담 +1
-  대니얼 모리셋 +1
-  세케레시 터마시 +1
-  이벤 루올 +1

