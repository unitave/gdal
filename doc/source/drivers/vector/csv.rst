.. _vector.csv:

쉼표 구분 값 (.csv)
============================

.. shortname:: CSV

.. built_in_by_default::

OGR은 CSV(Comma Separated Value) 파일에 저장된 주로 표 형식 비공간 데이터의 읽기 및 쓰기를 지원합니다. CSV 파일은 표 형식 데이터를 지원하는 소프트웨어 패키지들 간의 공통 정보 교환 포맷으로, 텍스트 편집기 또는 종단 사용자가 작성한 스크립트 또는 프로그램으로도 직접 쉽게 생성할 수 있습니다.

CSV 파일은 이론적으로 어떤 확장자든 가질 수 있지만 OGR가 ".csv" 확장자로 끝나는 CSV 파일만 지원하기 때문에, 자동 인식을 위해 ".csv" 확장자를 사용하는 편이 좋습니다. 데이터소스 이름은 단일 CSV 파일일 수도 있고 디렉터리를 가리킬 수도 있습니다. 디렉터리를 CSV 데이터소스로 인식시키려면 디렉터리에 있는 파일들 가운데 최소한 절반 이상은 ".csv" 확장자로 끝나야 합니다. 접근한 CSV 파일 하나 당 레이어(테이블) 하나를 생성합니다.

CSV 구조이지만 ".csv" 확장자로 끝나지 않는 파일의 경우, 파일명 앞에 'CSV:' 접두어를 붙여서 CSV 드라이버가 강제로 불러오게 할 수 있습니다.

OGR CSV 드라이버는 쓰기 및 읽기를 지원합니다. CSV 포맷이 여러 길이의 텍스트 줄들을 가지고 있기 때문에, 읽기 작업은 순차적으로 진행됩니다. 객체를 임의의 순서로 읽어오는 것은 일반적으로 아주 느릴 것입니다. OGR CSV 레이어는 개별 .prj 파일에 저장된 좌표계를 가지고 있을 수도 있습니다. (GeoCSV 사양을 참조하십시오.) "WKT"라는 필드를 읽어오는 경우 해당 필드가 WKT 도형을 담고 있다고 가정하지만, 정규 필드로도 취급합니다. OGR CSV 드라이버는 (".csvt" 확장자를 가진) 필드 유형 정보 파일을 사용할 수 없는 경우 모든 속성 열을 문자열 데이터 유형으로 반환합니다.

CSV 파일과 같은 이름을 가졌지만 확장자는 ".csvt"인 필드 유형 정보 파일을 통해 Integer, Real, String, Date (YYYY-MM-DD), Time (HH:MM:SS+nn), DateTime (YYYY-MM-DD HH:MM:SS+nn)이라는 제한된 유형을 인식할 수 있습니다. 각 유형을 큰따옴표로 감싸고 쉼표로 구분해서 (예: "Integer","String") 한 줄로 목록화해야 합니다. 각 열의 길이와 정밀도를 "Integer(5)","Real(10.7)","String(15)"처럼 명확하게 지정할 수도 있습니다. 그러면 이 드라이버는 이런 유형들을 CSV 열에 지정된 대로 사용할 것입니다. 하위 유형을 괄호 사이에 넣어서 -- "Integer(Boolean)", "Integer(Int16)" 그리고 "Real(Float32)" 처럼 -- 전송할 수 있습니다. GDAL 2.1버전부터, `GeoCSV 사양 <http://giswiki.hsr.ch/GeoCSV>`_ 에 따라 경도/편동을 가진 열을 지정하기 위해 "CoordX" 또는 "Point(X)" 유형을, 위도/편북 값에 "CoordY" 또는 "Point(Y)" 유형을, 그리고 WKT 서식으로 인코딩된 도형에 "WKT" 유형을 사용할 수 있습니다.

GDAL 2.2버전부터, OGR StringList, IntegerList, Integer64List 및 RealList 유형에 각각 대응하는 "JSonStringList", "JSonIntegerList", "JSonInteger64List" 및 "JSonRealList" 유형을 사용할 수 있습니다. 그러면 필드값을 적절하게 CSV 이스케이프 처리한 JSon 배열로 인코딩합니다.

아래 "열기 옵션" 단락에서 설명하는 열기 옵션을 지정하면 필드 유형을 자동으로 추정할 수도 있습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::

포맷
------

