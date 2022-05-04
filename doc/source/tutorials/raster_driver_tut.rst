.. _raster_driver_tut:

================================================================================
래스터 드라이버 구현 예제
================================================================================

.. highlight:: cpp

전반적인 접근법
---------------

일반적으로 새 포맷은 포맷 특화 드라이버를 :cpp:class:`GDALDataset` 클래스의 하위 클래스로, 밴드 접근자(accessor)를 :cpp:class:`GDALRasterBand` 클래스의 하위 클래스로 구현해서 GDAL에 추가됩니다. 또한 시스템이 해당 포맷에 관해 알고 있도록 보장하기 위해 포맷을 위한 :cpp:class:`GDALDriver` 인스턴스를 생성한 다음 :cpp:class:`GDALDriverManager` 로 등록합니다.

이 예제에서는 (JDEM 드라이버를 기반으로) 단순한 읽기 전용 드라이버를 구현한 다음 :cpp:class:`RawRasterBand` 도우미 클래스를 활용해서 생성 가능하고 업데이트 가능한 포맷을 구현합니다. 몇몇 난해한 문제점들도 논의할 것입니다.

GDAL 드라이버를 구현하려 시도하기 전에 :ref:`raster_data_model` 을 살펴보고 이해할 것을 강력히 권장합니다.

데이터셋 구현하기
-----------------

일본 DEM 포맷(`jdemdataset.cpp <https://github.com/OSGeo/gdal/blob/master/frmts/jdem/jdemdataset.cpp>`_) 용 읽기 전용 드라이버를 최소한으로 구현하는 방법으로 시작하겠습니다. 먼저 포맷 특화 데이터셋 클래스를, 이 경우 :cpp:class:`JDEMDataset` 을 선언합니다:

.. code-block:: c++

    class JDEMDataset : public GDALPamDataset
    {
        friend class JDEMRasterBand;
        FILE        *fp;
        GByte       abyHeader[1012];

    public:
                    ~JDEMDataset();
        static GDALDataset *Open( GDALOpenInfo * );
        static int          Identify( GDALOpenInfo * );
        CPLErr      GetGeoTransform( double * padfTransform );
        const char *GetProjectionRef();
    };

일반적으로 :cpp:class:`GDALDataset` 기본 클래스에 대해 다양한 가상 메소드를 대체해서 드라이버에 케이퍼빌리티를 제공합니다. 하지만 :cpp:func:`Open` 메소드는 특별합니다. 이 메소드는 기본 클래스에 대한 가상 메소드가 아니며, 이 작업에 독립형 함수가 필요할 것이기 때문에 이 메소드를 정적이라고 선언합니다. :cpp:func:`Open` 메소드를 JDEMDataset 안의 메소드로 구현하면 편리합니다. 데이터셋 객체의 콘텐츠를 수정할 수 있는 권한을 가지고 접근할 수 있기 때문입니다.

``Open()`` 메소드 자체는 다음처럼 보일 수도 있습니다:

.. code-block:: c++

    GDALDataset *JDEMDataset::Open( GDALOpenInfo *poOpenInfo )
    {
        // 헤더가 JDEM 데이터셋과 호환되는지 확인합니다.
        if( !Identify(poOpenInfo) )
            return NULL;

        // 요구되는 접근을 지원하는지 확인합니다.
        if( poOpenInfo->eAccess == GA_Update )
        {
            CPLError(CE_Failure, CPLE_NotSupported,
                    "The JDEM driver does not support update access to existing "
                    "datasets.");
            return NULL;
        }

        // GDALOpenInfo* 로부터 나온 파일 포인터를 사용할 수 있는지 확인합니다.
        if( poOpenInfo->fpL == NULL )
        {
            return NULL;
        }

        // 대응하는 GDALDataset을 생성합니다.
        JDEMDataset *poDS = new JDEMDataset();

        // GDALOpenInfo* 로부터 파일 포인터를 빌려옵니다.
        poDS->fp = poOpenInfo->fpL;
        poOpenInfo->fpL = NULL;

        // 헤더를 읽어옵니다.
        VSIFReadL(poDS->abyHeader, 1, 1012, poDS->fp);
        poDS->nRasterXSize =
            JDEMGetField(reinterpret_cast<char *>(poDS->abyHeader) + 23, 3);
        poDS->nRasterYSize =
            JDEMGetField(reinterpret_cast<char *>(poDS->abyHeader) + 26, 3);
        if( poDS->nRasterXSize <= 0 || poDS->nRasterYSize <= 0 )
        {
            CPLError(CE_Failure, CPLE_AppDefined,
                    "Invalid dimensions : %d x %d",
                    poDS->nRasterXSize, poDS->nRasterYSize);
            delete poDS;
            return NULL;
        }

        // 밴드 정보 객체를 생성합니다.
        poDS->SetBand(1, new JDEMRasterBand(poDS, 1));

        // 모든 PAM 정보를 초기화합니다.
        poDS->SetDescription(poOpenInfo->pszFilename);
        poDS->TryLoadXML();

        // 기본 오버뷰들을 초기화합니다.
        poDS->oOvManager.Initialize(poDS, poOpenInfo->pszFilename);
        return poDS;
    }

모든 데이터베이스 :cpp:func:`Open` 함수에서 첫 번째 단계는 전송되는 파일이 실제로 해당 드라이버 용 포맷인지 검증하는 것입니다. 하나가 성공할 때까지 각 드라이버의 :cpp:func:`Open` 함수를 차례로 호출한다는 사실을 아는 것이 중요합니다. 전송되는 파일이 자신의 포맷이 아닌 경우 드라이버가 조용히 NULL을 반환해야만 합니다. 전송되는 파일이 드라이버가 지원하는 포맷으로 보이기는 하지만 어떤 이유 때문에 지원할 수 없거나 오류가 발생하는 경우에만 오류를 발생시켜야 합니다. 열어야 할 파일에 대한 정보는 :cpp:class:`GDALOpenInfo` 객체에 담아 전송됩니다. :cpp:class:`GDALOpenInfo` 클래스는 다음 공개 데이터 멤버들을 포함합니다:

   -  char       \*pszFilename;
   -  char\**    papszOpenOptions;
   -  GDALAccess eAccess;  // GA_ReadOnly 또는 GA_Update
   -  int        nOpenFlags;
   -  int        bStatOK;
   -  int        bIsDirectory;
   -  VSILFILE   \*fpL;
   -  int        nHeaderBytes;
   -  GByte      \*pabyHeader;

