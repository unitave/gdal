.. _raster.marfa:

================================================================================
MRF -- 메타 래스터 포맷
================================================================================

.. shortname:: MRF

.. versionadded:: 2.1

.. built_in_by_default::

색인된 정규 타일(블록) 덩어리에 접근합니다. 일반적으로 0수준이 전체 해상도 이미지인 오버뷰 피라미드 구조로 된 XML 파일로 제어합니다. NONE, PNG, JPEG, ZLIB 타일 패킹(packing)을 구현했습니다.

파일 생성 옵션은 "gdalinfo --format MRF" 명령어로 참조하십시오.

드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::

링크
-----

-  `MRF 사용자 지침서 <https://github.com/nasa-gibs/mrf/blob/master/doc/MUG.md>`_
-  `MRF 사양 <https://github.com/nasa-gibs/mrf/blob/master/spec/mrf_spec.md>`_
-  `소스 저장소 nasa-gibs/mrf <https://github.com/nasa-gibs/mrf>`_
