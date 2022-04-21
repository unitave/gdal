.. _vector.shapefile:

ESRI Shapefile / DBF
====================

.. shortname:: ESRI Shapefile

.. built_in_by_default::

ESRI Shapefile 드라이버는 ESRI Shapefile의 모든 변이형을 읽고, 생성하고, 편집할 수 있을 것입니다. 이 드라이버는 관련 .shp 파일이 없는 독립형 DBF 파일도 처리할 수 있습니다.

OGR Shapefile 드라이버는 일반적으로 전체 shapefile 디렉터리를 데이터셋으로, 그리고 해당 디렉터리 안에 있는 단일 shapefile을 레이어로 취급합니다. 이 경우 디렉터리 이름을 데이터셋 이름으로 사용해야 합니다. 하지만 shapefile 세트의 (.shp, .shx 또는 .dbf) 파일 가운데 하나를 데이터셋 이름으로 설정할 수도 있는데, 그러면 레이어 하나를 가진 데이터셋으로 취급할 것입니다.

SHPT_ARC 유형 shapefile을 읽어올 때 대응하는 레이어를 wkbLineString 유형으로 리포트할 것이지만, 각 도형의 부분 개수에 따라 각 객체의 실제 도형 유형이 OGRLineString일 수도 있고 OGRMultiLineString일 수도 있다는 사실을 기억하십시오. SHPT_POLYGON 유형 shapefile도 마찬가지로, wkbPolygon 유형 레이어로 리포트할 것이지만 각 도형의 부분 개수에 따라 각 객체의 실제 도형 유형이 OGRPolygon일 수도 있고 OGRMultiPolygon일 수도 있습니다.

측정(M 좌표)을 지원합니다. 지정한 도형이 측정 유형이거나 적절한 레이어 생성 옵션을 사용하는 경우 측정을 가진 shapefile을 생성합니다. 측정 도형을 가지고 있을 수도 있는 shapefile을 열 때, 첫 번째 도형(shape)을 검사해서 측정을 사용하는 경우 그에 맞춰 레이어의 도형(geometry) 유형을 설정합니다. ADJUST_GEOM_TYPE 열기 옵션으로 이 습성을 변경할 수 있습니다.

이 드라이버는 멀티패치(MultiPatch) 파일을 읽어와서 각 패치(patch) 도형을 팬(fan) 또는 메시(mesh)를 위한 TIN 표현의 TIN 또는 GEOMETRYCOLLECTION으로 변환합니다.

예전 Arc/Info 또는 새 ESRI OGC WKT 스타일의 .prj 파일이 존재하는 경우, 해당 파일을 읽어와서 객체에 투영법을 관련짓는 데 사용할 것입니다. GDAL 2.3버전부터, EPSG 데이터베이스의 카탈로그에 있는 항목으로 .prj 파일의 공간 좌표계를 식별하기 위해 EPSG 데이터베이스와 일치하는지 확인하려 시도할 것입니다.

이 드라이버의 판독기는 다중 부분(multipart) 폴리곤이 사양을 따른다고 가정합니다. 다시 말해 외곽 고리의 꼭짓점들이 X/Y 평면에서 시계 방향이고 내곽 고리의 꼭짓점들은 반시계 방향이라는 뜻입니다. 이 규칙과 관련해서 shapefile에 오류가 발생하는 경우, :decl_configoption:`OGR_ORGANIZE_POLYGONS` 환경설정 옵션을 DEFAULT로 설정해서 폴리곤 부분들의 위상 관계를 기반으로 전체 분석을 수행, 산출되는 폴리곤이 OGC 단순 피처(Simple Feature) 규범을 정확하게 준수하도록 할 수 있습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::

인코딩
--------

.cpg 파일에 있는 코드 페이지 설정을, 또는 대체제로서 .dbf 파일로부터 LDID/codepage 설정을 읽어와서, 이를 이용해서 읽기 작업 시 문자열 필드를 UTF-8로 변환하고 쓰기 작업 시 그 반대로 변환하려 시도합니다. LDID "87 / 0x57"를 알맞지 않을 수도 있는 ISO-8859-1로 취급합니다. :decl_configoption:`SHAPE_ENCODING` 환경설정 옵션을 사용해서 shapefile의 인코딩 해석을 CPLRecode가 지원하는 어떤 인코딩으로든 대체할 수도 있고, 또는 이 옵션을 ""로 설정해서 재 인코딩을 막을 수도 있습니다.

