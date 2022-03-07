.. _ogrtindex:

================================================================================
ogrtindex
================================================================================

.. only:: html

    타일 색인을 생성합니다.

.. Index:: ogrtindex

개요
--------

.. code-block::

    ogrtindex [-lnum n]... [-lname name]... [-f output_format]
              [-write_absolute_path] [-skip_different_projection]
              [-t_srs target_srs]
              [-src_srs_name field_name] [-src_srs_format [AUTO|WKT|EPSG|PROJ]
              [-accept_different_schemas]
              <output_dataset> <src_dataset>...

설명
-----------

:program:`ogrtindex` 프로그램을 사용해서 타일 색인(tileindex)을 생성할 수 있습니다. 타일 색인이란 공간 범위를 가진 다른 파일들 여러 개의 식별 정보 목록을 담고 있는 파일입니다. 이 프로그램은 OGR 연결 유형을 사용하는 레이어에 타일화된 접근을 하기 위해 `MapServer <http://mapserver.org/>`_ 에 사용하려는 목적으로 개발되었습니다.

.. program:: ogrtindex

.. option:: -lnum <n>

    타일 인덱스에 있는 각 소스 파일로부터 ``n`` 번 레이어를 추가합니다.

.. option:: -lname <name>

    타일 인덱스에 있는 각 소스 파일로부터 ``name`` 이라는 이름의 레이어를 추가합니다.

.. option:: -f <output_format>

    산출물 포맷 이름을 선택합니다. 기본값은 shapefile을 생성하는 것입니다.

.. option:: -tileindex <field_name>

    데이터셋 이름으로 사용할 이름입니다. 기본값은 LOCATION입니다.

.. option:: -write_absolute_path

    파일명을 절대 경로로 작성합니다.

.. option:: -skip_different_projection

    이미 타일 색인에 삽입된 레이어와 동일한 투영 좌표계를 가진 레이어만 삽입할 것입니다.

.. option:: -t_srs <target_srs>

    입력 파일들의 범위를 원하는 대상 좌표계로 변형할 것입니다. 이 옵션을 사용해서 생성된 파일들은 MapServer 7.2 미만 버전과 호환되지 않습니다. 기본값은 입력 벡터 레이어들과 동일한 좌표계를 사용하는 단순 직사각형 폴리곤을 생성하는 것입니다.

    .. versionadded:: 2.2.0

.. option:: -src_srs_name <field_name>

    각 타일의 공간 좌표계를 저장할 필드의 이름입니다. MapServer 7.2버전부터, 이 필드 이름을 TILESRS 키워드의 값으로 사용할 수 있습니다.

    .. versionadded:: 2.2.0

.. option:: -src_srs_format <format>

    각 타일의 공간 좌표계를 지정한 서식으로 작성해야만 합니다. ``AUTO``, ``WKT``, ``EPSG``, ``PROJ`` 서식을 지정할 수 있습니다.

    .. versionadded:: 2.2.0

.. option:: -accept_different_schemas

    ogrtindex는 기본적으로 색인에 삽입되는 모든 레이어가 동일한 속성 스키마를 가지고 있는지 검증합니다. 이 옵션을 지정하면, 검증하지 않을 것입니다. 이 옵션을 사용해서 생성된 색인은 MapServer와 호환되지 않을 수도 있으니 조심하십시오!

:option:`-lnum` 또는 :option:`-lname` 인자를 지정하지 않는 경우, 타일 색인에 소스 데이터셋에 있는 모든 레이어를 독립적인 레코드로 추가해야 한다고 가정합니다.

기존 타일 색인이 존재하는 경우 해당 파일에 추가(append)할 것이고, 존재하지 않는다면 새 타일 색인 파일을 생성할 것입니다.

예시
-------

이 예시는 :file:`wrk` 디렉터리에 있는 모든 NTF 파일의 ``BL2000_LINK`` 레이어들의 타일 색인을 담고 있는 shapefile(:file:`tindex.shp`)을 생성할 것입니다:

.. code-block::

    ogrtindex tindex.shp wrk/*.NTF 1069148.900,419873.100 1069147.500,419870.200
      1069146.400,419862.100 1069143.000,419860 1069142,419854.900
      1069138.600,419850 1069135,419848.800 1069134.100,419843
      1069130,419836.200 1069127.600,419824.600 1069123.800,419820.200
      1069126.900,419815.500 1069126.900,419808.200 1069116.500,419798.700
      1069117.600,419794.100 1069115.100,419796.300 1069109.100,419801.800
      1069106.800,419805.000  1069107.300)
