.. _vector.libkml:

LIBKML 드라이버 (.kml .kmz)
=========================

.. shortname:: LIBKML

.. build_dependencies:: libkml

LIBKML 드라이버는 `KML <http://www.opengeospatial.org/standards/kml/>`_ 읽기 및 쓰기를 크로스 플랫폼 C++ 라이브러리의 형태로 참조 구현한 `libkml <https://github.com/libkml/libkml>`_ 의 클라이언트입니다. 이 OGR 드라이버를 사용하기 위해서는 libkml을 빌드하고 설치해야만 합니다. libkml 1.3버전 또는 마스터 브랜치를 빌드해야 한다는 점을 주의하십시오.

LIBKML 드라이버를 빌드하고 포함시키는 경우, OGR에서 이전 :ref:`KML 드라이버 <vector.kml>` 를 무시하고 이 드라이버를 KML의 기본 판독기로 사용할 것이라는 사실을 기억하십시오. 그래도 명령줄을 통해 산출 드라이버를 KML 또는 LIBKML 가운데 하나로 지정할 수 있습니다.

구글이 제공하는 libkml은 무결한 모든 KML 파일에 대한 읽기 서비스를 지원합니다. 하지만, 일부 KML 특수 기능은 OGR가 사용하는 단순 피처(Simple Feature) 사양의 내부 구조로 매핑되지 않기 때문에 주의해야 합니다. 따라서 이 드라이버는 libkml 라이브러리를 이용해서 OGR로 읽어온 KML 파일의 내용을 이해하기 위해 최선을 다할 테지만, 그 결과는 다를 수 있습니다. 드라이버가 어떤 것을 이해하는지에 대해 감을 잡으려면 KML 파일을 몇 개 샘플로 시도해보십시오. 특히 심도가 1을 초과하는 객체 집합의 내포 작업은 OGR의 내부 포맷을 지원하기 위해 평탄화될 것입니다.

드라이버 케이퍼빌리티
-------------------

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::

데이터소스
----------
데이터소스를 KML 파일 ``somefile.kml``, 디렉터리 ``somedir/``, 또는 KMZ 파일 ``somefile.kmz`` 로 지정할 수도 있습니다.

디렉터리 및 KMZ 데이터소스의 경우 기본적으로 doc.kml 파일에 모든 레이어의 색인 파일을 읽고 쓸 것입니다. 이 파일은 데이터소스에 있는 각 레이어의 `<NetworkLink> <https://developers.google.com/kml/documentation/kmlreference#networklink>`_ 를 담고 있습니다. LIBKML_USE_DOC.KML 환경설정 옵션을 NO로 설정해서 이 기능을 비활성화시킬 수 있습니다.

StyleTable
~~~~~~~~~~

데이터소스 스타일 테이블은 KML 파일의 경우 .kml 파일의, KMZ 파일의 경우 style/style.kml 파일의, 또는 디렉터리의 경우 style.kml 파일의 `<Document> <https://developers.google.com/kml/documentation/kmlreference#document>`_ 에 하나 이상의 `<Style> <https://developers.google.com/kml/documentation/kmlreference#style>`_ 요소로 작성됩니다. 모든 :ref:`ogr_feature_style` 을 KML로 변환하지는 못 합니다.

데이터소스 생성 옵션
~~~~~~~~~~~~~~~~~~~~~~~~~~~

다음과 같은 데이터소스 생성 옵션들을 사용해서 최상위 <Document> 수준에 `<atom:Author> <https://developers.google.com/kml/documentation/kmlreference#atomauthor>`_ 요소를 생성할 수 있습니다.

-  **AUTHOR_NAME**
-  **AUTHOR_URI**
-  **AUTHOR_EMAIL**

**LINK** 데이터소스 생성 옵션을 사용해서 최상위 <Document> 수준에 있는 `<atom:link> <https://developers.google.com/kml/documentation/kmlreference#atomlink>`_ 요소의 하이퍼텍스트 참조(href)를 지정할 수 있습니다.

**PHONENUMBER** 데이터소스 생성 옵션을 사용해서 최상위 <Document> 수준에 있는 `<phoneNumber> <https://developers.google.com/kml/documentation/kmlreference#phonenumber>`_ 요소를 지정할 수 있습니다. 이 옵션의 값은 `IETF RFC 3966 <http://tools.ietf.org/html/rfc3966>`_ 의 문법을 따라야만 합니다.

GDAL 2.2버전부터, **DOCUMENT_ID** 데이터소스 생성 옵션을 사용해서 루트 <Document> 노드의 ID를 지정할 수 있습니다. 기본값은 'root_doc'입니다.

컨테이너 속성
^^^^^^^^^^^^^^^^^^^^

다음과 같은 데이터셋 생성 옵션들을 사용해서 컨테이너 옵션을 설정할 수 있습니다:

-  **NAME**:
   `<name> <https://developers.google.com/kml/documentation/kmlreference#name>`_ 요소
-  **VISIBILITY**:
   `<visibility> <https://developers.google.com/kml/documentation/kmlreference#visibility>`_ 요소
-  **OPEN**:
   `<open> <https://developers.google.com/kml/documentation/kmlreference#open>`_ 요소
-  **SNIPPET**:
   `<snippet> <https://developers.google.com/kml/documentation/kmlreference#snippet>`_ 요소
-  **DESCRIPTION**:
   `<description> <https://developers.google.com/kml/documentation/kmlreference#description>`_ 요소

목록 스타일
^^^^^^^^^^

다음과 같은 데이터셋 생성 옵션들을 사용해서 `<ListStyle> <https://developers.google.com/kml/documentation/kmlreference#liststyle>`_ 요소를 통해 구글 어스 브라우저의 장소(Places) 패널에 주 폴더(레이어 폴더)가 나타나는 방식을 제어할 수 있습니다:

-  **LISTSTYLE_TYPE**:
   "check", "radioFolder", "checkOffOnly" 또는 "checkHideChildren" 가운데 하나로 지정할 수 있습니다.
   이 옵션은 `<listItemType> <https://developers.google.com/kml/documentation/kmlreference#listItemType>`_ 요소를 설정합니다.
-  **LISTSTYLE_ICON_HREF**:
   주 폴더에 표시할 아이콘의 URL을 지정합니다.
   이 옵션은 `<ItemIcon> <https://developers.google.com/kml/documentation/kmlreference#itemicon>`_ 요소의 <href> 요소를 설정합니다.

말풍선 스타일
^^^^^^^^^^^^^

*foo* 스타일을 정의한 경우, **foo_BALLOONSTYLE_BGCOLOR** 그리고/또는 **foo_BALLOONSTYLE_TEXT** 옵션을 지정해서 해당 스타일에 `<BalloonStyle> <https://developers.google.com/kml/documentation/kmlreference#balloonstyle>`_ 요소를 추가할 수 있습니다.

NetworkLinkControl
^^^^^^^^^^^^^^^^^^

다음 데이터셋 생성 옵션들 가운데 최소한 하나를 지정하면 `<NetworkLinkControl> <https://developers.google.com/kml/documentation/kmlreference#networklinkcontrol>`_ 요소를 정의할 수 있습니다:

-  **NLC_MINREFRESHPERIOD** :
   `<minRefreshPeriod> <https://developers.google.com/kml/documentation/kmlreference#minrefreshperiod>`_ 요소를 설정합니다.
-  **NLC_MAXSESSIONLENGTH** :
   `<maxSessionLength> <https://developers.google.com/kml/documentation/kmlreference#maxsessionlength>`_ 요소를 설정합니다.
-  **NLC_COOKIE** :
   `<cookie> <https://developers.google.com/kml/documentation/kmlreference#cookie>`_ 요소를 설정합니다.
-  **NLC_MESSAGE** :
   `<message> <https://developers.google.com/kml/documentation/kmlreference#message>`_ 요소를 설정합니다.
-  **NLC_LINKNAME** :
   `<linkName> <https://developers.google.com/kml/documentation/kmlreference#linkname>`_ 요소를 설정합니다.
-  **NLC_LINKDESCRIPTION** :
   `<linkDescription> <https://developers.google.com/kml/documentation/kmlreference#linkdescription>`_ 요소를 설정합니다.
-  **NLC_LINKSNIPPET** :
   `<linkSnippet> <https://developers.google.com/kml/documentation/kmlreference#linksnippet>`_ 요소를 설정합니다.
-  **NLC_EXPIRES** :
   `<expires> <https://developers.google.com/kml/documentation/kmlreference#expires>`_ 요소를 설정합니다.

문서 업데이트
^^^^^^^^^^^^^^^^
**UPDATE_TARGETHREF** 데이터셋 생성 옵션을 정의하는 경우, `<Update> <https://developers.google.com/kml/documentation/kmlreference#update>`_ 요소를 가진 NetworkLinkControl KML 파일을 업데이트할 것입니다. `업데이트 예제 <https://developers.google.com/kml/documentation/updates>`_ 를 참조하십시오.

레이어 상에서의 CreateFeature() 작업은 `<Create> <https://developers.google.com/kml/documentation/kmlreference#create>`_ 요소로 변환될 것입니다.

레이어 상에서의 SetFeature() 작업은 `<Change> <https://developers.google.com/kml/documentation/kmlreference#change>`_ 요소로 변환될 것입니다.

레이어 상에서의 DeleteFeature() 작업은 `<Delete> <https://developers.google.com/kml/documentation/kmlreference#delete>`_ 요소로 변환될 것입니다.

레이어
-----

:cpp:class:`OGRLayer` 클래스는 KML 파일에서 `<Document> <https://developers.google.com/kml/documentation/kmlreference#document>`_ 또는 `<Folder> <https://developers.google.com/kml/documentation/kmlreference#folder>`_ 요소로 매핑되며, KMZ 파일 또는 디렉터리의 경우 개별 KML 파일로 변환됩니다.

스타일
~~~~~

레이어 스타일 테이블은 `<Folder> <https://developers.google.com/kml/documentation/kmlreference#folder>`_ 요소인 KML 레이어에서 읽거나 쓸 수 없습니다. 그렇지 않은 경우 레이어인 `<Document> <https://developers.google.com/kml/documentation/kmlreference#document>`_ 요소 안에 있습니다.

스키마
~~~~~~

KML 파일, KMZ 파일 및 디렉터리에서 `<Schema> <https://developers.google.com/kml/documentation/kmlreference#schema>`_ 요소의 읽기 및 쓰기를 지원합니다.

레이어 생성 옵션
~~~~~~~~~~~~~~~~~~~~~~

다음 레이어 생성 옵션들을 사용해서 레이어 수준에 있는 `<LookAt> <https://developers.google.com/kml/documentation/kmlreference#lookat>`_ 요소를 생성할 수 있습니다:

-  **LOOKAT_LONGITUDE**: (필수)
-  **LOOKAT_LATITUDE**: (필수)
-  **LOOKAT_RANGE**: (필수)
-  **LOOKAT_HEADING**
-  **LOOKAT_TILT**
-  **LOOKAT_ALTITUDE**
-  **LOOKAT_ALTITUDEMODE**

또는 `<Camera> <https://developers.google.com/kml/documentation/kmlreference#camera>`_ 요소를 생성할 수도 있습니다:

-  **CAMERA_LONGITUDE**: (필수)
-  **CAMERA_LATITUDE**: (필수)
-  **CAMERA_ALTITUDE**: (필수)
-  **CAMERA_ALTITUDEMODE**: (필수)
-  **CAMERA_HEADING**
-  **CAMERA_TILT**
-  **CAMERA_ROLL**

`<Region> <https://developers.google.com/kml/documentation/kmlreference#region>`_ 요소를 생성해서 레이어의 객체의 가시성을 제어할 수 있습니다. REGION_XMIN, REGION_YMIN, REGION_XMAX 및 REGION_YMAX를 지정하는 경우, 레이어에 작성되고 있는 객체의 공간 범위로부터 영역 좌표를 판단합니다:

-  **ADD_REGION=YES/NO** :
   기본값은 NO입니다.
-  **REGION_XMIN**: (선택적)
   영역의 서쪽 좌표를 정의합니다.
-  **REGION_YMIN**: (선택적)
   영역의 남쪽 좌표를 정의합니다.
-  **REGION_XMAX**: (선택적)
   영역의 동쪽 좌표를 정의합니다.
-  **REGION_YMAX**: (선택적)
   영역의 북쪽 좌표를 정의합니다.
-  **REGION_MIN_LOD_PIXELS**: (선택적)
   영역이 표시되기 위한 픽셀 단위 최소 크기입니다. 기본값은 256입니다.
-  **REGION_MAX_LOD_PIXELS**: (선택적)
   영역이 표시되기 위한 픽셀 단위 최대 크기입니다. 기본값은 -1(무한대)입니다.
-  **REGION_MIN_FADE_EXTENT**: (선택적)
   도형이 완전 불투명으로부터 완전 투명으로 희미해지는 거리를 정의합니다. 기본값은 0입니다.
-  **REGION_MAX_FADE_EXTENT**: (선택적)
   도형이 완전 투명으로부터 완전 불투명으로 뚜렷해지는 거리를 정의합니다. 기본값은 0입니다.

`<ScreenOverlay> <https://developers.google.com/kml/documentation/kmlreference#screenoverlay>`_ 요소를 사용해서 로고, 범례 등등을 추가할 수 있습니다:

-  **SO_HREF**: (필수) 표시할 이미지의 URL을 지정합니다.
-  **SO_NAME**: (선택적)
-  **SO_DESCRIPTION**: (선택적)
-  **SO_OVERLAY_X**: (선택적)
-  **SO_OVERLAY_Y**: (선택적)
-  **SO_OVERLAY_XUNITS**: (선택적)
-  **SO_OVERLAY_YUNITS**: (선택적)
-  **SO_SCREEN_X**: (선택적). 기본값은 0.05입니다.
-  **SO_SCREEN_Y**: (선택적). 기본값은 0.05입니다.
-  **SO_SCREEN_XUNITS**: (선택적). 기본값은 분수(fraction)입니다.
-  **SO_SCREEN_YUNITS**: (선택적). 기본값은 분수(fraction)입니다.
-  **SO_SIZE_X**: (선택적)
-  **SO_SIZE_Y**: (선택적)
-  **SO_SIZE_XUNITS**: (선택적)
-  **SO_SIZE_YUNITS**: (선택적)

기본적으로 레이어를 `<Document> <https://developers.google.com/kml/documentation/kmlreference#document>`_ 요소로 작성합니다. **FOLDER** 레이어 생성 옵션을 YES로 설정하면, (KML 파일인 경우에만) 레이어를 `<Folder> <https://developers.google.com/kml/documentation/kmlreference#folder>`_ 요소로도 작성할 수 있습니다.

다음 레이어 생성 옵션들을 사용해서 컨테이너 옵션을 설정할 수 있습니다:

-  **NAME**:
   `<name> <https://developers.google.com/kml/documentation/kmlreference#name>`_ 요소
-  **VISIBILITY**:
   `<visibility> <https://developers.google.com/kml/documentation/kmlreference#visibility>`_ 요소
-  **OPEN**:
   `<open> <https://developers.google.com/kml/documentation/kmlreference#open>`_ 요소
-  **SNIPPET**:
   `<snippet> <https://developers.google.com/kml/documentation/kmlreference#snippet>`_ 요소
-  **DESCRIPTION**:
   `<description> <https://developers.google.com/kml/documentation/kmlreference#description>`_ 요소

다음과 같은 레이어 생성 옵션들을 사용해서 `<ListStyle> <https://developers.google.com/kml/documentation/kmlreference#liststyle>`_ 요소를 통해 구글 어스 브라우저의 장소(Places) 패널에 해당 레이어의 폴더가 나타나는 방식을 제어할 수 있습니다:

-  **LISTSTYLE_TYPE**:
   "check", "radioFolder", "checkOffOnly" 또는 "checkHideChildren" 가운데 하나로 지정할 수 있습니다.
   이 옵션은 `<listItemType> <https://developers.google.com/kml/documentation/kmlreference#listItemType>`_ 요소를 설정합니다.
-  **LISTSTYLE_ICON_HREF**:
   레이어에 표시할 아이콘의 URL을 지정합니다.
   이 옵션은 `<ItemIcon> <https://developers.google.com/kml/documentation/kmlreference#itemicon>`_ 요소의 <href> 요소를 설정합니다.

피처
-------

:cpp:class:`OGRFeature` 클래스는 일반적으로 KML의 `<Placemark> <https://developers.google.com/kml/documentation/kmlreference#placemark>`_ 요소로 변환되고, 그 반대의 경우도 마찬가지입니다.

