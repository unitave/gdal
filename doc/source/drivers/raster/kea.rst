.. _raster.kea:

================================================================================
KEA
================================================================================

.. shortname:: KEA

.. build_dependencies:: libkea 및 libhdf5 라이브러리

GDAL은 libkea 라이브러리를 통해 KEA 포맷 파일을 읽고, 쓰고, 업데이트할 수 있습니다.

KEA는 뉴질랜드 새의 이름을 딴 이미지 파일 포맷으로, HDF5 파일 내에 GDAL 데이터 모델을 완전히 구현한 포맷입니다. 소프트웨어 라이브러리인 libkea를 사용해서 파일 포맷에 접근합니다. 이 포맷은 기존 HDF5 포맷 대비 더 적은 용량으로 생성되면서도 기존 포맷과 비등한 성능을 보여줍니다. 이 포맷은 이미 뉴질랜드의 랜드케어 연구소와 여러 커뮤니티에서 수많은 프로젝트에 활발히 쓰이고 있습니다.

KEA 포맷은 다음과 같은 GDAL 데이터 모델 기능들을 지원합니다:

-  서로 다른 데이터 유형일 수도 있는 다중 밴드 지원, AddBand() API를 통해 기존 데이터셋에 밴드를 추가할 수 있습니다.
-  이미지 블록 작업 지원
-  이미지 블록 데이터 읽기, 생성 및 업데이트
-  아핀 지리변형, WKT 투영법, GCP
-  데이터셋 수준 및 밴드 수준의 메타데이터
-  밴드 별 설명
-  밴드 별 NODATA 및 색상 해석
-  밴드 별 색상표
-  임의의 크기의 밴드 별 RAT(Raster Attribute Table)
-  내부 오버뷰 및 마스크 밴드

드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::

.. supports_create::

.. supports_georeferencing::

.. versionadded:: 3.0

    .. supports_virtualio::

생성 옵션
----------------

다음 생성 옵션들을 사용할 수 있습니다. 일부 옵션은 조금 난해하기 때문에, 사용자가 기저 HDF5 포맷의 기작에 대해 잘 알지 못 한다면 쉽게 지정해서는 안 됩니다.

-  **IMAGEBLOCKSIZE=integer_value**:
   이미지 데이터의 각 블록의 크기를 설정합니다. 기본값은 256입니다.

-  **ATTBLOCKSIZE=integer_value**:
   속성 데이터의 각 블록의 크기를 설정합니다. 기본값은 1000입니다.

-  **MDC_NELMTS=integer_value**:
   메타데이터 캐시에 있는 요소들의 개수를 설정합니다. 기본값은 0입니다.
   HDF5 문서의 `데이터 캐시 작업 <http://www.hdfgroup.org/HDF5/doc/H5.user/Caching.html>`_ 을 참조하십시오.

-  **RDCC_NELMTS=integer_value**:
   RAW 데이터 덩어리(chunk) 캐시에 있는 요소들의 개수를 설정합니다. 기본값은 512입니다.
   HDF5 문서의 `데이터 캐시 작업 <http://www.hdfgroup.org/HDF5/doc/H5.user/Caching.html>`_ 을 참조하십시오.

-  **RDCC_NBYTES=integer_value**:
   RAW 데이터 덩어리(chunk) 캐시의 바이트 단위 총 용량입니다. 기본값은 1048576입니다.
   HDF5 문서의 `데이터 캐시 작업 <http://www.hdfgroup.org/HDF5/doc/H5.user/Caching.html>`_ 을 참조하십시오.

-  **RDCC_W0=floating_point_value between 0 and 1**:
   선취(preemption) 정책을 설정합니다. 기본값은 0.75입니다.
   HDF5 문서의 `데이터 캐시 작업 <http://www.hdfgroup.org/HDF5/doc/H5.user/Caching.html>`_ 을 참조하십시오.

-  **SIEVE_BUF=integer_value**:
   데이터 거르기(sieve) 버퍼의 최대 크기를 설정합니다. 기본값은 65536입니다.
   `H5Pset_sieve_buf_size() <http://www.hdfgroup.org/HDF5/doc/RM/RM_H5P.html#Property-SetSieveBufSize>`_ 문서를 참조하십시오.

-  **META_BLOCKSIZE=integer_value**:
   메타데이터 블록 할당의 최소 크기를 설정합니다. 기본값은 2048입니다.
   `H5Pset_meta_block_size() <http://www.hdfgroup.org/HDF5/doc/RM/RM_H5P.html#Property-SetMetaBlockSize>`_ 문서를 참조하십시오.

-  **DEFLATE=integer_value**:
   압축 수준을 0(비압축)에서 9(최대 압축) 사이로 설정합니다. 기본값은 1입니다.

-  **THEMATIC=YES/NO**:
   이 옵션을 YES로 설정하면 모든 밴드를 테마 밴드(thematic band)로 설정합니다. 기본값은 NO입니다.

참고
--------

-  `libkea GitHub 저장소 <https://github.com/ubarsc/kealib>`_
-  `KEAimage 파일 포맷, 피터 번팅(Peter Bunting)과 샘 길링엄(Sam Gillingham), 컴퓨터 &amp; 지구과학(Computers &amp; Geosciences) 지에 발표 <http://www.sciencedirect.com/science/article/pii/S0098300413001015>`_
-  :ref:`HDF5 <raster.hdf5>` 드라이버
