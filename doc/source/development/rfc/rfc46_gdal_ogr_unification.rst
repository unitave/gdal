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
     But can also be set at driver level because, in practice, layer creation options do not depend on the dataset instance.
     The value of this item is an XML snippet with a format similar to dataset creation options. 
     If specified, the passed creation options to CreateLayer() are validated against that authorized creation option list.
     Below an example of such an authorized open option list in the Shapefile driver.

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

-  The main methods from :cpp:class:`OGRDataSource`  have been moved to :cpp:class:`GDALDataset`  :

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

::

   The following matching C API is available :

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

::

   OGRDataSource definition is now reduced to :

::

   class CPL_DLL OGRDataSource : public GDALDataset
   {
   public:
                           OGRDataSource();

       virtual const char  *GetName() = 0;

       static void         DestroyDataSource( OGRDataSource * );
   };

::

   The existing OGR_DS_* API is preserved. The implementation of those functions
   casts the OGRDataSourceH opaque pointer to GDALDataset*, so it is possible to
   consider GDALDatasetH and OGRDataSourceH as equivalent from the C API point of
   view. Note that it is not true at the C++ level !

-  OGRDataSource::SyncToDisk() has been removed. The equivalent
   functionality should be implemented in existing FlushCache().
   GDALDataset::FlushCache() nows does the job of the previous generic
   implementation of OGRDataSource::SyncToDisk(), i.e. iterate over all
   layers and call SyncToDisk() on them.

-  :cpp:class:`GDALDataset`  has now a protected ICreateLayer() method.

::

       virtual OGRLayer   *ICreateLayer( const char *pszName, 
                                        OGRSpatialReference *poSpatialRef = NULL,
                                        OGRwkbGeometryType eGType = wkbUnknown,
                                        char ** papszOptions = NULL );

::

   This method is what used to be CreateLayer(), i.e. that drivers should
   rename their specialized CreateLayer() implementations as ICreateLayer().
   CreateLayer() is kept at GDALDataset level, but its implementation does a
   prior validation of passed creation options against an optional authorized
   creation option list (GDAL_DS_LAYER_CREATIONOPTIONLIST), before calling
   ICreateLayer() (this is similar to RasterIO() / IRasterIO() )
   A global pass on all in-tree OGR drivers has been made to rename CreateLayer()
   as ICreateLayer(). 

-  GDALOpenEx() is added to be able to open raster-only, vector-only, or
   raster-vector datasets. It accepts read-only/update mode,
   shared/non-shared mode. A list of potential candidate drivers can be
   passed. If NULL, all drivers are probed. A list of open options
   (NAME=VALUE syntax) can be passed. If the list of sibling files has
   already been established, it can also be passed. Otherwise
   GDALOpenInfo will establish it.

::

   GDALDatasetH CPL_STDCALL GDALOpenEx( const char* pszFilename,
                                    unsigned int nOpenFlags,
                                    const char* const* papszAllowedDrivers,
                                    const char* const* papszOpenOptions,
                                    const char* const* papszSiblingFiles );

::

   The nOpenFlags argument is a 'or-able' combination of the following values :

::

   /* Note: we define GDAL_OF_READONLY and GDAL_OF_UPDATE to be on purpose */
   /* equals to GA_ReadOnly and GA_Update */

   /** Open in read-only mode. */
   #define     GDAL_OF_READONLY        0x00
   /** Open in update mode. */
   #define     GDAL_OF_UPDATE          0x01

   /** Allow raster and vector drivers. */
   #define     GDAL_OF_ALL             0x00

   /** Allow raster drivers. */
   #define     GDAL_OF_RASTER          0x02
   /** Allow vector drivers. */
   #define     GDAL_OF_VECTOR          0x04
   /* Some space for GDAL 3.0 new types ;-) */
   /*#define     GDAL_OF_OTHER_KIND1   0x08 */
   /*#define     GDAL_OF_OTHER_KIND2   0x10 */

   /** Open in shared mode. */
   #define     GDAL_OF_SHARED          0x20

   /** Emit error message in case of failed open. */
   #define     GDAL_OF_VERBOSE_ERROR   0x40

::

   The existing GDALOpen(), GDALOpenShared(), OGROpen(), OGROpenShared(),
   OGR_Dr_Open() are just wrappers of GDALOpenEx() with appropriate open flags.
   From the user point of view, their behavior is identical to the existing one,
   i.e. GDALOpen() family will only returns datasets of drivers with declared raster
   capabilities, and similarly with OGROpen() family with vector.

