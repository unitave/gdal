.. _raster.cad:

================================================================================
CAD -- AutoCAD DWG 래스터 레이어
================================================================================

.. shortname:: CAD

.. versionadded:: 2.2

.. build_dependencies:: (내부 libopencad 제공)

OGR DWG 지원은 libopencad를 기반으로 하기 때문에, libopencad 문서에서 지원되는 DWG(DXF) 버전 목록을 볼 수 있습니다. 모든 그리기 항목(drawing entity)은 DWG 파일에서와 마찬가지로 레이어 별로 구분되어 있습니다. 래스터는 보통 개별 지리참조 파일로 (GeoTiff, Jpeg, Png 등등) DWG 파일 안에 개별 레이어로 존재합니다. 이 드라이버는 DWG 이미지 설명으로부터 공간 좌표계와 기타 메타데이터를 가져와서 GDALDataset에 설정하려 합니다.

주의: ``ogr/ogrsf_frmts/cad/gdalcaddataset.cpp`` 로 구현되었습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

.. supports_virtualio::
