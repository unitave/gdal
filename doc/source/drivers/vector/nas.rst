.. _vector.nas:

NAS - ALKIS
===========

.. shortname:: NAS

.. build_dependencies:: Xerces

NAS 드라이버는 독일의 지적(地籍) 데이터에 사용되는 NAS/ALKIS 포맷의 읽기를 지원합니다. 이 포맷은 일반 OGR GML 드라이버로 쉽게 읽어올 수 없는 꽤 복잡한 GML3 객체를 가진 GML 프로파일입니다.

이 드라이버를 사용하려면 GDAL/OGR가 Xerces XML 파싱 라이브러리와 함께 빌드되어 있어야 합니다.

이 드라이버는 입력물이 NAS 파일인지 판단하기 위해, "opengis.net/gml"과 (기본값이 "NAS-Operationen;AAA-Fachschema;aaa.xsd;aaa-suite"인) **NAS_INDICATOR** 옵션에 있는 쌍반점으로 구분된 문자열 목록을 검색해서 일치하는 내용이 없는 모든 파일을 무시합니다.

GDAL 2.3버전에서, 이 드라이버가 (*zeigtAufExternes* 같은) 속성 충돌을 방지하기 위해 내부적으로 몇몇 요소들과 속성들을 다시 매핑하거나 무시하게 만들었던 많은 임시방편(workaround)이 제거되었습니다. 그 대신 이 드라이버는 이제 GML 드라이버에서와 마찬가지로 GFS 파일을 이용해서 요소 경로를 객체 속성에 깔끔하게 매핑시킬 수 있게 해주는 **NAS_GFS_TEMPLATE** 옵션을 입력받습니다. 한 레이어에 여러 도형 유형이 있어도 (예를 들어 정규 wkb_geometry 옆에 ax_flurstueck.objektkoordinaten이 있어도) 읽어올 수 있습니다.

전체 NAS 스키마의 `GFS 템플릿 <https://github.com/norBIT/alkisimport/blob/master/alkis-schema.gfs>`_ 과 그에 대응하는 `PostgreSQL 스키마 <https://github.com/norBIT/alkisimport/blob/master/alkis-schema.sql>`_ 는 (가져오기를 쉽게 만들어주는 셸 스크립트와 PyQt 프론트엔드도 가지고 있는) `norGIS ALKIS-Import <http://www.norbit.de/68/>`_ 의 일부입니다. 이 두 파일은 공식 응용 프로그램 스키마로부터 (`xmi2db <https://github.com/pkorduan/xmi2db>`_ 의 포크인) `xmi2db <https://github.com/norBIT/xmi2db/>`_ 를 이용해서 생성되었습니다.

GDAL 2.3버전에서, 새로운 **NAS_NO_RELATION_LAYER** 옵션도 도입되었습니다. 이 옵션은 *alkis_beziehungen* 테이블 채우기를 비활성화할 수 있습니다. 이 테이블에 작성되는 정보는 원본 요소/테이블에 담겨 있는 관계 필드와 중복되기 때문입니다. 이 옵션을 활성화시키면 진행 상황도 리포트합니다.

이 드라이버는 `PostNAS 프로젝트 <http://trac.wheregroup.com/PostNAS>`_ 의 맥락 안에서 구현되었습니다. 이 프로젝트는 NAS 드라이버의 사용법 및 기타 관련 프로젝트에 관한 더 많은 정보를 가지고 있습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

.. supports_virtualio::
