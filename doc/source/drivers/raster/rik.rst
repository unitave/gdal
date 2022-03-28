.. _raster.rik:

================================================================================
RIK -- 스웨덴 그리드 맵
================================================================================

.. shortname:: RIK

.. build_dependencies:: (필요한 경우 내부 zlib 사용)

GDAL은 RIK 포맷의 읽기 접근을 지원합니다. 이 포맷은 스웨덴의 란트메테리에트(Lantmäteriet) 기구가 발행하는 맵에 사용됩니다. RIK 포맷 버전 1, 2, 3을 지원하지만 픽셀 당 8비트 데이터 유형만 지원합니다.

이 드라이버는 `TRikPanel <http://sourceforge.net/projects/trikpanel/>`_ 프로젝트의 결과물을 기반으로 개발되었습니다.

주의: ``gdal/frmts/rik/rikdataset.cpp`` 로 구현되었습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

.. supports_virtualio::
