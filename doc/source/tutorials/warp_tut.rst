.. _warp_tut:

================================================================================
GDAL 왜곡(warp) API 예제 (재투영 등등)
================================================================================

.. highlight:: cpp

개요
--------

(:ref:`gdalwarper.h <gdalwarp_cpp>` 에 선언된) GDAL 왜곡 API는 응용 프로그램이 제공하는 측지 변환 함수(GDALTransformerFunc), 다양한 리샘플링 커널들, 그리고 다양한 마스크 작업 옵션을 이용해서 고성능 이미지 왜곡 작업을 위한 서비스를 제공합니다. 메모리에 다 담을 수 없을 정도로 대용량인 파일도 왜곡시킬 수 있습니다.

이 예제는 왜곡 API를 이용하는 응용 프로그램을 구현하는 방법을 보여줍니다. 왜곡 API 용 C 및 파이썬 바인딩이 불완전하기 때문에 C++ 언어로 구현한다고 가정합니다. 개발자가 :ref:`raster_data_model` 그리고 일반 GDAL API에도 익숙하다고 가정합니다.

일반적으로 응용 프로그램은 사용할 옵션을 가진 :cpp:class:`GDALWarpOptions` 구조를 초기화하고, 이 옵션들을 기반으로 :cpp:class:`GDALWarpOperation` 을 인스턴스화한 다음, :cpp:func:`GDALWarpOperation::ChunkAndWarpImage` 메소드를 호출해서 내부적으로 :cpp:class:`GDALWarpKernel` 이용하는 왜곡 옵션들을 실행, 왜곡 작업을 수행합니다.

단순 재투영 사례
----------------

먼저 상대적으로 이미지를 재투영하는 단순한 예시를 구성할 것입니다. 적절한 산출 파일이 이미 존재하고 오류 확인은 최소화한다고 가정합니다.

.. code-block::

    #include "gdalwarper.h"

    int main()
    {
        GDALDatasetH  hSrcDS, hDstDS;

        // 입력 및 산출 파일 열기
        GDALAllRegister();
        hSrcDS = GDALOpen( "in.tif", GA_ReadOnly );
        hDstDS = GDALOpen( "out.tif", GA_Update );

        // 왜곡 옵션 설정
        GDALWarpOptions *psWarpOptions = GDALCreateWarpOptions();
        psWarpOptions->hSrcDS = hSrcDS;
        psWarpOptions->hDstDS = hDstDS;
        psWarpOptions->nBandCount = 1;
        psWarpOptions->panSrcBands =
            (int *) CPLMalloc(sizeof(int) * psWarpOptions->nBandCount );
        psWarpOptions->panSrcBands[0] = 1;
        psWarpOptions->panDstBands =
            (int *) CPLMalloc(sizeof(int) * psWarpOptions->nBandCount );
        psWarpOptions->panDstBands[0] = 1;
        psWarpOptions->pfnProgress = GDALTermProgress;

        // 재투영 변환기 설정
        psWarpOptions->pTransformerArg =
            GDALCreateGenImgProjTransformer( hSrcDS,
                                            GDALGetProjectionRef(hSrcDS),
                                            hDstDS,
                                            GDALGetProjectionRef(hDstDS),
                                            FALSE, 0.0, 1 );
        psWarpOptions->pfnTransformer = GDALGenImgProjTransform;

        // 왜곡 작업 초기화 및 실행
        GDALWarpOperation oOperation;
        oOperation.Initialize( psWarpOptions );
        oOperation.ChunkAndWarpImage( 0, 0,
                                    GDALGetRasterXSize( hDstDS ),
                                    GDALGetRasterYSize( hDstDS ) );
        GDALDestroyGenImgProjTransformer( psWarpOptions->pTransformerArg );
        GDALDestroyWarpOptions( psWarpOptions );
        GDALClose( hDstDS );
        GDALClose( hSrcDS );
        return 0;
    }

