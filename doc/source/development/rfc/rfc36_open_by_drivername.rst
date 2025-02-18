.. _rfc-36:

================================================================================
RFC 36: GDALOpen 상에서 의도한 드라이버 지정 허용
================================================================================

저자: 이방 루세나(Ivan Lucena)

연락처: ivan.lucena@pmldnet.com

상태: 제안

요약
----

이 RFC는 GDAL에 어떤 드라이버로 특정 데이터셋을 열어야 할지를 명확하게 지정할 수 있는 메커니즘을 제안합니다.

타당성
------

드라이버를 선택함으로써, 사용자는 처리 시간을 최적화하고 드라이버 탐지 메커니즘 때문에 정확하지 않은 또는 원하지 않는 드라이버를 선택하게 되는 일을 피할 수 있습니다.

개념
----

:cpp:func:`GDALOpen` 에 "driver=" 토큰과 드라이버 이름 그리고 파일명과 구분하는 쉼표를 담고 있는 문자열을 전송하는 것입니다:

::

   [driver=driver-name,]file-name

예시:

::

   $ gdalinfo driver=nitf,imagefile01.ntf

이 경우 드라이버 탐지 과정이 필요없습니다. 사용자가 특정 드라이버를 사용한다고 지정했기 때문입니다. 어떤 이유로든 이런 과정이 실패하는 경우, 함수가 NULL을 반환하고 다른 드라이버로 파일을 열려는 시도를 하지 않습니다.

구현
----

구현에 필요한 코드는 매우 적으며, 제안 패치가 이미 #3043 티켓에 존재합니다.

활용
----

GDAL API를 사용하는 모든 응용 프로그램 또는 GDAL 명령줄 도구를 사용하는 사용자는 특정 드라이버를 사용해서 강제로 데이터셋을 열고 싶을 때가 있습니다.

하위 호환성 문제점
------------------

:cpp:func:`GDALOpen` 처리 과정에서 이 옵션 항목이 현재 로직에 영향을 미쳐서는 안 됩니다.

테스트
------

-  테스트 스크립트에 추가 테스트가 추가될 것입니다.

문제점
------

gdalbuildvrt 및 gdaltindex 유틸리티의 경우 드라이버 선택 옵션을 와일드카드 문자와 함께, 예를 들면 ``driver=gtiff,*.tif`` 처럼 사용할 수 없을 것입니다.

