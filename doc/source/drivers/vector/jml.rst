.. _vector.jml:

JML: OpenJUMP JML 포맷
========================

.. shortname:: JML

.. build_dependencies:: (읽기 지원에 libexpat 필요) 

OGR는 OpenJUMP 소프트웨어가 사용하는 .JML 파일의 읽기 및 쓰기를 지원합니다. GDAL이 *Expat* 라이브러리 지원과 함께 빌드된 경우에만 읽기를 지원합니다.

JML 포맷은 GML 포맷의 변이형입니다. 이 포맷의 공식적인 정의는 없습니다. JML 포맷은 파일 하나 당 단일 레이어 하나, 혼합 도형 유형, 그리고 각 객체(feature) 당 도형 하나와 정수형, 더블형, 문자열, 날짜 또는 객체(object) 유형의 속성 여러 개를 지원합니다. 예를 들면 64비트 정수형을 저장하는 데 쓰이지만 임의의 직렬화 자바(Java) 객체일 수도 있는 이 객체(object) 데이터 유형을 읽어오는 경우 문자열로 변환합니다. GML과는 달리, 필드 정의가 .jml 파일 시작 부분에 내장되어 있습니다.

GDAL 2.3 이상 버전에서 공간 좌표계의 읽기 및 쓰기를 지원합니다.

드라이버 케이퍼빌리티
-------------------

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::

인코딩 문제점
---------------

Expat 라이브러리는 다음 내장 인코딩 읽기를 지원합니다:

-  US-ASCII
-  UTF-8
-  UTF-16
-  ISO-8859-1
-  Windows-1252

OGR가 반환하는 콘텐츠는 파일 헤더에 언급된 인코딩으로 변환한 다음 UTF-8로 인코딩될 것입니다. 그러나 OpenJUMP가 생성한 파일은 항상 UTF-8로 인코딩됩니다.

JML 파일 작성 시, 이 드라이버는 UTF-8 콘텐츠가 전송되어 올 것으로 예상합니다.

스타일 작업
-------

OpenJUMP 소프트웨어는 "R_G_B"라는 선택적인 문자열 속성을 이용해서 객체의 색상을 판단합니다. 이 속성 필드의 값은 "RRGGBB" 형식으로, RR, GG, BB가 각각 00에서 FF까지의 16진법 값으로 표현된 적색, 녹색, 청색 구성요소의 값입니다. .jml 파일을 읽어올 때, OGR는 OGR_STYLE 속성이 존재하지 않는 한 R_G_B 속성을 OGR 피처 스타일(Feature Style) 인코딩으로 변환할 것입니다. .jml 파일을 작성하는 경우, OGR는 지정된 객체에 R_G_B 속성이 정의되어 있지 않은 이상 R_G_B 속성을 작성하기 위해 피처 스타일 문자열로부터 PEN 도구의 색상 또는 BRUSH 도구의 전경색(forecolor)을 추출할 것입니다. CREATE_R_G_B_FIELD 레이어 생성 옵션을 NO로 설정하면 R_G_B 속성을 추가하지 않습니다.

생성 문제점
---------------

JML 작성기는 다음 *레이어* 생성 옵션을 지원합니다:

-  **CREATE_R_G_B_FIELD=YES/NO**:
   OGR 피처 스타일 문자열의 PEN 도구의 색상 또는 BRUSH 도구의 전경색을 담을 R_G_B 필드를 생성할지 여부를 선택합니다. 기본값은 YES입니다.

-  **CREATE_OGR_STYLE_FIELD=YES/NO**:
   피처 스타일 문자열을 담을 OGR_STYLE 필드를 생성할지 여부를 선택합니다. 기본값은 NO입니다.

참고
--------

- :ref:`ogr_feature_style`

감사의 말
-------

이 드라이버는 유카 라흐코넨(Jukka Rahkonen)의 재정 지원으로 개발되었습니다.

