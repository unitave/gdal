.. _raster.iris:

================================================================================
IRIS -- 바이살라(Vaisala) 사의 기상 레이더 소프트웨어 포맷
================================================================================

.. shortname:: IRIS

.. built_in_by_default::

이 읽기전용 GDAL 드라이버는 IRIS 기상 레이더 소프트웨어가 생성하는 상품에 접근하기 위해 개발되었습니다.

IRIS 소프트웨어 포맷은 여러 가지 상품을 포함하는데, 래스터가 아닌 포맷도 있습니다. 이 드라이버는 현재 다음 포맷들을 읽을 수 있습니다:

-  PPI (반사율 및 속도): 평면 위치 표시기(Plan Position Indicator)
-  CAPPI: 정고도(Constant Altitude) PPI
-  RAIN1: 1시간 누적 강수량(hourly rainfall accumulation)
-  RAINN: N시간 누적 강수량(N-Hour rainfall accumulation)
-  TOPS: 선택 가능한 dBZ(레이더 반사율) 윤곽(contour)의 높이
-  VIL: 선택 레이어의 수직 통합 액체(vertically integrated liquid)
-  MAX: Column Max Z WF W/NS 구간(section)

대부분의 메타데이터를 읽어옵니다.

http://www.vaisala.com/en/defense/products/weatherradar/Pages/IRIS.aspx 에서 바이살라 사의 포맷과 소프트웨어에 대한 정보를 찾아볼 수 있습니다.

주의: ``gdal/frmts/iris/irisdataset.cpp`` 로 구현되었습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

.. supports_virtualio::

