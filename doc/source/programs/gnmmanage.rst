.. _gnmmanage:

================================================================================
gnmmanage
================================================================================

.. only:: html

    네트워크를 관리합니다.

.. Index:: gnmmanage

개요
--------

.. code-block::

    gnmmanage [--help][-q][-quiet][--long-usage]
            [info]
            [create [-f <format_name>] [-t_srs <srs_name>] [-dsco NAME=VALUE]... ]
            [import src_dataset_name] [-l layer_name]
            [connect <gfid_src> <gfid_tgt> <gfid_con> [-c <cost>] [-ic <inv_cost>] [-dir <dir>]]
            [disconnect <gfid_src> <gfid_tgt> <gfid_con>]
            [rule <rule_str>]
            [autoconnect <tolerance>]
            [delete]
            [change [-bl gfid][-unbl gfid][-unblall]]
            <gnm_name> [<layer> [<layer> ...]]


설명
-----------

:program:`gnmmanage` 프로그램은 GDAL의 지리 네트워크(geographical network) 상에서 다양한 관리 작업을 수행할 수 있습니다. 이 프로그램은 네트워크 생성 및 삭제는 물론 네트워크의 객체, 위상 및 규칙을 관리하는 기능을 가지고 있습니다.

.. program:: gnmmanage

.. option:: -info

    시스템 및 클래스 레이어, 네트워크 메타데이터, 네트워크 특수 참조 등 네트워크에 대한 다양한 정보를 출력합니다.

.. option:: create

    네트워크를 생성합니다.

    .. option:: -f <format_name>

        산출물 파일 포맷의 이름

    .. option:: -t_srs <srs_name>

        대상 공간 좌표계

    .. option:: -dsco NAME=VALUE

        name=value 쌍으로 설정하는 네트워크 설정 옵션

.. option:: import <src_dataset_name>

    복사할 데이터셋의 이름으로 레이어 가져오기

    .. option:: -l layer_name

    데이터셋에 있는 레이어 이름입니다. 설정하지 않는 경우 0번 레이어를 복사합니다.

.. option:: connect <gfid_src> <gfid_tgt> <gfid_con>

    gfid_src와 gfid_tgt가 꼭짓점이고 gfid_con이 경계인 위상 연결을 생성합니다. (시스템 경계를 삽입하려면 gfid_con을 -1로 지정하십시오.)

    다음 값들을 직접 할당할 수 있습니다:

    .. option:: -c <cost>

        비용/가중치

    .. option:: -ic <invcost>

        역비용(inverse cost)

    .. option:: -dir <dir>

        경계의 방향

.. option:: disconnect <gfid_src> <gfid_tgt> <gfid_con>

    네트워크 그래프에서 연결성을 제거합니다.

.. option:: rule <rule_str>

    지정한 rule_str 문자열로 네트워크에 규칙을 생성합니다.

.. option:: autoconnect <tolerance>

    지정한 Double 데이터 유형 허용 오차와 레이어 이름으로 위상을 자동 생성합니다. 레이어 이름을 지정하지 않으면 네트워크의 모든 레이어를 사용할 것입니다.

.. option:: delete

    네트워크를 삭제합니다.

.. option:: change

    네트워크 경계 또는 꼭짓점의 차단 상태(blocking state)를 변경합니다.

    .. option:: -bl <gfid>

        주요 작업 전에 객체를 차단합니다. 차단한 객체는 특수 레이어에 저장됩니다.

    .. option:: -unbl <gfid>

        주요 작업 전에 객체를 차단 해제합니다.

    .. option:: -unblall

        주요 작업 전에 차단된 객체를 모두 차단 해제합니다.

.. option:: <gnm_name>

    작업할 네트워크 (경로와 이름)

.. option:: <layer>

    네트워크 레이어의 이름
