.. _vector.sdts:

SDTS
====

.. shortname:: SDTS

.. built_in_by_default::

SDTS(Spatial Data Transfer Standard) 드라이버는 SDTS TVP(Topological Vector Profile) 및 포인트 프로파일(Point Profile) 데이터셋에 읽기 접근을 지원합니다. 주요 속성, 노드(포인트), 라인 및 폴리곤 모듈을 각각 개별 레이어로 취급합니다.

SDTS 변환(transfer)을 선택하려면, 예를 들어 ``TR01CATD.DDF`` 같은 카탈로그 파일 이름을 사용해야 합니다. 이때 처음 4개의 문자는 계속 달라집니다.

SDTS에 정의된 대부분의 좌표계의 경우 SDTS 좌표계 정보를 제대로 지원합니다.

SDTS 드라이버는 업데이트 또는 생성을 지원하지 않습니다.

TVP 데이터셋에서 라인 모듈에 있는 도형으로부터 폴리곤 도형을 형성한다는 사실을 기억하십시오. 주요 속성 모듈의 속성이 관련 노드, 라인, 또는 폴리곤 객체에 알맞게 추가되어야 하지만, 각 유형의 레이어로 개별적으로 접근할 수도 있습니다.

이 드라이버는 래스터(DEM) SDTS 데이터셋을 지원하지 않습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

.. supports_virtualio::

참고
--------

-  `SDTS 추상 라이브러리 <https://web.archive.org/web/20130730111701/http://home.gdal.org/projects/sdts/index.html>`_:
   이 드라이버를 구현하기 위해 사용된 기반 라이브러리입니다.
-  `http://mcmcweb.er.usgs.gov/sdts <http://mcmcweb.er.usgs.gov/sdts/>`_:
   USGS SDTS 웹페이지입니다.

