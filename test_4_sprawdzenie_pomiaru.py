import asyncio
from playwright.async_api import async_playwright
from modul_strona import odpalanie_strony

async def pause(ms=1000):
    await asyncio.sleep(ms / 1000)

async def test_mierzenie_odleglosci(page):
    # 1. Kliknij ikonę narzędzi
    await page.wait_for_selector('#map-controls > div.map-controls__bottomToolbar > mapy-map-toggle', timeout=7000)
    await page.click('#map-controls > div.map-controls__bottomToolbar > mapy-map-toggle')
    print("Kliknięto ikonę narzędzi")
    await pause()

    # 2. Wybierz "Mierzenie odległości" (7 opcja)
    await page.wait_for_selector(
        'body > div.ui-popover.toolsMenu__popOver > mapy-mapmenu > mapy-mapmenu-item:nth-child(7)', 
        timeout=7000
    )
    await page.click(
        'body > div.ui-popover.toolsMenu__popOver > mapy-mapmenu > mapy-mapmenu-item:nth-child(7)'
    )
    print("Wybrano 'Mierzenie odległości'")
    await pause()

    # 3. Powiększ mapę dwukrotnie
    for _ in range(2):
        await page.mouse.wheel(delta_x=0, delta_y=-300)
        await pause(500)
    print("Powiększono mapę")

    # 4. Kliknij dwa punkty na mapie
    await page.wait_for_selector('#map > div:nth-child(1) > svg', timeout=7000)
    svg = await page.query_selector('#map > div:nth-child(1) > svg')
    box = await svg.bounding_box()
    if box:
        mid_x = box["width"] / 2
        mid_y = box["height"] / 2
        await svg.click(position={"x": mid_x, "y": mid_y})
        await pause()
        await svg.click(position={"x": mid_x + 120, "y": mid_y + 80})
        print("Kliknięto dwa punkty na mapie")
        await pause()

    # 5. Odczytaj wynik i jednostkę
    await page.wait_for_selector('#distance-meter > div > div.scroll-section > ul > li.distance > strong', timeout=7000)
    dystans = await page.inner_text('#distance-meter > div > div.scroll-section > ul > li.distance > strong')
    jednostka = await page.inner_text('#distance-meter > div > div.scroll-section > ul > li.distance > small.unit')
    print(f"Zmierzoną odległość to: {dystans} {jednostka}")
    await pause(2000)

async def main():
    async with async_playwright() as p:
        context, page = await odpalanie_strony(p)
        try:
            await test_mierzenie_odleglosci(page)
        finally:
            await context.close()

if __name__ == "__main__":
    asyncio.run(main())
