.. _raster.sentinel2:

================================================================================
SENTINEL2 -- 센티널-2 상품
================================================================================

.. shortname:: SENTINEL2

.. built_in_by_default::

센티널-2 1B수준, 1C수준 및 2A수준 상품 용 드라이버입니다.
GDAL 2.1.3버전부터, "안전 밀집(Safe Compact)" 인코딩된 1C수준도 지원합니다.

센티널-2 데이터 상품의 루트에 있는 (일반적으로 S2A_OPER_MTD_SAFL1C\_....xml 같은 이름의) 주 메타데이터 .xml 파일을 열면 SENTINEL2 드라이버를 사용할 것입니다. 이 드라이버는 `센티널 과학 데이터 허브 <https://scihub.copernicus.eu/>`_ 에서 다운로드한 .zip 파일도 직접 입력받을 수 있습니다.

영상을 읽을 수 있으려면, GDAL을 JPEG2000 호환 드라이버 가운데 최소한 하나로 환경설정해야만 합니다.

가시광 및 근적외선(VNIR) 그리고 단파장 적외선(SWIR) 영역에 있는 스펙트럼 밴드 13개 상에서 센티널-2 데이터를 수집합니다. 다음은 그 13개 밴드를 설명하는 표입니다:

========= ============== ======================= =============== ===================
밴드 이름 해상도 (m)     중심 파장 (nm)          밴드 너비 (nm)  목적
========= ============== ======================= =============== ===================
B01       60             443                     20              에어로졸 탐지
B02       10             490                     65              청색
B03       10             560                     35              녹색
B04       10             665                     30              적색
B05       20             705                     15              식생 범주화
B06       20             740                     15              식생 범주화
B07       20             783                     20              식생 범주화
B08       10             842                     115             근적외선
B08A      20             865                     20              식생 범주화
B09       60             945                     20              수증기
B10       60             1375                    30              권운(cirrus)
B11       20             1610                    90              눈/얼음/구름 구별
B12       20             2190                    180             눈/얼음/구름 구별
========= ============== ======================= =============== ===================

드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

.. supports_virtualio::

1B수준
--------

1B수준 상품은 센서 도형으로 되어 있는 (예: 정사보정되지 않은) 최대 25km의 트랙 횡축(across-track) x 최대 23km의 트랙 종축(along-track) 크기의 입상(粒狀; granule) 몇 개로 이루어져 있습니다. 각 입상은 트랙 종축 방향으로 배치된 탐지기 12개 가운데 하나가 촬영한 영상에 대응합니다. (즉 관측 영역(swath) 너비가 총 290km라는 의미입니다.) 각 밴드의 영상은 개별 JPEG2000 파일로 저장됩니다.

1B수준 상품은 고급 사용자 용입니다.

주 메타데이터 .xml 파일을 열면, 일반적으로 드라이버가 하위 데이터셋 N x 3개를 노출시킬 것입니다. 이때 N은 사용자 상품을 구성하는 입상의 개수이고 3은 공간 해상도 개수에 대응합니다. 10m 밴드 4개의 공간 해상도, 20m 밴드 6개의 공간 해상도, 그리고 60m 밴드 3개의 공간 해상도가 있습니다.
주의할 점: 이런 하위 데이터셋들의 개수는 일반적으로 수백 개 이상이 될 수 있습니다.

지정한 입상의 메타데이터 .xml 파일을 열 수도 있습니다. 이 경우 공간 해상도 3개 각각에 대한 하위 데이터셋 3개를 리포트할 것입니다.

하위 데이터셋을 여는 경우, 지상 기준점(GCP) 5개로 -- 이미지 모서리 4개와 중심 1개로 -- 지리참조 작업합니다.

1C수준
--------

1C수준 상품은 UTM WGS84 투영법으로 되어 있는 100km x 100km 크기의 정사보정 타일들로 구성되어 있습니다. 각 밴드의 영상은 개별 JPEG2000 파일로 저장됩니다.

