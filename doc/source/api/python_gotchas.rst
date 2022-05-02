.. _python_gotchas:

================================================================================
GDAL 및 OGR 파이썬 바인딩에서의 파이썬 Gotcha
================================================================================

이 페이지에서는 파이썬 프로그래머에게 예상치 못 한 방식으로 다가올 수 있는 GDAL 및 OGR 파이썬 바인딩의 면면을 목록화합니다. 사용자가 새로운 `Gotcha <https://en.wikipedia.org/wiki/Gotcha_(programming)>`_ 를 찾았다면 주저하지 말고 이 목록에 추가해주십시오. 그러나 먼저 `gdal-dev 메일링 리스트 <https://lists.osgeo.org/mailman/listinfo/gdal-dev>`_ 에서 논의해볼 것을 권장합니다. 사용자가 문제점을 완전히 이해하고 있는지 그리고 다른 사용자들이 해당 문제점이 예상치 못 한, "파이썬적이지 않은", 또는 많은 파이썬 프로그래머에게 예상치 못 한 방식으로 다가올 수 있는 문제점이라고 동의하는지 확인하기 위해서입니다. 이메일 스레드, 깃허브 티켓, 그리고 다른 추가 정보 소스를 참조하도록 확인해주십시오.

이 목록은 버그를 리포트하는 곳이 아닙니다. 어떤 문제점이 버그라고 확신하는 경우 `티켓을 열고 <https://github.com/OSGeo/gdal/issues>`_ 'gdal-dev'에 문제점을 리포트해주십시오. 그 다음 해당 문제점이 특히 파이썬에 관련되어 있다면 이 문서에 추가하는 것을 고려해보십시오. 일반 GDAL 또는 OGR 관련 문제이고 특별히 파이썬 바인딩 관련 문제점이 아니라면 이 목록에 추가하지 마십시오.

이 목록의 모든 항목이 버그는 아닙니다. 몇몇 항목들은 그냥 GDAL 및 OGR이 작동하는 방식이기 때문에 기존 코드를 뒤엎지 않고서는 쉽게 수정할 수 없습니다. 어떤 항목이 작동하는 방식이 마음에 들지 않고 수정되어야 한다고 생각한다면, 주저하지 말고 'gdal-dev'에서 논의해보고 어떻게 수정할 수 있는지 알아보십시오.

설계된, 또는 이력별 Gotcha
--------------------------

이 항목들은 예상치 못 한 습성들로 GDAL 및 OGR 팀이 버그로 간주하지 않으며, 요구되는 인력/시간 때문에 수정될 가능성이 없는, 또는 수정하는 경우 하위 호환성에 영향을 미칠 수도 있는 등의 항목들입니다.

파이썬 바인딩은 사용자가 ``UseExceptions()`` 를 명확하게 호출하지 않는 한 예외를 선언하지 않는다
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

GDAL 및 OGR 파이썬 바인딩은 기본적으로 오류가 발생하는 경우 예외를 선언하지 않습니다. 그 대신 ``None`` 같은 오류값을 반환하고 ``sys.stdout`` 에 오류 메시지를 작성합니다. 예를 들어 존재하지 않는 데이터셋을 GDAL로 열려 시도하는 경우:

.. code-block::

    >>> from osgeo import gdal
    >>> gdal.Open('C:\\foo.img')
    ERROR 4: 'C:\foo.img does not exist in the file system,
    and is not recognized as a supported dataset name.

    >>>

파이썬에서는 전통적으로 예외를 선언해서 오류를 리포트합니다. ``UseExceptions()`` 함수를 호출하면 GDAL 및 OGR에서 이 습성을 활성화시킬 수 있습니다:

.. code-block::

   >>> from osgeo import gdal
   >>> gdal.UseExceptions()    # Enable exceptions
   >>> gdal.open('C:\\foo.img')
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   RuntimeError: 'C:\foo.img' does not exist in the file system,
   and is not recognized as a supported dataset name.

   >>>

