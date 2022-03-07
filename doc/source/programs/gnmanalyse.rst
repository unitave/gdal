.. _gnmanalyse:

================================================================================
gnmanalyse
================================================================================

.. only:: html

    네트워크를 분석합니다.

.. Index:: gnmanalyse

개요
--------

.. code-block::

    gnmanalyse [--help][-q][-quiet][--long-usage]
            [dijkstra <start_gfid> <end_gfid> [[-alo NAME=VALUE] ...]]]
            [kpaths <start_gfid> <end_gfid> <k> [[-alo NAME=VALUE] ...]]]
            [resource [[-alo NAME=VALUE] ...]]]
            [-ds <ds_name>][-f <ds_format>][-l <layer_name>]
            [[-dsco NAME=VALUE] ...][-lco NAME=VALUE]
            <gnm_name>

설명
-----------

:program:`gnmanalyse` 프로그램은 GDAL의 지리 네트워크를 분석하는 기능을 가지고 있습니다. 계산 결과를 OGRLayer 포맷으로, 또는 해당 레이어가 정의되지 않은 경우 콘솔 텍스트 출력으로 반환합니다. 모든 계산은 객체의 차단 상태를 고려해서 이루어집니다.

.. program:: gnmanalyse

.. option:: dijkstra <start_gfid> <end_gfid>

    데이크스트라(Dijkstra) 알고리즘을 이용해서 start_gfid 포인트에서 end_gfid 포인트까지 두 포인트 사이의 최적 경로를 계산합니다.

.. option:: kpaths <start_gfid> <end_gfid>

    (내부적으로 단일 경로 계산에 데이크스트라 알고리즘을 사용하는) 옌(Yen) 알고리즘을 사용해서 start_gfid 포인트에서 end_gfid 포인트까지 두 포인트 사이의 K번째 최단 경로를 계산합니다.

.. option:: resource

    "리소스 분포(resource distribution)"를 계산합니다. 너비 우선 탐색(breadth-first search) 기법을 사용해서 규칙이 'EMITTERS'로 표시한 객체들로부터 연결 요소 검색을 수행합니다.

.. option:: -d <ds_name>

    산출 경로를 가진 레이어를 저장할 데이터셋의 이름과 경로입니다. 기존 데이터셋일 필요는 없습니다.

.. option:: -f <ds_format>

    새로 생성되는 데이터셋의 포맷을 설정합니다.

.. option:: -l <layer_name>

    산출 레이어의 이름입니다. 레이어가 이미 존재하는 경우 레이어를 재작성할 것입니다.

.. option:: <gnm_name>

    작업할 네트워크 (경로와 이름)

.. option:: -dsco NAME=VALUE

    데이터셋 생성 옵션 (특정 포맷 지원)

.. option:: -lco NAME=VALUE

    레이어 생성 옵션 (특정 포맷 지원)

.. option:: -alo NAME=VALUE

    알고리즘 옵션 (특정 포맷 지원)
