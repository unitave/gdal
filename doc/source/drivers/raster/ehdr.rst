.. _raster.ehdr:

================================================================================
EHdr -- ESRI .hdr Labelled
================================================================================

.. shortname:: EHdr

.. built_in_by_default::

GDAL은 ESRI BIL 포맷이라고 불리기도 하는 ESRI .hdr labeling 포맷의 읽기와 쓰기를 지원합니다. 32비트 부동소수점 유형은 물론 8, 16, 32비트 정수 래스터 데이터 유형도 지원합니다. (.prj 파일로부터 나오는) 좌표계, 그리고 지리참조를 지원합니다. .hdr 파일에서 식별할 수 없는 옵션은 무시합니다. 데이터셋을 열려면 이미지 파일을 가지고 있는 (확장자가 .bil인 경우가 많은) 파일을 선택하십시오. .clr 색상표 파일이 있는 경우 해당 파일을 읽어오지만, 쓰지는 않습니다. image.rep 파일이 있는 경우, SpatioCarte Defense 1.0 래스터 상품의 투영 시스템을 추출하기 위해 해당 파일을 읽어올 것입니다.

이 드라이버는 언제나 부동소수점형 데이터와 정수형 데이터를 잘 구분하지는 못 합니다. 이런 구분 작업을 위해, GDAL은 .hdr 포맷에 FLOAT, SIGNEDINT 또는 UNSIGNEDINT 가운데 하나를 값으로 가지는 PIXELTYPE이란 이름의 필드를 추가합니다. PIXELTYPE 필드를 NBITS 필드와 함께 이용하면 픽셀 유형의 모든 변이형을 서술할 수 있습니다.

다음은 그 예입니다:

::

     ncols 1375
     nrows 649
     cellsize 0.050401
     xllcorner -130.128639
     yllcorner 20.166799
     nodata_value 9999.000000
     nbits 32
     pixeltype float
     byteorder msbfirst

이 드라이버는 GTOPO30 데이터를 읽어오기에 충분할 수도 있습니다.

주의: ``gdal/frmts/raw/ehdrdataset.cpp`` 로 구현되었습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::

참고
--------

-  `ESRI 백서: + ArcView GIS 3.1 및 3.2를 위한 확장 가능한 이미지 포맷들 <http://downloads.esri.com/support/whitepapers/other_/eximgav.pdf>`_ (BIL 포맷은 p.5 참조)
-  `GTOPO30 - 지구 지형 데이터(Global Topographic Data) <http://edcdaac.usgs.gov/gtopo30/gtopo30.html>`_
-  `GTOPO30 문서 <http://edcdaac.usgs.gov/gtopo30/README.html>`_
-  `SpatioCarte Defense 1.0 사양 <http://eden.ign.fr/download/pub/doc/emabgi/spdf10.pdf/download>`_ (프랑스어)
-  `SRTMHGT 드라이버 <#SRTMHGT>`_
