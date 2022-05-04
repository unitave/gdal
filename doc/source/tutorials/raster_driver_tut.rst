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

이제 한 단계 더 나아가 지리참조 정보 지원을 추가해보겠습니다. :cpp:class:`GDALDataset` 기본 클래스에 있는 메소드 서명과 정확하게 일치하도록 주의하면서, :cpp:class:`JDEMDataset` 에 다음 가상 메소드 2개를 재정의합니다.

.. code-block:: c++

    CPLErr      GetGeoTransform( double * padfTransform );
    const char *GetProjectionRef();

:cpp:func:`GDALDataset::GetGeoTransform` 구현은 제공되는 버퍼에 일반적인 지리변환 행렬을 복사할 뿐입니다. :cpp:func:`GDALDataset::GetGeoTransform` 메소드를 자주 호출할 수도 있기 때문에 이 메소드 안에서 연산을 많이 하는 것은 일반적으로 현명하지 않다는 사실을 기억하십시오. 많은 경우 :cpp:func:`Open` 이 지리변환을 수집할 것이고, 이 메소드는 복사해올 뿐입니다. 또 반환되는 지리변환은 몇몇 패키지에서 사용되는 픽셀 중심 접근법이 아니라 좌상단 픽셀의 좌상단 모서리 위치에 있는 기준점(anchor point) 기반이라는 사실도 기억하십시오.

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

:cpp:func:`GDALDataset::GetProjectionRef` 메소드는 OGC WKT 포맷으로 된 좌표계 정의를 담고 있는 내부 문자열을 가리키는 포인터를 반환합니다. 이 경우 이 포맷으로 된 모든 파일이 동일한 좌표계를 공유하지만, 더 복잡한 경우에는 좌표계 정의를 실시간(on-the-fly)으로 구성해야 할 수도 있습니다. 이런 경우 좌표계 정의 작성을 돕기 위한 :cpp:class:`OGRSpatialReference` 클래스를 사용하면 도움이 될 수도 있습니다.

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

이것으로 JDEM 드라이버의 기능 설명을 마칩니다. :file:`jdemdataset.cpp` 의 전체 소스를 필요한 만큼 살펴볼 수 있습니다.

오버뷰
---------

GDAL은 파일 포맷이 :cpp:func:`GDALRasterBand::GetOverview` 및 관련 메소드를 통해 응용 프로그램이 사용할 수 있는 사전 빌드된 오버뷰를 생성할 수 있도록 허용하고 있습니다. 하지만 이를 구현하는 것은 상당히 복잡하며 현재로서는 이 문서의 범위를 벗어납니다. 오버뷰 리포트 및 생성 지원을 구현한 파일 포맷의 예시를 보고 싶다면 GeoTIFF 드라이버(:file:`gdal/frmts/gtiff/geotiff.cpp`) 및 관련 소스를 살펴보면 됩니다.

:cpp:class:`GDALRasterBand` 에 대해 :cpp:func:`GDALRasterBand::HasArbitraryOverviews` 메소드를 대체하고 TRUE를 반환해서 파일 포맷이 임의 오버뷰를 가지고 있다고 리포트할 수도 있습니다. 이 경우 래스터 밴드 객체가 :cpp:func:`GDALRasterBand::RasterIO` 메소드 자체를 대체하고 리샘플링된 영상에 효율적인 접근을 구현할 것으로 예상됩니다. 이 또한 상당히 복잡하며 :cpp:func:`RasterIO` 를 정확하게 구현하기 위해서는 수많은 요구 사항을 만족시켜야 합니다. OGDI 및 ECW 포맷에서 이에 대한 예시를 찾아볼 수 있습니다.

