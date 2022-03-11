.. _raster.derived:

================================================================================
DERIVED -- 파생된 하위 데이터셋 드라이버
================================================================================

.. shortname:: DERIVED

.. built_in_by_default::

이 드라이버는 입력 데이터셋으로부터 파생된 하위 데이터셋에 접근할 수 있게 해줍니다. 이 파생된 데이터셋들은 원본 데이터셋과 동일한 투영법 참조, 지리변형 및 메타데이터를 가지고 있지만, GDAL 픽셀 함수를 이용해서 새 픽셀 값을 파생시킵니다.

사용할 수 있는 함수들
-------------------

다음과 같은 파생 데이터셋을 사용할 수 있습니다:

-  AMPLITUDE: 입력 밴드로부터 나온 픽셀들의 진폭
-  PHASE: 입력 밴드로부터 나온 픽셀들의 페이즈(phase)
-  REAL: 입력 밴드로부터 나온 픽셀들의 실수 부분
-  IMAG: 입력 밴드로부터 나온 픽셀들의 허수 부분
-  CONJ: 입력 밴드로부터 나온 픽셀들의 켤레(conjugate)
-  INTENSITY: 입력 밴드로부터 나온 픽셀들의 강도(진폭의 제곱)
-  LOGAMPLITUDE: 입력 밴드로부터 나온 픽셀들의 진폭의 Log10

주의: 복소수 데이터 유형이 아닌 경우, LOGAMPLITUDE만 사용할 수 있습니다.

일반적으로 모든 복소수 데이터셋의 진폭, 페이즈 또는 진폭 로그에 직접 접근하기 위해 사용됩니다.

파생 하위 데이터셋에 접근
-----------------------------

파생 하위 데이터셋은 DERIVED_SUBDATASETS 메타데이터 도메인에 저장되며, 다음 문법을 사용해서 접근할 수 있습니다:

::

     DERIVED_SUBDATASET:FUNCTION:dataset_name

이때 함수는 AMPLITUDE, PHASE, REAL, IMAG, CONJ, INTENSITY, LOGAMPLITUDE 가운데 하나입니다. 따라서 숫자의 정확도를 보장하기 위해 모든 파생 하위 데이터셋 밴드는 (사용한 함수에 따라) Float64 또는 CFloat64 정확도를 가지게 될 것입니다.

예시:

::

     $ gdalinfo cint_sar.tif

