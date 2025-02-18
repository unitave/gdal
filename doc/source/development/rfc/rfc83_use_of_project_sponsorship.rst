.. _rfc-83:

=============================================================
RFC 83: GDAL 프로젝트 후원금 사용에 대한 지침
=============================================================

======= =============================
저자:   이벤 루올 (RFC 9의 내용 포함)
연락처: even.rouault@spatialys.com
제안일: 2021년 5월 19일
상태:   승인
======= =============================

요약
-------

:ref:`rfc-80` 에 따라, GDAL 프로젝트는 후원으로부터 나오는 다년간에 걸친 예산의 혜택을 받게 됩니다. 이 RFC는 프로젝트가 이 예산을 사용할 방법에 대한 지침을 공식화하고 :ref:`rfc-9` 을 대체합니다.

자금이 지원될 작업에는 두 가지 서로 다른 유형이 있습니다:

-  일일 유지/관리 작업:
   공동 유지관리자 여러 명이 이 작업을 수행할 것입니다.

-  특정 개발을 달성하기 위한 작업.

일일 유지/관리 작업
-------------------

범위
++++

-  버그 트래커 유지/관리:

   -  재생산성을 보장하기 위한 버그 리포트의 완성도 검증하기

   -  지침을 준수하지 않거나 무결하지 않은 버그 리포트 종료하기

   -  적절한 라벨 및 마일스톤으로 문제점 태그하기

   -  수정 사항이 관련이 있는 경우 풀 요청으로 문제점 해결하기

   -  재귀적인 테스트 스위트에 최대한 실용적으로 테스트를 추가하기 또는 개선하기

   -  주어진 시간보다 더 오래 걸릴 것으로 예상되거나 발견된 작업은 관리자에게 확인받아야 합니다.

-  지속적 통합 유지/관리 및 개선:
   GDAL 프로젝트에는 지속적 통합 환경설정이 여러 개 있습니다. 그 중 일부는 외부 원인(더 이상 사용할 수 없는 네트워크 자원, 의존성 변경 등등)으로 인해 정기적으로 망가집니다. 공동 유지관리자는 이런 환경설정을 작동 상태로 유지하기 위해 필요한 활동을 취할 것입니다.

-  코드 및 문서 기여의 검토:
   이런 기여는 현재 깃허브 풀 요청을 통해 이루어지고 있습니다. 공동 유지관리자는 기여 내용을 검토하고 제안자가 검토 내용을 승인하도록 만들기 위한 단계를 안내할 것입니다:

   -  지속적 통합이 리포트하는 문제점을 식별하기
   -  가능할 때마다 새 테스트 개발을 요청하기
   - ...

   기여자가 자신의 기여를 마무리할 능력이 되지 않는 경우, 공동 유지관리자 자신이 마무리할 수도 있습니다.

-  안정 브랜치(들)로 백포트하기에 적합한 수정 사항들이 백포트되는지 확인합니다.

-  프로젝트 소통 채널(메일링 리스트, IRC, 슬랙 채널 등등)을 모니터링합니다. 공동 유지관리자는 특히 이런 수단을 통해 보고되는 문제점들을 식별하고 대응하는 티켓으로 문제점을 파악하도록 확인합니다.
   공동 유지관리자는 때때로 라이브러리 및 도구의 사용에 대한 질문에 답변할 수도 있지만, 사용자에 대한 심층적인 지원은 공동 유지관리자의 작업 범위에 들어가지 않습니다. (사용자는 이런 목적을 위해 서비스 제공자를 이용할 수도 있습니다.)

-  GDAL이 의존하는 라이브러리의 새 버전들을 사전 추적하고, 컴파일 및 적절한 런타임 습성에 필요한 변경 사항들을 처리합니다.

