.. _vector.pds:

PDS - 행성 데이터 시스템 TABLE
==================================

.. shortname:: PDS

.. built_in_by_default::

OGR PDS 드라이버는 PDS(Planetary Data Systems) 데이터셋으로부터 TABLE 객체를 읽어옵니다. PDS 데이터셋으로부터 래스터 IMAGE 객체를 읽어오는 GDAL PDS 드라이버가 있다는 사실을 기억하십시오.

이 드라이버의 입력물은 (실제 데이터는 개별 파일에 있는 경우라도) 상품 수준 파일이어야만 합니다.

라벨 파일이 *TABLE* 객체를 담고 있는 경우, 데이터셋의 유일한 레이어로 읽어올 것입니다. *TABLE* 객체가 없다면, 드라이버가 TABLE 문자열을 담고 있는 모든 객체를 검색해서 레이어에 하나씩 읽어올 것입니다.

ASCII 및 BINARY 테이블을 지원합니다. 이 드라이버는 그때 그때 즉시 처리하는 COLUMN 객체로부터 또는 ^STRUCTURE가 가리키는 개별 파일로부터 필드 설명을 읽어올 수 있습니다.

테이블이 REAL 유형의 LONGITUDE 및 LATITUDE 열을 가지고 있고 UNIT=DEGREE인 경우, POINT 도형을 반환하는 데 사용할 것입니다.

드라이버 케이퍼빌리티
-------------------

.. supports_virtualio::

참고
--------

-  `PDS 포맷 설명 <https://pds.jpl.nasa.gov/tools/standards-reference.shtml>`_
   (StdRef_20090227_v3.8.pdf의 부록 A.29 참조)
