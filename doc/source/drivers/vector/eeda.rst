.. _vector.eeda:

구글 어스 엔진 데이터 API
============================

.. versionadded:: 2.4

.. shortname:: EEDA

.. build_dependencies:: libcurl

이 드라이버는 구글 어스 엔진 REST API를 이용해서 이미지를 목록화하고 이미지의 메타데이터를 벡터 레이어로 목록화하는 읽기전용 작업을 지원합니다.

드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

데이터셋 이름 문법
-------------------

데이터소스를 열기 위한 최소한의 문법은 다음과 같습니다:

::

   EEDA:[collection]

<collection>은 projects/earthengine-public/assets/COPERNICUS/S2 같은 경로입니다.

열기 옵션
------------

다음 열기 옵션을 사용할 수 있습니다:

-  **COLLECTION=string**: 연결 문자열에 <collection>을 지정하지 않은 경우 <collection>을 지정합니다.

인증 메소드
----------------------

다음 인증 메소드를 사용할 수 있습니다:

-  :decl_configoption:`EEDA_BEARER` 또는 :decl_configoption:`EEDA_BEARER_FILE` 환경설정 옵션을 통해 전송되는 인증 베어러(Authentication Bearer)
-  :decl_configoption:`GOOGLE_APPLICATION_CREDENTIALS` 환경설정 옵션을 통해 전송되는 서비스 계정 프라이빗 키 파일
-  :decl_configoption:`EEDA_PRIVATE_KEY` 또는 :decl_configoption:`EEDA_PRIVATE_KEY_FILE` 및 :decl_configoption:`EEDA_CLIENT_EMAIL` 환경설정 옵션을 통해 전송되는 OAuth2 서비스 계정 인증
-  마지막으로 앞의 세 메소드가 모두 실패한 경우 코드가 현재 머신이 구글 컴퓨트 엔진 인스턴스인지 확인하고, 그렇다면 (가상 머신과 관련된 기본 서비스 계정을 이용해서) 구글 엔진 관련 권한을 사용할 것입니다. 강제로 가상 머신을 구글 컴퓨트 엔진 인스턴스로 (예를 들어 부트 로그에 접근할 수 없는 컨테이너에서 실행되는 코드처럼) 탐지되게 만들려면 :decl_configoption:`CPL_MACHINE_IS_GCE` 를 YES로 설정하면 됩니다.

환경설정 옵션
---------------------

다음 :ref:`환경설정 옵션들 <configoptions>` 을 사용할 수 있습니다:

-  :decl_configoption:`EEDA_BEARER` =value: API에 전송할 인증 베어러 값입니다. 이 옵션은 외부 코드가 토큰을 계산한 경우에만 유용합니다. 베어러의 무결성은 일반적으로 베어러를 요청한 시간 이후 1시간까지입니다.
-  :decl_configoption:`EEDA_BEARER_FILE` =filename: 값을 직접 전송하는 대신 값을 읽어와야 할 파일명을 지정한다는 점을 제외하면, EEDA_BEARER 옵션과 비슷합니다.
-  :decl_configoption:`GOOGLE_APPLICATION_CREDENTIALS` =file.json: 프라이빗 키와 클라이언트 이메일을 담고 있는 서비스 계정 프라이빗 키 파일입니다.
-  :decl_configoption:`EEDA_PRIVATE_KEY` =string: PKCS#8 PEM 헤더와 푸터를 가진 PKCS#8 PEM 파일로 인코딩된 RSA 프라이빗 키입니다. OAuth2 서비스 계정 인증을 사용하려면 EEDA_CLIENT_EMAIL과 함께 사용해야 합니다. GDAL이 libcrypto++ 또는 libssl을 대상으로 빌드되어 있어야 합니다.
-  :decl_configoption:`EEDA_PRIVATE_KEY_FILE` =filename: 키를 직접 전송하는 대신 키를 읽어와야 할 파일명을 지정한다는 점을 제외하면, EEDA_PRIVATE_KEY 옵션과 비슷합니다.
-  :decl_configoption:`EEDA_CLIENT_EMAIL` =string: OAuth2 서비스 계정 인증을 사용하려면 EEDA_PRIVATE_KEY 또는 EEDA_PRIVATE_KEY_FILE과 함께 지정해야 하는 이메일입니다.
-  :decl_configoption:`EEDA_PAGE_SIZE`:
   기본적으로 서버로부터 객체들을 1,000개 덩어리로 가져옵니다. (이 값은 서버가 받아들일 수 있는 최대 개수입니다.)  이 환경설정 옵션으로 이 개수를 변경할 수 있습니다.

속성
----------

"collection"으로부터 단일 이미지를 요청해서 이미지의 "properties" 요소에서 스키마를 추정, 레이어 필드 정의를 작성합니다. GDAL 환경설정의 "eedaconf.json" 파일도 읽어와서 "collection"의 스키마가 해당 파일에 서술되어 있는지 확인할 것입니다. 서술되어 있다면 앞에서 언급한 추정 작업을 수행하지 않을 것입니다.

다음 속성들은 항상 존재할 것입니다:

.. list-table:: EEDA Layer Field Definitions
   :header-rows: 1
   :widths: 15, 10, 30, 20
   
   * - 필드명
     - 유형
     - 의미
     - 서버쪽 필터 호환성
   * - name
     - String
     - 이미지 이름 (예: projects/earthengine-public/assets/COPERNICUS/S2/20170430T190351_20170430T190351_T10SEG)
     - Ｘ
   * - id
     - String
     - 이미지 ID, "projects/\*/assets/" 접두어가 없는 이름과 동일 (예: users/USER/ASSET)
     - Ｘ
   * - path
     - String
     - (더 이상 사용되지 않아 퇴출된) 이미지 경로, id와 동일
     - Ｘ
   * - gdal_dataset
     - String
     - :ref:`raster.eedai` 드라이버로 열 수 있는 GDAL 데이터셋 이름 (예: EEDAI:projects/earthengine-public/assets/COPERNICUS/S2/20170430T190351_20170430T190351_T10SEG)
     - Ｘ
   * - startTime
     - DateTime
     - 촬영 시작 날짜
     - **Ｏ** (최상위 수준에서의 >= 비교에 제한됨)
   * - endTime
     - DateTime
     - 촬영 종료 날짜
     - **Ｏ** (최상위 수준에서의 <= 비교에 제한됨)
   * - updateTime
     - DateTime
     - 업데이트 날짜
     - Ｘ
   * - sizeBytes
     - Integer64
     - 바이트 단위 파일 용량
     - Ｘ
   * - band_count
     - Integer
     - 밴드 개수
     - Ｘ
   * - band_max_width
     - Integer
     - 밴드들 가운데 최대 너비
     - Ｘ
   * - band_max_height
     - Integer
     - 밴드들 가운데 최대 높이
     - Ｘ
   * - band_min_pixel_size
     - Real
     - 밴드들 가운데 최소 픽셀 크기
     - Ｘ
   * - band_upper_left_x
     - Real
     - X 원점 (모든 밴드 사이에 동일한 경우에만 설정)
     - Ｘ
   * - band_upper_left_y
     - Real
     - Y 원점 (모든 밴드 사이에 동일한 경우에만 설정)
     - Ｘ
   * - band_crs
     - String
     - EPSG:XXXX 또는 WKT 서식의 좌표계 (모든 밴드 사이에 동일한 경우에만 설정)
     - Ｘ
   * - other_properties
     - String
     - 키가 독립적인 필드가 아닌 키/값 쌍을 가진 직렬화된 JSon 딕셔너리
     - Ｘ

"서버쪽 필터 호환성"이란 속성 필터에 이 필드를 포함시킬 경우 서버로 포워딩한다는 의미입니다. (아닐 경우 클라이언트쪽에서 필터링합니다.)

도형
~~~~~~~~

각 이미지의 촬영 범위(footprint)를 경도/위도 WGS84 좌표계(EPSG:4326)를 사용하는 멀티폴리곤으로 리포트합니다.

필터링
~~~~~~~~~

이 드라이버는 :cpp:func:`OGRLayer::SetSpatialFilter` 함수에 설정된 모든 공간 필터를 서버로 포워딩할 것입니다. :cpp:func:`OGRLayer::SetAttributeFilter` 함수에 설정된 속성 필터도 마찬가지입니다. 불(boolean) 연산자 3개(AND, OR, NOT) 및 비교 연산자들(=, <>, <, <=, > 및 >=)을 지원합니다.

페이지 작업(paging)
~~~~~~

기본적으로 서버로부터 객체들을 1,000개 덩어리로 가져옵니다. (이 값은 서버가 받아들일 수 있는 최대 개수입니다.) :decl_configoption:`EEDA_PAGE_SIZE` 환경설정 옵션으로 이 개수를 변경할 수 있습니다.

범위 및 객체 개수
~~~~~~~~~~~~~~~~~~~~~~~~

리포트되는 범위 및 객체 개수는 언제나 각각 (-180,-90,180,90) 및 -1일 것입니다. 서버로부터 이런 쿼리에 대한 효율적인 응답을 가져올 방법이 없기 때문입니다.

예시
~~~~~~~~

사용할 수 있는 모든 이미지를 목록화하기:

::

   ogrinfo -ro -al "EEDA:" -oo COLLECTION=projects/earthengine-public/assets/COPERNICUS/S2 --config EEDA_CLIENT_EMAIL "my@email" --config EEDA_PRIVATE_KEY_FILE my.pem

또는

::

   ogrinfo -ro -al "EEDA:projects/earthengine-public/assets/COPERNICUS/S2" --config EEDA_CLIENT_EMAIL "my@email" --config EEDA_PRIVATE_KEY_FILE my.pem

(위도,경도)=(40,-100) 포인트 아래 있는 모든 이미지를 목록화하기:

::

   ogrinfo -ro -al "EEDA:projects/earthengine-public/assets/COPERNICUS/S2" -spat -100 40 -100 40 --config EEDA_CLIENT_EMAIL "my@email" --config EEDA_PRIVATE_KEY_FILE my.pem

기준과 일치하는 모든 이미지를 목록화하기:

::

   ogrinfo -ro -al "EEDA:projects/earthengine-public/assets/COPERNICUS/S2" -where "startTime >= '2015/03/26 00:00:00' AND endTime <= '2015/06/30 00:00:00' AND CLOUDY_PIXEL_PERCENTAGE < 10" --config EEDA_CLIENT_EMAIL "my@email" --config EEDA_PRIVATE_KEY_FILE my.pem

참고
---------

-  :ref:`구글 어스 엔진 데이터 API 이미지 <raster.eedai>` 드라이버

