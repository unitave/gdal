.. _vector.netcdf:

NetCDF: 네트워크 공통 데이터 형식 - 벡터
=========================================

.. versionadded:: 2.1

.. shortname:: netCDF

.. build_dependencies:: libnetcdf

netCDF 드라이버는 벡터 데이터셋 읽기 및 쓰기를 (처음부터 생성 그리고 어떤 경우 추가 작업을) 지원합니다. (:ref:`래스터 <raster.netcdf>` 드라이버 문서도 있습니다.)

NetCDF(Network Common Data Form)는 배열 지향 데이터 접근을 위한 인터페이스로 과학 데이터를 표현하기 위해 쓰입니다.

이 드라이버는 CF-1.6 규범의 "point" 및 "profile" `객체 유형  <http://cfconventions.org/cf-conventions/v1.6.0/cf-conventions.html#_features_and_feature_types>`_ 을 처리합니다. CF-1.7 이하(는 물론 CF가 아닌 파일)의 경우, 포인트가 아닌 도형에 좀 더 사용자 지정 접근법도 지원합니다.

이 드라이버는 내부에 단순 도형 정보가 인코딩된 CF-1.8 규범을 준수하는 파일로부터 읽기 및 쓰기도 지원합니다.

드라이버 케이퍼빌리티
-------------------

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::

규범 및 데이터 포맷
----------------------------

netCDF 벡터 드라이버는 CF(Climate and Forecast) 메타데이터 규범을 준수하는 netCDF 파일의 읽기 및 쓰기를 지원합니다. CF-1.8 규범의 단순 도형 사양을 이용해서, 또는 CF-1.6 규범을 이용해서 포인트가 아닌 도형 항목을 WKT로 작성하면 벡터 데이터셋을 작성할 수 있습니다.

두 포맷들을 구별하기
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

netCDF 파일을 읽어올 때, 이 드라이버는 전체 수준 *Conventions* 속성을 읽어오려 시도할 것입니다. 이 속성의 값이 *CF-1.8* 이상인 경우 (CF 규범에 지정된 것과 똑같은 포맷인 경우) 이 드라이버는 netCDF 파일을 내부에 *CF-1.8* 도형을 담고 있는 파일로 취급할 것입니다. *Conventions* 속성의 값이 CF-1.6이면, CF-1.6 규범을 따르는 파일로 취급할 것입니다.

CF-1.8 쓰기 제한 사항
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

CF-1.8 netCDF 데이터셋을 작성하는 경우 몇몇 제한 사항이 존재합니다. CF-1.8 표준이 지정하는 객체 유형의 쓰기만 지원하며 (자세한 내용은 `도형 <#geometry>`_ 단락 참조) 측정 객체(measured feature)는 부분적으로만 지원합니다. 단순하지 않은 만곡 도형 같은 다른 도형들은 어떤 식으로도 지원하지 않습니다.

CF-1.8 데이터셋은 *추가(append)* 접근 모드도 지원하지 않습니다.

CF-1.8 데이터셋을 위해 *예약된 변수 이름* 으로 간주되는 항목이 있습니다. 이 드라이버가 메타데이터를 저장하는 데 이 변수 이름들을 이용합니다. 레이어 여러 개를 가진 데이터셋을 작성하는 경우 명명 충돌을 막으려면 이 변수 이름들을 레이어 이름으로 사용하지 마십시오.

CF-1.8 데이터셋에 있는 어떤 레이어의 이름이 LAYER이고 이 레이어가 FIELD라는 필드를 가지고 있다고 해봅시다. 그렇다면 다음과 같은 이름들이 *예약* 되었다고 간주할 것입니다:

-  *LAYER_node_coordinates*: 포인트 정보를 저장하는 데 사용됩니다.
-  *LAYER_node_count*: 도형(shape) 별 포인트 개수 정보를 저장하는 데 사용됩니다. (LAYER가 포인트 도형 유형을 가지고 있는 경우 생성되지 않습니다.)
-  *LAYER_part_node_count*: 부분(part) 별 포인트 개수 정보를 저장하는 데 사용됩니다. (LAYER가 멀티라인스트링, 멀티폴리곤으로 이루어져 있거나, 내곽 고리를 가진 폴리곤을 최소한 하나 가지고 있는 경우에만 생성됩니다.)
-  *LAYER_interior_ring*: 내곽 고리(interior ring) 정보를 저장하는 데 사용됩니다. (LAYER가 내곽 고리를 가진 폴리곤을 최소한 하나 가지고 있는 경우에만 생성됩니다.)
-  *LAYER_field_FIELD*: FIELD에 대한 필드 정보를 저장하는 데 사용됩니다.