해당 파일을 지원하는지 판단하기 위해 드라이버가 이 공개 데이터를 검사할 수 있습니다. 'pszFilename'이 파일 시스템에 있는 객체를 참조하는 경우, 'bStatOK' 플래그가 TRUE로 설정될 것입니다. 마찬가지로 파일을 성공적으로 열었다면 처음 몇 KB를 읽어와서 정확히 'nHeaderBytes' 용량을 가진 'pabyHeader'에 넣습니다.

이 전형적인 테스트 작업 예시에서, 파일을 성공적으로 열었고, 테스트를 수행하기 위해 최소한으로 필요한 헤더 정보를 가지고 있으며, 해당 포맷에 예상되는 다양한 헤더 부분들이 존재한다는 사실을 검증했습니다. 이 경우 JDEM 포맷에 매직 넘버가 존재하지 않기 때문에 타당한 세기(century) 값을 가졌다고 보장하기 위해 다양한 날짜 필드들을 확인합니다. 이 테스트가 실패하는 경우, 이 파일을 지원하지 않는다는 사실을 나타내는 NULL을 조용히 반환합니다.

실제로는 식별 작업을 :cpp:func:`Identify` 정적 함수에 위임합니다:

.. code-block:: c++

    /************************************************************************/
    /*                              Identify()                              */
    /************************************************************************/
    int JDEMDataset::Identify( GDALOpenInfo * poOpenInfo )
    {
        // 헤더의 예상 위치에 날짜로 보이는 내용이 있는지 확인합니다.
        // 안타깝게도 상대적으로 엉성한 테스트입니다.
        if( poOpenInfo->nHeaderBytes < 50 )
            return FALSE;

        // 세기(century) 값이 타당하게 보이는지 확인합니다.
        const char *psHeader = reinterpret_cast<char *>(poOpenInfo->pabyHeader);
        if( (!EQUALN(psHeader + 11, "19", 2) &&
            !EQUALN(psHeader + 11, "20", 2)) ||
            (!EQUALN(psHeader + 15, "19", 2) &&
            !EQUALN(psHeader + 15, "20", 2)) ||
            (!EQUALN(psHeader + 19, "19", 2) &&
            !EQUALN(psHeader + 19, "20", 2)) )
        {
            return FALSE;
        }
        return TRUE;
    }

"이 포맷을 지원하는가" 테스트를 가능한 한 엄격하게 만드는 것이 중요합니다. 이 특정한 예시에서 테스트가 엉성하기 때문에 몇몇 위치에 19 또는 20이라는 값을 우연히 가지고 있는 파일을 JDEM 포맷으로 잘못 인식할 수 있습니다. 당연히 해당 파일을 제대로 처리하지 못 할 것입니다.
파일이 지원하는 포맷으로 검증되었다면, 해당 파일을 사용할 수 있는지, 그리고 특히 원하는 접근 수준을 지정할 수 있는지 검증하기 위해 필요한 다른 모든 테스트를 수행할 수 있습니다. JDEM 드라이버가 업데이트를 지원하지 않기 때문에 업데이트를 시도하는 경우 오류가 발생할 것입니다.

.. code-block:: c++

    if( poOpenInfo->eAccess == GA_Update )
    {
        CPLError(CE_Failure, CPLE_NotSupported,
                 "The JDEM driver does not support update access to existing "
                 "datasets.");
        return NULL;
    }

그 다음 단계에서는 다양한 관심 정보를 설정할 데이터베이스 클래스의 인스턴스를 생성해야 합니다.

.. code-block:: c++

    // GDALOpenInfo* 로부터 나온 파일 포인터를 사용할 수 있는지 확인합니다.
    if( poOpenInfo->fpL == NULL )
    {
        return NULL;
    }
    JDEMDataset *poDS = new JDEMDataset();

    // GDALOpenInfo* 로부터 파일 포인터를 빌려옵니다.
    poDS->fp = poOpenInfo->fpL;
    poOpenInfo->fpL = NULL;

이 단계에서 :cpp:class:`GDALOpenInfo*` 클래스가 담고 있는 파일 핸들(handle)을 "빌려옵니다". 이 파일 포인터는 디스크 상에 있는 파일에 접근하기 위해 VSI*L GDAL API를 사용합니다. 이 가상화 POSIX 스타일 API는 대용량 파일, 인메모리 파일 및 ZIP 압축 파일을 지원하는 등 몇몇 특수 케이퍼빌리티를 제공합니다.

그 다음, 헤더로부터 X 및 Y 크기를 추출합니다. 'nRasterXSize' 및 'nRasterYSize'가 :cpp:class:`GDALDataset` 기본 클래스로부터 상속된 데이터 필드로, :cpp:func:`Open` 메소드로 설정되어야만 합니다.

.. code-block:: c++

    VSIFReadL(poDS->abyHeader, 1, 1012, poDS->fp);
    poDS->nRasterXSize =
        JDEMGetField(reinterpret_cast<char *>(poDS->abyHeader) + 23, 3);
    poDS->nRasterYSize =
        JDEMGetField(reinterpret_cast<char *>(poDS->abyHeader) + 26, 3);
    if  (poDS->nRasterXSize <= 0 || poDS->nRasterYSize <= 0 )
    {
        CPLError(CE_Failure, CPLE_AppDefined,
                "Invalid dimensions : %d x %d",
                poDS->nRasterXSize, poDS->nRasterYSize);
        delete poDS;
        return NULL;
    }

