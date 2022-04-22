.. _vector.svg:

SVG - 가변 벡터 그래픽
==============================

.. shortname:: SVG

.. build_dependencies:: libexpat

OGR는 (GDAL이 *Expat* 라이브러리 지원과 함께 빌드된 경우) SVG(Scalable Vector Graphics) 포맷의 읽기를 지원합니다.

현재 OGR SVG 드라이버는 클라우드메이드 벡터 스트림 서버(Cloudmade Vector Stream Server)가 생성한 SVG 파일만 읽어올 것입니다.

모든 좌표는 의사 메르카토르 공간 좌표계(EPSG:3857)에 상대적인 좌표입니다.

이 드라이버는 다음 3개의 레이어를 반환할 것입니다:

-  'points'
-  'lines'
-  'polygons'

드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

.. supports_virtualio::

참고
--------

-  `W3C SVG 페이지 <http://www.w3.org/TR/SVG/>`_
-  `클라우드메이드 벡터 문서 <http://developers.cloudmade.com/wiki/vector-stream-server/Documentation>`_

