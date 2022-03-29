.. _raster.sgi:

================================================================================
SGI -- SGI 이미지 포맷
================================================================================

.. shortname:: SGI

.. built_in_by_default::

SGI 드라이버는 현재 SGI 이미지 파일의 읽기 및 쓰기를 지원합니다.

이 드라이버는 현재 1밴드, 2밴드, 3밴드 및 4밴드 이미지를 지원합니다. 이 드라이버는 현재 "채널 당 8비트 값" 이미지를 지원합니다. 이 드라이버는 읽기 작업의 경우 비압축 및 런 렝스(run-length) 인코딩 이미지를 지원하지만, 쓰기 작업의 경우 언제나 RLE 압축 파일을 생성합니다.

GDAL SGI 드라이버는 폴 보크(Paul Bourke)의 SGI 이미지 판독 코드를 기반으로 개발되었습니다.


Driver capabilities
-------------------

.. supports_createcopy::

.. supports_create::

.. supports_virtualio::


참고
----

-  ``gdal/frmts/sgi/sgidataset.cpp`` 로 구현되었습니다.

-  `폴 보크의 SGI 이미지 판독 코드 <http://astronomy.swin.edu.au/~pbourke/dataformats/sgirgb/>`_
-  `SGI 이미지 파일 포맷 문서 <ftp://ftp.sgi.com/graphics/SGIIMAGESPEC>`_

