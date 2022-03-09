.. _raster.cog:

================================================================================
COG -- 클라우드 최적화 GeoTIFF 생성기
================================================================================

.. versionadded:: 3.1

.. shortname:: COG

.. built_in_by_default::

이 드라이버는 COG(Cloud Optimized GeoTIFF)를 생성할 수 있습니다.

이 드라이버는 본질적으로 ``COPY_SRC_OVERVIEWS=YES`` 생성 옵션을 가진 :ref:`raster.gtiff` 드라이버에 의존하지만, 필요한 사전 처리 (요청이 있는 경우 재투영, 이미지 그리고/또는 마스크의 오버뷰 생성) 단계를 수행하지 않은 경우 자동으로 수행하고, 몇몇 압축 유형을 사용하는 경우 입력 데이터셋을 예상 형태로 변형(morph)하는 작업을 처리하기도 합니다. (예를 들어 JPEG 압축을 선택했다면 RGBA 데이터셋을 알기 쉽게 RGB+마스크 데이터셋으로 변환할 것입니다.)

드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::

.. supports_georeferencing::

.. supports_virtualio::

생성 옵션
----------------

일반 생성 옵션
************************

-  **BLOCKSIZE=n**: 타일 너비와 높이를 픽셀 단위로 설정합니다. 기본값은 512입니다.

-  **COMPRESS=[NONE/LZW/JPEG/DEFLATE/ZSTD/WEBP/LERC/LERC_DEFLATE/LERC_ZSTD/LZMA]**: 사용할 압축 방법을 설정합니다.
   GDAL 3.4버전부터 기본값은 ``LZW`` 입니다. (이전 버전까지 기본값은 ``NONE`` 이었습니다.)

   * ``JPEG`` 은 일반적으로 (채널 당 8비트인) 바이트 유형 데이터에만 사용해야 합니다. 하지만 GDAL이 내부 libtiff와 libjpeg으로 빌드된 경우, TIFF 파일을 (NBITS 값이 12인 UInt16 데이터 유형 밴드로 보이는) 12비트 JPEG 압축 TIFF로 읽고 쓸 수 있습니다. 더 자세한 내용은 `"TIFF에서 8비트 및 12비트 JPEG" <http://trac.osgeo.org/gdal/wiki/TIFF12BitJPEG>`_ 위키 페이지를 참조하십시오. COG 드라이버의 경우, 밴드 3개 또는 4개 이미지를 위한 JPEG 압축은 자동적으로 Y, Cb, Cr 구성 요소를 4:2:2로 서브샘플링한 PHOTOMETRIC=YCBCR 색 공간(color space)을 선택합니다.

   * ``LZW``, ``DEFLATE`` and ``ZSTD`` 압축은 PREDICTOR 생성 옵션과 함께 사용할 수 있습니다.

   * ``ZSTD`` 는 내부 libtiff를 사용하며 GDAL이 libzstd 1.0 이상 버전을 대상으로 빌드된 경우 또는 zstd를 지원하는 외부 libtiff를 대상으로 빌드된 경우 사용할 수 있습니다.

   * ``LERC`` 는 내부 libtiff를 사용하는 경우 사용할 수 있습니다.

   * ``LERC_ZSTD`` 는 ``LERC`` 과 ``ZSTD`` 를 사용할 수 있는 경우 사용할 수 있습니다.

-  **LEVEL=integer_value**: DEFLATE/ZSTD/LERC_DEFLATE/LERC_ZSTD/LZMA 압축 수준입니다. 숫자가 낮을수록 압축 속도는 빨라지지만 압축 효율은 떨어집니다. 1로 설정하면 속도가 가장 빠릅니다.

   * DEFLATE/LZMA의 경우, 9로 (또는 libdeflate를 지원하는 libtiff를 사용하는 경우 12로) 설정하면 속도는 가장 느리지만 압축률은 가장 높습니다. 기본값은 6입니다.
   * ZSTD의 경우, 22로 설정하면 속도는 가장 느리지만 압축률은 가장 높습니다. 기본값은 9입니다.

