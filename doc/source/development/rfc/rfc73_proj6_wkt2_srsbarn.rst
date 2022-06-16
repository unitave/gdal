.. _rfc-73:

=======================================================================================================
RFC 73: WKT2, 후기 바인딩 케이퍼빌리티, 시간 지원 및 통합 좌표계 데이터베이스를 위한 PROJ6 통합
=======================================================================================================

============ ==========================
저자:        이벤 루올
연락처:      even.rouault@spatialys.com
제안일:      2019년 1월 8일
최신 수정일: 2019년 5월 2일
상태:        승인, GDAL 3.0버전에 구현
============ ==========================

요약
----

이 RFC는 GDAL과 PROJ 6버전의 통합과 관련된 작업을 설명합니다. 이 통합으로 다음과 같은 케이퍼빌리티가 추가됩니다:

-  좌표계 WKT 2 지원
-  좌표계들 간의 좌표 변환을 위한 "후기 바인딩(late binding)" 케이퍼빌리티
-  좌표 작업을 위한 시간 차원 지원
-  통합 좌표계 데이터베이스 사용

동기
----

이 RFC를 제안하게 된 동기는 `https://gdalbarn.com/#why <https://gdalbarn.com/#why>`_ 에서 설명하고 있습니다. 그 내용을 발췌했습니다.

GDAL, PROJ, 및 libgeotiff의 좌표계는 현대적인 케이퍼빌리티를 누락하고 있기 때문에 철저한 리팩토링(refactoring)이 필요합니다:

-  PROJ_LIB 및 GDAL_DATA의 꺼려지는 즉석(ad hoc) CSV 데이터베이스는 사용자가 짜증을 내게 하고, 개발자에게는 문제를 일으키며, 좌표계 정의를 상호 운용하는 것을 방해합니다.

-  GDAL과 PROJ는 OGC WKT 2를 지원하지 않습니다.

-  PROJ 5.0 이상 버전은 더 이상 WGS84에서 최대 2미터까지 오류가 날 수도 있는 원점 변환 회전(datum transformation pivot)을 요구하지 않습니다. 그러나 다른 도구들이 이 이점을 취하지 않습니다.

CSV 데이터베이스
~~~~~~~~~~~~~~~~

EPSG 및 다른 좌표계 정의에 대해 SQLite 기반 데이터베이스를 사용하면 프로젝트에 더 많은 케이퍼빌리티(영역 인식 검증)를 추가할 수 있고, 프로젝트의 사용자 지정 고유 데이터 구조를 좀 더 보편적으로 사용할 수 있는 데이터 구조로 전환할 수 있으며, 소프트웨어 도구들이 다루는 수많은 좌표계들 간에 좌표계 정의 상호 운용성을 촉진할 수 있습니다.

WKT2
~~~~

`OGC WKT2 <https://docs.opengeospatial.org/is/12-063r5/12-063r5.html>`_ 가 오래 이어져 왔던 좌표계 정의 상호 운용성 불일치를 수정합니다. WKT 2는 시간 종속 좌표계를 설명하기 위한 도구를 담고 있습니다. PROJ 5 이상 버전은 이제 시간 종속 변환을 할 수 있지만, GDAL 및 다른 도구들이 아직 지원하지 않습니다.

몇몇 국가들이 국가 측지 인프라스트럭처가 시간 종속 좌표계를 포함시키도록 업데이트하고 있습니다. 예를 들면 호주와 미국이 각각 2020년과 2022년에 시간 종속 좌표계로 전환할 예정입니다. 북미에서 널리 쓰이던 NAD83 및 NAVD88을 NATRF2022 및 NAPGD2022로 대체하는 중이며, 산업계도 빠르건 늦건 이런 문제에 적응해 나가야 할 것입니다.

WGS84 회전
~~~~~~~~~~

예전 PROJ는 WGS84에서 파라미터 7개를 사용해서 회전(pivot)시키는 원점 변환을 요구했습니다. 이 회전은 실용적인 해결책이지만 약 2미터에 달하는 오류를 낼 수 있고, 또 수많은 레거시 원점들을 WGS84로 정의할 수 없기도 합니다. PROJ 5.0 이상 버전은 `변환 파이프라인 프레임워크 <https://proj.org/usage/transformation.html#geodetic-transformation>`_ 를 통해 후기 바인딩을 지원하는 도구들을 제공하지만, GDAL과 다른 도구들은 아직 이 프레임워크를 사용하지 못 합니다. 정확도가 더 높은 새로운 변환은 WGS84를 거치지 않으며, 지역 측지 기관의 사이드카 데이터를 사용해서 추가 변환 단계를 없앱니다.