CF-1.8 데이터셋에 적용되는 예약 이름들은 이들뿐입니다.

CF-1.6/WKT 데이터셋에는 앞에서 언급한 제한 사항이 적용되지 않습니다.

개념 매핑
-------------------

필드 유형
~~~~~~~~~~~

netCDF 파일 생성 작업 시, OGR 필드 유형과 netCDF 유형을 다음과 같이 매핑합니다:

================ =========================================================
OGR 필드 유형    netCDF 유형
================ =========================================================
String(1)        char
String           char(2차원), 또는 NC4의 경우 문자열
Integer          int
Integer(Boolean) byte
Integer(Int16)   short
Integer64        NC4의 경우 int64 NC4, 또는 NC3의 경우 폴백으로서의 double
Real             double
Real(Float32)    float
Date             int (units="days since 1970-1-1")
DateTime         double (units="seconds since 1970-1-1 0:0:0")
================ =========================================================

이 드라이버는 각 OGR 필드/netCDF 변수에 대해 다음 속성도 작성합니다.

-  *ogr_field_name*: OGR 필드 이름 (netCDF 변수 이름이 충돌 때문에 다른 경우 유용합니다.)
-  *ogr_field_type*: OGR 필드 유형 (String, Integer, Date, DateTime, ...)
-  *ogr_field_width*: OGR 필드 길이. 길이가 0이 아닌 경우에만 설정합니다. 문자열은 0인 경우에도 설정합니다.
-  *ogr_field_precision*: OGR 필드 정밀도. 정밀도가 0이 아닌 경우에만 설정합니다.

이 속성들을 (WRITE_GDAL_TAGS 데이터셋 생성 옵션을 NO로 설정하지 않는 이상) 기본적으로 작성합니다. 이 속성들은 읽기 작업에 필수는 아니지만, 필드 특성을 더 잘 식별할 수 있게 해줄 수도 있습니다.

읽기 작업 시에는 다음과 같이 매핑합니다:

================================================== ==============
netCDF 유형                                        OGR 필드 유
================================================== ==============
byte                                               Integer
ubyte (NC4 전용)                                   Integer
char (1차원)                                       String(1)
char (2차원)                                       String
string (NC4 전용)                                  String
short                                              Integer(Int16)
ushort (NC4 전용)                                  Integer
int                                                Integer
int 또는 double (units="days since 1970-1-1")      Date
uint (NC4 전용)                                    Integer64
int64 (NC4 전용)                                   Integer64
uint64 (NC4 전용)                                  Real
float                                              Real(Float32)
double                                             Real
double (units="seconds since 1970-1-1 0:0:0")      DateTime
================================================== ==============

레이어
~~~~~~

CF-1.8을 준수하는 드라이버에서, 단일 레이어는 CF-1.8 준수 netCDF 파일 안에 있는 단일 **도형 컨테이너** 에 대응합니다. 또다른 변수가 (아마도 데이터 변수가) -- CF-1.8 사양에 따라 -- **geometry** 속성을 통해 이 도형 컨테이너를 탐조합니다.
CF-1.8 준수 netCDF 파일을 읽어올 때, 열린 데이터셋에 netCDF 파일 안에 있는 모든 도형 컨테이너를 개별 레이어로 나타낼 것입니다. 마찬가지로 CF-1.8 데이터셋을 작성할 때 각 레이어를 변수 이름이 소스 레이어의 변수 이름인 도형 컨테이너에 작성할 것입니다.
CF-1.8 데이터셋으로 지정해서 작성하는 경우, MULTIPLE_LAYERS 데이터셋 생성 옵션의 값과 상관없이 다중 레이어는 항상 활성화되고 항상 단일 netCDF 파일로 작성합니다.

