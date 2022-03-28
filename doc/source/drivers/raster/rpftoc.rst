.. _raster.rpftoc:

================================================================================
RPFTOC -- 래스터 상품 포맷/RPF (a.toc)
================================================================================

.. shortname:: RPFTOC

.. built_in_by_default::

이 드라이버는 CADRG 또는 CIB처럼 RPF 교환으로부터 목차(table of content) 파일 -- A.TOC -- 을 사용해서 커버리지가 목차에 담겨 있는 프레임들의 집합인 가상 데이터셋으로 노출시키는 RPF(Raster Product Format) 상품을 위한 읽기 전용 판독기입니다.

이 드라이버는 A.TOC 파일에 있는 각 하위 데이터셋을 서로 다른 하위 데이터셋으로 리포트할 것입니다.

다음은 A.TOC 파일에 gdalinfo를 실행한 결과물입니다:

::

   Subdatasets:
     SUBDATASET_1_NAME=NITF_TOC_ENTRY:CADRG_GNC_5M_1_1:GNCJNCN/rpf/a.toc
     SUBDATASET_1_DESC=CADRG:GNC:Global Navigation Chart:5M:1:1
   [...]
     SUBDATASET_5_NAME=NITF_TOC_ENTRY:CADRG_GNC_5M_7_5:GNCJNCN/rpf/a.toc
     SUBDATASET_5_DESC=CADRG:GNC:Global Navigation Chart:5M:7:5
     SUBDATASET_6_NAME=NITF_TOC_ENTRY:CADRG_JNC_2M_1_6:GNCJNCN/rpf/a.toc
     SUBDATASET_6_DESC=CADRG:JNC:Jet Navigation Chart:2M:1:6
   [...]
     SUBDATASET_13_NAME=NITF_TOC_ENTRY:CADRG_JNC_2M_8_13:GNCJNCN/rpf/a.toc
     SUBDATASET_13_DESC=CADRG:JNC:Jet Navigation Chart:2M:8:13

어떤 상황에서는, 하위 데이터셋 안에 있는 :ref:`raster.nitf` 타일이 동일한 색상표를 공유하지 않는 경우가 있습니다. RPFTOC 드라이버는 gdalinfo가 리포트한 색상표에 (하위 데이터셋의 첫 번째 타일의 색상표에) 이런 서로 다른 색상표들을 매핑하기 위해 최선을 다할 것 입니다. 매핑 결과물이 썩 좋지 않은 경우, 데이터셋을 열기 전에 RPFTOC_FORCE_RGBA 환경설정 변수를 TRUE로 설정해볼 수 있습니다. 이렇게 하면 드라이버가 하위 데이터셋을 색상표가 아니라 RGBA 데이터셋으로 노출시키게 될 것입니다.

하위 데이터셋의 외부 오버뷰를 작성할 수도 있습니다. 첫 번째 하위 데이터셋의 오버뷰는 예를 들어 A.TOC.1.ovr로, 두 번째 하위 데이터셋의 오버뷰는 A.TOC.2.ovr로, ... 명명될 것입니다. 하위 데이터셋 생성 시 사용했던 RPFTOC_FORCE_RGBA 설정과 동일한 설정으로 하위 데이터셋을 다시 열어야만 한다는 사실을 기억하십시오. 색상표를 가진 (RPFTOC_FORCE_RGBA 설정을 해제한) 하위 데이터셋의 오버뷰를 작성하는 경우 NEAREST가 아닌 다른 리샘플링 메소드를 사용해서는 안 됩니다.

이런 하위 데이터셋에 gdalinfo를 실행하면 다양한 NITF 메타데이터는 물론 하위 데이터셋의 NITF 파일 목록도 반환할 것입니다.


드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

.. supports_virtualio::


참고
----

-  ``gdal/frmts/nitf/rpftocdataset.cpp`` 로 구현되었습니다.

-  `MIL-PRF-89038 <http://www.everyspec.com/MIL-PRF/MIL-PRF+%28080000+-+99999%29/MIL-PRF-89038_25371/>`_: RPF, CADRG, CIB 상품 사양

