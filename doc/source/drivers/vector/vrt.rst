.. _vector.vrt:

VRT -- 가상 포맷
=====================

.. shortname:: VRT

.. built_in_by_default::

OGR 가상 포맷(Virtual Format)은 XML 제어 파일에 지정된 기준을 기반으로 다른 드라이버로부터 읽어온 객체를 변환(transform)하는 드라이버입니다. 속성 열에 공간 정보를 가지고 있는 평탄(flat) 테이블로부터 공간 레이어를 파생시키기 위해 주로 사용합니다. 좌표계 정보를 데이터소스와 연결하기 위해, 단일 데이터소스에 다른 데이터소스로부터 나온 레이어를 병합시키기 위해, 또는 그저 비(非) 파일(non-file) 지향 데이터소스에 접근하기 위한 앵커(anchor) 파일을 제공하기 위해 사용할 수도 있습니다.

현재 가상 파일은 일반적으로 사용자가 직접 작성해서 준비해야 합니다.

드라이버 케이퍼빌리티
-------------------

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::

생성 문제점
---------------

다음 조건들을 만족하는 경우, VRT 데이터셋의 레이어 상에서 CreateFeature(), SetFeature() 및 DeleteFeature() 작업을 지원합니다:

-  VRT 데이터셋을 업데이트 모드로 연다.
-  기저 소스 레이어가 해당 작업을 지원한다.
-  (*SrcSQL* 요소가 아니라) *SrcLayer* 요소를 사용한다.
-  VRT 객체의 FID가 소스 객체의 FID와 동일하다. 다시 말해 *FID* 요소를 지정하지 않는다.

가상 파일 포맷
-------------------

XML 제어 파일의 루트 요소는 **OGRVRTDataSource** 입니다. 이 요소는 가상 데이터소스에 있는 각 레이어의 **OGRVRTLayer** (또는 **OGRVRTWarpedLayer** 또는 **OGRVRTUnionLayer**) 하위 요소 및 **Metadata** 요소를 가지고 있습니다.

`OGR VRT 포맷의 XML 스키마 <https://github.com/OSGeo/gdal/blob/master/data/ogrvrt.xsd>`_ 를 사용할 수 있습니다. GDAL에 libXML2 지원을 환경설정했다면, VRT 문서를 검증하기 위해 이 스키마를 사용할 것입니다. 스키마를 준수하지 않은 경우 경고로만 리포트할 것입니다. :decl_configoption:`GDAL_XML_VALIDATION` 환경설정 옵션을 NO로 설정하면 이 검증 작업을 비활성화시킬 수 있습니다.

메타데이터 요소
++++++++++++++++

-  **Metadata** (선택적):
   이 요소는 데이터셋 전체와 연결된 메타데이터 이름/값 쌍들의 목록을 담고 있습니다. 이 요소는 <MDI>(metadata item) 하위 요소를 가지고 있는데, 이 하위 요소는 "key" 속성과 그 값을 데이터로 가지고 있습니다. Metadata 요소는 여러 번 반복될 수 있는데 이 경우 반드시 메타데이터 도메인의 이름을 나타내는 "domain" 속성과 함께 쓰여야만 합니다.

OGRVRTLayer 요소
+++++++++++++++++++

**OGRVRTLayer** 요소는 레이어 이름을 가진 **name** 속성을 가져야 하며, 다음 하위 요소들을 가질 수도 있습니다:

-  **SrcDataSource** (필수):
   이 요소의 값은 이 레이어를 파생시켜 올 데이터소스의 이름입니다. 이 요소는 기본값이 0인 **relativeToVRT** 속성을 가질 수도 있는데, 이 속성이 1이라면 소스 데이터소스를 가상 파일에 상대적인 것으로 해석해야 한다는 뜻입니다. 소스 데이터소스는 ODBC, CSV 등등을 포함, OGR가 지원하는 모든 데이터셋일 수 있습니다. 이 요소는 데이터소스를 공유 모드로 열어야 할지 여부를 제어하는 **shared** 속성을 가질 수도 있습니다. 이 속성의 기본값은 SrcLayer 사용 시 OFF, SrcSQL 사용 시 ON입니다.

-  **OpenOptions** (선택적):
   이 요소는 열기 옵션 여러 개를 ``<OOI key="key_name">value_name</OOI>`` 형식의 하위 요소들의 목록을 가질 수도 있습니다.