다른 라이브러리에서의 관련 작업
-------------------------------

이 RFC는 "`gdalbarn <https://gdalbarn.com/>`_" 작업의 마지막 단계입니다. 예전 단계들은 `PROJ RFC 2 <https://proj.org/community/rfc/rfc-2.html>`_ 에 따라 PROJ 마스터 저장소에 관련 변경 사항들을 구현하고 `libgeotiff 풀 요청 2번 <https://github.com/OSGeo/libgeotiff/pull/2>`_ 에 따라 libgeotiff 마스터 저장소에 관련 변경 사항들을 구현하는 단계들이었습니다.

제안
----

제3자 라이브러리 요구 사항
~~~~~~~~~~~~~~~~~~~~~~~~~~

GDAL 마스터(향후 3.0버전)를 빌드하고 실행하려면 PROJ 마스터(향후 PROJ 6.0버전)와 libgeotiff 마스터(향후 libgeotiff 1.5 또는 2.0버전)가 필요할 것입니다.

PROJ와 관련해서, GDAL 마스터에 어떤 PROJ 내부 복사본도 내장시키지 않을 것입니다. PROJ 예전 버전들을 지원하는 것은 불가능합니다. GDAL로부터 PROJ로 완전히 옮겨진 다음 기능들의 이점을 이용하기 위해 :cpp:class:`OGRSpatialReference` 클래스를 상당 부분 재작성했기 때문입니다:

-  PROJ 문자열 가져오기 및 내보내기
-  WKT 문자열 가져오기 및 내보내기
-  EPSG 데이터베이스 이용

일부 GDAL 의존성이 시스템이 제공하는 libproj를 이용하는데 PROJ 마스터와 이 예전 libproj를 아무 생각 없이 혼합해서 런타임 크래시가 발생하는 복잡한 설정(setup)에서 GDAL 마스터와 PROJ 마스터를 좀 더 쉽게 이용하려면, PROJ 마스터의 공개 심볼의 별명을 지정하는 ``CFLAGS/CXXFLAGS=-DPROJ_RENAME_SYMBOLS`` 를 이용해서 PROJ를 빌드하면 됩니다. 이렇게 하면 GDAL이 이 사용자 지정 빌드를 사용할 수 있을 것입니다.
이 방법은 장기적으로 사용하기 위한 해결책이 아니라는 사실을 기억하십시오. 제대로 된 패키지 작업 솔루션은 결국 PROJ 6를 사용해서 모든 역 의존성을 재작성할 것이기 때문입니다. 환경설정 또는 nmake 시 PROJ가 필요하다는 사실도 기억해둬야 합니다. 런타임 시 dlopen() / LoadLibrary()를 통한 동적 불러오기를 더 이상 사용할 수 없기 때문입니다.

libgeotiff와 관련해서, :file:`frmts/gtiff/libgeotiff` 에 있는 복사본을 업스트림 libgeotiff 마스터의 내용으로 새로고침했습니다.

모든 지속적 통합(Continuous Integration) 시스템이 (Travis-CI 및 AppVeyor가) GDAL 빌드의 일부분으로 PROJ 마스터를 빌드하도록 업데이트했습니다.

OGRSpatialReference 재작성
~~~~~~~~~~~~~~~~~~~~~~~~~~

GDAL/OGR에서는 :cpp:class:`OGRSpatialReference` 클래스가 모든 좌표계 조작을 관장합니다. GDAL 2.4버전까지, 이 클래스는 주로 WKT 1 표현의 OGR_SRSNode 루트 노드를 담고 있었으며 모든 게터(getter)와 세터(setter)가 이 트리 표현을 조작했습니다. 이 RFC의 일부분으로서, :cpp:class:`OGRSpatialReference` 가 내부적으로 담고 있는 주요 객체가 이제 PROJ PJ 객체이며, 메소드는 이 PJ 객체 상에서 PROJ C API 게터 및 세터를 호출합니다. 이는 (``*``)가 대부분 표현 독립적일 수 있게 해줍니다.

