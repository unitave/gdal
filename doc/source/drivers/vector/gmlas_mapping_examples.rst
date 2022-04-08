.. _gmlas_mapping_examples:

GMLAS - 매핑 예
========================

이 페이지에서는 :ref:`vector.gmlas` 드라이버가 XML 구조를 어떻게 OGR 레이어 및 필드에 매핑하는지에 관한 몇 가지 예시를 제공합니다.


.. list-table:: Mapping examples
   :header-rows: 1

   * - 스키마
     - 문서
     - OGR 레이어
     - 주석
   * - .. code-block:: xml

            <schema xmlns="http://www.w3.org/2001/XMLSchema">
            <element name="MyFeature">
            <complexType>
                <sequence>
                    <element name="name" type="string"/>
                </sequence>
                <attribute name="id" type="ID" use="required"/>
                <attribute name="attr" type="string"/>
            </complexType>
            </element>
            </schema>
     - .. code-block:: xml

            <MyFeature id="my_id" attr="attr_value">
                <name>my_name</name>
            </MyFeature>

     - ::

            Layer name: MyFeature
            Geometry: None
            id: String (0.0) NOT NULL
            attr: String (0.0)
            name: String (0.0) NOT NULL
            OGRFeature(MyFeature):1
                id (String) = my_id
                attr (String) = attr_value
                name (String) = my_name
     - 단순 유형의 속성 및 하위 요소를 가지고 있고 최대 집합원 개수(cardinality)가 1인 요소
   * - .. code-block:: xml

            <schema xmlns="http://www.w3.org/2001/XMLSchema">
            <element name="MyFeature">
            <complexType>
                <sequence>
                    <element name="str_array" type="string"
                            maxOccurs="2"/>
                    <element name="dt_array" type="dateTime"
                            maxOccurs="unbounded"/>
                </sequence>
                <attribute name="id" type="ID" use="required"/>
            </complexType>
            </element>
            </schema>

     - .. code-block:: xml

            <MyFeature id="my_id">
                <str_array>first string</str_array>
                <str_array>second string</str_array>
                <dt_array>2016-09-24T15:31:00Z</dt_array>
                <dt_array>2016-09-24T15:32:00Z</dt_array>
            </MyFeature>

     - ::

            Layer name: MyFeature
            Geometry: None
            id: String (0.0) NOT NULL
            str_array: StringList (0.0) NOT NULL
            OGRFeature(MyFeature):1
                id (String) = my_id
                str_array (StringList) = 
                    (2:first string,second string)

            Layer name: MyFeature_dt_array
            Geometry: None
            ogr_pkid: String (0.0) NOT NULL
            parent_id: String (0.0) NOT NULL
            value: DateTime (0.0)
            OGRFeature(MyFeature_dt_array):1
                ogr_pkid (String) = my_id_dt_array_1
                parent_id (String) = my_id
                value (DateTime) = 2016/09/24 15:31:00+00

            OGRFeature(MyFeature_dt_array):2
                ogr_pkid (String) = my_id_dt_array_2
                parent_id (String) = my_id
                value (DateTime) = 2016/09/24 15:32:00+00
     - 배열과 하위 레이어를 가진 예시
   * - .. code-block:: xml

            <schema xmlns="http://www.w3.org/2001/XMLSchema">
            <element name="MyFeature">
            <complexType>
                <sequence>
                <element name="identifier">
                    <complexType>
                    <sequence>
                        <element name="name">
                        <complexType>
                            <simpleContent>
                            <extension base="string">
                                <attribute name="lang"
                                        type="string"/>
                            </extension>
                            </simpleContent>
                        </complexType>
                        </element>
                        <element name="namespace" type="string"
                                minOccurs="0"/>
                    </sequence>
                    </complexType>
                </element>
                </sequence>
                <attribute name="id" type="ID" use="required"/>
            </complexType>
            </element>
            </schema>

     - .. code-block:: xml

            <MyFeature id="my_id">
                <identifier>
                    <name lang="en">my_name</name>
                    <namespace>baz</namespace>
                </identifier>
            </MyFeature>

     - ::

            Layer name: MyFeature
            Geometry: None
            id: String (0.0) NOT NULL
            identifier_name_lang: String (0.0)
            identifier_name: String (0.0)
            identifier_namespace: String (0.0)
            OGRFeature(MyFeature):1
                id (String) = my_id
                identifier_name_lang (String) = en
                identifier_name (String) = my_name
                identifier_namespace (String) = baz

     - 주 레이어로 접어 넣을 수 있는 내포 요소의 예시. 하위 요소에 있는 속성 사용.
   * - .. code-block:: xml

            <schema xmlns:myns="http://myns"
                    targetNamespace="http://myns"
                    elementFormDefault="qualified"
                    xmlns="http://www.w3.org/2001/XMLSchema">

            <element name="AbstractFeature" abstract="true"/>

            <element name="FeatureCollection">
            <complexType><sequence>
                <element ref="myns:AbstractFeature" maxOccurs="unbounded"/>
            </sequence></complexType>
            </element>

            <complexType name="namesType">
            <sequence>
                <element ref="myns:name" maxOccurs="unbounded"/>
            </sequence>
            </complexType>

            <element name="MyFeature" substitutionGroup="myns:AbstractFeature">
            <complexType><sequence>
                <element name="names" type="myns:namesType"/>
                </sequence>
                <attribute name="id" type="ID" use="required"/>
            </complexType>
            </element>

            <element name="MyFeature2" substitutionGroup="myns:AbstractFeature">
            <complexType><sequence>
                <element name="names" type="myns:namesType"/>
                </sequence>
                <attribute name="id" type="ID" use="required"/>
            </complexType>
            </element>

            <element name="name">
            <complexType><sequence>
                <element name="name" type="string"/>
                <element name="lang" type="string"/>
            </sequence></complexType>
            </element>

            </schema>

     - .. code-block:: xml

            <FeatureCollection xmlns="http://myns">
                <MyFeature id="my_id">
                    <names>
                        <name>
                        <name>name</name>
                        <lang>en</lang>
                        </name>
                        <name>
                        <name>nom</name>
                        <lang>fr</lang>
                        </name>
                    </names>
                </MyFeature>
                <MyFeature2 id="my_id2">
                    <names>
                        <name>
                        <name>nom2</name>
                        <lang>fr</lang>
                        </name>
                    </names>
                </MyFeature2>
            </FeatureCollection>

     - ::

            Layer name: name
            OGRFeature(name):1
                ogr_pkid (String) = _name_1
                name (String) = name
                lang (String) = en

            OGRFeature(name):2
                ogr_pkid (String) = _name_2
                name (String) = nom
                lang (String) = fr

            OGRFeature(name):3
                ogr_pkid (String) = _name_3
                name (String) = nom2
                lang (String) = fr

            Layer name: MyFeature
            OGRFeature(MyFeature):1
                id (String) = my_id

            Layer name: MyFeature2
            OGRFeature(MyFeature2):1
                id (String) = my_id2

            Layer name: MyFeature_names_name_name
            OGRFeature(MyFeature_names_name_name):1
                occurrence (Integer) = 1
                parent_pkid (String) = my_id
                child_pkid (String) = _name_1

            OGRFeature(MyFeature_names_name_name):2
                occurrence (Integer) = 2
                parent_pkid (String) = my_id
                child_pkid (String) = _name_2

            Layer name: MyFeature2_names_name_name
            OGRFeature(MyFeature2_names_name_name):1
                occurrence (Integer) = 1
                parent_pkid (String) = my_id2
                child_pkid (String) = _name_3

     - "MyFeature" 및 "MyFeature1" 두 레이어가 참조하는 공통 요소 "name"의 예시. "MyFeature_names_name_name" 및 "MyFeature2_names_name_name" 두 연결(junction) 레이어를 통해 링크를 확립합니다.

