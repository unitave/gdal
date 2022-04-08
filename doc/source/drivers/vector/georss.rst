.. _vector.georss:

GeoRSS : RSS 피드 용 지리 인코딩 객체
=====================================================

.. shortname:: GeoRSS

.. build_dependencies:: (읽기 지원에 libexpat 필요)

GeoRSS(Geographically Encoded Objects for RSS feeds)란 RSS 또는 ATOM 피드에서 위치를 인코딩하는 방식을 말합니다.

OGR는 GeoRSS 읽기 및 쓰기를 지원합니다. GDAL이 *Expat* 라이브러리 지원과 함께 빌드된 경우에만 읽기 지원을 사용할 수 있습니다.

이 드라이버는 RSS 2.0 또는 ATOM 1.0 포맷 RSS 문서를 지원합니다.

`위치를 인코딩하는 세 가지 방법 <https://georss.org/model.html>`_ -- GeoRSS Simple, GeoRSS GML 그리고 W3C Geo (후자는 퇴출되었습니다) -- 도 지원합니다.

이 드라이버는 위치 정보가 없는 문서도 읽고 쓸 수 있습니다.

GeoRSS 문서의 기본 원점(datum)은 WGS84 원점(EPSG:4326)입니다. XML 파일에서 GeoRSS 위치를 위도-경도 순서로 인코딩하긴 하지만, 이 드라이버가 리포트하거나 예상하는 좌표는 모두 경도-위도 순서입니다. OGR가 사용하는 경도/위도 순서는 다른 OGR 드라이버 및 유틸리티 대부분과의 호환성을 위한 것입니다. GML로 인코딩된 위치의 경우, 이 드라이버는 다른 공간 좌표계를 서술하기 위한 srsName을 지원할 것입니다.

Simple 및 GML 인코딩은 *box* 를 도형으로 인식합니다. OGR 단순 피처 모델에서는 *box* 를 직사각형(폴리곤 도형)으로 디코딩할 것입니다.

RSS 문서를 읽어오는 동안 단일 레이어 하나를 반환합니다. <item>(RSS 문서) 또는 <entry>(ATOM 문서) 요소의 내용으로부터 객체들을 가져옵니다.

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

OGR가 반환하는 콘텐츠는 파일 헤더에 언급된 인코딩으로 변환한 다음 UTF-8로 인코딩될 것입니다.

사용자의 GeoRSS 파일이 앞의 인코딩 가운데 하나로 인코딩되지 않은 경우, GeoRSS 드라이버로 파싱되지 않을 것입니다. 해당 파일을 지원되는 인코딩 가운데 하나로 -- 예를 들면 *iconv* 유틸리티를 이용해서 -- 변환한 다음 XML 헤더에 있는 *encoding* 파라미터를 그레 맞춰 변경할 수도 있습니다.

GeoRSS 파일 작성 시, 이 드라이버는 UTF-8 콘텐츠가 전송되어 올 것으로 예상합니다.

필드 정의
-----------------

GeoRSS 문서를 읽어올 때, 드라이버가 먼저 문서 전체를 스캔해서 필드 정의를 가져올 것입니다.

이 드라이버는 RSS 채널 또는 ATOM 피드의 기반 스키마에 있는 요소들을 반환할 것입니다. 이름공간(namespace)에 허용되는 확장 사양 요소들도 반환할 것입니다.

첫 번째 수준 요소의 속성을 필드로 노출시킬 것입니다.

복잡 콘텐츠(첫 번째 수준 요소 안에 있는 요소들)를 XML 블랍(blob)으로 반환할 것입니다.

동일한 요소가 반복되는 경우, 속성 이름 뒤에 반복 횟수를 의미하는 숫자를 붙일 것입니다. RSS 및 ATOM 문서에 있는, 예를 들어 <category> 요소의 경우 이 습성이 유용합니다.

다음과 같은 내용을:

::

       <item>
           <title>My tile</title>
           <link>http://www.mylink.org</link>
           <description>Cool description !</description>
           <pubDate>Wed, 11 Jul 2007 15:39:21 GMT</pubDate>
           <guid>http://www.mylink.org/2007/07/11</guid>
           <category>Computer Science</category>
           <category>Open Source Software</category>
           <georss:point>49 2</georss:point>
           <myns:name type="my_type">My Name</myns:name>
           <myns:complexcontent>
               <myns:subelement>Subelement</myns:subelement>
           </myns:complexcontent>
       </item>

