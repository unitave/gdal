.. _raster.isis3:

================================================================================
ISIS3 -- USGS 천체 지질학 ISIS Cube (버전 3)
================================================================================

.. shortname:: ISIS3

.. built_in_by_default::

ISIS3는 USGS 행성 지도 제작(Planetary Cartography) 그룹이 행성 영상 데이터를 저장하고 배포하기 위해 사용하는 포맷입니다. GDAL은 ISIS3 포맷 영상 데이터 읽기, 생성 및 업데이트 접근을 지원합니다.

ISIS3 Cube 파일의 확장자는 거의 .cub이며, 관련 .lbl 라벨 파일을 가지고 있는 경우도 있습니다. .lbl 파일이 존재하는 경우 .cub 파일보다는 .lbl 파일을 데이터셋 이름으로 사용해야 합니다. GDAL 2.2부터 이 드라이버는 개별 GeoTIFF 파일에 저장된 영상도 지원합니다.

또한 거의 모든 ISIS3 영상 환경설정을 지원하기 위해, 이 드라이버는 지리참조와 좌표계 정보는 물론 선택한 다른 헤더 메타데이터도 읽어옵니다.

GDAL 2.2부터, 마스크 밴드가 각 소스 밴드에 추가되었습니다. 픽셀값이 NULL 값, 하위/상위 기기 상 또는 처리된 채도값(low/high on-intstrument/processed saturation value) 가운데 하나, 또는 픽셀값이 무결할 때 255인 경우 이 마스크 밴드의 값은 0입니다.

이 드라이버는 미국 지질조사국(United States Geological Survey)의 지원으로 구현되었습니다.

ISIS3는 PDS와 ISIS2를 포함하는 관련 포맷 패밀리의 일원입니다.

드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::

메타데이터
---------

GDAL 2.2버전부터, ISIS3 라벨을 json:ISIS3 메타데이터 도메인에 있는 순서대로 나열된(serialized) JSON 콘텐츠로 가져올 수 있습니다.

예시:

::

   $ python
   from osgeo import gdal
   ds = gdal.Open('../autotest/gdrivers/data/isis3_detached.lbl')
   print(ds.GetMetadata_List('json:ISIS3')[0])
   {
     "IsisCube":{
       "_type":"object",
       "Core":{
         "_type":"object",
         "StartByte":1,
         "^Core":"isis3_detached.cub",
         "Format":"BandSequential",
         "Dimensions":{
           "_type":"group",
           "Samples":317,
           "Lines":30,
           "Bands":1
         },
         "Pixels":{
           "_type":"group",
           "Type":"UnsignedByte",
           "ByteOrder":"Lsb",
           "Base":0.000000,
           "Multiplier":1.000000
         }
       },
       "Instrument":{
         "_type":"group",
         "TargetName":"Mars"
       },
       "BandBin":{
         "_type":"group",
         "Center":1.000000,
         "OriginalBand":1
       },
       "Mapping":{
         "_type":"group",
         "ProjectionName":"Equirectangular",
         "CenterLongitude":184.412994,
         "TargetName":"Mars",
         "EquatorialRadius":{
           "value":3396190.000000,
           "unit":"meters"
         },
         "PolarRadius":{
           "value":3376200.000000,
           "unit":"meters"
         },
         "LatitudeType":"Planetographic",
         "LongitudeDirection":"PositiveWest",
         "LongitudeDomain":360,
         "MinimumLatitude":-14.822815,
         "MaximumLatitude":-14.727503,
         "MinimumLongitude":184.441132,
         "MaximumLongitude":184.496521,
         "UpperLeftCornerX":-4766.964984,
         "UpperLeftCornerY":-872623.628822,
         "PixelResolution":{
           "value":10.102500,
           "unit":"meters\/pixel"
         },
         "Scale":{
           "value":5864.945312,
           "unit":"pixels\/degree"
         },
         "CenterLatitude":-15.147000,
         "CenterLatitudeRadius":3394813.857978
       }
     },
     "Label":{
       "_type":"object",
       "Bytes":65536,
     },
     "History":{
       "_type":"object",
       "Name":"IsisCube",
       "StartByte":1,
       "Bytes":957,
       "^History":"r0200357_10m_Jul20_o_i3_detatched.History.IsisCube"
     },
     "OriginalLabel":{
       "_type":"object",
       "Name":"IsisCube",
       "StartByte":1,
       "Bytes":2482,
       "^OriginalLabel":"r0200357_10m_Jul20_o_i3_detatched.OriginalLabel.IsisCube"
     }
   }

또는

::

   $ gdalinfo -json ../autotest/gdrivers/data/isis3_detached.lbl -mdd all

