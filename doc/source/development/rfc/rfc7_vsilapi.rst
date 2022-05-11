.. _rfc-7:

=======================================================================================
RFC 7: VSI*L 함수 용 VSILFILE 사용
=======================================================================================

저자: 이벤 루올(Even Rouault) (원저자: 에리크 됭게스(Eric Dönges))

연락처: even.rouault@spatialys.com, Eric.Doenges@gmx.net

상태: 승인

목적
----

VSI\*L 계열 함수를 위한 API가 현재 FILE 데이터 유형 대신 새로운 VSILFILE 유형을 사용하도록 변경합니다.

배경, 근거
----------

현재 GDAL은 추상 파일 접근 함수에 두 가지 (이 문서에서 VSI\* 및 VSI\*L이라고 부르는) API를 제공합니다. 두 API 모두 FILE 포인터 상에서 작업한다고 주장하지만, VSI\*L 함수는 VSIFOpenL 함수가 생성한 FILE 포인터 상에서만 작업할 수 있습니다. VSIFOpenL 함수가 실제 FILE 포인터가 아니라 FILE 포인터로 유형 캐스트(typecast)된 내부 C++ 클래스를 가리키는 포인터를 반환하기 때문입니다. 때문에 VSI\* 및 VSI\*L 함수가 적절하지 못 하게 섞여 있는 경우 컴파일러가 경고할 수 없게 만듭니다.

제안 수정안
-----------

새로운 불분명한(opaque) VSILFILE 데이터 유형을 선언해야 합니다. 모든 VSI\*L 함수가 FILE 데이터 유형 대신 새로운 VSILFILE 유형을 사용하도록 변경해야 합니다. 뿐만 아니라 VSI\*L 함수를 사용하는 모든 GDAL 코드도 이 데이터 유형을 사용하도록 변경해야만 합니다.

RawRasterBand 변경
------------------

-  'FILE\*' 대신 'void\* fpRaw'를 받아들이도록 구성자 2개를 변경합니다.

-  새로운 'VSILFILE\* fpRawL' 멤버를 추가합니다. 기존 'FILE\* fpRaw' 멤버는 그대로 유지합니다. 구성자들이 bIsVSIL 파라미터의 값에 따라 적절한 멤버를 설정할 것입니다.

-  새로운 VSILFILE\* GetFPL() 메소드를 추가합니다.

-  오래된 FILE\* GetFP() 메소드는 이전과 동일한 습성을 갖도록 (구성자에 전송된 핸들에 따라 표준 FILE 핸들 또는 VSI\*L 핸들을 반환할 수 있도록) 조정되었습니다.

이런 변경 사항들은 RawRasterBand 사용 시 캐스트의 필요성을 최소화하기 위한 것입니다. API 하위 호환성이 보전됩니다.

호환성 문제점, 전환 시간표
--------------------------

컴파일러가 모든 VSI\*L 함수에 전송되는 부적절한 파라미터를 탐지할 수 있게 하기 위해, 비어 있는 정방향 선언(forward declaration)의 도움을 받아 다음과 같이 VSILFILE을 선언할 것입니다:

::

   typedef struct _VSILFILE VSILFILE

\_VSILFILE 구조 자체는 정의하지 않습니다.

하지만, 이렇게 하면 VSI\*L API를 사용하는 모든 기존 코드에 대한 소스 호환성을 무너뜨릴 것입니다. 따라서 현재로서는 VSIL_STRICT_ENFORCE 매크로를 정의하지 않는 이상 VSILFILE을 FILE의 별명으로 정의합니다:

::

   #ifdef VSIL_STRICT_ENFORCE
   typedef struct _VSILFILE VSILFILE;
   #else
   typedef FILE VSILFILE;
   #endif

향후 배포판(GDAL 2.0?)에서는 새로운 강력한 유형을 적용하도록 습성을 변경할 것입니다.

이 RFC를 승인한 이후 모든 개발 작업에서 VSIF\*L API를 처리하는 경우 VSILFILE을 사용해야 합니다.

의문
----

-  DEBUG를 정의하는 경우 기본적으로 VSIL_STRICT_ENFORCE를 정의해야 하는가?

이렇게 하면 GDAL 개발자가 적절한 유형을 적용하기가 더 쉬워지지만, 배포 모드 사용시 API/ABI에 영향을 미치지는 않습니다.

구현
----

VSIL_STRICT_ENFORCE 모드에서 컴파일 작업이 작동하도록 전체 소스 트리(:file:`port`, :file:`gcore`, :file:`frmts`, :file:`ogr`, :file:`swig/include`)를 그에 맞춰 변경할 것입니다. #3799 티켓이 이를 구현한 패치를 담고 있습니다. 컴파일 작업은 어떤 새로운 경고도 추가하지 않습니다. 이렇게 변경한 다음에도 자동 테스트 스위트는 계속 작동합니다.

변환 과정 도중 지오래스터(GeoRaster) 및 JPIPKAK 드라이버를 수정하지 않았지만, 이는 저자가 이 드라이버들을 컴파일할 수 있는 권한을 가지고 있지 않기 때문입니다. 테스트가 필요합니다. 변환 과정에서 변경된 다른 모든 드라이버들은 컴파일되었습니다.

변환 과정 도중, CEOS2 드라이버에서 대용량 파일 핸들러를 가진 POSIX FILE API를 오용한 사실을 발견했지만 해당 함수를 사용하지는 않습니다.

투표 이력
--------------

-  프랑크 바르메르담(Frank Warmerdam) +1
-  세케레시 터마시(Szekeres Tamás) +1
-  대니얼 모리셋(Daniel Morissette) +1
-  하워드 버틀러(Howard Butler) +1
-  이벤 루올(Even Rouault) +1

