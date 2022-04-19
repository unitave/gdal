.. _vector.openfilegdb:

ESRI 파일 지리 데이터베이스 (OpenFileGDB)
===================================

.. shortname:: OpenFileGDB

.. built_in_by_default::

OpenFileGDB 드라이버는 ArcGIS 9 이상 버전이 생성한 파일 지리 데이터베이스(.gdb 디렉터리)의 벡터 레이어에 읽기 접근을 지원합니다. 데이터셋 이름은 디렉터리/폴더 이름이어야만 하며, .gdb 확장자로 끝나야만 합니다.

이 드라이버는 ZIP 압축 파일 안에 .gdb 디렉터리가 최상위 수준에 있다면 (확장자가 .gdb.zip인) ZIP 압축된 .gdb 디렉터리도 직접 읽어올 수 있습니다.

("system" 테이블을 포함하는) 특화 .gdbtable 파일도 직접 열 수 있습니다.

GDAL 2.2버전부터 도형 안에 있는 곡선도 읽기를 지원합니다.

드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

.. supports_virtualio::

공간 필터링
-----------------

GDAL 3.2버전부터, 이 드라이버는 공간 필터링 작업에 네이티브 .spx 공간 색인을 사용할 수 있습니다.

이전 버전들에서는 공간 필터링의 속도를 올리기 위해 도형 블랍(blob) 시작 부분에 포함된 최소 경계 직사각형을 사용합니다. 기본적으로 레이어의 첫 번째 순차 읽기 도중에 인메모리(in-memory) 공간 색인을 실시간(on the fly)으로 작성하기도 합니다. 그 다음 해당 레이어에 대한 공간 필터링 작업을 하는 경우 이 공간 색인의 혜택을 받을 것입니다. :decl_configoption:`OPENFILEGDB_IN_MEMORY_SPI` 환경설정 옵션을 NO로 설정하면 이 인메모리 공간 색인 작성을 비활성화시킬 수 있습니다.

SQL 지원
-----------

OGR SQL 엔진을 통해 SQL 문을 실행합니다. 속성 색인(.atx 파일)이 존재하는 경우, 이 드라이버는 속성 색인을 사용해서 WHERE 절 또는 SetAttributeFilter() 호출의 속도를 높일 것입니다.

특수 SQL 요청
~~~~~~~~~~~~~~~~~~~~

"GetLayerDefinition a_layer_name" 및 "GetLayerMetadata a_layer_name"을 특수 SQL 요청으로 이용해서 각각 FileGDB 테이블의 정의 및 메타데이터를 XML 콘텐츠로 가져올 수 있습니다. (ArcGIS 10 이상 버전이 생성한 파일 지리 데이터베이스에만 사용할 수 있습니다.)

데이터셋 열기 옵션
--------------------

-  **LIST_ALL_TABLES=YES/NO**: (GDAL 3.4 이상 버전)
   (GDB_* 테이블 같은) 시스템 및 내부 테이블을 포함하는 모든 테이블을 강제로 목록화하려면 이 옵션을 YES로 설정할 수도 있습니다.

필드 도메인
-------------

.. versionadded:: 3.3

인코딩된 그리고 범위가 지정된 필드 도메인을 지원합니다.

계층 구조
------------------------

.. versionadded:: 3.4

다음 메소드를 통해 최상위 요소로서의 또는 객체 데이터셋 내부에 있는 테이블 및 객체 클래스들의 계층 구조를 탐색할 수 있습니다:

   -  :cpp:func:`GDALDataset::GetRootGroup`
   -  :cpp:func:`GDALGroup::GetGroupNames`
   -  :cpp:func:`GDALGroup::OpenGroup`
   -  :cpp:func:`GDALGroup::GetVectorLayerNames`
   -  :cpp:func:`GDALGroup::OpenVectorLayer`

FileGDB 드라이버와의 비교
----------------------------------

(FileGDB API SDK 1.4버전을 이용해서 FileGDB 드라이버와 비교했습니다.)

OpenFileGDB 드라이버의 장점:

-  ArcGIS 10 이상 버전만이 아니라 ArcGIS 9.x 지리 데이터베이스도 읽어올 수 있습니다.
-  어떤 공간 좌표계를 사용하는 레이어라도 열 수 있습니다.
-  스레드 안전(thread safety) (예: 데이터소스들을 병렬로 처리할 수 있습니다.)
-  VSI 가상 파일 API를 이용하기 때문에, 사용자가 ZIP 파일로 된 또는 HTTP 서버에 저장된 지리 데이터베이스를 읽어올 수 있습니다.
-  수많은 필드를 가진 데이터베이스 상에서 작업 속도가 더 빠릅니다.
-  제 3자 라이브러리에 의존하지 않습니다.
-  오류가 발생한 지리 데이터베이스 파일에 강합니다.

OpenFileGDB 드라이버의 단점:

-  읽기 전용입니다.
-  CDF(Compressed Data Format)로 압축된 데이터로부터 데이터를 읽어오지 못 합니다.

예시
--------

-  FileGDB로부터 레이어를 읽어와서 PostGIS로 불러오기:

   ::

      ogr2ogr -overwrite -f "PostgreSQL" PG:"host=myhost user=myuser dbname=mydb password=mypass" "C:\somefolder\BigFileGDB.gdb" "MyFeatureClass"

-  FileGDB 상세 정보를 가져오기:

   ::

      ogrinfo -al "C:\somefolder\MyGDB.gdb"

-  ZIP 압축된 FileGDB 상세 정보를 가져오기:

   ::

      ogrinfo -al "C:\somefolder\MyGDB.gdb.zip"

링크
-----

-  FileGDB API SDK에 의존하는 :ref:`FileGDB <vector.filegdb>` 드라이버
-  `FileGDB 포맷을 리버스 엔지니어링한 사양 <https://github.com/rouault/dump_gdbtable/wiki/FGDB-Spec>`_

