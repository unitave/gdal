.. _raster.rasterlite2:

================================================================================
RasterLite2 - SQLite 데이터베이스 래스터
================================================================================

.. versionadded:: 2.2

.. shortname:: SQLite

.. note:: 앞의 단축명은 오타가 아닙니다.
          RasterLite2의 기능은 :ref:`vector.sqlite` 드라이버의 일부분입니다.

.. build_dependencies:: libsqlite3, librasterlite2, libspatialite

SQLite 드라이버는 RasterLite2 커버리지를 담고 있는 SQLite 데이터베이스를 읽고 쓸 수 있습니다.

-  rl2tools 같은 `RasterLite2 <https://www.gaia-gis.it/fossil/librasterlite2>`_ 유틸리티를 사용하면 이런 데이터베이스를 생성할 수 있습니다.

-  이 드라이버는 libRasterLite2가 지원하는 여러 압축 포맷으로 타일을 저장하는 회색조, 색상표, RGB, 다중 스펙트럼 이미지의 읽기를 지원합니다. 오버뷰/피라미드, 공간 좌표계 및 공간 범위도 읽어올 수 있습니다.

GDAL/OGR를 librasterlite2 및 libspatialite 라이브러리를 대상으로 OGR SQLite 드라이버 지원과 함께 컴파일해야만 합니다.

이 드라이버는 SQLite/SpatiaLite/ RasterLite2 벡터 및 래스터 통합 호환 드라이버로 구현되었습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::

.. supports_georeferencing::

.. supports_virtualio::

열기 문법
--------------

RasterLite2 파일명을 연결 문자열로 지정할 수 있습니다. 파일이 단일 RasterLite2 커버리지를 담고 있는 경우, 이 커버리지를 GDAL 데이터셋으로 노출시킬 것입니다. 파일이 커버리지 여러 개를 담고 있다면 RASTERLITE2:filename:coverage_name이라는 문법으로 각 커버리지를 하위 데이터셋으로 노출시킬 것입니다. `RasterLite2 기본 개념 <https://www.gaia-gis.it/fossil/librasterlite2/wiki?name=basic_concepts>`_ 을 참조하십시오.

커버리지가 여러 부분(section)들로 이루어져 있다면, 개별적으로 접근할 수 있도록 이 부분들을 커버리지 데이터셋의 하위 데이터셋으로 목록화할 것입니다. 기본적으로 이 부분들은 통합 데이터셋으로 노출될 것입니다. 부분-기반 데이터셋의 문법은 RASTERLITE2:filename:coverage_name:section_id:section_name입니다.

생성
--------

이 드라이버는 새 데이터베이스를 처음부터 생성하고, 기본 데이터베이스에 새 커버리지를 추가하며, 기존 커버리지에 부분들을 추가할 수 있습니다.

생성 옵션
----------------

-  **APPEND_SUBDATASET=YES/NO**:
   기존 파일에 래스터를 추가할지 여부를 선택합니다. YES로 설정하는 경우, COVERAGE 옵션도 지정해야만 합니다. 기본값은 NO입니다. (즉 기존 파일을 덮어씁니다.)

-  **COVERAGE=string**:
   커버리지 이름을 설정합니다. 지정하지 않는 경우, 산출 파일의 기본명(basename)을 사용합니다.

-  **SECTION=string**:
   부분(section) 이름을 설정합니다. 지정하지 않는 경우, 산출 파일의 기본명(basename)을 사용합니다.

-  **COMPRESS=NONE/DEFLATE/LZMA/PNG/CCITTFAX4/JPEG/WEBP/CHARS/JPEG2000**:
   압축 메소드를 설정합니다. 기본값은 NONE입니다. `지원 코덱 정보 <https://www.gaia-gis.it/fossil/librasterlite2/wiki?name=codecs>`_ 를 참조하십시오.
   librasterlite2를 어떻게 빌드했느냐에 따라 일부 코덱들을 사용할 수 없을 수도 있다는 사실을 기억하십시오.

-  **QUALITY=0 to 100**:
   JPEG, WEBP 및 JPEG2000 압축을 사용하는 경우 이미지 품질을 설정합니다. 압축 메소드에 따라 설정값의 의미가 달라집니다. WEBP 및 JPEG2000의 경우, 100으로 설정하면 비손실 압축을 사용할 것입니다.

-  **PIXEL_TYPE=MONOCHROME/PALETTE/GRAYSCALE/RGB/MULTIBAND/DATAGRID**:
   래스터 픽셀 유형을 설정합니다. 측광 해석을 결정합니다. `지원 픽셀 유형 정보 <https://www.gaia-gis.it/fossil/librasterlite2/wiki?name=reference_table>`_ 를 참조하십시오.
   이 드라이버는 입력 밴드 특성에 따라 알맞은 픽셀 유형을 자동적으로 결정할 것입니다.

-  **BLOCKXSIZE=int_value**:
   블록 너비를 설정합니다. 기본값은 512입니다.

-  **BLOCKYSIZE=int_value**:
   블록 높이를 설정합니다. 기본값은 512입니다.

-  **NBITS=1/2/4**:
   비트 길이를 강제로 설정합니다. 기본적으로는 소스 래스터 밴드의 IMAGE_STRUCTURE 메타데이터 도메인에 있는 NBITS 메타데이터 항목으로부터 비트 길이를 가져올 것입니다.

-  **PYRAMIDIZE=YES/NO**:
   관련 피라미드/오버뷰를 자동 작성할지 여부를 선택합니다. 기본값은 NO입니다.
   BuildOverviews() / gdaladdo 메소드로 피라미드를 작성할 수 있습니다.

예시
--------

-  단일 커버리지를 가지고 있는 RasterLite2 데이터베이스를 읽어오기:

   ::

      gdalinfo my.rl2

-  커버리지 여러 개를 가지고 있는 RasterLite2 데이터베이스의 커버리지에 대응하는 하위 데이터셋을 목록화하기:

   ::

      gdalinfo multiple_coverages.rl2

-  커버리지 하나에 대응하는 하위 데이터셋 하나를 읽어오기:

   ::

      gdalinfo RASTERLITE2:multiple_coverages.rl2:my_coverage

-  회색조 이미지로부터 RasterLite2 데이터셋을 생성하기:

   ::

      gdal_translate -f SQLite byte.tif byte.rl2

-  JPEG 압축을 사용해서 RGB 이미지로부터 RasterLite2 데이터셋을 생성하기:

   ::

      gdal_translate -f SQLite rgb.tif rgb.rl2 -co COMPRESS=JPEG

-  기존 SpatiaLite/RasterLite2 데이터베이스에 RasterLite2 커버리지를 추가하기:

   ::

      gdal_translate -f SQLite rgb.tif rgb.rl2 -co APPEND_SUBDATASET=YES -co COVERAGE=rgb

-  커버리지에 피라미드를 추가하기:

   ::

      gdaladdo rgb.rl2 2 4 8 16

참고
--------

-  `Rasterlite2 홈페이지 <https://www.gaia-gis.it/fossil/librasterlite2/index>`_

-  :ref:`OGR SQLite <vector.sqlite>` 드라이버

