.. _vector.idb:

IDB
===

.. shortname:: IDB

.. build_dependencies:: Informix DataBlade

IDB 드라이버는 DataBlade 공간 모듈로 확장된 IBM Informix에 있는 공간 테이블에 접근하기 위한 지원을 구현했습니다.

데이터베이스를 열 때, 다음과 같은 형식으로 된 이름을 지정해야 합니다:

::

   IDB:dbname={dbname} server={host} user={login} pass={pass} table={layertable}

"IDB:" 접두어를 사용해서 이름을 IDB 연결 문자열로 표시합니다.

*geometry_columns* 테이블이 존재하는 경우, 목록화된 테이블 및 명명된 뷰를 모두 OGR 레이어로 취급할 것입니다. 그렇지 않으면 모든 정규 사용자 테이블을 레이어로 취급할 것입니다.

정규 (비공간) 테이블에 접근할 수 있으며, 도형이 아니라 속성을 가진 객체를 반환할 것입니다. 테이블에 "st_*" 필드가 존재하는 경우, 공간 테이블로 취급할 것입니다. 필드를 읽는 방법을 판단하기 위해 필드 유형을 조사합니다.

이 드라이버는 자동 FID 탐지를 지원합니다.

드라이버 케이퍼빌리티
-------------------

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::

환경 변수
---------------------

-  **INFORMIXDIR**:
   Informix 클라이언트 SDK 설치 디렉터리로 설정해야 합니다.
-  **INFORMIXSERVER**:
   기본 Informix 서버 이름입니다.
-  **DB_LOCALE**:
   Informix 데이터베이스의 로케일입니다.
-  **CLIENT_LOCALE**:
   클라이언트 로케일입니다.
-  **IDB_OGR_FID**:
   'ogc_fid' 대신 사용할 기본 키의 이름을 설정합니다.

Informix 변수에 관해 더 많은 정보를 알고 싶다면 Informix 클라이언트 SDK 문서를 읽어보십시오.

예시
-------

다음 예시는 ogrinfo를 사용해서 다른 호스트에 있는 Informix DataBlade 레이어를 목록화하는 방법을 보여줍니다:

::

   ogrinfo -ro IDB:"server=demo_on user=informix dbname=frames"

