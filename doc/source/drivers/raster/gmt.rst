.. _raster.gmt:

================================================================================
GMT -- GMT 호환 netCDF
================================================================================

.. shortname:: GMT

.. build_dependencies:: libnetcdf

GDAL은 netCDF *그리드* 파일 읽기 및 쓰기를 제한적으로 지원합니다. 이 드라이버는 그리드로 식별되지 않는 (차원이라 불리는 변수들 및 Z가 없는) NetCDF 파일을 조용히 무시할 것입니다. 이 드라이버는 `GMT <http://gmt.soest.hawaii.edu/>`_ 패키지와의 그리드 교환을 위한 메커니즘을 우선적으로 제공하기 위해 개발되었습니다. 더 일반적인 netCDF 데이터셋에 대해서는 netCDF 드라이버를 사용해야 합니다.

파일에 있는 단위 정보는 무시할 것이지만, 래스터의 지리참조 범위를 얻기 위해 x_range와 y_range 정보를 읽어올 것입니다. 모든 netCDF 데이터 유형 읽기를 지원할 것입니다.

새로 생성된 (``GMT`` 유형의) 파일은 언제나 x, y 및 z에 대해 "meters" 단위를 사용하지만, x_range, y_range 및 z_range는 정확할 것입니다. netCDF 데이터는 부호 없는 바이트 데이터 유형을 가지고 있지 않기 때문에, 8비트 래스터를 GMT로 내보내기 위해서는 일반적으로 Int16형으로 벼환해야 할 것입니다.

GDAL의 NetCDF 지원은 선택적인 옵션으로, 기본적으로 함께 컴파일되지 않습니다.

주의: ``gdal/frmts/netcdf/gmtdataset.cpp`` 로 구현되었습니다.

참고: `유니데이터 NetCDF 페이지 <http://www.unidata.ucar.edu/software/netcdf/>`_

드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::

.. supports_georeferencing::
