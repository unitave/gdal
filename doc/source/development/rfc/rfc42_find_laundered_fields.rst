.. _rfc-42:

=======================================================================================
RFC 42: OGR 레이어에서 세탁된 필드 검색
=======================================================================================

저자: 위르겐 피셔(Jürgen Fischer)

연락처: jef@norbit.de

요약
----

이 (소규모) RFC는 :cpp:class:`OGRLayer` 클래스에 드라이버가 (예를 들어 OCI 또는 PG 드라이버에서 LAUNDER를 통해) 이름을 변경한 필드들의 필드 색인을 검색할 수 있는 새 메소드를 추가할 것을 제안합니다.

구현
----

이 RFC를 구현한 `풀(pull) 요청 <https://github.com/OSGeo/gdal/pull/23>`_ 이 이미 깃허브 상에 존재합니다.
일반 매핑을 구현하는 :cpp:func:`OGRLayer::FindFieldIndex` 가상 메소드를 추가하는데, 드라이버가 이를 무시할 수 있습니다. OCI 드라이버는 원본 필드가 존재하지 않는 경우 선택적으로 LAUNDER 처리된 필드의 색인을 반환하기 위해 이 가상 메소드를 추가합니다. 이 풀 요청은 ogr2ogr 유틸리티가 이 메소드를 사용하도록 수정하고, 이 메소드를 활성화시키는 "-relaxedFieldNameMatch" 스위치도 제공합니다.

배경
----

NAS가 보통 사전에 존재하는 스키마 상에서 작업하기 때문에 NAS를 사용하는 경우 특히 자주 일어나는 문제입니다.
NAS에 있는 많은 식별자의 길이가 오라클의 식별자 길이 제한 조건을 초과하기 때문에 이 스키마를 오라클에 맞게 조정해야 했습니다. 따라서 ogr2ogr 유틸리티는 단축명과 단축명에 해당하는 긴 이름을 매핑하는 데 실패하고 해당 필드를 비워두게 됩니다.

참조
----

-  `https://github.com/OSGeo/gdal/pull/23 <https://github.com/OSGeo/gdal/pull/23>`_
-  PostgreSQL NAS 스키마:
   `http://trac.wheregroup.com/PostNAS/browser/trunk/import/alkis_PostNAS_schema.sql <http://trac.wheregroup.com/PostNAS/browser/trunk/import/alkis_PostNAS_schema.sql>`_
-  Oracle NAS 스키마:
   `http://trac.wheregroup.com/PostNAS/browser/trunk/import/alkis_PostNAS_ORACLE_schema.sql <http://trac.wheregroup.com/PostNAS/browser/trunk/import/alkis_PostNAS_ORACLE_schema.sql>`_
-  스크립트를 PG로부터 OCI로 변환:
   `http://trac.wheregroup.com/PostNAS/browser/trunk/import/pg-to-oci.pl <http://trac.wheregroup.com/PostNAS/browser/trunk/import/pg-to-oci.pl>`_

투표 이력
---------

-  대니얼 모리셋 +1
-  이벤 루올 +1
-  프랑크 바르메르담 +1
-  세케레시 터마시 +1
-  유카 라흐코넨(Jukka Rahkonen)  +1
-  위르겐 피셔 +1


커밋
----

r26572 & r26573

