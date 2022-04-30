.. _configoptions:

================================================================================
환경설정 옵션
================================================================================

이 페이지에서는 GDAL 용 런타임 환경설정 옵션에 대해 논의합니다. 런타임 환경설정 옵션은 빌드 시 환경설정 스크립트에 사용되는 옵션들과는 다릅니다. 런타임 환경설정 옵션은 모든 플랫폼 상에 적용되며, 런타임 시 평가됩니다. 사용자가 명령줄 스위치 또는 환경 변수에 직접 작성해서 프로그램적으로 설정할 수 있습니다.

환경설정 옵션은 일반적으로 GDAL/OGR 드라이버의, 그리고 어떤 경우 GDAL/OGR 코어의 기본 습성을 변경하기 위해 사용됩니다. 환경설정 옵션은 본질적으로 사용자가 설정할 수 있는 전체 수준 변수입니다.

환경설정 옵션 설정 방법
-----------------------

환경설정 옵션의 예를 들자면, 이를테면 :decl_configoption:`GDAL_CACHEMAX` 옵션이 있습니다. 이 옵션은 GDAL 블록 캐시의 용량을 메가바이트 단위로 제어합니다. 유닉스 (bash/bourne) 셸에서 다음과 같이 환경 변수로 설정할 수 있습니다:

::

    export GDAL_CACHEMAX=64

또는 다음과 같이 명령어에 포함시킬 수도 있습니다:

::

    GDAL_CACHEMAX=64 gdal_translate 64 in.tif out.tif


도스/윈도우 명령 프롬프트에서는 다음과 같이 설정할 수 있습니다:

::

    set GDAL_CACHEMAX=64

명령줄에서 대부분의 GDAL 및 OGR 유틸리티에 ``--config`` 스위치로 설정할 수 있긴 하지만, 이 스위치가 제 시간에 평가되지 않아 습성에 영향을 미치지 못 하는 경우도 있습니다:

::

    gdal_translate --config GDAL_CACHEMAX 64 in.tif out.tif

C/C++에서는 :cpp:func:`CPLSetConfigOption` 함수로 환경설정 스위치를 프로그램적으로 설정할 수 있습니다:

.. code-block:: c

    #include "cpl_conv.h"
    ...
        CPLSetConfigOption( "GDAL_CACHEMAX", "64" );

환경설정 옵션은 일반적으로 프로그램에서 활성화된 모든 스레드에 적용되지만, :cpp:func:`CPLSetThreadLocalConfigOption` 함수로 현재 스레드에만 적용되도록 제한할 수 있습니다:

.. code-block:: c

    CPLSetThreadLocalConfigOption( "GTIFF_DIRECT_IO", "YES" );

불(boolean) 옵션의 경우, 옵션을 활성화시키려면 YES, TRUE 또는 ON 값으로, 비활성화시키려면 NO, FALSE 또는 OFF 값으로 설정하면 됩니다.

.. _gdal_configuration_file:

GDAL 환경설정 파일
-----------------------

.. versionadded:: 3.3

드라이버 등록 시, 사전 정의 파일 집합으로부터 환경설정 불러오기를 시도합니다.

:cpp:func:`CPLLoadConfigOptionsFromPredefinedFiles` 메소드가 다음 위치를 시도합니다:

   -  먼저 GDAL_CONFIG_FILE 환경 변수(또는 환경설정 옵션)가 가리키는 위치를 시도합니다. 이 변수(또는 옵션)가 설정된 경우 다음 단계를 시도하지 않습니다.

   -  유닉스 빌드의 경우, 먼저 ``${sysconfdir}/gdal/gdalrc`` 가 가리키는 위치를 시도합니다. (이때 './configure'의 ``--sysconfdir`` 스위치를 호출하지 않는 이상 '${sysconfdir}'는 '${prefix}/etc'로 평가됩니다.) 그 다음 ``$(HOME)/.gdal/gdalrc`` 를 시도하는데, 'sysconfdir'로 불러온 경로를 대체할 수도 있습니다.

   -  윈도우 빌드의 경우, ``$(USERPROFILE)/.gdal/gdalrc`` 가 가리키는 위치를 시도합니다.

환경설정 파일은 .ini 스타일 서식으로 된 텍스트 파일이며, 그 내용은 환경설정 옵션과 그 값의 목록입니다. 주석 줄은 '#' 문자로 시작합니다. 다음은 그 예시입니다:

.. code-block::

    [configoptions]
    # FOO 환경설정 옵션의 값을 BAR로 설정
    FOO=BAR

:cpp:func:`CPLSetConfigOption` 또는 :cpp:func:`CPLSetThreadLocalConfigOption` 메소드를 호출하면, 또는 ``--config`` 명령줄 스위치를 통해 환경설정 파일에 설정된 환경설정 옵션을 대체할 수 있습니다.

환경설정 파일에 설정된 값 대신 GDAL 구동 전에 설정된 환경 변수의 값을 사용할 것입니다.

.. _list_config_options:

환경설정 옵션 목록 및 적용 드라이버
-----------------------------------

.. note::

   이 목록은 완성되지 않았습니다. 이 목록은 GDAL 문서에서 환경설정 옵션을 언급하는 경우 제대로 된 색인 표시를 했느냐에 따라 달라집니다.
   이 목록을 제대로 만들고 싶다면, 환경설정 옵션을 언급하는 위치에 ``:decl_configoption:`NAME``` 문법을 사용하십시오.

.. include:: configoptions_index_generated.rst