:cpp:func:`SetBand` 메소드를 이용해서 이 데이터셋에 관련된 모든 밴드들을 생성하고 추가해야만 합니다. 곧 :cpp:class:`JDEMRasterBand` 클래스를 탐구할 것입니다.

.. code-block:: c++

    // 밴드 정보 객체를 생성합니다.
    poDS->SetBand(1, new JDEMRasterBand(poDS, 1));

마지막으로 데이터셋 객체에 이름을 할당하고, 사용할 수 있는 경우 .aux.xml 파일로부터 보조 정보를 초기화할 수 있는 :cpp:func:`GDALPamDataset::TryLoadXML` 메소드를 호출합니다. 이런 서비스들에 대해 더 자세히 알고 싶다면 :cpp:class:`GDALPamDataset` 및 관련 클래스들을 살펴보십시오.

.. code-block:: c++

        // 모든 PAM 정보를 초기화합니다.
        poDS->SetDescription( poOpenInfo->pszFilename );
        poDS->TryLoadXML();
        return poDS;
    }

RasterBand 구현하기
-------------------

:cpp:class:`GDALDataset` 으로부터 하위 클래스로 파생된 사용자 지정 :cpp:class:`JDEMDataset` 클래스와 비슷하게, JDEM 파일의 밴드(들)에 접근하려면 :cpp:class:`GDALRasterBand` 클래스로부터 파생된 사용자 지정 :cpp:class:`JDEMRasterBand` 클래스도 선언하고 구현해야 합니다. :cpp:class:`JDEMRasterBand` 의 경우 다음과 같이 선언합니다:

.. code-block:: c++

    class JDEMRasterBand : public GDALPamRasterBand
    {
    public:
        JDEMRasterBand( JDEMDataset *, int );
        virtual CPLErr IReadBlock( int, int, void * );
    };

구성자(constructor)는 어떤 서명이든 가질 수 있고, :cpp:func:`Open` 메소드에서만 호출됩니다. :cpp:func:`GDALRasterBand::IReadBlock` 같은 다른 가상 메소드는 "gdal_priv.h" 파일에 있는 메소드 서명과 정확히 일치해야만 합니다.

구성자(constructor)는 다음과 같이 구현합니다:

.. code-block:: c++

    JDEMRasterBand::JDEMRasterBand( JDEMDataset *poDSIn, int nBandIn )
    {
        poDS = poDSIn;
        nBand = nBandIn;
        eDataType = GDT_Float32;
        nBlockXSize = poDS->GetRasterXSize();
        nBlockYSize = 1;
    }

:cpp:class:`GDALRasterBand` 클래스로부터 다음 데이터 멤버들을 상속하고, 일반적으로 밴드 구성자에 설정해야 합니다.

   -  poDS: 상위 GDALDataset을 가리키는 포인터입니다.
   -  nBand: 데이터셋 안에 있는 밴드의 개수입니다.
   -  eDataType: 해당 밴드에 있는 픽셀의 데이터 유형입니다.
   -  nBlockXSize: 해당 밴드에 있는 블록 하나의 너비입니다.
   -  nBlockYSize: 해당 밴드에 있는 블록 하나의 높이입니다.

가능한 :cpp:class:`GDALDataType` 값의 전체 목록은 "gdal.h" 파일에 선언되어 있고, GDT_Byte, GDT_UInt16, GDT_Int16, 및 GDT_Float32 유형을 포함합니다. 블록 크기는 데이터에 접근하기 위해 자연스럽거나 효율적인 블록 크기를 확립하는 데 사용됩니다. 타일화 데이터셋의 경우 블록 크기가 타일의 크기일 것이지만 다른 대부분의 데이터셋의 경우 이 예시에서와 마찬가지로 블록 크기가 스캔라인 한 줄의 크기일 것입니다.

다음은 실제로 이미지 데이터를 읽어오는 코드 :cpp:func:`IReadBlock` 을 구현하는 예시입니다:

.. code-block:: c++

    CPLErr JDEMRasterBand::IReadBlock( int nBlockXOff, int nBlockYOff,
                                    void * pImage )
    {
        JDEMDataset *poGDS = static_cast<JDEMDataset *>(poDS);
        int nRecordSize = nBlockXSize * 5 + 9 + 2;
        VSIFSeekL(poGDS->fp, 1011 + nRecordSize*nBlockYOff, SEEK_SET);
        char *pszRecord = static_cast<char *>(CPLMalloc(nRecordSize));
        VSIFReadL(pszRecord, 1, nRecordSize, poGDS->fp);
        if( !EQUALN(reinterpret_cast<char *>(poGDS->abyHeader), pszRecord, 6) )
        {
            CPLFree(pszRecord);
            CPLError(CE_Failure, CPLE_AppDefined,
                    "JDEM Scanline corrupt.  Perhaps file was not transferred "
                    "in binary mode?");
            return CE_Failure;
        }
        if( JDEMGetField(pszRecord + 6, 3) != nBlockYOff + 1 )
        {
            CPLFree(pszRecord);
            CPLError(CE_Failure, CPLE_AppDefined,
                    "JDEM scanline out of order, JDEM driver does not "
                    "currently support partial datasets.");
            return CE_Failure;
        }
        for( int i = 0; i < nBlockXSize; i++ )
            ((float *) pImage)[i] = JDEMGetField(pszRecord + 9 + 5 * i, 5) * 0.1;
        return CE_None;
    }

다음 중요 항목들을 기억해둘 만합니다:

-  일반적으로 :cpp:class:`GDALRasterBand::poDS` 클래스 멤버를 이 클래스를 소유한 데이터셋의 파생 유형으로 캐스트합니다. 사용자의 RasterBand 클래스가 이 클래스를 소유한 데이터셋 객체에 접근하기 위한 권한이 필요할 경우, RasterBand 클래스를 `friend <https://docs.microsoft.com/ko-kr/cpp/cpp/friend-cpp?view=msvc-170>`_ 로 선언했는지 확인하십시오. (앞의 예시에서는 간결함을 위해 생략했습니다.)