-  **Metadata** (선택적):
   이 요소는 레이어 전체와 연결된 메타데이터 이름/값 쌍들의 목록을 담고 있습니다. 이 요소는 <MDI>(metadata item) 하위 요소를 가지고 있는데, 이 하위 요소는 "key" 속성과 그 값을 데이터로 가지고 있습니다. Metadata 요소는 여러 번 반복될 수 있는데 이 경우 반드시 메타데이터 도메인의 이름을 나타내는 "domain" 속성과 함께 쓰여야만 합니다.

-  **SrcLayer** (선택적):
   이 요소의 값은 이 가상 레이어를 파생시켜 와야 할 소스 데이터소스에서의 레이어 이름입니다. 이 요소를 지정하지 않는 경우 SrcSQL 요소를 지정해야만 합니다.

-  **SrcSQL** (선택적):
   원하는 레이어 결과물을 생성하기 위해 실행할 SQL 선언문입니다. 선언문으로 결과물을 파생시키려면 SrcLayer 요소 대신 이 요소를 지정해야 합니다. SQL 파생 레이어에는 몇몇 제한이 적용될 수도 있습니다. SrcSQL 요소 상에 선택적인 **dialect** 속성을 지정할 수 있습니다. 이 속성은 어떤 SQL "방언"을 사용해야 할지를 지정합니다. 현재 지정할 수 있는 값은 :ref:`OGR SQL <ogr_sql_dialect>` 또는 :ref:`SQLITE <sql_sqlite_dialect>` 입니다. 이 속성을 지정하지 않는 경우, 데이터소스의 기본 방언을 사용할 것입니다.

-  **FID** (선택적):
   객체의 FID를 파생시켜 와야 할 소스 속성 열의 이름입니다. 이 요소를 지정하지 않는 경우, 소스 객체의 FID를 직접 사용할 것입니다.

   GDAL 2.4 이상 버전의 논리: 다음과 같은 서로 다른 상황이 있을 수 있습니다:

   -  .. code-block:: XML

         <FID>source_field_name</FID>

      FID 열을 source_field_name 소스 필드의 내용을 가진 source_field_name으로 리포트할 것입니다.

   -  .. code-block:: XML

         <FID name="dest_field_name">source_field_name</FID>

      FID 열을 source_field_name 소스 필드의 내용을 가진 dest_field_name으로 리포트할 것입니다. dest_field_name을 빈 문자열로 설정할 수도 있습니다.

   -  .. code-block:: XML

         <FID />

      FID 열을 리포트하지 않습니다. VRT 객체의 FID 값은 소스 객체의 FID 값입니다.

   -  .. code-block:: XML

         <FID name="dest_field_name"/>

      FID 열을 암묵적인 소스 FID 열의 내용을 가진 dest_field_name으로 리포트할 것입니다. VRT 객체의 FID 값은 소스 객체의 FID 값입니다.

   GDAL 2.4 미만 버전의 논리: FID 열을 정규 필드로도 리포트하는 경우 레이어가 FID 열 이름만 리포트할 것입니다. FID 열 이름을 항상 리포트하도록 FID 요소에 "name" 속성을 지정할 수 있습니다.

-  **Style** (선택적):
   객체 스타일을 파생시켜 와야 할 속성 열의 이름입니다. 이 요소를 지정하지 않는 경우, 소스 객체의 스타일을 직접 사용할 것입니다.

-  **GeometryType** (선택적):
   레이어에 할당할 도형 유형입니다. 이 요소를 지정하지 않는 경우, 소스 레이어로부터 가져올 것입니다. "wkbNone", "wkbUnknown", "wkbPoint", "wkbLineString", "wkbPolygon", "wkbMultiPoint", "wkbMultiLineString", "wkbMultiPolygon", 또는 "wkbGeometryCollection" 가운데 하나로 지정해야 합니다. Z 좌표를 포함하고 있다고 표시하기 위해 뒤에 "25D"를 선택적으로 붙일 수도 있습니다. 기본값은 어떤 도형 유형도 될 수 있는 "wkbUnknown"입니다.

