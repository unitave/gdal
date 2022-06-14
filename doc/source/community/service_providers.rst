.. _service_providers:

*****************************************************************************
GDAL 서비스 제공자
*****************************************************************************

전세계 기업 및 개인들의 풍요로운 생태계가 GDAL을 개발하고 지원하고 있습니다.

이 페이지에서는 GDAL에 대한 투자를 최대한 활용할 수 있도록 도움을 줄 수 있는 서비스 제공자들의 목록을 제공합니다. 이런 서비스는 여러분이 시작하는 데 도움이 되는 교육 및 기술 지원부터 소프트웨어를 발전시키고 여러분의 기관의 임무 수행에 필수적인 응용 프로그램을 지원하기 위한 전문적인 개발 및 지원 서비스에 이르기까지 다양합니다.


.. note::

   이 목록은 완전하지 않으며, 여기에 목록화되지 않은 다른 서비스 제공자가 여러분의 지역에 있을 가능성이 높습니다. 여러분의 기관이 이 목록에 포함되어야 한다고 생각한다면 이 페이지에 추가해달라는 풀 요청을 제출해주십시오.

.. note::

   우리는 핵심 기여자에게만 제공되는 정보의 정확성, 신뢰성 또는 완전성에 대한 책임을 집니다.

.. only:: html

   .. note::

      서비스 제공자들의 순서는 페이지 불러오기 시 무작위로 지정됩니다.

핵심 기여자
-----------

핵심 기여자(Core Contributor) 기관은 기관 부서에 GDAL 커밋 개발자 그리고/또는 프로젝트 운영 위원회 회원이 있으며, 이들이 소프트웨어의 핵심 개발에 가장 가깝기 때문에 일반적으로 지원을 받기 가장 좋습니다.

이들은 어떤 일이 가능한지 알 수 있고 GDAL에 대한 어떤 개선도 올바른 방법으로 수행되고 향후 소프트웨어에 포함될 것을 보장할 수 있을 정도로 아키텍처를 충분히 파악하고 있습니다.

이들이 여러분이 사용하는 소프트웨어를 작성했기 때문에 여러분이 소프트웨어를 최대한 활용할 수 있도록 도와주리라 신뢰할 수 있습니다.

.. container:: service-provider

  |logo_spatialys|

  .. container:: service-provider-description

      `Spatialys`_ (프랑스)는 이벤 루올이 설립한 회사로 고객에게 GDAL/OGR, PROJ, MapServer, 그리고 QGIS 같은 오픈 소스 지리공간 소프트웨어와 개방형 표준에 대한 최고의 전문 지식을 제공하기 위해 최선을 다하고 있습니다.

기여자
------

이 목록에 있는 기여자 기관은 일반적으로 소프트웨어의 다양한 측면에 대한 수년간의 기여로 인해 GDAL 커뮤니티에 잘 알려져 있기 때문에 GDAL에 대해 지원할 수 있는 매우 좋은 위치에 있는 고급 사용자와 숙련된 통합자(integrator)를 기관 부서의 일원으로 두고 있습니다.

.. container:: service-provider

  목록화된 기여자가 없습니다.


기타 서비스 제공자
------------------

이 카테고리의 서비스 제공자는 GDAL 및 관련 오픈 소스 기술에 대한 서비스를 제공합니다.

.. container:: service-provider

  |logo_faunalia|

  .. container:: service-provider-description

      `Faunalia`_ (이탈리아)는 (특히 QGIS, PostGIS 등등의) 자유-오픈 소스 소프트웨어를 기반으로 GIS 분야에서 15년 이상 활동한 회사입니다. 우리의 주요 고객은 공공 행정, 민간 기업, 협회입니다. Faunalia의 본사는 이탈리아에 있으며 전세계적으로 운영되고 있습니다. Faunalia는 GDAL에 대한 교육 서비스를 제공합니다.

.. container:: service-provider

  |logo_mundialis|

  .. container:: service-provider-description

      `mundialis`_ (독일)는 대용량 지리공간 및 원격탐사 데이터 처리에 특화되어 있습니다. 오픈 소스 지리공간 시스템 GRASS GIS, actinia 및 QGIS에 중점을 둔 mundialis의 서비스는 본사의 프로세스 체인(process chain), 프로젝트 및 맞춤형 솔루션으로 통합되어 있습니다. mundialis는 토지 황폐화 및 토지 이용 변화에 대해 위성, 항공 및 드론 이미지를 분석합니다. GRASS GIS 및 GDAL에 대한 지원 및 교육도 지원합니다.

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
                // 남아 있는 요소 선택...
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
    $('#core-contributors').randomize('div.service-provider');
    $('#contributors').randomize('div.service-provider');
    $('#other-service-providers').randomize('div.service-provider');
  </script>

.. seealso::

   `OSGeo 서비스 제공자 <https://www.osgeo.org/service-providers/>`_ 를 이용해서 GDAL 서비스 제공자를 검색하십시오.

회사를 추가하는 방법
--------------------

:ref:`rfc-79` 문서에서 서비스 제공자 목록에 회사를 추가하는 단계들에 대해서 설명하고 있습니다.

.. ###########
.. 핵심 기여자 - 로고에 최대(너비=200px,높이=200px) 사용
.. ###########

.. _`Spatialys`: http://www.spatialys.com/
.. |logo_spatialys| image:: ../../images/logo-spatialys.png
   :class: img-logos
   :height: 200 px
   :target: `Spatialys`_

.. ###########
.. 기여자      - 로고에 최대(너비=150px,높이=150px) 사용
.. ###########


.. ###########
.. 기타 서비스 제공자 - 로고에 최대(너비=100px,높이=100px) 사용
.. ###########

.. _`Faunalia`: https://www.faunalia.eu/
.. |logo_faunalia| image:: ../../images/logo-faunalia.png
   :class: img-logos
   :width: 100 px
   :target: `Faunalia`_

.. _`mundialis`: https://www.mundialis.de/
.. |logo_mundialis| image:: ../../images/logo-mundialis.png
   :class: img-logos
   :width: 100 px
   :target: `mundialis`_

