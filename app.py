import streamlit as st
import fitz  # PyMuPDF
import tempfile
import os

st.set_page_config(page_title="PDF Záchranářka AI", layout="centered")
st.title("\U0001f9e0 PDF Záchranářka AI")
st.write("Zkusím vytáhnout text a obrázky i z poškozeného PDF.")

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
            st.download_button(
                label="⬇️ Stáhnout extrahovaný text jako TXT",
                data=all_text,
                file_name="extrahovany_text.txt",
                mime="text/plain"
            )

        st.subheader("🖼️ Extrahované obrázky")
        img_count = 0
        for i, page in enumerate(doc):
            images = page.get_images(full=True)
            for img_index, img in enumerate(images):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                img_count += 1
                st.image(image_bytes, caption=f"Stránka {i+1} - Obrázek {img_index+1}", use_column_width=True)

        if img_count == 0:
            st.info("Nebyly nalezeny žádné obrázky.")

    except Exception as e:
        st.error(f"Nepodařilo se načíst PDF: {e}")
    finally:
        os.unlink(tmp_path)
