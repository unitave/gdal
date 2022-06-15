.. _sponsors:

================================================================================
후원자
================================================================================

GDAL은 다양한 기관들이 그 성공을 위해 자원을 기여하고 있는 진정한 협동 프로젝트입니다. 다음 기관들은 프로젝트의 상태를 유지/관리하고 개선하기 위해 매년 무제한의 자금을 제공하는 추가적인 조치를 취하고 있습니다:

-  골드 레벨:

  .. _gold-sponsors:
  .. container:: horizontal-logos

    .. Note: HTML에서는 무작위 순서로 나타날 것입니다.

    .. container:: horizontal-logo

        .. note: AWS 로고의 정사각형 형태를 다른 로고들과 비교할 때, AWS 로고가 더 커 보이지 않게 하기 위해 너비를 조금 줄여야 했습니다.

        .. image:: ../../images/sponsors/logo-aws.png
           :class: img-logos
           :width: 225 px
           :target: https://aws.amazon.com

    .. container:: horizontal-logo

        .. image:: ../../images/sponsors/logo-esri.png
           :class: img-logos
           :width: 250 px
           :target: https://www.esri.com

    .. container:: horizontal-logo

        .. image:: ../../images/sponsors/logo-maxar.png
           :class: img-logos
           :width: 250 px
           :target: https://www.maxar.com

    .. container:: horizontal-logo

        .. image:: ../../images/sponsors/logo-microsoft.png
           :class: img-logos
           :width: 250 px
           :target: https://www.microsoft.com

    .. container:: horizontal-logo

        .. image:: ../../images/sponsors/logo-planet.png
           :class: img-logos
           :width: 250 px
           :target: https://www.planet.com

-  실버 레벨:

  .. _silver-sponsors:
  .. container:: horizontal-logos

    .. Note: HTML에서는 무작위 순서로 나타날 것입니다.

    .. container:: horizontal-logo

        .. image:: ../../images/sponsors/logo-google.png
           :class: img-logos
           :width: 200 px
           :target: https://www.google.com

    .. container:: horizontal-logo

        .. image:: ../../images/sponsors/logo-safe.png
           :class: img-logos
           :width: 200 px
           :target: https://www.safe.com



-  브론즈 레벨:

  .. _bronze-sponsors:
  .. container:: horizontal-logos

    .. Note: HTML에서는 무작위 순서로 나타날 것입니다.

    .. container:: horizontal-logo

        .. image:: ../../images/sponsors/logo-aerometrex.png
           :class: img-logos
           :width: 150 px
           :target: https://aerometrex.com.au

    .. container:: horizontal-logo

        .. image:: ../../images/sponsors/logo-frontiersi.png
           :class: img-logos
           :width: 150 px
           :target: https://frontiersi.com.au

    .. container:: horizontal-logo

        .. image:: ../../images/sponsors/logo-koordinates.png
           :class: img-logos
           :width: 150 px
           :target: https://www.koordinates.com

    .. container:: horizontal-logo

        .. image:: ../../images/sponsors/logo-l3harris.png
           :class: img-logos
           :width: 150 px
           :target: https://www.l3harrisgeospatial.com

    .. container:: horizontal-logo

        .. image:: ../../images/sponsors/logo-mapgears.png
           :class: img-logos
           :width: 150 px
           :target: https://www.mapgears.com

    .. container:: horizontal-logo

        .. image:: ../../images/sponsors/logo-sparkgeo.png
           :class: img-logos
           :width: 150 px
           :target: https://www.sparkgeo.com


-  지원자 레벻:

  .. _supporter-sponsors:
  .. container:: horizontal-logos

    .. container:: horizontal-logo

        마일스 서덜랜드(Myles Sutherland)

    .. container:: horizontal-logo

        `Kaplan Open Source Consulting <https://kaplanopensource.co.il/>`_

    .. container:: horizontal-logo

        `Space Intelligence <https://www.space-intelligence.com>`_

    .. container:: horizontal-logo

        `Umbra <https://umbra.space/>`_

