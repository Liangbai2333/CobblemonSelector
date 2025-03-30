from nonebot_plugin_htmlrender import get_new_page

from . import config


async def screenshot(route, device_scale_factor=2) -> bytes:
    async with get_new_page(device_scale_factor) as page:
        await page.goto(f"http://localhost:{config.cs_server_port}/{route}")
        image_bytes = await page.locator(".pokemon-start").screenshot(
            type="png",
            timeout=30_000,
        )
        return image_bytes