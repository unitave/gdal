.. _gdal_rasterize:

================================================================================
gdal_rasterize
================================================================================

.. only:: html

    벡터 도형을 래스터로 변환(burn)합니다.

.. Index:: gdal_rasterize

개요
--------

.. code-block::

    gdal_rasterize [-b band]* [-i] [-at]
        {[-burn value]* | [-a attribute_name] | [-3d]} [-add]
        [-l layername]* [-where expression] [-sql select_statement]
        [-dialect dialect] [-of format] [-a_srs srs_def] [-to NAME=VALUE]*
        [-co "NAME=VALUE"]* [-a_nodata value] [-init value]*
        [-te xmin ymin xmax ymax] [-tr xres yres] [-tap] [-ts width height]
        [-ot {Byte/Int16/UInt16/UInt32/Int32/Float32/Float64/
                CInt16/CInt32/CFloat32/CFloat64}]
        [-optim {[AUTO]/VECTOR/RASTER}] [-q]
        <src_datasource> <dst_filename>

설명
-----------

이 프로그램은 (포인트, 라인 및 폴리곤) 벡터 도형을 래스터 이미지의 래스터 밴드(들)에 덮어씁니다. OGR이 지원하는 벡터 포맷들로부터 벡터를 읽어옵니다.

GDAL 2.1.0부터 벡터 데이터를 래스터 데이터의 좌표계로 실시간(on the fly) 재투영하는 기능을 지원한다는 사실을 기억하십시오.

.. program:: gdal_rasterize

.. option:: -b <band>

    값을 덮어쓸 밴드(들)입니다. 밴드 여러 개에 덮어쓰기 위해 -b 인자를 여러 번 사용할 수도 있습니다. 기본값은 밴드 1에 덮어쓰는 것입니다. 새 래스터를 생성하는 경우 사용하지 않습니다.

.. option:: -i

    역(逆) 래스터화입니다. 고정된 덮어쓸 값을 덮어쓰거나, 지정한 폴리곤 안에 들어가지 *않는* 이미지의 모든 부분에 첫 번째 객체와 관련된 덮어쓸 값을 덮어씁니다.

.. option:: -at

    라인 렌더링 경로 상에 있거나 폴리곤 내부에 중심 포인트가 있는 픽셀만이 아니라, 라인 또는 폴리곤에 접한 모든 픽셀을 업데이트하도록 ALL_TOUCHED 래스터화 옵션을 활성화합니다. 기본값은 일반 렌더링 규칙을 따르기 위한 비활성화 상태입니다.

.. option:: -burn <value>

    모든 객체의 밴드에 덮어쓸 고정값입니다. 작성할 밴드 당 :option:`-burn` 옵션을 하나씩 지정한 목록을 사용할 수 있습니다.

.. option:: -a <attribute_name>

    덮어쓸(burn-in) 값을 위해 사용할 객체의 속성 필드를 식별합니다. 모든 산출 밴드에 값을 덮어쓸 것입니다.

.. option:: -3d

    객체의 "Z" 값으로부터 덮어쓸 값을 추출해야 한다는 사실을 나타냅니다. 포인트와 라인에 대해 (각 선분을 따라 선형 보간하는 방식으로) 작동합니다. 폴리곤의 경우, 폴리곤이 평평한 (모든 꼭짓점의 Z 값이 동일한) 경우에만 제대로 작동합니다.

.. option:: -add

    새 값을 덮어쓰는 대신, 이 옵션은 기존 래스터에 새 값을 추가합니다. 예를 들자면 히트 맵(heat map)에 적합합니다.

.. option:: -l <layername>

    입력 객체로 사용될, 데이터소스에서 나온 레이어(들)를 설정합니다. 여러 번 지정할 수도 있지만, 최소한 레이어 이름 하나 또는 :option:`-sql` 옵션 하나를 지정해야만 합니다.

.. option:: -where <expression>

    입력 레이어(들)로부터 나온, 값을 덮어쓸 객체를 선택하기 위해 적용되는, 선택적인 SQL WHERE 스타일의 쿼리 표현식입니다.

.. option:: -sql <select_statement>

    값을 덮어쓸 객체의 가상 레이어를 생성하기 위한 데이터소스를 대상으로 평가될 SQL 선언문입니다.

.. option:: -dialect <dialect>

    SQL 방언(dialect)입니다. 어떤 경우 ``OGRSQL`` 을 전송해서 RDBMS의 네이티브 SQL 대신 (최적화되지 않은) :ref:`ogr_sql_dialect` 을 사용하기 위해 쓰일 수도 있습니다. 모든 데이터소스에서 ``SQLITE`` 방언도 사용할 수 있습니다.

    .. versionadded:: 2.1

.. include:: options/of.rst

.. option:: -a_nodata <value>

    산출 밴드에 지정한 NODATA 값을 할당합니다.

.. option:: -init <value>

    산출 이미지 밴드를 이 값으로 사전 초기화합니다. 하지만 산출물 파일에서 이 값을 NODATA 값으로 표시하지는 않습니다. 값을 하나만 지정하는 경우, 모든 밴드에 동일한 값을 사용합니다.

.. option:: -a_srs <srs_def>

    산출물 파일의 투영법을 무시합니다. 지정하지 않는 경우, 입력 벡터 파일의 투영법을 사용할 수 있다면 해당 투영법을 사용할 것입니다. 이 옵션을 사용할 때, 어떤 객체도 입력 벡터의 공간 좌표계로부터 산출 래스터의 지정된 공간 좌표계로 재투영하지 않습니다. 따라서 무결하지 않은 소스 공간 좌표계를 수정하기 위해서만 이 옵션을 사용하십시오. <srs_def>는 완전한 WKT, PROJ.4, EPSG:n 또는 WKT를 담고 있는 파일 등 일반적인 GDAL/OGR 양식이라면 무엇이든 될 수 있습니다.

.. option:: -to NAME=VALUE

    :cpp:func:`GDALCreateGenImgProjTransformer2` 를 전송(pass)하기에 적합한 변환기(transformer) 옵션을 설정합니다. 도형의 좌표를 대상 래스터 픽셀 공간으로 변환하는 경우 이 옵션을 사용합니다. 예를 들면 RPC 관련 변환기 옵션을 지정하기 위해 이 옵션을 사용할 수 있습니다.

    .. versionadded:: 2.3

.. include:: options/co.rst

.. option:: -te <xmin> <ymin> <xmax> <ymax>

    지리참조 범위를 설정합니다. 이 값은 지리참조 단위로 표현되어야만 합니다. 이 옵션을 지정하지 않는 경우, 산출물 파일의 범위는 벡터 레이어들의 범위가 될 것입니다.

.. option:: -tr <xres> <yres>

    대상 해상도를 설정합니다. 이 값은 지리참조 단위로 표현되어야만 합니다. 두 값 모두 양의 값이어야만 합니다.

.. option:: -tap

    (대상에 정렬된 픽셀(target aligned pixels)) 산출물 파일의 범위의 좌표를 :option:`-tr` 옵션의 값에 정렬시켜 정렬된 범위가 최소 범위를 포함하도록 합니다.

.. option:: -ts <width> <height>

    산출물 파일의 크기를 픽셀과 행 단위로 설정합니다. :option:`-ts` 와 :option:`-tr` 을 함께 사용할 수 없다는 사실을 기억하십시오.

.. option:: -ot <type>

    산출 밴드가 지정한 데이터 유형이도록 강제합니다. 기본값은 ``Float64`` 입니다.

.. option:: -optim {[AUTO]/VECTOR/RASTER}}

    최적화 알고리즘을 사용하도록 강제합니다. (결과는 동일합니다.) 대부분의 경우 래스터 모드를 사용해서 읽기/쓰기 작업을 최적화합니다. 벡터 모드는 입력 객체가 상당히 많은 경우 유용하며 CPU 사용을 최적화합니다. 래스터 모드를 효율적으로 사용하려면 타일화된 이미지에 사용해야 합니다. (기본값인) AUTO 모드는 입력물과 산출물의 속성을 바탕으로 알고리즘을 선택할 것입니다.

    .. versionadded:: 2.3

.. option:: -q

    진행 상황 모니터 및 기타 오류가 아닌 결과를 표시하지 않습니다.

.. option:: <src_datasource>

    OGR이 지원하는 읽기 가능한 모든 데이터소스를 설정할 수 있습니다.

.. option:: <dst_filename>

    GDAL이 지원하는 산출물 파일입니다. 업데이트 모드 접근을 지원해야만 합니다. :option:`-of`, :option:`-a_nodata`, :option:`-init`, :option:`-a_srs`, :option:`-co`, :option:`-te`, :option:`-tr`, :option:`-tap`, :option:`-ts`, 또는 :option:`-ot` 옵션을 사용해서 이 파일을 생성할 (또는 파일이 이미 존재하는 경우 덮어쓸) 것입니다.

:option:`-of`, :option:`-a_nodata`, :option:`-init`, :option:`-a_srs`, :option:`-co`, :option:`-te`, :option:`-tr`, :option:`-tap`, :option:`-ts`, 또는 :option:`-ot` 옵션 가운데 하나라도 사용되는 경우 이 프로그램은 새 대상 래스터 이미지를 생성합니다. 모든 새 래스터에 대해 :option:`-tr` 또는 :option:`-ts` 옵션을 사용해서 해상도 또는 크기를 지정해야만 합니다. 대상 래스터가 이미 존재하고 생성 관련 옵션 가운데 하나라도 사용되는 경우 대상 래스터를 덮어쓸 것입니다.

C API
-----

C에서 :cpp:func:`GDALRasterize` 로 이 유틸리티를 호출할 수 있습니다.

.. versionadded:: 2.1

예시
-------

다음 명령어는 RGB TIFF 파일인 work.tif에 mask.shp의 모든 폴리곤을 적색(RGB = 255,0,0)으로 덮어쓸 것입니다.

::

    gdal_rasterize -b 1 -b 2 -b 3 -burn 255 -burn 0 -burn 0 -l mask mask.shp work.tif


다음 명령어는 ROOF_H 속성으로부터 정상 표고(top elevation)를 가져와서 산출 표고 파일에 모든 "class A" 건물을 덮어쓸 것입니다.

::

    gdal_rasterize -a ROOF_H -where "class='A'" -l footprints footprints.shp city_dem.tif


다음 명령어는 새 1000x1000픽셀 크기의 RGB TIFF에 footprint.shp의 모든 폴리곤을 적색으로 덮어쓸 것입니다. :option:`-b` 를 사용하지 않는다는 점을 기억하십시오. :option:`-burn` 옵션들의 순서가 산출 래스터의 밴드 순서를 결정합니다.

::

    gdal_rasterize -burn 255 -burn 0 -burn 0 -ot Byte -ts 1000 1000 -l footprints footprints.shp mask.tif