이 예시는 기존 입력 및 산출 파일을 (in.tif 및 out.tif를) 엽니다. A :cpp:class:`GDALWarpOptions` 구조를 할당하고 (:cpp:func:`GDALCreateWarpOptions` 함수가 여러 가지에 대해 합리적인 기본값을 설정하기 때문에, 기본값을 사용하려면 항상 이 함수를 사용하십시오) 입력 및 산출 파일 핸들과 밴드 목록을 설정합니다. 여기에 'panSrcBands' 및 'panDstBands' 목록을 동적으로 할당한 다음, 나중에 :cpp:func:`GDALDestroyWarpOptions` 함수로 자동 해제할 것입니다. 단순한 터미널 산출 진행 상황 모니터(:cpp:func:`GDALTermProgress`)를 설치해서 사용자에게 완료 진행 상황을 리포트합니다.

:cpp:func:`GDALCreateGenImgProjTransformer` 를 사용해서 소스와 대상 이미지 사이의 재투영 변환을 초기화합니다. 이미 소스 및 대상 이미지에 합리적인 경계와 좌표계가 설정되어 있다고 가정합니다. GCP는 사용할 수 없습니다.

옵션 구조의 준비가 끝나면 이 옵션들을 사용해서 :cpp:class:`GDALWarpOperation` 클래스를 인스턴스화하고, 실제 왜곡 작업은 :cpp:func:`GDALWarpOperation::ChunkAndWarpImage` 메소드가 수행합니다. 그 다음 변환기, 왜곡 옵션, 그리고 데이터셋들을 정리합니다.

일반적으로 파일을 연 다음, 재투영 변환기를 설정한 다음 (실패 시 NULL을 반환합니다) 그리고 왜곡을 초기화한 다음 오류 확인이 필요할 것입니다.

다른 재투영 옵션들
------------------

:cpp:class:`GDALWarpOptions` 구조는 왜곡 작업 습성을 제거하는 데 사용할 수 있는 여러 가지 옵션들을 담고 있습니다. 그 중에서 특히 흥미로운 옵션들을 소개합니다:

-  :cpp:member:`GDALWarpOptions::dfWarpMemoryLimit`:
   작업할 이미지 덩어리(chunk)의 용량을 선택하는 경우 :cpp:class:`GDALWarpOperation` 이 사용할 수 있는 최대 메모리 용량을 설정합니다. 이 값은 바이트 단위이며, 기본값은 보수적일 (작을) 가능성이 높습니다. 덩어리 크기를 늘리면 몇몇 상황에서 상당한 도움이 될 수도 있지만, 덩어리 용량 더하기 GDAL 캐시 용량 더하기 GDAL, 사용자 응용 프로그램 및 운영 체제가 사용하는 총 메모리 용량이 RAM 용량을 넘지 않도록 주의해야 합니다. 그렇지 않으면 과도한 메모리 스와핑 때문에 성능이 저하될 가능성이 큽니다. RAM 256MB를 가진 시스템 상에서는 최소 64MB(약 64,000,000바이트) 값이 합리적입니다. 이 값에 GDAL이 저수준 블록 캐시 작업에 사용하는 메모리는 포함되지 않는다는 사실을 기억하십시오.

-  :cpp:member:`GDALWarpOpations::eResampleAlg`:
   'GRA_NearestNeighbour'(기본값, 가장 빠름), 'GRA_Bilinear'(2x2 이중선형 리샘플링) 또는 'GRA_Cubic' 가운데 하나로 설정합니다. 테마 이미지(주제도) 또는 색상 매핑 이미지의 경우 일반적으로 'GRA_NearestNeighbour' 유형으로 설정해야 합니다. 테마 이미지의 경우, 특히 해상도를 상당하게 변경하는 경우 다른 리샘플링 유형들이 더 나은 결과를 보일 수도 있습니다.