생성 시, "json:ISIS3" 메타데이터 도메인에 있는 SetMetadata() 인터페이스에 소스 템플릿 라벨을 전송할 수 있습니다.

생성 지원
----------------

GDAL 2.2버전부터, ISIS3 드라이버는 CreateCopy() 및 Create() 인터페이스를 통해 기존 데이터셋의 영상 업데이트 및 새 데이터셋 생성을 지원합니다.

gdal_translate 또는 gdalwarp로 CreateCopy() 사용 시, ISIS3를 ISIS3로 변환하는 경우 원본 라벨을 가능한 한 보전하려고 노력할 것입니다. USE_SRC_LABEL 생성 옵션을 NO로 설정하면 이 습성을 비활성화시킬 수 있습니다.

다음 생성 옵션들을 사용할 수 있습니다:

-  **DATA_LOCATION=LABEL/EXTERNAL/GEOTIFF**:
   픽셀 데이터의 위치를 지정합니다. 기본값은 LABEL로, 예를 들면 영상이 라벨 바로 뒤에 온다는 뜻입니다. EXTERNAL로 설정하면, 주 파일명과 .cub 확장자를 가진 RAW 파일에 영상을 넣습니다. GEOTIFF로 설정하면 주 파일명과 .tif 확장자를 가진 개별 GeoTIFF 파일에 영상을 넣습니다.

-  **GEOTIFF_AS_REGULAR_EXTERNAL=YES/NO**:
   GeoTIFF 파일이 비압축 파일인 경우, GeoTIFF 파일을 정규 RAW 파일로 등록할지 여부를 선택합니다. 기본값은 YES로, ISIS3 드라이버의 예전 버전과의 호환성을 극대화시킵니다.

-  **GEOTIFF_OPTIONS=string**:
   GeoTIFF 드라이버로 전송할 쉼표로 구분된 KEY=VALUE 투플(tuple) 목록입니다.
   GEOTIFF_OPTIONS=COMPRESS=LZW처럼 설정합니다.

-  **EXTERNAL_FILENAME=filename**:
   기본 외부 파일명을 대체합니다. DATA_LOCATION 생성 옵션을 EXTERNAL 또는 GEOTIFF로 설정한 경우에만 사용할 수 있습니다.

-  **TILED=YES/NO**:
   픽셀 데이터를 타일화해야 할지 여부를 선택합니다. 기본값은 NO입니다. (예: BSQ(Band-Sequential) 구조)

-  **BLOCKXSIZE=int_value**:
   타일 너비를 픽셀 단위로 설정합니다. TILED=YES를 설정한 경우에만 사용할 수 있습니다. 기본값은 256입니다.

-  **BLOCKYSIZE=int_value**:
   타일 높이를 픽셀 단위로 설정합니다. TILED=YES를 설정한 경우에만 사용할 수 있습니다. 기본값은 256입니다.

-  **COMMENT=string**:
   라벨에 추가할 주석입니다.

-  **LATITUDE_TYPE=Planetocentric/Planetographic**:
   Mapping.LatitudeType의 값을 설정합니다. 기본값은 Planetocentric(행성 중심)입니다. USE_SRC_MAPPING=YES를 설정하고 이 옵션을 설정하는 경우, 소스 LatitudeType을 대체하기 위해 이 옵션을 연산에 넣을 것입니다.

-  **LONGITUDE_DIRECTION=PositiveEast/PositiveWest**:
   Mapping.LongitudeDirection의 값을 설정합니다. 기본값은 PositiveEast입니다. USE_SRC_MAPPING=YES를 설정하고 이 옵션을 설정하는 경우, 소스 LongitudeDirection을 대체하기 위해 이 옵션을 연산에 넣을 것입니다.

-  **TARGET_NAME=string**:
   Mapping.TargetName의 값을 설정합니다. 일반적으로는 공간 좌표계 원점(datum) 이름으로부터 추정하는 값입니다. USE_SRC_MAPPING=YES를 설정하고 이 옵션을 설정하는 경우, 소스 TargetName을 대체하기 위해 이 옵션을 연산에 넣을 것입니다.

-  **FORCE_360=YES/NO**:
   경도 범위를 강제로 [0, 360] 범위로 할지 여부를 선택합니다. 기본값은 NO입니다.

-  **WRITE_BOUNDING_DEGREES=YES/NO**:
   long 데이터 유형 최소/최대 위도 값을 작성할지 여부를 선택합니다. 기본값은 YES입니다.

-  **BOUNDING_DEGREES=min_long,min_lat,max_long,max_lat**:
   경계 상자(bounding box)를 직접 설정합니다. (LONGITUDE_DIRECTION 또는 FORCE_360 생성 옵션은 이 값들을 수정하지 않을 것입니다.)

