import streamlit as st
import requests
import streamlit.components.v1 as components
import pandas as pd
import json
import datetime
from datetime import date,datetime
import pickle
import re

from data import preenche_formulario


opcoes = {
      "Vouga": "101204609",
      "CDA": "101204610",
      "Sanauto": "101185528",
      "Jangada Renault": "101204604",
      "Nissan MT": "101204600",
      "Nissan WS": "101204608",
      "BYD Carmais": "101204605",
      "Honda BS": "101204612",
      "Honda WS": "101204684",
      "Honda SD": "101204686",
      "Honda SUL": "101204687",
      "NOSSAMOTO - HONDA": "101204688",
      "BYD Teresina": "101212127",
      "BYD Natal": "101212126",
      "GWM SLZ": "101212128",
      "NOSSAMOTO BATURITE": "101247207",
      "NOSSAMOTO CONJUNTO CEARA": "101247174",
      "NOSSAMOTO SIQUEIRA": "101247183",
      "GEELY": "101258510"     
}

empresas = list(opcoes.keys())

st.subheader("FORMULÁRIO VDI",divider="gray")

if "mostrar_form" not in st.session_state:
    st.session_state.mostrar_form = False

if st.button("Abrir Formulário"):
    st.session_state.mostrar_form = True

if st.session_state.mostrar_form:

    if st.button("Fechar Formulário"):
            st.session_state.mostrar_form = False


    with st.form("meu_form"):

        

        empresa = st.selectbox(
                                "Empresa",
                                empresas
                            )

        emp_selecionada = opcoes[empresa]

        placa = st.text_input("Placa do VU:")

        valor_venda = st.number_input(
                                        "Digite o valor da venda",
                                        min_value=0.0,
                                        step=100.0,
                                        format="%.2f"
                                        )
        
        margem = st.number_input(
                                "Digite o valor a margem liquida final",
                                min_value=0.0,
                                step=100.0,
                                format="%.2f"
                                )
        
        expectativa_cliente = st.number_input(
                                "Expectativa do Cliente da venda VU",
                                min_value=0.0,
                                step=100.0,
                                format="%.2f"
                                )

        top = st.selectbox(
                            "Tem Top?",
                            ["N", "S"],
                            format_func=lambda x: "Sim" if x == "S" else "Não"
    )

        bonus = st.selectbox(
                            "Tem Bonus Agregado do Fabricante?",
                            ["N", "S"],
                            format_func=lambda x: "Sim" if x == "S" else "Não"
                        )


        valor_bonus = st.number_input(
                                "Valor do Bonus",
                                min_value=0.0,
                                step=100.0,
                                format="%.2f"
                                )
        numero_carta = st.text_input("Digite o numero da carte:")
        condicionante = st.text_input("Digite a condicionante do bonus:")
        validade_bonus = st.date_input("Validade do Bonus")
        dt_bonus_formatada = validade_bonus.strftime("%d/%m/%Y")

        # VENDAS ESTOQUE VN
        emplacamento = st.selectbox(
                            "Tem Serviço de Emplacamento Interno?",
                            ["N", "S"],
                            format_func=lambda x: "Sim" if x == "S" else "Não"
                        )
        
        cliente_paga_emplacamento = st.selectbox(
                            "Cliente Paga?",
                            ["N", "S"],
                            format_func=lambda x: "Sim" if x == "S" else "Não"
                        )
        
        emplacamento_desconto = st.selectbox(
                            "Tem desconto no serviço de emplacamento?",
                            ["N", "S"],
                            format_func=lambda x: "Sim" if x == "S" else "Não"
                        )

        financiamento = st.selectbox(
                            "Tem Financiamento?",
                            ["N", "S"],
                            format_func=lambda x: "Sim" if x == "S" else "Não"
                        )


        valor_financiamento = st.text_input("Digite o valor do Financiamento:")
        
        plus_bancario = st.selectbox(
                            "Tem Plus Bancario?",
                            ["N", "S"],
                            format_func=lambda x: "Sim" if x == "S" else "Não"
                        )


        valor_plus_bancario = st.text_input("Digite o valor do Plus Bancario:")

        acessorios = st.selectbox(
                            "Tem Acessorio?",
                            ["N", "S"],
                            format_func=lambda x: "Sim" if x == "S" else "Não"
                        )

        entrega_vu = st.selectbox(
                            "O cliente vai entregar o carro imediato?",
                            ["N", "S"],
                            format_func=lambda x: "Sim" if x == "S" else "Não"
                        )
        
        previsa_entrega = data_inicio = st.date_input("Previsão de entrega do VU")
        previsao_entrega_formatada = previsa_entrega.strftime("%d/%m/%Y")
        
        submitted = st.form_submit_button("Salvar")

        if submitted:

            if not placa or placa.strip() == "":
                st.error("O campo Placa é obrigatório.")
            else:

                def to_float(valor):
                        if valor in (None, "", " "):
                            return 0
                        return float(valor)
                payload = {
                    "empresa": emp_selecionada.strip(),
                    "placa": placa.upper().replace("-", "").strip(),  # maiúsculo e sem hífen

                    "valor_venda": to_float(valor_venda),
                    "margem": to_float(margem),
                    "expectativa_cliente": to_float(expectativa_cliente),

                    "top_tp": top,
                    "bonus": bonus,
                    "valor_bonus": to_float(valor_bonus),

                    "numero_carta": numero_carta.strip() if numero_carta else None,
                    "condicionante": condicionante.strip() if condicionante else None,

                    # Flask/pymssql aceitam bem string ISO
                    "dt_bonus_formatada": validade_bonus.strftime("%Y-%m-%d 00:00:00"),

                    "emplacamento": emplacamento,
                    "cliente_paga_emplacamento": cliente_paga_emplacamento,
                    "emplacamento_desconto": emplacamento_desconto,

                    "financiamento": financiamento,
                    "valor_financiamento": to_float(valor_financiamento),

                    "plus_bancario": plus_bancario,
                    "valor_plus_bancario": to_float(valor_plus_bancario),

                    "acessorios": acessorios,
                    "entrega_vu": entrega_vu,

                    "previsao_entrega_formatada": previsa_entrega.strftime("%Y-%m-%d 00:00:00")
                }

                resultado = preenche_formulario(payload)

                if resultado["error"]:
                    st.error(f"Erro de conexão: {resultado['error']}")

                elif resultado["status_code"] == 201:
                    mensagem = resultado["data"].get("message", "Registro inserido com sucesso")
                    st.success(mensagem)

                else:
                    st.error(f"Erro ao inserir: {resultado['data']}")

       