.. _raster_common_options:

================================================================================
래스터 프로그램 용 공통 옵션
================================================================================

GDAL 명령줄 프로그램들은 모두 다음 공통 옵션을 지원합니다.

.. option:: --version

    GDAL 버전을 리포트한 다음 엑시트합니다.

.. option:: --build

    GDAL에 대한 상세 정보를 리포트한 다음 엑시트합니다.

.. _raster_common_options_formats:
.. option:: --formats

    현재 GDAL 빌드가 지원하는 모든 (읽기전용 및 읽기쓰기) 래스터 포맷들의 목록을 표시한 다음 엑시트합니다. 포맷 지원은 다음과 같이 표시됩니다: 'ro'는 읽기전용(read-only)이고, 'rw'는 읽기 또는 쓰기를 허용하며 (예: CreateCopy를 지원) 'rw+'는 읽기, 쓰기와 업데이트를 허용하는 (예: Create를 지원) 드라이버입니다. 'v'는 가상 IO(/vsimem, /vsigzip, /vsizip 등등)를 지원하는 포맷에 붙으며, 's'는 하위 데이터셋을 지원하는 포맷에 붙습니다. 주의: gdalwarp의 산출물로써 무결한 포맷들은 CreateCopy() 메소드만이 아니라 Create() 메소드도 지원하는 (rw+로 표시된) 포맷들입니다.

.. option:: --format <format>

    단일 포맷 드라이버에 대한 상세 정보를 목록화합니다. 이때 포맷의 이름은 GTiff처럼 --formats 목록에 표시된 단축명이어야 합니다.

.. _raster_common_options_optfile:
.. option:: --optfile <filename>

    명명된 파일을 읽고 그 내용을 명령줄 옵션 목록에 대체시킵니다. #으로 시작하는 행은 무시할 것입니다. 여러 단어로 이루어진 인자는 큰따옴표로 묶일 수도 있습니다.

.. option:: --config <key> <value>

    명명된 환경설정 키워드를 환경 변수로 설정하는 대신 입력된 값으로 설정합니다. 공통 환경설정 키워드로는 GDAL_CACHEMAX(메가바이트 단위로 내부 캐시 작업을 하기 위해 사용되는 메모리), :decl_configoption:`GDAL_DATA` (GDAL "data" 디렉터리의 경로) 등이 있습니다. 기타 :ref:`환경설정 옵션 <list_config_options>` 이 개별 드라이버에 영향을 미칠 수도 있습니다.

.. option:: --debug <value>

    디버그 작업 메시지가 어떤 내용을 내놓을지를 제어합니다. 값을 ON으로 설정하면 모든 디버그 메시지를 활성화할 것입니다. 값을 OFF로 설정하면 모든 디버그 메시지를 비활성화합니다. 다른 값으로 설정하는 경우, 디버그 접두어 코드에 해당 문자열을 담고 있는 디버그 메시지만 선택할 것입니다.

.. option:: --help-general

    일반적인 GDAL 명령줄 옵션을 위한 간단한 활용법 메시지를 표시한 뒤 엑시트합니다.

새 파일 생성하기
------------------

기존 파일에 접근해서 파일을 읽는 과정은 일반적으로 매우 단순합니다. 명령줄에 파일 또는 데이터셋의 이름을 지정하기만 하면 됩니다. 하지만 파일을 생성하는 과정은 훨씬 복잡합니다. 생성할 포맷을 지정해야 할 수도 있고, 어떻게 생성할지에 대해 영향을 미치는 생성 옵션들도 다양하고, 또 좌표계도 할당해야 할 수도 있습니다. 서로 다른 GDAL 유틸리티들이 이 옵션들 가운데 다수를 유사한 방법으로 처리하고 있습니다. 다음은 이런 옵션들에 대한 설명입니다.

.. option:: -of <format>

    새 파일을 어떤 포맷으로 생성할지 선택합니다. 포맷을 GTiff(GeoTIFF) 또는 HFA(Erdas Imagine)처럼 단축명으로 지정하십시오. 모든 포맷 코드들의 목록은 :option:`--formats` 스위치로 확인할 수 있습니다. 이때 ``(rw)`` (읽기/쓰기)로 표시된 포맷들만 작성할 수 있습니다.

    .. versionadded:: 2.3

        포맷을 지정하지 않는 경우, 확장자로 포맷을 추정합니다.
        이전에는 일반적으로 래스터의 경우 GTiff, 또는 벡터의 경우 ESRI Shapefile이었습니다.

.. include:: options/co.rst

.. option:: -a_srs <srs>
.. option:: -s_srs <srs>
.. option:: -t_srs <srs>

    몇몇 (예: :command:`gdal_translate` 및 :command:`gdalwarp`) 유틸리티는 :option:`-a_srs` (산출물에 SRS를 할당), :option:`-s_srs` (소스 SRS) 그리고 :option:`-t_srs` (대상 SRS) 같은 명령줄 옵션으로 좌표계를 지정할 수 있는 기능을 포함하고 있습니다. 이 유틸리티들은 다양한 포맷에 공간좌표계(SRS; Spatial Reference System)를 할당할 수 있습니다.

    * ``NAD27|NAD83|WGS84|WGS72``

        이 흔한 지리좌표계(위도/경도)들은 이름만으로 사용할 수 있습니다.

    * ``EPSG:n``

        EPSG 코드를 기반으로 (투영 또는 지리) 좌표계를 선택할 수 있습니다. 예를 들어 :samp:`EPSG:27700` 은 영국 국가 그리드입니다. GDAL 데이터 파일 :file:`gcs.csv` 와 :file:`pcs.csv` 에서 EPSG 좌표계 목록을 볼 수 있습니다.

    * ``PROJ.4 정의``

        PROJ.4 정의 문자열을 좌표계로 사용할 수 있습니다. 명령어에 proj.4 문자열을 단일 인자로 (보통 큰따옴표를 사용해서) 유지하도록 신경을 쓰십시오.

        예를 들면 :samp:`+proj=utm +zone=11 +datum=WGS84` 같은 문자열입니다.

    * ``OpenGIS WKT(Well Known Text)``

        OGC(Open GIS Consortium)는 단순 피처 사양의 일부로써 좌표계를 설명하기 위한 텍스트 포맷을 정의하고 있습니다. 이 포맷은 GDAL에서 사용되는 좌표계 용 내부 작동 포맷입니다. WKT 좌표계 정의를 담고 있는 파일의 이름을 좌표계 인자로 사용할 수도 있고, 전체 좌표계 자체를 명령줄 옵션으로 사용할 수도 있습니다. (물론 WKT 안에서 모든 따옴표들을 맞추는 일이 힘들긴 하겠지요.)

    * ``ESRI WKT(Well Known Text)``

        ESRI는 ArcGIS 제품에 OGC WKT 포맷을 살짝 바꾼 포맷(ArcGIS :file:`.prj` 파일)을 사용하며,
        이 포맷은 WKT 파일과 비슷한 방식으로 사용할 수도 있습니다. 하지만 파일 이름 앞에 접두어
        ``ESRI::`` 가 붙어야 합니다.

        예를 들면, `"ESRI::NAD 1927 StatePlane Wyoming West FIPS 4904.prj"` 처럼 말이죠.

    * ``URL로부터 나온 좌표(Spatial Reference)``

        예시: http://spatialreference.org/ref/user/north-pacific-albers-conic-equal-area/

    * :file:`파일명`

        WKT, PROJ.4 문자열, 또는 XML/GML 좌표계 정의를 담고 있는 파일을 제공할 수 있습니다.
