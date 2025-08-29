# Aula Teórica de Física Mecânica 
# rev.1a 28-08-2025 

# Interface
import streamlit as st
# Listas e Matrizes
import pandas as pd
import numpy as np
# Calculos
import numbers
import math
# Listas

# IO e Imagens
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Arc
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import os 


# ------------------------------------------------------------
# Configuração geral
# ------------------------------------------------------------

#==============================================================================
#                                  Semana 4 - Física Mecânica
#==============================================================================
# =========================
# Utilidades de desenho
# =========================

def _set_axes(ax, lim=1.1):
    ax.axhline(0, lw=0.8, color="black", alpha=0.6)
    ax.axvline(0, lw=0.8, color="black", alpha=0.6)
    ax.set_aspect("equal", adjustable="datalim")
    ax.grid(True, linestyle=":", alpha=0.4)
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)

def draw_vector(ax, vec, label, color="C0", origin=(0,0)):
    ox, oy = origin
    ax.quiver(ox, oy, vec[0], vec[1], angles="xy", scale_units="xy", scale=1, color=color)
    ax.text(ox + vec[0]*1.04, oy + vec[1]*1.04, label, color=color, fontsize=10, ha="left", va="bottom")

def draw_components(ax, vec, color="gray", alpha=0.7):
    # traça projeções no x e y a partir da ponta do vetor
    x, y = vec
    ax.plot([0, x, x], [y, y, 0], linestyle="--", color=color, alpha=alpha)

def figure_vectors(vectors, title="", lim_auto=True, lim_val=1.1):
    fig, ax = plt.subplots()
    # calcula limite automático a partir dos vetores
    if lim_auto and vectors:
        xs = [abs(v[0][0]) for v in vectors]
        ys = [abs(v[0][1]) for v in vectors]
        m = max([1e-9] + xs + ys)
        lim_val = 1.2*m
    _set_axes(ax, lim=lim_val)
    for (vec, label, color) in vectors:
        draw_vector(ax, vec, label, color)
        draw_components(ax, vec)
    ax.set_title(title)
    return fig

def deg(x):  # atalho para converter rad em graus
    return x*180.0/math.pi

def rad(x):  # atalho para converter graus em rad
    return x*math.pi/180.0

# =========================
# Exercício 2 - Teoria
# =========================
def ex4_2_theory():
    st.title("Exercício 2 — Alpinista e limite de tração")
    
    m = 90.0
    g = 9.8
    P = m*g                      # peso (N)
    Tmax = 1500.0               # tração limite na corda 3 (N)

    st.subheader("Dados")
    st.markdown(f"- Massa do alpinista: **{m:.0f} kg**  \n- Aceleração da gravidade: **{g:.2f} m/s²**  \n- Peso: **P = {P:.2f} N**  \n- Tração máxima na corda 3: **T₃ₘₐₓ = {Tmax:.0f} N**")

    st.subheader("Observação importante sobre a figura")
    st.markdown(
        "Como o enunciado do PDF usa **três cordas** e mede o ângulo de forma específica no desenho, há mais de uma maneira de "
        "definir o ângulo θ (com a **vertical**, com a **horizontal**, ou ainda entre a **corda 3** e outra corda). "
        "Para fins de apresentação, mostro **duas leituras** didáticas e indico qual delas reproduz o **gabarito oficial (30,45°)**."
    )

    colA, colB = st.columns(2, gap="large")

    # --- Interpretação A: configuração simétrica (duas cordas idênticas sustentando P)
    with colA:
        st.markdown("**Interpretação A (simétrica clássica)**")
        st.latex(r""" \text{Equilíbrio vertical: } \\
                 2T\sin\theta = P \Rightarrow \sin\theta = \frac{P}{2T_{\max}} """)
        thetaA = math.degrees(math.asin(P/(2*Tmax)))  # 17,1°
        st.latex(r" \theta_A = \arcsin\!\Big(\frac{P}{2T_{\max}}\Big) ")
        st.info(f"θ_A ≈ {thetaA:.2f}° (ângulo da **corda com a horizontal** em uma configuração simétrica).")

        # diagrama A
        T = Tmax
        thetaA_rad = rad(thetaA)
        T1 = np.array([ -(T*math.cos(thetaA_rad)),  T*math.sin(thetaA_rad)])
        T2 = np.array([T*math.cos(thetaA_rad),  T*math.sin(thetaA_rad)])
        Pvec = np.array([0.0, -P])
        figA = figure_vectors(
            [(T1, "T₁", "C0"), (T2, "T₂", "C2"), (Pvec, "P", "C3")],
            title="Interpretação A (simétrica)"
        )
        st.pyplot(figA, use_container_width=True)

    # --- Interpretação B: ângulo como no gabarito (30,45°)
    with colB:
        st.markdown("**Interpretação B compatível aproximada**")
        st.markdown(
            "Pelo desenho do material, mede-se **θ** de forma a obter a relação "
            r"$\tan\theta = \dfrac{P}{T_{3,\max}}$ no limite de ruptura. Assim:"
        )
        st.latex(r"\theta_B = \arctan\!\Big(\frac{P}{T_{3,\max}}\Big)")
        thetaB = math.degrees(math.atan(P/Tmax))      # 30,45°
        st.success(f"θ_B ≈ **{thetaB:.2f}°**  ← *Resposta aproxiamada da oficial*")

        # Diagrama conceitual B (T3 com módulo no limite e P horizontal/vertical compondo)
        thetaB_rad = rad(thetaB)
        T3 = np.array([-(Tmax*math.cos(thetaB_rad)), Tmax*math.sin(thetaB_rad)])
        Pvec = np.array([0.0, -P])
        # um cabo auxiliar horizontal equilibraria a componente horizontal de T3
        H = np.array([-T3[0], 0.0])
        figB = figure_vectors(
            [(T3, "T₃", "C0"), (H, "Reação/corda horizontal", "C2"), (Pvec, "P", "C3")],
            title="Interpretação B compatível aproximada"
        )
        st.pyplot(figB, use_container_width=True)

    st.caption("As diferentes **referências de ângulo** levam a números diferentes; a atividade adota a Interpretação B para obter 30,45°.")