주 메타데이터 .xml 파일을 열면, 일반적으로 드라이버가 다음 하위 데이터셋 4개를 노출시킬 것입니다:

-  10m 밴드 4개
-  20m 밴드 6개
-  60m 밴드 3개
-  R, G, B 밴드의 320m 해상도 수준 미리보기

동일한 해상도와 투영법을 가진 타일 모두를 함께 모자이크할 것입니다. 상품이 UTM 구역 여러 개에 걸쳐 있는 경우, 각 구역을 개별 하위 데이터셋으로 노출시킬 것입니다.

각 타일의 메타데이터 .xml 파일을 열 수도 있습니다. (원본 1C수준 인코딩인 경우만, "안전 밀집(Safe Compact)" 인코딩은 지원하지 않습니다.) 이 경우 일반적으로 드라이버가 앞에서 언급한 하위 데이터셋 유형 4개를 노출시킬 것입니다.

2A수준
--------

1C수준과 마찬가지로, 2A수준 상품도 UTM WGS84 투영법으로 되어 있는 100km x 100km 크기의 정사보정 타일들로 구성되어 있습니다. 각 밴드의 영상은 개별 JPEG2000 파일로 저장됩니다. 대기층 바닥(Bottom-Of-Atmosphere; BOA) 반사율을 값으로 가지고 있습니다. 다음과 같은 2A수준 특화 밴드도 계산합니다:

-  AOT: 에어로졸 광학 두께(Aerosol Optical Thickness) 맵 (550nm 파장)
-  CLD: 높은 신뢰도의 맑은 하늘인 0에서 높은 신뢰도의 흐린 하늘인 100 사이 범위의 래스터 마스크 값
-  SCL: 신(scene) 범주화. 밴드의 카테고리 이름이 값들의 의미를 나타냅니다.
-  SNW: 높은 신뢰도의 눈/얼음 없음인 0에서 높은 신뢰도의 눈/얼음 있음인 100 사이 범위의 래스터 마스크 값
-  WVP: 신(scene) 평균 수증기 맵

주 메타데이터 .xml 파일을 열면, 일반적으로 드라이버가 다음 하위 데이터셋 4개를 노출시킬 것입니다:

-  네이티브 10m 밴드 4개와 2A수준 특화 밴드들 (AOT 및 WVP)
-  네이티브 20m 밴드 6개, B08 밴드를 제외하고 20m로 리샘플링된 10m 밴드들, 그리고 2A수준 특화 밴드들 (AOT, WVP, SCL, CLD 및 SNW)
-  네이티브 60m 밴드 3개, B08 밴드를 제외하고 60m로 리샘플링된 10m 및 20m 밴드들그리고 2A수준 특화 밴드들 (AOT, WVP, SCL, CLD 및 SNW)
-  R, G, B 밴드의 320m 해상도 수준 미리보기

동일한 해상도와 투영법을 가진 타일 모두를 함께 모자이크할 것입니다. 상품이 UTM 구역 여러 개에 걸쳐 있는 경우, 각 구역을 개별 하위 데이터셋으로 노출시킬 것입니다.

메타데이터
---------

일반 메타데이터 도메인에서 주 메타데이터 .xml 파일의 메타데이터를 사용할 수 있습니다. xml:SENTINEL2 메타데이터 도메인을 통해 전체 XML 파일에도 접근할 수 있습니다.

하위 데이터셋은 VRT 포맷 기반이기 때문에, xml:VRT 메타데이터 도메인을 쿼리하면 이 VRT의 정의를 수집할 수 있습니다.

1C수준 및 2A수준의 성능 문제점
----------------------------------

