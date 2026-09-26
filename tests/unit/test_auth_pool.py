import pytest

from xscrape.auth import Account, AuthPool
from xscrape.exceptions import PoolExhaustedError


@pytest.mark.asyncio
async def test_acquire_release():
    pool = AuthPool([Account(name="a", cookies="x=y")])
    acc = await pool.acquire()
    assert acc.name == "a"
    await pool.release(acc)
    acc2 = await pool.acquire()
    assert acc2 is acc


@pytest.mark.asyncio
async def test_pool_exhausted():
    pool = AuthPool([Account(name="a", cookies="x=y")])
    await pool.acquire()
    with pytest.raises(PoolExhaustedError):
        await pool.acquire()