# =========================
# Exercício 3 - Teoria
# =========================
def ex4_3_theory():
    st.title("Exercício 3 — Motor no anel, duas trações e o peso")

    W = 3150.0  # N

    st.subheader("Dados do enunciado")
    st.markdown("- Peso do motor: **W = 3150 N**  \n- Ângulos marcados no slide: **10°** e **80°** (conforme a figura)")

    st.subheader("Equilíbrio no nó")
    st.latex(r"""
    \begin{aligned}
    \sum F_x &= 0 \\
    \sum F_y &= 0
    \end{aligned}
    """)

    st.markdown(
        "Há **ambiguidade** comum: os 10°/80° podem estar **com a vertical** ou **com a horizontal**, e o lado (esquerda/direita) "
        "muda os **sinais** das componentes. Para apresentação, mostro duas leituras:"
    )

    tab1, tab2 ,tab3= st.tabs(["Leitura literal do desenho (10° com a vertical / 80° com a horizontal)", 
                          "Leitura alternativa 1","Leitura alternativa 2"])

    st.info("""
    Cada aba possui um código de implementação, que foi mantido como exemplo, 
    e todos se baseiam uma decomposição de componentes diferente resultando em
    uma abordagem e resultados diferentes)
    """)
    # --- Leitura 1: T1 10° com a vertical (à esquerda), T2 80° com a horizontal (à direita)
    with tab1:
        st.markdown("**Leitura 1 (literal):** T₁ faz **10° com a vertical** à esquerda; T₂ faz **80° com a horizontal** à direita.")
        a1 = rad(10.0)   # ângulo de T1 com a vertical
        b1 = rad(80.0)   # ângulo de T2 com a horizontal

        # Componentes escolhendo +x para a direita e +y para cima
        # T1 inclina à esquerda: x = -T1*sin(10°), y =  T1*cos(10°)
        # T2 inclina para cima à direita com 80° da horizontal: x =  T2*cos(80°), y = T2*sin(80°)
        A = np.array([
            [-math.sin(a1),  math.cos(b1)],  # Fx: -T1*sin(a1) + T2*cos(b1) = 0
            [ math.cos(a1),  math.sin(b1)]   # Fy:  T1*cos(a1) + T2*sin(b1) = W
        ], dtype=float)
        b = np.array([0.0, W], dtype=float)
        T1, T2 = np.linalg.solve(A, b)
        
        st.latex(r"""
        \begin{cases}
        -\,T_1\sin(10^\circ)+T_2\sin(80^\circ)=0\\
        T_1\cos(10^\circ)+T_2\cos(80^\circ)=3150
        \end{cases}
        """)
        
        st.markdown(f"**Resultado desta leitura:** T₁ ≈ **{T1:.2f} N**, T₂ ≈ **{T2:.2f} N** (nesse arranjo, ficam praticamente iguais, ~1600 N cada).")

        # Diagrama
        T1_vec = np.array([-T1*math.sin(a1),  T1*math.cos(a1)])
        T2_vec = np.array([ T2*math.cos(b1),  T2*math.sin(b1)])
        W_vec  = np.array([0.0, -W])
        fig1 = figure_vectors([(T1_vec, "T₁", "C0"), (T2_vec, "T₂", "C2"), (W_vec, "W", "C3")],
                              title="Leitura 1 (literal)")
        st.pyplot(fig1, use_container_width=True)
        st.warning("Perceba que esta leitura **não** reproduz o objetivado.")

    # --- Leitura 2: compatível com gabarito (T1 próximo da horizontal à esquerda; T2 próximo da vertical à direita)
    with tab2:
        st.markdown(
            "**Leitura 2 aproximada:** considere T₁ fazendo **10° com a horizontal (à esquerda)** e T₂ fazendo **10° com a vertical (à direita)**."
        )
        alpha = rad(10.0)  # T1 com a horizontal
        beta  = rad(10.0)  # T2 com a vertical

        # Componentes:
        # T1 à esquerda e levemente para cima: x = -T1*cos(alpha), y = T1*sin(alpha)
        # T2 à direita e quase vertical:       x =  T2*sin(beta),  y = T2*cos(beta)
        A2 = np.array([
            [-math.cos(alpha),  math.sin(beta)],   # Fx: -T1 cos a + T2 sin b = 0
            [ math.sin(alpha),  math.cos(beta)]    # Fy:  T1 sin a + T2 cos b = W
        ], dtype=float)
        b2 = np.array([0.0, W], dtype=float)
        T1b, T2b = np.linalg.solve(A2, b2)

        st.latex(r"""
        \begin{cases}
        -\,T_1\cos(10^\circ)+T_2\sin(80^\circ)=0\\
        T_1\sin(10^\circ)+T_2\cos(80^\circ)=3150
        \end{cases}
        """)
        st.markdown(
            "Da 1ª equação: "
            r"$T_2 = T_1\cot(10^\circ)$; substituindo na 2ª, resulta "
            r"$T_1 = W\sin(10^\circ)$ e $T_2 = W\cos(10^\circ)$."
        )
        T1b_analit = W*math.sin(alpha)
        T2b_analit = W*math.cos(alpha)
        st.markdown(f"**Cálculo analítico:** T₁ = W·sin(10°) ≈ **{T1b_analit:.2f} N**;  T₂ = W·cos(10°) ≈ **{T2b_analit:.2f} N**.")

        st.info(
            "Com esses ângulos, obtemos valores **próximos** da resposta objetivada. "
            "Pequenas diferenças (≈5–6%) podem vir de **arredondamentos** do desenho/ângulos e da leitura no slide."
        )
        st.info(f"""
                Resposta final : **T₁ = {T1b:.0f} N; T₂ = {T2b:.0f} N**
                \nEsta difere do objetivado
                """)

        # Diagrama
        T1_vec = np.array([-T1b*math.cos(alpha),  T1b*math.sin(alpha)])
        T2_vec = np.array([ T2b*math.sin(beta),   T2b*math.cos(beta)])
        W_vec  = np.array([0.0, -W])
        fig2 = figure_vectors([(T1_vec, "T₁", "C0"), (T2_vec, "T₂", "C2"), (W_vec, "W", "C3")],
                              title="Leitura 2 aproximação e hipótese")
        st.pyplot(fig2, use_container_width=True)
    with tab3: 
        st.info("""Internamente o código tem sua própria abordagem, mas foi deixado comentado a lógica da professora
        nos comentários e seu raciocínio foi deixado na descrição das fórmulas para cálculo sem recurso computacional""")
        st.markdown(
            "**Leitura 3:** considere T₁ fazendo **10° com a horizontal (à esquerda)** e T₂ fazendo **80° com a horizontal (à direita)**."
        )
        #================================================================================
        # Ângulos em radianos  (Abordagem do código)
        
        theta1 = math.radians(10)   # T1
        theta2 = math.radians(80)   # T2
        #================================================================================
        # Ângulos em graus (Abordagem da professora)
        # theta1 = math.degree(10)   # T1
        # theta2 = math.degree(80)   # T2
        
        #================================================================================
        # Matrizes de equilíbrio  (Abordagem do código)
        # ΣFx = T1 cosθ1 + T2 cosθ2 = 0
        # ΣFy = T1 sinθ1 + T2 sinθ2 - W = 0
        A = np.array([
            [math.cos(theta1), math.cos(theta2)],
            [math.sin(theta1), math.sin(theta2)]
        ])
        #================================================================================
        # Matrizes de equilíbrio (Abordagem da professora)
        # ΣFx = T1 sinθ1 + T2 sinθ2 = 0
        # ΣFy = T1 cosθ1 + T2 cosθ2 - W = 0
        #A = np.array([
         #   [math.sin(theta1), math.sin(theta2)],
          #  [math.cos(theta1), math.cos(theta2)]
        #])
        #================================================================================
        b = np.array([0.0, W])  # lado direito (Fx=0, Fy=W para equilibrar peso)

        #================================================================================
        # Resolve sistema linear  (Abordagem do código)
        T1, T2 = np.linalg.solve(A, b)

        st.latex(r"""
        \begin{cases}
        -\,T_1\sin(10^\circ)+T_2\sin(80^\circ)=0\\
        T_1\cos(10^\circ)+(-\,T_2\cos(80^\circ))=3150
        \end{cases}
        """)

        sum_T2f = math.cos(theta1) - ((math.sin(theta1)/math.sin(theta2)) * math.cos(theta2))

        
        st.markdown("""
        #### Deixando em termos de $T_1$ para obter $T_2$:
        """)
        st.latex(r"""
        T_2 = \frac{T_1 \sin(10^\circ)}{\sin(80^\circ)}
        """)
        st.latex(r"""
        T_1 \cos(10^\circ) - \frac{T_1 \sin(10^\circ)}{\sin(80^\circ)} \cos(80^\circ) = 3150
        """)
        st.latex(fr"""T_1 ({math.cos(theta1):.4f}-{(math.sin(theta1)/math.sin(theta2))*math.cos(theta2):.4f}) = 3150 
        """)
        st.latex(fr"""T_1 = \frac{{3150}}{{{sum_T2f:.4f}}} \approx {{{abs(T2):.4f}}}
        """
        )
        st.markdown("#### Calculando valor de $T_2$:")
        st.latex(r"""
        T_1 \sin(10^\circ) = T_2 \sin(80^\circ)
        """)
        st.latex(r"""
        T_2 = \frac{T_1 \sin(10^\circ)}{\sin(80^\circ)} = """fr"""
         \frac{{{T2:.2f} \times {math.sin(theta1):.4f}}}{{{math.sin(theta2):.4f}}} \approx {{{abs(T1):.2f}}}
        """)
        st.success(r"##### Resultados: $T_2 \approx$ "f"{abs(T1):.2f}"r" N ; $T_1 \approx$  "f"{T2:.2f} N")

        # Vetores para plotagem
        T1_vec = np.array([-(T1*math.cos(theta1)), T1*math.sin(theta1)])
        T2_vec = np.array([-(T2*math.cos(theta2)), T2*math.sin(theta2)])
        W_vec  = np.array([0.0, -W])

        fig = figure_vectors(
            [(T1_vec, "T₂", "C0"), (T2_vec, "T₁", "C2"), (W_vec, "W", "C3")],
            title="Diagrama — Exercicio 3 C"
        )
        st.pyplot(fig, use_container_width=True)


