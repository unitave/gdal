.. _raster.srtmhgt:

================================================================================
SRTMHGT -- SRTM HGT 포맷
================================================================================

.. shortname:: SRTMHGT

.. built_in_by_default::

SRTM HGT 드라이버는 현재 SRTM-3 및 SRTM-1 v2 (HGT) 파일의 읽기를 지원합니다. 파일명은 NXXEYYY.hgt 형식이어야만 하고, 또는 GDAL 2.1.2버전부터는 NXXEYYY[.something].hgt 형식이어야만 합니다.

GDAL 2.2버전부터, 이 드라이버는 .hgt.zip 파일의 이름이 NXXEYYY[.something].hgt.zip 형식이고 NXXEYYY.hgt 파일을 담고 있는 경우 .hgt.zip 파일을 직접 읽어올 수 있습니다. GDAL 이전 버전을 사용한다면 /vsizip//path/to/NXXEYYY[.something].hgt.zip/NXXEYYY.hgt 문법을 사용하십시오.

이 드라이버가 새 파일 생성을 지원하긴 하지만, 입력 데이터가 정확히 SRTM-3 또는 SRTM-1 셀 형식 포맷이어야만 합니다. 다시 말해 크기 및 경계가 셀에 알맞아야만 한다는 뜻입니다.


드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

.. supports_virtualio::


참고
----

-  ``gdal/frmts/srtmhgt/srtmhgtdataset.cpp`` 로 구현되었습니다.

-  `SRTM 문서 <http://dds.cr.usgs.gov/srtm/version2_1/Documentation>`_

-  `SRTM FAQ <http://www2.jpl.nasa.gov/srtm/faq.html>`_

-  `SRTM 데이터 <http://dds.cr.usgs.gov/srtm/version2_1/>`_