이 드라이버의 예전 (CF-1.8 이전) 버전으로 생성된 파일을 작업하는 경우, 해당 파일이 1차원 변수만 담고 있고 동일한 차원으로 (또는 char 유형인 경우 2차원 변수로) 색인되어 있다면 일반적으로 단일 netCDF 파일이 단일 OGR 레이어에 대응합니다.
다중 그룹을 가진 netCDF 4버전의 경우, 각 그룹을 개별 OGR 레이어로 볼 수도 있습니다. 작성 작업 시, MULTIPLE_LAYERS 데이터셋 생성 옵션을 이용해서 다중 레이어를 비활성화시켜야 할지 여부를, 또는 다중 레이어들을 각각 개별 파일로 또는 개별 그룹으로 생성해야 할지를 제어할 수 있습니다.

문자열
~~~~~~~

netCDF 3버전 포맷은 가변 길이 문자열을 네이티브하게 지원하지 않습니다. 이 문제를 해결하기 위해 OGR는 2차원 char 변수를 사용합니다. 첫 번째 차원은 레코드 차원이고 두 번째 차원은 문자열의 최대 길이입니다.

OGR는 작성 시 기본적으로 "자동 성장(auto-grow)" 모드를 구현합니다. 즉 필요한 경우 OGR 문자열 필드를 저장하기 위해 사용되는 변수 최대 길이를 연장합니다.

WKT 데이터셋의 경우, 이때 이미 작성된 레코드를 처음부터 다시 작성하게 됩니다. 이 과정이 사용자에게는 알기 쉽겠지만, 생성 과정이 비선형적인 방식으로 느려질 수 있습니다. 포인트가 아닌 도형 유형을 가진 레이어에 도형의 ISO WKT 표현을 저장하는 경우에도 비슷한 메커니즘을 사용합니다.

CF-1.8 데이터셋의 경우, 문자열 길이 차원을 연장하는 것은 레코드를 재복사하지 않고 단순한 정수 재할당만 하는 상대적으로 성능에 영향을 주지 않는 처리 과정입니다. CF-1.8 데이터셋에서 차원 성장은 성능에 그리 영향을 주지 않기 때문에 문자열 길이 차원의 자동 성장이 항상 활성화되어 있습니다.

netCDF 4버전 산출물 포맷(NC4)을 사용할 때 문자열은 기본적으로 netCDF 4버전 가변 길이 문자열로 작성될 것입니다.

도형
~~~~~~~~

CF-1.8 규범을 준수하는 netCDF 파일로부터 읽어오는 경우 OGRPoint, OGRLineString, OGRPolygon, OGRMultiPoint, OGRMultiLineString, 그리고 OGRMultiPolygon 객체 유형을 지원합니다.
CF-1.8 규범에서 폴리곤 대 멀티폴리곤에 관해 존재하는 약간의 애매함 때문에, 이 드라이버는 **geometry_type** 폴리곤을 가진 레이어의 도형에 대해 대부분의 경우 기본적으로 멀티폴리곤이라고 가정할 것입니다. 폴리곤 유형을 사용할 유일한 예외는 레이어의 도형 컨테이너 안에 **part_node_count** 속성이 존재하지 않는 경우입니다.
규범의 요구 사항에 따라, 이 드라이버는 X, Y, Z 축을 가진 도형의 읽기 및 쓰기를 지원합니다. M 축을 담고 있는 객체를 가진 소스 레이어로부터 쓰기도 부분적으로 지원합니다. CF-1.8 netCDF 파일에서 측정 객체의 X, Y, Z 정보를 수집할 수 있지만, 측정 정보는 완전히 사라질 것입니다.

CF-1.6/WKT 데이터셋을 작업하는 경우 Point 또는 Point25D 도형 유형을 가진 레이어가 존재한다면 투영 좌표계의 경우 x,y(,z) 변수를 내부적으로 생성하고, 또는 지리 좌표계의 경우 lon,lat(,z) 변수를 내부적으로 생성할 것입니다.
다른 도형 유형의 경우 (NC3 산출물의 경우 2차원 char, 또는 NC4의 경우 문자열 유형의) "ogc_wkt" 변수를 생성하고 ISO WKT 문자열로 도형을 저장하기 위해 사용합니다.

"프로파일" 객체 유형
~~~~~~~~~~~~~~~~~~~~~~