OGR 단순 피처 모델은 이렇게 해석할 것입니다:

::

     title (String) = My title
     link (String) = http://www.mylink.org
     description (String) = Cool description !
     pubDate (DateTime) = 2007/07/11 15:39:21+00
     guid (String) = http://www.mylink.org/2007/07/11
     category (String) = Computer Science
     category2 (String) = Open Source Software
     myns_name (String) = My Name
     myns_name_type (String) = my_type
     myns_complexcontent (String) = <myns:subelement>Subelement</myns:subelement>
     POINT (2 49)

생성 문제점
---------------

내보내기 작업 시, 모든 레이어를 단일 파일로 작성합니다. 기존 파일 업데이트는 지원하지 않습니다.

산출 파일이 이미 존재하는 경우, 작성하지 않을 것입니다. 먼저 기존 파일을 삭제해야 합니다.

방금 생성한 파일을 즉시 읽어올 수 없습니다. 종료한 다음 다시 열어야 합니다. 다시 말해 동일한 세션에서 데이터셋이 읽기전용이기도 하고 쓰기전용이기도 하다는 의미입니다.

다음 도형을 지원합니다:

-  wkbPoint/wkbPoint25D 유형의 객체
-  wkbLineString/wkbLineString25D 유형의 객체
-  wkbPolygon/wkbPolygon25D 유형의 객체

다른 도형 유형은 지원하지 않으며, 암묵적으로 무시할 것입니다.

GeoRSS 작성기는 다음 *데이터셋* 생성 옵션들을 지원합니다:

-  **FORMAT=RSS|ATOM**:
   문서 포맷을 RSS 2.0 또는 ATOM 1.0 가운데 하나로 설정합니다. 기본값은 RSS입니다.

-  **GEOM_DIALECT=SIMPLE|GML|W3C_GEO**: (RSS 또는 ATOM 문서)
   위치 정보의 인코딩을 설정합니다. 기본값은 SIMPLE입니다.
   W3C_GEO는 포인트 도형만 지원합니다.
   SIMPLE 또는 W3C_GEO는 지리 WGS84 좌표 도형만 지원합니다.

-  **USE_EXTENSIONS=YES|NO**:
   기본값은 NO입니다. YES로 설정하면, 확장 사양 필드를 (다시 말해 RSS 또는 ATOM 문서의 기반 스키마에 없는 필드를) 작성할 것입니다. 기반 스키마에 없는 필드명이 foo_bar 패턴과 일치하는 경우, "foo"를 요소의 이름공간으로 간주하고 <foo:bar> 요소를 작성할 것입니다. 그렇지 않으면, <ogr:> 이름공간에 요소를 작성할 것입니다.

-  **WRITE_HEADER_AND_FOOTER=YES|NO**:
   기본값은 YES입니다. NO로 설정하는 경우, <entry> 또는 <item> 요소만 작성할 것입니다. 사용자가 문서의 알맞은 헤더와 푸터를 작성해줘야 할 것입니다. 이 경우 다음 옵션들은 의미가 없습니다.

-  **HEADER**: (RSS 또는 ATOM 문서)
   RSS 문서의 경우 <channel> 요소와 첫 번째 <item> 사이에 들어갈, 또는 ATOM 문서의 경우 xml 태그와 첫 번째 <entry> 요소 사이에 들어갈 XML 내용입니다. 이 옵션을 설정하는 경우, 다음 옵션들을 대체할 것입니다.

-  **TITLE**: (RSS 또는 ATOM 문서)
   헤더의 <title> 요소 안에 넣을 값을 설정합니다. 설정하지 않는 경우, 해당 요소가 필수적이기 때문에 더미값을 사용할 것입니다.

-  **DESCRIPTION**: (RSS 문서)
   헤더의 <description> 요소 안에 넣을 값을 설정합니다. 설정하지 않는 경우, 해당 요소가 필수적이기 때문에 더미값을 사용할 것입니다.

-  **LINK**: (RSS 문서)
   헤더의 <link> 요소 안에 넣을 값을 설정합니다. 설정하지 않는 경우, 해당 요소가 필수적이기 때문에 더미값을 사용할 것입니다.