# =========================
# Exercício 4 - Teoria
# =========================
def ex4_4_theory():
    st.title("Exercício 4 — Cabo de guerra bidimensional (Crossfit)")
    st.subheader("Dados")
    FA = 220.0  # N (Ana Clara)
    FC = 170.0  # N (Camila) — módulo conhecido; direção a determinar
    st.markdown(f"""- **Ana Clara = F_A** = {FA:.0f} N  
                \n- **Camila = F_C** = {FC:.0f} N (módulo conhecido; direção a achar)
                \n- **Brenda = F_B**: módulo **desconhecido**, direção vertical (para baixo)""")

    st.subheader("Escolha de eixos e ângulos conforme o desenho")
    st.markdown(
        "- Eixo **+x** para a direita; **+y** para cima.  \n"
        "- **F_B** atua em **-y** (vertical para baixo).  \n"
        "- A figura indica **F_A** no 2º quadrante, formando **137°** com o eixo +x (aponta para a esquerda e para cima).  \n"
        "- **F_C** tem módulo 170 N e ângulo **φ** (desconhecido) medido a partir do eixo +x."
    )
    tab1,tab2=st.tabs(["Método Literal", "Metodo até 90 graus"])
    
    with tab1:
        

        st.subheader("Equilíbrio vetorial")
        st.latex(r"\vec F_A + \vec F_B + \vec F_C = \vec 0 \quad \Longrightarrow \quad \begin{cases}\sum F_x = 0\\ \sum F_y = 0\end{cases}")

        # Componentes de FA conhecidos
        thetaA = rad(137.0)
        FAx = FA*math.cos(thetaA)   # negativo
        FAy = FA*math.sin(thetaA)   # positivo

        st.latex(r"""
        \begin{aligned}
        F_{Ax} &= 220\cos(137^\circ) \\
        F_{Ay} &= 220\sin(137^\circ)
        \end{aligned}
        """)

        # Se FC = (FC cosφ, FC sinφ) e FB = (0, -FB), então:
        # Somatório em x: FAx + FC cosφ = 0  -> cosφ = -FAx/FC
        cosphi = -FAx/FC
        # Proteção numérica (limitar ao domínio de arccos)
        cosphi = max(-1.0, min(1.0, cosphi))
        phi = math.acos(cosphi)  # em rad
        phi_deg = deg(phi)

        # Somatório em y: FAy + FC sinφ - FB = 0  -> FB = FAy + FC sinφ
        FB_mod = FAy + FC*math.sin(phi)

        st.markdown("Das componentes:")
        st.latex(r"""
        \begin{cases}
        F_{Ax} + F_C\cos\varphi = 0 \ \Rightarrow\ \cos\varphi = -\dfrac{F_{Ax}}{F_C} \\
        F_{Ay} + F_C\sin\varphi - F_B = 0 \ \Rightarrow\ F_B = F_{Ay} + F_C\sin\varphi
        \end{cases}
        """)
        st.markdown(f"**Ângulo de $F_C$:**  φ ≈ **{phi_deg:.2f}°**  \n**Módulo de $F_B$:**  F_B ≈ **{FB_mod:.2f} N**")

        # Diagramas
        FA_vec = np.array([FAx, FAy])
        FC_vec = np.array([FC*math.cos(phi), FC*math.sin(phi)])
        FB_vec = np.array([0.0, -FB_mod])
        fig = figure_vectors([(FA_vec, "F_A", "C0"), (FC_vec, "F_C", "C2"), (FB_vec, "F_B", "C3")],
                            title="Equilíbrio no pneu (Ex. 4)")
        st.pyplot(fig, use_container_width=True)

        st.caption("Nota: Como a orientação de F_C não é dada explicitamente no texto, aqui ela é **deduzida** do equilíbrio (mantendo os módulos de F_A e F_C).")
    with tab2:
        st.markdown(r"""
        Como Brenda exerce uma força direcionada 0$^\circ$/ 90$^\circ$ S, o ângulo entre Ana Clara se divide em 90$^\circ$ e 47$^\circ$. \
        **Passo 1:** Decompor a Força de Ana Clara ($F_A$): \
        Use a trigonometria para encontrar as componentes horizontal ($F_Ax$) \
        e vertical ($F_Ay$) de $F_A$. \
        Componente x: 
        - $F_Ax$=$F_A \cos(43^\circ)$ 
        - $F_Ax =220 . \cos(43^\circ) \approx 220 . (−\,0,73135) \approx −\,160,90$ N \
        Componente y: 
        - $F_Ay$=$F_A \sin(43^\circ)$ 
        - $F_Ay =220 . \sin(43^\circ) \approx 220 . (0,68199) \approx 150,04$ N \
        **Passo 2:** Encontrar o Ângulo de Camila ($\phi$) \
        Use a condição de equilíbrio no eixo horizontal ($\sum F_x = 0$). \
        A soma das componentes horizontais deve ser zero.
        - $F_Ax + F_C \cos(\phi)= 0$ 
        - $−\,160,90 + 170 \cos(\phi)=0$ 
        - $170 \cos(\phi) = 160,90$ 
        - $\cos( \phi)= \frac {160,90}{170} \approx 0,94647$ \
        Para encontrar o ângulo $\phi$, use a função arco-cosseno ($\arccos$): 
        - $\phi = \arccos (0,94647) \approx 18,83^\circ$
        **Passo 3:** Encontrar o Módulo da Força de Brenda ($F_B$) \
        Use a condição de equilíbrio no eixo vertical ($\sum F_y = 0$). 
        A soma das componentes verticais deve ser zero. Lembre-se que $F_B$ \
        é negativa, pois aponta para baixo.
        - $F_Ay + F_C \sin(\phi) - F_B = 0$ 
        - $150,04 + 170 \sin(18,83^\circ) - F_B = 0$ 
        - $F_B = 150,04 + 170 \sin(18,83^\circ)$
        - $F_B \approx 150,04 + 170 ⋅ (0,3227)$
        - $F_B \approx 150,04+54,86$
        - $F_B \approx 204,90$ N
        """)
        thetaA = rad(137.0)
        FAx = FA*math.cos(thetaA)   # negativo
        FAy = FA*math.sin(thetaA)   # positivo
        cosphi = -FAx/FC
        # Proteção numérica (limitar ao domínio de arccos)
        cosphi = max(-1.0, min(1.0, cosphi))
        phi = math.acos(cosphi)  # em rad
        phi_deg = deg(phi)
        # Somatório em y: FAy + FC sinφ - FB = 0  -> FB = FAy + FC sinφ
        FB_mod = FAy + FC*math.sin(phi)
        # Diagramas
        FA_vec = np.array([FAx, FAy])
        FC_vec = np.array([FC*math.cos(phi), FC*math.sin(phi)])
        FB_vec = np.array([0.0, -FB_mod])
        fig = figure_vectors([(FA_vec, "F_A", "C0"), (FC_vec, "F_C", "C2"), (FB_vec, "F_B", "C3")],
                            title="Equilíbrio no pneu (Ex. 4)")
        st.pyplot(fig, use_container_width=True)

        st.caption("Nota: Como a orientação de F_C não é dada explicitamente no texto, aqui ela é **deduzida** do equilíbrio (mantendo os módulos de F_A e F_C).")