-  오류가 발생하는 경우, :cpp:func:`CPLError` 로 리포트하고 CE_Failure를 반환하십시오. 오류가 발생하지 않는다면 CE_None을 반환하십시오.

-  'pImage' 버퍼를 데이터의 블록 하나로 채워야 합니다. 이 블록의 크기는 래스터 밴드에 'nBlockXSize'와 'nBlockYSize'로 선언된 크기입니다. 'pImage' 내부의 데이터 유형은 래스터 밴드 객체에 'eDataType'으로 선언된 유형과 일치해야 합니다.

-  'nBlockXOff' 및 'nBlockYOff'는 블록 오프셋이기 때문에, 128x128 크기의 타일화 데이터셋의 값이 1인 경우 (128,128)에서 (255,255)까지의 블록을 불러와야 합니다.

드라이버
--------

이제 이미지 데이터를 읽어오기 위해 사용할 :cpp:class:`JDEMDataset` 과 :cpp:class:`JDEMRasterBand` 가 준비되었긴 하지만, GDAL 시스템이 어떻게 새 드라이버에 관해 알고 있는지 명확하지 않습니다. :cpp:class:`GDALDriverManager` 클래스를 통해 이를 달성합니다. 새 포맷을 등록하기 위해 등록(registration) 함수를 구현하십시오. :file:`gcore/gdal_frmts.h` 에 다음과 같이 선언합니다:

.. code-block:: c++

    void CPL_DLL GDALRegister_JDEM(void);

드라이버 파일에 다음과 같이 정의합니다:

.. code-block:: c++

    void GDALRegister_JDEM()
    {
        if( !GDAL_CHECK_VERSION("JDEM") )
            return;

        if( GDALGetDriverByName("JDEM") != NULL )
            return;

        GDALDriver *poDriver = new GDALDriver();
        poDriver->SetDescription("JDEM");
        poDriver->SetMetadataItem(GDAL_DCAP_RASTER, "YES");
        poDriver->SetMetadataItem(GDAL_DMD_LONGNAME,
                                "Japanese DEM (.mem)");
        poDriver->SetMetadataItem(GDAL_DMD_HELPTOPIC,
                                "frmt_various.html#JDEM");
        poDriver->SetMetadataItem(GDAL_DMD_EXTENSION, "mem");
        poDriver->SetMetadataItem(GDAL_DCAP_VIRTUALIO, "YES");
        poDriver->pfnOpen = JDEMDataset::Open;
        poDriver->pfnIdentify = JDEMDataset::Identify;
        GetGDALDriverManager()->RegisterDriver(poDriver);
    }

``GDAL_CHECK_VERSION`` 매크로를 사용한다는 사실을 기억하십시오. 외부 라이브러리에 의존하지 않는 GDAL 트리 안에 있는 드라이버에 대한 선택적인 매크로이지만, 사용자 드라이버를 플러그인으로 (다시 말해 트리 바깥에 있는 드라이버로) 컴파일하는 경우 매우 유용할 수 있습니다. GDAL C++ ABI가 GDAL 배포판들 사이에 (예를 들어 GDAL 1.x버전과 1.y버전 사이에) 변경될 수도 있고 변경될 것이기 때문에, 사용자 드라이버를 사용자가 작업하고자 하는 GDAL 버전의 헤더 파일을 대상으로 다시 컴파일해야 할 수도 있습니다. ``GDAL_CHECK_VERSION`` 매크로가 드라이버가 컴파일된 GDAL 버전과 드라이버가 실행되는 GDAL 버전이 호환되는지 확인할 것입니다.

등록 함수를 처음 호출하면 :cpp:class:`GDALDriver` 객체의 인스턴스를 생성한 다음 :cpp:class:`GDALDriverManager` 로 등록할 것입니다. :cpp:class:`GDALDriverManager` 로 등록하기 전에 드라이버에 다음 필드들을 설정할 수 있습니다.

- 설명(description)은 포맷의 단축명입니다. 이 포맷의 유일한 이름으로, 스크립트 및 명령줄 프로그램에서 드라이버를 식별하기 위해 사용되는 경우가 많습니다. 일반적으로 문자 3~5개 길이이고 포맷 클래스의 접두어와 일치해야 합니다. (필수)

- GDAL_DCAP_RASTER:
  이 드라이버가 래스터 데이터를 처리한다는 사실을 나타내려면 YES로 설정하십시오. (필수)

- GDAL_DMD_LONGNAME:
  파일 포맷의 더 긴 서술적인 이름이지만, 그래도 문자 50~60개 길이를 넘지 않습니다. (필수)

- GDAL_DMD_HELPTOPIC:
  (하나라도 존재하는 경우) 이 드라이버를 위해 출력할 도움말 주제의 이름입니다. 이 경우 JDEM 포맷이 :file:`gdal/html` 에 있는 다양한 포맷 웹페이지 안에 담겨 있습니다. (선택적)

- GDAL_DMD_EXTENSION:
  이 유형의 파일에 사용되는 확장자입니다. 하나 이상인 경우 최우선 확장자를 선택하거나, 하나도 선택하지 마십시오. (선택적)

- GDAL_DMD_MIMETYPE:
  이 파일 포맷의 -- "image/png" 같은 -- 표준 미디어 유형(MIME)입니다. (선택적)

- GDAL_DMD_CREATIONOPTIONLIST:
  생성 옵션을 설명하는 메커니즘에 대한 작업이 진화하고 있습니다. 이에 대한 예시를 보고 싶다면 GeoTIFF 드라이버를 참조하십시오. (선택적)

