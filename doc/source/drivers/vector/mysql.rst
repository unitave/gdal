.. _vector.mysql:

MySQL
=====

.. shortname:: MySQL

.. build_dependencies:: MySQL 라이브러리

MySQL 드라이버는 `MySQL <http://www.mysql.org/>`_ 테이블에 있는 공간 데이터에 대한 읽기 및 쓰기 접근을 구현합니다.

데이터베이스를 열 때, 데이터베이스 이름을 "MYSQL:dbname[,options]" 형식으로 지정해야 합니다. 이때 [,options] 자리에 "user=*userid*", "password=*password*", "host=*host*" 및 "port=*port*" 같은 항목을 쉼표로 구분해서 넣을 수 있습니다.

또한 데이터베이스에 있는 특정 테이블에 접근하려면 "tables=*table*;*table*..." 옵션을 추가하면 됩니다. 데이터베이스에 수많은 테이블이 존재하기 때문에 모든 테이블의 스키마를 스캐닝하는 시간이 상당히 오래 걸리는 경우 이 옵션이 특히 유용합니다.

현재 모든 정규 사용자 테이블을 OGR 시점에서 레이어로 가정합니다. 이때 테이블 이름이 레이어 이름이 됩니다. 이름을 가진 뷰는 현재 지원하지 않습니다.

단일 정수형 필드가 기본 키인 경우 FID로 사용할 것입니다. 그렇지 않다면 FID를 순차적으로 할당하는데, FID로 가져오는 속도가 매우 느릴 것입니다.

기본적으로 MySQL 데이터베이스 엔진에 SQL 선언문을 직접 전송합니다. ExecuteSQL() 메소드에 **"OGRSQL"** 문자열을 SQL 방언 이름으로 전송해서 MySQL 드라이버가 SQL 선언문을 :ref:`OGR SQL <ogr_sql_dialect>` 엔진으로 처리하도록 요청할 수도 있습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_create::

.. supports_georeferencing::

주의할 점
-------

-  SQL 선언문으로 정의되는 레이어의 경우, "OGC_FID"로 명명된 필드 또는 NOT NULL로 정의된 필드를 PRIMARY KEY로 그리고 유사 정수형 필드를 FID로 가정할 것입니다.

-  WKB 포맷을 이용해서 MySQL로부터 도형 필드를 읽어옵니다. MySQL 5.0.16 이전 버전들은 WKB 생성 관련 문제점을 가지고 있는 것으로 알려져 있기 때문에 제대로 작동하지 않을 수도 있습니다.

-  MYSQL_FID 레이어 생성 옵션으로 대체할 수 있는 OGR_FID 열은 **INT UNIQUE NOT NULL AUTO_INCREMENT** 필드로 구현되었습니다. 이렇게 하면 필드에 내재적으로 색인을 생성한 것으로 나타납니다.

-  기본 이름이 *SHAPE* 이고 GEOMETRY_NAME 레이어 생성 옵션으로 대체할 수 있는 도형 열은 SPATIAL_INDEX를 비활성화하지 않은 이상 **NOT NULL** 열로 생성됩니다. 기본적으로 테이블을 생성하는 순간 공간 색인을 생성합니다.

-  SQL 레이아웃에 OGC 단순 피처(Simple Feature)를 이용해서 공간 좌표계를 저장합니다. 지정한 데이터베이스에 이미 *geometry_columns* 및 *spatial_ref_sys* 메타데이터 테이블이 없다면 두 테이블을 생성합니다. PostGIS처럼 사전에 *spatial_ref_sys* 테이블을 공간 좌표계 및 EPSG 값들로 채우지 **않습니다**. 지정한 테이블에 EPSG 코드가 하나도 없는 경우 MAX(SRID) 값을 사용합니다. MySQL 8.0버전부터, *spatial_ref_sys* 메타데이터 테이블 대신 데이터베이스가 제공하는 *ST_SPATIAL_REFERENCE_SYSTEMS* 테이블을 사용합니다.

-  **MYSQL_TIMEOUT** 환경 변수로 -- 예를 들어 ``MYSQL_TIMEOUT=3600`` 처럼 -- 서버 연결 시간 제한을 지정할 수 있습니다. 이 변수는 MySQL 서버의 OS가 윈도우인 경우에만 영향을 미칠 수도 있습니다.

-  MySQL 드라이버는 CLIENT_INTERACTIVE 모드를 사용해서 서버에 연결을 엽니다. 사용자 서버의 mysql.ini 또는 mysql.cnf 파일에 있는 이 (interactive_timeout) 설정을 사용자 마음대로 조정할 수 있습니다.

-  WKT를 이용해서 데이터베이스에 도형을 삽입하지 않습니다. 대용량 도형을 삽입하는 경우, MySQL 환경설정에 있는 *max_allowed_packet* 파라미터를 신경써야 할 것입니다. 이 파라미터는 기본적으로 1MB로 설정되어 있지만, 도형이 정말로 대용량인 경우 충분하지 않을 것입니다. "Got a packet bigger than 'max_allowed_packet' bytes" 같은 오류 메시지가 뜰 경우, 이 파라미터의 값을 높여야 할 것입니다.

