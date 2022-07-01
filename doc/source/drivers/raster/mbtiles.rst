.. _raster.mbtiles:

================================================================================
MBTiles
================================================================================

.. shortname:: MBTiles

.. build_dependencies:: libsqlite3

MBTiles 드라이버는 SQLite 데이터베이스에 타일화 맵 데이터를 저장하기 위한 사양인 MBTiles 포맷에 있는 래스터를 읽어올 수 있습니다.

GDAL 2.1버전부터, MBTiles 드라이버는 MBTiles 래스터 데이터셋의 생성 및 쓰기를 지원합니다.

GDAL 2.3버전부터, MBTiles 드라이버는 MBTiles 벡터 데이터셋 읽기 및 쓰기를 지원합니다. 독립형 맵박스 벡터 타일(Mapbox Vector Tile) 파일 또는 MVT 파일 집합의 경우, :ref:`MVT <vector.mvt>` 드라이버를 참조하십시오.
주의: 벡터 쓰기를 지원하려면 GDAL을 GEOS와 함께 빌드해야 합니다.

이 드라이버를 사용하려면 GDAL/OGR을 OGR SQLite 드라이버 지원, 그리고 JPEG 및 PNG 드라이버와 함께 컴파일해야만 합니다.

공간 좌표계는 항상 (구글 메르카토르 같은) 웹 메르카토르 투영법입니다.

GDAL 2.3버전부터, 이 드라이버는 데이터셋을 RGBA로 열 것입니다. 그 이전 버전들의 경우 드라이버가 타일 1개의 내용을 살펴서 밴드 개수를 판단하려 시도할 것입니다. MBTILES_BAND_COUNT 환경설정 옵션에 (또는 GDAL 2.1버전부터 BAND_COUNT 열기 옵션에) 밴드 개수를 정의하면 이 습성을 바꿀 수 있습니다. 이 옵션들에 설정할 수 있는 값은 1, 2, 3, 4 가운데 하나입니다. 저장할 수 있는, 다양하게 인코딩된 타일과 최고의 호환성을 보여주는 것은 4밴드(적색, 녹색, 청색, 알파) 데이터셋입니다.

이 드라이버는 메타데이터 테이블에 있는 'bounds' 메타데이터를 읽어와서 -- 필요하다면 -- 해당 범위를 따르기 위해 필요한 타일 자르기를 수행할 것입니다. 하지만 이 정보는 선택 옵션으로, 생략하는 경우 드라이버가 최대 확대/축소 수준의 타일들의 범위를 사용할 것입니다. 최대 확대/축소 수준의 타일들의 실제 범위를 강제로 사용하고 싶다면 사용자도 USE_BOUNDS=NO 열기 옵션을 지정하면 됩니다. 또는 범위를 사용자 지정하고 싶은 경우 MINX/MINY/MAXX/MAXY 가운데 하나라도 지정하면 됩니다.

이 드라이버는 -- 일부 MBTiles 파일에서 사용할 수 있는 -- UTFGrid 사양에 따라 인코딩된 픽셀 속성을 가져올 수 있습니다. gdallocationinfo 유틸리티를 사용하거나 밴드 객체에 GetMetadataItem("Pixel_iCol_iLine", "LocationInfo")을 호출하면 이 픽셀 정보를 수집할 수 있습니다.


드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::


열기 옵션
---------------

GDAL 2.1버전부터, 다음과 같은 열기 옵션들을 사용할 수 있습니다:

-  래스터 및 벡터:

   -  **ZOOM_LEVEL=value**:
      0에서 'tiles' 테이블에 있는 최대값 사이의 정수값을 설정합니다. 이 드라이버는 기본적으로 'tiles' 테이블에서 해당 확대/축소 수준의 타일을 최소한 1개는 찾도록 최대 확대/축소 수준을 선택할 것입니다.

   -  **USE_BOUNDS=YES/NO**:
      사용할 수 있는 경우 관심 영역을 판단하기 위해 'bounds' 메타데이터를 사용할지 여부를 선택합니다. 기본값은 YES입니다.

   -  **MINX=value**:
      관심 영역의 (EPSG:3857의) 최소 편동을 설정합니다.

   -  **MINY=value**: 
      관심 영역의 (EPSG:3857의) 최소 편북을 설정합니다.

   -  **MAXX=value**: 
      관심 영역의 (EPSG:3857의) 최대 편동을 설정합니다.

   -  **MAXY=value**:
      관심 영역의 (EPSG:3857의) 최대 편북을 설정합니다.

