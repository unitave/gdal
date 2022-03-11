.. _raster.db2:

================================================================================
DB2 래스터
================================================================================

.. shortname:: DB2

.. build_dependencies:: ODBC (그리고 PNG, JPEG, WEBP 드라이버 가운데 하나 또는 모두)

.. note::

    DB2 드라이버는 SQLITE 기능을 그에 대응하는 DB2 기능으로 대체한 OGR/DB2 GeoPackage(GPKG) 드라이버의 소스코드에 크게 바탕을 두고 있습니다. DB2 드라이버를 개발하기 위해 필요했던 노력을 극적으로 줄여준 GeoPackage 드라이버 개발자들에게 감사의 말을 전합니다. 공통 기능을 공유하기 위해 클래스 구조를 재작성하는 일이 과연 실용적인 것인지에 대한 연구가 언젠가 진행되어도 좋을 겁니다.

    DB2 드라이버는 GeoPackage 표준을 대부분 구현했지만, DB2 테이블 이름에서 "gpkg\_" 접두어를 "gpkg."로 대체해서 고유(distinct) 데이터베이스 스키마에 할당했다는 차이가 있습니다.

    이 문서의 내용 대부분은 :ref:`raster.gpkg` 문서에서 가져왔습니다. GeoPackage 표준에 대한 참조는 그대로 두었습니다. 구현에 대한 참조는 DB2로 변경했습니다. "DB2 타일"을 참조해야 하는지 또는 "GeoPackage 타일"을 참조해야 하는지 명확하지 않은 경우도 가끔 있습니다.

이 드라이버는 래스터 타일을 `OGC GeoPackage 포맷 표준 <http://www.geopackage.org/spec/>`_ 으로 담고 있는 테이블의 완전한 읽기/생성/업데이트 기능을 구현했습니다. GeoPackage 표준은 SQLite 데이터베이스 파일을 일반 컨테이너로 사용하며, 다음을 정의하고 있습니다:

-  예상 메타데이터 테이블 (``gpkg.contents``, ``gpkg.spatial_ref_sys``, ``gpkg.tile_matrix``, ``gpkg.tile_matrix_set`` 등등)
-  타일 포맷 인코딩(기반 사양은 PNG 및 JPEG for base specification, 확장 사양은 WebP) 및 타일 작업 규범
-  확장자의 명명 및 규범

이 드라이버는 DB2 데이터베이스의 DB2 테이블을 읽고 쓰기 때문에 이 드라이버가 작업하는 데이터베이스에 대한 생성 권한을 가지고 있는 사용자가 실행해야만 합니다.

이 드라이버는 DB2 벡터도 처리할 수 있습니다. :ref:`DB2 벡터 <vector.db2>` 문서도 읽어보십시오.

다양한 입력 데이터셋 유형을 DB2 래스터로 변환할 수 있습니다:

-  단일 밴드 회색조 수준
-  RGB 또는 RGBA 색상표를 가진 단일 밴드
-  2밴드: 첫 번째 밴드는 회색조 수준, 두 번째 밴드는 알파 채널
-  3밴드: 적색(Red), 녹색(Green), 청색(Blue)
-  4밴드: 적색(Red), 녹색(Green), 청색(Blue), 알파(Alpha)

DB2 래스터는 바이트 데이터 유형만 지원합니다.

GeoPackage 사양으로 표준화된 모든 래스터 확장자를 읽기 및 생성 지원합니다:

-  *gpkg.webp*: WebP 타일을 저장하는 경우, GDAL이 libwebp를 대상으로 컴파일되었다고 가정
-  *gpkg.zoom_other*: 연속하는 확대/축소 수준들의 해상도가 2배수로 변화하지 않는 경우

드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::

.. supports_create::

.. supports_georeferencing::

열기 옵션
---------------

이 드라이버는 기본적으로 DB2 데이터셋을 최대한 다양한 인코딩으로 타일을 저장할 수 있는 능력을 가진 4밴드(RGBA) 데이터셋으로 노출시킵니다. BAND_COUNT 열기 옵션으로 밴드 개수를 명확하게 지정할 수 있습니다.

