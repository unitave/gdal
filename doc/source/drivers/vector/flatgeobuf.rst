.. _vector.flatgeobuf:

FlatGeobuf
==========

.. versionadded:: 3.1

.. shortname:: FlatGeobuf

.. built_in_by_default::

이 드라이버는 `FlatGeobuf <https://github.com/bjornharrtell/flatgeobuf>`_ 포맷으로 인코딩된 객체에 접근하기 위한 읽기 및 쓰기 지원을 구현합니다. FlatGeobuf란 단순 피처(Simple Feature) 집합을 담을 수 있는 플랫버퍼(flatbuffer) 기반의 지리 데이터 용 성능 기반에 맞는 바이너리 인코딩 포맷입니다.

드라이버 케이퍼빌리티
-------------------

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::

다중 레이어 지원
-------------------

단일 .fgb 파일은 단일 레이어 하나만 담고 있습니다. 다중 레이어를 지원하려면 디렉터리 하나에 .fgb 파일 여러 개를 넣고 해당 디렉터리 이름을 연결 문자열로 사용하면 됩니다.

생성 작업 시, .fgb 접미어 없이 파일명을 전송하면 드라이버가 해당 이름의 디렉터리를 생성하고 그 디렉터리에 레이어들을 .fgb 파일들로 생성할 것입니다.

열기 옵션
------------

-  **VERIFY_BUFFERS=YES/NO**:
   이 옵션을 YES로 설정하면 읽어올 때 버퍼를 검증합니다. 성능은 저하되지만 무결하지 않은 또는 오류가 있는 데이터를 방지할 수 있습니다. 기본값은 YES입니다.

데이터셋 생성 옵션
------------------------

없습니다

레이어 생성 옵션
----------------------

-  **SPATIAL_INDEX=YES/NO**:
   이 옵션을 YES로 설정하면 공간 색인을 생성합니다. 기본값은 YES입니다.

-  **TEMPORARY_DIR=path**:
   임시 파일을 생성해야 할 기존 디렉터리를 가리키는 경로입니다. SPATIAL_INDEX=YES인 경우에만 사용할 수 있습니다. 지정하지 않는 경우, 정규 파일명에 대해 산출 파일 디렉터리를 사용할 것입니다. 다른 VSI 파일 시스템의 경우, :cpp:func:`CPLGenerateTempFilename` 함수가 지정하는 임시 디렉터리를 사용할 것입니다. 인 메모리 임시 파일의 경우 "/vsimem/"을 사용할 수 있습니다.

예시
--------

-  단일 shapefile을 FlatGeobuf 파일로 단순 변환합니다. abc.shp로부터 객체를 그리고 abc.dbf로부터 속성을 가져와서 'filename.fgb' 파일을 생성할 것입니다. 파일 생성 시 ``filename.fgb`` 파일이 이미 존재해서는 절대로 **안 됩니다**.

   ::

      ogr2ogr -f FlatGeobuf filename.fgb abc.shp

-  다중 레이어를 가진 지오패키지 파일을 변환합니다:

   ::

      ogr2ogr -f FlatGeobuf my_fgb_dataset input.gpkg

참고
--------

-  `깃허브의 FlatGeobuf <https://github.com/bjornharrtell/flatgeobuf>`_

