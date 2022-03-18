.. _raster.ida:

================================================================================
IDA -- 이미지 출력 및 분석(Image Display and Analysis)
================================================================================

.. shortname:: IDA

.. built_in_by_default::

.. deprecated_driver:: version_targeted_for_removal: 3.5
   env_variable: GDAL_ENABLE_DEPRECATED_DRIVER_IDA

GDAL은 몇몇 제약 아래 IDA 이미지 읽기 및 쓰기를 지원합니다. IDA 이미지는 WinDisp 4의 이미지 포맷입니다. IDA 파일은 언제나 8비트 데이터 유형의 단일 밴드 형식입니다. IDA 파일의 확장자는 주로 .img를 사용하지만 필수적인 것은 아닙니다.

투영법 및 지리참조 정보 읽기를 지원하지만, 몇몇 투영법은 (예: Meteosat, 함메르-아이토프(Hammer-Aitoff) 등) 지원하지 않습니다. IDA 파일 작성 시 투영법이 0이라는 가짜 편동과 가짜 편북을 가져야만 합니다. IDA는 지리 좌표계, 람베르트 정각원추, 람베르트 정적방위, 알베르스 정적원추 및 구드 호몰로사인(Goodes Homolosine) 좌표계를 지원합니다.

IDA 파일은 일반적으로 경사(slope) 및 오프셋을 통해 8비트로 크기 조정된 값을 담고 있습니다. 이 값들은 밴드의 경사 및 오프셋 값으로 반환되는데, 분석을 위해 데이터를 원본 RAW 값으로 다시 크기 조정하려는 경우 반드시 이 값들을 사용해야만 합니다.

주의: ``gdal/frmts/raw/idadataset.cpp`` 로 구현되었습니다.

참고: `WinDisp <http://www.fao.org/giews/english/windisp/windisp.htm>`_

드라이버 케이퍼빌리티
-------------------

.. supports_createcopy::

.. supports_create::

.. supports_georeferencing::

.. supports_virtualio::
