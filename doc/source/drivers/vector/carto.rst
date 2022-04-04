.. _vector.carto:

================================================================================
Carto
================================================================================

.. shortname:: CARTO

.. build_dependencies:: libcurl

이 드라이버는 Carto API를 구현한 서비스에 접속할 수 있습니다. Carto 드라이버를 컴파일하려면 GDAL/OGR를 cURL 지원과 함께 빌드해야만 합니다.

이 드라이버는 읽기 및 쓰기 작업을 지원합니다.

드라이버 케이퍼빌리티
-------------------

.. supports_create::

.. supports_georeferencing::

데이터셋 이름 문법
-------------------

Carto 데이터소스를 열기 위한 최소한의 문법은 다음과 같습니다:

.. code-block::

   Carto:[connection_name]

단일 사용자 계정의 경우, 계정명이 connection_name입니다. 다중 사용자 계정의 경우 connection_name이 계정명이 아니라 사용자 이름이어야만 합니다. 
':' 기호 뒤에 선택적인 추가 파라미터를 지정할 수 있습니다. 현재 다음 파라미터를 지원합니다:

-  **tables=table_name1[,table_name2]\**:
   테이블 이름 목록입니다. 예를 들어 공개(public) 테이블에 접근해야 하는 경우 필수입니다.

파라미터 여러 개를 지정하는 경우, 공백으로 구분해야만 합니다.

환경설정 옵션
---------------------

다음 환경설정 옵션들을 사용할 수 있습니다:

-  **CARTO_API_URL**:
   기본값은 https://[account_name].carto.com/api/v2/sql 입니다.
   또다른 서버를 가리키도록 설정할 수 있습니다.

-  **CARTO_HTTPS**:
   https:// 대신 http:// 프로토콜을 사용하려면 NO로 설정하면 됩니다.
   (CARTO_API_URL을 정의하지 않은 경우에만 사용할 수 있습니다.)

-  **CARTO_API_KEY**:
   다음 단락을 참조하십시오.

인증
--------------

작업 대부분에 -- 특히 쓰기 작업에 인증된 접근이 필수입니다. 공개 테이블에 읽기 전용 모드로 접근할 때가 유일한 예외입니다.

Carto 서비스의 관리 인터페이스에서 발행하는 API 키를 지정하면 인증된 접근을 할 수 있습니다.
CARTO_API_KEY 환경설정 옵션으로 API 키를 지정합니다.

도형
--------

OGR 드라이버는 RFC 41에 따라 레이어에서 ('the_geom_webmercator' 필드를 제외한) 사용할 수 있는 모든 도형 필드들을 리포트할 것입니다.

필터링
---------

이 드라이버는 :cpp:func:`OGRLayer::SetSpatialFilter` 함수에 설정된 모든 공간 필터를 서버로 포워딩할 것입니다. :cpp:func:`OGRLayer::SetAttributeFilter` 함수에 설정된 속성 필터도 마찬가지입니다.

페이지 작업(paging)
------------------

기본적으로 서버로부터 객체들을 500개 덩어리로 가져옵니다. CARTO_PAGE_SIZE 환경설정 옵션으로 이 개수를 변경할 수 있습니다.

쓰기 지원
-------------

테이블을 생성하고 삭제할 수 있습니다.

데이터소스를 업데이트 모드로 연 경우에만 쓰기 지원이 활성화됩니다.

Carto 서비스의 작업과 OGR 개념을 다음과 같이 매핑합니다:

- :cpp:func:`OGRFeature::CreateFeature` <==> ``INSERT`` 작업
- :cpp:func:`OGRFeature::SetFeature` <==> ``UPDATE`` 작업
- :cpp:func:`OGRFeature::DeleteFeature` <==> ``DELETE`` 작업
- :cpp:func:`OGRDataSource::CreateLayer` <==> ``CREATE TABLE`` 작업
- :cpp:func:`OGRDataSource::DeleteLayer` <==> ``DROP TABLE`` 작업

:cpp:func:`OGRFeature::CreateFeature` 함수로 새 객체를 삽입할 때 명령어가 성공적으로 실행되었다면, OGR이 반환된 rowid를 가져와서 OGR FID로 사용할 것입니다.

위 작업들은 기본적으로 OGR API 호출과 동시에 서버에 전송됩니다. 하지만 수많은 클라이언트/서버 교환 때문에 수많은 명령어들이 전송되는 경우, 이 때문에 성능이 저하될 수도 있습니다.

