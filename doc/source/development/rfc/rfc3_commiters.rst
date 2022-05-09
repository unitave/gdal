.. _rfc-3:

================================
RFC 3: GDAL 커밋 개발자 지침
================================

저자: 프랑크 바르메르담

연락처: warmerdam@pobox.com

상태: 승인

목적
----

SVN(또는 CVS) 커밋 접근을 공식화하고 SVN 커밋 개발자(committer)를 위한 몇몇 지침을 지정합니다.

SVN 커밋 접근으로 승격
----------------------

GDAL/OGR 프로젝트 운영 위원회(Project Steering Committee)가 승인한 경우에만 새로운 개발자에게 SVN 커밋 접근 권한을 제공해야 합니다. 새 커밋 개발자는 프로젝트 운영 위원회에 제안을 작성한 다음 정상적으로 투표를 기다려야 합니다. 이런 투표의 경우 RFC(Request for Comment) 문서를 작성할 필요는 없습니다. 'gdal-dev' 메일링 리스트에 제안하는 것만으로도 충분합니다.

SVN 커밋 접근 권한 박탈도 동일한 과정을 거쳐 처리해야 합니다.

새로운 커밋 개발자는 일반적으로 버그 리포트, 패치(patch) 제출, 그리고/또는 GDAL/OGR 메일링 리스트(들)에 활발히 참여함으로써 GDAL/OGR에 대한 헌신과 GDAL/OGR 소스 코드 및 프로세스에 대한 지식을 위원회가 만족할 정도로 입증해야 합니다.

새로운 커밋 개발자는 향후 배포판에서 자신이 GDAL/OGR 소스 트리에 커밋하는 모든 새로운 기능 또는 변경 사항도 지원할 준비가 되어 있어야 합니다. 아니면 자신이 담당하는 코드 부분을 더 이상 지원할 수 없는 경우 책임을 위임할 사람을 찾아야 합니다.

모든 커밋 개발자는 정책, 기술 개발 및 배포판 준비에 대한 정보를 받을 수 있도록 'gdal-dev' 메일링 리스트에도 가입해야 합니다.

새로운 커밋 개발자는 이 문서를 읽고 이해해야 할 책임이 있습니다.

커밋 개발자 추적
----------------

모든 프로젝트 커밋 개발자는 주 GDAL 디렉터리에 각 SVN 커밋 개발자별 (COMMITTERS라고 불리는) 파일로 목록화될 것입니다:

-  Userid: 해당 개발자에 대해 SVN에 나타날 ID입니다.
-  Full name: 개발자의 실제 이름입니다.
-  Email address: 커밋 개발자에게 연락할 수 있는 현재 이메일 주소입니다. 자동 수집을 어렵게 만들기 위해 정규 방식으로 변경될 수도 있습니다.
-  담당 영역에 대해 간단하게 표시합니다.

SVN 관리자
----------

프로젝트 운영 위원회의 멤버 한 명을 SVN 관리자(administrator)로 임명할 것입니다. 해당 멤버는 사람들에게 SVN 커밋 접근 권한을 승인하고, COMMITTERS 파일을 업데이트하며, 기타 SVN 관련 관리 업무를 수행할 책임을 질 것입니다. SVN 관리자는 당연히 SVN 서버에 로그인할 수 있어야 합니다.

프랑크 바르메르담이 초대 SVN 관리자가 될 것입니다.

SVN 커밋 실행
-------------

GDAL/OGR 프로젝트에 대해 다음과 같은 작업을 훌륭한 SVN 커밋 실행이라고 간주합니다:

-  SVN 커밋 로그에 의미가 있는 설명을 입력하십시오.

-  트랙(Trac) 티켓 관련 변경 사항을 커밋하는 경우 SVN 커밋 로그 항목 끝에 "(#1232)" 같은 버그 참조를 추가하십시오. '#' 문자가 트랙(Trac)이 변경 집합(changeset)으로부터 언급된 티켓으로의 하이퍼링크를 생성할 수 있게 해줍니다.

-  트랙(Trac) 티켓 관련 변경 사항을 커밋한 다음, 티켓 설명에 "Fixed in trunk (r12345) and in branches/1.7 (r12346)"처럼 수정한 트리 및 리비전을 작성하십시오. 'r' 문자가 트랙(Trac)이 티켓으로부터 변경 집합(changeset)으로의 하이퍼링크를 생성할 수 있게 해줍니다.

-  안정 브랜치에 대응하는 버그 ID 없이 변경 사항을 커밋해서는 안 됩니다. 안정적인 버전으로 푸시(push)할 가치가 있는 모든 변경 사항은 버그를 입력할 가치가 있습니다.

-  프로젝트 운영 위원회 또는 배포 관리자의 허가 없이는 안정 브랜치에 새 기능을 절대로 커밋하지 마십시오. 일반적으로 안정 브랜치에는 수정 사항만 들어가야 합니다.

-  새 기능은 주 개발 트렁크로 들어갑니다.

