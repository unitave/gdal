.. _using_gdal_in_cmake:

********************************************************************************
CMake 프로젝트에서 GDAL 사용하기
********************************************************************************

.. versionadded:: 3.5

CMake 프로젝트에서 GDAL 라이브러리를 사용하기 위해 권장하는 방법은 라이브러리와 함께 제공되는 CMake 환경설정이 제공하는 가져온 라이브러리 대상(target) ``GDAL::GDAL`` 과 링크하는 것입니다. 일반적인 사용법은 다음과 같습니다:

.. code::

    find_package(GDAL CONFIG REQUIRED)

    target_link_libraries(MyApp PRIVATE GDAL::GDAL)

대상 링크 라이브러리에 가져온 라이브러리 대상 ``GDAL::GDAL`` 을 추가하면, CMake가 컴파일러에 :file:`include` 디렉터리도 전송할 것입니다.

CMake 명령어 ``find_package`` 는 여러 위치에서 환경설정을 검색할 것입니다. ``CMAKE_PREFIX_PATH`` 캐시 변수 또는 환경 변수를 설정하면 모든 패키지에 대해 검색을 조정할 수 있습니다. 특히, CMake는 ``GDAL_DIR`` 캐시 변수를 참고(하고 설정)할 것입니다.

