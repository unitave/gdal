.. _raster.NetCDF:

================================================================================
NetCDF: 네트워크 공통 데이터 형식
================================================================================

.. shortname:: NetCDF

.. build_dependencies:: libNetCDF

NetCDF 드라이버는 NetCDF 포맷 읽기 및 쓰기 접근을 지원합니다. 이 페이지에서는 래스터 지원에 관해서만 설명합니다. (:ref:`벡터 지원 <vector.NetCDF>` 에 대한 문서는 따로 있습니다.) NetCDF는 배열 지향 데이터 접근을 위한 인터페이스로 과학 데이터를 표현하기 위해 쓰입니다. NODATA 값을 사용할 수 있는 경우 채우기값 메타데이터 또는 missing_value 하위 호환성을 NODATA 값으로 보전합니다.

주의: ``gdal/frmts/NetCDF/NetCDFdataset.cpp`` 로 구현되었습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::

.. supports_create::

.. supports_georeferencing::

다중 이미지 처리(하위 데이터셋)
-------------------------------------

네트워크 공통 데이터 형식(Network Common Data Form)은 과학 데이터셋을 저장하기 위해 가장 자주 쓰이는 서로 다른 여러 배열들을 위한 컨테이너입니다. NetCDF 파일 1개가 데이터셋 여러 개를 담고 있을 수도 있습니다. 데이터셋들의 크기, 차원 개수가 다를 수도 있고 서로 다른 지역의 데이터를 표현할 수도 있습니다.

파일이 이미지로 보이는 NetCDF 배열 하나만 담고 있는 경우 직접 접근할 수도 있지만, 파일이 이미지 여러 개를 담고 있다면 2단계 과정을 거쳐 파일을 가져와야 합니다.

1단계는 gdalinfo를 이용해서 파일에 있는 구성요소 이미지(데이터셋)들의 리포트를 얻은 다음 gdal_translate를 이용해서 원하는 이미지를 가져오는 것입니다. gdalinfo 유틸리티가 입력 NetCDF 파일로부터 모든 다중 차원 하위 데이터셋 목록을 리포트합니다.

개별 이미지 이름은 SUBDATASET_n_NAME 메타데이터 항목에 할당되어 있습니다. 각 이미지의 설명은 SUBDATASET_n_DESC 메타데이터 항목에 있습니다. NetCDF 이미지의 경우 이 설명은 *NetCDF:filename:variable_name* 과 같은 서식을 따를 것입니다.

이때 *filename* 이 입력 파일의 이름이고 *variable_name* 이 파일 내에서 선택한 데이터셋입니다.

2단계는 **gdalinfo** 에 이 이름을 입력해서 해당 데이터셋에 대한 정보를 얻거나, **gdal_translate** 에 이 이름을 입력해서 데이터셋을 읽어오는 것입니다.

예를 들어 NetCDF 파일로부터 데이터를 읽어오려면:

::

   $ gdalinfo sst.nc
   Driver: NetCDF/Network Common Data Format
   Size is 512, 512
   Coordinate System is `'
   Metadata:
     NC_GLOBAL#title=IPSL  model output prepared for IPCC Fourth Assessment SRES A2 experiment
     NC_GLOBAL#institution=IPSL (Institut Pierre Simon Laplace, Paris, France)
     NC_GLOBAL#source=IPSL-CM4_v1 (2003) : atmosphere : LMDZ (IPSL-CM4_IPCC, 96x71x19) ; ocean ORCA2 (ipsl_cm4_v1_8, 2x2L31); sea ice LIM (ipsl_cm4_v
     NC_GLOBAL#contact=Sebastien Denvil, sebastien.denvil@ipsl.jussieu.fr
     NC_GLOBAL#project_id=IPCC Fourth Assessment
     NC_GLOBAL#table_id=Table O1 (13 November 2004)
     NC_GLOBAL#experiment_id=SRES A2 experiment
     NC_GLOBAL#realization=1
     NC_GLOBAL#cmor_version=9.600000e-01
     NC_GLOBAL#Conventions=CF-1.0
     NC_GLOBAL#history=YYYY/MM/JJ: data generated; YYYY/MM/JJ+1 data transformed  At 16:37:23 on 01/11/2005, CMOR rewrote data to comply with CF standards and IPCC Fourth Assessment requirements
     NC_GLOBAL#references=Dufresne et al, Journal of Climate, 2015, vol XX, p 136
     NC_GLOBAL#comment=Test drive
   Subdatasets:
     SUBDATASET_1_NAME=NetCDF:"sst.nc":lon_bnds
     SUBDATASET_1_DESC=[180x2] lon_bnds (64-bit floating-point)
     SUBDATASET_2_NAME=NetCDF:"sst.nc":lat_bnds
     SUBDATASET_2_DESC=[170x2] lat_bnds (64-bit floating-point)
     SUBDATASET_3_NAME=NetCDF:"sst.nc":time_bnds
     SUBDATASET_3_DESC=[24x2] time_bnds (64-bit floating-point)
     SUBDATASET_4_NAME=NetCDF:"sst.nc":tos
     SUBDATASET_4_DESC=[24x170x180] sea_surface_temperature (32-bit floating-point)Corner Coordinates:
   Upper Left  (    0.0,    0.0)
   Lower Left  (    0.0,  512.0)
   Upper Right (  512.0,    0.0)
   Lower Right (  512.0,  512.0)
   Center      (  256.0,  256.0)

이 NetCDF 파일은 lon_bnds, lat_bnds, tim_bnds 및 tos 데이터셋 4개를 담고 있습니다. 이제 ``NetCDF:"sst.nc":tos`` ``[24x17x180] sea_surface_temperature (32-bit floating-point)`` 라고 서술된 변수를 선택해서 그 안에 있는 밴드 개수에 관한 정보를 얻으려면:

::

   $ gdalinfo NetCDF:"sst.nc":tos
   Driver: NetCDF/Network Common Data Format
   Size is 180, 170
   Coordinate System is `'
   Origin = (1.000000,-79.500000)
   Pixel Size = (1.98888889,0.99411765)
   Metadata:
     NC_GLOBAL#title=IPSL  model output prepared for IPCC Fourth Assessment SRES A2 experiment
     NC_GLOBAL#institution=IPSL (Institut Pierre Simon Laplace, Paris, France)

...수많은 메타데이터 출력물을 건너뛰어서...

::

     time#standard_name=time
     time#long_name=time
     time#units=days since 2001-1-1
     time#axis=T
     time#calendar=360_day
     time#bounds=time_bnds
     time#original_units=seconds since 2001-1-1
   Corner Coordinates:
   Upper Left  (   1.0000000, -79.5000000)
   Lower Left  (   1.0000000,  89.5000000)
   Upper Right (     359.000,     -79.500)
   Lower Right (     359.000,      89.500)
   Center      ( 180.0000000,   5.0000000)
   Band 1 Block=180x1 Type=Float32, ColorInterp=Undefined
     NoData Value=1e+20
     Metadata:
       NetCDF_VARNAME=tos
       NetCDF_DIMENSION_time=15
       NetCDF_time_units=days since 2001-1-1
   Band 2 Block=180x1 Type=Float32, ColorInterp=Undefined
     NoData Value=1e+20
     Metadata:
       NetCDF_VARNAME=tos
       NetCDF_DIMENSION_time=45
       NetCDF_time_units=days since 2001-1-1

...더 많은 밴드를 출력합니다.

::

   Band 22 Block=180x1 Type=Float32, ColorInterp=Undefined
     NoData Value=1e+20
     Metadata:
       NetCDF_VARNAME=tos
       NetCDF_DIMENSION_time=645
       NetCDF_time_units=days since 2001-1-1
   Band 23 Block=180x1 Type=Float32, ColorInterp=Undefined
     NoData Value=1e+20
     Metadata:
       NetCDF_VARNAME=tos
       NetCDF_DIMENSION_time=675
       NetCDF_time_units=days since 2001-1-1
   Band 24 Block=180x1 Type=Float32, ColorInterp=Undefined
     NoData Value=1e+20
     Metadata:
       NetCDF_VARNAME=tos
       NetCDF_DIMENSION_time=705
       NetCDF_time_units=days since 2001-1-1

gdalinfo는 이 하위 데이터셋에 있는 밴드의 개수를 출력합니다. 각 밴드는 메타데이터를 가지고 있습니다. 이 예시에서는 메타데이터를 통해 각 밴드가 2001년 1월부터 측정한 월별 해수면 온도의 배열에 대응한다는 사실을 알 수 있습니다. 이 하위 데이터셋은 24개월치의 데이터를 담고 있습니다. **gdal_translate** 를 이용해서 이 하위 데이터셋을 읽어올 수도 있습니다.

