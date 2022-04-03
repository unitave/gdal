.. _raster.zarr:

================================================================================
Zarr
================================================================================

.. versionadded:: 3.4

.. shortname:: Zarr

.. build_dependencies:: 기본적으로 빌드인되어 있지만 liblz4, libxz (lzma), libzstd 및 libblosc 등 모든 압축 라이브러리를 포함시킬 것을 강력히 권장합니다.

Zarr란 덩어리진(chunked), 압축된 N차원 배열을 저장하기 위한 포맷입니다. GDAL은 전통적인 2차원 래스터 API 또는 최신 다중 차원 API를 이용해서 이 포맷의 읽기 및 쓰기 접근을 지원합니다.

이 드라이버는 Zarr 버전 2 사양을 지원하며, 현재 개발 중인 Zarr 버전 3 사양도 실험적으로 지원합니다.

읽기 및 쓰기 작업 시 로컬 저장소와 클라우드 저장소를 지원합니다. (:ref:`virtual_file_systems` 참조)

드라이버 케이퍼빌리티
-------------------

.. supports_create::

.. supports_georeferencing::

.. supports_multidimensional::

.. supports_virtualio::

개념
--------

Zarr 데이터셋은 중간(intermediate) 노드들이 그룹(:cpp:class:`GDALGroup`)이고 리프(leaf)들이 배열(:cpp:class:`GDALMDArray`)인, 노드들의 계층 구조(hierarchy)로 이루어져 있습니다.

데이터셋 이름
------------

Zarr 버전 2의 경우, 이 드라이버의 Open() 메소드가 인식하는 데이터셋 이름은 :file:`.zgroup` 파일, :file:`.zarray` 파일 또는 :file:`.zmetadata` 파일(통합 메타데이터)를 담고 있는 디렉터리입니다. 이 드라이버는 데이터셋 발견 시 더 빠른 탐색을 위해 기본적으로 통합 메타데이터를 사용할 것입니다.

Zarr 버전 3의 경우, 이 드라이버의 Open() 메소드가 인식하는 데이터셋 이름은 :file:`zarr.json` 파일(데이터셋의 루트)을 담고 있는 디렉터리입니다.

/vsicurl/ 사용 시 종종 있는 일이지만 파일 목록을 신뢰할 수 없는 파일 시스템 상에 있는 데이터셋의 경우, 디렉터리 이름 앞에 접두어 ``ZARR:`` 를 붙일 수도 있습니다.

압축 메소드
-------------------

GDAL은 물론 `libblosc <https://github.com/Blosc/c-blosc>`_ 가 어떻게 빌드되었느냐에 따라 사용할 수 있는 압축 메소드가 달라집니다.

전체 기능을 포함하도록 빌드했다면 다음과 같이 출력될 것입니다:

::

    $ gdalinfo --format Zarr

    [...]

      Other metadata items:
        COMPRESSORS=blosc,zlib,gzip,lzma,zstd,lz4
        BLOSC_COMPRESSORS=blosclz,lz4,lz4hc,snappy,zlib,zstd

특정 사용례의 경우, :cpp:func:`CPLRegisterCompressor` 및 :cpp:func:`CPLRegisterDecompressor` 로 런타임에 추가 압축기(compressor) 및 압축 해제기(decompressor)를 등록할 수도 있습니다.

XArray _ARRAY_DIMENSIONS
------------------------

이 드라이버는 `XArray <http://xarray.pydata.org/en/stable/generated/xarray.open_zarr.html>`_ 가 배열의 차원 이름을 저장하기 위해 사용하는 ``_ARRAY_DIMENSIONS`` 특수 속성을 지원합니다.

NCZarr 확장 사양
-----------------

이 드라이버는 배열의 차원 이름을 저장하는 `NCZarr 버전 2 <https://www.unidata.ucar.edu/software/netcdf/documentation/NUG/nczarr_head.html>`_ 확장 사양을 지원합니다. (읽기 전용)

공간 좌표계 인코딩
------------

Zarr 사양은 공간 좌표계 인코딩을 위한 어떤 준비도 되어 있지 않습니다. GDAL은 다음 키들 가운데 하나 또는 몇 개를 담고 있을 수도 있는 디렉터리인 ``_CRS`` 속성을 이용합니다.

-  ``url``: OGC 좌표계 URL
-  ``wkt``: 쓰기 작업 시 기본적으로 WKT:2019, 읽기 작업 시 WKT1도 지원
-  ``projjson``

읽기 작업 시, GDAL은 기본적으로 ``url`` 을 사용할 것입니다. ``url`` 을 찾지 못 하는 경우 ``wkt`` 로, 그 다음엔 ``projjson`` 로 돌아갈 것입니다.