-  래스터 전용:

   -  **BAND_COUNT=AUTO/1/2/3/4**:
      데이터셋을 연 다음 노출시킬 밴드 개수를 설정합니다. 몇몇 변환 작업이 구현되어 사용할 수 있는 경우 수행할 것이지만, BAND_COUNT 값과 타일의 밴드 개수에 따라 변환에 실패할 수도 있습니다. 기본값은 AUTO입니다.

   -  **TILE_FORMAT=PNG/PNG8/JPEG**:
      타일을 저장할 포맷을 설정합니다. `타일 포맷 <#raster.mbtiles.tile_formats>`_ 단락을 참조하십시오. 업데이트 모드에서만 사용할 수 있습니다. 기본값은 PNG입니다.

   -  **QUALITY=1-100**:
      JPEG 압축 품질을 설정합니다. 업데이트 모드에서만 사용할 수 있습니다. 기본값은 75입니다.

   -  **ZLEVEL=1-9**:
      PNG 타일 용 DEFLATE 압축 수준을 설정합니다. 업데이트 모드에서만 사용할 수 있습니다. 기본값은 6입니다.

   -  **DITHER=YES/NO**:
      (TILE_FORMAT을 PNG8로 설정한 경우) 플로이드-스타인버그 디더링을 사용할지 여부를 선택합니다. 업데이트 모드에서만 사용할 수 있습니다. 기본값은 NO입니다.

-  벡터 전용(GDAL 2.3 이상 버전):

   -  **CLIP=YES/NO**:
      벡터 객체의 도형을 타일 범위에 맞춰 자를지 여부를 선택합니다. 기본값은 YES입니다.

   -  **ZOOM_LEVEL_AUTO=YES/NO**:
      벡터 레이어의 확대/축소 수준을 공간 필터 범위에 따라 자동 선택할지 여부를 선택합니다. 기본값은 NO입니다.


래스터 생성 문제점
----------------------

이 드라이버는 입력 데이터셋의 밴드 개수와 선택한 타일 포맷에 따라 타일 포맷을 호환시키기 위한 필수 변환 작업을 수행할 것입니다. (gdal_translate 같은) CreateCopy() API 사용 시, 적절한 확대/축소 수준들을 선택해서 입력 데이터셋을 EPSG:3857(웹 메르카토르)로 자동 재투영할 것입니다.

포맷이 허용하는 대로, 완전히 투명한 타일은 데이터베이스에 작성되지 않을 것입니다.

이 드라이버는 Create() 및 IWriteBlock() 메소드를 구현하기 때문에, 래스터 블록을 임의 작성할 수 있습니다. 즉 MBTiles를 gdalwarp 같은 유틸리티의 산출 데이터셋으로 직접 사용할 수 있다는 뜻입니다.

생성 작업 시, SetGeoTransform()으로 지리변형 행렬을 설정한 경우에만 래스터 블록을 작성할 수 있습니다. 픽셀 해상도, 데이터셋, 그리고 타일 크기를 기반으로 전체 해상도 데이터셋의 확대/축소 수준을 판단하기 위해서는 실질적으로 지리변형 행렬이 필요합니다.

