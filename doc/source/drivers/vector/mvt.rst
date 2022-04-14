.. _vector.mvt:

MVT: 맵박스 벡터 타일
========================

.. versionadded:: 2.3

.. shortname:: MVT

.. build_dependencies:: (쓰기 지원에 SQLite 및 GEOS 필요)

MVT 드라이버는 맵박스(Mapbox) 벡터 타일 파일을 (일반적으로 .pbf, .mvt, .mvt.gz 확장자를 가진) 비압축 또는 gzip 압축 독립형 파일로, 또는 해당 파일의 지정 확대/축소 수준에 있는 타일 집합(tileset)으로 읽고 쓸 수 있습니다. 쓰기를 지원하려면 GDAL이 libsqlite3 및 GEOS 지원과 함께 빌드되어 있어야 합니다.

:ref:`MBTiles <raster.mbtiles>` 드라이버가 SQLite 컨테이너 안에 MBTiles 포맷을 준수해서 저장된 맵박스 벡터 타일을 처리합니다.

예를 들어 `tippecanoe <https://github.com/mapbox/tippecanoe>`_ 또는 `tileserver-gl <https://github.com/klokantech/tileserver-gl>`_ 이 MVT 파일의 타일 집합을 생성할 수 있습니다. 산출 파일 계층(hierarchy)은 그 루트에 :ref:`metadata.json <mvt_metadata_json>` 을 담고 타일을 가진 {z}/{x}/{y}.pbf 파일을 담을 것입니다. 이때 z는 확대/축소 수준이고 (x, y)는 지정 확대/축소 수준에서의 타일 좌표입니다. 타일 작업 시스템의 원점(origin)은 (XYZ 규범을 따르는) 좌상단 타일입니다. 예를 들면 확대/축소 0수준 및 1수준의 경우:

::

   /metadata.json
   /0/
      0/
        0.pbf
   /1/
      0/
        0.pbf
        1.pbf
      1/
        0.pbf
        1.pbf

{Z}/{X}/{Y}.pbf 또는 {Z}-{X}-{Y}.pbf 같은 파일명을 가진 파일 또는 타일 집합의 확대/축소 수준을 열 때, 이 드라이버는 기본적으로 EPSG:3857 (웹 메르카토르 투영법) 공간 좌표계와 Z/X/Y 타일 작업 구조를 가정할 것입니다. 그렇지 않은 경우 정수형 좌표를 리포트할 것입니다.

주의: 타일 집합의 확대/축소 수준을 여는 경우 이 드라이버는 타일 여러 개와 중첩하는 객체의 도형들을 이어붙이려는 시도를 하지 않을 것입니다.

데이터베이스 케이퍼빌리티
-------------------

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::

연결 문자열
------------------

다음과 같은 연결 문자열을 지원합니다:

-  */path/to/some.pbf*

-  *MVT:http[s]://path/to/some.pbf*

-  */path/to/{Z}*:
   이때 ``{Z}`` 는 0에서 30 사이의 확대/축소 수준이고, 타일은 ``/path/to/{Z}/{X}/{Y}.pbf`` 파일에 있으며, 일반적으로 ``/path/to/metadata.json`` 또는 ``/path/to.json`` 파일이 존재합니다.

-  *MVT:http[s]://path/to/{Z]*

지침이 없는(non-guided) 식별 작업이 실패하는 드문 경우에 데이터셋을 강제로 식별할 수 있도록 파일명 또는 디렉터리 이름 앞에 "*MVT:*" 접두어를 추가할 수도 있습니다.

.. _mvt_metadata_json:

metadata.json
-------------

일반적으로 `tippecanoe <https://github.com/mapbox/tippecanoe>`_ 가 이 파일을 생성하며, 다음 예시와 같은 내용을 담고 있습니다:

.. code-block:: json

   {
       "name": "my_layername",
       "description": "my_layername",
       "version": "2",
       "minzoom": "0",
       "maxzoom": "0",
       "center": "2.500000,49.500000,0",
       "bounds": "2.000000,49.000000,3.000000,50.000000",
       "type": "overlay",
       "format": "pbf",
       "json": "{
           \"vector_layers\": [ {
               \"id\": \"my_layername\",
               \"description\": \"\",
               \"minzoom\": 0,
               \"maxzoom\": 0,
               \"fields\": {
                   \"bool_false\": \"Boolean\",
                   \"bool_true\": \"Boolean\",
                   \"float_value\": \"Number\",
                   \"pos_int_value\": \"Number\",
                   \"pos_int64_value\": \"Number\",
                   \"neg_int_value\": \"Number\",
                   \"neg_int64_value\": \"Number\",
                   \"pos_sint_value\": \"Number\",
                   \"pos_sint64_value\": \"Number\",
                   \"neg_sint_value\": \"Number\",
                   \"neg_sint64_value\": \"Number\",
                   \"real_value\": \"Number\",
                   \"string_value\": \"String\",
                   \"uint_value\": \"Number\",
                   \"uint64_value\": \"Number\"
               }
           } ],
           \"tilestats\": {
               \"layerCount\": 1,
               \"layers\": [
                   {
                   \"layer\": \"my_layername\",
                   \"count\": 2,
                   \"geometry\": \"Point\",
                   \"attributeCount\": 0,
                   \"attributes\": []
                   }
               ]
           }
       }}"
   }

MVT 드라이버는 레이어 이름, 레이어의 필드, 그리고 도형 유형을 가져오는 데 "json" 키만 사용하며, 레이어 범위를 가져오는 데에는 "bounds" 키를 사용합니다.

이 파일을 찾을 수 없는 경우, 타일(들)의 객체를 스캔해서 레이어 스키마를 확립합니다.

확장 사양으로서, OGR는 *crs*, *tile_origin_upper_left_x*, *tile_origin_upper_left_y* 및 *tile_dimension_zoom_0* 메타데이터 항목들을 이용해서 사용자 지정 타일 작업 스키마의 읽기 및 쓰기를 처리합니다. 예를 들어 핀란드 ETRS-TM35FIN (EPSG:3067) 타일 작업 스키마의 경우:

.. code-block:: json

   {
     "...": "...",
     "crs":"EPSG:3067",
     "tile_origin_upper_left_x":-548576.0,
     "tile_origin_upper_left_y":8388608.0,
     "tile_dimension_zoom_0":2097152.0,
   }

열기 옵션
---------------

다음 열기 옵션들을 사용할 수 있습니다:

-  **X=int_value**:
   EPSG:3857 타일의 X 좌표입니다.

-  **Y=int_value**:
   EPSG:3857 타일의 Y 좌표입니다.

-  **Z=int_value**:
   EPSG:3857 타일의 Z 좌표입니다.

-  **METADATA_FILE=filename**:
   metadata.json 유사 파일의 파일명입니다.
   /path/to/{Z}/{X}/{Y}.pbf 파일을 여는 경우, 이 드라이버는 기본적으로 /path/to/metadata.json 파일을 찾으려 시도할 것입니다. 이 옵션의 값을 비어 있는 문자열로 설정하면 metadata.json 파일이 사용되는 일을 막을 수 있습니다.

-  **CLIP=YES/NO**:
   벡터 객체의 도형을 타일 범위로 자를지 여부를 선택합니다. 벡터 타일 작성기는 일반적으로 타일 범위를 넘어가는 작은 버퍼를 가진 객체를 생성하기 때문에 여러 타일과 교차하는 도형들을 다시 통합시킬 수 있습니다. 기본값은 YES입니다. 즉 해당 버퍼를 제거하고 도형을 정확하게 타일 범위에 맞춰 자른다는 뜻입니다.

-  **TILE_EXTENSION=string**:
   타일 집합의 경우 타일의 확장자를 지정합니다. 기본값은 'pbf'입니다.

-  **TILE_COUNT_TO_ESTABLISH_FEATURE_DEFN=int_value**:
   메타데이터 파일이 없는 타일 집합의 경우, 레이어 스키마를 확립하기 위해 사용할 타일의 최대 개수를 지정합니다. 기본값은 1000입니다.

생성 옵션
---------------

기본적으로 웹 메르카토르 (EPSG:3857) 투영법으로 타일을 생성합니다. (사용자 지정 타일 작업 스키마는 TILING_SCHEME 옵션으로 정의할 수 있습니다.) 레이어를 여러 개 작성할 수 있습니다. 어떤 확대/축소 수준 범위에 레이어를 작성할지도 정할 수 있습니다.