GDAL 3.1부터, "SHAPEFILE" 도메인에 다음과 같은 메타데이터 항목들을 사용할 수 있습니다:

-  **LDID_VALUE=integer**:
   DBF 헤더로부터 나온 원시(raw) LDID 값입니다. 이 값이 0이 아닌 경우에만 존재합니다.

-  **ENCODING_FROM_LDID=string**:
   LDID_VALUE로부터 추정한 인코딩 이름입니다. LDID_VALUE가 존재하는 경우에만 존재합니다.

-  **CPG_VALUE=string**:
   .cpg 파일의 내용입니다. 파일이 존재하는 경우에만 존재합니다.

-  **ENCODING_FROM_CPG=string**:
   CPG_VALUE로부터 추정한 인코딩 이름입니다. CPG_VALUE가 존재하는 경우에만 존재합니다.

-  **SOURCE_ENCODING=string**:
   GDAL이 문자열을 인코딩/재 인코딩하기 위해 사용하는 인코딩입니다. 사용자가 :decl_configoption:`SHAPE_ENCODING` 환경설정 옵션 또는 ``ENCODING`` 열기 옵션을 (비어 있는 값도 포함해서) 지정하는 경우, 그 값으로 이 메타데이터 항목을 채웁니다. 지정하지 않는 경우, ENCODING_FROM_CPG가 존재하면 그 값과 동일합니다. 존재하지 않으면 ENCODING_FROM_LDID의 값과 동일합니다.

공간 및 속성 색인 작업
------------------------------

OGR Shapefile 드라이버는 공간 색인 작업과 제한된 형식의 속성 색인 작업을 지원합니다.

공간 색인 작업은 UMN MapServer가 사용하는 것과 동일한 .qix 사분 트리(quadtree) 공간 색인 파일을 이용합니다. 공간 색인 작업이 완료되면, 대용량 데이터셋 전체를 공간 필터링으로 훑어 좁은 영역을 선택하는 과정이 획기적으로 빨라질 수 있습니다.

이 드라이버는 ESRI 공간 색인 파일(.sbn 또는 .sbx)을 이용할 수도 있지만, 현재 이 파일들을 작성하지는 못 합니다.

공간 색인을 (.qix 포맷으로) 생성하려면, 다음과 같은 형식의 SQL 명령어를 발행하십시오:

::

   CREATE SPATIAL INDEX ON tablename [DEPTH N]

이때 선택적인 DEPTH 지정자(specifier)를 사용해서 생성되는 색인 트리 수준의 개수를 제어할 수 있습니다. DEPTH를 생략하면, shapefile에 있는 객체의 개수와 1에서 12까지인 그 값의 범위를 기반으로 트리 심도를 추정합니다.

공간 색인을 삭제하려면, 다음과 같은 형식의 SQL 명령어를 발행하십시오:

::

   DROP SPATIAL INDEX ON tablename

또는, `MapServer <http://mapserver.org>`_ shptree 유틸리티를 사용할 수도 있습니다:

::

   shptree <shpfile> [<depth>] [<index_format>]

이 유틸리티에 관한 더 자세한 정보는 `MapServer shptree 페이지 <http://mapserver.org/utilities/shptree.html>`_ 에서 찾아볼 수 있습니다.

현재 OGR Shapefile 드라이버는 유일 키 열에 있는 특정 값을 검색하기 위한 속성 색인만 지원합니다. 열에 대한 속성 색인을 생성하려면 다음과 같은 형식의 SQL 명령어를 발행하십시오:

::

   CREATE INDEX ON tablename USING fieldname

속성 색인을 삭제하려면, 다음과 같은 형식의 SQL 명령어를 발행하십시오:

::

   DROP INDEX ON tablename

속성 색인은 "fieldname = value" 형식의 WHERE 절 검색의 속도를 향상시킬 것입니다. 속성 색인은 실제로는 MapInfo 포맷 색인으로 저장되며 다른 모든 shapefile 응용 프로그램과 호환되지 않습니다.

생성 문제점
---------------

