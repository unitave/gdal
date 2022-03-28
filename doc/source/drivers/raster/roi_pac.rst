.. _raster.roi_pac:

================================================================================
ROI_PAC -- ROI_PAC
================================================================================

.. shortname:: ROI_PAC

.. built_in_by_default::

NASA의 제트추진연구소(Jet Propulsion Laboratory)의 `ROI_PAC 프로젝트 <https://aws.roipac.org/>`_ 에서 사용되는 이미지 포맷 용 드라이버입니다. .raw 이미지를 제외한 모든 이미지 유형을 지원합니다.

메타데이터는 ROI_PAC 도메인에 저장됩니다.

지리참조 작업을 지원하지만, ROI_PAC 포맷이 어떤 반구 필드도 저장하지 않기 때문에 UTM 투영법을 사용하는 경우 문제가 발생합니다.

파일 생성 작업 시, 파일 유형(slc, int 등등)에 대응하는 올바른 데이터 유형을 지정할 수 있어야 합니다. 그렇지 않으면 드라이버가 오류를 발생시킬 것입니다.

주의: ``gdal/frmts/raw/roipacdataset.cpp`` 로 구현되었습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::