-  GDALOpenInfo class. The following changes are done :

   -  the second argument of the constructor is now nOpenFlags instead
      of GDALAccess, with same semantics as GDALOpenEx(). GDALOpenInfo
      uses the read-only/update bit to "compute" the eAccess flag that
      is heavily used in existing drivers. Drivers with both raster and
      vector capabilities can use the GDAL_OF_VECTOR/GDAL_OF_RASTER bits
      to determine the intent of the caller. For example if a caller
      opens with GDAL_OF_RASTER only and the dataset only contains
      vector data, the driver might decide to not open the dataset (if
      it is a read-only driver. If it is a driver with update
      capability, it should do that only if the opening is done in
      read-only mode).
   -  the open options passed to GDALOpenEx() are stored into a
      papszOpenOptions member of GDALOpenInfo, so that drivers can use
      them.
   -  the "FILE\* fp" member is transformed into "VSILFILE\* fpL". This
      change is motivated by the fact that most popular drivers now use
      the VSI Virtual File API, so they can now directly use the fpL
      member instead of re-opening again the file. A global pass on all
      in-tree GDAL drivers that used fp has been made.
   -  A VSIStatExL() was done previously to determine the nature of the
      file passed. Now, we optimistically begin with a VSIFOpenL(),
      assuming that in most use cases the passed filename is a file. If
      the opening fails, VSIStatExL() is done to determine the nature of
      the filename.
   -  If the requested access mode is update, the opening of the file
      with VSIFOpenL() is done with "rb+" permissions to be directly
      usable.
   -  The papszSiblingFiles member is now private. It is accessed by a
      GetSiblingFiles() method that does the ReadDir() on demand. This
      can speed up the Identify() method that generally does not require
      to know sibling files.
   -  A new method, TryToIngest(), is added to read more than the first
      1024 bytes of a file. This is useful for a few vector drivers,
      like GML or NAS, that must fetch a bit more bytes to be able to
      identify the file.

레이어
~~~~~~

-  :cpp:class:`OGRLayer`  extends :cpp:class:`GDALMajorObject` . Drivers can now define layer
   metadata items that can be retrieved with the usual
   GetMetadata()/GetMetadateItem() API.

-  The GetInfo() method has been removed. It has never been implemented
   in any in-tree drivers and has been deprecated for a long time.

기타
~~~~

-  The deprecated and unused GDALProjDefH and GDALOptionDefinition types
   have been removed from gdal.h

-  GDALGeneralCmdLineProcessor() now interprets the nOptions
   (combination of GDAL_OF_RASTER and GDAL_OF_RASTER) argument as the
   type of drivers that should be displayed with the --formats option.
   If set to 0, GDAL_OF_RASTER is assumed.

-  the --formats option of GDAL utilities outputs whether drivers have
   raster and/or vector capabilities

-  the --format option of GDAL utilities outputs GDAL_DMD_EXTENSIONS,
   GDAL_DMD_OPENOPTIONLIST, GDAL_DS_LAYER_CREATIONOPTIONLIST.

-  OGRGeneralCmdLineProcessor() use GDALGeneralCmdLineProcessor()
   implementation, restricting --formats to vector capable drivers.

드라이버 변경 사항
------------------

-  OGR PCIDSK driver has been merged into GDAL PCIDSK driver.

-  OGR PDF driver has been merged into GDAL PDF driver.

-  A global pass has been made to in-tree OGR drivers that have to open
   a file to determine if they recognize it. They have been converted to
   :cpp:class:`GDALDriver`  to accept a GDALOpenInfo argument and they now use its
   pabyHeader field to examine the first bytes of files. The number of
   system calls realated to file access (open/stat), in order to
   determine that a file is not recognized by any OGR driver, has now
   dropped from 46 in GDAL 1.11 to 1. The converted drivers are :
   AeronavFAA, ArcGEN, AVCBin, AVCE00, BNA, CSV, DGN, EDIGEO, ESRI
   Shapefile, GeoJSON, GeoRSS, GML, GPKG, GPSBabel, GPX, GTM, HTF, ILI1,
   ILI2, KML, LIBKML, MapInfo File, MySQL, NAS, NTF, OpenAIR, OSM, PDS,
   REC, S57, SDTS, SEGUKOOA, SEGY, SOSI, SQLite, SUA, SVG, TIGER, VFK,
   VRT, WFS

-  Long driver description is set for most OGR drivers.

-  All classes deriving from :cpp:class:`OGRLayer`  have been modified to call
   SetDescription() with the value of
   GetName()/poFeatureDefn->GetName(). test_ogrsf tests that it is
   properly set.

-  Following drivers are kept as :cpp:class:`OGRSFDriver` , but their Open() method
   does early extension/prefix testing to avoid datasource object to be
   instantiated : CartoDB, CouchDB, DXF, EDIGEO, GeoConcept, GFT, GME,
   IDRISI, OGDI, PCIDSK, PG, XPlane.

-  Identify() has been implemented for CSV, DGN, DXF, EDIGEO, GeoJSON,
   GML, KML, LIBKML, MapInfo File, NAS, OpenFileGDB, OSM, S57, Shape,
   SQLite, VFK, VRT.

