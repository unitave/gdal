.. _raster.bt:

================================================================================
BT -- VTP .bt 바이너리 지형 포맷
================================================================================

.. shortname:: BT

.. built_in_by_default:: 

.bt 포맷은 VTP 소프트웨어에서 표고 데이터 용으로 사용됩니다. 이 드라이버는 Int16, Int32 및 Float32 픽셀 데이터 유형에 대한 지원을 포함하는 .bt 1.3 포맷 읽기와 쓰기를 지원합니다.

VTP 소프트웨어는 gzip(GNU zip) 압축된 .bt 파일(.bt.gz) 읽기와 쓰기를 지원하지만, 드라이버는 이를 지원하지 **않습니다**. GDAL에서 사용하기 전에 "gzip -d file.bt.gz" 명령어를 통해 파일을 압축해제하십시오.

외부 .prj 파일에서 투영법을 읽고 쓸 수 있으며, 대부분 내부적으로 정의된 좌표계들도 사용할 수 있습니다.

이 열 지향(column oriented) 데이터에 대한 아주 비효율적인 접근 전략 때문에, GDAL .bt 드라이버를 통해 영상에 읽기/쓰기 접근하는 것은 정말로 느립니다. 수정할 수 있는 문제이지만, 상당한 시간과 노력을 들여야 할 것입니다.

주의: ``gdal/frmts/raw/btdataset.cpp`` 로 구현되었습니다.

참고: `BT 파일 포맷 <http://www.vterrain.org/Implementation/Formats/BT.html>`_ 은 `VTP <http://www.vterrain.org/>`_ 웹사이트에 정의되어 있습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::

