.. _rfc-51:

=======================================================================================
RFC 51: RasterIO() 개선: 리샘플링 및 진행 상황 콜백
=======================================================================================

저자: 이벤 루올

연락처: even.rouault@spatialys.com

상태: 승인, GDAL 2.0버전에 구현

요약
----

이 RFC의 목적은 RasterIO() API가 서브샘플링 또는 오버샘플링을 수반하는 요청을 수행하는 경우 리샘플링 알고리즘을 지정할 수 있도록 확장하는 것입니다. 진행 상황을 알리고 사용자가 작업을 중단시킬 수 있도록 진행 상황(progress) 콜백도 지정할 수 있습니다.

핵심 변경 사항
--------------

GDALRasterIOExtraArg 구조 추가
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

새 옵션들을 담을 수 있는 새로운 GDALRasterIOExtraArg 구조(structure)를 추가합니다:

::

   /** RasterIO() 메소드에 추가 인자를 전송할 수 있는 구조
     * @since GDAL 2.0
     */
   typedef struct
   {
       /*! 구조의 버전 (구조의 향후 확장을 허용) */
       int                    nVersion;

       /*! 리샘플링 알고리즘 */ 
       GDALRIOResampleAlg     eResampleAlg;

       /*! 진행 상황 콜백 */ 
       GDALProgressFunc       pfnProgress;
       /*! 진행 상황 콜백 사용자 데이터 */ 
       void                  *pProgressData;

       /*! dfXOff, dfYOff, dfXSize 및 dfYSize가 설정되었는지 나타냅니다.
           보다 정확한 소스 창과 통신하기 위해 대부분 VRT 드라이버에 예약되어 있습니다.
           dfXOff - nXOff < 1.0, dfYOff - nYOff < 1.0, nXSize - dfXSize < 1.0
           그리고 nYSize - dfYSize < 1.0이어야만 합니다. */
       int                    bFloatingPointWindowValidity;
       /*! 좌상단 모서리에 대한 픽셀 오프셋입니다.
           bFloatingPointWindowValidity = TRUE인 경우에만 무결합니다 */
       double                 dfXOff;
       /*! 좌상단 모서리에 대한 줄 오프셋입니다.
           bFloatingPointWindowValidity = TRUE인 경우에만 무결합니다 */
       double                 dfYOff;
       /*! 관심 영역의 픽셀 단위 너비입니다.
           bFloatingPointWindowValidity = TRUE인 경우에만 무결합니다 */
       double                 dfXSize;
       /*! 관심 영역의 픽셀 단위 높이입니다.
           bFloatingPointWindowValidity = TRUE인 경우에만 무결합니다 */
       double                 dfYSize;
   } GDALRasterIOExtraArg;

   #define RASTERIO_EXTRA_ARG_CURRENT_VERSION  1

   /** GDALRasterIOExtraArg 구조의 인스턴스를 초기화하기 위한 매크로입니다.
     * @since GDAL 2.0
     */
   #define INIT_RASTERIO_EXTRA_ARG(s)  \
       do { (s).nVersion = RASTERIO_EXTRA_ARG_CURRENT_VERSION; \
            (s).eResampleAlg = GRIORA_NearestNeighbour; \
            (s).pfnProgress = NULL; \
            (s).pProgressData = NULL; \
            (s).bFloatingPointWindowValidity = FALSE; } while(0)

RasterIO() 메소드에 새로운 파라미터를 추가하는 대신 새 구조를 추가하는 데에는 몇 가지 이유가 있습니다:

-  코드 가독성 (:cpp:func:`GDALDataset::IRasterIO` 에는 이미 파라미터 14개가 있습니다.)

-  향후 모든 드라이버에서 프로토타입을 변경하지 않고 확장할 수 있도록

-  중요도는 낮지만, 효율성:
   RasterIO() 호출이 일반/특화 그리고/또는 데이터셋/래스터 밴드 구현 사이에 연결되는 것은 흔한 일입니다. 포인터만 전송하는 것이 더 효율적입니다.

이 구조에는 버전을 매깁니다. 향후 옵션을 더 추가하는 경우, 새 멤버를 구조 마지막 부분에 추가하고 버전 번호를 올릴 것입니다. 어떤 옵션을 사용할 수 있는지 판단하기 위해 GDAL 코어 및 드라이버의 코드가 버전 번호를 확인할 수 있습니다.

GDALRIOResampleAlg 구조 추가
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

다음 리샘플링 알고리즘을 사용할 수 있습니다:

::

   /** RasterIO() 리샘플링 메소드입니다.
     * @since GDAL 2.0
     */
   typedef enum
   {
       /*! 최근접 이웃(Nearest Neighbour) */               GRIORA_NearestNeighbour = 0,
       /*! 이중선형(bilinear) (2x2 kernel) */              GRIORA_Bilinear = 1,
       /*! 3차 회선 근사값(Cubic Convolution Approximation) (4x4 kernel) */
                                                           GRIORA_Cubic = 2,
       /*! 3차 B스플라인 근사값(Cubic B-Spline Approximation) (4x4 kernel) */
                                                           GRIORA_CubicSpline = 3,
       /*! 란초시 창함수 싱크 보간법(Lánczos windowed sinc interpolation) (6x6 kernel) */
                                                           GRIORA_Lanczos = 4,
       /*! 평균(average) */                                GRIORA_Average = 5,
       /*! 모드(mode) (표본 추출(sampling)한 모든 포인트 가운데 가장 흔히 나타나는 값을 선택) */
                                                           GRIORA_Mode = 6,
       /*! 가우스 흐림(Gauss blurring) */                  GRIORA_Gauss = 7
   } GDALRIOResampleAlg;

버퍼 크기(nBufXSize x nBufYSize)가 관심 영역 크기(nXSize x nYSize)와 다를 경우 :cpp:func:`GDALRasterBand::IRasterIO` 가 이 새로운 리샘플링 메소드들을 사용할 수 있습니다. 이 리샘플링 코드는 오버뷰 계산에 사용되는 알고리즘에 크게 의존하고 있으며, 오버샘플링도 처리할 수 있도록 조정되었습니다. 이중선형, 3차 스플라인 및 란초시는 오버뷰 계산에서도 새롭게 사용할 수 있게 된 알고리즘들이며, 개선된 3차(cubic) 오버뷰를 위해 최근 도입된 회선(convolution) 계산을 위한 일반 기반 구조(infrastructure)에 의존하고 있습니다. 일부 알고리즘은 색상표를 가진 래스터 밴드에 사용할 수 없습니다. 색상표를 가진 래스터 밴드에 이를 지원하지 않는 알고리즘을 사용하는 경우 경고를 발할 것이며, 대비책으로 최근접 이웃 알고리즘을 사용할 것입니다.

리샘플링 알고리즘을 지정하는 대안 방법으로 GDAL_RASTERIO_RESAMPLING 환경설정 옵션을 설정할 수 있습니다. 이 환경설정 옵션은 주로 아직 새 API를 사용하지 않는 응용 프로그램을 테스트할 때 유용합니다.

현재, GF_Read 작업에만 이 새 리샘플링 메소드들을 사용할 수 있습니다. GF_Write 작업의 사용례는 아직 확실하지 않지만, 필요한 경우 API를 변경하지 않고서도 추가할 수 있을 것입니다.

C++ 변경 사항
~~~~~~~~~~~~~

