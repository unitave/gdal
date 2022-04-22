.. _vector.vfk:

VFK - 체코 지적 정보 교환 데이터 포맷
==========================================

.. shortname:: VFK

.. build_dependencies:: libsqlite3

이 드라이버는 VFK 파일, 그러니까 **체코 지적(地籍) 정보 교환 데이터 포맷** 읽기를 지원합니다. VFK 파일은 레이어를 0개 이상 가진 데이터소스로 인식됩니다.

이 드라이버는 GDAL을 **SQLite 지원과 함께 빌드한 경우에만** 컴파일됩니다.

점은 wkbPoint로, 선 및 경계는 wkbLineString으로 그리고 면은 wkbPolygon으로 표현됩니다. wkbMulti\* 객체는 사용하지 않습니다. 레이어 하나에 객체 유형을 혼합할 수 없습니다.

드라이버 케이퍼빌리티
-------------------

.. supports_georeferencing::

.. supports_virtualio::

열기 옵션
------------

GDAL 2.3버전부터, (일반적으로 ogrinfo 또는 ogr2ogr의 ``-oo name=value`` 파라미터를 사용해서) 다음과 같은 열기 옵션들을 지정할 수 있습니다:

-  **SUPPRESS_GEOMETRY=YES/NO**: (기본값은 NO)
   이 옵션을 YES로 설정하면 도형 분해(resolve)를 건너뜁니다. 모든 레이어가 도형 유형을 가지고 있지 않다고 인식할 것입니다. 사용자가 속성에만 관심이 있는 경우 가장 유용합니다. 도형을 억제하면 드라이버가 입력 VFK 데이터를 읽어올 때 상당한 성능 향상을 볼 수 있다는 사실을 기억하십시오.

-  **FILE_FIELD=YES/NO**: (기본값은 NO)
   이 옵션을 YES로 설정하면 모든 레이어에 소스 VFK 파일의 이름을 담고 있는 새 *VFK_FILENAME* 필드를 추가할 것입니다.

환경설정 옵션
~~~~~~~~~~~~~

다음 :ref:`환경설정 옵션들 <configoptions>` 을 사용할 수 있습니다:

이 드라이버는 VFK 데이터를 읽어올 때 SQLite를 백엔드 데이터베이스로 사용합니다. 기본적으로, 입력 VFK 파일의 디렉터리에 SQLite 데이터베이스를 ('.db' 파일 확장자로) 생성합니다. 사용자가 데이터베이스 이름을 :decl_configoption:`OGR_VFK_DB_NAME` 환경설정 옵션으로 정의할 수 있습니다. :decl_configoption:`OGR_VFK_DB_OVERWRITE` 환경설정 옵션을 YES로 설정하면 드라이버가 기존 SQLite 데이터베이스를 덮어써서 새로 생성된 데이터베이스에 입력 VFK 파일로부터 읽어온 데이터를 저장합니다. :decl_configoption:`OGR_VFK_DB_DELETE` 환경설정 옵션을 YES로 설정하면, 데이터소스를 닫을 때 드라이버가 백엔드 SQLite 데이터베이스를 삭제합니다.

분해된 도형도 SQLite 데이터베이스에 저장됩니다. 즉 VFK 데이터로부터 SQLite 데이터베이스를 작성한 다음에야 도형을 분해한다는 뜻입니다. 도형은 WKB 포맷으로 저장됩니다. 이때 GDAL을 SpatiaLite 지원과 함께 빌드해야 할 필요는 없다는 사실을 기억하십시오. :decl_configoption:`OGR_VFK_DB_SPATIAL` 환경설정 옵션을 NO로 지정하는 경우 데이터베이스에 도형을 저장하지 않습니다. 이 경우 데이터베이스로부터 데이터를 읽어올 때 도형을 실시간(on-the-fly)으로 분해합니다.

내부 작업 및 성능 조정
~~~~~~~~~~~~~~~~~~~~~~

백엔드 SQLite 데이터베이스가 이미 존재하는 경우 드라이버가 입력 데이터소스로 지정된 입력 VFK 파일이 아니라 데이터베이스로부터 직접 객체를 읽어옵니다. 이 경우 드라이버가 객체를 읽어올 때 상당한 성능 향상을 볼 수 있습니다.

이 드라이버는 백엔드 SQLite 데이터베이스를 작성할 때 기본적으로 VFK 파일로부터 모든 데이터 블록을 읽어옵니다. :decl_configoption:`OGR_VFK_DB_READ_ALL_BLOCKS` 환경설정 옵션을 NO로 설정한 경우, 드라이버가 사용자가 요청한 데이터 블록만 읽어옵니다. 사용자가 VFK 데이터의 일부분만 처리하려는 경우 이 옵션이 유용할 수 있습니다.

데이터소스 이름
---------------

데이터소스 이름은 VFK 파일을 가리키는 전체 경로입니다.

이 드라이버는 VSI 가상 파일 시스템 API가 관리하는 파일의 읽기 및 쓰기를 지원합니다. VSI 가상 파일 시스템 API가 관리하는 파일에는 "정규" 파일은 물론 /vsizip/ , /vsigzip/ , /vsicurl/ 읽기 전용 도메인에 있는 파일도 포함됩니다.

GDAL 2.2버전부터 백엔드 SQLite 데이터베이스를 가리키는 전체 경로도 데이터소스 이름으로 사용할 수 있습니다. 기본적으로, 이런 데이터소스를 SQLite 드라이버로 읽어옵니다. :decl_configoption:`OGR_VFK_DB_READ` 환경설정 옵션을 YES로 설정하면 이런 데이터소스를 대신 VFK 드라이버로 엽니다.

레이어 이름
-----------

VFK 데이터 블록을 레이어 이름으로 사용합니다.

필터
-------

속성 필터
~~~~~~~~~

내부 SQL 엔진을 이용해서 표현식을 평가합니다. 속성 필터를 설정하고 나면 평가가 끝납니다.

공간 필터
~~~~~~~~~
위상 구조 안에 저장된 객체의 경계 상자를 이용해서 객체가 현재 공간 필터를 만족시키는지 평가합니다. 공간 필터를 설정하고 나면 평가가 끝납니다.

참고
----

-  `OGR VFK 드라이버 구현 문제점 <http://geo.fsv.cvut.cz/~landa/publications/2010/gis-ostrava-2010/paper/landa-ogr-vfk.pdf>`_
-  `VFK 포맷 용 오픈 소스 도구 <http://freegis.fsv.cvut.cz/gwiki/VFK>`_ (체코어)
-  `체코 지적 정보 교환 데이터 포맷 문서 <http://www.cuzk.cz/Dokument.aspx?PRARESKOD=998&MENUID=0&AKCE=DOC:10-VF_ISKNTEXT>`_ (체코어)

