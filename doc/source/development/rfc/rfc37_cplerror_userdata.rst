.. _rfc-37:

=========================================================================
RFC 37: CPLError에서의 사용자 데이터 콜백
=========================================================================

:날짜:  2011년 10월 25일
:저자:  하워드 버틀러
:연락처:  hobu.inc@gmail.com
:상태:  구현
:버전:  GDAL 1.9
:투표:  다음 멤버들이 +1 투표

        -  프랑크 바르메르담
        -  하워드 버틀러
        -  세케레시 터마시
        -  대니얼 모리셋
        -  이벤 루올


개요
----

이 RFC는 CPLErrorHandler 콜백 함수들에 사용자 맥락 데이터를 구현할 것을 제안합니다. 이 구현은 이미 사용 중인 기존 콜백 패턴을 방해하지 않으며, CPLErrorHandler에 완전히 보조적인 기능을 제공합니다.

근거
----

사용자들이 이미 대화형 작업을 제어하는 응용 프로그램 수준 전역(global)으로 오류 처리 함수의 사용자 맥락을 관리할 수 있다고 주장할 수도 있습니다. 기술적으로는 맞는 말이지만, 이 접근법은 라이브러리 사용자들이 엄청나게 복잡한 작업을 하게 만듭니다. 오류 콜백이 사용자 맥락 데이터를 다시 전송하는 시나리오는 GDAL 내부의 오류와 함께 사용자 응용 프로그램의 상태를 반환받기를 원하는 사용자를 위한 더 단순한 코드를 의미합니다.

다음과 같은 경우 콜백이 사용자 데이터를 전송합니다:

-  신호 기반 API의 경우 (CPLErrorHandler가 신호 기반 API 가운데 하나입니다) 일반적인 특징입니다.

-  라이브러리 사용자들에게 자신의 응용 프로그램에서 외부적으로 내부 라이브러리 오류 처리 상태를 관리하도록 요구하는 것보다 더 간단합니다.

구현 주의점
-----------

GDAL의 (그리고 OGR 및 OSR의) 오류 처리 콜백 메커니즘은 광범위하게 쓰이고 있기 때문에 기저 라이브러리에 콜백 서명 '또는' 기존 콜백 작업의 습성을 망가트릴 수 있는 변경 사항을 적용해서는 안 됩니다. 콜백에 사용자 데이터를 위한 지원을 추가하는 것은 오류 처리 작업에 이미 존재하는 기존 기능에 추가하는 방식으로 제공되어야 하며, 일반적으로 가장 깔끔한 접근법을 사용할 수 없는 경우, 기존 작업을 모방하거나 비슷하게 보이는 접근법이 GDAL을 위한 최선의 접근법일 것입니다.

변경 계획
---------

첫 번째 변경 사항은 :cpp:class:`CPLErrorHandlerNode` 에 ``void*`` 를 추가하는 것입니다:

.. code-block:: cpp

    typedef struct errHandler
    {
        struct errHandler   *psNext;
        void                *pUserData;
        CPLErrorHandler     pfnHandler;
    } CPLErrorHandlerNode;

그 다음 사용자 데이터를 가진 오류 핸들러를 추가하기 위해 메소드에 ``void*`` 를 추가할 것입니다:

.. code-block:: cpp

    CPLErrorHandler CPL_DLL CPL_STDCALL CPLSetErrorHandlerEx(CPLErrorHandler, void*);
    void CPL_DLL CPL_STDCALL CPLPushErrorHandlerEx( CPLErrorHandler, void* );

:cpp:func:`CPLSetErrorHandler` 및 :cpp:func:`CPLPushErrorHandler` 는 단순히 ``Ex`` 함수를 사용해서 'pUserData' 멤버에 NULL을 전송할 것입니다.

마지막으로, :cpp:func:`CPLGetLastErrorType` 및 :cpp:func:`CPLGetLastErrorMsg` 메소드와 마찬가지로, :cpp:func:`CPLGetErrorHandlerUserData` 를 추가할 것입니다:

.. code-block:: cpp

    void* CPL_STDCALL CPLGetErrorHandlerUserData(void);

SWIG 바인딩 고려 사항
~~~~~~~~~~~~~~~~~~~~~

이 RFC를 구현하기 위해 현재 활성화된 오류 핸들러 용 사용자 데이터에 접근할 수 있도록 SWIG 바인딩을 업데이트하지 '않을' 것입니다. 하지만 SWIG 바인딩 유지/관리자는 재량에 따라 이 새로운 기능의 장점을 활용할 수 있습니다.

티켓 이력
---------

`#4295 티켓 <https://trac.osgeo.org/gdal/ticket/4295>`_ 페이지가 제안 해결책을 구현하는 패치를 담고 있으며, 이 기능에 관한 맥락 및 논의를 제공합니다. `4295-hobu-rfc.patch <https://trac.osgeo.org/gdal/attachment/ticket/4295/4295-hobu-rfc.patch>`_ 페이지가 제안 기능을 구현하는 최신 패치를 담고 있습니다.

문서화
------

추가 함수들의 문서를 패치의 일부분으로 제공합니다.

구현
----

RFC 승인 이후 하워드 버틀러가 트렁크에 모든 코드를 구현할 것입니다.

