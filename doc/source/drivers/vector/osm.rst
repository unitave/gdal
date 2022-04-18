.. _vector.osm:

OSM - 오픈스트리트맵 XML 및 PBF
===============================

.. shortname:: OSM

.. build_dependencies:: libsqlite3 (및 OSM XML 용 libexpat)

OSM 드라이버는 (XML 기반) .osm 및 (최적화된 바이너리) .pbf 포맷으로 된 오픈스트리트맵(OpenStreetMap) 파일을 읽어옵니다.

GDAL이 SQLite 지원 및 .osm XML 파일 용 Expat 지원과 함께 빌드된 경우 이 드라이버를 사용할 수 있습니다.

파일명이 .osm 또는 .pbf 확장자로 끝나야만 합니다.

이 드라이버는 객체를 다음 다섯 가지 레이어로 카테고리화할 것입니다:

-  **points** : 특별한 의미가 있는 태그가 추가된 "node" 객체입니다.
-  **lines** : 면이 없는 것으로 인식되는 "way" 객체입니다.
-  **multilinestrings** : 멀티라인스트링을 형성하는 "relation" 객체입니다. (type = 'multilinestring' 또는 type = 'route')
-  **multipolygons** : 멀티폴리곤을 형성하는 "relation" 객체 (type = 'multipolygon' 또는 type = 'boundary') 그리고 면으로 인식되는 "way" 객체입니다.
-  **other_relations** : 위의 두 레이어에 속하지 않는 "relation" 객체입니다.

드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

.. supports_virtualio::

환경설정
-------------

GDAL 배포판의 *data* 폴더에 사용자의 필요에 맞춰 사용자 지정할 수 있는 `osmconf.ini <https://github.com/OSGeo/gdal/blob/master/data/osmconf.ini>`_ 파일이 있습니다. :decl_configoption:`OSM_CONFIG_FILE` 환경설정 옵션으로 대체 경로를 정의할 수도 있습니다.

이 사용자 지정은 본질적으로 어떤 OSM 속성 및 키를 OGR 레이어 필드로 변환해야 하는지를 정의하는 작업입니다.

다른 필드/태그로부터 (SQLite 엔진이 평가하는) SQL 표현식으로 필드를 계산할 수 있습니다. 예를 들어 z_order 속성을 계산할 수 있습니다.

"other_tags" 필드
~~~~~~~~~~~~~~~~~~

*osmconf.ini* 파일에서 키를 엄격하게 식별해놓지 않은 경우, "other_tags" 필드에 PostgreSQL HSTORE 유형과 호환되는 문법으로 키=값 쌍을 추가합니다. :ref:`PG <vector.pg>` 드라이버의 *COLUMN_TYPES* 레이어 생성 옵션을 참조하십시오.

예시:

::

   ogr2ogr -f PostgreSQL "PG:dbname=osm" test.pbf -lco COLUMN_TYPES=other_tags=hstore

"all_tags" 필드
~~~~~~~~~~~~~~~~

"all_tags" 필드는 다른 키들은 물론 전용 필드로 리포트되도록 특별히 식별되는 키 2개를 모두 담고 있다는 점을 제외하면 "other_tags"와 비슷합니다.

"all_tags"는 기본적으로 비활성화되어 있으며, 활성화할 경우 "other_tags"와 함께 사용할 수 없습니다.

내부 작업 및 성능 조정
-----------------------------------------

이 드라이버는 내부 SQLite 데이터베이스를 이용해서 도형을 분해(resolve)할 것입니다. 이 내부 데이터베이스가 100MB를 초과하지 않는 경우 RAM에 자리할 것입니다. 100MB를 초과하게 되면, 디스크 상에 임시 파일로 작성될 것입니다. :decl_configoption:`CPL_TMPDIR` 환경설정 옵션을 설정하지 않는 이상 기본적으로 현재 디렉터리에 이 파일을 작성할 것입니다. 기본 100MB 한계값은 :decl_configoption:`OSM_MAX_TMPFILE_SIZE` 환경설정 옵션으로 (MB 단위로 값을 설정해서) 조정할 수 있습니다.

노드 색인 작업의 경우, 기본적으로 SQLite를 의존하지 않는 맞춤형 메커니즘을 사용합니다. (관계성을 해결하기 위한 "way" 객체의 색인 작업은 그래도 SQLite를 의존합니다.) 하지만 어떤 상황에서는 (노드 ID가 증가하지 않거나 노드 ID가 예상 범위 안에 없는 상황에서는) 맞춤형 메커니즘이 작동하지 않을 수도 있으며 드라이버가 :decl_configoption:`OSM_USE_CUSTOM_INDEXING` 환경설정 옵션을 NO로 설정해서 다시 시작하라고 제안하는 오류 메시지를 출력할 것입니다.

맞춤형 색인 작업을 이용하는 경우 (기본적인 경우) :decl_configoption:`OSM_COMPRESS_NODES` 환경설정 옵션을 YES로 설정할 수 있습니다. (기본값은 NO입니다.)