WKT1, WKT2, ESRI WKT, PROJ 문자열 가져오기 및 내보내기는 이제 PROJ로 위임됩니다. 이제 proj.db SQLite 데이터베이스에 의존하는 EPSG 데이터베이스로부터 좌표계 가져오기에 대해서도 마찬가지입니다. 결과적으로 GDAL로부터 좌표계 관련 정보를 담고 있던 모든 :file:`data/*.csv` 파일을 제거했습니다. 이제 WKT를 가져올 때 ESRI WKT로부터의 "모핑(morphing)"을 자동으로 수행합니다.

IsSame() 또는 FindMatches() 같은 메소드들의 일반 의미 체계는 그대로 유지되지만, 하부 구현은 상당히 다르기 때문에 동일한 상황에서 예전 GDAL 버전들과는 다른 결과를 낼 수 있습니다. FindMatches() 메소드의 경우  데이터베이스에서의 쿼리 케이퍼빌리티가 개선되었기 때문에 일반적으로 EPSG 항목들에 대한 좌표계 식별은 향상됩니다.

*  코드의 모든 위치에서 이렇게 재작성하는 일은 실용적이지 않았기 때문에 "대부분의" 정밀도는 이 클래스 안에 있습니다. 즉 일부 메소드의 경우, 내부적으로 계속 WKT 1 내보내기를 실행합니다. ("GEOGCS|UNIT" 같은) 공간 좌표계 노드를 가리키는 경로를 인자로서 받는 메소드, 또는 OGC WKT 1 특화 이름을 예상하는 SetProjection(), GetProjParm() 같은 일부 메소드가 이에 해당합니다. 주로 드라이버들이 이런 이름을 사용한다고 생각됩니다. OGC WKT 1 이름을 EPSG 이름으로 바꾸면 여러 드라이버에 영향을 미칠 것입니다. 이 가운데 몇몇 드라이버는 공간 좌표계 지원이라는 측면에서 거의 테스트되지 않았는데, 따라서 주로 WKT 1 표현만 지원합니다.

OGRCoordinateTransformation 변경 사항
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

GDAL 2.3버전에서 PROJ 5를 처음 지원한 후로, 두 좌표계 간에 변환하는 경우 좌표 작업 파이프라인을 생성하기 위해 여전히 소스 및 대상 좌표계의 PROJ.4 문자열 내보내기에 의존하고 있었습니다. 즉 'towgs84' 또는 'nadgrids' PROJ 키워드를 통해 WGS84 회전을 사용하는 "초기 바인딩(early binding)"에 제한되어 있었습니다. 이제 두 좌표계 사이에서 적절한 좌표 작업을 찾을 수 있는 새로운 PROJ 케이퍼빌리티를 사용하기 때문에 "후기 바인딩" 케이퍼빌리티가 WGS84 또는 사용 영역(area of use) 이외의 다른 회전을 연산에 넣을 수 있습니다.

OGRCreateCoordinateOperation()이 이제 옵션들을 정의하기 위한 선택적인 추가 인자를 받습니다.

이런 옵션 가운데 하나는 후보 작업을 검색하는 경우 연산에 넣을 관심 영역(area of interest)을 정의합니다. 여러 작업이 일치하는 경우, (PROJ 정렬 기준에 따라) "최적(best)" 작업을 선택할 것입니다.
주의: 이후 Transform() 호출이 처음 관심 영역 밖에 있는 좌표를 사용하더라도 선택한 최적 작업을 시스템적으로 사용할 것입니다.

또다른 옵션은 적용할 좌표 작업을 지정할 수 있는 기능으로, (일반적으로 ``+proj=pipeline`` 인) PROJ 문자열 또는 WKT 좌표 작업/연쇄 작업 가운데 하나로 GDAL / PROJ가 자동 계산했을 작업을 대체합니다. 사용자들은 일반적으로 source_crs / target_crs 튜플로부터 후보 작업을 반환할 수 있는 새로운 PROJ projinfo 유틸리티를 사용해서 특정 좌표 작업을 선택할 수 있습니다.

어떤 작업도 지정되지 않은 경우, GDAL은 PROJ를 사용해서 모든 좌표 작업 후보들을 목록화할 것입니다. Transform()을 호출할 때마다, 입력 좌표의 평균 좌표를 계산해서 후보 작업들로부터 최적 좌표 작업을 판단하는 데 사용할 것입니다.

좌표 작업이 시간 종속적인 경우 이제 Transform() 메소드가 좌표 시대(coordinate epoch)를 담을 수 있는 추가 인자를 (일반적으로 십진수 연도 값으로) 받습니다. 이와 관련해서, 일반적으로 gdalwarp가 사용하는 :cpp:class:`GDALTransform` 의 변환 옵션들이 이제 동일한 목적으로 COORDINATE_EPOCH를 받아들입니다.