.. code-block:: json

    {
      "_CRS":{
        "wkt":"PROJCRS[\"NAD27 \/ UTM zone 11N\",BASEGEOGCRS[\"NAD27\",DATUM[\"North American Datum 1927\",ELLIPSOID[\"Clarke 1866\",6378206.4,294.978698213898,LENGTHUNIT[\"metre\",1]]],PRIMEM[\"Greenwich\",0,ANGLEUNIT[\"degree\",0.0174532925199433]],ID[\"EPSG\",4267]],CONVERSION[\"UTM zone 11N\",METHOD[\"Transverse Mercator\",ID[\"EPSG\",9807]],PARAMETER[\"Latitude of natural origin\",0,ANGLEUNIT[\"degree\",0.0174532925199433],ID[\"EPSG\",8801]],PARAMETER[\"Longitude of natural origin\",-117,ANGLEUNIT[\"degree\",0.0174532925199433],ID[\"EPSG\",8802]],PARAMETER[\"Scale factor at natural origin\",0.9996,SCALEUNIT[\"unity\",1],ID[\"EPSG\",8805]],PARAMETER[\"False easting\",500000,LENGTHUNIT[\"metre\",1],ID[\"EPSG\",8806]],PARAMETER[\"False northing\",0,LENGTHUNIT[\"metre\",1],ID[\"EPSG\",8807]]],CS[Cartesian,2],AXIS[\"easting\",east,ORDER[1],LENGTHUNIT[\"metre\",1]],AXIS[\"northing\",north,ORDER[2],LENGTHUNIT[\"metre\",1]],ID[\"EPSG\",26711]]",

        "projjson":{
          "$schema":"https:\/\/proj.org\/schemas\/v0.2\/projjson.schema.json",
          "type":"ProjectedCRS",
          "name":"NAD27 \/ UTM zone 11N",
          "base_crs":{
            "name":"NAD27",
            "datum":{
              "type":"GeodeticReferenceFrame",
              "name":"North American Datum 1927",
              "ellipsoid":{
                "name":"Clarke 1866",
                "semi_major_axis":6378206.4,
                "inverse_flattening":294.978698213898
              }
            },
            "coordinate_system":{
              "subtype":"ellipsoidal",
              "axis":[
                {
                  "name":"Geodetic latitude",
                  "abbreviation":"Lat",
                  "direction":"north",
                  "unit":"degree"
                },
                {
                  "name":"Geodetic longitude",
                  "abbreviation":"Lon",
                  "direction":"east",
                  "unit":"degree"
                }
              ]
            },
            "id":{
              "authority":"EPSG",
              "code":4267
            }
          },
          "conversion":{
            "name":"UTM zone 11N",
            "method":{
              "name":"Transverse Mercator",
              "id":{
                "authority":"EPSG",
                "code":9807
              }
            },
            "parameters":[
              {
                "name":"Latitude of natural origin",
                "value":0,
                "unit":"degree",
                "id":{
                  "authority":"EPSG",
                  "code":8801
                }
              },
              {
                "name":"Longitude of natural origin",
                "value":-117,
                "unit":"degree",
                "id":{
                  "authority":"EPSG",
                  "code":8802
                }
              },
              {
                "name":"Scale factor at natural origin",
                "value":0.9996,
                "unit":"unity",
                "id":{
                  "authority":"EPSG",
                  "code":8805
                }
              },
              {
                "name":"False easting",
                "value":500000,
                "unit":"metre",
                "id":{
                  "authority":"EPSG",
                  "code":8806
                }
              },
              {
                "name":"False northing",
                "value":0,
                "unit":"metre",
                "id":{
                  "authority":"EPSG",
                  "code":8807
                }
              }
            ]
          },
          "coordinate_system":{
            "subtype":"Cartesian",
            "axis":[
              {
                "name":"Easting",
                "abbreviation":"",
                "direction":"east",
                "unit":"metre"
              },
              {
                "name":"Northing",
                "abbreviation":"",
                "direction":"north",
                "unit":"metre"
              }
            ]
          },
          "id":{
            "authority":"EPSG",
            "code":26711
          }
        },

        "url":"http:\/\/www.opengis.net\/def\/crs\/EPSG\/0\/26711"
      }
    }

대표적인 래스터 API의 독특함
-----------------------------------------

Zarr 데이터셋이 2차원 단일 배열 하나를 담고 있는 경우, 대표적인 래스터 API 사용 시 정규 GDALDataset으로 노출시킬 것입니다.
Zarr 데이터셋이 이런 단일 배열을 하나 이상 담고 있거나 또는 3개 이상의 차원을 가진 배열을 담고 있는 경우, 이 드라이버는 각 배열에 접근하기 위해 그리고/또는 3개 이상의 차원을 가진 배열 안에 있는 2차원 분할(slice)에 접근하기 위해 하위 데이터셋들을 목록화할 것입니다.

열기 옵션
------------

다음 데이터셋 열기 옵션들을 사용할 수 있습니다:

-  **USE_ZMETADATA=YES/NO**: (기본값은 YES)
   .zmetadata 파일로부터 통합 메타데이터를 사용할지 여부를 선택합니다. (Zarr 버전 2 전용)

-  **CACHE_TILE_PRESENCE=YES/NO**: (기본값은 NO)
   존재하는 타일들의 초기 목록화를 수행할지 여부를 선택합니다.
   이 캐시 목록화 작업은 쓰기 권한을 가진 경우 .zarray 또는 .array.json.gmac 파일과 동일한 위치에 저장될 것입니다. 그렇지 않다면 :decl_configoption:`GDAL_PAM_PROXY_DIR` 환경설정 옵션을 이렇게 캐시된 파일을 저장할 기존 디렉터리로 설정해야 합니다. 캐시 목록화 작업이 종료되었다면, 더 이상 열기 옵션을 지정할 필요가 없습니다.
   주의: 이 옵션의 실행 시간은 몇 분, 또는 원격 파일 시스템 상에 저장된 대용량 데이터셋의 경우 더 걸릴 수 있습니다. 그리고 네트워크 파일 시스템의 경우 /vsicurl/ 자체에는 이 옵션이 거의 작동하지 않지만, 전용 디렉터리 목록화 작업을 하고 있는 (/vsis3/, /vsigs/, /vsiaz/ 등과 같은) 좀 더 클라우드 기반인 파일 시스템에는 작동할 것입니다.

멀티스레딩 캐시 작업
----------------------

이 드라이버는 :cpp:func:`GDALMDArray::AdviseRead` 메소드를 구현합니다. 이 메소드는 지정한 관심 영역과 교차하는 타일들을 멀티스레드로 디코딩합니다. 캐시 용량을 충분하게 지정해야만 합니다. 이 메소드 호출은 블록 기반입니다.

다음 옵션들을 메소드에 전송할 수 있습니다:

-  **CACHE_SIZE=value_in_byte**:
   사용할 최대 RAM 용량을 바이트 단위로 지정합니다. 지정하지 않는 경우, 남아 있는 GDAL 블록 캐시 크기의 절반을 사용할 것입니다.

-  **NUM_THREADS=integer or ALL_CPUS**:
   병렬 작업에 사용할 스레드 개수를 지정합니다. 지정하지 않는 경우, :decl_configoption:`GDAL_NUM_THREADS` 환경설정 옵션을 연산에 넣을 것입니다.

생성 옵션
----------------

다음 옵션들은 대표적인 래스터 API의 생성 옵션이거나 (:program:`gdalmdimtranslate` 를 이용해서 접두어 ``ARRAY:`` 를 붙여야만 하는) 다중 차원 API의 배열 수준 생성 옵션입니다:

-  **COMPRESS=[NONE/BLOSC/ZLIB/GZIP/LZMA/ZSTD/LZ4]**:
   압축 메소드를 설정합니다. 기본값은 NONE입니다.

-  **FILTER=[NONE/DELTA]**:
   필터링 메소드를 설정합니다. FORMAT=ZARR_V2인 경우에만 사용할 수 있습니다. 기본값은 NONE입니다.

-  **BLOCKSIZE=string**:
   쉼표로 구분된, 각 차원을 따라 존재하는 덩어리 크기 목록입니다. 이 옵션을 지정하지 않는 경우, 가장 빠르게 변화하는 차원들 (마지막 차원들) 가운데 블록 크기가 샘플 256개인 차원과 블록 크기가 샘플 1개인 차원을 사용합니다.

-  **CHUNK_MEMORY_LAYOUT=C/F**:
   인코딩하는 덩어리에 C순서(행 중심)를 사용할지 또는 F순서(열 중심)를 사용할지를 설정합니다. 압축 옵션을 사용하는 경우에만 유용합니다. 기본값은 C입니다. F로 설정하면 -- 배열 내용에 따라 -- 성능이 향상될 수도 있습니다.

-  **STRING_FORMAT=ASCII/UNICODE**:
   아스키 전용 문자열 또는 유니코드 문자열에 NumPy 유형을 사용할지를 설정합니다. 유니코드 문자열은 문자 하나 당 4바이트가 필요합니다. 기본값은 ASCII입니다.

-  **DIM_SEPARATOR=string**:
   덩어리 파일명에서 차원을 구분하기 위한 구분자를 설정합니다.
   기본값은 Zarr 버전 2의 경우 소수점이고 Zarr 버전 3의 경우 슬래시입니다.

-  **BLOSC_CNAME=bloclz/lz4/lz4hc/snappy/zlib/std**:
   Blosc 압축기 이름을 설정합니다. COMPRESS=BLOSC인 경우에만 사용할 수 있습니다. 기본값은 lz4입니다.

