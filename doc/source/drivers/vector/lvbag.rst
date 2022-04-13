.. _vector.lvbag:

================================================================================
네덜란드 Kadaster LV BAG 2.0 추출
================================================================================
.. versionadded:: 3.2


.. shortname:: LVBAG

.. build_dependencies:: libexpat

LVBAG 드라이버는 네덜란드 Kadaster BAG 상품이 제공하는 LV BAG 2.0 추출 포맷의 XML 파일을 읽어올 수 있습니다. 모든 LV BAG 2.0 추출 상품을 지원합니다. 이 드라이버는 BAG 2.0버전에서 도입된 레이어를 포함, 모든 BAG 레이어를 지원합니다.

GDAL/OGR를 Expat 라이브러리를 대상으로 컴파일했을 경우에만 이 드라이버를 사용할 수 있습니다.

각 추출 XML 파일은 단일 OGR 레이어 하나로 표현됩니다. 이 레이어는 자신의 네이티브(EPSG:28992) 공간 좌표계에서 지리참조됩니다.

https://www.kadaster.nl/zakelijk/producten/adressen-en-gebouwen/bag-2.0-extract 에서 LV BAG 2.0 포맷에 대한 더 많은 정보를 찾아볼 수 있습니다.

LV BAG 모델 정의는 https://developer.kadaster.nl/schemas/-/categories/4119958 에 있습니다.

주의 1: 이 드라이버는 초기 BAG 1.0 추출 포맷을 **지원하지 않습니다**.

주의 2: 이 드라이버는 ST(Standaard Levering) 추출 파일만 읽어올 것입니다. ML(Mutatie Levering) 변이형 파일은 지원하지 않습니다.

열기 옵션
------------

다음 열기 옵션들을 (일반적으로 ogrinfo 또는 ogr2ogr 유틸리티의 ``-oo name=value`` 파라미터를 통해) 지정할 수 있습니다:

-  **AUTOCORRECT_INVALID_DATAYES/NO**: (기본값은 NO)
   객체가 무결하지 않은 또는 오류를 일으키는 데이터를 담고 있는 경우 드라이버가 데이터를 수정하려 시도해야만 할지 여부를 선택합니다. 일반적으로 (GEOS 3.8.0 이상 버전을 이용해서) 무결하지 않은 도형, 날짜, 객체 상태 등등을 수정하는 작업을 포함합니다.

-  **LEGACY_ID=YES/NO**: (기본값은 NO)
   BAG 식별자를 BAG 1.0 포맷과 호환되는 서식으로 작성할지 여부를 선택합니다.

VSI 가상 파일 시스템 API 지원
-----------------------------------

이 드라이버는 VSI 가상 파일 시스템 API가 관리하는 파일의 읽기 및 쓰기를 지원합니다. VSI 가상 파일 시스템 API가 관리하는 파일에는 "정규" 파일은 물론 /vsizip/ 도메인에 있는 파일도 포함됩니다. 아래 예시를 참조하십시오.
The driver supports reading from files managed by VSI Virtual File
System API, which include "regular" files, as well as files in the
/vsizip/ domain. See examples below.

드라이버 케이퍼빌리티
-------------------

.. supports_virtualio::

예시
--------

-  ogr2ogr 유틸리티를 사용해서 LV BAG 추출 파일을 GeoJSON 형식의 WGS84로 변환한 결과물을 덤프하기:

   ::

      ogr2ogr -t_srs EPSG:4326 -f GeoJSON output.json 9999PND01012020_000001.xml

-  추출 파일의 내용을 OGR가 인식하는 대로 덤프하는 방법:

   ::

      ogrinfo -ro 9999PND01012020_000001.xml

-  복구된 객체를 WGS84 도형으로 LV BAG 추출 압축 파일로부터 PostgreSQL로 삽입하기. 9999PND18122019.zip 파일로부터 나온 객체들로 'pand' 테이블을 생성할 것입니다. 데이터베이스 인스턴스(lvbag)는 이미 존재해야만 하고, 'pand' 테이블이 이미 존재해서는 안 됩니다.

   ::

      ogr2ogr -oo AUTOCORRECT_INVALID_DATA=YES -t_srs EPSG:4326 -f PostgreSQL PG:dbname=lvbag /vsizip/9999PND18122019.zip

- LV BAG 추출 디렉터리를 Postgres로 불러오기:

   ::

     ogr2ogr \
       -f "PostgreSQL" PG:dbname="my_database" \
       9999PND18122019/ \
       -nln "name_of_new_table"

- 'Nummeraanduiding' 데이터셋으로부터 지오패키지를 생성하기:

   ::

     ogr2ogr \
       -f "GPKG" nummeraanduiding.gpkg \
       0000NUM01052020/

참고
--------

-  `Kadaster LV BAG 2.0 페이지 <https://www.kadaster.nl/zakelijk/producten/adressen-en-gebouwen/bag-2.0-extract>`_ (네덜란드어)