.. raw:: html

   <script type="text/javascript">
    // 무작위 로고
    $.fn.randomize = function(selector){
        var $elems = selector ? $(this).find(selector) : $(this).children(),
            $parents = $elems.parent();

        // https://stackoverflow.com/questions/2450954/how-to-randomize-shuffle-a-javascript-array/2450976#2450976
        // 에서 찾은 함수
        function shuffle(array) {
            var currentIndex = array.length, temporaryValue, randomIndex;
            // 뒤섞을 요소가 남아 있는 동안...
            while (0 !== currentIndex) {
                // Pick a remaining element...
                randomIndex = Math.floor(Math.random() * currentIndex);
                currentIndex -= 1;

                // 그리고 현재 요소와 뒤바꾸기
                temporaryValue = array[currentIndex];
                array[currentIndex] = array[randomIndex];
                array[randomIndex] = temporaryValue;
            }
            return array;
        }

        $parents.each(function(){
            var elements = $(this).children(selector);
            shuffle(elements);
            $(this).append(elements);
        });

        return this;
    };
    $('#gold-sponsors').randomize('div.horizontal-logo');
    $('#silver-sponsors').randomize('div.horizontal-logo');
    $('#bronze-sponsors').randomize('div.horizontal-logo');
    $('#supporter-sponsors').randomize('div.horizontal-logo');

   </script>

GDAL 프로젝트는 `OSGeo <https://www.osgeo.org>`_ 가 호스팅하고 있으며, 오픈 소스 과학 컴퓨팅 커뮤니티 지원에 전념하는 비영리 단체 `NumFOCUS <https://numfocus.org>`_ 의 제정 지원 프로젝트입니다. 여러분이 GDAL을 좋아하고 GDAL의 사명을 지원하고자 한다면 `기부 <https://numfocus.org/donate-to-gdal>`_ 를 통해 우리의 노력을 지원하는 것을 고려해주십시오.

NumFOCUS는 미국의 501(c)(3) 비영리 자선 단체입니다. 즉 NumFOCUS에 기부하면 법에 따라 세금을 감면받을 수 있습니다. 여느 기부와 마찬가지로, 여러분만의 세금 상황에 관해 개인 세무 고문 또는 IRS와 상담해야 합니다.

.. container:: horizontal-logos

    .. container:: horizontal-logo

        .. image:: ../../images/logo-osgeo.png
           :class: img-logos
           :width: 150 px
           :target: https://www.osgeo.org

    .. container:: horizontal-logo

        .. image:: ../../images/logo-numfocus.png
           :class: img-logos
           :width: 150 px
           :target: https://numfocus.org

후원
----

여러분의 조직이 GDAL의 혜택을 보고 있다면 앞의 후원자 그룹에 가입해서 "선행을 나누고(pay it forward)" 프로젝트가 건전성을 유지하고 성장시킬 수 있는 자원을 가지고 있는지 확인해볼 것을 권장합니다. 다양한 레벨의 후원자가 되면 받을 수 있는 혜택에 대해 알아보려면 `지속 가능한 GDAL 후원 안내서`_ 로부터 시작하십시오.
관심이 있거나, 주요 의사 결정권자를 설득하는 데 도움이 필요하거나, 질문이 있는 경우 주저하지 말고 gdal-sponsors@osgeo.org 로 연락을 주십시오.

관련 자원
---------

- `지속 가능한 GDAL 후원 안내서`_.
- :ref:`후원에 대해 자주 받는 질문(FAQ) <sponsoring-faq>`.

.. PDF의 소스는 https://docs.google.com/document/d/1yhMWeI_LgEXPUkngqOitqcKfp7ov6WsS41v5ulz-kd0/edit# 에 있습니다.

.. _지속 가능한 GDAL 후원 안내서: https://gdal.org/sponsors/Sustainable%20GDAL%20Sponsorship%20Prospectus.pdf

..
    개발자 메모: "make html"에는 index.html 파일로부터 테이블을 숨기는 꼼수가 포함되어 있습니다. 최상위 index.html에 해당 페이지들을 목록화할 수 있도록 가시화 상태를 유지해야 합니다.

.. toctree::
   :maxdepth: 0

   faq