따라서 새로 생성된 레이어에 대한 :cpp:func:`OGRFeature::CreateFeature` 의 ``INSERT`` 작업은 총 15MB가 될 때까지 함께 묶습니다. (이 용량은 CARTO_MAX_CHUNK_SIZE 환경설정 옵션을 MB 단위 숫자로 설정해서 변경할 수 있습니다) 15MB에 도달하면 ``INSERT`` 작업들을 서버로 전송합니다. CARTO_MAX_CHUNK_SIZE를 0으로 설정하면 그때 그때 즉시 전송합니다.

.. warning::

   테이블 덮어쓰기 작업에 :cpp:func:`OGRDataSource::DeleteLayer` 및 :cpp:func:`OGRDataSource::CreateLayer` 함수를 이용해서는 안 됩니다. 대신 :cpp:func:`OGRDataSource::CreateLayer` 함수를 OVERWRITE=YES 옵션과 함께 호출하십시오. 이렇게 하면 CARTO 드라이버가 해당 테이블에 의존하는 맵들을 삭제하지 않도록 할 것입니다.

SQL
---

:cpp:func:`OGRDataSource::ExecuteSQL` 함수 호출에 포함되는 SQL 명령어는 OGRSQL 방언을 지정하지 않는 이상 서버 쪽에서 실행됩니다. PostgreSQL + PostGIS SQL 케이퍼빌리티를 100퍼센트 이용할 수 있습니다.

열기 옵션
------------

다음 열기 옵션들을 사용할 수 있습니다:

-  **BATCH_INSERT=YES/NO**:
   객체 삽입 작업을 배치 작업으로 묶을지 여부를 선택합니다. 기본값은 YES입니다. 생성 또는 업데이트 모드에서만 적용됩니다.

-  **COPY_MODE=YES/NO**:
   COPY 모드에서 삽입 및 읽기를 작업하면 성능을 향상시킬 수 있습니다. 기본값은 YES입니다.

레이어 생성 옵션
----------------------

다음 레이어 생성 옵션들을 사용할 수 있습니다:

-  **OVERWRITE=YES/NO**:
   기존 테이블을 생성할 레이어 이름으로 덮어쓸지 여부를 선택합니다. 기본값은 NO입니다.

-  **GEOMETRY_NULLABLE=YES/NO**:
   도형 열의 값이 NULL일 수 있는지 여부를 선택합니다. 기본값은 YES입니다.

-  **CARTODBFY=YES/NO**:
   생성되는 레이어를 "Carto 데이터베이스화"할지 (예를 들면 대시보드에 등록할지) 여부를 선택합니다. 기본값은 YES입니다.
   다음 속성이 필요합니다:

   -  **SRS**:
      산출물의 공간 좌표계가 반드시 EPSG:4326이어야만 합니다. ``-a_srs`` 또는 ``-t_srs`` 를 사용해서 가져오기 전에 EPSG:4326을 할당 또는 EPSG:4326로 변환할 수 있습니다.
   -  **Geometry type**:
      NONE이 아닌 유형이어야만 합니다. ``-nlt GEOMETRY`` 를 사용해서 일반 도형 유형으로 설정할 수 있습니다.

-  **LAUNDER=YES/NO**:
   해당 레이어에 생성되는 새 필드의 이름을 PostgreSQL과 좀 더 호환되는 형식으로 강제 "세탁"하려면 이 옵션을 YES로 설정할 수도 있습니다. 이 옵션은 대문자를 소문자로 변환하고, "-" 및 "#" 같은 몇몇 특수 문자를 "_"로 변환합니다. NO로 설정하면 이름을 그대로 보전합니다. 기본값은 YES입니다. 이 옵션을 활성화하면 테이블(레이어) 이름도 세탁할 것입니다.

예시
--------

공개 테이블의 데이터에 접근하기:

.. code-block::

    ogrinfo -ro "Carto:gdalautotest2 tables=tm_world_borders_simpl_0_3"

shapefile로부터 테이블을 생성하고 채우기:

.. code-block::

    ogr2ogr --config CARTO_API_KEY abcdefghijklmnopqrstuvw -f Carto "Carto:myaccount" myshapefile.shp

EPSG:4326 좌표계를 사용하는 도형들을 담고 있는 CSV 파일로부터 테이블을 생성하고 채우기:

.. code-block::

    ogr2ogr --config CARTO_API_KEY abcdefghijklmnopqrstuvw -f Carto "Carto:myaccount" file.csv -a_srs 4326 -nlt GEOMETRY

.. note::

    CARTODBFY에 ``-a_srs`` 및 ``-nlt`` 를 반드시 지정해줘야 합니다.
    CSV 파일로부터 해당 정보를 추출하지 않기 때문입니다.

참고
--------

-  `Carto API 개요 <https://carto.com/docs/>`_

