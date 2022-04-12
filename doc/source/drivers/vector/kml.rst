.. _vector.kml:

KML - 키홀 마크업 언어
=============================

.. shortname:: KML

.. build_dependencies:: (read support needs libexpat) 

KML(Keyhole Markup Language)은 3차원 지리공간 데이터의 표시(display)를 관리하기 위한 XML 기반 언어입니다. KML은 OGC 표준으로 받아들여졌으며, 주요 지리 브라우저(GeoBrowser)들 상에서 어떤 방식으로든 지원되고 있습니다. KML 사양은 EPSG:4326 투영법 하나만 사용한다는 사실을 기억하십시오. 모든 OGR KML 산출물은 EPSG:4326 좌표계를 사용할 것입니다. OGR는 레이어를 정확한 좌표계로 생성하고 모든 도형을 그에 맞춰 변환할 것입니다.

KML 드라이버는 현재 벡터 레이어만 처리합니다. (*GDAL 프로젝트와 함께 제공되는 추가 스크립트로 다른 유형의 산출물을 작성할 수 있습니다.*)

드라이버 케이퍼빌리티
-------------------

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::

KML 읽기
~~~~~~~~~~~

GDAL/OGR가 Expat XML 파서와 함께 빌드된 경우에만 KML 파일을 읽을 수 있습니다. 그렇지 않다면 KML 쓰기만 지원할 것입니다.

``Point``, ``Linestring``, ``Polygon``, ``MultiPoint``, ``MultiLineString``, ``MultiPolygon`` 및 ``MultiGeometry`` 도형 유형을 지원합니다. 제한 사항도 있습니다. 예를 들면 소스 KML 파일에 있는 폴더의 내포 본질은 사라지고, 폴더의 ``<description>`` 태그는 산출물에 작성되지 않을 것입니다.
도형 유형 여러 개를 -- 예를 들어 POINT와 POLYGON을 함께 -- 담고 있는 폴더를 지원합니다.

KML 쓰기
~~~~~~~~~~~

KML의 모든 객체를 OGR 단순 피처 도형 모델로 표현할 수는 없기 때문에, GDAL/OGR 내에서 많은 KML 특화 속성을 생성하지 못 할 것입니다. 어떤 것이 가능한지 감을 잡으려면 먼저 테스트 파일 몇 개를 시도해보십시오.

KML 파일을 산출할 때, OGR KML 드라이버는 각 OGR 레이어를 KML 폴더로 변환할 것입니다. (레이어 하나에 요소들의 도형 유형을 -- 예를 들면 ``LINESTRING`` 과 ``POINT`` 데이터를 -- 혼합하려 하는 경우 예상하지 못 한 습성이 드러날 수도 있습니다.)

KML 드라이버는 몇몇 레이어 또는 소스 KML 폴더의 이름을 드라이버가 무결한 것으로 간주하는 새 이름으로 재명명할 것입니다. 예를 들어 첫 번째 이름 없는 레이어의 기본명인 '``Layer #0``' 을 ``'Layer__0'`` 으로 재명명합니다.

KML은 서식 및 객체 데이터의 혼합물입니다. 대부분의 지리 브라우저는 위치표시(Placemark)의 <description> 태그를 HTML으로 채워진 풍선으로 출력할 것입니다. KML을 작성할 때, 레이어 요소 속성을 단순 스키마 필드로 추가합니다. 이렇게 하면 객체 유형 정보를 가장 잘 보전합니다.

채우기, 라인 색상 및 기타 스타일 작업 속성을 제한적으로 지원합니다. 실제 습성에 대한 감을 잡으려면 먼저 샘플 파일 몇 개를 시도해보십시오.

인코딩 문제점
~~~~~~~~~~~~~~~

Expat 라이브러리는 다음 내장 인코딩 읽기를 지원합니다:

-  US-ASCII
-  UTF-8
-  UTF-16
-  ISO-8859-1
-  Windows-1252

OGR가 반환하는 콘텐츠는 파일 헤더에 언급된 인코딩으로 변환한 다음 UTF-8로 인코딩될 것입니다.