model 필드를 정의한 경우, <Placemark> 요소 안에 `<Model> <https://developers.google.com/kml/documentation/kmlreference#model>`_ 객체를 생성할 것입니다.

networklink 필드를 정의한 경우, `<NetworkLink> <https://developers.google.com/kml/documentation/kmlreference#networklink>`_ 를 생성할 것입니다. 다른 networklink 필드들은 선택적입니다.

photooverlay 필드를 정의한 경우, `<PhotoOverlay> <https://developers.google.com/kml/documentation/kmlreference#photooverlay>`_ 를 생성할 것입니다. (camera_longitude, camera_latitude, camera_altitude, camera_altitudemode, head 그리고/또는 tilt 그리고/또는 roll, leftfov, rightfov, bottomfov, topfov, near 필드도 설정되었다고 가정합니다. shape 필드는 선택적입니다.)

<PhotoOverlay> 객체가 대용량 이미지인 경우, `PhotoOverlay 예제 <https://developers.google.com/kml/documentation/photos>`_ 에서 설명하는 대로 타일화해서 오버뷰 수준들을 생성할 것을 강력히 권장합니다. 이 경우, URL이 photooverlay 필드에 있는 "$[level]", "$[x]" 및 "$[y]" 하위 문자열을 담고 있어야 하고, imagepyramid_tilesize, imagepyramid_maxwidth, imagepyramid_maxheight 및 imagepyramid_gridorigin 필드가 설정되어 있어야 합니다.

Placemark, Model, NetworkLink 및 PhotoOverlay 객체는 camera_longitude, camera_latitude, camera_altitude, camera_altitudemode, head 그리고/또는 tilt 그리고/또는 roll 필드가 정의되어 있는 경우 관련 카메라를 가질 수 있습니다.

(LIBKML_READ_GROUND_OVERLAY 환경설정 옵션이 FALSE로 설정되지 않은 이상) KML `<GroundOverlay> <https://developers.google.com/kml/documentation/kmlreference#groundoverlay>`_ 요소의 읽기를 지원합니다. 이 요소는 icon 및 drawOrder 필드를 가지고 있습니다.

.. _style-1:

스타일
~~~~~

피처 수준의 스타일 문자열은 KML의 각 `<Placemark> <https://developers.google.com/kml/documentation/kmlreference#placemark>`_ 에 `<Style> <https://developers.google.com/kml/documentation/kmlreference#style>`_ 또는 `<StyleUrl> <https://developers.google.com/kml/documentation/kmlreference#styleurl>`_ 가운데 하나로 매핑됩니다.

KML 피처를 읽어올 때 LIBKML_RESOLVE_STYLE 환경 변수가 YES로 설정되어 있는 경우, 스타일 테이블에서 StyleUrl을 검색해서 피처 스타일 문자열을 테이블로부터 나온 스타일로 설정합니다. 이렇게 하면 스타일 테이블을 읽어오지 않는 MapServer 같은 응용 프로그램에 공유 스타일을 읽어오게 할 수 있습니다.

KML 피처를 읽어올 때 LIBKML_EXTERNAL_STYLE 환경 변수가 YES로 설정되어 있는 경우, 디스크 또는 서버로부터 데이터소스 외부에 있는 StyleUrl을 가져와서 데이터소스 스타일 테이블에 파싱합니다. 스타일 KML을 읽어올 수 없거나 LIBKML_EXTERNAL_STYLE 환경 변수가 NO로 설정되어 있다면, StyleUrl을 스타일 문자열로 복사합니다.

KML StyleMap을 읽어올 때 기본 매핑은 "NORMAL"로 설정됩니다. 강조 스타일을 이용하고 싶다면 LIBKML_STYLEMAP_KEY 환경 변수를 "HIGHLIGHT"으로 설정하십시오.

KML 작성 시, "astylename_normal"과 "astylename_highlight" 형식의 스타일 2개가 있는 경우 (이때 astylename은 어떤 문자열이라도 될 수 있습니다) 두 스타일 모두로부터 StyleMap 객체를 생성하고 "astylename"으로 명명할 것입니다.

필드
------

OGR 필드(피처 속성)는 KML에 `<Schema> <https://developers.google.com/kml/documentation/kmlreference#schema>`_ 그리고 `<SimpleData> <https://developers.google.com/kml/documentation/kmlreference#simpledata>`_ 로 매핑됩니다. 아래 따로 설명하는 몇몇 특수 필드는 예외입니다.

주의: LIBKML_USE_SCHEMADATA 환경설정 옵션을 NO로 설정해서 필드를 `<Data> <https://developers.google.com/kml/documentation/kmlreference#data>`_ 요소로도 내보낼 수 있습니다.

풍부한 환경 변수 집합을 사용해서 입력물과 산출물의 필드들을 어떻게 KML `<Placemark> <https://developers.google.com/kml/documentation/kmlreference#placemark>`_ 에 매핑시킬지 정의할 수 있습니다.
예를 들어 'Cities'라는 필드를 KML에 `<name> <https://developers.google.com/kml/documentation/kmlreference#name>`_ 태그로 매핑시키고 싶다면, Name 환경 변수를 설정하면 됩니다.

Name
   이 문자열 필드는 KML `<name> <https://developers.google.com/kml/documentation/kmlreference#name>`_ 태그에 매핑됩니다.
   LIBKML_NAME_FIELD 환경 변수로 OGR 필드의 이름을 변경할 수 있습니다.
description
   이 문자열 필드는 KML `<description> <https://developers.google.com/kml/documentation/kmlreference#description>`_ 태그에 매핑됩니다.
   LIBKML_DESCRIPTION_FIELD 환경 변수로 OGR 필드의 이름을 변경할 수 있습니다.