-  **UPDATED**: (ATOM 문서)
   헤더의 <updated> 요소 안에 넣을 값을 설정합니다. XML 날짜&시간 서식으로 작성되어야 합니다. 설정하지 않는 경우, 해당 요소가 필수적이기 때문에 더미값을 사용할 것입니다.

-  **AUTHOR_NAME**: (ATOM 문서)
   헤더의 <author><name> 요소 안에 넣을 값을 설정합니다. 설정하지 않는 경우, 해당 요소가 필수적이기 때문에 더미값을 사용할 것입니다.

-  **ID**: (ATOM 문서)
   헤더의 <id> 요소 안에 넣을 값을 설정합니다. 설정하지 않는 경우, 해당 요소가 필수적이기 때문에 더미값을 사용할 것입니다.

소스 데이터셋으로부터 변환할 때, 소스 데이터셋의 필드 이름을 <title>, <description> 등등 같은 예상되는 RSS 또는 ATOM 속성 이름으로 재명명해야 할 수도 있습니다. 이 작업은 :ref:`OGR VRT <vector.vrt>` 데이터셋으로 할 수도 있고, 또는 ogr2ogr 유틸리티의 "-sql" 옵션을 사용해서 할 수도 있습니다. (:ref:`rfc-21` 을 참조하십시오.)

VSI 가상 파일 시스템 API 지원
-----------------------------------

이 드라이버는 VSI 가상 파일 시스템 API가 관리하는 파일의 읽기 및 쓰기를 지원합니다. VSI 가상 파일 시스템 API이 관리하는 파일에는 "정규" 파일은 물론 /vsizip/ (읽기-쓰기) , /vsigzip/ (읽기-쓰기) , /vsicurl/ (읽기 전용) 도메인에 있는 파일도 포함됩니다.

/dev/stdout 또는 /vsistdout/ 에 쓰기도 지원합니다.

예시
-------

-  ogrinfo 유틸리티를 사용해서 GeoRSS 데이터 파일의 콘텐츠를 덤프하기:

::

   ogrinfo -ro -al input.xml

-  ogr2ogr 유틸리티를 사용해서 GeoRSS에서 GeoRSS로 변환하기. 예를 들어, ATOM 문서를 RSS 문서로 변환하기:

::

   ogr2ogr -f GeoRSS output.xml input.xml "select link_href as link, title, content as description, author_name as author, id as guid from georss"

.. note::

   앞의 예시에서는 동등한 필드들을, 소스 이름으로부터 대상 포맷의 예상 이름으로 매핑합니다.

-  다음 파이썬 스크립트는 온라인 GeoRSS 피드의 내용을 어떻게 읽어오는지 보여줍니다:

.. code-block:: python

       #!/usr/bin/python
       import gdal
       import ogr
       import urllib2

       url = 'http://earthquake.usgs.gov/eqcenter/catalogs/eqs7day-M5.xml'
       content = None
       try:
           handle = urllib2.urlopen(url)
           content = handle.read()
       except urllib2.HTTPError, e:
           print 'HTTP service for %s is down (HTTP Error: %d)' % (url, e.code)
       except:
           print 'HTTP service for %s is down.' %(url)

       # Create in-memory file from the downloaded content
       gdal.FileFromMemBuffer('/vsimem/temp', content)

       ds = ogr.Open('/vsimem/temp')
       lyr = ds.GetLayer(0)
       feat = lyr.GetNextFeature()
       while feat is not None:
           print feat.GetFieldAsString('title') + ' ' + feat.GetGeometryRef().ExportToWkt()
           feat.Destroy()
           feat = lyr.GetNextFeature()

       ds.Destroy()

       # Free memory associated with the in-memory file
       gdal.Unlink('/vsimem/temp')

참고
--------

-  `GeoRSS 포맷 홈페이지 <https://georss.org/>`_

-  `GeoRSS 포맷 위키백과 페이지 <http://en.wikipedia.org/wiki/GeoRSS>`_

-  `RSS 포맷 위키백과 페이지 <http://en.wikipedia.org/wiki/RSS>`_

-  `RSS 2.0 사양 <http://www.rssboard.org/rss-specification>`_

-  `ATOM 포맷 위키백과 페이지 <http://en.wikipedia.org/wiki/ATOM_(standard)>`_

-  `ATOM 1.0 사양 <http://www.ietf.org/rfc/rfc4287.txt>`_

