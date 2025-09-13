import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import re

st.set_page_config(page_title="Punto de Equilibrio", layout="centered")

st.title("📊 Calculadora de Punto de Equilibrio entre Dos Ecuaciones")

st.markdown("""
Ingresa dos ecuaciones lineales en formato `y = ax + b`, por ejemplo:
- `y = 2x + 3`
- `y = -x + 5`
""")

# Función para parsear una ecuación en forma 'y = ax + b'
def parse_ecuacion(equacion):
    try:
        # Usamos regex para obtener coeficiente y término independiente
        pattern = r"y\s*=\s*([+-]?\s*\d*\.?\d*)x\s*([+-]\s*\d+\.?\d*)"
        match = re.match(pattern, ecuacion.replace(" ", ""))
        if not match:
            return None
        a = float(match.group(1).replace(" ", "") or "1")
        b = float(match.group(2).replace(" ", ""))
        return a, b
    except:
        return None

# Entradas de usuario
with st.form("ecuaciones_form"):
    eq1 = st.text_input("Ecuación 1:", value="y = 2x + 3")
    eq2 = st.text_input("Ecuación 2:", value="y = -x + 5")
    submitted = st.form_submit_button("📥 Ingresar ecuaciones")

if submitted:
    coef1 = parse_ecuacion(eq1)
    coef2 = parse_ecuacion(eq2)

    if coef1 and coef2:
        st.success("✅ Ecuaciones ingresadas correctamente.")
        st.session_state['coef1'] = coef1
        st.session_state['coef2'] = coef2
    else:
        st.error("❌ Formato incorrecto. Usa el formato: y = ax + b")

# Botón para calcular el punto de equilibrio
if 'coef1' in st.session_state and 'coef2' in st.session_state:
    if st.button("🔍 Calcular punto de equilibrio"):
        a1, b1 = st.session_state['coef1']
        a2, b2 = st.session_state['coef2']

        if a1 == a2:
            st.warning("⚠️ Las rectas son paralelas, no hay punto de equilibrio.")
        else:
            # Resolver a1x + b1 = a2x + b2
            x_eq = (b2 - b1) / (a1 - a2)
            y_eq = a1 * x_eq + b1

            st.success(f"📍 Punto de equilibrio encontrado:  \n**x = {x_eq:.2f}, y = {y_eq:.2f}**")

            # Mostrar gráfica
            x_vals = np.linspace(x_eq - 10, x_eq + 10, 400)
            y1_vals = a1 * x_vals + b1
            y2_vals = a2 * x_vals + b2

            fig, ax = plt.subplots()
            ax.plot(x_vals, y1_vals, label=eq1, color="blue")
            ax.plot(x_vals, y2_vals, label=eq2, color="green")
            ax.plot(x_eq, y_eq, 'ro', label="Punto de equilibrio")
            ax.axhline(0, color='black', linewidth=0.5)
            ax.axvline(0, color='black', linewidth=0.5)
            ax.legend()
            ax.grid(True)
            st.pyplot(fig)
