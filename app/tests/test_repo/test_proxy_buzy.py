import asyncio
import app.repo as R


async def test_proxy_busy_get():
    assert await R.ProxyBusy.is_free(1)


async def test_proxy_busy_set_get():
    await R.ProxyBusy.add(3)
    assert not await R.ProxyBusy.is_free(3)


async def test_proxy_set_expire(clear_redis):
    assert await R.ProxyBusy.is_free(3)
    await R.ProxyBusy.add(3, 1)
    assert not await R.ProxyBusy.is_free(3)
    await asyncio.sleep(1.2)
    assert await R.ProxyBusy.is_free(3)


async def test_proxy_free():
    await R.ProxyBusy.add(3)
    await R.ProxyBusy.free(3)
    assert await R.ProxyBusy.is_free(3)


async def test_get_all():
    for i in range(1, 15):
        await R.ProxyBusy.add(i)
    result = await R.ProxyBusy.get_all()
    assert len(result) == 14