OGR Shapefile 드라이버는 shapefile 디렉터리를 데이터셋으로, 그리고 각 shapefile 세트(.shp, .shx 및 .dbf)를 레이어로 취급합니다. 디렉터리 이름을 데이터셋 이름으로 취급할 것입니다. 디렉터리가 이미 존재한다면 해당 디렉터리를 사용하고 디렉터리 안에 있는 파일들은 무시합니다. 디렉터리가 존재하지 않는다면 생성할 것입니다.

새 데이터셋을 .shp 확장자로 생성하려 시도하는 특수한 경우에는 디렉터리 대신 단일 파일 세트를 생성할 것입니다.

ESRI shapefile은 레이어(shapefile) 당 한 가지 유형의 도형만 저장할 수 있습니다. 생성 작업 시 이 도형 유형은 (소스 드라이버로부터 일률적인 도형 유형을 전달받은 경우) 소스 파일을 기반으로 설정될 수도 있고, 또는 사용자가 (아래에서 설명하는) SHPT 레이어 생성 옵션으로 직접 설정할 수도 있습니다. 이 옵션을 설정하지 않으면 레이어 생성이 실패할 것입니다. 레이어에 호환되지 않는 도형 유형을 생성하는 경우, 산출 작업이 오류와 함께 중단될 것입니다.

이런 이유 때문에 ogr2ogr 유틸리티를 이용해서 또다른 포맷의 혼합 도형 레이어를 Shapefile 포맷으로 변환하는 작업이 아주 어려워질 수도 있다는 사실을 기억하십시오. ogr2ogr 유틸리티는 소스 레이어로부터 도형들을 분리하는 기능을 지원하지 않기 때문입니다. 이에 대한 해결법은 `FAQ <http://trac.osgeo.org/gdal/wiki/FAQVector#HowdoItranslateamixedgeometryfiletoshapefileformat>`_ 를 읽어보십시오.

Shapefile 포맷의 객체 속성이 관련 .dbf 파일에 저장되기 때문에, 속성에 여러 제한이 적용됩니다:

-  속성 이름이 문자 10개 길이를 넘어서는 안 됩니다. OGR Shapefile 드라이버는 유일한 필드명을 생성하려 시도하는데, 절단으로 인해 문자 10개로 줄어든 필드명을 포함하는 연속 중복 필드명을 문자 8개 길이로 절단하고 그 뒤에 1에서 99까지의 일련 번호를 붙일 것입니다.

   예시:

   -  a → a, a → a_1, A → A_2;
   -  abcdefghijk → abcdefghij, abcdefghijkl → abcdefgh_1

-  Integer, Integer64, Real, String 및 (DateTime 유형이 아닌 그냥 연-월-일 형식의) Date 필드 유형만 지원합니다. 다양한 목록 및 바이너리 필드 유형을 생성할 수 없습니다.

-  .dbf 파일에 저장 용량을 확립하기 위해 필드 길이 및 정밀도를 직접 사용합니다. 즉 필드 길이보다 긴 문자열, 또는 지정된 필드 서식에 들어맞지 않는 숫자를 절단할 것이라는 뜻입니다.

-  길이가 명확하게 설정되지 않은 Integer 필드 유형을 문자 9개 길이로 취급하고, 필요한 경우 10개 또는 11개로 늘입니다.

-  길이가 명확하게 설정되지 않은 Integer64 필드 유형을 문자 18개 길이로 취급하고, 필요한 경우 19개 또는 20개로 늘입니다.

-  길이가 명확하게 설정되지 않은 Real (부동소수점형) 필드 유형을 소수점 이하 자릿수가 15개인 정밀도를 가진 문자 24개 길이로 취급합니다.

-  할당된 길이가 없는 문자열 필드 유형을 문자 80개 길이로 취급합니다.

또한, .dbf 파일은 최소한 필드 하나를 가져야 합니다. 응용 프로그램이 필드를 하나도 생성하지 않았다면 "FID" 필드를 자동으로 생성하고 레코드 번호로 채울 것입니다.

OGR Shapefile 드라이버는 shapefile에 있는 기존 도형(shape) 재작성은 물론 도형 삭제도 지원합니다. 삭제된 파일은 .dbf 파일에 삭제되었다고 표시하고, 다음부터 OGR가 무시합니다. 실제로 도형을 영구 제거하려면 (FID를 다시 매기게 됩니다) 데이터소스 ExecuteSQL() 메소드를 통해 'REPACK <tablename>' SQL 선언문을 발행해야 합니다.

