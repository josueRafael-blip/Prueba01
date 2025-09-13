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

Un ejemplo ya viene cargado por defecto para que puedas probarlo fácilmente.
""")

# Función para parsear ecuación en formato 'y = ax + b'
def parse_ecuacion(equacion):
    try:
        # Regex para capturar 'a' y 'b'
        pattern = r"y\s*=\s*([+-]?\s*\d*\.?\d*)x\s*([+-]\s*\d+\.?\d*)"
        match = re.match(pattern, ecuacion.replace(" ", ""))
        if not match:
            return None
        a_str = match.group(1).replace(" ", "")
        b_str = match.group(2).replace(" ", "")
        a = float(a_str) if a_str not in ["", "+", "-"] else float(f"{a_str}1")
        b = float(b_str)
        return a, b
    except:
        return None

# Entradas del usuario con valores por defecto (ejemplo precargado)
eq1 = st.text_input("Ecuación 1:", value="y = 2x + 3")
eq2 = st.text_input("Ecuación 2:", value="y = -x + 5")

# Botón opcional para recalcular con nuevas ecuaciones
if st.button("🔍 Calcular punto de equilibrio"):
    st.session_state['eq1'] = eq1
    st.session_state['eq2'] = eq2

# Usar las ecuaciones actuales o las predeterminadas
ecuacion_1 = st.session_state.get('eq1', eq1)
ecuacion_2 = st.session_state.get('eq2', eq2)

coef1 = parse_ecuacion(ecuacion_1)
coef2 = parse_ecuacion(ecuacion_2)

if coef1 and coef2:
    a1, b1 = coef1
    a2, b2 = coef2

    if a1 == a2:
        st.warning("⚠️ Las rectas son paralelas. No hay punto de equilibrio.")
    else:
        # Calcular punto de equilibrio
        x_eq = (b2 - b1) / (a1 - a2)
        y_eq = a1 * x_eq + b1

        st.success(f"📍 Punto de equilibrio: **x = {x_eq:.2f}**, **y = {y_eq:.2f}**")

        # Graficar
        x_vals = np.linspace(x_eq - 10, x_eq + 10, 400)
        y1_vals = a1 * x_vals + b1
        y2_vals = a2 * x_vals + b2

        fig, ax = plt.subplots()
        ax.plot(x_vals, y1_vals, label=ecuacion_1, color="blue")
        ax.plot(x_vals, y2_vals, label=ecuacion_2, color="green")
        ax.plot(x_eq, y_eq, 'ro', label="Punto de equilibrio")
        ax.axhline(0, color='black', linewidth=0.5)
        ax.axvline(0, color='black', linewidth=0.5)
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)
else:
    st.error("❌ Formato incorrecto. Asegúrate de usar el formato: `y = ax + b`.")
