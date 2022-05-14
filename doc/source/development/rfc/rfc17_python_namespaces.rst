.. _rfc-17:

================================================================================
RFC 17: 파이썬 이름공간
================================================================================

저자: 하워드 버틀러(Howard Butler)

연락처: hobu.inc@gmail.com

상태: 승인

요약
-------

-  파이썬 용 GDAL 바인딩은 패키지 및 이름공간을 이용해서 구조(organization)를 제공하는 일반적인 파이썬 관행을 피해온 이력이 있습니다.

-  이 RFC는 GDAL 파이썬 바인딩이 이제부터 상주하게 될 'osgeo'라는 파이썬 용 새 이름공간을 구현합니다.
   하위 호환성을 제공하기 때문에 현재 코드를 변경하지 않고 계속 실행하지만, 코드 구조 및 전체 수준 이름공간 오염이라는 이유를 위해 이름공간을 사용해야 하도록 개발할 것입니다.
   2007년 10월 1일부로 이 RFC 17에서 설명하는 변경 사항들은 "차세대" 파이썬 바인딩에만 적용됩니다.
   GDAL 1.5버전에서는 이 바인딩이 기본 바인딩이 될 것으로 예상합니다.

목표
----

이름공간이 제대로 지정된 파이썬 패키지에 GDAL 파이썬 바인딩을 제공해서 파이썬의 전체 수준 이름공간 오염을 제거합니다.

과거 사용례
-----------

예전 GDAL의 파이썬 바인딩은 전체 수준에서 인식되는 파이썬 모듈들을 사용했습니다:

::

   import gdal
   import osr
   import ogr
   import gdalconst
   import gdalnumeric

새로운 사용례
-------------

RFC 17은 이제 'osgeo' 이름공간 아래 이 모듈들을 제공합니다:

::

   from osgeo import gdal
   from osgeo import osr
   from osgeo import ogr
   from osgeo import gdalconst
   from osgeo import gdal_array

뿐만 아니라, 예전 모듈 스타일의 가져오기도 퇴출 경고와 함께 계속 작동합니다:

::

   >>> import gdal
   /Users/hobu/svn/gdal/swig/python/gdal.py:3: DeprecationWarning: gdal.py was placed in a namespace, it is now available as osgeo.gdal
   warn('gdal.py was placed in a namespace, it is now available as osgeo.gdal', DeprecationWarning)

향후 적절한 시기에 GDAL 특화 전체 수준 모듈을 제거할 계획입니다.

기타 스프린트 업데이트
----------------------

하워드 버틀러와 크리스 바커(Chris Barker)가 FOSS4G2007 GDAL 코드 스프린트에서 이 RFC를 위한 작업을 수행했습니다. 파이썬 이름공간 작업만이 아니라 GDAL 바인딩 빌드라는 측면에서 몇몇 사소한 문제점들을 처리했습니다.

1. 차세대 파이썬 바인딩은 이제 설정 도구(setuptools)를 사용할 수 있는 경우 기본적으로 설정 도구를 사용합니다.
2. 순수한 파이썬 모듈로부터 확장 사양을 구분할 수 있도록 :file:`./swig/python` 디렉터리의 구조를 살짝 변경했습니다.
3. 페트르 클로칸(Petr Klokan)의 구글 서머 오브 코드(Google Summer of Code) 프로젝트인 gdal2tiles 유틸리티를 차세대 바인딩으로 통합했습니다.

투표 이력
---------

FOSS4G2007 스프린트에서 (최초의) 음성 투표가 시행되었습니다.

-  프랑크 바르메르담 +1
-  하워드 버틀러 +1
-  대니얼 모리셋 +1
-  세케레시 터마시 +1