변환 작업의 일부분은 기본적으로 스레드를 코어 수만큼 사용하는 멀티스레딩 작업입니다. :decl_configoption:`GDAL_NUM_THREADS` 환경설정 옵션을 이용해서 사용할 스레드의 개수를 제어할 수 있습니다.

데이터셋 생성 옵션
------------------------

-  **NAME=string**:
   타일 집합 이름을 지정합니다. 기본값은 산출 파일/디렉터리의 기본명입니다. 메타데이터 레코드를 채우는 데 쓰입니다.

-  **DESCRIPTION=string**:
   타일 집합 설명을 지정합니다. 메타데이터 레코드를 채우는 데 쓰입니다.

-  **TYPE=overlay/baselayer**:
   레이어 유형을 지정합니다. 메타데이터 레코드를 채우는 데 쓰입니다.

-  **FORMAT=DIRECTORY/MBTILES**:
   타일을 작성할 포맷을 지정합니다.
   DIRECTORY는 타일을 out_dir/{z}/{x}/{y}.pbf 같은 계층으로 작성한다는 뜻입니다.
   MBTILES는 MBTILES 컨테이너에 작성합니다.
   산출 파일명의 확장자가 .mbtiles가 아닌 한 기본값은 DIRECTORY입니다.

-  **TILE_EXTENSION=string**:
   파일 디렉터리로서의 타일 집합인 경우, 타일의 확장자를 지정합니다. 기본값은 pbf입니다.

-  **MINZOOM=integer**:
   타일을 생성할 최소 확대/축소 수준을 지정합니다. 기본값은 0입니다.

-  **MAXZOOM=integer**: 
   타일을 생성할 최대 확대/축소 수준을 지정합니다. 기본값은 5입니다. 지원하는 최대값은 22입니다.

-  **CONF=string**:
   레이어 환경설정을 JSon 직렬화 문자열로 지정합니다.
   또는 GDAL 3.0.1버전부터는 환경설정을 JSon으로 담고 있는 파일명을 지정합니다.

-  **SIMPLIFICATION=float**:
   라인 또는 폴리곤 도형 용 단순화 인자를 지정합니다. 단위는 도형 좌표를 타일 좌표로 정량화(quantification)한 후의 타일의 정수형 단위입니다. SIMPLIFICATION_MAX_ZOOM 옵션도 설정하지 않는 이상 모든 확대/축소 수준에 적용됩니다.

-  **SIMPLIFICATION_MAX_ZOOM=float**:
   최대 확대/축소 수준에만 적용되는 라인 또는 폴리곤 도형 용 단순화 인자를 지정합니다.

-  **EXTENT=positive_integer**:
   타일에 있는 단위의 개수를 지정합니다. 값이 클수록 도형 좌표가 더 정확해집니다. (타일의 바이트 용량은 커집니다.) 기본값은 4096입니다.

-  **BUFFER=positive_integer**:
   도형 버퍼 작업에 사용할 단위의 개수를 지정합니다. 이 값은 도형을 가져와서 자르게 될 타일의 각 변을 감쌀 버퍼에 대응합니다. 몇몇 렌더링 클라이언트가 타일 경계를 넘어가는 도형을 제대로 렌더링하기 위해 이 값을 사용합니다. EXTENT=4096인 경우 기본값은 80입니다.

-  **COMPRESS=YES/NO**:
   타일을 Deflate/GZip 알고리즘으로 압축할지 여부를 선택합니다. 기본값은 YES입니다. FORMAT=MBTILES인 경우 YES로 내버려둬야 합니다.

-  **TEMPORARY_DB=string**:
   타일 생성 작업에 사용되는 임시 데이터베이스 용 경로를 가진 파일명을 지정합니다. 기본적으로 이 파일은 산출 파일/디렉터리와 동일한 디렉터리에 있을 것입니다.

-  **MAX_SIZE=integer**:
   타일의 (압축 후) 바이트 단위 최대 용량을 지정합니다. 기본값은 500,000입니다. 타일 용량이 이 한계값을 초과하는 경우, 객체를 줄어든 정밀도로 작성하거나 또는 폐기할 것입니다.

-  **MAX_FEATURES=integer**:
   타일 당 객체의 최대 개수를 지정합니다. 기본값은 200,000입니다.

