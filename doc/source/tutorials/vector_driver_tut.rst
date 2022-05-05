.. _vector_driver_tut:

================================================================================
벡터 드라이버 구현 예제
================================================================================

.. highlight:: cpp

전반적인 접근법
---------------

일반적으로 새 포맷은 포맷 특화 드라이버를 :cpp:class:`GDALDataset` 클래스와 :cpp:class:`GDALDataset` 및 :cpp:class:`OGRLayer` 의 하위 클래스들을 인스턴스화해서 구현하는 방식으로 OGR에 추가됩니다. :cpp:class:`GDALDriver` 인스턴스는 런타임 시 :cpp:class:`GDALDriverManager` 를 통해 등록됩니다.

OGR 드라이버를 구현하기 위한 이 예제를 따라 하기 전에, :ref:`vector_data_model` 문서를 자세히 살펴봐주십시오.

이 예제는 간단한 아스키 포인트 포맷 구현을 기반으로 할 것입니다.

GDALDriver 구현하기
-------------------

포맷 특화 드라이버 클래스는 :cpp:class:`GDALDriver` 의 인스턴스로 구현됩니다. 일반적으로 드라이버의 인스턴스 하나를 생성하고 :cpp:class:`GDALDriverManager` 를 통해 등록할 것입니다. 드라이버 클래스와 동일한 파일에 위치한 다음과 비숫한 전체 수준 C 호출 가능 등록 함수가 드라이버의 인스턴스화를 처리합니다.

.. code-block::

    void RegisterOGRSPF()
    {
        if( GDALGetDriverByName("SPF") != NULL )
            return;

        GDALDriver *poDriver = new GDALDriver();

        poDriver->SetDescription("SPF");
        poDriver->SetMetadataItem(GDAL_DCAP_VECTOR, "YES");
        poDriver->SetMetadataItem(GDAL_DMD_LONGNAME, "Long name for SPF driver");
        poDriver->SetMetadataItem(GDAL_DMD_EXTENSION, "spf");
        poDriver->SetMetadataItem(GDAL_DMD_HELPTOPIC, "drv_spf.html");

        poDriver->pfnOpen = OGRSPFDriverOpen;
        poDriver->pfnIdentify = OGRSPFDriverIdentify;
        poDriver->pfnCreate = OGRSPFDriverCreate;

        poDriver->SetMetadataItem(GDAL_DCAP_VIRTUALIO, "YES");

        GetGDALDriverManager()->RegisterDriver(poDriver);
    }

:cpp:func:`GDALDriver::SetDescription` 함수가 드라이버 이름을 설정합니다. 데이터소스 생성 시 명령줄에 이 이름을 지정하기 때문에 일반적으로 어떤 특수 문자 또는 공백도 없는 짧은 이름을 설정하는 것이 좋습니다.

드라이버가 벡터 데이터를 처리할 것이라는 사실을 나타내기 위해 ``SetMetadataItem( GDAL_DCAP_VECTOR, "YES" )`` 를 지정합니다.

드라이버가 VSI*L GDAL API로 연 파일을 처리할 수 있다는 사실을 나타내기 위해 ``SetMetadataItem( GDAL_DCAP_VIRTUALIO, "YES" )`` 를 지정합니다. 처리할 수 없다면 이 메타데이터 항목을 정의해서는 안 됩니다.

읽기 또는 읽기 및 업데이트 접근을 (:cpp:func:`Open` 메소드를) 지원하는 그리고 생성을 (:cpp:func:`Create` 메소드를) 지원하는 포맷인 경우 일반적으로 다음과 같이 드라이버를 선언합니다.

.. code-block::

    static GDALDataset* OGRSPFDriverOpen(GDALOpenInfo* poOpenInfo);
    static int          OGRSPFDriverIdentify(GDALOpenInfo* poOpenInfo);
    static GDALDataset* OGRSPFDriverCreate(const char* pszName, int nXSize, int nYSize,
                                        int nBands, GDALDataType eDT, char** papszOptions);

:cpp:func:`GDALOpenEx` 함수가 :cpp:func:`Open` 메소드를 호출합니다. 전송된 파일명의 확장자가 드라이버가 지원하는 포맷의 확장자가 아닌 경우 조용히 NULL을 반환할 것입니다. 전송된 파일명이 대상 포맷의 파일명인 경우, 데이터셋에 대해 새 :cpp:class:`GDALDataset` 객체를 반환할 것입니다.

