import asyncio
from modul_strona import odpalanie_strony
from playwright.async_api import async_playwright

async def test_moja_lokalizacja(page):
    selector = 'mapy-map-button.map-controls__geolocation'
    await page.wait_for_selector(selector, timeout=5000)

    lokalizacja_button = await page.query_selector(selector)
    if lokalizacja_button and await lokalizacja_button.is_enabled():
        await lokalizacja_button.click()
        print("Kliknięto przycisk lokalizacji")
    else:
        print("Nie można kliknąć przycisku lokalizacji")
        return

    await page.wait_for_timeout(3000)

    try:
        await page.wait_for_selector('.geolocation-mark', timeout=5000)
        print("Znacznik lokalizacji pojawił się na mapie")
    except:
        print("Znacznik lokalizacji NIE pojawił się na mapie")

    url = page.url
    print(f"Obecny URL: {url}")
    if "x=17.0385380" in url and "y=51.1078830" in url:
        print("URL zawiera współrzędne lokalizacji (Wrocław) i cały test przebiegł prawidłowo")
    else:
        print("URL nie zawiera spodziewanych współrzędnych")

    print("Test lokalizacji zakończony")

async def main():
    async with async_playwright() as p:
        context, page = await odpalanie_strony(p)
        await test_moja_lokalizacja(page)
        await context.close()

if __name__ == "__main__":
    asyncio.run(main())