- GDAL_DMD_CREATIONDATATYPES:
  새 데이터셋을 생성하는 경우 해당 데이터셋이 지원하는 데이터 유형을 공백으로 구분한 목록입니다. :cpp:func:`Create` 메소드가 존재한다면, 이 데이터 유형들을 지원할 것입니다. :cpp:func:`CreateCopy` 메소드가 존재하는 경우, 비손실 내보내기할 수 있는 유형들의 목록일 것이지만 실제로 작성되는 유형보다 더 엉성한 유형을 포함할 수도 있습니다. 예를 들어, :cpp:func:`CreateCopy` 메소드가 지원하고 항상 Float32 유형으로 작성되는 포맷의 지원 유형 목록에 Byte, Int16 및 UInt16가 포함될 수도 있습니다. 이 유형들이 Float32 유형으로 비손실 변환될 수 있기 때문입니다. 예시: "Byte Int16 UInt16" (드라이버가 생성을 지원하는 경우 필수)

- GDAL_DCAP_VIRTUALIO:
  아 드라이버가 VSI*L GDAL API로 연 파일을 처리할 수 있다는 사실을 나타내려면 YES로 설정하십시오. 처리할 수 없다면 이 메타데이터 항목을 정의해서는 안 됩니다. (선택적)

- pfnOpen:
  이 포맷의 파일을 열기 위해 호출할 함수입니다. (선택적)

- pfnIdentify:
  이 포맷의 파일을 식별하기 위해 호출할 함수입니다. 드라이버가 해당 파일을 지원하는 포맷으로 인식하는 경우 1을 반환하고, 지원하지 **않는** 포맷으로 인식하는 경우 0을 반환하며, 헤더 바이트들을 검사하는 것만으로는 확실히 판단할 수 없는 경우 -1을 반환할 것입니다. (선택적)

- pfnCreate:
  이 포맷으로 된, 업데이트 가능한 새 데이터셋을 생성하기 위해 호출할 함수입니다. (선택적)

- pfnCreateCopy:
  이 포맷으로 된, 업데이트 가능할 필요는 없는 새 데이터셋을 또다른 소스로부터 복사해서 생성하기 위해 호출할 함수입니다. (선택적)

- pfnDelete:
  이 포맷으로 된 데이터셋을 삭제하기 위해 호출할 함수입니다. (선택적)

- pfnUnloadDriver:
  드라이버를 삭제하는 경우에만 호출하는 함수입니다. 드라이버 수준에서 데이터를 정리(cleanup)하기 위해 사용할 수 있습니다. 거의 사용되지 않습니다. (선택적)

GDAL 트리에 드라이버 추가하기
-----------------------------

JDEM 드라이버에 접근하기 위해서는 더 상위 수준에서 :cpp:func:`GDALRegister_JDEM` 메소드를 호출해야만 한다는 사실을 기억하십시오. 다음은 새 드라이버를 작성하는 일반적인 과정입니다:

-  :file:`gdal/frmts` 아래 단축명과 동일한 이름을 가진 드라이버 디렉터리를 추가하십시오.

-  해당 디렉터리에 다른 비슷한 디렉터리의 (예: 'jdem' 디렉터리의) 해당 파일들을 따라 :file:`GNUmakefile` 및 :file:`makefile.vc` 파일을 추가하십시오.

-  데이터셋과 래스터밴드를 구현한 모듈을 추가하십시오. 일반적으로 :file:`<short_name>dataset.cpp` 라는 이름을 가진 파일입니다. 이 파일 하나에 -- 모든 코드를 필수적으로 담을 필요는 없지만 -- 모든 GDAL 특화 코드를 담고 있습니다.

-  :file:`gdal/gcore/gdal_frmts.h` 에 등록 엔트리 포인트 선언을 (예: :cpp:func:`GDALRegister_JDEM`) 추가하십시오.

-  :file:`frmts/gdalallregister.cpp` 에 알맞은 "#ifdef"로 보호받는 등록 함수 호출을 추가하십시오.

-  :file:`GDALmake.opt.in` (그리고 :file:`GDALmake.opt`)에 있는 ``GDAL_FORMATS`` 매크로에 포맷 단축명을 추가하십시오.

-  :file:`frmts/makefile.vc` 에 있는 ``EXTRAFLAGS`` 매크로에 포맷 특화 항목을 추가하십시오.

이 모든 과정을 완료하고 GDAL을 다시 빌드하고 나면, 모든 유틸리티에서 새 포맷을 사용할 수 있게 될 것입니다. :ref:`gdalinfo` 유틸리티를 사용해서 새 포맷을 열고 관련 정보를 리포트할 수 있는지 테스트할 수 있습니다. :ref:`gdal_translate` 유틸리티를 사용하면 이미지를 읽어올 수 있는지 테스트할 수 있습니다.

지리참조 정보 추가하기
----------------------

Now we will take the example a step forward, adding georeferencing support. We add the following two virtual method overrides to JDEMDataset, taking care to exactly match the signature of the method on the GDALDataset base class.

.. code-block:: c++

    CPLErr      GetGeoTransform( double * padfTransform );
    const char *GetProjectionRef();

The implementation of :cpp:func:`GDALDataset::GetGeoTransform` just copies the usual geotransform matrix into the supplied buffer. Note that :cpp:func:`GDALDataset::GetGeoTransform` may be called a lot, so it isn't generally wise to do a lot of computation in it. In many cases the Open() will collect the geotransform, and this method will just copy it over. Also note that the geotransform return is based on an anchor point at the top left corner of the top left pixel, not the center of pixel approach used in some packages.

.. code-block:: c++

    CPLErr JDEMDataset::GetGeoTransform( double * padfTransform )
    {
        const char *psHeader = reinterpret_cast<char *>(abyHeader);
        const double dfLLLat = JDEMGetAngle(psHeader + 29);
        const double dfLLLong = JDEMGetAngle(psHeader + 36);
        const double dfURLat = JDEMGetAngle(psHeader + 43);
        const double dfURLong = JDEMGetAngle(psHeader + 50);
        padfTransform[0] = dfLLLong;
        padfTransform[3] = dfURLat;
        padfTransform[1] = (dfURLong - dfLLLong) / GetRasterXSize();
        padfTransform[2] = 0.0;
        padfTransform[4] = 0.0;
        padfTransform[5] = -1 * (dfURLat - dfLLLat) / GetRasterYSize();
        return CE_None;
    }