-  GDAL_DMD_EXTENSION/GDAL_DMD_EXTENSIONS set for following drivers:
   AVCE00, BNA, CSV, DGN, DWG, DXF, EDIGEO, FileGDB, Geoconcept,
   GeoJSON, Geomedia, GML, GMT, GPKG, GPX, GPSTrackMaker, IDRISI Vector,
   Interlis 1, Interlis 2, KML, LIBKML, MDB, MapInfo File, NAS, ODS,
   OpenFileGDB, OSM, PGDump, PGeo, REC, S57, ESRI Shapefile, SQLite,
   SVG, WaSP, XLS, XLSX, XPlane.

-  Document dataset and layer creation options of BNA, DGN, FileGDB,
   GeoConccept, GeoJSON, GeoRSS, GML, GPKG, KML, LIBKML, PG, PGDump and
   ESRI Shapefile drivers as GDAL_DMD_CREATIONOPTIONLIST /
   GDAL_DS_LAYER_CREATIONOPTIONLIST.

-  Add open options AAIGRID, PDF, S57 and ESRI Shapefile drivers.

-  GetFileList() implemented in OpenFileGDB, Shapefile and OGR VRT
   drivers.

-  Rename datasource SyncToDisk() as FlushCache() for LIBKML, OCI, ODS,
   XLSX drivers.

-  Use poOpenInfo->fpL to avoid useless file re-opening in GTiff, PNG,
   JPEG, GIF, VRT, NITF, DTED.

-  HTTP driver: declared as GDAL_DCAP_RASTER and GDAL_DCAP_VECTOR
   driver.

-  RIK: implement Identify()

-  Note: the compilation and good working of the following OGR drivers
   (mostly proprietary) could not be tested: ArcObjects, DWG, DODS, SDE,
   FME, GRASS, IDB, OCI, MSSQLSpatial(compilation OK, but not runtime
   tested)

유틸리티 변경 사항
------------------

-  gdalinfo accepts a -oo option to define open options
-  ogrinfo accepts a -oo option to define open options
-  ogr2ogr accepts a -oo option to define input dataset open options,
   and -doo to define destination dataset open options

SWIG 바인딩 변경 사항
---------------------

-  Python and Java bindings:

   -  add new :cpp:class:`GDALDataset`  methods taken from :cpp:class:`OGRDataSource`  :
      CreateLayer(), CopyLayer(), DeleteLayer(), GetLayerCount(),
      GetLayerByIndex(), GetLayerByName(), TestCapability(),
      ExecuteSQL(), ReleaseResultSet(), GetStyleTable() and
      SetStyleTable().
   -  make OGR Driver, DataSource and Layer objects derive from
      MajorObject

-  Perl and CSharp: make sure that it still compiles but some work would
   have to be done by their mainteners to be able to use the new
   capabilities

이 RFC에 포함되지 '않은' 잠재적인 변경 사항들
---------------------------------------------

"Natural" evolutions of current RFC :

-  Unifying the GDAL MEM and OGR Memory drivers.
-  Unifying the GDAL VRT and OGR VRT drivers.

Further unification steps :

-  Source tree changes to move OGR drivers from ogr/ogrsf_frmts/ to
   frmts/ , to move ogr/ogrsf_frmts/generic/\* to gcore/\*, etc...
-  Documentation unification (pages with list of drivers, etc...)
-  Renaming to remove traces of OGR namespace : OGRLayer -> GDALLayer,
   etc...
-  Kill --without-ogr compilation option ? It has been preserved in a
   working state even if it embeds now ogr/ogrsf_frmts/generic and
   ogr/ogrsf_frmts/mitab for conveniency.
-  Unification of some utilities : "gdal info XXX", "gdal convert XXX"
   that would work on all kind of datasets.

하위 호환성
-----------

GDALDriverManager::GetDriverCount(), GetDriver() now returns OGR
drivers, as well as GDAL drivers

The reference counting in GDAL datasets and GDAL 1.X OGR datasources was
a bit different. It starts at 1 for GDAL datasets, and started at 0 for
OGR datasources. Now that :cpp:class:`OGRDataSource`  is basically a :cpp:class:`GDALDataset` , it
starts at 1 for both cases. Hopefully there are very few users of the
OGR_DS_GetRefCount() API. If it was deemed necessary we could restore
the previous behavior at the C API, but that would not be possible at
the C++ level. For reference, neither MapServer nor QGIS use
OGR_DS_GetRefCount().

문서화
------

A pass should be made on the documentation to check that all new methods
are properly documented. The OGR general documentation (especially C++
API Read/Write tutorial, Driver implementation tutorial and OGR
architecture) should be updated to reflect the changes.

테스트
------

Very few changes have been made so that the existing autotest suite
still passes. Additions have been made to test the GDALOpenEx() API and
the methods "imported" from :cpp:class:`OGRDataSource`  into :cpp:class:`GDALDataset` .

버전 번호 매기기
----------------

Although the above describes changes should have very few impact on
existing applications of the C API, some behavior changes, C++ level
changes and the conceptual changes are thought to deserve a 2.0 version
number.

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