I/O 접근이 제한 요인인 경우 (일반적으로 회전 디스크인 경우) 성능을 개선하기 위해 이 옵션을 활성화시킬 수 있으며, 압축률이 최대 3 또는 4 인자까지 올라갈 수 있는 국가 크기 OSM 추출물의 경우 가장 효과적이고, 노드 데이터베이스를 운영 체제 I/O 캐시에 맞는 크기로 유지하는 데 도움이 됩니다. 지구 전체 파일의 경우 이 옵션의 효과가 덜 효율적일 것입니다. 이 옵션은 RAM 60MB를 추가로 사용합니다.

교차삽입 읽기
-------------------

OSM 파일의 특성 및 드라이버가 내부적으로 작동하는 방식 때문에, 레이어별로 작동하는 기본 읽기 모드가 올바르게 작동하지 않을 수도 있습니다. 사용자 응용 프로그램에서 소비되기 전에 레이어에 너무 많은 객체들이 누적될 것이기 때문입니다.

GDAL 2.2버전부터, 객체를 생성된 순서대로 반복하려면 응용 프로그램이 ``GDALDataset::GetNextFeature()`` API를 이용해야 합니다.

GDAL 2.2 이전 버전들의 경우, 응용 프로그램이 대용량 파일에 대해 :decl_configoption:`OGR_INTERLEAVED_READING` 환경설정 옵션을 YES로 설정해서 다음 읽기 패턴을 반드시 사용해야만 하는 특수 읽기 모드를 활성화시켜야 합니다:

.. code-block:: cpp

       bool bHasLayersNonEmpty;
       do
       {
           bHasLayersNonEmpty = false;

           for( int iLayer = 0; iLayer < poDS->GetLayerCount(); iLayer++ )
           {
               OGRLayer *poLayer = poDS->GetLayer(iLayer);

               OGRFeature* poFeature;
               while( (poFeature = poLayer->GetNextFeature()) != NULL )
               {
                   bHasLayersNonEmpty = true;
                   OGRFeature::DestroyFeature(poFeature);
               }
           }
       }
       while( bHasLayersNonEmpty );

주의: ogr2ogr 응용 프로그램은 어떤 특정 사용자 행위 없이도 :decl_configoption:`OGR_INTERLEAVED_READING` 모드를 사용하도록 수정되었습니다.

공간 필터링
-----------------

.osm 또는 .pbf 파일이 구성된 방식 및 파일 파싱이 종료되는 방식 때문에, 효율성이라는 이유에서 포인트 레이어에 적용된 공간 필터가 다른 레이어에도 영향을 미칠 것입니다. 라인 또는 폴리곤의 꼭짓점이 사라질 수도 있습니다.

이 문제점을 해결할 수 있는 가능성 가운데 하나는 포인트 레이어에 적당한 버퍼를 가진 더 큰 공간 필터를 사용한 다음 원하는 필터를 적용하기 위해 산출물을 후처리하는 것입니다. 하지만 폴리곤이 관심 영역으로부터 아주 멀리 떨어져 있는 꼭짓점을 가지고 있는 경우 이 방법은 작동하지 않을 것입니다. 이런 경우 파일을 또다른 포맷으로 완전히 변환한 다음 산출 라인 또는 폴리곤 레이어를 필터링해야 할 것입니다.

.osm.bz2 파일 그리고/또는 온라인 파일 읽기
------------------------------------------

.osm.bz2 파일은 네이티브하게 인식되지 않지만, (유닉스 상에서) 다음과 같은 명령어로 처리할 수는 있습니다:

::

   bzcat my.osm.bz2 | ogr2ogr -f SQLite my.sqlite /vsistdin/

.osm 또는 .pbf 파일을 다운로드하지 않은 채로 변환할 수 있습니다:

::

   wget -O - http://www.example.com/some.pbf | ogr2ogr -f SQLite my.sqlite /vsistdin/

   또는

   ogr2ogr -f SQLite my.sqlite /vsicurl_streaming/http://www.example.com/some.pbf -progress

그리고 위의 두 단계를 결합하면:

::

   wget -O - http://www.example.com/some.osm.bz2 | bzcat | ogr2ogr -f SQLite my.sqlite /vsistdin/

열기 옵션
------------

-  **CONFIG_FILE=filename**:
   환경설정 파일 이름을 지정합니다. 기본값은 '{GDAL_DATA}/osmconf.ini' 입니다.

-  **USE_CUSTOM_INDEXING=YES/NO**:
   맞춤형 색인 작업을 활성화할지 여부를 선택합니다. 기본값은 YES입니다.

-  **COMPRESS_NODES=YES/NO**:
   임시 데이터베이스에 노드를 압축할지 여부를 선택합니다. 기본값은 NO입니다.

-  **MAX_TMPFILE_SIZE=int_val**:
   인메모리 임시 파일의 MB 단위 최대 용량을 지정합니다. 임시 파일이 이 값을 초과하는 경우 디스크에 작성할 것입니다. 기본값은 100입니다.

-  **INTERLEAVED_READING=YES/NO**:
   교차삽입 읽기를 활성화할지 여부를 선택합니다. 기본값은 NO입니다.

참고
--------

-  `오픈스트리트맵 홈페이지 <http://www.openstreetmap.org/>`_
-  `OSM XML 포맷 설명 <http://wiki.openstreetmap.org/wiki/OSM_XML>`_
-  `OSM PBF 포맷 설명 <http://wiki.openstreetmap.org/wiki/PBF_Format>`_