기술/구현 메모: 일반적인 경우, GDAL 블록들이 단일 MBTiles 타일과 정확히 일치하지 않을 가능성이 있습니다. 이런 경우 각 GDAL 블록이 MBTiles 타일 4개와 중첩할 것입니다. 읽어오는 경우에는 쉽게 처리할 수 있지만, 생성/업데이트하는 경우에는 이런 환경설정이 수많은 타일들을 압축 해제/재압축시켜야 하는 상황을 일으킬 수 있습니다. 이런 상황이 발생하면 손실 압축 방식(JPEG)을 사용하는 경우 불필요한 품질 저하가 일어날 수도 있습니다. 이렇게 되는 일을 피하기 위해, 이 드라이버는 주 MBTiles 파일 옆에 부분 MBTiles 타일들을 비손실 (그리고 비압축) 방식으로 저장하기 위한 임시 데이터베이스를 생성할 것입니다. 그리고 타일이 자신의 4분면 및 모든 밴드의 데이터를 받은 다음 (또는 데이터셋을 닫거나, 캐시에서 데이터셋을 FlushCache()로 확실하게 제거한 다음) MBTiles 파일에 이 비압축 타일들을 적절한 방식으로 압축해서 확실히 전송합니다. GDAL API/유틸리티 사용자에게 이 모든 과정을 공개합니다.

.. _raster.mbtiles.tile_formats:

타일 포맷
~~~~~~~~~~~~

MBTiles는 타일을 PNG 또는 JPEG으로 저장할 수 있습니다. 이런 타일 포맷 지원은 GDAL에서 기저 드라이버를 사용할 수 있는지에 따라 달라집니다. GDAL은 기본적으로 PNG 타일을 사용할 것입니다.

TILE_FORMAT 생성/열기 옵션을 PNG, PNG8, 또는 JPEG 가운데 하나로 설정하면 타일 포맷을 선택할 수도 있습니다. JPEG을 선택한 경우, 알파 채널을 저장하지 않을 것입니다.

256색까지 지원하는 색상표를 가진 8비트 PNG를 사용하려면 PNG8을 선택하면 됩니다. 생성 작업 시, 각 타일에 최적화된 색상표를 계산합니다. 플로이드-스타인버그 디더링 알고리즘을 사용하려면 DITHER 옵션을 YES로 설정하면 됩니다. 이 알고리즘은 더 나은 렌더링을 위해 양자화 오류를 이웃하는 픽셀로 분산시킵니다. (하지만 이미지 확대 시 시각적으로 바람직하지 않은 결과를 보게 될 수 있다는 사실을 기억하십시오.) 일반적으로, DITHER 옵션을 YES로 설정하면 더 비효율적으로 압축하게 될 것입니다. 이때 8비트 PNG 같은 포맷은 완전히 불투명한 타일에만 사용된다는 사실을 기억하십시오. (PNG8 포맷이 투명도를 가진 색상표를 지원할 수는 있지만) 현재 최적 색상표를 계산하기 위해 구현된 중앙값 절단(Median Cut) 알고리즘이 알파 채널을 지원하지 않기 때문입니다. 따라서 PNG8을 선택하는 경우, 완전히 불투명하지 않은 타일은 32비트 PNG로 저장될 것입니다.


벡터 생성 문제점
----------------------

웹 메르카토르(EPSG:3857) 투영법으로 타일을 생성합니다. 어떤 확대/축소 수준 범위에서 지정한 레이어를 작성할지 결정할 수도 있습니다. 레이어 여러 개를 작성할 수 있지만 벡터 데이터의 경우 이 드라이버는 한 번 작성(write-once)만 지원합니다. 벡터 데이터셋 여러 개를 MBTiles 파일로 작성하는 경우, GeoPackage 같은 중간 포맷을 컨테이너로 사용해야만 모든 레이어를 동시에 변환할 수 있습니다. 한 번 작성(write-once)만 지원한다는 것은 기존 벡터 레이어를 편집할 수 없다는 뜻도 됩니다.

변환 작업의 일부분은 기본적으로 코어 개수만큼 많은 스레드를 사용하는 멀티스레딩입니다. :decl_configoption:`GDAL_NUM_THREADS` 환경설정 옵션으로 사용할 수 있는 스레드의 개수를 제어할 수 있습니다.

생성 옵션
----------------

다음과 같은 생성 옵션들을 사용할 수 있습니다:

-  래스터 및 벡터:

   -  **NAME=string**:
      'name' 메타데이터 항목을 설정하는 데 쓰이는 타일 집합 이름입니다. 지정하지 않는 경우, 파일명의 기본 이름(basename)을 사용할 것입니다.

   -  **DESCRIPTION=string**:
      'description' 메타데이터 항목을 설정하는 데 쓰이는 레이어 설명입니다. 지정하지 않는 경우, 파일명의 기본 이름(basename)을 사용할 것입니다.

   -  **TYPE=overlay/baselayer**:
      'type' 메타데이터 항목을 설정하는 데 쓰이는 레이어 유형입니다. 기본값은 'overlay'입니다.

-  래스터 전용:

   -  **VERSION=string**:
      'version' 메타데이터 항목을 설정하는 데 쓰이는 평문 숫자로 된 타일 집합의 버전입니다. 기본값은 '1.1'입니다.

   -  **BLOCKSIZE=integer**:
      (GDAL 2.3 이상 버전) 블록/타일 크기를 픽셀 단위 너비와 높이로 설정합니다. 기본값은 256입니다. 최대 4096까지 지원합니다.

   -  **TILE_FORMAT=PNG/PNG8/JPEG**:
      타일을 저장하기 위해 쓰이는 포맷입니다. `타일 포맷 <#raster.mbtiles.tile_formats>`_ 단락을 참조하십시오. 기본값은 PNG입니다.

   -  **QUALITY=1-100**:
      JPEG 압축 품질을 설정합니다. 기본값은 75입니다.

   -  **ZLEVEL=1-9**:
      PNG 타일 용 DEFLATE 압축 수준을 설정합니다. 기본값은 6입니다.

   -  **DITHER=YES/NO**:
      (TILE_FORMAT을 PNG8로 설정한 경우) 플로이드-스타인버그 디더링을 사용할지 여부를 선택합니다. 기본값은 NO입니다.

   -  **ZOOM_LEVEL_STRATEGY=AUTO/LOWER/UPPER**:
      확대/축소 수준을 결정할 전략을 선택합니다. LOWER는 내장되지 않은, 이론적으로 계산된 확대/축소 수준 바로 아래의 확대/축소 수준을 선택하고 서브샘플링 작업을 수행할 것입니다. UPPER는 그 반대로 바로 위의 확대/축소 수준을 선택하고 오버샘플링 작업을 수행할 것입니다. 기본값은 가장 가까운 확대/축소 수준을 선택하는 AUTO입니다.


   -  **RESAMPLING=NEAREST/BILINEAR/CUBIC/CUBICSPLINE/LANCZOS/MODE/AVERAGE**:
      리샘플링 알고리즘을 선택합니다. 기본값은 BILINEAR입니다.

   -  **WRITE_BOUNDS=YES/NO**:
      'bounds' 메타데이터 항목을 작성할지 여부를 선택합니다. 기본값은 YES입니다.

