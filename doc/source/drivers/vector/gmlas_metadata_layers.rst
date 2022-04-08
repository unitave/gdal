.. _gmlas_metadata_layers:

GMLAS - 메타데이터 레이어
=======================

이 페이지에서는 :ref:`vector.gmlas` 드라이버가 리포트하는 추가 메타데이터 레이어의 구조를 자세히 설명합니다.

\_ogr_fields_metadata 레이어
~~~~~~~~~~~~~~~~~~~~~~~~~~~

이 레이어는 OGR 필드는 물론, 상위와 하위 레이어 사이의 관계성을 설명하는 "추상" 필드에 관한 메타데이터를 제공합니다.

이 레이어의 필드는 다음과 같습니다:

- ``layer_name``: 필드가 속해 있는 레이어의 이름입니다.

- ``field_name``: 필드의 이름입니다. field_category가 PATH_TO_CHILD_ELEMENT_NO_LINK 또는 GROUP인 경우 NULL일 수도 있습니다.

- ``field_xpath``: 그 내용이 필드에 사용되는 요소/속성의 XPath입니다. XPath는 해당 요소/속성의 직계 상위로 간주되는 요소에, 또는 평탄화의 경우 상위 요소에 상대적입니다. OGR가 생성한 필드라면 NULL일 수도 있습니다.

- ``field_type``: XML 스키마 기본 데이터 유형(string, int, long, ID, ...)입니다. "geometry"로 확장됩니다. OGR가 생성한 필드라면 NULL일 수도 있습니다.

- ``field_is_list``: XML 유형이 목록인지 여부를 선택합니다.

- ``field_min_occurs``: 값 빈도의 최소 횟수인 정수값입니다. 일반적으로 0 또는 1입니다. 또는 배열 유형의 경우 그 이상일 수도 있습니다. OGR가 생성한 필드라면 NULL일 수도 있습니다.

- ``field_max_occurs``: 값 빈도의 최대 횟수인 정수값입니다. 일반적으로 1입니다. 또는 배열 유형의 경우 그 이상일 수도 있습니다. 2147483647은 무제한이라는 뜻입니다. OGR가 생성한 필드라면 NULL일 수도 있습니다.

- ``field_repetition_on_sequence``: 필드가 <sequence maxOccurs=">1 or unbounded"> 구조와 관련이 있는지를 나타내는 불 값입니다. field_max_occurs가 0 또는 1이 아닌 경우에만 설정됩니다.

- ``field_default_value``: 필드의 기본값, 또는 NULL

- ``field_fixed_value``: 필드의 고정값, 또는 NULL

- ``field_category``: 필드의 카테고리입니다. REGULAR, PATH_TO_CHILD_ELEMENT_NO_LINK, PATH_TO_CHILD_ELEMENT_WITH_LINK, PATH_TO_CHILD_ELEMENT_WITH_JUNCTION_TABLE, GROUP 또는 SWE_FIELD 가운데 하나일 수 있습니다. OGR가 생성한 필드라면 NULL일 수도 있습니다.

- ``field_related_layer``: field_category가 REGULAR가 아닌 경우 하위 레이어의 이름입니다.

- ``field_junction_layer``: 연결 레이어의 이름입니다. field_category가 PATH_TO_CHILD_ELEMENT_WITH_JUNCTION_TABLE인 경우에만 설정됩니다.

- ``field_documentation``: 스키마로부터 나온 문서입니다.

field_category 값의 설명:

-  REGULAR: 필드가 레이어의 루트로 간주되는 요소의 직계 하위 요소인 요소 또는 속성의 값으로 이루어져 있습니다.

-  PATH_TO_CHILD_ELEMENT_NO_LINK: 이 카테고리로 선언되는 필드는 'layer_name' 레이어의 ORG 필드로 인스턴스화되지 않습니다. 이 필드는 그냥 상위와 하위 레이어 사이의 관계성을 선언하기 위해 존재할 뿐입니다. 하위 요소가 복잡 유형이거나 또는 OGR 배열 유형 가운데 하나와 일치하지 않는 단순 유형의 반복되는 하위 요소인 경우입니다.

-  PATH_TO_CHILD_ELEMENT_WITH_LINK: 이 필드의 내용은 또다른 레이어의 OGR 객체의 기본 키(primary key)입니다. field_related_layer 필드가 링크된 해당 레이어의 이름을 담고 있습니다.