# =========================
# Exercício 5 - Teoria
# =========================
def ex4_5_theory():
    st.title("Exercício 5 — Soma de duas forças com 60° entre elas")
    st.markdown("""
    Dois cachorros puxam horizontalmente cordas amarradas a um poste; o ângulo entre as cordas 
    <br> é igual a 60,0°. Se o cachorro A exerce uma força de 270 N e o cachorro B, uma força de 300 N,
    <br>ache o módulo da força resultante e o ângulo que ela faz com a corda do cachorro A.
    <br>
    Resp.: 494 N e 31,7°""",unsafe_allow_html=True)
    FA = 270.0
    FB = 300.0
    theta = rad(60.0)

    st.subheader("Dados")
    st.markdown(f"- **F_A** = {FA:.0f} N  \n- **F_B** = {FB:.0f} N  \n- Ângulo entre as forças: **60°**")

    st.subheader("Módulo da resultante - Uso da Lei dos Cossenos")
    st.latex(r"R^2 = F_A^2 + F_B^2 + 2F_AF_B\cos(60^\circ)")
    st.latex(fr"""
    R = \sqrt{{F_A^2 + F_B^2 + 2F_AF_B\cos(60^\circ)}}
    """)
    st.latex(fr"""
        R = \sqrt{{{FA:.2f}^2 + {FB:.2f}^2 + 2({FA:.2f})({FB:.2f})\cos(60^\circ)}}
    """)
    R = math.sqrt(FA**2 + FB**2 + 2*FA*FB*math.cos(theta))
    st.markdown(r"**R $\approx$**"f"{R:.2f}"r"**N**")

    st.subheader("Ângulo da resultante com a corda do cachorro A")
    st.latex(r"\frac{\sin\alpha}{F_B} = \frac{\sin(60^\circ)}{R} \ \Rightarrow\ \alpha = \arcsin\!\Big(\frac{F_B\sin 60^\circ}{R}\Big)")
    alpha = math.degrees(math.asin((FB*math.sin(theta))/R))
    st.markdown(r"**$\alpha \approx$**"f"{alpha:.2f}"r"**$\circ$**")
    #st.markdown(f"**α ≈ {alpha:.2f}°**")

    st.success("Conferência com o gabarito: **R ≈ 494 N** e **α ≈ 31,7°**")

    # Diagrama vetorial
    FA_vec = np.array([FA, 0.0])
    FB_vec = np.array([FB*math.cos(theta), FB*math.sin(theta)])
    R_vec  = FA_vec + FB_vec
    fig = figure_vectors([(FA_vec, "F_A", "C0"), (FB_vec, "F_B", "C2"), (R_vec, "R", "C3")],
                         title="Composição de F_A e F_B (Ex. 5)")
    st.pyplot(fig, use_container_width=True)
#=============================================================================
def ex4_2_practice():
    st.subheader("Exercício 2")
    st.markdown("""
    <div>
    Um alpinista de 90 kg está suspenso pela corda mostrada na figura a seguir. A máxima tração que 
    <br>a corda 3 pode suportar sem romper-se é de 1500 N. Qual é o menor valor que o ângulo pode ter
    <br>antes que a corda se rompa e o alpinista cai no desfiladeiro?
    </div>
    """, unsafe_allow_html=True)
    massa = 90.0                                 # Peso do alpinista
    aceleracao_gravidade = 9.8             # Aceleração da gravidade
    forca_P = massa*aceleracao_gravidade            # Força peso (N)
    tracao_max = 1500.0               # Tração limite na corda 3 (N)
    angulo_cords=90               # 90° angulo entre as cordas 2 e 3

    
    st.subheader("Dados")
    st.markdown(
    r"""
    $\text{- Obs.: Peso = Massa} \times \text{Aceleração da gravidade = Kgfm(Kg} \times \text{m/s}^2$)
    """
    f"""
                \n- Massa do alpinista: **{massa:.0f} kg**  
                \n- Aceleração da gravidade: **{aceleracao_gravidade:.2f} m/s²**  
                \n- Peso: **P = {forca_P:.2f} N**  
                \n- Tração máxima na corda 3: **T₃ₘₐₓ = {tracao_max:.0f} N**""")
    st.markdown("**Interpretação compatível com o gabarito da atividade**")
    st.markdown(
        "Pelo desenho do material, mede-se "r"$\theta$"
        " de forma a obter a relação "
        r"$\tan\theta = \dfrac{P}{T_{3\max}}$ no limite de ruptura. Assim:"
    )
    st.latex(r"\theta_B = \arctan\!\Big(\frac{P}{T_{3\max}}\Big)")
    thetaB = math.degrees(math.atan(forca_P/tracao_max))      # 30,45°
    st.success(f"θ_B ≈ **{thetaB:.2f}°**  ← *Resposta aproxiamada da oficial*")

    # Diagrama conceitual B (T3 com módulo no limite e P horizontal/vertical compondo)
    thetaB_rad = rad(thetaB)
    T3 = np.array([-(tracao_max*math.cos(thetaB_rad)), tracao_max*math.sin(thetaB_rad)])
    Pvec = np.array([0.0, -forca_P])
    # um cabo auxiliar horizontal equilibraria a componente horizontal de T3
    H = np.array([-T3[0], 0.0])
    figB = figure_vectors(
        [(T3, "T₃", "C0"), (H, "Reação/corda horizontal", "C2"), (Pvec, "P", "C3")],
        title="Interpretação compatível aproximada)"
    )
    st.pyplot(figB, use_container_width=True)
