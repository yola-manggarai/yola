import streamlit as st
from pathlib import Path

st.title("Contoh Program Streamlit")

# Simpan foto yang Anda kirim dengan nama foto.jpg di folder yang sama dengan file ini
GAMBAR_DEFAULT = "foto.jpg"

with st.form(key="my_form"):
    nama = st.text_input("Nama Lengkap")
    jenis_kelamin = st.radio("Jenis Kelamin", ("Laki-Laki", "Perempuan"))
    hobi = st.multiselect(
        "Hobi",
        ["Tour Guide",  "Traveling", "Menggambar"]
    )
    gambar = st.file_uploader("Upload Gambar", type=["png", "jpg", "jpeg"])
    submit = st.form_submit_button(label="Kirim")

if submit:
    st.success("Data berhasil dikirim!")

    col1, col2 = st.columns([1, 2])

    with col1:
        if gambar is not None:
            st.image(gambar, use_container_width=True)
        elif Path(GAMBAR_DEFAULT).exists():
            st.image(GAMBAR_DEFAULT, use_container_width=True)
        else:
            st.info("Belum ada gambar")

    with col2:
        st.write(f"**Nama:** {nama}")
        st.write(f"**Jenis Kelamin:** {jenis_kelamin}")
        st.write(f"**Hobi:** {', '.join(hobi) if hobi else '-'}")