from playwright.async_api import TimeoutError

async def odpalanie_strony(p):
    context = await p.chromium.launch_persistent_context(
        user_data_dir="/tmp/playwright",
        headless=True,
        locale="pl-PL",
        permissions=["geolocation"],
        geolocation={"latitude": 51.107883, "longitude": 17.038538},
    )

    page = context.pages[0] if context.pages else await context.new_page()
    await page.goto("https://mapy.com/pl/")

    try:
        await page.wait_for_selector('button[data-testid="button-agree"]', timeout=5000)
        await page.click('button[data-testid="button-agree"]')
        await page.wait_for_timeout(1000)
        print("Przycisk cookies został kliknięty i zniknął")
    except TimeoutError:
        print("Przycisk cookies nie był widoczny, pomijam")

    try:
        strona = await page.wait_for_selector('//*[@id="mapycz"]', timeout=5000)
        if await strona.is_visible():
            print("Strona jest widoczna")
        else:
            print("Strona się nie załadowała")
    except TimeoutError:
        print("Nie udało się znaleźć elementu z mapą")

    return context, page
