
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Simulasi Hukum Kirchhoff II",
    page_icon="⚡",
    layout="wide"
)

st.title("Simulasi Hukum Kirchhoff II (KVL)")
st.write("Simulasi rangkaian seri dengan Hukum Ohm dan Hukum Kirchhoff II.")

st.subheader("1. Ubah Parameter Rangkaian")

col1, col2, col3, col4 = st.columns(4)

with col1:
    Vs = st.slider("Tegangan sumber Vs (V)", 0.0, 24.0, 13.0, 0.5)
with col2:
    R1 = st.slider("Resistor R1 (Ω)", 10, 1000, 100, 10)
with col3:
    R2 = st.slider("Resistor R2 (Ω)", 10, 1000, 220, 10)
with col4:
    R3 = st.slider("Resistor R3 (Ω)", 10, 1000, 330, 10)

Rt = R1 + R2 + R3
I = Vs / Rt if Rt > 0 else 0

VR1 = I * R1
VR2 = I * R2
VR3 = I * R3
sisa = Vs - VR1 - VR2 - VR3

st.subheader("2. Hasil Perhitungan")

a, b, c, d = st.columns(4)
a.metric("Hambatan Total", f"{Rt} Ω")
b.metric("Arus Rangkaian", f"{I * 1000:.2f} mA")
c.metric("Tegangan R1", f"{VR1:.2f} V")
d.metric("Tegangan R2 + R3", f"{VR2 + VR3:.2f} V")

st.subheader("3. Diagram Rangkaian")

st.markdown(
    f"""
    **Sumber tegangan:** {Vs:.2f} V

    (+) ── [R1: {R1} Ω] ── [R2: {R2} Ω] ── [R3: {R3} Ω] ── (-)

    **Arus rangkaian:** {I * 1000:.2f} mA
    """
)

st.subheader("4. Grafik Tegangan")

fig, ax = plt.subplots()
ax.bar(["Sumber", "R1", "R2", "R3"], [Vs, VR1, VR2, VR3])
ax.set_ylabel("Tegangan (V)")
ax.set_title("Perbandingan Tegangan")
ax.grid(axis="y", alpha=0.3)
st.pyplot(fig)
plt.close(fig)

st.subheader("5. Verifikasi Hukum Kirchhoff II")

st.latex(r"V_s - V_{R1} - V_{R2} - V_{R3} = 0")

st.write(
    f"{Vs:.2f} - {VR1:.2f} - {VR2:.2f} - {VR3:.2f} "
    f"= {sisa:.6f} V"
)

if abs(sisa) < 1e-9:
    st.success("Hukum Kirchhoff II terpenuhi.")
else:
    st.error("Periksa kembali perhitungan.")
