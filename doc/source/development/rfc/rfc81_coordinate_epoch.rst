.. _rfc-81:

=============================================================
RFC 81: 지리공간 포맷의 좌표 시대 지원
=============================================================
============ ==========================
저자:        이벤 루올
연락처:      even.rouault@spatialys.com
제안일:      2021년 5월 10일
최신 수정일: 2021년 6월 18일
상태:        승인
대상:        GDAL 3.4버전
============ ==========================

요약
----

이 RFC는 몇몇 중요 지리공간 포맷과 GDAL/OGR API 및 유틸리티가 좌표 시대(coordinate epoch)를 지원할 것을 제안하고 설명합니다.

동기
----

많은 좌표계를 "동적 좌표계"라고 부르는데, 지표면 상에 있는 포인트의 해당 좌표계를 사용하는 좌표가 시간에 따라 변할 수도 있다는 의미입니다. 명확하게 말하자면 해당 좌표가 언제나 좌표가 무결한 시대라는 조건을 갖추어야만 한다는 뜻입니다. 좌표 시대가 반드시 관측 정보가 수집된 시대일 필요는 없습니다.

동적 좌표계의 예시를 들자면 ``WGS 84 (G1762)``, ``ITRF2014``, ``ATRF2014`` 등이 있습니다.

일반 EPSG:4326 WGS84 좌표계도 동적 좌표계로 간주되긴 하지만, 위치 정확도가 2미터인 원점(datum) 집합을 기반으로 하기 때문에 사용을 권장하지 않습니다. 오히려 `WGS 84 (G1762) <https://epsg.io/7664>`_ 같은 구현 가운데 하나를 사용하는 편이 낫습니다.

이 문서 작성 당시, GDAL/OGR가 처리하는 포맷 가운데 좌표 시대를 인코딩하는 표준화된 방식을 가지고 있는 포맷은 없습니다. 그 결과 기존 판독기들과 가능한 한 하위 호환되는 것을 목표로, 항상 명쾌하지는 않은 인코딩 방법을 선택했습니다. 대응하는 공식 사양이 이 개념을 고려하도록 진화하는 경우, 이 인코딩 방법이 변경될 수도 있습니다. 그러나 이는 조금이지만 닭과 달걀 문제이기 때문에 ("좌표 시대를 사용할 수 있는 소프트웨어가 없는데 어째서 좌표 시대를 저장해야 합니까?") 이 초기 해결책으로 시작하겠습니다.

PROJ는 판 이동(plate motion)을 고려해서 -- 예를 들어 GDA2020(호주의 정적 좌표계/원점)을 ATRF2014(호주의 동적 좌표계/원점)로 변환하는 것과 같은 -- 여러 정적 좌표계와 동적 좌표계 간의 시간 종속 변환을 처리할 수 있습니다. 좌표 시대 저장을 지원하면 보다 정확한 좌표 변환을 더 쉽게 수행할 수 있을 것입니다.

상세 사항
---------

API에 미치는 영향, 여러 포맷에서의 좌표계 인코딩, 그리고 기존 유틸리티에 미치는 영향에 대해서는 `좌표 시대 지원 문서 <https://github.com/rouault/gdal/blob/coordinate_epoch_v2/gdal/doc/source/user/coordinate_epoch.rst>`_ 를 참조하십시오.

하위 호환성
-----------

API 수준에서는 새 메소드들을 추가할 뿐입니다.

새 데이터셋의 생성과 관련해서, 데이터셋을 데이터셋 좌표계와 연결된 좌표 시대 없이 생성하는 경우 어떤 하위 호환성 문제도 발생하지 않습니다. 좌표 시대 인코딩은 필요한 경우에만 추가되기 때문입니다.

그리고 좌표 시대를 사용하는 경우, 기존 판독기에 영향을 미치지 않을 방식으로 사용합니다. 유일한 예외는 비 EPSG로 인코딩된 좌표계를 좌표 시대와 함께 작성하는 경우의 FlatGeobuf 포맷일 것입니다. (이 경우 오류를 막기 위해 GDAL 3.3버전 브랜치에 대한 백포트(backport)를 수행할 것입니다.)

문서화
------

새로운 메소드들을 문서화하고, 사용자 문서에 상세 사항 단락에 언급된 페이지를 추가할 것입니다.

테스트
------

새 메소드들을 테스트합니다. 좌표 시대 지원으로 확장된 포맷들도 새로운 테스트를 받습니다.

관련 풀 요청
------------

`풀 요청 4011번 <https://github.com/OSGeo/gdal/pull/4011>`_

투표 이력
---------

-  유카 라흐코넨 +1
-  이벤 루올 +1

-  커트 슈베어 +0

-  하워드 버틀러 -0