GDAL에 **SUBDATASET_n_NAME** 로 표시된 줄의 내용을 **NetCDF:** 접두어를 포함해서 정확히 지정해야 한다는 사실을 기억하십시오.

**NetCDF:** 접두어가 맨 앞에 와야 합니다. 이 접두어는 하위 데이터셋 NetCDF 드라이버를 촉발합니다. 이 드라이버의 목적은 오직 원격 탐사 및 지리공간 데이터셋을 래스터 이미지 형태로 가져오는 것입니다. NetCDF 파일에 담겨 있는 모든 데이터를 탐색하길 바란다면 다른 도구를 사용해야 합니다.

GDAL 3.5버전부터, NetCDF 파일이 동일한 유형의 2차원 변수만 담고 있고 동일한 차원으로 색인되어 있는 경우 **VARIABLES_AS_BANDS=YES** 열기 옵션을 이용해서 드라이버에 이 하위 데이터셋들이 동일한 데이터셋의 다중 밴드로 리포트될 것이라는 사실을 알려줄 수 있습니다.

::

    $ gdalinfo autotest/gdrivers/data/NetCDF/two_vars_scale_offset.nc -oo VARIABLES_AS_BANDS=YES

    Driver: NetCDF/Network Common Data Format
    Files: autotest/gdrivers/data/NetCDF/two_vars_scale_offset.nc
    Size is 21, 21
    Metadata:
      NC_GLOBAL#Conventions=COARDS/CF-1.0
      x#actual_range={-10,10}
      x#long_name=x
      y#actual_range={-10,10}
      y#long_name=y
      z#add_offset=1.5
      z#long_name=z
      z#scale_factor=0.01
    Corner Coordinates:
    Upper Left  (    0.0,    0.0)
    Lower Left  (    0.0,   21.0)
    Upper Right (   21.0,    0.0)
    Lower Right (   21.0,   21.0)
    Center      (   10.5,   10.5)
    Band 1 Block=21x1 Type=Float32, ColorInterp=Undefined
      NoData Value=9.96920996838686905e+36
      Offset: 1.5,   Scale:0.01
      Metadata:
        add_offset=1.5
        long_name=z
        NetCDF_VARNAME=z
        scale_factor=0.01
    Band 2 Block=21x1 Type=Float32, ColorInterp=Undefined
      NoData Value=9.96920996838686905e+36
      Offset: 2.5,   Scale:0.1
      Metadata:
        add_offset=2.5
        long_name=q
        NetCDF_VARNAME=q
        scale_factor=0.1


차원
---------

NetCDF 드라이버는 데이터가 `UNIDATA <https://docs.unidata.ucar.edu/NetCDF-c/current/>`_ 의 CF-1 규범을 따른다고 가정합니다. NetCDF 파일 내부의 차원은 (Z,Y,X) 규칙을 사용합니다. 차원이 3개 이상인 경우, 이 드라이버는 해당 차원을 밴드로 병합합니다. 예를 들어 (P, T, Y, X) 유형의 4차원 배열이 있다고 하면 드라이버가 마지막 차원 2개를 곱할 (P*T) 것입니다. 드라이버는 밴드를 다음 순서로 표시합니다: 먼저 T를 증분(increment)시킨 다음 P를 증분시킬 것입니다. 메타데이터는 해당 T 및 P 값들과 함께 각 밴드에 표시될 것입니다.


지리참조
------------

NetCDF 파일에 지리참조 정보를 저장하는 보편적인 방법은 없습니다. 이 드라이버는 먼저 UNIDATA의 CF-1 규범을 따라 "grid_mapping"이라는 메타데이터를 검색합니다. "grid_mapping"이 존재하지 않는 경우, 드라이버가 지리변형 배열을 설정하기 위한 위도/경도 그리드 배열을 찾으려 시도할 것입니다. NetCDF 드라이버는 위도/경도 그리드가 균등한 간격으로 떨어져 있는지 검증합니다.

.. versionadded:: 3.4 crs_wkt 속성 지원

이 두 가지 메소드가 실패한 경우, NetCDF 드라이버는 다음 메타데이터를 직접 읽어와서 지리참조 정보를 설정하려 시도할 것입니다.

