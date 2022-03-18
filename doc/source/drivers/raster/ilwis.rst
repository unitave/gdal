.. _raster.ilwis:

================================================================================
ILWIS -- 래스터 맵
================================================================================

.. shortname:: ILWIS

.. built_in_by_default::

이 드라이버는 ILWIS 래스터 맵과 맵 목록 읽기 및 쓰기를 구현합니다. ``the.mpr`` (래스터 맵) 또는 ``the.mpl`` (맵 목록) 확장자를 가진 래스터 파일을 선택하십시오.

기능:

-  바이트, Int16, Int32 및 Float64 픽셀 데이터 유형을 지원합니다.
-  관련 ILWIS 래스터 맵 집합을 가진 맵 목록을 지원합니다.
-  지리참조 파일(.grf)을 읽고 씁니다. 북쪽이 위를 향하는(north-oriented) GeoRefCorner로의 지리참조 변환만 지원합니다. 가능한 경우, 모서리 좌표로부터 아핀 변환을 계산합니다.
-  좌표 파일(.csy)을 읽고 씁니다. CSY 파일에 정의된 투영 및 위도/경도 유형의 투영법 유형만 지원합니다. 사전 정의된 나머지 투영법 유형은 무시합니다.

제약:

-  내부 래스터 맵 저장소를 가진 (예: 일반 래스터 가져오기(Import General Raster)를 통해 생성된) 맵 목록을 지원하지 않습니다.
-  현재 ILWIS 도메인 파일(.dom) 및 표현 파일(.rpr)을 무시합니다.

주의: ``gdal/frmts/ilwis`` 로 구현되었습니다.

참고: http://www.itc.nl/ilwis/default.asp

드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::
