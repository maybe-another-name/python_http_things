import contextlib


@contextlib.contextmanager
def make_context():
  print('entering')
  try:
    # can change to open as binary, and then write strings to generate an error w/i context manager
    fo = open("foo2.txt", "wb")
    fo.write(b"File Heading\n")
    print('before yield')
    yield fo
    print('after yield')
  except RuntimeError as err:
    print(f'ERROR: {err}')
  finally:
    print('exiting')
    fo.write('File End\n')
    fo.close()


with make_context() as fo:
  i = 0
  while i < 10:
    print(f'writing {i}')
    fo.write("Line: %s \n" % str(i))
    i += 1
