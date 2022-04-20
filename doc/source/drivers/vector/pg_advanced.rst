.. _vector.pg_advanced:

PostgreSQL / PostGIS - 고급 드라이버 정보
==================================================

이 페이지에 수집된 정보는 :ref:`OGR PostgreSQL 드라이버 정보 <vector.pg>` 페이지에서 찾을 수 없는 고급 주제들을 다루고 있습니다.

스키마 및 테이블 관련 연결 옵션
------------------------------------------------

이전 버전들보다 데이터베이스를 여는 속도가 훨씬 빨라졌을 것이기 때문에, 'tables=' 또는 'schemas=' 옵션을 사용해도 속도가 크게 향상되지는 않을 것입니다.

연결 문자열 안에 ``tables=[schema.]table[(geom_column_name)][,[schema2.]table2[(geom_column_name2)],...]`` 을 지정하면 스캔할 테이블 집합을 대체할 수 있습니다. 이 파라미터가 존재하는 경우, 드라이버는 다음 절에 서술된 테이블 목록을 건너뜁니다.

테이블 목록을 확립하는 동안 스캔하게 될 스키마를 제약할 수도 있습니다. 연결 문자열 안에 ``schemas=schema_name[,schema_name2]`` 를 지정하면 됩니다. 스키마가 아주 많이 있는 경우 이렇게 하면 PostgreSQL 데이터베이스에 연결하는 속도가 더 빨라질 수도 있습니다. 스키마 목록에 스키마 하나만 지정하면, 해당 스키마를 자동적으로 활성 스키마로 사용할 것입니다. (그리고 스키마 이름을 레이어 이름 앞에 접두어로 붙이지 않을 것입니다.) 스키마를 여러 개 지정하는 경우, 'active_schema=' 옵션으로 달리 지정하지 않는 이상 활성 스키마는 계속 'public'입니다.

연결 문자열 안에 ``active_schema=schema_name`` 을 지정하면 (기본값이 'public'인) 활성 스키마를 대체할 수 있습니다. 활성 스키마란 테이블 이름 앞에 스키마 이름이 명확하게 접두어로 붙지 않아도 테이블 생성 또는 검색 대상이 되는 스키마를 말합니다. 기본 활성 스키마를 대체하더라도 목록화될 테이블을 제약하지 않는다는 사실을 기억하십시오. (앞의 'schemas=' 옵션을 참조하십시오.) 테이블 목록을 가져올 때, 이 활성 스키마 안에 있는 테이블 이름 앞에 스키마 이름이 접두어로 붙지 않을 것입니다. 예를 들어 공개 스키마 안에 'foo' 테이블이 있고 'bar_schema' 안에도 'foo' 테이블이 있는데 'active_schema=bar_schema'를 지정한 경우, ('bar_schema' 안에 있다는 사실을 암시하는) 'foo' 레이어와 'public.foo' 레이어 2개가 목록화될 것입니다.

다중 도형 열
-------------------------

PostgreSQL 드라이버는 PostGIS 도형 열을 여러 개 가지고 있는 테이블에 접근을 지원합니다.

OGR는 (:ref:`rfc-41` 에 따라) PostGIS 도형 열을 여러 개 가진 테이블의 읽기, 업데이트, 생성을 지원합니다. 이런 테이블의 경우, 도형 필드를 테이블에 있는 도형 열의 개수만큼 가진 단일 OGR 레이어를 리포트할 것입니다.

하위 호환성을 위해 GetLayerByName() 메소드를 'foo(bar)' 같은 서식으로 된 이름으로 호출해서 레이어를 쿼리할 수도 있습니다. 이때 'foo'가 테이블 이름이고 'bar'는 도형 열 이름입니다.

레이어
------

PostGIS가 활성화되었더라도, 사용자가 다음 환경 변수를 정의하면

::

   PG_LIST_ALL_TABLES=YES

(그리고 'tables=' 를 지정하지 않으면) 정규 사용자 테이블 및 명명된 뷰를 모두 레이어로 취급할 것입니다. 하지만, 도형 열 여러 개를 가진 테이블은 오직 이 모드에서만 리포트될 것입니다. 즉 주로 공간 데이터를 가지지 않은 테이블 또는 'geometry_columns' 테이블에 항목이 없는 뷰를 찾기 위해 PostGIS를 활성화시킨 경우 이 환경 변수가 유용합니다.

어떤 경우든, GetLayerByName() 메소드로 모든 사용자 테이블을 명확하게 쿼리할 수 있습니다.