이 드라이버는 `gpkg.contents <http://www.geopackage.org/spec/#_contents>`_ 테이블에 지정된 지리/투영 범위를 사용하는데, 해당 범위를 따르기 위해 필요하다면 잘라내기 작업을 수행할 것입니다. 하지만 이 정보는 선택적인 옵션으로, 이 옵션이 없을 경우 `gpkg.tile_matrix_set <http://www.geopackage.org/spec/#_tile_matrix_set>`_ 이 제공하는, 모든 확대/축소 수준의 범위를 커버하는 범위를 사용할 것입니다. 사용자가 최대 확대/축소 수준의 실제 타일 범위를 사용하려는 경우 USE_TILE_EXTENT=YES 열기 옵션을 지정하면 됩니다.

다음 열기 옵션들을 사용할 수 있습니다:

-  **TABLE**\ =table_name: 타일을 담고 있는 테이블의 이름입니다. (GeoPackage 사양 용어로는 `"타일 피라미드 사용자 데이터 테이블" <http://www.geopackage.org/spec/#tiles_user_tables>`_ 이라고 합니다.) DB2 데이터셋이 테이블 하나만 담고 있는 경우, 이 옵션은 필요없습니다. 테이블이 하나 이상이라면 필수입니다.
-  **ZOOM_LEVEL**\ =value: 0에서 *gpkg.tile_matrix* 테이블의 최대값 사이의 정수값입니다. 이 드라이버는 기본적으로 래스터 테이블에서 해당 확대/축소 수준의 타일을 최소한 1개는 찾도록 최대 확대/축소 수준을 선택할 것입니다.
-  **BAND_COUNT**\ =1/2/3/4: 데이터셋을 연 다음 노출되는 밴드 개수입니다. 구현되어 있고 사용할 수 있는 경우 몇몇 변환 작업을 수행할 것이지만, BAND_COUNT 값과 타일의 밴드 개수에 따라 실패하는 경우도 생길 수 있습니다. 기본값은 (언제나 안전한 값인) 4입니다.
-  **MINX**\ =value: 관심 영역의 최소 경도/편동(easting)입니다.
-  **MINY**\ =value: 관심 영역의 최소 위도/편북(northing)입니다.
-  **MAXX**\ =value: 관심 영역의 최대 경도/편동(easting)입니다.
-  **MAXY**\ =value: 관심 영역의 최대 위도/편북(northing)입니다.
-  **USE_TILE_EXTENT**\ =YES/NO: 전체 해상도 데이터셋의 확대/축소 수준의 실제 기존 타일들의 범위를 사용할지 여부를 선택합니다. 기본값은 NO입니다.
-  **TILE_FORMAT**\ =PNG_JPEG/PNG/PNG8/JPEG/WEBP: 타일을 저장하기 위해 쓰이는 포맷입니다. `타일 포맷 <#tile-formats>`_ 단락을 참조하십시오. 업데이트 모드에서만 사용합니다. 기본값은 PNG_JPEG입니다.
-  **QUALITY**\ =1-100: JPEG 및 WEBP 압축의 경우 품질을 설정합니다. 업데이트 모드에서만 사용합니다. 기본값은 75입니다.
-  **ZLEVEL**\ =1-9: PNG 타일 용 DEFLATE 압축 수준을 설정합니다. 업데이트 모드에서만 사용합니다. 기본값은 6입니다.
-  **DITHER**\ =YES/NO: (TILE_FORMAT=PNG8일 때) 플로이드-스타인버그 디더링(Floyd–Steinberg dithering)을 사용할지 여부를 선택합니다. 업데이트 모드에서만 사용합니다. 기본값은 NO입니다.

주의: 대부분의 GDAL 유틸리티에서는 일반적으로 오픈 옵션을 "-oo name=value" 문법 또는 GDALOpenEx() API 호출로 지정합니다.

생성 문제점
---------------

