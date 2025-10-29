try:
    import pydantic_core
    print('pydantic_core imported OK, file=', getattr(pydantic_core, '__file__', None))
except Exception as e:
    import traceback
    traceback.print_exc()
    print('EXCEPTION:', repr(e))

try:
    import pydantic
    print('pydantic imported OK, file=', getattr(pydantic, '__file__', None))
except Exception as e:
    import traceback
    traceback.print_exc()
    print('EXCEPTION:', repr(e))
