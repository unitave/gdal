.. _gdal_proximity:

================================================================================
gdal_proximity.py
================================================================================

.. only:: html

    래스터 근접성 맵을 생성합니다.

.. Index:: gdal_proximity

개요
--------

.. code-block::

    gdal_proximity.py <srcfile> <dstfile> [-srcband n] [-dstband n]
                      [-of format] [-co name=value]*
                      [-ot Byte/UInt16/UInt32/Float32/etc]
                      [-values n,n,n] [-distunits PIXEL/GEO]
                      [-maxdist n] [-nodata n] [-use_input_nodata YES/NO]
                      [-fixed-buf-val n]

설명
-----------

:program:`gdal_proximity.py` 스크립트는 각 픽셀의 중심(center)에서 대상 픽셀로 식별된 최근접 픽셀의 중심까지의 거리를 나타내는 래스터 근접성(proximity) 맵을 생성합니다. 대상 픽셀은 래스터 픽셀 값이 대상 픽셀 값 집합에 있는 소스 래스터의 픽셀입니다.

.. program:: gdal_proximity

.. option:: <srcfile>

    대상 픽셀을 식별하기 위해 사용하는 소스 래스터 파일입니다.

.. option:: <dstfile>

    근접성 맵을 작성할 대상 래스터 파일입니다. srcfile과 동일한 크기의 기존 파일일 수도 있습니다. 기존에 존재하지 않는 경우 새로 생성할 것입니다.

.. option:: -srcband <n>

    소스 파일에서 사용할 밴드를 식별합니다. (기본값은 1입니다.)

.. option:: -dstband <n>

    대상 파일에서 사용할 밴드를 식별합니다. (기본값은 1입니다.)

.. include:: options/of.rst

.. include:: options/co.rst

.. option:: -ot <type>

    드라이버가 지원하는 데이터 유형을 지정합니다. 다음 가운데 하나를 사용할 수 있습니다: ``Byte``, ``UInt16``, ``Int16``, ``UInt32``, ``Int32``, ``Float32`` (기본값), 또는 ``Float64``.

.. option:: -values <n>,<n>,<n>

    소스 이미지에서 대상 픽셀로 간주되기 위한 대상 픽셀값의 목록입니다. 지정하지 않는 경우, 0값이 아닌 모든 픽셀을 대상 픽셀로 간주할 것입니다.

.. option:: -distunits PIXEL|GEO

    생성된 거리를 픽셀 단위로 나타낼지 또는 지리참조 좌표로 나타낼지 설정합니다. (기본값은 PIXEL입니다.)

.. option:: -maxdist <n>

    생성할 거리의 최대값입니다. 이 거리를 초과하는 픽셀에 대해서는 NODATA 값을 사용할 것입니다. NODATA 값을 지정하지 않는 경우, 산출 밴드에 산출 밴드의 NODATA 값을 쿼리할 것입니다. 산출 밴드가 NODATA 값을 가지고 있지 않은 경우, 65535값을 사용할 것입니다. -distunits를 GEO로 지정하지 않았다면 거리를 픽셀 단위로 해석합니다.

.. option:: -nodata <n>

    산출 근접성 래스터에 사용할 NODATA 값을 지정합니다.

.. option:: -use_input_nodata YES/NO

    입력 래스터에 있는 NODATA 픽셀이 산출 래스터의 NODATA가 되어야 할지를 나타냅니다. (기본값은 NO입니다.)

.. option:: -fixed-buf-val <n>

    거리 값이 아니라 대상 픽셀의 -maxdist 안에 들어오는 (대상 픽셀을 포함하는) 모든 픽셀에 적용할 값을 지정합니다.
