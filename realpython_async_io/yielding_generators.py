# https://stackoverflow.com/questions/49005651/how-does-asyncio-actually-work/51116910#51116910
def inner():
  inner_result = yield 2
  print('inner', inner_result)
  return 3


def outer():
  yield 1
  val = yield from inner()
  print('outer', val)
  yield 4


generator = outer()
print("--first call")
print(next(generator))
print("--second call")
print(next(generator))
print("--send")
print(generator.send("abc"))
