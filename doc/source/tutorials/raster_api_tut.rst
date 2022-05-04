.. _raster_api_tut:

================================================================================
래스터 API 예제
================================================================================

파일 열기
---------

GDAL이 지원하는 래스터 데이터 저장소를 열기 전에 드라이버를 등록해야 합니다. 지원하는 포맷별로 드라이버가 존재합니다. 일반적으로 :cpp:func:`GDALDriverManager::AutoLoadDrivers` 함수를 이용해서 .so 파일로부터 자동으로 불러오는 드라이버를 포함, 알려진 모든 드라이버를 등록하려 시도하는 :cpp:func:`GDALAllRegister` 함수로 드라이버를 등록합니다. 일부 응용 프로그램의 경우 등록되는 드라이버 집합을 제한해야 한다면, :file:`gdalallregister.cpp` 파일의 코드를 살펴보는 것이 도움이 될 수도 있습니다. 파이썬은 GDAL 모듈을 가져올 때 자동적으로 :cpp:func:`GDALAllRegister` 함수를 호출합니다.

드라이버를 등록한 다음, 응용 프로그램이 독립형 :cpp:func:`GDALOpen` 함수를 호출해서 데이터셋의 이름 및 원하는 접근법(GA_ReadOnly 또는 GA_Update)을 전송해서 데이터를 열어야 합니다.

C++ 코드:

.. code-block:: c++

    #include "gdal_priv.h"
    #include "cpl_conv.h" // CPLMalloc() 용
    int main()
    {
        GDALDataset  *poDataset;
        GDALAllRegister();
        poDataset = (GDALDataset *) GDALOpen( pszFilename, GA_ReadOnly );
        if( poDataset == NULL )
        {
            ...;
        }

C 코드:

.. code-block:: c

    #include "gdal.h"
    #include "cpl_conv.h" /* CPLMalloc() 용 */
    int main()
    {
        GDALDatasetH  hDataset;
        GDALAllRegister();
        hDataset = GDALOpen( pszFilename, GA_ReadOnly );
        if( hDataset == NULL )
        {
            ...;
        }


파이썬 코드:

.. code-block:: python

    from osgeo import gdal
    dataset = gdal.Open(filename, gdal.GA_ReadOnly)
    if not dataset:
        ...

:cpp:func:`GDALOpen` 이 NULL을 반환한다면 파일 열기가 실패했으며 이미 :cpp:func:`CPLError` 함수를 통해 오류 메시지를 발송했을 것이라는 의미입니다. 오류가 사용자에게 리포트되는 방법을 제어하고 싶다면 :cpp:func:`CPLError` 문서를 살펴보십시오. 일반적으로, 모든 GDAL이 :cpp:func:`CPLError` 함수를 이용해서 오류를 리포트합니다. 또한 'pszFilename'이 실제로 디스크 상에 존재하는 파일의 이름일 필요는 없다는 사실을 기억하십시오. (보통 실제로 존재하는 파일의 이름이긴 합니다.) 데이터셋 이름의 해석은 드라이버에 따라 달라지며, 이 이름은 URL일 수도 있고 파일 열기를 제어하는 추가 파라미터가 뒤에 추가된 파일명일 수도 있고, 또는 거의 어떤 것이든 될 수 있습니다. GDAL 파일 선택 대화창을 디스크 상에 존재하는 파일만 선택하기 위한 것으로 제한하지 말아주십시오.

데이터셋 정보 수집하기
----------------------

:ref:`raster_data_model` 에서 설명했듯이, :cpp:class:`GDALDataset` 클래스는 모두 동일 영역 범위이고 동일 해상도를 가진 래스터 밴드들의 목록을 담고 있습니다. 메타데이터, 좌표계, 지리참조 변환, 래스터 크기, 그리고 다양한 기타 정보도 가지고 있습니다.

특수하지만 동시에 흔한 경우로, 기울어지지 않은 또는 전단(剪斷)되지 않은 "북쪽이 위"인 이미지의 경우 지리참조 변환 :ref:`geotransforms_tut` 는 다음 형식을 취합니다:

.. code-block:: c

    adfGeoTransform[0] /* 좌상단 x */
    adfGeoTransform[1] /* w-e 픽셀 해상도 */
    adfGeoTransform[2] /* 0 */
    adfGeoTransform[3] /* 좌상단 y */
    adfGeoTransform[4] /* 0 */
    adfGeoTransform[5] /* n-s 픽셀 해상도 (음의 값) */

일반적인 경우, 이는 아핀 변환입니다.

데이터셋에 관한 몇몇 일반 정보를 출력하고자 하는 경우 다음과 같은 코드를 실행할 수도 있습니다:

C++ 코드:

.. code-block:: c++

    double        adfGeoTransform[6];
    printf( "Driver: %s/%s\n",
            poDataset->GetDriver()->GetDescription(),
            poDataset->GetDriver()->GetMetadataItem( GDAL_DMD_LONGNAME ) );
    printf( "Size is %dx%dx%d\n",
            poDataset->GetRasterXSize(), poDataset->GetRasterYSize(),
            poDataset->GetRasterCount() );
    if( poDataset->GetProjectionRef()  != NULL )
        printf( "Projection is `%s'\n", poDataset->GetProjectionRef() );
    if( poDataset->GetGeoTransform( adfGeoTransform ) == CE_None )
    {
        printf( "Origin = (%.6f,%.6f)\n",
                adfGeoTransform[0], adfGeoTransform[3] );
        printf( "Pixel Size = (%.6f,%.6f)\n",
                adfGeoTransform[1], adfGeoTransform[5] );
    }

C 코드:

.. code-block:: c

    GDALDriverH   hDriver;
    double        adfGeoTransform[6];
    hDriver = GDALGetDatasetDriver( hDataset );
    printf( "Driver: %s/%s\n",
            GDALGetDriverShortName( hDriver ),
            GDALGetDriverLongName( hDriver ) );
    printf( "Size is %dx%dx%d\n",
            GDALGetRasterXSize( hDataset ),
            GDALGetRasterYSize( hDataset ),
            GDALGetRasterCount( hDataset ) );
    if( GDALGetProjectionRef( hDataset ) != NULL )
        printf( "Projection is `%s'\n", GDALGetProjectionRef( hDataset ) );
    if( GDALGetGeoTransform( hDataset, adfGeoTransform ) == CE_None )
    {
        printf( "Origin = (%.6f,%.6f)\n",
                adfGeoTransform[0], adfGeoTransform[3] );
        printf( "Pixel Size = (%.6f,%.6f)\n",
                adfGeoTransform[1], adfGeoTransform[5] );
    }

파이썬 코드:

.. code-block:: python

    print("Driver: {}/{}".format(dataset.GetDriver().ShortName,
                                dataset.GetDriver().LongName))
    print("Size is {} x {} x {}".format(dataset.RasterXSize,
                                        dataset.RasterYSize,
                                        dataset.RasterCount))
    print("Projection is {}".format(dataset.GetProjection()))
    geotransform = dataset.GetGeoTransform()
    if geotransform:
        print("Origin = ({}, {})".format(geotransform[0], geotransform[3]))
        print("Pixel Size = ({}, {})".format(geotransform[1], geotransform[5]))

래스터 밴드 가져오기
--------------------

현재 GDAL을 통해 래스터 데이터에 접근하면 한 번에 밴드 하나씩 접근합니다. 또한 밴드별로 메타데이터, 블록 크기, 색상표, 그리고 다양한 기타 정보를 사용할 수 있습니다. 다음 코드들은 (:cpp:func:`GDALRasterBand::GetRasterCount` 함수를 통해 1번으로 번호가 매겨진) 데이터셋으로부터 :cpp:class:`GDALRasterBand` 객체를 가져와서 관련 정보를 출력합니다:

C++ 코드:

.. code-block:: c++

    GDALRasterBand  *poBand;
    int             nBlockXSize, nBlockYSize;
    int             bGotMin, bGotMax;
    double          adfMinMax[2];
    poBand = poDataset->GetRasterBand( 1 );
    poBand->GetBlockSize( &nBlockXSize, &nBlockYSize );
    printf( "Block=%dx%d Type=%s, ColorInterp=%s\n",
            nBlockXSize, nBlockYSize,
            GDALGetDataTypeName(poBand->GetRasterDataType()),
            GDALGetColorInterpretationName(
                poBand->GetColorInterpretation()) );
    adfMinMax[0] = poBand->GetMinimum( &bGotMin );
    adfMinMax[1] = poBand->GetMaximum( &bGotMax );
    if( ! (bGotMin && bGotMax) )
        GDALComputeRasterMinMax((GDALRasterBandH)poBand, TRUE, adfMinMax);
    printf( "Min=%.3fd, Max=%.3f\n", adfMinMax[0], adfMinMax[1] );
    if( poBand->GetOverviewCount() > 0 )
        printf( "Band has %d overviews.\n", poBand->GetOverviewCount() );
    if( poBand->GetColorTable() != NULL )
        printf( "Band has a color table with %d entries.\n",
                poBand->GetColorTable()->GetColorEntryCount() );


C 코드:

.. code-block:: c

    GDALRasterBandH hBand;
    int             nBlockXSize, nBlockYSize;
    int             bGotMin, bGotMax;
    double          adfMinMax[2];
    hBand = GDALGetRasterBand( hDataset, 1 );
    GDALGetBlockSize( hBand, &nBlockXSize, &nBlockYSize );
    printf( "Block=%dx%d Type=%s, ColorInterp=%s\n",
            nBlockXSize, nBlockYSize,
            GDALGetDataTypeName(GDALGetRasterDataType(hBand)),
            GDALGetColorInterpretationName(
                GDALGetRasterColorInterpretation(hBand)) );
    adfMinMax[0] = GDALGetRasterMinimum( hBand, &bGotMin );
    adfMinMax[1] = GDALGetRasterMaximum( hBand, &bGotMax );
    if( ! (bGotMin && bGotMax) )
        GDALComputeRasterMinMax( hBand, TRUE, adfMinMax );
    printf( "Min=%.3fd, Max=%.3f\n", adfMinMax[0], adfMinMax[1] );
    if( GDALGetOverviewCount(hBand) > 0 )
        printf( "Band has %d overviews.\n", GDALGetOverviewCount(hBand));
    if( GDALGetRasterColorTable( hBand ) != NULL )
        printf( "Band has a color table with %d entries.\n",
                GDALGetColorEntryCount(
                    GDALGetRasterColorTable( hBand ) ) );

파이썬 코드:

.. code-block:: python

    band = dataset.GetRasterBand(1)
    print("Band Type={}".format(gdal.GetDataTypeName(band.DataType)))

    min = band.GetMinimum()
    max = band.GetMaximum()
    if not min or not max:
        (min,max) = band.ComputeRasterMinMax(True)
    print("Min={:.3f}, Max={:.3f}".format(min,max))

    if band.GetOverviewCount() > 0:
        print("Band has {} overviews".format(band.GetOverviewCount()))

    if band.GetRasterColorTable():
        print("Band has a color table with {} entries".format(band.GetRasterColorTable().GetCount()))

래스터 데이터 읽기
------------------

래스터 데이터를 읽어올 수 있는 방법이 몇 가지 있지만, 가장 흔한 방법은 :cpp:func:`GDALRasterBand::RasterIO` 메소드를 통해 읽어오는 것입니다. 이 메소드는 데이터 유형 변환, 업샘플링/다운샘플링 및 윈도윙(windowing) 작업을 자동으로 처리할 것입니다. 다음 코드들은 데이터의 첫 번째 스캔라인을 부동소수점형으로 변환시켜 비슷한 크기의 버퍼로 읽어올 것입니다.

C++ 코드:

.. code-block:: c++

    float *pafScanline;
    int   nXSize = poBand->GetXSize();
    pafScanline = (float *) CPLMalloc(sizeof(float)*nXSize);
    poBand->RasterIO( GF_Read, 0, 0, nXSize, 1,
                    pafScanline, nXSize, 1, GDT_Float32,
                    0, 0 );

더 이상 사용하지 않을 때 :cpp:func:`CPLFree()` 함수로 'pafScanline' 버퍼를 해제해줘야 합니다.

C 코드:

.. code-block:: c

    float *pafScanline;
    int   nXSize = GDALGetRasterBandXSize( hBand );
    pafScanline = (float *) CPLMalloc(sizeof(float)*nXSize);
    GDALRasterIO( hBand, GF_Read, 0, 0, nXSize, 1,
                pafScanline, nXSize, 1, GDT_Float32,
                0, 0 );

더 이상 사용하지 않을 때 :cpp:func:`CPLFree()` 함수로 'pafScanline' 버퍼를 해제해줘야 합니다.

파이썬 코드:

.. code-block:: python

    scanline = band.ReadRaster(xoff=0, yoff=0,
                            xsize=band.XSize, ysize=1,
                            buf_xsize=band.XSize, buf_ysize=1,
                            buf_type=gdal.GDT_Float32)

반환되는 스캔라인이 문자열 유형이고 원시(raw) 바이너리 부동소수점형 데이터 'XSize*4'바이트를 담고 있다는 사실을 기억하십시오. 다음과 같이 표준 라이브러리의 'struct' 모듈을 이용해서 이 스캔라인을 파이썬 값으로 변환할 수 있습니다:

.. code-block:: python

    import struct
    tuple_of_floats = struct.unpack('f' * b2.XSize, scanline)

:cpp:func:`GDALRasterBand::RasterIO` 함수는 다음 인자들을 입력받습니다:

.. code-block:: c++

    CPLErr GDALRasterBand::RasterIO( GDALRWFlag eRWFlag,
                                    int nXOff, int nYOff, int nXSize, int nYSize,
                                    void * pData, int nBufXSize, int nBufYSize,
                                    GDALDataType eBufType,
                                    int nPixelSpace,
                                    int nLineSpace )

동일한 :cpp:func:`GDALRasterBand::RasterIO` 호출이 'eRWFlag'의 설정을 (GF_Read 또는 GF_Write) 기반으로 읽기 또는 쓰기에 사용된다는 사실을 기억하십시오. 'nXOff', 'nYOff', 'nXSize', 'nYSize' 인자는 디스크에서 읽어올 (또는 작성할) 래스터 데이터의 윈도우를 서술합니다. 이 윈도우가 꼭 타일 경계선과 일치할 필요는 없지만 일치하는 경우 더욱 효율적으로 접근할 수 있을 것입니다.

'pData'는 데이터를 읽어올 (또는 작성할) 메모리 버퍼입니다. 이 버퍼의 실수 유형은 GDT_Float32 또는 GDT_Byte처럼 eBufType으로 전송되는 값이어야만 합니다. :cpp:func:`RasterIO` 를 호출하면 버퍼의 데이터 유형과 밴드의 데이터 유형 간의 변환을 처리할 것입니다. 부동소수점형 데이터를 정수형으로 변환하는 경우 :cpp:func:`RasterIO` 가 값을 내림(round down)하고, 산출물의 정당한 범위를 벗어나는 소스 값을 변환하는 경우 정당한 범위 안에 있는 최근접 값을 사용한다는 사실을 기억하십시오. 다시 말해, 예를 들면 GDT_Byte 버퍼로 16비트 데이터를 읽어올 때 255를 초과하는 모든 값을 255로 변환할 것입니다. 데이터를 크기 조정하지 않습니다!

'nBufXSize' 및 'nBufYSize' 값은 버퍼의 크기를 서술합니다. 전체 해상도 수준의 데이터를 불러오는 경우 버퍼 크기가 윈도우 크기와 동일할 것입니다. 하지만 감소 해상도 오버뷰를 불러오는 경우 디스크 상에서의 윈도우보다 작게 설정할 수 있습니다. 이 경우 오버뷰를 사용하는 편이 더 적합하다면 :cpp:func:`RasterIO` 가 I/O를 더 효율적으로 수행하기 위해 오버뷰를 활용할 것입니다.

일반적으로 'nPixelSpace' 및 'nLineSpace' 값은 기본값을 사용해야 한다는 뜻인 0입니다. 하지만 이 값들을 사용해서 메모리 데이터 버퍼에의 접근을 제어할 수 있습니다. 예를 들어 다른 픽셀 교차삽입 데이터를 담고 있는 버퍼에 데이터를 읽어올 수 있습니다.

데이터셋 종료하기
-----------------

:cpp:class:`GDALRasterBand` 객체는 해당 데이터셋의 소유이기 때문에, 절대로 C++ 삭제 연산자로 삭제해서는 안 된다는 사실을 기억하십시오. :cpp:func:`GDALClose` 함수를 호출하면 :cpp:class:`GDALDataset` 클래스를 종료할 수 있습니다. (윈도우 사용자의 경우 GDALDataset에 삭제 연산자를 사용하는 것을 권장하지 않습니다. 모듈 경계에 걸쳐 메모리를 할당하고 해제하는 경우 발생한다고 알려진 문제점 때문입니다. FAQ에서 관련 주제를 읽어보십시오.) :cpp:func:`GDALClose` 함수를 호출하면 제대로 마무리(cleanup)하고 대기 중인 모든 쓰기를 플러싱(flushing)할 것입니다. GeoTIFF 같은 유명한 포맷으로 된 데이터셋을 업데이트 모드로 열었는데 이 데이터셋에 대해 :cpp:func:`GDALClose` 함수를 호출하는 일을 잊었다면, 일반적으로 다시 열 수 없게 될 것입니다.

파일 생성 기법
--------------

GDAL이 지원하는 포맷의 드라이버가 생성을 지원하는 경우 해당 포맷으로 된 새 파일을 생성할 수도 있습니다. :cpp:func:`GDALDriver::CreateCopy` 그리고 :cpp:func:`GDALDriver::Create` 메소드를 사용하는 일반 기법이 두 가지 존재합니다. CreateCopy 메소드는 포맷 드라이버에 :cpp:func:`CreateCopy` 함수를 호출해서 복사해야 할 데이터셋에 전송합니다. Create 메소드는 드라이버에 :cpp:func:`Create` 함수를 호출한 다음, 모든 메타데이터와 래스터 데이터를 개별 호출로 명확하게 작성합니다. 새 파일 생성을 지원하는 모든 드라이버는 :cpp:func:`CreateCopy` 메소드를 지원하지만, :cpp:func:`Create` 메소드를 지원하는 드라이버는 몇 개 없습니다.

특정 포맷이 :cpp:func:`Create` 또는 :cpp:func:`CreateCopy` 를 지원하는지 판단하려면 포맷 드라이버 객체 상에 DCAP_CREATE 및 DCAP_CREATECOPY 메타데이터가 존재하는지 확인해보면 됩니다. :cpp:func:`GDALDriverManager::GetDriverByName` 함수를 호출하기 전에 :cpp:func:`GDALAllRegister` 를 호출했는지 확인하십시오. 다음은 드라이버 객체를 가져와서 :cpp:func:`Create` 그리고/또는 :cpp:func:`CreateCopy` 를 지원하는지 판단하는 예시입니다:

C++ 코드:

.. code-block:: c++

    #include "cpl_string.h"
    ...
        const char *pszFormat = "GTiff";
        GDALDriver *poDriver;
        char **papszMetadata;
        poDriver = GetGDALDriverManager()->GetDriverByName(pszFormat);
        if( poDriver == NULL )
            exit( 1 );
        papszMetadata = poDriver->GetMetadata();
        if( CSLFetchBoolean( papszMetadata, GDAL_DCAP_CREATE, FALSE ) )
            printf( "Driver %s supports Create() method.\n", pszFormat );
        if( CSLFetchBoolean( papszMetadata, GDAL_DCAP_CREATECOPY, FALSE ) )
            printf( "Driver %s supports CreateCopy() method.\n", pszFormat );

C 코드:

.. code-block:: c

        #include "cpl_string.h"
        ...
        const char *pszFormat = "GTiff";
        GDALDriverH hDriver = GDALGetDriverByName( pszFormat );
        char **papszMetadata;
        if( hDriver == NULL )
            exit( 1 );
        papszMetadata = GDALGetMetadata( hDriver, NULL );
        if( CSLFetchBoolean( papszMetadata, GDAL_DCAP_CREATE, FALSE ) )
            printf( "Driver %s supports Create() method.\n", pszFormat );
        if( CSLFetchBoolean( papszMetadata, GDAL_DCAP_CREATECOPY, FALSE ) )
            printf( "Driver %s supports CreateCopy() method.\n", pszFormat );

파이썬 코드:

.. code-block:: python

    fileformat = "GTiff"
    driver = gdal.GetDriverByName(fileformat)
    metadata = driver.GetMetadata()
    if metadata.get(gdal.DCAP_CREATE) == "YES":
        print("Driver {} supports Create() method.".format(fileformat))

    if metadata.get(gdal.DCAP_CREATECOPY) == "YES":
        print("Driver {} supports CreateCopy() method.".format(fileformat))

드라이버들 가운데 상당수가 읽기 전용이기 때문에 :cpp:func:`Create` 또는 :cpp:func:`CreateCopy` 를 지원하지 않을 것이라는 사실을 기억하십시오.

CreateCopy() 사용하기
---------------------

:cpp:func:`GDALDriver::CreateCopy` 메소드를 사용해서 소스 데이터셋으로부터 대부분의 정보를 꽤 간단하게 수집할 수 있습니다. 하지만 이 메소드는 포맷 특화 생성 옵션을 전송하기 위한 옵션들과 대용량 데이터셋을 복사하는 동안 사용자에게 진행 상황을 리포트하기 위한 옵션들을 포함합니다. 이전에 불러온 드라이버의 포맷에 기본 옵션을 사용해서 'pszSrcFilename'이라는 기존 파일을 'pszDstFilename'이라는 새 파일로 복사하는 단순한 코드는 다음과 같을 것입니다:

C++ 코드:

.. code-block:: c++

    GDALDataset *poSrcDS =
    (GDALDataset *) GDALOpen( pszSrcFilename, GA_ReadOnly );
    GDALDataset *poDstDS;
    poDstDS = poDriver->CreateCopy( pszDstFilename, poSrcDS, FALSE,
                                    NULL, NULL, NULL );
    /* 작업이 끝나면 데이터셋을 제대로 종료합니다 */
    if( poDstDS != NULL )
        GDALClose( (GDALDatasetH) poDstDS );
    GDALClose( (GDALDatasetH) poSrcDS );

C 코드:

.. code-block:: c

    GDALDatasetH hSrcDS = GDALOpen( pszSrcFilename, GA_ReadOnly );
    GDALDatasetH hDstDS;
    hDstDS = GDALCreateCopy( hDriver, pszDstFilename, hSrcDS, FALSE,
                            NULL, NULL, NULL );
    /* 작업이 끝나면 데이터셋을 제대로 종료합니다 */
    if( hDstDS != NULL )
        GDALClose( hDstDS );
    GDALClose(hSrcDS);

파이썬 코드:

.. code-block:: python

    src_ds = gdal.Open(src_filename)
    dst_ds = driver.CreateCopy(dst_filename, src_ds, strict=0)
    # 작업이 끝나면 데이터셋을 제대로 종료합니다
    dst_ds = None
    src_ds = None

:cpp:func:`CreateCopy` 메소드는 작성 가능한 데이터셋을 반환하며, 쓰기를 완료하고 데이터셋을 디스크로 플러싱하기 위해서는 이 데이터셋을 제대로 종료해야만 한다는 사실을 기억하십시오. 파이썬 코드의 경우 "dst_ds"가 범위를 벗어날 때 데이터셋을 자동으로 종료합니다. :cpp:func:`CreateCopy` 호출에서 대상 파일명 바로 뒤에 오는 'bStrict' 옵션의 값이 FALSE(또는 0)인 경우 대상 데이터셋을 입력 데이터셋과 정확하게 일치하도록 생성할 수 없더라도 치명적인 오류 없이 :cpp:func:`CreateCopy` 호출을 진행해야 한다는 뜻입니다. 예를 들면 산출 포맷이 입력 데이터셋의 픽셀 데이터 유형을 지원하지 않거나 또는 지리참조 정보 작성을 지원하지 못 하기 때문일 수도 있습니다.

다음은 생성 옵션을 전송하고 사전 정의된 진행 상황 모니터를 사용하는 좀 더 복잡한 경우의 예시입니다:

C++ 코드:

.. code-block:: c++

        #include "cpl_string.h"
        ...
        char **papszOptions = NULL;
        papszOptions = CSLSetNameValue( papszOptions, "TILED", "YES" );
        papszOptions = CSLSetNameValue( papszOptions, "COMPRESS", "PACKBITS" );
        poDstDS = poDriver->CreateCopy( pszDstFilename, poSrcDS, FALSE,
                                        papszOptions, GDALTermProgress, NULL );
        /* 작업이 끝나면 데이터셋을 제대로 종료합니다 */
        if( poDstDS != NULL )
            GDALClose( (GDALDatasetH) poDstDS );
        CSLDestroy( papszOptions );

C 코드:

.. code-block:: c

        #include "cpl_string.h"
        ...
        char **papszOptions = NULL;
        papszOptions = CSLSetNameValue( papszOptions, "TILED", "YES" );
        papszOptions = CSLSetNameValue( papszOptions, "COMPRESS", "PACKBITS" );
        hDstDS = GDALCreateCopy( hDriver, pszDstFilename, hSrcDS, FALSE,
                                papszOptions, GDALTermProgres, NULL );
        /* 작업이 끝나면 데이터셋을 제대로 종료합니다 */
        if( hDstDS != NULL )
            GDALClose( hDstDS );
        CSLDestroy( papszOptions );

파이썬 코드:

.. code-block:: python

    src_ds = gdal.Open(src_filename)
    dst_ds = driver.CreateCopy(dst_filename, src_ds, strict=0,
                            options=["TILED=YES", "COMPRESS=PACKBITS"])
    # 작업이 끝나면 데이터셋을 제대로 종료합니다
    dst_ds = None
    src_ds = None

Create() 사용하기
-----------------

기존 파일을 그냥 새 파일로 내보내는 것이 아닌 상황이라면, (가상 파일 또는 인메모리 파일을 이용해서 몇몇 흥미로운 옵션들을 사용할 수 있긴 하지만) 일반적으로 :cpp:func:`GDALDriver::Create` 메소드를 이용해야 합니다. :cpp:func:`Create` 메소드는 :cpp:func:`CreateCopy` 와 대부분 비슷한 옵션 목록을 입력받지만, 이미지 크기, 밴드 개수 및 밴드 유형을 명확하게 지정해줘야만 합니다:

C++ 코드:

.. code-block:: c++

    GDALDataset *poDstDS;
    char **papszOptions = NULL;
    poDstDS = poDriver->Create( pszDstFilename, 512, 512, 1, GDT_Byte,
                                papszOptions );

C 코드:

.. code-block:: c

    GDALDatasetH hDstDS;
    char **papszOptions = NULL;
    hDstDS = GDALCreate( hDriver, pszDstFilename, 512, 512, 1, GDT_Byte,
                        papszOptions );

파이썬 코드:

.. code-block:: python

    dst_ds = driver.Create(dst_filename, xsize=512, ysize=512,
                        bands=1, eType=gdal.GDT_Byte)

데이터셋을 성공적으로 생성하고 나면, 파일에 적절한 모든 메타데이터와 래스터 데이터를 작성해야만 합니다. 사용례에 따라 어떤 메타데이터와 래스터 데이터가 적절한지 달라지지만, 다음은 투영법, 지리변환 및 래스터 데이터를 처리하는 단순한 경우의 예시입니다:

C++ 코드:

.. code-block:: c++

    double adfGeoTransform[6] = { 444720, 30, 0, 3751320, 0, -30 };
    OGRSpatialReference oSRS;
    char *pszSRS_WKT = NULL;
    GDALRasterBand *poBand;
    GByte abyRaster[512*512];
    poDstDS->SetGeoTransform( adfGeoTransform );
    oSRS.SetUTM( 11, TRUE );
    oSRS.SetWellKnownGeogCS( "NAD27" );
    oSRS.exportToWkt( &pszSRS_WKT );
    poDstDS->SetProjection( pszSRS_WKT );
    CPLFree( pszSRS_WKT );
    poBand = poDstDS->GetRasterBand(1);
    poBand->RasterIO( GF_Write, 0, 0, 512, 512,
                    abyRaster, 512, 512, GDT_Byte, 0, 0 );
    /* 작업이 끝나면 데이터셋을 제대로 종료합니다 */
    GDALClose( (GDALDatasetH) poDstDS );

C 코드:

.. code-block:: c

    double adfGeoTransform[6] = { 444720, 30, 0, 3751320, 0, -30 };
    OGRSpatialReferenceH hSRS;
    char *pszSRS_WKT = NULL;
    GDALRasterBandH hBand;
    GByte abyRaster[512*512];
    GDALSetGeoTransform( hDstDS, adfGeoTransform );
    hSRS = OSRNewSpatialReference( NULL );
    OSRSetUTM( hSRS, 11, TRUE );
    OSRSetWellKnownGeogCS( hSRS, "NAD27" );
    OSRExportToWkt( hSRS, &pszSRS_WKT );
    OSRDestroySpatialReference( hSRS );
    GDALSetProjection( hDstDS, pszSRS_WKT );
    CPLFree( pszSRS_WKT );
    hBand = GDALGetRasterBand( hDstDS, 1 );
    GDALRasterIO( hBand, GF_Write, 0, 0, 512, 512,
                abyRaster, 512, 512, GDT_Byte, 0, 0 );
    /* 작업이 끝나면 데이터셋을 제대로 종료합니다 */
    GDALClose( hDstDS );

파이썬 코드:

.. code-block:: python

    from osgeo import osr
    import numpy
    dst_ds.SetGeoTransform([444720, 30, 0, 3751320, 0, -30])
    srs = osr.SpatialReference()
    srs.SetUTM(11, 1)
    srs.SetWellKnownGeogCS("NAD27")
    dst_ds.SetProjection(srs.ExportToWkt())
    raster = numpy.zeros((512, 512), dtype=numpy.uint8)
    dst_ds.GetRasterBand(1).WriteArray(raster)
    # 작업이 끝나면 데이터셋을 제대로 종료합니다
    dst_ds = None

