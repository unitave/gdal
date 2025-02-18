.. _ogr_feature_style:

================================================================================
피처 스타일 사양
================================================================================

0.016버전 - 2018년 12월 3일

1. 개요
-----------

이 문서는 GDAL 벡터 드라이버(OGR)에서 피처 스타일 정보(예: 색상, 선 굵기, 심볼 등등)를 다양한 수준에서 처리해야 하는 방식을 정의합니다.

다음 GDAL 벡터 드라이버는 피처 스타일을 다양한 수준에서 지원합니다:

-  :ref:`DWG (libopencad) <vector.cad>`
-  :ref:`DWG (Teigha) <vector.dwg>`
-  :ref:`DXF <vector.dxf>`
-  :ref:`KML (libkml) <vector.libkml>`
-  :ref:`MapInfo <vector.mitab>`
-  :ref:`마이크로스테이션 DGN v7 <vector.dgn>` 및 :ref:`DGN v8 <vector.dgnv8>`
-  :ref:`OpenJUMP JML <vector.jml>` 및 :ref:`PDF <raster.pdf>`

1.1 스타일은 피처 객체의 속성(property)이다
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

피처 스타일은 개념적으로 피처의 속성(property)으로 보여야 합니다. 일부 시스템이 특수 속성(attribute)에 스타일 정보를 저장하긴 하지만, GDAL에서는 더 일관적으로 -- 피처의 도형도 속성(property)인 것과 똑같은 방식으로 -- 스타일을 속성(property)으로 간주합니다.

그렇다고는 하지만 스타일에 대한 준비가 되어 있지 않은 몇몇 포맷을 작성하는 경우 (예: E00) 속성(attribute)에 스타일 정보를 저장하는 일을 피할 수는 없습니다. 그러나 GDAL을 통해 데이터셋을 여는 것과 같은 때에, 스타일 정보를 담고 있는 속성(attribute)의 이름을 메타데이터에 지정하거나 또는 사용자가 지정해야 합니다.

또한 SFCOM 인터페이스에서는 도형과 마찬가지로 속성(attribute)에 스타일 정보를 저장할 것입니다.

1.2 피처 스타일은 2개 수준에 저장할 수 있다
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

스타일은 피처를 그려야 하는 방식을 정의하지만, 피처 여러 개가 동일한 스타일을 공유하는 경우도 매우 흔합니다. 이런 경우 각 피처에 스타일 정보를 복제하는 대신 스타일 정보를 공유할 수 있는 더 효율적인 방식을 제공할 것입니다.

스타일 정보를 찾을 수 있는 수준이 2개 있습니다:

-  **데이터셋** 이 향우 레이어 또는 개별 피처가 참조할 수 있는 사전 정의 스타일 테이블을 가질 수 있습니다. 이 문서에 이를 위한 메커니즘을 정의하고 있습니다.

-  **피처 (OGRFeature 객체)** 가 자신만의 완전한 스타일 정의를 가질 수 있습니다. 또는 데이터셋의 스타일 테이블에 있는 스타일에 피처를 링크시킬 수 있는데, 동일한 스타일을 자주 재사용하는 경우 저장소 공간을 절약할 수 있습니다.

어떤 데이터셋을 작업하는 동안 하나 이상의 여러 수준에 스타일 정보를 저장할 수 있을 것입니다. 스타일을 실제로 저장하는 수준(들)은 지금 작업 중인 포맷에 대한 가장 효율적인 접근법이 무엇이냐에 따라 달라집니다.

1.3 그리기 도구
~~~~~~~~~~~~~~~~~

스타일 정의를 작성하는 데 사용되는 몇몇 그리기(drawing) 도구의 집합을 정의합니다:

-  **PEN**: 선 스타일 용
-  **BRUSH**: 면 채우기 용
-  **SYMBOL**: 포인트 심볼
-  **LABEL**: 주석 용

이 그리기 도구들은 각각 (모두 선택적인) 파라미터 여러 개를 가질 수 있습니다. 스타일 문법은 이 가능한 모든 파라미터를 전부 지원하지 못 하는 시스템이 지원하지 않는 파라미터들을 안전하게 건너뛰고 무시할 수 있는 방식으로 작성됩니다. 이런 문법은 향후 기존 코드 또는 응용 프로그램을 건드리지 않고 사양을 확장시키기 쉽게 해줄 것입니다.

스타일은 단일 도구를 사용할 수도 있고, 또는 하나 이상의 도구를 결합해서 사용할 수도 있습니다. 스타일에 도구 여러 개를 결합해서 사용하면 거의 모든 유형의 그래픽 표현을 작성할 수 있습니다. 예를 들어 SYMBOL 도구를 사용해서 라인을 따라 일정 간격으로 심볼을 배치할 수 있습니다. 또 LABEL 도구를 사용해서 포인트 위에 텍스트를 배치하고 라인을 따라 늘릴 수 있습니다. 여기에 LABEL 도구와 PEN 도구를 결합하면 라인을 텍스트 라벨의 지시선으로 사용해서 라인의 마지막 꼭짓점에 텍스트 문자열을 그릴 수도 있습니다.

물론, 이 모든 것을 지원할 수 있는 시스템은 많지 않습니다. 그러나 여기에서 강조하고자 하는 것은 스타일 사양이 모든 유형의 포맷이 스타일 정보를 가능한 한 손실 없이 교환할 수 있도록 해주는 충분히 강력하고 유연한 사양이라는 점입니다.

1.4 스타일 정의가 피처 속성(attribute)을 사용할 수 있다
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

스타일 정의가 어떤 도구 파라미터의 값에 대해 스타일 자체 안에 하드코딩된 값을 가지는 대신 피처의 속성 필드를 참조하는 것이 더 유용한 경우가 종종 있습니다.

텍스트 기울기 각도, 텍스트 문자열 등등 각 단일 텍스트 라벨별로 달라지는 값을 예로 들 수 있습니다. 각 피처의 속성에서 각도 및 텍스트 문자열을 검색할 수 있다면 레이어 수준에서 나머지 라벨 스타일을 공유할 수 있습니다.

스타일 문자열의 문법은 모든 파라미터 값이 상수값 또는 속성 필드 검색값 가운데 하나일 수 있는 방식입니다.

1.5 도구 파라미터 단위
~~~~~~~~~~~~~~~~~~~~~~~~