-  :cpp:member:`GDALWarpOptions::padfSrcNoDataReal`:
   일부 배경 픽셀값이 대상 이미지로 복사되는 일을 막고 싶은 경우 이 배열을 (처리되는 밴드 당 배열 하나씩) 각 밴드에 대한 "NODATA" 값으로 설정할 수도 있습니다.

-  :cpp:member:`GDALWarpOptions::papszWarpOptions`:
   왜곡기(warper)로 전송되는 "이름=값" 옵션들의 문자열 목록입니다. :cpp:member:`GDALWarpOptions::papszWarpOptions` 문서에서 모든 옵션을 볼 수 있습니다. 그 중에서도 다음 옵션들을 지원합니다:

   *  INIT_DEST=[value] 또는 INIT_DEST=NO_DATA:
      이 옵션은 대상 이미지를 (모든 밴드에 대해) 설정된 값으로 강제로 초기화하거나, 또는 'padfDstNoDataReal' / 'padfDstNoDataImag' 에 있는 NO_DATA 값으로 초기화해야 한다는 사실을 나타냅니다. 이 값을 설정하지 않는 경우 대상 이미지를 읽어와서 그 위에 소스 이미지를 왜곡한 이미지를 덮어쓸 것입니다.

   *  WRITE_FLUSH=YES/NO:
      이 옵션은 각 덩어리를 처리한 다음 강제로 데이터를 디스크로 플러싱합니다. 어떤 경우 이 옵션은 산출 데이터를 직렬 쓰기하도록 보장합니다. 그렇지 않으면 입력 버퍼의 데이터 블록을 읽어올 때마다 데이터 블록이 디스크에 작성되기 때문에 디스크 상에서 수많은 추가 검색이 발생하고 I/O 처리량이 감소할 수 있습니다. 현재 기본값은 NO입니다.

산출 파일 생성하기
------------------

앞의 예시에서는 적절한 산출 파일이 이미 존재한다고 가정했습니다. 이번에는 새 좌표계에서 적절한 경계를 가지는 새 파일을 생성하는 사례를 살펴볼 것입니다. 이 작업은 왜곡 API와 특별히 관련이 있지는 않습니다. 그냥 변환(transformation) API를 사용할 뿐입니다.

.. code-block::

    #include "gdalwarper.h"
    #include "ogr_spatialref.h"
    ...
    GDALDriverH hDriver;
    GDALDataType eDT;
    GDALDatasetH hDstDS;
    GDALDatasetH hSrcDS;

    // 소스 파일 열기
    hSrcDS = GDALOpen( "in.tif", GA_ReadOnly );
    CPLAssert( hSrcDS != NULL );

    // 첫 번째 입력 밴드와 동일한 데이터 유형으로 산출물 생성
    eDT = GDALGetRasterDataType(GDALGetRasterBand(hSrcDS,1));

    // 산출 드라이버 (GeoTIFF 포맷) 불러오기
    hDriver = GDALGetDriverByName( "GTiff" );
    CPLAssert( hDriver != NULL );

    // 소스 좌표계 가져오기
    const char *pszSrcWKT, *pszDstWKT = NULL;
    pszSrcWKT = GDALGetProjectionRef( hSrcDS );
    CPLAssert( pszSrcWKT != NULL && strlen(pszSrcWKT) > 0 );

    // 산출 좌표계 (UTM 11 WGS84) 설정
    OGRSpatialReference oSRS;
    oSRS.SetUTM( 11, TRUE );
    oSRS.SetWellKnownGeogCS( "WGS84" );
    oSRS.exportToWkt( &pszDstWKT );

    // 소스 픽셀/줄 좌표를 (대상 픽셀/줄 좌표가 아니라)
    // 대상 지리참조 좌표로 매핑하는 변환기 생성.
    // 대상 데이터셋 핸들을 (NULL로 설정해서) 생략하면 됩니다.
    void *hTransformArg;
    hTransformArg =
        GDALCreateGenImgProjTransformer( hSrcDS, pszSrcWKT, NULL, pszDstWKT,
                                         FALSE, 0, 1 );
    CPLAssert( hTransformArg != NULL );

    // 파일의 산출 지리참조 경계 및 해상도의 근사치 가져오기
    double adfDstGeoTransform[6];
    int nPixels=0, nLines=0;
    CPLErr eErr;
    eErr = GDALSuggestedWarpOutput( hSrcDS,
                                    GDALGenImgProjTransform, hTransformArg,
                                    adfDstGeoTransform, &nPixels, &nLines );
    CPLAssert( eErr == CE_None );
    GDALDestroyGenImgProjTransformer( hTransformArg );

    // 산출 파일 생성
    hDstDS = GDALCreate( hDriver, "out.tif", nPixels, nLines,
                         GDALGetRasterCount(hSrcDS), eDT, NULL );
    CPLAssert( hDstDS != NULL );

    // 투영법 정의 작성
    GDALSetProjection( hDstDS, pszDstWKT );
    GDALSetGeoTransform( hDstDS, adfDstGeoTransform );

    // 필수인 경우 색상표 복사
    GDALColorTableH hCT;
    hCT = GDALGetRasterColorTable( GDALGetRasterBand(hSrcDS,1) );
    if( hCT != NULL )
        GDALSetRasterColorTable( GDALGetRasterBand(hDstDS,1), hCT );
    ... 이전과 마찬가지로 왜곡 작업 진행 ...

