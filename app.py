import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import streamlit.components.v1 as components

st.set_page_config(page_title="Simulasi KVL RLC", page_icon="⚡", layout="wide")

st.markdown("""
<style>
.stApp {background:#ffffff;color:#172033}
.block-container {padding-top:1.5rem;max-width:1250px}
h1,h2,h3 {color:#14213d}
[data-testid="stMetric"] {background:#f6f8fb;border:1px solid #e5eaf1;padding:14px;border-radius:12px}
div[data-testid="stSidebar"] {background:#f7f9fc}
.small-note {color:#64748b;font-size:.9rem}
</style>
""", unsafe_allow_html=True)

st.title("⚡ Simulasi Hukum Kirchhoff Tegangan (KVL)")
st.caption("Simulasi rangkaian RLC seri dengan sumber tegangan bolak-balik (AC)")

with st.sidebar:
    st.header("Parameter rangkaian")
    Vs = st.number_input("Tegangan sumber RMS (V)", min_value=0.1, max_value=10000.0, value=12.0, step=1.0)
    f = st.number_input("Frekuensi (Hz)", min_value=0.1, max_value=100000.0, value=50.0, step=1.0)
    R = st.number_input("Resistansi R (Ω)", min_value=0.1, max_value=1000000.0, value=100.0, step=1.0)
    L_mH = st.number_input("Induktansi L (mH)", min_value=0.01, max_value=1000000.0, value=100.0, step=10.0)
    C_uF = st.number_input("Kapasitansi C (µF)", min_value=0.01, max_value=1000000.0, value=100.0, step=10.0)
    st.divider()
    st.caption("Animasi arus")
    speed = st.slider("Kecepatan animasi", 0.25, 3.0, 1.0, 0.25)
    show_values = st.checkbox("Tampilkan label nilai komponen", value=True)

L = L_mH / 1000.0
C = C_uF / 1_000_000.0
w = 2 * np.pi * f
XL = w * L
XC = 1 / (w * C)
X = XL - XC
Z = np.sqrt(R**2 + X**2)
I = Vs / Z
phi = np.arctan2(X, R)
VR = I * R
VL = I * XL
VC = I * XC
PF = np.cos(phi)
P = I**2 * R
Q = I**2 * X
S = Vs * I
f0 = 1 / (2 * np.pi * np.sqrt(L * C))
Vpeak = np.sqrt(2) * Vs
Ipeak = np.sqrt(2) * I

