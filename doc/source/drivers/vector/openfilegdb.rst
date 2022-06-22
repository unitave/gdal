.. _vector.openfilegdb:

ESRI 파일 지리 데이터베이스 (OpenFileGDB)
===================================

.. shortname:: OpenFileGDB

.. built_in_by_default::

OpenFileGDB 드라이버는 ArcGIS 9 이상 버전이 생성한 파일 지리 데이터베이스(.gdb 디렉터리)의 벡터 레이어에 읽기, 쓰기 및 업데이트 접근을 지원합니다. 데이터셋 이름은 디렉터리/폴더 이름이어야만 하며, .gdb 확장자로 끝나야만 합니다.

이 드라이버는 ZIP 압축 파일 안에 .gdb 디렉터리가 최상위 수준에 있다면 (확장자가 .gdb.zip인) ZIP 압축된 .gdb 디렉터리도 직접 읽어올 수 있습니다.

("system" 테이블을 포함하는) 특화 .gdbtable 파일도 직접 열 수 있습니다.

GDAL 2.2버전부터 도형 안에 있는 곡선도 읽기를 지원합니다.

GDAL 3.6 이상 버전부터 쓰기 및 업데이트 케이퍼빌리티를 지원합니다.

드라이버 케이퍼빌리티
-------------------

.. supports_create::

    .. versionadded:: GDAL 3.6

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

``CREATE INDEX idx_name ON layer_name(field_name)`` SQL 요청을 사용해서 속성 색인을 생성할 수 있습니다. 'idx_name' 은 16문자 길이 이하여야만 하며, 글자로 시작해야만 하고, 알파벳 및 숫자 또는 언더바 문자만 담고 있어야만 합니다.

``RECOMPUTE EXTENT ON layer_name`` SQL 요청을 사용해서 레이어 메타데이터에 있는 레이버 범위의 업데이트를 촉발시킬 수 있습니다. 피처를 업데이트 또는 삭제할 때 일반 레이어 범위를 변경하게 되는 경우 유용합니다.

``REPACK`` 또는 ``REPACK layer_name`` SQL 요청을 사용해서 각각 전체 데이터셋 또는 지정한 레이어의 용량을 줄일 수 있습니다. :file:`.gdbtable` 파일에 구멍을 남길 수도 있는 편집 작업(업데이트 또는 피처 삭제)을 하는 경우 유용합니다. ``REPACK`` 명령어는 :file:`.gdbtable` 파일을 구멍 없이 재작성하도록 합니다. 이 치밀화(compact) 작업은 범위를 다시 계산하지 않는다는 사실을 기억하십시오.

데이터셋 열기 옵션
--------------------

-  **LIST_ALL_TABLES=YES/NO**: (GDAL 3.4 이상 버전)
   (GDB_* 테이블 같은) 시스템 및 내부 테이블을 포함하는 모든 테이블을 강제로 목록화하려면 이 옵션을 YES로 설정할 수도 있습니다.

데이터셋 생성 옵션
------------------

없음.

레이어 생성 옵션
----------------

-  **FEATURE_DATASET=string**:
   이 옵션을 설정하면, 이름을 설정한 FeatureDataset 폴더에 새 레이어를 생성할 것입니다. 이 폴더가 이미 존재하고 있지 않다면 폴더도 생성할 것입니다.

-  **LAYER_ALIAS=string**:
   레이어 별명을 설정합니다.

-  **GEOMETRY_NAME=string**:
   새 레이어에 있는 도형 열의 이름을 설정합니다. 기본값은 "SHAPE"입니다.

-  **GEOMETRY_NULLABLE=YES/NO**:
   도형 열의 값이 NULL일 수 있는지 여부를 설정합니다. NO로 설정해서 도형이 필수라고 지정할 수도 있습니다. 기본값은 "YES"입니다.

-  **FID**:
   생성할 OID 열의 이름을 설정합니다. 기본값은 "OBJECTID"입니다.

-  **XYTOLERANCE, ZTOLERANCE, MTOLERANCE=value**:
   이 파라미터들은 네트워크 및 위상 규칙 같은 고급 ArcGIS 기능에 사용되는 스냅 작업 허용 오차를 제어합니다. 어떤 OGR 작업에도 영향을 미치지 않지만, ArcGIS가 이 파라미터들을 사용할 것입니다. 파라미터 단위는 좌표계 단위입니다.

   ArcMap 10.0버전 및 OGR의 XYTOLERANCE 기본값은 투영 좌표계의 경우 0.001m(또는 이와 동등한 길이)이고 지리 좌표계의 경우 0.000000008983153°입니다.
   ArcMap 10.0버전 및 OGR의 ZTOLERANCE와 MTOLERANCE 기본값은 0.0001입니다.