-  정적/동적 분석기(analyzer)의 리포트를 모니터링하고 처리합니다. 현재 다음과 같은 분석기가 존재합니다:

   -  `OSS-Fuzz <https://google.github.io/oss-fuzz/>`_
   -  `cppcheck <https://cppcheck.sourceforge.io/>`_
   -  `Clang 정적 분석기 <https://clang-analyzer.llvm.org/>`_
   -  `Coverity Scan <https://scan.coverity.com/>`_
   -  GCC 및 CLANG 메모리, 정의되지 않은 습성 등등의 분석기

-  문서 개선

-  소프트웨어 배포 관련 활동:

   -  릴리즈 노트 작성
   -  후보 배포판 발행
   -  피드백 처리
   -  배포 마무리

-  경험이 많은 기여자의 경우, 경험이 적은 기여자가 GDAL에 합류해서 함께 할 수 있도록 도와주십시오.

이런 활동과 관련된 프로젝트에는 물론 GDAL 자체도 있지만, GDAL에 필수적이거나 매우 흔한 의존성으로 강력하게 연계되어 있고 유사한 유지/관리 자금의 혜택을 받지 못 하는 일반적으로 더 소규모의 다른 자유-오픈 소스 프로젝트도 있습니다. (이와는 반대로, GDAL을 사용하는 프로젝트들은 GDAL 후원 자금의 지원을 받을 자격이 없습니다.) 현재 이런 프로젝트 목록에는 다음이 포함됩니다:

   -  PROJ
   -  libtiff
   -  libgeotiff
   -  shapelib
   -  GEOS
   -  OpenJPEG

공동 유지관리자가 문제점을 조사하는 과정에서 또다른 오픈 소스 구성 요소에 있는 문제점을 발견했는데 패치를 제안할 수 있다면, 공동 유지관리자가 해당 작업을 수행해도 됩니다.

일반적인 시간 분배는 GDAL에 75%, 다른 프로젝트들에 25% 정도가 적당할 것입니다.

GDAL은 방대하고 복잡한 프로젝트입니다. 공동 유지관리자 각자가 GDAL의 모든 측면에 전문성을 가지리라 기대하지 않습니다. 유지/관리 지원자는 시간의 흐름에 따라 발전할 수 있는 자신의 관심 영역을 제시하고 작업을 어떻게 할당할지에 대해 다른 이해 관계자와 조정해야 할 것입니다.

방향
++++

.. 대부분 RFC 9에서 가져온 내용이지만, 후원자가 제기하는 문제점에
   우선 순위를 부여한다는 주요 차이점이 존재합니다.

일반적으로 프로젝트 운영 위원회가 공동 유지관리자를 관리합니다. 하지만 일상적인 결정의 경우 프로젝트 운영 위원회 회원 한 명이 공동 유지관리자의 관리자로 임명될 수도 있습니다. (이 프로그램을 통해 자금 지원을 받는 프로젝트 운영 위원회 회원은 자신의 작업 우선 순위를 정하기 위해 기존 의사 결정 과정을 이용할 것입니다.) 이 관리자가 이메일 또는 IRC 토의를 통해 공동 유지관리자와 조율할 것입니다.

.. 이런 상황을 처리하는 방법을 확신하지 못 했지만, 관리자 역할은
   시간을 다소 들여야 할 수도 있으며 자금을 지원받는 프로젝트 운영 위원회
   회원을 감독하도록 자금 지원을 받는 프로젝트 운영 위원회 회원이 없을 경우
   실제로 제대로 작동하지 않을 수도 있습니다.

관리자는 작업 우선 순위를 결정할 때 다음을 염두에 두려 노력해야 할 것입니다:

-  이전 배포판과 비교해서 재귀적인 티켓을 다른 작업보다 더 우선해야 합니다.

-  버그 리포트를 다른 작업보다 더 우선해야 합니다. (후원자의 버그 리포트는 더 높은 우선 순위 취급을 받을 자격을 갖추지 '못 할' 것입니다.)

-  프로젝트 운영 위원회가 식별한 집중 영역을 다른 작업보다 더 우선해야 합니다.

-  많은 사용자에게 영향을 미치는 버그 또는 요구 사항을 더 우선해야 합니다.

