.. _vector.geojsonseq:

GeoJSONSeq: GeoJSON 객체 시퀀스
========================================

.. versionadded:: 2.4

.. shortname:: GeoJSONSeq

.. built_in_by_default::

GeoJSONSeq 드라이버는 `GeoJSON <http://geojson.org/>`_ Feature 객체로 개별 인코딩된, 새줄 문자(LF) -- `새줄 문자 구분 JSON <http://ndjson.org/>`_ -- 또는 레코드 구분자(record-separator; RS) 문자 -- `RFC 8142 <https://tools.ietf.org/html/rfc8142>`_ 표준: GeoJSON 텍스트 시퀀스 -- 로 구분된 객체들의 읽기 및 생성 지원을 구현합니다.

이런 파일들은 GeoJSON FeatureCollection과 동등하지만, 증분 파싱을 더 쉽게 할 수 있습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::

데이터소스
----------

이 드라이버는 세 가지 유형의 데이터소스를 입력받습니다:

-  URL(`Uniform Resource Locator <http://en.wikipedia.org/wiki/URL>`_)

   *  `HTTP <http://en.wikipedia.org/wiki/HTTP>`_ 요청을 수행하기 위한 웹 주소입니다.

-  .geojsonl 또는 .geojsons 파일 확장자로 식별되는, GeoJSON 데이터를 가진 평문 텍스트 파일

-  직접 전송되는, GeoJSON 시퀀스로 인코딩된 텍스트

다른 드라이버들과의 혼동을 피하기 위해 'URL', 'filename', 'text' 앞에 'GeoJSONSeq:' 접두어를 붙여야 할 수도 있습니다.

레이어 생성 옵션
----------------------

-  **RS=YES/NO**:
   `RFC 8142 <https://tools.ietf.org/html/rfc8142>`_ 표준과의 호환성을 위해 레코드를 RS=0x1E 문자로 시작할지 여부를 선택합니다. 파일 확장자가 ".geojsons"가 아닌 이상 기본값은 NO입니다.

-  **COORDINATE_PRECISION=int_number**:
   좌표값의 소수점 뒤에 작성할 최대 자릿수를 설정합니다. 기본값은 7입니다. 후행 0들을 제거하기 위해 "스마트" 절단(truncation)을 수행할 것입니다.

-  **SIGNIFICANT_FIGURES=int_number**:
   부동소수점형 숫자를 작성할 때 산출할 유효 숫자(significant digit) 자릿수를 지정합니다. 기본값은 17입니다. 이 옵션을 명확하게 지정하고 COORDINATE_PRECISION 옵션은 지정하지 않은 경우, 좌표에도 이 옵션을 적용할 것입니다.

-  **ID_FIELD=string**:
   Feature 객체의 'id' 멤버로 작성해야만 하는 소스 필드의 이름을 설정합니다.

-  **ID_TYPE=AUTO/String/Integer**:
   Feature 객체의 'id' 멤버의 유형을 설정합니다.

참고
--------

-  :ref:`GeoJSON <vector.geojson>` 드라이버

-  `RFC 7946 <https://tools.ietf.org/html/rfc7946>`_ 표준: GeoJSON 포맷

-  `RFC 8142 <https://tools.ietf.org/html/rfc8142>`_ 표준: GeoJSON 텍스트 시퀀스 (RS 구분자)

-  `새줄 문자 구분 JSON <http://ndjson.org/>`_

-  `GeoJSONL <https://www.interline.io/blog/geojsonl-extracts/>`_: 대용량 지리 데이터셋을 위한 최적화 포맷

