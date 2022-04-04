.. _vector.csw:

CSW - OGC CSW (웹 용 카탈로그 서비스)
===========================================

.. shortname:: CSW

.. build_dependencies:: libcurl

이 드라이버는 OGC CSW 서비스에 접속할 수 있습니다. CSW 2.0.2 프로토콜을 지원합니다.
protocol. CSW 드라이버를 컴파일하려면 GDAL/OGR를 cURL 지원과 함께 빌드해야만 합니다. 또한 읽기 지원을 위해 GML 드라이버를 설정해야 합니다. (즉 GDAL/OGR를 Xerces 또는 Expat 지원과 함께 빌드해야만 합니다.)

이 드라이버는 더블린 코어(Dublin Core) 메타데이터를 가진 레코드를 가져옵니다.

드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

데이터셋 이름 문법
-------------------

CSW 데이터소스를 열기 위한 최소한의 문법은 다음과 같습니다:

::

   CSW:[URL=...]

또는

::

   CSW:http://path/to/CSW/endpoint


다음과 같은 열기 옵션들을 사용할 수 있습니다:

-  **URL**:
   CSW 서버 종단점(endpoint)을 가리키는 URL입니다. (연결 문자열에 이미 존재하는 경우 지정하지 않습니다.)

-  **ELEMENTSETNAME=brief/summary/full**:
   속성 상세 정보 수준을 지정합니다. 기본값은 full입니다.

-  **FULL_EXTENT_RECORDS_AS_NON_SPATIAL=YES/NO**:
   [-180,-90,180,90] 범위를 가진 레코드를 비공간 레코드로 간주할지 여부를 선택합니다. 기본값은 NO입니다.

-  **OUTPUT_SCHEMA=URL**:
   서버가 지원하는 제한된 집합에서 outputSchema 파라미터의 값을 지정합니다.
   *gmd* 특수값을 http://www.isotc211.org/2005/gmd 를 가리키는 단축키로 사용할 수 있고, *csw* 특수값을 http://www.opengis.net/cat/csw/2.0.2 를 가리키는 단축키로 사용할 수 있습니다. 이 열기 옵션을 설정하는 경우, *raw_xml* 필드를 각 레코드의 XML 내용으로 채울 것입니다. 다른 메타데이터 필드는 빈 채로 내버려 둘 것입니다.

-  **MAX_RECORDS=value**:
   한 번에 가져올 레코드의 최대 개수를 지정합니다. 기본값은 500입니다. 서버가 더 낮은 값을 지원할 수도 있습니다.

필터링
---------

이 드라이버는 :cpp:func:`OGRLayer::SetSpatialFilter` 함수에 설정된 모든 공간 필터를 서버로 포워딩할 것입니다. 가능한 경우 :cpp:func:`OGRLayer::SetAttributeFilter` 함수에 설정된 속성 필터에 대해서도 (OGR SQL 언어를 OGC 필터 설명으로 변환해서) 마찬가지로 최선을 다할 것입니다.

모든 텍스트 필드를 검색하려면 *anytext* 필드를 쿼리하면 됩니다. 하지만 정보가 복제되는 일을 피하기 위해 OGR 쪽에서 항상 NULL 컨텐츠로 반환한다는 사실을 기억하십시오.

문제점
------

일부 서버가 EPSG 축 순서를, 특히 WGS84 측지 좌표의 위도/경도 순서를 지원하지 않습니다. 이런 경우 GML_INVERT_AXIS_ORDER_IF_LAT_LONG 환경설정 옵션을 NO로 지정해야 할 수도 있습니다.

예시
--------

CSW 서버의 모든 레코드를 목록화하기:

::

   ogrinfo -ro -al -noextent CSW:http://catalog.data.gov/csw

지정한 필드에 공간 및 속성 필터를 적용해서 CSW 서버의 모든 레코드를 목록화하기:

::

   ogrinfo -ro -al -noextent CSW:http://catalog.data.gov/csw -spat 2 49 2 49 -where "subject LIKE '%mineralogy%'"

모든 텍스트 필드에서 지정한 텍스트와 일치하는 CSW 서버의 모든 레코드를 목록화하기:

::

   ogrinfo -ro -al -q CSW:http://catalog.data.gov/csw -spat 2 49 2 49 -where "anytext LIKE '%France%'"

CSW 서버의 모든 레코드를 ISO 19115/19119로 목록화하기:

::

   ogrinfo -ro -al -q CSW:http://catalog.data.gov/csw -oo OUTPUT_SCHEMA=gmd

참고
--------

-  `OGC CSW 표준 <http://www.opengeospatial.org/standards/cat>`_

-  :ref:`GML <vector.gml>` 드라이버