def ex4_3_practice():
    st.title("Exercício 3 — Motor no anel, duas trações e o peso")

    st.write(""" 
Um motor de automóvel possui um peso  cujo 
módulo é W = 3150 N(0° na divisa entre 3° quadrante e 4° quadrante(270°)). 
Este motor está sendo posicionado acima de um compartimento, como ilustrado 
na Figura a seguir. Para posicionar o motor, um operário está usando 
uma corda. Determine a tração T1(10° no 2° quadrante(100°)) no cabo de sustentação e a 
tração T2(80° no 4° quadrante(350°)) na corda de posicionamento. 
Resp.:582 N; 3300,69N
""")
    

    W = 3150.0  # N

    st.subheader("Dados do enunciado")
    st.markdown("""
        - Peso do motor: **W = 3150 N**
        - Direções: P a 0° (origem para sul)
        - T₁ a 10° (origem para noroeste)
        - T₂ a 80° (origem para sudeste)
    """
    )

    st.info("""**Uso - Abordagem C da Teoria:** Internamente o código tem sua própria abordagem, mas foi deixado comentado a lógica da professora
    nos comentários e seu raciocínio foi deixado na descrição das fórmulas para cálculo sem recurso computacional""")
    st.markdown(
        "**Leitura 3:** considere T₁ fazendo **10° com a horizontal (à esquerda)** e T₂ fazendo **80° com a horizontal (à direita)**."
    )
    #================================================================================
    # Ângulos em radianos  (Abordagem do código)
    
    theta1 = math.radians(10)   # T1
    theta2 = math.radians(80)   # T2
    #================================================================================
    # Ângulos em graus (Abordagem da professora)
    # theta1 = math.degree(10)   # T1
    # theta2 = math.degree(80)   # T2
    
    #================================================================================
    # Matrizes de equilíbrio  (Abordagem do código)
    # ΣFx = T1 cosθ1 + T2 cosθ2 = 0
    # ΣFy = T1 sinθ1 + T2 sinθ2 - W = 0
    A = np.array([
        [math.cos(theta1), math.cos(theta2)],
        [math.sin(theta1), math.sin(theta2)]
    ])
    #================================================================================
    # Matrizes de equilíbrio (Abordagem da professora)
    # ΣFx = T1 sinθ1 + T2 sinθ2 = 0
    # ΣFy = T1 cosθ1 + T2 cosθ2 - W = 0
    #A = np.array([
        #   [math.sin(theta1), math.sin(theta2)],
        #  [math.cos(theta1), math.cos(theta2)]
    #])
    #================================================================================
    b = np.array([0.0, W])  # lado direito (Fx=0, Fy=W para equilibrar peso)

    #================================================================================
    # Resolve sistema linear  (Abordagem do código)
    T1, T2 = np.linalg.solve(A, b)

    st.latex(r"""
    \begin{cases}
    -\,T_1\sin(10^\circ)+T_2\sin(80^\circ)=0\\
    T_1\cos(10^\circ)+(-\,T_2\cos(80^\circ))=3150
    \end{cases}
    """)

    sum_T2f = math.cos(theta1) - ((math.sin(theta1)/math.sin(theta2)) * math.cos(theta2))

    
    st.markdown("""
    #### Deixando em termos de $T_1$ para obter $T_2$:
    """)
    st.latex(r"""
    T_2 = \frac{T_1 \sin(10^\circ)}{\sin(80^\circ)}
    """)
    st.latex(r"""
    T_1 \cos(10^\circ) - \frac{T_1 \sin(10^\circ)}{\sin(80^\circ)} \cos(80^\circ) = 3150
    """)
    st.latex(fr"""T_1 ({math.cos(theta1):.4f}-{(math.sin(theta1)/math.sin(theta2))*math.cos(theta2):.4f}) = 3150 
    """)
    st.latex(fr"""T_1 = \frac{{3150}}{{{sum_T2f:.4f}}} \approx {{{abs(T2):.4f}}}
    """
    )
    st.markdown("#### Calculando valor de $T_2$:")
    st.latex(r"""
    T_1 \sin(10^\circ) = T_2 \sin(80^\circ)
    """)
    st.latex(r"""
    T_2 = \frac{T_1 \sin(10^\circ)}{\sin(80^\circ)} = """fr"""
        \frac{{{T2:.2f} \times {math.sin(theta1):.4f}}}{{{math.sin(theta2):.4f}}} \approx {{{abs(T1):.2f}}}
    """)
    st.success(r"##### Resultados: $T_2 \approx$ "f"{abs(T1):.2f}"r" N ; $T_1 \approx$  "f"{T2:.2f} N")

    # Vetores para plotagem
    T1_vec = np.array([-(T1*math.cos(theta1)), T1*math.sin(theta1)])
    T2_vec = np.array([-(T2*math.cos(theta2)), T2*math.sin(theta2)])
    W_vec  = np.array([0.0, -W])

    fig = figure_vectors(
        [(T1_vec, "T₂", "C0"), (T2_vec, "T₁", "C2"), (W_vec, "W", "C3")],
        title="Diagrama — Exercicio 3 C"
    )
    st.pyplot(fig, use_container_width=True)


