.. _raster.plmosaic:

================================================================================
PLMosaic (플래닛 랩스 모자이크 API)
================================================================================

.. shortname:: PLMosaic

.. build_dependencies:: libcurl

이 드라이버는 플래닛 랩스 모자이크(Planet Labs Mosaics) API에 접속할 수 있습니다. PLMosaic 드라이버를 컴파일하기 위해서는 GDAL/OGR을 cURL 지원과 함께 빌드해야만 합니다.

이 드라이버는 모자이크 목록화 및 읽기를 지원합니다. 모자이크의 최고 해상도 수준에 접근합니다. 모자이크는 일반적으로 4096x4096픽셀의 사변형(quad)으로 이루어져 있습니다.

바이트 데이터 유형인 모자이크의 경우, 타일 API를 이용해서 오버뷰를 사용할 수 있습니다. 다른 데이터 유형이라면 오버뷰를 지원하지 않기 때문에 다운샘플링 관련 요청이 종료될 때까지 시간이 꽤 걸릴 수도 있습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

데이터셋 이름 문법
-------------------

데이터소스를 열기 위한 최소한의 문법은 다음과 같습니다:

::

   PLMosaic:[options]

':' 기호 뒤에 추가적인 선택 파라미터를 지정할 수 있습니다. 현재 다음 파라미터들을 지원합니다:

-  **api_key=value**:
   플래닛 API 키를 지정합니다. API_KEY 열기 옵션 또는 PL_API_KEY 환경설정 옵션으로 지정하지 않는 경우 반드시 지정해야만 합니다.

-  **mosaic=mosaic_name**:
   모자이크 이름을 지정합니다.

-  **cache_path=path**:
   캐시된 사변형(과 타일)을 저장하는 디렉터리를 가리키는 경로를 지정합니다. 이 경로 아래 plmosaic_cache/{mosaic_name} 하위 디렉터리를 생성할 것입니다. 디스크 캐시 작업을 비활성화시키려면 이 파라미터를 비어 있는 문자열로 지정하면 됩니다.

-  **trust_cache=YES/NO**:
   이미 캐시된 사변형을 서버가 더 최신 버전을 가지고 있는지 사전 확인하지 않은 채 직접 재사용해야 할지 여부를 선택합니다. 주의: 이 파라미터는 타일이 아니라 사변형에만 적용됩니다. 기본값은 NO입니다.

-  **use_tiles=YES/NO**:
   전체 해상도 데이터에 접근하기 위해 사변형들을 다운로드하는 대신 타일 API를 사용할지 여부를 선택합니다. 바이트형 모자이크에만 적용됩니다. 기본값은 NO입니다.

파라미터 여러 개를 지정하는 경우, 쉼표로 구분해야만 합니다.

모자이크 파라미터를 하나도 지정하지 않으면, 사용할 수 있는 모자이크 목록을 하위 데이터셋으로 반환할 것입니다. 사용할 수 있는 모자이크가 하나밖에 없다면 해당 모자이크를 직접 열 것입니다.

열기 옵션
------------

다음과 같은 열기 옵션들을 사용할 수 있습니다:

   -  API_KEY
   -  MOSAIC
   -  CACHE_PATH
   -  TRUST_CACHE
   -  USE_TILES

이 옵션들은 앞에서 설명한 같은 이름을 가진 파라미터와 동일한 의미를 가집니다.

환경설정 옵션
---------------------

다음 환경설정 옵션을 사용할 수 있습니다:

-  **PL_API_KEY=value**:
   플래닛 API 키를 지정합니다.

위치 정보
--------------------

*LocationInfo* 메타데이터 도메인의 *Pixel_{x}_{y}* 특수 메타데이터 항목을 쿼리해서 하부(underneath) 사변형을 구성하는 신(scene)들에 대한 정보를 수집할 수 있습니다. 이때 x는 모자이크의 열, y는 모자이크의 행입니다. gdallocationinfo 유틸리티가 사용하는 문법입니다. (:ref:`rfc-32` 참조)

다음은 반환되는 정보의 예시입니다:

::

   <LocationInfo>
     <Scenes>
       <Scene>
         <link>https://api.planet.com/data/v1/item-types/PSScene3Band/items/20161025_000336_0e19</link>
       </Scene>
       <Scene>
         <link>https://api.planet.com/data/v1/item-types/PSScene3Band/items/20161119_000453_0e14</link>
       </Scene>
       <Scene>
         <link>https://api.planet.com/data/v1/item-types/PSScene3Band/items/20161010_000309_0e26</link>
       </Scene>
       <Scene>
         <link>https://api.planet.com/data/v1/item-types/PSScene3Band/items/20161119_000452_0e14</link>
       </Scene>
     </Scenes>
   </LocationInfo>

예시
~~~~~~~~

사용할 수 있는 모든 모자이크를 (계정 권한으로) 목록화하는 명령어들:

::

   gdalinfo "PLMosaic:" -oo API_KEY=some_value

또는

::

   gdalinfo "PLMosaic:api_key=some_value"

또는

::

   gdalinfo "PLMosaic:" --config PL_API_KEY some_value

이 명령어들은 (다중 모자이크의 경우) 다음과 같은 정보를 반환합니다:

::

   Driver: PLMOSAIC/Planet Labs Mosaics API
   Files: none associated
   Size is 512, 512
   Coordinate System is `'
   Image Structure Metadata:
     INTERLEAVE=PIXEL
   Subdatasets:
     SUBDATASET_1_NAME=PLMOSAIC:mosaic=global_quarterly_2017q1_mosaic
     SUBDATASET_1_DESC=Mosaic global_quarterly_2017q1_mosaic
     ...
   Corner Coordinates:
   Upper Left  (    0.0,    0.0)
   Lower Left  (    0.0,  512.0)
   Upper Right (  512.0,    0.0)
   Lower Right (  512.0,  512.0)
   Center      (  256.0,  256.0)

특정 모자이크 하나를 열면:

::

   gdalinfo "PLMosaic:mosaic=global_quarterly_2017q1_mosaic" -oo API_KEY=some_value

다음과 같은 정보를 반환합니다:

::

   Driver: PLMOSAIC/Planet Labs Mosaics API
   Files: none associated
   Size is 8388608, 4427776
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
       EXTENSION["PROJ4","+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +wktext +no_defs"],
       AUTHORITY["EPSG","3857"]]
   Origin = (-20037508.342789243906736,13384429.400847502052784)
   Pixel Size = (4.777314267823516,-4.777314267823516)
   Metadata:
     FIRST_ACQUIRED=2017-01-01T00:00:00.000Z
     LAST_ACQUIRED=2017-04-01T00:00:00.000Z
     NAME=global_quarterly_2017q1_mosaic
   Image Structure Metadata:
     INTERLEAVE=PIXEL
   Corner Coordinates:
   Upper Left  (-20037508.343,13384429.401) (180d 0' 0.00"W, 76d 0'57.94"N)
   Lower Left  (-20037508.343,-7768448.059) (180d 0' 0.00"W, 57d 2'26.63"S)
   Upper Right (20037508.343,13384429.401) (180d 0' 0.00"E, 76d 0'57.94"N)
   Lower Right (20037508.343,-7768448.059) (180d 0' 0.00"E, 57d 2'26.63"S)
   Center      (       0.000, 2807990.671) (  0d 0' 0.01"E, 24d26'49.74"N)
   Band 1 Block=256x256 Type=Byte, ColorInterp=Red
     Overviews: 4194304x4194304, ..., 256x256
     Mask Flags: PER_DATASET ALPHA
     Overviews of mask band: Overviews: 4194304x4194304, ..., 256x256
   Band 2 Block=256x256 Type=Byte, ColorInterp=Green
     Overviews: 4194304x4194304, ..., 256x256
     Mask Flags: PER_DATASET ALPHA
     Overviews of mask band: Overviews: 4194304x4194304, ..., 256x256
   Band 3 Block=256x256 Type=Byte, ColorInterp=Blue
     Overviews: 4194304x4194304, ..., 256x256
     Mask Flags: PER_DATASET ALPHA
     Overviews of mask band: Overviews: 4194304x4194304, ..., 256x256
   Band 4 Block=256x256 Type=Byte, ColorInterp=Alpha
     Overviews: 4194304x4194304, ..., 256x256

참고
--------

-  `플래닛 랩스 모자이크 API 문서 <https://developers.planet.com/docs/basemaps/reference/>`_

-  `API 인증 <https://developers.planet.com/docs/apis/data/api-mechanics/>`_

-  :ref:`벡터 PLScenes / 플래닛 랩스 신(Planet Labs Scenes) API <vector.plscenes>` 드라이버