GDAL에서 OGRSpatialReference 사용
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

현재 GDAL 데이터셋은 공간 좌표계를 서술하기 위해 WKT 1 문자열을 받아들이고 반환합니다. 실제 인코딩으로부터 좀 더 독립적이기 위해 그리고 예를 들어 지오패키지 래스터 데이터셋이 WKT 2를 이용할 수 있도록 하기 위해, (WKT 1 또는 WKT 2) 표현에 의존적이지 않은 공간 좌표계를 추가할 수 있는 기능이 필요합니다. 따라서 ``const char*`` 문자열 대신 :cpp:class:`OGRSpatialReference` 객체를 사용하는 편이 좋습니다.

:cpp:class:`GDALDataset` 에 다음 새 메소드들을 추가합니다:

-  ``virtual const OGRSpatialReference* GetSpatialRef() const;``
-  ``virtual CPLErr SetSpatialRef(const OGRSpatialReference*);``
-  ``virtual const OGRSpatialReference* GetGCPSpatialRef() const;``
-  ``virtual CPLErr SetGCPs(int nGCPCount, const GDAL_GCP *pasGCPList, const OGRSpatialReference*);``

전환을 쉽게 하기 위해, :cpp:class:`GDALDataset` 에 다음과 같은 비가상 메소드들을 추가합니다:

-  ``const OGRSpatialReference* GetSpatialRefFromOldGetProjectionRef() const;``
-  ``CPLErr OldSetProjectionFromSetSpatialRef(const OGRSpatialReference* poSRS);``
-  ``const OGRSpatialReference* GetGCPSpatialRefFromOldGetGCPProjection() const;``
-  ``CPLErr OldSetGCPsFromNew( int nGCPCount, const GDAL_GCP *pasGCPList, const OGRSpatialReference * poGCP_SRS );``

그 다음 예전 GetProjectionRef(), SetProjection(), GetGCPProjection() 및 SetGCPs() 앞에 언더바(``_``)를 붙여서 투영 가상 메소드로서 사용할 수 있습니다.

기존 드라이버를 변환하는 이 방법은 드라이버의 GetProjectionRef() 메소드를 \_GetProjectionRef()로 재명명하고 다음을 추가하는 것입니다:

::

   const OGRSpatialReference* GetSpatialRef() const override {
       return GetSpatialRefFromOldGetProjectionRef();
   }

기본 WKT 버전
~~~~~~~~~~~~~

:cpp:func:`OGRSpatialReference::exportToWkt()` 을 옵션 없이 호출하면 이 표현으로 된 호환 가능한 좌표계에 대한 WKT 1을 (명확한 AXIS 노드들과 함께. 다음 "축 순서 문제점" 단락을 참조하십시오) 리포트할 것입니다. 옵션을 지정해서 호출하면 (일반적으로 3차원 지리 좌표계를 위한) WKT2:2018을 사용할 것입니다.

exportToWkt() 개선 버전은 여러 줄 또는 한 줄 산출물을 사용해야만 하는 경우를 포함하는 여러 상황에서 사용하는 WKT의 정확한 버전을 지정하는 옵션을 받아들입니다.

아니면 (exportToWkt()의 옵션으로 어떤 명확한 버전도 전송하지 않은 경우) OSR_WKT_FORMAT 환경설정 옵션을 사용해서 exportToWkt()가 사용하는 WKT 버전을 수정할 수 있습니다.

gdalinfo, ogrinfo 및 gdalsrsinfo 유틸리티는 기본값으로 WKT2:2018을 산출할 것입니다.

축 순서 문제점
~~~~~~~~~~~~~~

축 순서는 반복되는 문제점입니다. 이 RFC는 `RFC 20: OGRSpatialReference 축 지원 <./rfc20_srs_axes>`_ 에 따라 초기에 수행되었던 내용에 대해 (완전히 해결했다는 척을 하지 않고) 새로운 접근법을 제안합니다. 이 문제점은 공식 좌표계 정의가 GIS 응용 프로그램에서 래스터 또는 벡터 데이터가 일반적으로 인코딩되는 방식을 준수하지 않는 축 순서를 사용한다는 것입니다. 전형적인 예시가 바로 EPSG, EPSG:4326의 "WGS 84" 지리 좌표계 정의로, 위도를 첫 번째 축 그리고 경도를 두 번째 축으로 사용합니다. RFC 20은 기관의 축 순서가 GIS 친화적인 순서와 일치하지 않는 경우 기본적으로 WKT로부터 AXIS 정의를 제거할 것을 (그리고 사용자 지정 EPSGA 기관 코드에 공식 AXIS 요소를 가진 WKT를 사용할 것을) 결정했습니다.

