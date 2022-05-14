.. _rfc-18:

================================================================================
RFC 18: C API에서의 OGR 스타일 지원
================================================================================

저자: 대니얼 모리셋(Daniel Morissette)

연락처: dmorissette@mapgears.com

상태: 승인 (2007년 12월 5일)

요약
----

OGR는 스타일 정보의 인코딩을 처리해서 피처에 추가하는 C++ 클래스 여러 개를 가지고 있습니다. 더 자세한 정보는 :ref:`ogr_feature_style` 문서에서 찾아볼 수 있습니다.

GDAL/OGR 1.4.x 이전 버전에서는 C API를 이용해서 스타일 정보를 처리할 수 없었습니다. 이 RFC는 GDAL/OGR 1.5버전에서 C API에 스타일 정보를 처리할 수 있는 함수들을 추가할 것을 제안합니다.

구현 상세 사항
--------------

-  다음 목록을 :file:`ogr_featurestyle.h` 로부터 :file:`ogr_core.h` 로 이동시킵니다:

::

       OGRSTClassId;
       OGRSTUnitId;
       OGRSTPenParam;
       OGRSTBrushParam;
       OGRSTSymbolParam;
       OGRSTLabelParam;

-  C API에 (:cpp:class:`OGRStyleMgr` C++ 클래스에 대응하는) :c:class:`OGRStyleMgrH` 클래스를 추가할 것입니다:

::

       OGRStyleMgrH  OGR_SM_Create()
       void          OGR_SM_Destroy(OGRStyleMgrH hSM)

       const char   *OGR_SM_InitFromFeature(OGRStyleMgrH hSM)
       int           OGR_SM_InitFromStyleString(const char *pszStyleString)
       int           OGR_SM_GetPartCount(OGRStyleMgrH hSM)
       OGRStyleToolH OGR_SM_GetPart(OGRStyleMgrH hSM)
       int           OGR_SM_AddPart(OGRStyleMgrH hSM, OGRStyleTool *sPart)

-  C API에 (:cpp:class:`OGRStyleTool` C++ 클래스에 대응하는) :c:class:`OGRStyleToolH` 클래스를 추가할 것입니다:

::

        OGRStyleToolH OGR_ST_Create(OGRSTClassId eClassId)
        void          OGR_ST_Destroy(OGRStyleToolH hST)
        OGRSTClassId  OGR_ST_GetType(OGRStyleToolH hST)

        OGRSTUnitId   OGR_ST_GetUnit(OGRStyleToolH hST)
        void          OGR_ST_SetUnit(OGRStyleToolH hST, OGRSTUnitId eUnit, double dfGroundPaperScale)

        int           OGR_ST_GetParamIsNull(OGRStyleToolH hST, int eParam)
        const char   *OGR_ST_GetParamStr(OGRStyleToolH hST, int eParam)
        int           OGR_ST_GetParamNum(OGRStyleToolH hST, int eParam)
        double        OGR_ST_GetParamDbl(OGRStyleToolH hST, int eParam)
        void          OGR_ST_SetParamStr(OGRStyleToolH hST, int eParam, const char *pszParamString)
        void          OGR_ST_SetParamNum(OGRStyleToolH hST, int eParam, int nParam)
        void          OGR_ST_SetParamDbl(OGRStyleToolH hST, int eParam, double dfParam)
        const char   *OGR_ST_GetStyleString(OGRStyleToolH hST)

        int           OGR_ST_GetRGBFromString(OGRStyleToolH hST, const char *pszColor, 
                                             int *nRed, int *nGreen, int *nBlue, int *nAlpha);

주의: 구현 시 C++ 메소드들에 더 근접하게 매핑하기 위해 모든 :c:func:`OGR_ST_GetParam...` 함수들 상에서 :c:func:`OGR_ST_GetParamIsNull` 을 제거하고 'int \*bValueIsNull' 인자로 대체했습니다.

-  앞의 :c:func:`OGR_ST_*` 래퍼(wrapper)들이 내부적으로 처리하는 다음 C++ 클래스들에 대한 래퍼는 필요없습니다:

::

       class OGRStylePen : public OGRStyleTool
       class OGRStyleBrush : public OGRStyleTool
       class OGRStyleSymbol : public OGRStyleTool
       class OGRStyleLabel : public OGRStyleTool

-  :file:`ogr_featurestyle.h` 파일이 :c:class:`OGRSTVectorParam` 목록 및 대응하는 :cpp:class:`OGRStyleVector` 클래스도 담고 있지만 이 클래스는 현재 사용되지 않기 때문에 향후 제거될 수도 있습니다. 따라서 C API에 :cpp:class:`OGRStyleVector` 클래스를 위한 지원을 구현하지 않을 것입니다. (또한 :c:class:`OGRSTVectorParam` 목록을 :file:`ogr_core.h` 로 이동시키지 않을 것입니다.)

파이썬 및 기타 언어 바인딩
--------------------------

이 초기 구현은 C API 전용이므로 파이썬 및 기타 스크립트 작업 언어 바인딩으로 이식 또는 테스트되지 않을 것입니다. 향후 배포판을 기다려야 할 것입니다.

구현
----

대니얼 모리셋이 GDAL/OGR 1.5.0버전 배포판을 위해 C API에 이 RFC에서 설명하는 변경 사항들을 구현할 것입니다.

새 C API 함수들의 첫 번째 테스트는 MapServer의 :file:`mapogr.cpp` 가 새 함수들을 사용하도록 변환하는 것이 될 것입니다.

관련 티켓(들)
-------------

#2061

투표 이력
---------

프로젝트 운영 위원회의 모든 멤버가 +1 투표

-  프랑크 바르메르담
-  대니얼 모리셋
-  하워드 버틀러
-  세케레시 터마시
-  안드레이 키셀레프

