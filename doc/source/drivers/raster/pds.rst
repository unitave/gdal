.. _raster.pds:

================================================================================
PDS -- 행성 데이터 시스템 v3
================================================================================

.. shortname:: PDS

.. built_in_by_default::

PDS(Planetary Data System)는 NASA가 태양, 달 및 행성 영상 데이터를 저장하고 배포하기 위해 주로 사용하는 포맷입니다. GDAL은 PDS 포맷 영상 데이터에 읽기전용 접근을 지원합니다.

PDS 파일의 확장자는 거의 .img이며, 관련 .lbl 라벨 파일을 가지고 있는 경우도 있습니다. .lbl 파일이 존재하는 경우 .img 파일보다는 .lbl 파일을 데이터셋 이름으로 사용해야 합니다.

또한 거의 모든 PDS 영상 환경설정을 지원하기 위해, 이 드라이버는 지리참조와 좌표계 정보는 물론 선택한 다른 헤더 메타데이터도 읽어옵니다.

이 드라이버는 미국 지질조사국(United States Geological Survey)의 지원으로 구현되었습니다.

.. note::
    PDS3 데이터셋은 VICAR 헤더를 도입했습니다. GDAL은 이런 상황에서 기본적으로 PDS 드라이버를 사용할 것입니다. GDAL 3.1버전부터, :decl_configoption:`GDAL_TRY_PDS3_WITH_VICAR` 환경설정 옵션을 YES로 설정한 경우, :ref:`VICAR <raster.vicar>` 드라이버로 데이터셋을 열 것입니다.

드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

.. supports_virtualio::

지리참조 작업
--------------

PDS 사양의 모호함 때문에 일부 상품의 지리참조 정보가 미묘하게 또는 전체적으로 부정확합니다. 이런 상품의 지리참조 정보의 해석을 수정하기 위해 설정할 수도 있는 환경설정 변수들이 있습니다. `티켓 #5941 <http://trac.osgeo.org/gdal/ticket/5941>`_ 및 `티켓 #3940 <http://trac.osgeo.org/gdal/ticket/3940>`_ 에서 자세한 내용을 찾아볼 수 있습니다.

테스트를 위해 달의 `LOLA DEM <http://pds-geosciences.wustl.edu/missions/lro/lola.htm>`_ 이 필요합니다. `LOLA PDS 라벨 <http://pds-geosciences.wustl.edu/lro/lro-l-lola-3-rdr-v1/lrolol_1xxx/data/lola_gdr/cylindrical/img/ldem_4.lbl>`_ 과 `LOLA PDS v3 이미지 <http://pds-geosciences.wustl.edu/lro/lro-l-lola-3-rdr-v1/lrolol_1xxx/data/lola_gdr/cylindrical/img/ldem_4.img>`_ 에서 라벨과 이미지를 둘 다 다운로드하십시오. 어떤 환경설정 옵션도 없이 gdalinfo를 통해 리포트된 중심이 데카르트 공간에서 완벽하게 0.0, 0.0미터 위치에 있어야 합니다:

::

   $ gdalinfo ldem_4.lbl

GeoTiff 변환 예시:

::

   $ gdal_translate ldem_4.lbl out_LOLA.tif

일부 PDS 라벨에 정의된 오프셋과 곱수(multiplier) 값을 적용해서 변환하는 예시:

::

   $ gdal_translate -ot Float32 -unscale ldem_4.lbl out_LOLA_32bit.tif

--------------

오프셋 문제점을 수정하는 예시를 보이려면 PDS 포맷의 `MOLA DEM <http://pds-geosciences.wustl.edu/missions/mgs/megdr.html>`_ 이 필요합니다. `MOLA PDS 라벨 <http://pds-geosciences.wustl.edu/mgs/mgs-m-mola-5-megdr-l3-v1/mgsl_300x/meg004/megt90n000cb.lbl>`_ 과 `MOLA PDS v3 이미지 <http://pds-geosciences.wustl.edu/mgs/mgs-m-mola-5-megdr-l3-v1/mgsl_300x/meg004/megt90n000cb.img>`_ 를 둘 다 다운로드하십시오. 현재 MOLA 라벨이 1픽셀 오프셋을 담고 있습니다. 이 파일을 정확하게 읽어오려면, 다음 옵션으로 GDAL을 사용하십시오:

::

   $ gdalinfo --config PDS_SampleProjOffset_Shift -0.5 --config PDS_LineProjOffset_Shift -0.5 megt90n000cb.lbl

마찬가지로, 이런 선택적인 파라미터로 gdalinfo를 통해 리포트된 중심이 데카르트 공간에서 완벽하게 0.0, 0.0미터 위치에 있어야 합니다.

MOLA 데이터의 변환 예시:

::

   $ gdal_translate --config PDS_SampleProjOffset_Shift -0.5 --config PDS_LineProjOffset_Shift -0.5 megt90n000cb.lbl out_MOLA_4ppd.tif

일부 PDS 라벨에 정의된 오프셋과 곱수(multiplier) 값을 적용해서 변환하는 예시:

::

   $ gdal_translate -ot Float32 -unscale --config PDS_SampleProjOffset_Shift -0.5 --config PDS_LineProjOffset_Shift -0.5 megt90n000cb.lbl out_MOLA_4ppd_32bit.tif

--------------

PDS는 ISIS2와 ISIS3를 포함하는 관련 포맷 패밀리의 일원입니다.


참고
--------

-  ``gdal/frmts/pds/pdsdataset.cpp`` 로 구현되었습니다.

-  `NASA 행성 데이터 시스템(Planetary Data System) <http://pds.nasa.gov/>`_

-  :ref:`raster.isis2` 드라이버

-  :ref:`raster.isis3` 드라이버