AXIS 요소 정의가 WKT 1 문법으로 작성되었기 때문에 이 접근법이 기술적으로 가능했습니다. 하지만 AXIS 정의를 제거한다는 것은 실제로 어떤 축 순서를 사용하는지가 명확하지 않기 때문에 잠재적인 혼란의 이유가 되었습니다. 게다가 WKT 2에서는 AXIS 요소가 필수적이며 내부 PROJ 표현도 좌표계를 정의할 것을 요구합니다. 즉 다음과 같은 두 가지 만족스럽지 않은 선택지가 남게 됩니다:

-  계속 공식 기관 코드를 사용하면서도 GIS 친화적 순서를 가진 공식 축 정의의 패치된 버전을 반환합니다. 소스 코드와의 링크를 유지하고 있기 때문에 실용적인 접근법이지만, 공식 정의를 수정하기 때문에 거짓된 방법이기도 합니다. 사용자는 인코딩된 순서를 신뢰해야 하는지 아니면 기관의 공식 순서를 신뢰해야 하는지 알 수 없게 될 것입니다.

-  공식 기관 코드 없이 GIS 친화적 순서를 가진 공식 축 정의의 패치된 버전을 반환합니다. 이 접근법은 GIS 응용 프로그램에서 래스터 또는 벡터 데이터가 일반적으로 인코딩되는 방식을 준수하지만, 공식 기관 코드와의 링크를 잃게 될 것입니다.

이 RFC에서 지향하는 해결책은 "데이터 축을 공간 좌표계 축에 매핑" 개념을 추가하는 것입니다. 이 접근법은 WCS DescribeCoverage 응답에서 공간 좌표계 축이 어떻게 커버리지의 그리드 축에 매핑되는지 설명하기 위해 수행하는 방식과 조금 비슷합니다.

다음은 EPSG:4326을 사용하는 커버리지에 대한 `GeoServer 문서 <https://docs.geoserver.org/stable/en/user/extensions/wcs20eo/index.html>`_ 에서 발췌한 내용입니다.

::

         <gml:coverageFunction>
           <gml:GridFunction>
             <gml:sequenceRule axisOrder="+2 +1">Linear</gml:sequenceRule>
             <gml:startPoint>0 0</gml:startPoint>
           </gml:GridFunction>
         </gml:coverageFunction>

이와 유사한 매핑을 추가해서 지리변환 행렬 또는 :cpp:class:`OGRGeometry` 에서 'x' 및 'y' 구성요소를 어떻게 좌표 정의가 정의한 축에 매핑하는지 정의합니다.

:cpp:class:`OGRSpatialReference` 의 새로운 메소드가 이런 매핑을 지원합니다.

::

   const std::vector<int>& GetDataAxisToSRSAxisMapping() const

이 메소드의 의미 체계를 설명하려면, 먼저 이 메소드가 2, -1, 3을 반환한다고 생각해보십시오. 이 숫자들은 다음과 같이 해석됩니다:

-  2: 좌표계의 첫 번째 축을 데이터의 두 번째 축에 매핑합니다.
-  -1: 좌표계의 두 번째 축을 데이터의 첫 번째 축에, 축의 값을 음의 값으로 변환해서 매핑합니다.
-  3: 좌표계의 세 번째 축을 데이터의 세 번째 축에 매핑합니다.

이는 `PROJ axisswap 작업 <https://proj.org/operations/conversions/axisswap.html>`_ 과 유사합니다.

기본적으로, :cpp:class:`OGRSpatialReference` 객체를 새로 생성할 때 GetDataAxisToSRSAxisMapping()가 기관이 정의한 축 순서를 준수하는 1,2[,3] 식별 정보를 반환합니다.

모든 GDAL 드라이버와 거의 대부분의 OGR 드라이버가 "GIS 축 매핑" 사용에 의존하기 때문에, ``SetAxisMappingStrategy( OAMS_TRADITIONAL_GIS_ORDER 또는 OAMS_AUTHORITY_COMPLIANT 또는 OAMS_CUSTOM )`` 메소드를 추가해서 드라이버가 쉽게 축 매핑을 지정할 수 있도록 합니다.

