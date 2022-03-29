.. _raster.stacta:

================================================================================
STACTA - 시공간 자산 카탈로그 타일화 자산
================================================================================

.. versionadded:: 3.3

.. shortname:: STACTA

.. built_in_by_default::

이 드라이버는 `시공간 자산 카탈로그 타일화 자산(Spatio-Temporal Asset Catalog Tiled Assets) <https://github.com/stac-extensions/tiled-assets>`_ 사양을 따르는 JSON 파일 열기를 지원합니다. 이런 JSON 파일은 타일 작업 스키마에 따르면 대용량일 가능성이 있는 데이터셋으로부터 분할된 (메타타일이라고도 하는) 확대/축소 수준 여러 개를 가진 타일들을 참조합니다. 이 드라이버는 JSON 파일이 서술하는 데이터셋의 단일 래스터 뷰를 오버뷰와 함께 제공합니다. 이 드라이버는 임의 크기의 메타타일을 지원합니다.

열기 문법
-----------

다음 문법 가운데 하나로 STACTA 데이터셋/하위 데이터셋에 접근할 수 있습니다:

* ``filename.json``: 로컬 파일

* ``STACTA:"https://example.com/filename.json"``: 원격 파일

* ``STACTA:"filename.json":my_asset``: 로컬/원격 파일의 자산을 지정합니다.

* ``STACTA:"filename.json":my_asset:my_tms``: 로컬/원격 파일의 자산과 타일 작업 스키마를 지정합니다.

JSON 파일의 루트가 ``Feature`` 유형이어야만 합니다.

열기 옵션
------------

다음 열기 옵션들을 지원합니다:

-  **WHOLE_METATILE=YES/NO**:
   이 옵션을 YES로 설정하면, 메타타일 전체를 (메모리로) 다운로드할 것입니다. 기본값 NO로 설정하는 경우, 메타파일 용량이 한계값을 초과한다면 구분적인(piece-wise) 방식으로 메타타일에 접근할 것입니다.

-  **SKIP_MISSING_METATILE=YES/NO**:
   이 옵션을 YES로 설정하면, 오류를 발생시키지 않고 누락된 메타타일을 건너뛸 것입니다. 데이터셋에서 누락 메타타일에 해당하는 영역은 NODATA 값으로, 또는 NODATA 값이 없는 경우 0으로 채워질 것입니다. :decl_configoption:`GDAL_STACTA_SKIP_MISSING_METATILE` 환경설정 옵션으로도 이 설정을 할 수 있습니다.

하위 데이터셋
------------

STACTA JSON 파일이 컬렉션, 자산 템플릿 여러 개 그리고/또는 타일 작업 스키마를 담고 있는 경우, 이 드라이버는 사용 가능한 하위 데이터셋 각각을 열 수 있는 하위 데이터셋 이름 목록을 반환할 것입니다.

드라이버 케이퍼빌리티
-------------------

.. supports_virtualio::

참고
--------

-  :ref:`raster.stacit` 드라이버

