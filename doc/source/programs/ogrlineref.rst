.. _ogrlineref:

================================================================================
ogrlineref
================================================================================

.. only:: html

    선형 참조를 생성하고 이를 이용한 계산을 수행합니다.

.. Index:: ogrlineref

개요
--------

.. code-block::

    ogrlineref [--help-general] [-progress] [-quiet]
           [-f format_name] [[-dsco NAME=VALUE] ...] [[-lco NAME=VALUE]...]
           [-create]
           [-l src_line_datasource_name] [-ln layer_name] [-lf field_name]
           [-p src_repers_datasource_name] [-pn layer_name] [-pm pos_field_name] [-pf field_name]
           [-r src_parts_datasource_name] [-rn layer_name]
           [-o dst_datasource_name] [-on layer_name]  [-of field_name] [-s step]
           [-get_pos] [-x long] [-y lat]
           [-get_coord] [-m position]
           [-get_subline] [-mb position] [-me position]

설명
-----------

:program:`ogrlineref` 프로그램을 사용해서:

-  입력 데이터로부터 선형 참조(linear reference) 파일을 생성할 수 있습니다.
-  경로 상에 있는 입력 좌표(포인트)의 투영법에 대한 "선형 참조된" 거리를 반환할 수 있습니다.
-  "선형 참조된" 거리에 따라 경로 상에 있는 좌표(포인트)를 반환할 수 있습니다.
-  "선형 참조된" 시작 및 종단 거리에 따라 경로의 일부분을 반환할 수 있습니다.

:program:`ogrlineref` 는 선형 참조 - 특수한 (예를 들어 참조 단위로 된 1km) 길이의 선분들을 담고 있는 파일을 생성하고 이 파일로부터 좌표, 선형 참조된 거리 또는 하위 라인(하위 경로)를 계산합니다. 이 유틸리티에 도형의 ``M`` 또는 ``Z`` 값은 필수가 아닙니다. 산출물을 OGR이 지원하는 모든 포맷으로 저장할 수 있습니다. 또한 표준 출력(stdout)에 몇몇 정보도 작성합니다.

.. option:: --help-general

    활용법을 출력합니다.

.. option:: -progress

    진행 상황을 출력합니다.

.. option:: -quiet

    오류 및 결과를 제외한 모든 메시지를 출력하지 않습니다.

.. option:: -f <format_name>

    산출물 포맷 이름을 선택합니다. 기본값은 shapefile을 생성하는 것입니다.

.. option:: -dsco <NAME=VALUE>

    데이터셋 생성 옵션 (특정 포맷 지원)

.. option:: -lco <NAME=VALUE>

    레이어 생성 옵션 (특정 포맷 지원)

.. option:: -create

    선형 참조 파일(부분들의 라인스트링)을 생성합니다.

.. option:: -l <src_line_datasource_name>

    입력 라인스트링 (예: 도로 등) 데이터소스를 가리키는 경로입니다.

.. option:: -ln <layer_name>

    데이터소스에 있는 레이어 이름입니다.

.. option:: -lf <field_name>

    입력 라인들을 (예: 도로 집합 등으로) 구분하기 위한 단일(unique) 값들의 필드 이름입니다.

.. option:: -p <src_repers_datasource_name>

    선형 참조 포인트를 (예: 도로 이정표 등을) 가리키는 경로입니다.

.. option:: -pn <layer_name>

    데이터소스에 있는 레이어 이름입니다.

.. option:: -pm <pos_field_name>

    경로를 따라 측정한 거리의 (예: 이정표 값 등의) 필드 이름입니다.

.. option:: -pf <field_name>

    라인에 입력 참조 포인트를 매핑하기 위한 단일(unique) 값들의 필드 이름입니다.

.. option:: -r <src_parts_datasource_name>

    선형 참조 파일을 가리키는 경로입니다.

.. option:: -rn <layer_name>

    데이터소스에 있는 레이어 이름입니다.

.. option:: -o <dst_datasource_name>

    산출 선형 참조 파일(라인스트링 데이터소스)을 가리키는 경로입니다.

.. option:: -on <layer_name>

    데이터소스에 있는 레이어 이름입니다.

.. option:: -of <field_name>

    입력 라인의 단일(unique) 값들을 저장하기 위한 필드의 이름입니다.

.. option:: -s <step>

    부분의 크기를 선형 단위로 설정합니다.

.. option:: -get_pos

    입력 X, Y에 대해 선형 참조된 위치를 반환합니다.

.. option:: -x <long>

    입력 X 좌표

.. option:: -y <lat>

    입력 Y 좌표

.. option:: -get_coord

    입력 선형 거리에 대한 경로 상 포인트를 반환합니다.

.. option:: -m <position>

    입력 선형 거리입니다.

.. option:: -get_subline

    입력 경로에서 입력 선형 위치로부터 입력 선형 위치까지의 부분을 반환합니다.

.. option:: -mb <position>

    입력 시작 선형 거리

.. option:: -me <position>

    입력 종단 선형 거리

예시
-------

이 예시는 선형 참조에 필요한 데이터를 (1km 부분들을) 담고 있는 shapefile(:file:`parts.shp`)을 생성할 것입니다.

.. code-block::

    ogrlineref -create -l roads.shp -p references.shp -pm dist -o parts.shp -s 1000 -progress
