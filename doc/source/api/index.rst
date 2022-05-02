.. _api:

================================================================================
API
================================================================================

.. only:: not latex

   `전체 독시젠(Doxygen) 산출물 <../doxygen/index.html>`_
   ----------------------------------------------

   C API
   -----

   .. toctree::
       :maxdepth: 1

       cpl
       raster_c_api
       vector_c_api
       gdal_alg
       ogr_srs_api
       gdal_utils

   C++ API
   -------

   래스터 API
   +++++++++++++++++++++++++++

   .. toctree::
       :maxdepth: 1

       gdaldriver_cpp
       gdaldataset_cpp
       gdalrasterband_cpp
       gdalwarp_cpp

   벡터 API
   +++++++++++++++++++++++++++

   .. toctree::
       :maxdepth: 1

       ogrfeature_cpp
       ogrfeaturestyle_cpp
       ogrgeometry_cpp
       ogrlayer_cpp

   공간 좌표계 API
   ++++++++++++++++++++++++++++

   .. toctree::
       :maxdepth: 1

       ogrspatialref

   다중 차원 배열 API
   +++++++++++++++++++++++++++

   .. toctree::
       :maxdepth: 1

       gdalgroup_cpp
       gdaldimension_cpp
       gdalabstractmdarray_cpp
       gdalmdarray_cpp
       gdalattribute_cpp
       gdalextendeddatatype_cpp

   기타 C++ API
   ++++++++++++++++++++++++++++

   .. toctree::
       :maxdepth: 1

       cpl_cpp
       gnm_cpp

   파이썬 API
   ----------

   .. toctree::
       :maxdepth: 1

       python
       python_api_ref
       python_gotchas
       python_samples


   `자바 API <../java/index.html>`_
   --------------------------------


   다른 언어로 된 GDAL/OGR
   ---------------------------

   GDAL 소스 트리에 ('swig' 하위 디렉터리에) 일반 `SWIG <http://www.swig.org/>`_ 인터페이스 파일들의 집합과 그에 기반한 언어 바인딩 집합이 있습니다. 현재 다음 파일들이 활성 상태입니다:

   .. toctree::
       :maxdepth: 1

       csharp/index
       java/index

   GDAL 소스 트리 외부에서 개발된 다른 바인딩들도 있습니다. (**주의**: )
   There are also other bindings that are developed outside of the GDAL source tree (**note**: 이런 언어 바인딩들은 GDAL/OGR C/C++ API와 엄격하게 결합되지 않은 API를 제공합니다.) 다음과 같은 바인딩들을 포함합니다:

      .. toctree::
       :maxdepth: 1

       Go <https://github.com/lukeroth/gdal>
       Julia <https://github.com/JuliaGeo/GDAL.jl>
       Lua <https://trac.osgeo.org/gdal/wiki/GdalOgrInLua>
       원본 Node.js 바인딩 <https://github.com/naturalatlas/node-gdal>
       전체 프로미스(Promise) 기반 비동기 및 TypeScript 지원을 포함하는 Node.js 포크 <https://www.npmjs.com/package/gdal-async>
       펄(Perl) <https://metacpan.org/release/Geo-GDAL-FFI>
       PHP <http://dl.maptools.org/dl/php_ogr/php_ogr_documentation.html>
       R <http://cran.r-project.org/web/packages/rgdal/index.html>

   .. warning::
        펄의 경우, GDAL 3.5버전부터 `Perl <https://trac.osgeo.org/gdal/wiki/GdalOgrInPerl>`_ 링크가 퇴출되었기 때문에, 앞의 링크를 대신 사용하십시오.

        R의 경우, 소스포지(SourceForge)에 있는 rgdal이 오래되었습니다.

   벡터/OGR 함수를 좀 더 파이썬처럼 사용하는 방식도 있습니다:

      .. toctree::
       :maxdepth: 1

       Fiona <https://github.com/Toblerity/Fiona>
       Rasterio <https://github.com/mapbox/rasterio>

   래스터 함수를 좀 더 관용적인 Go 언어처럼 사용하는 방식이 있습니다:

      .. toctree::
       :maxdepth: 1

       Godal <https://github.com/airbusgeo/godal>

.. only:: latex

   이 PDF 문서에서는 API가 생략되었습니다. https://gdal.org/api/index.html 에서 볼 수 있습니다.