-  spatial_ref (WKT)
-  GeoTransform (지리변형 배열)

또는

-  Northernmost_Northing
-  Southernmost_Northing
-  Easternmost_Easting
-  Westernmost_Easting

이 습성을 제어하는 **GDAL_NetCDF_VERIFY_DIMS** 및 **GDAL_NetCDF_IGNORE_XY_AXIS_NAME_CHECKS** 환경설정 옵션도 참조하십시오.

열기 옵션
------------

다음 열기 옵션들을 사용할 수 있습니다:

-  **HONOUR_VALID_RANGE=YES/NO**:
   (GDAL 2.2버전 이후) valid_min, valid_max 또는 valid_range 속성이 알려주는 무결성(validity) 범위 바깥에 NODATA 픽셀값을 설정할지 여부를 선택합니다. 기본값은 YES입니다.

-  **IGNORE_XY_AXIS_NAME_CHECKS=YES/NO**:
   (GDAL 3.4.2 이상 버전) 규범적인 속성으로 확인되지 않은 경우에도 항상 X, Y 차원을 지리공간 축으로 간주해야 할지 여부를 선택합니다. 기본값은 NO입니다.

-  **VARIABLES_AS_BANDS=YES/NO**:
   (GDAL 3.5 이상 버전) NetCDF 파일이 동일한 유형의 2차원 변수만 담고 있고 동일한 차원으로 색인되어 있는 경우 이 옵션을 YES로 선택하면 이 하위 데이터셋들을 동일한 데이터셋의 다중 밴드로 리포트할 것입니다. 기본값은 NO입니다. (즉 각 변수를 개별 하위 데이터셋으로 리포트할 것입니다.)

생성 문제점
---------------

이 드라이버는 CF-1 규범을 따르는 NetCDF 파일 생성을 지원합니다. 2차원 데이터셋 집합을 생성할 수도 있습니다. 각 변수 배열은 Band1, Band2, ... BandN으로 명명됩니다.

각 밴드는 밴드가 담고 있는 데이터를 간략히 설명하는 메타데이터를 가지게 될 것입니다.

GDAL NetCDF 메타데이터
---------------------

모든 NetCDF 속성은 투명하게 GDAL 메타데이터로 변환됩니다.

이 변환 작업은 다음과 같은 규칙을 따릅니다:

-  전체 수준 NetCDF 메타데이터 앞에는 **NC_GLOBAL** 태그가 붙습니다.
-  데이터셋 수준 메타데이터 앞에는 메타데이터의 **변수 이름** 이 붙습니다.
-  각 접두어 뒤에는 **#** 기호가 붙습니다.
-  NetCDF 속성은 **이름=값** 형식을 따릅니다.

예시:

::

   $ gdalinfo NetCDF:"sst.nc":tos
   Driver: NetCDF/Network Common Data Format
   Size is 180, 170
   Coordinate System is `'
   Origin = (1.000000,-79.500000)
   Pixel Size = (1.98888889,0.99411765)
   Metadata:

NetCDF 전체 수준 속성

::

     NC_GLOBAL#title=IPSL  model output prepared for IPCC Fourth Assessment SRES A2 experiment

tos, lon, lat 및 time에 대한 변수 속성

::

     tos#standard_name=sea_surface_temperature
     tos#long_name=Sea Surface Temperature
     tos#units=K
     tos#cell_methods=time: mean (interval: 30 minutes)
     tos#_FillValue=1.000000e+20
     tos#missing_value=1.000000e+20
     tos#original_name=sosstsst
     tos#original_units=degC
     tos#history= At   16:37:23 on 01/11/2005: CMOR altered the data in the following ways: added 2.73150E+02 to yield output units;  Cyclical dimension was output starting at a different lon;
     lon#standard_name=longitude
     lon#long_name=longitude
     lon#units=degrees_east
     lon#axis=X
     lon#bounds=lon_bnds
     lon#original_units=degrees_east
     lat#standard_name=latitude
     lat#long_name=latitude
     lat#units=degrees_north
     lat#axis=Y
     lat#bounds=lat_bnds
     lat#original_units=degrees_north
     time#standard_name=time
     time#long_name=time
     time#units=days since 2001-1-1
     time#axis=T
     time#calendar=360_day
     time#bounds=time_bnds
     time#original_units=seconds since 2001-1-1

작성 작업 시 CreateCopy() 인터페이스 또는 gdal_translate를 사용하는 경우, NC_GLOBAL#키=값 명명 규범을 따르는 데이터셋 수준 메타데이터를 사용해서 NetCDF 속성을 작성할 것입니다. 밴드 수준에서도 키=값으로 설정되는 메타데이터를 사용해서 변수 속성을 작성할 것입니다.

상품 특화 습성
--------------------------

Sentinel 5
++++++++++

.. versionadded:: 3.4

다음 메타데이터 도메인의 메타데이터가 가장 장황하게 리포트됩니다:

-  ``json:ISO_METADATA``
-  ``json:ESA_METADATA``
-  ``json:EOP_METADATA``
-  ``json:QA_STATISTICS``
-  ``json:GRANULE_DESCRIPTION``
-  ``json:ALGORITHM_SETTINGS``
-  ``json:SUPPORT_DATA``

다음과 같은 명령어로 찾아볼 수 있습니다:

::

    gdalinfo -mdd all -json S5P.nc


생성 옵션
----------------

-  **FORMAT=[NC/NC2/NC4/NC4C]**:
   사용할 NetCDF 파일 포맷을 설정합니다. 기본값은 NC입니다. NC2는 최근 NetCDF 설치본이라면 일반적으로 지원하지만, NC4 및 NC4C를 지원하려면 NetCDF가 NetCDF-4 (그리고 HDF5) 지원과 함께 컴파일되어 있어야 합니다.

-  **COMPRESS=[NONE/DEFLATE]**:
   사용할 압축 방식을 설정합니다. NetCDF가 NetCDF-4 지원과 함께 컴파일된 경우에만 DEFLATE를 사용할 수 있습니다. DEFLATE 압축을 설정한 경우 기본값은 NC4C입니다.

-  **ZLEVEL=[1-9]**:
   DEFLATE 압축을 사용하는 경우 압축 수준을 설정합니다. 9가 최고 압축, 1이 최저 압축입니다. 기본값은 1로, 최고의 압축 시간과 압축률을 보여줍니다.

-  **WRITE_BOTTOMUP=[YES/NO]**:
   데이터를 내보낼 때 드라이버가 탐지한 Y축 순서를 대체할지 선택합니다. NetCDF 파일은 보통 "아래를 위로(bottom-up)" 순서를 취하는데, 이는 GDAL 모델의 "북쪽을 위로(north up)" 순서와 정반대입니다. 일반적으로는 Y축 순서에 문제를 일으키지 않지만, Y축 지리참조 정보가 없는 경우는 다릅니다. 이 옵션의 기본값은 YES입니다. 즉 파일들을 NetCDF 기본값인 "아래를 위로" 순서로 내보낼 것이라는 뜻입니다. 가져오기의 경우 아래에 있는 GDAL_NetCDF_BOTTOMUP 환경설정 옵션을 참조하십시오.

-  **WRITE_GDAL_TAGS=[YES/NO]**:
   CF 태그에 추가로 지리참조에 쓰인 GDAL 태그(spatial_ref 및 GeoTransform)를 내보내야 할지 여부를 선택합니다. CF 태그에 (유명한 원점 및 EPSG 코드 같은) 모든 정보가 저장돼 있지는 않기 때문에 드라이버가 기본적으로 이런 변수를 내보냅니다. 가져오기 작업 시 CF "grid_mapping" 변수를 우선하고, GDAL 태그가 CF 메타데이터와 충돌하지 않는다면 GDAL 태그를 사용합니다. GDAL 버전 4에서는 spatial_ref를 내보내지 않고 대신 crs_wkt CF 메타데이터 속성을 사용할 것입니다.

-  **WRITE_LONLAT=[YES/NO/IF_NEEDED]**:
   파일에 CF 경도/위도 변수를 작성할지 여부를 선택합니다. 기본값은 지리 공간 좌표계의 경우 YES, 투영 공간 좌표계의 경우 NO 입니다. GDAL과 다른 많은 응용 프로그램이 X, Y 차원 변수와 CF 투영법 정보를 사용하기 때문에 투영 공간 좌표계의 경우 보통 이 옵션은 필요없습니다. IF_NEEDED로 설정하면 투영법이 CF-1.5 표준에 속하지 않는 경우 경도/위도 변수를 생성합니다.

-  **TYPE_LONLAT=[float/double]**:
   경도/위도 변수에 사용할 변수 유형을 설정합니다. 기본값은 지리 공간 좌표계의 경우 Double형, 투영 공간 좌표계의 경우 부동소수점형입니다. 투영 공간 좌표계에 경도/위도 변수를 작성하는 경우, (각 변수가 X*Y 공간을 사용하기 때문에) 파일 용량이 상당히 커지게 됩니다. 따라서 TYPE_LONLAT=float일 때 디스크 공간을 절약하기 위해 COMPRESS=DEFLATE를 함께 사용하는 것을 권장합니다.

-  **PIXELTYPE=[DEFAULT/SIGNEDBYTE]**:
   이 옵션을 SIGNEDBYTE로 설정하면 새 바이트형 파일을 강제로 부호 있는 바이트형으로 작성할 수 있습니다.

-  **WRITE_GDAL_VERSION=[YES/NO]**: (GDAL 3.5.0 이상 버전)
   파일 생성 시 GDAL 버전 앞에 "GDAL" 텍스트 전체 수준 속성을 추가해야 할지 여부를 선택합니다. 기본값은 YES입니다.

-  **WRITE_GDAL_HISTORY=[YES/NO]**: (GDAL 3.5.0 이상 버전)
   파일 생성 시 날짜/시간 및 GDAL 정보 앞에 "history" 전체 수준 속성을 추가해야 할지 여부를 선택합니다. 기본값은 YES입니다.

CreateCopy() 2D 래스터 API를 이용한 다중 차원 파일 생성
------------------------------------------------------------------

GDAL 3.1버전부터, 2차원을 초과하는 파일을 생성하는 경우 :ref:`multidim_raster_data_model` API를 사용하는 방식을 선호합니다. 하지만 CreateCopy() 메소드를 이용해서 이런 파일을 2차원 래스터 API로 생성할 수도 있습니다. (파일 쓰기 작업 시 Create() 메소드 사용은 지원하지 않는다는 사실을 기억하십시오.)

소스 데이터 상에 ``NetCDF_DIM_EXTRA={dim1_name,...dimN_name}`` 메타데이터 항목이 반드시 설정되어 있어야만 합니다. 이때 dim1_name이 가장 느리게 변화하는 차원이고 dimN_name은 가장 빠르게 변화하는 차원입니다.

각 추가 차원에 ``NetCDF_DIM_{dim_name}_DEF={dimension_size,NetCDF_data_type}`` 메타데이터 항목이 반드시 설정되어 있어야만 합니다. 이때 dimension_size가 차원의 크기(해당 차원을 따라 존재하는 샘플 개수)이며 NetCDF_data_type은 각 차원에 대응하는 색인 변수(indexing variable)의 NetCDF 데이터 유형을 나타내는 정수값입니다. 다음은 이 가운데 가장 유용한 데이터 유형입니다:

- 4: Int
- 5: Float
- 6: Double
- 10: Int64

차원에 대응하는 색인 변수의 값을 정의하기 위한 ``NetCDF_DIM_{dim_name}_VALUES={value1,...valueN}`` 을 설정합니다.

차원에 대응하는 색인 변수의 속성을 정의하기 위한 ``dim_name#attribute`` 메타데이터 항목도 설정할 수 있습니다.

다음은 파이썬으로 Time,Z,Y,X 4D 파일을 생성하는 예시입니다:

.. code-block:: python

    # Create in-memory file with required metadata to define the extra >2D
    # dimensions
    size_z = 2
    size_time = 3
    src_ds = gdal.GetDriverByName('MEM').Create('', 4, 3, size_z * size_time)
    src_ds.SetMetadataItem('NetCDF_DIM_EXTRA', '{time,Z}')
    # 6 is NC_DOUBLE
    src_ds.SetMetadataItem('NetCDF_DIM_Z_DEF', f"{{{size_z},6}}")
    src_ds.SetMetadataItem('NetCDF_DIM_Z_VALUES', '{1.25,2.50}')
    src_ds.SetMetadataItem('Z#axis', 'Z')
    src_ds.SetMetadataItem('NetCDF_DIM_time_DEF', f"{{{size_time},6}}")
    src_ds.SetMetadataItem('NetCDF_DIM_time_VALUES', '{1,2,3}')
    src_ds.SetMetadataItem('time#axis', 'T')
    src_ds.SetGeoTransform([2,1,0,49,0,-1])

    # Create NetCDF file
    gdal.GetDriverByName('NetCDF').CreateCopy('out.nc', src_ds)


환경설정 옵션
---------------------

-  **GDAL_NetCDF_BOTTOMUP=[YES/NO]**:
   데이터를 가져올 때 드라이버가 탐지한 Y축 순서를 대체할지 선택합니다.
   특정 데이터셋이 문제를 발생시키지 않는 이상 이 옵션을 사용할 필요는 거의 없습니다.
   (문제가 발생하는 경우 `GDAL Trac <https://github.com/OSGeo/gdal>`_ 으로 리포트해주십시오.)

