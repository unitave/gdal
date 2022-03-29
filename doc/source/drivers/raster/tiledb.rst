.. _raster.tiledb:

================================================================================
TileDB - TileDB
================================================================================

.. shortname:: TileDB

.. versionadded:: 3.0

.. build_dependencies:: TileDB

GDAL은 TileDB 라이브러리를 통해 TileDB 배열을 읽고 쓸 수 있습니다.

이 드라이버는 오픈소스 `TileDB 라이브러리 <https://github.com/TileDB-Inc/TileDB>`_ (MIT 사용 허가)를 의존합니다.

드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::

생성 옵션
----------------

여러 생성 옵션과 열기 옵션이 존재하지만, 그 중에서도:

-  **TILEDB_CONFIG=config**:
   `TileDB 환경설정 옵션 <https://docs.tiledb.io/en/stable/tutorials/config.html>`_ 을 가지고 있는 로컬 파일을 설정합니다.

참고
--------

-  `TileDB 홈페이지 <https://tiledb.io/>`_
