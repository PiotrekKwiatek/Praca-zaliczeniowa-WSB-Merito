import asyncio
from modul_strona import odpalanie_strony
from playwright.async_api import async_playwright

async def test_wyszukiwanie_trasy(page):
    await page.wait_for_selector('#search > form > input[type="text"]', timeout=7000)
    await page.fill('#search > form > input[type="text"]', 'Zoo Wrocław')
    print("Wpisano 'Zoo Wrocław'")

    await page.click('#search > form > button.submit.notranslate')
    print("Kliknięto ikonę lupy")

    await page.wait_for_selector('a:has-text("Trasa")', timeout=10000)
    await page.click('a:has-text("Trasa")')
    print("Kliknięto przycisk 'Trasa'")

    await page.wait_for_selector('input[placeholder="Wskaż początek"]', timeout=7000)
    await page.fill('input[placeholder="Wskaż początek"]', 'Rynek Wrocław')
    print("Wpisano 'Rynek Wrocław' jako start")

    await page.wait_for_selector('div.route-items-list.unrouted ul li:nth-child(1)', timeout=7000)
    await page.click('div.route-items-list.unrouted ul li:nth-child(1)')
    print("Kliknięto pierwszy element na liście tras")

    await page.wait_for_selector('span.distance', timeout=10000)
    distance_text = await page.inner_text('span.distance')
    print("Wyznaczona trasa ma długość:", distance_text)

async def main():
    async with async_playwright() as p:
        context, page = await odpalanie_strony(p)
        try:
            await test_wyszukiwanie_trasy(page)
        finally:
            await context.close()

if __name__ == "__main__":
    asyncio.run(main())