-  다른 사람이 할 의향이 없고 할 수 없는 작업을 처리하는 데 공동 유지관리자를 투입해야 합니다. (예를 들면 자원봉사자를 대체하기보다 빈 자리를 채워야 합니다.)

-  프로젝트 운영 위원회의 지시가 없는 이상 공동 유지관리자가 여러 주 동안 하나의 큰 작업에 매여 있지 않도록 노력하십시오.

-  공동 유지관리자에게 다른 사람이 급여를 받는 작업을 수행하도록 지시해서는 안 됩니다.

공동 유지관리자는 프로젝트 운영 위원회의 발의에 의한 지시에 의해서만 실질적인 신규 개발 프로젝트를 수행할 것입니다. (또는 프로젝트 운영 위원회가 공동 유지관리자가 변경 사항에 대해 작업하도록 지명할 수도 있습니다.)

GDAL에 대한 실질적인 모든 변경 사항에 대해 공동 유지관리자와 그 관리자는 일반적인 RFC 프로세스의 적용을 받는다는 사실을 기억하십시오.

보고
++++

공동 유지관리자는 (일반적으로 공유 스프레드시트에) 작업한 내용을 나타내는 월별 보고서를 작성할 것입니다. 이 보고서에는 일반적으로 티켓 및 풀 요청을 가리키는 링크와 보고 기간 동안 소요된 시간이 포합됩니다.

지원할 수 있는 사람은?
++++++++++++++++++++++

유지/관리 지원자는 다음과 같은 자질을 충족하는 것으로 입증된 공개 실적을 가진 자영업자 또는 직원의 시간을 이런 활동에 할당하는 데 동의하는 회사의 직원인 개인이어야 합니다:

-  작업에 요구되는 프로그램 언어에 대한 지식:
   GDAL 라이브러리를 위한 C/C++ 및 테스트 스위트를 위한 파이썬, 그리고/또는 SWIG 바인딩 가운데 하나 이상의 언어에 대한 적절한 지식이 필요합니다.

-  지리공간 분야에 대한 지식:
   이상적으로는 하나 이상의 오픈 소스 지리 공간 프로젝트에 대한 지식 그리고/또는 파일 포맷 및 저수준 고려 사항에 대한 경험이 필요합니다.

-  행동 수칙(Code of Conduct)을 준수해서 오픈 소스 커뮤니티 회원들과 대화형 작업을 할 수 있는 능력이 필요합니다.

-  문어체 영어에 대한 괜찮은 지식이 필요합니다.

공식적인 기준을 정할 수는 없지만, 이상적으로는 지원자가 신규에서 전문으로 이행하는 시간을 상각(償却)할 수 있도록 수년간에 걸쳐 프로젝트에 관여할 것을 목표로 삼아야 합니다.

공동 유직관리자 각자에게 분기별로 최대 작업 시간을 할당할 것이며 (각자 계획된 가용 시간을 알려주면 프로젝트 운영 위원회가 효율적인 할당을 결정할 것입니다) 공동 유직관리자 각자는 해당 할당 내에서 효율적으로 소요한 시간에 대해 청구할 것입니다.

유지/관리 지원자는 프로젝트 운영 위원회에 (개인적으로) 자신의 시간당 급여를 미국 달러 단위로 알려줘야 합니다.

특정 개발을 달성하기 위한 작업
------------------------------

.. 더 나은 이름이 있을까요? QGIS처럼 보조금 프로그램이라고 불러야 할까요?
   "보조금"이라는 용어가 비용을 분담해야 한다는 뜻을 암시할 수도 있지만
   GDAL이 제안의 전체 비용을 충당할 수 있다고 생각합니다.

GDAL 프로젝트 운영 위원회는 특정 개발을 달성하고자 하는 제안자의 제안을 (주기는 조정될 수 있지만 아마도 분기별로) 요청할 것입니다. 프로젝트 운영 위원회는 사용할 수 있는 총 예산 및 기타 조건들을 발표할 것입니다. 프로젝트 운영 위원회가 제안을 받기를 바라는 몇몇 아이디어를 제안할 수도 있습니다.

