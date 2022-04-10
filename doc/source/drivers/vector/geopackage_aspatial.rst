.. _vector.geopackage_aspatial:

지오패키지 비공간 확장 사양
=============================

지오패키지 1.0 확장 사양

이 확장 사양은 OGC `지오패키지 1.0 사양`_ 의 첨부 I(Annex I)의 템플릿을 따릅니다.

확장 사양 제목
---------------

비공간(Aspatial) 지원

소개
^^^^^^^^^^^^

관련 메타데이터를 가지고 있을 수도 있는 (예를 들면 도형 열이 없는 SQLite 테이블/뷰 같은) 비공간 데이터를 지원합니다.

이 확장 사양은 지오패키지 1.2버전의 "attributes" data_type이 도입되기 전, GDAL 2.0 및 2.1버전에서 쓰였습니다. GDAL 2.2버전부터, 기본적으로 "attributes"를 사용할 것이기 때문에 이 확장 사양은 현재 레거시 사양이 되었습니다.

확장 사양 저자
^^^^^^^^^^^^^^^^

`GDAL - 지리공간 데이터 추상 라이브러리(Geospatial Data Abstraction Library)`_, author_name은 'gdal'입니다.

확장 사양 이름 또는 템플릿
^^^^^^^^^^^^^^^^^^^^^^^^^^

SQL

.. code-block:: sql

    INSERT INTO gpkg_extensions
    (table_name, column_name, extension_name, definition, scope)
    VALUES
    (
        NULL,
        NULL,
        'gdal_aspatial',
        'http://gdal.org/geopackage_aspatial.html',
        'read-write'
    );

확장 사양 유형
^^^^^^^^^^^^^^

기존 요구 사항의 확장 사양은 2번 절에 있습니다.

적용 가능성
^^^^^^^^^^^^^

이 확장 사양은 ``gpkg_contents`` 테이블에서 "data_type" 열의 값이 소문자 "aspatial"로 지정된 모든 비공간 사용자 데이터 테이블 또는 뷰에 적용됩니다.

스코프
^^^^^

읽기-쓰기

요구 사항
^^^^^^^^^^^^

지오패키지
""""""""""

'contents' 테이블 - Aspatial

'gpkg_contents' 테이블이 각 비공간 사용자 데이터 테이블 또는 뷰에 "data_type" 열의 값이 소문자 "aspatial"인 행을 담고 있어야 합니다.

사용자 데이터 테이블

앞의 "'contents' 테이블 - Aspatial" 절에서 설명하는 확장 지오패키지(Extended GeoPackage)에 있는 비공간 테이블의 SQL 스키마의 두 번째 구성요소는 비공간 사용자 데이터를 담고 있는 사용자 테이블 또는 뷰입니다.

사용자 데이터 테이블을 담기 위해 비공간을 지원하는 확장 지오패키지를 요구하지 않습니다. 사용자 데이터 테이블이 비어 있을 수도 있기 때문입니다.

비공간을 지원하는 확장 지오패키지가 테이블 또는 뷰를 담고 있을 수도 있습니다. 이런 비공간 테이블 또는 뷰는 EXAMPLE 별로 INTEGER 및 PRIMARY KEY AUTOINCREMENT 열 제약 조건 열 유형인 열을 가질 수도 있습니다.


.. list-table:: Aspatial User Data Table
   :header-rows: 1

   * - 열 이름
     - 유형
     - 설명
     - NULL
     - 기본값
     - 키
   * - `id`
     - INTEGER
     - 자동 증가 기본 키
     - Ｘ
     -
     - PK
   * - `text_attribute`
     - TEXT
     - 행의 텍스트 속성
     - Ｏ
     -
     -
   * - `real_attribute`
     - REAL
     - 행의 실수 속성
     - Ｏ
     -
     -
   * - `boolean_attribute`
     - BOOLEAN
     - 행의 불(boolean) 속성
     - Ｏ
     -
     -
   * - `raster_or_photo`
     - BLOB
     - 사진
     - Ｏ
     -
     -

비공간 테이블 또는 뷰의 정수형 기본 키는 2.4.3 메타데이터 참조 테이블 절에 설명된 대로 'pkg_metadata_reference' 테이블에 있는 `SQLite ROWID`_ 를 이용해서 객체를 'gpkg_metadata' 테이블에 있는 행 수준 메타데이터 레코드와 링크할 수 있게 해줍니다.

비공간 테이블 또는 뷰가 도형 열을 가지고 있어서는 안 됩니다.

비공간 테이블 또는 뷰에 있는 열은 1.1.1.1.3 절의 1번 표에 지정된 데이터 유형만을 사용해서 정의되어야 합니다.

지오패키지 SQLite 환경설정
"""""""""""""""""""""""""""""""

없습니다.

지오패키지 SQLite 확장 사양
"""""""""""""""""""""""""""

없습니다.

.. _`지오패키지 1.0 사양`: http://www.geopackage.org/
.. _`GDAL - 지리공간 데이터 추상 라이브러리(Geospatial Data Abstraction Library)`: http://gdal.org
.. _`SQLite ROWID`: http://www.sqlite.org/lang_createtable.html#rowid
