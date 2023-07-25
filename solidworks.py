import clr

# Add the .NET Core assembly DLL file reference
clr.AddReference(r'SolidworksLaye\bin\Debug\net7.0\SolidworksLayer.dll')

# Now import your C# namespace and class
from SolidworksLayer import ExampleClass

# Call your C# function
result = ExampleClass.HelloWorld("World")
print(result)  # Should print: Hello, World!