OAMS_TRADITIONAL_GIS_ORDER는 다음을 의미합니다:

-  2차원 지리 좌표계의 경우,

   -  (EPSG:4326처럼) Latitude NORTH, Longitude EAST라면 GetDataAxisToSRSAxisMapping()가 {2,1}을 반환합니다. 데이터 축 순서가 경도, 위도라는 뜻입니다.
   -  (OGC:CRS84처럼) Longitude EAST, Latitude NORTH라면 {1,2}를 반환합니다.

-  투영 좌표계의 경우,

   -  (대부분의 투영 좌표계처럼) EAST, NORTH라면 {1,2}를 반환합니다.
   -  NORTH, EAST라면 {2,1}을 반환합니다.
   -  EPSG:5041("WGS 84 / UPS North (E,N)")와 같이 East/SOUTH, North/SOUTH인 북극 좌표계라면 {1,2}를 반환할 것입니다.
   -  EPSG:32661("WGS 84 / UPS North (N,E)")와 같이 northing/SOUTH, easting/SOUTH인 북극 좌표계라면 {2,1}을 반환할 것입니다.
   -  남극 좌표계도 마찬가지입니다.
   -  다른 모든 경우 {1,2}를 반환합니다.

OGRCreateCoordinateTransformation()가 이제 "데이터 축을 공간 좌표계 축에 매핑" 개념을 지원합니다.

주의: 저자가 예전 이메일에 썼던 내용과는 반대로, gdaltransform 유틸리티의 습성은 바뀌지 않습니다. :cpp:class:`GDALTransform` 메커니즘이 내부적으로 GIS 친화적 순서를 강제하기 때문입니다.

래스터 데이터셋이 자신이 반환하는 ``OGRSpatialReference*`` 상에서 ``SetAxisMappingStrategy(OAMS_TRADITIONAL_GIS_ORDER)`` 를 호출하고 SetSpatialRef()에서 이를 가정하도록 수정합니다. (현재 가정만 하고 확인하지는 않습니다.)

벡터 레이어는 주로 GetSpatialRef()가 반환하는 ``OGRSpatialReference*`` 상에서 ``SetAxisMappingStrategy(OAMS_TRADITIONAL_GIS_ORDER)`` 를 호출합니다. GML 드라이버의 경우, 사용자가 INVERT_AXIS_ORDER_IF_LAT_LONG 열기 옵션을 정의한다면 (예전과 마찬가지로) 축 순서 뒤바꾸기를 수행하지 않고 AUTHORITY_COMPLIANT 전략을 사용합니다. ``OGRSpatialReference*`` 를 받을 때 ICreateLayer()가 축 매핑 전략을 변경할 수도 있습니다. (대부분의 경우 변경할 것입니다.) 다시 말해 GML 드라이버가 AUTHORITY_COMPLIANT 순서를 가진 :cpp:class:`OGRSpatialReference` 객체를 받는 경우 TRADITIONAL_GIS_ORDER로 변경하도록 결정할 수도 있으며 :cpp:func:`GetSpatialRef::GetDataAxisToSRSAxisMapping` 이 이를 반영할 것입니다. 이런 경우 ogr2ogr가 도형 축 순서 뒤바꾸기를 수행하도록 수정합니다.

이 변경 사항과 관련해서 WKT 1 내보내기는 이제 항상 AXIS 요소를 반환하고, 따라서 EPSG:xxxx는 EPSGA:xxxx와 동일하게 동작합니다.

즉 이 접근법을 요약하자면: 공간 좌표계 공식 정의에서 축 순서를 더 이상 훼손하지 않지만, 실제로 공간 좌표계 정의와 일치하게 만드는 방법을 설명할 수 있는 추가적인 인터페이스를 추가합니다.

드라이버 변경 사항
~~~~~~~~~~~~~~~~~~

대부분의 경우 호환성 레이어를 사용해서, GetProjectionRef(), SetProjection(), GetGCPProjection() 및 SetGCPs() 메소드들을 통해 공간 좌표계를 WKT 문자열로 반환하는/받아들이는 래스터 드라이버들이 새 가상 메소드들을 이용하도록 업그레이드했습니다.

:cpp:class:`GDALPamDataset` (PAM .aux.xml 파일) 및 GDAL VRT 드라이버가 새 인터페이스를 지원하고 데이터 축을 공간 좌표계 축에 매핑한 값들을 직렬화(serialize)/직렬화 해제(deserialize)하도록 완전히 업그레이드했습니다.