이 논리에 대해 조금 설명하자면:

-  변환기(transformer)를 사용해서 소스 이미지에 있는 픽셀을 대상 지리참조 좌표와 매핑하기 때문에, 픽셀/줄 좌표가 아니라 지리참조 좌표를 산출하는 변환기를 생성해야 합니다.

-  :cpp:func:`GDALSuggestedWarpOutput` 함수는 소스 이미지의 모든 픽셀을 담아야 할 산출 이미지 크기 및 지리참조된 범위를 서술하는 'adfDstGeoTransform', 'nPixels' 및 'nLines'를 반환할 것입니다. 해상도는 소스와 비슷해야 하지만, 산출 픽셀은 입력 픽셀의 형태와 관계없이 항상 정사각형입니다.

-  왜곡기는 산출 파일의 포맷이 "임의" 쓰기를 지원하는 포맷일 것을 요구합니다. 이 때문에 일반적으로 (:cpp:func:`CreateCopy` 가 아닌) :cpp:func:`Create` 메소드를 구현하는 비압축 포맷으로 제한됩니다. 압축 포맷으로 또는 :cpp:func:`CreateCopy` 스타일 포맷으로 왜곡시키려면 더 나은 습성을 가진 포맷으로 이미지의 전체 임시 복사본을 생성한 다음 :cpp:func:`CreateCopy` 메소드를 이용해서 원하는 최종 포맷으로 변환해야 합니다.

-  왜곡 API는 픽셀만 복사합니다. 응용 프로그램이 모든 색상표, 지리참조 정보 및 기타 메타데이터를 대상으로 복사해야만 합니다.

성능 최적화
-----------

왜곡 API의 성능을 최적화하기 위해 할 수 있는 일이 많이 있습니다:

-  왜곡 API 덩어리 작업에 사용할 수 있는 메모리 용량을 증가시켜 한 번에 더 큰 덩어리를 작업할 수 있게 하십시오. :cpp:member:`GDALWarpOptions::dfWarpMemoryLimit` 파라미터의 값입니다. 이론적으로 작업하는 덩어리 용량이 클수록 I/O 전략과 근사치 변환의 효율이 더 높아질 것입니다. 하지만 왜곡 메모리와 GDAL 캐시의 합이 RAM 용량보다 작아야 합니다. RAM 용량의 2/3이 적당합니다.

