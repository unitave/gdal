OGRSpatialReference.SetFromUserInput() 호출이 지원하는 좌표계라면 어떤 좌표계든 전송(pass)할 수 있습니다. 이 지원 좌표계에는 투영 EPSG, 지리 또는 복합 좌표계(예: EPSG:4296), WKT(Well Known Text) 좌표계 정의, PROJ.4 선언, 또는 WKT 좌표계 정의를 담고 있는 .prj 파일의 이름 등이 포함됩니다.

GDAL 2.2버전부터 공간 좌표계가 PROJ.4 지오이드그리드(geoidGrid)를 가리키는 명백한 수직 데이터를 가지고 있고 입력 데이터셋이 단일 밴드 데이터셋인 경우, 데이터셋의 값들에 수직 보정이 적용될 것입니다.
