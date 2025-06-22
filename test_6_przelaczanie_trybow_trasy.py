import asyncio
from modul_strona import odpalanie_strony
from playwright.async_api import async_playwright

async def test_porownanie_trybow_po_wyszukaniu(page):
    await page.wait_for_selector('#search > form > input[type="text"]', timeout=7000)
    await page.fill('#search > form > input[type="text"]', 'Jelenia Góra')
    print("Wpisano 'Jelenia Góra'")

    await page.click('#search > form > button.submit.notranslate')
    print("Kliknięto ikonę lupy")

    await page.wait_for_selector('a:has-text("Trasa")', timeout=10000)
    await page.click('a:has-text("Trasa")')
    print("Kliknięto przycisk 'Trasa'")

    await page.wait_for_selector('input[placeholder="Wskaż początek"]', timeout=7000)
    await page.fill('input[placeholder="Wskaż początek"]', 'Karpacz')
    print("Wpisano 'Karpacz' jako start")

    await page.wait_for_selector('div.route-items-list.unrouted ul li:nth-child(1)', timeout=7000)
    await page.click('div.route-items-list.unrouted ul li:nth-child(1)')
    print("Kliknięto pierwszy element na liście tras")

    await page.wait_for_selector('span.distance', timeout=10000)
    dystans = await page.inner_text('span.distance')
    print("Wyznaczona trasa ma długość:", dystans)

    tryby = [
        "Samochodem",
        "Pieszo",
        "Rowerem",
        "Transportem publicznym"
    ]

    await page.wait_for_selector('button:has(svg > title)', timeout=10000)

    poprzedni_dystans = None
    test_udany = False  

    for tryb in tryby:
        selector = f'button:has(svg > title:text("{tryb}"))'
        print(f"Klikam tryb: {tryb}")
        await page.click(selector)

        await page.wait_for_selector('span.distance', timeout=10000)
        dystans_trybu = await page.inner_text('span.distance')
        print(f"Dystans dla trybu '{tryb}': {dystans_trybu}")

        if poprzedni_dystans is not None:
            if dystans_trybu == poprzedni_dystans:
                print(f"Uwaga! Dystans dla trybu '{tryb}' jest taki sam jak poprzedni: {dystans_trybu}")
            else:
                print(f"Dystans dla trybu '{tryb}' różni się od poprzedniego.")
                test_udany = True
        poprzedni_dystans = dystans_trybu

        await page.wait_for_timeout(1000)

    if test_udany:
        print("Test przeszedł pomyślnie — trasy dla różnych trybów się różnią.")
    else:
        print("Test NIE przeszedł — dystanse dla wszystkich trybów są takie same.")

async def main():
    async with async_playwright() as p:
        context, page = await odpalanie_strony(p)
        try:
            await test_porownanie_trybow_po_wyszukaniu(page)
        finally:
            await context.close()

if __name__ == "__main__":
    asyncio.run(main())
