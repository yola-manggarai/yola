import base64
from html import escape
from pathlib import Path

import streamlit as st

# ---------------------------------------------------------------
# Konfigurasi halaman
# ---------------------------------------------------------------
st.set_page_config(page_title="Profil Saya", page_icon="🦎", layout="centered")

# Simpan foto Anda dengan nama foto.jpg di folder yang sama dengan file ini
GAMBAR_DEFAULT = "foto.jpg"

# ---------------------------------------------------------------
# Background kadal
# Letakkan foto "kadal.jpg" / "kadal.png" di folder yang sama untuk
# memakai foto sendiri. Jika tidak ada, dipakai pola kadal bawaan.
# ---------------------------------------------------------------
KADAL_SVG = """
<svg xmlns='http://www.w3.org/2000/svg' width='220' height='220' viewBox='0 0 220 220'>
  <rect width='220' height='220' fill='#2d5a3d'/>
  <g transform='rotate(-20 110 110)' stroke='#1f3d2a' stroke-width='2'
     stroke-linecap='round' stroke-linejoin='round'>
    <path d='M74 110 C45 110 45 140 15 142' fill='none' stroke-width='9'/>
    <path d='M95 98 L82 80 L70 82 M130 98 L140 80 L152 82
             M95 122 L82 140 L70 138 M130 122 L140 140 L152 138'
          fill='none' stroke-width='6'/>
    <ellipse cx='110' cy='110' rx='38' ry='16' fill='#5aa86b'/>
    <ellipse cx='158' cy='110' rx='16' ry='12' fill='#6dbb7c'/>
    <circle cx='163' cy='106' r='2.5' fill='#000' stroke='none'/>
    <circle cx='163' cy='114' r='2.5' fill='#000' stroke='none'/>
  </g>
</svg>
"""


def muat_background():
    """Kembalikan (css_background, ukuran) untuk gambar kadal."""
    for nama_file, mime in (("kadal.jpg", "jpeg"), ("kadal.jpeg", "jpeg"), ("kadal.png", "png")):
        if Path(nama_file).exists():
            b64 = base64.b64encode(Path(nama_file).read_bytes()).decode()
            return (
                f'url("data:image/{mime};base64,{b64}") no-repeat center center fixed',
                "cover",
            )
    b64 = base64.b64encode(KADAL_SVG.encode()).decode()
    return f'url("data:image/svg+xml;base64,{b64}") repeat', "220px 220px"


BG_KADAL, BG_UKURAN = muat_background()

# ---------------------------------------------------------------
# Dua tema warna:
#   - "awal"    : tampilan gelap (sebelum / saat isian belum lengkap)
#   - "lengkap" : tampilan hijau (saat semua isian terisi)
# ---------------------------------------------------------------
TEMA = {
    "awal": {
        "overlay": "rgba(0,0,0,0.30)",
        "btn_a": "#2f6f8f", "btn_b": "#3fa796", "btn_shadow": "47,111,143",
        "chip_bg": "#e3f2ef", "chip_fg": "#1d6b5f", "chip_border": "#b9e0d8",
        "tag_bg": "#2f6f8f",
        "card_border": "#3fa796",
    },
    "lengkap": {
        "overlay": "rgba(22,163,74,0.30)",
        "btn_a": "#16a34a", "btn_b": "#84cc16", "btn_shadow": "22,163,74",
        "chip_bg": "#fff3c4", "chip_fg": "#8a5a00", "chip_border": "#f5d77a",
        "tag_bg": "#16a34a",
        "card_border": "#16a34a",
    },
}


