# 🚀 TANKI - Tank Battle Project

Lokálna multiplayerová prestrelka pre 2 hráčov.
* **Inšpirácia:** Tank Trouble
* **Prostredie:** Náhodne generované bludiská
* **Cieľ:** Eliminácia súpera odrážajúcimi sa strelami

---

## 🎮 Ovládanie

### **Hráč 1 (Zelený)**
* **Pohyb:** `W`, `A`, `S`, `D`
* **Streľba:** `SPACE`

### **Hráč 2 (Červený)**
* **Pohyb:** `Šípky`
* **Streľba:** `RSHIFT`

### **Všeobecné**
* **Menu / Návrat:** `ESC`
* **Potvrdenie:** `ENTER`

---

## ✨ Vlastnosti hry
* **Mapy:** 5 náhodných rozložení z matice
* **Boj:** Projektily s odrazom (max. 3-krát)
* **Riziko:** Možnosť zasiahnuť sám seba po odraze
* **Nastavenia:** Nastaviteľná rýchlosť a počet životov
* **Audio:** Dynamické SFX pre streľbu a zásah

---

## 🔊 Zvukové zdroje (Credits)
* **Shoot SFX:** [https://shorturl.at/ieATP](https://shorturl.at/ieATP)
* **Hit SFX:** [https://shorturl.at/4DBWA](https://shorturl.at/4DBWA)

---

## 🛠 Inštalácia a spustenie
1. **Python 3.x** (vyžadovaný)
2. **Inštalácia knižnice:**
   ```bash
   pip install pygame
3. **Spustenie hry:**
   ```bash
   python __main__.py

---

## 📂 Štruktúra projektu

* `__main__.py` – Hlavný spúšťač aplikácie  
* `game_engine.py` – Jadro hry, spracovanie kolízií a stavov  
* `sprites.py` – Definícia objektov (Tank, Bullet, Wall)  
* `ui.py` – Správa menu, nastavení a HUD rozhrania  
* `constants.py` – Konštanty, farby a matice máp  
* `assets/` – Priečinok pre zvukové súbory (`.wav`, `.mp3`)  

---

## 👥 Tím a príspevky

* **Študent A:** Architektúra, herná slučka, matice máp a kolízie so stenami  
* **Študent B:** Trieda Tank, rotačný pohyb, UI systém a správa životov  
* **Študent C:** Systém streľby, odrazy striel, implementácia audia a dokumentácia  