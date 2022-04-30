.. _gdal_python_utilities:

================================================================================
GDAL 파이썬 유틸리티
================================================================================

GDAL 파이썬 유틸리티는 GDAL에 포함되어 있습니다. GDAL을 설치했다면 사용할 수 있다는 뜻입니다. 하지만 GDAL을 변경하지 않고 최신 또는 예전 버전의 유틸리티를 사용하고 싶을 수도 있습니다. 이런 경우 **gdal-utils** 를 사용하면 됩니다.

-  **gdal-utils**:
   GDAL 파이썬 유틸리티 '배포판'입니다. 이걸 설치하면 됩니다. 홈페이지는 https://pypi.org/project/gdal-utils/ 입니다. ``pip install gdal-utils`` 명령어로 설치하십시오.

-  **osgeo_utils**:
   파이썬 '패키지'입니다. 이 패키지를 설치한 다음 사용자의 코드에 ``from osgeo_utils import ...`` 처럼 사용합니다. 사용자가 코드를 작성하지 않는다면 무시하십시오.

자주 사용되는 유틸리티에는 다음 유틸리티가 포함됩니다:

-  gdal_merge
-  gdal_edit
-  gdal_calc
-  ogrmerge

완전한 목록을 보고 싶다면 :ref:`프로그램 <programs>` 페이지에서 ``.py`` 로 끝나는 유틸리티를 찾아보십시오.

개발자
----------

:ref:`gdal-utils 프로젝트 헌장 <rfc-78>` 을 읽어보십시오.

`GDAL 프로젝트 <https://github.com/osgeo/gdal/>`_ 를 복제하거나 다운로드하십시오.

사용자의 IDE(Integrated Development Environment)에서 "gdal-utils"를 루트 폴더의 `.../swig/python/gdal-utils <https://github.com/OSGeo/gdal/tree/master/swig/python/gdal-utils/>`_ 로 설정하십시오.

   -  **./osgeo_utils**:
      (``pip`` 로 생성하고 ``PYTHONHOME/Scripts`` 에 추가된 시작 래퍼(launch wrapper)를 가진 스크립트인) 프로그램을 담고 있습니다.

   -  **./osgeo_utils/samples**:
      작동하는 파이썬 스크립트이지만 일반적으로 해당 경로에서만 사용할 수 있습니다. (``python path/to/samples/something.py`` 같은 명령어로 실행하십시오.)

웹 페이지를 생성하는 `.../doc/source <https://github.com/OSGeo/gdal/tree/master/doc/source>`_ 에 있는 RST 파일을 편집해서 문서를 향상시키십시오:

-  https://gdal.org/api/index.html#python-api
-  https://gdal.org/programs/index.html#programs
-  https://gdal.org/api/python_samples.html

주 GDAL 프로젝트의 사용자 포크로부터 `풀 요청(Pull Request) <https://github.com/OSGeo/gdal/pulls>`_ 을 'gdal-utils' 라벨로 전송해서 변경 사항을 반영하도록 요청하십시오.