하지만 지금까지 오버뷰를 구현하기 위한 가장 흔한 접근법은 데이터셋과 동일한 이름이지만 .ovr 확장자가 추가된 TIFF 파일로 저장된 외부 오버뷰를 위한 GDAL 기본 지원을 사용하는 것입니다. 이런 스타일의 오버뷰를 읽고 생성하기 위해서는 :cpp:class:`GDALDataset` 자체 안에 있는 'oOvManager' 객체를 초기화시켜야 합니다. 일반적으로 :cpp:func:`Open` 메소드의 마지막 가까이에 (PAM :cpp:func:`GDALDataset::TryLoadXML` 다음에) 다음과 같이 호출하면 초기화시킬 수 있습니다.

.. code-block:: c++

    poDS->oOvManager.Initialize(poDS, poOpenInfo->pszFilename);

이렇게 하면 해당 포맷에 대해 오버뷰 읽기 및 생성의 기본 구현이 활성화될 것입니다. 사용자 지정 오버뷰 메커니즘이 연결되어 있지 않은 이상 모든 단순 파일 시스템 기반 포맷에 대해 이렇게 활성화시킬 것을 권장합니다.

파일 생성
---------

파일 생성을 위한 접근법이 2개 있습니다. 첫 번째는 :cpp:func:`GDALDriver::CreateCopy` 메소드로, 소스 :cpp:class:`GDALDataset` 으로부터 필요한 모든 영상 및 기타 정보를 가져와서 산출 포맷으로 된 파일을 작성할 수 있는 함수를 구현해야 합니다. 두 번째는 동적 생성 메소드로, :cpp:func:`Create` 메소드를 구현해서 파일의 뼈대를 생성한 다음 응용 프로그램이 메소드를 설정하는 호출을 통해 다양한 정보를 작성합니다.

첫 번째 메소드의 장점은 산출 파일 생성 시 모든 정보를 사용할 수 있다는 것입니다. 파일 생성 시 색상표 및 지리참조 정보 같은 정보를 요구하는 외부 라이브러리를 사용하는 파일 포맷을 구현하는 경우 특히 중요할 수 있습니다. 이 메소드의 다른 장점은 :cpp:func:`CreateCopy` 메소드가 동일한 기능을 하는 다른 설정 메소드가 없는 상황에서 최소값/최대값, 크기 조정 인자, 설명 및 GCP 같은 몇몇 종류의 정보를 읽어올 수 있다는 것입니다.

두 번째 메소드의 장점은 응용 프로그램이 비어 있는 새 파일을 생성한 다음 결과물을 사용할 수 있게 될 때 빈 파일에 결과물을 작성할 수 있다는 것입니다. 원하는 데이터의 전체 이미지를 사전에 준비할 필요가 없습니다.

매우 중요한 포맷의 경우 이 두 메소드가 구현되어 있을 수도 있습니다. 그렇지 않은 경우 더 단순한 쪽을 수행하거나, 필요한 케이퍼빌리티를 제공합니다.

CreateCopy
++++++++++

:cpp:func:`GDALDriver::CreateCopy` 메소드 호출을 직접 전송해서 인자들의 자세한 내용에 대해 메소드를 참조할 수 있게 해야 합니다. 하지만 다음 내용을 기억해두십시오:

-  'bStrict' 플래그가 FALSE라면, 드라이버가 소스 데이터셋을 정확하게 표현하지 못 하거나 데이터 유형을 실시간으로 변환하지 못 하거나 지리참조 정보를 폐기하거나 등등의 경우 드라이버가 타당한 작업을 시도해야 합니다.

-  진행 상황 리포트 작업을 정확하게 구현하는 것은 상당히 복잡합니다. 진행 상황 함수가 반환하는 결과물은 언제나 취소하는 경우인지 확인해야 하며, 적당한 간격으로 진행 상황을 리포트해야 합니다. :cpp:func:`JPEGCreateCopy` 메소드가 이 진행 상황 함수를 훌륭하게 처리하는 예시를 보여줍니다.

-  온라인 도움말에 특수 생성 옵션들을 문서화해야 합니다. 옵션이 "NAME=VALUE" 서식을 입력받는 경우, :cpp:func:`JPEGCreateCopy` 메소드의 QUALITY 및 PROGRESSIVE 플래그의 처리에서 볼 수 있듯이 :cpp:func:`CPLFetchNameValue` 함수로 'papszOptions' 목록을 수정할 수 있습니다.

