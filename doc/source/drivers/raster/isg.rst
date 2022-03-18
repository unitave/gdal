.. _raster.isg:

================================================================================
ISG -- 지오이드 용 국제 서비스
================================================================================

.. versionadded:: 3.1

.. shortname:: ISG

.. built_in_by_default::

http://www.isgeoid.polimi.it/Geoid/reg_list.html 에 있는 여러 지오이드 모델에 쓰이는 지오이드(Geoid) 텍스트 포맷 용 국제 서비스(International Service)의 그리드 읽기를 지원합니다.

포맷 사양은 http://www.isgeoid.polimi.it/Geoid/ISG_format_20160121.pdf 에서 찾아볼 수 있습니다.

NOTE: Implemented as ``gdal/frmts/aaigrid/aaigriddataset.cpp``.

드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

.. note::

    항상 제멋대로 WGS84를 그리드의 보간 좌표계로 리포트할 것입니다.
    정확한 좌표계를 적용하려면 그리드 문서를 읽어보십시오.

.. supports_virtualio::
