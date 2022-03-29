.. _raster.sigdem:

================================================================================
SIGDEM -- 크기 조정 정수 그리드 DEM
================================================================================

.. shortname:: SIGDEM

.. versionadded:: 2.4

.. built_in_by_default:: 

SIGDEM 드라이버는 `크기 조정 정수 그리드 DEM(Scaled Integer Gridded DEM) <https://github.com/revolsys/sigdem>`_ 파일의 읽기 및 쓰기를 지원합니다.

SIGDEM 파일은 정확히 1개의 밴드를 담고 있습니다. 인메모리(in-memory) 밴드 데이터는 GDT_Float64형을 사용해서 저장됩니다.

SIGDEM은 좌표계로 파일 안에 있는 EPSG ID를 사용하는 것을 선호합니다. 공간 좌표계가 EPSG ID를 가지고 있지 않은 경우에만 .prj 파일을 쓰거나 읽을 것입니다.

주의: ``gdal/frmts/sigdem/sigdemdataset.cpp`` 로 구현되었습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::

.. supports_georeferencing::

.. supports_virtualio::
