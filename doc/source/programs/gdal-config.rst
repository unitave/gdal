.. _gdal-config:

================================================================================
gdal-config (Unix)
================================================================================

.. only:: html

GDAL 설치에 대한 다양한 정보를 결정합니다.

.. Index:: gdal-config

개요
--------

.. code-block::

    gdal-config [OPTIONS]
    Options:
            [--prefix[=DIR]]
            [--libs]
            [--cflags]
            [--version]
            [--ogr-enabled]
            [--formats]

설정
-----------

이 (유닉스 시스템에서 사용할 수 있는) 유틸리티 스크립트를 사용하면 GDAL 설치에 대한 다양한 정보를 결정할 수 있습니다. 일반적으로 GDAL을 사용하는 응용 프로그램을 위한 환경설정 스크립트만 이 유틸리티를 사용하지만, 최종 사용자도 쿼리할 수 있습니다.

.. option:: --prefix

    GDAL 설치를 위한 최고 수준 디렉터리입니다.

.. option:: --libs

    GDAL을 사용하기 위해 필수적인 라이브러리와 링크 지시문(link directives)입니다.

.. option:: --cflags

    GDAL을 사용하는 모듈을 컴파일하기 위해 필수적인 include 및 macro 정의입니다.

.. option:: --version

    GDAL 버전을 리포트합니다.

.. option:: --ogr-enabled

    OGR이 GDAL 내에 빌드되었는지에 따라 표준 출력(stdout)에 "yes" 또는 "no"를 리포트합니다.

.. option:: --formats

    GDAL 내에 어떤 포맷들이 환경설정되었는지 표준 출력(stdout)에 리포트합니다.
