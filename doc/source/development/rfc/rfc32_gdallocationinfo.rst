.. _rfc-32:

================================================================================
RFC 32: gdallocationinfo 유틸리티
================================================================================

저자: 프랑크 바르메르담

연락처: warmerdam@pobox.com

상태: 승인

요약
----

이 RFC는 래스터에 있는 어느 위치(픽셀)에 관한 상세 정보를 리포트하는 GDAL 용 새 표준 명령줄 유틸리티를 추가할 것을 제안합니다.

근거
----

1. 특정 픽셀/위치에 대한 요청을 만족시키기 위해 사용되는 VRT 파일을 식별할 수 있었으면 하는 사용자 요구 사항이 있습니다.

2. 많은 사용자들이 해당 이미지의 좌표계와는 다른 좌표계로 표현된 어느 위치의 값을 찾을 수 있는 도구를 자주 요청했습니다. 예를 들자면 "지정한 위도/경도 위치의 표고는?" 같은 질문들이 많았습니다.

gdallocationinfo 유틸리티의 목적은 바라건대 "래스터 포인트 쿼리" 도구 같은 일반적인 가치를 가질 수 있는 방식으로 이 두 가지 요구 사항에 답하는 것입니다.

gdallocationinfo
----------------

:ref:`gdallocationinfo` 페이지에서 완전한 문서를 볼 수 있습니다.

::

   사용례: gdallocationinfo [--help-general] [-xml] [-lifonly] [-valonlyl]
                            [-b band]* [-l_srs srs_def] [-geoloc] [-wgs84]
                            srcfile x y

이 유틸리티의 주요 측면은 지정 위치의 좌표계를 제어('-s_srs', '-geoloc', '-wgs84')하고 산출 포맷을 다양하게 제어('-xml', '-lifonly', '-valonly')하는 것입니다. 다음은 완전한 XML 포맷 산출물의 예시입니다:

::

   $ gdallocationinfo -xml -wgs84 utm.vrt -117.5 33.75
   <Report pixel="217" line="282">
     <BandReport band="1">
       <LocationInfo>
         <File>utm.tif</File>
       </LocationInfo>
       <Value>16</Value>
     </BandReport>
   </Report>

LocationInfo 메타데이터 도메인
------------------------------

gdallocationinfo 유틸리티에 작성된 픽셀값 및 위치 변환 로직을 더 손 볼 필요는 없습니다. 좀 더 실험적인 부분은 데이터소스로부터 쿼리한 "LocationInfo"를 리포트하는 부분입니다.

직접적인 요구 사항은 :cpp:class:`VRTSourcedRasterBand` 클래스가 대상 픽셀과 중첩하는 파일(들)에 대한 정보를 반환하도록 하는 것입니다. 그러나 이론적으로 서로 다른 드라이버들이 한 위치에 관해 서로 다른 종류의 정보를 반환할 수도 있습니다. 예를 들면 WMS 드라이버는 지정 위치에 대해 GetFeatureInfo를 호출해서 그 결과값을 반환할 수도 있습니다.

데이터소스를 쿼리하는 메커니즘은 대상 밴드(들)의 "LocationInfo" 도메인을 대상으로 하는 GetMetadataItem() 요청으로 특별히 명명되었습니다. 다음 예시의 요청 항목 이름은 "Pixel_x_y" 형식이며 이때 x 및 y가 각각 쿼리하는 픽셀 및 픽셀의 줄입니다.

이 항목으로부터 반환되는 값은 NULL 또는 "" 루트 요소를 가진 XML 문서 가운데 하나여야 합니다. 이 문서가 제대로 구성된 XML인 이상, 문서의 내용은 따로 정의되지 않습니다. VRT 드라이버는 해당 위치에 있는 각 파일에 대해 일련의 xxx 항목들을 반환합니다.

예를 들어 다음 호출은:

::

       GDALGetMetadataItem( hBand, "Pixel_100_200", "LocationInfo" );

다음과 같은 내용을 반환할 수도 있습니다:

::

       <LocationInfo>
         <File>utm.tif</File>
       </LocationInfo>

테스트 스위트
-------------

GDAL 유틸리티 스위트에 새 테스트를 도입하고, 유틸리티 및 VRT 습성에 대한 :file:`gdrivers/vrt.py` 스크립트를 각각 도입할 것입니다.

문서화
-------------

이 유틸리티를 위한 문서를 이미 준비했으며 앞에서 참조했습니다.

구현
--------------

GDAL 트렁크에 이미 구현을 완료했습니다. RFC 개정 때문에 필요한 경우 프랑크 바르메르담이 수정할 수 있습니다.

