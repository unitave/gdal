.. _raster.msg:

================================================================================
MSG -- 2세대 Meteosat
================================================================================

.. shortname:: MSG

.. build_dependencies:: msg 라이브러리

이 드라이버는 MSG(Meteosat Second Generation) 파일 읽기를 구현했습니다. MSG 포맷은 ``H-000-MSG1\_\_-MSG1\_\_\_\_\_\_\_\_-HRV\_\_\_\_\_\_-000007\_\_\_-200405311115-C\_`` 같은 이름을 가지고 있는 파일들로, 보통 날짜로 되어 있는 (예를 들어 앞의 이름에서 ``2004\05\31``) 폴더 구조로 배포됩니다.

MSG 파일은 웨이블릿 압축 파일입니다. 압축 해제 라이브러리를 (`공공 웨이블릿 변환 압축 해제 라이브러리 소프트웨어 <https://gitlab.eumetsat.int/open-source/PublicDecompWT>`_, 단축명은 *웨이블릿 변환 소프트웨어(Wavelet Transform Software)* 를) 사용하려면 `EUMETSAT <http://www.eumetsat.int/>`_ 의 사용 허가가 필요합니다. 마이크로소프트 윈도우, 리눅스 및 솔라리스 운영 체제 상에서 이 소프트웨어를 컴파일할 수 있으며, 32비트 및 64비트는 물론 혼합 아키텍처에서도 작동합니다. 아파치 버전 2에 이 소프트웨어의 사용 권한이 포함되어 있습니다.

이 드라이버는 기본적으로 "활성화"되어 있지 않습니다. `빌드 지침 <#build_instructions>`_ 에서 사용자의 GDAL 라이브러리에 어떻게 이 드라이버를 포함시키는지에 관해 읽어보십시오.

드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

빌드 지침
------------------

CMake 빌드
++++++++++++

:ref:`build_hints` 의 ``GDAL_USE_PUBLICDECOMPWT`` 옵션을 참조하십시오.

기타 빌드 시스템
+++++++++++++++++++

웨이블릿 압축 해제 용 EUMETSAT 라이브러리를 ``frmts/msg`` 로 복사하십시오.

비주얼 스튜디오 6.0으로 빌드하는 경우, 해당 디렉터리에 저장되어 있는 ``PublicDecompWTMakefiles.zip`` 파일로부터 *PublicDecompWT* 를 위한 .vc makefile을 추출하십시오.

GNUMakefile을 이용해서 빌드하는 경우, ``--with-msg`` 옵션으로 MSG 드라이버를 활성화하십시오:

::

   ./configure --with-msg

사용자가 makefile 그리고/또는 MSG 소스 파일에서 조정이 필요한 점을 알아냈다면, "커밋(commit)"해주십시오. EUMETSAT 라이브러리는 "크로스 플랫폼"이지만, 마이크로소프트 윈도우와 비주얼 스튜디오 6.0과 작업하면서 다른 플랫폼의 MSG 드라이버를 확인할 여력이 없었습니다. 그리고 :ref:`raster_driver_tut` 의 "GDAL 트리에 드라이버 추가하기" 단락에 있는 4단계부터 7단계까지를 적용하십시오.

`MSG 위키 페이지 <https://trac.osgeo.org/gdal/wiki/MSG>`_ 에서 MSG 빌드 및 활용에 대한 힌트를 문서화하고 있습니다.

소스 데이터셋 사양
-------------------------------

개별 파일을 선택해서 열 수도 있습니다. 이런 경우, 드라이버가 동일 이미지의 다른 스트립(strip)들에 대응하는 파일을 수집해서 이미지를 정확하게 구성할 것입니다.

다음은 gdal_translate.exe를 사용하는 예시입니다:

::

   gdal_translate
    C:\hrit_a\2004\05\31\H-000-MSG1__-MSG1________-HRV______-000008___-200405311115-C_
    C:\output\myimage.tif

다음 문법을 사용해서 MSG 파일을 열 수도 있습니다:

-   MSG(source_folder,timestamp,(channel,channel,...,channel),use_root_folder,data_conversion,nr_cycles,step)

   -  source_folder: 파일들을 담고 있는 폴더 구조를 가리키는 경로
   -  timestamp: 해당 시간에 촬영된 이미지 12개의 파일 114개를 식별하는 날짜/시간을 표현하는 12자리 숫자. 예: 200501181200
   -  channel: 1에서 12 사이의 숫자. 사용할 수 있는 채널 12개를 각각 표현합니다. 채널 1개만 지정하는 경우, 괄호는 있어도 없어도 됩니다.
   -  use_root_folder: Y로 설정하면 파일들이 지정한 source_folder 자체에 존재한다는 의미입니다. N로 설정하면 파일들이 날짜 구조의 폴더(source_folder/YYYY/MM/DD)에 존재한다는 의미입니다.
   -  data_conversion:

      -  원본 10비트 DN 값을 유지하려면 N으로 설정하십시오. UInt16형 데이터를 산출합니다.
      -  (GIF 및 JPEG 이미지의 경우 편리한) 8비트로 변환하려면 B로 설정하십시오. 바이트형 데이터를 산출합니다.
      -  방사측정 보정을 수행하고 mW/m2/sr/(cm-1)-1 단위로 변환하려면 R로 설정하십시오. Float32 데이터를 산출합니다.
      -  방사측정 보정을 수행하고 W/m2/sr/um 단위로 변환하려면 L로 설정하십시오. Float32 데이터를 산출합니다.
      -  가시 밴드(1, 2, 3 및 12)의 반사율 및 적외선 밴드(다른 모든 밴드)의 켈빈 온도 단위 기온으로 변환하려면 T로 설정하십시오. Float32 데이터를 산출합니다.

   -  nr_cycles: 동일 (시계열) 파일에 포함되기 위해 필요한 연속 사이클의 횟수를 나타내는 숫자입니다. 추가적인 밴드로 첨부됩니다.
   -  step: 다중 사이클을 선택했을 때 단계 크기(stepsize)를 나타내는 숫자입니다. 예를 들어 15분마다: step = 1, 30분마다: step = 2, ... 사이클은 정확히 15분 간격이기 때문에 그 사이의 시간으로부터 이미지를 얻을 수는 없다는 사실을 기억하십시오. (step은 정수형이기 때문입니다.)

다음은 gdal_translate 유틸리티를 사용하는 예시입니다.

200501181200 MSG 이미지의 1, 2, 3번 밴드를 IMG 포맷으로 가져오는 예시:

::

   gdal_translate -of HFA MSG(\\pc2133-24002\RawData\,200501181200,(1,2,3),N,N,1,1) d:\output\outfile.img

동일하지만, 모든 값을 4로 나누어 10비트 이미지를 8비트로 변환해서 JPG 포맷으로 가져오는 예시:

::

   gdal_translate -of JPEG MSG(\\pc2133-24002\RawData\,200501181200,(1,2,3),N,B,1,1) d:\output\outfile.jpg

동일하지만, JPEG 이미지의 밴드를 RGB 비슷하게 재정렬하는 예시:

::

   gdal_translate -of JPEG MSG(\\pc2133-24002\RawData\,200501181200,(3,2,1),N,B,1,1) d:\output\outfile.jpg

원본 10비트 값을 유지하면서 2번 밴드만 Geotiff 포맷으로 가져오는 예시:

::

   gdal_translate -of GTiff MSG(\\pc2133-24002\RawData\,200501181200,2,N,N,1,1) d:\output\outfile.tif

동일하지만, 12번 밴드만:

::

   gdal_translate -of GTiff MSG(\\pc2133-24002\RawData\,200501181200,12,N,N,1,1) d:\output\outfile.tif

동일하지만, 12번 밴드를 mW/m2/sr/(cm-1)-1 단위로 방사측정 보정:

::

   gdal_translate -of GTiff MSG(\\pc2133-24002\RawData\,200501181200,12,N,R,1,1) d:\output\outfile.tif

\\\pc2133-24002\RawData\... 대신 c:\hrit-data\2005\01\18 로부터 데이터 추출:

::

   gdal_translate -of GTiff MSG(c:\hrit-data\2005\01\18,200501181200,12,Y,R,1,1) d:\output\outfile.tif

동일하지만, 다른 옵션으로 ("use_root_folder" 파라미터 자리의 Y와 N의 차이점을 주목하십시오):

::

   gdal_translate -of GTiff MSG(c:\hrit-data\,200501181200,12,N,R,1,1) d:\output\outfile.tif

방사측정 보정을 빼고, 연속 사이클 10회 (따라서 1200에서 1415까지):

::

   gdal_translate -of GTiff MSG(c:\hrit-data\,200501181200,12,N,N,10,1) d:\output\outfile.tif

연속 사이클 10회, 그러나 1시간 간격으로 (따라서 1200에서 2100까지):

::

   gdal_translate -of GTiff MSG(c:\hrit-data\,200501181200,12,N,N,10,4) d:\output\outfile.tif

1시간 간격으로 연속 사이클 10회, 3, 2, 1 밴드를 가져오는 예시:

::

   gdal_translate -of GTiff MSG(c:\hrit-data\,200501181200,(3,2,1),N,N,10,4) d:\output\outfile.tif

지리참조 및 투영법
---------------------------

MSG 이미지는 정지위성 뷰(Geostationary Satellite View) 투영법을 사용합니다. 대부분의 GIS 패키지는 이 투영법을 인식하지 못 하지만 (이 투영법을 사용할 수 있다고 알려진 드라이버는 ILWIS가 유일합니다) gdalwarp.exe를 사용하면 이미지를 재투영할 수 있습니다.

참고
--------

-  ``gdal/frmts/msg/msgdataset.cpp`` 로 구현되었습니다.
-  http://www.eumetsat.int - 유럽기상위성개발기구
