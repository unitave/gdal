.. _gdal2tiles:

================================================================================
gdal2tiles.py
================================================================================

.. only:: html

    TMS 타일, KML, 단순 웹 뷰어를 가진 디렉터리를 생성합니다.

.. Index:: gdal2tiles

개요
--------

.. code-block::


    gdal2tiles.py [-p profile] [-r resampling] [-s srs] [-z zoom]
                  [-e] [-a nodata] [-v] [-q] [-h] [-k] [-n] [-u url]
                  [-w webviewer] [-t title] [-c copyright]
                  [--processes=NB_PROCESSES] [--mpi] [--xyz]
                  --tilesize=PIXELS
                  [-g googlekey] [-b bingkey] input_file [output_dir] [COMMON_OPTIONS]

설명
-----------

이 유틸리티는 OSGeo 타일 맵 서비스 사양을 따르는 작은 타일들과 메타데이터를 가진 디렉터리를 생성합니다. 구글 지도, 오픈레이어스(OpenLayers)와 리플릿(Leaflet) 기반 뷰어를 가진 단순 웹 페이지도 생성합니다. 즉 사용자가 (MapServer 같은) 특수한 소프트웨어를 설치하거나 환경설정할 필요 없이 맵이 웹 브라우저에서 빠르게 서비스되기 때문에 누구라도 온라인에서 사용자의 맵을 편안하게 탐색할 수 있다는 뜻입니다. 웹 서버에 생성된 디렉터리를 업로드하기만 하면 됩니다.

GDAL2Tiles는 제공하는 맵이 EPSG:4326 투영법을 사용하는 경우 구글 어스 용 필수 메타데이터(KML SuperOverlay)도 생성합니다.

타일 생성 도중 월드 파일과 내장된 지리참조를 사용하지만, 제대로 된 지리참조 없이도 이미지를 공개할 수 있습니다.

.. note::

    바이트가 아닌 데이터 유형인 (예: ``Int16``, ``UInt16``, ...) 입력물의 경우 데이터 유형이 ``Byte`` 데이터 유형으로 고정되어 잘못된 결과를 내게 됩니다. 이를 피하려면 `gdal_translate` 유틸리티를 사용해서 입력물을 ``Byte`` 데이터 유형으로 변환해야 합니다.

.. note::

    입력물 드라이버의 환경설정 옵션이 gdal2tiles의 산출물에 영향을 미칠 수도 있습니다. 이런 드라이버 환경설정 옵션의 예로는 GDAL_PDF_DPI가 있는데, :ref:`configoptions` 에서 찾아볼 수 있습니다.


.. program:: gdal2tiles

.. option:: -p <PROFILE>, --profile=<PROFILE>

    타일 자르기(tile cutting) 프로파일(mercator, geodetic, raster) - 기본값은 'mercator'(구글 지도 호환)입니다.

    GDAL 3.2버전부터, GDAL data 디렉터리에 있는 tms_XXXX.json 파일로부터 추가 프로파일을 사용할 수 있습니다. (모든 확대/축소 수준이 동일한 원점, 타일 크기, 그리고 연이어 2배씩 변화하는 확대/축소 수준들 사이의 해상도를 사용해야 합니다.)

.. option:: -r <RESAMPLING>, --resampling=<RESAMPLING>

    리샘플링 메소드(average, near, bilinear, cubic, cubicspline, lanczos, antialias, mode, max, min, med, q1, q3) - 기본값은 'average'입니다.

.. option:: -s <SRS>, --s_srs=<SRS>

    소스 입력 데이터에 사용된 공간 좌표계입니다.

.. option:: --xyz

    TMS 대신 (OSM Slippy Map 표준인) XYZ 타일을 생성합니다. 기본 모드(TMS)에서는 y=0 위치에 있는 타일이 가장 남쪽에 있는 타일인 반면, (OGC WMTS도 사용하는) XYZ 모드에서는 y=0 위치에 있는 타일이 가장 북쪽에 있습니다.

    .. versionadded:: 3.1

.. option:: -z <ZOOM>, --zoom=<ZOOM>

    렌더링할 확대/축소 수준입니다(서식:'2-5', '10-' 또는 '10').

.. option:: -e, --resume

    다시 시작(resume) 모드입니다. 누락된 파일들만 생성합니다.

.. option:: -a <NODATA>, --srcnodata=<NODATA>

    입력 데이터셋에서 투명하다고 간주되는 값입니다. 입력 데이터셋이 이미 관련 NODATA 값을 가지고 있는 경우, 지정한 값으로 무시합니다.

.. option:: -v, --verbose

    타일 생성에 대한 자세한 설명을 생성합니다.

.. option:: -x, --exclude

    산출 타일셋에서 투명한 타일을 제외시킵니다.

.. option:: -q, --quiet

    stdout으로 나가는 메시지와 상태(status)를 비활성화합니다.

    .. versionadded:: 2.1

.. option:: --processes=<NB_PROCESSES>

    계산 속도를 높이기 위해 타일 작업에 사용할 병렬 프로세스의 개수입니다.

    .. versionadded:: 2.3

.. option:: --mpi

    mpiexec이 실행했다고 가정하고, MPI 병렬성(parallelism)을 활성화하고 --processes를 무시합니다. 작동하는 MPI 환경 및 파이썬 패키지 용 MPI(mpi4py)가 필수입니다. 사용자가 GDAL_CACHEMAX를 노드 당 메모리와 노드 당 실행된 프로세스의 개수를 기반으로 하는 프로세스 별 적절한 캐시 크기로 설정해야 합니다.

    .. versionadded:: 3.5

.. option:: --tilesize=<PIXELS>

    타일의 픽셀 단위 너비와 높이입니다. 기본값은 256입니다.

    .. versionadded:: 3.1

.. option:: -h, --help

    도움말 메시지를 표시하고 엑시트합니다.

.. option:: --version

    프로그램의 버전 숫자를 표시하고 엑시트합니다.


KML (구글 어스) 옵션
++++++++++++++++++++++++++

생성된 구글 어스 SuperOverlay 메타데이터 용 옵션

.. option:: -k, --force-kml

    구글 어스 용 KML을 생성합니다. 기본값은 'geodetic' 프로파일과 EPSG:4326 투영법을 사용하는 'raster'입니다. 이와 다른 투영법을 사용하는 데이터셋의 경우 주의하십시오!

.. option:: -n, --no-kml

    EPSG:4326 용 KML 파일을 자동 생성하지 않습니다.

.. option:: -u <URL>, --url=<URL>

    생성된 타일들이 공개될 URL 주소입니다.


웹 뷰어 옵션
++++++++++++++++++

구글 지도 방식으로 생성된 HTML 뷰어 용 옵션

.. option:: -w <WEBVIEWER>, --webviewer=<WEBVIEWER>

    생성할 웹 뷰어(all, google, openlayers, leaflet, mapml, none) - 기본값은 'all'입니다.

.. option:: -t <TITLE>, --title=<TITLE>

    맵의 제목입니다.

.. option:: -c <COPYRIGHT>, --copyright=<COPYRIGHT>

    맵의 저작권입니다.

.. option:: -g <GOOGLEKEY>, --googlekey=<GOOGLEKEY>

    http://code.google.com/apis/maps/signup.html 에서 받은 구글 지도 API 키입니다.

.. option:: -b <BINGKEY>, --bingkey=<BINGKEY>

    https://www.bingmapsportal.com/ 에서 받은 빙 맵 API 키입니다.


.. note::

    gdal2tiles.py는 파이썬 스크립트로, 파이썬 GDAL 바인딩을 대상으로 실행되어야 합니다.

MapML 옵션
+++++++++++++

GDAL 3.2버전부터 MapML을 지원합니다. --webviewer=mapml을 지정한 경우, --xyz도 지정했다고 가정하고, --profile=geodetic을 지정했다면 --tmscompatible도 설정했다고 가정합니다.

다음 프로파일을 지원합니다:

- mercator: OSMTILE MapML 타일 작업 스키마로 매핑
- geodetic: WGS84 MapML 타일 작업 스키마로 매핑
- APSTILE: tms_MapML_APSTILE.json 데이터 파일로부터

산출물 디렉터리에 생성된 MapML 파일은 ``mapml.mapl`` 입니다.

다음 옵션을 사용할 수 있습니다:

.. option:: --mapml-template=<filename>

    변수들을 대신할 템플릿 MapML 파일의 이름입니다. 지정하지 않는 경우 GDAL 데이터 리소스에 있는 일반 template_tiles.mapml 파일을 사용할 것입니다.

템플릿 MapML 파일의 ``${URL}`` 을 대신하기 위한 --url 옵션도 사용합니다.

예시
--------

기본 예시:

.. code-block::

  gdal2tiles.py --zoom=2-5 input.tif output_folder


MapML 생성:

.. code-block::

  gdal2tiles.py --zoom=16-18 -w mapml -p APSTILE --url "https://example.com" input.tif output_folder


MPI 예시:

.. code-block::

  mpiexec -n $NB_PROCESSES gdal2tiles.py --mpi --config GDAL_CACHEMAX 500 --zoom=2-5 input.tif output_folder
