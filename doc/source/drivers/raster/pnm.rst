.. _raster.pnm:

================================================================================
PNM -- Netpbm (.pgm, .ppm)
================================================================================

.. shortname:: PNM

.. built_in_by_default::

GDAL은 Netpbm 도구와 호환되는 (회색조) .pgm 파일과 (RGB 색상) .ppm 파일 읽기 및 생성을 지원합니다. 바이너리(RAW) 포맷만 지원합니다.

이 드라이버는 Netpbm 파일을 PNM 유형 가운데 하나로 생성할 수 있습니다.


Driver capabilities
-------------------

.. supports_createcopy::

.. supports_virtualio::


생성 옵션
---------

-  **MAXVAL=n**:
   산출 PNM 파일의 최대 색상값을 **n** 으로 강제 설정합니다. PNM 파일의 네이티브 최대 색상값을 허용하지 않는 소프트웨어에서 산출 파일을 사용하려 하는 경우 유용할 수도 있습니다.

주의: ``gdal/frmts/raw/pnmdataset.cpp`` 로 구현되었습니다.