생성 문제점
---------------

MySQL 드라이버는 새 데이터셋(MySQL 내부의 데이터베이스) 생성을 지원하지 않지만, 기존 데이터베이스 안에 새 레이어를 생성할 수는 있습니다.

MySQL 드라이버는 기본적으로 MySQL 레이어를 생성하고 읽어올 때 OGR 객체의 정밀도를 보전하려 시도할 것입니다. 길이가 지정된 정수형 필드의 경우, 정밀도가 0으로 지정된 **DECIMAL** 을 MySQL 필드 유형으로 사용할 것입니다. 실수형 필드의 경우, 길이 및 정밀도가 지정된 **DOUBLE** 을 사용할 것입니다. 길이가 지정된 문자열 필드의 경우, **VARCHAR** 를 사용할 것입니다.

MySQL 드라이버는 현재 문자 인코딩을 허용하지 않습니다.

MySQL 드라이버는 현재 트랜잭션도 허용하지 않습니다.

레이어 생성 옵션
~~~~~~~~~~~~~~~~~~~~~~

-  **OVERWRITE**:
   요청한 레이어를 생성하기 전에 요청한 이름을 가진 기존 레이어를 강제로 삭제하고 싶다면 이 옵션을 YES로 설정할 수도 있습니다.

-  **LAUNDER**:
   해당 레이어에 생성되는 새 필드의 이름을 MySQL과 좀 더 호환되는 형식으로 강제 "세탁"하려면 이 옵션을 YES로 설정할 수도 있습니다. 이 옵션은 대문자를 소문자로 변환하고, "-" 및 "#" 같은 몇몇 특수 문자를 "_"로 변환합니다. 이 옵션을 NO로 설정하면 이름을 그대로 보전합니다. 기본값은 YES입니다.

-  **PRECISION**:
   MySQL 레이어의 생성 및 읽기를 위해 길이 및 정밀도 정보를 보전하려 시도하려면 이 옵션을 TRUE로 설정할 수도 있습니다. 기본값은 TRUE입니다.

-  **GEOMETRY_NAME**:
   도형 열 이름을 설정합니다. 기본값은 'SHAPE'입니다.

-  **FID**:
   FID 열의 이름을 지정합니다. 기본값은 'OGR_FID'입니다.
   주의: GDAL 2 이전 배포판들에서는 이 옵션이 MYSQL_FID였습니다.

-  **FID64**:
   64비트 길이의 식별자를 지원할 수 있는 FID 열을 생성하려면 이 옵션을 TRUE로 설정할 수도 있습니다. 기본값은 FALSE입니다.

-  **SPATIAL_INDEX**:
   도형 열에 공간 색인을 자동 생성하지 않으려면 이 옵션을 NO로 설정할 수도 있습니다.
   이 경우 NULL 도형을 허용하며, 불러오기가 더 빨라질 수도 있습니다.

-  **ENGINE**:
   사용할 데이터베이스 엔진을 지정할 수 있는 선택적 옵션입니다. MySQL 4.x버전에서 공간 테이블을 사용하려면 이 옵션을 반드시 MyISAM으로 설정해야만 합니다.

예시
----

-  다음 예시 데이터소스 이름은 *3306* 포트에서 *root* 사용자명과 *psv9570* 비밀번호로 *westholland* 데이터베이스 스키마를 엽니다. 호스트명을 지정하지 않았기 때문에 localhost로 가정합니다. 'tables=directive'는 bedrijven 테이블만 스캔해서 사용할 레이어로 나타낸다는 의미입니다:

::

   MYSQL:westholland,user=root,password=psv9570,port=3306,tables=bedrijven

-  다음 예시는 ogr2ogr 유틸리티를 이용해서 shapefile의 world_borders 레이어를 MySQL 테이블로 생성/복사합니다. 기존 *borders2* 테이블이 존재하는 경우 덮어쓰고, 레이어 생성 옵션으로 도형 열 이름을 *SHAPE2* 로 지정합니다:

::

   ogr2ogr -f MySQL MySQL:test,user=root world_borders.shp -nln borders2 -update -overwrite -lco GEOMETRY_NAME=SHAPE2

-  다음 예시는 ogrinfo 유틸리티를 이용해서 test 데이터베이스에 있는 borders2 레이어에 관한 몇몇 요약 정보를 반환합니다:

::

   ogrinfo MySQL:test,user=root borders2 -so

       Layer name: borders2
       Geometry: Polygon
       Feature Count: 3784
       Extent: (-180.000000, -90.000000) - (180.000000, 83.623596)
       Layer SRS WKT:
       GEOGCS["GCS_WGS_1984",
           DATUM["WGS_1984",
               SPHEROID["WGS_84",6378137,298.257223563]],
           PRIMEM["Greenwich",0],
           UNIT["Degree",0.017453292519943295]]
       FID Column = OGR_FID
       Geometry Column = SHAPE2
       cat: Real (0.0)
       fips_cntry: String (80.0)
       cntry_name: String (80.0)
       area: Real (15.2)
       pop_cntry: Real (15.2)

