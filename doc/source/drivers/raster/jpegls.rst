.. _raster.jpegls:

================================================================================
JPEGLS
================================================================================

.. shortname:: JPEGLS

.. build_dependencies:: CharLS 라이브러리

.. deprecated_driver:: version_targeted_for_removal: 3.5
   env_variable: GDAL_ENABLE_DEPRECATED_DRIVER_JPEGLS

이 드라이버는 오픈소스 CharLS 라이브러리(BSD 스타일 사용 허가)를 기반으로 구현한 JPEG-LS 판독기/작성기입니다.

이 드라이버는 비손실 또는 준-비손실(near-lossless) 이미지를 읽고 쓸 수 있습니다. (가상 메모리가 충분한 경우를 제외하면) 이 드라이버의 목적이 너무 큰 이미지를 처리하려는 것이 아니라는 사실을 기억하십시오. 전체 이미지를 단일 작업으로 압축/압축 해제해야만 하기 때문입니다.

드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::

.. supports_virtualio::

생성 옵션
----------------

-  **INTERLEAVE=PIXEL/LINE/BAND**:
   압축 스트림에서의 데이터 교차삽입 방식을 설정합니다. 기본값은 BAND입니다.

-  **LOSS_FACTOR=error_threshold**:
   기본값 0은 비손실 압축을 의미합니다. 0보다 큰 값은 최대 오류 한계값이 될 것입니다.

참고
---------

-  ``gdal/frmts/jpegls/jpeglsdataset.cpp`` 로 구현되었습니다.

-  `CharLS 라이브러리 홈페이지 <https://github.com/team-charls/charls>`_
