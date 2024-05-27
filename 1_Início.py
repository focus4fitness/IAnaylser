# BIBLIOTECAS USADAS

import streamlit as st
from PIL import Image
from io import BytesIO

import pandas as pd
import numpy as np
import requests

from plots.plots_insta1 import *
from plots.layout import *
from plots.plots import *

im = Image.open("instagram.png")
st.set_page_config(page_title="Instagram Monitor", page_icon=im, layout="wide")

st.markdown(""" <style>
        footer {visibility: hidden;}
        </style> """, unsafe_allow_html=True)


st.markdown("<h1 style='font-size:250%; text-align: center; color: #8435B4; padding: 0px 0px;'" +
                ">Instagram Monitor</h1>", unsafe_allow_html=True)
st.markdown('---')

st.markdown("""<style> .css-z5fcl4.egzxvld4 {margin-top: -75px;}</style>""", unsafe_allow_html=True)
st.markdown("""<style> .css-1544g2n.e1fqkh3o4 {margin-top: -40px;}</style>""", unsafe_allow_html=True)
st.markdown("""<style> .card {margin-top: -50px;}</style>""", unsafe_allow_html=True)



with st.sidebar:
    st.markdown("<h1 style='font-size:150%; text-align: center; color: #8435B4; padding: 0px 0px;'" +
                ">Painel de controle</h1>", unsafe_allow_html=True)
    st.markdown('---')

    API = st.radio('Selecione o tipo da análise sobre o Perfil:',
                   ['Informações Perfil', 'Feed 50+ Posts'],
                   help='Tipos de análise do Perfil:\n\n'
                        '- INFORMAÇÕES PERFIL: nesta aba, é possível visualizar informações básicas sobre o perfil '
                        'do Instagram pesquisado, como nome de usuário, número de seguidores, seguidos e quantidade '
                        'de publicações. Também são apresentadas as últimas 12 publicações do perfil, permitindo uma '
                        'rápida visualização do tipo de conteúdo postado.\n\n'
                        '- FEED 50+ POSTS: nesta aba, o usuário tem acesso a uma análise mais detalhada das publicações '
                        'do perfil pesquisado. Inicialmente são exibidas as últimas 50 publicações, mas é possível '
                        'selecionar até 250 posts. Através dessa análise, é possível ter uma visão completa do perfil '
                        'e entender melhor como os seguidores interagem com as publicações.',

                   index=0, key=99, horizontal=True)

    perfil = st.text_input("Insira o Perfil que deseja analisar:",
                           help='Pesquise qualquer Perfil do Instagram ABERTO com mais de 12 publicações '
                                'para começar sua análise. Preencha apenas com nome da conta, SEM @')

    if API == 'Feed 50+ Posts':
        end_cursor = st.slider('Selecione o N° de Publicações:',
                                   min_value=50, max_value=250, value=50, step=50, key=95)

    FUNCAO = st.radio('Selecione o tipo da análise:',
                      ['Dashboard Personalizado 📈', 'Observatório de Dados 🔎'],
                      help = 'Escolha o tipo de analise para realizar nos dados:\n\n'
                             '- DASHBOARD PERSONALIZADO: explore dados de forma rápida e simples através de gráficos pré-desenvolvidos. Descubra insights valiosos respondendo às principais perguntas.\n\n'
                             '- OBSERVATÓRIO DE DADOS: analise todas as variáveis dos dados sob diferentes perspectivas, usando diversos gráficos e filtros para responder às perguntas mais criativas.',
                      index=0, key=97, horizontal=False)


if len(perfil) == 0:
    st.markdown(html_card_1, unsafe_allow_html=True)

elif len(perfil) != 0:
    res_info = requi_info(perfil)
    df_info = convert_info_instagram_looter2(res_info)

    userid = df_info['USER_ID'].values
    if API == 'Informações Perfil':
        df_midia = convert_info_midias(res_info)

    elif API == 'Feed 50+ Posts':
        res_midias = requi_midias0(userid, "50")
        df_midia = convert_midias0(res_midias)

        df_midia = api_feed(end_cursor, res_midias, df_midia, userid)

    with st.sidebar:
        with st.expander("🎲️ Filtrar os dados"):
            tipo_df = df_midia['TIPO POST'].unique().tolist()
            tipo_df = st.multiselect("Selecione os tipos de publicação:",
                                              options=tipo_df, default=tipo_df, key=41)

            like_max = int(df_midia['LIKES'].max())
            like_min = int(df_midia['LIKES'].min())
            likes_range_min, likes_range_max = st.slider('Selecione o intervalo de likes:',
                                                     min_value=like_min, max_value=like_max,
                                                     value=(like_min, like_max), step=1, key=44)
            mask_likes = (df_midia['LIKES'] >= likes_range_min) & (df_midia['LIKES'] <= likes_range_max)

            comentarios_max = int(df_midia['COMENTARIOS'].max())
            comentarios_min = int(df_midia['COMENTARIOS'].min())
            comentarios_range_min, comentarios_range_max = st.slider('Selecione o intervalo de comentários:',
                                                         min_value=comentarios_min, max_value=comentarios_max,
                                                         value=(comentarios_min, comentarios_max), step=1, key=45)
            mask_comentarios = (df_midia['COMENTARIOS'] >= comentarios_range_min) & \
                               (df_midia['COMENTARIOS'] <= comentarios_range_max)

            df_midia['DIA'] = pd.to_datetime(df_midia['DIA'])

            dia_min = df_midia['DIA'].min().date()
            dia_max = df_midia['DIA'].max().date()

            if dia_max != dia_min:

                dia_range_min, dia_range_max = st.slider('Selecione o intervalo de dias:',
                                                         min_value=dia_min, max_value=dia_max,
                                                         value=(dia_min, dia_max),
                                                         step=pd.Timedelta(days=1))
            else:
                st.info('Filtro indisponível, base de dados com apenas um dia, selecione mais dados.')


            # filtrar o DataFrame usando a máscara

            ano_max = int(df_midia['HORA'].max())
            ano_min = int(df_midia['HORA'].min())
            ano_range_min, ano_range_max = st.slider('Selecione o intervalo de horas:',
                                                      min_value=ano_min, max_value=ano_max,
                                                     value=(ano_min, ano_max), step=1)
            mask_valor = (df_midia['HORA'] >= ano_range_min) & (df_midia['HORA'] <= ano_range_max)

            semana_df = df_midia['SEMANA'].unique().tolist()
            semana_df = st.multiselect("Selecione os dias da semana:",
                                     options=semana_df, default=semana_df, key=43)


    df_midia = df_midia.loc[mask_valor]
    df_midia = df_midia[df_midia['TIPO POST'].isin(tipo_df)]
    df_midia = df_midia[df_midia['SEMANA'].isin(semana_df)]




    if FUNCAO == 'Observatório de Dados 🔎':
        parte1(df_info, df_midia)

    elif FUNCAO == 'Dashboard Personalizado 📈':
        dashboard(df_info, df_midia)








rodape()