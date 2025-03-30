from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.internal.matcher import matcher
from nonebot_plugin_htmlrender import get_new_page


async def screenshot(route, device_scale_factor=2) -> bytes:
    async with get_new_page(device_scale_factor) as page:
        await page.goto(f"http://localhost:8888/{route}")
        image_bytes = await page.locator(".pokemon-start").screenshot(
            type="png",
            timeout=30_000,
        )
        return image_bytes