::

   Driver: GTiff/GeoTIFF
   Files: cint_sar.tif
   Size is 5, 6
   Coordinate System is `'
   GCP Projection =
   GEOGCS["WGS 84",
       DATUM["WGS_1984",
           SPHEROID["WGS 84",6378137,298.257223563,
               AUTHORITY["EPSG","7030"]],
           AUTHORITY["EPSG","6326"]],
       PRIMEM["Greenwich",0],
       UNIT["degree",0.0174532925199433],
       AUTHORITY["EPSG","4326"]]
   GCP[  0]: Id=1, Info=
             (-1910.5,-7430.5) -> (297.507,16.368,0)
   GCP[  1]: Id=2, Info=
             (588.5,-7430.5) -> (297.938,16.455,0)
   GCP[  2]: Id=3, Info=
             (588.5,7363.5) -> (297.824,16.977,0)
   GCP[  3]: Id=4, Info=
             (-1910.5,7363.5) -> (297.393,16.89,0)
   Metadata:
     AREA_OR_POINT=Area
     CEOS_ACQUISITION_TIME=19970718024119087
     CEOS_ELLIPSOID=GEM6
     CEOS_INC_ANGLE=24.824
     CEOS_LINE_SPACING_METERS=3.9900000
     CEOS_LOGICAL_VOLUME_ID=0001667400297672
     CEOS_PIXEL_SPACING_METERS=7.9040000
     CEOS_PIXEL_TIME_DIR=INCREASE
     CEOS_PLATFORM_HEADING=347.339
     CEOS_PLATFORM_LATITUDE=16.213
     CEOS_PLATFORM_LONGITUDE=-65.311
     CEOS_PROCESSING_AGENCY=ESA
     CEOS_PROCESSING_COUNTRY=ITALY
     CEOS_PROCESSING_FACILITY=ES
     CEOS_SEMI_MAJOR=6378.1440000
     CEOS_SEMI_MINOR=6356.7590000
     CEOS_SENSOR_CLOCK_ANGLE=90.000
     CEOS_SOFTWARE_ID=ERS2-SLC-6.1
     CEOS_TRUE_HEADING=345.5885834
   Image Structure Metadata:
     INTERLEAVE=BAND
   Corner Coordinates:
   Upper Left  (    0.0,    0.0)
   Lower Left  (    0.0,    6.0)
   Upper Right (    5.0,    0.0)
   Lower Right (    5.0,    6.0)
   Center      (    2.5,    3.0)
   Band 1 Block=5x6 Type=CInt16, ColorInterp=Gray

::

     $ gdalinfo DERIVED_SUBDATASET:LOGAMPLITUDE:cint_sar.tif

::

   Driver: DERIVED/Derived datasets using VRT pixel functions
   Files: cint_sar.tif
   Size is 5, 6
   Coordinate System is `'
   GCP Projection =
   GEOGCS["WGS 84",
       DATUM["WGS_1984",
           SPHEROID["WGS 84",6378137,298.257223563,
               AUTHORITY["EPSG","7030"]],
           AUTHORITY["EPSG","6326"]],
       PRIMEM["Greenwich",0],
       UNIT["degree",0.0174532925199433],
       AUTHORITY["EPSG","4326"]]
   GCP[  0]: Id=1, Info=
             (-1910.5,-7430.5) -> (297.507,16.368,0)
   GCP[  1]: Id=2, Info=
             (588.5,-7430.5) -> (297.938,16.455,0)
   GCP[  2]: Id=3, Info=
             (588.5,7363.5) -> (297.824,16.977,0)
   GCP[  3]: Id=4, Info=
             (-1910.5,7363.5) -> (297.393,16.89,0)
   Metadata:
     AREA_OR_POINT=Area
     CEOS_ACQUISITION_TIME=19970718024119087
     CEOS_ELLIPSOID=GEM6
     CEOS_INC_ANGLE=24.824
     CEOS_LINE_SPACING_METERS=3.9900000
     CEOS_LOGICAL_VOLUME_ID=0001667400297672
     CEOS_PIXEL_SPACING_METERS=7.9040000
     CEOS_PIXEL_TIME_DIR=INCREASE
     CEOS_PLATFORM_HEADING=347.339
     CEOS_PLATFORM_LATITUDE=16.213
     CEOS_PLATFORM_LONGITUDE=-65.311
     CEOS_PROCESSING_AGENCY=ESA
     CEOS_PROCESSING_COUNTRY=ITALY
     CEOS_PROCESSING_FACILITY=ES
     CEOS_SEMI_MAJOR=6378.1440000
     CEOS_SEMI_MINOR=6356.7590000
     CEOS_SENSOR_CLOCK_ANGLE=90.000
     CEOS_SOFTWARE_ID=ERS2-SLC-6.1
     CEOS_TRUE_HEADING=345.5885834
   Corner Coordinates:
   Upper Left  (    0.0,    0.0)
   Lower Left  (    0.0,    6.0)
   Upper Right (    5.0,    0.0)
   Lower Right (    5.0,    6.0)
   Center      (    2.5,    3.0)
   Band 1 Block=5x6 Type=Float64, ColorInterp=Undefined

사용할 수 있는 하위 데이터셋 목록
-----------------------------

DERIVED_SUBDATASETS 메타데이터 도메인에 사용할 수 있는 하위 데이터셋들을 리포트합니다. 입력 데이터셋에 사용할 수 있는 함수만 리포트할 것입니다. 즉 데이터셋이 복소수 유형 밴드를 최소한 1개 이상 가지고 있는 경우에만 AMPLITUDE, PHASE, REAL, IMAG, CONJ 및 INTENSITY를 리포트할 것입니다. 그럼에도, 리포트되지 않았더라도 앞에서 설명한 문법으로 파생 데이터셋에 접근할 수 있습니다.

::

       $ gdalinfo -mdd DERIVED_SUBDATASETS cint_sar.tif


