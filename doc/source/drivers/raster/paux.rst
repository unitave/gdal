.. _raster.paux:

================================================================================
PAux -- PCI .aux 명찰 RAW 포맷
================================================================================

.. shortname:: PAux

.. built_in_by_default::

GDAL은 PCI .aux 명찰(labelled) RAW 래스터 파일의 읽기, 쓰기 및 생성 지원을 부분적으로 구현했습니다. PCI 명찰 파일을 열려면 RAW 데이터 파일 자체를 선택하십시오. (공통 기본명을 가지고 있어야만 하는) .aux 파일은 자동으로 확인할 것입니다.

새 파일을 생성하는 경우 포맷 유형은 ``PAux`` 입니다. 모든 PCI 데이터 유형(8U, 16U, 16S 및 32R)을 지원합니다. 현재 지리참조, 투영법 및 기타 메타데이터는 무시합니다.


드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::

.. supports_create::

.. supports_virtualio::


생성 옵션
--------

-  **INTERLEAVE=PIXEL/LINE/BAND**:
   산출물의 교차삽입 방식을 설정합니다. 기본값은 BAND입니다.
   GDAL 3.5버전부터, INTERLEAVE 메타데이터 항목을 노출시키는 다중 밴드를 가진 소스 데이터셋으로부터 복사할 때 INTERLEAVE 생성 옵션을 지정하지 않는 경우, 소스 데이터셋의 INTERLEAVE를 자동적으로 연산에 넣을 것입니다.


참고
----
-  ``gdal/frmts/raw/pauxdataset.cpp`` 로 구현되었습니다.

-  `PCI의 .aux 포맷 설명 <http://www.pcigeomatics.com/cgi-bin/pcihlp/GDB%7CSupported+File+Formats%7CRaw+Binary+Image+Format+(RAW)%7CRaw+.aux+Format>`_