-  **BOUNDS=min_long,min_lat,max_long,max_lat**:
   작성되는 객체의 범위로부터 계산되는 <bounds> 메타데이터 항목의 기본값을 대체할 값을 지정합니다.

-  **CENTER=long,lat,zoom_level**:
   최소 확대/축소 수준에서의 BOUNDS 중심인 <center> 메타데이터 항목의 기본값을 대체할 값을 지정합니다.

-  **TILING_SCHEME=crs,tile_origin_upper_left_x,tile_origin_upper_left_y,tile_dimension_zoom_0**:
   (일반적으로 EPSG:XXXX로 지정되는) 좌표계, 해당 좌표계에서 (0,0)인 좌상단 타일의 좌상단 모서리의 좌표, 그리고 확대/축소 0수준에서의 타일 크기를 가지고 있는 사용자 지정 타일 작업 스키마를 정의합니다.
   FORMAT=DIRECTORY인 경우에만 사용할 수 있습니다.
   표준 웹 메르카토르 타일 작업 스키마는 "EPSG:3857,-20037508.343,20037508.343,40075016.686"로 정의될 것입니다.
   WGS84 측지 좌표계의 경우 타일 작업 스키마는 "EPSG:4326,-180,180,360"일 수 있습니다.
   핀란드 ETRS-TM35FIN (EPSG:3067) 타일 작업 스키마는 "EPSG:3067,-548576,8388608,2097152"입니다.
   이런 사용자 지정 타일 작업 스키마를 사용할 때, metadata.json 파일에 'crs', 'tile_origin_upper_left_x', 'tile_origin_upper_left_y' 및 'tile_dimension_zoom_0' 항목을 추가하고 OGR MVT 판독기는 이를 준수합니다.

레이어 환경설정
-------------------

앞에서 언급했던 CONF 데이터셋 생성 옵션의 값을 다음과 같은 JSon 직렬화 문서인 문자열로 설정할 수 있습니다:

.. code-block:: json

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

*boundaries_lod0* 및 *boundaries_lod1* 이 대상 MVT 데이터셋으로 생성되는 OGR 레이어의 이름입니다. 이 레이어들은 대상 MVT 레이어 *boundaries*로 매핑됩니다.

ogr2ogr 사용례에서 사용하기 불편하긴 하지만, 다음 레이어 생성 옵션으로도 동일한 습성을 얻을 수 있습니다.

레이어 생성 옵션
----------------------

-  **MINZOOM=integer**:
   타일을 생성할 최소 확대/축소 수준을 지정합니다. 기본값은 데이터셋 생성 옵션 MINZOOM의 값입니다.

-  **MAXZOOM=integer**:
   타일을 생성할 최대 확대/축소 수준을 지정합니다. 기본값은 데이터셋 생성 옵션 MAXZOOM의 값입니다.
   지원하는 최대값은 22입니다.

-  **NAME=string**:
   대상 레이어 이름을 지정합니다. 기본값은 소스 레이어 이름이지만, OGR 레이어 여러 개를 대상 단일 MVT 레이어로 매핑시키기 위해 대체할 수 있습니다. 이 옵션의 전형적인 사용례는 상호배타적인 확대/축소 수준 범위에 서로 다른 OGR 레이어를 생성하는 것입니다.

-  **DESCRIPTION=string**:
   레이어의 설명을 지정합니다.

예시
--------

::

   ogrinfo MVT:https://free.tilehosting.com/data/v3/1 -oo tile_extension="pbf.pict?key=${YOUR_KEY}" --debug on -oo metadata_file="https://free.tilehosting.com/data/v3.json?key=${YOUR_KEY}"

::

   ogr2ogr -f MVT mytileset source.gpkg -dsco MAXZOOM=10

참고
----

-  `맵박스 벡터 타일 사양 <https://github.com/mapbox/vector-tile-spec>`_

-  :ref:`MBTiles <raster.mbtiles>` 드라이버

-  `tippecanoe <https://github.com/mapbox/tippecanoe>`_:
   GeoJSON, Geobuf, 또는 CSV 객체의 대용량 (또는 소용량) 집합(collection)으로부터 벡터 타일 집합을 작성합니다.

-  `맵박스 벡터 타일을 처리하는 도구 링크 <https://github.com/mapbox/awesome-vector-tiles>`_