-  벡터 전용(GDAL 2.3 이상 버전):

   -  **MINZOOM=integer**:
      타일을 생성할 최소 확대/축소 수준을 설정합니다. 기본값은 0입니다.

   -  **MAXZOOM=integer**:
      타일을 생성할 최대 확대/축소 수준을 설정합니다. 기본값은 5입니다. 최대 22까지 설정할 수 있습니다.

   -  **CONF=string**:
      레이어를 JSON 직렬화(serialized) 문자열로 환경설정합니다.

   -  **SIMPLIFICATION=float**:
      라인 또는 폴리곤 도형 용 단순화 인자를 설정합니다. 단위는 도형 좌표를 타일 좌표로 수량화(quantification)한 후의 타일의 정수형 단위입니다. SIMPLIFICATION_MAX_ZOOM을 함께 정의하지 않는 한 모든 확대/축소 수준에 적용됩니다.

   -  **SIMPLIFICATION_MAX_ZOOM=float**:
      라인 또는 폴리곤 도형 용 단순화 인자가 설정한 최대 확대/축소 수준까지만 적용됩니다.

   -  **EXTENT=positive_integer**:
      타일 하나에 있는 단위 개수를 설정합니다. 큰 값을 설정할수록 (타일의 바이트 용량은 커지지만) 더 정확한 도형 좌표를 작성합니다. 기본값은 4096입니다.

   -  **BUFFER=positive_integer**:
      도형 버퍼 작업 용 단위 개수를 설정합니다. 이 값은 도형을 가져오고 자르는 기준이 되는 타일 각 변 주위의 버퍼에 대응합니다. 몇몇 렌더링 클라이언트가 타일 경계와 교차하는 도형을 제대로 렌더링하기 위해 사용하는 값입니다. EXTENT를 4096으로 설정한 경우 기본값은 80입니다.

   -  **COMPRESS=YES/NO**:
      타일을 DEFALTE/gzip 알고리즘으로 압축할지 여부를 선택합니다. 기본값은 YES입니다. FORMAT을 MBTILES로 설정한 경우 YES로 유지해야 합니다.

   -  **TEMPORARY_DB=string**:
      타일 생성에 쓰이는 임시 데이터베이스를 가리키는 경로+파일명입니다. 이 파일은 기본적으로 산출 파일/디렉터리와 동일한 디렉터리에 있을 것입니다.

   -  **MAX_SIZE=integer**:
      (압축 후) 최대 타일 용량을 바이트 단위로 설정합니다. 기본값은 500,000입니다. 타일 용량이 이 한계값을 초과하는 경우, 객체를 줄어든 정밀도로 작성하거나 또는 폐기할 것입니다.

   -  **MAX_FEATURES=integer**:
      타일 당 최대 객체 개수를 설정합니다. 기본값은 200,000입니다.

   -  **BOUNDS=min_long,min_lat,max_long,max_lat**:
      작성된 객체의 범위로부터 계산한 'bounds' 메타데이터 항목의 기본값을 대체합니다.

   -  **CENTER=long,lat,zoom_level**:
      최소 확대/축소 수준에서 BOUNDS의 중심인 'center' 메타데이터 항목의 기본값을 대체합니다.


레이어 환경설정 (벡터)
----------------------------

앞에서 언급했던 데이터셋 생성 옵션 CONF를 다음과 같이 그 값이 JSON 직렬화 문서인 문자열로 설정할 수 있습니다:

::

           {
               "boundaries_lod0": {
                   "target_name": "boundaries",
                   "description": "Country boundaries",
                   "minzoom": 0,
                   "maxzoom": 2
               },
               "boundaries_lod1": {
                   "target_name": "boundaries",
                   "minzoom": 3,
                   "maxzoom": 5
               }
           }

*boundaries_lod0* 및 *boundaries_lod1* 은 대상 MVT 데이터셋으로 생성되는 OGR 레이어의 이름입니다. 이들은 MVT 대상 레이어 *boundaries* 로 매핑됩니다.

ogr2ogr를 사용하는 경우에는 불편하긴 하지만, 다음 레이어 생성 옵션으로도 동일한 결과를 얻을 수 있습니다.


레이어 생성 옵션 (벡터)
-------------------------------

-  **MINZOOM=integer**:
   타일을 생성할 최소 확대/축소 수준을 설정합니다. 기본값은 데이터셋 생성 옵션 MINZOOM의 값입니다.

-  **MAXZOOM=integer**:
   타일을 생성할 최대 확대/축소 수준을 설정합니다. 기본값은 데이터셋 생성 옵션 MAXZOOM의 값입니다. 최대 22까지 설정할 수 있습니다.

-  **NAME=string**:
   대상 레이어의 이름을 설정합니다. 기본값은 입력 레이어 이름이지만, OGR 레이어 여러 개를 대상 MVT 레이어 1개로 매핑할 수 있도록 무시할 수 있습니다. 이 옵션은 상호 배타적인 확대/축소 범위에 서로 다른 OGR 레이어를 작성하고자 할 때 주로 쓰입니다.

-  **DESCRIPTION=string**:
   레이어의 설명입니다.


오버뷰 (래스터)
------------------

gdaladdo 또는 BuildOverviews()를 사용해서 오버뷰를 계산할 수 있습니다. 2의 거듭제곱 오버뷰 인자(2, 4, 8, 16, ...)만 지원합니다.

사용할 수 있는 것보다 더 많은 오버뷰 수준을 지정하는 경우, 초과하는 수준들은 조용히 무시합니다.