def terapkan_tema(nama_tema):
    """Pasang CSS sesuai tema yang dipilih."""
    t = TEMA[nama_tema]
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient({t['overlay']}, {t['overlay']}), {BG_KADAL};
            background-size: auto, {BG_UKURAN};
        }}
        header[data-testid="stHeader"] {{ background: transparent; }}
        .block-container {{ padding-top: 2.5rem; max-width: 760px; }}

        .judul {{ text-align: center; color: #ffffff; margin-bottom: 1.5rem;
                  text-shadow: 0 2px 12px rgba(0,0,0,.6); }}
        .judul h1 {{ font-size: 2.4rem; margin: 0; font-weight: 800; }}
        .judul p  {{ margin: .3rem 0 0; font-size: 1.05rem; opacity: .92; }}

        /* Kartu form */
        [data-testid="stForm"] {{
            background: rgba(255,255,255,.88);
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255,255,255,.6);
            border-radius: 20px;
            padding: 1.6rem 1.8rem;
            box-shadow: 0 12px 36px rgba(0,0,0,.28);
        }}
        [data-testid="stForm"] label p {{ color: #1f2d3d; font-weight: 600; }}

        /* Label pilihan hobi */
        [data-baseweb="tag"] {{ background-color: {t['tag_bg']} !important; }}
        [data-baseweb="tag"] span {{ color: #ffffff !important; }}

        /* Tombol */
        [data-testid="stFormSubmitButton"] button {{
            width: 100%;
            background: linear-gradient(90deg, {t['btn_a']}, {t['btn_b']});
            color: #fff; border: none; border-radius: 12px;
            padding: .6rem 0; font-weight: 700; letter-spacing: .3px;
            transition: transform .15s ease, box-shadow .15s ease;
        }}
        [data-testid="stFormSubmitButton"] button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 18px rgba({t['btn_shadow']},.45);
            color: #fff;
        }}

        /* Kartu hasil */
        .st-key-hasil {{
            background: rgba(255,255,255,.92);
            border-radius: 20px;
            border-left: 8px solid {t['card_border']};
            padding: 1.4rem 1.6rem;
            margin-top: 1.4rem;
            box-shadow: 0 12px 36px rgba(0,0,0,.28);
        }}
        .st-key-hasil img {{ border-radius: 16px; box-shadow: 0 6px 16px rgba(0,0,0,.25); }}
        .info-nama {{ font-size: 1.6rem; font-weight: 800; color: #17324d; margin: 0 0 .2rem; }}
        .info-gender {{ color: #4b5f78; margin-bottom: .9rem; font-weight: 500; }}
        .info-cita {{ font-size: 1.1rem; font-weight: 600; color: #17324d; margin: 0 0 .9rem; }}
        .info-label {{ font-size: .8rem; text-transform: uppercase; letter-spacing: 1px;
                       color: #6b7f95; margin-bottom: .35rem; font-weight: 700; }}
        .chip {{ display: inline-block; background: {t['chip_bg']}; color: {t['chip_fg']};
                 padding: .3rem .85rem; border-radius: 999px; margin: 0 .35rem .35rem 0;
                 font-size: .9rem; font-weight: 600; border: 1px solid {t['chip_border']}; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------
# Logika Tema Awal (sebelum submit) & Judul
# ---------------------------------------------------------------
terapkan_tema("awal")

st.markdown(
    """
    <div class="judul">
        <h1>🦎 Profil Saya</h1>
        <p>Isi data diri Anda, lalu lihat hasilnya di bawah</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------
# Form
# ---------------------------------------------------------------
with st.form(key="my_form"):
    nama = st.text_input("Nama Lengkap", placeholder="Masukkan nama lengkap Anda")
    jenis_kelamin = st.radio("Jenis Kelamin", ("Laki-Laki", "Perempuan"), horizontal=True)
    cita_cita = st.text_input("Cita-cita", placeholder="Contoh: Dokter, Pilot, Programmer")
    hobi = st.multiselect(
        "Hobi",
        ["Tour Guide", "Traveling", "Menggambar"],
        placeholder="Pilih satu atau lebih hobi",
    )
    gambar = st.file_uploader("Upload Gambar", type=["png", "jpg", "jpeg"])
    submit = st.form_submit_button(label="Kirim")

# ---------------------------------------------------------------
# Hasil & Logika Tema Setelah Submit
# ---------------------------------------------------------------
if submit:
    lengkap = (
        bool(nama.strip())
        and bool(cita_cita.strip())
        and bool(hobi)
        and gambar is not None
    )

    # Jika semua terisi, timpa dengan tema "lengkap"
    if lengkap:
        terapkan_tema("lengkap")

    if not nama.strip():
        st.warning("Nama lengkap belum diisi.")
    else:
        if lengkap:
            st.success("Semua data terisi lengkap dan berhasil dikirim! 🎉")
        else:
            st.success("Data berhasil dikirim!")
            st.info("Lengkapi nama, cita-cita, hobi, dan gambar untuk mengubah warna tampilan.")

        with st.container(key="hasil"):
            col1, col2 = st.columns([1, 2], gap="large")

            with col1:
                if gambar is not None:
                    st.image(gambar, use_container_width=True)
                elif Path(GAMBAR_DEFAULT).exists():
                    st.image(GAMBAR_DEFAULT, use_container_width=True)
                else:
                    st.info("Belum ada gambar")

            with col2:
                ikon = "👨" if jenis_kelamin == "Laki-Laki" else "👩"
                chips = (
                    "".join(f'<span class="chip">{escape(h)}</span>' for h in hobi)
                    if hobi
                    else "-"
                )
                cita_tampil = escape(cita_cita.strip()) if cita_cita.strip() else "-"
                st.markdown(
                    f"""
                    <p class="info-nama">{escape(nama.strip())}</p>
                    <p class="info-gender">{ikon} {jenis_kelamin}</p>
                    <p class="info-label">Cita-cita</p>
                    <p class="info-cita">🎯 {cita_tampil}</p>
                    <p class="info-label">Hobi</p>
                    <div>{chips}</div>
                    """,
                    unsafe_allow_html=True,
                )