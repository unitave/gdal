.. _raster.doq2:

================================================================================
DOQ2 -- 새 명찰 USGS DOQ
================================================================================

.. shortname:: DOQ2

.. built_in_by_default::

이 드라이버는 지리참조 아핀 변환(affine transform) 읽기와 투영법 문자열 수집 및 기타 보조 필드를 메타데이터로 읽어오기를 포함하는 읽기 접근을 지원합니다. USGS가 개발한 새로운 명찰(labelled) DOQ(Digital Ortho Quad) 포맷입니다.

데릭 J. 브래시어(Derrick J. Brashear)가 이 드라이버를 구현했습니다.

주의: ``gdal/frmts/raw/doq2dataset.cpp`` 로 구현되었습니다.

참고: `USGS DOQ 표준 <http://rockyweb.cr.usgs.gov/nmpstds/doqstds.html>`_

드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

.. supports_virtualio::

