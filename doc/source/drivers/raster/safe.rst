.. _raster.safe:

================================================================================
SAFE -- 센티널-1 SAFE XML 상품
================================================================================

.. shortname:: SAFE

.. built_in_by_default::


이 드라이버는 센티널(Sentinel) 상품 용입니다. 현재 센티널-1 SAR 상품만 지원합니다. :ref:`GDAL 센티널-2 <raster.sentinel2>` 드라이버도 참조하십시오.

SAFE(Standard Archive Format for Europe) 포맷 사양의 SENTINEL 특화 변이형을 사용해서 SENTINEL 데이터 상품을 배포합니다. SAFE 포맷은 유럽 우주국의 지구 관측자료 보관 시설 안에서 데이터를 보관하고 전송하기 위한 공통 포맷으로 작동하도록 설계되었습니다.


manifest.safe 파일 또는 이 파일을 담고 있는 디렉터리를 선택하면 SAFE 드라이버를 사용할 것입니다. 이 드라이버는 모든 영상을 하나의 일관된 데이터셋으로 처리할 수 있습니다.

SAFE 드라이버는 메타데이터로부터 지리 위치 그리드 포인트(geolocation grid point)도 읽어와서 데이터셋 상의 GCP로 표현합니다.

유럽 우주국은 이 포맷으로 된 다른 위성 데이터셋들을 배포할 것입니다. 하지만 현재, 이 드라이버는 특정 센티널-1 SAR 상품만 지원합니다. 다른 종류의 모든 상품은 무시하거나 여러 가지 런타임 오류를 발생시킬 것입니다.

드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

.. supports_virtualio::

다중 관측
---------------------

상품이 (예를 들어 편광 데이터 여러 개 같은) 여러 관측 데이터를 담고 있는 경우, 관측 영역(swath)이 동일하다면 관측 데이터 각각을 래스터 밴드 하나로 사용할 수 있습니다. 관측 영역이 동일하다는 것은 지역도 동일하다는 뜻이니까요.

상품이 관측 영역 여러 개와 편광 데이터 여러 개를 담고 있다면, 이 드라이버는 기본적으로 첫 번째 관측 영역을 출력할 것입니다. 다른 관측 영역에 접근하려면 사용자가 특정 하위 데이터셋을 선택해야만 합니다.

GDAL 3.4버전에서 하위 데이터셋 명명 문법 및 내용이 크게 변경되었습니다.

예시
--------

-  센티널-1 상품 열기:

   ::

      $ gdalinfo S1A_IW_GRDH_1SDV_20150705T064241_20150705T064306_006672_008EA0_24EE.SAFE/manifest.safe

   ::

      Driver: SAFE/Sentinel-1 SAR SAFE Product
      Files: S1A_IW_GRDH_1SDV_20150705T064241_20150705T064306_006672_008EA0_24EE.SAFE/manifest.safe
             S1A_IW_GRDH_1SDV_20150705T064241_20150705T064306_006672_008EA0_24EE.SAFE/measurement/s1a-iw-grd-vh-20150705t064241-20150705t064306-006672-008ea0-002.tiff
             S1A_IW_GRDH_1SDV_20150705T064241_20150705T064306_006672_008EA0_24EE.SAFE/measurement/s1a-iw-grd-vv-20150705t064241-20150705t064306-006672-008ea0-001.tiff
      Size is 256, 167
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
      GCP[  0]: Id=1, Info=
                (0,0) -> (-8.03500070209827,39.6332161725022,141.853266630322)
      Metadata:
        ACQUISITION_START_TIME=2015-07-05T06:42:41.504840
        ACQUISITION_STOP_TIME=2015-07-05T06:43:06.503530
        BEAM_MODE=IW
        BEAM_SWATH=IW
        FACILITY_IDENTIFIER=UPA_
        LINE_SPACING=1.000655e+01
        MISSION_ID=S1A
        MODE=IW
        ORBIT_DIRECTION=DESCENDING
        ORBIT_NUMBER=6672
        PIXEL_SPACING=1.000000e+01
        PRODUCT_TYPE=GRD
        SATELLITE_IDENTIFIER=SENTINEL-1
        SENSOR_IDENTIFIER=SAR
        SWATH=IW
      Subdatasets:
        SUBDATASET_1_NAME=SENTINEL1_DS:S1A_IW_GRDH_1SDV_20150705T064241_20150705T064306_006672_008EA0_24EE.SAFE:IW_VH
        SUBDATASET_1_DESC=Single band with IW swath and VH polarization
        SUBDATASET_2_NAME=SENTINEL1_DS:S1A_IW_GRDH_1SDV_20150705T064241_20150705T064306_006672_008EA0_24EE.SAFE:IW_VV
        SUBDATASET_2_DESC=Single band with IW swath and VV polarization
        SUBDATASET_3_NAME=SENTINEL1_DS:S1A_IW_GRDH_1SDV_20150705T064241_20150705T064306_006672_008EA0_24EE.SAFE:IW
        SUBDATASET_3_DESC=IW swath with all polarizations as bands
      Corner Coordinates:
      Upper Left  (    0.0,    0.0)
      Lower Left  (    0.0,  167.0)
      Upper Right (  256.0,    0.0)
      Lower Right (  256.0,  167.0)
      Center      (  128.0,   83.5)
      Band 1 Block=256x16 Type=UInt16, ColorInterp=Undefined
        Metadata:
          POLARISATION=VH
          SWATH=IW
      Band 2 Block=256x16 Type=UInt16, ColorInterp=Undefined
        Metadata:
          POLARISATION=VV
          SWATH=IW

-  반드시 manifest.safe 파일을 열 필요는 없습니다. 그냥 폴더명만 전송해도 됩니다:

   ::

      $ gdalinfo S1A_IW_GRDH_1SDV_20150705T064241_20150705T064306_006672_008EA0_24EE.SAFE

-  단일 관측 데이터 열기 (예: IW/VH):

   ::

      $ gdalinfo SENTINEL1_DS:S1A_IW_GRDH_1SDV_20150705T064241_20150705T064306_006672_008EA0_24EE.SAFE:IW_VV


   또는 GDAL 3.4버전부터

   ::

      $ gdalinfo SENTINEL1_CALIB:UNCALIB:test.SAFE:IW_VV:AMPLITUDE

데이터 보정
----------------

GDAL 3.4버전부터, SIGMA0, BETA0 및 GAMMA 보정 하위 데이터셋에 보정을 적용합니다.

참고
--------

-  `SAR 포맷 (ESA 센티널 온라인) <https://sentinel.esa.int/web/sentinel/user-guides/sentinel-1-sar/data-formats/sar-formats>`_
-  `SAFE 사양 (ESA 센티널 온라인) <https://sentinel.esa.int/web/sentinel/user-guides/sentinel-1-sar/data-formats/safe-specification>`_
-  :ref:`GDAL Sentinel-2 <raster.sentinel2>` 드라이버