정규 (비공간) 테이블에 접근할 수 있고, 속성을 가진 객체를 반환하지만 도형은 반환하지 않을 것입니다. 해당 테이블이 "wkb_geometry" 필드를 가지고 있는 경우 공간 테이블로 취급할 것입니다. 필드를 어떻게 읽어올지 결정하기 위해 필드 유형을 조사합니다. OGC WKT 형식으로 다시 반환될 것으로 간주되는 PostGIS **geometry** 필드일 수도 있고, 또는 BYTEA 또는 OID 필드 유형일 수도 있는데 이 경우 OGC WKB 도형의 소스로 사용합니다.

공간 테이블을 상속받은 테이블을 지원합니다.

"ogc_fid" 필드가 존재하는 경우 객체의 FID를 설정하는 데 사용하고 정규 필드로 취급하지는 않을 것입니다.

레이어 이름이 "schema.table" 형식일 수도 있습니다. 이때 해당 스키마는 반드시 존재해야만 하고, 사용자가 대상 및 공개 스키마에 대한 쓰기 권한을 가지고 있어야 합니다.

사용자가 다음 환경 변수를 정의하면

::

   PG_SKIP_VIEWS=YES

(그리고 'tables=' 를 지정하지 않으면) 정규 사용자 테이블만 레이어로 취급할 것입니다. 기본 습성은 뷰를 포함시키는 것입니다. 뷰로부터 불필요한 데이터를 가져오지 않으면서 데이터를 다른 포맷으로 복사하려는 경우 이 환경 변수가 특히 유용합니다.

명명된 뷰
-----------

접속한 데이터베이스에 대해 PostGIS가 활성화되었다면, 'geometry_columns' 테이블에 해당 뷰 항목이 있다는 가정 하에 명명된 뷰를 지원합니다. 하지만 AddGeometryColumn() SQL 함수가 뷰에 대한 항목을 추가하는 것을 허용하지 않는다는 사실을 기억하십시오. (정규 테이블 항목만 받아들입니다.) 따라서, 일반적으로 다음과 같은 SQL 선언문으로 직접 추가해줘야만 합니다:

::

   "INSERT INTO geometry_columns VALUES ( '', 'public', 'name_of_my_view', 'name_of_geometry_column', 2, 4326, 'POINT');"

명명된 뷰를 'geometry_columns' 테이블에 행을 삽입하지 않고 사용할 수도 있습니다. 이렇게 하려면, 연결 문자열의 "tables=" 옵션에 뷰 이름을 명확하게 지정해야 합니다. 첫 단락을 참조하십시오. 이 방법의 단점은 OGR가 무결한 공간 좌표계를 리포트할 수 없고 알맞은 도형 유형을 판단하지 못 할 것이라는 점입니다.

새로 삽입된 객체의 FID 가져오기
----------------------------------------

복사 모드 이외의 모드에서, CreateFeature() 메소드로 테이블에 삽입되는 (예를 들면 일반적으로 객체의 OGC_FID 열의 값인) 객체의 FID를 데이터베이스로부터 가져오는데 이때 GetFID() 메소드로 FID를 얻을 수 있습니다. 이 새로운 습성의 부작용 가운데 한 가지는 삽입을 만드는 루프에서 동일한 피처 객체를 재사용하는 경우 주의해야만 한다는 것입니다. 첫 번째 반복 이후, FID가 NULL이 아닌 값으로 설정되기 때문에 두 번째 반복 시 CreateFeature() 메소드가 이전 객체의 FID로 새 객체를 삽입하려 시도할 것입니다. 이 경우 동일한 FID를 가진 객체를 2개 삽입할 수 없기 때문에 실패할 것입니다. 따라서 이 경우 CreateFeature() 메소드를 호출하기 전에 FID를 명확하게 리셋하거나 또는 전과 다른 피처 객체를 사용해야만 합니다.

다음은 이런 경우의 파이썬 코드 조각 예시입니다:

::

       feat = ogr.Feature(lyr.GetLayerDefn())
       for i in range(100):
           feat.SetFID(-1)  # Reset FID to null value
           lyr.CreateFeature(feat)
           print('The feature has been assigned FID %d' % feat.GetFID())

또는:

::

       for i in range(100):
           feat = ogr.Feature(lyr.GetLayerDefn())
           lyr.CreateFeature(feat)
           print('The feature has been assigned FID %d' % feat.GetFID())

:decl_configoption:`OGR_PG_RETRIEVE_FID` 환경설정 옵션을 FALSE로 설정하면 예전의 GDAL 습성을 부활시킬 수 있습니다.

트랜잭션 문제점
------------------------