-  PATH_TO_CHILD_ELEMENT_WITH_JUNCTION_TABLE: 이 카테고리로 선언되는 필드는 'layer_name' 레이어의 ORG 필드로 인스턴스화되지 않습니다. 이 필드는 그냥 상위와 하위 레이어 사이의 관계성을 선언하기 위해 존재할 뿐입니다. 상위와 하위 레이어 사이의 링크가 연결 테이블을 통해 이루어진 경우입니다. (즉 다른 상위 레이어들이 해당 하위 레이어를 참조하는 경우입니다.)

-  GROUP: 이 카테고리로 선언되는 필드는 'layer_name' 레이어의 ORG 필드로 인스턴스화되지 않습니다. 이 필드는 그냥 상위와 하위 레이어 사이의 관계성을 선언하기 위해 존재할 뿐입니다. 레이어가 반복되는 집합원 개수를 가진 XML 스키마 그룹 구조를 사용하는 경우입니다.

-  SWE_FIELD: swe:DataRecord 또는 swe:DataArray 요소의 특수 처리로부터 파생된 필드입니다.


\_ogr_layers_metadata 레이어
~~~~~~~~~~~~~~~~~~~~~~~~~~~

이 레이어는 OGR 레이어에 관한 메타데이터를 제공합니다.

이 레이어의 필드는 다음과 같습니다:

- ``layer_name``: 레이어의 이름입니다.

- ``layer_xpath``: 레이어의 루트 요소로 사용되는 요소의 XPath입니다. 그룹 구조 또는 반복되는 요소의 반복되는 시퀀스인 경우 해당 상위 요소의 XPath와 구별하기 위해 ";extra=XXXX" 접미어가 붙을 수도 있습니다. 연결 테이블 또는 SWE_DATA_ARRAY 레이어의 경우 NULL일 것입니다.

- ``layer_category``: 레이어의 카테고리입니다. TOP_LEVEL_ELEMENT, NESTED_ELEMENT, JUNCTION_TABLE 또는 SWE_DATA_ARRAY 가운데 하나입니다.

- ``layer_pkid_name``: 기본 키 필드의 이름입니다. 객체를 (레이어에서) 유일하게 식별하는 텍스트 속성입니다. 존재하는 경우 xs:ID 유형의 XML 속성/이름이며, 그렇지 않다면 "ogr_pkid" 필드를 자동으로 생성합니다. SWE_DATA_ARRAY 레이어의 경우 NULL일 것입니다.

- ``layer_parent_pkid_name``: 해당 레이어의 상위 레이어를 가리키는 외래 키(foreign key)인 필드의 이름입니다. NESTED_ELEMENT 레이어에만 설정됩니다.

- ``layer_documentation``: 스키마로부터 나온 문서입니다.


\_ogr_layer_relationships 레이어
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

이 레이어는 OGR 레이어들 사이의 관계성에 관한 메타데이터를 제공합니다.

이 레이어의 필드는 다음과 같습니다:

- ``parent_layer``: 상위 레이어의 이름입니다.

- ``parent_pkid``: 상위 레이어의 기본 키 이름입니다.

- ``parent_element_name``: 상위로부터 하위를 링크하는 XML 요소의 이름입니다. 하위 레이어가 그룹 구조 또는 상위의 반복되는 요소의 반복되는 시퀀스인 경우 NULL일 것입니다.

- ``child_layer``: 하위 레이어의 이름입니다.

- ``child_pkid``: 하위 레이어의 기본 키 이름입니다. SWE_DATA_ARRAY 레이어의 경우 NULL일 것입니다.


\_ogr_other_metadata 레이어
~~~~~~~~~~~~~~~~~~~~~~~~~~

이 레이어는 서로 다른 정보를 가진 키/값 쌍들을 담고 있습니다.

이 레이어의 필드는 다음과 같습니다:

- ``key``: 메타데이터 항목의 이름
- ``value``: 메타데이터 항목의 값

다음과 같은 키들이 있을 수 있습니다:

-  document_filename: 읽어온 XML/GML 파일의 파일명

-  configuration_filename: 사용한 XML 환경설정 파일의 파일명

-  configuration_inlined: 환경설정 파일의 XML 내용

-  namespace_uri_XX: 스키마(들)가 참조하는 이름공간의 URI

-  namespace_location_XX: 스키마의 위치

-  namespace_prefix_XX: 스키마(들)가 참조하는 이름공간의 접두어

-  gml_version: GML 버전, 예: 2.1.2, 3.1.1 또는 3.2.1

참고
--------

-  :ref:`GMLAS 드라이버의 주 문서 페이지 <vector.gmlas>`

