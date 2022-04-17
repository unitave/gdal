.. _vector.ngw:

NGW -- NextGIS 웹
==================

.. versionadded:: 2.4

.. shortname:: NGW

.. build_dependencies:: libcurl

NextGIS 웹은 서버 GIS로, 지리 데이터(geodata)를 저장하고 편집할 수 있으며 웹브라우저에 맵을 출력할 수 있습니다. 또한 NextGIS 웹은 다른 NextGIS 소프트웨어와 지리 데이터를 공유할 수 있습니다.

NextGIS 웹은 다음과 같은 기능을 가지고 있습니다:

-  웹브라우저에 (서로 다른 레이어 및 스타일을 가진 서로 다른) 맵을 출력하기
-  유연한 권한 관리
-  PostGIS로부터 지리 데이터 불러오기 또는 GIS 포맷(ESRI Shapefile, GeoJSON 또는 GeoTIFF)로부터 가져오기
-  다음 포맷에 있는 벡터 지리 데이터 불러오기: GeoJSON, CSV, ESRI Shapefile, Mapinfo 탭(tab)
-  QGIS 프로젝트로부터 맵 스타일 가져오기 또는 직접 설정하기
-  TMS, WMS, MVT, WFS 서버 역할
-  WMS 클라이언트 역할
-  사용자가 웹 인터페이스 또는 WFS-T 프로토콜을 통해 레코드에 사진을 추가하고 레코드 속성을 변경할 수 있습니다.

NextGIS 웹은 오픈소스 소프트웨어입니다. (GPL 버전 2 이상의 사용 허가, `GNU 일반 공중 사용 허가서 버전 2 <https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html>`_ 참조)

드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

드라이버
------

NGW 드라이버는 NextGIS 웹 REST API를 구현하는 서비스에 접속할 수 있습니다.
이 드라이버를 사용하려면 GDAL이 cURL을 지원해야 합니다. 이 드라이버는 읽기 및 쓰기 작업을 지원합니다.

데이터셋 이름 문법
-------------------

NGW 데이터소스를 열 수 있는 최소한의 문법은 다음과 같습니다:

::

   NGW:[NextGIS Web URL][/resource/][resource identifier]