-  GDAL 캐시 작업 용 메모리 용량을 증가시키십시오. 스캔라인 지향 대용량 입력 및 산출 이미지를 작업하는 경우 특히 중요합니다. 입력 및 산출 스캔라인이 교차하는 각 덩어리마다 입력 및 산출 스캔라인을 다시 읽어와야 한다면 성능이 크게 저하될 수도 있습니다. GDAL 내부 캐시 작업에 사용할 수 있는 메모리 용량은 :cpp:func:`GDALSetCacheMax` 로 제어할 수 있습니다.

-  변환할 각 픽셀에 대해 정확한 재투영 대신 근사치 변환을 사용하십시오. 다음 코드는 재투영 변환을 기반으로 오류 한계값을 (산출 픽셀의 'dfErrorThreshold') 지정해서 근사치 변환을 생성할 수 있는 방법을 보여줍니다.

.. code-block::

    hTransformArg =
        GDALCreateApproxTransformer( GDALGenImgProjTransform,
                                     hGenImgProjArg, dfErrorThreshold );
    pfnTransformer = GDALApproxTransform;

-  비어 있는 산출 파일을 작성하는 경우, :cpp:member:`GDALWarpOptions::papszWarpOptions` 파라미터에 INIT_DEST 옵션을 사용해서 산출 덩어리를 산출물로부터 읽어오는 대신 고정값으로 초기화하십시오. 필요없는 I/O 작업을 크게 줄일 수 있습니다.

-  타일화 입력 및 산출 포맷을 사용하십시오. 타일화 포맷은 추가 이미지 데이터를 크게 건드릴 필요없이 소스 및 대상 영상의 지정한 덩어리에 접근할 수 있게 해줍니다. 대용량 스캔라인 지향 파일의 경우 추가적인 I/O 작업이 크게 낭비될 수 있습니다.

-  모든 밴드를 호출 한 번으로 처리하십시오. 변환 연산을 각 밴드별로 해야 할 필요를 없애줍니다.

-  :cpp:func:`GDALWarpOperation::ChunkAndWarpImage` 대신 :cpp:func:`GDALWarpOperation::ChunkAndWarpMulti` 메소드를 사용하십시오. 개별 스레드에서 I/O와 실제 이미지 왜곡 작업을 각각 수행하기 때문에 CPU 및 I/O 대역폭을 더 효율적으로 사용할 수 있습니다. 이를 위해서는 GDAL이 멀티스레딩 지원과 함께 빌드되어 있어야 합니다. (Win32 및 유닉스 상에서는 기본값이며, 이전 버전들의 경우 환경설정에 "-with-threads" 파라미터가 필수입니다.)

-  리샘플링 커널은 요구되는 작업이 가장 적은 경우 최근접 이웃(nearest neighbour), 그 다음 이중선형(bilinear), 그리고 가장 많은 경우 3차(cubic)로 달라집니다. 필요한 것보다 더 복잡한 리샘플링 커널을 사용하지 마십시오.

-  공통 특수 사례에 특수 단순화 논리 사례를 사용하도록 난해한 마스크 작업 옵션 사용을 피하십시오. 예를 들어 일반 사례와 비교했을 때 8비트 데이터를 마스크를 사용하지 않고 최근접 이웃 리샘플링하는 경우가 훨씬 최적화가 잘 되어 있습니다.

기타 마스크 작업 옵션
---------------------

:cpp:class:`GDALWarpOptions` 클래스는 입력물 및 출력물에 대한 무결성(validity) 마스크 및 밀도(density) 마스크와 관련된 난해한 마스크 작업 케이퍼빌리티를 다수 포함하고 있습니다. 이 가운데 몇몇은 아직 구현되지 않았고, 다른 몇몇은 구현되었으나 제대로 테스트되지 않았습니다. 현재, 밴드별 무결성 마스크를 제외한 다른 기능들은 주의해서 사용할 것을 권장합니다.

