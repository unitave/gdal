.. _gdal_create:

================================================================================
gdal_create
================================================================================

.. only:: html

    .. versionadded:: 3.2.0

    래스터 파일을 (소스 데이터셋 없이) 생성합니다.

.. Index:: gdal_create

개요
--------

.. code-block::


    gdal_create [--help-general]
       [-of format]
       [-outsize xsize ysize]
       [-bands count]
       [-burn value]*
       [-ot {Byte/Int16/UInt16/UInt32/Int32/Float32/Float64/
             CInt16/CInt32/CFloat32/CFloat64}] [-strict]
       [-a_srs srs_def] [-a_ullr ulx uly lrx lry] [-a_nodata value]
       [-mo "META-TAG=VALUE"]* [-q]
       [-co "NAME=VALUE"]*
       [-if input_dataset]
       out_dataset

설명
-----------

:program:`gdal_create` 유틸리티를 사용하면 차원, 밴드 개수로부터 새 래스터 파일을 초기화하고 좌표계, 지리변형, NODATA 값, 메타데이터 같은 다양한 파라미터를 설정할 수 있습니다. XML 구성 파일로부터 PDF 파일을 생성하는 것처럼 특별한 경우에도 이 유틸리티를 쓸 수 있습니다.

.. program:: gdal_create

.. include:: options/ot.rst

.. include:: options/of.rst

.. option:: -outsize <xsize> <ysize>

    산출물 파일의 크기를 픽셀 단위로 설정합니다. 첫 번째 숫자가 너비, 두 번째 숫자가 높이입니다.

.. option:: -bands <count>

    밴드의 개수입니다. -outsize를 설정한 경우 기본값은 1, 설정하지 않은 경우 기본값은 0입니다.

.. option:: -burn <value>

    모든 객체의 밴드에 덮어쓸 고정값입니다. 밴드마다 다른 값을 작성하려면 :option:`-burn` 옵션들의 목록을 지정하면 됩니다.

.. option:: -a_srs <srs_def>

    산출물 파일의 투영법을 무시합니다. <srs_def>는 완전한 WKT, PROJ.4, EPSG:n 또는 WKT를 담고 있는 파일 등 일반적인 GDAL/OGR 양식이라면 무엇이든 될 수 있습니다. 어떤 재투영도 하지 않습니다.

.. option:: -a_ullr <ulx> <uly> <lrx> <lry>

    산출물 파일의 지리참조 경계를 할당합니다.

.. option:: -a_nodata <value>

    산출 밴드에 지정한 NODATA 값을 할당합니다.

.. option:: -mo META-TAG=VALUE

    가능하다면 산출 데이터셋에 설정할 메타데이터 키와 값을 전송(pass)합니다.

.. include:: options/co.rst

.. option:: -q

    진행 상황 모니터 및 기타 오류가 아닌 결과를 표시하지 않습니다.

.. option:: -if <input_dataset>

    .. versionadded:: 3.3

    -outsize, -bands, -ot, -a_srs, -a_ullr 및 -a_nodata 옵션들의 기본값을 위한 템플릿 역할을 하는 GDAL 입력 데이터셋의 이름입니다. 픽셀 값을 복사하지 *않을* 것이라는 점을 기억하십시오.

.. option:: <out_dataset>

    대상 파일의 이름입니다.

예시
--------

- 10이라는 균일한 값으로 새 GeoTIFF 파일을 초기화합니다:

    ::

        gdal_create -outsize 20 20 -a_srs EPSG:4326 -a_ullr 2 50 3 49 -burn 10 out.tif


- XML 구성 파일로부터 PDF 파일을 생성합니다:

    ::

        gdal_create -co COMPOSITION_FILE=composition.xml out.pdf



- GeoTIFF 파일로부터 비어 있는 GeoTIFF 파일을 초기화합니다:

    ::

        gdal_create -if prototype.tif output.tif

