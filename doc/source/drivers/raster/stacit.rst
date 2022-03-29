.. _raster.stacit:

================================================================================
STACIT - 시공간 자산 카탈로그 항목(Spatio-Temporal Asset Catalog Items)
================================================================================

.. versionadded:: 3.4

.. shortname:: STACIT

.. built_in_by_default::

이 드라이버는 JSON 파일 또는 또는 일반적으로 원격 쿼리의 결과물의 읽기를 지원합니다.
이들은 `STAC 컬렉션 <https://github.com/radiantearth/stac-api-spec/blob/master/stac-spec/collection-spec/collection-spec.md>`_ 의 ``items`` 링크로, 이 항목들은 `투영법 확장 사양 <https://github.com/stac-extensions/projection/>`_ 도 구현합니다. 이 드라이버는 항목들로부터 가상 모자이크를 작성합니다.

하위 데이터셋을 하나도 가지고 있지 않은 STACIT 데이터셋은 사실 :ref:`raster.vrt` 데이터셋입니다. 따라서 이런 STACIT 데이터셋을 VRT로 변환하면 항목들을 직접 참조하는 VRT 파일을 생성할 것입니다.

열기 문법
-----------

다음 문법 가운데 하나로 STACIT 데이터셋/하위 데이터셋에 접근할 수 있습니다:

* ``filename.json``: 로컬 파일

* ``STACIT:"https://example.com/filename.json"``: 원격 파일

* ``STACIT:"filename.json":asset=my_asset``: 로컬/원격 파일의 자산을 지정합니다.

* ``STACIT:"filename.json":collection=my_collect,asset=my_asset``: 로컬/원격 파일의 자산 및 컬렉션을 지정합니다.

* ``STACIT:"filename.json":collection=my_collect,asset=my_asset,crs=my_crs``: 컬렉션, 자산, 그리고 로컬/원격 파일의 좌표계를 지정합니다.

열기 옵션
------------

다음 열기 옵션들을 지원합니다:

-  **MAX_ITEMS= number**:
   가져올 항목들의 최대 개수를 설정합니다. 0은 무제한이라는 뜻입니다. 기본값은 1000입니다.

-  **COLLECTION=string**:
   항목을 필터링할 컬렉션의 이름을 설정합니다.

-  **ASSET=string**:
   항목을 필터링할 자산의 이름을 설정합니다.

-  **CRS=string**:
   항목을 필터링할 좌표계의 이름을 설정합니다.

-  **RESOLUTION=AVERAGE/HIGHEST/LOWEST**:
   데이터셋 해상도를 결정하기 위해 사용할 전략을 설정합니다. 기본값은 AVERAGE입니다.

하위 데이터셋
------------

STACIT JSON 파일이 컬렉션, 자산 또는 좌표계 여러 개를 담고 있는 경우, 이 드라이버는 사용 가능한 하위 데이터셋 각각을 열 수 있는 하위 데이터셋 이름 목록을 반환할 것입니다.

드라이버 케이퍼빌리티
-------------------

.. supports_virtualio::

예시
--------

지정한 컬렉션, 경계 상자에 대한 `STAC 검색 <https://github.com/radiantearth/stac-api-spec/tree/master/item-search>`_ 과 관련된 하위 데이터셋을 날짜/시간(datetime)으로부터 시작하도록 목록화합니다:

::

    gdalinfo "STACIT:\"https://planetarycomputer.microsoft.com/api/stac/v1/search?collections=naip&bbox=-100,40,-99,41&datetime=2019-01-01T00:00:00Z%2F..\""


앞의 요청으로 반환되는 하위 데이터셋을 엽니다:

::

    gdalinfo "STACIT:\"https://planetarycomputer.microsoft.com/api/stac/v1/search?collections=naip&bbox=-100,40,-99,41&datetime=2019-01-01T00:00:00Z%2F..\":asset=image"


참고
--------

-  :ref:`raster.stacta` 드라이버

