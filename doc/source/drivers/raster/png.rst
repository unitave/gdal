.. _raster.png:

================================================================================
PNG -- 포터블 네트워크 그래픽스(Portable Network Graphics)
================================================================================

.. shortname:: PNG

.. built_in_by_default:: 내부 libpng 제공

GDAL은 .png 파일의 읽기 및 생성을 지원합니다. 회색조, 의사색상, 색상표 RGB 및 RBBA PNG 파일은 물론 샘플 당 8비트 및 16비트 정밀도 PNG 파일도 지원합니다.

GDAL PNG 드라이버는 libpng 라이브러리를 이용해서 빌드되었습니다. GeoTIFF 드라이버도 PNG가 핵심적으로 사용하는 압축 알고리즘인 DEFLATE로 압축된 타일을 가진 타일화 TIFF를 지원한다는 사실을 기억하십시오.

PNG 파일은 선형적으로 압축되어 있기 때문에, 대용량 PNG 파일을 읽어오는 작업은 매우 비효율적일 수 있습니다. (파일의 시작으로부터 압축 해제를 다시 시작하는 일이 많습니다.) GDAL이 생성할 수 있는 PNG 파일의 최대 크기는 libpng가 설정하는 1,000,000x1,000,000픽셀 크기입니다.

일반적으로 텍스트 덩어리(chunk)를 항목 당 여러 줄을 가진 메타데이터로 변환합니다. .pgw, .pngw 또는 .wld 확장자를 가진 :ref:`raster.wld` 을 읽어올 것입니다. GDAL은 회색조 파일에 있는 단일 투명도 값을 NODATA 값으로 인식할 것입니다. 색상표 이미지에 있는 투명도 색인은 색상표를 읽어올 때 보전됩니다.

읽어올 원형(prototype)을 요구하는 CreateCopy() 메소드를 이용해서 PNG 파일을 PNG 유형 가운데 하나로 생성할 수 있습니다. 다양한 이미지 유형 쓰기를 지원하며, 투명도/NODATA 값을 보전할 것입니다. WORLDFILE 옵션을 설정한 경우 지리참조 용 .wld 파일을 작성합니다. 부호 없는 16비트형이 아닌 다른 모든 픽셀 유형은 8비트로 작성될 것입니다.

파일로부터 XMP 메타데이터를 추출할 수 있고, xml:XMP 메타데이터 도메인에 추출한 메타데이터를 XML 원본(raw) 내용으로 저장할 것입니다.


드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::

.. supports_georeferencing::

.. supports_virtualio::


색상 프로파일 메타데이터
----------------------

GDAL은 COLOR_PROFILE 도메인에 있는 다음과 같은 색상 프로파일 메타데이터를 처리할 수 있습니다:

-  SOURCE_ICC_PROFILE:
   파일에 내장된 Base64 인코딩 ICC 프로파일입니다. 이 태그가 존재하는 경우 다른 태그들을 무시합니다.

-  SOURCE_ICC_PROFILE_NAME:
   ICC 프로파일 이름입니다. sRGB를 특수한 값으로 인식합니다.

-  SOURCE_PRIMARIES_RED:
   "x,y,1" 서식의 적색을 우선하는 xyY입니다.

-  SOURCE_PRIMARIES_GREEN:
   "x,y,1" 서식의 녹색을 우선하는 xyY입니다.

-  SOURCE_PRIMARIES_BLUE:
   "x,y,1" 서식의 청색을 우선하는 xyY입니다.

-  SOURCE_WHITEPOINT:
   "x,y,1" 서식의 화이트 포인트(white point; 모니터에서 흰색을 가장 이상적으로 보이도록 맞춤) 용 xyY입니다.

-  PNG_GAMMA

원본 RAW 픽셀 데이터에서만 이 메타데이터 속성들을 사용할 수 있다는 사실을 기억하십시오. RGB로의 자동 변환이 이루어진 경우, 색상 프로파일 정보를 사용할 수 없습니다.

이 메타데이터 태그들을 모두 생성 옵션으로 사용할 수 있습니다.


생성 옵션
---------

-  **WORLDFILE=YES**:
   관련 ESRI 월드 파일(.wld)을 강제로 생성합니다.
   자세한 내용은 :ref:`raster.wld` 을 참조하십시오.

-  **ZLEVEL=n**:
   압축 작업에 쓸 시간을 설정합니다. 기본값은 6입니다.
   1로 설정하면 빠르지만 압축을 하지 않고, 9로 설정하면 느리지만 최고 압축을 수행합니다.

-  **TITLE=value**:
   TEXT 덩어리 또는 iTXt 덩어리에 작성되는 제목입니다.

-  **DESCRIPTION=value**:
   TEXT 덩어리 또는 iTXt 덩어리에 작성되는 설명입니다.

-  **COPYRIGHT=value**:
   TEXT 덩어리 또는 iTXt 덩어리에 작성되는 저작권입니다.

-  **COMMENT=value**:
   TEXT 덩어리 또는 iTXt 덩어리에 작성되는 주석입니다.

-  **WRITE_METADATA_AS_TEXT=YES/NO**:
   TEXT 덩어리에 소스 데이터셋의 메타데이터를 작성할지 여부를 선택합니다.

-  **NBITS=1/2/4**: (GDAL 2.1 이상 버전)
   산출물의 비트 수를 강제로 설정합니다.


참고
----

-  ``gdal/frmts/png/pngdataset.cpp`` 로 구현되었습니다.

-  libpng 참조 라이브러리를 기반으로 PNG 지원을 구현했습니다. http://www.libpng.org/pub/png 에서 자세한 정보를 찾아볼 수 있습니다.
