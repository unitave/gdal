.. _csharp_usage:

================================================================================
C# 바인딩 사용례 조언
================================================================================

GDAL/OGR 집합에 참조 추가하기
-----------------------------

작성 예정

인터페이스 클래스 사용하기
--------------------------

작성 예정

로컬 검색 경로 수정하기
-----------------------

시스템 PATH를 영구적으로 변경하지 않아도 되도록 런타임 도중 PATH에 폴더를 추가하고 싶다면, C#에서 다음과 같은 방법으로 할 수 있습니다:

.. code-block:: C#

    using System.Runtime.InteropServices;

    ...

    [DllImport("kernel32.dll", CharSet=CharSet.Auto, SetLastError=true)]
    public static extern bool
    SetEnvironmentVariable(string lpName, string lpValue);

    ...

    string GDAL_HOME = @";C:\Program Files\FWTools\bin";  // for example

    string path = Environment.GetEnvironmentVariable("PATH");
    path += ";" + GDAL_HOME;
    SetEnvironmentVariable("PATH", path);

MSDN 문서:

-  `http://msdn2.microsoft.com/en-us/library/ms686206.aspx <http://msdn2.microsoft.com/en-us/library/ms686206.aspx>`_
-  `http://msdn2.microsoft.com/en-us/library/system.environment.setenvironmentvariable.aspx <http://msdn2.microsoft.com/en-us/library/system.environment.setenvironmentvariable.aspx>`_

:program:`SetEnvironmentVariable()` 에 P/Invoke를 호출하는 대신, C# 네이티브 :program:`Environment.SetEnvironmentVariable()` 메소드를 사용할 수 있습니다. 이 메소드에는 두 가지 버전이 있기 때문에, 문서를 자세히 읽어보십시오. P/Invoke를 통해 접근하는 Win32 API 호출과는 달리, :program:`Environment.SetEnvironmentVariable()` 메소드는 프로세스들에 걸쳐 환경을 영구적으로 변경'할 수도' 있는 오버로드를 가지고 있습니다.

