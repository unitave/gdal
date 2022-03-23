.. _raster.mg4lidar:

================================================================
MG4Lidar -- MrSID/MG4 LiDAR 압축 / 포인트 클라우드 뷰 파일
================================================================

.. shortname:: MG4Lidar

.. build_dependencies:: LIDAR SDK

.. deprecated_driver:: version_targeted_for_removal: 3.5
   env_variable: GDAL_ENABLE_DEPRECATED_DRIVER_MG4LIDAR

이 드라이버는 MrSID/MG4 압축 LiDAR 파일을 래스터 DEM으로서 볼 수 있는 방법을 제공합니다. 변환 작업의 세부 사항은 원하는 셀 크기, 필터 기준, 집계 방법 및 선택적인 기타 몇몇 파라미터에 따라 달라집니다. 이런 이유 때문에, **MrSID/MG4 압축 LiDAR 파일을 읽을 수 있는 최상의 방법은 뷰(.view) 파일에서 이를 참조하는 것입니다. 뷰 파일도 자체 래스터 변환을 파라미터로 제어하기 때문입니다. 이 드라이버는 MG4 파일을 직접 읽을 수 있지만, 기본 래스터화 파라미터를 사용하기 때문에 제대로 된 산출물을 생성하지 못 할 수도 있습니다.** 뷰 파일의 내용은 :ref:`MrSID/MG4 LiDAR View 문서 <mg4lidar_view_point_cloud>` 사양에서 설명하고 있습니다.

MrSID/MG4는 웨이블릿 기반 포인트 클라우드 압축 기술입니다. 용량이 더 작고 공간 색인을 내장하고 있다는 점을 제외하면 LAS 파일과 비슷하다고 할 수 있습니다. 익스텐시스(Extensis) 사가 이 압축 기술을 개발하고 배포합니다. 이 드라이버는 익스텐시스의 DSDK(Decoding Software Development Kit)를 이용해서 MG4 LiDAR 파일 읽기를 지원합니다. **이 DSDK는 무료로 배포되지만, 오픈소스 소프트웨어는 아닙니다. DSDK를 사용하려면 익스텐시스 사에 연락해야 합니다. (이 페이지 마지막에 있는 링크를 참조하십시오.)**

예시 뷰 파일 (View 문서 사양에서 발췌)
-----------------------------------------------------

가능한 한 가장 단순한 .view 파일
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

MG4 파일을 볼 수 있는 가장 단순한 방법은 뷰 파일(.view) 안에 MG4 파일을 다음과 같이 참조시키는 것입니다. 이때 MG4 파일을 가리키는 상대 참조는 MG4 파일이 .view 파일과 같은 디렉터리에 존재해야만 한다는 의미입니다. 어떤 밴드도 명확하게 매핑하고 있지 않기 때문에, 표고뿐인 기본 이미지를 보게 됩니다. 기본적으로 평균을 기반으로 집계합니다. 다시 말해 포인트 2개(또는 그 이상)가 단일 셀 안에 들어오는 경우 포인트 2개의 평균값을 노출시킬 것입니다. 어떤 필터링도 하지 않기 때문에 범주 코드나 반환 숫자에 상관없이 모든 포인트를 수집하게 될 것입니다. 표고의 네이티브 데이터 유형이 "Float64"이기 때문에 밴드를 Float64 데이터 유형으로 노출시킬 것입니다.

::

   <PointCloudView>
      <InputFile>Tetons.sid</InputFile>
   </PointCloudView>

데이터 잘라내기
~~~~~~~~~~~~~~
앞의 예시와 비슷하지만, 선택 옵션인 ClipBox 태그를 이용해서 클라우드를 관통하는 북-남 방향 300미터 길이의 견본(swatch)을 선택합니다. 동-서 방향으로 데이터를 잘라내려면, NOFITLER를 사용하는 대신 그 자리에 명확하게 지정해주면 됩니다. 마찬가지로 Z 방향으로도 잘라낼 수 있습니다.

::

   <PointCloudView>
      <InputFile>Tetons.sid</InputFile>
      <ClipBox>505500 505800 NOFILTER NOFILTER</ClipBox>
   </PointCloudView>

맨땅(bare earth) (최대) DEM으로 노출시키기
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

이번엔 단일 밴드(표고)를 노출시켰지만 "Ground"로 분류된 포인트들만 원한다고 해봅시다. ClassificationFilter 태그로 2라는 값을 -- "Ground" 포인트를 규정하는 ASPRS 포인트 범주 코드를 -- 지정합니다. 또한, 기본 "Mean" 집계 대신 "Max"를 지정합니다. 이렇게 하면 포인트 2개(또는 그 이상)가 단일 셀 안에 들어오는 경우 포인트 2개 가운데 더 큰 표고값을 노출시킵니다.

::

   <PointCloudView>
      <InputFile>E:\ESRIDevSummit2010\Tetons.sid</InputFile>
      <Band> <!-- Max Bare Earth-->
         <Channel>Z</Channel>
         <AggregationMethod>Max</AggregationMethod>
         <ClassificationFilter>2</ClassificationFilter>
      </Band>
   </PointCloudView>

강도 이미지
~~~~~~~~~~~~~~~

포인트 클라우드로부터 강도(intensity) 이미지를 노출시킵니다.

::

   <PointCloudView>
      <InputFile>Tetons.sid</InputFile>
      <Band>
         <!-- All intensities -->
         <Channel>Intensity</Channel>
      </Band>
   </PointCloudView>

RGB 이미지
~~~~~~~~~

일부 포인트 클라우드 이미지는 RGB 데이터를 포함하고 있습니다. 이런 경우, .view 파일에 다음과 같이 작성하면 RGB 데이터를 노출시킬 수 있습니다.

::

   <PointCloudView>
      <InputFile>Grass Lake Small.xyzRGB.sid</InputFile>
      <Band>
         <Channel>Red</Channel>
      </Band>
      <Band>
         <Channel>Green</Channel>
      </Band>
      <Band>
         <Channel>Blue</Channel>
      </Band>
   </PointCloudView>

쓰기 지원 없음
---------------------

이 드라이버는 MG4 파일 쓰기를 지원하지 않습니다.

현재 구현 한계
-------------------------------------

*<InputFile>* 태그를 하나만 지원합니다. 이 태그는 MG4 파일을 참조해야만 합니다.

*<InterpolationMethod>* 태그가 지원하는 옵션은 *<None>*(기본값)뿐입니다. 기본값(데이터 유형의 최대값)이 원하는 값이 아닌 경우 이 태그를 이용해서 NODATA 값을 지정하십시오. 자세한 내용은 View 문서 사양을 참조하십시오.

포맷 오류 및 무결하지 않은 파라미터에 대한 오류 확인이 충분하지 않습니다. 무결하지 않은 항목 가운데 많은 항목들이 조용히 실패할 것입니다.

참고
---------

-  ``gdal/frmts/mrsid_lidar/gdal_MG4Lidar.cpp`` 으로 구현되었습니다.

-  :ref:`MrSID/MG4 LiDAR View 문서 사양 <mg4lidar_view_point_cloud>`

-  `익스텐시스 웹페이지 <http://www.extensis.com/support/developers>`_

.. toctree::
   :maxdepth: 1
   :hidden:

   mg4lidar_view_point_cloud
