import streamlit as st
import requests
import streamlit.components.v1 as components
import pandas as pd
import json
from datetime import datetime
from components import input 
from data import consulta_auto_avaliar,trata_estoque,ano_garantia,tem_garantia,resposta,trata_data,referencias_media,referencias_min,referencias_max,trata_itens,define_placa,consulta_negociacao

def dados_da_avaliacao(avaliacao,classificacao):

    st.markdown(input("Data Avaliação",trata_data(avaliacao['valuation_date'])),unsafe_allow_html=True)
    st.markdown(input("Veiculo Avaliado",avaliacao['vehicle']['model']['name'] + " " + avaliacao['vehicle']['version']['name']),unsafe_allow_html=True)
    st.markdown(input("Veiculo de Interesse",value=avaliacao['interested_vehicle']),unsafe_allow_html=True)
    st.markdown(input("Família",value=avaliacao['vehicle']['model']['name']),unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(input("KM",value=avaliacao['vehicle']['mileage']),unsafe_allow_html=True)
    with col2:
        st.markdown(input("Ano Modelo",value=avaliacao['vehicle']['year']),unsafe_allow_html=True)


    col3, col4 = st.columns(2)
    with col3:
        st.markdown(input("Finalidade",value=avaliacao['goal_name']),unsafe_allow_html=True)
    with col4:
        st.markdown(input("Classificacao",value=classificacao[avaliacao['rating']]),unsafe_allow_html=True)
    col5, col6 = st.columns(2)
    with col5:
        st.markdown(input("Tipo de Avaliação",value=avaliacao['valuation_type_name']),unsafe_allow_html=True)
    with col6:
        st.markdown(input("Municipio Vec",value=avaliacao.get('vehicle', {}).get('city', '')),unsafe_allow_html=True)
    col7, col8 = st.columns(2)
    with col7:
        st.markdown(input("Avaliador",value=avaliacao['valuer']['name']),unsafe_allow_html=True)
    with col8:
        st.markdown(input("Vendedor",value=avaliacao['user']['name']),unsafe_allow_html=True)
    col9, col10, col11 = st.columns(3)
    with col9:
        st.markdown(input("Cor",value=avaliacao['vehicle']['color']['name']),unsafe_allow_html=True)
    with col10:
        st.markdown(input("Combustivel",value=avaliacao['vehicle']['fuel']['name']),unsafe_allow_html=True)
    with col11:
        st.markdown(input("Transmissão",value=avaliacao['vehicle']['transmission']['name']),unsafe_allow_html=True)
    st.markdown(input("Motor",avaliacao['vehicle']['version']['name']),unsafe_allow_html=True)

def referencias_garantia(avaliacao,classificacao):

        st.markdown(input("Marca",value=avaliacao['vehicle']['make']['name']),unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(input("Ano Fabricacao",value=avaliacao['vehicle']['assembly']),unsafe_allow_html=True)
        with col2:
            st.markdown(input("Anos de Garantia",value=ano_garantia(avaliacao['vehicle']['make']['name'],)),unsafe_allow_html=True)
        st.markdown(input("Provavel Garantia",value=tem_garantia(avaliacao['vehicle']['make']['name'],avaliacao['vehicle']['assembly'])),unsafe_allow_html=True)
        col3, col4 = st.columns(2)
        with col3:
            st.markdown(input("Concessionaria Origem",value=resposta(avaliacao['questions'],240)),unsafe_allow_html=True)
        with col4:
            st.markdown(input("Revisoes Garantia",value= ("Sim" if resposta(avaliacao['questions'],154) == "1" else "Nao")),unsafe_allow_html=True)
        col5, col6 = st.columns(2)
        with col5:
            st.markdown(input("Revisão 10.000KM",value= ("Sim" if resposta(avaliacao['questions'],241) == "1" else "Nao")),unsafe_allow_html=True)
        with col6:
            st.markdown(input("Revisão 20.000KM",value= ("Sim" if resposta(avaliacao['questions'],242) == "1" else "Nao")),unsafe_allow_html=True)
        st.markdown(input("Revisão 30.000KM",value= ("Sim" if resposta(avaliacao['questions'],243) == "1" else "Nao")),unsafe_allow_html=True)

def referencias(avaliacao,classificacao):

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(input("Valor Avaliado",value=avaliacao['valuation_value']),unsafe_allow_html=True)
    with col2:
        st.markdown(input("Gasto Previsto",value=avaliacao['expenses_value']),unsafe_allow_html=True)
    with col3:
        st.markdown(input("Top",value=avaliacao['top_dealer']),unsafe_allow_html=True)
    with col4:
        custo = avaliacao['valuation_value'] + avaliacao['expenses_value']
        st.markdown(input("Custo",value=custo),unsafe_allow_html=True)

    col5, col6 = st.columns(2)
    with col5:
        st.markdown(input("Fipe",value=avaliacao['fipe_value']),unsafe_allow_html=True)
    with col6:
        percent_fipe = (custo / avaliacao['fipe_value'])*100
        st.markdown(input("% fipe",value=f"{int(percent_fipe)} %"),unsafe_allow_html=True)

    col7, col8, col9, col10 = st.columns(4)
    with col7:
        st.markdown(input("Compra Fortaleza",value=referencias_media(avaliacao['references'],2)),unsafe_allow_html=True)
    with col8:
        st.markdown(input("Compra CE",value=referencias_max(avaliacao['references'],2)),unsafe_allow_html=True)
    with col9:
        st.markdown(input("Compra Brasil",value=referencias_min(avaliacao['references'],2)),unsafe_allow_html=True)

    col11, col12, col13, col14 = st.columns(4)
    with col11:
        st.markdown(input("B2B Fortaleza",value=referencias_media(avaliacao['references'],8)),unsafe_allow_html=True)
    with col12:
        st.markdown(input("B2B Ceara",value=referencias_max(avaliacao['references'],8)),unsafe_allow_html=True)
    with col13:
        st.markdown(input("B2B Brasil",value=referencias_min(avaliacao['references'],8)),unsafe_allow_html=True)

    col15, col16, col17, col18 = st.columns(4)
    with col15:
        st.markdown(input("B2C Fortaleza",value=referencias_media(avaliacao['references'],7)),unsafe_allow_html=True)
    with col16:
        st.markdown(input("B2C Ceara",value=referencias_max(avaliacao['references'],7)),unsafe_allow_html=True)
    with col17:
        st.markdown(input("B2C Brasil",value=referencias_min(avaliacao['references'],7)),unsafe_allow_html=True)

    st.markdown(input("WEB MOTORS",value=referencias_min(avaliacao['references'],1)),unsafe_allow_html=True)

    st.markdown(input("Sugestao de Venda",value=avaliacao['proposed_value']),unsafe_allow_html=True)

    st.markdown(input("Expectativa do Cliente",value=avaliacao['expected_value']),unsafe_allow_html=True)

def itens_avaliados(avaliacao):

    st.table(trata_itens(avaliacao['items']))

def simulador_vu(df_vendas):
        
        # VENDAS ESTOQUE VU (VEICULOS USADOS)
        vendas_vu = df_vendas[df_vendas['est_cd'] == "VU"]
        total_vendas = vendas_vu['nf_nr'].count()
        total_venda_media_mes = int(((vendas_vu['nf_nr'].count())/6).round(0))
        total_qtd_fin = vendas_vu['qtd_fin'].sum()
        percent_fin = (total_qtd_fin / total_vendas).round(1) * 100
        total_emplacamento = vendas_vu['emplacamento'].sum()
        percent_emplacamento = (total_emplacamento / total_vendas).round(2) * 100
        total_nf_margem = vendas_vu['nf_margem'].sum().round(2)
        total_faturamento = vendas_vu['nf_vlliquido'].sum().round(2)
        percent_margem = (total_nf_margem / total_faturamento).round(2) * 100

        
        

        col19, col20 = st.columns(2)
        with col19:
            st.markdown(input("Vendas Ultimos 6 Meses",total_vendas),unsafe_allow_html=True)
        with col20:
            st.markdown(input("Vendas por Mes",total_venda_media_mes),unsafe_allow_html=True)

        col21, col22 = st.columns(2)
        with col21:
            st.markdown(input("% Financiado",percent_fin),unsafe_allow_html=True)
        with col22:
            st.markdown(input("% Emplacamento",percent_emplacamento),unsafe_allow_html=True)
        st.markdown(input("% Margem",percent_margem),unsafe_allow_html=True)


def simulador_repasse(df_vendas):

    # VENDAS ESTOQUE REPASSE

        vendas_repasse = df_vendas[df_vendas['est_cd'].isin(['UF', 'VR'])]
        total_vendas_repasse = vendas_repasse['nf_nr'].count()
        total_venda_media_mes_repasse = int(((vendas_repasse['nf_nr'].count())/6).round(0))
        total_qtd_fin_repasse = vendas_repasse['qtd_fin'].sum()
        percent_fin_repasse = (total_qtd_fin_repasse / total_vendas_repasse).round(0) * 100
        total_emplacamento_repasse = vendas_repasse['emplacamento'].sum()
        percent_emplacamento_repasse = (total_emplacamento_repasse / total_vendas_repasse).round(1) * 100
        total_nf_margem_repasse = vendas_repasse['nf_margem'].sum().round(2)
        total_faturamento_repasse = vendas_repasse['nf_vlliquido'].sum().round(2)
        percent_margem_repasse = ((total_nf_margem_repasse / total_faturamento_repasse) * 100).round(0)
    
        col23, col24 = st.columns(2)
        with col23:
            st.markdown(input("Vendas Ultimos 6 Meses",total_vendas_repasse),unsafe_allow_html=True)
        with col24:
            st.markdown(input("Vendas por Mes",total_venda_media_mes_repasse),unsafe_allow_html=True)

        col25, col26 = st.columns(2)
        with col25:
            st.markdown(input("% Financiado",percent_fin_repasse),unsafe_allow_html=True)
        with col26:
            st.markdown(input("% Emplacamento",percent_emplacamento_repasse),unsafe_allow_html=True)
        st.markdown(input("% Margem",percent_margem_repasse),unsafe_allow_html=True)

def estoque_vu(df_estoque):

    # VENDAS ESTOQUE VU

    estoque_vu = df_estoque[df_estoque['est_cd'].isin(['VU', 'VT'])]
    total_estoque = estoque_vu['ve_nr'].count()
    media_dias_estoque = estoque_vu['dias'].mean().round(0)

    estoque_repasse = df_estoque[df_estoque['est_cd'].isin(['UF', 'VR'])]
    total_estoque_repasse = estoque_repasse['ve_nr'].count()
    media_dias_estoque_repasse = estoque_repasse['dias'].mean().round(0)


    col27, col28 = st.columns(2)
    with col27:
        st.markdown(input("Estoque SHOWROOM",total_estoque),unsafe_allow_html=True)
    with col28:
        st.markdown(input("Estoque REPASSE",total_estoque_repasse),unsafe_allow_html=True)

    col29, col30 = st.columns(2)
    with col29:
        st.markdown(input("Media DE",media_dias_estoque),unsafe_allow_html=True)
    with col30:
        st.markdown(input("Media DE REPASSE",media_dias_estoque_repasse),unsafe_allow_html=True)
        

def simulador_vn(df_vendas,modelo_interesse):
        
        # VENDAS ESTOQUE VN (VEICULOS NOVOS)
        vendas_vn = df_vendas[df_vendas['est_cd'] == "VN"]
        total_vendas = vendas_vn['nf_nr'].count()
        total_venda_media_mes = int(((vendas_vn['nf_nr'].count())/6).round(0))
        total_qtd_fin = vendas_vn['qtd_fin'].sum()
        percent_fin = (total_qtd_fin / total_vendas).round(1) * 100
        total_emplacamento = vendas_vn['emplacamento'].sum()
        percent_emplacamento = (total_emplacamento / total_vendas).round(2) * 100
        total_nf_margem = vendas_vn['nf_margem'].sum().round(2)
        total_faturamento = vendas_vn['nf_vlliquido'].sum().round(2)
        percent_margem = (total_nf_margem / total_faturamento).round(2) * 100

        st.markdown(input("Modelo Interesse",modelo_interesse),unsafe_allow_html=True)

        col19, col20 = st.columns(2)
        with col19:
            st.markdown(input("Vendas Ultimos 6 Meses",total_vendas),unsafe_allow_html=True)
        with col20:
            st.markdown(input("Vendas por Mes",total_venda_media_mes),unsafe_allow_html=True)

        col21, col22 = st.columns(2)
        with col21:
            st.markdown(input("% Financiado",percent_fin),unsafe_allow_html=True)
        with col22:
            st.markdown(input("% Emplacamento",percent_emplacamento),unsafe_allow_html=True)
        st.markdown(input("% Margem",percent_margem),unsafe_allow_html=True)

def estoque_vn(df_estoque):

    # VENDAS ESTOQUE VN

    estoque_vn = df_estoque[df_estoque['est_cd'] == "VN"]
    total_estoque = estoque_vn['ve_nr'].count()
    media_dias_estoque = estoque_vn['dias'].mean().round(0)

    col27, col28 = st.columns(2)
    with col27:
        st.markdown(input("Estoque SHOWROOM VN",total_estoque),unsafe_allow_html=True)
    with col28:
        st.markdown(input("Media DE",media_dias_estoque),unsafe_allow_html=True)


def preenchimento_usuario():



    #proposta = st.text_input("Digite o nr da Proposta")

    with st.form("meu_form"):

        valor_venda = st.text_input("Qual o valor de venda")
        margem = st.text_input("Qual o valor de margem?")

        top = st.selectbox(
                            "Tem Top?",
                            ["Sim", "Não"]
                        )
        

        valor_top = st.text_input("Digite o valor do TOP:")

        bonus = st.selectbox(
                            "Tem Bonus Agregado do Fabricante?",
                            ["Sim", "Não"]
                        )
        

        valor_bonus = st.text_input("Digite o valor do Bonus:")

        # VENDAS ESTOQUE VN
        emplacamento = st.selectbox(
                            "Tem Emplacamento?",
                            ["Sim", "Não"]
                        )
                        

 
        valor_emplacamento = st.text_input("Digite o valor do emplacamento:")
        
        financiamento = st.selectbox(
                            "Tem Financiamento?",
                            ["Sim", "Não"]
                        )
        

        valor_financiamento = st.text_input("Digite o valor do Financiamento:")
        if valor_financiamento:
            retorno_pb = float(valor_financiamento) * 0.035

        acessorios = st.selectbox(
                            "Tem Acessorio?",
                            ["Sim", "Não"]
                        )
        
        entrega_vu = st.selectbox(
                            "O cliente vai entregar o carro imediato?",
                            ["Sim", "Não"]
                        )
        enviar = st.form_submit_button("Enviar")

    
    
def analise_financeira(avaliacao,negociacao):

    dados = negociacao[0]
    custo_previsto = dados["expectativa_cliente"] + avaliacao['expenses_value']
    

    # DADOS B2B

    b2b_for = referencias_media(avaliacao['references'],8)
    #custo_previsto = avaliacao['valuation_value'] + avaliacao['expenses_value']
    margem_b2b_for = b2b_for - custo_previsto
    percent_b2b_for = ((margem_b2b_for / b2b_for) * 100)

    b2b_ce = referencias_max(avaliacao['references'],8)
    margem_b2b_ce = b2b_ce - custo_previsto
    percent_b2b_ce = ((margem_b2b_ce / b2b_ce) * 100)

    b2b_br = referencias_min(avaliacao['references'],8)
    margem_b2b_br = b2b_br - custo_previsto
    percent_b2b_br = ((margem_b2b_br / b2b_br) * 100)

    # DADOS B2C

    b2c_for = referencias_media(avaliacao['references'],7)
    margem_b2c_for = b2c_for - custo_previsto
    percent_b2c_for = (margem_b2c_for / b2c_for) * 100
 

    b2c_ce = referencias_max(avaliacao['references'],7)
    margem_b2c_ce = b2c_ce - custo_previsto
    percent_b2c_ce = ((margem_b2c_ce / b2c_ce))

    b2c_br = referencias_min(avaliacao['references'],7)
    margem_b2c_br = b2c_br - custo_previsto
    percent_b2c_br = ((margem_b2c_br / b2c_br) * 100)               

    valor_avaliado = avaliacao['valuation_value']

    # simulacao b2b

    simulacao_b2b_br = dados['valor_plus_bancario'] + dados['margem'] + margem_b2b_br
    simulacao_b2b_ce = dados['valor_plus_bancario'] + dados['margem'] + margem_b2b_ce
    simulacao_b2b_for = dados['valor_plus_bancario'] + dados['margem'] + margem_b2b_for

    # simulacao b2c

    simulacao_b2c_br = dados['valor_plus_bancario'] + dados['margem'] + margem_b2c_br
    simulacao_b2c_ce = dados['valor_plus_bancario'] + dados['margem'] + margem_b2c_ce
    simulacao_b2c_for = dados['valor_plus_bancario'] + dados['margem'] + margem_b2c_for

    st.markdown(input("Expectativa do Cliente",value=dados["expectativa_cliente"]),unsafe_allow_html=True)
    
    st.divider()


     # analise b2b br

    col1, col2, col3= st.columns(3)

    with col1:
        st.markdown(input("B2B BR",value=round(b2b_br,0)),unsafe_allow_html=True)
    with col2:
        st.markdown(input("Margem B2B BR",value=round(margem_b2b_br,0)),unsafe_allow_html=True)
    with col3:
        st.markdown(input("% Margem",value=round(percent_b2b_br,0)),unsafe_allow_html=True)

    # analise b2b ce

    st.divider()

    col1, col2, col3= st.columns(3)

    with col1:
        st.markdown(input("B2B CE",value=round(b2b_ce,0)),unsafe_allow_html=True)
    with col2:
        st.markdown(input("Margem B2B CE",value=round(margem_b2b_ce,0)),unsafe_allow_html=True)
    with col3:
        st.markdown(input("% Margem",value=round(percent_b2b_ce,0)),unsafe_allow_html=True)

    # analise b2b for

    st.divider()

    col1, col2, col3= st.columns(3)

    with col1:
        st.markdown(input("B2B For",value=round(b2b_for,0)),unsafe_allow_html=True)
    with col2:
        st.markdown(input("Margem B2B For",value=round(margem_b2b_for,0)),unsafe_allow_html=True)
    with col3:
        st.markdown(input("% Margem",value=round(percent_b2b_for,0)),unsafe_allow_html=True)

    #b2c br

    st.divider()

    col1, col2, col3= st.columns(3)

    with col1:
        st.markdown(input("B2C BR",value=round(b2c_br,0)),unsafe_allow_html=True)
    with col2:
        st.markdown(input("Margem B2C BR",value=round(margem_b2c_br,0)),unsafe_allow_html=True)
    with col3:
        st.markdown(input("% Margem",value=round(percent_b2c_br,0)),unsafe_allow_html=True)
    
    #b2c ce

    st.divider()


    col1, col2, col3= st.columns(3)

    with col1:
        st.markdown(input("B2C CE",value=round(b2c_ce,0)),unsafe_allow_html=True)
    with col2:
        st.markdown(input("Margem B2C CE",value=round(margem_b2c_ce,0)),unsafe_allow_html=True)
    with col3:
        st.markdown(input("% Margem",value=round(percent_b2c_ce,0)),unsafe_allow_html=True)
    
    #b2c for

    st.divider()

    col1, col2, col3= st.columns(3)

    with col1:
        st.markdown(input("B2C For",value=round(b2c_for,0)),unsafe_allow_html=True)
    with col2:
        st.markdown(input("Margem B2C For",value=round(margem_b2c_for,0)),unsafe_allow_html=True)
    with col3:
        st.markdown(input("% Margem",value=round(percent_b2c_for,0)),unsafe_allow_html=True)

    st.divider()

    col1, col2= st.columns(2)

    with col1:
        st.markdown("###### Pontos Positivos")
        #st.markdown("Pontos Positivos ✅")
        if dados["cliente_paga_emplacamento"] == "S ":
            st.markdown("Emplacamento Interno ✅")

        if dados["emplacamento_desconto"] == "N ":
            st.markdown("Emplacamento sem Desconto ✅")

        if dados["entrega_vu"] == "S ":
            data = datetime.fromtimestamp(dados['previsao_entrega_formatada'] / 1000)

            data_formatada = data.strftime("%d/%m/%Y")
            #st.markdown("Entrega do VU Imediata ✅" & {dados["previsao_entrega_formatada"]})
            st.markdown(
                        f"Entrega do VU Imediata ✅ {data_formatada}"
                    )

        if dados["financiamento"] == "S ":
            st.markdown("Financiamento Interno ✅")

        if dados["acessorios"] == "S ":
            st.markdown("Acessorio Vendido ✅")
    with col2:
        st.markdown("###### Pontos Negativos")
        if dados["cliente_paga_emplacamento"] == "N ":
            st.markdown("Emplacamento Interno ❌")

        if dados["emplacamento_desconto"] == "S ":
            st.markdown("Emplacamento com Desconto ❌")

        if dados["entrega_vu"] == "N ":
            st.markdown("Entrega do VU Imediata ❌")

        if dados["financiamento"] == "N ":
            st.markdown("Financiamento Interno ❌")

        if dados["acessorios"] == "N ":
            st.markdown("Acessorio Vendido ❌")

    st.divider()

    st.markdown("###### Simulação de negócio")
    st.write("A simulação é a soma das margens do VN com a previsão de margem do VU")
    st.divider()

    # SIMULACAO B2C

    st.write("Simulação no B2B BR")
    col1, col2, col3, col4= st.columns(4)

    
    with col1:
        st.markdown(input("Margem B2B BR",value=round(margem_b2b_br,0)),unsafe_allow_html=True)
    with col2:
        st.markdown(input("Margem do VN",value=dados['margem']),unsafe_allow_html=True)
    with col3:
       st.markdown(input("Plus Bancario do VN",value=dados['valor_plus_bancario']),unsafe_allow_html=True)
    with col4:
        st.markdown(input("Margem FINAL",value=round(simulacao_b2b_br,0)),unsafe_allow_html=True)

    st.divider()

    st.write("Simulação no B2B CE")
    col1, col2, col3, col4= st.columns(4)
    
    with col1:
        st.markdown(input("Margem B2B CE",value=round(margem_b2b_ce,0)),unsafe_allow_html=True)
    with col2:
        st.markdown(input("Margem do VN",value=dados['margem']),unsafe_allow_html=True)
    with col3:
       st.markdown(input("Plus Bancario do VN",value=dados['valor_plus_bancario']),unsafe_allow_html=True)
    with col4:
        st.markdown(input("Margem FINAL",value=round(simulacao_b2b_ce,0)),unsafe_allow_html=True)

    st.divider()

    st.write("Simulação no B2B FOR")
    col1, col2, col3, col4= st.columns(4)
    
    with col1:
        st.markdown(input("Margem B2B FOR",value=round(margem_b2b_for,0)),unsafe_allow_html=True)
    with col2:
        st.markdown(input("Margem do VN",value=dados['margem']),unsafe_allow_html=True)
    with col3:
       st.markdown(input("Plus Bancario do VN",value=dados['valor_plus_bancario']),unsafe_allow_html=True)
    with col4:
        st.markdown(input("Margem FINAL",value=round(simulacao_b2b_for,0)),unsafe_allow_html=True)

    st.divider()

    # SIMULACAO B2C
    st.write("Simulação no B2C BR")
    col1, col2, col3, col4= st.columns(4)

    
    with col1:
        st.markdown(input("Margem B2C BR",value=round(margem_b2c_br,0)),unsafe_allow_html=True)
    with col2:
        st.markdown(input("Margem do VN",value=dados['margem']),unsafe_allow_html=True)
    with col3:
       st.markdown(input("Plus Bancario do VN",value=dados['valor_plus_bancario']),unsafe_allow_html=True)
    with col4:
        st.markdown(input("Margem FINAL",value=round(simulacao_b2c_br,0)),unsafe_allow_html=True)

    st.divider()

    st.write("Simulação no B2C CE")
    col1, col2, col3, col4= st.columns(4)
    
    with col1:
        st.markdown(input("Margem B2C CE",value=round(margem_b2c_ce,0)),unsafe_allow_html=True)
    with col2:
        st.markdown(input("Margem do VN",value=dados['margem']),unsafe_allow_html=True)
    with col3:
       st.markdown(input("Plus Bancario do VN",value=dados['valor_plus_bancario']),unsafe_allow_html=True)
    with col4:
        st.markdown(input("Margem FINAL",value=round(simulacao_b2c_ce,0)),unsafe_allow_html=True)

    st.divider()

    st.write("Simulação no B2B FOR")
    col1, col2, col3, col4= st.columns(4)
    
    with col1:
        st.markdown(input("Margem B2B FOR",value=round(margem_b2c_for,0)),unsafe_allow_html=True)
    with col2:
        st.markdown(input("Margem do VN",value=dados['margem']),unsafe_allow_html=True)
    with col3:
       st.markdown(input("Plus Bancario do VN",value=dados['valor_plus_bancario']),unsafe_allow_html=True)
    with col4:
        st.markdown(input("Margem FINAL",value=round(simulacao_b2c_for,0)),unsafe_allow_html=True)
    
    
    



    



def dados_negociacao(df_negociacao):

    # VENDAS ESTOQUE VN

    dados = df_negociacao[0]

    col1, col2= st.columns(2)

    with col1:
        st.markdown(input("Valor Venda",value=dados['valor_venda']),unsafe_allow_html=True)
        st.markdown(input("Valor Financiado",value=dados['valor_financiamento']),unsafe_allow_html=True)
    
    
    with col2:
        st.markdown(input("Margem Liquida",value=dados['margem']),unsafe_allow_html=True)
        st.markdown(input("Plus Bancario",value=dados['valor_plus_bancario']),unsafe_allow_html=True)
        