def ex4_4_practice():
    F_A = 220
    F_C = 170
    st.markdown(f"""<div class="enunciado-container">
                <h2>Exercício 4 — Cabo de guerra bidimensional (Crossfit)</h2>
                <p>Três pessoas praticam um "cabo de guerra" bidimensional 
                em torno de um pneu. Ana Clara exerce uma 
                <br>
                força <b>F_A = {F_A} N</b> a um ângulo de <b>137°</b>. 
                Camila exerce uma força <b>F_C = {F_C} N</b>, 
                com um ângulo φ 
                <br>
                desconhecido. Uma terceira pessoa exerce uma força 
                <b>F_B</b>, vertical para baixo. Determine o ângulo φ 
                <br>da força de Camila e o módulo da força de F_B para que o pneu permaneça em 
                equilíbrio.</p></div>""",unsafe_allow_html=True)
    
    st.markdown(r"""
    Como Brenda exerce uma força direcionada 0$^\circ$/ 90$^\circ$ S, o ângulo entre Ana Clara se divide em 90$^\circ$ e 47$^\circ$. \
    **Passo 1:** Decompor a Força de Ana Clara ($F_A$): \
    Use a trigonometria para encontrar as componentes horizontal ($F_Ax$) \
    e vertical ($F_Ay$) de $F_A$. \
    Componente x: 
    - $F_Ax$=$F_A \cos(43^\circ)$ 
    - $F_Ax =220 . \cos(43^\circ) \approx 220 . (−\,0,73135) \approx −\,160,90$ N \
    Componente y: 
    - $F_Ay$=$F_A \sin(43^\circ)$ 
    - $F_Ay =220 . \sin(43^\circ) \approx 220 . (0,68199) \approx 150,04$ N \
    **Passo 2:** Encontrar o Ângulo de Camila ($\phi$) \
    Use a condição de equilíbrio no eixo horizontal ($\sum F_x = 0$). \
    A soma das componentes horizontais deve ser zero.
    - $F_Ax + F_C \cos(\phi)= 0$ 
    - $−\,160,90 + 170 \cos(\phi)=0$ 
    - $170 \cos(\phi) = 160,90$ 
    - $\cos( \phi)= \frac {160,90}{170} \approx 0,94647$ \
    Para encontrar o ângulo $\phi$, use a função arco-cosseno ($\arccos$): 
    - $\phi = \arccos (0,94647) \approx 18,83^\circ$
    **Passo 3:** Encontrar o Módulo da Força de Brenda ($F_B$) \
    Use a condição de equilíbrio no eixo vertical ($\sum F_y = 0$). 
    A soma das componentes verticais deve ser zero. Lembre-se que $F_B$ \
    é negativa, pois aponta para baixo.
    - $F_Ay + F_C \sin(\phi) - F_B = 0$ 
    - $150,04 + 170 \sin(18,83^\circ) - F_B = 0$ 
    - $F_B = 150,04 + 170 \sin(18,83^\circ)$
    - $F_B \approx 150,04 + 170 ⋅ (0,3227)$
    - $F_B \approx 150,04+54,86$
    - $F_B \approx 204,90$ N
    """)
    
    thetaA = rad(137.0)
    FAx = F_A*math.cos(thetaA)   # negativo
    FAy = F_A*math.sin(thetaA)   # positivo
    cosphi = -FAx/F_C
    # Proteção numérica (limitar ao domínio de arccos)
    cosphi = max(-1.0, min(1.0, cosphi))
    phi = math.acos(cosphi)  # em rad
    #phi_deg = deg(phi)
    # Somatório em y: FAy + FC sinφ - FB = 0  -> FB = FAy + FC sinφ
    FB_mod = FAy + F_C*math.sin(phi)
    # Diagramas
    FA_vec = np.array([FAx, FAy])
    FC_vec = np.array([F_C*math.cos(phi), F_C*math.sin(phi)])
    FB_vec = np.array([0.0, -FB_mod])
    fig = figure_vectors([(FA_vec, "F_A", "C0"), (FC_vec, "F_C", "C2"), (FB_vec, "F_B", "C3")],
                        title="Equilíbrio no pneu (Ex. 4)")
    st.pyplot(fig, use_container_width=True)

    st.caption("Nota: Como a orientação de F_C não é dada explicitamente no texto, aqui ela é **deduzida** do equilíbrio (mantendo os módulos de F_A e F_C).")

#=============================================================================
def week4_practice():    
    st.sidebar.subheader("Semana 4 - Prática")
    op = st.sidebar.selectbox("Exercícios", ["Selecione","2", "3", "4", "5"])
    if op == "2":
        ex4_2_practice()
    elif op == "3":
        ex4_3_practice()
    elif op == "4":
        ex4_4_practice()
    elif op == "5":
        # A teeoria e a prática são idênticas pois foram aceitas
        ex4_5_theory()
    else:
        st.write("Aguardando escolha.....")

def week4_theory():  
    st.sidebar.subheader("Semana 4 - teoria")  
    op = st.sidebar.selectbox("Exercícios", ["Selecione","2", "3", "4", "5"])
    if op == "2":
        ex4_2_theory()
    elif op == "3":
        ex4_3_theory()
    elif op == "4":
        ex4_4_theory()
    elif op == "5":
        ex4_5_theory()
    else:
        st.write("Aguardando escolha.....")
def practice_4_theory():
    op = st.sidebar.selectbox("Estudo e Prática", ["Selecione","Teoria", "Prática"])
    if op == "Teoria":
        week4_theory()
    elif op == "Prática":
        week4_practice()
    else:
        st.header("Seja Bem-vindo")
        st.markdown("""
        Programa desenvolvida durante 2º semestre de 2025
        
        para a materia de Fisica Mecânica

        na Graduação em Engenharia da Computação pela 
        
        PUC Minas Coração Eucarístico

        **Autora:** Professora Kelly
        
        **Desenvolvido por:** Gabriel da Silva Cassino
        
        **Motivação:** Tornar fácil o acesso ao conteúdo, mesmo sem um computador
        permitindo revisar conceitos de forma prática, seja por leitura dos conceitos, ou execução das atividades práticas implementadas
        
        **Tecnologia em  uso:** A aplicação foi feita completamente em Python fazendo 
        uso do framework Streamlit, que grava as imagens em um arquivo JSON e 
        também carrega as imagens a partir do mesmo.
        
        **Versão** 1-28-08-2025
        
        """)


#==============================================================================
#                     Semana 4 - Laboratorio de Física Mecânica
#==============================================================================

