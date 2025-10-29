import sys
import platform
import struct
import os

print('exe:', sys.executable)
print('version:', sys.version)
print('arch:', struct.calcsize('P')*8)
print('platform:', platform.platform())

site_packages = os.path.join(sys.prefix, 'Lib', 'site-packages')
print('site-packages (expected):', site_packages)

pydantic_core_dir = os.path.join(site_packages, 'pydantic_core')
print('pydantic_core dir exists at expected location:', os.path.isdir(pydantic_core_dir))

if os.path.isdir(pydantic_core_dir):
    print('\nListing pydantic_core directory:')
    for name in sorted(os.listdir(pydantic_core_dir)):
        print('  ', name)
else:
    print('\npydantic_core not found at expected location. Searching sys.path for pydantic_core...')
    found = []
    for p in sys.path:
        try:
            candidate = os.path.join(p, 'pydantic_core')
            if os.path.isdir(candidate):
                found.append(candidate)
        except Exception:
            pass
    print('Found pydantic_core directories:', found)

# Try to report installed versions using importlib.metadata
try:
    import importlib.metadata as im
except Exception:
    import importlib_metadata as im

def ver(name):
    try:
        return im.version(name)
    except Exception as e:
        return f'not installed ({e})'

print('\npydantic version:', ver('pydantic'))
print('pydantic-core version:', ver('pydantic-core'))

# Also try to import and show info if possible (will show error if import fails)
print()
try:
    import pydantic
    print('import pydantic OK; file:', getattr(pydantic, '__file__', None))
except Exception as e:
    print('import pydantic raised:', repr(e))

try:
    import pydantic_core
    print('import pydantic_core OK; file:', getattr(pydantic_core, '__file__', None))
except Exception as e:
    print('import pydantic_core raised:', repr(e))
