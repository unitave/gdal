.. _gdaltransform:

================================================================================
gdaltransform
================================================================================

.. only:: html

    좌표를 변환합니다.

.. Index:: gdaltransform

개요
--------

.. code-block::

    gdaltransform [--help-general]
        [-i] [-s_srs srs_def] [-t_srs srs_def] [-to "NAME=VALUE"]
        [-ct proj_string] [-order n] [-tps] [-rpc] [-geoloc]
        [-gcp pixel line easting northing [elevation]]* [-output_xy]
        [srcfile [dstfile]]

설명
-----------

gdaltransform 유틸리티는 좌표 목록을 GCP 기반 변환을 포함하는 모든 지원 투영법으로 재투영합니다.

.. program:: gdaltransform

.. option:: -s_srs <srs_def>

    소스 공간 좌표계를 설정합니다. OGRSpatialReference.SetFromUserInput() 호출이 지원하는 모든 좌표계를 전송(pass)할 수 있습니다. 이 모든 좌표계는 EPSG PCS와 GCS들(예: EPSG:4296), (앞에서 보인대로의) PROJ.4 선언문, 또는 WKT를 담고 있는 .prj 파일의 이름을 포함합니다.

.. option:: -t_srs <srs_def>

    대상 공간 좌표계를 설정합니다. OGRSpatialReference.SetFromUserInput() 호출이 지원하는 모든 좌표계를 전송(pass)할 수 있습니다. 이 모든 좌표계는 EPSG PCS와 GCS들(예: EPSG:4296), (앞에서 보인대로의) PROJ.4 선언문, 또는 WKT를 담고 있는 .prj 파일의 이름을 포함합니다.

.. option:: -ct <string>

    PROJ 문자열(한 단계 작업 또는 +proj=pipeline으로 시작하는 여러 단계 작업 문자열)로, CoordinateOperation을 설명하는 WKT2 문자열, 또는 소스로부터 대상 좌표계로의 기본 변환을 무시하는 urn:ogc:def:coordinateOperation:EPSG::XXXX URN입니다. 소스 및 대상 좌표계의 축 순서를 고려해야만 합니다.

    .. versionadded:: 3.0

.. option:: -to NAME=VALUE

    :cpp:func:`GDALCreateGenImgProjTransformer2` 에 전송하기에 적합한 변환기(transformer) 옵션을 설정합니다.

.. option:: -order <n>

    왜곡 작업에 쓰이는 다항(polynomial)의 순서(1에서 3까지)입니다. 기본값은 GCP 개수를 기반으로 하는 다항 순서를 선택하는 것입니다.

.. option:: -tps

    사용할 수 있는 GCP를 기반으로 박막 스플라인(thin plate spline) 변환기를 강제로 사용시킵니다.

.. option:: -rpc

    RPC를 강제로 사용시킵니다.

.. option:: -geoloc

    지리위치 배열(Geolocation Array)를 강제로 사용시킵니다.

.. option:: -i

    역변환(Inverse transformation): 대상으로부터 소스로.

.. option:: -gcp <pixel> <line> <easting> <northing> [<elevation>]

    변환 작업에 쓰일 GCP를 지정합니다. (일반적으로 3개 이상이 필요합니다.)

.. option:: -output_xy

    산출물을 "x y z" 대신 "x y"로 제한합니다.

.. option:: <srcfile>

    소스 또는 GCP의 투영법 정의를 가진 파일입니다. 지정하지 않는 경우, 명령줄 :option:`-s_srs` 또는 :option:`-gcp` 파라미터로부터 소스 투영법을 읽어옵니다.

.. option:: <dstfile>

    대상 투영법 정의를 가진 파일입니다.

좌표를 쌍으로, (3D의 경우) 3개 값으로, 또는 (GDAL 3.0.0부터 X, Y, Z, 시간의 경우) 4개 값으로 읽어와서, 표준 산출물에 동일한 방식으로 변환해서 작성합니다. GCP 기반 변환을 포함, gdalwarp가 제공하는 모든 변환 메소드를 처리합니다.

입력물과 산출물이 언제나 소수점(decimal) 양식이어야만 한다는 사실을 기억하십시오. 현재 DMS 입력 또는 산출을 지원하지 않습니다.

입력 이미지 파일을 지정한 경우, 입력물의 좌표는 해당 이미지의 픽셀/라인 좌표 단위입니다. 산출물 파일을 지정한 경우, 산출물의 좌표는 해당 이미지의 픽셀/라인 좌표 단위입니다.

예시
--------

재투영 예시
++++++++++++++++++++

어떤 투영 좌표계로부터 다른 투영 좌표계로의 단순 재투영:

::

    gdaltransform -s_srs EPSG:28992 -t_srs EPSG:31370
    177502 311865

"Belge 1972 / Belgian Lambert 72" 투영법을 사용하는 다음 미터 단위 산출물을 생성합니다:

::

    244510.77404604 166154.532871342 -1046.79270555763

이미지 RPC 예시
+++++++++++++++++

다음 명령어는 지정한 파일과 연관된 RPC 모델을 사용하는 RPC 기반 변환을 요청합니다. -i (inverse) 플래그를 사용하기 때문에, 산출물의 지리참조(WGS84) 좌표를 이미지 좌표로 다시 변환합니다.


::

    gdaltransform -i -rpc 06OCT20025052-P2AS-005553965230_01_P001.TIF
    125.67206 39.85307 50

이미지 상의 픽셀과 라인 단위로 측정된 산출물을 생성합니다:

::

    3499.49282422381 2910.83892848414 50

X, Y, Z, 시간 변환
++++++++++++++++++++

2000.0 시대(epoch) 좌표를 파라미터 15개를 사용해서 ITRF2000으로부터 ITRF93로 시간 의존적 헬메르트(Helmert) 좌표 변환:

::

    gdaltransform -ct "+proj=pipeline +step +proj=unitconvert +xy_in=deg \
    +xy_out=rad +step +proj=cart +step +proj=helmert +convention=position_vector \
    +x=0.0127 +dx=-0.0029 +rx=-0.00039 +drx=-0.00011 +y=0.0065 +dy=-0.0002 \
    +ry=0.00080 +dry=-0.00019 +z=-0.0209 +dz=-0.0006 +rz=-0.00114 +drz=0.00007 \
    +s=0.00195 +ds=0.00001 +t_epoch=1988.0 +step +proj=cart +inv +step \
    +proj=unitconvert +xy_in=rad +xy_out=deg"
    2 49 0 2000

경도, 위도 및 미터 단위 타원체 높이 단위로 측정된 산출물을 생성합니다:

::

    2.0000005420366 49.0000003766711 -0.0222802283242345