-  **BLOSC_CLEVEL=integer**: [1-9]
   Blosc 압축 수준을 설정합니다. COMPRESS=BLOSC인 경우에만 사용할 수 있습니다. 기본값은 5입니다.

-  **BLOSC_SHUFFLE=NONE/BYTE/BIT**:
   셔플 알고리즘의 유형을 설정합니다. COMPRESS=BLOSC인 경우에만 사용할 수 있습니다. 기본값은 BYTE입니다.

-  **BLOSC_BLOCKSIZE=integer**:
   Blosc 블록 크기를 설정합니다. COMPRESS=BLOSC인 경우에만 사용할 수 있습니다. 기본값은 0입니다.

-  **BLOSC_NUM_THREADS=string**:
   압축에 사용할 작업자 스레드의 개수를 설정합니다. ``ALL_CPUS`` 로도 설정할 수 있습니다. COMPRESS=BLOSC인 경우에만 사용할 수 있습니다. 기본값은 1입니다.

-  **ZLIB_LEVEL=integer**: [1-9]
   ZLib 압축 수준을 설정합니다. COMPRESS=ZLIB인 경우에만 사용할 수 있습니다. 기본값은 6입니다.

-  **GZIP_LEVEL=integer**: [1-9]
   GZip 압축 수준을 설정합니다. COMPRESS=GZIP인 경우에만 사용할 수 있습니다. 기본값은 6입니다.

-  **LZMA_PRESET=integer**: [0-9]
   LZMA 압축 수준을 설정합니다. COMPRESS=LZMA인 경우에만 사용할 수 있습니다. 기본값은 6입니다.

-  **LZMA_DELTA=integer**: 
   델타 거리를 바이트 단위로 설정합니다. COMPRESS=LZMA인 경우에만 사용할 수 있습니다. 기본값은 1입니다.

-  **ZSTD_LEVEL=integer**: [1-9]
   ZSTD 압축 수준을 설정합니다. COMPRESS=ZSTD인 경우에만 사용할 수 있습니다. 기본값은 13입니다.

-  **LZ4_ACCELERATION=integer**: [1-]
   LZ4 가속 인자를 설정합니다. 값이 높을수록 압축 품질이 떨어집니다. COMPRESS=LZ4인 경우에만 사용할 수 있습니다. 기본값은 1(가장 빠름)입니다.

-  **DELTA_DTYPE=string**:
   `NumPy 배열 프로토콜 유형 문자열 (typestr) 서식 <https://numpy.org/doc/stable/reference/arrays.interface.html#arrays-interface>`_ 을 따르는 데이터 유형을 설정합니다.
   엔디언 플래그 접두어(리틀 엔디언의 경우 ``<``, 빅 엔디언의 경우 ``>``)가 붙을 수도 있는 ``u1``, ``i1``, ``u2``, ``i2``, ``u4``, ``i4``, ``u8``, ``i8``, ``f4``, ``f8`` 만 지원합니다.
   FILTER=DELTA인 경우에만 사용할 수 있습니다. 기본값은 네이티브 데이터 유형입니다.


다음 옵션들은 대표적인 래스터 API의 생성 옵션이거나 다중 차원 API의 데이터셋 수준 생성 옵션입니다:

-  **FORMAT=[ZARR_V2/ZARR_V3]**:
   기본값은 ZARR_V2입니다.

-  **CREATE_ZMETADATA=[YES/NO]**:
   통합 메타데이터를 .zmetadata 파일로 생성할지 여부를 선택합니다. (Zarr 버전 2 전용) 기본값은 YES입니다.


다음 옵션들은 대표적인 래스터 API 전용 생성 옵션입니다:

-  **ARRAY_NAME=string**:
   배열 이름을 설정합니다. 지정하지 않는 경우 파일명으로부터 추정합니다.

-  **APPEND_SUBDATASET=YES/NO**:
   새 데이터셋을 기존 Zarr 계층 구조에 추가할지 여부를 선택합니다. 기본값은 NO입니다.


예시
--------

다중 차원 도구를 이용해서 데이터셋 정보를 가져오기:

::

    gdalmdiminfo my.zarr

다중 차원 도구를 이용해서 netCDF 파일을 Zarr로 변환하기:

::

    gdalmdimtranslate in.nc out.zarr -co ARRAY:COMPRESS=GZIP

3차원 배열의 (2차원이 아닌 차원의 0번 색인 위치에 있는) 2차원 분할(slice)을 GeoTIFF로 변환하기:

::

    gdal_translate ZARR:"my.zarr":/group/myarray:0 out.tif


참고
---------

- `Zarr 포맷과 Zarr 포맷의 파이썬 구현 <https://zarr.readthedocs.io/en/stable/>`_

- `(개발 중) Zarr 버전 3 사양 <https://zarr-specs.readthedocs.io/en/core-protocol-v3.0-dev/>`_

