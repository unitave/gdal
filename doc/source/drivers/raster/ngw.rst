.. _raster.ngw:

NGW -- NextGIS 웹
==================

.. versionadded:: 2.4

.. shortname:: NGW

.. build_dependencies:: libcurl

NextGIS 웹(Web)은 서버 GIS로, 웹브라우저에서 지리 데이터(geodata)를 저장하고 편집하며 맵을 출력할 수 있습니다.
또 NextGIS 웹은 다른 NextGIS 소프트웨어와도 지리 데이터를 공유할 수 있습니다.

NextGIS 웹의 기능은 다음과 같습니다:

-  웹브라우저에 맵 출력 (서로 다른 레이어와 스타일을 가지고 있는 서로 다른 맵들)
-  유연한 권한 관리
-  PostGIS로부터 지리 데이터를 불러오거나 GIS 포맷(ESRI Shapefile, GeoJSON 또는 GeoTIFF)으로부터 가져오기
-  GeoJSON, CSV, ESRI Shapefile, Mapinfo TAB 등의 포맷으로부터 벡터 지리 데이터 불러오기
-  QGIS 프로젝트로부터 맵 스타일 가져오기 또는 직접 설정하기
-  TMS, WMS, MVT, WFS 서버로 작동
-  WMS 용 클라이언트로 작동
-  웹 인터페이스 또는 WFS-T 프로토콜을 통해 사용자가 레코드에 사진을 추가하고 레코드를 변경할 수 있음

NextGIS 웹은 오픈소스 소프트웨어입니다. (GPL 버전 2 이상의 사용 허가, `GNU 일반 공중 사용 허가서 버전 2 <https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html>`_ 참조)

드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

드라이버
-------

NextGIS 웹은 다음 래스터 유형들을 지원합니다:

-  래스터 스타일
-  벡터 스타일
-  WMS 레이어
-  WMS 서비스
-  래스터와 벡터 스타일을 결합한 웹 맵(Web Map)

NextGIS 웹 래스터 레이어는 각각 하나 이상의 래스터 스타일을 가질 수 있습니다.
NextGIS 웹 벡터 또는 PostGIS 레이어는 각각 하나 이상의 벡터 스타일을 가질 수 있습니다. (QGIS QML 또는 MapServer XML)
외부 WMS 서비스의 WMS 레이어에는 스타일이 없습니다.
WMS 서비스는 일반 WMS 프로토콜을 구현한 것입니다.

NGW 드라이버는 래스터 및 벡터 스타일과 WMS 레이어만 지원합니다.
래스터 데이터를 타일 또는 이미지로 가져올 수 있습니다. (현재 타일만 지원합니다.)

이 드라이버는 기존 소스 데이터셋의 래스터 상에서의 작업으로부터 읽기 및 복사를 지원합니다.

데이터셋 이름 문법
-------------------

다음은 NGW 데이터소스를 열기 위한 최소한의 문법입니다:

NGW:[NextGIS 웹 URL][/resource/][resource identifier]

-  **NextGIS 웹 URL**:
   NextGIS.com 클라우드 서비스(예: https://demo.nextgis.com)를 가리키는 URL일 수도 있고, 또는 포트와 추가 경로를 포함하는 다른 URL(예: http://192.168.1.1:8000/test)일 수도 있습니다.
-  **resource**:
   전체 URL에서 리소스 식별자를 분리하는 필수 키워드입니다.
-  **resource identifier**:
   0에서 시작하는 양의 숫자값입니다.
   리소스 그룹, 벡터, PostGIS 또는 래스터 레이어, 스타일일 수도 있습니다.

식별자가 리소스 그룹인 경우, 모든 벡터 레이어, PostGIS, 래스터 레이어, 스타일을 하위 리소스로 목록화할 것입니다. 그렇지 않은 경우 식별자가 개별 래스터일 것입니다.

환경설정 옵션
---------------------

다음과 같은 환경설정 옵션을 사용할 수 있습니다:

-  **NGW_USERPWD**:
   쌍점으로 구분된 사용자명과 비밀번호입니다.
   선택 옵션이며, 열기 옵션을 이용해서 설정할 수도 있습니다.

-  **NGW_CACHE_EXPIRES**:
   캐시된 파일을 사용할 수 있는 유효 기간을 초 단위로 설정합니다.
   유효 기간을 초과했을 때 최대 캐시 용량을 넘어섰다면 캐시된 파일을 삭제합니다. 유효 기간을 초과한 파일을 웹으로부터 받은 새 파일로 덮어쓸 수도 있습니다. 기본값은 604800(7일)입니다.

-  **NGW_CACHE_MAX_SIZE**:
   바이트 단위 최대 캐시 용량을 설정합니다. 캐시가 최대 용량을 넘어선 경우, 캐시된 파일 가운데 유효 기간을 초과한 파일을 삭제할 것입니다. 기본값은 67108864(64Mb)입니다.

-  **NGW_JSON_DEPTH**:
   파싱할 수 있는 JSON 응답의 심도를 설정합니다.
   심도가 이 값을 초과하는 경우 파싱 오류를 발생시킵니다.

인증
--------------

모든 작업 (읽기, 쓰기, 메타데이터 가져오기, 속성 변경 등등) 시 인증 접근이 필요할 수도 있습니다. 열기 옵션, 생성 옵션 또는 환경설정 옵션에서 사용자명과 비밀번호를 지정하면 인증된 접근을 할 수 있습니다.

열기 옵션
------------

다음과 같은 열기 옵션을 사용할 수 있습니다:

-  **USERPWD**:
   쌍점으로 구분된 사용자명과 비밀번호입니다.

-  **CACHE_EXPIRES=604800**:
   캐시된 파일을 사용할 수 있는 유효 기간을 초 단위로 설정합니다.
   유효 기간을 초과했을 때 최대 캐시 용량을 넘어섰다면 캐시된 파일을 삭제합니다. 유효 기간을 초과한 파일을 웹으로부터 받은 새 파일로 덮어쓸 수도 있습니다. 기본값은 604800(7일)입니다.

-  **CACHE_MAX_SIZE=67108864**:
   바이트 단위 최대 캐시 용량을 설정합니다. 캐시가 최대 용량을 넘어선 경우, 캐시된 파일 가운데 유효 기간을 초과한 파일을 삭제할 것입니다. 기본값은 67108864(64Mb)입니다.

-  **JSON_DEPTH=32**:
   파싱할 수 있는 JSON 응답의 심도를 설정합니다.
   심도가 이 값을 초과하는 경우 파싱 오류를 발생시킵니다.

생성 복사 옵션
-------------------

NextGIS 웹은 GeoTIFF 포맷 파일만 지원합니다. 이전 3.1버전은 바이트 데이터 유형의 밴드 3개(RGB) 또는 4개(RGBA)를 가진 래스터만 지원했습니다. CreateCopy() 함수에서 소스 데이터셋이 GeoTIFF 포맷 파일이면 그대로 복사할 것입니다. 다른 포맷이라면 임시 GeoTIFF 파일에 추가적인 변환을 실행할 것입니다.

다음 복사 옵션들을 사용할 수 있습니다:

-  KEY:
   키 값입니다. NextGIS 웹 전체에서 유일한(unique) 값이어야만 합니다. 선택 옵션입니다.

-  DESCRIPTION:
   리소스 설명입니다. 선택 옵션입니다.

-  RASTER_STYLE_NAME:
   래스터 스타일의 이름입니다. 선택 옵션입니다. 기본값은 래스터 레이어 이름입니다.

-  RASTER_QML_PATH:
   QGIS QML 래스터 스타일 파일을 가리키는 경로입니다. RGB/RGBA 이미지의 경우 선택 옵션이고, 다른 밴드 개수/픽셀 유형을 가진 이미지의 경우 필수 옵션입니다.

-  USERPWD:
   쌍점으로 구분된 사용자명과 비밀번호입니다.

-  CACHE_EXPIRES=604800:
   캐시된 파일을 사용할 수 있는 유효 기간을 초 단위로 설정합니다.
   유효 기간을 초과했을 때 최대 캐시 용량을 넘어섰다면 캐시된 파일을 삭제합니다. 유효 기간을 초과한 파일을 웹으로부터 받은 새 파일로 덮어쓸 수도 있습니다. 기본값은 604800(7일)입니다.

-  CACHE_MAX_SIZE=67108864:
   바이트 단위 최대 캐시 용량을 설정합니다. 캐시가 최대 용량을 넘어선 경우, 캐시된 파일 가운데 유효 기간을 초과한 파일을 삭제할 것입니다. 기본값은 67108864(64Mb)입니다.

-  JSON_DEPTH=32:
   파싱할 수 있는 JSON 응답의 심도를 설정합니다.
   심도가 이 값을 초과하는 경우 파싱 오류를 발생시킵니다.

메타데이터
---------

데이터소스, 벡터, PostGIS, 래스터 레이어 및 스타일에서 NextGIS 웹 메타데이터를 지원합니다. 메타데이터는 특화 도메인 "NGW"에 저장됩니다. NextGIS 웹 메타데이터는 문자열과 숫자값 유형을 지원합니다. 10진수 숫자값을 가진 메타데이터 키는 접미어 **.d** 가 붙고, 실수 숫자값의 경우 접미어 **.f** 가 붙을 것입니다. 새 메타데이터 항목을 생성하려면, SetMetadataItem() 함수와 알맞은 접미어를 사용해서 NGW 도메인에 새 키=값 쌍을 추가하십시오. NextGIS 웹으로 전송하는 과정에서 접미어를 생략시킬 것입니다. 사용자는 숫자가 문자열로부터 숫자값으로 정확하게 변환되었는지 확인해야만 합니다.

NextGIS 웹은 리소스 설명과 키를 기본 도메인에 있는 알맞은 *description* 및 *keyname* 메타데이터 항목으로 매핑시킵니다. 이런 메타데이터 항목들을 변경하면 리소스 속성을 업데이트시킬 것입니다.

NextGIS 웹은 리소스 생성 날짜, 유형 및 상위 식별자를 기본 도메인에 있는 알맞은 *creation_date*, *resource_type* 및 *parent_id* 읽기전용 메타데이터 항목으로 매핑시킵니다.

예시
--------

데이터소스 내용 읽어오기 (1730은 리소스 그룹 식별자입니다):

::

       gdalinfo NGW:https://demo.nextgis.com/resource/1730

래스터 상세 정보 읽어오기 (1734는 래스터 레이어 식별자입니다):

::

       gdalinfo NGW:https://demo.nextgis.com/resource/1734

참고
--------

-  :ref:`NextGIS 웹 드라이버의 벡터 지원 <vector.ngw>`
-  `NextGIS 웹 문서 <http://docs.nextgis.com/docs_ngweb/source/toc.html>`_
-  `개발자를 위한 NextGIS 웹 <http://docs.nextgis.com/docs_ngweb_dev/doc/toc.html>`_
