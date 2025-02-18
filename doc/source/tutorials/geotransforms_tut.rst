.. _geotransforms_tut:

================================================================================
지리변환 예제
================================================================================

지리변환(geotransform) 소개
---------------------------

지리변환이란 (픽셀, 줄)이라고도 하는 (행, 열) 이미지 좌표 공간으로부터 지리참조된 (투영 또는 지리) 좌표 공간으로의 아핀 변환(affine transformation)을 말합니다.

지리변환은 다음 6개의 계수(coefficient) 집합으로 이루어져 있습니다:

-  ``GT(0)``: 좌상단 픽셀의 좌상단 모서리의 X 좌표입니다.
-  ``GT(1)``: 서-동 픽셀 해상도 / 픽셀 너비입니다.
-  ``GT(2)``: 행 기울기입니다. (일반적으로 0)
-  ``GT(3)``: 좌상단 픽셀의 좌상단 모서리의 Y 좌표입니다.
-  ``GT(4)``: 열 기울기입니다. (일반적으로 0)
-  ``GT(5)``: 북-남 픽셀 해상도 / 픽셀 높이입니다. (북쪽이 위인 이미지의 경우 음의 값)

이미지 좌표 공간으로부터 지리참조된 좌표 공간으로 변환
------------------------------------------------------

.. code-block::

    X_geo = GT(0) + X_pixel * GT(1) + Y_line * GT(2)
    Y_geo = GT(3) + X_pixel * GT(4) + Y_line * GT(5)

이때 픽셀/줄 좌표가 좌상단 픽셀의 좌상단 모서리 (0.0,0.0)에서 시작해서 우하단 픽셀의 우하단 모서리 (width_in_pixels,height_in_pixels)에서 끝난다는 사실을 기억하십시오. 즉 좌상단 픽셀의 중심의 픽셀/줄 위치는 (0.5,0.5)일 것이라는 의미입니다.

북쪽이 위인 이미지의 경우
-------------------------

-  ``GT(2)``, ``GT(4)`` 계수가 0입니다.
-  ``GT(1)``, ``GT(5)`` 이 픽셀 크기입니다.
-  ``GT(0)``, ``GT(3)`` 위치가 래스터의 좌상단 픽셀의 좌상단 모서리 위치입니다.

