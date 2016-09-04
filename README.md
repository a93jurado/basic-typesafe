## A basic test  of a typesafe library


##### Example of use:
```
    @typesafe
	def test(a:int, b:int) -> int:
		return a + b

	test(2, b=3)

```