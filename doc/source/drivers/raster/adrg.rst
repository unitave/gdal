.. _raster.adrg:

================================================================================
ADRG -- ADRG/ARC 수치화 래스터 그래픽스 (.gen/.thf)
================================================================================

.. shortname:: ADRG

.. built_in_by_default::

GDAL이 읽기 접근을 위해 지원합니다. 생성 작업도 가능하지만, 실험적인 드라이버로 간주하고 읽기 접근을 테스트하기 위한 수단으로써만 사용해야 합니다. (다른 GIS 소프트웨어가 이 드라이버가 생성한 파일을 성공적으로 읽어올 수 있기는 하지만 말입니다.)

ADRG 데이터셋은 파일 몇 개로 이루어져 있습니다. GDAL이 인식하는 파일은 일반 정보(General Information) 파일(.GEN)입니다. GDAL은 실제 데이터가 있는 이미지 파일(.IMG)도 필요로 할 것입니다.

GDAL은 전송 헤더(Transmission Header) 파일(.THF)도 입력받을 수 있습니다. THF 파일이 하나 이상의 이미지를 참조하는 경우, GDAL은 THF 파일을 구성하고 있는 이미지들을 하위 데이터셋으로 리포트할 것입니다. THF 파일이 이미지 하나만 참조한다면, GDAL은 THF 파일을 직접 열 것입니다.

오버뷰, 범례 및 삽입 맵(inset)은 사용하지 않습니다. 극 구역(ARC 9 및 18구역)은 (테스트 데이터가 부족하기 때문에) 지원하지 않습니다.

참고: the `ADRG 사양
(MIL-A-89007) <http://earth-info.nga.mil/publications/specs/printed/89007/89007_ADRG.pdf>`__


드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::
