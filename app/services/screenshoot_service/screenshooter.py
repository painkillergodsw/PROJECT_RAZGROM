import asyncio
from pathlib import Path
from typing import Awaitable, Callable
from urllib.parse import quote

from playwright.async_api import (
    Browser,
    BrowserContext,
    Playwright,
    async_playwright,
)

class Screenshooter:
    def __init__(
        self,
        *,
        workers: int = 5,
        width: int = 800,
        height: int = 600,
        timeout: int = 30_000,
        debug_dir: str | Path | None = None,
        wait_b4_scrn: int = 5000,
        save_callback: callable = None
    ):
        self._wait_b4_scrn = wait_b4_scrn
        self._workers = workers
        self._timeout = timeout
        self._viewport = {
            "width": width,
            "height": height,
        }

        self._debug_dir = Path(debug_dir) if debug_dir else None
        self._save_callback = save_callback

        self._playwright: Playwright | None = None
        self._browser: Browser | None = None
        self._context: BrowserContext | None = None

    async def start(self):
        self._playwright = await async_playwright().start()

        self._browser =  await self._playwright.chromium.launch(
            headless=True,
        )

        self._context =  await self._browser.new_context(
            viewport=self._viewport,
        )

        if self._debug_dir:
            self._debug_dir.mkdir(parents=True, exist_ok=True)

    async def ensure_started(self):
        if self._browser is None:
            await self.start()

    async def close(self):
        if self._browser:
            await self._browser.close()

        if self._playwright:
            await self._playwright.stop()

    async def capture_many(
        self,
        project_id: str,
        to_screenshot: tuple[str],
    ):
        await self.ensure_started()

        semaphore = asyncio.Semaphore(self._workers)

        async def worker(url: str):
            async with semaphore:
                media_path = await self._capture(url, project_id)
                return url, media_path

        results = await asyncio.gather(
            *(
                worker(url)
                for url in to_screenshot
            )
        )
        return dict(results)

    async def _capture(
        self,
        url: str,
        project_id: str,
    ):
        page = await self._context.new_page()
        media_path = None

        try:

            await page.goto(
                url,
                timeout=self._timeout,
            )

            await page.wait_for_timeout(self._wait_b4_scrn)

            png = await page.screenshot(
                type="png",
                full_page=True,
            )

            filename = hash(url)

            if self._save_callback:
                object_name = f"{project_id}/{filename}"
                media_path = await self._save_callback(
                    object_name,
                    png,
                )

            if self._debug_dir:
                path = self._debug_dir / f"{filename}.png"
                path.parent.mkdir(
                    parents=True,
                    exist_ok=True,
                )

                path.write_bytes(png)

            return media_path
        finally:
            await page.close()
