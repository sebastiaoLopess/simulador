import streamlit as st
import requests
import streamlit.components.v1 as components
import pandas as pd
import json
from components import input 
from data import consulta_auto_avaliar,trata_estoque,ano_garantia,tem_garantia,resposta,trata_data,consulta_revisao,consulta_vendas_simulador,consulta_estoque_vu,consulta_negociacao
from paginas import dados_da_avaliacao,referencias_garantia, referencias, itens_avaliados,simulador_vu,simulador_repasse,estoque_vu,simulador_vn,estoque_vn,preenchimento_usuario,analise_financeira,dados_negociacao


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

classificacao = {
      int(1): "A",
      int(2): "B",
      int(3): "C",
      int(4): "D",
      int(5): "E"
}

cod_auth = [
            7582,
            4218,
            7735,
            6045,
            1079,
            5139,
            9099,
            4529,
            1707,
            6577,
            1631,
            8063,
            9456,
            7687,
            2274,
            6882,
            3604,
            6334,
            2094,
            5031,
            5516,
            7343,
            3059,
            9369,
            8184,
            4197,
            3578,
            5711,
            1350,
            1292,
            9595,
            1982,
            2204,
            7962,
            6111,
            6010,
            6498,
            7898,
            9713,
            8431,
            4927,
            6382,
            4621,
            7891,
            9149,
            6149,
            5381,
            9478,
            3341,
            7184,
            5145,
            2074,
            6556,
            1696,
            3616,
            3105,
            5541,
            5418,
            5938,
            1484,
            6732,
            2254,
            8784,
            4309,
            1240,
            9433,
            5722,
            4312,
            2268,
            8162,
            4070,
            6001,
            3698,
            1786,
            1151
            ]

empresas = list(opcoes.keys())

st.link_button("Abrir Formulario", "https://formcarmais.streamlit.app/")

st.header("VDI CARMAIS", divider="gray")
col1, col2 = st.columns(2)
with col1:
    placa = st.text_input("Placa")
with col2:
    autenticator = st.text_input("Autenticador",type="password")

empresa = st.selectbox(
    "Empresa",
    empresas
)

emp_selecionada = opcoes[empresa]



button = st.button("Gerar TCO", type="primary")

if button and autenticator in str(cod_auth) and autenticator:

    avaliacao = consulta_auto_avaliar(placa,emp_selecionada)
    negociacao = consulta_negociacao(placa,emp_selecionada)
    modelo_avaliado = avaliacao['vehicle']['model']['name']
    modelo_interesse = avaliacao['interested_vehicle_details']['model']['name']

    venda = consulta_vendas_simulador(modelo_avaliado)
    venda_interesse = consulta_vendas_simulador(modelo_interesse)
    df_estoque = consulta_estoque_vu(modelo_avaliado)
    df_estoque_interesse = consulta_estoque_vu(modelo_interesse)

    st.subheader("DADOS DA NEGOCIAÇÃO",divider="gray")

    dados_negociacao(negociacao)


    st.subheader("DADOS DO VEICULO DE INTERESSE",divider="gray")
    simulador_vn(venda_interesse,modelo_interesse)
    estoque_vn(df_estoque_interesse)


    st.subheader("DADOS DO VU AVALIADO",divider="gray")

    st.markdown(input("Modelo Avaliado",modelo_avaliado),unsafe_allow_html=True)
    col5, col6 = st.columns(2)
    with col5:
        #st.subheader("DADOS DA VENDA DO VU REPASSE",divider="gray")
        st.markdown("###### DADOS SHOWROOM")
        
        simulador_vu(venda)
    with col6:

        #st.subheader("DADOS DA VENDA REPASSE",divider="gray")
        st.markdown("###### DADOS REPASSE")
        simulador_repasse(venda)

    col3, col4 = st.columns(2)
    with col3:
        st.subheader("DADOS DA AVALIAÇÃO",divider="gray")

        dados_da_avaliacao(avaliacao,classificacao)
    with col4:

        st.subheader("DADOS DE GARANTIA",divider="gray")

        referencias_garantia(avaliacao,classificacao)

    st.subheader("REFERÊNCIAS",divider="gray")

    referencias(avaliacao,classificacao)

    st.subheader("ITENS AVALIADOS",divider="gray")

    itens_avaliados(avaliacao)

    st.subheader("ANALISE ECONOMICA DO RISCO",divider="gray")

    st.write("As previsões abaixo tem como premissa de custo a expectatica do cliente")


    analise_financeira(avaliacao,negociacao)

    
  








