.. _pct2rgb:

================================================================================
pct2rgb.py
================================================================================

.. only:: html

    8비트 색상표 이미지를 24비트 RGB 이미지로 변환합니다.

.. Index:: pct2rgb

개요
--------

.. code-block::

    pct2rgb.py [-of format] [-b band] [-rgba] source_file dest_file

설명
-----------

이 유틸리티는 입력 파일에 있는 의사색상 밴드를 원하는 포맷의 산출 RGB 파일로 변환할 것입니다.

.. program:: pct2rgb

.. option:: -of <format>

    산출물 포맷을 선택합니다. GDAL 2.3버전부터 이 옵션을 지정하지 않는 경우 확장자로부터 포맷을 추정합니다. (이전 버전까지는 GTiff를 사용했습니다.) 단축 포맷명을 사용하십시오.

.. option:: -b <band>

    RGB로 변환할 밴드입니다. 기본값은 1입니다.

.. option:: -rgba

    (기본값인 RGB 파일 대신) RGBA 파일을 생성합니다.

.. option:: <source_file>

    입력 파일입니다.

.. option:: <dest_file>

    생성할 산출 RGB 파일입니다.

주의: pct2rgb.py는 파이썬 스크립트로, GDAL이 파이썬 지원과 함께 빌드된 경우에만 작동할 것입니다.

:ref:`gdal_translate` 의 '-expand rgb|rgba' 옵션이 이 유틸리티를 퇴역시켰습니다.
