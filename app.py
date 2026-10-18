
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Simulasi KVL | RLC AC",
    page_icon="⚡",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #081426, #10243b);
    color: #f1f5f9;
}
h1, h2, h3, p, label {
    color: #f1f5f9 !important;
}
[data-testid="stMetric"] {
    background: #172d46;
    padding: 16px;
    border-radius: 12px;
    border: 1px solid #31516e;
}
[data-testid="stMetricValue"] {
    color: #5eead4;
}
.stButton button {
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

st.title("⚡ SIMULASI HUKUM KIRCHHOFF II")
st.subheader("Rangkaian RLC Seri Arus Bolak-Balik (AC)")
st.write(
    "Ubah parameter rangkaian dan amati perubahan arus, "
    "impedansi, tegangan komponen, grafik gelombang, dan diagram fasor."
)

with st.sidebar:
    st.header("⚙️ Parameter Rangkaian")
    Vs = st.slider("Tegangan sumber RMS (V)", 1.0, 220.0, 12.0, 1.0)
    f = st.slider("Frekuensi (Hz)", 10, 1000, 50, 10)
    R = st.slider("Resistansi R (Ω)", 1.0, 200.0, 30.0, 1.0)
    L_mH = st.slider("Induktansi L (mH)", 1.0, 1000.0, 100.0, 1.0)
    C_uF = st.slider("Kapasitansi C (µF)", 1.0, 1000.0, 100.0, 1.0)

L = L_mH / 1000
C = C_uF / 1_000_000
w = 2 * np.pi * f

XL = w * L
XC = 1 / (w * C)
X = XL - XC
Z = np.sqrt(R**2 + X**2)
phi = np.degrees(np.arctan2(X, R))
I = Vs / Z

VR = I * R
VL = I * XL
VC = I * XC

st.markdown("---")
st.header("1. Hasil Perhitungan")

cols = st.columns(4)
cols[0].metric("Arus RMS", f"{I:.4f} A")
cols[1].metric("Impedansi", f"{Z:.3f} Ω")
cols[2].metric("Sudut fase", f"{phi:.2f}°")
cols[3].metric("Frekuensi", f"{f} Hz")

cols = st.columns(3)
cols[0].metric("Reaktansi induktif XL", f"{XL:.3f} Ω")
cols[1].metric("Reaktansi kapasitif XC", f"{XC:.3f} Ω")
cols[2].metric("Reaktansi total", f"{X:.3f} Ω")

cols = st.columns(3)
cols[0].metric("Tegangan resistor VR", f"{VR:.3f} V")
cols[1].metric("Tegangan induktor VL", f"{VL:.3f} V")
cols[2].metric("Tegangan kapasitor VC", f"{VC:.3f} V")

st.markdown("---")
st.header("2. Diagram Rangkaian RLC Seri")

fig, ax = plt.subplots(figsize=(12, 3.5))
fig.patch.set_facecolor("#f8fafc")
ax.set_facecolor("#f8fafc")
ax.set_xlim(0, 12)
ax.set_ylim(0, 4)
ax.axis("off")

# Kabel rangkaian
ax.plot([1, 2], [2, 2], color="#2563eb", lw=2.5)
ax.plot([3.5, 4.3], [2, 2], color="#2563eb", lw=2.5)
ax.plot([5.8, 6.7], [2, 2], color="#2563eb", lw=2.5)
ax.plot([8.2, 9.0], [2, 2], color="#2563eb", lw=2.5)
ax.plot([10, 11], [2, 2], color="#2563eb", lw=2.5)
ax.plot([11, 11], [2, 0.6], color="#2563eb", lw=2.5)
ax.plot([11, 1], [0.6, 0.6], color="#2563eb", lw=2.5)
ax.plot([1, 1], [0.6, 1.4], color="#2563eb", lw=2.5)
ax.plot([1, 1], [2.6, 2], color="#2563eb", lw=2.5)

# Sumber AC
source = plt.Circle((1, 2), 0.6, fill=False, color="#0f766e", lw=2.5)
ax.add_patch(source)
theta = np.linspace(-np.pi, np.pi, 100)
ax.plot(1 + 0.38 * theta / np.pi, 2 + 0.2 * np.sin(theta),
        color="#0f766e", lw=1.8)
ax.text(1, 3.0, f"Vs = {Vs:g} V RMS", ha="center", fontsize=10)

# Resistor zigzag
rz = np.array([
    [2,2],[2.15,2.25],[2.4,1.75],[2.65,2.25],
    [2.9,1.75],[3.15,2.25],[3.4,2]
])
ax.plot(rz[:,0], rz[:,1], color="#dc2626", lw=2.5)
ax.text(2.7, 2.65, f"R = {R:g} Ω", ha="center", fontsize=10)

# Induktor
xcoil = np.linspace(4.3, 5.8, 200)
ycoil = 2 + 0.22 * np.sin(np.linspace(0, 4*np.pi, 200))
ax.plot(xcoil, ycoil, color="#7c3aed", lw=2.5)
ax.text(5.05, 2.65, f"L = {L_mH:g} mH", ha="center", fontsize=10)

# Kapasitor
ax.plot([7.15, 7.15], [1.5, 2.5], color="#d97706", lw=3)
ax.plot([7.65, 7.65], [1.5, 2.5], color="#d97706", lw=3)
ax.text(7.4, 2.75, f"C = {C_uF:g} µF", ha="center", fontsize=10)

# Arus
ax.annotate("", xy=(9.5, 2.35), xytext=(8.5, 2.35),
            arrowprops=dict(arrowstyle="->", color="#059669", lw=2.5))
ax.text(9, 2.65, f"I = {I:.3f} A", ha="center", color="#047857")

ax.text(6, 0.15, "Rangkaian seri: arus yang mengalir sama pada R, L, dan C",
        ha="center", fontsize=10)
st.pyplot(fig, use_container_width=True)
plt.close(fig)

st.markdown("---")
st.header("3. Grafik Gelombang AC")

t = np.linspace(0, 3/f, 1200)
wt = w*t
i_t = np.sqrt(2)*I*np.sin(wt)
vR_t = np.sqrt(2)*VR*np.sin(wt)
vL_t = np.sqrt(2)*VL*np.sin(wt + np.pi/2)
vC_t = np.sqrt(2)*VC*np.sin(wt - np.pi/2)
vS_t = vR_t + vL_t + vC_t

fig2, ax2 = plt.subplots(figsize=(12, 5))
ax2.plot(t*1000, vS_t, label="Tegangan sumber", lw=2)
ax2.plot(t*1000, vR_t, label="Tegangan R")
ax2.plot(t*1000, vL_t, label="Tegangan L")
ax2.plot(t*1000, vC_t, label="Tegangan C")
ax2.set_xlabel("Waktu (ms)")
ax2.set_ylabel("Tegangan sesaat (V)")
ax2.set_title("Gelombang Tegangan pada Rangkaian RLC")
ax2.grid(True, alpha=0.3)
ax2.legend()
st.pyplot(fig2, use_container_width=True)
plt.close(fig2)

st.markdown("---")
st.header("4. Diagram Fasor")

fig3, ax3 = plt.subplots(figsize=(7, 6))
ax3.quiver(0, 0, VR, 0, angles="xy", scale_units="xy",
           scale=1, color="red", label="VR")
ax3.quiver(VR, 0, 0, VL, angles="xy", scale_units="xy",
           scale=1, color="blue")
ax3.quiver(VR, VL, 0, -VC, angles="xy", scale_units="xy",
           scale=1, color="green")
ax3.quiver(0, 0, VR, VL-VC, angles="xy", scale_units="xy",
           scale=1, color="purple")
ax3.set_xlim(-max(Vs, 1), max(Vs, VR+1)*1.3)
lim = max(Vs, VR, VL, VC, 1)*1.3
ax3.set_ylim(-lim, lim)
ax3.set_xlabel("Komponen sefase arus (V)")
ax3.set_ylabel("Komponen reaktif (V)")
ax3.set_title("Fasor Tegangan (arus sebagai referensi)")
ax3.grid(True, alpha=0.3)
ax3.axhline(0, color="black", lw=0.7)
ax3.axvline(0, color="black", lw=0.7)
st.pyplot(fig3, use_container_width=True)
plt.close(fig3)

st.markdown("---")
st.header("5. Verifikasi Hukum Kirchhoff II")

st.latex(r"V_s = V_R + V_L + V_C")
st.write(
    "Untuk AC, tegangan harus dijumlahkan sebagai fasor, bukan "
    "menjumlahkan nilai RMS secara aritmetika."
)
Vs_calc = np.sqrt(VR**2 + (VL-VC)**2)
st.metric("Tegangan sumber hasil fasor", f"{Vs_calc:.4f} V")
st.metric("Selisih terhadap sumber", f"{abs(Vs_calc-Vs):.8f} V")

st.markdown("---")
st.header("6. Interpretasi Otomatis")

if abs(X) < 0.01:
    st.success("Rangkaian mendekati resonansi: XL ≈ XC.")
elif X > 0:
    st.info("Rangkaian bersifat induktif: XL > XC, arus tertinggal terhadap tegangan.")
else:
    st.info("Rangkaian bersifat kapasitif: XC > XL, arus mendahului tegangan.")

st.write(f"""
- Reaktansi induktif: **{XL:.3f} Ω**
- Reaktansi kapasitif: **{XC:.3f} Ω**
- Impedansi total: **{Z:.3f} Ω**
- Arus efektif: **{I:.4f} A**
- Faktor daya: **{np.cos(np.radians(phi)):.4f}**
""")

with st.expander("Lihat rumus yang digunakan"):
    st.latex(r"X_L = 2\pi fL")
    st.latex(r"X_C = \frac{1}{2\pi fC}")
    st.latex(r"|Z| = \sqrt{R^2+(X_L-X_C)^2}")
    st.latex(r"I_{\mathrm{RMS}} = \frac{V_{\mathrm{RMS}}}{|Z|}")
    st.latex(r"\phi = \tan^{-1}\left(\frac{X_L-X_C}{R}\right)")

st.caption("Simulasi edukasi RLC seri AC — Hukum Kirchhoff II (KVL).")
