import asyncio
from playwright.async_api import async_playwright, TimeoutError
from modul_strona import odpalanie_strony  # Twój moduł z funkcją odpalanie_strony

async def wpisz_i_pobierz_wyniki(page, zapytanie: str):
    await page.fill('#search > form > input[type="text"]', '')

    # Zapamiętaj tekst pierwszego wyniku przed zmianą
    poprzedni_tekst = ''
    pierwszy_wynik = await page.query_selector('li.item span.text > strong')
    if pierwszy_wynik:
        poprzedni_tekst = (await pierwszy_wynik.inner_text()).strip()

    await page.type('#search > form > input[type="text"]', zapytanie, delay=100)

    try:
        # Czekaj, aż pierwszy wynik się zmieni (tekst będzie inny niż poprzednio)
        await page.wait_for_function(
            f'document.querySelector("li.item span.text > strong") && ' +
            f'document.querySelector("li.item span.text > strong").innerText.trim() != "{poprzedni_tekst}"',
            timeout=10000
        )
    except TimeoutError:
        print(f"Lista wyników dla '{zapytanie}' nie zmieniła się w czasie 10 sekund.")
        return []

    # Pobierz wszystkie wyniki
    elementy = await page.query_selector_all('li.item')
    wyniki = []
    for el in elementy:
        strong = await el.query_selector('span.text > strong')
        nazwa = (await strong.inner_text()).strip() if strong else ''
        em = await el.query_selector('span.text > em')
        adres = (await em.inner_text()).strip() if em else ''
        wyniki.append((nazwa, adres))

    return wyniki

async def main():
    async with async_playwright() as p:
        context, page = await odpalanie_strony(p)

        try:
            wyniki1 = await wpisz_i_pobierz_wyniki(page, "Zoo")
            print(f"Znaleziono {len(wyniki1)} wyników dla 'Zoo':")
            for i, (nazwa, adres) in enumerate(wyniki1, 1):
                print(f"{i}. {nazwa} - {adres}")

            wyniki2 = await wpisz_i_pobierz_wyniki(page, "Zoo Wrocław")
            print(f"\nZnaleziono {len(wyniki2)} wyników dla 'Zoo Wrocław':")
            for i, (nazwa, adres) in enumerate(wyniki2, 1):
                print(f"{i}. {nazwa} - {adres}")

            set1 = set(wyniki1)
            set2 = set(wyniki2)
            wspolne = set1.intersection(set2)
            tylko_wyniki1 = set1 - set2
            tylko_wyniki2 = set2 - set1

            print(f"\nLiczba wyników wspólnych: {len(wspolne)}")
            print(f"Liczba wyników tylko dla 'Zoo': {len(tylko_wyniki1)}")
            print(f"Liczba wyników tylko dla 'Zoo Wrocław': {len(tylko_wyniki2)}")

            if len(tylko_wyniki1) > 0 or len(tylko_wyniki2) > 0:
                print("\n✅ Wyniki wyszukiwania różnią się między frazami, co oznacza, że strona poprawnie wyszukuje różne miejsca.")
            else:
                print("\n⚠️ Wyniki dla obu fraz są identyczne. Może to oznaczać, że wyszukiwarka na stronie nie działa prawidłowo lub frazy nie są rozróżniane.")

        finally:
            await context.close()

if __name__ == "__main__":
    asyncio.run(main())
