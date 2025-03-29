# 🧠 PDF Záchranářka AI

Chytrá aplikace pro extrakci textu a obrázků z PDF dokumentů s podporou OCR a překladu pomocí DeepL.  
Užitečný nástroj pro humanitní vědy, archivnictví, výuku nebo výzkum.

![logo](cat.png)

---

## 🔧 Co aplikace umí:

- 📄 Extrahuje text z PDF (včetně poškozených dokumentů)
- 🖼️ Rozpoznává text z vložených obrázků (OCR pomocí Tesseract)
- 🌍 Překládá text do češtiny pomocí **DeepL API**
- 📥 Nabízí stažení všech výstupů jako `.txt`
- 🧪 Připraveno pro budoucí integraci HTR (Kraken, Transkribus...)

---

## 🌐 Podporované jazyky

- Angličtina (ENG)
- Čeština (CZ)
- Němčina (NJ)
- Francouzština (FJ)

> 🔤 Překlad probíhá do češtiny (CS), pokud originál není v češtině.

---

## 🚀 Jak spustit lokálně

1. **Naklonuj repozitář:**
```bash
git clone https://github.com/TVOJE-REPO/pdf-zachranarka.git
cd pdf-zachranarka
```

2. **Nainstaluj závislosti:**
```bash
pip install -r requirements.txt
```

3. **Vytvoř složku `.streamlit` a uvnitř soubor `secrets.toml`:**

```
.streamlit/secrets.toml
```

A vlož svůj DeepL API klíč:
```toml
[deepl]
api_key = "TVUJ-DEEPL-KLIC"
```

4. **Spusť aplikaci:**
```bash
streamlit run app.py
```

---
☁️ Nasazení na Streamlit Cloud (https://streamlit.io/cloud)

Nahraj repozitář na GitHub.

Přihlas se do Streamlit Cloud a propoj svůj repozitář.

V Settings → Secrets přidej proměnnou:

[deepl]
api_key = "TVUJ-DEEPL-KLIC"

V Settings → Advanced nastav Python version = 3.10 (nebo podle potřeby).

To je vše – aplikace poběží online bez nutnosti nahrávat secrets.toml!

---

## 📁 Struktura projektu

```
pdf-zachranarka/
├── app.py
├── cat.png
├── requirements.txt
├── README.md
├── .gitignore
└── .streamlit/
    └── secrets.toml
```

---

## ⚠️ Bezpečnost

- API klíč **nikdy neukládej veřejně** do repozitáře.
- `.streamlit/secrets.toml` je v `.gitignore`, takže zůstane soukromý.
- Bezplatný tarif DeepL má **limit 50 000 znaků/měsíc**.

---

## 💡 Autor

Tento projekt vytvořila **Klára Rybenská** ❤️  
S podporou 🧠 ChatGPT jako vývojového partnera.

---

## ✨ Budoucí rozšíření

- 📜 Integrace HTR (Kraken, TrOCR, Transkribus)
- 🧠 Trénování vlastního modelu pro historickou češtinu
- ☁️ Nasazení na Streamlit Cloud pro online přístup

> Děkujeme, že zachraňujete PDFka s námi! 🚀