swe:DataArray
-------------

다음 코드 조각은

.. code-block:: xml

       <swe:DataArray>
           <swe:elementCount>
               <swe:Count>
                       <swe:value>2</swe:value>
               </swe:Count>
           </swe:elementCount>
           <swe:elementType name="Components">
               <swe:DataRecord>
                       <swe:field name="myTime">
                           <swe:Time definition="http://www.opengis.net/def/property/OGC/0/SamplingTime">
                                   <swe:uom xlink:href="http://www.opengis.net/def/uom/ISO-8601/0/Gregorian"/>
                           </swe:Time>
                       </swe:field>
                       <swe:field name="myCategory">
                           <swe:Category definition="http://dd.eionet.europa.eu/vocabulary/aq/observationverification"/>
                       </swe:field>
                           <swe:field name="myQuantity">
                           <swe:Quantity definition="http://dd.eionet.europa.eu/vocabulary/aq/primaryObservation/hour">
                                   <swe:uom xlink:href="http://dd.eionet.europa.eu/vocabulary/uom/concentration/ug.m-3"/>
                           </swe:Quantity>
                       </swe:field>
                       <swe:field name="myCount">
                           <swe:Count definition="http://"/>
                       </swe:field>
                           <swe:field name="myText">
                           <swe:Text definition="http://"/>
                       </swe:field>
                           <swe:field name="myBoolean">
                           <swe:Boolean definition="http://"/>
                       </swe:field>
               </swe:DataRecord>
           </swe:elementType>
           <swe:encoding>
                   <swe:TextEncoding decimalSeparator="." blockSeparator="@@" tokenSeparator=","/>
           </swe:encoding>
           <swe:values>2016-09-01T00:00:00+01:00,1,2.34,3,foo,true@@2017-09-01T00:00:00,2,3.45</swe:values>
       </swe:DataArray>

전용 레이어로 매핑되도록 특수 처리될 것입니다:

::

   Layer name: dataarray_1_components
   Geometry: None
   Feature Count: 2
   Layer SRS WKT:
   (unknown)
   parent_ogr_pkid: String (0.0) NOT NULL
   mytime: DateTime (0.0)
   mycategory: String (0.0)
   myquantity: Real (0.0)
   mycount: Integer (0.0)
   mytext: String (0.0)
   myboolean: Integer(Boolean) (0.0)
   OGRFeature(dataarray_1_components):1
     parent_ogr_pkid (String) = BAE8440FC4563A80D2AB1860A47AA0A3_DataArray_1
     mytime (DateTime) = 2016/09/01 00:00:00+01
     mycategory (String) = 1
     myquantity (Real) = 2.34
     mycount (Integer) = 3
     mytext (String) = foo
     myboolean (Integer(Boolean)) = 1

   OGRFeature(dataarray_1_components):2
     parent_ogr_pkid (String) = BAE8440FC4563A80D2AB1860A47AA0A3_DataArray_1
     mytime (DateTime) = 2017/09/01 00:00:00
     mycategory (String) = 2
     myquantity (Real) = 3.45


참고
--------

-  :ref:`GMLAS 드라이버의 주 문서 페이지 <vector.gmlas>`