CSV 파일은 한 줄마다 레이어(테이블)에 있는 객체(레코드) 하나를 가지고 있습니다. 속성 필드의 값들은 쉼표로 구분됩니다. 한 줄 당 필드가 최소한 2개는 있어야만 합니다. 이 줄들은 도스(CR/LF) 또는 유닉스(LF) 스타일의 새줄 문자(line terminator)로 끝날 수도 있습니다. 각 레코드는 동일한 개수의 필드를 가지고 있어야 합니다. 이 드라이버는 쌍반점, 탭 또는 공백 문자도 필드 구분자로 지원할 것입니다. 하지만 이런 자동 탐지는 CSV 파일의 첫 줄에 잠재적인 다른 구분자가 없을 경우에만 가능합니다. 그렇지 않을 경우 -- 잠재적인 구분자가 2개 이상 존재하는 경우 -- 기본값인 쉼표만 구분자로 인식할 것입니다.

(쉼표, 따옴표 또는 새줄 문자를 담고 있는 속성값 같은) 복잡 속성값은 큰따옴표로 감싸져 있을 수도 있습니다. 이렇게 큰따옴표 처리된 문자열 안에 다른 큰따옴표가 있을 경우, 이를 "이스케이프" 처리하려면 문자열 내부 큰따옴표를 중복시켜야 합니다.

이 드라이버는 기본적으로 파일의 첫 줄을 모든 필드에 대한 필드명 목록으로 취급하려 시도합니다. 하지만, 하나 이상의 이름이 모두 숫자일 경우 첫 줄이 실제로는 데이터라고 가정하고 내부적으로 더미(dummy) 필드명을 (field_1에서
field_n까지) 생성해서 첫 번째 레코드를 객체로 취급합니다. 숫자값이 큰따옴표로 감싸져 있는 경우 필드명으로 취급합니다. GDAL 2.1버전부터, HEADERS 열기 옵션으로 이 습성을 변경할 수 있습니다.

모든 CSV 파일을 UTF-8 인코딩으로 취급합니다. 파일의 시작 위치에 있는 BOM(Byte Order Mark)은 정확하게 파싱될 것입니다. WRITE_BOM 옵션을 사용해서 바이트 순서 표식(Byte Order Mark)을 가진 파일을 생성할 수 있는데, 이렇게 하면 몇몇 소프트웨어(특히 엑셀)와의 호환성을 향상시킬 수 있습니다.

예시 (employee.csv):

::

   ID,Salary,Name,Comments
   132,55000.0,John Walker,"The ""big"" cheese."
   133,11000.0,Jane Lake,Cleaning Staff

첫 번째 레코드의 Comments 값이 큰따옴표를 담고 있기 때문에 큰따옴표 사이에 있고, 값이 담고 있는 큰따옴표가 큰따옴표로 감싼 문자열의 끝을 의미하는 것이 아니라는 것을 알려주기 위해 내부의 큰따옴표를 중복시켰다는 사실을 기억하십시오.

탭을 구분자로 사용하거나 필드 유형 또는 구조를 정의하는 다른 보조 데이터를 가진, 쉼표는 없지만 고정 열 길이를 가진 파일을 포함하는 수많은 텍스트 유형 입력물의 변이형들을 쉼표 구분 값 파일이라고 부르는 경우가 있습니다. 이 드라이버는 이런 파일들 전부를 지원하려 하지는 않지만, 그 대신 자동 인식할 수 있는 단순한 .csv 파일을 지원하려 합니다. 일반적으로 스크립트 또는 다른 메커니즘을 이용해서 이런 다른 변이형들을 OGR CSV 드라이버와 호환되는 형식으로 변환할 수 있습니다.

공간 정보를 담고 있는 CSV 읽기 작업
------------------------------------------

포인트 도형 작성 작업
~~~~~~~~~~~~~~~~~~~~~~~~~

다음과 같은 CSV 파일(test.csv)이 있다고 할 때:

::

   Latitude,Longitude,Name
   48.1,0.25,"First point"
   49.2,1.1,"Second point"
   47.5,0.75,"Third point"

GDAL 2.1버전부터, X_POSSIBLE_NAMES 및 Y_POSSIBLE_NAMES 열기 옵션으로 X/경도와 Y/위도를 담고 있을 수도 있는 잠재적인 열의 이름을 직접 지정할 수 있습니다:

::

   ogrinfo -ro -al test.csv -oo X_POSSIBLE_NAMES=Lon\* -oo Y_POSSIBLE_NAMES=Lat\* -oo KEEP_GEOM_COLUMNS=NO