The :cpp:func:`GDALDataset::GetProjectionRef` method returns a pointer to an internal string containing a coordinate system definition in OGC WKT format. In this case the coordinate system is fixed for all files of this format, but in more complex cases a definition may need to be composed on the fly, in which case it may be helpful to use the :cpp:class:`OGRSpatialReference` class to help build the definition.

.. code-block:: c++

    const char *JDEMDataset::GetProjectionRef()
    {
        return
            "GEOGCS[\"Tokyo\",DATUM[\"Tokyo\",SPHEROID[\"Bessel 1841\","
            "6377397.155,299.1528128,AUTHORITY[\"EPSG\",7004]],TOWGS84[-148,"
            "507,685,0,0,0,0],AUTHORITY[\"EPSG\",6301]],PRIMEM[\"Greenwich\","
            "0,AUTHORITY[\"EPSG\",8901]],UNIT[\"DMSH\",0.0174532925199433,"
            "AUTHORITY[\"EPSG\",9108]],AXIS[\"Lat\",NORTH],AXIS[\"Long\",EAST],"
            "AUTHORITY[\"EPSG\",4301]]";
    }

This completes explanation of the features of the JDEM driver. The full source for jdemdataset.cpp can be reviewed as needed.

Overviews
---------

GDAL allows file formats to make pre-built overviews available to applications via the :cpp:func:`GDALRasterBand::GetOverview` and related methods. However, implementing this is pretty involved, and goes beyond the scope of this document for now. The GeoTIFF driver (gdal/frmts/gtiff/geotiff.cpp) and related source can be reviewed for an example of a file format implementing overview reporting and creation support.

Formats can also report that they have arbitrary overviews, by overriding the :cpp:func:`GDALRasterBand::HasArbitraryOverviews` method on the GDALRasterBand, returning TRUE. In this case the raster band object is expected to override the :cpp:func:`GDALRasterBand::RasterIO` method itself, to implement efficient access to imagery with resampling. This is also involved, and there are a lot of requirements for correct implementation of the RasterIO() method. An example of this can be found in the OGDI and ECW formats.

However, by far the most common approach to implementing overviews is to use the default support in GDAL for external overviews stored in TIFF files with the same name as the dataset, but the extension .ovr appended. In order to enable reading and creation of this style of overviews it is necessary for the GDALDataset to initialize the `oOvManager` object within itself. This is typically accomplished with a call like the following near the end of the Open() method (after the PAM :cpp:func:`GDALDataset::TryLoadXML`).

.. code-block:: c++

    poDS->oOvManager.Initialize(poDS, poOpenInfo->pszFilename);

This will enable default implementations for reading and creating overviews for the format. It is advised that this be enabled for all simple file system based formats unless there is a custom overview mechanism to be tied into.

File Creation
-------------

There are two approaches to file creation. The first method is called the :cpp:func:`GDALDriver::CreateCopy` method, and involves implementing a function that can write a file in the output format, pulling all imagery and other information needed from a source GDALDataset. The second method, the dynamic creation method, involves implementing a Create method to create the shell of the file, and then the application writes various information by calls to set methods.

The benefits of the first method are that that all the information is available at the point the output file is being created. This can be especially important when implementing file formats using external libraries which require information like color maps, and georeferencing information at the point the file is created. The other advantage of this method is that the CreateCopy() method can read some kinds of information, such as min/max, scaling, description and GCPs for which there are no equivalent set methods.

The benefits of the second method are that applications can create an empty new file, and write results to it as they become available. A complete image of the desired data does not have to be available in advance.

For very important formats both methods may be implemented, otherwise do whichever is simpler, or provides the required capabilities.

CreateCopy
++++++++++

The GDALDriver::CreateCopy() method call is passed through directly, so that method should be consulted for details of arguments. However, some things to keep in mind are:

- If the `bStrict` flag is FALSE the driver should try to do something reasonable when it cannot exactly represent the source dataset, transforming data types on the fly, dropping georeferencing and so forth.
- Implementing progress reporting correctly is somewhat involved. The return result of the progress function needs always to be checked for cancellation, and progress should be reported at reasonable intervals. The JPEGCreateCopy() method demonstrates good handling of the progress function.
- Special creation options should be documented in the on-line help. If the options take the format "NAME=VALUE" the papszOptions list can be manipulated with :cpp:func:`CPLFetchNameValue` as demonstrated in the handling of the QUALITY and PROGRESSIVE flags for JPEGCreateCopy().
- The returned GDALDataset handle can be in ReadOnly or Update mode. Return it in Update mode if practical, otherwise in ReadOnly mode is fine.

The full implementation of the CreateCopy function for JPEG (which is assigned to pfnCreateCopy in the GDALDriver object) is here.
static GDALDataset *