이 드라이버는 입력 데이터셋의 밴드 개수와 선택한 타일 포맷에 따라 타일 포맷을 호환시키기 위해 필수 변환 작업을 수행할 것입니다.

DB2 데이터셋에 타일 테이블 여러 개를 (GDAL 하위 데이터셋으로 간주해서) 추가하려면, 또는 기존 벡터 전용 DB2에 타일 테이블을 추가하려면, 일반 APPEND_SUBDATASET=YES 생성 옵션을 반드시 지정해야만 합니다.

완전히 투명한 타일은 포맷이 지원하더라도 데이터베이스에 작성되지 않을 것입니다.

이 드라이버는 Create() 및 IWriteBlock()을 구현하기 때문에, DB2를 gdalwarp 같은 유틸리티들의 산출 데이터셋으로 직접 사용할 수 있도록 래스터 블록을 임의(arbitrary) 작성할 수 있습니다.

생성 작업 시, SetGeoTransform()으로 지리변형(geotransformation) 행렬을 설정한 경우에만 래스터 블록을 작성할 수 있습니다. 픽셀 해상도, 데이터셋, 그리고 타일 크기를 바탕으로 전체 해상도 데이터셋의 확대/축소 수준을 결정하기 위해서는 실질적으로 지리변형 행렬이 필요합니다.

기술/구현 메모: 데이터셋을 기본값이 아닌 관심 영역으로 여는 경우 (예를 들어 MINX,MINY,MAXX,MAXY 또는 USE_TILE_EXTENT 열기 옵션을 사용하는 경우) 또는 데이터셋을 사용자 지정(custom)이 아닌 타일 작업 스키마로 생성/열기하는 경우, GDAL 블록들이 단일 DB2 타일과 정확히 일치하지 않을 가능성이 있습니다. 이런 경우, 각 GDAL 블록이 DB2 타일 4개와 중첩할 것입니다. 읽어오는 경우에는 쉽게 처리할 수 있지만, 생성/업데이트하는 경우에는 이런 환경설정이 수많은 타일들을 압축 해제/재압축시켜야 하는 상황을 일으킬 수 있습니다. 이런 상황이 발생하면 손실 압축 방식(JPEG, WebP)을 사용하는 경우 불필요한 품질 저하가 일어날 수도 있습니다. 이렇게 되는 일을 피하기 위해, 이 드라이버는 주 DB2 테이블 외에 부분 DB2 타일들을 비손실 (그리고 비압축) 방식으로 저장하기 위한 임시 데이터베이스를 생성할 것입니다. 그리고 타일이 자신의 4분면 및 모든 밴드의 데이터를 받은 다음 (또는 데이터셋을 닫거나, 캐시에서 데이터셋을 FlushCache()로 확실하게 제거한 다음) DB2 테이블에 이 비압축 타일들을 적절한 방식으로 압축해서 확실히 전송합니다. GDAL API/유틸리티 사용자에게 이 모든 과정을 공개합니다.

타일 포맷
~~~~~~~~~~~~

DB2는 타일을 서로 다른 포맷으로 저장할 수 있습니다. PNG 그리고/또는 JPEG을 기본 사양으로 사용하고, WebP를 확장 DB2 사양으로 사용합니다. 이런 타일 포맷 지원은 GDAL에서 기저 드라이버를 사용할 수 있는지에 따라 달라집니다. PNG와 JPEG의 경우 일반적으로 기저 드라이버를 사용할 수 있지만, WebP의 경우 GDAL이 선택적인 libwebp를 대상으로 컴파일되어야 하기 때문에 기저 드라이버를 반드시 사용할 수 있다고 장담할 수는 없습니다.

GDAL은 기본적으로 PNG와 JPEG을 혼합해서 사용할 것입니다. 입력 데이터셋이 완전히 불투명하지 않은 내용을 가진 알파 밴드를 가졌거나, 래스터의 우측 또는 하단 경계에서 래스터를 잘라냈거나, 데이터셋을 기본값이 아닌 관심 영역으로 또는 사용자 지정(custom)이 아닌 타일 작업 스키마로 열었기 때문에 완전히 불투명하지 않아진 타일을 저장하기 위해 PNG 파일을 사용할 것입니다. 그 반대로, 완전히 불투명한 타일은 JPEG으로 저장할 것입니다.

