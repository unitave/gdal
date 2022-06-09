.. _rfc-71:

===========================
RFC 71: 깃허브 마이그레이션
===========================

======= ==========================
저자:   이벤 루올
연락처: even.rouault@spatialys.com
제안일: 2018년 3월
상태:   승인, 구현
======= ==========================

요약
----

GDAL 소스 트리 및 티켓 데이터베이스를 OSGeo가 호스팅하는 서브버전(Subversion) 저장소/트랙(Trac) 데이터베이스로부터 깃허브(GitHub)로 옮길 것을 제안합니다. 소스 코드 이력은 온전히 보전될 것입니다. 이 마이그레이션을 보다 간단하게 하기 위해, 기존 티켓들은 OSGeo 트랙에 남겨두고 깃허브로 마이그레이션하지 않을 것입니다. 새 티켓은 깃허브에서 열어야 할 것입니다.

동기
----

1. GDAL 개발에 관심을 가진 대부분의 개발자들이 요즘 서브버전보다 깃(git)에 더 익숙한 것으로 보이며, 서브버전을 주 소스 제어 관리 도구로 계속 사용하는 경우 기여자들의 참여도가 떨어질 것으로 생각됩니다.

2. 2012년부터 `https://github.com/OSGeo/gdal <https://github.com/OSGeo/gdal>`_ 미러 사이트가 존재했으며, 그 동안 직접 SVN에 접속할 수 없는 기여자들이 (또는 접속할 수 있는 기여자들조차) -- 특히 유지/관리자가 기여 코드가 알려져 있는 퇴행(regression)을 도입하진 않았는지 확인할 수 있게 해주는 `Travis-CI <https://www.travis-ci.com/>`_ 와 `AppVeyor <https://www.appveyor.com/>`_ 의 `지속적 통합 <https://ko.wikipedia.org/wiki/%EC%A7%80%EC%86%8D%EC%A0%81_%ED%86%B5%ED%95%A9>`_ 서비스와 풀 요청에 코멘트를 다는 친화적인 방식이 합쳐져 -- 깃허브에 기여 코드를 커밋하는 편을 선호해왔습니다. 하지만 GDAL 유지/관리자들이 **깃허브** 풀 요청을 트랙으로 직접 포팅하는 일은 조금 벅찹니다.

3. GitHub has become the de-facto hosting platform for a lot of open-source projects.

마이그레이션 상세 사항
----------------------

0. The existing GitHub git repository will be pushed to `https://github.com/OSGeo/gdal_svn_mirror_backup <https://github.com/OSGeo/gdal_svn_mirror_backup>`_ (eventually removed once we are confident further steps have not messed things up)

1. As GitHub also uses the syntax "#1234" to link commit messages to its issues that was also used in Trac, currently when following links in **깃허브** that point to a Trac ticket, one ends up to a non-existing or unrelated **깃허브** issue/pull request.
   So the commit messages of the current **깃허브** mirror will be rewritten by a "git filter-branch --msg-filter 'python rewrite.py' -- --all" command to replace "#1234" with "`https://trac.osgeo.org/gdal/ticket/1234 <https://trac.osgeo.org/gdal/ticket/1234>`_"

2. The git 'trunk' branch will be renamed 'master' to follow git best practices

3. The existing 'tag/x.y.z' branches will be replaced by proper git tags.

4. This modified repository will be forced push to `https://github.com/OSGeo/gdal <https://github.com/OSGeo/gdal>`_
   This will have the consequence of invalidating existing pull request or forks of repository that will have to be rebased to the new one.
   From that point, "svn commit" should be avoided and changes should go to the git repository.

5. The cron job on the OSGeo server that refreshes the website from sources will be modified to pull from **깃허브** rather than SVN.

6. Ticket creation permissions will be removed in Trac.
   Modification or closing of existing open tickets will still be possible.
   From that point, if closing a Trac ticket, one will have manually to reference the github commit.

7. The settings of the GDAL GitHub repository will be changed allow tickets to be filed. Labels and Milestones will be populated with relevant content

Further actions required, in no particular order, and for which help from other GDAL developers/contributors would be welcome:

-  Most visible Trac wiki documentation will have to be revised to point to GitHub

-  HOWTO-RELEASE will have to be revised.

-  Existing SVN committers still interested in the project will have to request commit access to the GitHub repo.

-  Some support from OSGeo SAC will be needed to turn the GDAL SVN repository to read-only (a complementary option would be to rename it to gdal_historical so that people pulling from the old one are well aware of the migration by having their scripts 'cleanly' error out)

-  Some guidelines on how we intend to use git/GitHub features will have to be rewritten.

출구 전략
---------

GitHub is a closed platform. In case it would close or would start asking to pay unreasonable fees, some backup strategy of the tickets would be needed. The solutions might be:

-  `https://github.com/josegonzalez/python-github-backup <https://github.com/josegonzalez/python-github-backup>`_

-  GitLab has an import module from GitHub.
   Although some experimentation has been done with those, this RFC does *not* cover setting up those solutions as a regular backup system.

이 RFC가 다루지 않은 내용
-------------------------

-  Migration of Trac wiki content to GitHub wiki is not in the scope of this RFC. Can be done later

관련된 예전 논의들
------------------

-  `https://lists.osgeo.org/pipermail/gdal-dev/2018-March/048240.html <https://lists.osgeo.org/pipermail/gdal-dev/2018-March/048240.html>`_
-  `https://lists.osgeo.org/pipermail/gdal-dev/2017-September/047060.html <https://lists.osgeo.org/pipermail/gdal-dev/2017-September/047060.html>`_

투표 이력
---------

-  하워드 버틀러 +1
-  유카 라흐코넨 +1
-  커트 슈베어 +1
-  이벤 루올 +1