.. code-block:: c++

    JPEGCreateCopy( const char * pszFilename, GDALDataset *poSrcDS,
                    int bStrict, char ** papszOptions,
                    GDALProgressFunc pfnProgress, void * pProgressData )
    {
        const int nBands = poSrcDS->GetRasterCount();
        const int nXSize = poSrcDS->GetRasterXSize();
        const int nYSize = poSrcDS->GetRasterYSize();
        // 몇몇 기본적인 확인
        if( nBands != 1 && nBands != 3 )
        {
            CPLError(CE_Failure, CPLE_NotSupported,
                    "JPEG driver doesn't support %d bands.  Must be 1 (grey) "
                    "or 3 (RGB) bands.", nBands);
            return NULL;
        }

        if( poSrcDS->GetRasterBand(1)->GetRasterDataType() != GDT_Byte && bStrict )
        {
            CPLError(CE_Failure, CPLE_NotSupported,
                    "JPEG driver doesn't support data type %s. "
                    "Only eight bit byte bands supported.",
                    GDALGetDataTypeName(
                        poSrcDS->GetRasterBand(1)->GetRasterDataType()));
            return NULL;
        }

        // 사용자가 어떤 옵션을 선택했는가?
        int nQuality = 75;
        if( CSLFetchNameValue(papszOptions, "QUALITY") != NULL )
        {
            nQuality = atoi(CSLFetchNameValue(papszOptions, "QUALITY"));
            if( nQuality < 10 || nQuality > 100 )
            {
                CPLError(CE_Failure, CPLE_IllegalArg,
                        "QUALITY=%s is not a legal value in the range 10 - 100.",
                        CSLFetchNameValue(papszOptions, "QUALITY"));
                return NULL;
            }
        }

        bool bProgressive = false;
        if( CSLFetchNameValue(papszOptions, "PROGRESSIVE") != NULL )
        {
            bProgressive = true;
        }

        // 데이터셋을 생성합니다.
        VSILFILE *fpImage = VSIFOpenL(pszFilename, "wb");
        if( fpImage == NULL )
        {
            CPLError(CE_Failure, CPLE_OpenFailed,
                    "Unable to create jpeg file %s.",
                    pszFilename);
            return NULL;
        }

        // 파일에 대한 JPG 접근을 초기화합니다.
        struct jpeg_compress_struct sCInfo;
        struct jpeg_error_mgr sJErr;
        sCInfo.err = jpeg_std_error(&sJErr);
        jpeg_create_compress(&sCInfo);
        jpeg_stdio_dest(&sCInfo, fpImage);
        sCInfo.image_width = nXSize;
        sCInfo.image_height = nYSize;
        sCInfo.input_components = nBands;
        if( nBands == 1 )
        {
            sCInfo.in_color_space = JCS_GRAYSCALE;
        }
        else
        {
            sCInfo.in_color_space = JCS_RGB;
        }
        jpeg_set_defaults(&sCInfo);
        jpeg_set_quality(&sCInfo, nQuality, TRUE);
        if( bProgressive )
            jpeg_simple_progression(&sCInfo);
        jpeg_start_compress(&sCInfo, TRUE);

        // 이미지를 반복하며 이미지 데이터를 복사합니다.
        GByte *pabyScanline = static_cast<GByte *>(CPLMalloc(nBands * nXSize));
        for( int iLine = 0; iLine < nYSize; iLine++ )
        {
            for( int iBand = 0; iBand < nBands; iBand++ )
            {
                GDALRasterBand * poBand = poSrcDS->GetRasterBand(iBand + 1);
                const CPLErr eErr =
                    poBand->RasterIO(GF_Read, 0, iLine, nXSize, 1,
                                    pabyScanline + iBand, nXSize, 1, GDT_Byte,
                                    nBands, nBands * nXSize);
                // 할 일: 핸들(handle) 오류.
            }
            JSAMPLE *ppSamples = pabyScanline;
            jpeg_write_scanlines(&sCInfo, &ppSamples, 1);
        }
        CPLFree(pabyScanline);
        jpeg_finish_compress(&sCInfo);
        jpeg_destroy_compress(&sCInfo);
        VSIFCloseL(fpImage);
        return static_cast<GDALDataset *>(GDALOpen(pszFilename, GA_ReadOnly));
    }

Dynamic Creation
++++++++++++++++

In the case of dynamic creation, there is no source dataset. Instead the size, number of bands, and pixel data type of the desired file is provided but other information (such as georeferencing, and imagery data) would be supplied later via other method calls on the resulting GDALDataset.

The following sample implement PCI .aux labeled raw raster creation. It follows a common approach of creating a blank, but valid file using non-GDAL calls, and then calling GDALOpen(,GA_Update) at the end to return a writable file handle. This avoids having to duplicate the various setup actions in the Open() function.

.. code-block:: c++

    GDALDataset *PAuxDataset::Create( const char * pszFilename,
                                    int nXSize, int nYSize, int nBands,
                                    GDALDataType eType,
                                    char ** /* papszParamList */ )
    {
        // 입력 옵션을 검증합니다.
        if( eType != GDT_Byte && eType != GDT_Float32 &&
            eType != GDT_UInt16 && eType != GDT_Int16 )
        {
            CPLError(
                CE_Failure, CPLE_AppDefined,
                "Attempt to create PCI .Aux labeled dataset with an illegal "
                "data type (%s).",
                GDALGetDataTypeName(eType));
            return NULL;
        }

        // 파일 생성을 시도합니다.
        FILE *fp = VSIFOpen(pszFilename, "w");
        if( fp == NULL )
        {
            CPLError(CE_Failure, CPLE_OpenFailed,
                    "Attempt to create file `%s' failed.",
                    pszFilename);
            return NULL;
        }

        // 바이너리 파일을 확립하기 위해 바이트 몇 개만 작성한 다음
        // 종료합니다.
        VSIFWrite("\0\0", 2, 1, fp);
        VSIFClose(fp);

        // 보조 파일명을 생성합니다.
        char *pszAuxFilename = static_cast<char *>(CPLMalloc(strlen(pszFilename) + 5));
        strcpy(pszAuxFilename, pszFilename);;
        for( int i = strlen(pszAuxFilename) - 1; i > 0; i-- )
        {
            if( pszAuxFilename[i] == '.' )
            {
                pszAuxFilename[i] = '\0';
                break;
            }
        }
        strcat(pszAuxFilename, ".aux");

        // 파일을 엽니다.
        fp = VSIFOpen(pszAuxFilename, "wt");
        if( fp == NULL )
        {
            CPLError(CE_Failure, CPLE_OpenFailed,
                    "Attempt to create file `%s' failed.",
                    pszAuxFilename);
            return NULL;
        }

        // AuxiliaryTarget 줄에 어떤 경로 구성요소도 없이
        // 원본 파일명을 작성해야 합니다. 여기에서 작성합니다.
        int iStart = strlen(pszFilename) - 1;
        while( iStart > 0 && pszFilename[iStart - 1] != '/' &&
            pszFilename[iStart - 1] != '\\' )
            iStart--;
        VSIFPrintf(fp, "AuxilaryTarget: %s\n", pszFilename + iStart);

        // 데이터셋 전체에 대한 원시(raw) 정의를 작성합니다.
        VSIFPrintf(fp, "RawDefinition: %d %d %d\n",
                nXSize, nYSize, nBands);

        // 각 밴드에 대한 정의를 작성합니다.
        // 현재 밴드를 언제나 순차 파일로 작성합니다.
        // GDAL이 꽤 효율적으로 처리할 수 있기 때문입니다.
        int nImgOffset = 0;
        for( int iBand = 0; iBand < nBands; iBand++ )
        {
            const int nPixelOffset = GDALGetDataTypeSize(eType)/8;
            const int nLineOffset = nXSize * nPixelOffset;
            const char *pszTypeName = NULL;
            if( eType == GDT_Float32 )
                pszTypeName = "32R";
            else if( eType == GDT_Int16 )
                pszTypeName = "16S";
            else if( eType == GDT_UInt16 )
                pszTypeName = "16U";
            else
                pszTypeName = "8U";
            VSIFPrintf( fp, "ChanDefinition-%d: %s %d %d %d %s\n",
                        iBand + 1, pszTypeName,
                        nImgOffset, nPixelOffset, nLineOffset,
    #ifdef CPL_LSB
                        "Swapped"
    #else
                        "Unswapped"
    #endif
                        );
            nImgOffset += nYSize * nLineOffset;
        }

        // 정리(cleanup).
        VSIFClose(fp);
        return static_cast<GDALDataset *>(GDALOpen(pszFilename, GA_Update));
    }