-  **NextGIS Web URL** 은 nextgis.com 클라우드 서비스를 (예를 들어 https://demo.nextgis.com 을) 가리키는 URL일 수도 있습니다. 또는 포트 번호와 추가 경로를 포함하는 (예를 들면 http://192.168.1.1:8000/test 같은) 다른 URL일 수도 있습니다.
-  **resource** 는 리소스 식별자를 URL 나머지 부분과 구분하는 필수 키워드입니다.
-  **resource identifier** 는 0 이상의 양의 숫자입니다. 리소스 그룹, 벡터, PostGIS 또는 래스터 레이어, 스타일일 수도 있습니다.

모든 벡터 레이어, PostGIS, 래스터 레이어, 스타일은 식별자가 리소스 그룹인 경우 하위 리소스로 목록화됩니다. 그렇지 않은 경우 각각 개별 레이어가 될 것입니다.

환경설정 옵션
---------------------

다음 :ref:`환경설정 옵션들 <configoptions>` 을 사용할 수 있습니다:

-  :decl_configoption:`NGW_USERPWD`: User name and password separated with colon.
   Optional and can be set using open options.
-  :decl_configoption:`NGW_BATCH_SIZE`: Size of feature insert and update operations
   cache before send to server. If batch size is -1 batch mode is
   disabled. Delete operation will execute immediately.
-  :decl_configoption:`NGW_PAGE_SIZE`: If supported by server, fetch features from remote
   server will use paging. The -1 value disables paging even it
   supported by server.
-  :decl_configoption:`NGW_NATIVE_DATA`: Whether to store the json *extensions* key in
   feature native data.
-  :decl_configoption:`NGW_JSON_DEPTH`: The depth of json response that can be parsed. If
   depth is greater than this value, parse error occurs.
-  :decl_configoption:`NGW_EXTENSIONS`: Comma separated extensions list. Available values are 
   `description` and `attachment`. This needed to fill native data.

Authentication
--------------

Any operations (read, write, get metadata, change properties, etc.) may
require an authenticated access. Authenticated access is obtained by
specifying user name and password in open, create or configuration
options.

Feature
-------

If the NATIVE_DATA open option is set to YES, the *extensions* json
object will store as a serialized json object in the NativeData
property of the OGRFeature object (and "application/json" in the
NativeMediaType property). If writing OGRFeature has NativeMediaType property
set to "application/json" and its NativeData property set to serialized json
object the new NGW feature *extensions* json object will fill from this json
object.

Extensions json object structure see in `NextGIS Web API
documentation <http://docs.nextgis.comu/docs_ngweb_dev/doc/developer/resource.html#feature>`__

Geometry
--------

NextGIS Web supports only one geometry column. Default spatial reference
is Web Mercator (EPSG:3857). The following geometry types are available:

-  POINT
-  LINESTRING
-  POLYGON
-  MULTIPOINT
-  MULTILINESTRING
-  MULTIPOLYGON

Geometry with Z value also supported.

Field data types
----------------

NextWeb supports only following field types:

-  OFTInteger
-  OFTInteger64
-  OFTReal
-  OFTString
-  OFTDate
-  OFTTime
-  OFTDateTime

Paging
------

Features can retrieved from NextGIS Web by chunks if supported by server
(available since NextGIS Web 3.1). The chunk size can be altered with
the :decl_configoption:`NGW_PAGE_SIZE` configuration option or PAGE_SIZE open option.

Write support
-------------

Datasource and layers creation and deletion is possible. Write support
is only enabled when the datasource is opened in update mode and user
has appropriate permissions. Vector and PostGIS layers insert and update operations
are cached if BATCH_SIZE is greater 0. Delete operation executes
immediately.

Open options
------------

The following open options are available:

-  USERPWD - Username and password, separated by colon.
-  PAGE_SIZE=-1 - Limit feature count while fetching from server.
   Default value is -1 - no limit.
-  BATCH_SIZE=-1 - Size of feature insert and update operations cache
   before send to server. If batch size is -1 batch mode is disabled.
   Default value is -1.
-  NATIVE_DATA=NO - Whether to store the json *extensions* key in
   feature native data. Default value is NO.
-  JSON_DEPTH=32 - The depth of json response that can be parsed. If
   depth is greater than this value, parse error occurs.
-  EXTENSIONS - Comma separated extensions list. Available values are 
   `description` and `attachment`. This needed to fill native data.

Dataset creation options
------------------------

The following dataset/datasource creation options are available:

-  KEY - Key value. Must be unique in whole NextGIS Web instance.
   Optional.
-  DESCRIPTION - Resource description. Optional.
-  USERPWD - Username and password, separated by colon.
-  PAGE_SIZE=-1 - Limit feature count while fetching from server.
   Default value is -1 - no limit.
-  BATCH_SIZE=-1 - Size of feature insert and update operations cache
   before send to server. If batch size is -1 batch mode is disable.
   Default value is -1.
-  NATIVE_DATA=NO - Whether to store the json *extensions* key in
   feature native data. Default value is NO.
-  JSON_DEPTH=32 - The depth of json response that can be parsed. If
   depth is greater than this value, parse error occurs.
-  EXTENSIONS - Comma separated extensions list. Available values are 
   `description` and `attachment`. This needed to fill native data.

Layer creation options
----------------------

The following layer creation options are available:

-  OVERWRITE - Whether to overwrite an existing table with the layer
   name to be created. The resource will delete and new one will
   created. This leads that resource identifier will change. Defaults to
   NO. Optional.
-  KEY - Key value. Must be unique in whole NextGIS Web instance.
   Optional.
-  DESCRIPTION - Resource description. Optional.

Metadata
--------

NextGIS Web metadata are supported in datasource, vector, PostGIS,
raster layers and styles. Metadata are stored at specific domain "NGW".
NextGIS Web supported metadata are strings and numbers. Metadata keys
with decimal numbers will have suffix **.d** and for real numbers -
**.f**. To create new metadata item, add new key=value pair in NGW
domain using the *SetMetadataItem* function and appropriate suffix. During
transferring to NextGIS Web, suffix will be omitted. You must ensure
that numbers correctly transform from string to number.

Resource description and key map to appropriate *description* and
*keyname* metadata items in default domain. Changing those metadata
items will cause an update of resource properties.

Resource creation date, type and parent identifier map to appropriate
read-only metadata items *creation_date*, *resource_type* and
*parent_id* in default domain.

Vector layer field properties (alias, identifier, label field, grid
visibility) map to layer metadata the following way:

-  field alias -> FIELD_{field number}_ALIAS (for example FIELD_0_ALIAS)
-  identifier -> FIELD_{field number}_ID (for example FIELD_0_ID)
-  label field -> FIELD_{field number}_LABEL_FIELD (for example
   FIELD_0_LABEL_FIELD)
-  grid visibility -> FIELD_{field number}_GRID_VISIBILITY (for example
   FIELD_0_GRID_VISIBILITY)

Starting from GDAL 3.3 field alias can be set/get via `SetAlternativeName`
and `GetAlternativeNameRef`.

Filters
-------

Vector and PostGIS layers support SetIgnoredFields method. When this method
executes any cached features will be freed.

Vector and PostGIS layers support SetAttributeFilter and
SetSpatialFilter methods. The attribute filter will evaluate at server side
if condition is one of following comparison operators:

 - greater (>)
 - lower (<)
 - greater or equal (>=)
 - lower or equal (<=)
 - equal (=)
 - not equal (!=)
 - LIKE SQL statement (for strings compare)
 - ILIKE SQL statement (for strings compare)

Also only AND operator without brackets supported between comparison. For example,

::

   FIELD_1 = 'Value 1'

::

   FIELD_1 = 'Value 1' AND FIELD_2 > Value 2

In other cases attribute filter will evaluate on client side.

You can set attribute filter using NextGIS Web native format. For
example,

::

   NGW:fld_FIELD_1=Value 1&fld_FIELD_2__gt=Value 2

Don't forget to add 'NGW:' perefix to where clause and 'fld\_' prefix to
field name.

Dataset supports ExecuteSQL method. Only the following queries are
supported:

-  DELLAYER: layer_name; - delete layer with layer_name.
-  DELETE FROM layer_name; - delete any features from layer with
   layer_name.
-  DROP TABLE layer_name; - delete layer with layer_name.
-  ALTER TABLE src_layer RENAME TO dst_layer; - rename layer.
-  SELECT field_1,field_2 FROM src_layer WHERE field_1 = 'Value 1' AND
   field_2 = 'Value 2';

In SELECT statement field list or asterisk can be provided. The WHERE
clause has same limitations as SetAttributeFilter method input.

Examples
--------

Read datasource contents (1730 is resource group identifier):

::

       ogrinfo -ro NGW:https://demo.nextgis.com/resource/1730

Read layer details (`1730` is resource group identifier, `Parks` is vecror layer
name):

::

       ogrinfo -ro -so NGW:https://demo.nextgis.com/resource/1730 Parks

Creating and populating a vector layer from a shapefile in existing resource
group with identifier 1730. New vector layer name will be "some new name":

::

       ogr2ogr -f NGW -nln "some new name" -update -doo "BATCH_SIZE=100" -t_srs EPSG:3857 "NGW:https://demo.nextgis.com/resource/1730" myshapefile.shp

.. warning::
   The `-update` key is mandatory, otherwise the destination datasource will
   silently delete. The `-t_srs EPSG:3857` key is mandatory because vector
   layers spatial reference in NextGIS Web can be only in EPSG:3857.

.. note::
   The `-doo "BATCH_SIZE=100"` key is recommended for speed up feature transferring.

Creating and populating a vector layer from a shapefile in new resource
group with name "new group" and parent identifier 1730. New vector layer name
will be "some new name":

::

       ogr2ogr -f NGW -nln "Название на русском языке" -dsco "BATCH_SIZE=100" -t_srs EPSG:3857 "NGW:https://demo.nextgis.com/resource/1730/new group" myshapefile.shp

See also
--------

-  :ref:`Raster side of the driver <raster.ngw>`
-  `NextGIS Web
   documentation <http://docs.nextgis.com/docs_ngweb/source/toc.html>`__
-  `NextGIS Web for
   developers <http://docs.nextgis.com/docs_ngweb_dev/doc/toc.html>`__
