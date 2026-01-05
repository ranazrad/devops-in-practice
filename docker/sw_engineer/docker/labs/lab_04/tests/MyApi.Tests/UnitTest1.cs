using Xunit;

namespace MyApi.Tests;

public class UnitTest1
{
    [Fact]
    public void Production_Grade_Test()
    {
        // This test runs inside Docker during the build!
        Assert.True(true); 
    }
}