일반적으로 말하자면 사용자 지향 기능보다는 (새로운 드라이버, 새로운 유틸리티 등은 관심을 가진 기관들의 자금 지원을 받기가 더 쉽습니다) 프로젝트 유지/관리 작업 및 프로젝트(들)의 직접적으로 사용자 지향적이지 않은 측면들을 해결하는 제안에 우선 순위를 둘 것입니다. 그러나 사용자 지향 기능이 충분히 큰 관심을 받고 있다고 판단되는 경우에는 제안할 수 있습니다.

다음은 이 기준에 따라 처리해야 하는 주제의 불완전한 목록입니다:

-  코드베이스의 일부분을 개선하기/재작성하기
-  코드배이스의 큰 부분에 영향을 미치는 변경 사항
-  속도 최적화
-  일부 플랫폼에 대한 지원 추가하기/개선하기
-  테스트 스위트/지속적 통합 개선 사항
-  빌드 시스템 개선 사항
-  문서화 개선 사항
-  패키지 작업 노력 (완벽하게 재현 가능한 오픈 소스 빌드 지침을 사용한다는 가정 하에)

제안 신청자는 지원받을 자금을 밝혀야 합니다. 한 명 또는 여러 명의 개인이 제안서를 작성할 수 있습니다. (여러 명이 작성하는 경우 팀에 "청구서 발행 담당자"를 두고 회원들 간에 어떻게 배분할지를 조정하게 할 수 있는지, 또는 팀의 각 구성원이 자신 몫의 지원 자금을 신청해야 하게 할 수 있는지 결정해야 합니다.) 제안 신청자는 여러 주제에 대한 제안서를 제출할 수 있습니다.

제안 신청자는 커뮤니티의 관심 있는 구성원과 협력해서 제안에 대해 논의할 수 있는 버그 트래커에 자신의 제안서의 기술적인 세부 정보를 이슈로서 (또는 일반적으로 RFC에 걸맞는 변경 사항의 경우 RFC로서) 제출해야 합니다.

.. 앞의 내용은 QGIS 개선 제안 메커니즘의 영향을 받았습니다.
   https://github.com/qgis/QGIS-Enhancement-Proposals/issues?q=is%3Aissue+is%3Aopen+label%3AGrant-2021 을 참조하십시오.

신청자에 대한 기준은 앞 단락의 기준과 동일합니다.

결정 과정
---------

프로젝트 운영 위원회가 공동 유지관리자 및 특정 개발의 수탁자(grantee)의 선택을 통해 자금의 할당을 결정할 것입니다.

.. note:: 

   프로젝트 운영 위원회는 유지/관리 우선 순위에 대한 자문 회의의 의견, 커뮤니티가 제공하는 다른 의견, 그리고 프로젝트 운영 위원회의 자체 우선 순위 분석을 대등하게 고려할 것입니다.

자금을 요청한 또는 이해가 상충하는 (예를 들면 제안 신청자와 같은 회사에서 일하는) 또는 이해가 상충하는 다른 모든 상황에 있는 프로젝트 운영 위원회 회원은 논의에 참여할 수도 있지만 자금 할당과 관련된 결정에 대해 투표해서는 안 됩니다.

메모
----

이 RFC는 프로젝트의 새로운 운영 방식이기 때문에 시간의 흐름에 따라 후원 프로그램 관리에서 누적되는 경험을 통해 발전할 것으로 예상됩니다.

투표 이력
---------

https://lists.osgeo.org/pipermail/gdal-dev/2021-June/thread.html#54249

-  마테우시 워스코트 +1
-  하워드 버틀러 +1
-  프랑크 바르메르담 +1
-  커트 슈베어 +1
-  션 길리스 +1
-  유카 라흐코넨 +1
-  대니얼 모리셋 +1
-  이벤 루올 +1