timestamp
   이 문자열 또는 날짜&시간 또는 날짜 그리고/또는 시간 유형 필드는 KML `<timestamp> <https://developers.google.com/kml/documentation/kmlreference#timestamp>`_ 태그에 매핑됩니다.
   LIBKML_TIMESTAMP_FIELD 환경 변수로 OGR 필드의 이름을 변경할 수 있습니다.
begin
   이 문자열 또는 날짜&시간 또는 날짜 그리고/또는 시간 유형 필드는 KML `<begin> <https://developers.google.com/kml/documentation/kmlreference#begin>`_ 태그에 매핑됩니다.
   LIBKML_BEGIN_FIELD 환경 변수로 OGR 필드의 이름을 변경할 수 있습니다.
end
   이 문자열 또는 날짜&시간 또는 날짜 그리고/또는 시간 유형 필드는 KML `<end> <https://developers.google.com/kml/documentation/kmlreference#end>`_ 태그에 매핑됩니다.
   LIBKML_END_FIELD 환경 변수로 OGR 필드의 이름을 변경할 수 있습니다.
altitudeMode
   이 문자열 필드는 KML `<altitudeMode> <https://developers.google.com/kml/documentation/kmlreference#altitudemode>`_ 또는 `<gx:altitudeMode> <https://developers.google.com/kml/documentation/kmlreference#gxaltitudemode>`_ 태그에 매핑됩니다.
   LIBKML_ALTITUDEMODE_FIELD 환경 변수로 OGR 필드의 이름을 변경할 수 있습니다.
tessellate
   이 정수형 필드는 KML `<tessellate> <https://developers.google.com/kml/documentation/kmlreference#tessellate>`_ 태그에 매핑됩니다.
   LIBKML_TESSELLATE_FIELD 환경 변수로 OGR 필드의 이름을 변경할 수 있습니다.
extrude
   이 정수형 필드는 KML `<extrude> <https://developers.google.com/kml/documentation/kmlreference#extrude>`_ 태그에 매핑됩니다.
   LIBKML_EXTRUDE_FIELD 환경 변수로 OGR 필드의 이름을 변경할 수 있습니다.
visibility
   이 정수형 필드는 KML `<visibility> <https://developers.google.com/kml/documentation/kmlreference#visibility>`_ 태그에 매핑됩니다.
   LIBKML_VISIBILITY_FIELD 환경 변수로 OGR 필드의 이름을 변경할 수 있습니다.
icon
   이 문자열 필드는 KML `<icon> <https://developers.google.com/kml/documentation/kmlreference#icon>`_ 태그에 매핑됩니다.
   LIBKML_ICON_FIELD 환경 변수로 OGR 필드의 이름을 변경할 수 있습니다.
drawOrder
   이 정수형 필드는 KML `<drawOrder> <https://developers.google.com/kml/documentation/kmlreference#draworder>`_ 태그에 매핑됩니다.
   LIBKML_DRAWORDER_FIELD 환경 변수로 OGR 필드의 이름을 변경할 수 있습니다.
snippet
   이 정수형 필드는 KML `<snippet> <https://developers.google.com/kml/documentation/kmlreference#snippet>`_ 태그에 매핑됩니다.
   LIBKML_SNIPPET_FIELD 환경 변수로 OGR 필드의 이름을 변경할 수 있습니다.
heading
   이 실수형 필드는 KML `<heading> <https://developers.google.com/kml/documentation/kmlreference#heading>`_ 태그에 매핑됩니다.
   LIBKML_HEADING_FIELD 환경 변수로 OGR 필드의 이름을 변경할 수 있습니다. 읽기 작업 시, <Placemark>가 <heading> 요소를 가진 <Camera>를 가지고 있는 경우에만 이 필드가 존재합니다.
tilt
   이 실수형 필드는 KML `<tilt> <https://developers.google.com/kml/documentation/kmlreference#tilt>`_ 태그에 매핑됩니다.
   LIBKML_TILT_FIELD 환경 변수로 OGR 필드의 이름을 변경할 수 있습니다. 읽기 작업 시, <Placemark>가 <tilt> 요소를 가진 <Camera>를 가지고 있는 경우에만 이 필드가 존재합니다.
roll
   이 실수형 필드는 KML `<roll> <https://developers.google.com/kml/documentation/kmlreference#roll>`_ 태그에 매핑됩니다.
   LIBKML_ROLL_FIELD 환경 변수로 OGR 필드의 이름을 변경할 수 있습니다. 읽기 작업 시, <Placemark>가 <roll> 요소를 가진 <Camera>를 가지고 있는 경우에만 이 필드가 존재합니다.
model
   이 문자열 필드를 사용해서 3차원 `<model> <https://developers.google.com/kml/documentation/kmlreference#model>`_ 의 URL을 정의할 수 있습니다.
   LIBKML_MODEL_FIELD 환경 변수로 OGR 필드의 이름을 변경할 수 있습니다.
scale_x
   이 실수형 필드는 3차원 모델 용 KML `<scale> <https://developers.google.com/kml/documentation/kmlreference#scale>`_ 태그의 x 요소에 매핑됩니다.
   LIBKML_SCALE_X_FIELD 환경 변수로 OGR 필드의 이름을 변경할 수 있습니다.
scale_y
   이 실수형 필드는 3차원 모델 용 KML `<scale> <https://developers.google.com/kml/documentation/kmlreference#scale>`_ 태그의 y 요소에 매핑됩니다.
   LIBKML_SCALE_Y_FIELD 환경 변수로 OGR 필드의 이름을 변경할 수 있습니다.