PostgreSQL에서 순차 읽기를 효율적으로 하려면 트랜잭션 안에서 해야 합니다. (기술적으로 따지면 "CURSOR WITHOUT HOLD"입니다.) 즉 객체를 가져왔을 때 열려 있는 트랜잭션이 없는 경우 PostgreSQL 드라이버가 암묵적으로 순차 읽기를 위한 트랜잭션을 열 것입니다. (다른 레이어를 계속 읽어오는 중이 아니라는 가정 하에) 이 트랜잭션은 ResetReading() 메소드를 호출하면 해제될 것입니다.

이런 암묵적인 트랜잭션 안에서 데이터셋 수준 StartTransaction() 메소드가 명확하게 호출되는 경우, PostgreSQL 드라이버는 읽어오는 레이어 상에 활성 커서를 계속 열어놓은 채 트랜잭션 습성을 제대로 모방하기 위해 "SAVEPOINT"를 사용할 것입니다.

레이어를 읽어오기 전에 데이터셋 수준 StartTransaction()으로 트랜잭션을 명확하게 열었다면, 이 트랜잭션을 이용해서 레이어에 커서를 반복할 것입니다. 트랜잭션을 명확하게 커밋하거나 롤백하는 경우, 커서가 무결하지 않게 될 것입니다. 이때 ResetReading()을 다시 호출해서 처음부터 읽기를 다시 시작해야 합니다.

SetAttributeFilter() 또는 SetSpatialFilter() 메소드를 호출한다는 것은 암묵적으로 ResetReading()을 호출한다는 의미이기 때문에, 이 메소드들도 ResetReading()과 동일한 영향을 미칩니다. 다시 말해서 암묵적인 트랜잭션이 진행 중일 때 SetAttributeFilter() 또는 SetSpatialFilter() 메소드를 호출하면 (다른 레이어를 읽어오는 중이 아닌 경우) 트랜잭션을 커밋하고 다음 GetNextFeature() 호출 시 새 트랜잭션을 다시 시작할 것입니다. 그 반대로 명확한 트랜잭션 안에서 SetAttributeFilter() 또는 SetSpatialFilter() 메소드를 호출하는 경우 트랜잭션을 유지합니다.

앞의 이런 규칙을 따라, 다음 예시들은 서로 다른 시나리오 상에서 OGR API를 사용할 때 실행되는 SQL 지침을 보여줍니다:

::


   lyr1->GetNextFeature()             BEGIN (implicit)
                                      DECLARE cur1 CURSOR FOR SELECT * FROM lyr1
                                      FETCH 1 IN cur1

   lyr1->SetAttributeFilter('xxx')
        --> lyr1->ResetReading()      CLOSE cur1
                                      COMMIT (implicit)

   lyr1->GetNextFeature()             BEGIN (implicit)
                                      DECLARE cur1 CURSOR  FOR SELECT * FROM lyr1 WHERE xxx
                                      FETCH 1 IN cur1

   lyr2->GetNextFeature()             DECLARE cur2 CURSOR  FOR SELECT * FROM lyr2
                                      FETCH 1 IN cur2

   lyr1->GetNextFeature()             FETCH 1 IN cur1

   lyr2->GetNextFeature()             FETCH 1 IN cur2

   lyr1->CreateFeature(f)             INSERT INTO cur1 ...

   lyr1->SetAttributeFilter('xxx')
        --> lyr1->ResetReading()      CLOSE cur1
                                      COMMIT (implicit)

   lyr1->GetNextFeature()             DECLARE cur1 CURSOR  FOR SELECT * FROM lyr1 WHERE xxx
                                      FETCH 1 IN cur1

   lyr1->ResetReading()               CLOSE cur1

   lyr2->ResetReading()               CLOSE cur2
                                      COMMIT (implicit)

   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   ds->StartTransaction()             BEGIN

   lyr1->GetNextFeature()             DECLARE cur1 CURSOR FOR SELECT * FROM lyr1
                                      FETCH 1 IN cur1

   lyr2->GetNextFeature()             DECLARE cur2 CURSOR FOR SELECT * FROM lyr2
                                      FETCH 1 IN cur2

   lyr1->CreateFeature(f)             INSERT INTO cur1 ...

   lyr1->SetAttributeFilter('xxx')
        --> lyr1->ResetReading()      CLOSE cur1
                                      COMMIT (implicit)

   lyr1->GetNextFeature()             DECLARE cur1 CURSOR  FOR SELECT * FROM lyr1 WHERE xxx
                                      FETCH 1 IN cur1

   lyr1->ResetReading()               CLOSE cur1

   lyr2->ResetReading()               CLOSE cur2

   ds->CommitTransaction()            COMMIT

   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   ds->StartTransaction()             BEGIN

   lyr1->GetNextFeature()             DECLARE cur1 CURSOR FOR SELECT * FROM lyr1
                                      FETCH 1 IN cur1

   lyr1->CreateFeature(f)             INSERT INTO cur1 ...

   ds->CommitTransaction()            CLOSE cur1 (implicit)
                                      COMMIT

   lyr1->GetNextFeature()             FETCH 1 IN cur1      ==> Error since the cursor was closed with the commit. Explicit ResetReading() required before

   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   lyr1->GetNextFeature()             BEGIN (implicit)
                                      DECLARE cur1 CURSOR FOR SELECT * FROM lyr1
                                      FETCH 1 IN cur1

   ds->StartTransaction()             SAVEPOINT savepoint

   lyr1->CreateFeature(f)             INSERT INTO cur1 ...

   ds->CommitTransaction()            RELEASE SAVEPOINT savepoint

   lyr1->ResetReading()               CLOSE cur1
                                      COMMIT (implicit)

