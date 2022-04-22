.. _vector.sosi:

================================================================================
노르웨이 SOSI 표준
================================================================================

.. shortname:: SOSI

.. build_dependencies:: FYBA 라이브러리

SOSI 드라이버는 FYBA 라이브러리를 요구합니다.

열기 옵션
------------

GDAL 3.1버전부터, 다음 열기 옵션을 (일반적으로 ogrinfo 또는 ogr2ogr 유틸리티의 '-oo name=value' 파라미터로) 지정할 수 있습니다:

-  **appendFieldsMap**: (기본값은 비어 있는 값입니다)
   동등한 필드명을 가진 모든 행들을 객체에 추가하는 것이 기본 습성이지만, 이 파라미터를 사용하면 사용자가 어떤 필드가 무결할지를 선택할 수 있습니다.

예시
~~~~~~~~

-  이 예시는 객체에 있는 모든 중복 필드를 쉼표로 구분해서 추가하는 방식으로 SOSI 파일을 shapefile로 변환할 것입니다:

   ::

      ogr2ogr -t_srs EPSG:4258 test_poly.shp test_duplicate_fields.sos polygons

-  이 예시는 BEITEBRUKERID 및 OPPHAV 중복 필드만 쉼표로 구분해서 추가하는 방식으로 SOSI 파일을 shapefile로 변환할 것입니다:

   ::

      ogr2ogr -t_srs EPSG:4258  test_poly.shp test_duplicate_fields.sos polygons -oo appendFieldsMap="BEITEBRUKERID&OPPHAV"

-  이 예시는 BEITEBRUKERID 및 OPPHAV 중복 필드를 쌍반점과 쉼표로 구분해서 추가하는 방식으로 SOSI 파일을 shapefile로 변환할 것입니다:

   ::

      ogr2ogr -t_srs EPSG:4258  test_poly.shp test_duplicate_fields.sos polygons -oo appendFieldsMap="BEITEBRUKERID:;&OPPHAV:,"
   