센티널-2 상품 구조 방식 때문에, 특히 사용된 JPEG2000 파일의 개수 때문에, 많은 타일로 이루어진 상품의 경우 축소(zoom-out) 작업이 아주 느릴 수 있습니다. 따라서 대화형 디스플레이를 위한 오버뷰를 생성하는 것이 유용할 수 있습니다. (오버뷰 생성 자체도 시간이 걸릴 수 있습니다.) gdaladdo 유틸리티를 하위 데이터셋 이름과 함께 실행하면 됩니다. 이 오버뷰 파일은 주 메타데이터 .xml 파일 옆에 같은 이름으로 생성되지만, XX가 10m, 20m, 60m 또는 PREVIEW이고 YYYYY가 EPSG 코드인 접미어 \_XX_EPSG_YYYYY.tif.ovr가 .xml 파일의 기본명 뒤에 붙습니다.

요령: 사용례에서 축소(zoom-out) 미리보기의 내용이 중요하지 않은 경우, NONE 리샘플링 메소드를 이용해서 (gdaladdo의 '-r none' 스위치) 비어 있는 오버뷰를 즉석에서 생성할 수 있습니다.

JP2OpenJPEG 드라이버를 이용해서 하위 데이터셋을 타일화 GeoTIFF 같은 또다른 포맷으로 변환할 때, :decl_configoption:`GDAL_CACHEMAX` 환경설정 옵션의 권장 최소값은 INTERLEAVE=BAND GeoTIFF를 생성하는 경우 (subdataset_width \* 2048 \* 2 ) / 10000000이고, 또는 기본 INTERLEAVE=PIXEL 환경설정인 경우 이 값을 밴드 개수로 곱한 값입니다. OpenJPEG 라이브러리 현재 버전도 JPEG2000 타일을 디코딩하는 데 많은 메모리를 (600MB까지) 사용하기 때문에, 메모리가 부족할 경우 :decl_configoption:`GDAL_NUM_THREADS` 환경설정 옵션을 적당한 스레드 개수로 지정하는 편이 좋을 수도 있습니다. (이 환경설정 옵션의 기본값은 가상 CPU의 총 개수입니다.)

열기 옵션
------------

이 드라이버는 다음 열기 옵션을 전송할 수 있습니다:

-  **ALPHA=YES/NO**:
   알파 밴드를 노출시킬지 여부를 선택합니다. 기본값은 NO입니다.
   YES로 설정하는 경우, 센티널-2 밴드들 뒤에 알파 채널을 가진 추가 밴드를 추가합니다. 알파 밴드의 값은:

   -  타일이 없는 영역 또는 타일 데이터가 NODATA 또는 SATURATED 특수 값으로 설정된 경우 0,
   -  무결한 데이터를 가진 영역은 4095입니다.

주의: 이 열기 옵션 앞에 SENTINEL2\_ 접두어를 붙이면 (예: SENTINEL2_ALPHA) 환경설정 옵션으로도 지정할 수 있습니다.

예시
--------