-  **MAX_Z_ERROR=threshold**: LERC/LERC_DEFLATE/LERC_ZSTD 압축에 대한 최대 오류 한계값을 설정합니다. 기본값은 0(비손실)입니다.

-  **QUALITY=integer_value**: JPEG/WEBP 품질을 설정합니다. 값이 100이면 최고 품질(최저 압축), 1이면 최저 품질(최고 압축)입니다. 기본값은 75입니다. WEBP의 경우, QUALITY=100으로 설정하면 자동적으로 비손실 모드를 활성화합니다.

-  **NUM_THREADS=number_of_threads/ALL_CPUS**: 작업자 스레드의 개수를 지정해서 멀티스레딩 압축을 활성화합니다. 기본값은 주 스레드에서 압축하는 것입니다. 이 옵션은 TILING_SCHEME 또는 TARGET_SRS 생성 옵션으로 재투영하는 경우 사용하는 스레드 개수도 결정합니다. (GDAL 3.2버전부터 오버뷰 생성도 멀티스레딩을 지원합니다.)

-  **PREDICTOR=[YES/NO/STANDARD/FLOATING_POINT]**: LZW, DEFLATE 및 ZSTD를 위한 예측 변수(predictor)를 설정합니다. 기본값은 NO입니다. YES를 지정하는 경우, 정수 데이터 유형에 표준 예측 변수(Predictor=2)를 사용하고 부동소수점 데이터 유형에는 부동소수점 예측 변수(Predictor=3)를 사용합니다. (부동소수점형 데이터에 대해 부동소수점 예측 변수보다 표준 예측 변수가 더 나은 성능을 보이는 경우도 있을 수 있습니다.) 원하는 알고리즘을 정확하게 선택하려면 STANDARD 또는 FLOATING_POINT로 지정해도 됩니다.

-  **BIGTIFF=YES/NO/IF_NEEDED/IF_SAFER**: 파일을 BigTIFF로 생성할지 또는 전형적인 TIFF로 생성할지 제어합니다.

   -  ``YES`` 는 강제로 BigTIFF를 생성합니다.
   -  ``NO`` 는 강제로 전형적인 TIFF를 생성합니다.
   -  ``IF_NEEDED`` 는 분명히 필요한 경우에만 BigTIFF를 생성할 것입니다. (압축하지 않고, 이미지 용량이 4GB를 초과하는 경우. 따라서 이런 경우에는 압축 방법을 지정해도 영향을 미치지 않습니다.)
   -  ``IF_SAFER`` 는 생성되는 파일이 4GB를 *초과할 수도 있는* 경우 BigTIFF를 생성할 것입니다. 주의: 압축률에 따라 동작하지 않을 수도 있는 휴리스틱(heuristic) 옵션입니다.

   BigTIFF란 4GB를 초과하는 데이터를 담을 수 있는 TIFF의 변이형입니다. (전형적인 TIFF의 용량은 4GB를 넘을 수 없도록 제한되어 있습니다.) GDAL이 libtiff 라이브러리 4.0 이상 버전과 함께 빌드된 경우 이 옵션을 사용할 수 있습니다. 기본값은 IF_NEEDED입니다.

   새 GeoTIFF를 압축하지 않고 생성하는 경우, GDAL은 생성될 파일의 용량을 사전에 계산합니다. 이렇게 계산한 파일 용량이 4GB를 초과하면 GDAL은 BigTIFF 파일을 생성하도록 자동으로 결정할 것입니다. 하지만 압축을 사용하는 경우, 파일의 최종 용량을 사전에 알 수는 없기 때문에 전형적인 TIFF를 선택할 것입니다. 이런 경우에 최종 파일이 전형적인 TIFF 파일이 감당하기에는 너무 커질 거라고 예측된다면, 사용자가 BIGTIFF=YES 옵션으로 BigTIFF 생성을 명확하게 요구해야만 합니다. BigTIFF 생성을 명확하게 요구하지 않거나 추정하지 못 했는데 생성된 파일이 전형적인 TIFF 파일이 감당하기에는 너무 큰 경우, libtiff가 "TIFFAppendToStrip:Maximum TIFF file size exceeded" 같은 오류 메시지와 함께 정지할 것입니다.

