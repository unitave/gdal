.. _vector.plscenes_data_v1:

PLScenes (플래닛 랩스 신), 데이터 v1 API
==========================================

.. versionadded:: 2.2

PLScenes 드라이버는 신(scene)과 그 메타데이터를 "PSOrthoTile", "REOrthoTile", "PSScene3Band", "PSScene4Band", "REScene", "Landsat8L1G", "Sentinel2L1C" 항목 유형별로 벡터 레이어 하나씩으로 목록화하는 읽기 전용 작업을 지원합니다. 이 드라이버는 래스터 신도 접근할 수 있습니다

드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

데이터셋 이름 문법
-------------------

데이터소스를 열기 위한 최소한의 문법은 다음과 같습니다:

::

   PLScenes:[options]

':' 기호 뒤에 추가적인 선택 파라미터를 지정할 수 있습니다. 현재 다음 파라미터들을 지원합니다:

-  **version=data_v1**:
   요청할 API 버전을 지정합니다.

-  **api_key=value**:
   플래닛 API 키를 지정합니다. API_KEY 열기 옵션 또는 :decl_configoption:`PL_API_KEY` 환경설정 옵션으로 지정하지 않는 경우 반드시 지정해야만 합니다.

-  **follow_links=YES/NO**:
   각 신(벡터) 뒤에 자산(asset) 링크가 붙어야 할지 여부를 선택합니다. 자산을 가져오려면 각 신별로 HTTP 요청을 해야 하는데, 수많은 상품들을 처리하는 경우 성능에 영향을 미칠 수도 있습니다. 기본값은 NO입니다.

-  **scene=scene_id**:
   래스터 데이터에 접근하는 경우 신 ID를 지정합니다. 벡터 레이어 접근의 경우 선택 파라미터입니다.

-  **itemtypes=name**:
   항목 유형 이름을 지정합니다. 벡터 레이어 접근의 경우 선택 파라미터이고, 래스터 접근의 경우 필수 파라미터입니다.

-  **asset=value**:
   (래스터를 가져오는 경우) 자산 유형을 지정합니다. 기본값은 "visual"입니다. 벡터 레이어 접근의 경우 선택 옵션입니다. 신의 'visual' 자산 카테고리가 존재하지 않는데 이 옵션을 지정하지 않는다면 (또는 이 옵션의 값을 'list'로 지정한다면) 반환되는 데이터셋이 사용할 수 있는 자산 카테고리를 위한 하위 데이터셋을 가질 것입니다.

-  **medata=YES/NO**: (래스터 전용)
   API로부터 신 메타데이터를 가져와서 래스터 데이터셋에 추가해야 할지 여부를 선택합니다. 기본값은 YES입니다.

파라미터를 여러 개 지정하는 경우 쉼표로 구분해야만 합니다.

열기 옵션
------------

다음과 같은 열기 옵션들을 사용할 수 있습니다:

-  **VERSION=data_v1**:
   요청할 API 버전을 지정합니다.

-  **API_KEY=value**:
   플래닛 API 키를 지정합니다.

-  **FOLLOW_LINKS=YES/NO**:
   각 신(벡터) 뒤에 자산(asset) 링크가 붙어야 할지 여부를 선택합니다. 자산을 가져오려면 각 신별로 HTTP 요청을 해야 하는데, 수많은 상품들을 처리하는 경우 성능에 영향을 미칠 수도 있습니다. 기본값은 NO입니다.

-  **SCENE=scene_id**:
   래스터 데이터에 접근하는 경우 신 ID를 지정합니다. 벡터 레이어 접근의 경우 선택 옵션입니다.

-  **ITEMTYPES=name**:항목 유형 이름을 지정합니다. 벡터 레이어 접근의 경우 선택 옵션이고, 래스터 접근의 경우 필수 옵션입니다.

-  **ASSET=value**:
   (래스터를 가져오는 경우) 자산 유형을 지정합니다. 기본값은 "visual"입니다. 벡터 레이어 접근의 경우 선택 옵션입니다. 신의 'visual' 자산 카테고리가 존재하지 않는데 이 옵션을 지정하지 않는다면 (또는 이 옵션의 값을 'list'로 지정한다면) 반환되는 데이터셋이 사용할 수 있는 자산 카테고리를 위한 하위 데이터셋을 가질 것입니다.

-  **RANDOM_ACCESS=YES/NO**:
   래스터에 임의 접근 모드로 접근해야 할지 여부를 선택합니다. (그러나 최적 효율이 아닐 수도 있습니다.) NO로 지정하면 인메모리로 처리합니다. 기본값은 YES입니다.

-  **ACTIVATION_TIMEOUT=int**:
   (래스터) 자산 활성화 대기 시간을 초 단위로 지정합니다. 기본값은 3600입니다.

-  **METADATA=YES/NO**: (래스터 전용)
   API로부터 신 메타데이터를 가져와서 래스터 데이터셋에 추가해야 할지 여부를 선택합니다. 기본값은 YES입니다.

환경설정 옵션
-------------

다음 :ref:`환경설정 옵션 <configoptions>` 을 사용할 수 있습니다:

-  :decl_configoption:`PL_API_KEY` =value:
   플래닛 API 키를 지정합니다.

속성
----------

GDAL 환경설정에 있는 "plscensconf.json" 파일로부터 레이어 필드 정의를 작성합니다. 다운로드할 수 있는 상품을 가리키는 링크는 *asset_XXXXX_location* 속성에 있습니다. 자산이 활성화된 경우 XXXXX가 자산 카테고리 ID입니다. 활성화되지 않았다면 *asset_XXXXX_activate_link* 속성에 있는 URL에 POST 요청을 전송해서 활성화시켜야 합니다. (래스터 드라이버는 이 과정을 자동으로 수행합니다.)

도형
~~~~~~~~

각 신의 촬영 범위(footprint)를 경도/위도 WGS84 좌표계(EPSG:4326)를 사용하는 멀티폴리곤으로 리포트합니다.

필터링
~~~~~~~~~

이 드라이버는 :cpp:func:`OGRLayer::SetSpatialFilter` 함수에 설정된 모든 공간 필터를 서버로 포워딩할 것입니다. :cpp:func:`OGRLayer::SetAttributeFilter` 함수에 설정된 단순 속성 필터도 마찬가지입니다. 모든 속성이 모든 비교 연산자를 지원하지는 않는다는 사실을 기억하십시오. `메타데이터 속성 <https://www.planet.com/docs/v0/scenes/#metadata>`_ 에 있는 비교 연산자(comparator) 열을 참조하십시오.

페이지 작업(Paging)
~~~~~~~~~~~~~~~~~~~

기본적으로 서버로부터 객체들을 250개 덩어리로 가져옵니다. (이 값은 서버가 받아들일 수 있는 최대 개수입니다.) :decl_configoption:`PLSCENES_PAGE_SIZE` 환경설정 옵션으로 이 개수를 변경할 수 있습니다.

벡터 데이터 (신 메타데이터) 예시
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

(계정 권한으로) 사용할 수 있는 모든 신을 목록화하기:

::

   ogrinfo -ro -al "PLScenes:" -oo API_KEY=some_value

또는

::

   ogrinfo -ro -al "PLScenes:api_key=some_value"

또는

::

   ogrinfo -ro -al "PLScenes:" --config PL_API_KEY some_value

(위도,경도)=(40,-100) 포인트 아래에서 사용할 수 있는 모든 PSOrthoTile 항목 유형 신을 목록화하기:

::

   ogrinfo -ro -al "PLScenes:" -oo API_KEY=some_value PSOrthoTile -spat -100 40 -100 40

(위도,경도)=(40,-100)에서 (위도,경도)=(39,-99)까지의 경계 상자 안에서 사용할 수 있는 모든 신을 목록화하기:

::

   ogrinfo -ro -al "PLScenes:" -oo API_KEY=some_value -spat -100 40 -99 39

기준과 일치하는 모든 사용할 수 있는 이미지를 목록화하기:

::

   ogrinfo -ro -al "PLScenes:" -oo API_KEY=some_value PSOrthoTile -where "acquired >= '2015/03/26 00:00:00' AND cloud_cover < 10"

다운로드할 수 있는 신을 모두 목록화하기:

::

   ogrinfo -ro -al -q "PLScenes:" -oo API_KEY=some_value PSOrthoTile -where "permissions='assets:download'"

래스터 접근
-------------

신 ID를 'scene' 파라미터 또는 SCENE 열기 옵션으로 지정했다는 가정 하에, 신을 래스터 데이터셋으로서 접근할 수 있습니다. 'itemtypes' 파라미터 또는 ITEMTYPES 열기 옵션도 지정되어 있어야만 합니다. 'asset' 파라미터 또는 ASSET 열기 옵션으로 (visual, analytic 등등의) 자산 유형을 지정할 수 있습니다. 신 ID는 객체의 'id' 필드값의 내용입니다.

상품이 서버 상에 이미 생성되어 있지 않은 경우, 상품 생성이 활성화되고 드라이버는 상품을 사용할 수 있을 때까지 대기할 것입니다. ACTIVATION_TIMEOUT 열기 옵션으로 이 재시도의 제한 대기 시간을 환경설정할 수 있습니다.

래스터 접근 예시
~~~~~~~~~~~~~~~~~~~~~~

래스터 메타데이터 출력하기:

::

   gdalinfo "PLScenes:scene=scene_id,itemtypes=itemypes,asset=analytic" -oo API_KEY=some_value

또는

::

   gdalinfo "PLScenes:" -oo API_KEY=some_value -oo ITEMTYPES=itemtypes -oo SCENE=scene_id -oo ASSET=analytic

전체 파일을 변환/다운로드하기:

::

   gdal_translate "PLScenes:" -oo API_KEY=some_value -oo SCENE=scene_id \
                   -oo ITEMTYPES=itemtypes -oo ASSET=analytic -oo RANDOM_ACCESS=NO out.tif

참고
--------

-  :ref:`PLScenes <vector.plscenes>` 드라이버 일반 문서 페이지

-  `플래닛 랩스 신(Planet Labs Scenes) 데이터 API v1 문서 <https://developers.planet.com/docs/apis/data/>`_

-  :ref:`래스터 PLMosaic / 플래닛 랩스 모자이크(Planet Labs Mosaics) API <raster.plmosaic>` 드라이버