이 드라이버는 예를 들어 고정 수평 위치에서 수직 라인을 따라 몇몇 위치에서 발생하는 현상 같은 "프로파일(profile)" 객체 유형을 처리할 수 있습니다. 이런 표현에서, 프로파일이 일부 변수를 색인화하고 관찰(observation)이 다른 변수들을 색인화합니다.

더 정확하게 말하자면 이 드라이버는 프로파일의 "`색인화된 비정형 배열 표현(Indexed ragged array representation) <http://cfconventions.org/cf-conventions/v1.6.0/cf-conventions.html#_indexed_ragged_array_representation_of_profiles>`_" 에 따라 구성된 프로파일의 읽기 및 쓰기를 지원합니다.

읽기 작업 시, 이 드라이버는 프로파일 차원을 가리키는 "instance_dimension" 속성을 가진 "parentIndex" 같은 변수를 기반으로 프로파일 차원이 색인화한 변수들의 값들을 수집해서 관찰 차원이 색인화한 변수들의 개수만큼 노출시킵니다.

쓰기 작업 시 FEATURE_TYPE 레이어 생성 옵션을 YES로 설정해야만 하며, 드라이버에 프로파일 차원이 색인화한 OGR 필드가 어떤 것인지 그리고 관찰 차원이 색인화한 OGR 필드가 어떤 것인지 알려줘야 할 것입니다. PROFILE_VARIABLES 레이어 생성 옵션으로 프로파일 차원이 색인화한 필드들의 목록을 지정할 수 있습니다. (그 외의 필드들은 관찰 차원이 색인화한 것으로 가정합니다.)
프로파일이 색인화한 필드는 (내부적으로 생성된) 수평 지리 위치(geolocation)와 위치 이름 등등 같은 기타 사용자 속성들입니다. 어떤 변수들이 프로파일 차원이 색인화한 변수들인지, 변수를 선택할 때 주의를 기울여야 합니다. (프로파일 차원이 색인화한 변수인 경우에만 연산에 넣는) OGR 객체가 2개 있다고 할 때, 두 객체가 이런 변수에 서로 다른 값을 가지고 있다면 서로 다른 프로파일에 속해 있다고 간주할 것입니다.

다음 예시에서 프로파일 차원이 station_name 및 time 변수를 색인화했을 수도 있습니다. (프로파일 차원이 도형도 색인화했다고 가정합니다.) 이 변수들 가운데 하나에 대해 동일한 값을 가진 모든 레코드가 다른 변수들에 대해서도 동일한 값을 가지고 있기 때문입니다. 그에 반해 temperature 및 Z 변수는 기본 차원이 색인화한 것일 것입니다.

============ ==================== ================== =========== ===
station_name time                 geometry           temperature Z
============ ==================== ================== =========== ===
Paris        2016-03-01T00:00:00Z POINT (2 49)       25          100
Vancouver    2016-04-01T12:00:00Z POINT (-123 49.25) 5           100
Paris        2016-03-01T00:00:00Z POINT (2 49)       3           500
Vancouver    2016-04-01T12:00:00Z POINT (-123 49.25) -15         500
============ ==================== ================== =========== ===

(동일한 이름의 정수형 OGR 필드가 존재하지 않는 이상) 프로파일 차원의 (PROFILE_DIM_NAME 레이어 생성 옵션으로 대체할 수 있는 기본 이름은 "profile") 이름을 가진 정수형 필드를 이용해서 프로파일 사이트의 자동 계산된 ID를 저장할 것입니다.

NC4가 아닌 산출물 포맷의 경우 프로파일 차원의 크기의 기본값은 100이고, 추가적인 프로파일이 추가되는 경우 이 크기는 자동으로 늘어납니다. (자동 성장 문자열과 비슷한 성능 문제점을 가지고 있습니다.) NC4 산출물 포맷의 경우, 프로파일 차원의 크기는 기본적으로 무제한입니다.

데이터셋 생성 옵션
------------------------

-  **GEOMETRY_ENCODING=CF_1.8/WKT**:
   데이터셋 내부에 새 레이어를 생성할 때 어떤 도형 인코딩을 사용할지 선택합니다. 기본값은 CF_1.8입니다.

