import pytest

if __name__ == '__main__':
    rc = pytest.main(['-q'])
    print('PYTEST_EXIT_CODE=', rc)