작업 중인 파일 포맷에 따라 몇몇 파라미터 값을 서로 다른 측정 단위로 표현할 수 있습니다. 예를 들면 일부 시스템들은 선 굵기 또는 텍스트 높이를 포인트 단위로 표현하는데 다른 시스템들은 픽셀 단위로 표현하고 또다른 시스템들은 지상 단위로 표현합니다. 이 모든 단위를 수용하기 위해, 모든 파라미터를 다음 단위계 가운데 하나로 지정할 수 있습니다:

-  **g**: 맵 지상 단위(Map Ground Unit) (맵의 좌표계 단위)
-  **px**: 픽셀
-  **pt**: 포인트 (1/72 인치)
-  **mm**: 밀리미터
-  **cm**: 센티미터
-  **in**: 인치

몇몇 도구는 한 단위계로부터 다른 단위계로의 값 변환을 단순화하기 위해 GDAL 클라이언트 수준에서 단위계를 지정해야 합니다. 즉 지상 단위로부터 종이/픽셀 단위로의 변환을 수행할 수 있도록 GDAL 클라이언트가 맵 축척을 지정해야 한다는 뜻입니다.

--------------

2. 피처 스타일 문자열
-----------------------

앞에서 말했듯이, 스타일 정의는 보통 레이어별 (또는 데이터셋별) 테이블에 또는 피처에 직접 문자열로 저장됩니다.

2.1 예시
~~~~~~~~~~~~

다음은 스타일 정의 문자열의 몇몇 예시입니다:

-  5픽셀 굵기의 적색 라인:
   ``PEN(c:#FF0000,w:5px)``
-  외곽선이 흑색이고 안은 청색으로 채워진 폴리곤A:
   ``BRUSH(fc:#0000FF);PEN(c:#000000)``
-  포인트 심볼:
   ``SYMBOL(c:#00FF00,id:"points.sym-45,ogr-sym-7")``
-  "text_attribute" 속성(attribute) 테이블로부터 텍스트 문자열을 가져오는 텍스트 라벨:
   ``LABEL(f:"Times New Roman",s:12pt,t:{text_attribute})"``

다음은 앞의 모든 스타일을 담고 있는 스타일 테이블의 모습의 예시입니다:

::

       road:      PEN(c:#FF0000,w:5px)
       lake:      BRUSH(fc:#0000FF);PEN(c:#000000)
       campsite:  SYMBOL(c:#00FF00,id:"points.sym-45,ogr-sym-7")
       label:     LABEL(f:"Times New Roman",s:12pt,t:{text_attribute})

이런 테이블이 있다면 개별 피처가 스타일 속성(property)에 있는 스타일 이름 앞에 "@" 문자를 붙여서 이 테이블로부터 스타일을 참조할 수 있습니다.

예를 들어, 스타일이 "@road"로 설정된 객체는 적색 선으로 그려질 것입니다.

2.2 스타일 문자열 문법
~~~~~~~~~~~~~~~~~~~~~~~

각 피처 객체는 스타일 속성(property) 문자열을 가집니다:

::

    <style_property> = "<style_def>" | "" | "@<style_name>" | "{<field_name>}"

-  ``<style_def>`` 는 이 아래에서 정의합니다.
-  비어 있는 스타일 문자열은 피처 스타일을 지정하지 않았다는 의미입니다. 피처가 비가시화되었다는 의미가 아닙니다. 비가시화 피처는 ``PEN(c:#00000000)`` 처럼 완전히 투명한 색상을 사용해서 나타냅니다.
-  ``@<style_name>`` 은 레이어 또는 데이터셋 스타일 테이블에 있는 사전 정의 스타일을 참조한다는 뜻입니다. 먼저 레이어의 테이블을 검색해서 "style_name"이 없는 경우 데이터셋의 테이블을 검색할 것입니다.
-  마지막으로, ``{<field_name>}`` 은 지정한 속성(attribute) 필드로부터 스타일 속성(property)을 읽어와야 한다는 의미입니다.

<style_def>가 실제 스타일 정의입니다. 스타일 정의는 하나 이상의 스타일 부분들을 쌍반점으로 구분해서 결합한 것입니다. 각 <style_part>는 완전한 그래픽 표현의 일부분을 정의하는 그리기 도구를 사용합니다:

::

  <style_def> =    <style_part>[;<style_part>[;...]]

  <style_part> =   <tool_name>([<tool_param>[,<tool_param>[,...]]])

  <tool_name> =    그리기 도구의 이름, 현재: PEN | BRUSH | SYMBOL | LABEL

  <tool_param> =   <param_name>:<param_value>

  <param_name> =   각 그리기 도구의 파라미터 이름 목록 참조

  <param_value> =  <value> | <value><units>

  <value> =        "<string_value>" | <numeric_value> | {<field_name>}

  <units> =        g | px | pt | mm | cm | in

기본적으로, 각 부분에 서로 다른 수준 파라미터 값이 할당되어 있지 않는 이상 <style_def> 문자열에 나타나는 순서대로 스타일 부분을 그립니다. (수준 파라미터 정의를 참조하십시오.)

그리기 도구의 파라미터는 모두 선택적입니다. 따라서 비어 있는 그리기 도구 파라미터 목록을 가진 (예: ``PEN()``) <style_part>를 작성할 수 있습니다. 값을 지정하지 않은 각 파라미터의 경우 클라이언트 응용 프로그램에 따라 자신만의 기본값을 사용할 것입니다. 이 문서는 파라미터 대부분에 대한 권장 기본값을 제공하지만, 응용 프로그램이 이 기본값들을 반드시 사용해야 하는 것은 아닙니다.

<tool_param> 값에 {<field_name>}를 사용하는 경우, 단위에 따라 각각 몇 개의 옵션을 사용할 수 있습니다. 이 단위는 ``PEN(c:#FF0000,w:{line_width}pt)`` 처럼 필드 이름 뒤에 지정할 수도 있고 또는 ``PEN(c:#FF0000,w:{line_width})`` 처럼 지정하지 않을 수도 있습니다. 전자의 경우 기본 단위가 포인트(pt)이지만 "line_width" 속성(attribute) 필드의 값 뒤에 단위 축약어가 붙은 경우 (예: ``5px``) 이 속성 필드에 지정된 단위를 우선합니다. (이 경우 픽셀 단위를 사용할 것입니다.)
대부분의 경우 속성 필드가 단위 값을 담고 있지 않을 것이라는 사실을 기억하십시오. 속성 필드의 값이 기본 단위를 대체할 수 있는 선택적인 기능일 뿐입니다.

2.3 펜 도구 파라미터
~~~~~~~~~~~~~~~~~~~~~~~

**적용할 수 있는 도형 유형:**

-  포인트:
   포인트에 적용되는 경우, PEN 도구는 그릴 포인트의 색상과 크기만 정의할 수 있습니다.

-  폴리라인:
   가장 당연한 경우입니다.

-  폴리곤:
   폴리곤의 외곽선을 그려야 할 방식을 정의합니다.

다음은 현재 PEN 도구의 파라미터 목록입니다. 이제까지 맞닥뜨렸던 모든 경우들을 다루기에 충분하지만 향후 새로운 유형의 그래픽 표현을 처리하기 위해 새로운 파라미터가 추가될 수도 있습니다. 다시 한번 모든 파라미터가 선택적이라는 사실을 기억하십시오:

- ``c``: **펜 색상**, 16진법으로 표현 (#RRGGBB[AA])

  * [AA]: 마지막 두 자리가 알파 채널 값을 정의합니다. 00이 투명, FF가 불투명입니다. 기본값은 FF(불투명)입니다.
  * 권장 기본값: 흑색(c:#000000)
  * 예시: PEN(c:#FF0000) 또는 PEN(C:#FF0000FF)


- ``w``: **펜 굵기**, 단위(g, px, pt, mm, cm, in)를 가진 숫자형 값으로 표현

  * 권장 기본값: 1픽셀
  * 예시: PEN(c:#FF0000,w:5px), PEN(w:3pt), PEN(w:50g)

- ``p``: **패턴**. 점선을 생성합니다. 펜다운(pen-down)/펜업(pen-up) 거리 목록입니다.

  예시:

  * |style_pen1| = PEN(c:#FF0000,w:2px,p:"4px 5px"): 짧은파선

  * |style_pen2| = PEN(c:#FF0000,w:2px,p:"10px 5px"): 긴파선

  * |style_pen3| = PEN(c:#FF0000,w:2px,p:"10px 5px 4px 5px"): 1점 쇄선

.. |style_pen1| image:: ../../images/style_pen1.png
   :width: 75px
   :height: 15px
.. |style_pen2| image:: ../../images/style_pen2.png
   :width: 75px
   :height: 15px
.. |style_pen3| image:: ../../images/style_pen3.png
   :width: 75px
   :height: 15px

- ``id``: **펜 이름 또는 ID의 쉼표 구분 목록**.
  이름 또는 ID를 가진 펜을 식별하는 시스템 용 파라미터입니다. 대상 시스템이 한 이름을 인식할 때까지 ID 쉼표 구분 목록에서 이름을 스캔합니다. 펜 ID는 (아래에서 설명하는) 시스템 특화 ID일 수도 있고 또는 알려진 선 패턴을 위해 사전 정의된 OGR 펜 ID 가운데 하나일 수도 있습니다. ``id`` 파라미터는 응용 프로그램이 시스템 특화 ID를 이해할 것이라는 가정에 의존하는 일이 없도록 항상 쉼표 구분 목록 마지막에 OGR ID 하나를 포함해야 합니다.

  다음은 현재 OGR 펜 ID 목록입니다(시간이 지나며 늘어날 수 있습니다):

  -  ogr-pen-0: 실선(solid) (ID를 지정하지 않는 경우 기본값입니다)
  -  ogr-pen-1: NULL 펜 (비가시화)
  -  ogr-pen-2: 파선(dash)
  -  ogr-pen-3: 짧은파선(short-dash)
  -  ogr-pen-4: 긴파선(long-dash)
  -  ogr-pen-5: 점선(dot line)
  -  ogr-pen-6: 1점 쇄선(dash-dot line)
  -  ogr-pen-7: 2점 쇄선(dash-dot-dot line)
  -  ogr-pen-8: 대체선(alternate-line) (픽셀마다 설정)

  시스템 특화 ID는 특화 ID를 생성한 특정 시스템에만 의미가 있을 가능성이 높습니다. 특화 ID는 시스템 이름으로 시작해서 대시("-")가 붙고 그 뒤에 해당 시스템에 의미가 있는 어떤 정보든 (숫자, 이름, 파일명 등등) 붙여야 합니다. 예를 들면 "mapinfo-5", "mysoft-lines.sym-123", 또는 "othersystems-funnyline"처럼 말입니다.

  외부 파일에 선 패턴을 저장하거나 자신만의 사전 정의 선 스타일 집합을 가진 시스템의 데이터를 처리하는 경우 (예를 들면 MapInfo MIF 포맷을 TAB으로 손실 없이 변환하려는 경우) 정보 손실을 방지하기 위해 시스템 특화 ID를 사용합니다.

  예시:
 
  - PEN(c:#00FF00,id:"ogr-pen-0") - 단순 실선
  - PEN(c:#00FF00,id:"mapinfo-5,ogr-pen-7") - MapInfo의 5번 펜에 대응하며, MapInfo 펜을 이해하지 못 하는 시스템에서는 기본 "ogr-pen-7"(2점 쇄선)으로 돌아갑니다.

- ``cap``: **펜 끝(Pen Cap)** - 선의 마지막 포인트의 형태를 설정합니다.

  * "cap:b" - 편평(Butt): 선의 마지막이 마지막 포인트를 넘어서지 않습니다. 기본값입니다.
  * "cap:r" - 둥글림(Round): 선의 마지막을 선 굵기가 지름인 원으로 마무리합니다.
  * "cap:p" - 투영(Projecting): 편평과 비슷하지만, 선의 마지막이 마지막 포인트를 선 굵기의 반만큼 넘어섭니다.


- ``j``: **펜 결합(Pen Join)** - 선들의 결합 포인트(꼭짓점)의 형태를 설정합니다.

  * "j:m" - 마이터(Miter): 선들의 외곽 경계가 접할 때까지 늘립니다. 기본값입니다.
  * "j:r" - 둥글림(Rounded): 중심이 결합 포인트이고 지름이 선 굵기인 원호로 선들을 결합합니다.
  * "j:b" - 베벨(Bevel): 편평 끝을 가진 선들을 결합한 다음 결합 위치에 만들어지는 삼각형 홈을 채웁니다.

- ``dp``: **수직 오프셋(Perpendicular Offset)**, 숫자형 값 단위(g, px, pt, mm, cm, in)로 표현됩니다.

  라인 중심으로부터의 오프셋입니다. 음수로 지정하면 주 선분의 왼쪽에 펜을 그리고, 그렇지 않으면 오른쪽에 그릴 것입니다.

- ``l``: **우선 순위 수준(Priority Level)** - 스타일 부분들을 그려야 할 순서를 정의하는 숫자형 값입니다.

  우선 순위가 낮은 스타일 부분을 먼저 그리고, 그 위에 우선 순위가 높은 스타일 부분을 그립니다. 우선 순위 수준을 지정하지 않는 경우 기본값은 1입니다.

2.4 브러시 도구 파라미터
~~~~~~~~~~~~~~~~~~~~~~~~~

**적용할 수 있는 도형 유형:**

-  포인트: 적용할 수 없습니다.
-  폴리라인: 적용할 수 없습니다.
-  폴리곤: 폴리곤의 면을 채울 방식을 정의합니다.

다음은 현재 BRUSH 도구의 파라미터 목록입니다. 다시 한번 향후 새로운 파라미터가 추가될 수도 있으며 모든 파라미터가 선택적이라는 사실을 기억하십시오:

- ``fc``: **브러시 전경색(Brush ForeColor)**, 16진법으로 표현(#RRGGBB[AA])됩니다. 브러시 패턴 자체를 칠하는 데 사용되는 색상입니다.

  * [AA]: 마지막 두 자리가 알파 채널 값을 정의합니다. 00이 투명, FF가 불투명입니다. 기본값은 FF(불투명)입니다.
  * 권장 기본값: 50% 회색 (c:#808080)
  * 예시: BRUSH(fc:#FF0000)

- ``bc``: **브러시 배경색(Brush BackColor)**, 6진법으로 표현(#RRGGBB[AA])됩니다. 브러시 패턴 아래의 면을 칠하는 데 사용되는 색상입니다.

  * [AA]: 마지막 두 자리가 알파 채널 값을 정의합니다. 00이 투명, FF가 불투명입니다. 기본값은 FF(불투명)입니다.
  * 권장 기본값: 투명 (c:#FFFFFF00)
  * 예시: BRUSH(fc:#FF0000,bc:#FFEEDD)

- ``id``: **브러시 이름 또는 브러시 ID**.
  브러시 이름 또는 ID를 쉼표로 구분한 목록입니다. 대상 시스템이 한 이름을 인식할 때까지 ID 쉼표 구분 목록에서 이름을 스캔합니다.

  브러시 ID는 (아래에서 설명하는) 시스템 특화 ID일 수도 있고 또는 잘 알려진 브러시 패턴을 위해 사전 정의된 OGR 브러시 ID 가운데 하나일 수도 있습니다. ``id`` 파라미터는 응용 프로그램이 시스템 특화 ID를 이해할 것이라는 가정에 의존하는 일이 없도록 항상 쉼표 구분 목록 마지막에 OGR ID 하나를 포함해야 합니다.

  다음은 현재 OGR 브러시 ID 목록입니다(시간이 지나며 늘어날 수 있습니다):

  .. image:: ../../images/style_ogr_brush.png

  - ogr-brush-0: 단색(solid) 전경색 (ID를 지정하지 않는 경우 기본값입니다)
  - ogr-brush-1: NULL 브러시 (투명 - 채우지 않음, fc 또는 bc 값을 무시)
  - ogr-brush-2: 수평 해치(hatch)
  - ogr-brush-3: 수직 해치
  - ogr-brush-4: 좌상단-우하단 사선 해치
  - ogr-brush-5: 좌하단-우상단 사선 해치
  - ogr-brush-6: 십자 해치
  - ogr-brush-7: 사선 십자 해치

  펜 ID와 마찬가지로, 시스템 특화 ID는 특화 ID를 생성한 특정 시스템에만 의미가 있을 가능성이 높습니다. 특화 ID는 시스템 이름으로 시작해서 대시("-")가 붙고 그 뒤에 해당 시스템에 의미가 있는 어떤 정보든 (숫자, 이름, 파일명 등등) 붙여야 합니다.

  시스템 특화 브러시 ID에 사용되는 공통 규범은 다음과 같습니다:

  - 윈도우 BMP 패턴의 경우 "bmp-filename.bmp"

  다른 (벡터 심볼, WMF 등등) 규범이 향후 추가될 수도 있습니다.

- ``a``: **각도** - 브러시 패턴에 적용할 (도 단위, 시계 반대 방향) 기울기 각도입니다.

- ``s``: **크기 또는 크기 조정 인자(Size or Scaling Factor)** - 단위가 있거나 없는 숫자형 값입니다.

  단위가 지정된 경우 이 값은 브러시 또는 심볼을 그릴 절대 크기입니다.
  단위가 지정되지 않은 경우 이 값은 심볼의 기본 크기에 상대적인 크기 조정 인자입니다.

- ``dx``, ``dy``: **간격(Spacing)** - 단위(g, px, pt, mm, cm, in)를 가진 숫자형 값으로 표현됩니다.

  포인트 심볼을 사용해서 면을 채우는 경우, 이 값이 포인트 사이의 거리를 정의할 것입니다.
  "dx"는 두 인접 심볼들의 중심 사이의 수평 거리이고 "dy"는 수직 거리입니다.
  기본값은 심볼의 경계 상자 너비를 "dx"로, 높이를 "dy"로 사용하는 것입니다.

- ``l``: **우선 순위 수준(Priority Level)** - 스타일 부분들을 그려야 할 순서를 정의하는 숫자형 값입니다.

  우선 순위가 낮은 스타일 부분을 먼저 그리고, 그 위에 우선 순위가 높은 스타일 부분을 그립니다. 우선 순위 수준을 지정하지 않는 경우 기본값은 1입니다.


2.5 심볼 도구 파라미터
~~~~~~~~~~~~~~~~~~~~~~~~~~

**적용할 수 있는 도형 유형:**

-  포인트: 포인트 위치에 심볼을 배치합니다.
-  폴리라인: 폴리라인을 따라 심볼을 각 꼭짓점에 또는 일정한 간격으로 배치합니다.
-  폴리곤: 심볼을 폴리곤 외곽선에 배치합니다.

다음은 현재 SYMBOL 도구의 파라미터 목록입니다. 다시 한번 향후 새로운 파라미터가 추가될 수도 있으며 모든 파라미터가 선택적이라는 사실을 기억하십시오:

- ``id``: **Symbol Name or Id** - 심볼 이름 또는 ID를 쉼표로 구분한 목록입니다. 대상 시스템이 한 이름을 인식할 때까지 ID 쉼표 구분 목록에서 이름을 스캔합니다.

  심볼 ID는 (아래에서 설명하는) 시스템 특화 ID일 수도 있고 또는 잘 알려진 심볼을 위해 사전 정의된 OGR 심볼 ID 가운데 하나일 수도 있습니다. ``id`` 파라미터는 응용 프로그램이 시스템 특화 ID를 이해할 것이라는 가정에 의존하는 일이 없도록 항상 쉼표 구분 목록 마지막에 OGR ID 하나를 포함해야 합니다.

  다음은 현재 OGR 심볼 ID 목록입니다(시간이 지나며 늘어날 수 있습니다):

  .. image:: ../../images/style_ogr_sym.png

  - ogr-sym-0: 십자(cross) (+)
  - ogr-sym-1: 사선 십자(diagcross) (X)
  - ogr-sym-2: 원(circle) (채우기 없음)
  - ogr-sym-3: 원(circle) (채우기 있음)
  - ogr-sym-4: 정사각형(square) (채우기 없음)
  - ogr-sym-5: 정사각형(square) (채우기 있음)
  - ogr-sym-6: 삼각형(triangle) (채우기 없음)
  - ogr-sym-7: 삼각형(triangle) (채우기 있음)
  - ogr-sym-8: 별표(star) (채우기 없음)
  - ogr-sym-9: 별표(star) (채우기 있음)
  - ogr-sym-10: 수직 막대(vertical bar) (사선 막대를 생성하려면 각도 속성(attribute)을 이용해서 기울이면 됩니다)

  펜 ID와 마찬가지로, 시스템 특화 ID는 특화 ID를 생성한 특정 시스템에만 의미가 있을 가능성이 높습니다. 특화 ID는 시스템 이름으로 시작해서 대시("-")가 붙고 그 뒤에 해당 시스템에 의미가 있는 어떤 정보든 (숫자, 이름, 파일명 등등) 붙여야 합니다.

  시스템 특화 심볼 ID에 사용되는 공통 규범은 다음과 같습니다:

  - 윈도우 BMP 심볼의 경우 "bmp-filename.bmp"
  - 글꼴 심볼의 경우 "font-sym-%d", 이때 '%d'가 글꼴 안의 글리프(glyph) 번호이고 **f** 스타일 필드가 글꼴 계열(font family)을 정의합니다.

  다른 (벡터 심볼, WMF 등등) 규범이 향후 추가될 수도 있습니다.

- ``a``: **각도** - 심볼에 적용할 (도 단위, 시계 반대 방향) 기울기 각도입니다.

- ``c``: **심볼 색상**, 16진법으로 표현 (#RRGGBB[AA])

  * [AA]: 마지막 두 자리가 알파 채널 값을 정의합니다. 00이 투명, FF가 불투명입니다. 기본값은 FF(불투명)입니다.
  * 권장 기본 심볼 색상: 흑색(c:#000000) 
  * 예시: SYMBOL(c:#FF0000)

- ``o``: **심볼 외곽선 색상(Symbol Outline Color)** - 16진법으로 표현됩니다(#RRGGBB[AA]).

  이 파라미터를 설정하는 경우, 심볼 주변에 이 색상의 할로(halo) 또는 경계선을 추가로 그립니다.

- ``s``:  **크기 또는 크기 조정 인자(Size or Scaling Factor)** - 단위가 있거나 없는 숫자형 값입니다.

  단위가 지정된 경우 이 값은 심볼을 그릴 절대 크기입니다.
  단위가 지정되지 않은 경우 이 값은 심볼의 기본 크기에 상대적인 크기 조정 인자입니다.

- ``dx``, ``dy``: **X 및 Y 오프셋** - 단위(g, px, pt, mm, cm, in)를 가진 숫자형 값으로 표현되는 심볼 삽입 포인트입니다.

  포인트 도형에 그리고 폴리라인의 각 꼭짓점에 심볼을 배치합니다.

- ``ds``, ``dp``, ``di``: **간격(Spacing) 파라미터** -  심볼을 단위(g, px, pt, mm, cm, in)를 가진 숫자형 값으로 표현되는 간격으로 라인을 따라 배치합니다.

  * ``ds``: 라인을 따라 심볼을 배치할 때 사용할 간격입니다.
    라인 도형을 가진 피처에 심볼을 적용하면 기본적으로 각 꼭짓점에 배치하지만, "ds"를 설정하면 라인을 따라 일정한 간격으로 심볼을 배치합니다. 이 파라미터는 포인트 도형을 가진 피처에는 아무 영향도 미치지 못 합니다.

  * ``dp``: "ds"와 함께 사용해서 심볼의 중심과 심볼이 배치된 라인 사이의 수직 거리를 지정할 수 있습니다.

  * ``di``: 라인의 시작점으로부터의 시작 오프셋을 지정할 수 있습니다.

  * 예시:

    ::

        SYMBOL(id:123, s:5, di:5px, ds:50px)

- ``l``: **우선 순위 수준(Priority Level)** - 스타일 부분들을 그려야 할 순서를 정의하는 숫자형 값입니다.

  우선 순위가 낮은 스타일 부분을 먼저 그리고, 그 위에 우선 순위가 높은 스타일 부분을 그립니다. 우선 순위 수준을 지정하지 않는 경우 기본값은 1입니다.

- ``f``: **글꼴 이름** - 글꼴 이름을 쉼표로 구분한 목록입니다.

  CSS 'font-family' 속성(property)처럼 작동합니다: 알려진 글꼴 이름을 찾을 때까지 글꼴 이름 목록을 스캔합니다.

  * 예시:

    ::

        SYMBOL(c:#00FF00,s:12pt,id:"font-sym-75,ogr-sym-9",f:"MapInfo_Cartographic")

2.6 라벨 도구 파라미터
~~~~~~~~~~~~~~~~~~~~~~~~~

**적용할 수 있는 도형 유형:**

-  포인트: 포인트 위치에 텍스트 라벨을 배치합니다.
-  폴리라인: 폴리라인을 따라 텍스트 라벨을 배치합니다.
-  폴리곤: 폴리곤 중심점(centroid)에 텍스트 라벨을 배치합니다. 모든 파라미터가 해당 도형이 폴리곤 중심점에 위치한 포인트인 것처럼 작동합니다.

다음은 현재 LABEL 도구의 파라미터 목록입니다. 다시 한번 향후 새로운 파라미터가 추가될 수도 있으며 모든 파라미터가 선택적이라는 사실을 기억하십시오:

- ``f``: **글꼴 이름** - 글꼴 이름을 쉼표로 구분한 목록입니다.

  CSS 'font-family' 속성(property)처럼 작동합니다: 알려진 글꼴 이름을 찾을 때까지 글꼴 이름 목록을 스캔합니다.

  * 예시:

    ::

        LABEL(f:"Noto Sans, Helvetica", s:12pt, t:"Hello World!")

- ``s``: **글꼴 크기** - 단위(g, px, pt, mm, cm, in)를 가진 숫자형 값으로 표현됩니다.

  CAD 분야에서 글꼴 크기 또는 "텍스트 높이"는 글꼴 제작자들이 "캡 높이(cap-height)"라고 부르는 대문자의 높이를 결정합니다. 그러나 조판(typeset), 그래픽 및 지도 제작(cartography) 분야에서 글꼴 크기라고 하면 캡 높이보다 더 높은 글꼴의 "em 높이"를 말합니다. 즉 DXF 파일에서 1인치 높이가 할당된 텍스트가 PDF 파일 또는 MapInfo 맵에서 72포인트 높이인 텍스트보다 더 크게 (거의 45% 더 크게) 보일 것이라는 의미입니다.
  GDAL 벡터 드라이버는 현재 "s:" 스타일 문자열 값을 해당 포맷이 네이티브하게 사용하는 (캡 높이든 em 높이든) 글꼴 크기 측정치로 취급하기 때문에, ogr2ogr 도구 사용 시 텍스트 크기가 부정확하게 출력될 수도 있습니다. 이 파라미터는 향후 사양을 더 명확하게 정의해야 할 대상이 될 수 있습니다.

- ``t``: **텍스트 문자열** - 고정값 문자열일 수도 있고, 또는 속성(attribute) 필드의 값을 가리키는 참조일 수도 있습니다.

  문자열 안에 큰따옴표 또는 백슬래시("\") 문자가 존재하는 경우 그 앞에 백슬래시 문자를 넣어 이스케이프 처리해야 합니다.

  * 예시:

    ::

        LABEL(f:"Arial, Helvetica", s:12pt, t:"Hello World!")
        LABEL(f:"Arial, Helvetica", s:12pt, t:"Hello World with escaped \"quotes\" and \\backslash!")
        LABEL(f:"Arial, Helvetica", s:12pt, t:{text_attribute})

- ``a``: **각도** - (도 단위, 시계 반대 방향) 기울기 각도입니다.

- ``c``: **텍스트 전경색**, 16진법으로 표현 (#RRGGBB[AA])

  권장 기본값: 흑색(c:#000000)

- ``b``: **텍스트 배경색** - 16진법으로 (#RRGGBB[AA]) 표현되는, 라벨 아래 그릴 채우기 상자의 색상입니다. 설정하지 않는 경우 상자를 그리지 않습니다.

- ``o``: **텍스트 외곽선 색상** - 16진법으로 (#RRGGBB[AA]) 표현되는 텍스트 외곽선 (MapInfo 용어로는 할로(halo)) 색상입니다. 설정하지 않는 경우 외곽선을 그리지 않습니다.

- ``h``: **음영 색상** - 16진법으로 (#RRGGBB[AA]) 표현되는 텍스트 음영의 색상입니다. 설정하지 않는 경우 음영을 그리지 않습니다.

- ``w``: **늘리기(Stretch)** - 늘리기 인자는 글꼴의 모든 문자의 너비를 지정한 백분율로 변경합니다.
  예를 들어 150으로 설정하면 글꼴의 모든 문자를 기본 너비의 150%로 늘입니다. 늘리기 인자의 기본값은 100입니다.

- ``m``: **라벨 배치 모드(Label Placement Mode)** - 객체의 도형을 기준으로 텍스트를 그리는 방법을 지정합니다.

  * "m:p" - 기본값입니다. 포인트 또는 폴리라인의 첫 번째 꼭짓점에 단순 라벨을 붙입니다.
  * "m:l" - 폴리라인의 마지막 꼭짓점에 텍스트 라벨을 붙입니다. 이 LABEL 도구에 PEN 도구를 결합해서 폴리라인을 라벨을 가리키는 지시선으로 그릴 수 있습니다.
  * "m:s" - 폴리라인을 따라 텍스트 문자열을 늘입니다. 이때 각 문자 사이의 간격은 일정합니다.
  * "m:m" - 폴리라인의 (총 라인 길이를 기반으로 한) 중앙에 텍스트를 단일 라벨로 배치합니다.
  * "m:w" - 폴리라인에 있는 라인 선분 당 단어 하나씩 배치합니다.
  * "m:h" - 폴리라인에 추가된 텍스트의 모든 단어를 해당 선분에 평행하게 배치합니다. 이때 기준점(anchor point)은 해당 선분의 중앙입니다.
  * "m:a" - 폴리라인에 추가된 텍스트의 모든 단어를 폴리라인의 선분에 맞게 늘인 다음 해당 선분을 따라 배치합니다. 이때 기준점은 해당 선분의 시작점입니다.

- ``p``: **기준 위치(Anchor Position)** - 라벨이 추가된 포인트를 기준으로 라벨 위치를 정의하는 1에서 12까지의 값입니다.

  수직 정렬 모드가 *baseline*, *center*, *top* 및 *bottom* 4개가 있고, 수평 정렬 모드는 *left*, *center* 및 *right* 3개가 있습니다.

  .. image:: ../../images/style_textanchor.png

  현재, 이 값들의 정확한 해석은 (예를 들어 "p:7"으로 설정하는 경우 대문자의 정점이 정렬 포인트 위 또는 아래에 있을지 여부는) 파일 포맷에 따라 달라집니다. 이 파라미터는 향후 사양을 더 명확하게 정의해야 할 대상이 될 수 있습니다.

- ``dx``, ``dy``: **X 및 Y 오프셋** - 단위(g, px, pt, mm, cm, in)를 가진 숫자형 값으로 표현되는 라벨 삽입 포인트입니다.

  포인트 도형에 그리고 폴리라인의 각 꼭짓점에 텍스트를 배치합니다.

- ``dp``: ``dp``: **수직 오프셋(Perpendicular Offset)** - 숫자형 값 단위(g, px, pt, mm, cm, in)로 표현되는, 라인을 따라 배치된 라벨에 적용할 수직 오프셋입니다.

  "dp"는 라벨과 라벨이 배치된 라인 사이의 수직 거리입니다. 음수로 지정하면 주 선분의 왼쪽으로 라벨을 이동시키고, 그렇지 않으면 오른쪽으로 이동시킬 것입니다.

- ``bo``: **볼드체(Bold)** - 굵은 글꼴로 출력하려면 1로 설정합니다. 그렇지 않다면 0으로 설정하거나 파라미터를 생략하십시오.

- ``it``: **이탤릭체(Italic)** - 기울임 글꼴로 출력하려면 1로 설정합니다. 그렇지 않다면 0으로 설정하거나 파라미터를 생략하십시오.

- ``un``: **밑줄(Underline)** - 텍스트에 밑줄을 그으려면 1로 설정합니다. 그렇지 않다면 0으로 설정하거나 파라미터를 생략하십시오.

- ``st``:  **취소선(Strikethrough)** - 텍스트에 취소선을 그으려면 1로 설정합니다. 그렇지 않다면 0으로 설정하거나 파라미터를 생략하십시오.

- ``l``: **우선 순위 수준(Priority Level)** - 스타일 부분들을 그려야 할 순서를 정의하는 숫자형 값입니다.

  우선 순위가 낮은 스타일 부분을 먼저 그리고, 그 위에 우선 순위가 높은 스타일 부분을 그립니다. 우선 순위 수준을 지정하지 않는 경우 기본값은 1입니다.

2.7 스타일 테이블 서식
~~~~~~~~~~~~~~~~~~~~~~~

스타일 테이블을 지원하는 파일 포맷의 경우, 해당 포맷에 사전 정의 스타일을 저장할 것입니다.

스타일 테이블을 지원하지 않는 파일 포맷의 경우, 데이터셋과 동일한 기본명과 .ofs (OGR 피처 스타일) 확장자를 가진 텍스트 파일에 스타일 테이블을 저장할 수 있습니다. ESRI Shapefile 같은 포맷에 적용될 수 있습니다.

다음은 .ofs 파일의 예시입니다:

::

    #OFS-Version: 1.0
    #StyleField: "style"

    DefaultStyle: PEN(c:#000000)
    road:      PEN(c:#FF0000,w:5px)
    lake:      BRUSH(fc:#0000FF);PEN(c:#000000)
    campsite:  SYMBOL(c:#00FF00,id:"points.sym-45,ogr-sym-7")
    label:     LABEL(f:"Times New Roman",s:12pt,t:{text_attribute})

첫 줄이 버전 번호의 서명으로, 반드시 존재해야만 합니다.

두 번째 줄(StyleField: "style")은 해당 레이어에 있는 각 객체의 피처 스타일 문자열이 저장된 속성(attribute) 필드의 이름입니다. 이 줄은 선택적으로, 설정하지 않는 경우 레이어에 있는 모든 객체가 DefaultStyle에 정의된 동일한 스타일을 공유할 것입니다.

세 번째 줄(DefaultStyle:...)은 스타일이 명확하게 지정되지 않은 모든 객체에 기본적으로 적용될 스타일을 정의합니다.

그 다음 줄부터 스타일 정의 목록이 나열됩니다.

2.8 OGR SQL을 사용해서 데이터소스들 간에 스타일을 전송하기
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**OGR_STYLE** 특수 필드를 사용해서 피처 수준 스타일을 추출할 수 있고, 다음 예시와 같은 문법으로 ogr2ogr 유틸리티를 이용해서 데이터소스들 간에 추출한 스타일 문자열을 전송할 수 있습니다:

::

    ogr2ogr -f "ESRI Shapefile" -sql "select *, OGR_STYLE from rivers" rivers.shp rivers.tab

스타일 필드의 길이를 지정하지 않으면 산출 드라이버가 필드 길이를 기본값에 맞춰 절단(truncate)할 수도 있습니다. 따라서 대상 길이를 다음과 같이 직접 지정해줘야 할 수도 있습니다:

::

    ogr2ogr -f "ESRI Shapefile" -sql "select *, CAST(OGR_STYLE AS character(255)) from rivers" rivers.shp rivers.tab

OGR는 OGR_STYLE 필드가 존재하는 경우 사용할 것이며, 스타일 문자열을 프로그램적으로 지정하지 않은 경우 :cpp:func:`OGRFeature::GetStyleString` 함수가 이 필드의 값을 반환할 것입니다.

--------------

3. OGR 지원 클래스
----------------------

:cpp:class:`OGRFeature` 클래스는 피처의 스타일 문자열을 C 스타일 문자열로 대화형 작업하기 위해 사용할 수도 있는 :cpp:func:`OGRFeature::GetStyleString`, :cpp:func:`OGRFeature::SetStyleString` 및 :cpp:func:`OGRFeature::SetStyleStringDirectly` 함수들을 멤버로 가지고 있습니다.
뿐만 아니라 스타일 테이블을 :cpp:class:`OGRStyleTable` 클래스의 인스턴스로 관리하기 위한 :cpp:func:`OGRFeature::GetStyleTable`, :cpp:func:`OGRFeature::SetStyleTable` 및
:cpp:func:`OGRFeature::SetStyleTableDirectly` 함수들도 있습니다.

:cpp:class:`OGRLayer` 및 :cpp:class:`GDALDataset` 클래스도 :cpp:func:`OGRLayer::GetStyleTable`, :cpp:func:`OGRLayer::SetStyleTable` 및 :cpp:func:`OGRLayer::SetStyleTableDirectly` 함수들을 멤버로 가지고 있습니다.

스타일 문자열을 파싱하기 위해 :cpp:class:`OGRStyleMgr` 클래스를 사용합니다. 문자열에 있는 각 스타일 도구를 :cpp:class:`OGRStyleTool` 클래스의 인스턴스로 접근합니다. 마지막으로 각 도구에 대한 도우미 클래스 4개가 각각(:cpp:class:`OGRStylePen`, :cpp:class:`OGRStyleBrush`, :cpp:class:`OGRStyleSymbol`, :cpp:class:`OGRStyleLabel`) 존재합니다. 게터(getter) 및 세터(setter) 멤버 함수가 각 도우미 클래스가 사용할 수 있는 파라미터를 표현합니다. 이 클래스들을 더 잘 이해하고 싶다면 `ogr_featurestyle.h <https://github.com/OSGeo/gdal/blob/master/ogr/ogr_featurestyle.h>`_ 와 `ogrfeaturestyle.cpp <https://github.com/OSGeo/gdal/blob/master/ogr/ogrfeaturestyle.cpp>`_ 코드 파일을 읽어보면 도움이 될 수도 있습니다.

다음은 C++ 코드 예시입니다:

.. code-block:: c++

      OGRStyleTable oStyleTable;

      OGRStyleMgr *poStyleMgr = new OGRStyleMgr(&oStyleTable);

      // 전체 스타일 문자열을 지정해서 스타일 테이블에 새 스타일을 생성

      if (poStyleMgr->AddStyle("@Name","PEN(c:#123456;w:10px);BRUSH(c:#345678)"))
      {
        poStyleMgr->SetFeatureStyleString(poFeature,"@Name",TRUE)
        // 또는
        poStyleMgr->SetFeatureStyleString(poFeature,"PEN(c:#123456,w:10px);BRUSH(c:#345678)",FALSE)
      }

      oStyleTable->SaveStyleTable("ttt.tbl");


      // 각 도구(부분)를 문자열로 지정해서 스타일 테이블에 새 스타일을 생성

      poStyleMgr->InitStyleString();
      poStyleMgr->AddPart("PEN(c:#123456,w:10px)");
      poStyleMgr->AddPart("BRUSH(c:345678)");
      poStyleMgr->AddStyle("@Name");
      poStyleMgr->SetFeatureStyleString(poFeature,"@Name",TRUE);

      oStyleTable->SaveStyleTable("ttt.tbl");


      // 스타일 도구 도우미 클래스를 이용해서 스타일 테이블에 새 스타일을 생성

      OGRStyleTool *poStylePen = new OGRStylePen;

      poStylePen->SetColor("#123456");
      poStylePen->SetUnit(OGRSTUPixel);
      poStylePen->SetWidth(10.0);
      poStyleMgr->AddPart(poStylePen);

      delete poStylePen;


      // 스타일 읽어오기

      OGRStyleTool *poStyleTool;

      poStyleMgr->GetStyleString(poFeature);

      for (int iPart = 0; iPart < poStyleMgr->GetPartCount(); iPart++)
      {
         poStyleTool = GetPart(iPart);
         switch (poStyleTool->GetType())
         {
            case OGRSTCPen:
               poStylePen = (OGRStylePen *)poStyleTool;
               pszColor = poStylePen->Color(bDefault);
               if (bDefault == FALSE)
                 poStylePen->GetRGBFromString(pszColor, nRed, nGreen,
                                          nBlue, nTrans);
               else
                 // 색상 정의되지 않음

               dfWidth = poStylePen->Width(bDefault);
               if (bDefault == FALSE)
                 // Use dfWidth
               else
                 // dfWidth 정의되지 않음

              :
              :
          }
       }


.. only:: html

    개정 이력
    ----------------

    -  **0.016버전 - 2018년 12월 3일 - 앤드루 수도르긴(Andrew Sudorgin)**
       포인트 심볼 용 글꼴 속성 복원 및 문서화
    -  **0.015버전 - 2018년 1월 8일 - 앨런 토마스(Alan Thomas)**
       구식이 된 내용 업데이트; BRUSH 'id' 및 LABEL 't', 'bo', 'it', 'un', 'st'에 사소한 변경; BRUSH 'fc', 'bc', SYMBOL 'o' 및 LABEL 's', 'w', 'p'의 의미 명확화
    -  **0.014버전 - 2011년 7월 24일 - 이벤 루올(Even Rouault)**
       LABEL의 텍스트 문자열에서 큰따옴표 문자 이스케이프 처리에 관한 언급 추가 (ticket #3675)
    -  **0.013버전 - 2008년 7월 29일 - 대니얼 모리셋(Daniel Morissette)**
       포인트 심볼 외곽선 색상 용 'o:' 추가 (ticket #2509)
    -  **0.012버전 - 2008년 7월 21일 - 대니얼 모리셋(Daniel Morissette)**
       텍스트 외곽선 색상 용 'o:' 추가, 'b:'를 라벨 배경 상자 채우기로 업데이트 (ticket #2480)
    -  **0.011버전 - 2008년 2월 28일 - 세케레시 터마시(Szekeres Tamás)**
       데이터소스들 사이에 스타일을 전송하기 위한 OGR SQL에 관한 메모
    -  **0.010버전 - 2006년 9월 23일 - 안드레이 키셀레프(Andrey Kiselev)**
       라벨 스타일 'w', 'st', 'h', 'm:h', 'm:a', 'p:{10,11,12}' 추가
    -  **0.009버전 - 2005년 3월 11일 - 프랑크 바르메르담(Frank Warmerdam)**
       OGRWin에 대한 참조 제거, OGR 배포판으로 이동
    -  **0.008버전 - 2001년 3월 21일 - 프랑크 바르메르담(Frank Warmerdam)**
       몇몇 오타 수정 (예시에서 s:12pt 대신 h:12pt)
    -  **0.008버전 - 2000년 7월 15일 - 스테판 빌뇌브(Stephane Villeneuve)**
       레이어에서 스타일 테이블 제거, 브러시에 전경색 및 배경색 추가
    -  **0.007버전 - 2000년 6월 22일 - 대니얼 모리셋(Daniel Morissette)**
       오타 수정 및 PEN에 offset 파라미터 추가
    -  **0.006버전 - 2000년 6월 20일 - 대니얼 모리셋(Daniel Morissette)**
       OGR-Win 아이디어를 추가하고 이것저것 수정
    -  **0.005버전 - 2000년 6월 12일 - 대니얼 모리셋(Daniel Morissette)**
       PEN의 "id" 파라미터에 이름들의 쉼표 구분 목록 허용
       시스템 독립적인 펜 스타일 이름들 정의
    -  **0.004버전 - 2000년 6월 9일 - 스테판 빌뇌브(Stephane Villeneuve)**
       PEN cap 및 join 파라미터 추가
       API 정의를 좀 더 명확하게 수정
    -  **0.003버전 - 2000년 2월 15일 - 대니얼 모리셋(Daniel Morissette)**
       첫 번째 완성(에 가까운) 버전.