-  **FORMAT=NC/NC2/NC4/NC4C**:
   netCDF 포맷을 지정합니다.
   NC는 (netCDF 3.X 및 4.X버전 라이브러리와 호환되는) 전형적인 netCDF 포맷입니다.
   NC2는 4GB를 초과하는 파일을 위한 NC 확장 사양입니다.
   NC4는 HDF5 컨테이너를 이용해서 netCDF 4버전 라이브러리에서만 사용할 수 있는 새로운 케이퍼빌리티(새 유형들, 그룹 개념 등등)를 제공하는 netCDF 4버전 포맷입니다.
   NC4C는 NC4 포맷을 전형적인 netCDF 포맷이 지원하는 개념들로 제약하는 포맷입니다.
   기본값은 NC입니다.

-  **WRITE_GDAL_TAGS=YES/NO**:
   GDAL 특화 정보를 netCDF 속성으로 작성할지 여부를 선택합니다. 기본값은 YES입니다.

-  **CONFIG_FILE=string**:
   산출물을 정밀하게 제어하기 위한 `XML 환경설정 파일 <#xml-configuration-file>`_ (또는 그때 그때 즉시 처리되는 그 내용)을 가리키는 경로를 지정합니다.

GEOMETRY_ENCODING=WKT를 동시에 지정한 경우에만 다음 옵션이 영향을 미칠 것입니다:

-  **MULTIPLE_LAYERS=NO/SEPARATE_FILES/SEPARATE_GROUPS**:
   기본값인 NO로 설정하면, 예를 들어 데이터셋이 단일 OGR 레이어 하나만 담을 수 있습니다.
   SEPARATE_FILES로 설정하면, 각 OGR 레이어를 단일 netCDF 파일에 넣을 수 있습니다. 이 경우 데이터셋 생성 시 전송된 이름을 디렉터리로 사용하고, 레이어 이름을 netCDF 파일의 기본명으로 사용합니다.
   FORMAT=NC4일 때 동일한 파일 안에 있는 각 개별 netCDF 그룹에 각 OGR 레이어를 넣으려면 SEPARATE_GROUPS로 설정하면 됩니다.

레이어 생성 옵션
----------------------

다음 옵션은 두 데이터셋 유형 모두에 적용됩니다:

-  **USE_STRING_IN_NC4=YES/NO**:
   NC4 포맷의 문자열에 NetCDF 문자열 유형을 사용할지 여부를 선택합니다. NO로 설정하면 2차원 char 변수를 사용합니다.
   FORMAT=NC4일 때 기본값은 YES입니다.

다음 옵션들은 GEOMETRY_ENCODING=WKT인 데이터셋의 경우에만 영향을 미칩니다:

-  **RECORD_DIM_NAME=string**:
   객체들을 색인화하는 무제한 차원의 이름을 지정합니다. 기본값은 "record"입니다.

-  **STRING_DEFAULT_WIDTH=int**:
   (2차원 char 변수를 사용하는 경우) 문자열의 기본 길이를 지정합니다. 자동 성장 모드의 기본값은 10이고, 그렇지 않은 경우 80입니다.

-  **WKT_DEFAULT_WIDTH=int**:
   (2차원 char 변수를 사용하는 경우) WKT 문자열의 기본 길이를 지정합니다. 자동 성장 모드의 기본값은 1,000이고, 그렇지 않은 경우 10,000입니다.

-  **AUTOGROW_STRINGS=YES/NO**:
   문자열 필드를 2차원 char 변수로 직렬화하는 경우, 고정되지 않은 길이의 문자열 필드 또는 ogc_wkt 특수 필드를 자동 성장시킬지 여부를 선택합니다. 기본값은 YES입니다.
   NO로 설정하면, 문자열이 (STRING_DEFAULT_WIDTH로 설정된) 최대 초기 길이를 초과하는 경우 절단합니다. 도형인 경우에는 완전히 폐기합니다.

-  **FEATURE_TYPE=AUTO/POINT/PROFILE**:
   CF FeatureType을 선택합니다.
   기본값인 AUTO로 설정하면, 레이어 도형 유형이 포인트인 경우 FeatureType=Point를 선택하고 그렇지 않은 경우 "ogc_wkt" 필드를 이용하는 사용자 지정 접근법을 사용합니다.
   `PROFILE <#profile>`_ 로 설정해서, 색인화된 비정형 배열 표현을 생성하도록 선택할 수도 있습니다.

