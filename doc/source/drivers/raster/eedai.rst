.. _raster.eedai:

================================================================================
EEDAI - 구글 어스 엔진 데이터 API 이미지
================================================================================

.. shortname:: EEDAI

.. versionadded:: 2.4

.. build_dependencies:: libcurl

이 드라이버는 구글 어스 엔진 REST API를 이용해서 이미지 내용에 접근하는 읽기전용 작업을 지원합니다.

드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

데이터셋 이름 문법
-------------------

데이터소스를 열기 위한 최소한의 문법은 다음과 같습니다:

::

   EEDAI:[asset][:band_names]

<asset>은 projects/earthengine-public/assets/COPERNICUS/S2/20170430T190351_20170430T190351_T10SEG 같은 주소이며, <band_names>는 쉼표로 구분된 밴드 이름 목록입니다. (일반적으로 주 이미지의 하위 데이터셋을 나타냅니다.)

열기 옵션
------------

다음과 같은 열기 옵션들을 사용할 수 있습니다:

-  **ASSET**\ =string: 연결 문자열에 <asset>을 지정하지 않은 경우 <asset>을 지정합니다.
-  **BANDS**\ =bandname1[,bandnameX]*: 쉼표로 구분된 밴드 이름 목록입니다.
-  **PIXEL_ENCODING**\ =AUTO/PNG/JPEG/AUTO_JPEG_PNG/GEO_TIFF/NPY: 픽셀을 요청할 포맷을 선택합니다.
-  **BLOCK_SIZE**\ =integer: GDAL 블록의 크기로, 픽셀을 쿼리할 수 있는 최소 단위입니다. 기본값은 256입니다.

인증 메소드
----------------------

다음 인증 메소드를 사용할 수 있습니다:

-  EEDA_BEARER 또는 EEDA_BEARER_FILE 환경설정 옵션을 통해 전송되는 인증 베어러(Authentication Bearer)
-  GOOGLE_APPLICATION_CREDENTIALS 환경설정 옵션을 통해 전송되는 서비스 계정 프라이빗 키 파일
-  EEDA_PRIVATE_KEY 또는 EEDA_PRIVATE_KEY_FILE 및 EEDA_CLIENT_EMAIL 환경설정 옵션을 통해 전송되는 OAuth2 서비스 계정 인증
-  마지막으로 앞의 세 메소드가 모두 실패한 경우 코드가 현재 가상 머신이 구글 컴퓨트 엔진인지 확인하고, 그렇다면 (가상 머신과 관련된 기본 서비스 계정을 이용해서) 구글 엔진 관련 권한을 사용할 것입니다. 강제로 가상 머신을 구글 컴퓨트 엔진 인스턴스로 (예를 들어 부트 로그에 접근할 수 없는 컨테이너에서 실행되는 코드처럼) 탐지되게 만들려면 CPL_MACHINE_IS_GCE를 YES로 설정하면 됩니다.

환경설정 옵션
---------------------

다음 환경설정 옵션들을 사용할 수 있습니다:

-  **EEDA_BEARER**\ =value: API에 전송할 인증 베어러 값입니다. 이 옵션은 외부 코드가 토큰을 계산한 경우에만 유용합니다. 베어러의 무결성은 일반적으로 베어러를 요청한 시간 이후 1시간까지입니다.
-  **EEDA_BEARER_FILE**\ =filename: 값을 직접 전송하는 대신 값을 읽어올 수 있는 파일명을 전송한다는 점을 제외하면, EEDA_BEARER 옵션과 비슷합니다.
-  **GOOGLE_APPLICATION_CREDENTIALS**\ =file.json: 프라이빗 키와 클라이언트 이메일을 담고 있는 서비스 계정 프라이빗 키 파일입니다.
-  **EEDA_PRIVATE_KEY**\ =string: PKCS#8 PEM 헤더와 푸터를 가진 PKCS#8 PEM 파일로 인코딩된 RSA 프라이빗 키입니다. OAuth2 서비스 계정 인증을 사용하려면 EEDA_CLIENT_EMAIL과 함께 사용해야 합니다. GDAL이 libcrypto++ 또는 libssl을 대상으로 빌드되어 있어야 합니다.
-  **EEDA_PRIVATE_KEY_FILE**\ =filename: 키를 직접 전송하는 대신 키를 읽어올 수 있는 파일명을 전송한다는 점을 제외하면, EEDA_PRIVATE_KEY 옵션과 비슷합니다.
-  **EEDA_CLIENT_EMAIL**\ =string: OAuth2 서비스 계정 인증을 사용하려면 EEDA_PRIVATE_KEY 또는 EEDA_PRIVATE_KEY_FILE과 함께 지정해야 하는 이메일입니다.

오버뷰
---------

이 드라이버는 감소하는 2의 거듭제곱 인자라는 논리에 따라 가장 작은 오버뷰의 두 크기 모두 256픽셀 미만이 될 때까지 오버뷰를 노출시킵니다.

하위 데이터셋
------------

모든 밴드가 동일한 지리참조, 해상도, 좌표계 또는 이미지 크기를 가지고 있지 않은 경우, 이 드라이버는 하위 데이터셋을 노출시킬 것입니다. 각 하위 데이터셋은 동일한 크기, 범위, 해상도 및 좌표계를 가진 밴드를 기준으로 그룹화합니다.

메타데이터
---------

이 드라이버는 "properties"에 리포트된 메타데이터를 데이터셋 수준 또는 밴드 수준 메타데이터로 노출시킬 것입니다.

픽셀 인코딩
--------------

이 드라이버는 기본적으로 (PIXEL_ENCODING=AUTO) 밴드의 개수 및 데이터 유형과 호환되는 포맷으로 픽셀을 요청합니다. 바이트 유형 밴드만 PNG, JPEG 및 AUTO_JPEG_PNG 포맷을 사용할 수 있습니다.

예시
~~~~~~~~

이미지에 있는 메타데이터를 가져오기:

::

   gdalinfo "EEDAI:" -oo ASSET=projects/earthengine-public/assets/COPERNICUS/S2/20170430T190351_20170430T190351_T10SEG --config EEDA_CLIENT_EMAIL "my@email" --config EEDA_PRIVATE_KEY_FILE my.pem

또는

::

   gdalinfo "EEDAI:projects/earthengine-public/assets/COPERNICUS/S2/20170430T190351_20170430T190351_T10SEG" --config EEDA_CLIENT_EMAIL "my@email" --config EEDA_PRIVATE_KEY_FILE my.pem

참고
--------

-  :ref:`구글 어스 엔진 데이터 API 드라이버 <vector.eeda>`