이 명령어는 다음을 반환할 것입니다:

::

   OGRFeature(test):1
     Name (String) = First point
     POINT (0.25 48.1)

   OGRFeature(test):2
     Name (String) = Second point
     POINT (1.1 49.2)

   OGRFeature(test):3
     Name (String) = Third point
     POINT (0.75 47.5)

CSV 파일이 헤더 줄을 가지고 있지 않은 경우, 더미 "field_n" 이름을 좌표 필드의 잠재적인 이름으로 사용할 수 있습니다. 예를 들어 다음 명령어를 실행하면 평문 XYZ 포인트 데이터를 열 수 있습니다:

::
   ogrinfo -ro -al elevation.xyz -oo X_POSSIBLE_NAMES=field_1 -oo Y_POSSIBLE_NAMES=field_2 -oo Z_POSSIBLE_NAMES=field_3*

그렇지 않고 열 하나 또는 여러 개가 WKT, (16진법으로 인코딩된) WKB 또는 GeoJSON으로 인코딩된 도형 정의를 담고 있는 경우 (이때 GeoJSON의 내용은 CSV 규칙에 따른 서식이어야만 합니다. 다시 말해 큰따옴표로 감싸져야만 하고, 제대로 이스케이프 처리하기 위해 문자열 안에 있는 큰따옴표는 중복시켜야만 합니다) GEOM_POSSIBLE_NAMES 열기 옵션으로 이런 열(들)의 이름을 지정해야 합니다.

이전 버전의 경우 :ref:`VRT <vector.vrt>` 드라이버를 통해 X 및 Y 좌표 열을 가지고 있는 CSV 파일로부터 공간 정보(포인트)를 추출할 수 있습니다.

관련 VRT 파일(test.vrt)을 다음과 같이 작성할 수 있습니다:

::

   <OGRVRTDataSource>
       <OGRVRTLayer name="test">
           <SrcDataSource>test.csv</SrcDataSource>
           <GeometryType>wkbPoint</GeometryType>
           <LayerSRS>WGS84</LayerSRS>
           <GeometryField encoding="PointFromColumns" x="Longitude" y="Latitude"/>
       </OGRVRTLayer>
   </OGRVRTDataSource>

그리고 다음 명령어를 실행하면:

::

   ogrinfo -ro -al test.vrt

다음을 반환할 것입니다:

::

   OGRFeature(test):1
     Latitude (String) = 48.1
     Longitude (String) = 0.25
     Name (String) = First point
     POINT (0.25 48.1 0)

   OGRFeature(test):2
     Latitude (String) = 49.2
     Longitude (String) = 1.1
     Name (String) = Second point
     POINT (1.1 49.200000000000003 0)

   OGRFeature(test):3
     Latitude (String) = 47.5
     Longitude (String) = 0.75
     Name (String) = Third point
     POINT (0.75 47.5 0)

라인 도형 작성 작업
~~~~~~~~~~~~~~~~~~~~~~~~

다음과 같은 CSV 파일(test.csv)이 있다고 할 때:

::

   way_id,pt_id,x,y
   1,1,2,49
   1,2,3,50
   2,1,-2,49
   2,2,-3,50

Spatialite 지원이 활성화된 GDAL 빌드에서 다음 명령어를 실행하면:

::

   ogrinfo test.csv -dialect SQLite -sql "SELECT way_id, MakeLine(MakePoint(CAST(x AS float),CAST(y AS float))) FROM test GROUP BY way_id"


다음을 반환할 것입니다:

::

   OGRFeature(SELECT):0
     way_id (String) = 1
     LINESTRING (2 49,3 50)

   OGRFeature(SELECT):1
     way_id (String) = 2
     LINESTRING (-2 49,-3 50)

VSI 가상 파일 시스템 API 지원
-----------------------------------

이 드라이버는 VSI 가상 파일 시스템 API가 관리하는 파일의 읽기 및 쓰기를 지원합니다. VSI 가상 파일 시스템 API가 관리하는 파일에는 "정규" 파일은 물론 /vsizip/ (읽기-쓰기) , /vsigzip/ (읽기 전용) , /vsicurl/ (읽기 전용) 도메인에 있는 파일도 포함됩니다.

/dev/stdout 또는 /vsistdout/ 에 쓰기도 지원합니다.

열기 옵션
------------