객체 도형(geometry)이 SetFeature() 메소드로 수정된 경우 REPACK 절은 .shp 파일을 재작성하게 만들고, .shp 파일에 있는 도형의 바이너리 인코딩 용량을 변경시킵니다.

GDAL 2.2버전부터, 파일을 닫을 때 또는 FlushCache()/SyncToDisk() 메소드를 호출할 때 REPACK 절도 자동 호출합니다. 구멍을 가진 shapefile은 다른 소프트웨어들과 상호 호환성 문제를 일으키기 때문입니다.

필드 크기
-----------

이 드라이버는 삽입되는 데이터의 길이에 대해 충분한 공간을 동적으로 제공하기 위해 문자열 및 정수형 필드의 길이를 (DBF 포맷이 강요하는 255바이트 제한까지) 자동으로 늘릴 수 있습니다.

데이터소스 ExecuteSQL() 메소드를 통해 'RESIZE <tablename>' SQL 선언문을 발행해서 필드를 최적 길이로 강제 크기 조정할 수도 있습니다. (문자열 필드의 경우 문자 80개인) 기본 열 길이가 필요 이상으로 긴 경우 이 방법이 유용합니다.

공간 범위
--------------

Shapefile 포맷은 .shp 파일에 레이어 공간 범위를 저장합니다. shapefile에 새 객체를 삽입하는 경우 레이어 공간 범위를 자동으로 업데이트합니다. 하지만 기존 객체를 업데이트할 때 이전 도형(shape)이 레이어 범위 경계 상자와 접하는데 업데이트된 도형은 새 범위와 접하지 않는다면 계산된 범위가 정확하지 않을 것입니다. 이런 경우 데이터소스 ExecuteSQL() 메소드를 통해 'RECOMPUTE EXTENT ON <tablename>' SQL 선언문을 발행해서 강제로 다시 계산하게 해야 합니다. 도형을 삭제하는 경우에도 마찬가지입니다.

용량 문제점
-----------

-  도형:
   Shapefile 포맷은 명확하게 32비트 오프셋을 사용하기 때문에 8GB를 초과할 수 없지만 (실제로 16비트 워드(word)에 32비트 오프셋을 사용합니다) OGR shapefile 구현은 4GB로 제한되어 있습니다.

-  속성:
   DBF 포맷에는 오프셋이 없기 때문에 임의의 용량으로 커질 수 있습니다.

2GB_LIMIT 레이어 생성 옵션을 YES로 설정하면 2GB 제한을 엄격하게 강제할 수 있습니다. 업데이트 모드의 경우, :decl_configoption:`SHAPE_2GB_LIMIT` 환경설정 옵션을 YES로 설정해서 비슷한 효과를 볼 수 있습니다. 아무것도 설정하지 않는 경우 2GB 제한에 도달할 때 경고를 발할 것입니다.

압축 파일
----------------

GDAL 3.1버전부터, 이 드라이버는 (단일 레이어의 .shp, .shx, .dbf 및 기타 사이드카 파일을 담고 있는 ZIP 압축 파일인) .shz 파일과 (하나 이상의 레이어를 담고 있는 ZIP 압축 파일인) .shp.zip 파일도 읽고, 생성하고, 편집할 수 있습니다. 생성 및 편집 작업 시 임시 파일을 생성합니다.

열기 옵션
------------

다음 열기 옵션들을 사용할 수 있습니다:

-  **ENCODING=encoding_name**:
   shapefile의 인코딩 해석을 CPLRecode가 지원하는 어떤 인코딩으로든 대체할 수도 있고, 또는 이 옵션을 ""로 설정해서 재 인코딩을 막을 수도 있습니다.

-  **DBF_DATE_LAST_UPDATE=YYYY-MM-DD**:
   DBF 헤더에 연-월-일 서식으로 작성할 수정일입니다. 지정하지 않는 경우 현재 날짜를 사용합니다.