-  시험판 코드 동결 도중에는 코드에 프로젝트 운영 위원회 또는 배포 관리자의 허가 없이 버그 수정 사항만 커밋해야 합니다.

-  주 개발 버전에 대한 중요한 변경 사항은 커밋하기 전에 'gdal-dev' 메일링 리스트에서 논의해야 하며, 더 큰 변경 사항은 프로젝트 운영 위원회가 승인한 RFC 문서를 필요로 합니다.

-  프로젝트 운영 위원회의 승인 없이 새 브랜치를 생성하지 마십시오. 배포 관리자는 브랜치 생성 권한을 가진다고 간주합니다.

-  SVN에 있는 모든 소스 코드는 DOS 텍스트 모드가 아니라 유닉스 텍스트 서식이어야 합니다.

-  기존 소스 코드에 새 기능 또는 중요한 변경 사항을 커밋하는 경우, 커밋 개발자는 소스 코드가 가장 공통적으로 지원되는 플랫폼(현재 리눅스와 윈도우) 상에서 계속 빌드되고 작동되도록 보장하기 위해, 이 플랫폼들 상에서 직접 테스트하거나, [wiki:Buildbot] 테스트를 실행하거나, 해당 플랫폼 상에서 작업하는 다른 개발자들의 도움을 받거나 하는 합당한 조치를 취해야 합니다. 새 파일 또는 라이브러리 의존성을 추가하는 경우, configure.in, Makefile.in, Makefile.vc 파일과 관련 문서들을 최신으로 유지해야 합니다.

GDAL/OGR 코드 베이스에서 가져온 다른 업스트림 프로젝트와의 관계
---------------------------------------------------------------

GDAL/OGR 코드 베이스의 일부분은 다른 업스트림 프로젝트로부터 정기적으로 새로고침됩니다. 따라서 해당 영역의 변경 사항은 먼저 해당 업스트림 프로젝트로 들어가야 합니다. 그렇지 않으면 다음 새로고침 때 변경 사항이 사라질 수도 있습니다. 이런 디렉터리에는 GDAL 특화 파일과 업스트림 파일이 섞여 있을 수도 있습니다. 이런 상황은 사례별로 확인해야 합니다. (CVS 변경 로그(changelog)로 시작하는 파일은 업스트림 프로젝트에 속해 있을 가능성이 높습니다.)

현재 이런 업스트림 프로젝트 영역은 다음과 같습니다:

-  :file:`frmts/gtiff/libtiff`: libtiff CVS
   (`http://www.remotesensing.org/libtiff/ <http://www.remotesensing.org/libtiff/>`_)
-  :file:`frmts/gtiff/libgeotiff`: libgeotiff SVN
   (`http://trac.osgeo.org/geotiff/ <http://trac.osgeo.org/geotiff/>`_)
-  :file:`frmts/jpeg/libjpeg`: libjpeg 프로젝트
   (`http://sourceforge.net/projects/libjpeg/ <http://sourceforge.net/projects/libjpeg/>`_)
-  :file:`frmts/png/libpng`: libpng 프로젝트
   (`http://www.libpng.org/pub/png/libpng.html <http://www.libpng.org/pub/png/libpng.html>`_)
-  :file:`frmts/gif/giflib`: giflib 프로젝트
   (`http://sourceforge.net/projects/giflib <http://sourceforge.net/projects/giflib>`_)
-  :file:`frmts/zlib`: zlib 프로젝트
   (`http://www.zlib.net/ <http://www.zlib.net/>`_)
-  :file:`ogr/ogrsf_frmts/mitab`: MITAB CVS
   (`http://mitab.maptools.org/ <http://mitab.maptools.org/>`_)
-  :file:`ogr/ogrsf_frmts/avc`: AVCE00 CVS
   (`http://avce00.maptools.org/ <http://avce00.maptools.org/>`_)
-  :file:`ogr/ogrsf_frmts/shape/[dbfopen.c, shpopen.c, shptree.c, shapefil.h]`: shapelib 프로젝트
   (`http://shapelib.maptools.org/ <http://shapelib.maptools.org/>`_)
-  :file:`data/`: libgeotiff로부터 나온 좌표계 관련 몇몇 .csv 파일

법적 요건
---------

커밋 개발자는 부적절하게 기여된 코드로부터 코드 베이스를 깨끗하게 유지하는 최전선 문지기입니다. GDAL/OGR 사용자, 개발자 및 OSGeo 재단이 프로젝트에 프로젝트 사용 허가 아래 사용 권한이 명확하게 부여되지 않은 코드를 기여하는 일을 피하는 것이 중요합니다.

일반적으로, 주요 문제점은 저장소에 포함될 코드를 제공하는 당사자가 해당 코드가 MIT 허가서(MIT license) 아래 배포될 것이고 코드를 제공한 당사자가 코드를 배포할 권리를 가진다는 사실을 이해해야 한다는 점입니다.
커밋 개발자의 경우 이 사용 허가에 관해 스스로 명확하게 이해기를 바랍니다.
그 외의 기여자의 경우 기여자가 사용 허가를 이해한다는 것을 확신하지 않는 한 (예를 들어 자주 기여하는 사람이 아니라면) 커밋 개발자가 기여자가 사용 허가를 잘 이해하고 있는지 확인해야 합니다.

