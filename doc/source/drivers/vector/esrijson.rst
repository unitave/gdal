.. _vector.esrijson:

ESRIJSON / 피처 서비스 드라이버
================================

.. shortname:: ESRIJSON

.. built_in_by_default::

.. note::

   GDAL 2.3 이전 버전에서는 GeoJSON 드라이버에서 이 드라이버의 기능을 사용할 수 있습니다. 현재 이 두 드라이버는 확연하게 구분됩니다.

ESRIJSON 드라이버는 -- `ArcGIS 서버 REST API <http://help.arcgis.com/en/arcgisserver/10.0/apis/rest/index.html>`_ 가 구현한 것처럼 -- `GeoServices REST 사양 <http://www.esri.com/industries/landing-pages/geoservices/geoservices.html>`_ 에 따라 피처 서비스(Feature Service) 요청의 JSON 산출물을 읽을 수 있습니다.
이 드라이버는 (ArcGIS 서버 10.3 이상 버전에서) 여러 페이지에 걸쳐 있는 이런 결과물 집합을 스크롤할 수 있습니다. URL에 *resultOffset* 파라미터가 명확하게 설정되지 않은 경우 이 기능을 자동적으로 활성화시킵니다. 해당 파라미터가 설정되어 있지만 그래도 스크롤하고 싶다면 FEATURE_SERVER_PAGING 열기 옵션을 YES로 설정해야만 합니다.
*resultRecordCount* 파라미터로 (서버 제한에 종속적이기는 하지만) 페이지 크기를 명확하게 설정할 수 있습니다. 이 파라미터를 설정하지 않는 경우, OGR가 서버가 허용하는 최고값으로 설정할 것입니다.

주의: 페이지 구조의 요청이 제대로 작동하려면, 일반적으로 필드에 정렬 구문을 추가해야 합니다. 보통 URL에 "&orderByFields=OBJECTID+ASC" 파라미터로 OBJECTID를 삽입하면 서버가 신뢰할 수 있는 방식으로 결과물을 반환합니다.

드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

.. supports_virtualio::

데이터 소스
----------

이 드라이버는 세 가지 유형의 데이터소스를 입력받습니다:

-  URL(`Uniform Resource Locator <http://en.wikipedia.org/wiki/URL>`_)

   *  `HTTP <http://en.wikipedia.org/wiki/HTTP>`_ 요청을 수행하기 위한 웹 주소입니다.

-  .json 파일 확장자로 식별되는, ESRIJSON 데이터를 가진 평문 텍스트 파일

-  직접 전송되는, ESRI JSON으로 인코딩된 텍스트

GDAL 2.3버전부터, 다른 드라이버들과의 혼동을 피하기 위해 'URL', 'filename', 'text' 앞에 'ESRIJSON:' 접두어를 붙여야 할 수도 있습니다.

열기 옵션
------------

-  **FEATURE_SERVER_PAGING=YES/NO**:
   ArcGIS 피처 서비스 종단점을 가진 결과물을 자동 스크롤할지 여부를 선택합니다. ArcGIS 서버 10.3 이상 버전 그리고 supportsPagination=true 케이퍼빌리티를 가진 레이어의 경우에만 영향을 미칩니다.

예시
-------

GeoServices REST 서버에 대한 피처 서비스 요청의 결과물을 읽어오기(이 서버는 페이지 작업을 지원하지 않는다는 사실에 주의하십시오):

::

   ogrinfo -ro -al "http://sampleserver3.arcgisonline.com/ArcGIS/rest/services/Hydrography/Watershed173811/FeatureServer/0/query?where=objectid+%3D+objectid&outfields=*&f=json"

참고
--------

-  :ref:`GeoJSON <vector.geojson>` 드라이버

-  `GeoServices REST 사양 <http://www.esri.com/industries/landing-pages/geoservices/geoservices.html>`_

