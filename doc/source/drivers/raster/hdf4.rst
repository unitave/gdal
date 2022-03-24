.. _raster.hdf4:

================================================================================
HDF4 -- 계층적 데이터 형식(Hierarchical Data Format) 배포판 4 (HDF4)
================================================================================

.. shortname:: HDF4

.. shortname:: HDF4Image

.. build_dependencies:: libdf

HDF 포맷은 HDF4(4.x 및 이전 배포판들)와 HDF5 두 종류가 있습니다. 이 두 포맷은 완전히 다르며 호환되지 않습니다. 이 드라이버는 HDF4 파일 포맷을 가져오기 위해 개발되었습니다. NASA의 지구 관측 시스템(Earth Observing System; EOS)은 HDF-EOS라는 고유 HDF 수정 버전을 관리하고 있습니다. 이 수정 버전은 원격 탐사 데이터 이용에 안성맞춤이며, 기저 HDF와도 완벽하게 호환됩니다. 이 드라이버는 HDF4-EOS 파일도 가져올 수 있습니다.
현재 EOS는 ('Terra'와 'Aqua' 위성의 원격 탐사 자료) 데이터 저장에 HDF4-EOS를 사용하고 있습니다. 향후 'Aura' 위성의 원격 탐사 자료를 저장하는 데 사용될 HDF5-EOS 포맷으로 교체될 예정입니다.

드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::

.. supports_create::

.. supports_georeferencing::

다중 이미지 처리(하위 데이터셋)
-------------------------------------

계층적 데이터 형식(Hierarchical Data Format)은 몇 가지 서로 다른 데이터셋을 담기 위한 컨테이너입니다. 데이터 저장에는 과학적 데이터셋(Scientific Datasets; SDS)을 가장 자주 사용합니다. SDS는 데이터로 채워진 다중 차원 배열입니다. HDF 파일 하나가 서로 다른 SDS 배열 여러 개를 담을 수도 있습니다. 이 배열들은 차원의 크기, 개수가 다를 수도 있고 서로 다른 지역의 데이터를 표현할 수도 있습니다.

HDF 파일이 이미지로 보이는 SDS 하나만 담고 있는 경우 일반적인 방식으로 접근할 수도 있지만, 이미지 여러 개를 담고 있다면 2단계 과정을 거쳐 파일을 가져와야 할 수도 있습니다. 1단계는 **gdalinfo** 를 이용해서 파일의 구성요소 이미지(SDS 배열)의 리포트를 수집한 다음 **gdal_translate** 를 이용해서 원하는 이미지를 가져오는 것입니다. **gdalinfo** 유틸리티는 입력 HDF 파일로부터 모든 다중 차원 하위 데이터셋의 목록을 수집합니다. 개별 이미지(하위 데이터셋)의 이름은 **SUBDATASET_n_NAME** 메타데이터 항목에 할당되어 있습니다. 각 이미지의 설명은 **SUBDATASET_n_DESC** 메타데이터 항목에 있습니다. HDF4 이미지의 경우 하위 데이터셋 이름이 다음과 같은 서식일 것입니다:

*HDF4_SDS:subdataset_type:file_name:subdataset_index*

이때 *subdataset_type* 은 잘 알려진 몇몇 HDF 데이터셋에 사전 정의된 이름을 보여주고, *file_name* 은 입력 파일의 이름, 그리고 *subdataset_index* 는 (GDAL 내부에서) 사용할 이미지의 색인을 보여줍니다.

2단계에서는 데이터를 실제로 읽어오기 위해 **gdalinfo** 또는 **gdal_translate** 에 이 이름을 지정해줘야 합니다.

예를 들어, MODIS 1B수준 데이터셋으로부터 데이터를 읽어오려면:

::

   $ gdalinfo GSUB1.A2001124.0855.003.200219309451.hdf
   Driver: HDF4/Hierarchical Data Format Release 4
   Size is 512, 512
   Coordinate System is `'
   Metadata:
     HDFEOSVersion=HDFEOS_V2.7
     Number of Scans=204
     Number of Day mode scans=204
     Number of Night mode scans=0
     Incomplete Scans=0

...수많은 메타데이터 출력물을 건너뛰어서...

::

   Subdatasets:
     SUBDATASET_1_NAME=HDF4_SDS:MODIS_L1B:GSUB1.A2001124.0855.003.200219309451.hdf:0
     SUBDATASET_1_DESC=[408x271] Latitude (32-bit floating-point)
     SUBDATASET_2_NAME=HDF4_SDS:MODIS_L1B:GSUB1.A2001124.0855.003.200219309451.hdf:1
     SUBDATASET_2_DESC=[408x271] Longitude (32-bit floating-point)
     SUBDATASET_3_NAME=HDF4_SDS:MODIS_L1B:GSUB1.A2001124.0855.003.200219309451.hdf:2
     SUBDATASET_3_DESC=[12x2040x1354] EV_1KM_RefSB (16-bit unsigned integer)
     SUBDATASET_4_NAME=HDF4_SDS:MODIS_L1B:GSUB1.A2001124.0855.003.200219309451.hdf:3
     SUBDATASET_4_DESC=[12x2040x1354] EV_1KM_RefSB_Uncert_Indexes (8-bit unsigned integer)
     SUBDATASET_5_NAME=HDF4_SDS:MODIS_L1B:GSUB1.A2001124.0855.003.200219309451.hdf:4
     SUBDATASET_5_DESC=[408x271] Height (16-bit integer)
     SUBDATASET_6_NAME=HDF4_SDS:MODIS_L1B:GSUB1.A2001124.0855.003.200219309451.hdf:5
     SUBDATASET_6_DESC=[408x271] SensorZenith (16-bit integer)
     SUBDATASET_7_NAME=HDF4_SDS:MODIS_L1B:GSUB1.A2001124.0855.003.200219309451.hdf:6
     SUBDATASET_7_DESC=[408x271] SensorAzimuth (16-bit integer)
     SUBDATASET_8_NAME=HDF4_SDS:MODIS_L1B:GSUB1.A2001124.0855.003.200219309451.hdf:7
     SUBDATASET_8_DESC=[408x271] Range (16-bit unsigned integer)
     SUBDATASET_9_NAME=HDF4_SDS:MODIS_L1B:GSUB1.A2001124.0855.003.200219309451.hdf:8
     SUBDATASET_9_DESC=[408x271] SolarZenith (16-bit integer)
     SUBDATASET_10_NAME=HDF4_SDS:MODIS_L1B:GSUB1.A2001124.0855.003.200219309451.hdf:9
     SUBDATASET_10_DESC=[408x271] SolarAzimuth (16-bit integer)
     SUBDATASET_11_NAME=HDF4_SDS:MODIS_L1B:GSUB1.A2001124.0855.003.200219309451.hdf:10
     SUBDATASET_11_DESC=[408x271] gflags (8-bit unsigned integer)
     SUBDATASET_12_NAME=HDF4_SDS:MODIS_L1B:GSUB1.A2001124.0855.003.200219309451.hdf:12
     SUBDATASET_12_DESC=[16x10] Noise in Thermal Detectors (8-bit unsigned integer)
     SUBDATASET_13_NAME=HDF4_SDS:MODIS_L1B:GSUB1.A2001124.0855.003.200219309451.hdf:13
     SUBDATASET_13_DESC=[16x10] Change in relative responses of thermal detectors (8-bit unsigned integer)
     SUBDATASET_14_NAME=HDF4_SDS:MODIS_L1B:GSUB1.A2001124.0855.003.200219309451.hdf:14
     SUBDATASET_14_DESC=[204x16x10] DC Restore Change for Thermal Bands (8-bit integer)
     SUBDATASET_15_NAME=HDF4_SDS:MODIS_L1B:GSUB1.A2001124.0855.003.200219309451.hdf:15
     SUBDATASET_15_DESC=[204x2x40] DC Restore Change for Reflective 250m Bands (8-bit integer)
     SUBDATASET_16_NAME=HDF4_SDS:MODIS_L1B:GSUB1.A2001124.0855.003.200219309451.hdf:16
     SUBDATASET_16_DESC=[204x5x20] DC Restore Change for Reflective 500m Bands (8-bit integer)
     SUBDATASET_17_NAME=HDF4_SDS:MODIS_L1B:GSUB1.A2001124.0855.003.200219309451.hdf:17
     SUBDATASET_17_DESC=[204x15x10] DC Restore Change for Reflective 1km Bands (8-bit integer)
   Corner Coordinates:
   Upper Left  (    0.0,    0.0)
   Lower Left  (    0.0,  512.0)
   Upper Right (  512.0,    0.0)
   Lower Right (  512.0,  512.0)
   Center      (  256.0,  256.0)

이제 ``[12x2040x1354] EV_1KM_RefSB (16-bit unsigned integer)`` 라고 설명된 하위 데이터셋 1개를 선택합니다:

::

   $ gdalinfo HDF4_SDS:MODIS_L1B:GSUB1.A2001124.0855.003.200219309451.hdf:2
   Driver: HDF4Image/HDF4 Internal Dataset
   Size is 1354, 2040
   Coordinate System is `'
   Metadata:
     long_name=Earth View 1KM Reflective Solar Bands Scaled Integers