-  **RESAMPLING=[NEAREST/AVERAGE/BILINEAR/CUBIC/CUBICSPLINE/LANCZOS]**: 
   오버뷰 생성 또는 재투영에 쓰이는 리샘플링 메소드를 선택합니다.
   기본적으로 색상표 이미지의 경우 NEAREST를 사용하고, 다른 경우에는 CUBIC을 사용합니다.

-  **OVERVIEW_RESAMPLING=[NEAREST/AVERAGE/BILINEAR/CUBIC/CUBICSPLINE/LANCZOS]**:
   (GDAL 3.2버전부터) 오버뷰 생성에 쓰이는 리샘플링 메소드를 선택합니다.
   기본적으로 색상표 이미지의 경우 NEAREST를 사용하고, 다른 경우에는 CUBIC을 사용합니다.
   오버뷰 생성 시 ``RESAMPLING`` 을 설정했다면 이 옵션이 그 값을 무시합니다.

-  **WARP_RESAMPLING=[NEAREST/AVERAGE/BILINEAR/CUBIC/CUBICSPLINE/LANCZOS]**:
   (GDAL 3.2버전부터) 오버뷰 재투영에 쓰이는 리샘플링 메소드를 선택합니다.
   기본적으로 색상표 이미지의 경우 NEAREST를 사용하고, 다른 경우에는 CUBIC을 사용합니다.
   오버뷰 재투영 시 ``RESAMPLING`` 을 설정했다면 이 옵션이 그 값을 무시합니다.

- **OVERVIEWS=[AUTO/IGNORE_EXISTING/FORCE_USE_EXISTING/NONE]**:
   오버뷰 생성 및 소스 오버뷰 사용에 대한 습성을 설명합니다.

  - ``AUTO`` (기본값): 소스 오버뷰가 존재하는 경우 (최소 수준의 크기가 512픽셀 미만이 아니라고 하더라도) 사용할 것입니다. 존재하지 않는 경우, 산출 파일에 오버뷰를 자동으로 생성할 것입니다.

  - ``IGNORE_EXISTING``: 소스 데이터셋에 존재할 수도 있는 기존 오버뷰를 무시하고 새 오버뷰를 자동으로 생성할 것입니다.

  - ``FORCE_USE_EXISTING``: 소스 데이터셋에 존재할 수도 있는 기존 오버뷰를 (최소 수준의 크기가 512픽셀 미만이 아니라고 하더라도) 사용할 것입니다. 소스 오버뷰가 없다면, ``NONE`` 을 지정하는 것과 동일합니다.

  - ``NONE``: 존재할 수도 있는 소스 오버뷰를 무시하고 어떤 오버뷰도 생성하지 않을 것입니다.

    .. note::

        gdal_translate 유틸리티 사용 시 일반 옵션을 (예를 들어 하위 집합 생성 작업 등 생성 옵션이 아닌 옵션을) 사용한다면 소스 오버뷰를 사용할 수 없을 것입니다.

- **OVERVIEW_COMPRESS=[AUTO/NONE/LZW/JPEG/DEFLATE/ZSTD/WEBP/LERC/LERC_DEFLATE/LERC_ZSTD/LZMA]**:
  COG에 오버뷰를 저장하는 경우 사용할 압축 메소드를 설정합니다. (``COMPRESS`` 참조)

  기본적으로 (``AUTO``) 오버뷰를 COG와 동일한 압축 메소드로 생성할 것입니다.

