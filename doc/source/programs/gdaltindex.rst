.. _gdaltindex:

================================================================================
gdaltindex
================================================================================

.. only:: html

    OGR 지원 데이터셋을 래스터 타일 색인으로 생성합니다.

.. Index:: gdaltindex

개요
--------

.. code-block::

    gdaltindex [-f format] [-tileindex field_name] [-write_absolute_path]
            [-skip_different_projection] [-t_srs target_srs]
            [-src_srs_name field_name] [-src_srs_format [AUTO|WKT|EPSG|PROJ]
            [-lyr_name name] index_file [gdal_file]*

설명
-----------

이 프로그램은 각 입력 래스터 파일에 대한 레코드, 파일명을 담고 있는 속성, 그리고 래스터 윤곽선을 그리는 폴리곤 도형을 가지고 있는 OGR 지원 데이터셋을 생성합니다. 이 산출물은 `MapServer <http://mapserver.org/>`_ 에서 래스터 타일 색인으로 사용하는 데 적합합니다.

.. program:: ogrtindex

.. option:: -f <format>

    산출 타일 색인 파일의 OGR 포맷입니다. GDAL 2.3버전부터, 이 옵션을 지정하지 않는 경우 확장자로부터 포맷을 추정합니다. (이전 버전까지는 ESRI Shapefile을 기본값으로 사용했습니다.)

.. option:: -tileindex <field_name>

    색인된 래스터를 가리키는 파일 경로/위치를 담은 산출물 필드명입니다. 기본 타일 색인 필드명은 ``location`` 입니다.

.. option:: -write_absolute_path

    래스터 파일을 가리키는 절대 경로는 타일 색인 파일에 저장됩니다. 기본적으로 래스터 파일명은 명령줄에서 지정한 그대로 파일에 들어갈 것입니다.

.. option:: -skip_different_projection

    (:option:`-t_srs` 를 설정하지 않았다면) 타일 색인에 이미 삽입된 파일과 동일한 투영법을 가진 파일만 삽입될 것입니다. 기본값은 투영법을 확인하지 않고 모든 입력을 받아들이는 것입니다.

.. option:: -t_srs <target_srs>:

    입력 파일의 도형을 원하는 대상 좌표계로 변환할 것입니다. 기본값은 단순 직사각형 폴리곤을 입력 래스터와 동일한 좌표계로 생성하는 것입니다.

.. option:: -src_srs_name <field_name>

    각 타일의 공간 좌표계를 저장할 필드의 이름입니다. MapServer에서 이 필드명을 TILESRS 키워드의 값으로 사용할 수 있습니다.

.. option:: -src_srs_format <type>

    이 옵션에서 지정한 서식으로 각 타일의 공간 좌표계를 작성해야만 합니다. AUTO, WKT, EPSG, PROJ 유형을 지정할 수 있습니다.

.. option:: -lyr_name <name>

    산출 타일 색인 파일에 생성/추가할 레이어 이름입니다.

.. option:: index_file

    생성/추가할 산출물 파일의 이름입니다. 기본 데이터셋이 없다면 산출물을 생성할 것이고, 기본 데이터셋이 있다면 기존 데이터셋에 추가할 것입니다.

.. option:: <gdal_file>

    입력 GDAL 래스터 파일로, 공백으로 분리된 파일 여러 개일 수도 있습니다. 와일드카드("*")도 쓰일 수 있습니다. :option:`-write_absolute_path` 옵션을 이미 사용한 경우가 아니라면 이 옵션에 지정한 스타일대로 파일 위치를 저장합니다.

예시
--------

- 유틸리티가 ``doq`` 폴더에서 탐지한 모든 이미지에 대한 레코드를 가진 shapefile(``doq_index.shp``)을 생성합니다. 각 레코드는 이미지의 위치를 가리키는 정보는 물론 이미지의 경계를 보여주는 경계 상자 도형도 가지고 있습니다.:

::

    gdaltindex doq_index.shp doq/*.tif

- 앞과 동일한 작업을 수행하지만, 다음은 shapefile 대신 GeoPackage를 생성하는 명령어입니다:

::

    gdaltindex -f GPKG doq_index.gpkg doq/*.tif

- :option:`-t_srs` 옵션을 사용하면 모든 입력 래스터를 동일한 산출 투영법으로 변환할 수 있습니다:

::

    gdaltindex -t_srs EPSG:4326 -src_srs_name src_srs tile_index_mixed_srs.shp *.tif

- 텍스트 파일에 있는 파일 목록으로 타일 색인을 만듭니다:

::

    gdaltindex doq_index.shp --optfile my_list.txt

참고
--------

다른 명령줄 옵션을 알고 싶다면 :ref:`raster_common_options` 를 읽어보십시오. 특히 :ref:`--optfile <raster_common_options_optfile>` 스위치는 입력 데이터셋 목록을 지정하는 데 쓰일 수 있습니다.