...메타데이터를 건너뛰고...

::

   Corner Coordinates:
   Upper Left  (    0.0,    0.0)
   Lower Left  (    0.0, 2040.0)
   Upper Right ( 1354.0,    0.0)
   Lower Right ( 1354.0, 2040.0)
   Center      (  677.0, 1020.0)
   Band 1 Block=1354x2040 Type=UInt16, ColorInterp=Undefined
   Band 2 Block=1354x2040 Type=UInt16, ColorInterp=Undefined
   Band 3 Block=1354x2040 Type=UInt16, ColorInterp=Undefined
   Band 4 Block=1354x2040 Type=UInt16, ColorInterp=Undefined
   Band 5 Block=1354x2040 Type=UInt16, ColorInterp=Undefined
   Band 6 Block=1354x2040 Type=UInt16, ColorInterp=Undefined
   Band 7 Block=1354x2040 Type=UInt16, ColorInterp=Undefined
   Band 8 Block=1354x2040 Type=UInt16, ColorInterp=Undefined
   Band 9 Block=1354x2040 Type=UInt16, ColorInterp=Undefined
   Band 10 Block=1354x2040 Type=UInt16, ColorInterp=Undefined
   Band 11 Block=1354x2040 Type=UInt16, ColorInterp=Undefined
   Band 12 Block=1354x2040 Type=UInt16, ColorInterp=Undefined

또는 이 데이터셋으로부터 이미지 밴드를 읽어오기 위해 **gdal_translate** 를 사용할 수도 있습니다.

GDAL에 **SUBDATASET_n_NAME** 으로 표시된 줄의 내용을 **HDF4_SDS:** 접두어를 포함해서 정확하게 지정해야 한다는 사실을 기억하십시오.

이 드라이버의 목적은 오직 원격 탐사 및 지리공간 데이터셋을 래스터 이미지 형태로 가져오는 것입니다. HDF 파일에 담겨 있는 모든 데이터를 탐색하길 바란다면 다른 도구를 사용해야 합니다. (이 페이지의 마지막 부분에 있는 링크를 통해 다른 HDF 도구들에 관한 정보를 찾아볼 수 있습니다.)

지리참조
------------

HDF 파일에 지리참조 정보를 저장하는 보편적인 방법은 없습니다. 하지만 일부 상품 유형이 지리참조 정보를 저장하기 위한 메커니즘을 가지고 있고, GDAL이 이 가운데 몇몇을 지원합니다. 현재 지원되는 방법은 다음과 같습니다(*subdataset_type* 은 괄호 안에 있습니다):

-  GDAL로 생성한 HDF4 파일 (**GDAL_HDF4**)
-  ASTER 1A수준 (**ASTER_L1A**)
-  ASTER 1B수준 (**ASTER_L1B**)
-  ASTER 2수준 (**ASTER_L2**)
-  ASTER DEM (**AST14DEM**)
-  MODIS 1B수준 어스뷰(Earth View) 상품 (**MODIS_L1B**)
-  MODIS 3수준 상품 (**MODIS_L3**)
-  SeaWiFS 3수준 표준 매핑 이미지 상품 (**SEAWIFS_L3**)

HDF4 드라이버는 기본적으로 EOS_SWATH 데이터셋으로부터 10번째 행과 열에서마다 GCP만 읽어옵니다. GEOL_AS_GCPS 환경 변수를 PARTIAL(기본값), NONE, 또는 FULL 가운데 하나로 설정하면 이 습성을 변경할 수 있습니다.

생성 문제점
---------------