-  반환되는 :cpp:class:`GDALDataset` 핸들이 ReadOnly 또는 Update 모드일 수 있습니다. 업데이트 모드가 실용적인 경우 핸들을 업데이트 모드로 반환하고, 그렇지 않다면 읽기 전용 모드로 반환해도 됩니다.

다음은 (:cpp:class:`GDALDriver` 객체에 있는 'pfnCreateCopy'에 할당되는) JPEG 용 :cpp:func:`CreateCopy` 메소드를 완전하게 구현하는 예시입니다:

.. code-block:: c++

    static GDALDataset *

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

동적 생성
+++++++++

동적 생성의 경우, 소스 데이터셋이 존재하지 않습니다. 그 대신 원하는 파일의 크기, 밴드 개수, 그리고 픽셀 데이터 유형을 지정합니다. 나중에 산출되는 :cpp:class:`GDALDataset` 에 다른 메소드들을 호출해서 (지리참조, 영상 데이터 같은) 다른 정보를 작성할 것입니다.

다음 예시는 PCI .aux 확장자를 사용하는 원시(raw) 래스터 생성을 구현합니다. GDAL이 아닌 메소드를 호출해서 비어 있지만 무결한 파일을 생성한 다음, 마지막에 :cpp:func:`GDALOpen` (그리고 :cpp:func:`GA_Update`) 함수를 호출해서 쓰기 가능한 파일 핸들을 반환합니다. 이렇게 하면 :cpp:func:`Open` 함수에 다양한 설정 액션을 복제해야 하는 일을 피할 수 있습니다.

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

동적 생성을 지원하는 또는 제자리(in-place) 업데이트 접근만 지원하는 파일 포맷도 래스터 밴드 클래스에 대한 :cpp:func:`IWriteBlock` 메소드를 구현해야 합니다. 이 메소드는 :cpp:func:`IReadBlock` 과 비슷한 의미를 가지고 있습니다. 또한 다양한 난해한 이유 때문에, 래스터 밴드 삭제자(destructor)에 :cpp:func:`FlushCache` 메소드를 구현하는 것이 정말 중요합니다. 삭제자를 호출하기 전에 밴드에 대한 모든 쓰기 캐시 블록을 플러싱시키도록 보장하기 위해서입니다.

RawDataset/RawRasterBand 도우미 클래스
--------------------------------------

많은 파일 포맷들이 실제 영상 데이터를 정규, 바이너리, 스캔라인 지향 포맷으로 저장합니다. 각 포맷별로 이를 위한 접근 의미를 다시 구현하기보다, :file:`gcore/` 에 선언된 :cpp:class:`RawDataset` 및 :cpp:class:`RawRasterBand` 클래스를 활용해서 효율적이고 편리한 접근을 구현할 수 있습니다.

이런 경우 포맷 특화 밴드 클래스가 필요하지 않을 수도 있고, 또는 필요한 경우 :cpp:class:`RawRasterBand` 로부터 파생시킬 수 있습니다. 데이터셋 클래스는 :cpp:class:`RawDataset` 으로부터 파생되어야 합니다.

그 다음 데이터셋에 대한 :cpp:func:`Open` 메소드가 구성자(constructor)에게 모든 레이아웃 정보를 전송해서 래스터 밴드를 인스턴스화합니다. 예를 들면 PNM 드라이버는 다음과 같은 호출을 사용해서 래스터 밴드를 생성합니다:

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

:cpp:class:`RawRasterBand` 클래스는 다음 인자들을 입력받습니다:

-  poDS:
   이 밴드의 상위 클래스가 될 :cpp:class:`GDALDataset` 입니다. 이 데이터셋은 반드시 :cpp:class:`RawRasterDataset` 으로부터 파생된 클래스여야 합니다.

