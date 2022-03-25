.. _raster.pcraster:

================================================================================
PCRaster -- PCRaster 래스터 파일 포맷
================================================================================

.. shortname:: PCRaster

.. build_dependencies:: (내부 제공 libcf)

GDAL은 PCRaster 래스터 파일 읽기 및 쓰기를 지원합니다. PCRaster는 분산 시뮬레이션(distributed simulation) 모델을 위한 동적 모델 작업 시스템입니다. PCRaster의 주 용처는 지리, 수문, 생태 등등의 환경 모델 작업입니다. 이에 대한 예를 들자면 지구 수문학 연구용 모델, 식생 경쟁 모델, 사면 안정성 모델과 토지이용 변경 모델 등을 포함합니다.

이 드라이버는 모든 PCRaster 맵 유형(booleans, nominal, ordinals, scalar, directional 및 ldd(local drain direction))을 읽어옵니다. 파일에 값을 저장하기 위해 쓰이는 셀 표현(cell representation)과 동일한 방식으로 메모리에 값을 저장합니다.

이 드라이버는 GDAL 래스터의 소스가 PCRaster인지 아닌지 여부를 탐지합니다. 이런 래스터를 파일로 작성할 때 원본 래스터의 값 척도(value scale)를 사용할 것입니다. 이 드라이버는 값 척도에 따라 **언제나** UINT1, INT4 또는 REAL4 셀 표현을 이용해서 값을 작성합니다.

============ ===================
값 척도      셀 표현
============ ===================
VS_BOOLEAN   CR_UINT1
VS_NOMINAL   CR_INT4
VS_ORDINAL   CR_INT4
VS_SCALAR    CR_REAL4
VS_DIRECTION CR_REAL4
VS_LDD       CR_UINT1
============ ===================

PCRaster 래스터 파일이 소스가 아닌 래스터의 경우, 다음 규칙에 따라 값 척도와 셀 표현을 결정합니다:

=============== =================== ==========================
소스 유형       대상 값 척도        대상 셀 표현
=============== =================== ==========================
GDT_Byte        VS_BOOLEAN          CR_UINT1
GDT_Int32       VS_NOMINAL          CR_INT4
GDT_Float32     VS_SCALAR           CR_REAL4
GDT_Float64     VS_SCALAR           CR_REAL4
=============== =================== ==========================

이 드라이버는 지원하는 어떤 셀 표현으로부터 지원하는 다른 셀 표현으로 값을 변환할 수 있습니다. 지원하지 않는 셀 표현을 변환하지는 못 합니다. 예를 들어 CR_INT2(GDT_Int16) 표현을 사용하는 값으로부터 PCRaster 래스터 파일을 작성할 수는 없습니다.

PCRaster 래스터 파일의 실질적인 확장자가 .map이지만, PCRaster 소프트웨어에서는 표준화된 파일 확장자가 필수가 아닙니다.


드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::


참고
----

-  ``gdal/frmts/pcraster/pcrasterdataset.cpp`` 로 구현되었습니다.

-  `위트레흐트(Utrecht) 대학교 PCRaster 웹사이트 <http://pcraster.geo.uu.nl>`_