File formats supporting dynamic creation, or even just update-in-place access also need to implement an IWriteBlock() method on the raster band class. It has semantics similar to IReadBlock(). As well, for various esoteric reasons, it is critical that a FlushCache() method be implemented in the raster band destructor. This is to ensure that any write cache blocks for the band be flushed out before the destructor is called.

RawDataset/RawRasterBand Helper Classes
---------------------------------------

Many file formats have the actual imagery data stored in a regular, binary, scanline oriented format. Rather than re-implement the access semantics for this for each formats, there are provided :cpp:class:`RawDataset` and :cpp:class:`RawRasterBand` classes declared in gcore/ that can be utilized to implement efficient and convenient access.

In these cases the format specific band class may not be required, or if required it can be derived from RawRasterBand. The dataset class should be derived from RawDataset.

The Open() method for the dataset then instantiates raster bands passing all the layout information to the constructor. For instance, the PNM driver uses the following calls to create it's raster bands.

.. code-block:: c++

    if( poOpenInfo->pabyHeader[1] == '5' )
    {
        poDS->SetBand(
            1, new RawRasterBand(poDS, 1, poDS->fpImage,
                                iIn, 1, nWidth, GDT_Byte, TRUE));
    }
    else
    {
        poDS->SetBand(
            1, new RawRasterBand(poDS, 1, poDS->fpImage,
                                iIn, 3, nWidth*3, GDT_Byte, TRUE));
        poDS->SetBand(
            2, new RawRasterBand(poDS, 2, poDS->fpImage,
                                iIn+1, 3, nWidth*3, GDT_Byte, TRUE));
        poDS->SetBand(
            3, new RawRasterBand(poDS, 3, poDS->fpImage,
                                iIn+2, 3, nWidth*3, GDT_Byte, TRUE));
    }

The RawRasterBand takes the following arguments.

- poDS: The GDALDataset this band will be a child of. This dataset must be of a class derived from RawRasterDataset.
- nBand: The band it is on that dataset, 1 based.
- fpRaw: The FILE * handle to the file containing the raster data.
- nImgOffset: The byte offset to the first pixel of raster data for the first scanline.
- nPixelOffset: The byte offset from the start of one pixel to the start of the next within the scanline.
- nLineOffset: The byte offset from the start of one scanline to the start of the next.
- eDataType: The GDALDataType code for the type of the data on disk.
- bNativeOrder: FALSE if the data is not in the same endianness as the machine GDAL is running on. The data will be automatically byte swapped.

Simple file formats utilizing the Raw services are normally placed all within one file in the gdal/frmts/raw directory. There are numerous examples there of format implementation.

Metadata, and Other Exotic Extensions
-------------------------------------

There are various other items in the GDAL data model, for which virtual methods exist on the GDALDataset and GDALRasterBand. They include:

- Metadata: Name/value text values about a dataset or band. The GDALMajorObject (base class for GDALRasterBand and GDALDataset) has built-in support for holding metadata, so for read access it only needs to be set with calls to SetMetadataItem() during the Open(). The SAR_CEOS (frmts/ceos2/sar_ceosdataset.cpp) and GeoTIFF drivers are examples of drivers implementing readable metadata.

- ColorTables: GDT_Byte raster bands can have color tables associated with them. The frmts/png/pngdataset.cpp driver contains an example of a format that supports colortables.

- ColorInterpretation: The PNG driver contains an example of a driver that returns an indication of whether a band should be treated as a Red, Green, Blue, Alpha or Greyscale band.

- GCPs: GDALDatasets can have a set of ground control points associated with them (as opposed to an explicit affine transform returned by GetGeotransform()) relating the raster to georeferenced coordinates. The MFF2 (gdal/frmts/raw/hkvdataset.cpp) format is a simple example of a format supporting GCPs.

- NoDataValue: Bands with known "nodata" values can implement the GetNoDataValue() method. See the PAux (frmts/raw/pauxdataset.cpp) for an example of this.

- Category Names: Classified images with names for each class can return them using the GetCategoryNames() method though no formats currently implement this.