- **OVERVIEW_QUALITY=integer_value**: JPEG/WEBP 품질을 설정합니다. 값이 100이면 최고 품질(최저 압축), 1이면 최저 품질(최고 압축)입니다. 오버뷰의 압축 유형을 COG와 다르게 지정한 경우가 아니라면 기본적으로 오버뷰를 COG와 동일한 품질로 생성할 것입니다. 다르게 지정했다면 기본값은 75입니다.

- **OVERVIEW_PREDICTOR=[YES/NO/STANDARD/FLOATING_POINT]**: LZW, DEFLATE 및 ZSTD 오버뷰 압축을 위한 예측 변수(predictor)를 설정합니다. 오버뷰의 압축 유형을 COG와 다르게 지정한 경우가 아니라면 기본적으로 오버뷰를 COG와 동일한 예측 변수로 생성할 것입니다. 다르게 지정했다면 기본값은 NO입니다.

- **GEOTIFF_VERSION=[AUTO/1.0/1.1]**:
  지리참조 정보를 인코딩하기 위해 쓰이는 GeoTIFF 표준의 버전을 선택합니다.
  ``1.0`` 은 원조 `1995, GeoTIFF Revision 1.0, by Ritter & Ruth <http://geotiff.maptools.org/spec/geotiffhome.html>`_ 입니다.
  ``1.1`` 은 OGC 표준 19-008로, 1.0의 애매했던 표현을 고치고 대부분 좌표계의 수직 부분의 처리 과정에 있던 모순들을 수정한 진화형입니다.
  ``AUTO`` 모드(기본값)는 인코딩할 좌표계가 수직 구성요소를 가지고 있거나 3차원 좌표계가 아니라면 일반적으로 1.0을 선택할 것입니다. 수직 구성요소를 가지고 있거나 3차원 좌표계인 경우 1.1을 선택합니다.

  .. note::

    GeoTIFF 1.1의 경우 쓰기를 지원하려면 libgeotiff 1.6.0 이상 버전이 필요합니다.

- **SPARSE_OK=TRUE/FALSE** (GDAL 3.2 이상): 
  디스크에서 비어 있는 블록을 생략해야 할지 여부를 선택합니다.
  이 옵션을 설정한 경우, (파일 안에 대응하는 블록이 이미 할당되어 있는 경우가 아니라면) 모든 픽셀이 0 또는 NODATA 값인 어떤 블록도 작성되지 못 할 것입니다. 희소(sparse) 파일은 작성되지 않는 블록을 위한 타일/스트립 오프셋을 하나도 가지고 있지 않아 디스크 공간을 절약합니다. 하지만, GDAL이 아닌 대부분의 패키지는 이런 파일을 읽어오지 못 합니다.
  읽기라는 관점에서 보면, 비어 있지 않은 타일 뒤에 생략된 타일이 존재하는 경우 최적화된 판독기가 TileByteCounts 배열에 GET 요청을 추가로 전송해야 할 수도 있습니다.
  기본값은 FALSE입니다.

재투영 관련 생성 옵션
*************************************

- **TILING_SCHEME=CUSTOM/GoogleMapsCompatible/other**:
  기본값은 CUSTOM입니다. CUSTOM이 아닌 다른 값으로 설정하는 경우, 지정한 타일 작업 스키마를 사용해서 데이터셋을 스키마 좌표계로 재투영하고, 스키마의 확대/축소 수준에 가장 가까운 해상도를 선택한 다음, 해당 해상도의 타일 경계에 정렬할 것입니다. 사용자가 BLOCKSIZE 생성 옵션으로 값을 지정한 경우가 아니라면 타일 작업 스키마 정의에 있는 타일 크기를 (일반적으로 256픽셀) 설정할 것입니다. 사용자가 지정한 경우에는 사용자 지정 값을 사용할 것입니다. (이때 사용자가 256을 초과하는 값을 지정했다면 HiDPI 타일 크기를 연산에 넣도록 원본 타일 작업 스키마를 수정합니다.) CUSTOM이 아닌 모드에서는 TARGET_SRS, RES 및 EXTENT 옵션을 무시합니다. GDAL 3.2버전부터 TILING_SCHEME의 값이 `OGC 2차원 타일 행렬 집합 표준`_ 을 따르는 JSON 파일의 파일명, 해당 파일을 가리키는 URL, GDAL data 디렉터리에 있는 정의 파일의 어근(語根, 예: ``tms_FOO.json`` 라는 파일명의 경우 ``FOO``) 또는 그때그때 즉시 처리되는(inline) JSON 정의가 될 수도 있습니다.