:cpp:func:`Open` 메소드를 실제 포맷의 :cpp:class:`GDALDataset` 클래스 상의 :cpp:func:`Open` 메소드로 위임하는 것은 흔한 일입니다.

.. code-block::

    static GDALDataset *OGRSPFDriverOpen( GDALOpenInfo* poOpenInfo )
    {
        if( !OGRSPFDriverIdentify(poOpenInfo) )
            return NULL;

        OGRSPFDataSource *poDS = new OGRSPFDataSource();
        if( !poDS->Open(poOpenInfo->pszFilename, poOpenInfo->eAccess == GA_Update) )
        {
            delete poDS;
            return NULL;
        }

        return poDS;
    }

:cpp:func:`Identify` 메소드는 다음과 같이 구현됩니다:

.. code-block::

    static int OGRSPFDriverIdentify( GDALOpenInfo* poOpenInfo )
    {
        // .spf 파일로 보입니까?
        return EQUAL(CPLGetExtension(poOpenInfo->pszFilename), "spf");
    }

:cpp:func:`Create` 메소드의 예시는 생성 및 업데이트에 대한 단락에 있습니다.

데이터소스만 기본 읽기
----------------------

최소한의 읽기 전용 데이터소스를 구현하는 것으로 시작하겠습니다. 작업을 최적화하려는 시도를 하지 않고, :cpp:class:`GDALDataset` 으로부터 상속받은 많은 메소드들의 기본 구현을 사용합니다.

데이터소스의 최우선 책무는 레이어 목록을 관리하는 것입니다. SPF 포맷의 경우 데이터소스가 레이어 하나를 표현하는 단일 파일이기 때문에 최대 1개의 레이어가 존재합니다. 일반적으로 데이터소스의 "이름"은 :cpp:func:`Open` 메소드에 전송되는 이름이어야 합니다.

다음 예시에서 :cpp:func:`Open` 메소드는 기본 클래스 메소드를 대체하지 않지만, 드라이버 클래스가 위임한 열기 작업으로 구현했습니다.

이 간단한 사례에서, 모든 확장 케이퍼빌리티에 대해 FALSE를 반환하는 토막(stub) :cpp:func:`GDALDataset::TestCapability` 함수를 지정합니다. :cpp:func:`TestCapability` 메소드는 순수한 가상 함수이기 때문에 구현할 필요가 없습니다.

.. code-block::

    class OGRSPFDataSource : public GDALDataset
    {
        OGRSPFLayer       **papoLayers;
        int                 nLayers;

    public:
                            OGRSPFDataSource();
                            ~OGRSPFDataSource();

        int                 Open( const char *pszFilename, int bUpdate );

        int                 GetLayerCount() { return nLayers; }
        OGRLayer            *GetLayer( int );

        int                 TestCapability( const char * ) { return FALSE; }
    };

다음 구성자(constructor)는 단순히 기본 상태로 초기화시킵니다. :cpp:func:`Open` 메소드가 파일에 이 구성자를 실제로 추가할 것입니다. 삭제자(destructor)는 레이어를 순서대로 정리(cleanup)하는 역할입니다.

.. code-block::

    OGRSPFDataSource::OGRSPFDataSource()
    {
        papoLayers = NULL;
        nLayers = 0;
    }

    OGRSPFDataSource::~OGRSPFDataSource()
    {
        for( int i = 0; i < nLayers; i++ )
            delete papoLayers[i];
        CPLFree(papoLayers);
    }

:cpp:func:`Open` 메소드가 데이터소스에 대해 가장 중요한 메소드이긴 하지만, 이 특정한 예시에서 :cpp:func:`Open` 메소드가 파일이 원하는 포맷이라고 판단하는 경우 대부분의 작업을 :cpp:func:`OGRSPFLayer` 구성자로 넘깁니다.

:cpp:func:`Open` 메소드가 가능한 한 효율적으로 파일이 식별된 포맷이 아닌지 판단하려 시도해야 한다는 사실을 기억하십시오. 정확한 드라이버를 찾을 때까지 잘못된 포맷의 파일을 가지고 수많은 드라이버를 호출할 수도 있기 때문입니다. 이 특정한 :cpp:func:`Open` 사례에서는 파일 확장자만 테스트하지만 일반적으로는 파일 포맷을 식별하는 데 약한 방법입니다. 사용할 수 있는 경우, 헤더의 "매직 넘버" 또는 그와 비슷한 것을 확인하는 편이 좋습니다.