지오패키지 드라이버가 이제 'gpkg_spatial_ref_sys' 테이블에 WKT 2 문자열 정의를 저장하기 위해 사용되는 공식 "gpkg_crs_wkt" 확장 사양을 완전하게 지원합니다. 이 드라이버는 공간 좌표계를 WKT 1 문자열로 인코딩할 수 있는 경우 이 확장 사양을 사용하지 않으려 시도하고, WKT 2를 필요로 하는 공간 좌표계(일반적으로 3차원 지리 좌표계)가 삽입되는 경우 자동적으로 기존 'gpkg_spatial_ref_sys' 테이블에 "definition_12_063" 열을 추가할 것입니다.

유틸리티 변경 사항
~~~~~~~~~~~~~~~~~~

-  gdalinfo 및 ogrinfo가 좌표계를 리포트할 때마다 "데이터 축을 좌표계 축에 매핑"을 리포트합니다. "-wkt_format wkt1"을 지정하지 않는 이상 이 두 유틸리티는 기본적으로 WKT2_2018로도 출력할 것입니다.

::

   Driver: GTiff/GeoTIFF
   Files: out.tif
   Size is 20, 20
   Coordinate System is:
   GEOGCRS["WGS 84",
       DATUM["World Geodetic System 1984",
           ELLIPSOID["WGS 84",6378137,298.257223563,
               LENGTHUNIT["metre",1]]],
       PRIMEM["Greenwich",0,
           ANGLEUNIT["degree",0.0174532925199433]],
       CS[ellipsoidal,2],
           AXIS["geodetic latitude (Lat)",north,
               ORDER[1],
               ANGLEUNIT["degree",0.0174532925199433]],
           AXIS["geodetic longitude (Lon)",east,
               ORDER[2],
               ANGLEUNIT["degree",0.0174532925199433]],
       USAGE[
           SCOPE["unknown"],
           AREA["World"],
           BBOX[-90,-180,90,180]],
       ID["EPSG",4326]]
   Data axis to CRS axis mapping: 2,1 <-- here
   Origin = (2.000000000000000,49.000000000000000)
   Pixel Size = (0.100000000000000,-0.100000000000000)

-  gdalwarp, ogr2ogr 및 gdaltransform에 고급 사용자가 앞의 "OGRCoordinateTransformation 변경 사항" 단락에서 설명한 대로 (일반적으로 ``+proj=pipeline`` 인) PROJ 문자열 또는 WKT 좌표 작업/연쇄 작업 가운데 하나로 좌표 작업을 지정하기 위해 사용할 수 있는 "-ct" 스위치를 추가합니다.
   주의: 기저 래스터/벡터 드라이버가 "GIS 친화적인" 축 순서를 사용하더라도 파이프라인은 좌표계의 축 순서를 고려해야만 합니다. 예를 들어 EPSG:4326로부터 EPSG:32631로 변환하는 경우 ``+proj=pipeline +step +proj=axisswap +order=2,1 +step +proj=unitconvert +xy_in=deg +xy_out=rad +step +proj=utm +zone=31 +ellps=WGS84`` 를 사용해야 합니다.

-  gdalsrsinfo가 WKT2_2015 및 WKT2_2018 2개의 새로 지원하는 WKT 변이형을 지정할 수 있도록 개선합니다. 기본값은 WKT2_2018로 출력하는 것입니다.

SWIG 바인딩 변경 사항
~~~~~~~~~~~~~~~~~~~~~

SWIG 바인딩을 통해 개선된 ExportToWkt() 및 OGRCoordinateTransformation() 메소드를 사용할 수 있습니다.
파이썬이 아닌 언어의 경우 (특히 4차원 X, Y, Z, 시간 좌표를 지원하기 위해) 추가적인 유형 매핑이 필요할 수도 있습니다.

하위 호환성
-----------

이 작업의 의도는 '대부분' 하위 호환성을 확보하려는 것이지만, 그래도 어쩔 수 없는 차이점이 나타날 것입니다. 예를 들면 PROJ에 WKT 1 및 PROJ 문자열 내보내기를 완전히 재작성했기 때문에, GDAL 2.4 이전 버전들이 생성하는 내용과 일치하기를 바라지만 엄격하게 동일하지는 않습니다: 유효 숫자(significant digit)의 개수, PROJ 파라미터들의 순서, 반올림, ...

