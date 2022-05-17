.. _rfc-29:

================================================================================
RFC 29: OGR 무시 필드 설정
================================================================================

저자: 마르틴 도비아시(Martin Dobiáš)

연락처: wonder.sk@gmail.com

상태: 승인

요약
-------

피처를 가져올 때 성능을 향상시키기 위해, 이 RFC는 OGR에 이어지는 :cpp:func:`GetFeature` / :cpp:func:`GetNextFeature` 호출이 어떤 필드를 요청하지 않을지 알려주는 방법을 제안합니다. 드라이버가 이런 필드를 무시하고 그 값을 NULL로 유지할 것입니다. 이 RFC는 피처 도형 및 스타일을 무시할 수 있는 가능성도 고려합니다.

공통 사용례:

1. 클라이언트가 레이어를 렌더링한다:
   모든 (또는 대부분의) 필드를 무시할 수 있습니다. 도형만 필수입니다.

2. 클라이언트가 속성 테이블을 표시한다:
   모든 필드가 필수이며, 도형을 무시할 수 있습니다.

상세 사항
---------

:cpp:class:`OGRLayer` 클래스에 클라이언트가 어떤 필드를 가져오지 '않을지' 설정할 수 있게 해주는 새 함수를 추가할 것입니다:

.. code-block:: cpp

   virtual OGRErr OGRLayer::SetIgnoredFields( const char **papszFields );

C API에도 동등한 호출을 추가할 것입니다:

.. code-block:: c

   OGRErr CPL_DLL OGR_L_SetIgnoredFields( OGRLayerH, const char **papszFields );

이 함수의 인자는 무시할 필드들의 이름 목록이며, "OGR_GEOMETRY" 및 "OGR_STYLE" 특수 필드 이름들을 각각 피처의 도형 및 스타일 값을 참조하도록 해석할 것입니다. OGR_GEOMETRY, OGR_STYLE, 그리고 향후 추가될 수 있는 몇몇 다른 특수 필드들도 처리할 수 있도록 필드 이름을 전송하는 방식을 선택했습니다. "원하는" 필드를 지정하는 것이 아니라 "무시할" 필드를 지정하도록 결정한 이유는 원하는 필드 목록에 명확하게 목록화되지 않았다는 이유만으로 도형 및 스타일 같은 필드들을 우연히 생략하지 않도록 하기 위해서입니다.

'papszFields'에 NULL을 전송하면 무시할 목록을 정리할 것입니다.

이 메소드가 필드 선택을 지원하지 않는 경우에도 필드 이름들을 모두 분해(resolve)할 수 있는 한 이 메소드는 OGRERR_NONE을 반환할 것입니다.

이 메소드를 지원하는 드라이버는 OLCIgnoreFields ("IgnoreFields") 케이퍼빌리티에 TRUE를 반환할 것입니다.

이 메소드는 :cpp:class:`OGRLayer` 클래스 수준에서 구현될 것입니다. 이 메소드는 필드 색인을 분해해서 어떤 필드를 무시해야 할지를 나타내는 다음 새 멤버 변수들을 설정할 것입니다. :cpp:class:`OGRFeatureDefn` 및 :cpp:class:`OGRFieldDefn` 클래스 안에 플래그들을 저장할 것이며, 다음 가져오기(getter) 함수들로 플래그들을 사용할 수 있습니다:

.. code-block:: cpp

   bool OGRFieldDefn::IsIgnored();
   bool OGRFeatureDefn::IsGeometryIgnored();
   bool OGRFeatureDefn::IsStyleIgnored();

:cpp:class:`OGRLayer` 클래스가 사용하는 설정하기(setter) 함수로 가져오기 멤버 함수를 구현할 것입니다. 클라이언트가 직접 "ignored" 플래그를 설정하는 일은 금지될 것입니다.

드라이버가 특별한 요구 사항을 가지고 있는 경우 드라이버 구현에서 :cpp:func:`SetIgnoredFields` 메소드를 선택적으로 무시할 수 있습니다.

드라이버에 구현
---------------

이 RFC를 지원하려면 드라이버 구현을 조금 조정해야 할 것입니다. 이 추가 사항을 사용하지 않는 드라이버는 그냥 호출자가 요청하지 않는 필드/도형/스타일도 계속 가져올 것입니다.

드라이버 구현에서의 조정은 다음과 같이 보일 것입니다:

.. code-block:: cpp

   if (!poDefn->IsGeometryIgnored())
   {
     // 도형 가져오기
   }
   if (!poDefn->IsStyleIgnored())
   {
     // 스타일 가져오기
   }

   for( int iField = 0; iField < poDefn->GetFieldCount(); iField++ )
   {
     if (poDefn->GetFieldDefn(iField)->IsIgnored())
       continue;

     // 필드 가져오기
   }

호환성
------

이 변경 사항은 하위 호환성을 완전하게 지원합니다. OGR는 기본적으로 계속해서 도형, 스타일 및 모든 필드를 가져올 것입니다. 제안하는 API를 사용하는 응용 프로그램만 새 습성을 경험할 것입니다.

처음에는 일부 (Shapefile 및 기타 몇 개 안 되는) 드라이버들만 이 RFC를 구현할 것입니다. RFC 승인 시 모든 기존 드라이버를 수정해야 할 필요는 없습니다 -- 무시할 필드를 고려하지 않는 드라이버들은 그냥 계속해서 전과 같이 모든 속성을 가져올 것입니다. 드라이버가 이 RFC를 사용하는지 확인하려면, OLCIgnoreFields 케이퍼빌리티를 검사하면 됩니다.

ogr2ogr 명령줄 도구는 요청 필드 목록을 가진 "-select" 인자를 받는 경우 이 RFC를 사용할 것입니다. 지정한 필드 이외의 필드들을 무시할 것입니다.

투표 이력
---------

-  프랑크 바르메르담 +1
-  세케레시 터마시 +1
-  대니얼 모리셋 +0
-  하워드 버틀러 +0
-  이벤 루올 +0

