import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Configuração da página
st.set_page_config(page_title="Exercício 2 - Soma de Vetores", layout="wide")
st.title("📐 Exercício 2 - Soma de Vetores")
st.markdown("""
**Enunciado:** Um corredor se desloca 145 m em direção nordeste fazendo 20° com a direção norte (vetor deslocamento A) e depois 105 m em direção sudeste fazendo 35,0° com a direção leste (vetor deslocamento B). Usando componentes, determine o módulo, a direção e o sentido do vetor C resultante destes dois deslocamentos.
""")

st.divider()

# Dados do problema
mag_a = 145.0  # m
angle_a_north = 20.0  # graus
mag_b = 105.0  # m
angle_b_east = 35.0  # graus

# Solução passo a passo
st.header("🔍 Resolução passo a passo")

# Passo 1: Decomposição dos vetores A e B em componentes
st.subheader("Passo 1: Decomposição dos vetores em componentes")

# Ângulos em relação ao eixo +x
angle_a = 90.0 - angle_a_north
angle_b = -angle_b_east

# Componentes de A
a_x = mag_a * np.cos(np.radians(angle_a))
a_y = mag_a * np.sin(np.radians(angle_a))

st.markdown("### Vetor A")
st.latex(f"A_x = |A| \\cdot \\cos({angle_a}^\\circ) = 145 \\cdot \\cos(70^\\circ) \\approx \\boxed{{{a_x:.2f}}} \\text{{m}}")
st.latex(f"A_y = |A| \\cdot \\sin({angle_a}^\\circ) = 145 \\cdot \\sin(70^\\circ) \\approx \\boxed{{{a_y:.2f}}} \\text{{m}}")

# Componentes de B
b_x = mag_b * np.cos(np.radians(angle_b))
b_y = mag_b * np.sin(np.radians(angle_b))

st.markdown("### Vetor B")
st.latex(f"B_x = |B| \\cdot \\cos({angle_b}^\\circ) = 105 \\cdot \\cos(-35^\\circ) \\approx \\boxed{{{b_x:.2f}}} \\text{{m}}")
st.latex(f"B_y = |B| \\cdot \\sin({angle_b}^\\circ) = 105 \\cdot \\sin(-35^\\circ) \\approx \\boxed{{{b_y:.2f}}} \\text{{m}}")

st.divider()

# Passo 2: Componentes do vetor resultante C
st.subheader("Passo 2: Componentes do vetor resultante C")
c_x = a_x + b_x
c_y = a_y + b_y

st.latex(f"C_x = A_x + B_x = {a_x:.2f} + {b_x:.2f} = \\boxed{{{c_x:.2f}}} \\text{{m}}")
st.latex(f"C_y = A_y + B_y = {a_y:.2f} + {b_y:.2f} = \\boxed{{{c_y:.2f}}} \\text{{m}}")

st.divider()

# Passo 3: Cálculo do módulo de C
st.subheader("Passo 3: Cálculo do módulo de C")
modulo_c = np.sqrt(c_x**2 + c_y**2)

st.latex(f"|\\vec{{C}}| = \\sqrt{{C_x^2 + C_y^2}} = \\sqrt{{({c_x:.2f})^2 + ({c_y:.2f})^2}} = \\boxed{{{modulo_c:.2f}}} \\text{{m}}")

st.divider()

# Passo 4: Direção e sentido do vetor resultante
st.subheader("Passo 4: Direção e sentido do vetor resultante")
angle_c_rad = np.arctan2(c_y, c_x)
angle_c_deg = np.degrees(angle_c_rad)

st.latex(f"\\tan(\\theta) = \\frac{{C_y}}{{C_x}} = \\frac{{{c_y:.2f}}}{{{c_x:.2f}}}")
st.latex(f"\\theta = \\arctan\\left(\\frac{{{c_y:.2f}}}{{{c_x:.2f}}}\\right) \\approx \\boxed{{{angle_c_deg:.2f}^\\circ}}")
st.markdown(f"Como as componentes $C_x$ e $C_y$ são positivas, o vetor resultante C está no primeiro quadrante, com um ângulo de **{angle_c_deg:.2f}°** em relação ao eixo leste.")

st.divider()

# Visualização gráfica
st.header("📊 Visualização Gráfica")

# Configuração do gráfico
fig, ax = plt.subplots(figsize=(8, 8))

# Vetores
ax.quiver(0, 0, a_x, a_y, angles='xy', scale_units='xy', scale=1, color='blue', label=f'A ({mag_a} m)')
ax.quiver(a_x, a_y, b_x, b_y, angles='xy', scale_units='xy', scale=1, color='red', label=f'B ({mag_b} m)')
ax.quiver(0, 0, c_x, c_y, angles='xy', scale_units='xy', scale=1, color='purple', width=0.005, label=f'C ({modulo_c:.2f} m)')

# Configurações do gráfico
ax.set_xlim([-10, 160])
ax.set_ylim([-10, 160])
ax.set_xlabel('Eixo x (m)')
ax.set_ylabel('Eixo y (m)')
ax.grid(True)
ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
ax.axvline(x=0, color='k', linestyle='-', alpha=0.3)
ax.set_title('Soma Vetorial: A + B = C')
ax.legend(loc='upper left')
ax.set_aspect('equal')
st.pyplot(fig)

st.divider()

# Conclusão
st.header("✅ Conclusão")
st.markdown(f"""
**Resultado final:**
| Grandeza | Valor |
| :--- | :--- |
| Módulo de **C** | $\\boxed{{{modulo_c:.2f}}} \\text{{m}}$ |
| Ângulo **θ** | $\\boxed{{{angle_c_deg:.2f}^\\circ}}$ |
| Sentido | Nordeste |
""")
