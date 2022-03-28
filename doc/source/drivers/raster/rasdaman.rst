.. _raster.rasdaman:

================================================================================
Rasdaman GDAL 드라이버
================================================================================

.. shortname:: Rasdaman

.. build_dependencies:: raslib

Rasdaman은 관계형 데이터베이스에 저장된 무제한 용량의 다중 차원 배열에 대한 SQL 스타일 쿼리 언어를 제공하는 래스터 데이터베이스 미들웨어입니다. 오픈 소스 코드, 문서 등을 살펴보고 싶다면 `www.rasdaman.org <http://www.rasdaman.org>`_ 홈페이지를 참조하십시오. 현재 Rasdaman은 OSGeo 인큐베이션의 후보로 고려 중에 있습니다.

이 드라이버의 구현에서, GDAL은 모든 접근 시 구상적인 부분 집합 상자(concrete subsetting box)가 인스턴스화하는 쿼리 템플릿을 정의해서 Rasdaman에 접속합니다. 이렇게 하면 (초분광 위성 시계열, 다중 변수 기상 시뮬레이션 데이터, 해양 모델 데이터 등과 같은) n차원 데이터셋으로부터 잘라낸 2차원 데이터를 전송할 수 있습니다. 특히 지상 실측 데이터(ground truth data)로부터 쿼리 요청에 의해 파생된 가상 영상을 제공할 수 있습니다. 다음은 몇몇 기술적인 상세 사항에 관한 예시입니다.

-  연결 문자열 문법은 WKT 래스터 패턴을 따르며, 다음과 같습니다:

::

   rasdaman: query='select a[$x_lo:$x_hi,$y_lo:$y_hi] from MyImages as a' [tileXSize=1024] [tileYSize=1024] [host='localhost'] [port=7001] [database='RASBASE'] [user='rasguest'] [password='rasguest']

이 경우 Rasdaman 쿼리 언어(rasql) 문자열은 부분 집합 작업만 수행합니다. GDAL이 이미지에 접근할 때, $ 파라미터를 입력 타일 좌표로부터 계산한 구상적인 부분 집합 상자로 대체합니다.

-  하지만, 쿼리가 2차원 데이터를 반환하는 한 쿼리에 어떤 유형의 처리 작업도 포함시킬 수 있습니다. 예를 들어 다음 쿼리는 가장 오래된 이미지 시계열로부터 적색 및 근적외선 픽셀들의 평균값을 반환합니다:

::

   query='select ( a.red+a.nir ) /2 [$x_lo:$x_hi,$y_lo:$y_hi, 0 ] from SatStack as a'

현재 지리참조 정보 읽기 또는 쓰기는 지원하지 않습니다.

참고
--------

-  `Rasdaman 프로젝트 <http://www.rasdaman.org/>`__