-  **GDAL_NetCDF_VERIFY_DIMS=[YES/STRICT]**:
   STRICT로 설정하면 어떤 차원이 위도 또는 경도를 나타내는지 해당 차원의 속성만으로 추정하려 합니다.
   또는 YES로 설정하면 차원의 이름으로 추정합니다. 기본값은 YES입니다.

-  **GDAL_NetCDF_IGNORE_XY_AXIS_NAME_CHECKS=[YES/NO]**:
   규범적인 속성으로 확인되지 않은 경우에도 항상 X, Y 차원을 지리공간 축으로 간주해야 할지 여부를 선택합니다. 기본값은 NO입니다.

VSI 가상 파일 시스템 API 지원
-----------------------------------

GDAL 2.4버전부터, 리눅스 커널이 4.3버전 이상이고 libNetCDF가 4.5버전 이상인 경우 /vsi 파일 시스템 상의 읽기 작업을 지원합니다.

읽기 작업 시 NetCDF-4 그룹 지원 (GDAL 3.0이상 버전)
------------------------------------------------

이 드라이버는 GDAL 3.0버전에서 읽기 작업 시 NetCDF-4 그룹을 지원하기 위해 엄청난 변화를 겪었습니다:

-  하위 데이터셋 목록을 생성하기 위해 내포된 모든 그룹들을 재귀적으로 탐색합니다.