몇몇 차이점을 반영시키기 위해 :file:`MIGRATION_GUIDE.TXT` 를 업데이트했습니다:

-  OSRImportFromEPSG()가 공식 축 순서를 연산에 넣습니다.

-  OPTGetProjectionMethods(), OPTGetParameterList() 및 OPTGetParameterInfo()를 제거합니다. 동등한 메소드는 없습니다.

-  OSRFixup() 및 OSRFixupOrdering()을 제거합니다:
   객체 구조가 항상 무결하기 때문에 더 이상 필요하지 않습니다.

-  OSRStripCTParms()를 제거합니다:
   대신 OSRExportToWktEx()를 FORMAT=SQSQL 옵션으로 사용합니다.

-  exportToWkt()가 AXIS 노드를 산출합니다.

-  OSRIsSame():
   OSRIsSameEx()에 IGNORE_DATA_AXIS_TO_SRS_AXIS_MAPPING=YES 옵션을 설정하지 않는 이상 이제 "데이터 축을 좌표계 축에 매핑"을 연산에 넣습니다.

-  :file:`ogr_srs_api.h`:
   AXIS가 없는 WKT가 너무 모호하기 때문에 더 이상 SRS_WKT_WGS84 매크로를 기본적으로 선언하지 않습니다. 개선 사항으로 SRS_WKT_WGS84_LAT_LONG을 사용할 것을 추천합니다. 또는 ``#include <ogr_srs_api.h>`` 앞에 ``#define USE_DEPRECATED_SRS_WKT_WGS84`` 를 삽입하십시오.

새로운 GetSpatialRef(), SetSpatialRef(), GetGCPSpatialRef() 및 SetGCPs(..., const OGRSpatialReference* poSRS) 가상 메소드들의 도입과 이 새 메소드들에 대응했던, ``OGRSpatialReference*`` 인스턴스 대신 WKT 문자열을 사용했던 예전 메소드들을 제거했기 때문에 트리 외부에 있는 래스터 드라이버들이 영향을 받을 것입니다.

문서화
------

새로운 메소드들을 문서화했으며, 개발 도중 적절한 경우 기존 메소드들의 문서도 변경했습니다. 그렇기는 하지만 좀 더 철저하게 훑어봐야 할 것입니다. 예제도 업데이트해야 할 것입니다.

테스트
------

여러 가지 이유로 (WKT로 AXIS 노드 내보내기, WKT와 PROJ 문자열 생성의 차이점 등등) 예상 결과물이 달라졌기 때문에 자동 테스트 스위트를 여러 군데 수정했습니다. 새 케이퍼빌리티에 대한 새로운 테스트도 추가했습니다.

자동 테스트가 반드시 모든 것을 확인하는 것은 아니며, 수동 테스트를 통해 여러 문제점들을 발견하고 수정했다는 사실을 기억해야 할 것입니다. "데이터 축을 좌표계 축에 매핑" 개념의 도입도 상당히 오류가 발생하기 쉽습니다. 서로 다른 여러 위치에 OAMS_TRADITIONAL_GIS_ORDER 전략을 설정해야 하기 때문입니다.

따라서 이 작업이 마스터에 들어가고 나면 사용자 및 개발자가 GDAL을 철저하게 테스트해볼 것을 권장합니다.

구현
----

이벤 루올(`Spatialys <http://www.spatialys.com>`_)이 `gdalbarn <https://gdalbarn.com/>`_ 의 후원을 받아 이 RFC를 구현했습니다.

제안한 구현은 `풀 요청 1185번 <https://github.com/OSGeo/gdal/pull/1185>`_ 에서 사용할 수 있습니다.

**더 쉬운** 검토를 위해 이 RFC 구현을 여러 차례에 걸쳐 커밋하지만, 마스터에 포함시키기 위한 단일 커밋에서는 아마도 전체 구현을 우겨넣게 될 것입니다. 개발 도중 PROJ 심볼을 재명명했기 때문에 양분성(bisectability)을 망가뜨릴 가능성이 있어 중간 단계를 거치는 경우 전체 구현을 모두 빌드하지 못 할 수도 있기 때문입니다.

투표 이력
---------

-  하워드 버틀러 +1
-  유카 라흐코넨 +1
-  대니얼 모리셋 +1
-  이벤 루올 +1

수정 사항
---------

2019년 5월 2일: GDAL 2.5를 GDAL 3.0으로 변경