-  **LayerSRS** (선택적):
   이 요소의 값은 레이어에 사용할 공간 좌표계입니다. 이 요소를 지정하지 않는 경우, 소스 레이어로부터 상속받습니다. 이 요소의 값은 WKT일 수도 있고 또는 OGRSpatialReference::SetUserInput() 메소드가 입력받을 수 있는 다른 모든 입력물일 수도 있습니다. NULL로 설정하면, 레이어에 어떤 공간 좌표계도 사용하지 않을 것입니다.

-  **GeometryField** (선택적):
   이 요소를 사용해서 객체의 도형을 어떻게 파생시켜야 할 것인지 정의합니다.

   이 요소를 지정하지 않는 경우, 소스 객체의 도형을 직접 복사합니다. 도형 유형의 인코딩은 **encoding** 속성으로 나타냅니다. 이 속성의 값은 "WKT", "WKB" 또는 "PointFromColumns" 가운데 하나일 수도 있습니다.

   인코딩이 "WKT" 또는 "WKB"이면 **field** 속성이 WKT 또는 WKB 도형을 담고 있는 필드의 이름을 가질 것입니다.
  
   인코딩이 "PointFromColumns"이면 **x**, **y**, **z** 및 **m** 속성이 X, Y, Z 및 M 좌표에 사용되는 열들의 이름을 가질 것입니다. **z** 및 **m** 속성은 선택적입니다. (OGR 2.1.1 이상 버전에서만 m을 지원합니다.)

   선택적인 **reportSrcColumn** 속성을 사용해서 소스 도형 필드를 (**field**, **x**, **y**, **z**, **m** 속성에 설정된 필드를) VRT 레이어의 필드로 리포트해야 할지 여부를 지정할 수 있습니다. 기본값은 TRUE입니다. 이 속성을 FALSE로 설정하면, 소스 도형 필드만 사용해서 VRT 레이어의 객체의 도형을 작성할 것입니다.

   도형 필드 여러 개를 생성하기 위해 GeometryField 요소를 필요한 만큼 여러 번 반복할 수 있습니다. 이 요소는 VRT 도형 필드 이름을 정의하는 데 이용할 (권장) **name** 속성을 가질 수 있습니다. **encoding** 속성을 지정하지 않은 경우, **field** 속성을 이용해서 소스 레이어에서 대응하는 도형 필드 이름을 판단할 것입니다. **encoding** 도 **field** 도 지정하지 않는 경우, 소스 도형 필드의 이름이 **name** 속성의 값이라고 가정합니다.

   선택적인 **nullable** 속성을 사용해서 도형 필드가 NULL일 수 있는지 여부를 지정할 수 있습니다. 이 속성의 기본값은 "true"입니다.

   도형 필드를 여러 개 사용하는 경우, **GeometryField** 의 다음 하위 요소들을 정의해서 도형 유형, 공간 좌표계, 소스 영역 또는 범위를 명확하게 설정할 수 있습니다.

   *  **GeometryType** (선택적):
      OGRVRTLayer 수준 **GeometryType** 요소와 동일한 문법입니다.
   *  **SRS** (선택적):
      OGRVRTLayer 수준 **LayerSRS** 요소와 동일한 문법입니다. (SRS와 LayerSRS로 이름이 다르다는 사실을 기억하십시오.)
   *  **SrcRegion** (선택적):
      OGRVRTLayer 수준 **SrcRegion** 요소와 동일한 문법입니다.
   *  **ExtentXMin**, **ExtentYMin**, **ExtentXMax** 및 **ExtentXMax** (선택적):
      동일한 이름을 가진 OGRVRTLayer 수준 요소들과 동일한 문법입니다.

   **GeometryField** 요소를 지정하지 않는 경우, 소스 레이어의 모든 도형 필드를 VRT 레이어로 노출시킬 것입니다. 소스 레이어의 도형 필드를 하나도 노출시키지 않으려면 OGRVRTLayer 수준 **GeometryType** 요소를 "wkbNone"으로 설정해야 합니다.