TILE_FORMAT 생성/열기 옵션을 PNG, JPEG 또는 WEBP 가운데 하나로 설정하면 유일한 타일 포맷 하나만 선택할 수도 있습니다. JPEG을 선택한 경우, 알파 채널을 저장하지 않을 것입니다. WebP를 선택한 경우, `gpkg.webp <http://www.geopackage.org/spec/#extension_tiles_webp>`_ 확장자를 등록할 것입니다. WebP의 손실 압축 방식을 사용합니다. WebP 타일에서 알파 채널을 지원하려면 최신 (0.1.4버전 이상의) libwebp을 사용해야만 한다는 사실을 기억하십시오.

256색까지 지원하는 색상표를 가진 8비트 PNG를 사용하려면 PNG8을 선택하면 됩니다. 생성 작업 시, 각 타일에 최적화된 색상표를 계산합니다. 플로이드-스타인버그 디더링 알고리즘을 사용하려면 DITHER 옵션을 YES로 설정하면 됩니다. 이 알고리즘은 더 나은 렌더링을 위해 양자화 오류를 이웃하는 픽셀로 분산시킵니다. (하지만 이미지 확대 시 시각적으로 바람직하지 않은 결과를 보게 될 수 있다는 사실을 기억하십시오.) 일반적으로, DITHER 옵션을 YES로 설정하면 더 비효율적으로 압축하게 될 것입니다. 이때 8비트 PNG 같은 포맷은 완전히 불투명한 타일에만 사용된다는 사실을 기억하십시오. (PNG8 포맷이 투명도를 가진 색상표를 지원할 수는 있지만) 현재 최적 색상표를 계산하기 위해 구현된 중앙값 절단(Median Cut) 알고리즘이 알파 채널을 지원하지 않기 때문입니다. 따라서 PNG8을 선택하는 경우, 완전히 불투명하지 않은 타일은 32비트 PNG로 저장될 것입니다.

타일 작업 스키마
~~~~~~~~~~~~~~~

기본적으로, DB2로 변환 시 (PNG 같은 비손실 타일 포맷을 사용하는 경우) 입력 데이터를 픽셀 및 지리참조 두 수준에서 손실 없이 변환할 수 있는 사용자 지정 타일 작업 스키마를 생성하게 됩니다. 이 타일 작업 스키마는 `gpkg.tile_matrix_set <http://www.geopackage.org/spec/#_tile_matrix_set>`_ 에 있는 타일 원점(*min_x*, *max_y*)이 데이터셋의 좌상단 모서리와 정확히 일치하고, `gpkg.tile_matrix <http://www.geopackage.org/spec/#_tile_matrix>`_ 테이블의 계산된 최대 확대/축소 수준에서 선택된 해상도(*pixel_x_size*, *pixel_y_size*)가 래스터의 픽셀 너비 및 높이와 일치하도록 생성됩니다.

하지만 구현된 다른 기능과 작업 호환을 쉽게 하려면 그리고 DB2를 타일 서비스 소프트웨어와 함께 사용할 수 있도록 하려면, 지구 전체를 커버하는, 사전 정의된 다음과 같은 타일 작업 스키마를 사용할 수도 있습니다:

-  *GoogleCRS84Quad*, `OGC 07-057r7 WMTS 1.0 <http://portal.opengeospatial.org/files/?artifact_id=35326>`_ 사양에서 설명하는 Annex E.3입니다. 이 타일 작업 스키마는 [-180,180] 사이에 있는 경도와 위도 단위의 범위를 가진 EPSG:4326 좌표계의 확대/축소 0수준에서 크기 256x256인 단일 타일로 이루어져 있습니다. 그 결과 확대/축소 0수준에서 해당 타일의 최상단 및 최하단에 있는 라인 64개를 사용하지 않습니다. 이로 인해 몇몇 사양 구현에 문제가 생길 수도 있고, 이 타일 작업 스키마의 정확한 정의가 약간 모호해지기도 합니다. 따라서 이 스키마 대신 InspireCRS84Quad 또는 PseudoTMS_GlobalGeodetic 스키마를 사용하도록 권장합니다.
-  *GoogleMapsCompatible*, WMTS 1.0 사양에서 설명하는 Annex E.4입니다. 이 타일 작업 스키마는 [-20037508.34,20037508.34] 사이에 있는 편동과 편북 단위의 범위를 가진 EPSG:3857 좌표계의 확대/축소 0수준에서 크기 256x256인 단일 타일로 이루어져 있습니다.
-  *InspireCRS84Quad*, as described in `인스파이어 뷰 서비스(Inspire View Services) <http://inspire.ec.europa.eu/documents/Network_Services/TechnicalGuidance_ViewServices_v3.0.pdf>`_ 문서에서 설명하는 이 타일 작업 스키마는 [-180,180] 사이에 있는 경도와 [-90,90] 사이에 있는 위도 단위의 범위를 가진 EPSG:4326 좌표계의 확대/축소 0수준에서 크기 256x256인 타일 2개로 이루어져 있습니다.
-  *PseudoTMS_GlobalGeodetic*, 이 타일 작업 스키마는 OSGeo TMS(Tile Map Service)의 `global-geodetic <http://wiki.osgeo.org/wiki/Tile_Map_Service_Specification#global-geodetic>`_ 프로파일을 기반으로 합니다. 이 스키마는 *InspireCRS84Quad* 타일 작업 스키마와 정확히 동일하게 정의됩니다. 하지만 TMS가 좌하단 모서리를 원점으로 사용하는 반면 DB2는 (WMTS 규범을 준수하도록) 좌상단 모서리를 타일 번호 원점으로 삼기 때문에 TMS와 완전한 작업 호환은 불가능하다는 사실을 기억하십시오.
-  *PseudoTMS_GlobalMercator*, 이 타일 작업 스키마는 OSGeo TMS(Tile Map Service)의 `global-mercator <http://wiki.osgeo.org/wiki/Tile_Map_Service_Specification#global-mercator>`_ 프로파일을 기반으로 합니다. 이 타일 작업 스키마는 [-20037508.34,20037508.34] 사이에 있는 편동과 편북 단위의 범위를 가진 EPSG:3857 좌표계의 확대/축소 0수준에서 크기 256x256인 타일 4개로 이루어져 있습니다. TMS와의 작업 호환성에 대해서는 PseudoTMS_GlobalGeodetic과 동일합니다.

이 모든 사전 정의 타일 작업 스키마에서, 연속되는 확대/축소 수준은 2배수의 해상도만큼씩 달라집니다.

생성 옵션
~~~~~~~~~~~~~~~~

다음과 같은 생성 옵션들을 사용할 수 있습니다:

