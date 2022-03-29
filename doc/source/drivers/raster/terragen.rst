.. _raster.terragen:

================================================================================
Terragen -- Terragen™ 지형 파일
================================================================================

.. shortname:: Terragen

.. built_in_by_default::

Terragen 지형 파일은 선택적인 그리드 간격 정보(gridspacing)를 가진 (그러나 배치 정보(positioning)는 없는) 16비트형 표고값을 저장합니다. Terragen 고도장(heightfield)의 파일 확장자는 "TER" 또는 "TERRAIN"입니다. (이때 .TER는 Leveller 포맷의 파일 확장자와 동일하지만, 이 드라이버는 Terragen 파일만 인식할 것입니다.) 드라이버 ID는 "Terragen"입니다. 데이터셋은 파일 기반으로 표고 밴드 1개만 가지고 있습니다. 고도 보이드(void elevation)는 지원하지 않습니다. 픽셀을 포인트로 간주합니다.


드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::

읽기
-------

-  ``dataset::GetProjectionRef()`` 는 미터법을 사용하는 로컬 좌표계를 반환합니다.

-  ``band::GetUnitType()`` 은 미터를 반환합니다.

-  표고는 ``Int16`` 데이터 유형입니다. 이 값을 미터 단위로 변환하려면 ``band::GetScale()`` 및 ``band::GetOffset()`` 을 사용해야만 합니다.


쓰기
-------

-  ``Create`` 호출을 사용하십시오. ``MINUSERPIXELVALUE`` (부동소수점형) 옵션을 사용자 표고 데이터에서 가장 낮은 표고값으로, ``MAXUSERPIXELVALUE`` 를 가장 높은 표고값으로 설정하십시오. 이때 표고 단위가 사용자가 ``band::SetUnitType()`` 에 입력한 표고 단위와 일치해야만 합니다.

-  ``dataset::SetProjection()`` 및  ``dataset::SetGeoTransform()`` 을 사용자의 좌표계 상세 정보와 함께 호출하십시오. 그렇지 않으면 드라이버가 물리적 표고를 제대로 인코딩하지 못 할 것입니다. (도 단위 기반) 지리 좌표계를 로컬 미터 단위 기반 좌표계로 변환할 것입니다.

-  정밀도를 유지하기 위해, 최적 기반 높이(base height)와 크기 조정(scaling)을 사용해서 가능한 한 넓은 16비트 범위를 사용할 것입니다.

-  표고는 ``Float32`` 데이터 유형입니다.


좌표계 문제점
-------------

도 단위 기반 좌표계를 작성하는 경우 한 번 실행할 때마다 표고값은 몇 센티미터 그리고 지표 범위는 1 또는 2미터까지 오류가 나는 경향이 있습니다. 이 드라이버가 현재 미터법만 사용하기 때문에, 대용량 도 단위 기반 DEM의 경우 왜곡 발생을 피할 수 없습니다.

참고
--------

-  ``gdal/frmts/terragen/terragendataset.cpp`` 로 구현되었습니다.

-  설치 및 지원 정보를 알고 싶다면 `readme.txt <./readme.txt>`_ 파일을 읽어보십시오.

-  `Terragen 지형 파일 사양 <http://www.planetside.co.uk/terragen/dev/tgterrain.html>`_