.. _`OGC 2차원 타일 행렬 집합 표준`: http://docs.opengeospatial.org/is/17-083r2/17-083r2.html

- **ZOOM_LEVEL_STRATEGY=AUTO/LOWER/UPPER** (GDAL 3.2 이상): 확대/축소 수준을 결정할 전략을 선택합니다. TILING_SCHEME이 CUSTOM이 아닌 경우에만 사용합니다. LOWER는 내장되지 않은, 이론적으로 계산된 확대/축소 수준 바로 아래의 확대/축소 수준을 선택하고 서브샘플링 작업을 수행할 것입니다. UPPER는 그 반대로 바로 위의 확대/축소 수준을 선택하고 오버샘플링 작업을 수행할 것입니다. 기본값은 가장 가까운 확대/축소 수준을 선택하는 AUTO입니다.

- **TARGET_SRS=string**: 입력 데이터셋을 또다른 공간 좌표계로 강제로 재투영합니다. WKT 문자열, EPSG:XXXX 코드 또는 PROJ 문자열을 지정할 수 있습니다.

- **RES=value**: 대상 래스터의 해상도를 TARGET_SRS 단위로 설정합니다. TARGET_SRS를 지정한 경우에만 연산에 넣습니다.

- **EXTENT=minx,miny,maxx,maxy**: 대상 래스터의 범위를 TARGET_SRS 단위로 설정합니다. TARGET_SRS를 지정한 경우에만 연산에 넣습니다.

- **ALIGNED_LEVELS=INT**: GeoTIFF 타일과 타일 작업 스키마에 정의된 타일들이 서로 일치하는 해상도 수준의 개수입니다. 이 옵션을 지정하면, 필요한 경우 GeoTIFF 타일과 타일 작업 스키마의 타일이 서로 일치하도록 대상 래스터의 좌측과 상단에 완충(padding) 타일을 추가할 것입니다. TILING_SCHEME이 CUSTOM이 아닌 경우에만 연산에 넣습니다. 값을 2 이상으로 설정하는 경우에만 이 옵션의 효과를 볼 수 있습니다. 전체 해상도 수준은 기본적으로 타일 작업 스키마에 정렬되기 때문입니다. 연속되는 확대/축소 수준 해상도가 2의 배수로 달라지는 타일 작업 스키마의 경우, 각 수준에 타일 2^(ALIGNED_LEVELS-1)개까지 추가될 수도 있기 때문에 이 수준 개수 값을 큰 값으로 설정하지 않도록 주의해야 합니다. 이 드라이버는 10을 초과하지 않도록 엄격히 제한하고 있습니다.

- **ADD_ALPHA=YES/NO**: 재투영하는 경우 알파 밴드를 추가할지 여부를 선택합니다. 기본값은 YES입니다.


파일 포맷 상세 정보
-------------------

고급
**********

클라우드 최적화 GeoTIFF는 다음과 같은 특성을 가지고 있습니다:

- TIFF 또는 BigTIFF 파일
- 영상, 마스크 및 오버뷰를 타일화 (기본 크기 512픽셀)
- 최소 오버뷰 수준의 최대 크기가 512픽셀 미만이 될 때까지 오버뷰 생성
- 압축 또는 비압축
- 다중 밴드 데이터셋의 경우 픽셀 교차 삽입(interleaving)
- 판독기가 임의로 읽기 접근 시 필요한 GET 요청의 수를 최소화하기 위해 TIFF 부분(section)들의 레이아웃 최적화

일반
*********

COG 파일은 다음과 같이 조직되어 있습니다. (libtiff 4.0.11 이상 버전 또는 GDAL 내부 libtiff를 사용하는 경우입니다. 다른 버전을 사용한다면, 레이아웃이 달라질 것이며 몇몇 최적화도 사용할 수 없게 됩니다.)

- TIFF/BigTIFF 헤더/서명 및 첫 번째 IFD(Image File Directory)를 가리키는 포인터
- COG 최적화를 거친 "고스트 영역(ghost area)" (`헤더 고스트 영역`_ 참조)
- 전체 해상도 이미지의 IFD, 그 뒤에 오는 TileOffsets 및 TileByteCounts 배열을 제외한 TIFF 태그 값들
- 전체 해상도 이미지의 마스크가 존재하는 경우 해당 마스크의 IFD, 그 뒤에 오는 TileOffsets 및 TileByteCounts 배열을 제외한 TIFF 태그 값들
- 첫 번째 (가장 큰 크기의) 오버뷰 수준이 있는 경우 해당 IFD
- ...
- 마지막 (가장 작은 크기의) 오버뷰 수준이 있는 경우 해당 IFD
- 마스크의 첫 번째 (가장 큰 크기의) 오버뷰 수준이 있는 경우 해당 IFD
- ...
- 마스크의 마지막 (가장 작은 크기의) 오버뷰 수준이 있는 경우 해당 IFD
- 이 IFD들의 TileOffsets 및 TileByteCounts 배열들
- 가장 작은 오버뷰가 있는 경우 해당 오버뷰의 :ref:`리더 및 트레일러 바이트 <cog.tile_data_leader_trailer>` 를 가진 타일 데이터(오버뷰의 각 타일에 대응하는 마스크 데이터의 타일이 있는 경우 오버뷰의 각 타일 뒤에 마스크 데이터의 타일이 옵니다)
- ...
- 가장 큰 오버뷰가 있는 경우 해당 오버뷰의 타일 데이터 (마스크 데이터가 있는 경우 해당 데이터와 교차 삽입)
- 전체 해상도 이미지가 있는 경우 해당 이미지의 타일 데이터 (대응하는 마스크 데이터가 있는 경우 해당 데이터와 교차 삽입)

헤더 고스트 영역
*****************

COG 파일의 특정 레이아웃을 설명하기 위해, 파일 시작 부분에 사용하는 객체에 대한 설명이 있습니다. 즉 (GDAL 같은) 최적화된 판독기가 이 설명을 이용해서 지름길을 택할 수 있도록 말입니다. 전형적인 GeoTIFF의 첫 8바이트 (또는 BigTIFF의 경우 첫 16바이트) 바로 뒤에 이런 객체들의 ASCII 문자열 설명이 "숨겨져" 있습니다. 이런 문자열들 바로 뒤에 첫 번째 IFD가 시작됩니다. TIFF 파일 안에 이런 *고스트 영역* 이 있는 것은 완전히 유효합니다. 판독기는 일반적으로 이런 영역을 건너뛸 것입니다. 투명도 마스크를 가진 COG 파일의 경우, 이런 문자열들은 다음과 비슷할 것입니다:

::

    GDAL_STRUCTURAL_METADATA_SIZE=000174 bytes
    LAYOUT=IFDS_BEFORE_DATA
    BLOCK_ORDER=ROW_MAJOR
    BLOCK_LEADER=SIZE_AS_UINT4
    BLOCK_TRAILER=LAST_4_BYTES_REPEATED
    KNOWN_INCOMPATIBLE_EDITION=NO
    MASK_INTERLEAVED_WITH_IMAGERY=YES

