.. _gdalmanage:

================================================================================
gdalmanage
================================================================================

.. only:: html

    래스터 데이터 파일을 식별, 삭제, 재명명, 복사합니다.

.. Index:: gdalmanage

개요
--------

.. code-block::

    Usage: gdalmanage mode [-r] [-u] [-f format]
                      datasetname [newdatasetname]

설명
-----------

:program:`gdalmanage` 프로그램은 선택한 *모드* 에 따라 래스터 데이터 파일에 여러 작업을 수행할 수 있습니다. 이 작업에는 래스터 데이터 유형을 식별하고, 파일을 삭제, 재명명, 복사하는 기능이 포함됩니다.

.. option:: <mode>

    작업 모드

    **identify** *<datasetname>*:
        파일의 데이터 포맷을 목록화합니다.
    **copy** *<datasetname>* *<newdatasetname>*:
        래스터 파일의 복사본을 새 이름으로 생성합니다.
    **rename** *<datasetname>* *<newdatasetname>*:
        래스터 파일의 이름을 변경합니다.
    **delete** *<datasetname>*:
        래스터 파일을 삭제합니다.

.. option:: -r

    파일/폴더들을 재귀적으로 스캔해서 래스터 파일을 찾습니다.

.. option:: -u

    파일 유형이 식별되지 않는 경우 실패를 리포트합니다.

.. option:: -f <format>

    응용 프로그램이 식별하지 못 하는 래스터 파일의 포맷을 지정합니다. 단축 데이터 포맷명을 (예: *GTiff*) 사용하십시오.

.. option:: <datasetname>

    작업할 래스터 파일입니다.

.. option:: <newdatasetname>

    복사 및 재명명 모드의 경우, 운영 체제에서 복사 및 이동 명령어를 사용할 때와 마찬가지로 사용자가 *소스* 파일명과 *대상* 파일명을 지정해야 합니다.

예시
--------

식별 모드 사용
~~~~~~~~~~~~~~~~~~~

*identify* 모드를 사용, 데이터 파일명을 지정해서 래스터 파일의 데이터 포맷을 리포트합니다:

.. code-block::

    $ gdalmanage identify NE1_50M_SR_W.tif

    NE1_50M_SR_W.tif: GTiff

재귀(recursive) 모드를 사용하면 하위 폴더를 스캔해서 데이터 포맷을 리포트할 것입니다:

.. code-block::

    $ gdalmanage identify -r 50m_raster/

    NE1_50M_SR_W/ne1_50m.jpg: JPEG
    NE1_50M_SR_W/ne1_50m.png: PNG
    NE1_50M_SR_W/ne1_50m_20pct.tif: GTiff
    NE1_50M_SR_W/ne1_50m_band1.tif: GTiff
    NE1_50M_SR_W/ne1_50m_print.png: PNG
    NE1_50M_SR_W/NE1_50M_SR_W.aux: HFA
    NE1_50M_SR_W/NE1_50M_SR_W.tif: GTiff
    NE1_50M_SR_W/ne1_50m_sub.tif: GTiff
    NE1_50M_SR_W/ne1_50m_sub2.tif: GTiff

복사 모드 사용
~~~~~~~~~~~~~~~

래스터 데이터를 복사합니다:

.. code-block::

    $ gdalmanage copy NE1_50M_SR_W.tif ne1_copy.tif

재명명 모드 사용
~~~~~~~~~~~~~~~~~

래스터 데이터를 재명명합니다:

.. code-block::

    $ gdalmanage rename NE1_50M_SR_W.tif ne1_rename.tif

삭제 모드 사용
~~~~~~~~~~~~~~~~~

래스터 데이터를 삭제합니다:

.. code-block::

    gdalmanage delete NE1_50M_SR_W.tif
