.. _vector.sxf:

SXF - 저장소 및 정보 교환 포맷
=================================

.. shortname:: SXF

.. built_in_by_default::

이 드라이버는 러시아 GIS 소프트웨어 파노라마(Panorama)에서 주로 사용되는 오픈 포맷인 SXF(Storage and eXchange Format) 파일 읽기를 지원합니다.

SXF 드라이버는 읽기 전용이지만, 데이터소스 삭제를 지원합니다. 이 드라이버는 SXF 바이너리 파일 3.0 이상 버전을 지원합니다.

SXF 레이어는 다음과 같은 케이퍼빌리티를 지원합니다:

-  UTF-8 인코딩 문자열
-  임의 읽기
-  빠른 객체 개수 세기
-  빠른 범위 가져오기
-  색인으로 빠른 다음 설정하기

이 드라이버는 SXF로부터 나온 객체를 레이어에 매핑하기 위해 분류자(classifier; RSC 파일)를 사용합니다. 어떤 레이어에도 속하지 않은 객체는 "Not_Classified"라는 이름의 레이어에 넣습니다. 데이터소스에 객체가 없는 레이어는 존재하지 않습니다.

RSC 파일을 자동적으로 사용하려면 SXF 파일과 동일한 기본명을 가지고 있어야 합니다. 사용자가 :decl_configoption:`SXF_RSC_FILENAME` 환경설정 옵션을 사용해서 RSC 파일 경로를 지정할 수 있습니다. 이 환경설정 옵션이 동일 기반명 RSC 파일 사용을 대체합니다.

RSC 파일은 보통 레이어의 긴 이름과 단축명을 함께 저장합니다. 긴 이름은 보통 러시아어, 단축명은 영어로 되어 있습니다. :decl_configoption:`SXF_LAYER_FULLNAME` 환경설정 옵션을 사용해서 어떤 레이어 이름을 사용할지 선택할 수 있습니다. :decl_configoption:`SXF_LAYER_FULLNAME` 환경설정 옵션을 TRUE로 설정하면 드라이버가 긴 이름을 사용하고, FALSE로 설정하면 단축명을 사용합니다.

이 드라이버는 SXF 파일로부터 속성을 읽어옵니다. 동일한 레이어에서 서로 다른 개수의 속성을 가진 객체들을 위해 필드 최대 개수를 생성합니다. 속성이 RSC 파일에 매핑된 코드를 가진 경우, 드라이버가 코드만 추가합니다. (값의 유형이 필드 유형과 다를 수도 있기 때문에 RSC 파일로부터 실제 값을 가져오지 않습니다.)

:decl_configoption:`SXF_SET_VERTCS` 환경설정 옵션을 ON으로 설정하면, 수직 좌표계 설명이 존재하는 경우 수직 좌표계 설명에 레이어의 공간 좌표계를 포함시킬 것입니다.

GDAL 3.1버전부터 환경설정 옵션을 드라이버의 열기 옵션으로 전송할 수 있습니다.

데이터 케이퍼빌리티
-------------------

.. supports_georeferencing::

.. supports_virtualio::

참고
--------

-  `파노라마 웹페이지 <http://gisinfo.ru>`_
-  `SXF 바이너리 포맷 설명 v.4 (러시아어) - pdf <http://gistoolkit.ru/download/doc/sxf4bin.pdf>`_
-  `SXF 바이너리 포맷 설명 v.4 (러시아어) - doc <http://gistoolkit.ru/download/classifiers/formatsxf.zip>`_
-  `SXF 포맷 설명 v.3 (러시아어) <http://loi.sscc.ru/gis/formats/Format-geo/sxf/sxf3-231.txt>`_
-  `RSC 포맷 설명 (러시아어) <http://gistoolkit.ru/download/classifiers/formatrsc.zip>`_
-  `SXF 포맷 공간 데이터 테스트 (러시아어) <http://www.gisinfo.ru/price/price_map.htm>`_
-  `몇몇 RSC 파일 (러시아어) <http://www.gisinfo.ru/classifiers/classifiers.htm>`_

