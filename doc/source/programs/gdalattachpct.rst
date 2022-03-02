.. _gdalattachpct:

================================================================================
gdalattachpct.py
================================================================================

.. only:: html

    한 파일의 색상표를 다른 파일에 첨부시킵니다.

.. Index:: gdalattachpct

개요
--------

.. code-block::

    gdalattachpct.py [-of format] palette_file source_file dest_file

설명
-----------

이 유틸리티는 입력 래스터 파일의 색상표 파일 또는 독립적인 색상표 파일을 또다른 래스터에 첨부시킵니다.

.. program:: gdalattachpct

.. option:: -of <format>

    산출물 포맷을 선택합니다. GDAL 2.3버전부터 이 옵션을 지정하지 않는 경우 확장자로부터 포맷을 추정합니다. (이전 버전까지는 GTiff를 사용했습니다.) 단축 포맷명을 사용하십시오.

.. option:: <palette_file>

    <palette_file>로부터 색상표를 추출합니다. <palette_file>은 GDAL이 지원하는 포맷의 색상표를 가진 래스터 파일 또는 이 프로그램이 지원하는 포맷(txt, qml, qlr)으로 된 색상 파일 가운데 하나여야만 합니다.

.. option:: <source_file>

    입력 파일입니다.

.. option:: <dest_file>

    생성할 산출 RGB 파일입니다.

주의: gdalattachpct.py는 파이썬 스크립트로, GDAL이 파이썬 지원과 함께 빌드된 경우에만 작동할 것입니다.