scale_z
   이 실수형 필드는 3차원 모델 용 KML `<scale> <https://developers.google.com/kml/documentation/kmlreference#scale>`_ 태그의 z 요소에 매핑됩니다.
   LIBKML_SCALE_Z_FIELD 환경 변수로 OGR 필드의 이름을 변경할 수 있습니다.
networklink
   이 문자열 필드는 KML NetworkLink의 `<href> <https://developers.google.com/kml/documentation/kmlreference#href>`_ 태그의 href 요소에 매핑됩니다.
   LIBKML_NETWORKLINK_FIELD 환경 변수로 OGR 필드의 이름을 변경할 수 있습니다.
networklink_refreshvisibility
   이 정수형 필드는 KML NetworkLink의 `<refreshVisibility> <https://developers.google.com/kml/documentation/kmlreference#refreshvisibility>`_ 태그에 매핑됩니다.
   LIBKML_NETWORKLINK_REFRESHVISIBILITY_FIELD 환경 변수로 OGR 필드의 이름을 변경할 수 있습니다.
networklink_flytoview
   이 정수형 필드는 KML NetworkLink의 `<flyToView> <https://developers.google.com/kml/documentation/kmlreference#flytoview>`_ 태그에 매핑됩니다.
   LIBKML_NETWORKLINK_FLYTOVIEW_FIELD 환경 변수로 OGR 필드의 이름을 변경할 수 있습니다.
networklink_refreshmode
   이 문자열 필드는 KML NetworkLink의 `<refreshMode> <https://developers.google.com/kml/documentation/kmlreference#refreshmode>`_ 태그에 매핑됩니다.
   LIBKML_NETWORKLINK_REFRESHMODE_FIELD 환경 변수로 OGR 필드의 이름을 변경할 수 있습니다.
networklink_refreshinterval
   이 실수형 필드는 KML NetworkLink의 `<refreshInterval> <https://developers.google.com/kml/documentation/kmlreference#refreshinterval>`_ 태그에 매핑됩니다.
   LIBKML_NETWORKLINK_REFRESHINTERVAL_FIELD 환경 변수로 OGR 필드의 이름을 변경할 수 있습니다.
networklink_viewrefreshmode
   이 문자열 필드는 KML NetworkLink의 `<viewRefreshMode> <https://developers.google.com/kml/documentation/kmlreference#viewrefreshmode>`_ 태그에 매핑됩니다.
   LIBKML_NETWORKLINK_VIEWREFRESHMODE_FIELD 환경 변수로 OGR 필드의 이름을 변경할 수 있습니다.
networklink_viewrefreshtime
   이 실수형 필드는 KML NetworkLink의 `<viewRefreshTime> <https://developers.google.com/kml/documentation/kmlreference#viewrefreshtime>`_ 태그에 매핑됩니다.
   LIBKML_NETWORKLINK_VIEWREFRESHTIME_FIELD 환경 변수로 OGR 필드의 이름을 변경할 수 있습니다.
networklink_viewboundscale
   이 실수형 필드는 KML NetworkLink의 `<viewBoundScale> <https://developers.google.com/kml/documentation/kmlreference#viewboundscale>`_ 태그에 매핑됩니다.
   LIBKML_NETWORKLINK_VIEWBOUNDSCALE_FIELD 환경 변수로 OGR 필드의 이름을 변경할 수 있습니다.
networklink_viewformat
   이 문자열 필드는 KML NetworkLink의 `<viewFormat> <https://developers.google.com/kml/documentation/kmlreference#viewformat>`_ 태그에 매핑됩니다.
   LIBKML_NETWORKLINK_VIEWFORMAT_FIELD 환경 변수로 OGR 필드의 이름을 변경할 수 있습니다.
networklink_httpquery
   이 문자열 필드는 KML NetworkLink의 `<httpQuery> <https://developers.google.com/kml/documentation/kmlreference#httpquery>`_ 태그에 매핑됩니다.
   LIBKML_NETWORKLINK_HTTPQUERY_FIELD 환경 변수로 OGR 필드의 이름을 변경할 수 있습니다.
camera_longitude
   이 실수형 필드는 KML `<Camera> <https://developers.google.com/kml/documentation/kmlreference#camera>`_ 의 `<longitude> <https://developers.google.com/kml/documentation/kmlreference#longitude>`_ 태그에 매핑됩니다.
   LIBKML_CACameraMERA_LONGITUDE_FIELD 환경 변수로 OGR 필드의 이름을 변경할 수 있습니다.
camera_latitude
   이 실수형 필드는 KML `<Camera> <https://developers.google.com/kml/documentation/kmlreference#camera>`_ 의 `<latitude> <https://developers.google.com/kml/documentation/kmlreference#latitude>`_ 태그에 매핑됩니다.
   LIBKML_CAMERA_LATITUDE_FIELD 환경 변수로 OGR 필드의 이름을 변경할 수 있습니다.
camera_altitude
   이 실수형 필드는 KML `<Camera> <https://developers.google.com/kml/documentation/kmlreference#camera>`_ 의 `<altitude> <https://developers.google.com/kml/documentation/kmlreference#altitude>`_ 태그에 매핑됩니다.
   LIBKML_CAMERA_ALTITUDE_FIELD 환경 변수로 OGR 필드의 이름을 변경할 수 있습니다.
camera_altitudemode
   이 실수형 필드는 KML `<Camera> <https://developers.google.com/kml/documentation/kmlreference#camera>`_ 의 `<altitudeMode> <https://developers.google.com/kml/documentation/kmlreference#altitudemode>`_ 태그에 매핑됩니다.
   LIBKML_CAMERA_ALTITUDEMODE_FIELD 환경 변수로 OGR 필드의 이름을 변경할 수 있습니다.
