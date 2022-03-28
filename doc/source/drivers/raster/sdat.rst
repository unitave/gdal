.. _raster.sdat:

================================================================================
SAGA -- SAGA GIS 바이너리 그리드 파일 포맷
================================================================================

.. shortname:: SAGA

.. built_in_by_default::

이 드라이버는 SAGA GIS 바이너리 그리드의 읽기 및 (생성, 삭제 및 복사를 포함하는) 쓰기를 모두 지원합니다. SAGA GIS 바이너리 그리드 데이터셋은 공통 기본명을 가진 아스키 헤더(.SGRD)와 바이너리 데이터(.SDAT) 파일로 이루어져 있습니다. 데이터셋에 접근하려면 .SDAT 파일을 선택해야 합니다.
GDAL 2.3버전부터, 이 드라이버는 .sgrd, .sdat 및 .prj 파일의 ZIP으로 압축한 .sg-grd-z 압축 파일을 읽어올 수 있습니다.

이 드라이버는 다음과 같은 SAGA 데이터 유형을 읽을 수 있습니다(괄호 안은 대응하는 GDAL 유형입니다):

   -  BIT (GDT_Byte)
   -  BYTE_UNSIGNED (GDT_Byte)
   -  BYTE (GDT_Byte)
   -  SHORTINT_UNSIGNED (GDT_UInt16)
   -  SHORTINT (GDT_Int16)
   -  INTEGER_UNSIGNED (GDT_UInt32)
   -  INTEGER (GDT_Int32)
   -  FLOAT (GDT_Float32)
   -  DOUBLE (GDT_Float64)

이 드라이버는 다음과 같은 SAGA 데이터 유형을 작성할 수 있습니다:

   -  BYTE_UNSIGNED (GDT_Byte)
   -  SHORTINT_UNSIGNED (GDT_UInt16)
   -  SHORTINT (GDT_Int16)
   -  INTEGER_UNSIGNED (GDT_UInt32)
   -  INTEGER (GDT_Int32)
   -  FLOAT (GDT_Float32)
   -  DOUBLE (GDT_Float64)

이 드라이버는 현재 1 이외의 zFactor를 지원하지 않으며, TOPTOBOTTOM 방식으로 작성된 SAGA 그리드를 읽을 수 없습니다.

주의: ``gdal/frmts/saga/sagadataset.cpp`` 로 구현되었습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::