::

   Driver: GTiff/GeoTIFF
   Files: cint_sar.tif
   Size is 5, 6
   Coordinate System is `'
   GCP Projection =
   GEOGCS["WGS 84",
       DATUM["WGS_1984",
           SPHEROID["WGS 84",6378137,298.257223563,
               AUTHORITY["EPSG","7030"]],
           AUTHORITY["EPSG","6326"]],
       PRIMEM["Greenwich",0],
       UNIT["degree",0.0174532925199433],
       AUTHORITY["EPSG","4326"]]
   GCP[  0]: Id=1, Info=
             (-1910.5,-7430.5) -> (297.507,16.368,0)
   GCP[  1]: Id=2, Info=
             (588.5,-7430.5) -> (297.938,16.455,0)
   GCP[  2]: Id=3, Info=
             (588.5,7363.5) -> (297.824,16.977,0)
   GCP[  3]: Id=4, Info=
             (-1910.5,7363.5) -> (297.393,16.89,0)
   Metadata:
     AREA_OR_POINT=Area
     CEOS_ACQUISITION_TIME=19970718024119087
     CEOS_ELLIPSOID=GEM6
     CEOS_INC_ANGLE=24.824
     CEOS_LINE_SPACING_METERS=3.9900000
     CEOS_LOGICAL_VOLUME_ID=0001667400297672
     CEOS_PIXEL_SPACING_METERS=7.9040000
     CEOS_PIXEL_TIME_DIR=INCREASE
     CEOS_PLATFORM_HEADING=347.339
     CEOS_PLATFORM_LATITUDE=16.213
     CEOS_PLATFORM_LONGITUDE=-65.311
     CEOS_PROCESSING_AGENCY=ESA
     CEOS_PROCESSING_COUNTRY=ITALY
     CEOS_PROCESSING_FACILITY=ES
     CEOS_SEMI_MAJOR=6378.1440000
     CEOS_SEMI_MINOR=6356.7590000
     CEOS_SENSOR_CLOCK_ANGLE=90.000
     CEOS_SOFTWARE_ID=ERS2-SLC-6.1
     CEOS_TRUE_HEADING=345.5885834
   Metadata (DERIVED_SUBDATASETS):
     DERIVED_SUBDATASET_1_NAME=DERIVED_SUBDATASET:AMPLITUDE:cint_sar.tif
     DERIVED_SUBDATASET_1_DESC=Amplitude of input bands from cint_sar.tif
     DERIVED_SUBDATASET_2_NAME=DERIVED_SUBDATASET:PHASE:cint_sar.tif
     DERIVED_SUBDATASET_2_DESC=Phase of input bands from cint_sar.tif
     DERIVED_SUBDATASET_3_NAME=DERIVED_SUBDATASET:REAL:cint_sar.tif
     DERIVED_SUBDATASET_3_DESC=Real part of input bands from cint_sar.tif
     DERIVED_SUBDATASET_4_NAME=DERIVED_SUBDATASET:IMAG:cint_sar.tif
     DERIVED_SUBDATASET_4_DESC=Imaginary part of input bands from cint_sar.tif
     DERIVED_SUBDATASET_5_NAME=DERIVED_SUBDATASET:CONJ:cint_sar.tif
     DERIVED_SUBDATASET_5_DESC=Conjugate of input bands from cint_sar.tif
     DERIVED_SUBDATASET_6_NAME=DERIVED_SUBDATASET:INTENSITY:cint_sar.tif
     DERIVED_SUBDATASET_6_DESC=Intensity (squared amplitude) of input bands from cint_sar.tif
     DERIVED_SUBDATASET_7_NAME=DERIVED_SUBDATASET:LOGAMPLITUDE:cint_sar.tif
     DERIVED_SUBDATASET_7_DESC=log10 of amplitude of input bands from cint_sar.tif
   Image Structure Metadata:
     INTERLEAVE=BAND
   Corner Coordinates:
   Upper Left  (    0.0,    0.0)
   Lower Left  (    0.0,    6.0)
   Upper Right (    5.0,    0.0)
   Lower Right (    5.0,    6.0)
   Center      (    2.5,    3.0)
   Band 1 Block=5x6 Type=CInt16, ColorInterp=Gray

참고:
---------

-  :ref:`GDAL VRT 예제의 파생 밴드 사용하기 부분 <vrt_derived_bands>`