gdaladdo의 -clean 옵션으로 (또는 BuildOverviews()의 nOverviews=0 파라미터로) 오버뷰를 제거할 수도 있습니다.

벡터 타일
------------

GDAL 2.3버전부터, MBTiles 드라이버는 맵박스 벡터 타일 포맷을 준수하는 벡터 타일을 담고 있는 MBTiles 파일(.pbf)을 읽어올 수 있습니다.

이 드라이버는 'json'이라는 항목을 담기 위한 'metadata' 테이블을 필요로 합니다. 'json' 항목은 레이어와 그 스키마를 서술하는 'vector_layers' 배열을 가지고 있습니다. :ref:`metadata.json <mvt_metadata_json>` 을 참조하십시오.

주의: 이 드라이버는 타일 여러 개에 중첩하는 객체의 도형들을 함께 병합하려는 시도를 하지 않을 것입니다.

예시
---------

-  원격 MBTiles 래스터에 접근하기:

   ::

      $ gdalinfo /vsicurl/http://a.tiles.mapbox.com/v3/kkaefer.iceland.mbtiles

   산출물:

   ::

      Driver: MBTiles/MBTiles
      Files: /vsicurl/http://a.tiles.mapbox.com/v3/kkaefer.iceland.mbtiles
      Size is 16384, 16384
      Coordinate System is:
      PROJCS["WGS 84 / Pseudo-Mercator",
          GEOGCS["WGS 84",
              DATUM["WGS_1984",
                  SPHEROID["WGS 84",6378137,298.257223563,
                      AUTHORITY["EPSG","7030"]],
                  AUTHORITY["EPSG","6326"]],
              PRIMEM["Greenwich",0,
                  AUTHORITY["EPSG","8901"]],
              UNIT["degree",0.0174532925199433,
                  AUTHORITY["EPSG","9122"]],
              AUTHORITY["EPSG","4326"]],
          PROJECTION["Mercator_1SP"],
          PARAMETER["central_meridian",0],
          PARAMETER["scale_factor",1],
          PARAMETER["false_easting",0],
          PARAMETER["false_northing",0],
          UNIT["metre",1,
              AUTHORITY["EPSG","9001"]],
          AXIS["X",EAST],
          AXIS["Y",NORTH],
          EXTENSION["PROJ4","+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +wktext  +no_defs"],
          AUTHORITY["EPSG","3857"]]
      Origin = (-3757031.250000000000000,11271093.750000000000000)
      Pixel Size = (152.873992919921875,-152.873992919921875)
      Image Structure Metadata:
        INTERLEAVE=PIXEL
      Corner Coordinates:
      Upper Left  (-3757031.250,11271093.750) ( 33d44'59.95"W, 70d36'45.36"N)
      Lower Left  (-3757031.250, 8766406.250) ( 33d44'59.95"W, 61d36'22.97"N)
      Upper Right (-1252343.750,11271093.750) ( 11d14'59.98"W, 70d36'45.36"N)
      Lower Right (-1252343.750, 8766406.250) ( 11d14'59.98"W, 61d36'22.97"N)
      Center      (-2504687.500,10018750.000) ( 22d29'59.97"W, 66d30'47.68"N)
      Band 1 Block=256x256 Type=Byte, ColorInterp=Red
        Overviews: 8192x8192, 4096x4096, 2048x2048, 1024x1024, 512x512
        Mask Flags: PER_DATASET ALPHA
        Overviews of mask band: 8192x8192, 4096x4096, 2048x2048, 1024x1024, 512x512
      Band 2 Block=256x256 Type=Byte, ColorInterp=Green
        Overviews: 8192x8192, 4096x4096, 2048x2048, 1024x1024, 512x512
        Mask Flags: PER_DATASET ALPHA
        Overviews of mask band: 8192x8192, 4096x4096, 2048x2048, 1024x1024, 512x512
      Band 3 Block=256x256 Type=Byte, ColorInterp=Blue
        Overviews: 8192x8192, 4096x4096, 2048x2048, 1024x1024, 512x512
        Mask Flags: PER_DATASET ALPHA
        Overviews of mask band: 8192x8192, 4096x4096, 2048x2048, 1024x1024, 512x512
      Band 4 Block=256x256 Type=Byte, ColorInterp=Alpha
        Overviews: 8192x8192, 4096x4096, 2048x2048, 1024x1024, 512x512

-  UTFGrid 사양에 따라 인코딩된 픽셀 속성 읽어오기:

   ::

      $ gdallocationinfo /vsicurl/http://a.tiles.mapbox.com/v3/mapbox.geography-class.mbtiles -wgs84 2 49 -b 1 -xml

   산출물:

   ::

      <Report pixel="33132" line="22506">
        <BandReport band="1">
          <LocationInfo>
            <Key>74</Key>
            <JSon>{"admin":"France","flag_png":"iVBORw0KGgoAAAANSUhEUgAAAGQAAABDEAIAAAC1uevOAAAACXBIWXMAAABIAAAASABGyWs+AAAABmJLR0T///////8JWPfcAAABPklEQVR42u3cMRLBQBSA4Zc9CgqcALXC4bThBA5gNFyFM+wBVNFqjYTszpfi1Sm++bOv2ETEdNK2pc/T9ny977rCn+fx8rjtc7dMmybnxXy9KncGWGCBBRZYYIEFFlhggQUWWGCBBRZYYIE1/GzSLB0CLLAUCyywwAILLLDAAgsssGyFlcAqnJRiKRZYYIEFFlhggQUWWGDZCsFSLLDAAgsssP4DazQowVIssMACy1ZYG6wP30qxwFIssMACCyywwOr/HAYWWIplKwQLLLDAAgssZyywwAILLLDAqh6We4VgKZatECywFAsssMACCyywwAILLLBshWCBpVhggQUWWGCBBRZYYIFlKwQLLMUCCyywwAILLLBG+T8ZsMBSLFshWIoFFlhg/fp8BhZYigUWWGB9C+t9ggUWWGD5FA44XxBz7mcwZM9VAAAAJXRFWHRkYXRlOmNyZWF0ZQAyMDExLTA5LTAyVDIzOjI5OjIxLTA0OjAwcQbBWgAAACV0RVh0ZGF0ZTptb2RpZnkAMjAxMS0wMi0yOFQyMTo0ODozMS0wNTowMJkeu+wAAABSdEVYdHN2ZzpiYXNlLXVyaQBmaWxlOi8vL2hvbWUvYWovQ29kZS90bS1tYXN0ZXIvZXhhbXBsZXMvZ2VvZ3JhcGh5LWNsYXNzL2ZsYWdzL0ZSQS5zdmen2JoeAAAAAElFTkSuQmCC"}</JSon>
          </LocationInfo>
          <Value>238</Value>
        </BandReport>
      </Report>

-  데이터셋을 MBTiles로 변환하고 오버뷰 추가하기:

   ::

      $ gdal_translate my_dataset.tif my_dataset.mbtiles -of MBTILES
      $ gdaladdo -r average my_dataset.mbtiles 2 4 8 16

-  벡터 MBTiles 열기:

   ::

      $ ogrinfo /home/even/gdal/data/mvt/out.mbtiles
      INFO: Open of `/home/even/gdal/data/mvt/out.mbtiles'
            using driver `MBTiles' successful.
      Metadata:
        ZOOM_LEVEL=5
        name=out.mbtiles
        description=out.mbtiles
        version=2
        minzoom=0
        maxzoom=5
        center=16.875000,44.951199,5
        bounds=-180.000000,-85.051129,180.000000,83.634101
        type=overlay
        format=pbf
      1: ne_10m_admin_1_states_provinces_shpgeojson (Multi Polygon)

-  지오패키지를 벡터 타일 MBTILES로 변환하기:

   ::

      $ ogr2ogr -f MBTILES target.mbtiles source.gpkg -dsco MAXZOOM=10

참고
--------

-  `MBTiles 사양 <https://github.com/mapbox/mbtiles-spec>`_

-  `UTFGrid 사양 <https://github.com/mapbox/utfgrid-spec/blob/master/1.0/utfgrid.md>`_

-  :ref:`맵박스 벡터 타일 <vector.mvt>` 드라이버

