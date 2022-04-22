.. _vector.topojson:

TopoJSON 드라이버
=================

.. shortname:: TopoJSON

.. built_in_by_default::

.. note::

   GDAL 2.3 이전 버전들에서, 이 드라이버의 기능을 GeoJSON 드라이버에서도 사용할 수 있었습니다. 현재 이 둘은 개별 드라이버입니다.

이 드라이버는 `TopoJSON 포맷 <https://github.com/topojson/topojson-specification/blob/master/README.md>`_ 을 읽을 수 있습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

.. supports_virtualio::

데이터소스
----------

TopoJSON 드라이버는 세 가지 유형의 데이터소스를 입력받습니다:

-  `URL(Uniform Resource Locator) <https://ko.wikipedia.org/wiki/URL>`_:
   `HTTP <https://ko.wikipedia.org/wiki/HTTP>`_ 요청을 수행하기 위한 웹 주소입니다.

-  TopoJSON 데이터를 가진 평문 텍스트 파일:
   .json 또는 .topojson 파일 확장자로 식별되는 파일입니다.

-  TopoJSON으로 인코딩되어 직접 전송되는 텍스트

GDAL 2.3버전부터, 다른 드라이버와의 혼동을 피하기 위해 URL, 파일명, 텍스트 앞에 "TopoJSON:" 접두어가 붙을 수도 있습니다.

참고
--------

-  :ref:`GeoJSON <vector.geojson>` 드라이버
-  `TopoJSON 포맷 사양 <https://github.com/topojson/topojson-specification/blob/master/README.md>`_