# ------------------------------------------------------------
# JSON: textos-base, dados e observações
# ------------------------------------------------------------
TEXTOS: Dict[str, Any] = {
    "thread_1": {
        "titulo": "Exercício – Construção de Gráfico e Regressão Linear",
        "intro": (
            "Construa o gráfico **Peso (N)** em função da **Massa (kg)** e estime a gravidade **g** "
            "via regressão linear. Apresente a incerteza (erro-padrão) do coeficiente angular."
        ),
        "observacoes": [
            "Converta massas informadas em gramas (g) para quilogramas (kg): m_kg = m_g / 1000.",
            "O ajuste deve ser P = g * m + b. Idealmente b≈0; valores pequenos de b podem refletir erro sistemático.",
            "Use a incerteza do coeficiente angular (erro-padrão) como estimativa de incerteza de g.",
            "Propague e discuta unidades: g em N/kg (= m/s²)."
        ],
        # Dados-base do enunciado (m em g; P em N)
        "dados": {
            "m_g": [100, 132, 184, 205, 271],
            "P_N": [0.954, 1.302, 1.608, 2.018, 2.704]
        },
        "colunas": {"massa_g": "Massa (g)", "massa_kg": "Massa (kg)", "peso_N": "Peso (N)"}
    },
    "thread_2": {
        "titulo": "Aula Envio – Trajetos Manual e Sensores",
        "intro": (
            "Dados de posição (mm) e tempo (s) para dois conjuntos: **Manual** e **Sensores**. "
            "É possível analisar como **posição varia com o tempo** (x(t)) ou como **tempo varia com a posição** (t(x)). "
            "No ajuste linear, o coeficiente angular representa velocidade (quando x=f(t)) ou 1/velocidade (quando t=f(x))."
        ),
        "observacoes": [
            "Para x=f(t): x = S0 + V·t → slope = V (mm/s), intercepto S0 (mm).",
            "Para t=f(x): t = t0 + (1/V)·x → slope = 1/V (s/mm), de onde V = 1/slope (mm/s).",
            "Compare os ajustes de **Manual** e **Sensores** e discuta linearidade e resíduos.",
            "Se a inclinação (velocidade) cresce com o tempo, a aceleração não é nula – verifique via ajuste por janelas ou comparação de segmentos."
        ],
        # Pares (posição_mm, tempo_s) — extraídos do PDF (vírgula decimal convertida)
        "manual": {
            "pos_mm":  [0, 50, 100, 150, 200, 250, 300, 350, 400],
            "tempo_s": [0.00000, 0.84810, 1.72415, 2.59935, 3.55420, 4.41590, 5.25940, 6.18030, 7.02990]
        },
        "sensores": {
            "pos_mm":  [0, 50, 100, 150, 200, 250, 300, 350, 400],
            "tempo_s": [0.00000, 0.18890, 0.36335, 0.41335, 0.50440, 0.57160, 0.60565, 0.67855, 0.80030]
        },
        # Observações originais do PDF (como referências para discussão em aula)
        "anotacoes_pdf": {
            "manual": [
                "A medida será a cada 50 mm resultando em 8 intervalos.",
                "Regressão linear mostrada no relatório (sugere modelo t(x) ou x(t)).",
                "Resultados exemplares citam intercepto ≈1,22 e slope ≈56,60 (unidades no PDF estão confusas)."
            ],
            "sensores": [
                "A inclinação tangente ao gráfico representa a velocidade instantânea da esfera.",
                "A inclinação aumenta com o tempo mostrando que a velocidade cresce.",
                "Portanto a aceleração é diferente de zero."
            ]
        }
    }
}