photooverlay
   이 문자열 필드는 KML `<PhotoOverlay> <https://developers.google.com/kml/documentation/kmlreference#photooverlay>`_ 의 `<href> <https://developers.google.com/kml/documentation/kmlreference#href>`_ 태그의 <href> 요소에 매핑됩니다.
   LIBKML_PHOTOOVERLAY_FIELD 환경 변수로 OGR 필드의 이름을 변경할 수 있습니다.
leftfov
   이 실수형 필드는 KML `<PhotoOverlay> <https://developers.google.com/kml/documentation/kmlreference#photooverlay>`_ 의 `<LeftFov> <https://developers.google.com/kml/documentation/kmlreference#leftfov>`_ 태그에 매핑됩니다.
   LIBKML_LEFTFOV_FIELD 환경 변수로 OGR 필드의 이름을 변경할 수 있습니다.
rightfov
   이 실수형 필드는 KML `<PhotoOverlay> <https://developers.google.com/kml/documentation/kmlreference#photooverlay>`_ 의 `<RightFov> <https://developers.google.com/kml/documentation/kmlreference#rightfov>`_ 태그에 매핑됩니다.
   LIBKML_RightFOV_FIELD 환경 변수로 OGR 필드의 이름을 변경할 수 있습니다.
bottomfov
   이 실수형 필드는 KML `<PhotoOverlay> <https://developers.google.com/kml/documentation/kmlreference#photooverlay>`_ 의 `<BottomFov> <https://developers.google.com/kml/documentation/kmlreference#bottomfov>`_ 태그에 매핑됩니다.
   LIBKML_BOTTOMTFOV_FIELD 환경 변수로 OGR 필드의 이름을 변경할 수 있습니다.
topfov
   이 실수형 필드는 KML `<PhotoOverlay> <https://developers.google.com/kml/documentation/kmlreference#photooverlay>`_ 의 `<TopFov> <https://developers.google.com/kml/documentation/kmlreference#topfov>`_ 태그에 매핑됩니다.
   LIBKML_TOPFOV_FIELD 환경 변수로 OGR 필드의 이름을 변경할 수 있습니다.
near
   이 실수형 필드는 KML `<PhotoOverlay> <https://developers.google.com/kml/documentation/kmlreference#photooverlay>`_ 의 `<Near> <https://developers.google.com/kml/documentation/kmlreference#leftfov>`_ 태그에 매핑됩니다.
   LIBKML_NEAR_FIELD 환경 변수로 OGR 필드의 이름을 변경할 수 있습니다.
shape
   이 문자열 필드는 KML `<PhotoOverlay> <https://developers.google.com/kml/documentation/kmlreference#photooverlay>`_ 의 `<shape> <https://developers.google.com/kml/documentation/kmlreference#shape>`_ 태그에 매핑됩니다.
   LIBKML_SHAPE_FIELD 환경 변수로 OGR 필드의 이름을 변경할 수 있습니다.
   variable .
imagepyramid_tilesize
   이 정수형 필드는 KML `<ImagePyramid> <https://developers.google.com/kml/documentation/kmlreference#imagepyramid>`_ 의 `<tileSize> <https://developers.google.com/kml/documentation/kmlreference#tilesize>`_ 태그에 매핑됩니다.
   LIBKML_IMAGEPYRAMID_TILESIZE 환경 변수로 OGR 필드의 이름을 변경할 수 있습니다.
imagepyramid_maxwidth
   이 정수형 필드는 KML `<ImagePyramid> <https://developers.google.com/kml/documentation/kmlreference#imagepyramid>`_ 의 `<maxWidth> <https://developers.google.com/kml/documentation/kmlreference#maxwidth>`_ 태그에 매핑됩니다.
   LIBKML_IMAGEPYRAMID_MAXWIDTH 환경 변수로 OGR 필드의 이름을 변경할 수 있습니다.
imagepyramid_maxheight
   이 정수형 필드는 KML `<ImagePyramid> <https://developers.google.com/kml/documentation/kmlreference#imagepyramid>`_ 의 `<maxHeight> <https://developers.google.com/kml/documentation/kmlreference#maxheight>`_ 태그에 매핑됩니다.
   LIBKML_IMAGEPYRAMID_MAXHEIGHT 환경 변수로 OGR 필드의 이름을 변경할 수 있습니다.
imagepyramid_gridorigin
   이 문자열 필드는 KML `<ImagePyramid> <https://developers.google.com/kml/documentation/kmlreference#imagepyramid>`_ 의 `<gridOrigin> <https://developers.google.com/kml/documentation/kmlreference#maxheight>`_ 태그에 매핑됩니다.
   LIBKML_IMAGEPYRAMID_GRIDORIGIN 환경 변수로 OGR 필드의 이름을 변경할 수 있습니다.
OGR_STYLE
   이 문자열 필드는 피처 스타일 문자열에 매핑되며, 피처에 설정된 스타일 문자열이 없는 경우 OGR가 이 필드를 읽어옵니다.

도형
--------

:cpp:class:`OGRGeometry` 클래스를 KML 도형으로 변환하는 것은 두어 가지 예외를 제외하면 매우 간단한 편입니다.

-  포인트를 `<Point> <https://developers.google.com/kml/documentation/kmlreference#point>`_ 로 (heading 그리고/또는 tilt 그리고/또는 roll 필드명이 존재하는 경우 `Camera <https://developers.google.com/kml/documentation/kmlreference#camera>`_ 객체를 생성할 것입니다.)

-  라인스트링을 `<LineString> <https://developers.google.com/kml/documentation/kmlreference#linestring>`_ 으로

