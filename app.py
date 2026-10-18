import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Arc

# =====================================================
# KONFIGURASI WEBSITE
# =====================================================
st.set_page_config(
    page_title="Simulasi KVL RLC Seri AC",
    page_icon="⚡",
    layout="wide"
)

# Warna tampilan
BG = "#0b1220"
PANEL = "#142238"
WIRE = "#dbeafe"
BLUE = "#38bdf8"
ORANGE = "#fb923c"
PURPLE = "#c084fc"
GREEN = "#4ade80"

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0b1220, #13233b);
    color: #f1f5f9;
}
h1, h2, h3, p, label {
    color: #f1f5f9;
}
div[data-testid="stMetric"] {
    background: #142238;
    border: 1px solid #30445f;
    border-radius: 12px;
    padding: 14px;
}
</style>
""", unsafe_allow_html=True)

st.title("⚡ Simulasi Hukum Kirchhoff II")
st.subheader("Rangkaian RLC Seri dengan Sumber Tegangan AC")
st.write(
    "Ubah parameter rangkaian, amati arah arus sesaat, "
    "dan periksa hubungan tegangan pada rangkaian."
)

# =====================================================
# PANEL KONTROL
# =====================================================
with st.sidebar:
    st.header("🎛️ Panel Kontrol")

    st.markdown("### Sumber AC")
    Vs = st.slider(
        "Tegangan sumber RMS (V)",
        1.0, 100.0, 12.0, 1.0
    )
    f = st.slider(
        "Frekuensi (Hz)",
        10, 500, 50, 10
    )

    st.markdown("### Komponen RLC")
    R = st.slider(
        "Resistor R (Ω)",
        1, 500, 100, 1
    )
    L_mH = st.slider(
        "Induktor L (mH)",
        1, 1000, 100, 1
    )
    C_uF = st.slider(
        "Kapasitor C (µF)",
        1, 1000, 100, 1
    )

    st.markdown("---")
    st.markdown("### Posisi pada Gelombang AC")
    fase_deg = st.slider(
        "Fase waktu (derajat)",
        0, 359, 0, 1
    )

    st.caption(
        "Geser fase untuk melihat perubahan arus dan "
        "tegangan sesaat. Perhitungan RMS tetap berdasarkan "
        "parameter rangkaian."
    )

# =====================================================
# PERHITUNGAN RLC SERI AC
# =====================================================
L = L_mH / 1000
C = C_uF / 1_000_000

omega = 2 * np.pi * f
XL = omega * L
XC = 1 / (omega * C)

X = XL - XC
Z = np.sqrt(R**2 + X**2)
phi = np.arctan2(X, R)
phi_deg = np.degrees(phi)

I = Vs / Z

VR = I * R
VL = I * XL
VC = I * XC

# Fasor: arus menjadi referensi sudut 0 derajat
VR_ph = complex(VR, 0)
VL_ph = complex(0, VL)
VC_ph = complex(0, -VC)
Vs_ph = VR_ph + VL_ph + VC_ph

# Fase waktu
theta = np.radians(fase_deg)

# Nilai sesaat
I_peak = np.sqrt(2) * I
i_inst = I_peak * np.sin(theta)

vR_inst = np.sqrt(2) * VR * np.sin(theta)
vL_inst = np.sqrt(2) * VL * np.sin(theta + np.pi / 2)
vC_inst = np.sqrt(2) * VC * np.sin(theta - np.pi / 2)

vs_inst = vR_inst + vL_inst + vC_inst

# =====================================================
# RINGKASAN HASIL
# =====================================================
st.markdown("## 1. Hasil Perhitungan")

a, b, c, d = st.columns(4)
a.metric("Arus RMS", f"{I:.4f} A")
b.metric("Impedansi |Z|", f