-  **ADJUST_TYPE=YES/NO**:
   이 옵션을 YES로 설정하면 .dbf 파일 전체를 읽어와서 가능한 경우 Real 필드 유형을 Integer/Integer64 유형으로 또는 Integer64 필드 유형을 Integer 유형으로 수정합니다. 기본값은 NO입니다. 필드 길이가 명확하지 않은데 OGR가 기본적으로 더 큰 데이터 유형을 선택할 것 같을 때 이 옵션을 사용할 수 있습니다.
   예를 들어 소수점 이하 자릿수가 0이고 길이가 문자 10개 또는 11개인 숫자형 필드는 Integer 또는 Integer64 데이터 유형을, 길이가 문자 19개 또는 20개인 숫자형 필드는 Integer64 또는 (Real 필드 유형으로 담기게 되는) 더 큰 정수형을 담을 수 있습니다.

-  **ADJUST_GEOM_TYPE=NO/FIRST_SHAPE/ALL_SHAPES**: (GDAL 2.1 이상 버전)
   특히 M 차원에 상위(significant) 값을 가지고 있는 도형(shape)을 가진 shapefile과 M 값이 NODATA 값으로 설정된 shapefile을 구별하기 위해 레이어 도형 유형을 계산하는 방법을 정의합니다.
   기본값 FIRST_SHAPE으로 지정하면, 드라이버가 첫 번째 도형을 읽고 M 값을 가지고 있는 경우 해당 레이어가 M 차원을 가지고 있다고 노출시킬 것입니다.
   ALL_SHAPES로 지정하면, 드라이버가 무결한 M 값을 가지고 있는 도형을 찾을 때까지 객체를 반복해서 적절한 레이어 유형을 결정할 것입니다.

-  **AUTO_REPACK=YES/NO**: (OGR 2.2 이상 버전) GDAL 2.2버전에서 기본값은 YES입니다.
   데이터셋을 닫을 때 또는 FlushCache()/SyncToDisk() 메소드를 호출할 때 필요한 경우 shapefile에 REPACK 절을 자동으로 발행할지 여부를 선택합니다.

-  **DBF_EOF_CHAR=YES/NO**: (OGR 2.2 이상 버전) GDAL 2.2버전에서 기본값은 YES입니다.
   DBF 사양에서와 같이 그리고 다른 소프트웨어 회사들이 그러듯이 .dbf 파일을 0x1A 파일 끝(end-of-file) 문자로 중단시킬 것인지 여부를 선택합니다. 이전 GDAL 버전들에서는 이 문자를 작성하지 않았습니다.

데이터셋 생성 옵션
------------------------

없음

레이어 생성 옵션
----------------------

-  **SHPT=type**: 생성되는 shapefile의 유형을 대체합니다.

   -  .shp 파일이 없는 단순 .dbf 파일의 경우 NULL,
   -  2차원 도형의 경우 POINT, ARC, POLYGON 또는 MULTIPOINT,
   -  3차원 도형의 경우 POINTZ, ARCZ, POLYGONZ, MULTIPOINTZ 또는 MULTIPATCH,
   -  측정 도형의 경우 POINTM, ARCM, POLYGONM 또는 MULTIPOINTM,
   -  3차원 측정 도형의 경우 POINTZM, ARCZM, POLYGONZM 또는 MULTIPOINTZM
   
   가운데 하나로 설정할 수 있습니다.
   측정 지원은 GDAL 2.1버전에서 추가되었습니다.
   MULTIPATCH 파일은 GDAL 2.2버전부터 지원했습니다.

-  **ENCODING=value**:
   DBF 파일에 인코딩 값을 설정합니다. 기본값은 "LDID/87"입니다. 다른 값들이 적절할 수 있는지는 명확하지 않습니다.

-  **RESIZE=YES/NO**:
   이 옵션을 YES로 설정하면 필드를 자신의 최적 길이로 크기 조정합니다. 앞의 "필드 크기" 단락을 읽어보십시오. 기본값은 NO입니다.

-  **2GB_LIMIT=YES/NO**:
   이 옵션을 YES로 설정하면 .shp 파일 또는 .dbf 파일의 용량을 2GB로 제한합니다. 기본값은 NO입니다.

-  **SPATIAL_INDEX=YES/NO**:
   이 옵션을 YES로 설정하면 공간 색인(.qix 파일)을 생성합니다. 기본값은 NO입니다.

-  **DBF_DATE_LAST_UPDATE=YYYY-MM-DD**:
   DBF 헤더에 연-월-일 서식으로 작성할 수정일입니다. 지정하지 않는 경우 현재 날짜를 사용합니다.
   주의: 과거 GDAL 배포판들의 습성은 현재 날짜가 아니라 1995-07-26을 작성하는 것이었습니다.

