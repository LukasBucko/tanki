# TANKI - Tank Battle Project
Jednoduchá lokálna multiplayerová hra pre dvoch hráčov inšpirovaná klasikou Tank Trouble. Hráči ovládajú tanky v náhodne generovanom bludisku, strieľajú odrážajúce sa projektily a snažia sa eliminovať súpera.
# Ovládanie
Hra je určená pre dvoch hráčov na jednej klávesnici:
Hráč 1 (Zelený tank)
Pohyb: W, A, S, D
Streľba: Medzerník (SPACE)
Hráč 2 (Červený tank)
Pohyb: Šípky (Hore, Dole, Vľavo, Vpravo)
Streľba: Pravý Shift (RSHIFT)
Všeobecné
Menu / Návrat: ESC
Potvrdenie v menu: ENTER
# Vlastnosti hry
Náhodné mapy: Hra obsahuje 5 rôznych máp generovaných z matice.
Bojový systém: Projektily sa odrážajú od stien (max. 3 odrazy). Tank sa môže zničiť aj vlastnou strelou po odraze.
Nastavenia: V menu je možné upraviť rýchlosť tankov a počet životov pre danú hru.
Dynamické SFX: Zvukové efekty pri streľbe a zásahu súpera.
🛠 Inštalácia a spustenie
Uisti sa, že máš nainštalovaný Python 3.x.
Nainštaluj knižnicu Pygame:
code
Bash
pip install pygame
Spusti hru pomocou hlavného súboru:
code
Bash
python __main__.py
# Štruktúra projektu
__main__.py - Vstupný bod aplikácie.
game_engine.py - Hlavná herná logika, spracovanie kolízií a stavov hry.
sprites.py - Definícia tried pre Tank, Projektil a Stenu.
ui.py - Vykresľovanie menu, nastavení a herného rozhrania (HUD).
constants.py - Konštanty, farby a definície máp.
assets/ - Priečinok so zvukovými efektmi (.wav/.mp3).
# Tím a príspevky
Tento projekt vznikol v rámci tímovej spolupráce:
Študent A (Architektúra & Mapy): Návrh hernej slučky, systém stavov (Menu/Hra), generovanie máp z matice a kolízie so stenami.
Študent B (Objekty & UI): Implementácia triedy Tank, plynulý rotačný pohyb, tvorba používateľského rozhrania a systému životov.
Študent C (Bojový systém & Audio): Implementácia systému striel (odrazy, kolízie), integrácia zvukových efektov a finálna dokumentácia.