-  nBand:
   해당 데이터셋에 있는 밴드의 1에서 시작하는 번호입니다.

-  fpRaw:
   래스터 데이터를 담고 있는 파일을 가리키는 ``FILE *`` 핸들입니다.

-  nImgOffset:
   래스터 데이터의 첫 번째 스캔라인의 첫 번째 픽셀에 대한 바이트 오프셋입니다.

-  nPixelOffset:
   스캔라인 안에 있는 한 픽셀의 시작으로부터 다음 픽셀의 시작까지의 바이트 오프셋입니다

-  nLineOffset:
   한 스캔라인의 시작으로부터 다음 스캔라인의 시작까지의 바이트 오프셋입니다.

-  eDataType:
   디스크 상에 있는 데이터의 유형을 나타내는 :cpp:class:`GDALDataType` 코드입니다.

-  bNativeOrder:
   데이터가 GDAL이 실행 중인 머신과 동일한 엔디언(endian)에 있지 않는 경우 FALSE로 설정합니다. 데이터의 바이트를 자동으로 뒤바꿀 것입니다.

"Raw" 서비스를 활용하는 단순 파일 포맷들은 일반적으로 :file:`gdal/frmts/raw` 디렉터리에 있는 파일 하나 안에 배치됩니다. 포맷 구현에 대한 수많은 예시들이 있습니다.

메타데이터 및 기타 실험적인 확장 사양
-------------------------------------

GDAL 데이터 모델에는 다양한 다른 항목들이 있으며, :cpp:class:`GDALDataset` 및 :cpp:class:`GDALRasterBand` 상에 이에 대한 가상 메소드들이 존재합니다. 이 가상 메소드에는 다음이 포함됩니다:

-  Metadata:
   데이터셋 또는 밴드에 관한 이름/값 텍스트 값입니다. (:cpp:class:`GDALDataset` 및 :cpp:class:`GDALRasterBand` 의 기반 클래스인) :cpp:class:`GDALMajorObject` 는 메타데이터를 담기 위한 지원을 내장하고 있기 때문에, 읽기 접근의 경우 :cpp:func:`Open` 도중 :cpp:func:`SetMetadataItem` 함수를 호출하도록 설정하기만 하면 됩니다. 읽기 가능한 메타데이터를 구현한 드라이버의 예시로는 SAR_CEOS(:file:`frmts/ceos2/sar_ceosdataset.cpp`) 및 GeoTIFF 드라이버가 있습니다.

-  ColorTables:
   GDT_Byte 래스터 밴드는 연결된 색상표를 가질 수 있습니다. :file:`frmts/png/pngdataset.cpp` 드라이버가 색상표를 지원하는 포맷의 예시를 담고 있습니다.

-  ColorInterpretation:
   PNG 드라이버가 어떤 밴드를 적색, 녹색, 청색, 알파 또는 회색조 밴드로 취급해야 할지 여부를 나타내는 값을 반환하는 드라이버의 예시를 담고 있습니다.

-  GCP:
   :cpp:class:`GDALDataset` 은 연결된 지상기준점(Ground Control Point) 집합을 가질 수 있습니다. GCP는 (:cpp:func:`GetGeotransform` 함수가 반환하는 명확한 아핀 변환과는 반대로) 래스터를 지리참조 좌표에 연결합니다. GCP를 지원하는 단순 포맷의 예시로는 MFF2(:file:`gdal/frmts/raw/hkvdataset.cpp`) 포맷이 있습니다.

-  NoDataValue:
   알려진 "NODATA" 값을 가진 밴드는 :cpp:func:`GetNoDataValue` 메소드를 구현할 수 있습니다. 이 예시를 보고 싶다면 PAux(:file:`frmts/raw/pauxdataset.cpp`) 포맷을 참조하십시오.

-  카테고리 이름:
   :cpp:func:`GetCategoryNames` 메소드를 사용하면 범주 이미지의 각 범주의 이름을 반환할 수 있지만 현재 이 메소드를 구현한 포맷은 없습니다.