-  **PROFILE_DIM_NAME=string**:
   프로파일 차원 및 변수의 이름입니다. 기본값은 "profile"입니다.
   FEATURE_TYPE=PROFILE인 경우에만 사용할 수 있습니다.

-  **PROFILE_DIM_INIT_SIZE=int or string**:
   프로파일 차원의 초기 크기를 지정하거나 또는 NC4 파일의 경우 "UNLIMITED"입니다.
   FORMAT 옵션의 값이 NC4가 아닌 경우 기본값은 100이고, NC4인 경우 "UNLIMITED"입니다.
   FEATURE_TYPE=PROFILE인 경우에만 사용할 수 있습니다.

-  **PROFILE_VARIABLES=string**:
   프로파일 차원이 색인화해야만 하는 필드들의 이름을 쉼표로 구분한 목록입니다.
   FEATURE_TYPE=PROFILE인 경우에만 사용할 수 있습니다.

다음 옵션들은 GEOMETRY_ENCODING=CF_1.8인 데이터셋의 경우에만 영향을 미칩니다:

-  **BUFFER_SIZE=int**:
   쓰기 버퍼의 바이트 단위 연성 제한(soft limit)을 지정합니다. 일반적으로 값이 클수록 성능이 향상될 수 있지만, 사용할 수 있는 실제 메모리 용량보다는 안정적으로 작아야 합니다. 그렇지 않은 경우 스래싱(thrashing)이 발생할 수 있습니다. 이 값은 기본적으로 사용 가능한 실제 메모리의 20% 수준으로 설정됩니다. (여기에서 사용 가능이란 가상 주소 공간 용량을 고려한 실제 총 RAM을 의미합니다.)
   버퍼 콘텐츠는 객체 변환 *도중* 이 아니라 객체 변환 사이에 커밋되기 때문에, 이 제한은 단일 객체에는 적용되지 않습니다. 설정할 수 있는 최소값은 4096입니다. 이보다 작은 값을 설정하면 기본값을 사용할 것입니다.

-  **GROUPLESS_WRITE_BACK=YES/NO**:
   대상 netCDF 파일에 데이터를 작성하는 데 걸리는 시간을 줄이기 위해, 데이터를 배열에 함께 그룹화해서 한 번에 작성하는 경우가 많습니다. 이 배열은 대상 데이터셋에 있는 변수와 각각 관련되어 있습니다.
   netCDF 파일에 관련 데이터를 작성하는 즉시 배열을 폐기하는데, 이는 변수에 대한 완전한 데이터 배열이 메모리에 조합되는 즉시 발생합니다.
   메모리 용량이 작은 컴퓨터의 경우, 대용량 레이어들을 가진 대용량 데이터셋을 작성할 때 이런 최적화가 문제를 일으킬 수도 있습니다. 이 옵션을 YES로 설정하면 배열 작성을 비활성화하고 데이터를 데이터 별로 작성하게 합니다. 메모리 부족 오류 또는 성능 문제가 발생하지 않는 이상 이 옵션을 NO로 놔둘 것을 강력하게 권장합니다.
   일반적인 경우, 이 기능은 변환 효율성을 크게 향상시킵니다. 기본값은 NO입니다.

XML 환경설정 파일
----------------------

다음 `스키마 <https://github.com/OSGeo/gdal/blob/master/data/netcdf_config.xsd>`_ 를 준수하는 XML 환경설정 파일을 이용해서 산출물 포맷을 매우 정밀하게 제어할 수 있습니다. 특히 (units 같은) 필요한 모든 속성이 `NetCDF CF-1.6 규범 <http://cfconventions.org/cf-conventions/v1.6.0/cf-conventions.html>`_ 을 준수하도록 설정할 수 있습니다.

이 환경설정 파일은 `MapServer OGR 산출물 <http://mapserver.org/output/ogr_output.html>`_ 관련 사용례에서 사용할 수 있도록 특별히 설계되었지만, MapServer 산출물 전용은 아닙니다.

이 파일을 사용해서:

-  데이터셋 및 레이어 생성 옵션을 설정할 수 있습니다.
-  전체 수준 netCDF 속성을 설정할 수 있습니다.
-  OGR 필드명을 netCDF 변수명에 매핑할 수 있습니다.
-  netCDF 변수에 추가된 netCDF 속성을 설정할 수 있습니다.

이 파일의 영향 범위는 요소가 루트 <Configuration> 노드의 직계 하위 요소로 정의된 경우 전체 수준에 적용되거나, <Layer> 노드의 하위 요소로 정의된 경우 해당 레이어에 국한됩니다.

CONFIG_FILE 데이터셋 생성 옵션으로 XML 환경설정 파일의 이름을 지정할 수 있습니다. 또는, 그때 그때 즉시 처리하도록 파일의 내용을 옵션의 값으로 지정할 수도 있습니다. (이 값은 반드시 "<Configuration" 문자열로 시작해야만 합니다.)

다음 예시는 이런 모든 가능성 및 우선 순위 규칙을 보여주고 있습니다:

.. code-block:: xml

   <Configuration>
       <DatasetCreationOption name="FORMAT" value="NC4"/>
       <DatasetCreationOption name="MULTIPLE_LAYERS" value="SEPARATE_GROUPS"/>
       <LayerCreationOption name="RECORD_DIM_NAME" value="observation"/>
   <!-- applies to all layers -->
       <Attribute name="copyright" value="Copyright(C) 2016 Example"/>
       <Field name="weight">  <!-- edit user field/variable -->
           <Attribute name="units" value="kg"/>
           <Attribute name="maximum" value="10" type="double"/>
       </Field>
       <Field netcdf_name="z"> <!-- edit predefined variable -->
           <Attribute name="long_name" value="Elevation"/>
       </Field>
   <!-- start of layer specific definitions -->
       <Layer name="1st_layer" netcdf_name="firstlayer"> <!-- OGR layer "1st_layer" is renamed as "firstlayer" netCDF group -->
           <LayerCreationOption name="FEATURE_TYPE" value="POINT"/>
           <Attribute name="copyright" value="Public domain"/> <!-- override global one -->
           <Attribute name="description" value="This is my first layer"/> <!-- additional attribute -->
           <Field name="1st_field" netcdf_name="firstfield"/> <!-- rename OGR field "1st_field" as the "firstfield" netCDF variable -->
           <Field name="weight"/> <!-- cancel above global customization -->
           <Field netcdf_name="lat"> <!-- edit predefined variable -->
               <Attribute name="long_name" value=""/> <!-- remove predefined attribute -->
           </Field>
       </Layer>
       <Layer name="sounding">
           <LayerCreationOption name="FEATURE_TYPE" value="PROFILE"/>
           <Field name="station_name" main_dim="profile"/> <!-- the corresponding netCDF variable will be indexed against the profile dimension, instead of the observation dimension -->
           <Field name="time" main_dim="profile"/> <!-- the corresponding netCDF variable will be indexed against the profile dimension, instead of the observation dimension -->
       </Layer>
   </Configuration>

**ncdump** 유틸리티를 실행하면 산출물이 받은 영향을 확인할 수 있습니다.

추가 참고 목록
---------------

-  :ref:`netCDF 래스터 <raster.netcdf>` 드라이버
-  `NetCDF CF-1.6 규범 <http://cfconventions.org/cf-conventions/v1.6.0/cf-conventions.html>`_
-  `NetCDF CF-1.8 규범 초안 <https://github.com/cf-convention/cf-conventions/blob/master/ch07.adoc>`_
-  `NetCDF 컴파일된 라이브러리 <http://www.unidata.ucar.edu/downloads/netcdf/index.jsp>`_
-  `NetCDF 문서 <http://www.unidata.ucar.edu/software/netcdf/docs/>`_

감사의 말
-------

netCDF의 벡터 읽기/쓰기 케이퍼빌리티는 `캐나다 기상청(Meteorological Service of Canada) <https://www.ec.gc.ca/meteo-weather/>`_ , `세계 오존 및 자외선 데이터 센터(World Ozone and Ultraviolet Radiation Data Centre) <http://woudc.org>`_, 그리고 `미국 지질조사국 <https://www.usgs.gov>`_ 의 재정 지원으로 개발되었습니다.