-  내포 그룹에 있는 하위 데이터셋들은, NetCDF-3 드라이버와의 하위 호환성을 위한 슬래시가 앞에 붙지 않는 루트 그룹에 있는 변수를 제외하면, /group1/group2/.../groupn/var 표준 NetCDF-4 규범을 사용합니다.

-  각 내포 그룹의 전체 수준 속성은 동일한 /group1/group2/.../groupn/NC_GLOBAL#attr_name 규범을 사용해서 GDAL 데이터셋 메타데이터로 수집됩니다. 이때에도 하위 호환성을 위한 슬래시가 앞에 붙지 않는 루트 그룹의 속성은 제외됩니다.

-  선택한 하위 데이터셋에 관한 -- 좌표 변수 또는 grid_mapping 같은 -- 보조 정보를 담고 있는 변수를 검색하는 경우, 이제 `CF 그룹 지원 <https://github.com/cf-convention/cf-conventions/issues/144>`_ 에 지정된 대로 상위 그룹들은 물론 그 하위 그룹들까지 검색합니다.

다중 차원 API 지원
----------------------------

.. versionadded:: 3.1

NetCDF 드라이버는 읽기 및 생성 작업을 위해 :ref:`multidim_raster_data_model` 을 지원합니다.

:cpp:func:`GDALGroup::GetGroupNames` 메소드는 다음 옵션을 지원합니다:

-  GROUP_BY=SAME_DIMENSION:
   이 옵션을 설정하면, 단일 차원 변수를 "가상" 하위 그룹으로 노출시킬 것입니다. 이렇게 하면 사용자가 변수 구조를 더 확실히 알 수 있습니다. 예를 들어 서로 다른 궤도에 속해 있는 변수들이 서로 다른 차원으로 색인되지만 같은 NetCDF 그룹에 섞여 있는 데이터셋 같은 경우 말입니다.

:cpp:func:`GDALGroup::OpenGroup` 메소드는 다음 옵션을 지원합니다:

-  GROUP_BY=SAME_DIMENSION:
   앞의 설명을 참조하십시오.

:cpp:func:`GDALGroup::GetMDArrayNames` 메소드는 다음 옵션들을 지원합니다:

-  SHOW_ALL=YES/NO:
   기본값은 NO입니다. YES로 설정하면, 모든 변수를 목록화합니다.