-  선형 고리(LinearRing)를 `<LinearRing> <https://developers.google.com/kml/documentation/kmlreference#linearring>`_ 으로

-  폴리곤을 `<Polygon> <https://developers.google.com/kml/documentation/kmlreference#polygon>`_ 으로

OGR에서 폴리곤은 선형 고리 배열을 담고 있으며, 이때 첫 번째 고리가 외곽 고리(outer ring)입니다. KML은 이 두 가지 고리를 구분하기 위한 `<outerBoundaryIs> <https://developers.google.com/kml/documentation/kmlreference#outerboundaryis>`_ 및 `<innerBoundaryIs> <https://developers.google.com/kml/documentation/kmlreference#innerboundaryis>`_ 태그를 가지고 있습니다.

OGR는 다중 도형 유형 몇 개를 가지고 있습니다:

-  도형 집합(GeometryCollection)
-  멀티폴리곤(MultiPolygon)
-  멀티포인트(MultiPoint)
-  멀티라인스트링(MultiLineString)

가능한 경우, OGR는 `<MultiGeometry> <https://developers.google.com/kml/documentation/kmlreference#multigeometry>`_ 를 더 정밀한 OGR 도형 유형으로 (멀티포인트, 멀티라인스트링 또는 멀티폴리곤으로) 매핑하려 시도할 것입니다. 혼합된 콘텐츠의 경우 기본값은 도형 집합입니다.

KML 도형이 날짜 변경선을 걸치는 경우가 있는데, QGIS 또는 MapServer 같은 응용 프로그램에서 이런 도형은 지구 전체를 한바퀴 도는 수평 라인을 생성할 것입니다. LIBKML_WRAPDATELINE 환경 변수를 YES로 설정하면 LIBKML 드라이버가 이런 도형을 읽어올 때 해당 도형을 날짜 변경선으로 분할할 것입니다.

VSI 가상 파일 시스템 API 지원
-----------------------------------

이 드라이버는 VSI 가상 파일 시스템 API가 관리하는 파일의 읽기 및 쓰기를 지원합니다. VSI 가상 파일 시스템 API가 관리하는 파일에는 "정규" 파일은 물론 /vsizip/ (읽기-쓰기) , /vsigzip/ (읽기-쓰기) , /vsicurl/ (읽기 전용) 도메인에 있는 파일도 포함됩니다.

/dev/stdout 또는 /vsistdout/ 에 쓰기도 지원합니다.

예시
-------

다음 배시(bash) 스크립트는 :ref:`csv <vector.csv>` 파일과 :ref:`vrt <vector.vrt>` 파일을 생성한 다음 :ref:`ogr2ogr` 유틸리티를 이용해서 그 파일들을 타임스탬프와 스타일 정보를 가진 KML 파일로 변환할 것입니다:

::

   #!/bin/bash
   # Copyright (c) 2010, Brian Case
   #
   # Permission is hereby granted, free of charge, to any person obtaining a
   # copy of this software and associated documentation files (the "Software"),
   # to deal in the Software without restriction, including without limitation
   # the rights to use, copy, modify, merge, publish, distribute, sublicense,
   # and/or sell copies of the Software, and to permit persons to whom the
   # Software is furnished to do so, subject to the following conditions:
   #
   # The above copyright notice and this permission notice shall be included
   # in all copies or substantial portions of the Software.
   #
   # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
   # OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
   # FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
   # THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
   # LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
   # FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
   # DEALINGS IN THE SOFTWARE.


   icon="http://maps.google.com/mapfiles/kml/shapes/shaded_dot.png"
   rgba33="#FF9900"
   rgba70="#FFFF00"
   rgba150="#00FF00"
   rgba300="#0000FF"
   rgba500="#9900FF"
   rgba800="#FF0000"

   function docsv {

       IFS=','

       while read Date Time Lat Lon Mag Dep
       do
           ts=$(echo $Date | sed 's:/:-:g')T${Time%%.*}Z
           rgba=""

           if [[ $rgba == "" ]] && [[ $Dep -lt 33 ]]
           then
               rgba=$rgba33
           fi

           if [[ $rgba == "" ]] && [[ $Dep -lt 70 ]]
           then
               rgba=$rgba70
           fi

           if [[ $rgba == "" ]] && [[ $Dep -lt 150 ]]
           then
               rgba=$rgba150
           fi

           if [[ $rgba == "" ]] && [[ $Dep -lt 300 ]]
           then
               rgba=$rgba300
           fi

           if [[ $rgba == "" ]] && [[ $Dep -lt 500 ]]
           then
               rgba=$rgba500
           fi

           if [[ $rgba == "" ]]
           then
               rgba=$rgba800
           fi



           style="\"SYMBOL(s:$Mag,id:\"\"$icon\"\",c:$rgba)\""

           echo $Date,$Time,$Lat,$Lon,$Mag,$Dep,$ts,"$style"
       done

   }


   wget http://neic.usgs.gov/neis/gis/qed.asc -O /dev/stdout |\
    tail -n +2 > qed.asc

   echo Date,TimeUTC,Latitude,Longitude,Magnitude,Depth,timestamp,OGR_STYLE > qed.csv

   docsv < qed.asc >> qed.csv

   cat > qed.vrt << EOF
   <OGRVRTDataSource>
       <OGRVRTLayer name="qed">
           <SrcDataSource>qed.csv</SrcDataSource>
           <GeometryType>wkbPoint</GeometryType>
           <LayerSRS>WGS84</LayerSRS>
           <GeometryField encoding="PointFromColumns" x="Longitude" y="Latitude"/>
       </OGRVRTLayer>
   </OGRVRTDataSource>

   EOF

   ogr2ogr -f libkml qed.kml qed.vrt

