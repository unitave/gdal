.. _raster.esric:

================================================================================
ESRIC -- ESRI 압축 캐시
================================================================================

.. shortname:: ESRIC

.. built_in_by_default::

이 드라이버는 ESRI 압축 캐시(Compact Cache) V2를 단일 래스터로 읽어옵니다.

드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

.. supports_virtualio::

ESRI 압축 캐시 V2
---------------------

`ESRI 압축 캐시 V2 <https://github.com/Esri/raster-tiles-compactcache>`_ 용 판독기입니다. 캐시는 특정 폴더 구조에 위치한 파일 여러 개로 저장됩니다. 이 드라이버의 시점에서 보자면, 캐시의 루트 폴더에 있는 conf.xml이라는 파일이 래스터를 표현합니다. ESRI는 이 XML 파일의 정확한 내용을 완전하게 문서화하지 않았으며, 향후 변경될 수도 있습니다. 이 드라이버는 XML 필드 가운데 래스터를 읽어오는 데 필요한 필드 몇 개만 사용합니다.

사용례
______________

/path/Layers 폴더가 정규 웹 메르카토르 타일 그리드인 V2 포맷의 ESRI 압축 캐시를 담고 있는 경우, 다음 명령어가 2수준 내용을 TIF 파일로 복사할 것입니다.

``gdal_translate -outsize 1024 1024 path/Layers/conf.xml output.tif``

기능과 제한
________________________

-  V2 압축 캐시만 지원합니다. 이 포맷은 conf.xml 파일의 **CacheInfo.TileCacheInfo.StorageFormat** 요소 안에 있는 **esriMapCacheStorageModeCompactV2** 값으로 식별됩니다. 다른 레거시 ESRI 캐시 포맷들은 지원하지 않습니다.

-  256x256 픽셀 크기의 타일을 가진 캐시만 지원합니다. 이 정보는 **CacheInfo.TileCacheInfo.TileRows** 및 **CacheInfo.TileCacheInfo.TileCols** 요소의 값으로 저장됩니다.

-  캐시에 있는 타일은 JPEG과 PNG를 포함하는, 서로 다른 포맷일 수 있습니다. 가장 자주 쓰이는 포맷은 8비트 색상 또는 회색조 JPEG과 불투명도를 지원 또는 비지원하는 색상 PNG입니다. 이런 캐시는 **CacheInfo.TileImageInfo.CacheTileFormat** 요소 안에 **JPEG**, **PNG** 또는 **MIXED** 값을 가지게 될 것입니다. **PNG8** 같은 다른 타일 포맷들은 지원하지 않습니다. 이 드라이버는 소스가 회색조이더라도 래스터를 RGB 또는 RGBA로 승격시킬 것입니다.

-  128x128개의 타일들을 번들 파일로 가지고 있는 캐시만 지원합니다. **CacheInfo.CacheStorageInfo.PacketSize** 요소가 번들에 있는 타일들의 선형 개수(linear number) 값을 담고 있습니다.

-  **CacheInfo.TileCacheInfo.SpatialReference.WKT** 필드로부터 공간 좌표계를 가져옵니다. 이 필드가 없다면, 기본값인 EPSG:4326로 가정합니다.

-  표준 conf.xml 파일에 정의된 대로, 캐시 타일 그리드는 X 및 Y로 구성된 **CacheInfo.TileCacheInfo.TileOrigin**  요소 안에 저장된 원점 위치를 가지고 있습니다. 캐시 크기는 명확하게 정의되지 않았습니다. ESRIC 포맷 드라이버는 참조 좌표계의 (0,0) 좌표를 둘러싼 대칭 영역을 가정할 것입니다. 표준 웹 메르카토르 및 GCS 참조 좌표계의 경우 이 습성이 잘 작동합니다. 하지만 이 가정이 작동하지 않는다면, conf.xml 파일에 **TileOrigin** 과 비슷한 X 및 Y 구성요소에 적절한 값을 가지고 있는 비표준 **CacheInfo.TileCacheInfo.TileEnd** 요소를 추가할 수 있습니다. 그리드 원점 및 크기는 래스터 데이터 범위와 다르다는 사실을 기억하십시오. 예를 들면 데이터가 지구의 아주 작은 한 부분만 커버하더라도, 캐시를 지구 전체를 대상으로 정의된 표준 웹 메르카토르 타일 그리드로 생성하는 경우는 흔합니다.

-  번들형 캐시는 일련의 **CacheInfo.TileCacheInfo.LODInfos.LODInfo** 노드들로 인코딩된 여러 개의 해상도 수준을 가지고 있습니다. **LevelID** 가 **LODInfo** XML 노드를 식별하는데 이때 **LevelID** 는 연속되어야 하며, **Resolution** 에 가장 큰 값을 가진 수준에서 0으로 시작해서 가장 작은 **Resolution** 값을 가진 **LODInfo** 노드를 향해 증가해야 합니다. 이 수준 규범은 예를 들어 WMTS가 사용하는 다른 수준, 행, 열 타일 어드레스 지정 스키마와 비슷합니다. 연속되는 두 수준의 해상도가 2배수로 변화하는 것이 흔한 일이기는 하지만, 이 포맷의 경우 필수는 아닙니다. 각 캐시 수준을 적당한 해상도의 오버뷰로 읽어올 것입니다. 해상도값은 픽셀 당 공간 좌표계 거리 단위입니다.

-  GDAL WMS 드라이버가 지원하는 많은 웹 맵 타일 프로토콜들처럼, 많은 캐시들도 서로 다른 소스로부터 수준 별로(level-by-level) 빌드됩니다. 즉 특정 수준의 내용이 인접 수준과는 다른 소스의 내용일 수도 있고, 또는 특정 수준의 내용이 완전히 누락되었을 수도 있습니다. 이 드라이버는 캐시에 지정한 해상도 수준의 타일이 없는 영역을 읽는 경우, 동일한 위치의 다른 수준에는 데이터가 존재하더라도, 불투명한 검은색을 반환할 것입니다.

-  캐시가 GDAL이 지원하는 최대 크기(어느 차원이든 INT32_MAX)를 초과하는 경우도 있습니다. 이 드라이버는 이런 캐시를 열 때 오류를 발생시킬 것입니다. 래스터 크기가 INT32_MAX밑으로 떨어질 때까지 conf.xml 파일에서 가장 높은 **LevelID** 를 가진 **LODInfo** 노드를 제거하면 해결되지만, 최고 해상도 수준을 읽어오지 못 하게 됩니다.

참고
--------
-  ``gdal/frmts/esric/esric_dataset.cpp`` 로 구현되었습니다.
