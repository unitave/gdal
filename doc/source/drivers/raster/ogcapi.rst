.. _raster.ogcapi:

================================================================================
OGCAPI -- OGC API 타일/맵/커버리지
================================================================================

.. versionadded:: 3.2

.. shortname:: OGCAPI

.. build_dependencies:: libcurl

서버가 구현하는 OGC API 타일, OGC API 맵, OGC API 커버리지에 접근합니다. 이 드라이버는 래스터와 벡터를 지원합니다.

.. warning::

    이 드라이버는 실험적인 드라이버로, "모듈식 OGC API 워크플로(Modular OGC API Workflows)" 계획 관련 작업을 시연하기 위해 개발되었습니다.
    이 드라이버는 완결되지 않은 버전의 OGC API 타일, 맵, 그리고 커버리지를 구현합니다.
    이 드라이버의 인터페이스는 언제라도 바뀔 수 있고, 또는 제거될 수도 있습니다.
    또 언젠가는 OGC API 객체(OGC API -2 Features) 드라이버와 병합될 수도 있습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

데이터셋 열기
---------------

이 드라이버는 다음 방법을 사용하는 열기를 지원합니다:

-  다음 예시와 같은 지연 처리(deferred processing)를 지정하는 JSON 문서를 담고 있는 파일(.moaw)의 이름을 전송합니다.

  .. code-block:: json
 
   {
       "process" : "https://maps.ecere.com/ogcapi/processes/RenderMap",
       "inputs" : {
           "transparent" : false,
           "background" : "navy",
           "layers" : [
                { "collection" : "https://maps.ecere.com/ogcapi/collections/NaturalEarth:physical:bathymetry" },
                { "collection" : "https://maps.ecere.com/ogcapi/collections/SRTM_ViewFinderPanorama" }
            ]
        }
    }

-  {url}이 OGC API로 연결되는 페이지를 가리키는 URL인 "OGCAPI:{url}" 문자열을 전송합니다.
   이 경우 드라이버가 서로 다른 선택 집합을 가진 하위 데이터셋을 반환할 것입니다.

-  {url}이 OGC API 선택 집합 설명을 가리키는 URL인 "OGCAPI:{url}" 문자열을 전송합니다.


이 드라이버가 래스터 선택 집합을 여는 경우, 타일 또는 맵 API가 자신을 노출시키는지 검색할 것입니다. 이 드라이버는 기본적으로 타일 API를 사용하며, 타일이 없을 경우 맵 API를 사용합니다. 드라이버가 이미지 포맷도 식별하는데, 사용할 수 있는 경우 PNG를 우선할 것입니다.

벡터 선택 집합을 여는 경우, 이 드라이버가 GeoJSON 또는 맵박스 벡터 타일로 타일 API를 처리합니다.

타일 API 사용 시, 드라이버가 기본적으로 -- 사용할 수 있는 경우 -- WorldCRS84Quad 타일 행렬 집합을 이용할 것입니다.

열기 옵션
------------

다음과 같은 열기 옵션들을 사용할 수 있습니다:

-  **API=AUTO/MAPS/TILES/COVERAGE/ITEMS**:
   데이터 수집을 위해 사용할 API를 설정합니다. 기본값은 AUTO입니다.
   래스터에 접근하는 경우 AUTO 모드를 사용하면 사용할 수 있는 경우 커버리지 API를 사용하고, 사용할 수 없다면 먼저 타일 API를, 그 다음 마지막으로 맵 API를 사용합니다.

-  **IMAGE_FORMAT=AUTO/PNG/PNG_PREFERRED/JPEG/JPEG_PREFERRED**:
   타일 또는 맵 API를 사용하는 경우 픽셀 수집을 위해 사용할 포맷을 설정합니다.
   기본값은 AUTO입니다. 사용할 수 있는 경우 PNG를 사용하고, 그렇지 않다면 JPEG을 사용할 것이라는 의미입니다.
   PNG 또는 JPEG을 지정하는 경우, 지정한 포맷을 사용할 수 있어야만 합니다. 사용할 수 없다면 드라이버가 오류를 반환할 것입니다. PNG_PREFERRED 또는 JPEG_PREFERRED 가운데 하나를 지정하면, 사용할 수 있는 경우 지정한 포맷을 사용하고 그렇지 않다면 다른 포맷을 사용할 것입니다.

-  **VECTOR_FORMAT=AUTO/GEOJSON/GEOJSON_PREFERRED/MVT/MVT_PREFERRED**:
   벡터 데이터 수집을 위해 사용할 포맷을 설정합니다.
   기본값은 AUTO입니다. 사용할 수 있는 경우 MVT(Mapbox Vector Tiles)를 사용하고, 그렇지 않다면 GEOJSON을 사용할 것이라는 의미입니다. MVT 또는 GEOJSON을 지정하는 경우, 지정한 포맷을 사용할 수 있어야만 합니다. 사용할 수 없다면 드라이버가 오류를 반환할 것입니다. MVT_PREFERRED 또는 GEOJSON_PREFERRED 가운데 하나를 지정하면, 사용할 수 있는 경우 지정한 포맷을 사용하고 그렇지 않다면 다른 포맷을 사용할 것입니다.

-  **TILEMATRIXSET=id**:
   요청한 타일 행렬 집합의 식별자입니다. 타일 API를 사용하는 경우에만 설정합니다.
   이 타일 행렬 집합을 사용할 수 없는 경우 드라이버가 실패할 것입니다.
   이 옵션을 지정하지 않으면 드라이버가 사용할 수 있는 타일 행렬 집합들 가운데 하나를 자동 선택할 것입니다.
   TILEMATRIXSET과 PREFERRED_TILEMATRIXSET 옵션은 함께 사용할 수 없습니다.

-  **PREFERRED_TILEMATRIXSET=id**:
   선호하는 타일 행렬 집합의 식별자입니다. 타일 API를 사용하는 경우에만 설정합니다.
   이 타일 행렬 집합을 사용할 수 없는 경우 또는 이 옵션을 지정하지 않는 경우, 드라이버가 사용할 수 있는 타일 행렬 집합들 가운데 하나를 자동 선택할 것입니다.
   TILEMATRIXSET과 PREFERRED_TILEMATRIXSET 옵션은 함께 사용할 수 없습니다.

-  **TILEMATRIX=id**:
   선택한 타일 행렬 집합의 특정 타일 행렬(확대/축소 수준)의 식별자입니다.
   이 옵션을 지정하지 않으면, 사용할 수 있는 모든 타일 행렬을 (래스터 데이터의 경우) 오버뷰 또는 (벡터 데이터의 경우) 레이어로 반환합니다.
  
-  **CACHE=YES/NO**:
   블록/타일 캐시 작업을 활성화할지 여부를 선택합니다.
   타일 API를 래스터 데이터와 사용하는 경우에만 설정합니다. 기본값은 YES입니다.
  
-  **MAX_CONNECTIONS=number**:
   병렬 타일 다운로드를 위한 연결의 최대 개수입니다.
   타일 API를 래스터 데이터와 사용하는 경우에만 설정합니다. 기본값은 5입니다.
  
-  **MINX/MINY/MAXX/MAXY=number**:
   TileMatrixSet의 데이터셋/레이어를 노출시킬 영역을 제한하기 위한 공간 좌표계 단위 경계입니다.
