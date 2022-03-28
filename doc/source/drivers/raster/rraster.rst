.. _raster.rraster:

================================================================================
RRASTER -- R 래스터
================================================================================

.. shortname:: RRASTER

.. versionadded:: 2.2

.. built_in_by_default::

이 드라이버는 `R 래스터 패키지 <https://cran.r-project.org/web/packages/raster/index.html>`_ 가 처리하는 데이터셋을 위한 읽기 전용 판독기입니다. 이런 데이터셋은 .grd 텍스트 헤더 파일과 래스터 데이터 자체를 담고 있는 .gri 바이너리 파일로 이루어져 있습니다. GDAL은 .grd 파일을 엽니다. GDAL 2.3버전부터, 이 드라이버는 합리값(ratvalue; 정수 또는 분수값)을 RAT 또는 색상표로 읽어옵니다. GDAL 밴드 설명에 레이어 이름을 할당할 것입니다. GDAL 'CREATOR' 및 'CREATED' 데이터셋 메타데이터 항목에 '[general]' 부분의 'creator' 및 'created' 속성을 할당할 것입니다.

GDAL 2.3버전부터, 이 드라이버는 쓰기를 지원합니다. 색상표 또는 RAT을 작성할 것입니다. 'CREATOR' 및 'CREATED' 데이터셋 메타데이터 항목을 '[general]' 부분의 'creator' 및 'created' 속성으로 작성할 것입니다. 밴드 설명은 '[description]' 부분의 'layername' 속성으로 작성할 것입니다.


Driver capabilities
-------------------

.. supports_createcopy::

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::


생성 옵션
---------

다음 생성 옵션들을 지원합니다:

-  **INTERLEAVE=BIP/BIL/BSQ**: 지정한 교차삽입 유형을 강제로 생성합니다.
  
   - **BIP** --- 픽셀 단위 밴드(band interleaved by pixel)
   - **BIL** -- 라인 단위 밴드(band interleaved by line)
   - **BSQ** -- 밴드 단위 밴드(band sequential)
   
   GDAL 3.5버전부터, INTERLEAVE 메타데이터 항목을 노출하는 다중 밴드를 가진 소스 데이터셋으로부터 복사할 때 INTERLEAVE 생성 옵션을 지정하지 않는다면 소스 데이터셋의 INTERLEAVE를 자동적으로 연산에 넣을 것입니다.

-  **PIXELTYPE=SIGNEDBYTE**:
   바이트형 밴드를 부호 없는 바이트가 아니라 부호 있는 바이트형으로 작성합니다.


참고
--------

-  `"rasterfile" 포맷 <https://rspatial.org/raster/pkg/appendix2.html>`_ 설명