(일반적으로 ogrinfo 또는 ogr2ogr의 ``-oo name=value`` 파라미터를 사용해서) 다음과 같은 열기 옵션들을 지정할 수 있습니다:

-  **MERGE_SEPARATOR=YES/NO**: (기본값은 NO)
   YES로 설정하면 연속되는 구분자들을 병합할 것입니다. 구분자가 공백 문자인 경우 가장 유용합니다.

-  **AUTODETECT_TYPE=YES/NO**: (기본값은 NO)
   YES로 설정하면 필드 데이터 유형을 자동 탐지할 것입니다. (자동 탐지에 사용된 레코드들 이상의) 레코드를 읽어오는 동안 자동 탐지된 데이터 유형에 해당하지 않는 값이 존재하는 경우, 경고를 발생시키고 필드를 비울 것입니다.

-  **KEEP_SOURCE_COLUMNS=YES/NO**: (기본값은 NO)
   추정 작업이 활성화돼 있는데 추정된 유형이 문자열과 다른 경우 원본 열의 복사본을 유지합니다. 원본 열의 이름 뒤에 접미어 "_original"을 붙일 것입니다. AUTODETECT_TYPE=YES인 경우에만 이 플래그를 사용해야 합니다.

-  **AUTODETECT_WIDTH=YES/NO/STRING_ONLY**: (기본값은 NO)
   YES로 설정하면 문자열 및 정수형 필드의 길이를 탐지하고, 실수형 필드의 길이와 정밀도를 탐지합니다. STRING_ONLY로 설정하면 문자열 필드의 길이만 탐지합니다. NO로 설정하면 기본 크기 및 길이를 선택합니다. 
   (자동 탐지에 사용된 레코드들 이상의) 레코드를 읽어오는 동안 자동 탐지된 길이/정밀도에 해당하지 않는 값이 존재하는 경우, 경고를 발생시키고 필드를 비울 것입니다.

-  **AUTODETECT_SIZE_LIMIT=size**:
   데이터 유형과 길이/정밀도를 판단하기 위해 조사할 바이트 개수를 지정합니다. 기본값은 1,000,000입니다. 0으로 지정하면 파일 전체를 조사합니다.
   주의: 표준 입력물로부터 읽어오는 경우 /vsistdin/ 이 구현된 방식 때문에 값이 1MB로 제한될 것입니다.

-  **QUOTED_FIELDS_AS_STRING=YES/NO**: (기본값은 NO)
   AUTODETECT_TYPE=YES인 경우에만 사용할 수 있습니다.
   YES로 설정하면 큰따옴표로 감싸인 필드를 문자열 필드로 강제합니다. 기본값 NO로 설정하면 큰따옴표로 감싸인 필드의 콘텐츠가 실수, 정수, ... 데이터 유형인지 테스트할 것입니다.

-  **X_POSSIBLE_NAMES=list_of_names**: (GDAL 2.1 이상 버전)
   포인트의 X/경도 좌표 필드명으로 사용할 수 있는 이름들을 쉼표로 구분한 목록입니다. 각 이름은 prefix*, \*suffix 또는 \*middle* 처럼 시작 그리고/또는 마지막 위치에 별표 문자를 사용한 패턴일 수도 있습니다. 이 열에 있는 값은 반드시 부동소수점형이어야만 합니다. X_POSSIBLE_NAMES 및 Y_POSSIBLE_NAMES 옵션이 둘 다 지정되어 있어야만 하며 CSV 파일의 열들 가운데 각각 일치하는 이름이 있어야만 합니다. X_POSSIBLE_NAMES 및 Y_POSSIBLE_NAMES 옵션을 사용하는 경우 레이어 하나 당 도형 열 하나만 작성할 수도 있습니다.

-  **Y_POSSIBLE_NAMES=list_of_names**: (GDAL 2.1 이상 버전)
   포인트의 Y/위도 좌표 필드명으로 사용할 수 있는 이름들을 쉼표로 구분한 목록입니다. 각 이름은 prefix*, \*suffix 또는 \*middle* 처럼 시작 그리고/또는 마지막 위치에 별표 문자를 사용한 패턴일 수도 있습니다. 이 열에 있는 값은 반드시 부동소수점형이어야만 합니다. X_POSSIBLE_NAMES 및 Y_POSSIBLE_NAMES 옵션이 둘 다 지정되어 있어야만 하며 CSV 파일의 열들 가운데 각각 일치하는 이름이 있어야만 합니다.