-  **AUTO_REPACK=YES/NO**: (OGR 2.2 이상 버전) GDAL 2.2버전에서 기본값은 YES입니다.
   데이터셋을 닫을 때 또는 FlushCache()/SyncToDisk() 메소드를 호출할 때 필요한 경우 shapefile에 REPACK 절을 자동으로 발행할지 여부를 선택합니다.

-  **DBF_EOF_CHAR=YES/NO**: (OGR 2.2 이상 버전) GDAL 2.2버전에서 기본값은 YES입니다.
   DBF 사양에서와 같이 그리고 다른 소프트웨어 회사들이 그러듯이 .dbf 파일을 0x1A 파일 끝(end-of-file) 문자로 중단시킬 것인지 여부를 선택합니다. 이전 GDAL 버전들에서는 이 문자를 작성하지 않았습니다.

환경설정 옵션
---------------------

다음 :ref:`환경설정 옵션들 <configoptions>` 을 사용할 수 있습니다:

-  :decl_configoption:`SHAPE_REWIND_ON_WRITE`:
   이 옵션을 NO로 설정하면 shapefile 작성기가 외곽/내곽 고리의 돌아가는 방향을 Shapefile 사양이 요구하는 방향을 준수하도록 수정하는 것을 막을 수 있습니다. shapefile 작성기에 전송된 멀티폴리곤이 단일 피처(Single Feature) 규범을 준수하는 폴리곤은 아니지만 (Shapefile/FileGDB/PGeo 데이터소스로부터 나온) 멀티패치 객체 예시를 기반으로 생성된 폴리곤인 경우 이 옵션이 유용할 수 있습니다.

-  :decl_configoption:`SHAPE_RESTORE_SHX`: (GDAL 2.1 이상 버전)
   이 옵션을 YES로 설정하면 파일을 여는 동안 관련 .shp 파일로부터 망가졌거나 사라진 .shx 파일을 복구할 수 있습니다. 기본값은 NO입니다.

-  :decl_configoption:`SHAPE_2GB_LIMIT`:
   이 옵션을 YES로 설정하면 shapefile 업데이트 시 파일 용량을 2GB로 엄격히 제한합니다. 아무것도 설정하지 않는 경우 2GB 제한에 도달할 때 경고를 발할 것입니다.

-  :decl_configoption:`OGR_ORGANIZE_POLYGONS`:
   이 옵션을 DEFAULT로 설정하면 폴리곤 부분들의 위상 관계를 기반으로 전체 분석을 수행, 모든 폴리곤 고리의 돌아가는 방향이 OGC 단순 피처(Simple Feature) 규범을 정확하게 준수하도록 할 수 있습니다.

-  :decl_configoption:`SHAPE_ENCODING`:
   이 옵션으로 shapefile의 인코딩 해석을 CPLRecode가 지원하는 어떤 인코딩으로든 대체할 수도 있고, 또는 이 옵션을 ""로 설정해서 재 인코딩을 막을 수도 있습니다.

예시
--------

-  'file1.shp' 및 'file2.shp' 두 shapefile을 새 'file_merged.shp' 파일로 병합시키는 작업은 다음과 같이 수행됩니다:

   ::

      ogr2ogr file_merged.shp file1.shp
      ogr2ogr -update -append file_merged.shp file2.shp -nln file_merged

   두 번째 명령어가 file_merged.shp 파일을 업데이트 모드로 열어서, 기존 레이어를 찾아 복사된 객체들을 추가하려 시도합니다.

   '-nln' 옵션은 복사해넣을 레이어의 이름을 설정합니다.

-  공간 색인 작성하기:

   ::

      ogrinfo file1.shp -sql "CREATE SPATIAL INDEX ON file1"

-  .dbf 파일의 열들을 최적 길이로 크기 조정하기:

   ::

      ogrinfo file1.dbf -sql "RESIZE file1"

참고
--------

-  `Shapelib 페이지 <http://shapelib.maptools.org/>`_
-  `OGR Shapefile 드라이버에 대한 사용자 메모 <http://trac.osgeo.org/gdal/wiki/UserDocs/Shapefiles>`_