고용주를 대신해서 기여 코드가 개발된 경우 (근무 시간에, 작업 프로젝트의 일부로서 등등) 고용주의 적절한 대표자가 코드가 MIT 허가서 아래 제공될 것이라는 사실을 이해하는 것이 중요합니다. 승인된 감독자/관리자 등과 협의해서 명확히 해야 합니다.

기여 코드는 기여자가 개발한 코드, 또는 공개 도메인 또는 호환 가능한 사용 허가 아래 오픈 소스와 같이 정당하게 기여할 수 있는 소스로부터 나온 코드여야 합니다.

비정상적인 모든 상황을 논의 그리고/또는 문서화해야 합니다.

커밋 개발자는 다음 지침을 준수해야 하며, 소스 저장소에 코드를 부적절하게 기여하는 경우 개인적으로 법적 책임을 질 수도 있습니다:

-  기여자(및 고용주)가 기여 조건을 알고 있는지 확인하십시오.
-  기여자가 아닌 소스로부터 나온 (이를테면 또다른 프로젝트로부터 따온) 코드에 대해 명확하게 원본 소스, 저작권자, 사용 허가 조건 등등을 명확하게 표시해야 합니다. 파일 헤더에 이런 정보를 넣으면 되지만, 일반 프로젝트 사용 허가서(:file:`gdal/LICENSE.txt`)와 정확하게 일치하지 않는 경우 프로젝트 사용 허가서 파일에도 추가해야 합니다.
-  기존 저작권 헤더 및 사용 허가서 텍스트를 파일로부터 삭제해서는 절대로 안 됩니다. 저작권자가 저작권을 포기하고자 하는 경우 저작권 표시를 제거하기 전에 OSGeo 재단에 서면으로 저작권 포기를 알려야 합니다. 사용 허가 기준을 변경하는 경우, 저작권자의 허가를 (이메일로 작성된 동의도 괜찮습니다) 득해야만 합니다.
-  사용자에게 이름 언급(credit) 또는 공개를 요구하는 사용 허가를 가진 코드는 :file:`/trunk/gdal/LICENSE.TXT` 파일에 추가해야 합니다.
-  파일에 (중요한 패치 같은) 상당한 양의 기여 코드가 추가되는 경우 해당 파일의 저작권자 목록에 저자/기여자를 추가해야 합니다.
-  코드 베이스에 기여하기 위해 변경 사항을 커밋하는 것이 적절한지 불확실한 경우, 프로젝트 운영 위원회 또는 OSGeo 재단 법률 고문에게 자세한 정보를 요청하십시오.

시동
----

다음 기존 커밋 개발자들이 커밋 개발자 지침을 살펴보고 준수하겠다고 동의하는 한, GDAL/OGR 커밋 개발자로 승인된 것으로 간주할 것입니다. 각 개인을 확인하는 것은 SVN 관리자의 책임일 것입니다.

-  대니얼 모리셋(Daniel Morissette)
-  프랑크 바르메르담(Frank Warmerdam)
-  질리언 월터(Gillian Walter)
-  안드레이 키셀레프(Andrey Kiselev)
-  알레산드로 아미치(Alessandro Amici)
-  코르 더용(Kor de Jong)
-  하워드 버틀러(Howard Butler)
-  왕리춘(Wang Lichun)
-  노먼 바인(Norman Vine)
-  켄 멜레로(Ken Melero)
-  케빈 룰랜드(Kevin Ruland)
-  마레크 브루트카(Marek Brudka)
-  피르민 칼베러(Pirmin Kalberer)
-  스티브 술레(Steve Soule)
-  프란스 반 덴 버그(Frans van der Bergh)
-  드니 나도(Denis Nadeau)
-  올렉 세미킨(Oleg Semykin)
-  줄리앙-사뮈엘 라크로와(Julien-Samuel Lacroix)
-  다니엘 발너(Daniel Wallner)
-  찰스 F. I. 새비지(Charles F. I. Savage)
-  마테우시 워스코트(Mateusz Łoskot)
-  너지 페테르(Nagy Peter)
-  사이먼 퍼킨스(Simon Perkins)
-  라딤 블라제크(Radim Blažek)
-  스티브 할라스(Steve Halasz)
-  나초 브로딘(Nacho Brodin)
-  벤저민 콜린스(Benjamin Collins)
-  이방 루세나(Ivan Lucena)
-  아리 욜마(Ari Jolma)
-  세케레시 터마시(Szekeres Tamás)

--------------

-  `COMMITTERS <http://trac.osgeo.org/gdal/browser/trunk/gdal/COMMITTERS>`_ 파일
-  `GDAL SVN 그룹 편집 <https://www.osgeo.org/cgi-bin/auth/ldap_group.py?group=gdal>`_