-  **Z_POSSIBLE_NAMES=list_of_names**: (GDAL 2.1 이상 버전)
   포인트의 Z/표고 좌표 필드명으로 사용할 수 있는 이름들을 쉼표로 구분한 목록입니다. 각 이름은 prefix*, \*suffix 또는 \*middle* 처럼 시작 그리고/또는 마지막 위치에 별표 문자를 사용한 패턴일 수도 있습니다. 이 열에 있는 값은 반드시 부동소수점형이어야만 합니다. X_POSSIBLE_NAMES 및 Y_POSSIBLE_NAMES 와 함께 지정하는 경우에만 연산에 넣습니다.

-  **GEOM_POSSIBLE_NAMES=list_of_names**: (GDAL 2.1 이상 버전)
   WKT, (16진법으로 인코딩된, PostGIS 2.0 확장 사양 WKB일 수도 있는) WKB 또는 GeoJSON으로 인코딩된 도형 정의를 담고 있는 도형 열의 이름으로 사용할 수 있는 이름들을 쉼표로 구분한 목록입니다. 각 이름은 prefix*, \*suffix 또는 \*middle* 처럼 시작 그리고/또는 마지막 위치에 별표 문자를 사용한 패턴일 수도 있습니다.

-  **KEEP_GEOM_COLUMNS=YES/NO**: (기본값은 YES)
   탐지된 X, Y, Z 또는 도형 열을 정규 속성 필드로 노출시킵니다.

-  **HEADERS=YES/NO/AUTO**: (기본값은 AUTO) (GDAL 2.1 이상 버전)
   파일의 첫 줄이 열 이름을 담고 있는지 여부를 선택합니다. AUTO로 설정하면, 어떤 값도 엄격하게 숫자가 아닌 경우 GDAL이 첫 줄이 열 이름을 담고 있다고 가정할 것입니다.

-  **EMPTY_STRING_AS_NULL=YES/NO**: (기본값은 NO) (GDAL 2.1 이상 버전)
   읽기 작업 시 비어 있는 문자열을 NULL 필드로 간주할지 여부를 선택합니다.

생성 문제점
---------------

이 드라이버는 (.csv 파일들의 디렉터리로) 새 데이터베이스 생성, 기존 디렉터리 또는 기존 .csv 파일에 새 .csv 파일 추가 또는 기존 .csv 테이블에 객체 추가를 지원합니다. GDAL 2.1버전부터, 완료된 수정 작업의 용량이 디스크로 플러시(flush)하기 전에 RAM에 임시로 저장할 수 있을 정도로 작은 경우 기존 객체 삭제 또는 대체, 또는 필드 추가/수정/삭제를 지원합니다.

레이어 생성 옵션
----------------

-  **LINEFORMAT**:
   기본적으로 새 .csv 파일을 생성할 때 로컬 플랫폼의 새줄 문자 규범으로 (win32에서는 CR/LF로 또는 다른 모든 시스템에서는 LF로) 생성합니다. **CRLF** (도스 서식) 또는 **LF** (유닉스 서식) 값을 가질 수 있는 LINEFORMAT 레이어 생성 옵션을 이용하면 이 기본 습성을 대체할 수 있습니다.

-  **GEOMETRY**:
   기본적으로 .csv 파일에 작성되는 객체의 도형을 폐기합니다. **GEOMETRY=AS_WKT** 를 지정하면 도형을 WKT 표현으로 내보낼 수 있습니다. **GEOMETRY=AS_XYZ**, **GEOMETRY=AS_XY** 또는 **GEOMETRY=AS_YX** 를 지정하면 포인트 도형을 해당 X, Y, Z 구성요소로 (CSV 파일에 서로 다른 열들로) 내보낼 수도 있습니다. 이 도형 열(들)은 속성값을 가진 열들 앞에 추가될 것입니다. SQLite SQL 방언 쿼리를 이용하면 도형을 GeoJSON 표현으로 내보낼 수도 있습니다. 아래 예시를 참조하십시오.

-  **CREATE_CSVT=YES/NO**:
   레이어의 각 열의 유형 및 선택적인 길이와 정밀도를 서술하는 관련 .csvt 파일을 생성할지 여부를 선택합니다. (위에 있는 설명을 참조하십시오.) 기본값은 NO입니다.

-  **SEPARATOR=COMMA/SEMICOLON/TAB/SPACE**:
   필드 구분자 문자를 지정합니다. 기본값은 COMMA입니다.