주의: 실제로는 PostgreSQL 드라이버가 객체 500개를 한 번에 가져옵니다. 'FETCH 1'은 설명을 분명하게 하기 위한 것입니다.

고급 예시
-----------------

-  이 예시는 ogrinfo를 사용해서 'tables=' 옵션으로 지정한 레이어들만 목록화하는 방법을 보여줍니다:

   ::

      ogrinfo -ro PG:'dbname=warmerda tables=table1,table2'

-  이 예시는 ogrinfo를 사용해서 도형 열을 여러 개 ('geom1'과 'geom2') 가진 'foo' 테이블을 쿼리하는 방법을 보여줍니다:

   ::

      ogrinfo -ro -al PG:dbname=warmerda 'foo(geom2)'

-  이 예시는 'apt200810' 및 'apt200812' 스키마 안에 있는 레이어만 목록화하는 방법을 보여줍니다. 레이어 이름 앞에 레이어가 속해 있는 스키마 이름이 접두어로 붙을 것입니다:

   ::

      ogrinfo -ro PG:'dbname=warmerda schemas=apt200810,apt200812'

-  이 예시는 ogrinfo를 사용해서 'apt200810'이라는 스키마 안에 있는 레이어만 목록화하는 방법을 보여줍니다. 스키마 하나만 지정했기 때문에 레이어 이름 앞에 접두어 'apt200810'이 붙지 않을 것이라는 사실을 기억하십시오:

   ::

      ogrinfo -ro PG:'dbname=warmerda schemas=apt200810'

-  이 예시는 apt200810 디렉터리 안에 있는 shapefile 집합을 기존 PostgreSQL 스키마 'apt200810'으로 변환하는 방법을 보여줍니다. 이 명령어에서 'schemas=' 옵션을 대신 사용해도 됩니다:

   ::

      ogr2ogr -f PostgreSQL "PG:dbname=warmerda active_schema=apt200810" apt200810

-  이 예시는 'apt200810' 스키마 안에 있는 모든 테이블을 apt200810 디렉터리 안에 shapefile 집합으로 변환하는 방법을 보여줍니다. 스키마 하나만 지정했기 때문에 레이어 이름 앞에 접두어 'apt200810'이 붙지 않을 것이라는 사실을 기억하십시오:

   ::

      ogr2ogr apt200810 PG:'dbname=warmerda schemas=apt200810'

-  이 예시는 기존 스키마에 있는 기존 테이블을 덮어쓰는 방법을 보여줍니다. 조건에 맞는 레이어 이름을 지정하기 위해 '-nln' 옵션을 사용한다는 사실을 기억하십시오:

   ::

      ogr2ogr -overwrite -f PostgreSQL "PG:dbname=warmerda" mytable.shp mytable -nln myschema.mytable

   이 경우 '-nln' 대신 '-lco SCHEMA=mytable'을 사용하면 작동하지 않을 것입니다.
   (자세한 내용은 `#2821 <http://trac.osgeo.org/gdal/ticket/2821>`_ 을 참조하십시오.)

   스키마에 있는 테이블 여러 개를 한 번에 덮어써야 하는 경우, '-nln' 옵션은 더 이상 적합하지 않습니다. 이 경우 연결 문자열 안에 'active_schema='를 사용하는 편이 더 쉬울 수도 있습니다. 다음 예시는 필요한 경우 apt200810 디렉터리 안에 있는 shapefile 집합과 대응하는 모든 PostgreSQL 테이블을 덮어쓸 것입니다:

   ::

      ogr2ogr -overwrite -f PostgreSQL "PG:dbname=warmerda active_schema=apt200810" apt200810

참고
--------

-  :ref:`OGR PostgreSQL 드라이버 정보 <vector.pg>`