# ------------------------------------------------------------
# Utilitários: regressão linear + incertezas
# ------------------------------------------------------------
def regressao_linear(x: np.ndarray, y: np.ndarray) -> Dict[str, float]:
    """
    Ajuste y = a*x + b. Retorna coeficientes, erro-padrão, R^2 e resíduos.
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    n = len(x)
    A = np.vstack([x, np.ones(n)]).T
    # coeficientes via mínimos quadrados
    a, b = np.linalg.lstsq(A, y, rcond=None)[0]
    # resíduos e métricas
    y_pred = a * x + b
    resid = y - y_pred
    sse = np.sum(resid**2)
    sst = np.sum((y - np.mean(y))**2)
    r2 = 1 - sse/sst if sst > 0 else 1.0
    # erro-padrão do slope e intercepto
    sigma2 = sse / (n - 2) if n > 2 else np.nan
    sx2 = np.sum((x - np.mean(x))**2)
    se_a = math.sqrt(sigma2 / sx2) if sx2 > 0 and np.isfinite(sigma2) else np.nan
    se_b = math.sqrt(sigma2 * (1/n + (np.mean(x)**2)/sx2)) if sx2 > 0 and np.isfinite(sigma2) else np.nan
    return {
        "a": a, "b": b,
        "se_a": se_a, "se_b": se_b,
        "r2": r2,
        "sse": sse,
        "n": n
    }

def plot_scatter_fit(x, y, xlabel, ylabel, titulo):
    fig, ax = plt.subplots()
    ax.scatter(x, y)
    # linha de melhor ajuste
    a, b = np.polyfit(x, y, 1)
    x_line = np.linspace(min(x), max(x), 200)
    y_line = a * x_line + b
    ax.plot(x_line, y_line)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(titulo)
    st.pyplot(fig)

# ------------------------------------------------------------
# Thread 1 – Regressão para estimar g
# ------------------------------------------------------------
def thread_1():
    meta = TEXTOS["thread_1"]
    st.header(meta["titulo"])
    st.write(meta["intro"])

    # Dados-base
    m_g = meta["dados"]["m_g"]
    P_N = meta["dados"]["P_N"]

    # DataFrame
    df = pd.DataFrame({
        meta["colunas"]["massa_g"]: m_g,
        meta["colunas"]["peso_N"]: P_N
    })
    df[meta["colunas"]["massa_kg"]] = df[meta["colunas"]["massa_g"]] / 1000.0
    df = df[[meta["colunas"]["massa_g"], meta["colunas"]["massa_kg"], meta["colunas"]["peso_N"]]]

    st.subheader("Tabela de dados")
    st.dataframe(df, use_container_width=True)

    # Regressão: P = g*m + b (usar massa em kg)
    x = df[meta["colunas"]["massa_kg"]].to_numpy()
    y = df[meta["colunas"]["peso_N"]].to_numpy()
    res = regressao_linear(x, y)

    g = res["a"]
    g_se = res["se_a"]
    b = res["b"]
    b_se = res["se_b"]

    col1, col2 = st.columns(2)
    with col1:
        plot_scatter_fit(
            x, y,
            xlabel="Massa (kg)",
            ylabel="Peso (N)",
            titulo="Peso × Massa – Ajuste Linear"
        )
    with col2:
        st.markdown("### Resultados do ajuste")
        st.write(f"- **g (coef. angular)** = {g:.4f} ± {g_se:.4f} N/kg  (≈ m/s²)")
        st.write(f"- **Intercepto (b)** = {b:.4f} ± {b_se:.4f} N")
        st.write(f"- **R²** = {res['r2']:.4f}")
        st.caption(
            "O ideal é b≈0; desvios podem indicar erros sistemáticos (ex.: tara do dinamômetro, "
            "atrito, leitura inicial não nula)."
        )

    with st.expander("Observações & considerações didáticas"):
        for obs in meta["observacoes"]:
            st.markdown(f"- {obs}")

# ------------------------------------------------------------
# Thread 2 – Aula Envio (Manual e Sensores)
# ------------------------------------------------------------
def _make_df_trilha(pos_mm: List[float], tempo_s: List[float]) -> pd.DataFrame:
    df = pd.DataFrame({"Posição (mm)": pos_mm, "Tempo (s)": tempo_s})
    # Conversões auxiliares
    df["Posição (m)"] = df["Posição (mm)"] / 1000.0
    return df

def _ajustes_basicos(df: pd.DataFrame, modo: str):
    """
    modo: 'x(t)'  -> x = a*t + b   (velocidade = a [mm/s])
          't(x)'  -> t = a*x + b   (1/velocidade = a [s/mm], velocidade = 1/a [mm/s])
    """
    if modo == "x(t)":
        x = df["Tempo (s)"].to_numpy()
        y = df["Posição (mm)"].to_numpy()
        res = regressao_linear(x, y)
        V = res["a"]
        V_se = res["se_a"]
        return res, ("Tempo (s)", "Posição (mm)"), f"Velocidade (slope) ≈ {V:.3f} ± {V_se:.3f} mm/s"
    else:
        x = df["Posição (mm)"].to_numpy()
        y = df["Tempo (s)"].to_numpy()
        res = regressao_linear(x, y)
        invV = res["a"]
        invV_se = res["se_a"]
        V = 1.0/invV if invV != 0 else np.nan
        # Propagação simples de incerteza de V = 1/a: sV ≈ s_a / a^2
        V_se = invV_se / (invV**2) if invV not in (0, np.nan) and np.isfinite(invV) and np.isfinite(invV_se) else np.nan
        return res, ("Posição (mm)", "Tempo (s)"), f"Velocidade ≈ {V:.3f} ± {V_se:.3f} mm/s (derivada de t=f(x))"

def _plotar(df: pd.DataFrame, eixo_x: str, eixo_y: str, titulo: str):
    fig, ax = plt.subplots()
    ax.scatter(df[eixo_x], df[eixo_y])
    a, b = np.polyfit(df[eixo_x], df[eixo_y], 1)
    x_line = np.linspace(df[eixo_x].min(), df[eixo_x].max(), 200)
    y_line = a * x_line + b
    ax.plot(x_line, y_line)
    ax.set_xlabel(eixo_x)
    ax.set_ylabel(eixo_y)
    ax.set_title(titulo)
    st.pyplot(fig)

def _analise_segmentada(df: pd.DataFrame) -> Tuple[float, float]:
    """
    Ajusta x=f(t) em duas metades para verificar possível aumento de velocidade.
    Retorna (V1, V2) em mm/s.
    """
    mid = len(df)//2
    df1 = df.iloc[:mid]
    df2 = df.iloc[mid:]
    # x = a*t + b em cada segmento
    r1 = regressao_linear(df1["Tempo (s)"].to_numpy(), df1["Posição (mm)"].to_numpy())
    r2 = regressao_linear(df2["Tempo (s)"].to_numpy(), df2["Posição (mm)"].to_numpy())
    return r1["a"], r2["a"]

def thread_2():
    meta = TEXTOS["thread_2"]
    st.header(meta["titulo"])
    st.write(meta["intro"])

    # Dados-base
    df_manual = _make_df_trilha(meta["manual"]["pos_mm"], meta["manual"]["tempo_s"])
    df_sens = _make_df_trilha(meta["sensores"]["pos_mm"], meta["sensores"]["tempo_s"])

    tab1, tab2 = st.tabs(["Manual", "Sensores"])
    for nome, df, anot in [("Manual", df_manual, meta["anotacoes_pdf"]["manual"]),
                           ("Sensores", df_sens, meta["anotacoes_pdf"]["sensores"])]:
        with (tab1 if nome=="Manual" else tab2):
            st.subheader(f"Conjunto: {nome}")
            st.dataframe(df, use_container_width=True)

            # Seletor de modelo
            modo = st.radio(
                f"Escolha o modelo para {nome}",
                options=["x(t) – posição em função do tempo", "t(x) – tempo em função da posição"],
                horizontal=True,
                key=f"modelo_{nome}"
            )
            modo_curto = "x(t)" if modo.startswith("x(t)") else "t(x)"
            res, (xlabel, ylabel), resumoV = _ajustes_basicos(df, modo_curto)

            col1, col2 = st.columns(2)
            with col1:
                _plotar(df, xlabel, ylabel, f"{nome}: {ylabel} × {xlabel}")
            with col2:
                st.markdown("### Ajuste linear")
                st.write(f"- **Slope (a)** = {res['a']:.6f} ± {res['se_a']:.6f}")
                st.write(f"- **Intercepto (b)** = {res['b']:.6f} ± {res['se_b']:.6f}")
                st.write(f"- **R²** = {res['r2']:.4f}")
                st.write(f"- {resumoV}")

            # Checagem simples de aceleração via análise segmentada (x=f(t))
            V1, V2 = _analise_segmentada(df)
            with st.expander("Aceleração (diagnóstico simples)"):
                st.write(
                    "Comparamos a velocidade estimada (slope em x=f(t)) na primeira metade vs. segunda metade da série."
                )
                st.write(f"- **V (1ª metade)** ≈ {V1:.3f} mm/s")
                st.write(f"- **V (2ª metade)** ≈ {V2:.3f} mm/s")
                if np.isfinite(V1) and np.isfinite(V2):
                    if V2 > V1:
                        st.success("A velocidade aumentou — indício de aceleração positiva.")
                    elif V2 < V1:
                        st.warning("A velocidade diminuiu — indício de aceleração negativa (ou atrito).")
                    else:
                        st.info("Velocidade aproximadamente constante dentro da incerteza.")
                st.caption("Este teste é apenas indicativo; um ajuste quadrático x(t)=S0+V0 t + ½ a t² seria mais apropriado para quantificar a aceleração.")

            with st.expander("Observações & notas do relatório"):
                for a in anot:
                    st.markdown(f"- {a}")
            with st.expander("Considerações didáticas"):
                for obs in meta["observacoes"]:
                    st.markdown(f"- {obs}")

# ------------------------------------------------------------
# Seletor principal (lab_threads) Laboratório 
# ------------------------------------------------------------
def lab_threads():
    st.title("Laboratório de Física – Threads de Análise")
    escolha = st.selectbox(
        "Selecione a thread:",
        options=[
            "Exercício – Construção de Gráfico e Regressão Linear (thread_1)",
            "Aula Envio – Trajetos Manual e Sensores (thread_2)"
        ],
        index=0
    )
    if escolha.startswith("Exercício"):
        thread_1()
    else:
        thread_2()


    

def week_4_lab_theory():
    st.write("Em desenvolvimento")

def practice_4_lab():
    op = st.sidebar.selectbox("Estudo e Prática", ["Selecione","Teoria","Exercicio"])
    if op == "Teoria":
        week_4_lab_theory()
    elif op =="Exercicio":
        lab_threads()
    else:
        st.header("Seja Bem-vindo")
        st.markdown("""
        Programa desenvolvida durante 2º semestre de 2025
        
        para a materia Laboratório de Fisica Mecânica

        na Graduação em Engenharia da Computação pela 
        
        PUC Minas Coração Eucarístico

        **Autora:** Professora Joice
        
        **Desenvolvido por:** Gabriel da Silva Cassino
        
        **Motivação:** Tornar fácil o acesso ao conteúdo, mesmo sem um computador
        permitindo revisar conceitos de forma prática, seja por leitura dos conceitos, ou execução das atividades práticas implementadas
        
        **Tecnologia em  uso:** A aplicação foi feita completamente em Python fazendo 
        uso do framework Streamlit, que grava as imagens em um arquivo JSON e 
        também carrega as imagens a partir do mesmo.
        
        **Versão** 1-28-08-2025""")

#==============================================================================
def main():
    exercises =st.sidebar.selectbox("Materia",["Teorica","Laboratorio"])
    if exercises == "Teorica":
         practice_4_theory()     
    elif exercises == "Laboratorio":
        practice_4_lab()
if __name__ == "__main__":
    main()
