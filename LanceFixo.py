import streamlit as st

st.set_page_config(page_title="Simulador de Cálculo", layout="centered")

# Estilo visual
st.markdown("""
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
    .cards-container {
        display: flex;
        justify-content: center;
        gap: 40px;
        margin-top: 30px;
        flex-wrap: wrap;
    }
    .card {
        background-color: white;
        border-radius: 16px;
        padding: 30px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        text-align: center;
        width: 320px;
    }
    .card h2 {
        font-size: 20px;
        color: #333;
        margin-bottom: 10px;
    }
    .valor-destaque {
        font-size: 32px;
        font-weight: 800;
        color: #007bff;
        margin: 5px 0 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🔢 Lance Fixo")
st.markdown("Insira os valores abaixo para gerar o cálculo:")

# Inputs
valores_credito = {
    "R$ 40.000,00": 40000,
    "R$ 60.000,00": 60000,
    "R$ 65.000,00": 65000,
    "R$ 80.000,00": 80000,
    "R$ 85.000,00": 85000,
    "R$ 100.000,00": 100000
}

credito_selecionado = st.selectbox("Crédito", list(valores_credito.keys()))
credito = valores_credito[credito_selecionado]
recurso_proprio = st.number_input("Recurso Próprio", step=10000.0, format="%.2f")
lance_embutido = st.selectbox("Lance Embutido (%)", list(range(1, 26)))
taxa_adm = st.number_input("Taxa Adm (%)", min_value=0.0, step=0.1, format="%.2f")
prazo = st.number_input("Prazo (meses)", min_value=1, step=1, format="%d")

if st.button("Gerar"):

    def formatar(valor):
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    # Integral
    def calcular_integral(credito_base, taxa_adm, prazo, lance_pct):
        total = credito_base + (credito_base * (taxa_adm / 100))
        seguro = total * (6.86112 / 100)
        total_final = total + seguro
        print(total_final)
        credito_final = credito_base - ((lance_pct / 100) * total_final)
        parcela = total_final / prazo
        print(parcela)
        lance_valor = total_final * (lance_pct / 100)
        parcelas_restantes = int(prazo - 1 - (lance_valor / parcela))
        return {
            "credito_final": formatar(credito_final),
            "parcela": formatar(parcela),
            "restantes": parcelas_restantes
        }

    # Light
    def calcular_light(credito_base, prazo, lance_pct):
        total = (credito_base * 0.75) + (credito_base * (taxa_adm / 100))
        seguro = (credito_base + (credito_base * (taxa_adm / 100))) * (6.86112 / 100)
        total_final = total + seguro
        credito_final = credito_base - ((lance_pct / 100) * total_final)
        parcela = total_final / prazo
        sd_inicial = ((credito_base + (credito_base * (taxa_adm / 100))) + seguro) - (((credito_base + (credito_base * (taxa_adm / 100))) + seguro) / prazo)
        lance_valor = ((credito_base + (credito_base * (taxa_adm / 100))) + seguro) * (lance_pct / 100)
        sd_final = sd_inicial - lance_valor
        parcelas_restantes = int(prazo - 1 - int(lance_valor / parcela))
        parcela_final = sd_final / parcelas_restantes
        print(parcela_final)
        return {
            "credito_final": formatar(credito_final),
            "parcela": formatar(parcela_final),
            "restantes": parcelas_restantes
        }

    resultado_integral = calcular_integral(credito, taxa_adm, prazo, lance_embutido)
    resultado_light = calcular_light(credito, prazo, lance_embutido)

    st.markdown(
        f"""
        <div class="cards-container">
            <div class="card">
                <h2>Plano Integral</h2>
                <div class="valor-destaque">{resultado_integral['credito_final']}</div>
                <h2>Parcela</h2>
                <div class="valor-destaque">{resultado_integral['parcela']}</div>
                <h2>Parcelas Restantes</h2>
                <div class="valor-destaque">{resultado_integral['restantes']}</div>
            </div>
            <div class="card">
                <h2>Plano Light</h2>
                <div class="valor-destaque">{resultado_light['credito_final']}</div>
                <h2>Parcela</h2>
                <div class="valor-destaque">{resultado_light['parcela']}</div>
                <h2>Parcelas Restantes</h2>
                <div class="valor-destaque">{resultado_light['restantes']}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )