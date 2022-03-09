.. _raster.daas:

================================================================================
DAAS (공공 서비스로서의 에어버스 DS 정보 데이터 드라이버)
================================================================================

.. shortname:: DAAS

.. versionadded:: 3.0

.. build_dependencies:: libcurl

이 드라이버는 공공 서비스로서의 에어버스 DS 정보 데이터 API에 연결할 수 있습니다. DAAS 드라이버를 컴파일하려면 GDAL/OGR을 cURL 지원과 함께 빌드해야만 합니다.

(지리변형을 가진) 정사보정 및 (RPC를 가진) 원본(raw) 이미지를 지원합니다.

오버뷰도 지원합니다.

이 API는 공개되어 있지 않지만 곧 배포될 것입니다. 더 자세한 내용은 다음에서 찾아보십시오: https://api.oneatlas.airbus.com/

드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

데이터셋 이름 문법
-------------------

데이터베이스를 열기 위한 명목상의 문법은 다음과 같습니다:

::

   DAAS:https://example.com/path/to/image/metadata

더 미니멀한 문법도 사용할 수 있습니다:

::

   DAAS:

이때 GET_METADATA_URL 열기 옵션을 설정했다고 가정합니다.

인증
--------------

API에 접근하기 위해서는 인증 토큰이 필수입니다. 다음 두 메소드를 지원합니다:

-  API 키와 클라이언트 ID로 인증합니다. 각각 API_KEY 열기 옵션(또는 :decl_configoption:`GDAL_DAAS_API_KEY` 환경설정 옵션)과 CLIENT_ID 열기 옵션(또는 :decl_configoption:`GDAL_DAAS_CLIENT_ID` 환경설정 옵션)으로 지정해야만 합니다. 이런 경우, 접근 토큰을 얻기 위해 드라이버가 인증 종단점을 대상으로 인증할 것입니다.
-  ACCESS_TOKEN 열기 옵션(또는 :decl_configoption:`GDAL_DAAS_ACCESS_TOKEN` 환경설정 옵션)으로 접근 토큰을 직접 제공합니다.

두 경우 모두, X_FORWARDED_USER 열기 옵션(또는 :decl_configoption:`GDAL_DAAS_X_FORWARDED_USER` 환경설정 옵션)을 지정해서, 요청을 발송한 사용자 정보로 DAAS 서비스 종단점으로 전송되는 요청에 있는 HTTP X-Forwarded-User 헤더를 채울 수 있습니다.

더 자세한 내용은 https://api.oneatlas.airbus.com/guides/g-authentication/ 를 살펴보십시오.

열기 옵션
------------

다음과 같은 열기 옵션들을 사용할 수 있습니다:

-  **GET_METADATA_URL**\ =value: GetImageMetadata 종단점을 가리키는 URL입니다. 연결 문자열에 지정되지 않은 경우 필수적입니다.
-  **API_KEY**\ =value: 인증 용 API 키입니다. 지정하는 경우, CLIENT_ID 옵션과 함께 사용해야만 합니다. GDAL_DAAS_API_KEY 환경설정 옵션으로도 지정할 수 있습니다.
-  **CLIENT_ID**\ =value: 인증 용 클라이언트 ID입니다. 지정하는 경우, API_KEY 옵션과 함께 사용해야만 합니다. GDAL_DAAS_CLIENT_ID 환경설정 옵션으로도 지정할 수 있습니다.
-  **ACCESS_TOKEN**\ =value: 접근 토큰입니다. GDAL_DAAS_ACCESS_TOKEN 환경설정 옵션으로도 지정할 수 있습니다. API_KEY/CLIENT_ID와 함께 사용할 수 없습니다.
-  **X_FORWARDED_USER**\ =value: 요청을 발송한 사용자입니다. GDAL_DAAS_X_FORWARDED_USER 환경설정 옵션으로도 지정할 수 있습니다.
-  **BLOCK_SIZE**\ =value: 서버에 요청하는 블록의 픽셀 단위 크기입니다. 기본값은 512픽셀입니다. 64에서 8192까지 지정할 수 있습니다.
-  **PIXEL_ENCODING**\ =value: 이 포맷으로 픽셀을 요청합니다. 기본값은

   -  **AUTO**: 바이트 유형의 밴드 1개, 3개 또는 4개 밴드 이미지인 경우, PNG로 지정합니다. 그렇지 않다면 원본(raw)으로 지정합니다.
   -  **RAW**: 모든 이미지 유형과 호환됩니다. 픽셀을 비압축 원본(raw) 포맷으로 요청합니다.
   -  **PNG**: 바이트 유형의 밴드 1개, 3개 또는 4개 밴드 이미지와 호환됩니다.
   -  **JPEG**: 바이트 유형의 밴드 1개 또는 3개 밴드 이미지와 호환됩니다.
   -  **JPEG2000**: 모든 이미지 유형과 호환됩니다. GDAL을 반드시 GDAL이 지원하는 JPEG2000 호환 드라이버 가운데 하나와 함께 빌드해야 합니다.

-  **MASKS**\ =YES/NO: 마스크 밴드를 노출시킬지 여부를 선택합니다. 기본값은 YES입니다.
