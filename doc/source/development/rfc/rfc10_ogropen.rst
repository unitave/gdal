.. _rfc-10:

================================================================================
RFC 10: OGR 열기 파라미터 (미구현)
================================================================================

저자: 안드레이 키셀레프

연락처: dron@ak4719.spb.edu

상태: 개발 중, 구현되지 '않음'

요약
----

:cpp:func:`OGRSFDriver::Open` 및 :cpp:func:`OGRSFDriverRegistrar::Open` 호출을 호출자가 지정하는 임의의 추가 파라미터들을 담고 있는 추가적인 파라미터를 입력받을 수 있도록 변경해야 한다고 제안합니다. 이 새 기능을 C 인터페이스로 매핑하도록 :cpp:func:`OGROpenEx` 함수를 도입할 것입니다. 뿐만 아니라 :cpp:func:`OGRSFDriverRegistrar::Open` 호출이 :cpp:func:`OGRSFDriverRegistrar::OpenShared` 메소드를 사용하지 않도록 "update" 플래그를 추가할 것을 제안합니다.

열기 파라미터
-------------

OGR 드라이버에 열어야 할 데이터셋 이름과 함께 추가적인 정보를 전송해야 할 경우가 있습니다. 예를 들어 스타일 테이블 이름 (몇몇 드라이버는 스타일 테이블 여러 개 가운데 하나를 선택할 수 있습니다) 또는 다른 어떤 추가 데이터라도 전송해야 할 수 있습니다. 이를 위한 예전 방법은 데이터셋 이름 문자열에 추가 정보를 인코딩해 넣는 것이었습니다. 이런 방법은 불편한 접근법이기 때문에, :cpp:func:`OGRDataSource::CreateLayer` 호출에 구현된 것과 동일하게 :cpp:func:`OGRSFDriver::Open` 및 :cpp:func:`OGRSFDriverRegistrar::Open` 호출에 열기 옵션을 표현하는 개별 파라미터를 사용할 것을 제안합니다.

열기 옵션을 문자열 목록을 구성하는 NAME=VALUE 쌍들의 형식으로 지정한다고 가정합니다.

:cpp:func:`OGRSFDriverRegistrar::Open` 호출에 옵션 파라미터뿐만 아니라 특수 "shared" 플래그도 추가할 것이기 때문에, 개별 :cpp:func:`OGRSFDriverRegistrar::OpenShared` 메소드는 필요없을 것입니다.

구현
----

모든 :cpp:func:`Open` 함수를 다음과 같이 변경할 것입니다:

::

   static OGRDataSource *
   OGRSFDriverRegistrar::Open( const char * pszName, int bUpdate,
                               OGRSFDriver ** ppoDriver,
                   int bShared = FALSE,
                   char **papszOptions = NULL );


::

   OGRDataSource *
   OGRSFDriverRegistrar::OpenShared( const char * pszName, int bUpdate,
                                     OGRSFDriver ** ppoDriver )
       { return Open( pszName, bUpdate, ppoDriver, TRUE, NULL ); }

::

   virtual OGRDataSource
   OGRSFDriver::*Open( const char *pszName, int bUpdate=FALSE,
                       char **papszOptions = NULL ) = 0;

모든 OGR 드라이버에 마지막 변경 사항을 적용해야 합니다. 변경 사항 자체는 매우 단순합니다: 함수 정의에 추가 파라미터 하나를 추가해야 합니다. 그러나 제3자 OGR 드라이버에 영향을 미칩니다: 제3자 드라이버가 더 이상 소스 호환되지 않기 때문에 역시 변경해야 합니다.

또 알맞은 C 함수도 추가할 것입니다:

::

   OGRDataSourceH OGROpenEx( const char *pszName, int bUpdate,
                             OGRSFDriverH *pahDriverList,
                 int bShared, char **papszOptions );

::

   OGRDataSourceH OGR_Dr_OpenEx( OGRSFDriverH hDriver, const char *pszName, 
                                 int bUpdate, char **papszOptions );

OGR 유틸리티 용 새 옵션들
-------------------------

ogr2ogr 및 ogrinfo 유틸리티에서 '-doo NAME=VALUE' ("데이터소스 열기 옵션") 포맷 특화 파라미터를 통해 제안 기능을 사용할 수 있을 것입니다.

하위 호환성
-----------

제안 추가 사항들은 C 바이너리 호환성에 아무 영향도 미치지 않을 것입니다. C++ 바이너리 인터페이스는 망가질 것이고, 소스 수준 호환성은 제3자 OGR 드라이버에 대해서만 망가질 것입니다. 소스 수준에서는 고급 응용 프로그램에 아무 영향도 미치지 않을 것입니다.

책임자 및 작업 시간표
---------------------

안드레이 키셀레프가 이 제안을 구현할 책임을 집니다. GDAL 1.5.0버전에서 새 API를 사용할 수 있을 것입니다.