이 드라이버는 HDF4 과학적 데이터셋 생성을 지원합니다. 2차원 데이터셋 집합을 (각 입력 밴드 당 하나씩) 생성할 수도 있고, 또는 세 번째 타원이 밴드 번호를 나타내는 단일 3차원 데이터셋을 생성할 수도 있습니다. 입력 데이터셋의 모든 메타데이터와 밴드 설명은 HDF4 속성으로 저장됩니다. 투영 정보(가 존재한다면) 및 아핀 변환 계수도 속성이라는 형태로 저장됩니다. GDAL이 생성하는 파일은 다음 특수 속성을 가지고 있습니다:

"Signature=Created with GDAL (http://www.remotesensing.org/gdal/)"

그리고 읽어올 때 이 속성을 자동으로 식별하기 때문에, 투영 정보 및 변환 행렬을 복구합니다.

생성 옵션:

-  **RANK=n**: **n** 차원 SDS를 생성합니다. 현재 2차원 및 3차원 데이터셋만 지원합니다. 기본적으로 3차원 데이터셋을 생성할 것입니다.

메타데이터
---------

모든 HDF4 속성을 GDAL 메타데이터로 알기 쉽게 변환합니다. HDF 파일에서 속성은 전체 파일은 물론 특정 하위 데이터셋에 할당되었을 수도 있습니다.

열기 옵션
------------

다음 열기 옵션을 지원합니다:

- **LIST_SDS=AUTO/YES/NO**: (GDAL 3.2 이상 버전) 과학적 데이터셋 집합(SDS)을 리포트할지 여부를 설정합니다. HDF 파일이 EOS_SWATH 또는 EOS_GRID를 담고 있는 경우, SDS는 기본적으로 GDAL 하위 데이터셋 목록에 리포트되지 않을 것입니다. (두 번 리포트될 것이기 때문입니다.) LIST_SDS를 YES로 설정하면 SDS를 목록에 리포트시킬 수 있습니다.

다중 차원 API 지원
----------------------------

.. versionadded:: 3.1

HDF4 드라이버는 읽기 작업을 위해 :ref:`multidim_raster_data_model` 을 지원합니다.

드라이버 빌드 작업
----------------

이 드라이버는 NCSA HDF 라이브러리를 바탕으로 빌드되었기 때문에, GDAL이 HDF4를 지원하도록 빌드하려면 해당 라이브러리가 필요합니다. 사전 컴파일된 바이너리를 찾아 사용자의 운영 체제 배포판을 검색하거나, NCSA HDF 홈페이지에서 소스 코드 또는 바이너리를 다운로드할 수도 있습니다. (아래 링크 참조)

NCSA HDF 라이브러리는 *hlimits.h* 파일에 정의된 여러 개의 기본값으로 컴파일된다는 사실을 기억하십시오. 예를 들면 *hlimits.h* 파일은 한꺼번에 열 수 있는 최대 파일 개수를 다음과 같이 정의합니다:

::

   #   define MAX_FILE   32

한번에 더 많은 파일을 열어야 하는 경우 이 값을 수정하고 HDF4 라이브러리를 다시 빌드해야 합니다. (또 정적 HDF 라이브러리를 사용하는 경우 GDAL과 다시 링크시켜야 합니다.)

참고
--------

-  ``gdal/frmts/hdf4/hdf4dataset.cpp`` 및 ``gdal/frmts/hdf4/hdf4imagedataset.cpp`` 로 구현되었습니다.
-  `HDF 그룹 <http://www.hdfgroup.org/>`_
-  HDF4 및 HDF4-EOS 포맷 데이터의 소스:

   `지구 관측 시스템 데이터 포털 <http://edcimswww.cr.usgs.gov/pub/imswelcome/>`_

이 드라이버가 지원하는 개별 상품에 관한 문서:

-  `지리참조 ASTER L1B 데이터 <http://edcdaac.usgs.gov/aster/ASTER_GeoRef_FINAL.pdf>`_
-  `ASTER 표준 데이터 상품 사양 문서 <http://asterweb.jpl.nasa.gov/documents/ASTERHigherLevelUserGuideVer2May01.pdf>`_
-  `MODIS 1B수준 상품 정보 및 상태 <http://www.mcst.ssai.biz/mcstweb/L1B/product.html>`_
-  `MODIS 해양 사용자 용 지침서 <http://modis-ocean.gsfc.nasa.gov/userguide.html>`_
