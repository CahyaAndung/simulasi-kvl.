
import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import matplotlib.pyplot as plt

# =========================================================
# 1. KONFIGURASI DAN DESAIN
# =========================================================
st.set_page_config(
    page_title="Simulasi KVL - RLC Seri AC",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
.stApp {
    background: #ffffff;
    color: #24364b;
}
[data-testid="stSidebar"] {
    background: #f5f8fc;
    border-right: 1px solid #dce6f0;
}
h1, h2, h3 {
    color: #163a63 !important;
}
[data-testid="stMetric"] {
    background: #f7faff;
    border: 1px solid #dbe7f3;
    border-radius: 10px;
    padding: 14px;
}
[data-testid="stMetricValue"] {
    color: #1261a0;
}
hr {
    border-color: #e2e8f0;
}
</style>
""", unsafe_allow_html=True)

st.title("⚡ Simulasi Hukum Kirchhoff II")
st.subheader("Rangkaian RLC Seri — Arus Bolak-Balik (AC)")
st.caption(
    "Simulasi interaktif untuk mempelajari arus, impedansi, "
    "tegangan komponen, fasor, dan Hukum Kirchhoff II."
)
st.divider()

# =========================================================
# 2. INPUT PARAMETER
# =========================================================
with st.sidebar:
    st.header("Parameter Rangkaian")

    Vs = st.number_input(
        "Tegangan sumber RMS (V)",
        min_value=0.1, max_value=500.0,
        value=12.0, step=1.0
    )

    f = st.number_input(
        "Frekuensi (Hz)",
        min_value=1.0, max_value=10000.0,
        value=50.0, step=1.0
    )

    R = st.number_input(
        "Resistansi R (Ω)",
        min_value=0.1, max_value=100000.0,
        value=30.0, step=1.0
    )

    L_mH = st.number_input(
        "Induktansi L (mH)",
        min_value=0.1, max_value=100000.0,
        value=100.0, step=10.0
    )

    C_uF = st.number_input(
        "Kapasitansi C (µF)",
        min_value=0.1, max_value=1000000.0,
        value=100.0, step=10.0
    )

    st.divider()
    st.caption(
        "Tegangan dan arus utama menggunakan nilai RMS. "
        "Komponen diasumsikan ideal."
    )

# =========================================================
# 3. PERHITUNGAN LISTRIK
# =========================================================
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

power_factor = np.cos(phi)
P = I**2 * R
Q = I**2 * X
S = Vs * I
f_res = 1 / (2 * np.pi * np.sqrt(L * C))

# =========================================================
# 4. RINGKASAN HASIL
# =========================================================
st.header("1. Ringkasan Hasil")

a, b, c, d = st.columns(4)
a.metric("Arus RMS", f"{I:.4f} A")
b.metric("Impedansi |Z|", f"{Z:.3f} Ω")
c.metric("Sudut Fase", f"{phi_deg:.2f}°")
d.metric("Faktor Daya", f"{power_factor:.4f}")

a, b, c = st.columns(3)
a.metric("XL", f"{XL:.3f} Ω")
b.metric("XC", f"{XC:.3f} Ω")
c.metric("Reaktansi Total", f"{X:.3f} Ω")

a, b, c = st.columns(3)
a.metric("Tegangan VR", f"{VR:.3f} V")
b.metric("Tegangan VL", f"{VL:.3f} V")
c.metric("Tegangan VC", f"{VC:.3f} V")

# =========================================================
# 5. SKEMA RANGKAIAN INTERAKTIF
# =========================================================
st.divider()
st.header("2. Skema Rangkaian Interaktif")
st.caption(
    "Seret simbol sumber AC, R, L, atau C secara horizontal. "
    "Lepaskan pada posisi komponen lain untuk menukar urutannya."
)

components.html(r"""
<div style="font-family:Arial,sans-serif;border:1px solid #dbe5ef;
border-radius:12px;padding:12px;background:white">
<svg id="circuit" viewBox="0 0 800 250"
style="width:100%;height:auto;touch-action:none;user-select:none">

<g id="wires" stroke="#475569" stroke-width="2.5" fill="none"></g>

<g class="part" id="src" transform="translate(100 100)">
  <circle r="24" fill="white" stroke="#1672b8" stroke-width="2.5"/>
  <path d="M-15 0 C-10 -14,-5 -14,0 0 S10 14,15 0"
  stroke="#1672b8" stroke-width="2.2" fill="none"/>
  <text y="-38" text-anchor="middle" fill="#1672b8"
  font-size="14">Sumber AC</text>
  <text y="43" text-anchor="middle" fill="#1672b8"
  font-size="12">Vs</text>
</g>

<g class="part" id="res" transform="translate(300 100)">
  <path d="M-48 0 H-35 L-25 -12 L-10 12 L5 -12 L20 12 L35 0 H48"
  stroke="#d94841" stroke-width="2.5" fill="none"/>
  <text y="-38" text-anchor="middle" fill="#d94841"
  font-size="14">Resistor R</text>
  <text y="43" text-anchor="middle" fill="#d94841"
  font-size="12">R</text>
</g>

<g class="part" id="ind" transform="translate(500 100)">
  <path d="M-48 0 H-36
  C-36 -22,-18 -22,-18 0
  C-18 -22,0 -22,0 0
  C0 -22,18 -22,18 0
  C18 -22,36 -22,36 0 H48"
  stroke="#7c3aed" stroke-width="2.5" fill="none"/>
  <text y="-38" text-anchor="middle" fill="#7c3aed"
  font-size="14">Induktor L</text>
  <text y="43" text-anchor="middle" fill="#7c3aed"
  font-size="12">L</text>
</g>

<g class="part" id="cap" transform="translate(700 100)">
  <path d="M-48 0 H-8 M8 0 H48"
  stroke="#d97706" stroke-width="2.5" fill="none"/>
  <path d="M-8 -22 V22 M8 -22 V22"
  stroke="#d97706" stroke-width="3"/>
  <text y="-38" text-anchor="middle" fill="#d97706"
  font-size="14">Kapasitor C</text>
  <text y="43" text-anchor="middle" fill="#d97706"
  font-size="12">C</text>
</g>

<text x="400" y="215" text-anchor="middle"
font-size="13" fill="#64748b">
Rangkaian RLC seri AC
</text>
<text x="400" y="235" text-anchor="middle"
font-size="11" fill="#94a3b8">
Geser komponen secara horizontal untuk menukar posisi
</text>
</svg>
</div>

<script>
(() => {
  const svg = document.getElementById("circuit");
  const wires = document.getElementById("wires");
  const ids = ["src", "res", "ind", "cap"];
  const slots = [100, 300, 500, 700];
  let active = null;
  let startX = 0;
  let initialX = 0;

  function xOf(el) {
    const m = el.getAttribute("transform").match(
      /translate\(([-\d.]+)\s+([-\d.]+)\)/
    );
    return m ? Number(m[1]) : 0;
  }

  function moveTo(el, x) {
    el.setAttribute("transform", `translate(${x} 100)`);
  }

  function point(e) {
    const p = svg.createSVGPoint();
    p.x = e.clientX;
    p.y = e.clientY;
    return p.matrixTransform(svg.getScreenCTM().inverse());
  }

  function drawWires() {
    wires.innerHTML = "";
    const parts = ids.map(id => document.getElementById(id))
      .sort((a, b) => xOf(a) - xOf(b));
    const xs = parts.map(xOf);

    function line(x1, y1, x2, y2) {
      const el = document.createElementNS(
        "http://www.w3.org/2000/svg", "path"
      );
      el.setAttribute("d", `M${x1} ${y1} L${x2} ${y2}`);
      wires.appendChild(el);
    }

    for (let i = 0; i < xs.length - 1; i++) {
      line(xs[i] + 48, 100, xs[i + 1] - 48, 100);
    }

    line(xs[0], 124, xs[0], 170);
    line(xs[0], 170, xs[3], 170);
    line(xs[3], 170, xs[3], 124);
  }

  ids.forEach(id => {
    const el = document.getElementById(id);
    el.style.cursor = "grab";
    el.style.touchAction = "none";

    el.addEventListener("pointerdown", e => {
      active = el;
      startX = point(e).x;
      initialX = xOf(el);
      el.setPointerCapture(e.pointerId);
      e.preventDefault();
    });

    el.addEventListener("pointermove", e => {
      if (active !== el) return;
      const dx = point(e).x - startX;
      moveTo(el, Math.max(52, Math.min(748, initialX + dx)));
      drawWires();
    });

    el.addEventListener("pointerup", () => {
      if (active !== el) return;

      const current = xOf(el);
      const target = slots.reduce((a, b) =>
        Math.abs(b - current) < Math.abs(a - current) ? b : a
      );

      const other = ids.map(i => document.getElementById(i))
        .find(p => p !== el && Math.abs(xOf(p) - target) < 1);

      if (other) moveTo(other, initialX);
      moveTo(el, target);
      active = null;
      drawWires();
    });

    el.addEventListener("pointercancel", () => {
      active = null;
      drawWires();
    });
  });

  drawWires();
})();
</script>
""", height=300, scrolling=False)

st.info(
    "Catatan: posisi komponen dapat digeser dan ditukar secara visual. "
    "Nilai listrik tetap mengikuti input R, L, dan C di panel kiri."
)

# =========================================================
# 6. TABEL PERHITUNGAN
# =========================================================
st.divider()
st.header("3. Tabel Perhitungan")

data = {
    "Besaran": [
        "Frekuensi sudut",
        "Reaktansi induktif",
        "Reaktansi kapasitif",
        "Reaktansi total",
        "Impedansi",
        "Sudut fase",
        "Arus RMS",
        "Tegangan resistor",
        "Tegangan induktor",
        "Tegangan kapasitor",
        "Daya aktif",
        "Daya reaktif",
        "Daya semu",
        "Frekuensi resonansi",
    ],
    "Rumus": [
        "ω = 2πf",
        "XL = 2πfL",
        "XC = 1/(2πfC)",
        "X = XL − XC",
        "|Z| = √(R² + X²)",
        "φ = atan2(X, R)",
        "I = Vs/|Z|",
        "VR = IR",
        "VL = IXL",
        "VC = IXC",
        "P = I²R",
        "Q = I²X",
        "S = Vs × I",
        "f₀ = 1/(2π√LC)",
    ],
    "Hasil": [
        f"{omega:.4f} rad/s",
        f"{XL:.4f} Ω",
        f"{XC:.4f} Ω",
        f"{X:.4f} Ω",
        f"{Z:.4f} Ω",
        f"{phi_deg:.4f}°",
        f"{I:.6f} A",
        f"{VR:.4f} V",
        f"{VL:.4f} V",
        f"{VC:.4f} V",
        f"{P:.4f} W",
        f"{Q:.4f} var",
        f"{S:.4f} VA",
        f"{f_res:.4f} Hz",
    ],
}
st.dataframe(data, use_container_width=True, hide_index=True)

# =========================================================
# 7. DIAGRAM FASOR
# =========================================================
st.divider()
st.header("4. Diagram Fasor Tegangan")
st.caption(
    "Arus menjadi referensi: VR sefase, VL mendahului 90°, "
    "dan VC tertinggal 90°."
)

fig, ax = plt.subplots(figsize=(8, 5.5))
ax.set_facecolor("white")
fig.patch.set_facecolor("white")

ax.annotate("", xy=(VR, 0), xytext=(0, 0),
    arrowprops=dict(arrowstyle="->", lw=2.4, color="#d94841"))
ax.annotate("", xy=(VR, VL), xytext=(VR, 0),
    arrowprops=dict(arrowstyle="->", lw=2.4, color="#7c3aed"))
ax.annotate("", xy=(VR, VL-VC), xytext=(VR, VL),
    arrowprops=dict(arrowstyle="->", lw=2.4, color="#d97706"))
ax.annotate("", xy=(VR, VL-VC), xytext=(0, 0),
    arrowprops=dict(arrowstyle="->", lw=2.8, color="#1769aa"))

ax.text(VR/2, 0, f" VR={VR:.2f} V", color="#d94841", va="bottom")
ax.text(VR, VL/2, f" VL={VL:.2f} V", color="#7c3aed")
ax.text(VR, VL-VC/2, f" VC={VC:.2f} V", color="#d97706")
ax.text(VR/2, (VL-VC)/2, f" Vs={Vs:.2f} V", color="#1769aa")

xmax = max(VR, Vs, 1.0)
ymax = max(abs(VL), abs(VC), abs(VL-VC), Vs, 1.0)
ax.set_xlim(-0.12*xmax, max(VR, 1)*1.35)
ax.set_ylim(min(0, VL-VC)-0.2*ymax, max(VL, VL-VC)+0.2*ymax)
ax.set_xlabel("Komponen sefase arus (V)")
ax.set_ylabel("Komponen reaktif (V)")
ax.set_title("Penjumlahan Fasor Tegangan")
ax.axhline(0, color="#94a3b8", lw=0.8)
ax.axvline(0, color="#94a3b8", lw=0.8)
ax.grid(True, alpha=0.25)
fig.tight_layout()
st.pyplot(fig, use_container_width=True)
plt.close(fig)

# =========================================================
# 8. GRAFIK GELOMBANG AC
# =========================================================
st.divider()
st.header("5. Grafik Gelombang AC")
st.caption(
    "Gelombang ditampilkan selama tiga periode. "
    "Tegangan sumber adalah jumlah sesaat VR + VL + VC."
)

period = 1 / f
t = np.linspace(0, 3*period, 1500)
wt = omega*t

i_t = np.sqrt(2)*I*np.sin(wt)
vR_t = np.sqrt(2)*VR*np.sin(wt)
vL_t = np.sqrt(2)*VL*np.sin(wt + np.pi/2)
vC_t = np.sqrt(2)*VC*np.sin(wt - np.pi/2)
vS_t = vR_t + vL_t + vC_t

fig, ax = plt.subplots(figsize=(11, 4.8))
ax.plot(t*1000, vS_t, label="Sumber Vs", lw=2.4, color="#1769aa")
ax.plot(t*1000, vR_t, label="Resistor VR", lw=1.5, color="#d94841")
ax.plot(t*1000, vL_t, label="Induktor VL", lw=1.5, color="#7c3aed")
ax.plot(t*1000, vC_t, label="Kapasitor VC", lw=1.5, color="#d97706")
ax.set_xlabel("Waktu (ms)")
ax.set_ylabel("Tegangan sesaat (V)")
ax.set_title("Gelombang Tegangan Komponen RLC")
ax.grid(True, alpha=0.25)
ax.legend(ncol=2)
fig.tight_layout()
st.pyplot(fig, use_container_width=True)
plt.close(fig)

fig, ax = plt.subplots(figsize=(11, 3.5))
ax.plot(t*1000, i_t, color="#059669", lw=2)
ax.axhline(0, color="#94a3b8", lw=0.8)
ax.set_xlabel("Waktu (ms)")
ax.set_ylabel("Arus sesaat (A)")
ax.set_title("Gelombang Arus Rangkaian")
ax.grid(True, alpha=0.25)
fig.tight_layout()
st.pyplot(fig, use_container_width=True)
plt.close(fig)

# =========================================================
# 9. VERIFIKASI KVL
# =========================================================
st.divider()
st.header("6. Verifikasi Hukum Kirchhoff II")

st.latex(
    r"\underline{V}_s = \underline{V}_R + "
    r"\underline{V}_L + \underline{V}_C"
)

st.write(
    "Pada rangkaian AC, tegangan dijumlahkan sebagai fasor. "
    "Dengan arus sebagai referensi, fasor sumber adalah "
    "VR + j(VL − VC)."
)

Vs_calc = np.sqrt(VR**2 + (VL-VC)**2)
error = abs(Vs_calc - Vs)

a, b = st.columns(2)
a.metric("Tegangan sumber input", f"{Vs:.6f} V")
b.metric("Tegangan hasil fasor", f"{Vs_calc:.6f} V")

st.write(f"Selisih perhitungan: **{error:.10f} V**")

if np.isclose(Vs_calc, Vs, rtol=1e-9, atol=1e-9):
    st.success(
        "KVL terpenuhi: jumlah fasor tegangan sama dengan "
        "tegangan sumber."
    )
else:
    st.warning("Periksa kembali parameter dan perhitungan.")

# =========================================================
# 10. INTERPRETASI RANGKAIAN
# =========================================================
st.divider()
st.header("7. Interpretasi Rangkaian")

if np.isclose(X, 0, atol=1e-9):
    st.success(
        "Rangkaian berada pada kondisi resonansi: XL ≈ XC. "
        "Impedansi total mendekati R dan faktor daya mendekati 1."
    )
elif X > 0:
    st.info(
        f"Rangkaian bersifat induktif karena XL > XC. "
        f"Arus tertinggal terhadap tegangan sumber dengan "
        f"sudut fase {phi_deg:.2f}°."
    )
else:
    st.info(
        f"Rangkaian bersifat kapasitif karena XC > XL. "
        f"Arus mendahului tegangan sumber dengan "
        f"sudut fase {phi_deg:.2f}°."
    )

a, b, c = st.columns(3)
a.metric("Daya aktif P", f"{P:.3f} W")
b.metric("Daya reaktif Q", f"{Q:.3f} var")
c.metric("Daya semu S", f"{S:.3f} VA")

with st.expander("Lihat Rumus Dasar"):
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
    "Simulasi edukasi RLC seri AC dengan komponen ideal. "
    "Posisi skema interaktif bersifat visual; parameter listrik "
    "diatur melalui panel kiri."
)