GDAL 팀은 파이썬 프로그래머들이 예외가 기본적으로 활성화되었을 것이라고 예상한다는 사실을 알고 있지만, `하위 호환성을 보전하기 위해 <https://lists.osgeo.org/pipermail/gdal-dev/2010-September/026031.html>`_ 예외를 비활성화시킵니다.

어떤 객체를 삭제한 다음 해당 객체와 관계성을 가졌던 객체를 사용하는 경우 파이썬이 멈춘다
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

다음과 같은 예시가 있다고 해봅시다:

.. code-block::

   >>> from osgeo import gdal
   >>> dataset = gdal.Open('C:\\RandomData.img')
   >>> band = dataset.GetRasterBand(1)
   >>> print(band.Checksum())
   31212

이 예시에서 ``band`` 는 ``band`` 가 작동하려면 ``dataset`` 이 순서대로 할당되어 있어야 하는 ``dataset`` 과 관계를 맺고 있습니다. ``dataset`` 을 삭제한 다음 ``band`` 를 사용하려 시도하는 경우, 파이썬이 멈출 것입니다:

.. code-block::

   >>> from osgeo import gdal
   >>> dataset = gdal.Open('C:\\RandomData.img')
   >>> band = dataset.GetRasterBand(1)
   >>> del dataset           # 파이썬 가비지 수거기(garbage collector)가 데이터셋을 할당 해제시킬 것입니다
   >>> band.GetChecksum()    # 밴드의 데이터셋이 사라졌기 때문에 이 코드가 파이썬을 크래시시킬 것입니다
   < Python crashes >

이 문제는 미묘한 방식으로 나타날 수 있습니다. 예를 들어, 코드 한 줄 안에서 임시 데이터셋 인스턴스를 인스턴스화하려 시도하는 경우 나타날 수 있습니다:

.. code-block::

   >>> from osgeo import gdal
   >>> print(gdal.Open('C:\\RandomData.img').GetRasterBand(1).Checksum())
   < Python crashes >

이 예시에서, ``GetRasterBand()`` 를 호출한 다음 데이터셋 인스턴스가 더 이상 필요하지 않기 때문에 ``Checksum()`` 을 호출하기 *전에* 파이썬이 해당 인스턴스를 할당 해제합니다.

.. code-block::

   >>> from osgeo import gdal
   >>>
   >>> def load_band(data_filename):
   >>>     dataset = gdal.Open(data_filename)
   >>>     return dataset.GetRasterBand(1)
   >>>
   >>> band = load_band('c:\\RandomData.img')
   >>> print(band.Checksum())
   < Python crashes >

이 예시는 앞의 예시와 동일하지만 다르게 보입니다. ``load_band`` 함수에서만 데이터셋 객체를 사용할 수 있고 해당 함수를 떠난 직후 데이터셋을 삭제할 것입니다.

GDAL 및 OGR 객체가 C++로 구현되어 있고 C++을 사용하는 포인터에 객체들 사이의 관계성을 유지/관리하기 때문에 일어나는 문제입니다. 파이썬에서 데이터셋 인스턴스를 삭제할 때, 기저 C++ 객체를 할당 해제하게 됩니다. 그러나 밴드 인스턴스의 기저 C++ 객체는 이런 일이 일어났다는 사실을 모르기 때문에 더 이상 존재하지 않는 C++ 데이터셋 객체를 가리키는 포인터를 담고 있습니다. 이 밴드가 더 이상 존재하지 않는 객체에 접근하려 할 때 프로세스가 크래시되는 것입니다.

GDAL 팀은 이런 설계가 파이썬 프로그래머들이 예상하는 것이 아니라는 사실을 알고 있습니다. 안타깝게도 이 설계는 수정하기 어렵기 때문에 현재로서는 유지될 가능성이 높습니다. 더 자세한 내용을 알고 싶다면 GDAL 팀에 연락을 주십시오.

