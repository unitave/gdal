.. _developer_contribution:

======================================
GDAL로의 개발자 기여
======================================

필요한 모든 개발 패키지를 설치하십시오:

-  GNU Make
-  g++
-  ...

빌드:

::

   cd gdal
   ./autogen.sh
   ./configure [options]
   make -j8 -s
   cd apps; make -s test_ogrsf; cd ..

(설치 없이) 명령줄 유틸리티 실행:

::

   . scripts/setdevenv.sh
   gdalinfo --version

자동 테스트 스위트 실행:

::

   cd ../autotest
   pip install -r requirements.txt
   pytest

GDAL의 깃(git) 워크플로
-----------------------

이 단락은 깃 예제 또는 참조 매뉴얼이 아닙니다. GDAL 개발을 위해 깃 사용법의 모범 사례를 몇 가지 모아놓았을 뿐입니다.

메시지 커밋하기
+++++++++++++++

구성 요소 이름(예: 드라이버 이름), 간단한 설명 및 관련이 있을 경우 문제점에 대한 참조를 (해당 참조가 실제로 문제점을 수정하는 경우 'fixes #'와 함께) 나타내십시오.

::

   COMPONENT_NAME: fix bla bla (fixes #1234)

   Details here...

작업 저장소 시작하기
++++++++++++++++++++

깃허브 UI에서 `OSGeo/GDAL <https://github.com/OSGeo/gdal>`_ 을 포크한 다음:

::

   git clone https://github.com/OSGeo/gdal
   cd gdal
   git remote add my_user_name https://github.com/my_user_name/gdal.git

로컬 마스터를 업스트림 마스터로 업데이트하기
++++++++++++++++++++++++++++++++++++++++++++

::

   git checkout master
   git fetch origin
   # 조심하십시오: 여러분이 수정했던 모든 로컬 변경 사항이 없어질 것입니다.
   git reset --hard origin/master

기능 브랜치 작업하기
++++++++++++++++++++

::

   git checkout master
   (앞에서 설명한 대로 로컬 마스터를 업스트림 마스터로 업데이트할 가능성이 있습니다)
   git checkout -b my_new_feature_branch

   # 작업을 수행합니다. 예를 들어:
   git add my_new_file
   git add my_modifid_message
   git rm old_file
   git commit -a

   # 브랜치를 생성한 이후 추가된 버그 수정 또는 새 케이퍼빌리티가 필요한 경우
   # 마스터를 대상으로 다시 동기화해야 할 수도 있습니다.
   git fetch origin
   git rebase origin/master

   # 작업이 끝나면 중요하지 않은 커밋을 일관적인 집합으로 접어서
   # 이력이 타당한지 확인하십시오.
   git rebase -i master (예를 들어 커밋 여러 개를 병합하려면 'fixup'을 사용하고,
   커밋 메시지를 수정하려면 'reword'를 사용하십시오.)

   # 또는 커밋이 너무 많아서 모든 커밋을 'fixup'으로 표시하기 귀찮을 경우
   git fetch origin
   git rebase origin/master
   git reset --soft origin/master
   git commit -a -m "Put here the synthetic commit message"

   # 브랜치를 푸시하십시오.
   git push my_user_name my_new_feature_branch
   From GitHub UI, issue a pull request

풀 요청 논의 또는 CI 확인에 변경 사항이 필요한 경우, 로컬에서 커밋한 다음 푸시하십시오. 타당한 이력을 얻으려면 ``git rebase -i master`` 를 실행해야 할 수도 있습니다. 이 경우 ``git push -f my_user_name my_new_feature_branch`` 로 자신의 브랜치를 강제로 푸시해야 할 것입니다.

마스터로부터 안정 브랜치로 버그 수정을 백포팅(backport)하기
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

::

   git checkout master
   깃 로그를 사용해서 백포팅하려는 커밋의 sha1sum을 식별하십시오.
   git checkout 2.2 (2.2 버전으로 백포팅하려는 경우)
   git pull origin 2.2
   (git checkout -b branch_name: 백포트를 풀 요청으로 제출하려는 경우)
   git cherry-pick the_sha1_sum
   git push ...

변경 사항을 적용해야 하는 경우, 적용한 다음 ``git commit -a --amend`` 를 실행하십시오.

해서는 안 되는 일
+++++++++++++++++

(`OSGeo/GDAL <https://github.com/OSGeo/gdal>`_ 에 푸시할 권한을 가지고 있는 누구나)
어떤 커밋도 또는 https://github.com/OSGeo/gdal 에 커밋된 어떤 내용의 이력도 절대로 수정해서는 안 됩니다.

