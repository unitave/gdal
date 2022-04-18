.. _vector.oapif:

OGC API - 피처
==================

.. versionadded:: 2.3

.. shortname:: OAPIF

.. build_dependencies:: libcurl

OAPIF 드라이버는 OGC API - 피처(OGC API - Features) 서비스에 접속할 수 있습니다. 이 드라이버는 서비스가 각각 API 설명, 객체 집합(feature collection) 메타데이터 그리고 객체 집합 데이터를 위한 OpenAPI 3.0, JSON 그리고 GeoJSON 인코딩을 지원한다고 가정합니다.

.. note::

    GDAL 3.1 이전 버전들에서는 이 드라이버를 WFS3 드라이버라고 했으며 서비스 사양의 초안 버전들만 지원했습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

데이터셋 이름 문법
-------------------

OGC API - 피처 데이터소스를 열기 위한 문법은 다음과 같습니다:

::

   OAPIF:http://path/to/OAPIF/endpoint

이때 'endpoint'는 랜딩 페이지 또는 'collections/{id}'를 가리키는 경로입니다.

레이어 스키마
------------

OGR는 레이어별 고정 스키마를 필요로 하지만 OGC API - 피처 코어는 고정 스키마를 요구하지 않습니다. 따라서 이 드라이버는 객체들의 첫 페이지를 (객체 10개를) 가져와서 스키마를 확립할 것입니다.

필터링
---------

이 드라이버는 :cpp:func:`OGRLayer::SetSpatialFilter` 함수에 설정된 모든 공간 필터를 서버로 포워딩할 것입니다. OGC API - 피처 코어에서는 서버가 허용하는 속성 부분 집합만 잠재적인 AND 논리 연산자와 함께 쿼리할 수 있습니다. 더 복잡한 요청은 부분적으로 또는 완전히 클라이언트 쪽에서 평가될 것입니다.

직사각형 공간 필터도 서버로 포워딩합니다.

열기 옵션
------------

다음과 같은 열기 옵션들을 사용할 수 있습니다:

-  **URL=url**:
   OGC API - 피처 서버 랜딩 페이지 또는 지정한 집합을 가리키는 URL입니다. "OAPIF:" 문자열을 연결 문자열로 사용하는 경우 필수입니다.

-  **PAGE_SIZE=integer**:
   요청 당 가져올 객체의 개수입니다. 기본값은 10입니다. 최소 1개에서 최대 10,000개까지 지정할 수 있습니다.

-  **USERPWD**:
   원격 서버에 사용자 ID와 비밀번호를 전송하기 위해 *userid:password* 를 지정할 수도 있습니다.

-  **IGNORE_SCHEMA=YES/NO**: (GDAL 3.1 이상 버전)
   서버가 제공할 수도 있는 XML 스키마 또는 JSon 스키마를 무시하려면 YES로 설정하십시오.

예시
--------

-  OGC API - 피처 서버의 유형들을 목록화하기:

   ::

      $ ogrinfo OAPIF:https://www.ldproxy.nrw.de/rest/services/kataster

      INFO: Open of `OAPIF:https://www.ldproxy.nrw.de/rest/services/kataster'
            using driver `OAPIF' successful.
      1: flurstueck (Multi Polygon)
      2: gebaeudebauwerk (Multi Polygon)
      3: verwaltungseinheit (Multi Polygon)

-  OGC API - 피처 레이어의 요약 정보를 목록화하기:

   ::

      $ ogrinfo -al -so OAPIF:https://www.ldproxy.nrw.de/rest/services/kataster flurstueck

      Layer name: flurstueck
      Metadata:
        TITLE=Flurstück
      Geometry: Multi Polygon
      Feature Count: 9308456
      Extent: (5.612726, 50.237351) - (9.589634, 52.528630)
      Layer SRS WKT:
      GEOGCS["WGS 84",
          DATUM["WGS_1984",
              SPHEROID["WGS 84",6378137,298.257223563,
                  AUTHORITY["EPSG","7030"]],
              AUTHORITY["EPSG","6326"]],
          PRIMEM["Greenwich",0,
              AUTHORITY["EPSG","8901"]],
          UNIT["degree",0.0174532925199433,
              AUTHORITY["EPSG","9122"]],
          AUTHORITY["EPSG","4326"]]
      id: String (0.0)
      aktualit: Date (0.0)
      flaeche: Real (0.0)
      flstkennz: String (0.0)
      land: String (0.0)
      gemarkung: String (0.0)
      flur: String (0.0)
      flurstnr: String (0.0)
      gmdschl: String (0.0)
      regbezirk: String (0.0)
      kreis: String (0.0)
      gemeinde: String (0.0)
      lagebeztxt: String (0.0)
      tntxt: String (0.0)

-  속성에 대해 필터링하기(서버가 필터링 기능을 지원하느냐에 따라 달라질 수 있습니다. 필터는 부분적으로 또는 완전히 클라이언트 쪽에서 평가될 것입니다.):

   ::


      $ ogrinfo OAPIF:https://www.ldproxy.nrw.de/rest/services/kataster flurstueck -al -q -where "flur = '028'"
      Layer name: flurstueck
      Metadata:
        TITLE=Flurstück
      OGRFeature(flurstueck):1
        id (String) = DENW19AL0000geMFFL
        aktualit (Date) = 2017/04/26
        flaeche (Real) = 1739
        flstkennz (String) = 05297001600193______
        land (String) = Nordrhein-Westfalen
        gemarkung (String) = Wünnenberg
        flur (String) = 016
        flurstnr (String) = 193
        gmdschl (String) = 05774040
        regbezirk (String) = Detmold
        kreis (String) = Paderborn
        gemeinde (String) = Bad Wünnenberg
        lagebeztxt (String) = Bleiwäscher Straße
        tntxt (String) = Platz / Parkplatz;1739
        MULTIPOLYGON (((8.71191 51.491084,8.7123 51.491067,8.712385 51.491645,8.712014 51.491666,8.711993 51.491603,8.71196 51.491396,8.711953 51.491352,8.71191 51.491084)))

      [...]

-  공간에 대해 필터링하기

   ::

      $ ogrinfo OAPIF:https://www.ldproxy.nrw.de/rest/services/kataster flurstueck -al -q -spat 8.7 51.4 8.8 51.5

      Layer name: flurstueck
      Metadata:
        TITLE=Flurstück
      OGRFeature(flurstueck):1
        id (String) = DENW19AL0000ht7LFL
        aktualit (Date) = 2013/02/19
        flaeche (Real) = 18
        flstkennz (String) = 05292602900206______
        land (String) = Nordrhein-Westfalen
        gemarkung (String) = Fürstenberg
        flur (String) = 029
        flurstnr (String) = 206
        gmdschl (String) = 05774040
        regbezirk (String) = Detmold
        kreis (String) = Paderborn
        gemeinde (String) = Bad Wünnenberg
        lagebeztxt (String) = Karpke
        tntxt (String) = Fließgewässer / Bach;18
        MULTIPOLYGON (((8.768521 51.494915,8.768535 51.494882,8.768569 51.494908,8.768563 51.494925,8.768521 51.494915)))
      [...]

참고
--------

-  `"OGC API - 피처 - 1부: 코어" 표준 <http://docs.opengeospatial.org/is/17-069r3/17-069r3.html>`_

-  :ref:`WFS (1.0, 1.1, 2.0) <vector.wfs>` 드라이버