이 문제는 GDAL 밴드와 데이터셋 객체에만 제한되지 않습니다. 객체들이 서로 관계를 맺는 다른 분야에서도 일어납니다. 안타깝게도 이 문제가 일어나는 경우에 대한 완전한 목록이 없기 때문에, 사용자가 스스로 조심해야 합니다. 알려진 경우 가운데 하나는 OGR ``GetGeometryRef()`` 함수와 관련되어 있습니다:

.. code-block::

   >>> feat = lyr.GetNextFeature()
   >>> geom = feat.GetGeometryRef()     # geom이 C++ 피처 객체가 유지/관리하는 C++ 도형 객체를 가리키는 참조를 담고 있습니다
   >>> del feat                         # C++ 피처 객체 및 그 C++ 도형을 할당 해제합니다
   >>> print(geom.ExportToWkt())        # C++ 도형이 더 이상 존재하지 않기 때문에 크래시가 일어납니다
   < Python crashes >

GDAL 및 OGR API 문서를 자세히 읽어보았다면, "Ref"로 끝나는 함수들이 객체를 새로 복사하는 대신 내부 객체를 가리키는 참조를 얻어온다는 사실을 알고 있을 것입니다. 이 사실이 바로 문제가 일어날 수 있다는 단서입니다. "Ref"로 끝나는 함수를 이용하는 경우 주의하십시오. 또 ``SetGeometryDirectly()`` 처럼 내부 객체의 소유 권한(ownership)을 이전시키는, "Directly"로 끝나는 함수들도 조심하십시오:

.. code-block::

   >>> point = ogr.Geometry(ogr.wkbPoint)
   >>> feature = ogr.Feature(layer_defn)
   >>> feature.SetGeometryDirectly(point)    # C++ 도형의 소유 권한을 포인트로부터 피처로 이전합니다
   >>> del feature                           # 피처가 C++ 도형을 소유하고 있기 때문에 포인트가 내재적으로 무결하지 않게 됩니다
   >>> print(point.ExportToWkt())            # 크래시가 일어납니다
   < Python crashes >

"Ref" 및 "Directly"로 끝나는 함수들의 장점은 복제 객체를 생성할 필요가 없기 때문에 속도가 빠르다는 것입니다. 단점은 사용자가 이런 문제를 조심해야 한다는 것입니다.

.. 다음 줄을 주석 처리하는 이유는 아래 이벤 루올(Even Rouault)의 이메일과 중복되며 아래에서 논의하는 Destroy() 메소드와 관련이 있기 때문입니다.
   앞의 정보는 ​`이벤 루올이 보낸 이메일 <https://lists.osgeo.org/pipermail/gdal-dev/2010-September/026027.html>`_ 을 기반으로 합니다.

어떤 OGR 레이어 정의로부터 파생된 피처가 활성화된 상태에서 해당 레이어에 새 필드를 추가하는 경우 파이썬이 멈춘다
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

예시:

.. code-block::

   >>> feature = lyr.GetNextFeature()
   >>> field_defn = ogr.FieldDefn("foo", ogr.OFTString)
   >>> lyr.CreateField(field_defn)                       # 이제 이 레이어로부터 파생된 기존 피처가 무결하지 않습니다
   >>> feature.DumpReadable()                            # 분할 폴트(segfault)
   < Python crashes >

더 자세한 내용을 알고 싶다면 `#3552 <https://trac.osgeo.org/gdal/ticket/3552>`_ 를 참조하십시오.

``GetNextFeature()`` 를 사용하는 경우 속성 필터(``SetAttributeFilter()``)를 가진 레이어가 필터링된 피처만 반환할 것이다
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

``SetAttributeFilter()`` 에 대한 문서를 자세히 읽어보았다면 ``OGR_L_GetNextFeature()`` 에 관해 조심해야 할 점을 알고 있을 것입니다. 즉 ``GetNextFeature()`` 대신 ``GetFeature()`` 를 사용하는 경우, 레이어에서 필터가 적용되지 않는 피처에 계속 접근해서 작업할 수 있다는 뜻입니다. ``GetFeatureCount()`` 는 필터를 준수해서 필터링된 피처의 정확한 개수를 출력할 것입니다. 하지만  ``GetFeatureCount()`` 를 루프(loop)로 사용하면 미묘한 혼동이 일어날 수 있습니다.
피처에 접근하는 경우 레이어 객체를 반복하거나 ``GetNextFeature()`` 를 사용하는 것이 기본 메소드가 되어야 합니다:

.. code-block::

   >>> lyr = inDataSource.GetLayer()
   >>> lyr.SetAttributeFilter("PIN = '0000200001'")      # 단일 레코드에 대한 유일 필터입니다
   >>> for i in range( 0, lyr.GetFeatureCount() ):
   ...    feat = lyr.GetFeature( i )
   ...    print(feat)                                    # feat 하나를 출력할 것이지만, 레이어에 있는 첫 번째 feat로 필터링된 feat가 아닙니다
   ...

``Destroy()`` 메소드를 담고 있는 특정 객체가 있지만 절대 사용해서는 안 된다
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

``Destroy()`` 메소드를 호출하는 예시를 본 적이 있을 수도 있습니다. `이 예제 <https://www.gis.usu.edu/~chrisg/python/2009/lectures/ospy_slides2.pdf>`_ 의 12페이지에서는 ``Destroy()`` 메소드를 호출하는 경우에 관한 구체적인 조언도 하고 있습니다. 그러나 ​`이벤 루올(Even Rouault)이 보낸 이메일 <https://lists.osgeo.org/pipermail/gdal-dev/2010-September/026027.html>`_ 에 따르면 ``Destroy()`` 메소드를 호출할 필요가 없습니다:

.. code-block::

   > OGR 도형 객체를 다음과 같이 생성해서 내부적으로 이용하는 파이썬 코드가
   > 있습니다:
   > 
   > point = ogr.Geometry(ogr.wkbPoint)
   > 
   > 이 코드가 누출을 방지하기 위해 다음과 같이 이 도형들을 명확하게 삭제해야
   > 하는지, 또는 이 도형들을 그냥 스코프 밖으로 나가게 해서 파이썬의 참조
   > 세기(reference counting) 및 가비지 수거기가 삭제하도록 해야 할까요?
   > 
   > point.Destroy()

   Destroy()를 호출해야 할 이유가 전혀 없습니다. 파이썬 객체가 스코프 밖으로
   나가거나 또는 None으로 할당하는 경우 네이티브 객체를 삭제합니다. 따라서
   기저 C++ 객체를 삭제하는 시기를 제어하고 싶다면 foo.Destroy()를
   foo = None으로 대체하십시오.

   > 제가 지식이 없어 죄송합니다. 특정 상황에서 OGR 도형 객체를 명확하게
   > 삭제'해야 한다고' 말하는 GDAL 예제를 찾았습니다.
   > (https://www.gis.usu.edu/~chrisg/python/2009/lectures/ospy_slides2.pdf,
   > 12페이지를 참조하세요.) 그러나 이외의 다른 예제를 찾을 수가 없습니다.

   구세대 빌드를 사용한다면 Destroy()가 필요할 수도 있겠지만, 확신할 수가
   없군요... 어쩌면 절대로 호출하지 말아야 할지도요... 그러나, 저 예제의
   슬라이드에서도 언급하고 있듯이 Destroy()를 절대로 호출하지 말아야 하는
   상황이 있다는 것도 사실입니다.

데이터셋/데이터소스 저장 및 종료하기
+++++++++++++++++++++++++++++++++++++++

GDAL 래스터 데이터셋 또는 OGR 벡터 데이터소스를 저장하고 종료하려면, 객체를 ``None`` 또는 다른 값으로 설정하거나, 객체를 삭제해서 객체 참조를 해제해야 합니다. 데이터셋 또는 데이터소스 객체의 복사본이 하나 이상 존재하는 경우, 각 복사본을 참조 해제해야 합니다.

다음은 래스터 데이터셋을 생성하고 저장하는 예시입니다:

.. code-block::

   >>> from osgeo import gdal
   >>> driver = gdal.GetDriverByName('GTiff')
   >>> dst_ds = driver.Create('new.tif', 10, 15)
   >>> band = dst_ds.GetRasterBand(1)
   >>> arr = band.ReadAsArray()  # 모든 래스터 값은 0입니다
   >>> arr[2, 4:] = 50  # 일부 데이터를 수정합니다
   >>> band.WriteArray(arr)  # 래스터 파일이 아직 수정되지 않았습니다
   >>> band = None  # 앞에서 언급한 Gotcha를 방지하기 위해 밴드를 참조 해제합니다
   >>> dst_ds = None  # 저장, 종료

래스터 데이터셋에 대한 마지막 참조 해제가 데이터 수정 사항을 작성하고 래스터 파일을 종료합니다. GDAL 블록 캐시가 (일반적으로 40MB) 다 차지 않는 한 ``WriteArray(arr)`` 를 호출해도 디스크에 배열을 작성하지 않습니다.

일부 드라이버를 사용하는 경우 ``FlushCache()`` 를 이용해서 종료하지 않고서도 래스터 데이터셋을 중간에(intermittently) 저장할 수 있습니다. 마찬가지로 ``SyncToDisk()`` 를 이용하면 벡터 데이터셋도 중간에 저장할 수 있습니다. 하지만 이 메소드들 둘 다 디스크에 데이터셋을 작성한다고 보장하지는 않기 때문에, 앞의 예시처럼 참조를 해제하는 편이 낫습니다.

사용자 지정 오류 처리기에서 선언된 예외를 출력하지 않는다
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++

파이썬 바인딩은 사용자가 파이썬 callable()을 오류 처리기로 지정할 수 있게 해줍니다. (`#4993 <https://trac.osgeo.org/gdal/ticket/4993>`_ 을 참조하십시오.) 하지만, 이런 오류 처리기는 개별 스레드에서 호출되는 것으로 보이며 선언되는 모든 예외가 주 스레드로 다시 전송되지 않습니다. (`#5186 <https://trac.osgeo.org/gdal/ticket/5186>`_ 을 참조하십시오.)

따라서 사용자가 `오류는 물론 경고도 출력 <https://gis.stackexchange.com/questions/43404/how-to-detect-a-gdal-ogr-warning/68042>`_ 하고 싶은 경우, 다음과 같은 코드는 작동하지 않습니다:

.. code-block::

    from osgeo import gdal

    def error_handler(err_level, err_no, err_msg):
        if err_level >= gdal.CE_Warning:
            raise RuntimeError(err_level, err_no, err_msg)  # 이 예외가 주 스레드로 다시 전송되지 않습니다!

    if __name__ == '__main__':
        # Test custom error handler
        gdal.PushErrorHandler(error_handler)
        gdal.Error(gdal.CE_Warning, 2, 'test warning message')
        gdal.PopErrorHandler()

그 대신 다음과 같은 코드를 사용할 수 있습니다:

.. code-block::

    from osgeo import gdal

    class GdalErrorHandler(object):
        def __init__(self):
            self.err_level = gdal.CE_None
            self.err_no = 0
            self.err_msg = ''

        def handler(self, err_level, err_no, err_msg):
            self.err_level = err_level
            self.err_no = err_no
            self.err_msg = err_msg

    if __name__ == '__main__':
        err = GdalErrorHandler()
        gdal.PushErrorHandler(err.handler)
        gdal.UseExceptions()  # gdal.CE_Failure 이상의 모든 오류에 예외를 선언할 것입니다

        assert err.err_level == gdal.CE_None, 'the error level starts at 0'

        try:
            # 경고 메시지 처리 예시
            try:
                gdal.Error(gdal.CE_Warning, 8675309, 'Test warning message')
            except Exception:
                raise AssertionError('Operation raised an exception, this should not happen')
            else:
                assert err.err_level == gdal.CE_Warning, (
                    'The handler error level should now be at warning')
                print('Handled error: level={}, no={}, msg={}'.format(
                    err.err_level, err.err_no, err.err_msg))

            # 오류 메시지 처리 예시
            try:
                gdal.Error(gdal.CE_Failure, 42, 'Test error message')
            except Exception as e:
                assert err.err_level == gdal.CE_Failure, (
                    'The handler error level should now be at failure')
                assert err.err_msg == e.args[0], 'raised exception should contain the message'
                print('Handled warning: level={}, no={}, msg={}'.format(
                    err.err_level, err.err_no, err.err_msg))
            else:
                raise AssertionError('Error message was not raised, this should not happen')

        finally:
            gdal.PopErrorHandler()

