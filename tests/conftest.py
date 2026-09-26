import pytest 

from xscrape.auth import Account, AuthPool


@pytest.fixture
def fake_pool() -> AuthPool:
    return AuthPool([Account(name="test", cookies="auth_token=x; ct0=y")])