-  **USE_SRC_LABEL=YES/NO**:
   ISIS3를 ISIS3로 변환하는 작업에 소스 라벨을 사용할지 여부를 선택합니다. 기본값은 YES입니다.

-  **USE_SRC_MAPPING=YES/NO**:
   ISIS3를 ISIS3로 변환하는 작업에 소스 라벨로부터 나온 매핑 그룹을 사용할지 여부를 선택합니다. 기본값은 NO입니다. (즉 새 데이터셋의 지리변형 및 투영법으로부터 매핑 그룹의 내용을 생성할 것이라는 뜻입니다.)
   USE_SRC_LABEL=YES를 설정한 경우에만 사용할 수 있습니다.

-  **USE_SRC_HISTORY=YES/NO**:
   ISIS3를 ISIS3로 변환하는 작업에서 새 데이터셋에 소스 이력 객체가 가리키는 내용을 작성할지 여부를 선택합니다. 기본값은 YES입니다. USE_SRC_LABEL=YES를 설정한 경우에만 사용할 수 있습니다.
   ADD_GDAL_HISTORY와 USE_SRC_HISTORY를 둘 다 YES로 설정한 경우 (또는 둘 다 사용하지 않는 경우) 기존 이력에 새 이력 부분을 추가할 것입니다.

-  **ADD_GDAL_HISTORY=YES/NO**:
   ISIS3를 ISIS3로 변환하는 작업에서 이력 객체가 가리키는 내용에 GDAL 특화 이력을 추가할지 여부를 선택합니다. 기본값은 YES입니다. USE_SRC_LABEL=YES를 설정한 경우에만 사용할 수 있습니다.
   ADD_GDAL_HISTORY와 USE_SRC_HISTORY를 둘 다 YES로 설정한 경우 (또는 둘 다 사용하지 않는 경우) 기존 이력에 새 이력 부분을 추가할 것입니다.
   ADD_GDAL_HISTORY=YES를 설정하면, 일반적으로 현재 GDAL 버전, 바이너리 이름 및 경로, 호스트명, 사용자명 그리고 소스 및 대상 파일명으로부터 이력을 구성합니다. GDAL_HISTORY 생성 옵션을 지정하면 이 옵션을 완전히 무시할 수 있습니다.

-  **GDAL_HISTORY=string**:
   GDAL 이력을 직접 정의합니다. ISIS3 PDL 서식으로 작성해야만 합니다. 이 옵션을 지정하지 않는 경우, 자동으로 구성합니다. ADD_GDAL_HISTORY=YES를 설정한 경우에만 (또는 사용하지 않는 경우에만) 이 옵션을 사용할 수 있습니다.

예시
--------

GDAL 파이썬을 이용해서 IsisCube.Mapping 그룹의 파라미터를 수정하면서 소스 ISIS3 데이터셋의 복사본을 또다른 ISIS3 데이터셋으로 생성하는 방법:

::

   import json
   from osgeo import gdal

   src_ds = gdal.Open('in.lbl')
   # Load source label as JSon
   label = json.loads( src_ds.GetMetadata_List('json:ISIS3')[0] )
   # Update parameter
   label["IsisCube"]["Mapping"]["TargetName"] = "Moon"

   # Instantiate new raster
   # Note the USE_SRC_MAPPING=YES creation option, since we modified the
   # IsisCube.Mapping section, which otherwise is completely rewritten from
   # the geotransform and projection attached to the output dataset.
   out_ds = gdal.GetDriverByName('ISIS3').Create('out.lbl',
                                                 src_ds.RasterXSize,
                                                 src_ds.RasterYSize,
                                                 src_ds.RasterCount,
                                                 src_ds.GetRasterBand(1).DataType,
                                                 options = ['USE_SRC_MAPPING=YES'])
   # Attach the modified label
   out_ds.SetMetadata( [json.dumps(label)], 'json:ISIS3' )

   # Copy imagery (assumes that each band fits into memory, otherwise a line-by
   # line or block-per-block strategy would be more appropriate )
   for i in range(src_ds.RasterCount):
       out_ds.GetRasterBand(1).WriteRaster( 0, 0,
                                           src_ds.RasterXSize,
                                           src_ds.RasterYSize,
                                           src_ds.GetRasterBand(1).ReadRaster() )
   out_ds = None
   src_ds = None

참고
--------

-  ``gdal/frmts/pds/isis3dataset.cpp`` 로 구현되었습니다.
-  :ref:`raster.pds` 드라이버
-  :ref:`raster.isis2` 드라이버