-  **RASTER_TABLE**\ =string. 사용자 테이블의 이름입니다. 기본적으로 소스 파일명을 기반으로 합니다.
-  **APPEND_SUBDATASET**\ =YES/NO: YES로 설정하면 기존 테이블에 새 내용을 추가할 수 있도록, 사전에 기존 DB2 테이블을 삭제하지 않을 것입니다. 기본값은 NO입니다.
-  **RASTER_IDENTIFIER**\ =string. 사람이 읽을 수 있는 (예: 단축명) 식별자로, *gpkg.contents* 테이블의 *identifier* 열에 삽입됩니다.
-  **RASTER_DESCRIPTION**\ =string. 사람이 읽을 수 있는 설명으로, *gpkg.contents* 테이블의 *description* 열에 삽입됩니다.
-  **BLOCKSIZE**\ =integer. 블록 크기를 픽셀 단위 너비와 높이로 설정합니다. 기본값은 256입니다. 최대 4096까지 지원합니다. 사용자 지정(custom)이 아닌 TILING_SCHEME을 사용하는 경우 설정해서는 안 됩니다.
-  **BLOCKXSIZE**\ =integer. 블록 너비를 픽셀 단위로 설정합니다. 기본값은 256입니다. 최대 4096까지 지원합니다.
-  **BLOCKYSIZE**\ =integer. 블록 높이를 픽셀 단위로 설정합니다. 기본값은 256입니다. 최대 4096까지 지원합니다.
-  **TILE_FORMAT**\ =PNG_JPEG/PNG/PNG8/JPEG/WEBP: 타일을 저장하기 위해 쓰이는 포맷입니다. `타일 포맷 <#tile-formats>`_ 단락을 참조하십시오. 기본값은 PNG_JPEG입니다.
-  **QUALITY**\ =1-100: JPEG 및 WEBP 압축의 품질을 설정합니다. 기본값은 75입니다.
-  **ZLEVEL**\ =1-9: PNG 타일 용 DEFLATE 압축 수준을 설정합니다. 기본값은 6입니다.
-  **DITHER**\ =YES/NO: (TILE_FORMAT=PNG8일 때) 플로이드-스타인버그 디더링(Floyd–Steinberg dithering)을 사용할지 여부를 선택합니다. 기본값은 NO입니다.
-  **TILING_SCHEME**\ =CUSTOM/GoogleCRS84Quad/GoogleMapsCompatible/InspireCRS84Quad/PseudoTMS_GlobalGeodetic/PseudoTMS_GlobalMercator. `타일 작업 스키마 <#tiling-schemes>`_ 단락을 참조하십시오. 기본값은 CUSTOM입니다.
-  **ZOOM_LEVEL_STRATEGY**\ =AUTO/LOWER/UPPER. 확대/축소 수준을 결정할 전략을 선택합니다. TILING_SCHEME이 CUSTOM이 아닌 경우에만 사용합니다. LOWER는 내장되지 않은, 이론적으로 계산된 내장되지 않은 확대/축소 수준 바로 아래의 확대/축소 수준을 선택하고 서브샘플링 작업을 수행할 것입니다. UPPER는 그 반대로 바로 위의 확대/축소 수준을 선택하고 오버샘플링 작업을 수행할 것입니다. 기본값은 가장 가까운 확대/축소 수준을 선택하는 AUTO입니다.
-  **RESAMPLING**\ =NEAREST/BILINEAR/CUBIC/CUBICSPLINE/LANCZOS/MODE/AVERAGE. 리샘플링 알고리즘을 선택합니다. TILING_SCHEME이 CUSTOM이 아닌 경우에만 사용합니다. 기본값은 BILINEAR입니다.

오버뷰
---------

gdaladdo 또는 BuildOverviews()를 사용해서 오버뷰를 계산할 수 있습니다. 기본 GeoPackage 사양을 준수하려면 2의 거듭제곱 오버뷰 인자(2, 4, 8, 16, ...)를 사용해야 합니다. 다른 오버뷰 인자를 사용하면, GDAL 드라이버에서 작동도 하고 `gpkg.zoom_other <http://www.geopackage.org/spec/#extension_zoom_other_intervals>`_ 확장자를 등록도 할 것이지만, 해당 확장자를 지원하지 않는 다른 구현 기능들과 작업 호환이 안 되는 문제를 발생시킬 수도 있습니다.

gdaladdo의 -clean 옵션으로 (또는 BuildOverviews()의 nOverviews=0 파라미터로) 오버뷰를 제거할 수도 있습니다.

메타데이터
---------

GDAL은 표준화된 ```gpkg.metadata`` <http://www.geopackage.org/spec/#_metadata_table>`_ 및 ```gpkg.metadata_reference`` <http://www.geopackage.org/spec/#_metadata_reference_table>`_ 테이블을 사용해서 메타데이터를 읽고 씁니다.

