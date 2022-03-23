.. _raster.leveller:

================================================================================
Leveller -- Daylon Leveller 고도장
================================================================================

.. shortname:: Leveller

.. built_in_by_default::

Leveller 고도장(heightfield)은 32비트 표고값을 저장합니다. 여러 가지 주의 사항과 함께 (아래 참조) 지원합니다. Leveller 고도장 파일의 확장자는 ".TER"입니다. (Terragen 파일과 동일하지만, 이 드라이버는 Leveller 파일만 인식합니다.)

블록은 픽셀 높이 스캔 라인(행)으로 이루어져 있습니다. 첫 번째 스캔 라인이 DEM의 최상단(북단) 경계에 있고, 인접 픽셀들은 왼쪽에서 오른쪽 방향으로 (서쪽에서 동쪽으로) 이어집니다.

포맷 버전 4 및 5가 물리적으로 16.16 고정 소수점 방식(fixed-point)을 사용하긴 하지만, 밴드 데이터 유형은 언제나 Float32 유형입니다. 드라이버가 데이터를 부동소수점형으로 자동 변환합니다.

드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::

읽기
-------

``dataset::GetProjectionRef()`` 는 포맷 버전 4에서 6까지 지역 좌표계만 반환할 것입니다.

``dataset::GetGeoTransform()`` 은 포맷 버전 4에서 6까지 중심 원점 기준 단순 지구 크기 조정(simple world scaling)을 반환합니다. 7 이상 버전의 경우, 기울기를 제외한 실제 지구 변환(real-world transform)을 반환합니다. 항등 변환(identity transform)을 오류 조건으로 간주하지 않습니다. Leveller 문서에서 자주 사용되기 때문입니다.

``band::GetUnitType()`` 은 파일이 사용하는 일반적이지 않은 단위 유형을 미터로 변환하는 대신 파일이 사용하는 측정 단위를 그대로 리포트할 것입니다. ``levellerdataset.cpp`` 모듈이 단위 유형 목록을 가지고 있습니다.

``band::GetScale()`` 및 ``band::GetOffset()`` 은 표고 데이터 모델을 물리->논리(physical-to-logical) 변환해서 반환할 것입니다. (예: RAW->실제 지구)

쓰기
-------

``dataset::Create()`` 호출을 지원하지만, 포맷 버전 7에서만입니다.

``band::SetUnitType()`` 을 ``levellerdataset.cpp`` 모듈의 어떤 단위 유형으로도 설정할 수 있습니다.

``dataset::SetGeoTransform()`` 이 기울기 데이터를 포함해서는 안 됩니다.

Terragen 드라이버와 마찬가지로, ``MINUSERPIXELVALUE`` 옵션을 지정해줘야만 합니다. 이 옵션은 드라이버가 논리(실제 지구) 표고로부터 물리 표고로 정확하게 매핑할 수 있도록 해줍니다.

``band::IWriteBlock`` 을 처음 호출할 때 헤더 정보를 작성합니다.

참고
---------

-  ``gdal/frmts/leveller/levellerdataset.cpp`` 로 구현되었습니다.

-  Leveller 포맷 문서를 정리한 Leveller SDK가 있는 `Daylon Graphics <http://www.daylongraphics.com>`_ 를 방문해보십시오.
