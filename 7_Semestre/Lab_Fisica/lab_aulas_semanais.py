import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Arc

def exercises_2():
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

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.quiver(0, 0, a_x, a_y, angles='xy', scale_units='xy', scale=1, color='blue', label=f'A ({mag_a} m)')
    ax.quiver(a_x, a_y, b_x, b_y, angles='xy', scale_units='xy', scale=1, color='red', label=f'B ({mag_b} m)')
    ax.quiver(0, 0, c_x, c_y, angles='xy', scale_units='xy', scale=1, color='purple', width=0.005, label=f'C ({modulo_c:.2f} m)')

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

def exercises_3():
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

    st.header("🔍 Resolução passo a passo")

    st.subheader("Passo 1: Decomposição dos vetores em componentes")

    st.markdown(r"""
    ### Vetor A (horizontal, +x):
    $$
    \begin{cases}
    A_x = 35.0 \text{m} \\
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
    C_y = -10.0 \text{m}
    \end{cases}
    $$
    """)

    b_x = 23.0 * np.cos(np.radians(50))
    b_y = 23.0 * np.sin(np.radians(50))

    st.markdown(f"""
    **Cálculos:**
    - $B_x = 23.0 \\times \\cos(50^\\circ) \\approx 23.0 \\times 0.6428 = \\boxed{{{b_x:.2f}}} \\text{{m}}$
    - $B_y = 23.0 \\times \\sin(50^\\circ) \\approx 23.0 \\times 0.7660 = \\boxed{{{b_y:.2f}}} \\text{{m}}$
    """)

    st.subheader("Passo 2: Componentes do vetor resultante R")

    st.markdown(r"""
    A componente total da resultante é a soma das componentes de cada vetor:
    $$
    \begin{cases}
    R_x = A_x + B_x + C_x \\
    R_y = A_y + B_y + C_y
    \end{cases}
    $$
    """)

    st.divider()

    st.subheader("Passo 3: Cálculo do módulo de R")
    r_x = 35.0 + b_x + 0
    r_y = 0 + b_y - 10.0
    modulo_r = np.sqrt(r_x**2 + r_y**2)

    st.markdown(r"""
    Componentes de **R**:
    $$
    \begin{cases}
    R_x = A_x + B_x + C_x \\
    R_y = A_y + B_y + C_y
    \end{cases}
    $$
    """)

    st.markdown(f"""
    **Resultados dos componentes:**
    - $R_x = 35.0 + {b_x:.2f} + 0 = \\boxed{{{r_x:.2f}}} \\text{{m}}$
    - $R_y = 0 + {b_y:.2f} - 10.0 = \\boxed{{{r_y:.2f}}} \\text{{m}}$
    """)

    st.markdown(r"""
    Módulo de **R**:
    $$
    |\vec{R}| = \sqrt{R_x^2 + R_y^2}
    $$
    """)

    st.subheader("Cálculo do Módulo")
    st.latex(
        f"|\\vec{{R}}| = \\sqrt{{({r_x:.2f})^2 + ({r_y:.2f})^2}} = \\boxed{{{modulo_r:.1f}}} \\text{{m}}"
    )
    st.subheader("Passo 4: Direção do vetor resultante")
    angulo_r_rad = np.arctan2(r_y, r_x)
    angulo_r_deg = np.degrees(angulo_r_rad)

    st.markdown(r"""
    O ângulo $\theta$ é calculado pela tangente:
    $$
    \tan(\theta) = \frac{R_y}{R_x}
    $$
    """)

    st.markdown(f"""
    **Cálculo do Ângulo:**
    - $\\tan(\\theta) = \\frac{{{r_y:.2f}}}{{{r_x:.2f}}} \\implies \\theta \\approx \\boxed{{{angulo_r_deg:.1f}^\\circ}}$
    """)

    st.divider()

    st.header("📊 Visualização Gráfica")

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.quiver(0, 0, 35, 0, angles='xy', scale_units='xy', scale=1, color='blue', label='A (35.0 m)')
    ax.quiver(35, 0, b_x, b_y, angles='xy', scale_units='xy', scale=1, color='red', label='B (23.0 m)')
    ax.quiver(35 + b_x, b_y, 0, -10, angles='xy', scale_units='xy', scale=1, color='green', label='C (10.0 m)')
    ax.quiver(0, 0, r_x, r_y, angles='xy', scale_units='xy', scale=1, color='purple', width=0.005, label=f'R ({modulo_r:.1f} m)')

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
    st.pyplot(fig)

    st.divider()

    st.header("✅ Conclusão")
    st.markdown(f"""
    **Resultado final:**
    | Grandeza | Valor |
    |---|---|
    | Módulo de **R** | $\\boxed{{{modulo_r:.1f}}} \\text{{m}}$ |
    | Ângulo **θ** | $\\boxed{{{angulo_r_deg:.1f}^\\circ}}$ |

    **Fundamentação teórica:**
    - Decomposição vetorial (p. 33-39 da apostila)
    - Soma por componentes (p. 40-45 da apostila)
    """)

    st.info("""
    **Nota explicativa:**
    Existe uma contradição entre os dados fornecidos e a afirmação do enunciado de que a resultante R é paralela ao eixo x. Os cálculos demonstram que, com os dados fornecidos, a resultante possui uma componente vertical ($R_y \\neq 0$) e, portanto, não é paralela ao eixo x. O exercício foi resolvido considerando os dados e calculando a resultante, que tem um ângulo de aproximadamente 8.7° com o eixo x.
    """)

def main():
    st.sidebar.header("🏡Exercícios para Casa - Semana 2")
    exercises = st.sidebar.selectbox("Exercícios", ["Exercício 2", "Exercício 3"])
    if exercises == "Exercício 2":
        exercises_2()
    elif exercises == "Exercício 3":
        exercises_3()

if __name__ == "__main__":
    main()
