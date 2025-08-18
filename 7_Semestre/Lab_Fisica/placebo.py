import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Arc

# Configuração da página
st.set_page_config(page_title="Resolução de Vetores", layout="wide")
st.title("📐 Exercício 3 - Decomposição Vetorial")
st.markdown("""
**Enunciado:**  
Três vetores de deslocamento **A**, **B** e **C** são dispostos sequencialmente. 
A soma resultante **R** é paralela ao eixo **x**. Determine:
1. O módulo do vetor resultante **|R|**  
2. O ângulo **θ** que define sua direção  

**Dados:**  
- |**A**| = 35.0 m (direção horizontal)  
- |**B**| = 23.0 m (ângulo de 50.0° com o eixo +x)  
- |**C**| = 10.0 m (direção vertical, sentido -y)
""")

st.divider()

# Solução passo a passo
st.header("🔍 Resolução passo a passo")

# Passo 1: Decomposição vetorial
st.subheader("Passo 1: Decomposição dos vetores em componentes")

st.markdown(r"""
### Vetor A (horizontal, +x):
$$
\begin{cases}
A_x = 35.0  \text{m} \\
A_y = 0
\end{cases}
$$

### Vetor B (50.0° com +x):
$$
\begin{cases}
B_x = |B| \cdot \cos(50^\circ) = 23.0 \cdot \cos(50^\circ) \\
B_y = |B| \cdot \sin(50^\circ) = 23.0 \cdot \sin(50^\circ)
\end{cases}
$$

### Vetor C (vertical, -y):
$$
\begin{cases}
C_x = 0 \\
C_y = -10.0  \text{m}
\end{cases}
$$
""")

# Cálculos numéricos
b_x = 23.0 * np.cos(np.radians(50))
b_y = 23.0 * np.sin(np.radians(50))

st.markdown(f"""
**Cálculos:**  
- $B_x = 23.0 \\times \\cos(50^\\circ) \\approx 23.0 \\times 0.6428 = \\boxed{{{b_x:.2f}  \\text{{m}}}$  
- $B_y = 23.0 \\times \\sin(50^\\circ) \\approx 23.0 \\times 0.7660 = \\boxed{{{b_y:.2f}  \\text{{m}}}$
""")

# Passo 2: Componentes da resultante
st.subheader("Passo 2: Componentes do vetor resultante R")
st.markdown(r"""
Como **R** é paralelo ao eixo **x**, temos:
$$
R_y = 0
$$

A componente vertical total deve satisfazer:
$$
R_y = A_y + B_y + C_y = 0
$$
""")

st.divider()

# Passo 3: Cálculo do módulo
st.subheader("Passo 3: Cálculo do módulo de R")

st.markdown(r"""
Componentes de **R**:
$$
\begin{cases}
R_x = A_x + B_x + C_x = 35.0 + 14.78 + 0 \\
R_y = A_y + B_y + C_y = 0 + 17.62 + (-10.0)
\end{cases}
$$

Módulo de **R**:
$$
|\vec{R}| = \sqrt{R_x^2 + R_y^2}
$$
""")

# Cálculos finais
r_x = 35.0 + b_x
r_y = b_y - 10.0
modulo_r = np.sqrt(r_x**2 + r_y**2)

st.markdown(f"""
**Resultados:**  
- $R_x = 35.0 + {b_x:.2f} + 0 = \\boxed{{{r_x:.2f}  \\text{{m}}}$  
- $R_y = 0 + {b_y:.2f} - 10.0 = \\boxed{{{r_y:.2f}  \\text{{m}}}$  
- $|\vec{{R}}| = \sqrt{{ ({r_x:.2f})^2 + ({r_y:.2f})^2 }} = \\boxed{{{modulo_r:.1f}  \\text{{m}}}$
""")

# Passo 4: Direção do vetor
st.subheader("Passo 4: Direção do vetor resultante")
st.markdown(r"""
Como **R** é paralelo ao eixo **x**:
$$
\theta = 0^\circ \quad \text{(sentido positivo do eixo x)}
$$

O ângulo de 59.9° mencionado na apostila refere-se ao vetor **B**, não ao resultante **R**.
""")

st.divider()

# Visualização gráfica
st.header("📊 Visualização Gráfica")

# Configuração do gráfico
fig, ax = plt.subplots(figsize=(10, 6))

# Vetores
ax.quiver(0, 0, 35, 0, angles='xy', scale_units='xy', scale=1, color='blue', label='A (35.0 m)')
ax.quiver(35, 0, b_x, b_y, angles='xy', scale_units='xy', scale=1, color='red', label='B (23.0 m)')
ax.quiver(35+b_x, b_y, 0, -10, angles='xy', scale_units='xy', scale=1, color='green', label='C (10.0 m)')
ax.quiver(0, 0, r_x, r_y, angles='xy', scale_units='xy', scale=1, color='purple', width=0.005, label=f'R ({modulo_r:.1f} m)')

# Configurações do gráfico
ax.set_xlim([0, 60])
ax.set_ylim([-15, 25])
ax.set_xlabel('Eixo x (m)')
ax.set_ylabel('Eixo y (m)')
ax.grid(True)
ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
ax.axvline(x=0, color='k', linestyle='-', alpha=0.3)
ax.set_title('Soma Vetorial: A + B + C = R')
ax.legend(loc='upper right')
ax.set_aspect('equal')

# Anotações
ax.text(17, -1, "A", fontsize=12, color='blue')
ax.text(40, 10, "B", fontsize=12, color='red')
ax.text(49, 5, "C", fontsize=12, color='green')
ax.text(20, 5, "R", fontsize=12, color='purple')

# Mostrar o gráfico no Streamlit
st.pyplot(fig)

st.divider()

# Conclusão
st.header("✅ Conclusão")
st.markdown(f"""
**Resultado final:**  
| Grandeza       | Valor              |
|----------------|--------------------|
| Módulo de **R** | $\\boxed{{{modulo_r:.1f}  \\text{{m}}}$ |
| Ângulo **θ**   | $\\boxed{{0^\\circ}}$ |

**Fundamentação teórica:**  
- Decomposição vetorial (p. 33-39 da apostila)  
- Soma por componentes (p. 40-45 da apostila)
""")

st.info("""
**Nota explicativa:**  
O ângulo de 59.9° mencionado na apostila refere-se à direção do vetor **B**, não ao resultado. 
O vetor resultante **R** é paralelo ao eixo **x**, portanto seu ângulo é 0°.
""")