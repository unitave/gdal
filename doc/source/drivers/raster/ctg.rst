.. _raster.ctg:

================================================================================
CTG -- USGS LULC 합성 테마 그리드(Composite Theme Grid)
================================================================================

.. shortname:: CTG

.. built_in_by_default::

이 드라이버는 문자 서식 CTG로 인코딩된 USGS LULC(Land Use and Land Cover) 그리드를 읽어올 수 있습니다. 각 파일을 Int32 유형의 밴드 6개 데이터셋으로 리포트합니다. 각 밴드의 의미는 다음과 같습니다:

#. 토지 사용 및 토지 피복 코드
#. 정치 단위 코드
#. 인구 통계의 시군구 및 표준 대도시 통계 지구(SMSA) 지역 코드
#. 수리(水理) 단위 코드
#. 연방 토지 소유 코드
#. 주(州) 토지 소유 코드

이 파일들은 USGS 사이트에서 주로 grid_cell.gz, grid_cell1.gz 또는 grid_cell2.gz 와 같은 방식으로 명명됩니다.

-  `토지 사용 및 토지 피복 수치 데이터 (데이터 사용자 지침서 4) <http://edc2.usgs.gov/geodata/LULC/LULCDataUsersGuide.pdf>`_ - USGS의 PDF 버전
-  `토지 사용 및 토지 피복 수치 데이터 (데이터 사용자 지침서 4) <http://www.vterrain.org/Culture/LULC/Data_Users_Guide_4.html>`_ - 벤 디스코(Ben Discoe)가 변환한 HTML 버전
-  `1:250,000 및 1:100,000 축척의 USGS LULC 데이터 <http://edcftp.cr.usgs.gov/pub/data/LULC>`_

주의: ``gdal/frmts/ctg/ctgdataset.cpp`` 로 구현되었습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

.. supports_virtualio::

