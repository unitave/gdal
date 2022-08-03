.. _vector.filegdb:

ESRI 파일 지리 데이터베이스 (FileGDB)
===============================

.. shortname:: FileGDB

.. build_dependencies:: FileGDB API 라이브러리

FileGDB 드라이버는 ArcGIS 10 이상 버전이 생성한 파일 지리 데이터베이스(.gdb 디렉터리)의 벡터 레이어에 읽기 및 쓰기 접근을 지원합니다. 데이터셋 이름은 디렉터리/폴더 이름이어야만 하며, .gdb 확장자로 끝나야만 합니다.

.. note::
   
   :ref:`OpenFileGDB <vector.openfilegdb>` 드라이버가 (예를 들면 제3자 라이브러리에 의존하지 않는) 내장된 드라이버 대체제로서 존재합니다.

드라이버 케이퍼빌리티
-------------------

.. supports_create::

.. supports_georeferencing::

요구 사항
------------

`FileGDB API SDK <http://www.esri.com/apps/products/download/#File_Geodatabase_API_1.3>`_

GDAL 2.2버전부터 도형 안에 있는 곡선의 읽기를 지원합니다.

벌크 객체 불러오기
--------------------

:decl_configoption:`FGDB_BULK_LOAD` 환경설정 옵션을 YES로 설정하면 객체 삽입의 속도를 향상시킬 수 있습니다. (또는 어떤 경우 수많은 객체를 삽입할 때 발생하는 문제를 해결할 수도 있습니다. http://trac.osgeo.org/gdal/ticket/4420 를 참조하십시오.) 이 환경설정 옵션은 작성 방지(write lock)를 활성화시켜 색인을 임시로 비활성화시키는 효과가 있습니다. 데이터소스를 종료할 때 또는 읽기 작업이 끝났을 때 색인을 복원합니다.

새로 생성한 레이어에 기본적으로 (달리 지정하지 않는 한) 벌크 불러오기를 활성화합니다.

SQL 지원
-----------

SELECT 문을 제외하고, FileGDB SDK API의 SQL 엔진을 통해 SQL 문을 실행합니다. 하지만 현재 FileGDB SDK API 버전(v1.2)에서 SELECT 문을 제대로 또는 정확하게 지원하지 못 하기 때문에, SELECT 문은 기본적으로 OGR SQL 엔진으로 실행할 것입니다. ogrinfo 또는 ogr2ogr 유틸리티에 *-dialect FileGDB* 옵션을 지정하면 이 습성을 변경할 수 있습니다.

특수 SQL 요청
~~~~~~~~~~~~~~~~~~~~

"GetLayerDefinition a_layer_name" 및 "GetLayerMetadata a_layer_name"을 특수 SQL 요청으로 이용해서 각각 FileGDB 테이블의 정의 및 메타데이터를 XML 콘텐츠로 가져올 수 있습니다.

GDAL 3.5버전부터, 데이터베이스 치밀화(compaction)를 요구하는 "REPACK" 특수 SQL 요청을 전송할 수 있습니다.

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

트랜잭션 지원
-------------------

FileGDB 드라이버는 (:ref:`rfc-54` 에 따라) 에뮬레이션을 통해 데이터베이스 수준에서 트랜잭션을 구현합니다. FileGDB SDK 자체는 트랜잭션을 지원하지 않기 때문입니다. StartTransaction(force=TRUE)를 호출했을 때 지리 데이터베이스의 현재 상태를 백업함으로써 트랜잭션이 작동합니다. 트랜잭션이 커밋되면 백업 복사본을 제거합니다. 트랜잭션이 롤백되는 경우, 백업 복사본을 복원합니다. 즉 대용량 지리 데이터베이스를 운용하는 경우 성능을 저하시킬 수도 있습니다.

GDAL 2.1버전부터 리눅스/유닉스 상에서는 전체 복사본을 백업하는 대신 수정된 레이어만 백업합니다.

(동일한 또는 또다른 프로세스에서 서로 다른 연결을 통해) 업데이트가 동시에 여러 번 발생하는 경우 이 에뮬레이션이 불특정한 습성을 보인다는 사실을 기억하십시오.

CreateFeature() 지원
-----------------------

FileGDB SDK API는 사용자가 지정한 FID를 가진 객체를 생성하지 못 합니다. GDAL 2.1부터, FileGDB 드라이버는 사용자가 선택한 FID를 가진 객체를 생성할 수 있도록 해주는 특별한 FID 재(再)매핑 기술을 구현합니다.

데이터셋 생성 옵션
------------------------

없습니다.

레이어 생성 옵션
----------------------

-  **FEATURE_DATASET**:
   이 옵션을 설정하면, 지정한 FeatureDataset 폴더에 새 레이어를 생성할 것입니다. 지정한 폴더가 존재하지 않는 경우 폴더를 생성할 것입니다.

-  **LAYER_ALIAS=string**: (GDAL 2.3 이상 버전)
   레이어 이름의 별명(alias)을 설정합니다.

-  **GEOMETRY_NAME**:
   새 레이어의 도형 열의 이름을 설정합니다. 기본값은 "SHAPE"입니다.

-  **GEOMETRY_NULLABLE**: (GDAL 2.0 이상 버전)
   도형 열의 값이 NULL일 수 있는지 여부를 선택합니다. 도형을 필수로 하려면 NO로 설정하면 됩니다. 기본값은 "YES"입니다.

-  **FID**:
   생성할 OID 열의 이름을 설정합니다. 기본값은 "OBJECTID"입니다.
   주의: GDAL 버전 2 이전 배포판에서는 이 옵션의 이름이 OID_NAME이었습니다.

-  **XYTOLERANCE, ZTOLERANCE**:
   이 파라미터들은 네트워크 및 위상 규칙 같은 고급 ArcGIS 기능을 위한 스냅 허용 오차를 제어합니다. 어떤 OGR 작업에도 영향을 미치지 않지만, ArcGIS에서 사용하는 경우 영향을 미칠 것입니다. 이 파라미터들의 단위는 좌표계 단위입니다.

   ArcMap 10.0 및 OGR 기본값은 투영 좌표계의 경우 XYTOLERANCE가 0.001m(또는 이와 동일한 다른 단위의 값)이고, 지리 좌표계의 경우 0.000000008983153°입니다.

-  **XORIGIN, YORIGIN, ZORIGIN, XYSCALE, ZSCALE**:
   이 파라미터들은 파일 지리 데이터베이스 내부의 `좌표 정밀도 그리드 <http://help.arcgis.com/en/sdk/10.0/java_ao_adf/conceptualhelp/engine/index.html#//00010000037m000000>`_ 를 제어합니다. 그리드의 크기는 원점과 척도로 결정됩니다. 원점은 기준 그리드 포인트의 공간 위치를 정의합니다. 척도는 해상도와 반비례합니다. 따라서, 원점의 위치가 0이고 모든 축에서 해상도가 0.001인 그리드를 얻으려면 모든 원점을 0으로 설정하고 모든 척도를 1000으로 설정해야 할 것입니다.

   *중요*: ``(xmin=XORIGIN, ymin=YORIGIN, xmax=(XORIGIN + 9E+15 / XYSCALE), ymax=(YORIGIN + 9E+15 / XYSCALE))`` 으로 지정된 도메인은 객체 클래스에 가능한 모든 좌표값을 포함시켜야 합니다. 이 도메인 바깥에 위치하는 좌표를 가진 객체를 추가하는 경우, 공간 색인 작업, 객체 선택, 그리고 데이터 탐색 시 ArcGIS에서 오류가 발생할 것입니다.

   ArcMap 10.0 및 OGR 기본값:

   -  지리 좌표계의 경우: XORIGIN=-400, YORIGIN=-400, XYSCALE=1000000000
   -  투영 좌표계의 경우: XYTOLERANCE가 기본값 0.001m이면 XYSCALE=10000입니다. XORIGIN과 YORIGIN은 좌표계에 따라 달라지지만, 모든 좌표계에 XYSCALE 기본값과 함께 OGR 기본값 -2147483647이 적합합니다.

-  **XML_DEFINITION**:
   이 옵션을 설정하면, 이 값을 새 테이블을 생성하기 위한 XML 정의로 사용할 것입니다. 이런 XML 정의의 루트 노드는 반드시 FileGDBAPI.xsd를 준수하는 <esri:DataElement>여야만 합니다.

-  **CREATE_MULTIPATCH=YES**:
   이 옵션을 설정하면, 레이어의 멀티폴리곤 유형 도형을 멀티패치(MultiPatch) 유형으로 작성할 것입니다.

-  **CONFIGURATION_KEYWORD=DEFAULTS/TEXT_UTF16/MAX_FILE_SIZE_4GB/MAX_FILE_SIZE_256TB/GEOMETRY_OUTOFLINE/BLOB_OUTOFLINE/GEOMETRY_AND_BLOB_OUTOFLINE**:
   데이터 저장 방법을 사용자 지정합니다. 기본적으로 텍스트는 UTF-8로, 그리고 데이터는 1TB 용량까지 저장합니다.

-  **CREATE_SHAPE_AREA_AND_LENGTH_FIELDS=YES/NO**: (GDAL 3.6.0 이상 버전)
   기본값은 (CreateLayer() API를 통한) NO입니다. 이 옵션을 설정하는 경우 폴리곤 레이어를 위해 Shape_Area 및 Shape_Length 특수 필드를 생성할 것입니다. (Shape_Length는 선형 레이어 전용입니다.) 데이터셋에 새 피처를 추가하거나 기존 피처를 수정할 때마다 자동적으로 이 필드들을 피처 면적 또는 길이로 채울 것입니다. ogr2ogr를 이용해서 Shape_Area/Shape_Length 특수 필드를 가진 소스 레이어를 작업하는데 이 옵션을 명확하게 설정하지 않은 경우, 산출되는 파일 지리 데이터베이스(FileGeodatabase)가 이 필드들을 제대로 태그하도록 옵션을 자동으로 설정할 것입니다.

환경설정 옵션
-------------

다음 :ref:`환경설정 옵션 <configoptions>` 을 사용할 수 있습니다:

- :decl_configoption:`FGDB_BULK_LOAD`:
  이 옵션을 YES로 설정하면 객체 삽입의 속도를 향상시킬 수 있습니다. (또는 어떤 경우 수많은 객체를 삽입할 때 발생하는 문제를 해결할 수도 있습니다. http://trac.osgeo.org/gdal/ticket/4420 를 참조하십시오.) 이 환경설정 옵션은 작성 방지(write lock)를 활성화시켜 색인을 임시로 비활성화시키는 효과가 있습니다. 데이터소스를 종료할 때 또는 읽기 작업이 끝났을 때 색인을 복원합니다. 새로 생성되는 레이어의 경우 (달리 지정하지 않는 한) 덩어리 불러오기(bulk load)가 기본적으로 활성화되어 있습니다.

예시
--------

-  FileGDB로부터 레이어를 읽어와서 PostGIS로 불러오기:

-  FileGDB 상세 정보를 가져오기:

빌드 작업 메모
--------------

`플러그인 용 GDAL 윈도우 빌드 작업 예시 <http://trac.osgeo.org/gdal/wiki/BuildingOnWindows>`_ 를 읽어보십시오. FileGDB 용 :file:`nmake.opt` 파일에 비슷한 단락이 있을 것입니다. 준비가 되었다면 :file:`$gdal_source_root/ogr/ogrsf_frmts/filegdb*` 폴더로 가서 다음 명령어를 실행하십시오:

.. code-block:: c

    nmake /f makefile.vc plugin
    nmake /f makefile.vc plugin-install

알려진 문제점
------------

-  SDK가 특정 공간 좌표계를 사용하는 레이어를 열지 못 한다고 알려져 있습니다. ``ogrinfo --debug on the.gdb`` 를 실행할 때 (GDAL 2.0버전에서 경고로 리포트되는) "FGDB: Error opening XXXXXXX. Skipping it (Invalid function arguments.)" 메시지를 반환하는 경우가 이런 경우일 수도 있습니다. 보통 OpenFileGDB 드라이버를 사용하면 해결되는 문제입니다.

-  데이터셋 작성 시 FGDB 좌표 스냅이 도형을 변경하게 됩니다. 원점 및 척도 레이어 생성 옵션을 사용해서 스냅 습성을 제어하십시오.

-  이 드라이버는 SDC(Smart Data Compression) 포맷으로 된 데이터를 읽어오지 못 합니다. ESRI SDK가 해당 포맷의 읽기를 지원하지 않기 때문입니다.

-  CDF(Compressed Data Format) 포맷으로 압축된 데이터를 읽어오려면 ESRI SDK 1.4 이상 버전이 필수입니다.

-  몇몇 응용 프로그램이 GDB_Items 메타데이터에 존재하지 않는 비공간 테이블을 가진 FileGeodatabase 포맷을 생성합니다. ESRI SDK가 이런 테이블을 열지 못 하기 때문에, GDAL은 이런 테이블을 읽기 위해 자동적으로 OpenFileGDB 드라이버로 돌아갈 것입니다. 이에 따라 이런 테이블은 OpenFileGDB 드라이버의 제한 사항과 함께 열릴 것입니다. (예를 들면 읽기전용으로 열릴 것입니다.)


기타 제한 사항
-----------------

- FileGeodatabase 포맷은 (그리고 당연히 드라이버도) 64비트 정수형을 지원하지 않습니다.

링크
-----

-  `ESRI 파일 지리 데이터베이스(File Geodatabase) API 페이지 <https://github.com/Esri/file-geodatabase-api/>`_

-  제 3자 라이브러리/SDK에 의존하지 않는 :ref:`OpenFileGDB <vector.openfilegdb>` 드라이버