:cpp:class:`GDALDataset` 및 :cpp:class:`GDALDataset`GDALRasterBand` 의 (가상이 아닌) RasterIO()와 (가상) IRasterIO() 메소드는 ``GDALRasterIOExtraArg*`` 유형의 새로운 마지막 인자 'psExtraArg'를 가지고 있습니다. GDAL을 사용하는 코드의 경우 이 추가 인자의 기본값은 NULL이지만, 모든 인트리(in-tree) 코드에 필수적이기 때문에 인트리 코드가 호출자로부터 반환되었을 수도 있는 'psExtraArg'를 포워딩하는 것을 잊어버리는 일을 방지합니다.


:cpp:func:`GDALDataset::RasterIO` 및 :cpp:func:`GDALRasterBand::RasterIO` 메소드는 이 인자에 대해 NULL 포인터를 받아들일 수 있습니다. 이 경우 IRasterIO()에 기본 GDALRasterIOExtraArg 구조를 전송할 수 있도록 이 메소드들이 이 구조를 인스턴스화할 것입니다. IRasterIO()를 직접 호출하는 다른 모든 코드는 (몇몇 IReadBlock() 구현들은) IRasterIO()가 자신의 'psExtraArg'가 NULL이 아니라고 가정할 수 있도록 기본 GDALRasterIOExtraArg 구조를 인스턴스화하는 것을 확인해야 합니다.

몇 기가바이트보다 더 큰 버퍼를 가진 대용량 요청을 처리할 수 있도록 하기 위해, nPixelSpace, nLineSpace 및 nBandSpace 파라미터를 정수형 데이터 유형으로부터 부호 있는 64비트 정수형의 별명인 새로운 GSpacing 데이터 유형으로 승격시켰습니다.

:cpp:func:`GDALRasterBand::IRasterIO` 및 :cpp:func:`GDALDataset::BlockBasedRasterIO` 가 이제 사용할 수 있는 경우 진행 상황 콜백을 사용합니다.

C API 변경 사항
~~~~~~~~~~~~~~~

다음 내용만 추가합니다:

::

   CPLErr CPL_DLL CPL_STDCALL GDALDatasetRasterIOEx( 
       GDALDatasetH hDS, GDALRWFlag eRWFlag,
       int nDSXOff, int nDSYOff, int nDSXSize, int nDSYSize,
       void * pBuffer, int nBXSize, int nBYSize, GDALDataType eBDataType,
       int nBandCount, int *panBandCount, 
       GSpacing nPixelSpace, GSpacing nLineSpace, GSpacing nBandSpace,
       GDALRasterIOExtraArg* psExtraArg);

   CPLErr CPL_DLL CPL_STDCALL 
   GDALRasterIOEx( GDALRasterBandH hRBand, GDALRWFlag eRWFlag,
                   int nDSXOff, int nDSYOff, int nDSXSize, int nDSYSize,
                   void * pBuffer, int nBXSize, int nBYSize,GDALDataType eBDataType,
                   GSpacing nPixelSpace, GSpacing nLineSpace,
                   GDALRasterIOExtraArg* psExtraArg );

이 메소드들은 마지막 ``GDALRasterIOExtraArg* psExtraArg`` 인자를 가진 기존 함수와 동일하며, 간격 파라미터는 GSpacing으로 승격되었습니다.

드라이버 변경 사항Changes in drivers
------------------

-  RasterIO()를 구현하거나 사용하는 모든 인트리 드라이버가 ``GDALRasterIOExtraArg* psExtraArg`` 파라미터를 받아들이고 필요한 경우 포워딩하도록 편집했습니다. 사용자 지정 RasterIO() 구현을 가졌던 드라이버는 이제 사용할 수 있는 경우 진행 상황 콜백을 사용합니다.

-  VRT:
   'and' 요소가 'resampling' 속성을 받아들일 수 있습니다. VRT 드라이버는 또한 ``GDALRasterIOExtraArg*`` 의 dfXOff, dfYOff, dfXSize 및 dfYSize 필드가 소스 하위 픽셀 정확도를 가지도록 설정하기 때문에, :cpp:func:`GDALRasterBand::IRasterIO` 가 작은 관심 영역 또는 전체 래스터에 대해 작업할 때 일관된 결과를 얻게 됩니다. 그렇지 않은 경우 GDALDatasetCopyWholeRaster() 또는 다른 알고리즘에서 덩어리 작업을 수행했을 때 정수형 반올림 문제점 때문에 줄이 반복될 수 있습니다.

유틸리티 변경 사항
------------------

-  gdal_translate:
   리샘플링 알고리즘을 지정하는 "-r" 파라미터를 받아들입니다. 기본값은 NEAR입니다. BILINEAR, CUBIC, CUBICSPLINE, LANCZOS, AVEARAGE 또는 MODE로 설정할 수 있습니다. (내부적으로 이는 VRT 수준에서 새로운 리샘플링 속성을 설정합니다.)

-  gdaladdo:
   "-r" 파라미터가 이제 기존 알고리즘들에 추가로 BILINEAR, CUBICSPLINE 및 LANCZOS를 받아들입니다.

SWIG 바인딩 변경 사항
---------------------

-  파이썬 및 펑 바인딩의 경우:
   Band.ReadRaster(), Dataset.ReadRaster()가 이제 선택적인 resample_alg, callback 및 callback_data 인자를 받아들입니다. (펄에 대해 테스트하지는 않았지만, 기존 테스트를 통과했습니다.)

-  파이썬 바인딩의 경우, Band.ReadAsArray() 및 Dataset.ReadAsArray()가 이제 선택적인 resample_alg, callback 및 callback_data 인자를 받아들입니다.

호환성
------

-  C API/ABI는 보전됩니다.

-  :cpp:func:`GDALRasterBand::RasterIO` 및 :cpp:func:`GDALDataset::RasterIO` API의 C++ 사용자가 자신의 코드를 변경할 필요는 없습니다. 새로운 ``GDALRasterIOExtraArg* psExtraArg`` 가 트리 밖에 있는 코드에 대해 선택적인 인자이기 때문입니다.

-  IRasterIO()를 구현하는, 트리 밖에 있는 드라이버가 새로운 ``GDALRasterIOExtraArg* psExtraArg`` 인자를 받아들이도록 변경해야만 합니다.
   주의: 변경에 실패하더라도 컴파일 시 탐지되지 않을 것입니다. (C++ 가상 메소드 오버로드 작업이 작동하는 방식 때문입니다.)

:file:`MIGRATION_GUIDE.TXT` 에 이 두 가지 문제점을 언급할 것입니다.

문서화
------

새로운 메소드들을 모두 문서화합니다.

테스트
------

파이썬 바인딩에서 이 RFC의 다양한 측면들을 테스트했습니다:

-  Band.ReadRaster(), Dataset.ReadRaster(), Band.ReadAsArray() 및 Dataset.ReadAsArray()의 새 옵션들의 사용에 대해
-  RasterIO() 요청을 서브샘플링 및 오버샘플링하는 리샘플링 알고리즘에 대해
-  gdal_translate "-r" 옵션에 대해

구현
----

이벤 루올이 `R3 GIS <https://www.r3gis.com/>`_ 의 후원을 받아 이 RFC를 구현할 것입니다.

제안한 구현은 `"rasterio" 브랜치 <https://github.com/rouault/gdal2/tree/rasterio>`_ 저장소에 있습니다.

`변경 사항 목록 <https://github.com/rouault/gdal2/compare/rasterio>`_

투표 이력
---------

-  프랑크 바르메르담 +1
-  유카 라흐코넨 +1
-  하워드 버틀러 +1
-  대니얼 모리셋 +1
-  세케레시 터마시 +1
-  이벤 루올 +1