-  SHOW_ZERO_DIM=YES/NO:
   기본값은 NO입니다. NO로 설정하면, 목록에서 0차원을 가진 변수를 뺄 것입니다.
-  SHOW_COORDINATES=YES/NO:
   기본값은 YES입니다. NO로 설정하면, 목록에서 다른 변수의 ``coordinates`` 속성에 참조된 변수를 뺄 것입니다.
-  SHOW_BOUNDS=YES/NO:
   기본값은 YES입니다. NO로 설정하면, 목록에서 다른 변수의 ``bounds`` 속성에 참조된 변수를 뺄 것입니다.
-  SHOW_INDEXING=YES/NO:
   기본값은 YES입니다. NO로 설정하면, 목록에서 자신의 색인 변수와 같은 이름을 가진 단일 차원 변수를 뺄 것입니다.
-  SHOW_TIME=YES/NO:
   기본값은 YES입니다. NO로 설정하면, 목록에서 ``standard_name`` 속성이 "time"인 단일 차원 변수를 뺄 것입니다.
-  GROUP_BY=SAME_DIMENSION:
   이 옵션을 설정하면, 목록에서 단일 차원 변수를 뺄 것입니다.

:cpp:func:`GDALGroup::CreateMDArray` 메소드는 다음 옵션들을 지원합니다:

-  NC_TYPE=NC_CHAR/NC_BYTE/NC_INT64/NC_UINT64:
   보통 CreateMDArray()에 전송되는 GDAL 데이터 유형으로부터 추측하는 NetCDF 데이터 유형을 대체합니다. NC_CHAR는 고정 크기의 문자열에만 사용할 수 있습니다.
-  BLOCKSIZE=size_dim0,size_dim1,...,size_dimN:
   nc_def_var_chunking()이 설정하는 대로 NetCDF 덩어리(chunk) 크기를 설정합니다. 값의 개수가 딱 CreateMDArray()에 전송되는 차원의 개수만큼이어야만 합니다.
-  COMPRESS=DEFLATE:
   DEFLATE 압축을 요청합니다.
-  ZLEVEL=number:
   DEFLATE 압축 수준을 설정합니다. (1-9)
-  CHECKSUM=YES/NO:
   Fletcher32 체크섬을 활성화할지 여부를 선택합니다. 체크섬 생성에는 덩어리 작업이 필요한데, BLOCKSIZE 옵션으로 덩어리 작업을 명확하게 요청하지 않는다면 기본 덩어리 크기를 사용할 것입니다. 기본값은 NO입니다.
-  FILTER=filterid,param1,...,paramN:
   파일 쓰기에 사용되는 (보통 압축 메소드) 필터를 정의합니다. 쉼표로 구분된 숫자값이어야 합니다.
   첫 번째 값은 필터 ID이며 (`사용할 수 있는 값의 목록 <https://support.hdfgroup.org/services/contributions.html#filters>`_) 그 뒤에 오는 값들은 필터 별 파라미터들입니다.
   `여기 <https://www.unidata.ucar.edu/software/NetCDF/docs/md__Users_wfisher_Desktop_docs_NetCDF-c_docs_filters.html>`_ 에서 NetCDF-4 필터 지원에 대한 자세한 정보를 찾아볼 수 있습니다.
  

드라이버 빌드 작업
----------------

이 드라이버는 UNIDATA NetCDF 라이브러리와 함께 컴파일되었습니다.

GDAL을 NetCDF를 지원하도록 환경설정하기 전에 NetCDF 라이브러리를 다운로드하거나 컴파일해야 합니다.

HDF4, NetCDF-4 및 HDF5 관련 빌드 지침 및 정보를 알고 싶다면 `NetCDF GDAL 위키 <http://trac.osgeo.org/gdal/wiki/NetCDF>`_ 를 참조하십시오.

참고
---------

-  :ref:`NetCDF 드라이버의 벡터 지원 <vector.NetCDF>`

-  `NetCDF CF-1.5 규범 <http://cf-pcmdi.llnl.gov/documents/cf-conventions/1.5/cf-conventions.html>`_

-  `NetCDF로 컴파일된 라이브러리 <http://www.unidata.ucar.edu/downloads/NetCDF/index.jsp>`_

-  `NetCDF 문서 <http://www.unidata.ucar.edu/software/NetCDF/docs/>`_
