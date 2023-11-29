import asyncio
import app.repo as R


async def test_proxy_busy_get():
    assert not await R.ProxyBuzy.is_busy(1)


async def test_proxy_busy_set_get():
    await R.ProxyBuzy.add(3)
    assert await R.ProxyBuzy.is_busy(3)


async def test_proxy_set_expire():
    assert not await R.ProxyBuzy.is_busy(3)
    await R.ProxyBuzy.add(3, 1)
    assert await R.ProxyBuzy.is_busy(3)
    await asyncio.sleep(1.2)
    assert not await R.ProxyBuzy.is_busy(3)


async def test_proxy_free():
    await R.ProxyBuzy.add(3)
    await R.ProxyBuzy.free(3)
    assert not await R.ProxyBuzy.is_busy(3)


async def test_get_all():
    for i in range(1, 15):
        await R.ProxyBuzy.add(i)
    result = await R.ProxyBuzy.get_all()
    assert len(result) == 14
