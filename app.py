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
    .card {
        background-color: white;
        border-radius: 16px;
        padding: 30px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        margin-top: 30px;
        text-align: center;
    }
    .card h2 {
        font-size: 26px;
        margin-bottom: 10px;
        color: #333;
    }
    .card .valor-destaque {
        font-size: 42px;
        font-weight: 800;
        color: #007bff;
        margin-top: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🔢 Simulador de Cálculo")
st.markdown("Insira os valores abaixo para gerar o cálculo:")

# Inputs
credito = st.number_input("Crédito",step=10000.0, format="%.2f")
recurso_proprio = st.number_input("Recurso Próprio",step=10000.0, format="%.2f")
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
    qtd_parcelas_restante = int(prazo - 1 -(lance / parcela_seguro))
    # Aqui você pode adicionar seus cálculos com base nos inputs

    valor_formatado = f"R$ {credito_final:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    parcela_formatado = f"R$ {parcela_seguro:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    st.markdown(
    f"""
        <div class="card">
            <h3>Crédito a receber</h3>
            <div class="valor-destaque">{valor_formatado}</div>
            <h3>Valor da parcela</h3>
            <div class="valor-destaque">{parcela_formatado}</div>
            <h3>Parcelas Restantes</h3>
            <div class="valor-destaque">{qtd_parcelas_restante}</div>
        </div>
    """,
    unsafe_allow_html=True
    )

