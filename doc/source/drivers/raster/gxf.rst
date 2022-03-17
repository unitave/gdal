.. _raster.gxf:

================================================================================
GXF -- 그리드 교환 파일(Grid eXchange File)
================================================================================

.. shortname:: GXF

.. built_in_by_default::

이 포맷은 지오소프트(Geosoft) 사의 그리드 교환 포맷으로 중력장/자기장 분야에서 표준이 되었습니다. GDAL은 지리참조 정보 및 투영법 지원을 포함, GXF-3 파일 읽기를 지원합니다. (쓰기는 지원하지 않습니다.)

GDAL이 GXF 데이터셋에 반환하는 데이터 유형은 기본적으로 Float32입니다. GXF_DATATYPE 환경설정 옵션을 설정하면 데이터 유형을 지정할 수 있습니다. (현재 Float64를 지원합니다.)

`GXF-3 <https://web.archive.org/web/20130730111701/http://home.gdal.org/projects/gxf/index.html>`_ 페이지에서 지원하는 코드 및 포맷을 찾아볼 수 있습니다.

주의: ``gdal/frmts/gxf/gxfdataset.cpp`` 로 구현되었습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

.. supports_virtualio::