.. note::

    - 이 문자열들을 구분하기 위해 줄바꿈 문자 `\\n` 을 사용합니다.
    - `KNOWN_INCOMPATIBLE_EDITION=NO`의 줄바꿈 뒤에 공백 문자가 삽입되었습니다.
    - 마스크가 없는 COG의 경우, 당연히 `MASK_INTERLEAVED_WITH_IMAGERY` 항목이 존재하지 않을 것입니다.

고스트 영역은 (43바이트라는 고정 크기의) ``GDAL_STRUCTURAL_METADATA_SIZE=XXXXXX bytes\n`` 로 시작합니다. 이때 XXXXXX는 이 부분의 나머지 크기를 나타내는 여섯 자리 숫자입니다. (즉 이 시작 줄의 줄바꿈 문자 뒤로부터 시작하는 크기입니다.)

- ``LAYOUT=IFDS_BEFORE_DATA``: IFD들이 파일 시작 부분에 있습니다. GDAL은 16KB 크기의 첫 번째 범위 요청이 항상 모든 IFD를 가져올 수 있도록 타일 색인 배열도 IFD 바로 뒤, 영상 앞에 작성되었는지 확인할 것입니다.

- ``BLOCK_ORDER=ROW_MAJOR``: (strile은 'strip or tile'의 줄임말입니다) 타일의 데이터를 타일 ID 오름차순으로 작성합니다. 향후 개발을 통해 다른 레이아웃을 구현할 수도 있습니다.

- ``BLOCK_LEADER=SIZE_AS_UINT4``: 각 *고스트 영역* 은 물론 각 타일 데이터 앞에 실제 타일 크기를 (리틀 엔디언 순서로) 나타내는 4바이트를 삽입합니다. 자세한 내용은 :ref:`타일 데이터 리더 및 트레일러 <cog.tile_data_leader_trailer>` 를 읽어보십시오.

- ``BLOCK_TRAILER=LAST_4_BYTES_REPEATED``: 타일 데이터 바로 뒤에 타일 데이터의 마지막 4바이트를 반복합니다. 자세한 내용은 :ref:`타일 데이터 리더 및 트레일러 <cog.tile_data_leader_trailer>` 를 읽어보십시오.

- ``KNOWN_INCOMPATIBLE_EDITION=NO``: COG 생성 시 항상 이 문자열을 작성합니다. 생성 이후 GDAL을 사용해서 COG 파일을 수정하는 경우, 기존 COG 파일에 대부분의 변경 사항을 적용하기 때문에 최적화된 구조를 무너뜨릴 것입니다. 이때 사용자가 수정 작업 때문에 COG 파일의 구조를 무너뜨렸다는 사실을 알리기 위해 GDAL은 이 메타데이터 항목을 KNOWN_INCOMPATIBLE_EDITION=YES로 변경하고 변경 사항을 작성할 때, 그리고 이런 파일을 다시 열 때도 경고할 것입니다.

- ``MASK_INTERLEAVED_WITH_IMAGERY=YES``: 영상 데이터 바로 뒤에 마스크 데이터가 있다는 사실을 나타냅니다. 따라서 offset=TileOffset[i] - 4 및 size=TileOffset[i+1]-TileOffset[i]+4 옵션으로 파일을 여는 경우, 다음과 같은 내용을 가진 버퍼를 가져오게 될 것입니다:

   * 영상 타일 크기를 가진 리더 (4바이트)
   * (TileOffsets[i]에서 시작하고 TileByteCounts[i] 크기를 가진) 영상 데이터
   * 영상의 트레일러 (4바이트)
   * 마스크 타일 크기를 가진 리더 (4바이트)
   * (mask.TileOffsets[i]에서 시작하고 mask.TileByteCounts[i] 크기를 가졌지만 둘 다 실제로 읽어올 필요는 없는) 마스크 데이터
   * 마스크 데이터의 트레일러 (4바이트)

