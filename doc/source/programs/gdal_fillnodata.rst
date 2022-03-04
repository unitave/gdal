.. _gdal_fillnodata:

================================================================================
gdal_fillnodata.py
================================================================================

.. only:: html

    래스터 영역을 경계로부터 보간해서 채웁니다.

.. Index:: gdal_fillnodata

개요
--------

.. code-block::

    gdal_fillnodata.py [-q] [-md max_distance] [-si smooth_iterations]
                    [-o name=value] [-b band]
                    srcfile [-nomask] [-mask filename] [-of format] [dstfile]

설명
-----------

:program:`gdal_fillnodata.py` 스크립트는 (일반적으로 NODATA 영역인) 선택한 영역의 경계를 둘러싸고 있는 무결한 픽셀들로부터 보간해서 영역을 채웁니다.

:cpp:func:`GDALFillNodata` 문서에서 이 알고리즘에 대한 추가적인 내용을 찾을 수 있습니다.

.. option:: -q

    스크립트를 침묵 모드로 실행합니다. 진행 상황 모니터 및 통상적인 메시지를 표시하지 않습니다.

.. option:: -md max_distance

    알고리즘이 보간할 값을 검색할 (픽셀 단위) 최장 거리입니다. 기본값은 100픽셀입니다.

.. option:: -si smooth_iterations

    보간 작업의 결과를 평탄화하기 위해 실행할 3x3 평균 필터 평탄화 반복 작업의 횟수입니다. 기본값은 평탄화 작업을 0번 반복하는 것니다.

.. option:: -o name=value

    알고리즘에 특수 인자를 지정합니다. 현재 아무것도 지원하지 않습니다.

.. option:: -b band

    작업할 밴드입니다. 기본적으로 첫 번째 밴드를 작업합니다.

.. option:: srcfile

    대상 픽셀을 식별하기 위해 사용하는 소스 래스터 파일입니다. 밴드 하나만 사용합니다.

.. option:: -mask filename

    지정한 파일의 첫 번째 밴드를 무결성 마스크로 사용합니다. (0은 무결하지 않고, 0이 아닌 값은 무결합니다.)

.. option:: dstfile

    보간 결과와 함께 생성할 새 파일입니다. 지정하지 않는 경우 소스 밴드를 제자리(in place) 업데이트합니다.

.. option:: -of format

    산출물 포맷을 선택합니다. 기본값은 :ref:`raster.gtiff` 입니다. 단축 포맷명을 사용하십시오.
