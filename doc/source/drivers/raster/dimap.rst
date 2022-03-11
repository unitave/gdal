.. _raster.dimap:

================================================================================
DIMAP -- 스팟(Spot) DIMAP
================================================================================

.. shortname:: DIMAP

.. built_in_by_default::

이 드라이버는 스팟 DIMAP 서술 이미지를 위한 읽기 전용 판독기입니다. 이 드라이버를 사용하려면, product 디렉터리에 있는 METADATA.DIM (DIMAP 1), VOL_PHR.XML (DIMAP 2) 또는 VOL_PNEO.XML (DIMAP 2 VHR-2020) 파일을 선택하거나 product 디렉터리 자체를 선택하십시오.

스팟 영상은 다른 이미지들과 뚜렷하게 구분되는 영상 파일로 TIFF 파일인 경우가 많지만, DIMAP 데이터셋은 메타데이터 XML 파일로부터 데이터셋의 스팟 영상 파일, 관련 지리위치(geolocation) 그리고 기타 메타데이터에 접근할 수 있습니다.

래스터 밴드 수준에서 <Spectral_Band_Info> 노드의 내용을 메타데이터로서 리포트합니다. 아직도 첫 번째 밴드의 Spectral_Band_Info의 내용을 데이터셋의 메타데이터로서 리포트하지만, 이는 이 정보를 얻기 위했던 퇴출된 방식이라고 봐야 한다는 사실을 기억하십시오.

다중 구성 요소 상품의 경우, 하위 데이터셋 별로 각 구성 요소를 노출시킬 것입니다.

주의: ``gdal/frmts/dimap/dimapdataset.cpp`` 로 구현되었습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

.. supports_virtualio::
