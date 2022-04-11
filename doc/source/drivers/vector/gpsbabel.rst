.. _vector.gpsbabel:

GPSBabel
========

.. shortname:: GPSBabel

.. build_dependencies:: (읽기 지원에 GPX 드라이버 및 libexpat 필요)

GPSBabel 드라이버는 현재 다양한 GPS 파일 포맷에 접근하기 위해 `GPSBabel <http://www.gpsbabel.org>`_ 유틸리티에 의존합니다.

PATH를 통해 GPSBabel 실행 파일에 접근할 수 있어야만 합니다.

드라이버 케이퍼빌리티
-------------------

.. supports_create::

.. supports_georeferencing::

읽기 지원
------------

이 드라이버가 GPSBabel의 산출물을 파싱할 수 있으려면 :ref:`GPX <vector.gpx>` 드라이버를 (Expat 라이브러리를 통한) 읽기 지원으로 완전하게 환경설정해줘야 합니다. GPX를 중간 피벗(intermediate pivot) 파일로 사용하기 때문입니다.

입력 데이터에 따라 반환 레이어가 waypoints, routes, route_points, tracks, track_points일 수 있습니다.

입력 데이터소스를 지정하는 문법은 다음과 같습니다:

::

   GPSBabel:gpsbabel_file_format[,gpsbabel_format_option]*:[features=[waypoints,][tracks,][routes]:]filename

이때:

-  *gpsbabel_file_format* 은 GPSBabel이 처리하는 `파일 포맷 <http://www.gpsbabel.org/capabilities.shtml>`_ 가운데 하나입니다.

-  *gpsbabel_format_option* 은 지정한 GPSBabel 포맷이 처리하는 모든 옵션이 될 수 있습니다. (각 GPSBabel 포맷 문서를 참조하십시오.)

-  *features=* 를 사용하면 GPSBabel이 가져올 객체의 유형을 수정할 수 있습니다. waypoint는 GPSBabel 명령줄의 "-w" 옵션과, track은 "-t"와 그리고 route는 "-r"와 일치합니다. 이 옵션을 사용해서 GPSBabel이 기본적으로 waypoint만 가져왔을 느린 GPS 수신기로부터 전체 데이터를 요청할 수 있습니다. 더 자세한 내용은 `경로(route) 및 트랙(track) 모드 <http://www.gpsbabel.org/htmldoc-1.3.6/Route_And_Track_Modes.html>`_ 에 관한 문서를 읽어보십시오.

-  *filename* 은 디스크 상에 있는 실제 파일일 수도, GDAL 가상 파일 API를 통해 처리되는 파일일 수도, 또는 "usb:", "/dev/ttyS0", "COM1:" 등등처럼 GPSBabel이 처리하는 특수 기기일 수도 있습니다. 사용된 GPSBabel 포맷에 따라 실제로 지원하는 대상이 달라집니다.

이 뿐만이 아니라 선택된 일부 GPSBabel 포맷의 경우 파일명만 지정해줘도 충분할 수 있습니다. 현재 지원하는 목록은 다음과 같습니다:

-  garmin_txt
-  gtrnctr
-  gdb
-  magellan
-  mapsend
-  mapsource
-  nmea
-  osm
-  ozi
-  igc

USE_TEMPFILE 환경설정 옵션을 YES로 설정하면, 대용량 데이터를 읽어오는 경우 인메모리(in-memory)가 아니라 디스크 상에 임시 GPX 파일을 생성할 수 있습니다.

쓰기 지원
-------------

이 드라이버는 GPSBabel이 최종적으로 바람직한 GPSBabel 포맷으로 변환할 중간 파일 생성을 GPX 드라이버에 의존합니다. (GPSBabel 쓰기 지원을 위해 GPX 드라이버를 읽기 지원 환경설정할 필요는 없습니다.)

지원 도형, 옵션 및 기타 생성 문제점들은 모두 GPX 드라이버의 것들입니다. 자세한 내용은 :ref:`GPX 드라이버 <vector.gpx>` 문서를 참조하십시오.

산출 데이터소스를 지정하는 문법은 다음과 같습니다:

::

   GPSBabel:gpsbabel_file_format[,gpsbabel_format_option]*:filename
   
이때:

-  *gpsbabel_file_format* 은 GPSBabel이 처리하는 `파일 포맷 <http://www.gpsbabel.org/capabilities.shtml>`_ 가운데 하나입니다.

-  *gpsbabel_format_option* 은 지정한 GPSBabel 포맷이 처리하는 모든 옵션이 될 수 있습니다. (각 GPSBabel 포맷 문서를 참조하십시오.)

이 뿐만 아니라, 데이터셋 생성 옵션 GPSBABEL_DRIVER=gpsbabel_file_format[,gpsbabel_format_option]\* 을 지정해서 산출 데이터소스 이름을 그냥 파일명으로 전송할 수도 있습니다.

USE_TEMPFILE 환경설정 옵션을 YES로 설정하면, 대용량 데이터를 작성하는 경우 인메모리(in-memory)가 아니라 디스크 상에 임시 GPX 파일을 생성할 수 있습니다.

예시
~~~~~~~~

가민(Garmin) 사의 USB 수신기로부터 waypoint 읽어오기:

::

   ogrinfo -ro -al GPSBabel:garmin:usb:

shapefile을 마젤란(Magellan) 사의 Mapsend 포맷으로 변환하기:

::

   ogr2ogr -f GPSBabel GPSBabel:mapsend:out.mapsend in.shp

See Also
~~~~~~~~

-  `GPSBabel 홈페이지 <http://www.gpsbabel.org>`_

-  `GPSBabel 파일 포맷 <http://www.gpsbabel.org/capabilities.shtml>`_

-  :ref:`GPX <vector.gpx>` 드라이버