st.subheader("Skema rangkaian dengan animasi arus")
st.markdown("Titik biru bergerak bolak-balik untuk menggambarkan arus AC. Kecepatan animasi dapat diatur dari panel parameter.")
# SVG animation: dots move in both directions with sinusoidal AC polarity cue.
label_r = f"{R:g} Ω" if show_values else "R"
label_l = f"{L_mH:g} mH" if show_values else "L"
label_c = f"{C_uF:g} µF" if show_values else "C"
html = f"""
<!doctype html><html><head><meta charset="utf-8">
<style>
html,body{{margin:0;background:#fff;font-family:Arial,sans-serif}}
.wrap{{border:1px solid #e2e8f0;border-radius:14px;padding:8px;background:#fff}}
svg{{width:100%;height:auto;display:block;touch-action:pan-y}}
.wire{{stroke:#344256;stroke-width:3;fill:none;stroke-linecap:round;stroke-linejoin:round}}
.comp{{stroke:#344256;stroke-width:3;fill:#fff;stroke-linejoin:round}}
.label{{font-size:16px;fill:#172033;font-weight:600;text-anchor:middle}}
.sub{{font-size:13px;fill:#64748b;text-anchor:middle}}
.particle{{fill:#1687ff;filter:drop-shadow(0 0 3px #93c5fd)}}
.polarity{{font-size:20px;fill:#475569;font-weight:bold;text-anchor:middle}}
.status{{font-size:13px;fill:#475569}}
</style></head><body>
<div class="wrap">
<svg id="circuit" viewBox="0 0 1000 340" role="img" aria-label="Rangkaian RLC seri dengan arus AC bergerak">
  <defs>
    <marker id="arrow" markerWidth="8" markerHeight="8" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#1687ff"/></marker>
  </defs>
  <!-- Circuit wire and AC source -->
  <path class="wire" d="M130 170 H225 M325 170 H405 M505 170 H585 M685 170 H780 V265 H130 V170"/>
  <circle cx="130" cy="217" r="47" class="comp"/>
  <path d="M99 217 C108 192 119 192 130 217 S152 242 161 217" stroke="#1687ff" stroke-width="3" fill="none"/>
  <path class="wire" d="M130 170 V170 M130 264 V265"/>
  <text x="130" y="292" class="label">Sumber AC</text>
  <text x="130" y="312" class="sub">{Vs:g} V RMS · {f:g} Hz</text>
  <!-- resistor -->
  <rect x="225" y="150" width="100" height="40" rx="2" class="comp"/>
  <text x="275" y="126" class="label">Resistor (R)</text>
  <text x="275" y="213" class="sub">{label_r}</text>
  <!-- inductor: coils -->
  <path class="comp" d="M405 170 v-8 a12 12 0 0 1 24 0 a12 12 0 0 1 24 0 a12 12 0 0 1 24 0 a12 12 0 0 1 24 0 v8" transform="translate(0 0)" />
  <text x="455" y="126" class="label">Induktor (L)</text>
  <text x="455" y="213" class="sub">{label_l}</text>
  <!-- capacitor -->
  <path class="wire" d="M585 170 H620 M620 145 V195 M650 145 V195 M650 170 H685"/>
  <path class="wire" d="M620 145 H620 M650 145 H650"/>
  <text x="635" y="126" class="label">Kapasitor (C)</text>
  <text x="635" y="213" class="sub">{label_c}</text>
  <!-- current direction indicator -->
  <path id="arrowLine" d="M240 72 H720" stroke="#1687ff" stroke-width="2.5" fill="none" marker-end="url(#arrow)"/>
  <text x="480" y="52" class="label" fill="#1687ff">Arah arus sesaat i(t)</text>
  <text id="direction" x="480" y="95" class="sub">Arus bergerak</text>
  <!-- particles follow closed rectangular path -->
  <g id="particles"></g>
  <text x="500" y="324" class="status">Animasi konseptual arus AC pada rangkaian seri</text>
</svg>
</div>
<script>
(() => {{
 const svg = document.getElementById('circuit');
 const group = document.getElementById('particles');
 const dirText = document.getElementById('direction');
 const arrow = document.getElementById('arrowLine');
 const path = {{x1:130,y1:170,x2:780,y2:170,x3:780,y3:265,x4:130,y4:265}};
 // closed path, points placed along wire including top, right, bottom and source-side return
 const pts = [];
 const addLine=(x1,y1,x2,y2,n)=>{{for(let i=0;i<n;i++){{let t=i/n;pts.push([x1+(x2-x1)*t,y1+(y2-y1)*t]);}}}};
 addLine(130,170,780,170,42); addLine(780,170,780,265,7); addLine(780,265,130,265,42); addLine(130,265,130,170,7);
 const dots=[];
 for(let i=0;i<30;i++){{const c=document.createElementNS('http://www.w3.org/2000/svg','circle');c.setAttribute('r',4.2);c.setAttribute('class','particle');group.appendChild(c);dots.push(c);}}
 const speed={speed:g};
 let start=null;
 function frame(ts) {{
   if(start===null) start=ts;
   const t=(ts-start)/1000;
   // AC changes polarity every half-cycle. The particles reverse direction with sin(wt).
   const phase=2*Math.PI*{f:g}*t*speed*0.12;
   const signed=Math.sin(phase);
   const direction=Math.cos(phase)>=0?1:-1;
   // Titik bergerak maju-mundur secara halus; kecepatannya berubah mengikuti arus AC.
   const displacement=signed*pts.length*0.20;
   for(let i=0;i<dots.length;i++) {{
     let p=(Math.round(i*pts.length/dots.length + displacement) % pts.length + pts.length)%pts.length;
     const pos=pts[p];
     dots[i].setAttribute('cx',pos[0]); dots[i].setAttribute('cy',pos[1]);
     dots[i].setAttribute('opacity',0.45+0.55*Math.abs(signed));
   }}
   if(direction>0) {{
     arrow.setAttribute('d','M240 72 H720'); arrow.setAttribute('marker-end','url(#arrow)');
     dirText.textContent='Arus sesaat: arah maju';
   }} else {{
     arrow.setAttribute('d','M720 72 H240'); arrow.setAttribute('marker-end','url(#arrow)');
     dirText.textContent='Arus sesaat: arah berbalik';
   }}
   requestAnimationFrame(frame);
 }}
 requestAnimationFrame(frame);
}})();
</script>
</body></html>
"""
components.html(html, height=390, scrolling=False)

st.subheader("Hasil perhitungan")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Impedansi |Z|", f"{Z:.3f} Ω")
m2.metric("Arus RMS", f"{I:.4f} A")
m3.metric("Sudut fase φ", f"{np.degrees(phi):.2f}°")
m4.metric("Faktor daya", f"{PF:.3f}")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Reaktansi induktif XL", f"{XL:.3f} Ω")
m2.metric("Reaktansi kapasitif XC", f"{XC:.3f} Ω")
m3.metric("Frekuensi resonansi f₀", f"{f0:.2f} Hz")
m4.metric("Daya aktif P", f"{P:.3f} W")

st.subheader("Tegangan pada setiap komponen")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Vs RMS", f"{Vs:.3f} V")
col2.metric("VR", f"{VR:.3f} V")
col3.metric("VL", f"{VL:.3f} V")
col4.metric("VC", f"{VC:.3f} V")

