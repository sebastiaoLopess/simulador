import streamlit as st

# Configuração da página
st.set_page_config(page_title="Simulador de Cálculo", layout="centered")

# Estilo com cores azul e branco
st.markdown(
    """
    <style>
    body {
        background-color: #f0f8ff;
    }
    .stButton button {
        background-color: #007bff;
        color: white;
        border-radius: 8px;
        padding: 0.5em 2em;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🔢 Simulador de Cálculo")
st.markdown("Insira os valores abaixo para gerar o cálculo:")

# Inputs
credito = st.number_input("Crédito", min_value=0.0, step=100.0, format="%.2f")
recurso_proprio = st.number_input("Recurso Próprio", min_value=0.0, step=100.0, format="%.2f")
lance_embutido = st.selectbox("Lance Embutido (%)", list(range(1, 26)))
taxa_adm = st.number_input("Taxa Adm (%)", min_value=0.0, step=0.1, format="%.2f")
prazo = st.number_input("Prazo (meses)", min_value=1, step=1, format="%d")

total = credito + (credito * (taxa_adm/100))
seguro_total = total * (6.86112/100)
total_final = total + seguro_total
credito_final = credito - ((lance_embutido/100) * total_final)
parcela_seguro = total_final / prazo
parcela_sem_seguro = total / prazo
lance = total_final * (lance_embutido/100)

plano = st.selectbox("Plano", ["Plano Integral", "Plano Light"])

# Botão
if st.button("Gerar"):
    # Aqui você pode adicionar seus cálculos com base nos inputs
    st.success(f"Cálculos gerados com sucesso! {credito_final}")
    # Exemplo:
    st.write("🧮 Você pode exibir os resultados dos cálculos aqui.")