-  **WRITE_BOM=YES/NO**:
   파일의 시작 위치에 UTF-8 BOM(Byte Order Mark)을 작성할지 여부를 선택합니다. 기본값은 NO입니다.

-  **GEOMETRY_NAME=name**: (GDAL 2.1 이상 버전)
   도형 열의 이름을 지정합니다. GEOMETRY=AS_WKT 그리고 CREATE_CSVT=YES인 경우에만 사용할 수 있습니다. 기본값은 WKT입니다.

-  **STRING_QUOTING=IF_NEEDED/IF_AMBIGUOUS/ALWAYS**: (GDAL 2.3 이상 버전)
   문자열을 큰따옴표로 감쌀지를 지정합니다. IF_AMBIGUOUS로 설정하면 숫자로 보이는 문자열 값을 큰따옴표로 감쌀 것입니다. (이 값은 IF_NEEDED도 암시합니다.) 기본값은 IF_AMBIGUOUS입니다. (이전 버전의 기본값은 IF_NEEDED였습니다.)

환경설정 옵션
-------------

다음 :ref:`환경설정 옵션들 <configoptions>` 을 사용할 수 있습니다:

-  :decl_configoption:`OGR_WKT_PRECISION` =int:
   좌표값의 소수점 이하 자릿수를 지정합니다. 기본값은 15입니다. 
   소수점을 가진 숫자를 서식화할 때 나타날 수 있는 중요하지 않은 후행 00000x 또는 99999x를 제거하기 위해 휴리스틱한 방법을 사용합니다.

-  :decl_configoption:`OGR_WKT_ROUND` =YES/NO: (GDAL 2.3 이상 버전)
   중요하지 않은 후행 00000x 또는 99999x를 제거하기 위해 앞에서 언급한 휴리스틱 방법을 활성화할지 여부를 선택합니다. 기본값은 YES입니다.

예시
~~~~~~~~

-  다음은 ogr2ogr를 이용해서 포인트 도형을 가진 shapefile을 파일의 첫 번째 열에 포인트의 X, Y, Z 좌표를 가지고 있는 .csv 파일로 변환시키는 예시입니다:

   ::

      ogr2ogr -f CSV output.csv input.shp -lco GEOMETRY=AS_XYZ

-  다음은 ogr2ogr를 이용해서 shapefile을 GeoJSON 서식을 사용하는 지리 필드를 가진 .csv 파일로 변환시키는 예시입니다:

   ::

      ogr2ogr -f CSV -dialect sqlite -sql "select AsGeoJSON(geometry) AS geom, * from input" output.csv input.shp

- 다음은 CSV를 GeoPackage로 변환시키는 예시입니다. 좌표 열들의 이름을 지정하고 좌표계를 할당합니다:

   ::

      ogr2ogr \
        -f GPKG output.gpkg \
        input.csv \
        -oo X_POSSIBLE_NAMES=longitude \
        -oo Y_POSSIBLE_NAMES=latitude \
        -a_srs 'EPSG:4326'


특정 데이터소스
----------------------

CSV 드라이버는 CSV 파일과 유사한 구조를 가진 파일도 읽어올 수 있습니다:

-  `FAA 웹사이트 <http://www.faa.gov/airports/airport_safety/airportdata_5010/menu/index.cfm>`_ 에서 다운로드할 수 있는 NfdcFacilities.xls, NfdcRunways.xls, NfdcRemarks.xls 및 NfdcSchedules.xls 공항 데이터 파일들

-  `USGS GNIS <http://geonames.usgs.gov/domestic/download_data.htm>`_ (Geographic Names Information System)의 파일들
   

-  `GeoNames <http://www.geonames.org>`_ 의 allCountries 파일

-  `Eurostat .TSV 파일들 <http://epp.eurostat.ec.europa.eu/NavTree_prod/everybody/BulkDownloadListing?file=read_me.pdf>`_

기타 메모
-----------

-  `GeoCSV 사양 <http://giswiki.hsr.ch/GeoCSV>`_ (GDAL 2.1 이상 버전이 지원)

-  `DM 솔루션 그룹 <http://www.dmsolutions.ca/>`_ 과 `GoMOOS <http://www.gomoos.org/>`_ 이 OGR CSV 드라이버의 초기 개발을 지원했습니다.

-  필드 유형 자동 탐지 및 도형 열 관련 열기 옵션은 `Carto <https://carto.com/>`_ 사의 재정 지원으로 개발되었습니다.