st.markdown("### Tabel perhitungan")
table = {
    "Besaran": ["Kecepatan sudut (ω)", "XL = ωL", "XC = 1/(ωC)", "Reaktansi total (XL − XC)", "Impedansi (Z)", "Arus RMS (I = Vs/Z)", "Tegangan resistor (VR)", "Tegangan induktor (VL)", "Tegangan kapasitor (VC)", "Daya aktif (P)", "Daya reaktif (Q)", "Daya semu (S)"],
    "Hasil": [f"{w:.4f} rad/s", f"{XL:.4f} Ω", f"{XC:.4f} Ω", f"{X:.4f} Ω", f"{Z:.4f} Ω", f"{I:.5f} A", f"{VR:.4f} V", f"{VL:.4f} V", f"{VC:.4f} V", f"{P:.4f} W", f"{Q:.4f} var", f"{S:.4f} VA"]
}
st.dataframe(table, use_container_width=True, hide_index=True)

st.subheader("Diagram fasor tegangan")
fig, ax = plt.subplots(figsize=(7, 4.5))
ax.axhline(0, color="#9ca3af", lw=0.8)
ax.axvline(0, color="#9ca3af", lw=0.8)
ax.quiver(0, 0, VR, 0, angles="xy", scale_units="xy", scale=1, color="#2563eb", label="VR")
ax.quiver(VR, 0, 0, VL, angles="xy", scale_units="xy", scale=1, color="#16a34a", label="VL")
ax.quiver(VR, 0, 0, 0, -VC, angles="xy", scale_units="xy", scale=1, color="#dc2626", label="VC")
ax.quiver(0, 0, VR, VL-VC, angles="xy", scale_units="xy", scale=1, color="#7c3aed", label="Vs (resultan)")
ax.set_xlabel("Komponen sefase arus (V)")
ax.set_ylabel("Komponen reaktif (V)")
ax.set_title("Fasor tegangan RLC seri (arus sebagai referensi)")
ax.grid(True, alpha=0.25)
ax.legend()
maxval = max(VR, VL, VC, Vs, 1)
ax.set_xlim(-0.1*maxval, 1.2*maxval)
ax.set_ylim(-1.2*maxval, 1.2*maxval)
st.pyplot(fig, use_container_width=True)
plt.close(fig)

st.subheader("Grafik gelombang tegangan dan arus")
t = np.linspace(0, 2/f, 1200)
i_t = Ipeak * np.sin(w*t - phi)
vR_t = Ipeak * R * np.sin(w*t - phi)
vL_t = Ipeak * XL * np.sin(w*t - phi + np.pi/2)
vC_t = Ipeak * XC * np.sin(w*t - phi - np.pi/2)
vS_t = vR_t + vL_t + vC_t
fig2, ax2 = plt.subplots(figsize=(10, 4.5))
ax2.plot(t*1000, vS_t, label="Vs(t)", linewidth=2)
ax2.plot(t*1000, vR_t, label="VR(t)")
ax2.plot(t*1000, vL_t, label="VL(t)")
ax2.plot(t*1000, vC_t, label="VC(t)")
ax2.set_xlabel("Waktu (ms)")
ax2.set_ylabel("Tegangan (V)")
ax2.set_title("Gelombang tegangan sesaat pada rangkaian RLC")
ax2.grid(True, alpha=0.25)
ax2.legend(ncol=4)
st.pyplot(fig2, use_container_width=True)
plt.close(fig2)

st.subheader("Verifikasi Hukum Kirchhoff Tegangan (KVL)")
V_resultant = np.sqrt(VR**2 + (VL-VC)**2)
err = abs(V_resultant - Vs)
c1, c2 = st.columns(2)
c1.metric("Tegangan resultan", f"{V_resultant:.4f} V")
c2.metric("Selisih dari Vs", f"{err:.6f} V")
st.latex(r"\underline{V_s}=\underline{V_R}+\underline{V_L}+\underline{V_C}")
st.write("Dalam rangkaian AC, KVL diterapkan sebagai penjumlahan **fasor** tegangan, bukan penjumlahan sederhana nilai RMS magnitudo. Karena itu, tegangan sumber memenuhi hubungan fasor antara komponen resistif dan reaktif.")

if abs(X) < 0.05 * R:
    st.success("Rangkaian mendekati kondisi resonansi: XL dan XC relatif berdekatan.")
elif X > 0:
    st.info("Sifat rangkaian dominan induktif: XL > XC, sehingga arus tertinggal terhadap tegangan sumber.")
else:
    st.info("Sifat rangkaian dominan kapasitif: XC > XL, sehingga arus mendahului tegangan sumber.")

st.caption("Catatan: animasi arus adalah visualisasi konseptual. Perhitungan menggunakan model ideal RLC seri pada keadaan tunak sinusoidal.")