기본 메타데이터 도메인과 아마도 다른 메타데이터 도메인에서 나온 GDAL 메타데이터는 GDAL PAM(Persistent Auxiliary Metadata) .aux.xml 파일에서 쓰이는 서식을 준수하는 단일 XML 문서 안에 나열되고, gpkg.metadata에 md_scope=dataset 및 md_standard_uri=http://gdal.org 로 등록됩니다. gpkg.metadata_reference에서는 이 항목을 reference_scope=table 및 table_name={래스터 테이블의 이름}으로 참조합니다.

*GEOPACKAGE* 메타데이터 도메인을 사용하면 래스터 테이블뿐만 아니라 전체 수준 DB2에 적용되는 메타데이터를 읽고 쓸 수 있습니다.

GDAL에서 나오지 않은 메타데이터의 경우, 이 드라이버는 이를 읽어와서 gpkg.METADATA_ITEM_XXX 형태의 키와 gpkg.metadata 테이블의 *metadata* 열에 있는 값을 사용해서 메타데이터 항목으로 노출시킬 것입니다. 이런 메타데이터를 GDAL 인터페이스를 통해 업데이트하는 기능은 아직 지원하지 않습니다. (하지만 직접 SQL 명령어(Direct SQL Command)를 통해서는 업데이트할 수 있습니다.)

읽기/쓰기에 기본 메타데이터 도메인의 특정 DESCRIPTION 및 IDENTIFIER 메타데이터 항목을 사용하면 gpkg.contents 테이블의 대응하는 각 열을 읽기/업데이트할 수 있습니다.

예시
--------

-  GeoTIFF를 DB2로 단순 변환(translation)합니다. 타일과 함께 'byte' 테이블이 생성될 것입니다.

   ::

      gdal_translate -of DB2ODBC byte.tif DB2ODBC:database=sample;DSN=SAMPLE

-  GeoTIFF를 WebP 타일을 사용하는 DB2로 변환합니다.

   ::

      gdal_translate -of DB2ODBC byte.tif DB2ODBC:database=sample;DSN=SAMPLE -co TILE_FORMAT=WEBP

-  GeoTIFF를 (필요한 경우 재투영 및 리샘플링을 거친) GoogleMapsCompatible 타일 작업 스키마를 사용하는 DB2로 변환합니다.

   ::

      gdal_translate -of DB2ODBC byte.tif DB2ODBC:database=sample;DSN=SAMPLE -co TILING_SCHEME=GoogleMapsCompatible

-  기존 DB2의 오버뷰를 작성합니다.

   ::

      gdaladdo -oo RASTER_TABLE=world -r cubic DB2ODBC:database=sample;DSN=SAMPLE 2 4 8 16 32 64

-  기존 DB2에 새 하위 데이터셋을 추가하고, 래스터 테이블에 기본값이 아닌 이름을 명명합니다.

   ::

      gdal_translate -of DB2ODBC new.tif DB2ODBC:database=sample;DSN=SAMPLE -co APPEND_SUBDATASET=YES -co RASTER_TABLE=new_table

-  입력 데이터셋을 DB2로 재투영합니다.

   ::

      gdalwarp -of DB2ODBC -co RASTER_TABLE=new_table in.tif DB2ODBC:database=sample;DSN=SAMPLE -t_srs EPSG:3857

-  DB2에 있는 특정 래스터 테이블을 엽니다.

   ::

      gdalinfo DB2ODBC:database=sample;DSN=SAMPLE -oo TABLE=a_table

참고
--------

-  :ref:`DB2 벡터 <vector.db2>` 문서 페이지
-  :ref:`PNG 드라이버 <raster.png>` 문서 페이지
-  :ref:`JPEG 드라이버 <raster.jpeg>` 문서 페이지
-  :ref:`WEBP 드라이버 <raster.webp>` 문서 페이지
-  `OGC 07-057r7 WMTS 1.0 <http://portal.opengeospatial.org/files/?artifact_id=35326>`_ 사양
-  `OSGeo TMS (Tile Map Service) <http://wiki.osgeo.org/wiki/Tile_Map_Service_Specification>`_ 사양
