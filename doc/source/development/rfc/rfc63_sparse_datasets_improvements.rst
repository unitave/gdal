.. _rfc-63:

=======================================================================================
RFC 63 : 희소 데이터셋 개선
=======================================================================================

저자: 이벤 루올

연락처: even.rouault@spatialys.com

상태: 승인, GDAL 2.2버전에 구현

요약
----

이 RFC는 희소(sparse) 데이터셋을, 다시 말해 비어 있는 영역들을 상당히 많이 담고 있을 수 있는 데이터셋을 관리하기 위한 개선 사항을 제안합니다.

점근법
------

매우 큰 공간 범위를 커버하지만 상당한 부분에 데이터가 없는 데이터셋을 읽어오거나 생성할 필요가 있는 사용례가 존재합니다. GDAL API에는 데이터가 어떤 영역을 커버하고 어떤 영역을 커버하지 않는지를 빠르게 알 수 있는 방법이 전혀 없기 때문에 모든 픽셀을 처리해야만 합니다. 이런 방식은 비효율적입니다. 반면 GeoTIFF, VRT 또는 GeoPackage 같은 일부 포맷들은 픽셀들을 처리하지 않고서도 이런 정보를 제공할 수 있는 가능성이 있습니다.

따라서 :cpp:class:`GDALRasterBand` 클래스에 관심 영역의 창을 입력받고 해당 영역이 데이터로 이루어져 있는지, 비어 있는 블록인지, 또는 두 상태가 혼합되어 있는지를 반환하는 새로운 GetDataCoverageStatus() 메소드를 추가할 것을 제안합니다.

산출 드라이버가 그렇게 명령하는 경우 (CreateCopy() 및 gdal_translate가 사용하는) GDALDatasetCopyWholeRaster() 메소드가 이 메소드를 사용해서 희소 영역을 처리하는 일을 막을 것입니다.

C++ API
-------

:cpp:class:`GDALRasterBand` 클래스에 새 가상 메소드를 추가합니다:

::

    virtual int IGetDataCoverageStatus( int nXOff, int nYOff,
                                        int nXSize, int nYSize,
                                        int nMaskFlagStop,
                                        double* pdfDataPct);


   /**
    * \brief 래스터 하위 창의 커버리지 상태를 가져옵니다.
    *
    * 래스터의 하위 창이 데이터만 담고 있는지, 비어 있는 블록들만 담고 있는지,
    * 또는 두 상태가 혼합되어 있는지 여부를 반환합니다. 희소할 수도 있는
    * 데이터셋에 RasterIO / ReadBlock 요청을 발행할 가치가 있는지를 빠르게
    * 판단하는 데 이 함수를 사용할 수 있습니다.
    *
    * 비어 있는 블록이란 설정 시 값이 NODATA 값인 픽셀만 담고 있는 블록 또는
    * NODATA 값을 설정하지 않은 경우 값이 0인 픽셀만 담고 있는 블록을 말합니다.
    *
    * 실제 픽셀 값을 읽지 않는 효율적인 방식으로 쿼리를 수행합니다.
    * 이렇게 수행할 수 없거나 드라이버가 이를 전혀 구현하지 않는 경우,
    * GDAL_DATA_COVERAGE_STATUS_UNIMPLEMENTED | GDAL_DATA_COVERAGE_STATUS_DATA를
    * 반환할 것입니다.
    *
    * 함수가 반환할 수 있는 값은 다음과 같습니다. 이때 값이 바이너리 또는
    * 연산자와 결합되어 있을 수도 있습니다:
    * <ul>
    * <li>GDAL_DATA_COVERAGE_STATUS_UNIMPLEMENTED: 드라이버가 GetDataCoverageStatus()를
    * 구현하고 있지 않습니다. 이 플래그는 GDAL_DATA_COVERAGE_STATUS_DATA와 함께
    * 반환되어야 합니다.</li>
    * <li>GDAL_DATA_COVERAGE_STATUS_DATA: 쿼리 창에 데이터가 있을 가능성이 있습니다.</li>
    * <li>GDAL_DATA_COVERAGE_STATUS_EMPTY: 쿼리 창에 데이터가 없습니다. 일반적으로
    * 누락된 블록이라는 개념을 지원하는 포맷에 있는 누락된 블록으로 식별됩니다.
    * </li>
    * </ul>
    *
    * GDAL_DATA_COVERAGE_STATUS_DATA가 가짜 양의 값을 가질 수도 있으며 데이터가 존재할
    * 가능성에 대한 힌트로 해석해야 한다는 사실을 기억하십시오. 예를 들어
    * GeoTIFF 파일이 0으로 채워진 블록들로 생성되었다면 (또는 NODATA 값으로
    * 설정되었다면) 누락된 블록 메커니즘을 사용하는 대신
    * GDAL_DATA_COVERAGE_STATUS_DATA를 반환할 것입니다. 이와는 반대로,
    * GDAL_DATA_COVERAGE_STATUS_EMPTY는 가짜 양의 값을 가지지 않을 것입니다.
    *
    * nMaskFlagStop은 일반적으로 0으로 설정해야 합니다. 계산된 마스크가 nMaskFlagStop과
    * 일치하는 즉시 함수를 빠르게 종료할 수 있도록 앞에서 언급한 값들을
    * Binary OR 처리한 마스크로 설정할 수 있습니다. 예를 들어
    * 래스터 전체에 대해 nMaskFlagStop = GDAL_DATA_COVERAGE_STATUS_EMPTY로 요청을
    * 발행할 수 있습니다. 누락된 블록 하나를 발견하는 즉시 함수를 종료할 것이기
    * 때문에, 어떤 특정 영역(들)에 누락된 블록이 있는지를 찾을 수 있도록
    * 요청 영역을 세밀하게 구분할 수 있습니다.
    *
    * @see GDALGetDataCoverageStatus() 참조
    *
    * @param nXOff 쿼리할 밴드 영역의 좌상단 모서리에 대한 픽셀 오프셋입니다.
    *              좌측에서 시작하는 0일 것입니다.
    *
    * @param nYOff 쿼리할 밴드 영역의 좌상단 모서리에 대한 줄 오프셋입니다.
    *              상단에서 시작하는 0일 것입니다.
    *
    * @param nXSize 쿼리할 밴드 영역의 픽셀 단위 너비입니다.
    *
    * @param nYSize 쿼리할 밴드 영역의 픽셀 단위 높비입니다.
    *
    * @param nMaskFlagStop 0, 또는 GDAL_DATA_COVERAGE_STATUS_UNIMPLEMENTED,
    *                      또는 GDAL_DATA_COVERAGE_STATUS_DATA 및
    *                      GDAL_DATA_COVERAGE_STATUS_EMPTY의 가능한 값들을
    *                      Binary OR 처리한 마스크입니다. 커버리지 계산이
    *                      마스크와 일치하는 즉시 계산을 종료할 것입니다.
    *                      이 경우 *pdfDataPct가 무결하지 않을 것입니다.
    *
    * @param pdfDataPct 이 파라미터가 가리키는 값이 무결한 값을 가진 쿼리된
    *                   하위 창에 있는 픽셀들의 [0,100] 범위의 (근사치) 백분율로
    *                   설정될 선택적인 산출 파라미터입니다. 이 구현이 항상 이를
    *                   계산할 수 없을 수도 있는데, 이런 경우 음의 값으로 설정될 것입니다.
    *
    * @return GDAL_DATA_COVERAGE_STATUS_UNIMPLEMENTED, 또는 GDAL_DATA_COVERAGE_STATUS_DATA 및
    *         GDAL_DATA_COVERAGE_STATUS_EMPTY의 가능한 값들을 Binary OR 처리한 조합을
    *         반환합니다.
    *
    * @note GDAL 2.2버전에 추가
    */

이 메소드는 ``GDAL_DATA_COVERAGE_STATUS_UNIMPLEMENTED | GDAL_DATA_COVERAGE_STATUS_DATA`` 를 반환하는 비지능형(dumb) 기본 구현을 가지고 있습니다.

공개(public) API는 다음과 같이 구성됩니다:

::


   /** 드라이버가 GetDataCoverageStatus()를 구현하지 않은 경우
    * GDALGetDataCoverageStatus()가 반환하는 플래그입니다.
    * 이 플래그는 GDAL_DATA_COVERAGE_STATUS_DATA와 함께 반환되어야 합니다. */
   #define GDAL_DATA_COVERAGE_STATUS_UNIMPLEMENTED 0x01

   /** 쿼리 창에 데이터가 있을 가능성이 있는 경우
    * GDALGetDataCoverageStatus()가 반환하는 플래그입니다.
    * GDAL_DATA_COVERAGE_STATUS_UNIMPLEMENTED 또는
    * GDAL_DATA_COVERAGE_STATUS_EMPTY를 가진 바이너리 또는 연산자와
    * 결합될 수 있습니다. */
   #define GDAL_DATA_COVERAGE_STATUS_DATA          0x02

   /** 쿼리 창에 데이터가 없는 경우 GDALGetDataCoverageStatus()가
    * 반환하는 플래그입니다. 일반적으로 누락된 블록이라는 개념을
    * 지원하는 포맷에 있는 누락된 블록으로 식별됩니다.
    * GDAL_DATA_COVERAGE_STATUS_DATA를 가진 바이너리 또는 연산자와
    * 결합될 수 있습니다. */
   #define GDAL_DATA_COVERAGE_STATUS_EMPTY         0x04


   C++ :

   int  GDALRasterBand::GetDataCoverageStatus( int nXOff,
                                               int nYOff,
                                               int nXSize,
                                               int nYSize,
                                               int nMaskFlagStop,
                                               double* pdfDataPct)

   C :
   int GDALGetDataCoverageStatus( GDALRasterBandH hBand,
                                  int nXOff, int nYOff,
                                  int nXSize,
                                  int nYSize,
                                  int nMaskFlagStop,
                                  double* pdfDataPct);

:cpp:func:`GDALRasterBand::GetDataCoverageStatus` 는 IGetDataCoverageStatus()를 호출하기 전에 창의 무결성에 대한 기본적인 확인을 수행합니다.

변경 사항
---------

GDALDatasetCopyWholeRaster() 및 GDALRasterBandCopyWholeRaster()는 산출 드라이버가 YES로 설정해서 소스 데이터셋이 구멍(hole)만 담고 있는지 또는 그렇지 않은지 여부를 판단하기 위해 소스 데이터셋의 각 덩어리(chunk)에 대해 GetDataCoverageStatus()를 호출하게 만드는 SKIP_HOLES 옵션을 받아들입니다.

드라이버
--------

이 RFC는 GeoTIFF 및 VRT 드라이버가 IGetDataCoverageStatus() 메소드를 구현하도록 업그레이드합니다.

GeoTIFF 드라이버에는 이 주제와 관련된, 예를 들어 CreateCopy() 모드에서 SPARSE_OK=YES 생성 옵션을 입력받을 수 있는 (또는 업데이트 모드에서 SPARSE_OK 열기 옵션을 입력 받을 수 있는) 기능을 포함하는 수많은 이전의 개선 사항들도 적용합니다.

다음은 GeoTIFF 드라이버 문서에서 발췌한 내용입니다:

::

   GDAL은 오프셋과 바이트 개수가 0으로 설정된 TIFF 타일 또는 스트립, 즉
   대응하는 할당된 물리적 저장소가 없는 타일 또는 스트립을 특별하게
   해석합니다. 이런 파일을 읽어오는 경우, 이런 타일 또는 스트립이
   정의되었을 때 명확하게 0 또는 NODATA 값으로 설정되었다고 간주합니다.
   이런 파일을 작성할 때 Create() 인터페이스를 통해 SPARSE_OK 생성
   옵션을 YES로 설정하면 이런 타일 또는 스트립 생성을 활성화할 수
   있습니다. 그 다음, IWriteBlock()/IRasterIO() 인터페이스를 통해
   작성되지 않은 블록들의 오프셋과 바이트 개수를 0으로 설정할 것입니다.
   파일의 값을 채우기 위한 이후 처리 과정으로 넘기기 전에 파일을 초기화
   해야만 하는 경우 이 옵션이 디스크 용량 및 시간을 절약하는 데 특히 유용
   합니다. 다음 문단에서 논의할 또다른 희소 메커니즘과 혼동하지 않기 위해,
   이런 내포 타일/스트립을 가진 파일을 "TIFF 희소 파일"이라고 부를 것입니다.
   GDAL 기반이 아닌 TIFF 판독기는 이런 파일을 상호 작업할 수 **없을**
   것이며, 이런 내포 타일/스트립을 가진 파일을 결함이 있다고 간주할 것입니다.

   GDAL 2.2버전부터, 이 메커니즘이 (업데이트 모드를 위해) CreateCopy()는 물론
   Open() 인터페이스까지 확장되었습니다. SPARSE_OK 생성 옵션을 (또는 Open()의
   경우 SPARSE_OK 열기 옵션을) YES로 설정하면, 모든 0 또는 NODATA 블록을
   작성하려는 시도조차 탐지해서 이런 타일 또는 스트립이 물리적 저장소에
   할당되지 않도록 할 것입니다. (이미 저장소에 할당되어 있는 경우, 그 내용을
   0 또는 NODATA 내용으로 대체할 것입니다.)

   GDAL 2.2버전부터, SPARSE_OK를 정의하지 않으면 (또는 기본값 FALSE로 설정하면)
   NODATA 값이 설정되지 않았거나 0으로 설정된 비압축 파일의 경우, Create() 및
   CreateCopy() 모드에서 이 드라이버는 파일의 가장 마지막 부분에 작성하기 위해
   그리고 어떤 의미에서는 파일 시스템의 희소 파일 메커니즘과 호환될 수 있도록
   (앞에서 논의했던 TIFF 희소 파일 확장 사양과 구별할 수 있도록) 파일이 닫힐
   때까지 0값 블록의 할당을 지연시킬 것입니다. 즉 TIFF 관점에서는 모든 비어 있는
   블록이 제대로 할당된 것처럼 보이지만 (대응하는 타일/스트립이 무결한 오프셋과
   바이트 개수를 가질 것이지만) 대응하는 물리적 저장소는 없을 것입니다. 물론
   파일 시스템이 이런 희소 파일을 지원하는 경우에 말입니다. 리눅스의 유명한
   파일 시스템 대부분(ext2/3/4, xfs, btfs 등등) 또는 윈도우의 NTFS가 희소 파일을
   지원합니다. 파일 시스템이 희소 파일을 지원하지 않는다면 물리적 저장소를
   할당하고 0으로 채울 것입니다.

바인딩
------

파이썬 바인딩에 GDALGetDataCoverageStatus()의 매핑을 추가합니다. 다른 바인딩들도 업데이트할 수 있습니다. (상태 플래그와 백분율을 둘 다 반환할 수 있는 방법을 알아내야 합니다.)

유틸리티
--------

유틸리티에는 직접적인 변경 사항이 없습니다.

결과물
------

이 새로운 케이퍼빌리티를 사용하면, 각각 20x20 픽셀 크기의 영역을 2개 담고 있는 200,000 x 200,000 픽셀 크기의 VRT를 gdal_translate를 통해 2초만에 희소 타일 GeoTIFF로 변환할 수 있습니다. 산출되는 GeoTIFF 자체도 또다른 희소 타일 GeoTIFF로 동시에 변환할 수 있습니다.

향후 작업
---------

향후 오버뷰 작성 및 왜곡 작업에 새 케이퍼빌리티를 사용하도록 할 수 있습니다. 다른 드라이버들도 이 새 케이퍼빌리티로부터 혜택을 볼 수 있습니다:

   -  GeoPackage
   -  ERDAS Imagine
   -  ...

문서화
------

새로운 메소드를 문서화합니다.

테스트 스위트
-------------

VRT 및 GeoTIFF 드라이버의 테스트가 IGetDataCoverageStatus() 구현을 테스트하도록 확장합니다.

호환성 문제
-----------

C++ ABI를 변경했지만, 기능적으로 호환되지 않는 부분은 예상되지 않습니다.

구현
----

이벤 루올이 이 RFC를 구현할 것입니다.

제안한 구현은 `"희소 데이터셋" 브랜치 <https://github.com/rouault/gdal2/tree/sparse_datasets>`_ 에 있습니다.

`변경 사항 목록 <https://github.com/OSGeo/gdal/compare/trunk...rouault:sparse_datasets?expand=1>`_

투표 이력
---------

-  이벤 루올 +1
-  대니얼 모리셋 +1

