.. _vector.mapml:

MapML
=====

.. versionadded:: 3.1

.. shortname:: MapML

.. built_in_by_default::

MapML 드라이버는 `MapML 사양 <https://maps4html.org/MapML/spec>`_ 에 대한 읽기 및 쓰기를 구현합니다. 벡터 객체의 읽기 및 쓰기만 구현합니다.

.. warning::

    이 드라이버는 실험적인 사양을 구현한 것으로, 그 실험적인 상태도 물려받았습니다. 이 사양은 향후 변경될 수도 있고, 또는 도입되지 않을 수도 있습니다. GDAL 향후 버전에서 이 드라이버가 작성한 파일을 더 이상 읽지 못 할 수도 있습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::

읽기 지원
------------

객체의 ``class`` 속성으로 레이어를 식별합니다.

객체의 ``properties`` 요소에 있는 HTML 테이블로부터 필드를 가져옵니다. 필드가 드라이버의 작성기 쪽과 완전히 동일한 구조로 작성되었다고 가정합니다. 그렇지 않은 경우 어떤 필드도 가져오지 않을 것입니다. 값으로부터 필드 유형을 추정하는데, 결과적으로 부정확한 경우가 있을 수도 있습니다.

쓰기 지원
-------------

동일한 MapML 파일에 레이어를 여러 개 작성할 수 있습니다.

다음 좌표계들만 네이티브로 지원합니다:

-  EPSG:4326 (WGS 84)
-  EPSG:3857 (WebMercator)
-  EPSG:3978 (NAD83 / Canada Atlas Lambert)
-  EPSG:5936 (WGS 84 / EPSG Alaska Polar Stereographic)

다른 좌표계를 사용하는 레이어는 EPSG:4326으로 자동 재투영될 것입니다.

포인트(Point), 라인스트링(LineString), 폴리곤(Polygon), 멀티포인트(MultiPoint), 멀티라인스트링(MultiLineString), 멀티폴리곤(MultiPolygon) 및 도형 집합(GeometryCollection) 도형 유형을 지원합니다.

속성은 HTML 테이블로 작성합니다.

데이터셋 생성 옵션
------------------------

-  **HEAD=string**: <head> 요소 용 파일명 또는 그때 그때 즉시 처리하는 XML 콘텐츠를 지정합니다.
-  **EXTENT_UNITS=AUTO/WGS84/OSMTILE/CBMTILE/APSTILE**: 대체할 좌표계를 지정합니다.
-  **EXTENT_ACTION=string**: ``extent@action`` 속성의 값을 지정합니다.
-  **EXTENT_XMIN=float**: 대체할 범위 최소 X좌표 값을 지정합니다.
-  **EXTENT_YMIN=float**: 대체할 범위 최소 Y좌표 값을 지정합니다.
-  **EXTENT_XMAX=float**: 대체할 범위 최대 X좌표 값을 지정합니다.
-  **EXTENT_YMAX=float**: 대체할 범위 최대 Y좌표 값을 지정합니다.
-  **EXTENT_XMIN_MIN=float**: extent.xmin 값의 최소값을 지정합니다.
-  **EXTENT_XMIN_MAX=float**: extent.xmin 값의 최대값을 지정합니다.
-  **EXTENT_YMIN_MIN=float**: extent.ymin 값의 최소값을 지정합니다.
-  **EXTENT_YMIN_MAX=float**: extent.ymin 값의 최대값을 지정합니다.
-  **EXTENT_XMAX_MIN=float**: extent.xmax 값의 최소값을 지정합니다.
-  **EXTENT_XMAX_MAX=float**: extent.xmax 값의 최대값을 지정합니다.
-  **EXTENT_YMAX_MIN=float**: extent.ymax 값의 최소값을 지정합니다.
-  **EXTENT_YMAX_MAX=float**: extent.ymax 값의 최대값을 지정합니다.
-  **EXTENT_ZOOM=int**: extent.zoom 값을 지정합니다.
-  **EXTENT_ZOOM_MIN=int**: extent.zoom 값의 최소값을 지정합니다.
-  **EXTENT_ZOOM_MAX=int**: extent.zoom 값의 최대값을 지정합니다.
-  **EXTENT_EXTRA=string**: <extent> 요소에 삽입할 추가 콘텐츠를 위한 그때 그때 즉시 처리하는 XML 콘텐츠의 파일명을 지정합니다.
-  **BODY_LINKS=string**: <body>에 <link> 요소로 삽입할 추가 콘텐츠를 위한 그때 그때 즉시 처리하는 XML 콘텐츠를, 예를 들면 '<link type="foo" href="bar" /><link type="baz" href="baw" />' 와 같은 문자열로 지정합니다.

링크
-----

-  `MapML 사양 <https://maps4html.org/MapML/spec>`_
-  `MapML 스키마 <https://github.com/Maps4HTML/MapML/tree/gh-pages/schema>`_
-  :ref:`gdal2tiles` mapml 산출물