-  센티널-2 상품의 주 메타데이터 파일 열기:

   ::

      $ gdalinfo S2A_OPER_MTD_SAFL1C_PDMC_20150818T101440_R022_V20150813T102406_20150813T102406.xml

   ::

      Driver: SENTINEL2/Sentinel 2
      Files: S2A_OPER_MTD_SAFL1C_PDMC_20150818T101440_R022_V20150813T102406_20150813T102406.xml
      Size is 512, 512
      Coordinate System is `'
      Metadata:
        CLOUD_COVERAGE_ASSESSMENT=0.0
        DATATAKE_1_DATATAKE_SENSING_START=2015-08-13T10:10:26.027Z
        DATATAKE_1_DATATAKE_TYPE=INS-NOBS
        DATATAKE_1_ID=GS2A_20150813T101026_000734_N01.03
        DATATAKE_1_SENSING_ORBIT_DIRECTION=DESCENDING
        DATATAKE_1_SENSING_ORBIT_NUMBER=22
        DATATAKE_1_SPACECRAFT_NAME=Sentinel-2A
        DEGRADED_ANC_DATA_PERCENTAGE=0
        DEGRADED_MSI_DATA_PERCENTAGE=0
        FOOTPRINT=POLYGON((11.583573986577191 46.02490454425771, 11.538730738326866 45.03757398414644, 12.93007028286133 44.99812645604949, 12.999359413660665 45.98408391203724, 11.583573986577191 46.02490454425771, 11.583573986577191 46.02490454425771))
        FORMAT_CORRECTNESS_FLAG=PASSED
        GENERAL_QUALITY_FLAG=PASSED
        GENERATION_TIME=2015-08-18T10:14:40.000283Z
        GEOMETRIC_QUALITY_FLAG=PASSED
        PREVIEW_GEO_INFO=BrowseImageFootprint
        PREVIEW_IMAGE_URL=https://pdmcdam2.sentinel2.eo.esa.int/s2pdgs_geoserver/geo_service.php?service=WMS&version=1.1.0&request=GetMap&layers=S2A_A000022_N0103:S2A_A000022_N0103&styles=&bbox=11.538730738326866,44.99812645604949,12.999359413660665,46.02490454425771&width=1579&height=330&srs=EPSG:4326&format=image/png&time=2015-08-13T10:24:06.0Z/2015-08-13T10:24:06.0Z
        PROCESSING_BASELINE=01.03
        PROCESSING_LEVEL=Level-1C
        PRODUCT_START_TIME=2015-08-13T10:24:06.637Z
        PRODUCT_STOP_TIME=2015-08-13T10:24:06.637Z
        PRODUCT_TYPE=S2MSI1C
        QUANTIFICATION_VALUE=1000
        RADIOMETRIC_QUALITY_FLAG=PASSED
        REFERENCE_BAND=B1
        REFLECTANCE_CONVERSION_U=0.973195961910065
        SENSOR_QUALITY_FLAG=PASSED
        SPECIAL_VALUE_NODATA=1
        SPECIAL_VALUE_SATURATED=0
      Subdatasets:
        SUBDATASET_1_NAME=SENTINEL2_L1C:S2A_OPER_MTD_SAFL1C_PDMC_20150818T101440_R022_V20150813T102406_20150813T102406.xml:10m:EPSG_32632
        SUBDATASET_1_DESC=Bands B2, B3, B4, B8 with 10m resolution, UTM 32N
        SUBDATASET_2_NAME=SENTINEL2_L1C:S2A_OPER_MTD_SAFL1C_PDMC_20150818T101440_R022_V20150813T102406_20150813T102406.xml:20m:EPSG_32632
        SUBDATASET_2_DESC=Bands B5, B6, B7, B8A, B11, B12 with 20m resolution, UTM 32N
        SUBDATASET_3_NAME=SENTINEL2_L1C:S2A_OPER_MTD_SAFL1C_PDMC_20150818T101440_R022_V20150813T102406_20150813T102406.xml:60m:EPSG_32632
        SUBDATASET_3_DESC=Bands B1, B9, B10 with 60m resolution, UTM 32N
        SUBDATASET_4_NAME=SENTINEL2_L1C:S2A_OPER_MTD_SAFL1C_PDMC_20150818T101440_R022_V20150813T102406_20150813T102406.xml:PREVIEW:EPSG_32632
        SUBDATASET_4_DESC=RGB preview, UTM 32N
      Corner Coordinates:
      Upper Left  (    0.0,    0.0)
      Lower Left  (    0.0,  512.0)
      Upper Right (  512.0,    0.0)
      Lower Right (  512.0,  512.0)
      Center      (  256.0,  256.0)

-  .zip 파일을 직접 열기:

   ::

      $ gdalinfo S2A_OPER_PRD_MSIL1C_PDMC_20150818T101440_R022_V20150813T102406_20150813T102406.zip

-  1C수준 하위 데이터셋의 10m 해상도 밴드들을 열기:

   ::

      $ gdalinfo SENTINEL2_L1C:S2A_OPER_MTD_SAFL1C_PDMC_20150818T101440_R022_V20150813T102406_20150813T102406.xml:10m:EPSG_32632

   ::

      Driver: SENTINEL2/Sentinel 2
      Files: S2A_OPER_MTD_SAFL1C_PDMC_20150818T101440_R022_V20150813T102406_20150813T102406.xml
             ./GRANULE/S2A_OPER_MSI_L1C_TL_MTI__20150813T201603_A000734_T32TQR_N01.03/S2A_OPER_MTD_L1C_TL_MTI__20150813T201603_A000734_T32TQR.xml
             ./GRANULE/S2A_OPER_MSI_L1C_TL_MTI__20150813T201603_A000734_T32TQR_N01.03/IMG_DATA/S2A_OPER_MSI_L1C_TL_MTI__20150813T201603_A000734_T32TQR_B04.jp2
             ./GRANULE/S2A_OPER_MSI_L1C_TL_MTI__20150813T201603_A000734_T32TQR_N01.03/IMG_DATA/S2A_OPER_MSI_L1C_TL_MTI__20150813T201603_A000734_T32TQR_B03.jp2
             ./GRANULE/S2A_OPER_MSI_L1C_TL_MTI__20150813T201603_A000734_T32TQR_N01.03/IMG_DATA/S2A_OPER_MSI_L1C_TL_MTI__20150813T201603_A000734_T32TQR_B02.jp2
             ./GRANULE/S2A_OPER_MSI_L1C_TL_MTI__20150813T201603_A000734_T32TQR_N01.03/IMG_DATA/S2A_OPER_MSI_L1C_TL_MTI__20150813T201603_A000734_T32TQR_B08.jp2
      Size is 10980, 10980
      Coordinate System is:
      PROJCS["WGS 84 / UTM zone 32N",
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
          PROJECTION["Transverse_Mercator"],
          PARAMETER["latitude_of_origin",0],
          PARAMETER["central_meridian",9],
          PARAMETER["scale_factor",0.9996],
          PARAMETER["false_easting",500000],
          PARAMETER["false_northing",0],
          UNIT["metre",1,
              AUTHORITY["EPSG","9001"]],
          AXIS["Easting",EAST],
          AXIS["Northing",NORTH],
          AUTHORITY["EPSG","32632"]]
      Origin = (699960.000000000000000,5100060.000000000000000)
      Pixel Size = (10.000000000000000,-10.000000000000000)
      Metadata:
      [... same as above ...]
      Image Structure Metadata:
        COMPRESSION=JPEG2000
      Corner Coordinates:
      Upper Left  (  699960.000, 5100060.000) ( 11d35' 0.87"E, 46d 1'29.66"N)
      Lower Left  (  699960.000, 4990260.000) ( 11d32'19.43"E, 45d 2'15.27"N)
      Upper Right (  809760.000, 5100060.000) ( 12d59'57.69"E, 45d59' 2.70"N)
      Lower Right (  809760.000, 4990260.000) ( 12d55'48.25"E, 44d59'53.26"N)
      Center      (  754860.000, 5045160.000) ( 12d15'46.56"E, 45d30'48.07"N)
      Band 1 Block=128x128 Type=UInt16, ColorInterp=Red
        Description = B4, central wavelength 665 nm
        Overviews: 5490x5490, 2745x2745, 1373x1373, 687x687, 344x344
        Metadata:
          BANDNAME=B4
          BANDWIDTH=30
          BANDWIDTH_UNIT=nm
          SOLAR_IRRADIANCE=1512.79
          SOLAR_IRRADIANCE_UNIT=W/m2/um
          WAVELENGTH=665
          WAVELENGTH_UNIT=nm
        Image Structure Metadata:
          NBITS=12
      Band 2 Block=128x128 Type=UInt16, ColorInterp=Green
        Description = B3, central wavelength 560 nm
      [...]
      Band 3 Block=128x128 Type=UInt16, ColorInterp=Blue
        Description = B2, central wavelength 490 nm
      [...]
      Band 4 Block=128x128 Type=UInt16, ColorInterp=Undefined
        Description = B8, central wavelength 842 nm
      [...]

-  1C수준 하위 데이터셋을 타일화 GeoTIFF로 변환하기

   ::

      $ gdal_translate SENTINEL2_L1C:S2A_OPER_MTD_SAFL1C_PDMC_20150818T101440_R022_V20150813T102406_20150813T102406.xml:10m:EPSG_32632 \
                       10m.tif \
                       -co TILED=YES --config GDAL_CACHEMAX 1000 --config GDAL_NUM_THREADS 2

-  1C수준 하위 데이터셋에 비어 있는 오버뷰를 생성하기:

   ::

      $ gdaladdo -r NONE SENTINEL2_L1C:S2A_OPER_MTD_SAFL1C_PDMC_20150818T101440_R022_V20150813T102406_20150813T102406.xml:10m:EPSG_32632 4

-  하위 데이터셋으로부터 VRT 파일을 생성하기 (하위 데이터셋을 파일로 가지고 있으면 편리할 수 있습니다):

   ::

      $ python -c "import sys; from osgeo import gdal; ds = gdal.Open(sys.argv[1]); open(sys.argv[2], 'wb').write(ds.GetMetadata('xml:VRT')[0].encode('utf-8'))" \
               SENTINEL2_L1C:S2A_OPER_MTD_SAFL1C_PDMC_20150818T101440_R022_V20150813T102406_20150813T102406.xml:10m:EPSG_32632 10m.vrt

-  1B수준 하위 데이터셋의 10m 해상도 밴드들을 열기:

   ::

      $ gdalinfo SENTINEL2_L1B:S2A_OPER_MTD_L1B_GR_SGS__20151024T023555_S20151024T011315_D02.xml:10m

   ::

      Driver: SENTINEL2/Sentinel 2
      Files: S2A_OPER_MTD_L1B_GR_SGS__20151024T023555_S20151024T011315_D02.xml
             IMG_DATA/S2A_OPER_MSI_L1B_GR_SGS__20151024T023555_S20151024T011315_D02_B04.jp2
             IMG_DATA/S2A_OPER_MSI_L1B_GR_SGS__20151024T023555_S20151024T011315_D02_B03.jp2
             IMG_DATA/S2A_OPER_MSI_L1B_GR_SGS__20151024T023555_S20151024T011315_D02_B02.jp2
             IMG_DATA/S2A_OPER_MSI_L1B_GR_SGS__20151024T023555_S20151024T011315_D02_B08.jp2
      Size is 2552, 2304
      Coordinate System is `'
      GCP Projection =
      GEOGCS["WGS 84",
          DATUM["WGS_1984",
              SPHEROID["WGS 84",6378137,298.257223563,
                  AUTHORITY["EPSG","7030"]],
              AUTHORITY["EPSG","6326"]],
          PRIMEM["Greenwich",0,
              AUTHORITY["EPSG","8901"]],
          UNIT["degree",0.0174532925199433,
              AUTHORITY["EPSG","9122"]],
          AUTHORITY["EPSG","4326"]]
      GCP[  0]: Id=, Info=
                (0,0) -> (134.635194391036,-21.4282083310724,0)
      GCP[  1]: Id=, Info=
                (0,2304) -> (134.581480136827,-21.6408640426055,0)
      GCP[  2]: Id=, Info=
                (2552,2304) -> (134.833308274251,-21.686125031254,0)
      GCP[  3]: Id=, Info=
                (2552,0) -> (134.886750925145,-21.4734274382519,0)
      GCP[  4]: Id=, Info=
                (1276,1152) -> (134.734115530986,-21.5571457404287,0)
      Metadata:
        CLOUDY_PIXEL_PERCENTAGE=0
        DATASTRIP_ID=S2A_OPER_MSI_L1B_DS_SGS__20151024T023555_S20151024T011312_N01.04
        DATATAKE_1_DATATAKE_SENSING_START=2015-10-24T01:13:12.027Z
        DATATAKE_1_DATATAKE_TYPE=INS-NOBS
        DATATAKE_1_ID=GS2A_20151024T011312_001758_N01.04
        DATATAKE_1_SENSING_ORBIT_DIRECTION=DESCENDING
        DATATAKE_1_SENSING_ORBIT_NUMBER=45
        DATATAKE_1_SPACECRAFT_NAME=Sentinel-2A
        DEGRADED_ANC_DATA_PERCENTAGE=0
        DEGRADED_MSI_DATA_PERCENTAGE=0
        DETECTOR_ID=02
        DOWNLINK_PRIORITY=NOMINAL
        FOOTPRINT=POLYGON((134.635194391036 -21.4282083310724, 134.581480136827 -21.6408640426055, 134.833308274251 -21.686125031254, 134.886750925145 -21.4734274382519, 134.635194391036 -21.4282083310724))
        FORMAT_CORRECTNESS_FLAG=PASSED
        GENERAL_QUALITY_FLAG=PASSED
        GENERATION_TIME=2015-11-12T10:55:12.000947Z
        GEOMETRIC_QUALITY_FLAG=PASSED
        GRANULE_ID=S2A_OPER_MSI_L1B_GR_SGS__20151024T023555_S20151024T011315_D02_N01.04
        PREVIEW_GEO_INFO=BrowseImageFootprint
        PREVIEW_IMAGE_URL=https://pdmcdam2.sentinel2.eo.esa.int/s2pdgs_geoserver/geo_service.php?service=WMS&version=1.1.0&request=GetMap&layers=S2A_A000045_N0104:S2A_A000045_N0104&styles=&bbox=133.512786023161,-25.3930035889714,137.184847290108,-21.385906922696&width=1579&height=330&srs=EPSG:4326&format=image/png&time=2015-10-24T01:13:15.0Z/2015-10-24T01:14:13.0Z
        PROCESSING_BASELINE=01.04
        PROCESSING_LEVEL=Level-1B
        PRODUCT_START_TIME=2015-10-24T01:13:15.497656Z
        PRODUCT_STOP_TIME=2015-10-24T01:14:13.70431Z
        PRODUCT_TYPE=S2MSI1B
        RADIOMETRIC_QUALITY_FLAG=PASSED
        SENSING_TIME=2015-10-24T01:13:15.497656Z
        SENSOR_QUALITY_FLAG=PASSED
        SPECIAL_VALUE_NODATA=1
        SPECIAL_VALUE_SATURATED=0
      Corner Coordinates:
      Upper Left  (    0.0,    0.0)
      Lower Left  (    0.0, 2304.0)
      Upper Right ( 2552.0,    0.0)
      Lower Right ( 2552.0, 2304.0)
      Center      ( 1276.0, 1152.0)
      Band 1 Block=128x128 Type=UInt16, ColorInterp=Red
        Description = B4, central wavelength 665 nm
        Overviews: 1276x1152, 638x576, 319x288, 160x144
        Metadata:
          BANDNAME=B4
          BANDWIDTH=30
          BANDWIDTH_UNIT=nm
          WAVELENGTH=665
          WAVELENGTH_UNIT=nm
        Image Structure Metadata:
          NBITS=12
      Band 2 Block=128x128 Type=UInt16, ColorInterp=Green
        Description = B3, central wavelength 560 nm
      [...]
      Band 3 Block=128x128 Type=UInt16, ColorInterp=Blue
        Description = B2, central wavelength 490 nm
      [...]
      Band 4 Block=128x128 Type=UInt16, ColorInterp=Undefined
        Description = B8, central wavelength 842 nm
      [...]

참고
--------

-  `센티널 과학 데이터 허브 <https://scihub.copernicus.eu/>`_
-  `센티널 2 사용자 지침서 <https://sentinels.copernicus.eu/web/sentinel/user-guides/센티널-2-msi>`_
-  `센티널 2 사용자 안내서 <https://sentinels.copernicus.eu/web/sentinel/user-guides/document-library/-/asset_publisher/xlslt4309D5h/content/센티널-2-user-handbook>`_

감사의 말
---------

`Spatialys <http://spatialys.com>`_ 사가 `프랑스 국립 우주 연구 센터(Centre National d'Etudes Spatiales) <https://cnes.fr>`_ 의 재정 지원을 받아 이 드라이버를 개발했습니다.
