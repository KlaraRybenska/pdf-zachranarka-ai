import streamlit as st
import deepl
import fitz  # PyMuPDF
import tempfile
import os
import pytesseract
from PIL import Image
import io

# Načtení DeepL API klíče bezpečně z secrets.toml
translator = deepl.Translator(st.secrets["deepl"]["api_key"])

# Nastavení stránky
st.set_page_config(page_title="PDF Záchranářka AI", layout="centered")

# Logo a info
st.image("cat.png", width=250, caption="Záchranářka z galaxie čajové pěny 🪐🍵")
st.title("🧠 PDF Záchranářka AI")
st.write("Zkusím vytáhnout text a obrázky i z poškozeného PDF.")
st.write("Tento program využívá překladač od DeepL, bohužel pouze pro 50 000 znaků/měsíc zdarma. Pokud překlad nefunguje, znaky byly vyčerpány.")
st.write("Vyberte jazyk PDF dokumentu a nahrajte PDF dokument. Poté se zobrazí nejprve přepis v původním jazyce, níže v přeloženém do ČJ. Oba překlady lze stáhnout. Webová aplikace též dovede omezeně přepsat text z obrázků, je-li dobře čitelný.")

# Výběr jazyka OCR
lang_map = {
    "Angličtina (ENG)": "eng",
    "Čeština (CZ)": "ces",
    "Němčina (NJ)": "deu",
    "Francouzština (FJ)": "fra"
}
selected_lang = st.selectbox("Vyber jazyk pro OCR:", list(lang_map.keys()))
lang_code = lang_map[selected_lang]

# Jazykový kód pro DeepL
src_lang_map = {
    "Angličtina (ENG)": "EN",
    "Čeština (CZ)": "CS",
    "Němčina (NJ)": "DE",
    "Francouzština (FJ)": "FR"
}
src_lang = src_lang_map[selected_lang]

# Upload PDF
uploaded_file = st.file_uploader("Nahraj svůj PDF soubor", type=["pdf"], help="Limit souboru závisí na nastavení Streamlitu (standardně 200 MB)")

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    try:
        doc = fitz.open(tmp_path)
        st.success(f"Soubor načten: {len(doc)} stránek")

        st.subheader("📄 Extrahovaný text")
        all_text = ""

        for i, page in enumerate(doc):
            text = page.get_text()
            if text.strip():
                st.markdown(f"**Stránka {i+1}:**")
                st.text(text)
                all_text += f"\n--- Stránka {i+1} ---\n{text}\n"
            else:
                st.markdown(f"*Stránka {i+1} je prázdná nebo bez textu.*")

        if all_text.strip():
            st.download_button("⬇️ Stáhnout extrahovaný text jako TXT", all_text, "extrahovany_text.txt", "text/plain")

            if src_lang != "CS":
                try:
                    result = translator.translate_text(all_text.strip(), source_lang=src_lang, target_lang="CS")
                    st.subheader("🌍 Překlad celého dokumentu")
                    st.text(result.text)
                    st.download_button("⬇️ Stáhnout překlad jako TXT", result.text, "preklad_do_cestiny.txt", "text/plain")
                except Exception as e:
                    st.warning(f"❌ Překlad celého dokumentu se nezdařil: {e}")

        st.subheader("🖼️ Extrahované obrázky + OCR")
        img_count = 0
        ocr_text = ""

        for i, page in enumerate(doc):
            images = page.get_images(full=True)
            for img_index, img in enumerate(images):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                img_count += 1

                st.image(image_bytes, caption=f"Stránka {i+1} - Obrázek {img_index+1}", use_column_width=True)

                image = Image.open(io.BytesIO(image_bytes))
                ocr_result = pytesseract.image_to_string(image, lang=lang_code)

                if ocr_result.strip():
                    st.markdown(f"**OCR výstup pro obrázek {img_index+1} na stránce {i+1}:**")
                    st.text(ocr_result)
                    ocr_text += f"\n--- OCR Stránka {i+1} Obrázek {img_index+1} ---\n{ocr_result}\n"

                    if src_lang != "CS":
                        try:
                            preklad = translator.translate_text(ocr_result.strip(), source_lang=src_lang, target_lang="CS")
                            st.markdown("**Překlad do češtiny:**")
                            st.text(preklad.text)
                        except Exception as e:
                            st.warning(f"Překlad OCR části se nezdařil: {e}")

        if img_count == 0:
            st.info("Nebyly nalezeny žádné obrázky.")

        if ocr_text.strip():
            st.download_button("⬇️ Stáhnout OCR text jako TXT", ocr_text, "ocr_text.txt", "text/plain")

    except Exception as e:
        st.error(f"Nepodařilo se načíst PDF: {e}")
    finally:
        os.unlink(tmp_path)
