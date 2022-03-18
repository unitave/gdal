.. _raster.isce:

================================================================================
ISCE -- ISCE
================================================================================

.. shortname:: ISCE

.. built_in_by_default::

JPL의 ISCE(Interferometric synthetic aperture radar Scientific Computing Environment)에서 사용되는 이미지 포맷 용 드라이버입니다. GDAL 데이터 유형으로 매핑할 수 있는 데이터 유형을 가진 이미지만 지원합니다.

이미지 속성은 ISCE 메타데이터 도메인 아래 저장되어 있지만, 현재 기저 구성요소와 그 속성에 접근을 지원하지 않습니다. 마찬가지로, ISCE 메타데이터 도메인은 이미지 XML 파일에 속성으로서 저장될 것입니다.

지리참조는 아직 구현되지 않았습니다.

현재 ACCESS_MODE 속성을 무시합니다.

현재 사용할 수 있는 생성 옵션은 SCHEME뿐입니다. 이 옵션의 설정값(BIL, BIP 또는 BSQ)이 교차삽입 여부를 결정합니다. 기본값은 BIP입니다.

주의: ``gdal/frmts/raw/iscedataset.cpp`` 로 구현되었습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::