-  **SrcRegion** (선택적):
   이 요소를 사용해서 소스 객체에 대한 초기 공간 필터를 정의합니다. 이 공간 필터는 SetSpatialFilter() 메소드로 VRT 레이어 상에 명확하게 설정된 모든 공간 필터와 결합될 것입니다. 이 요소의 값은 폴리곤을 정의하는 무결한 WKT 문자열이어야만 합니다. 소스 영역에 맞춰 도형을 자르려면 선택적인 **clip** 속성을 TRUE로 설정하면 됩니다. 그렇지 않으면 소스 도형을 수정하지 않습니다.

  **Field** (선택적):
  이 요소로 하나 이상의 속성 필드를 정의할 수도 있습니다. 이 요소를 하나도 정의하지 않는 경우, VRT 레이어에 소스 레이어 또는 SQL 문의 필드를 정의할 것입니다. Field 요소는 다음 속성들을 가질 수도 있습니다:

   *  **name** (필수): 필드 이름입니다.
   *  **type**: 필드 유형입니다. "Integer", "IntegerList", "Real", "RealList", "String", "StringList", "Binary", "Date", "Time", 또는 "DateTime" 가운데 하나로 설정할 수 있습니다. 기본값은 "String"입니다.
   *  **subtype**: 필드 하위 유형입니다. "None", "Boolean", "Int16", "Float32" 가운데 하나로 설정할 수 있습니다. 기본값은 "None"입니다.
   *  **width**: 필드 길이입니다. 기본값은 없습니다.
   *  **precision**: 필드 정밀도입니다. 기본값은 0입니다.
   *  **src**: 이 속성에 복사해 올 소스 필드의 이름입니다. 기본값은 "name" 속성의 값입니다.
   *  **nullable**: 이 속성을 사용해서 필드가 NULL일 수 있는지 여부를 지정할 수 있습니다. 기본값은 "true"입니다.
   *  **unique** (GDAL 3.2 이상 버전): 이 속성을 사용해서 필드에 유일 제약 조건을 적용할지 여부를 지정할 수 있습니다. 기본값은 "false"입니다.

-  **FeatureCount** (선택적):
   (공간 또는 속성 필터가 하나도 설정되지 않은 경우) 이 요소를 사용해서 레이어의 객체 개수를 정의합니다. 소스 레이어에서 객체 개수를 세는 속도가 느린 정적 데이터의 경우 이 요소가 유용할 수 있습니다.

-  **ExtentXMin**, **ExtentYMin**, **ExtentXMax** 및 **ExtentXMax** (선택적):
   이 요소들을 사용해서 레이어의 범위를 정의합니다. 소스 레이어로부터 범위를 가져오는 속도가 느린 정적 데이터의 경우 이 요소들이 유용할 수 있습니다.

OGRVRTWarpedLayer 요소
+++++++++++++++++++++++++

**OGRVRTWarpedLayer** 요소를 사용해서 소스 레이어를 실시간(on-the-fly)으로 재투영합니다. 다음 하위 요소들을 가질 수도 있습니다:

-  **OGRVRTLayer**, **OGRVRTWarpedLayer** 또는 **OGRVRTUnionLayer** (필수):
   재투영할 소스 레이어입니다.

-  **SrcSRS** (선택적):
   이 요소의 값은 재투영하기 전 레이어에 사용할 공간 좌표계입니다. 이 요소를 지정하지 않는 경우, 소스 레이어로부터 추정합니다.

-  **TargetSRS** (필수):
   이 요소의 값은 재투영한 다음 레이어에 사용할 공간 좌표계입니다.

-  **ExtentXMin**, **ExtentYMin**, **ExtentXMax** 및 **ExtentXMax** (선택적):
   이 요소들을 사용해서 레이어의 범위를 정의합니다. 소스 레이어로부터 범위를 가져오는 속도가 느린 정적 데이터의 경우 이 요소가 유용할 수 있습니다.

-  **WarpedGeomFieldName** (선택적):
   이 요소의 값은 왜곡(warp)할 소스 레이어의 도형 필드 이름입니다. 이 요소를 지정하지 않는 경우, 첫 번째 도형 필드를 사용할 것입니다. 도형 필드가 여러 개 있다면 이 요소와 일치하는 필드만 왜곡할 것입니다. 나머지 필드들은 건드리지 않습니다.

OGRVRTUnionLayer 요소
++++++++++++++++++++++++

**OGRVRTUnionLayer** 요소를 사용해서 소스 레이어들의 콘텐츠를 연결(concatenate)합니다. 이 요소는 **name** 속성을 가지고 있어야 하며 다음 하위 요소들을 가질 수도 있습니다:

-  **OGRVRTLayer**, **OGRVRTWarpedLayer** or **OGRVRTUnionLayer** (필수, 반복할 수도 있음):
   통합(union)에 추가할 소스 레이어입니다.

