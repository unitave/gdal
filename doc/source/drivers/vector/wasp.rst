.. _vector.wasp:

WAsP - WAsP .map 포맷
=======================

.. shortname:: WAsP

.. built_in_by_default::

WAsP 드라이버는 WAsP 소프트웨어가 사용하는 .map 파일 쓰기를 지원합니다. 라인스트링 도형만 쓸 수 있습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::

환경설정 옵션
---------------------

다음 :ref:`환경설정 옵션들 <configoptions>` 을 사용할 수 있습니다:

-  :decl_configoption:`WASP_FIELDS`:
   쉼표로 구분된 필드 목록입니다. 표고의 경우, 고도장(height field)의 이름입니다. 험상(roughness)의 경우, 각각 왼쪽 및 오른쪽 험상 필드의 이름입니다.

-  :decl_configoption:`WASP_MERGE`:
   이 옵션을 NO로 설정할 수도 있습니다. 폴리곤으로부터 험상을 생성하는 경우에만 사용합니다. 모든 폴리곤 경계를 (왼쪽 및 오른쪽 험상이 동일한 폴리곤의 경계를 포함해서) 산출할 것입니다. ('-skipfailures' 옵션과 함께 사용하면) 부정확한 입력 도형을 디버그하는 데 유용합니다.

-  :decl_configoption:`WASP_GEOM_FIELD`:
   입력물이 도형 열을 여러 개 가지고 있는데 (기본값) 첫 번째 열이 올바른 열이 아닌 경우 이 옵션으로 지정할 수 있습니다.

-  :decl_configoption:`WASP_TOLERANCE`:
   ('geos'라고 불리는) 산출물의 라인 단순화 용 허용 오차를 지정합니다.

-  :decl_configoption:`WASP_ADJ_TOLER`:
   이전 포인트로부터 X 및 Y 좌표 둘 다 이 옵션으로 지정한 허용 오차 미만 거리에 있는 포인트를 생략합니다.

-  :decl_configoption:`WASP_POINT_TO_CIRCLE_RADIUS`:
   단순화 때문에 포인트가 된 라인을 포인트 8개인 원(팔각형)으로 대체합니다.

아무 옵션도 지정하지 않는 경우, 레이어를 라인스트링의 포인트의 Z 구성요소가 표고인 표고 레이어로 가정한다는 사실을 기억하십시오.

참고
----

-  `WAsP 홈페이지 <https://www.wasp.dk/wasp>`_