.. note::

    데이터셋 객체에 있는 ``TIFF`` 메타데이터 도메인의 ``GDAL_STRUCTURAL_METADATA`` 메타데이터 항목을 (GetMetadataItem()으로) 가져오면 헤더 고스트 영역의 내용을 가져올 수 있습니다.

.. _cog.tile_data_leader_trailer:

타일 데이터 리더 및 트레일러
****************************

각 타일 데이터 바로 앞에 리더(leader)가 있습니다. 이 리더는 리틀 엔디언 순서로 된 부호 없는 4바이트 정수형으로 이루어져 있는데, 뒤에 오는 타일 데이터의 *부하(payload)* 의 바이트 개수를 알려줍니다. TileOffsets[] 배열이 리더가 아니라 실제 부하를 가리킨다는 의미에서 이 리더는 *고스트* 입니다. 따라서 리더의 오프셋은 TileOffsets[i]-4가 됩니다.

즉 ``BLOCK_LEADER=SIZE_AS_UINT4`` 메타데이터 항목을 보는 최적화된 판독기는 리더의 위치를 추정하기 위해 TileOffset[i]와 TileOffset[i+1]을 검색해서 offset=TileOffset[i]-4 위치에서 시작하고 size=TileOffset[i+1]-TileOffset[i]+4 크기인 데이터를 가져와야만 합니다. 그 다음 첫 4바이트를 확인해서 이 리더 마커의 크기값이 TileOffset[i+1]-TileOffset[i]와 일치하는지 검증합니다. 마스크가 없는 경우, 일반적으로 일치해야 합니다. (BLOCK_LEADER와 BLOCK_TRAILER로 계산한 크기를 기준으로 삼습니다.) 마스크가 존재하고 MASK_INTERLEAVED_WITH_IMAGERY=YES인 경우, 리더가 알려주는 타일 크기는 TileOffset[i+1]-TileOffset[i] 미만일 것입니다. 영상 데이터 뒤에 마스크 데이터가 올 것이기 때문입니다. (MASK_INTERLEAVED_WITH_IMAGERY=YES 참조)

각 타일 데이터 바로 뒤에는 해당 타일 데이터의 부하의 마지막 4바이트를 반복하는 트레일러(trailer)가 있습니다. 이 트레일러의 크기는 TileByteCounts[] 배열에 포함되지 *않습니다*. 이 트레일러의 목적은 이런 최적화에 대해 알지 못 하는 TIFF 작성자가 최적화를 무너뜨리는 방향으로 TIFF 파일을 수정했는지 판독기가 검증할 수 있도록 강제하는 것입니다. 최적화된 판독기가 불일치를 탐지한 경우, TileOffsets[i] + TileByteCounts[i]를 사용하는 더 느린 정규 메소드로 일보후퇴할 수 있습니다.

예시
--------

::

    gdalwarp src1.tif src2.tif out.tif -of COG

::

    gdal_translate world.tif world_webmerc_cog.tif -of COG -co TILING_SCHEME=GoogleMapsCompatible -co COMPRESS=JPEG

참고
--------

- :ref:`raster.gtiff` 드라이버
- `클라우드 최적화 GeoTIFF 파일 생성 및 읽기 방법 <https://trac.osgeo.org/gdal/wiki/CloudOptimizedGeoTIFF>`_ (GDAL 3.1 이전 버전)
- 사용자의 소스 데이터셋이 사용자가 원하는 지리참조와 압축 방법을 적용한, 내부적으로 타일화된 GeoTIFF인 경우, (오버뷰를 생성하려면 gdaladdo와 함께 사용할 수도 있는) `cogger <https://github.com/airbusgeo/cogger>`_ 를 사용하는 편이 COG 드라이버를 사용하는 것보다 훨씬 빠를 것입니다.

