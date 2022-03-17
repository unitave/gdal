.. _raster.hdf5:

================================================================================
HDF5 -- 계층적 데이터 형식(Hierarchical Data Format) 배포판 5 (HDF5)
================================================================================

.. shortname:: HDF5

.. shortname:: HDF5Image

.. build_dependencies:: libhdf5

이 드라이버는 HDF5 파일 포맷을 가져오기 위해 개발되었습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

.. versionadded:: 2.4

    .. supports_virtualio::

다중 이미지 처리(하위 데이터셋)
-------------------------------------

계층적 데이터 형식(Hierarchical Data Format)은 몇 가지 서로 다른 데이터셋을 담기 위한 컨테이너입니다. 데이터 저장을 위해, HDF는 데이터로 채워진 다중 차원 배열을 담고 있습니다. HDF 파일 하나가 서로 다른 배열 여러 개를 담을 수도 있습니다. 이 배열들은 차원의 크기, 개수가 다를 수도 있습니다.

1단계로 **gdalinfo** 를 이용해서 파일의 구성요소 이미지(배열)의 리포트를 수집한 다음 **gdal_translate** 를 이용해서 원하는 이미지를 가져옵니다. **gdalinfo** 유틸리티는 입력 HDF 파일로부터 모든 다중 차원 하위 데이터셋의 목록을 수집합니다. 개별 이미지(하위 데이터셋)의 이름은 **SUBDATASET_n_NAME** 메타데이터 항목에 할당되어 있습니다. 각 이미지의 설명은 **SUBDATASET_n_DESC** 메타데이터 항목에 있습니다. HDF5 이미지의 경우 하위 데이터셋 이름이 다음과 같은 서식일 것입니다:

*HDF5:file_name:subdataset*

이때 *file_name* 은 입력 파일의 이름이고, *subdataset* 은 (GDAL 내부에서) 사용할 배열의 데이터셋 이름입니다.

2단계에서는 데이터를 실제로 읽어오기 위해 **gdalinfo** 또는 **gdal_translate** 에 이 이름을 지정해줘야 합니다.

예를 들어, OMI/Aura Ozone (O3) 데이터셋으로부터 데이터를 읽어오려면:

::

   $ gdalinfo OMI-Aura_L2-OMTO3_2005m0326t2307-o03709_v002-2005m0428t201311.he5
   Driver: HDF5/Hierarchical Data Format Release 5
   Size is 512, 512
   Coordinate System is `'

   Subdatasets:
     SUBDATASET_1_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/APrioriLayerO3
     SUBDATASET_1_DESC=[1496x60x11] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/APrioriLayerO3 (32-bit floating-point)
     SUBDATASET_2_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/AlgorithmFlags
     SUBDATASET_2_DESC=[1496x60] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/AlgorithmFlags (8-bit unsigned character)
     SUBDATASET_3_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/CloudFraction
     SUBDATASET_3_DESC=[1496x60] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/CloudFraction (32-bit floating-point)
     SUBDATASET_4_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/CloudTopPressure
     SUBDATASET_4_DESC=[1496x60] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/CloudTopPressure (32-bit floating-point)
     SUBDATASET_5_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/ColumnAmountO3
     SUBDATASET_5_DESC=[1496x60] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/ColumnAmountO3 (32-bit floating-point)
     SUBDATASET_6_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/LayerEfficiency
     SUBDATASET_6_DESC=[1496x60x11] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/LayerEfficiency (32-bit floating-point)
     SUBDATASET_7_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/NValue
     SUBDATASET_7_DESC=[1496x60x12] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/NValue (32-bit floating-point)
     SUBDATASET_8_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/O3BelowCloud
     SUBDATASET_8_DESC=[1496x60] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/O3BelowCloud (32-bit floating-point)
     SUBDATASET_9_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/QualityFlags
     SUBDATASET_9_DESC=[1496x60] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/QualityFlags (16-bit unsigned integer)
     SUBDATASET_10_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/Reflectivity331
     SUBDATASET_10_DESC=[1496x60] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/Reflectivity331 (32-bit floating-point)
     SUBDATASET_11_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/Reflectivity360
     SUBDATASET_11_DESC=[1496x60] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/Reflectivity360 (32-bit floating-point)
     SUBDATASET_12_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/Residual
     SUBDATASET_12_DESC=[1496x60x12] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/Residual (32-bit floating-point)
     SUBDATASET_13_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/ResidualStep1
     SUBDATASET_13_DESC=[1496x60x12] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/ResidualStep1 (32-bit floating-point)
     SUBDATASET_14_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/ResidualStep2
     SUBDATASET_14_DESC=[1496x60x12] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/ResidualStep2 (32-bit floating-point)
     SUBDATASET_15_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/SO2index
     SUBDATASET_15_DESC=[1496x60] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/SO2index (32-bit floating-point)
     SUBDATASET_16_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/Sensitivity
     SUBDATASET_16_DESC=[1496x60x12] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/Sensitivity (32-bit floating-point)
     SUBDATASET_17_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/StepOneO3
     SUBDATASET_17_DESC=[1496x60] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/StepOneO3 (32-bit floating-point)
     SUBDATASET_18_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/StepTwoO3
     SUBDATASET_18_DESC=[1496x60] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/StepTwoO3 (32-bit floating-point)
     SUBDATASET_19_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/TerrainPressure
     SUBDATASET_19_DESC=[1496x60] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/TerrainPressure (32-bit floating-point)
     SUBDATASET_20_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/UVAerosolIndex
     SUBDATASET_20_DESC=[1496x60] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/UVAerosolIndex (32-bit floating-point)
     SUBDATASET_21_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/dN_dR
     SUBDATASET_21_DESC=[1496x60x12] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/dN_dR (32-bit floating-point)
     SUBDATASET_22_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/dN_dT
     SUBDATASET_22_DESC=[1496x60x12] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/dN_dT (32-bit floating-point)
     SUBDATASET_23_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Geolocation_Fields/GroundPixelQualityFlags
     SUBDATASET_23_DESC=[1496x60] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Geolocation_Fields/GroundPixelQualityFlags (16-bit unsigned integer)
     SUBDATASET_24_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Geolocation_Fields/Latitude
     SUBDATASET_24_DESC=[1496x60] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Geolocation_Fields/Latitude (32-bit floating-point)
     SUBDATASET_25_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Geolocation_Fields/Longitude
     SUBDATASET_25_DESC=[1496x60] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Geolocation_Fields/Longitude (32-bit floating-point)
     SUBDATASET_26_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Geolocation_Fields/RelativeAzimuthAngle
     SUBDATASET_26_DESC=[1496x60] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Geolocation_Fields/RelativeAzimuthAngle (32-bit floating-point)
     SUBDATASET_27_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Geolocation_Fields/SolarAzimuthAngle
     SUBDATASET_27_DESC=[1496x60] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Geolocation_Fields/SolarAzimuthAngle (32-bit floating-point)
     SUBDATASET_28_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Geolocation_Fields/SolarZenithAngle
     SUBDATASET_28_DESC=[1496x60] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Geolocation_Fields/SolarZenithAngle (32-bit floating-point)
     SUBDATASET_29_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Geolocation_Fields/TerrainHeight
     SUBDATASET_29_DESC=[1496x60] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Geolocation_Fields/TerrainHeight (16-bit integer)
     SUBDATASET_30_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Geolocation_Fields/ViewingAzimuthAngle
     SUBDATASET_30_DESC=[1496x60] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Geolocation_Fields/ViewingAzimuthAngle (32-bit floating-point)
     SUBDATASET_31_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Geolocation_Fields/ViewingZenithAngle
     SUBDATASET_31_DESC=[1496x60] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Geolocation_Fields/ViewingZenithAngle (32-bit floating-point)
   Corner Coordinates:
   Upper Left  (    0.0,    0.0)
   Lower Left  (    0.0,  512.0)
   Upper Right (  512.0,    0.0)
   Lower Right (  512.0,  512.0)
   Center      (  256.0,  256.0)

이제 ``[1645x60] CloudFraction (32-bit floating-point)`` 라고 설명된 하위 데이터셋 1개를 선택합니다:

::

   $ gdalinfo HDF5:"OMI-Aura_L2-OMTO3_2005m0326t2307-o03709_v002-2005m0428t201311.he5":CloudFraction
   Driver: HDF5Image/HDF5 Dataset
   Size is 60, 1645
   Coordinate System is:
   GEOGCS["WGS 84",
       DATUM["WGS_1984",
           SPHEROID["WGS 84",6378137,298.257223563,
               AUTHORITY["EPSG","7030"]],
           TOWGS84[0,0,0,0,0,0,0],
           AUTHORITY["EPSG","6326"]],
       PRIMEM["Greenwich",0,
           AUTHORITY["EPSG","8901"]],
       UNIT["degree",0.0174532925199433,
           AUTHORITY["EPSG","9108"]],
       AXIS["Lat",NORTH],
       AXIS["Long",EAST],
       AUTHORITY["EPSG","4326"]]
   GCP Projection = GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],TOWGS84[0,0,0,0,0,0,0],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9108"]],AXIS["Lat",NORTH],AXIS["Long",EAST],AUTHORITY["EPSG","4326"]]
   GCP[  0]: Id=, Info=
             (0.5,0.5) -> (261.575,-84.3495,0)
   GCP[  1]: Id=, Info=
             (2.5,0.5) -> (240.826,-85.9928,0)
   GCP[  2]: Id=, Info=
             (4.5,0.5) -> (216.754,-86.5932,0)
   GCP[  3]: Id=, Info=
             (6.5,0.5) -> (195.5,-86.5541,0)
   GCP[  4]: Id=, Info=
             (8.5,0.5) -> (180.265,-86.2009,0)
   GCP[  5]: Id=, Info=
             (10.5,0.5) -> (170.011,-85.7315,0)
   GCP[  6]: Id=, Info=
             (12.5,0.5) -> (162.987,-85.2337,0)
   ... 3000 GCPs are read from the file if Latitude and Longitude arrays are presents
   Corner Coordinates: Upper Left (0.0, 0.0) Lower Left (0.0, 1645.0) Upper Right (60.0, 0.0) Lower Right (60.0, 1645.0) Center (30.0, 822.5)
   Band 1 Block=60x1 Type=Float32, ColorInterp=Undefined Open GDAL Datasets: 1 N DriverIsNULL 512x512x0

또는 이 데이터셋으로부터 이미지 밴드를 읽어오기 위해 **gdal_translate** 를 사용할 수도 있습니다.

GDAL에 **SUBDATASET_n_NAME** 으로 표시된 줄의 내용을 **HDF4_SDS:** 접두어를 포함해서 정확하게 지정해야 한다는 사실을 기억하십시오.

이 드라이버의 목적은 원격 탐사 및 지리공간 데이터셋을 래스터 이미지 (2차원 또는 3차원 배열) 형태로 가져오기 위한 것일 뿐입니다. HDF 파일에 담겨 있는 모든 데이터를 탐색하길 바란다면 다른 도구를 사용해야 합니다. (이 페이지의 마지막 부분에 있는 링크를 통해 다른 HDF 도구들에 관한 정보를 찾아볼 수 있습니다.)

지리참조
------------

HDF 파일에 지리참조 정보를 저장하는 보편적인 방법은 없습니다. 하지만 일부 상품 유형이 지리참조 정보를 저장하기 위한 메커니즘을 가지고 있고, GDAL이 이 가운데 몇몇을 지원합니다. 현재 지원되는 방법은 다음과 같습니다(*subdataset_type* 은 괄호 안에 있습니다):

-  HDF5 OMI/Aura Ozone (O3) Total Column 1-Orbit L2 Swath 13x24km
   (**Level-2 OMTO3**)


다중 파일 지원
------------------

GDAL 3.1버전부터, 이 드라이버는 파일 여러 개로 분할된 데이터셋을 'family' HDF5 파일 드라이버를 이용해서 열기를 지원합니다. 이를 위해 GDAL에 이름에 단일 '0' 문자를 담고 있거나 0.h5 또는 0.hdf5로 끝나는 첫 부분의 파일명을 지정해줘야만 합니다.

다중 차원 API 지원
----------------------------

.. versionadded:: 3.1

HDF5 드라이버는 읽기 작업을 위해 :ref:`multidim_raster_data_model` 을 지원합니다.

드라이버 빌드 작업
----------------

이 드라이버는 NCSA HDF 라이브러리를 바탕으로 빌드되었기 때문에, 사전 빌드된 HDF5-1.6.4버전 이상의 HDF5 라이브러리를 다운로드해야 합니다. zlib 1.2 및 szlib 2.0도 필요합니다. 윈도우 사용자의 경우 (특히 Cygwin을 사용하는 경우) 속성을 반드시 쓰기 가능으로 설정해야 하며, 사용자의 PATH 환경설정 변수에 포함되는 위치에 DLL을 설치해야 합니다. NCSA HDF 홈페이지에서 소스 코드를 다운로드할 수도 있습니다. (아래 링크 참조)

참고
--------

``gdal/frmts/hdf5/hdf5dataset.cpp`` 및 ``gdal/frmts/hdf5/hdf5imagedataset.cpp`` 로 구현되었습니다.

`미국 국립 수퍼컴퓨팅 응용 연구소(National Center for Supercomputing Applications) <http://www.ncsa.uiuc.edu/>`_ 의 `NCSA HDF5 다운로드 페이지 <http://hdf.ncsa.uiuc.edu/HDF5/release/obtain5.html>`_

`HDFView <http://hdf.ncsa.uiuc.edu/hdf-java-html/hdfview/>`_ 는 NCSA HDF4 및 HDF5 파일을 탐색하고 편집하기 위한 시각적 도구입니다.

이 드라이버가 지원하는 개별 상품에 관한 문서:

-  `OMTO3: OMI/Aura Ozone (O3) Total Column 1-Orbit L2 Swath 13x24km V003 <https://disc.gsfc.nasa.gov/uui/datasets/OMTO3_V003/summary>`_