-  **XORIGIN, YORIGIN, ZORIGIN, MORIGIN, XYSCALE, ZSCALE, ZORIGIN=value**:
   이 파라미터들은 파일 지리 데이터베이스 내부의 `좌표 정밀도 그리드(coordinate precision grid) <https://help.arcgis.com/en/sdk/10.0/java_ao_adf/conceptualhelp/engine/index.html#//00010000037m000000>`_ 를 제어합니다. 원점(origin)과 척도(scale)가 그리드 차원을 결정합니다. 원점은 공간에서 참조 그리드 포인트의 위치를 정의합니다. 척도는 해상도와 반비례합니다.
   즉, 원점이 0에 위치하고 모든 축 상에서 해상도가 0.001인 그리드를 생성하려면 모든 원점 파라미터를 0으로 모든 척도를 1000으로 설정해야 할 것입니다.

   *중요*: ``(xmin=XORIGIN, ymin=YORIGIN, xmax=(XORIGIN + 9E+15 / XYSCALE), ymax=(YORIGIN + 9E+15 / XYSCALE))`` 이 지정하는 도메인이 피처 클래스의 가능한 모든 좌표값을 포함할 수 있어야 합니다. 이 도메인 바깥에 떨어지는 좌표를 가진 피처를 추가하는 경우, ArcGIS에서 공간 색인 작업, 피처 선택, 그리고 데이터 내보내기 시 오류가 발생할 것입니다.

   ArcMap 10.0버전 및 OGR의 기본값:

   -  지리 좌표계의 경우: XORIGIN=-400, YORIGIN=-400, XYSCALE=1000000000
   -  투영 좌표계의 경우: XYTOLERANCE가 기본값 0.001m인 경우 XYSCALE의 기본값은 10,000입니다. XORIGIN과 YORIGIN의 기본값은 좌표계에 따라 달라지지만, XYSCALE이 기본값일 때 모든 좌표계에서 OGR 기본값인 -2,147,483,647이 적합합니다.
   -  ZORIGIN 및 MORIGIN: -100000
   -  ZSCALE 및 MSCALE: 10000

-  **COLUMN_TYPES=string**:
   필드의 FileGDB 열 유형을 강제로 생성하기 위한 ``field_name=fgdb_filed_type`` 서식의 (쉼표로 구분된) 문자열 목록입니다.

-  **DOCUMENTATION=string**:
   레이어에 대한 XML 문서입니다.

-  **CONFIGURATION_KEYWORD=DEFAULTS/MAX_FILE_SIZE_4GB/MAX_FILE_SIZE_256TB**:
   데이터 저장 방법을 사용자 지정합니다. 기본값은 텍스트를 UTF-8 인코딩으로 저장하고 데이터는 1TB까지 지원합니다.

-  **CREATE_SHAPE_AREA_AND_LENGTH_FIELDS=YES/NO**:
   기본값은 (CreateLayer() API를 통한) NO입니다. 이 옵션을 설정하는 경우 폴리곤 레이어를 위해 Shape_Area 및 Shape_Length 특수 필드를 생성할 것입니다. (Shape_Length는 선형 레이어 전용입니다.) 데이터셋에 새 피처를 추가하거나 기존 피처를 수정할 때마다 자동적으로 이 필드들을 피처 면적 또는 길이로 채울 것입니다. ogr2ogr를 이용해서 Shape_Area/Shape_Length 특수 필드를 가진 소스 레이어를 작업하는데 이 옵션을 명확하게 설정하지 않은 경우, 산출되는 파일 지리 데이터베이스(FileGeodatabase)가 이 필드들을 제대로 태그하도록 옵션을 자동으로 설정할 것입니다.

필드 도메인
-------------

.. versionadded:: 3.3

인코딩된 그리고 범위가 지정된 필드 도메인을 지원합니다.

계층 구조
---------

.. versionadded:: 3.4

다음 메소드를 통해 최상위 요소로서의 또는 객체 데이터셋 내부에 있는 테이블 및 객체 클래스들의 계층 구조를 탐색할 수 있습니다:

   -  :cpp:func:`GDALDataset::GetRootGroup`
   -  :cpp:func:`GDALGroup::GetGroupNames`
   -  :cpp:func:`GDALGroup::OpenGroup`
   -  :cpp:func:`GDALGroup::GetVectorLayerNames`
   -  :cpp:func:`GDALGroup::OpenVectorLayer`

트랜잭션 지원
-------------

OpenFileGDB 드라이버는 (:ref:`rfc-54` 에 따라) 에뮬레이션을 통해 데이터베이스 수준에서 트랜잭션을 구현합니다. StartTransaction(force=TRUE)를 호출했을 때 지리 데이터베이스에서 수정된 부분의 현재 상태를 백업함으로써 트랜잭션이 작동합니다. 트랜잭션이 커밋되면 백업 복사본을 제거합니다. 트랜잭션이 롤백되는 경우, 백업 복사본을 복원합니다.

(동일한 또는 또다른 프로세스에서 서로 다른 연결을 통해) 업데이트가 동시에 여러 번 발생하는 경우 이 에뮬레이션이 불특정한 습성을 보인다는 사실을 기억하십시오.

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

감사의 말
---------

네덜란드의 `자위트홀란트(Zuid-Holland) 주 <https://www.zuid-holland.eu/>`_, `헬데를란트(Gelderland) 주 <https://www.gelderland.nl/en>`_ 그리고 `암스테르담(Amsterdam) 시 <https://www.amsterdam.nl/en>`_ 의 재정 지원을 받아 이 드라이버의 편집/쓰기 케이퍼빌리티를 구현했습니다.