버그 또는 다른 소프트웨어의 습성으로부터 발생하는 Gotcha
--------------------------------------------------------

사용자가 NumPy를 업그레이드 또는 다운그레이드하는 경우 GDAL 함수에서 파이썬이 멈춘다
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

GDAL 파이썬 바인딩은 대부분 C++로 구현됩니다. NumPy 코어 대부분은 C로 구현됩니다. GDAL 파이썬 바인딩의 C++ 부분은 NumPy의 ABI(Application Binary Interface)를 통해 NumPy의 C 부분과 대화형 작업을 합니다. 이를 위해 NumPy C 구조를 정의하는 NumPy 헤더 파일을 이용해서 GDAL 파이썬 바인딩을 컴파일해야 합니다. 그런데 NumPy 버전에 따라 이 데이터 구조가 달라지는 경우가 있습니다. 이런 일이 발생하는 경우 새로운 NumPy 버전이 바이너리 수준에서 구 버전과 호환되지 않기 때문에 새 NumPy 버전과 작업하기 전에 GDAL 파이썬 바인딩을 다시 컴파일해야만 합니다. 그리고 다시 컴파일하면 아마도 구 버전과는 작동하지 않을 것입니다.

`http://gisinternals.com/sdk.php <http://gisinternals.com/sdk.php>`_ 에 있는 윈도우 패키지 같은 GDAL 파이썬 바인딩의 이전 컴파일 버전을 가져온 경우, 해당 패키지를 컴파일하는 데 어떤 NumPy 버전을 사용했는지 확인하고 사용자 머신에 해당 NumPy 버전을 설치해야 합니다.

ArcGIS 처리 중(in-process) 지리 정보 처리 도구에서 파이썬 바인딩을 성공적으로 사용할 수 없다 (ArcGIS 9.3 이상 버전)
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

ArcGIS에서 사용자 지정 파이썬 기반 지리 정보 처리(geoprocessing) 도구를 생성할 수 있습니다. ArcGIS 10버전까지, 래스터 데이터를 메모리로 쉽게 읽어올 수 있는 방법이 없었습니다. GDAL은 그런 메커니즘을 제공합니다.

ArcGIS 9.3버전부터, ArcGIS 프로세스 (ArcCatalog.exe 또는 ArcMap.exe) 자체에서 또는 개별 python.exe 작업자 프로세스에서 지리 정보 처리 도구를 실행할 수 있습니다. 안타깝게도 ArcGIS는 처리 중(in-process) 도구 실행 방법에 관한 버그를 가지고 있습니다. 따라서 처리 중 도구에서 GDAL을 사용하는 경우, 첫 번째에는 잘 실행될 것이지만 두 번째 실행부터는 ArcGIS 프로세스를 재시작할 때까지 ``TypeError`` 예외를 선언하며 실패할 수도 있습니다. 예를 들면 band.ReadAsArray() 메소드는 다음과 함께 실패합니다:

.. code-block::

    TypeError: in method 'BandRasterIONumpy', argument 1 of type 'GDALRasterBandShadow *'

이것은 ArcGIS의 버그입니다. 완전한 상세 정보 및 권장 해결법을 알고 싶다면 `#3672 <https://trac.osgeo.org/gdal/ticket/3672>`_ 를 참조하십시오.

