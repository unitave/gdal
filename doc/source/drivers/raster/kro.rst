.. _raster.kro:

================================================================================
KRO -- KOLOR RAW 포맷
================================================================================

.. shortname:: KRO

.. built_in_by_default::

이 드라이버는 KRO 포맷 읽기 접근, 업데이트 및 생성을 지원합니다. KRO 포맷은 바이너리 RAW 포맷으로, 밴드 개수가 여러 개인 (보통 RGB 또는 RGBA인 3밴드 또는 4밴드) 여러 심도의 (8비트, 부호 없는 16비트 정수형 및 32비트 부동소수점형) 데이터를 지원합니다. 운영 체제 파일 시스템이 제한하지 않는 한 파일 용량 제한은 없습니다.

`포맷 사양 <http://www.autopano.net/wiki-en/Format_KRO>`_

주의: ``gdal/frmts/raw/krodataset.cpp`` 로 구현되었습니다.


드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::

.. supports_create::

.. supports_virtualio::