-  **PreserveSrcFID** (선택적):
   이 요소를 ON 또는 OFF로 설정할 수 있습니다. ON으로 설정하는 경우, 소스 레이어로부터 나온 FID를 사용할 것입니다. 그렇지 않으면 계수기(counter)를 사용할 것입니다. 기본값은 OFF입니다.

-  **SourceLayerFieldName** (선택적):
   이 요소를 지정하는 경우, 레이어 필드 정의에 (SourceLayerFieldName 요소의 값으로 명명된) 추가 필드를 추가할 것입니다. 각 객체에 이 필드의 값을 객체가 나온 레이어의 이름과 함께 설정할 것입니다.

-  **GeometryType** (선택적):
   이 옵션의 문법은 OGRVRTLayer 요소의 GeometryType 하위 요소를 참조하십시오. 이 요소를 설정하지 않는 경우, 모든 소스 레이어의 도형 유형으로부터 도형 유형을 추정할 것입니다.

-  **LayerSRS** (선택적):
   이 옵션의 문법은 OGRVRTLayer 요소의 LayerSRS 하위 요소를 참조하십시오. 이 요소를 설정하지 않는 경우, 첫 번째 소스 레이어의 공간 좌표계를 사용할 것입니다.

-  **FieldStrategy** (선택적, **Field** 또는 **GeometryField** 요소와 함께 사용할 수 없음):
   처음 찾은 레이어로부터 나온 필드를 사용하려면 **FirstLayer** 로,
   모든 소스 레이어로부터 나온 모든 필드의 총집합을 사용하려면 **Union** 으로,
   모든 소스 레이어로부터 나온 모든 필드의 공통 필드 부분 집합을 사용하려면 **Intersection** 으로 설정하면 됩니다.
   기본값은 **Union** 입니다.

-  **Field** (선택적, **FieldStrategy** 요소와 함께 사용할 수 없음):
   이 옵션의 문법은 OGRVRTLayer 요소의 Field 하위 요소를 참조하십시오.
   주의: OGRVRTUnionLayer 요소의 맥락에서는 "src" 속성을 지원하지 않습니다. (필드 이름들을 동일하다고 가정하기 때문입니다.)

-  **GeometryField** (선택적, **FieldStrategy** 요소와 함께 사용할 수 없음):
   **name** 속성과 **GeometryType**, **SRS** 및 **Extent[X|Y][Min|Max]** 하위 요소들을 설정할 수 있습니다.

-  **FeatureCount** (선택적):
   이 옵션의 문법은 OGRVRTLayer 요소의 FeatureCount 하위 요소를 참조하십시오.

-  **ExtentXMin**, **ExtentYMin**, **ExtentXMax** 및 **ExtentXMax** (선택적):
   이 옵션의 문법은 OGRVRTLayer 요소를 참조하십시오.

예시: ODBC 포인트 레이어
-------------------------

다음 (disease.ovf) 예시에서 "DISEASE" ODBC 데이터베이스의 "worms" 테이블을 사용해서 공간 레이어를 형성합니다. 가상 파일이 공간 위치를 가져오기 위해 "x" 및 "y" 열을 사용합니다. 레이어를 포인트 레이어로, 그리고 레이어가 WGS84 좌표계를 사용한다고 표시합니다.

.. code-block:: XML

   <OGRVRTDataSource>
       <OGRVRTLayer name="worms">
           <SrcDataSource>ODBC:DISEASE,worms</SrcDataSource>
           <SrcLayer>worms</SrcLayer>
           <GeometryType>wkbPoint</GeometryType>
           <LayerSRS>WGS84</LayerSRS>
           <GeometryField encoding="PointFromColumns" x="x" y="y"/>
       </OGRVRTLayer>
   </OGRVRTDataSource>

예시: 속성 재명명
----------------------------

어떤 상황에서는 소스 레이어의 필드명을 다른 이름으로 재명명할 수 있다는 것이 유용할 수 있습니다. GPX처럼 (<name>, <desc> 등등) 스키마가 고정된 포맷으로 인코딩을 변환하려는 경우 특히 그렇습니다. 다음과 같은 방식으로 SQL 문을 사용하면 필드명을 재명명할 수 있습니다:

.. code-block:: XML

   <OGRVRTDataSource>
       <OGRVRTLayer name="remapped_layer">
           <SrcDataSource>your_source.shp</SrcDataSource>
           <SrcSQL>SELECT src_field_1 AS name, src_field_2 AS desc FROM your_source_layer_name</SrcSQL>
       </OGRVRTLayer>
   </OGRVRTDataSource>

명확한 필드 정의를 사용해서 재명명할 수도 있습니다:

.. code-block:: XML

   <OGRVRTDataSource>
       <OGRVRTLayer name="remapped_layer">
           <SrcDataSource>your_source.shp</SrcDataSource>
           <SrcLayer>your_source</SrcLayer>
           <Field name="name" src="src_field_1" />
           <Field name="desc" src="src_field_2" type="String" width="45" />
       </OGRVRTLayer>
   </OGRVRTDataSource>

예시: 투명한 공간 필터링
--------------------------------------

다음 예시는 소스 레이어로부터 (0,40)-(10,50) 영역과 교차하는 객체만 반환할 것입니다. 그리고 해당 영역에 맞춰 반환된 레이어를 자를 것입니다:

.. code-block:: XML

   <OGRVRTDataSource>
       <OGRVRTLayer name="source">
           <SrcDataSource>source.shp</SrcDataSource>
           <SrcRegion clip="true">POLYGON((0 40,10 40,10 50,0 50,0 40))</SrcRegion>
       </OGRVRTLayer>
   </OGRVRTDataSource>

예시: 재투영된 레이어
--------------------------

다음 예시는 EPSG:4326으로 재투영된 source.shp 레이어를 반환할 것입니다:

.. code-block:: XML

   <OGRVRTDataSource>
       <OGRVRTWarpedLayer>
           <OGRVRTLayer name="source">
               <SrcDataSource>source.shp</SrcDataSource>
           </OGRVRTLayer>
           <TargetSRS>EPSG:4326</TargetSRS>
       </OGRVRTWarpedLayer>
   </OGRVRTDataSource>

예시: 통합 레이어
--------------------

다음 예시는 source1.shp과 source2.shp을 연결한 레이어를 반환할 것입니다:

.. code-block:: XML

   <OGRVRTDataSource>
       <OGRVRTUnionLayer name="unionLayer">
           <OGRVRTLayer name="source1">
               <SrcDataSource>source1.shp</SrcDataSource>
           </OGRVRTLayer>
           <OGRVRTLayer name="source2">
               <SrcDataSource>source2.shp</SrcDataSource>
           </OGRVRTLayer>
       </OGRVRTUnionLayer>
   </OGRVRTDataSource>

예시: SQLite/Spatialite SQL 방언
--------------------------------------

다음 예시는 동일한 폴리곤 shapefile로부터 실시간으로 생성된 서로 다른 레이어 4개를 반환할 것입니다.
첫 번째 레이어는 shapefile 그대로의 shapefile 레이어입니다.
두 번째 레이어는 허용 오차 파라미터를 10으로 설정한 Simplify() SpatiaLite 함수를 적용해서 폴리곤을 단순화한 레이어입니다.
세 번째 레이어에서는 원본 도형을 해당 도형의 볼록 껍질(convex hull)로 대체합니다.
네 번째 레이어에서는 PointOnSurface() SpatiaLite 함수를 사용해서 원본 도형을 대응하는 소스 폴리곤 내부에 있는 포인트로 대체합니다.
이 VRT 파일의 두 번째에서 네 번째까지의 레이어를 사용하려면 GDAL을 SQLite 및 SpatiaLite와 함께 컴파일해야만 한다는 사실을 기억하십시오.

.. code-block:: XML

   <OGRVRTDataSource>
       <OGRVRTLayer name="polygons">
           <SrcDataSource>polygons.shp</SrcDataSource>
       </OGRVRTLayer>
       <OGRVRTLayer name="polygons_as_simplified">
           <SrcDataSource>polygons.shp</SrcDataSource>
           <SrcSQL dialect="sqlite">SELECT Simplify(geometry,10) from polygons</SrcSQL>
       </OGRVRTLayer>
       <OGRVRTLayer name="polygons_as_hulls">
           <SrcDataSource>polygons.shp</SrcDataSource>
           <SrcSQL dialect="sqlite">SELECT ConvexHull(geometry) from polygons</SrcSQL>
       </OGRVRTLayer>
       <OGRVRTLayer name="polygons_as_points">
           <SrcDataSource>polygons.shp</SrcDataSource>
           <SrcSQL dialect="sqlite">SELECT PointOnSurface(geometry) from polygons</SrcSQL>
       </OGRVRTLayer>
   </OGRVRTDataSource>