KML 파일이 앞의 인코딩 가운데 하나로 인코딩되지 않은 경우, KML 드라이버는 해당 파일을 파싱하지 않을 것입니다. 해당 파일을 지원되는 인코딩 가운데 하나로 -- 예를 들면 *iconv* 유틸리티를 이용해서 -- 변환한 다음 XML 헤더에 있는 *encoding* 파라미터를 그에 맞춰 변경할 수도 있습니다.

KML 파일 작성 시, 이 드라이버는 UTF-8 콘텐츠가 전송되어 올 것으로 예상합니다.

생성 옵션
~~~~~~~~~~~~~~~~

다음 데이터셋 생성 옵션들을 지원합니다:

-  **NameField**:
   KML <name> 요소를 위해 사용할 필드를 지정할 수 있습니다. 기본값은 'Name'입니다.

-  **DescriptionField**:
   KML <description> 요소를 위해 사용할 필드를 지정할 수 있습니다. 기본값은 'Description'입니다.

-  **AltitudeMode**:
   KML 도형에 사용할 AltitudeMode를 지정할 수 있습니다. 이 옵션은 3차원 도형에만 영향을 미치며, 무결한 KML 옵션 가운데 하나여야만 합니다. 자세한 정보는 `관련 KML 참고 자료 <http://code.google.com/apis/kml/documentation/kml_tags_21.html#altitudemode>`_ 를 참조하십시오.

   ::

      ogr2ogr -f KML output.kml input.shp -dsco AltitudeMode=absolute

-  **DOCUMENT_ID=string**:
   GDAL 2.2버전부터, DOCUMENT_ID 데이터소스 생성 옵션을 사용해서 루트 <Document> 노드의 ID를 지정할 수 있습니다. 기본값은 'root_doc'입니다.

VSI 가상 파일 시스템 API 지원
-----------------------------------

이 드라이버는 VSI 가상 파일 시스템 API가 관리하는 파일의 읽기 및 쓰기를 지원합니다. VSI 가상 파일 시스템 API이 관리하는 파일에는 "정규" 파일은 물론 /vsizip/ (읽기-쓰기) , /vsigzip/ (읽기-쓰기) , /vsicurl/ (읽기 전용) 도메인에 있는 파일도 포함됩니다.

/dev/stdout 또는 /vsistdout/ 에 쓰기도 지원합니다.

예시
-------

-  ogr2ogr 유틸리티를 사용해서 KML에 대한 PostGIS 쿼리의 결과물을 덤프하기:

   ::

      ogr2ogr -f KML output.kml PG:'host=myserver dbname=warmerda' -sql "SELECT pop_1994 from canada where province_name = 'Alberta'"

-  .kml 파일의 내용을 OGR가 인식하는 대로 덤프하는 방법:

   ::

      ogrinfo -ro somedisplay.kml

주의할 점
-------

구글 어스가 폴리곤 같은 복잡 도형의 좌표 개수와 관련된 몇 가지 제한을 가지고 있는 것으로 보입니다.
이런 문제가 발생할 경우, 문제가 되는 도형이 완전히 또는 부분적으로 수직 스트라이프로 덮입니다.
안타깝지만 KML 사양은 이런 제한 사항에 관한 정확한 개수를 명기하고 있지 않기 때문에, KML 드라이버가 이런 잠재적인 문제에 관해 경고하지 않을 것입니다.
사용할 수 있고 테스트된 해결 방법 가운데 하나는 라인 또는 폴리곤을 단순화해서 좌표 몇 개를 제거하는 것입니다.
`구글 KML 개발자 포럼 <http://groups.google.com/group/kml-support>`_ 의 `수직 스트라이프와 함께 표시되는 폴리곤(polygon displays with vertical stripes) <http://groups.google.com/group/kml-support-getting-started/browse_thread/thread/e6995b8073e69c41>`_ 스레드에서 이 문제점에 관해 토의하고 있습니다.

참고
--------

-  `KML 사양 <https://developers.google.com/kml/?csw=1>`_
-  `KML 예제 <https://developers.google.com/kml/documentation/kml_tut>`_
-  :ref:`LIBKML <vector.libkml>` 드라이버: 대안 GDAL KML 드라이버

