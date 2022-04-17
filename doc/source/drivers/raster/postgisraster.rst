.. _raster.postgisraster:

================================================================================
PostGISRaster -- PostGIS 래스터 드라이버
================================================================================

.. shortname:: PostGISRaster

.. build_dependencies:: PostgreSQL 라이브러리

(WKT 래스터로 알려졌던) PostGIS 래스터는 PostGIS에서 래스터를 지원하기 위한 프로젝트입니다. 2010년 9월 26일부터 PostGIS 2.0 이상 버전에 공식적으로 도입되었습니다.

이 드라이버의 개발은 2009년 GSoC(Google Summer of Code) 도중 시작되었으며, 이후로 크게 개선되었습니다.

현재, 이 드라이버는 PostGIS 래스터 데이터소스의 읽기만 지원하고 있습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::

.. supports_georeferencing::

데이터베이스에 접속하기
------------------------

PostGIS 래스터 데이터소스에 접속하려면, 데이터베이스 이름을 지정하는 연결 문자열을 필요한 추가 파라미터와 함께 사용하십시오.

::

   PG:"[host=''] [port:''] dbname='' [user=''] [password=''] [schema=''] [table=''] [column=''] [where=''] [mode=''] [outdb_resolution='']"

"table='"로 시작하는 부분까지의 문자열이 libpq 스타일 연결 문자열이라는 사실을 기억하십시오. 즉 (몇몇 경우 비밀번호 같은) 필요없는 필드를 생략해도 된다는 뜻입니다.

-  **schema**:
   요청한 래스터 테이블을 저장하고 있는 PostgreSQL 스키마의 이름입니다.

-  **table**:
   PostGIS 래스터 테이블의 이름입니다.
   (예를 들어 raster2pgsql 유틸리티 같은) 래스터 로더(loader)가 생성한 테이블입니다.

-  **column**:
   래스터 테이블에 있는 래스터 열의 이름입니다.

-  **where**:
   래스터 테이블의 요청 결과물을 필터링하기 위해 쓰이는 옵션입니다.
   모든 유형의 SQL-WHERE 표현식을 사용할 수 있습니다.

-  **mode**:
   래스터 테이블의 예상 구조 상태를 알기 위해 쓰이는 옵션입니다.
   두 가지 값 가운데 하나로 설정할 수 있습니다.

   -  **mode=1** - ONE_RASTER_PER_ROW 모드입니다.
      이 경우, 래스터 테이블을 한 무리의 서로 다른 래스터 파일들로 간주합니다. 이 모드는 서로 다른 래스터 파일들을 저장하고 있는 래스터 테이블 용입니다. 연결 문자열에 이 필드를 지정하지 않는 경우, 이 모드를 기본값으로 사용합니다.

   -  **mode=2** - ONE_RASTER_PER_TABLE 모드입니다.
      이 경우, 테이블이 행을 하나 이상 가지고 있더라도 래스터 테이블을 유일(unique) 래스터 타일로 간주합니다. 이 모드는 데이터베이스로부터 타일화 래스터를 읽어오기 위한 것입니다.

-  **outdb_resolution**: (GDAL 2.3.1 이상 버전)
   이 파라미터는 데이터베이스 외부에 있는 래스터를 처리할 방법을 지정합니다. 기본값은 server_side입니다.

   -  **server_side** - PostgreSQL 서버가 데이터베이스 외부에 있는 래스터를 가져올 것입니다. 데이터베이스 외부에 있는 래스터가 서버 상에서 활성화된 상태라는 뜻입니다.

   -  **client_side** - GDAL PostGISRaster 클라이언트에 데이터베이스 외부에 있는 래스터의 파일명을 반환할 것입니다. 그러면 클라이언트 향에서 해당 래스터를 열 것입니다. 클라이언트가 서버 상에 저장된 파일명에 접근할 수 있다는 뜻입니다.

   -  **client_side_if_possible** - GDAL PostGISRaster 클라이언트에 데이터베이스 외부에 있는 래스터의 파일명을 반환할 것입니다. 그러면 크라이언트가 해당 파일명에 접근할 수 있는지 확인할 것입니다. 접근할 수 있다면 client_side와 동일합니다. 접근할 수 없다면 server_side와 동일합니다. 이 모드로 설정하면 서버에 추가적인 쿼리를 발생시킨다는 사실을 기억하십시오.

추가 메모
~~~~~~~~~~~~~~~~

테이블이 타일화 래스터를 저장하고 있는데 드라이버를 mode=1 파라미터로 실행한 경우, 각 이미지 타일을 서로 다른 이미지로 간주하고 하위 데이터셋으로 리포트할 것입니다. 이 드라이버가 아직도 처리하지 못 하는 사용 사례들이 있습니다. 예를 들어 비정규 블록화 래스터를 탐지하면 오류를 발생시킵니다. 어쨌든 앞에서 언급했듯이 이 드라이버는 계속 개발 중이고, 앞으로 더 많은 래스터 구조를 처리할 수 있게 될 것입니다.

추가적인 작업 모드가 존재합니다. 테이블 이름을 설정하지 않는 경우, 드라이버가 사용 권한이 있는 모든 데이터베이스 스키마에 있는 기존 래스터 테이블을 검색해서 각 테이블을 하위 데이터셋으로 리포트할 것입니다.

gdalinfo, gdal_translate, gdalwarp 등등 모든 GDAL 도구에서 이 연결 문자열 서식을 사용해야만 합니다.

성능 힌트
~~~~~~~~~~~~~~~~~

이 드라이버의 최대 성능을 끌어내려면, PostGIS 래스터에 래스터를 다음과 같은 옵션들로 불러오는 것이 최선입니다:

-  타일화: raster2pgsql의 -t 스위치

-  오버뷰: raster2pgsql의 -l 2,4,8,... 스위치

-  래스터 열에 GIST 공간 색인 생성: raster2pgsql의 -I 스위치

-  제약 조건 등록: raster2pgsql의 -C 스위치

예시
--------

gdalinfo를 이용해서 GDAL을 통해 래스터에 관한 요약을 보려면:

::

   gdalinfo  "PG:host=localhost port=5432 dbname='mydb' user='postgres' password='secret' schema='public' table=mytable"

더 많은 예시를 원한다면 PostGIS 래스터 FAQ 단락을 살펴보십시오: `내 PostGIS 래스터 데이터를 다른 래스터 포맷으로 내보낼 수 있나요? <https://postgis.net/docs/RT_FAQ.html#idm28288>`_

감사의 말
--------

드라이버 개발자들

-  호르헤 아레발로(Jorge Arévalo, jorgearevalo@libregis.org)
-  데이빗 즈와그(David Zwarg, dzwarg@azavea.com)
-  이벤 루올(Even Rouault, even.rouault@spatialys.com)

참고
--------

-  `GDAL PostGISRaster 드라이버 위키 <https://trac.osgeo.org/gdal/wiki/frmts_wtkraster.html>`_

-  `PostGIS 래스터 문서 <https://postgis.net/docs/RT_reference.html>`_