예시: 다중 도형 필드
---------------------------------

다음 예시는 소스 레이어의 모든 속성과 도형 필드를 노출시킬 것입니다:

.. code-block:: XML

   <OGRVRTDataSource>
       <OGRVRTLayer name="test">
           <SrcDataSource>PG:dbname=testdb</SrcDataSource>
       </OGRVRTLayer>
   </OGRVRTDataSource>

필드들 가운데 일부분만 (또는 전부를!) 노출시키기:

.. code-block:: XML

   <OGRVRTDataSource>
       <OGRVRTLayer name="other_test">
           <SrcDataSource>PG:dbname=testdb</SrcDataSource>
           <SrcLayer>test</SrcLayer>
           <GeometryField name="pg_geom_field_1" />
           <GeometryField name="vrt_geom_field_2" field="pg_geom_field_2">
               <GeometryType>wkbPolygon</GeometryType>
               <SRS>EPSG:4326</SRS>
               <ExtentXMin>-180</ExtentXMin>
               <ExtentYMin>-90</ExtentYMin>
               <ExtentXMax>180</ExtentXMax>
               <ExtentYMax>90</ExtentYMax>
           </GeometryField>
           <Field name="vrt_field_1" src="src_field_1" />
       </OGRVRTLayer>w
   </OGRVRTDataSource>

'pg_geom_field_2' 도형 필드를 EPSG:4326으로 재투영하기:

.. code-block:: XML

   <OGRVRTDataSource>
       <OGRVRTWarpedLayer>
           <OGRVRTLayer name="other_test">
               <SrcDataSource>PG:dbname=testdb</SrcDataSource>
           </OGRVRTLayer>
           <WarpedGeomFieldName>pg_geom_field_2</WarpedGeomFieldName>
           <TargetSRS>EPSG:32631</TargetSRS>
       </OGRVRTWarpedLayer>
   </OGRVRTDataSource>

다중 도형 레이어 여러 개를 통합하고 그 가운데 몇 개만 보전하기:

.. code-block:: XML

   <OGRVRTDataSource>
       <OGRVRTUnionLayer name="unionLayer">
           <OGRVRTLayer name="source1">
               <SrcDataSource>PG:dbname=testdb</SrcDataSource>
           </OGRVRTLayer>
           <OGRVRTLayer name="source2">
               <SrcDataSource>PG:dbname=testdb</SrcDataSource>
           </OGRVRTLayer>
           <GeometryField name="pg_geom_field_2">
               <GeometryType>wkbPolygon</GeometryType>
               <SRS>EPSG:4326</SRS>
               <ExtentXMin>-180</ExtentXMin>
               <ExtentYMin>-90</ExtentYMin>
               <ExtentXMax>180</ExtentXMax>
               <ExtentYMax>90</ExtentYMax>
           </GeometryField>
           <GeometryField name="pg_geom_field_3" />
           <Field name="src_field_1" />
       </OGRVRTUnionLayer>
   </OGRVRTDataSource>

기타 메모
-----------

-  *GeometryField* 요소의 값이 "WKT"인 경우 소스 데이터소스로부터 모든 행을 추출한 다음 공간 필터링을 적용합니다. 본질적으로, WKT 파생 도형에 대한 빠른 공간 필터링은 불가능하다는 뜻입니다.

-  *GeometryField* 요소의 값이 "PointFromColumns"고 (*SrcSQL* 요소가 아니라) *SrcLayer* 요소를 사용하며 가상 레이어에 공간 필터가 적용되어 있는 경우, 내부적으로 공간 필터를 *SrcLayer* 요소에 있는 X 및 Y 열에 대한 속성 필터로 변환할 것입니다.
   빠른 공간 필터링이 중요한 경우 소스 데이터소스에 있는 X 및 Y 열을 -- 색인 작업이 가능한 경우 -- 색인 작업하면 도움이 될 수 있습니다. 예를 들면 소스가 RDBMS인 경우 색인 작업을 할 수 있습니다. *GeometryField* 요소의 *useSpatialSubquery* 속성을 "false"로 설정하면 이 기능을 비활성화시킬 수 있습니다.

