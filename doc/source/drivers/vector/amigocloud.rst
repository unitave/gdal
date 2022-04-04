.. _vector.amigocloud:

================================================================================
AmigoCloud
================================================================================

.. versionadded:: 2.1.0

.. shortname:: AmigoCloud

.. build_dependencies:: libcurl

이 드라이버는 AmigoCloud API 서비스에 접속할 수 있습니다. AmigoCloud 드라이버를 컴파일하려면 GDAL/OGR를 cURL 지원과 함께 빌드해야만 합니다.

이 드라이버는 읽기 및 쓰기 작업을 지원합니다.

드라이버 케이퍼빌리티
-------------------

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::

데이터셋 이름 문법
-------------------

AmigoCloud 데이터소스를 열기 위한 최소한의 문법은 다음과 같습니다:

.. code-block::

   AmigoCloud:[project_id]

':' 기호 뒤에 선택적인 추가 파라미터를 지정할 수 있습니다. 현재 다음 파라미터를 지원합니다:

-  **datasets=dataset_id1[,dataset_id2, ..]**:
   AmigoCloud 데이터셋 ID 목록입니다. 특정 AmigoCloud 데이터셋에 접근해야 하는 경우 필수입니다.

파라미터 여러 개를 지정하는 경우, 공백으로 구분해야만 합니다.

dataset_id를 하나도 지정하지 않으면, 드라이버가 해당 프로젝트에 사용할 수 있는 데이터셋 목록을 출력할 것입니다.

예를 들어 **"AmigoCloud:1234 datasets"** 라는 명령어를 실행하면 다음과 같은 내용을 출력할 것입니다:

.. code-block::

    List of available datasets for project id: 1234
    | id        | name
    |-----------|-------------------
    | 5551      | points
    | 5552      | lines

환경설정 옵션
---------------------

다음 환경설정 옵션들을 사용할 수 있습니다:

-  **AMIGOCLOUD_API_URL**:
   기본값은 https://app.amigocloud.com/api/v1 입니다.
   또다른 서버를 가리키도록 설정할 수 있습니다.

-  **AMIGOCLOUD_API_KEY**:
   다음 단락을 참조하십시오.

인증
--------------

AmigoCloud 백엔드가 모든 접근 권한을 정의합니다.

AmigoCloud 대시보드 웹 인터페이스에서 발행하는 API 키를 지정하면 인증된 접근을 할 수 있습니다. AMIGOCLOUD_API_KEY 환경설정 옵션으로 API 키를 지정합니다.

도형
--------

OGR 드라이버는 RFC 41에 따라 레이어에서 사용할 수 있는 모든 도형 필드들을 리포트할 것입니다.

필터링
---------

이 드라이버는 :cpp:func:`OGRLayer::SetSpatialFilter` 함수에 설정된 모든 공간 필터를 서버로 포워딩할 것입니다. :cpp:func:`OGRLayer::SetAttributeFilter` 함수에 설정된 속성 필터도 마찬가지입니다.

쓰기 지원
-------------

데이터셋을 생성하고 삭제할 수 있습니다.

데이터소스를 업데이트 모드로 연 경우에만 쓰기 지원이 활성화됩니다.

AmigoCloud 서비스의 작업과 OGR 개념을 다음과 같이 매핑합니다:

- :cpp:func:`OGRFeature::CreateFeature` <==> ``INSERT`` 작업
- :cpp:func:`OGRFeature::SetFeature` <==> ``UPDATE`` 작업
- :cpp:func:`OGRFeature::DeleteFeature` <==> ``DELETE`` 작업
- :cpp:func:`OGRDataSource::CreateLayer` <==> ``CREATE TABLE`` 작업
- :cpp:func:`OGRDataSource::DeleteLayer` <==> ``DROP TABLE`` 작업

:cpp:func:`OGRFeature::CreateFeature` 함수로 새 객체를 삽입할 때 명령어가 성공적으로 실행되었다면, OGR이 반환된 amigo_id(GUID)를 가져와서 그 해시(hash) 값을 OGR FID로 사용할 것입니다.

위 작업들은 기본적으로 OGR API 호출과 동시에 서버에 전송됩니다. 하지만 수많은 클라이언트/서버 교환 때문에 수많은 명령어들이 전송되는 경우, 이 때문에 성능이 저하될 수도 있습니다.

레이어 생성 옵션
----------------------

다음 레이어 생성 옵션들을 사용할 수 있습니다:

-  **OVERWRITE=YES/NO**:
   기존 테이블을 생성할 레이어 이름으로 덮어쓸지 여부를 선택합니다. 기본값은 NO입니다.

-  **GEOMETRY_NULLABLE=YES/NO**:
   도형 열의 값이 NULL일 수 있는지 여부를 선택합니다. 기본값은 YES입니다.

예시
--------

서로 다른 방법으로 AmigoCloud API 토큰을 제공하기:

.. code-block::

    ogrinfo --config AMIGOCLOUD_API_KEY abcdefghijklmnopqrstuvw -al "AmigoCloud:1234 datasets=987"
    ogrinfo -oo AMIGOCLOUD_API_KEY=abcdefghijklmnopqrstuvw -al "AmigoCloud:1234 datasets=987"
    env AMIGOCLOUD_API_KEY=abcdefghijklmnopqrstuvw ogrinfo -al "AmigoCloud:1234 datasets=987"

.. code-block::

    export AMIGOCLOUD_API_KEY=abcdefghijklmnopqrstuvw
    ogrinfo -al "AmigoCloud:1234 datasets=987"

데이터셋 목록을 출력하기:

.. code-block::

    $ ogrinfo -ro "AmigoCloud:1234 datasets"
    List of available datasets for project id: 1234
    | id        | name
    |-----------|-------------------
    | 5551      | points
    | 5552      | lines

데이터셋 목록으로부터 데이터 접근하기:

.. code-block::

    ogrinfo -ro "AmigoCloud:1234 datasets=1234,1235"

shapefile로부터 테이블을 생성하고 채우기:

.. code-block::

    ogr2ogr -f AmigoCloud "AmigoCloud:1234" myshapefile.shp

기존 테이블(dataset_id: 12345)에 shapefile의 데이터를 추가하기:

.. code-block::

    ogr2ogr -f AmigoCloud "AmigoCloud:1234 datasets=12345" myshapefile.shp

또는

.. code-block::

    ogr2ogr -append -f AmigoCloud "AmigoCloud:1234 datasets=12345" myshapefile.shp

기존 테이블(dataset_id: 12345)의 데이터를 shapefile의 데이터로 덮어쓰기:

.. code-block::

    ogr2ogr -append -doo OVERWRITE=YES -f AmigoCloud "AmigoCloud:1234 datasets=12345" myshapefile.shp

기존 데이터셋(dataset_id: 12345)을 삭제하고 shapefile의 데이터로 새 데이터셋을 생성하기:

.. code-block::

    ogr2ogr -overwrite -f AmigoCloud "AmigoCloud:1234 datasets=12345" myshapefile.shp

기존 테이블(dataset_id: 12345)의 데이터를 shapefile의 데이터로 덮어쓰기. "visited_on" 필드의 값이 2017-08-20 이후인 레코드만 필터링합니다.

.. code-block::

    ogr2ogr -append -doo OVERWRITE=YES -f AmigoCloud "AmigoCloud:1234 datasets=12345" -where "visited_on > '2017-08-20'" myshapefile.shp

참고
--------

-  `AmigoCloud API 토큰 관리 <https://www.amigocloud.com/accounts/tokens>`_

-  `AmigoCloud API 탐색기 <https://app.amigocloud.com/api/v1/>`_
