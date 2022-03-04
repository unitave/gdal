.. _gdalcompare:

================================================================================
gdalcompare.py
================================================================================

.. only:: html

    이미지 2개를 비교합니다.

.. Index:: gdalcompare.py

개요
--------

.. code-block::

    gdalcompare.py [-sds] golden_file new_file

설명
-----------

:program:`gdalcompare.py` 스크립트는 GDAL이 지원하는 데이터셋 2개를 비교해서 그 차이를 리포트합니다. 표준 출력(stdout)에 차이를 리포트하는 것에 더해, 이 스크립트는 차이의 개수도 엑시트 값으로 반환할 것입니다.

이미지 픽셀 및 다양한 메타데이터를 확인합니다. 차이 1개로 셈하게 될 바이트-바이-바이트 비교도 수행합니다. 즉 GDAL 가시화 데이터가 동일한지만 중요하다면 (바이너리 차이) 1개는 허용할 수 있을 것입니다.

.. program:: gdalcompare

.. option:: -sds

    이 플래그가 전송(pass)되면 스크립트가 데이터셋의 일부분인 모든 하위 데이터셋을 비교할 것이고, 그렇지 않은 경우 하위 데이터셋을 무시합니다.

.. option:: <golden_file>

    정확하다고 간주하는 파일을 골든 파일(golden file)이라고 부릅니다.

.. option:: <new_file>

    골든 파일에 비교되는 파일을 새 파일(new file)이라고 부릅니다.

:program:`gdalcompare.py` 스크립트도 (다른 모든 스크립트와 마찬가지로) 파이썬 코드 `from osgeo_utils import gdalcompare` 를 통해 라이브러리로써 호출할 수 있다는 사실을 기억하십시오. 주진입점(primary entry point)은 `gdalcompare.compare()`로, 골든 `gdal.Dataset` 과 새 `gdal.Dataset` 을 인자로 받아 (바이너리 비교를 제외한) 차이의 개수를 반환합니다. 하위 데이터셋들을 비교하려면 `gdalcompare.compare_sds()` 엔트리 포인트를 사용하면 됩니다.
