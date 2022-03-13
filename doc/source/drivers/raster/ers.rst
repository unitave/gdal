.. _raster.ers:

================================================================================
ERS -- ERMapper .ERS
================================================================================

.. shortname:: ERS

.. built_in_by_default::

몇몇 제한이 있기는 하지만, GDAL은 .ers 헤더 파일을 가진 래스터 읽기 및 쓰기를 지원합니다. ERMapper는 RAW 데이터 포맷 라벨 작업은 물론 확장 메타데이터 및 기타 몇몇 파일 포맷을 위한 지리참조 제공을 위해 .ers 아스키 포맷을 사용합니다. ERS 포맷 또는 그 변이형들은 ERMapper 알고리즘의 설명을 저장하는 데 쓰이기도 하지만, GDAL이 지원하는 기능은 아닙니다.

ERS 헤더에 있는 PROJ, DATUM 및 UNITS 값들은 ERS 메타데이터 도메인에 리포트됩니다.

드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::

생성 문제점
---------------

생성 옵션:

-  **PIXELTYPE=value**: 이 옵션을 SIGNEDBYTE로 설정하면, 새 바이트형 파일을 강제로 부호 있는 바이트형으로 작성하게 할 수 있습니다.
-  **PROJ=name**: 사용할 ERS 투영법 문자열의 이름입니다. 흔히 쓰이는 값으로는 NUTM11 또는 GEODETIC 등이 있습니다. 이 옵션을 정의하면, SetProjection() 또는 SetGCPs()가 계산한 값을 무시할 것입니다.
-  **DATUM=name**: 사용할 ERS 원점(datum) 문자열의 이름입니다. 흔히 쓰이는 값으로는 WGS84 또는 NAD83 등이 있습니다. 이 옵션을 정의하면, SetProjection() 또는 SetGCPs()가 계산한 값을 무시할 것입니다.
-  **UNITS=name**: 사용할 ERS 투영법 단위의 이름입니다. METERS(기본값) 또는 FEET(미국 피트) 가운데 하나로 설정할 수 있습니다. 이 옵션을 정의하면, SetProjection() 또는 SetGCPs()가 계산한 값을 무시할 것입니다.

참고
--------

-  ``gdal/frmts/ers/ersdataset.cpp`` 로 구현되었습니다.