SPF 포맷의 경우 제자리(in-place) 업데이트를 지원하지 않기 때문에 'bUpdate'가 FALSE인 경우 항상 실패할 것입니다.

.. code-block::

    int  OGRSPFDataSource::Open( const char *pszFilename, int bUpdate )
    {
        if( bUpdate )
        {
            CPLError(CE_Failure, CPLE_OpenFailed,
                    "Update access not supported by the SPF driver.");
            return FALSE;
        }

        // 대응하는 레이어 생성
        nLayers = 1;
        papoLayers = static_cast<OGRSPFLayer **>(CPLMalloc(sizeof(void *)));

        papoLayers[0] = new OGRSPFLayer(pszFilename);

        pszName = CPLStrdup(pszFilename);

        return TRUE;
    }

:cpp:func:`GetLayer` 메소드도 구현해야 합니다. :cpp:func:`Open` 이 레이어 목록을 생성하기 때문에 몇몇 안전성 테스트와 함께 검색하는 것뿐입니다.

.. code-block::

    OGRLayer *OGRSPFDataSource::GetLayer( int iLayer )
    {
        if( iLayer < 0 || iLayer >= nLayers )
            return NULL;

        return papoLayers[iLayer];
    }

레이어만 읽어오기
-----------------

:cpp:class:`OGRSPFLayer` 는 .spf 파일 용 레이어 의미를 구현합니다. 속성 열들의 특정 집합을 이용해서 일관적인 좌표계에 있는 피처 객체 집합에 접근할 수 있습니다. 이 클래스의 정의는 다음과 같습니다:

.. code-block::

    class OGRSPFLayer : public OGRLayer
    {
        OGRFeatureDefn     *poFeatureDefn;
        FILE               *fp;
        int                 nNextFID;

    public:
        OGRSPFLayer( const char *pszFilename );
    ~OGRSPFLayer();

        void                ResetReading();
        OGRFeature *        GetNextFeature();

        OGRFeatureDefn *    GetLayerDefn() { return poFeatureDefn; }

        int                 TestCapability( const char * ) { return FALSE; }
    };

레이어 구성자는 초기화를 담당합니다. 가장 중요한 초기화는 레이어 용 :cpp:class:`OGRFeatureDefn` 클래스를 설정하는 것입니다. 이 클래스가 레이어의 필드 목록, 필드 유형, 도형 유형 및 좌표계를 정의합니다. SPF 포맷에서는 필드 집합이 단일 문자열 필드 하나로 고정되어 있기 때문에 설정할 좌표계 정보가 없습니다.

:cpp:class:`OGRFeatureDefn` 의 참조 개수에 특히 신경을 쓰십시오. 이 레이어를 위한 :cpp:class:`OGRFeature` 도 이 정의를 참조하기 때문에, 레이어 자체의 관점에서도 참조를 확립하는 것이 중요합니다.

.. code-block::

    OGRSPFLayer::OGRSPFLayer( const char *pszFilename )
    {
        nNextFID = 0;

        poFeatureDefn = new OGRFeatureDefn(CPLGetBasename(pszFilename));
        SetDescription(poFeatureDefn->GetName());
        poFeatureDefn->Reference();
        poFeatureDefn->SetGeomType(wkbPoint);

        OGRFieldDefn oFieldTemplate("Name", OFTString);

        poFeatureDefn->AddFieldDefn(&oFieldTemplate);

        fp = VSIFOpenL(pszFilename, "r");
        if( fp == NULL )
            return;
    }

삭제자가 :cpp:class:`OGRFeatureDefn` 에 대해 :cpp:func:`OGRFeatureDefn::Release` 메소드를 사용한다는 사실을 기억하십시오. 삭제자는 참조 개수가 0까지 떨어지면 피처 정의를 삭제할 것이지만, 응용 프로그램이 이 레이어의 피처를 계속 담고 있는 경우 해당 피처가 피처 정의를 가리키는 참조를 담고 있을 것이기 때문에 이때 삭제되지 않을 것입니다. (좋은 일입니다!)

.. code-block::

    OGRSPFLayer::~OGRSPFLayer()
    {
        poFeatureDefn->Release();
        if( fp != NULL )
            VSIFCloseL(fp);
    }

