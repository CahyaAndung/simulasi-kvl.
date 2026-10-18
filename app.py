
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Arc, Rectangle

# =========================================================
# KONFIGURASI HALAMAN
# =========================================================
st.set_page_config(
    page_title="Simulasi KVL | RLC Seri AC",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# DESAIN PUTIH MINIMALIS
# =========================================================
st.markdown("""
<style>
    .stApp {
        background: #ffffff;
        color: #172b4d;
    }
    [data-testid="stHeader"] {
        background: rgba(255,255,255,0.96);
    }
    [data-testid="stSidebar"] {
        background: #f5f8fc;
        border-right: 1px solid #e2e8f0;
    }
    h1, h2, h3 {
        color: #163a63 !important;
        letter-spacing: -0.3px;
    }
    p, label, li {
        color: #334155;
    }
    [data-testid="stMetric"] {
        background: #f7faff;
        border: 1px solid #dbe7f3;
        border-radius: 10px;
        padding: 14px 16px;
    }
    [data-testid="stMetricLabel"] {
        color: #52657a;
    }
    [data-testid="stMetricValue"] {
        color: #1261a0;
    }
    div[data-testid="stAlert"] {
        border-radius: 9px;
    }
    .section-note {
        color: #64748b;
        font-size: 0.92rem;
    }
    hr {
        border-color: #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================
st.title("Simulasi Hukum Kirchhoff II")
st.markdown(
    "### Rangkaian RLC Seri — Arus Bolak-Balik (AC)"
)
st.markdown(
    '<p class="section-note">'
    'Laboratorium virtual untuk mempelajari impedansi, '
    'arus AC, tegangan komponen, diagram fasor, dan '
    'Hukum Kirchhoff II.'
    '</p>',
    unsafe_allow_html=True,
)
st.divider()

# =========================================================
# INPUT PARAMETER
# =========================================================
with st.sidebar:
    st.markdown("## Parameter rangkaian")
    st.caption("Ubah nilai untuk memperbarui simulasi.")

    Vs = st.number_input(
        "Tegangan sumber RMS (V)",
        min_value=0.1,
        max_value=500.0,
        value=12.0,
        step=1.0,
    )

    f = st.number_input(
        "Frekuensi (Hz)",
        min_value=1.0,
        max_value=10000.0,
        value=50.0,
        step=1.0,
    )

    R = st.number_input(
        "Resistansi R (Ω)",
        min_value=0.1,
        max_value=100000.0,
        value=30.0,
        step=1.0,
    )

    L_mH = st.number_input(
        "Induktansi L (mH)",
        min_value=0.1,
        max_value=100000.0,
        value=100.0,
        step=10.0,
    )

    C_uF = st.number_input(
        "Kapasitansi C (µF)",
        min_value=0.1,
        max_value=1000000.0,
        value=100.0,
        step=10.0,
    )

    st.divider()
    st.markdown("**Satuan**")
    st.caption("L dimasukkan dalam mH dan C dalam µF.")
    st.caption("Semua hasil tegangan dan arus utama menggunakan nilai RMS.")

# =========================================================
# PERHITUNGAN RLC SERI
# =========================================================
L = L_mH * 1e-3
C = C_uF * 1e-6
omega = 2 * np.pi * f

XL = omega * L
XC = 1 / (omega * C)
X = XL - XC

Z = np.sqrt(R**2 + X**2)
phi_rad = np.arctan2(X, R)
phi_deg = np.degrees(phi_rad)

I_rms = Vs / Z
I_peak = np.sqrt(2) * I_rms

VR = I_rms * R
VL = I_rms * XL
VC = I_rms * XC

power_factor = np.cos(phi_rad)
P = I_rms**2 * R
Q = I_rms**2 * X
S_apparent = Vs * I_rms

f_res = 1 / (2 * np.pi * np.sqrt(L * C))

# =========================================================
# RINGKASAN HASIL
# =========================================================
st.subheader("1. Ringkasan hasil")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Arus RMS", f"{I_rms:.4f} A")
c2.metric("Impedansi total", f"{Z:.3f} Ω")
c3.metric("Sudut fase", f"{phi_deg:.2f}°")
c4.metric("Faktor daya", f"{power_factor:.4f}")

c1, c2, c3 = st.columns(3)
c1.metric("Reaktansi induktif XL", f"{XL:.3f} Ω")
c2.metric("Reaktansi kapasitif XC", f"{XC:.3f} Ω")
c3.metric("Reaktansi total X", f"{X:.3f} Ω")

c1, c2, c3 = st.columns(3)
c1.metric("Tegangan resistor VR", f"{VR:.3f} V")
c2.metric("Tegangan induktor VL", f"{VL:.3f} V")
c3.metric("Tegangan kapasitor VC", f"{VC:.3f} V")

# =========================================================
# GAMBAR SKEMA RANGKAIAN
# =========================================================
st.divider()
st.subheader("2. Skema rangkaian RLC seri AC")
st.caption(
    "Skema menunjukkan hubungan seri antara sumber AC, "
    "resistor, induktor, dan kapasitor."
)

fig, ax = plt.subplots(figsize=(12, 4.2))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")
ax.set_xlim(0, 12)
ax.set_ylim(0, 5)
ax.axis("off")

wire = "#334155"
blue = "#1769aa"
red = "#d94841"
purple = "#7c3aed"
orange = "#d97706"

# Sumber AC di sisi kiri
source_center = (1.2, 2.5)
ax.plot([1.2, 1.2], [3.15, 3.8], color=wire, lw=2)
ax.plot([1.2, 1.2], [1.2, 1.85], color=wire, lw=2)
ax.add_patch(Circle(source_center, 0.65, fill=False, ec=blue, lw=2.2))
theta = np.linspace(-np.pi, np.pi, 150)
ax.plot(
    1.2 + 0.42 * theta / np.pi,
    2.5 + 0.23 * np.sin(theta),
    color=blue,
    lw=1.8,
)
ax.text(0.25, 2.5, "AC", ha="center", va="center",
        color=blue, fontsize=10)
ax.text(1.2, 3.95, f"Vs = {Vs:g} V RMS",
        ha="center", fontsize=10, color="#172b4d")

# Kabel atas dan bawah
ax.plot([1.2, 2.0], [3.8, 3.8], color=wire, lw=2)
ax.plot([3.7, 4.45], [3.8, 3.8], color=wire, lw=2)
ax.plot([6.25, 7.1], [3.8, 3.8], color=wire, lw=2)
ax.plot([7.75, 8.4], [3.8, 3.8], color=wire, lw=2)
ax.plot([9.7, 10.8], [3.8, 3.8], color=wire, lw=2)
ax.plot([10.8, 10.8], [3.8, 1.2], color=wire, lw=2)
ax.plot([10.8, 1.2], [1.2, 1.2], color=wire, lw=2)

# Resistor zigzag standar
rz_x = [2.0, 2.18, 2.42, 2.66, 2.90, 3.14, 3.38, 3.7]
rz_y = [3.8, 4.08, 3.52, 4.08, 3.52, 4.08, 3.52, 3.8]
ax.plot(rz_x, rz_y, color=red, lw=2.2)
ax.text(2.85, 4.35, f"R = {R:g} Ω",
        ha="center", color=red, fontsize=10)

# Induktor dengan lilitan setengah lingkaran
coil_start = 4.45
coil_width = 0.45
n_coils = 4
for j in range(n_coils):
    center_x = coil_start + coil_width * (j + 0.5)
    ax.add_patch(
        Arc(
            (center_x, 3.8),
            width=coil_width,
            height=0.55,
            theta1=0,
            theta2=180,
            ec=purple,
            lw=2.1,
        )
    )
ax.text(5.35, 4.35, f"L = {L_mH:g} mH",
        ha="center", color=purple, fontsize=10)

# Kapasitor dengan dua pelat
ax.plot([7.1, 7.35], [3.8, 3.8], color=wire, lw=2)
ax.plot([7.35, 7.35], [3.43, 4.17], color=orange, lw=3)
ax.plot([7.75, 7.75], [3.43, 4.17], color=orange, lw=3)
ax.text(7.55, 4.45, f"C = {C_uF:g} µF",
        ha="center", color=orange, fontsize=10)

# Panah arus pada kabel atas
ax.annotate(
    "",
    xy=(9.55, 4.1),
    xytext=(8.65, 4.1),
    arrowprops=dict(arrowstyle="->", color=blue, lw=2),
)
ax.text(9.1, 4.35, f"I = {I_rms:.3f} A RMS",
        ha="center", color=blue, fontsize=10)

# Label arah loop
ax.text(6, 0.55, "Arus sama pada seluruh komponen rangkaian seri",
        ha="center", fontsize=10, color="#475569")
ax.text(6, 0.18, "Sumber AC → R → L → C → kembali ke sumber",
        ha="center", fontsize=9, color="#64748b")

fig.tight_layout()
st.pyplot(fig, use_container_width=True)
plt.close(fig)

# =========================================================
# TABEL HASIL PERHITUNGAN
# =========================================================
st.divider()
st.subheader("3. Tabel perhitungan")

rows = [
    ("Frekuensi sudut", "ω = 2πf", f"{omega:.3f} rad/s"),
    ("Reaktansi induktif", "XL = 2πfL", f"{XL:.4f} Ω"),
    ("Reaktansi kapasitif", "XC = 1/(2πfC)", f"{XC:.4f} Ω"),
    ("Reaktansi total", "X = XL − XC", f"{X:.4f} Ω"),
    ("Impedansi", "|Z| = √(R² + X²)", f"{Z:.4f} Ω"),
    ("Sudut fase", "φ = atan2(X, R)", f"{phi_deg:.4f}°"),
    ("Arus RMS", "I = Vs/|Z|", f"{I_rms:.6f} A"),
    ("Tegangan resistor", "VR = IR", f"{VR:.4f} V"),
    ("Tegangan induktor", "VL = IXL", f"{VL:.4f} V"),
    ("Tegangan kapasitor", "VC = IXC", f"{VC:.4f} V"),
    ("Daya aktif", "P = I²R", f"{P:.4f} W"),
    ("Daya reaktif", "Q = I²X", f"{Q:.4f} var"),
    ("Daya semu", "S = Vs × I", f"{S_apparent:.4f} VA"),
    ("Frekuensi resonansi", "f₀ = 1/(2π√LC)", f"{f_res:.4f} Hz"),
]

st.table({
    "Besaran": [r[0] for r in rows],
    "Rumus": [r[1] for r in rows],
    "Hasil": [r[2] for r in rows],
})

# =========================================================
# DIAGRAM FASOR
# =========================================================
st.divider()
st.subheader("4. Diagram fasor tegangan")
st.caption(
    "Arus dijadikan referensi fase. VR sefase dengan arus, "
    "VL mendahului 90°, dan VC tertinggal 90°."
)

fig2, ax2 = plt.subplots(figsize=(8, 6))
fig2.patch.set_facecolor("white")
ax2.set_facecolor("white")

# Fasor digambar head-to-tail
ax2.annotate(
    "", xy=(VR, 0), xytext=(0, 0),
    arrowprops=dict(arrowstyle="->", lw=2.5, color=red),
)
ax2.annotate(
    "", xy=(VR, VL), xytext=(VR, 0),
    arrowprops=dict(arrowstyle="->", lw=2.5, color=purple),
)
ax2.annotate(
    "", xy=(VR, VL - VC), xytext=(VR, VL),
    arrowprops=dict(arrowstyle="->", lw=2.5, color=orange),
)
ax2.annotate(
    "", xy=(VR, VL - VC), xytext=(0, 0),
    arrowprops=dict(arrowstyle="->", lw=2.8, color=blue),
)

ax2.text(VR / 2, 0, f"  VR={VR:.2f} V", color=red, va="bottom")
ax2.text(VR, VL / 2, f" VL={VL:.2f} V", color=purple)
ax2.text(VR, VL - VC / 2, f" VC={VC:.2f} V", color=orange)
ax2.text(VR / 2, (VL - VC) / 2, f" Vs={Vs:.2f} V", color=blue)

all_x = [0, VR]
all_y = [0, VL, VL - VC]
xspan = max(max(all_x) - min(all_x), Vs, 1)
yspan = max(max(all_y) - min(all_y), Vs, 1)

ax2.set_xlim(-0.12 * xspan, max(all_x) + 0.25 * xspan)
ax2.set_ylim(min(all_y) - 0.2 * yspan, max(all_y) + 0.2 * yspan)
ax2.set_xlabel("Komponen sefase arus (V)")
ax2.set_ylabel("Komponen reaktif (V)")
ax2.set_title("Penjumlahan fasor tegangan")
ax2.axhline(0, color="#94a3b8", lw=0.8)
ax2.axvline(0, color="#94a3b8", lw=0.8)
ax2.grid(True, alpha=0.25)
ax2.set_aspect("auto")
fig2.tight_layout()
st.pyplot(fig2, use_container_width=True)
plt.close(fig2)

# =========================================================
# GRAFIK GELOMBANG AC
# =========================================================
st.divider()
st.subheader("5. Grafik gelombang tegangan dan arus")
st.caption(
    "Gelombang ditampilkan selama tiga periode. "
    "Tegangan sumber merupakan jumlah sesaat VR + VL + VC."
)

period = 1 / f
t = np.linspace(0, 3 * period, 1500)
wt = omega * t

i_t = np.sqrt(2) * I_rms * np.sin(wt)
vR_t = np.sqrt(2) * VR * np.sin(wt)
vL_t = np.sqrt(2) * VL * np.sin(wt + np.pi / 2)
vC_t = np.sqrt(2) * VC * np.sin(wt - np.pi / 2)
vS_t = vR_t + vL_t + vC_t

fig3, ax3 = plt.subplots(figsize=(11, 5))
ax3.plot(t * 1000, vS_t, label="Sumber Vs", lw=2.5, color=blue)
ax3.plot(t * 1000, vR_t, label="Resistor VR", lw=1.5, color=red)
ax3.plot(t * 1000, vL_t, label="Induktor VL", lw=1.5, color=purple)
ax3.plot(t * 1000, vC_t, label="Kapasitor VC", lw=1.5, color=orange)
ax3.set_xlabel("Waktu (ms)")
ax3.set_ylabel("Tegangan sesaat (V)")
ax3.set_title("Gelombang tegangan pada komponen RLC")
ax3.grid(True, alpha=0.25)
ax3.legend(ncol=2)
fig3.tight_layout()
st.pyplot(fig3, use_container_width=True)
plt.close(fig3)

fig4, ax4 = plt.subplots(figsize=(11, 3.8))
ax4.plot(t * 1000, i_t, color="#059669", lw=2)
ax4.axhline(0, color="#94a3b8", lw=0.8)
ax4.set_xlabel("Waktu (ms)")
ax4.set_ylabel("Arus sesaat (A)")
ax4.set_title("Gelombang arus rangkaian")
ax4.grid(True, alpha=0.25)
fig4.tight_layout()
st.pyplot(fig4, use_container_width=True)
plt.close(fig4)

# =========================================================
# VERIFIKASI KVL
# =========================================================
st.divider()
st.subheader("6. Verifikasi Hukum Kirchhoff II")

st.latex(r"\underline{V}_s = \underline{V}_R + \underline{V}_L + \underline{V}_C")
st.markdown(
    "Dalam rangkaian AC, tegangan dijumlahkan sebagai fasor. "
    "Dengan arus sebagai referensi, fasor sumber adalah "
    "VR + j(VL − VC)."
)

Vs_calc = np.sqrt(VR**2 + (VL - VC)**2)
error = abs(Vs_calc - Vs)

c1, c2 = st.columns(2)
c1.metric("Vs input", f"{Vs:.6f} V")
c2.metric("Vs hasil penjumlahan fasor", f"{Vs_calc:.6f} V")

st.write(f"Selisih perhitungan: **{error:.10f} V**")

if np.isclose(Vs_calc, Vs, rtol=1e-9, atol=1e-9):
    st.success("KVL terpenuhi: jumlah fasor tegangan sama dengan tegangan sumber.")
else:
    st.warning("Periksa kembali parameter dan perhitungan rangkaian.")

# =========================================================
# INTERPRETASI
# =========================================================
st.divider()
st.subheader("7. Interpretasi rangkaian")

if np.isclose(X, 0, atol=1e-9):
    st.success(
        "Rangkaian berada pada kondisi resonansi: XL sama dengan XC. "
        "Impedansi total sama dengan R dan faktor daya mendekati 1."
    )
elif X > 0:
    st.info(
        "Rangkaian bersifat induktif karena XL lebih besar daripada XC. "
        f"Sudut fase {phi_deg:.2f}° menunjukkan arus tertinggal "
        "terhadap tegangan sumber."
    )
else:
    st.info(
        "Rangkaian bersifat kapasitif karena XC lebih besar daripada XL. "
        f"Sudut fase {phi_deg:.2f}° menunjukkan arus mendahului "
        "tegangan sumber."
    )

c1, c2, c3 = st.columns(3)
c1.metric("Daya aktif P", f"{P:.3f} W")
c2.metric("Daya reaktif Q", f"{Q:.3f} var")
c3.metric("Daya semu S", f"{S_apparent:.3f} VA")

with st.expander("Lihat rumus dasar"):
    st.latex(r"\omega = 2\pi f")
    st.latex(r"X_L = \omega L")
    st.latex(r"X_C = \frac{1}{\omega C}")
    st.latex(r"X = X_L-X_C")
    st.latex(r"|Z| = \sqrt{R^2+X^2}")
    st.latex(r"I_{\mathrm{RMS}} = \frac{V_{\mathrm{RMS}}}{|Z|}")
    st.latex(r"\phi = \tan^{-1}\left(\frac{X}{R}\right)")
    st.latex(r"P = I^2R")
    st.latex(r"Q = I^2(X_L-X_C)")

st.divider()
st.caption(
    "Simulasi edukasi rangkaian RLC seri AC. "
    "Hasil dihitung berdasarkan model rangkaian ideal."
)