:cpp:func:`OGRLayer::GetNextFeature` 메소드가 일반적으로 :cpp:class:`OGRLayer` 구현의 핵심입니다. 이 메소드는 현재 설치된 공간 및 속성 필터에 따라 다음 피처를 읽어오는 역할입니다.

필터 조건을 만족하는 피처를 찾을 때까지 반복하는 'while()' 루프가 존재합니다. 다음 코드의 첫 번째 부분은 SPF 텍스트 파일의 한 줄을 파싱해서 해당 줄의 'x', 'y' 및 'name'을 확정합니다.

.. code-block::

    OGRFeature *OGRSPFLayer::GetNextFeature()
    {
        // 요구 사항을 만족하는 피처를 찾을 때까지 반복
        while( true )
        {
            const char *pszLine = CPLReadLineL(fp);

            // 파일의 마지막인가(피처가 더 이상 없는가)?
            if( pszLine == NULL )
                return NULL;

            const double dfX = atof(pszLine);

            pszLine = strstr(pszLine,"|");
            if( pszLine == NULL )
                continue; // 오류를 발생시켜야 함!
            else
                pszLine++;

            const double dfY = atof(pszLine);

            pszLine = strstr(pszLine,"|");

            const char *pszName = NULL;
            if( pszLine == NULL )
                continue; // 오류를 발생시켜야 함!
            else
                pszName = pszLine + 1;

그 다음 부분은 'x', 'y' 및 'name'을 피처로 변환합니다. 또한 선형적으로 증가하는 피처ID를 할당한다는 사실도 기억하십시오. 이 경우 첫 번째 피처의 피처ID를 0에서 시작했지만, 1에서 시작하는 드라이버들도 있습니다.

.. code-block::

        OGRFeature *poFeature = new OGRFeature(poFeatureDefn);

        poFeature->SetGeometryDirectly(new OGRPoint(dfX, dfY));
        poFeature->SetField(0, pszName);
        poFeature->SetFID(nNextFID++);

다음으로, 필터가 존재하는 경우 피처가 현재 속성 또는 공간 필터를 만족하는지 확인합니다. :cpp:class:`OGRLayer` 기반 클래스가 :cpp:class:`OGRLayer` 멤버 필드 :cpp:member:`OGRLayer::m_poFilterGeom` (공간 필터) 및 :cpp:member:`OGRLayer::m_poAttrQuery` (속성 필터)에 필터를 유지/관리하기 때문에, 여기에서는 그 값들이 NULL이 아니라면 그냥 해당 값을 사용하면 됩니다. 다음 테스트는 본질적으로 "저장된 값(stock)"이기 때문에 모든 포맷에 동일하게 작동합니다. 일부 포맷은 공간 색인을 이용해서 사전에 몇몇 공간 필터링을 하기도 합니다.

피처가 필터 조건을 만족하는 경우 해당 피처를 반환합니다. 만족하지 않는 경우 피처를 삭제하고 루프의 맨 위로 돌아가서 시도할 다른 피처를 가져옵니다.

.. code-block::

            if( (m_poFilterGeom == NULL ||
                FilterGeometry(poFeature->GetGeometryRef())) &&
                (m_poAttrQuery == NULL ||
                m_poAttrQuery->Evaluate(poFeature)) )
                return poFeature;

            delete poFeature;
        }
    }

레이어로부터 피처 집합을 읽어오는 동안, 또는 응용 프로그램이 :cpp:func:`OGRLayer::ResetReading` 메소드를 호출할 수 있는 때라면 언제라도 이 메소드를 호출해서 피처 집합의 처음부터 읽기를 다시 시작합니다. 파일의 처음으로 돌아가 검색하고 피처ID 계수기(counter)를 리셋하도록 해서 이 메소드를 구현합니다.

.. code-block::

    void OGRSPFLayer::ResetReading()
    {
        VSIFSeekL(fp, 0, SEEK_SET);
        nNextFID = 0;
    }

이 구현에서 :cpp:func:`GetFeature` 메소드를 위한 사용자 지정 구현을 제공하지 않습니다. 다시 말해 특정 피처의 피처ID로 피처를 읽어오려는 시도는 원하는 피처를 찾을 때까지 :cpp:func:`GetNextFeature` 를 수없이 호출하게 될 것이라는 의미입니다. 하지만 어차피 SPF 포맷 같은 순차 텍스트 포맷에서는 할 수 있는 일이 별로 없습니다.

끝났습니다! 간단한 읽기 전용 피처 파일 포맷 드라이버 구현을 완료했습니다.

