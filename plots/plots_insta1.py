import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import numpy as np
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from wordcloud import STOPWORDS
from datetime import datetime
import requests


from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode

config={"displayModeBar": True,
        "displaylogo": False,
        'modeBarButtonsToRemove': ['toggleSpikelines', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'hoverClosestCartesian']}


def agg_tabela(df, use_checkbox):

    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(enabled=False)
    gb.configure_default_column(groupable=True, value=True, enableRowGroup=True,
                                    aggFunc="sum", editable=True)
    gb.configure_selection(use_checkbox=use_checkbox, selection_mode='multiple')
    gb.configure_side_bar()
    gridoptions = gb.build()
    df_grid = AgGrid(df, gridOptions=gridoptions, enable_enterprise_modules=True,
                     update_mode=GridUpdateMode.SELECTION_CHANGED, height=300, width='100%')
    selected_rows = df_grid["selected_rows"]
    selected_rows = pd.DataFrame(selected_rows)

    return selected_rows


def bar_plot(df, varx, vary, cor1):


    values = df[varx]
    y = df[vary]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=values, y=y, text=y, textposition='inside', insidetextanchor='start', name='',
        textfont=dict(size=20, color='white', family='Arial'), texttemplate='%{text:.3s}',
        hovertemplate="</br><b>"+varx+":</b> %{x}" +
                      "</br><b>"+vary+":</b> %{y}",
        marker_color=cor1))
    fig.update_layout(
        paper_bgcolor="#F8F8FF", plot_bgcolor="#F8F8FF", font={'color': "#000000", 'family': "sans-serif"},
        height=315, margin=dict(l=80, r=20, b=10, t=30), autosize=False,
        dragmode=False, hovermode="x", clickmode="event+select")
    fig.update_yaxes(
        title_text=vary, title_font=dict(family='Sans-serif', size=12),
        tickfont=dict(family='Sans-serif', size=12), nticks=8, showgrid=True, gridwidth=0.5, gridcolor='#D3D3D3')
    fig.update_xaxes(
        title_text=varx, title_font=dict(family='Sans-serif', size=12),
        dtick=5, tickfont=dict(family='Sans-serif', size=12), nticks=10, showgrid=False
    )

    for figure in fig.data:
        figure.update(
            selected=dict(marker=dict(color="#E30613")),
            unselected=dict(marker=dict(color="#05A854", opacity=1)),
        )

    return fig

def line_plot(df, varx, vary, cor1):
    fig = go.Figure()

    values = df[varx]
    y = df[vary]

    fig.add_trace(go.Scatter(
        x=values, y=y,
        mode='lines+markers', hovertemplate=None, line=dict(width=3, color=cor1)))

    fig.update_layout(
        paper_bgcolor="#F8F8FF", plot_bgcolor="#F8F8FF", font={'color': "#000000", 'family': "sans-serif"},
        legend=dict(font_size=10, orientation="h", yanchor="top", y=1.10, xanchor="center", x=0.35),
        height=315, hovermode="x unified", autosize=False, dragmode=False, margin=dict(l=80, r=20, b=0, t=30),
        clickmode="event+select",
    )
    fig.update_yaxes(
        title_text=vary, title_font=dict(family='Sans-serif', size=12),
        tickfont=dict(family='Sans-serif', size=12), nticks=10, showgrid=True, gridwidth=0.5, gridcolor='#D3D3D3')
    fig.update_xaxes(
        title_text=varx, title_font=dict(family='Sans-serif', size=12),
        dtick=5, tickfont=dict(family='Sans-serif', size=12), nticks=10, showgrid=False
    )

    for figure in fig.data:
        figure.update(
            selected=dict(marker=dict(color="#E30613")),
            unselected=dict(marker=dict(color="#05A854", opacity=1)),
        )

    return fig

def barplot1(x, y):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=x, y=y, name="Mídias",
        hovertemplate="</br><b>Eixo Y:</b> %{y}" +
                      "</br><b>Eixo X:</b> %{x}",
        textposition='none', marker_color='#C13584'))
    fig.update_layout(
        paper_bgcolor="#F8F8FF", plot_bgcolor="#F8F8FF", font={'color': "#000000", 'family': "sans-serif"},
        height=300, barmode='stack', margin=dict(l=10, r=10, b=10, t=10), autosize=True)
    fig.update_xaxes(
        title_text="Eixo X - Mídias Publicadas", title_font=dict(family='Sans-serif', size=12),
        tickfont=dict(family='Sans-serif', size=12), showgrid=False)
    fig.update_yaxes(
        title_text="Eixo Y - Mídias Publicadas", title_font=dict(family='Sans-serif', size=12),
        tickfont=dict(family='Sans-serif', size=12), nticks=7, showgrid=True, gridwidth=0.5, gridcolor='#D3D3D3')

    return fig

def barplot2(x, y):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=x, y=y, name="Vídeos",
        hovertemplate="</br><b>Eixo Y:</b> %{y}" +
                      "</br><b>Eixo X:</b> %{x}",
        textposition='none', marker_color='#E1306C'))
    fig.update_layout(
        paper_bgcolor="#F8F8FF", plot_bgcolor="#F8F8FF", font={'color': "#000000", 'family': "sans-serif"},
        legend=dict(font_size=11, orientation="h", yanchor="top", y=1.20, xanchor="center", x=0.5),
        height=300, barmode='stack', margin=dict(l=10, r=10, b=10, t=10), autosize=True)
    fig.update_xaxes(
        title_text="Eixo X - Vídeos Publicados", title_font=dict(family='Sans-serif', size=12),
        tickfont=dict(family='Sans-serif', size=12), showgrid=False)
    fig.update_yaxes(
        title_text="Eixo Y - Vídeos Publicados", title_font=dict(family='Sans-serif', size=12),
        tickfont=dict(family='Sans-serif', size=12), nticks=7, showgrid=True, gridwidth=0.5, gridcolor='#D3D3D3')

    return fig

def lineplot1(x, y):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, y=y,
        name='Mídias', mode='lines', hovertemplate=None, xhoverformat="%d %b %y",
        line=dict(width=1, color='#E1306C'), stackgroup='one'))
    fig.update_layout(
        paper_bgcolor="#F8F8FF", plot_bgcolor="#F8F8FF", font={'color': "#000000", 'family': "sans-serif"},
        height=300, barmode='stack', margin=dict(l=10, r=10, b=10, t=10), autosize=True, hovermode="x unified")
    fig.update_xaxes(
        title_text="Eixo X - Mídias Publicadas", title_font=dict(family='Sans-serif', size=12),
        tickfont=dict(family='Sans-serif', size=12), showgrid=False)
    fig.update_yaxes(
        title_text="Eixo Y - Mídias Publicadas", title_font=dict(family='Sans-serif', size=12),
        tickfont=dict(family='Sans-serif', size=12), nticks=7, showgrid=True, gridwidth=0.5, gridcolor='#D3D3D3')

    return fig

def lineplot2(x, y):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, y=y,
        name='Vídeos', mode='lines', hovertemplate=None, xhoverformat="%d %b %y",
        line=dict(width=1, color='#E1306C'), stackgroup='one'))
    fig.update_layout(
        paper_bgcolor="#F8F8FF", plot_bgcolor="#F8F8FF", font={'color': "#000000", 'family': "sans-serif"},
        height=300, barmode='stack', margin=dict(l=10, r=10, b=10, t=10), autosize=True, hovermode="x unified")
    fig.update_xaxes(
        title_text="Eixo X - Vídeos Publicados", title_font=dict(family='Sans-serif', size=12),
        tickfont=dict(family='Sans-serif', size=12), showgrid=False)
    fig.update_yaxes(
        title_text="Eixo Y - Vídeos Publicados", title_font=dict(family='Sans-serif', size=12),
        tickfont=dict(family='Sans-serif', size=12), nticks=7, showgrid=True, gridwidth=0.5, gridcolor='#D3D3D3')

    return fig


def aggrid_tabela(df):
    gd = GridOptionsBuilder.from_dataframe(df)
    gd.configure_pagination(enabled=True)
    gd.configure_default_column(editable=True)
    gd.configure_selection()
    gd.configure_side_bar()
    gridoptions = gd.build()
    ag = AgGrid(df, gridOptions=gridoptions, enable_enterprise_modules=False,
                height=250, width='100%')

    return ag


def wordcloud(df):
    words = ' '.join(df['LEGENDA'])

    stop_words = STOPWORDS.update(["da", "do", "a", "e", "o", "em", "para", "um",
                                   "que", "por", "como", "uma", "de", "onde", "são",
                                   "sim", "não", "mas", "mais", "então", "das", "dos", "nas", "nos",
                                   "bio", "link", "isso", "tem", "até"])

    fig, ax = plt.subplots()
    wordcloud = WordCloud(
        height=150,
        min_font_size=8,
        scale=2.5,
        background_color='#F8F8FF',
        max_words=100,
        stopwords=stop_words,
        min_word_length=3).generate(words)
    plt.imshow(wordcloud)
    plt.axis('off')  # to off the axis of x and

    return fig






@st.cache_data
def requi_info(user_name):

    url = "https://instagram-looter2.p.rapidapi.com/profile"

    querystring = {"username": user_name}

    headers = {
        "X-RapidAPI-Key": "c84a203889mshb6a0f46c721ea40p154795jsnad2958a17b4c",
        "X-RapidAPI-Host": "instagram-looter2.p.rapidapi.com"
    }

    res = requests.request("GET", url, headers=headers, params=querystring).json()

    return res

st.cache_data
def requi_midias0(userid, batch_size):
    url = "https://instagram-looter2.p.rapidapi.com/user-feeds"

    querystring = {"id": userid, "count": batch_size}

    headers = {
        "X-RapidAPI-Key": "c84a203889mshb6a0f46c721ea40p154795jsnad2958a17b4c",
        "X-RapidAPI-Host": "instagram-looter2.p.rapidapi.com"
    }

    res = requests.request("GET", url, headers=headers, params=querystring).json()

    return res



@st.cache_data
def requi_midias1(userid, batch_size, end_cursor):
    url = "https://instagram-looter2.p.rapidapi.com/user-feeds"

    querystring = {"id": userid, "count": batch_size,
                   "end_cursor": end_cursor}

    headers = {
        "X-RapidAPI-Key": "c84a203889mshb6a0f46c721ea40p154795jsnad2958a17b4c",
        "X-RapidAPI-Host": "instagram-looter2.p.rapidapi.com"
    }

    res = requests.request("GET", url, headers=headers, params=querystring).json()

    return res

@st.cache_data
def requi_midias2(userid, batch_size, end_cursor):
    url = "https://instagram-looter2.p.rapidapi.com/user-feeds"

    querystring = {"id": userid, "count": batch_size,
                   "end_cursor": end_cursor}

    headers = {
        "X-RapidAPI-Key": "155b1ce6bemsh7851045d8978e84p13f9c6jsn1541a024d218",
        "X-RapidAPI-Host": "instagram-looter2.p.rapidapi.com"
    }

    res = requests.request("GET", url, headers=headers, params=querystring).json()

    return res

@st.cache_data
def requi_midias3(userid, batch_size, end_cursor):
    url = "https://instagram-looter2.p.rapidapi.com/user-feeds"

    querystring = {"id": userid, "count": batch_size,
                   "end_cursor": end_cursor}

    headers = {
        "X-RapidAPI-Key": "c84a203889mshb6a0f46c721ea40p154795jsnad2958a17b4c",
        "X-RapidAPI-Host": "instagram-looter2.p.rapidapi.com"
    }

    res = requests.request("GET", url, headers=headers, params=querystring).json()

    return res

@st.cache_data
def convert_info(res):
    ex_url = res["data"]["user"]["external_url"]
    id = res["data"]["user"]["id"]
    full_name = res["data"]["user"]["full_name"]
    is_verified = res["data"]["user"]["is_verified"]
    seguidores = res["data"]["user"]["edge_followed_by"]['count']
    seguindo = res["data"]["user"]["edge_follow"]['count']
    midia = res["data"]["user"]["edge_owner_to_timeline_media"]["count"]
    igtv = res["data"]["user"]["total_igtv_videos"]
    is_business = res["data"]["user"]["is_business"]
    category = res["data"]["user"]["category"]
    foto = res["data"]["user"]["profile_pic_url_hd"]

    dados = {'seguidores': seguidores, 'seguindo': seguindo, 'midia': midia, 'igtv': igtv,
             'verificado': is_verified, 'business': is_business, 'categoria':category,
             'full_name': full_name, 'userid': id, 'ex_url': ex_url, 'foto': foto }
    dados = pd.DataFrame([dados])

    return dados

@st.cache_data
def convert_info_instagram_looter2(res):
    ex_url = res["external_url"]
    id = res["id"]
    full_name = res["full_name"]
    is_verified = res["is_verified"]
    seguidores = res["edge_followed_by"]['count']
    seguindo = res["edge_follow"]['count']
    midia = res["edge_owner_to_timeline_media"]["count"]
    is_professional = res["is_professional_account"]
    is_business = res["is_business_account"]
    category = res["category_name"]
    foto = res["profile_pic_url_hd"]
    biography = res["biography"]

    dados = {'SEGUIDORES': seguidores, 'SEGUINDO': seguindo, 'PUBLICAÇÕES': midia, 'CATEGORIA':category,
             'NOME': full_name, 'VERIFICADO?': is_verified,
             'BUSINESS?': is_business,'PROFISSIONAL?': is_professional,
             'USER_ID': id, 'BIO': biography, 'LINK BIO': ex_url, 'FOTO HD': foto }
    dados = pd.DataFrame([dados])

    return dados

@st.cache_data
def convert_info_midias(res):
    df0m = res["edge_owner_to_timeline_media"]['edges'][0]['node']
    df1m = res["edge_owner_to_timeline_media"]['edges'][1]['node']
    df2m = res["edge_owner_to_timeline_media"]['edges'][2]['node']
    df3m = res["edge_owner_to_timeline_media"]['edges'][3]['node']
    df4m = res["edge_owner_to_timeline_media"]['edges'][4]['node']
    df5m = res["edge_owner_to_timeline_media"]['edges'][5]['node']
    df6m = res["edge_owner_to_timeline_media"]['edges'][6]['node']
    df7m = res["edge_owner_to_timeline_media"]['edges'][7]['node']
    df8m = res["edge_owner_to_timeline_media"]['edges'][8]['node']
    df9m = res["edge_owner_to_timeline_media"]['edges'][9]['node']
    df10m = res["edge_owner_to_timeline_media"]['edges'][10]['node']
    df11m = res["edge_owner_to_timeline_media"]['edges'][11]['node']

    df0_1 = df0m["edge_media_to_comment"]['count']
    df0_1 = pd.DataFrame([df0_1])
    df0_2 = df0m["edge_media_preview_like"]['count']
    df0_2 = pd.DataFrame([df0_2])
    df0_3 = df0m["edge_media_to_caption"]['edges'][0]['node']['text']
    df0_3 = pd.DataFrame([df0_3])

    df1_1 = df1m["edge_media_to_comment"]['count']
    df1_1 = pd.DataFrame([df1_1])
    df1_2 = df1m["edge_media_preview_like"]['count']
    df1_2 = pd.DataFrame([df1_2])
    df1_3 = df1m["edge_media_to_caption"]['edges'][0]['node']['text']
    df1_3 = pd.DataFrame([df1_3])

    df2_1 = df2m["edge_media_to_comment"]['count']
    df2_1 = pd.DataFrame([df2_1])
    df2_2 = df2m["edge_media_preview_like"]['count']
    df2_2 = pd.DataFrame([df2_2])
    df2_3 = df2m["edge_media_to_caption"]['edges'][0]['node']['text']
    df2_3 = pd.DataFrame([df2_3])

    df3_1 = df3m["edge_media_to_comment"]['count']
    df3_1 = pd.DataFrame([df3_1])
    df3_2 = df3m["edge_media_preview_like"]['count']
    df3_2 = pd.DataFrame([df3_2])
    df3_3 = df3m["edge_media_to_caption"]['edges'][0]['node']['text']
    df3_3 = pd.DataFrame([df3_3])

    df4_1 = df4m["edge_media_to_comment"]['count']
    df4_1 = pd.DataFrame([df4_1])
    df4_2 = df4m["edge_media_preview_like"]['count']
    df4_2 = pd.DataFrame([df4_2])
    df4_3 = df4m["edge_media_to_caption"]['edges'][0]['node']['text']
    df4_3 = pd.DataFrame([df4_3])

    df5_1 = df5m["edge_media_to_comment"]['count']
    df5_1 = pd.DataFrame([df5_1])
    df5_2 = df5m["edge_media_preview_like"]['count']
    df5_2 = pd.DataFrame([df5_2])
    df5_3 = df5m["edge_media_to_caption"]['edges'][0]['node']['text']
    df5_3 = pd.DataFrame([df5_3])

    df6_1 = df6m["edge_media_to_comment"]['count']
    df6_1 = pd.DataFrame([df6_1])
    df6_2 = df6m["edge_media_preview_like"]['count']
    df6_2 = pd.DataFrame([df6_2])
    df6_3 = df6m["edge_media_to_caption"]['edges'][0]['node']['text'];
    df6_3 = pd.DataFrame([df6_3])

    df7_1 = df7m["edge_media_to_comment"]['count']
    df7_1 = pd.DataFrame([df7_1])
    df7_2 = df7m["edge_media_preview_like"]['count']
    df7_2 = pd.DataFrame([df7_2])
    df7_3 = df7m["edge_media_to_caption"]['edges'][0]['node']['text']
    df7_3 = pd.DataFrame([df7_3])

    df8_1 = df8m["edge_media_to_comment"]['count']
    df8_1 = pd.DataFrame([df8_1])
    df8_2 = df8m["edge_media_preview_like"]['count']
    df8_2 = pd.DataFrame([df8_2])
    df8_3 = df8m["edge_media_to_caption"]['edges'][0]['node']['text']
    df8_3 = pd.DataFrame([df8_3])

    df9_1 = df9m["edge_media_to_comment"]['count']
    df9_1 = pd.DataFrame([df9_1])
    df9_2 = df9m["edge_media_preview_like"]['count']
    df9_2 = pd.DataFrame([df9_2])
    df9_3 = df9m["edge_media_to_caption"]['edges'][0]['node']['text']
    df9_3 = pd.DataFrame([df9_3])

    df10_1 = df10m["edge_media_to_comment"]['count'];
    df10_1 = pd.DataFrame([df10_1])
    df10_2 = df10m["edge_media_preview_like"]['count'];
    df10_2 = pd.DataFrame([df10_2])
    df10_3 = df10m["edge_media_to_caption"]['edges'][0]['node']['text'];
    df10_3 = pd.DataFrame([df10_3])

    df11_1 = df11m["edge_media_to_comment"]['count'];
    df11_1 = pd.DataFrame([df11_1])
    df11_2 = df11m["edge_media_preview_like"]['count'];
    df11_2 = pd.DataFrame([df11_2])
    df11_3 = df11m["edge_media_to_caption"]['edges'][0]['node']['text'];
    df11_3 = pd.DataFrame([df11_3])

    df0m = pd.DataFrame([df0m])
    df1m = pd.DataFrame([df1m])
    df2m = pd.DataFrame([df2m])
    df3m = pd.DataFrame([df3m])
    df4m = pd.DataFrame([df4m])
    df5m = pd.DataFrame([df5m])
    df6m = pd.DataFrame([df6m])
    df7m = pd.DataFrame([df7m])
    df8m = pd.DataFrame([df8m])
    df9m = pd.DataFrame([df9m])
    df10m = pd.DataFrame([df10m])
    df11m = pd.DataFrame([df11m])

    df0_ = pd.concat([df0m, df0_1, df0_2, df0_3], axis=1)
    df1_ = pd.concat([df1m, df1_1, df1_2, df1_3], axis=1)
    df2_ = pd.concat([df2m, df2_1, df2_2, df2_3], axis=1)
    df3_ = pd.concat([df3m, df3_1, df3_2, df3_3], axis=1)
    df4_ = pd.concat([df4m, df4_1, df4_2, df4_3], axis=1)
    df5_ = pd.concat([df5m, df5_1, df5_2, df5_3], axis=1)
    df6_ = pd.concat([df6m, df6_1, df6_2, df6_3], axis=1)
    df7_ = pd.concat([df7m, df7_1, df7_2, df7_3], axis=1)
    df8_ = pd.concat([df8m, df8_1, df8_2, df8_3], axis=1)
    df9_ = pd.concat([df9m, df9_1, df9_2, df9_3], axis=1)
    df10_ = pd.concat([df10m, df10_1, df10_2, df10_3], axis=1)
    df11_ = pd.concat([df11m, df11_1, df11_2, df11_3], axis=1)

    df0_.columns.values[-3] = "COMENTARIOS"
    df0_.columns.values[-2] = "LIKES"
    df0_.columns.values[-1] = "TEXTO"

    df1_.columns.values[-3] = "COMENTARIOS"
    df1_.columns.values[-2] = "LIKES"
    df1_.columns.values[-1] = "TEXTO"

    df2_.columns.values[-3] = "COMENTARIOS"
    df2_.columns.values[-2] = "LIKES"
    df2_.columns.values[-1] = "TEXTO"

    df3_.columns.values[-3] = "COMENTARIOS"
    df3_.columns.values[-2] = "LIKES"
    df3_.columns.values[-1] = "TEXTO"

    df4_.columns.values[-3] = "COMENTARIOS"
    df4_.columns.values[-2] = "LIKES"
    df4_.columns.values[-1] = "TEXTO"

    df5_.columns.values[-3] = "COMENTARIOS"
    df5_.columns.values[-2] = "LIKES"
    df5_.columns.values[-1] = "TEXTO"

    df6_.columns.values[-3] = "COMENTARIOS"
    df6_.columns.values[-2] = "LIKES"
    df6_.columns.values[-1] = "TEXTO"

    df7_.columns.values[-3] = "COMENTARIOS"
    df7_.columns.values[-2] = "LIKES"
    df7_.columns.values[-1] = "TEXTO"

    df8_.columns.values[-3] = "COMENTARIOS"
    df8_.columns.values[-2] = "LIKES"
    df8_.columns.values[-1] = "TEXTO"

    df9_.columns.values[-3] = "COMENTARIOS"
    df9_.columns.values[-2] = "LIKES"
    df9_.columns.values[-1] = "TEXTO"

    df10_.columns.values[-3] = "COMENTARIOS"
    df10_.columns.values[-2] = "LIKES"
    df10_.columns.values[-1] = "TEXTO"

    df11_.columns.values[-3] = "COMENTARIOS"
    df11_.columns.values[-2] = "LIKES"
    df11_.columns.values[-1] = "TEXTO"

    df = pd.concat([df0_, df1_, df2_, df3_, df4_, df5_, df6_, df7_, df8_, df9_, df10_, df11_], axis=0)

    df['TIME'] = [datetime.fromtimestamp(x) for x in df['taken_at_timestamp']]
    df['HORA'] = pd.to_datetime(df['TIME']).dt.hour
    df['DIA'] = pd.to_datetime(df['TIME']).dt.date
    df['DIA'] = df['DIA'].apply(lambda x: x.strftime('%Y-%m-%d'))
    df['SEMANA'] = pd.to_datetime(df['TIME']).apply(lambda x: x.weekday())

    conditions_semana = [(df['SEMANA'] == 0), (df['SEMANA'] == 1),(df['SEMANA'] == 2),
                         (df['SEMANA'] == 3),(df['SEMANA'] == 4), (df['SEMANA'] == 5),(df['SEMANA'] == 6)]

    df['SEMANA'] = np.select(conditions_semana,
                             ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo'])

    conditions = [(df['HORA'] >= 6) & (df['HORA'] <= 12),
                  (df['HORA'] >= 12) & (df['HORA'] <= 18),
                  (df['HORA'] >= 18) & (df['HORA'] <= 24),
                  (df['HORA'] >= 0) & (df['HORA'] <= 6)]
    values = ['Manhã', 'Tarde', 'Noite', 'Madrugada']
    df['TURNO'] = np.select(conditions, values)
    df['UNIDADE'] = np.where(df['LIKES'] == 2, 0, 1)
    df['shortcode'] = 'https://www.instagram.com/p/'+df['shortcode']


    df['COMENTARIOS'] = pd.to_numeric(df['COMENTARIOS'], errors='coerce').astype('Int64')
    df['LIKES'] = pd.to_numeric(df['LIKES'], errors='coerce').astype('Int64')
    df['HORA'] = pd.to_numeric(df['HORA'], errors='coerce').astype('Int64')

    df['INTERAÇÕES'] = df['LIKES'] + df['COMENTARIOS']

    df['% COMENTOU'] = df.apply(lambda row: round(row['COMENTARIOS']*100 / row['LIKES'], 2), axis=1)
    df['%VAR INTERAÇÕES'] = round((df['INTERAÇÕES'] - df['INTERAÇÕES'].shift(-1)) / df['INTERAÇÕES'].shift(-1) * 100, 2)
    df['VARIAÇÃO INTERAÇÕES'] = round((df['INTERAÇÕES'] - df['INTERAÇÕES'].shift(-1)), 2)

    df['UNIDADE'] = np.where(df['TIME'] == 2, 0, 1)

    df['__typename'].replace('GraphSidecar', 'Coleção', inplace=True)
    df['__typename'].replace('GraphImage', 'Imagem', inplace=True)
    df['__typename'].replace('GraphVideo', 'Vídeo', inplace=True)
    df = df[['TIME', '__typename', 'TEXTO', 'LIKES', 'COMENTARIOS', '% COMENTOU',
             'INTERAÇÕES', 'VARIAÇÃO INTERAÇÕES', '%VAR INTERAÇÕES',
             'shortcode', 'SEMANA', 'TURNO', 'HORA', 'DIA', 'id', 'UNIDADE']]

    df = df.rename(columns={'__typename': 'TIPO POST', 'shortcode': 'LINK', 'id': 'ID POST', 'TEXTO':'LEGENDA'})


    return df


@st.cache_resource
def convert_midias0(res):
    df0 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][0]['node']
    df1 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][1]['node']
    df2 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][2]['node']
    df3 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][3]['node']
    df4 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][4]['node']
    df5 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][5]['node']
    df6 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][6]['node']
    df7 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][7]['node']
    df8 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][8]['node']
    df9 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][9]['node']
    df10 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][10]['node']
    df11 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][11]['node']
    df12 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][12]['node']
    df13 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][13]['node']
    df14 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][14]['node']
    df15 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][15]['node']
    df16 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][16]['node']
    df17 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][17]['node']
    df18 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][18]['node']
    df19 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][19]['node']
    df20 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][20]['node']
    df21 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][21]['node']
    df22 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][22]['node']
    df23 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][23]['node']
    df24 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][24]['node']
    df25 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][25]['node']
    df26 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][26]['node']
    df27 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][27]['node']
    df28 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][28]['node']
    df29 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][29]['node']
    df30 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][30]['node']
    df31 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][31]['node']
    df32 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][32]['node']
    df33 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][33]['node']
    df34 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][34]['node']
    df35 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][35]['node']
    df36 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][36]['node']
    df37 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][37]['node']
    df38 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][38]['node']
    df39 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][39]['node']
    df40 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][40]['node']
    df41 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][41]['node']
    df42 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][42]['node']
    df43 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][43]['node']
    df44 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][44]['node']
    df45 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][45]['node']
    df46 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][46]['node']
    df47 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][47]['node']
    df48 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][48]['node']
    df49 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][49]['node']

    df0_1 = df0["edge_media_to_comment"]['count'];
    df0_1 = pd.DataFrame([df0_1])
    df0_2 = df0["edge_media_preview_like"]['count'];
    df0_2 = pd.DataFrame([df0_2])
    df0_3 = df0["edge_media_to_caption"]['edges'][0]['node']['text'];
    df0_3 = pd.DataFrame([df0_3])

    df1_1 = df1["edge_media_to_comment"]['count'];
    df1_1 = pd.DataFrame([df1_1])
    df1_2 = df1["edge_media_preview_like"]['count'];
    df1_2 = pd.DataFrame([df1_2])
    df1_3 = df1["edge_media_to_caption"]['edges'][0]['node']['text'];
    df1_3 = pd.DataFrame([df1_3])

    df2_1 = df2["edge_media_to_comment"]['count'];
    df2_1 = pd.DataFrame([df2_1])
    df2_2 = df2["edge_media_preview_like"]['count'];
    df2_2 = pd.DataFrame([df2_2])
    df2_3 = df2["edge_media_to_caption"]['edges'][0]['node']['text'];
    df2_3 = pd.DataFrame([df2_3])

    df3_1 = df3["edge_media_to_comment"]['count'];
    df3_1 = pd.DataFrame([df3_1])
    df3_2 = df3["edge_media_preview_like"]['count'];
    df3_2 = pd.DataFrame([df3_2])
    df3_3 = df3["edge_media_to_caption"]['edges'][0]['node']['text'];
    df3_3 = pd.DataFrame([df3_3])

    df4_1 = df4["edge_media_to_comment"]['count'];
    df4_1 = pd.DataFrame([df4_1])
    df4_2 = df4["edge_media_preview_like"]['count'];
    df4_2 = pd.DataFrame([df4_2])
    df4_3 = df4["edge_media_to_caption"]['edges'][0]['node']['text'];
    df4_3 = pd.DataFrame([df4_3])

    df5_1 = df5["edge_media_to_comment"]['count'];
    df5_1 = pd.DataFrame([df5_1])
    df5_2 = df5["edge_media_preview_like"]['count'];
    df5_2 = pd.DataFrame([df5_2])
    df5_3 = df5["edge_media_to_caption"]['edges'][0]['node']['text'];
    df5_3 = pd.DataFrame([df5_3])

    df6_1 = df6["edge_media_to_comment"]['count'];
    df6_1 = pd.DataFrame([df6_1])
    df6_2 = df6["edge_media_preview_like"]['count'];
    df6_2 = pd.DataFrame([df6_2])
    df6_3 = df6["edge_media_to_caption"]['edges'][0]['node']['text'];
    df6_3 = pd.DataFrame([df6_3])

    df7_1 = df7["edge_media_to_comment"]['count'];
    df7_1 = pd.DataFrame([df7_1])
    df7_2 = df7["edge_media_preview_like"]['count'];
    df7_2 = pd.DataFrame([df7_2])
    df7_3 = df7["edge_media_to_caption"]['edges'][0]['node']['text'];
    df7_3 = pd.DataFrame([df7_3])

    df8_1 = df8["edge_media_to_comment"]['count'];
    df8_1 = pd.DataFrame([df8_1])
    df8_2 = df8["edge_media_preview_like"]['count'];
    df8_2 = pd.DataFrame([df8_2])
    df8_3 = df8["edge_media_to_caption"]['edges'][0]['node']['text'];
    df8_3 = pd.DataFrame([df8_3])

    df9_1 = df9["edge_media_to_comment"]['count'];
    df9_1 = pd.DataFrame([df9_1])
    df9_2 = df9["edge_media_preview_like"]['count'];
    df9_2 = pd.DataFrame([df9_2])
    df9_3 = df9["edge_media_to_caption"]['edges'][0]['node']['text'];
    df9_3 = pd.DataFrame([df9_3])

    df10_1 = df10["edge_media_to_comment"]['count'];
    df10_1 = pd.DataFrame([df10_1])
    df10_2 = df10["edge_media_preview_like"]['count'];
    df10_2 = pd.DataFrame([df10_2])
    df10_3 = df10["edge_media_to_caption"]['edges'][0]['node']['text'];
    df10_3 = pd.DataFrame([df10_3])

    df11_1 = df11["edge_media_to_comment"]['count'];
    df11_1 = pd.DataFrame([df11_1])
    df11_2 = df11["edge_media_preview_like"]['count'];
    df11_2 = pd.DataFrame([df11_2])
    df11_3 = df11["edge_media_to_caption"]['edges'][0]['node']['text'];
    df11_3 = pd.DataFrame([df11_3])

    df12_1 = df12["edge_media_to_comment"]['count'];
    df12_1 = pd.DataFrame([df12_1])
    df12_2 = df12["edge_media_preview_like"]['count'];
    df12_2 = pd.DataFrame([df12_2])
    df12_3 = df12["edge_media_to_caption"]['edges'][0]['node']['text'];
    df12_3 = pd.DataFrame([df12_3])

    df13_1 = df13["edge_media_to_comment"]['count'];
    df13_1 = pd.DataFrame([df13_1])
    df13_2 = df13["edge_media_preview_like"]['count'];
    df13_2 = pd.DataFrame([df13_2])
    df13_3 = df13["edge_media_to_caption"]['edges'][0]['node']['text'];
    df13_3 = pd.DataFrame([df13_3])

    df14_1 = df14["edge_media_to_comment"]['count'];
    df14_1 = pd.DataFrame([df14_1])
    df14_2 = df14["edge_media_preview_like"]['count'];
    df14_2 = pd.DataFrame([df14_2])
    df14_3 = df14["edge_media_to_caption"]['edges'][0]['node']['text'];
    df14_3 = pd.DataFrame([df14_3])

    df15_1 = df15["edge_media_to_comment"]['count'];
    df15_1 = pd.DataFrame([df15_1])
    df15_2 = df15["edge_media_preview_like"]['count'];
    df15_2 = pd.DataFrame([df15_2])
    df15_3 = df15["edge_media_to_caption"]['edges'][0]['node']['text'];
    df15_3 = pd.DataFrame([df15_3])

    df16_1 = df16["edge_media_to_comment"]['count'];
    df16_1 = pd.DataFrame([df16_1])
    df16_2 = df16["edge_media_preview_like"]['count'];
    df16_2 = pd.DataFrame([df16_2])
    df16_3 = df16["edge_media_to_caption"]['edges'][0]['node']['text'];
    df16_3 = pd.DataFrame([df16_3])

    df17_1 = df17["edge_media_to_comment"]['count'];
    df17_1 = pd.DataFrame([df17_1])
    df17_2 = df17["edge_media_preview_like"]['count'];
    df17_2 = pd.DataFrame([df17_2])
    df17_3 = df17["edge_media_to_caption"]['edges'][0]['node']['text'];
    df17_3 = pd.DataFrame([df17_3])

    df18_1 = df18["edge_media_to_comment"]['count'];
    df18_1 = pd.DataFrame([df18_1])
    df18_2 = df18["edge_media_preview_like"]['count'];
    df18_2 = pd.DataFrame([df18_2])
    df18_3 = df18["edge_media_to_caption"]['edges'][0]['node']['text'];
    df18_3 = pd.DataFrame([df18_3])

    df19_1 = df19["edge_media_to_comment"]['count'];
    df19_1 = pd.DataFrame([df19_1])
    df19_2 = df19["edge_media_preview_like"]['count'];
    df19_2 = pd.DataFrame([df19_2])
    df19_3 = df19["edge_media_to_caption"]['edges'][0]['node']['text'];
    df19_3 = pd.DataFrame([df19_3])

    df20_1 = df20["edge_media_to_comment"]['count'];
    df20_1 = pd.DataFrame([df20_1])
    df20_2 = df20["edge_media_preview_like"]['count'];
    df20_2 = pd.DataFrame([df20_2])
    df20_3 = df20["edge_media_to_caption"]['edges'][0]['node']['text'];
    df20_3 = pd.DataFrame([df20_3])

    df21_1 = df21["edge_media_to_comment"]['count'];
    df21_1 = pd.DataFrame([df21_1])
    df21_2 = df21["edge_media_preview_like"]['count'];
    df21_2 = pd.DataFrame([df21_2])
    df21_3 = df21["edge_media_to_caption"]['edges'][0]['node']['text'];
    df21_3 = pd.DataFrame([df21_3])

    df22_1 = df22["edge_media_to_comment"]['count'];
    df22_1 = pd.DataFrame([df22_1])
    df22_2 = df22["edge_media_preview_like"]['count'];
    df22_2 = pd.DataFrame([df22_2])
    df22_3 = df22["edge_media_to_caption"]['edges'][0]['node']['text'];
    df22_3 = pd.DataFrame([df22_3])

    df23_1 = df23["edge_media_to_comment"]['count'];
    df23_1 = pd.DataFrame([df23_1])
    df23_2 = df23["edge_media_preview_like"]['count'];
    df23_2 = pd.DataFrame([df23_2])
    df23_3 = df23["edge_media_to_caption"]['edges'][0]['node']['text'];
    df23_3 = pd.DataFrame([df23_3])

    df24_1 = df24["edge_media_to_comment"]['count'];
    df24_1 = pd.DataFrame([df24_1])
    df24_2 = df24["edge_media_preview_like"]['count'];
    df24_2 = pd.DataFrame([df24_2])
    df24_3 = df24["edge_media_to_caption"]['edges'][0]['node']['text'];
    df24_3 = pd.DataFrame([df24_3])

    df25_1 = df25["edge_media_to_comment"]['count'];
    df25_1 = pd.DataFrame([df25_1])
    df25_2 = df25["edge_media_preview_like"]['count'];
    df25_2 = pd.DataFrame([df25_2])
    df25_3 = df25["edge_media_to_caption"]['edges'][0]['node']['text'];
    df25_3 = pd.DataFrame([df25_3])

    df26_1 = df26["edge_media_to_comment"]['count'];
    df26_1 = pd.DataFrame([df26_1])
    df26_2 = df26["edge_media_preview_like"]['count'];
    df26_2 = pd.DataFrame([df26_2])
    df26_3 = df26["edge_media_to_caption"]['edges'][0]['node']['text'];
    df26_3 = pd.DataFrame([df26_3])

    df27_1 = df27["edge_media_to_comment"]['count'];
    df27_1 = pd.DataFrame([df27_1])
    df27_2 = df27["edge_media_preview_like"]['count'];
    df27_2 = pd.DataFrame([df27_2])
    df27_3 = df27["edge_media_to_caption"]['edges'][0]['node']['text'];
    df27_3 = pd.DataFrame([df27_3])

    df28_1 = df28["edge_media_to_comment"]['count'];
    df28_1 = pd.DataFrame([df28_1])
    df28_2 = df28["edge_media_preview_like"]['count'];
    df28_2 = pd.DataFrame([df28_2])
    df28_3 = df28["edge_media_to_caption"]['edges'][0]['node']['text'];
    df28_3 = pd.DataFrame([df28_3])

    df29_1 = df29["edge_media_to_comment"]['count'];
    df29_1 = pd.DataFrame([df29_1])
    df29_2 = df29["edge_media_preview_like"]['count'];
    df29_2 = pd.DataFrame([df29_2])
    df29_3 = df29["edge_media_to_caption"]['edges'][0]['node']['text'];
    df29_3 = pd.DataFrame([df29_3])

    df30_1 = df30["edge_media_to_comment"]['count'];
    df30_1 = pd.DataFrame([df30_1])
    df30_2 = df30["edge_media_preview_like"]['count'];
    df30_2 = pd.DataFrame([df30_2])
    df30_3 = df30["edge_media_to_caption"]['edges'][0]['node']['text'];
    df30_3 = pd.DataFrame([df30_3])

    df31_1 = df31["edge_media_to_comment"]['count'];
    df31_1 = pd.DataFrame([df31_1])
    df31_2 = df31["edge_media_preview_like"]['count'];
    df31_2 = pd.DataFrame([df31_2])
    df31_3 = df31["edge_media_to_caption"]['edges'][0]['node']['text'];
    df31_3 = pd.DataFrame([df31_3])

    df32_1 = df32["edge_media_to_comment"]['count'];
    df32_1 = pd.DataFrame([df32_1])
    df32_2 = df32["edge_media_preview_like"]['count'];
    df32_2 = pd.DataFrame([df32_2])
    df32_3 = df32["edge_media_to_caption"]['edges'][0]['node']['text'];
    df32_3 = pd.DataFrame([df32_3])

    df33_1 = df33["edge_media_to_comment"]['count'];
    df33_1 = pd.DataFrame([df33_1])
    df33_2 = df33["edge_media_preview_like"]['count'];
    df33_2 = pd.DataFrame([df33_2])
    df33_3 = df33["edge_media_to_caption"]['edges'][0]['node']['text'];
    df33_3 = pd.DataFrame([df33_3])

    df34_1 = df34["edge_media_to_comment"]['count'];
    df34_1 = pd.DataFrame([df34_1])
    df34_2 = df34["edge_media_preview_like"]['count'];
    df34_2 = pd.DataFrame([df34_2])
    df34_3 = df34["edge_media_to_caption"]['edges'][0]['node']['text'];
    df34_3 = pd.DataFrame([df34_3])

    df35_1 = df35["edge_media_to_comment"]['count'];
    df35_1 = pd.DataFrame([df35_1])
    df35_2 = df35["edge_media_preview_like"]['count'];
    df35_2 = pd.DataFrame([df35_2])
    df35_3 = df35["edge_media_to_caption"]['edges'][0]['node']['text'];
    df35_3 = pd.DataFrame([df35_3])

    df36_1 = df36["edge_media_to_comment"]['count'];
    df36_1 = pd.DataFrame([df36_1])
    df36_2 = df36["edge_media_preview_like"]['count'];
    df36_2 = pd.DataFrame([df36_2])
    df36_3 = df36["edge_media_to_caption"]['edges'][0]['node']['text'];
    df36_3 = pd.DataFrame([df36_3])

    df37_1 = df37["edge_media_to_comment"]['count'];
    df37_1 = pd.DataFrame([df37_1])
    df37_2 = df37["edge_media_preview_like"]['count'];
    df37_2 = pd.DataFrame([df37_2])
    df37_3 = df37["edge_media_to_caption"]['edges'][0]['node']['text'];
    df37_3 = pd.DataFrame([df37_3])

    df38_1 = df38["edge_media_to_comment"]['count'];
    df38_1 = pd.DataFrame([df38_1])
    df38_2 = df38["edge_media_preview_like"]['count'];
    df38_2 = pd.DataFrame([df38_2])
    df38_3 = df38["edge_media_to_caption"]['edges'][0]['node']['text'];
    df38_3 = pd.DataFrame([df38_3])

    df39_1 = df39["edge_media_to_comment"]['count'];
    df39_1 = pd.DataFrame([df39_1])
    df39_2 = df39["edge_media_preview_like"]['count'];
    df39_2 = pd.DataFrame([df39_2])
    df39_3 = df39["edge_media_to_caption"]['edges'][0]['node']['text'];
    df39_3 = pd.DataFrame([df39_3])

    df40_1 = df40["edge_media_to_comment"]['count'];
    df40_1 = pd.DataFrame([df40_1])
    df40_2 = df40["edge_media_preview_like"]['count'];
    df40_2 = pd.DataFrame([df40_2])
    df40_3 = df40["edge_media_to_caption"]['edges'][0]['node']['text'];
    df40_3 = pd.DataFrame([df40_3])

    df41_1 = df41["edge_media_to_comment"]['count'];
    df41_1 = pd.DataFrame([df41_1])
    df41_2 = df41["edge_media_preview_like"]['count'];
    df41_2 = pd.DataFrame([df41_2])
    df41_3 = df41["edge_media_to_caption"]['edges'][0]['node']['text'];
    df41_3 = pd.DataFrame([df41_3])

    df42_1 = df42["edge_media_to_comment"]['count'];
    df42_1 = pd.DataFrame([df42_1])
    df42_2 = df42["edge_media_preview_like"]['count'];
    df42_2 = pd.DataFrame([df42_2])
    df42_3 = df42["edge_media_to_caption"]['edges'][0]['node']['text'];
    df42_3 = pd.DataFrame([df42_3])

    df43_1 = df43["edge_media_to_comment"]['count'];
    df43_1 = pd.DataFrame([df43_1])
    df43_2 = df43["edge_media_preview_like"]['count'];
    df43_2 = pd.DataFrame([df43_2])
    df43_3 = df43["edge_media_to_caption"]['edges'][0]['node']['text'];
    df43_3 = pd.DataFrame([df43_3])

    df44_1 = df44["edge_media_to_comment"]['count'];
    df44_1 = pd.DataFrame([df44_1])
    df44_2 = df44["edge_media_preview_like"]['count'];
    df44_2 = pd.DataFrame([df44_2])
    df44_3 = df44["edge_media_to_caption"]['edges'][0]['node']['text'];
    df44_3 = pd.DataFrame([df44_3])

    df45_1 = df45["edge_media_to_comment"]['count'];
    df45_1 = pd.DataFrame([df45_1])
    df45_2 = df45["edge_media_preview_like"]['count'];
    df45_2 = pd.DataFrame([df45_2])
    df45_3 = df45["edge_media_to_caption"]['edges'][0]['node']['text'];
    df45_3 = pd.DataFrame([df45_3])

    df46_1 = df46["edge_media_to_comment"]['count'];
    df46_1 = pd.DataFrame([df46_1])
    df46_2 = df46["edge_media_preview_like"]['count'];
    df46_2 = pd.DataFrame([df46_2])
    df46_3 = df46["edge_media_to_caption"]['edges'][0]['node']['text'];
    df46_3 = pd.DataFrame([df46_3])

    df47_1 = df47["edge_media_to_comment"]['count'];
    df47_1 = pd.DataFrame([df47_1])
    df47_2 = df47["edge_media_preview_like"]['count'];
    df47_2 = pd.DataFrame([df47_2])
    df47_3 = df47["edge_media_to_caption"]['edges'][0]['node']['text'];
    df47_3 = pd.DataFrame([df47_3])

    df48_1 = df48["edge_media_to_comment"]['count'];
    df48_1 = pd.DataFrame([df48_1])
    df48_2 = df48["edge_media_preview_like"]['count'];
    df48_2 = pd.DataFrame([df48_2])
    df48_3 = df48["edge_media_to_caption"]['edges'][0]['node']['text'];
    df48_3 = pd.DataFrame([df48_3])

    df49_1 = df49["edge_media_to_comment"]['count'];
    df49_1 = pd.DataFrame([df49_1])
    df49_2 = df49["edge_media_preview_like"]['count'];
    df49_2 = pd.DataFrame([df49_2])
    df49_3 = df49["edge_media_to_caption"]['edges'][0]['node']['text'];
    df49_3 = pd.DataFrame([df49_3])

    df0 = pd.DataFrame([df0])
    df1 = pd.DataFrame([df1])
    df2 = pd.DataFrame([df2])
    df3 = pd.DataFrame([df3])
    df4 = pd.DataFrame([df4])
    df5 = pd.DataFrame([df5])
    df6 = pd.DataFrame([df6])
    df7 = pd.DataFrame([df7])
    df8 = pd.DataFrame([df8])
    df9 = pd.DataFrame([df9])

    df10 = pd.DataFrame([df10])
    df11 = pd.DataFrame([df11])
    df12 = pd.DataFrame([df12])
    df13 = pd.DataFrame([df13])
    df14 = pd.DataFrame([df14])
    df15 = pd.DataFrame([df15])
    df16 = pd.DataFrame([df16])
    df17 = pd.DataFrame([df17])
    df18 = pd.DataFrame([df18])
    df19 = pd.DataFrame([df19])
    df20 = pd.DataFrame([df20])

    df21 = pd.DataFrame([df21])
    df22 = pd.DataFrame([df22])
    df23 = pd.DataFrame([df23])
    df24 = pd.DataFrame([df24])
    df25 = pd.DataFrame([df25])
    df26 = pd.DataFrame([df26])
    df27 = pd.DataFrame([df27])
    df28 = pd.DataFrame([df28])
    df29 = pd.DataFrame([df29])

    df30 = pd.DataFrame([df30])
    df31 = pd.DataFrame([df31])
    df32 = pd.DataFrame([df32])
    df33 = pd.DataFrame([df33])
    df34 = pd.DataFrame([df34])
    df35 = pd.DataFrame([df35])
    df36 = pd.DataFrame([df36])
    df37 = pd.DataFrame([df37])
    df38 = pd.DataFrame([df38])
    df39 = pd.DataFrame([df39])

    df40 = pd.DataFrame([df40])
    df41 = pd.DataFrame([df41])
    df42 = pd.DataFrame([df42])
    df43 = pd.DataFrame([df43])
    df44 = pd.DataFrame([df44])
    df45 = pd.DataFrame([df45])
    df46 = pd.DataFrame([df46])
    df47 = pd.DataFrame([df47])
    df48 = pd.DataFrame([df48])
    df49 = pd.DataFrame([df49])

    df0_ = pd.concat([df0, df0_1, df0_2, df0_3], axis=1)
    df1_ = pd.concat([df1, df1_1, df1_2, df1_3], axis=1)
    df2_ = pd.concat([df2, df2_1, df2_2, df2_3], axis=1)
    df3_ = pd.concat([df3, df3_1, df3_2, df3_3], axis=1)
    df4_ = pd.concat([df4, df4_1, df4_2, df4_3], axis=1)
    df5_ = pd.concat([df5, df5_1, df5_2, df5_3], axis=1)
    df6_ = pd.concat([df6, df6_1, df6_2, df6_3], axis=1)
    df7_ = pd.concat([df7, df7_1, df7_2, df7_3], axis=1)
    df8_ = pd.concat([df8, df8_1, df8_2, df8_3], axis=1)
    df9_ = pd.concat([df9, df9_1, df9_2, df9_3], axis=1)

    df10_ = pd.concat([df10, df10_1, df10_2, df10_3], axis=1)
    df11_ = pd.concat([df11, df11_1, df11_2, df11_3], axis=1)
    df12_ = pd.concat([df12, df12_1, df12_2, df12_3], axis=1)
    df13_ = pd.concat([df13, df13_1, df13_2, df13_3], axis=1)
    df14_ = pd.concat([df14, df14_1, df14_2, df14_3], axis=1)
    df15_ = pd.concat([df15, df15_1, df15_2, df15_3], axis=1)
    df16_ = pd.concat([df16, df16_1, df16_2, df16_3], axis=1)
    df17_ = pd.concat([df17, df17_1, df17_2, df17_3], axis=1)
    df18_ = pd.concat([df18, df18_1, df18_2, df18_3], axis=1)
    df19_ = pd.concat([df19, df19_1, df19_2, df19_3], axis=1)

    df20_ = pd.concat([df20, df20_1, df20_2, df20_3], axis=1)
    df21_ = pd.concat([df21, df21_1, df21_2, df21_3], axis=1)
    df22_ = pd.concat([df22, df22_1, df22_2, df22_3], axis=1)
    df23_ = pd.concat([df23, df23_1, df23_2, df23_3], axis=1)
    df24_ = pd.concat([df24, df24_1, df24_2, df24_3], axis=1)
    df25_ = pd.concat([df25, df25_1, df25_2, df25_3], axis=1)
    df26_ = pd.concat([df26, df26_1, df26_2, df26_3], axis=1)
    df27_ = pd.concat([df27, df27_1, df27_2, df27_3], axis=1)
    df28_ = pd.concat([df28, df28_1, df28_2, df28_3], axis=1)
    df29_ = pd.concat([df29, df29_1, df29_2, df29_3], axis=1)

    df30_ = pd.concat([df30, df30_1, df30_2, df30_3], axis=1)
    df31_ = pd.concat([df31, df31_1, df31_2, df31_3], axis=1)
    df32_ = pd.concat([df32, df32_1, df32_2, df32_3], axis=1)
    df33_ = pd.concat([df33, df33_1, df33_2, df33_3], axis=1)
    df34_ = pd.concat([df34, df34_1, df34_2, df34_3], axis=1)
    df35_ = pd.concat([df35, df35_1, df35_2, df35_3], axis=1)
    df36_ = pd.concat([df36, df36_1, df36_2, df36_3], axis=1)
    df37_ = pd.concat([df37, df37_1, df37_2, df37_3], axis=1)
    df38_ = pd.concat([df38, df38_1, df38_2, df38_3], axis=1)
    df39_ = pd.concat([df39, df39_1, df39_2, df39_3], axis=1)

    df40_ = pd.concat([df40, df40_1, df40_2, df40_3], axis=1)
    df41_ = pd.concat([df41, df41_1, df41_2, df41_3], axis=1)
    df42_ = pd.concat([df42, df42_1, df42_2, df42_3], axis=1)
    df43_ = pd.concat([df43, df43_1, df43_2, df43_3], axis=1)
    df44_ = pd.concat([df44, df44_1, df44_2, df44_3], axis=1)
    df45_ = pd.concat([df45, df45_1, df45_2, df45_3], axis=1)
    df46_ = pd.concat([df46, df46_1, df46_2, df46_3], axis=1)
    df47_ = pd.concat([df47, df47_1, df47_2, df47_3], axis=1)
    df48_ = pd.concat([df48, df48_1, df48_2, df48_3], axis=1)
    df49_ = pd.concat([df49, df49_1, df49_2, df49_3], axis=1)

    df0_.columns.values[-3] = "COMENTARIOS"
    df0_.columns.values[-2] = "LIKES"
    df0_.columns.values[-1] = "TEXTO"

    df1_.columns.values[-3] = "COMENTARIOS"
    df1_.columns.values[-2] = "LIKES"
    df1_.columns.values[-1] = "TEXTO"

    df2_.columns.values[-3] = "COMENTARIOS"
    df2_.columns.values[-2] = "LIKES"
    df2_.columns.values[-1] = "TEXTO"

    df3_.columns.values[-3] = "COMENTARIOS"
    df3_.columns.values[-2] = "LIKES"
    df3_.columns.values[-1] = "TEXTO"

    df4_.columns.values[-3] = "COMENTARIOS"
    df4_.columns.values[-2] = "LIKES"
    df4_.columns.values[-1] = "TEXTO"

    df5_.columns.values[-3] = "COMENTARIOS"
    df5_.columns.values[-2] = "LIKES"
    df5_.columns.values[-1] = "TEXTO"

    df6_.columns.values[-3] = "COMENTARIOS"
    df6_.columns.values[-2] = "LIKES"
    df6_.columns.values[-1] = "TEXTO"

    df7_.columns.values[-3] = "COMENTARIOS"
    df7_.columns.values[-2] = "LIKES"
    df7_.columns.values[-1] = "TEXTO"

    df8_.columns.values[-3] = "COMENTARIOS"
    df8_.columns.values[-2] = "LIKES"
    df8_.columns.values[-1] = "TEXTO"

    df9_.columns.values[-3] = "COMENTARIOS"
    df9_.columns.values[-2] = "LIKES"
    df9_.columns.values[-1] = "TEXTO"

    df10_.columns.values[-3] = "COMENTARIOS"
    df10_.columns.values[-2] = "LIKES"
    df10_.columns.values[-1] = "TEXTO"

    df11_.columns.values[-3] = "COMENTARIOS"
    df11_.columns.values[-2] = "LIKES"
    df11_.columns.values[-1] = "TEXTO"

    df12_.columns.values[-3] = "COMENTARIOS"
    df12_.columns.values[-2] = "LIKES"
    df12_.columns.values[-1] = "TEXTO"

    df13_.columns.values[-3] = "COMENTARIOS"
    df13_.columns.values[-2] = "LIKES"
    df13_.columns.values[-1] = "TEXTO"

    df14_.columns.values[-3] = "COMENTARIOS"
    df14_.columns.values[-2] = "LIKES"
    df14_.columns.values[-1] = "TEXTO"

    df15_.columns.values[-3] = "COMENTARIOS"
    df15_.columns.values[-2] = "LIKES"
    df15_.columns.values[-1] = "TEXTO"

    df16_.columns.values[-3] = "COMENTARIOS"
    df16_.columns.values[-2] = "LIKES"
    df16_.columns.values[-1] = "TEXTO"

    df17_.columns.values[-3] = "COMENTARIOS"
    df17_.columns.values[-2] = "LIKES"
    df17_.columns.values[-1] = "TEXTO"

    df18_.columns.values[-3] = "COMENTARIOS"
    df18_.columns.values[-2] = "LIKES"
    df18_.columns.values[-1] = "TEXTO"

    df19_.columns.values[-3] = "COMENTARIOS"
    df19_.columns.values[-2] = "LIKES"
    df19_.columns.values[-1] = "TEXTO"

    df20_.columns.values[-3] = "COMENTARIOS"
    df20_.columns.values[-2] = "LIKES"
    df20_.columns.values[-1] = "TEXTO"

    df21_.columns.values[-3] = "COMENTARIOS"
    df21_.columns.values[-2] = "LIKES"
    df21_.columns.values[-1] = "TEXTO"

    df22_.columns.values[-3] = "COMENTARIOS"
    df22_.columns.values[-2] = "LIKES"
    df22_.columns.values[-1] = "TEXTO"

    df23_.columns.values[-3] = "COMENTARIOS"
    df23_.columns.values[-2] = "LIKES"
    df23_.columns.values[-1] = "TEXTO"

    df24_.columns.values[-3] = "COMENTARIOS"
    df24_.columns.values[-2] = "LIKES"
    df24_.columns.values[-1] = "TEXTO"

    df25_.columns.values[-3] = "COMENTARIOS"
    df25_.columns.values[-2] = "LIKES"
    df25_.columns.values[-1] = "TEXTO"

    df26_.columns.values[-3] = "COMENTARIOS"
    df26_.columns.values[-2] = "LIKES"
    df26_.columns.values[-1] = "TEXTO"

    df27_.columns.values[-3] = "COMENTARIOS"
    df27_.columns.values[-2] = "LIKES"
    df27_.columns.values[-1] = "TEXTO"

    df28_.columns.values[-3] = "COMENTARIOS"
    df28_.columns.values[-2] = "LIKES"
    df28_.columns.values[-1] = "TEXTO"

    df29_.columns.values[-3] = "COMENTARIOS"
    df29_.columns.values[-2] = "LIKES"
    df29_.columns.values[-1] = "TEXTO"

    df30_.columns.values[-3] = "COMENTARIOS"
    df30_.columns.values[-2] = "LIKES"
    df30_.columns.values[-1] = "TEXTO"

    df31_.columns.values[-3] = "COMENTARIOS"
    df31_.columns.values[-2] = "LIKES"
    df31_.columns.values[-1] = "TEXTO"

    df32_.columns.values[-3] = "COMENTARIOS"
    df32_.columns.values[-2] = "LIKES"
    df32_.columns.values[-1] = "TEXTO"

    df33_.columns.values[-3] = "COMENTARIOS"
    df33_.columns.values[-2] = "LIKES"
    df33_.columns.values[-1] = "TEXTO"

    df34_.columns.values[-3] = "COMENTARIOS"
    df34_.columns.values[-2] = "LIKES"
    df34_.columns.values[-1] = "TEXTO"

    df35_.columns.values[-3] = "COMENTARIOS"
    df35_.columns.values[-2] = "LIKES"
    df35_.columns.values[-1] = "TEXTO"

    df36_.columns.values[-3] = "COMENTARIOS"
    df36_.columns.values[-2] = "LIKES"
    df36_.columns.values[-1] = "TEXTO"

    df37_.columns.values[-3] = "COMENTARIOS"
    df37_.columns.values[-2] = "LIKES"
    df37_.columns.values[-1] = "TEXTO"

    df38_.columns.values[-3] = "COMENTARIOS"
    df38_.columns.values[-2] = "LIKES"
    df38_.columns.values[-1] = "TEXTO"

    df39_.columns.values[-3] = "COMENTARIOS"
    df39_.columns.values[-2] = "LIKES"
    df39_.columns.values[-1] = "TEXTO"

    df40_.columns.values[-3] = "COMENTARIOS"
    df40_.columns.values[-2] = "LIKES"
    df40_.columns.values[-1] = "TEXTO"

    df41_.columns.values[-3] = "COMENTARIOS"
    df41_.columns.values[-2] = "LIKES"
    df41_.columns.values[-1] = "TEXTO"

    df42_.columns.values[-3] = "COMENTARIOS"
    df42_.columns.values[-2] = "LIKES"
    df42_.columns.values[-1] = "TEXTO"

    df43_.columns.values[-3] = "COMENTARIOS"
    df43_.columns.values[-2] = "LIKES"
    df43_.columns.values[-1] = "TEXTO"

    df44_.columns.values[-3] = "COMENTARIOS"
    df44_.columns.values[-2] = "LIKES"
    df44_.columns.values[-1] = "TEXTO"

    df45_.columns.values[-3] = "COMENTARIOS"
    df45_.columns.values[-2] = "LIKES"
    df45_.columns.values[-1] = "TEXTO"

    df46_.columns.values[-3] = "COMENTARIOS"
    df46_.columns.values[-2] = "LIKES"
    df46_.columns.values[-1] = "TEXTO"

    df47_.columns.values[-3] = "COMENTARIOS"
    df47_.columns.values[-2] = "LIKES"
    df47_.columns.values[-1] = "TEXTO"

    df48_.columns.values[-3] = "COMENTARIOS"
    df48_.columns.values[-2] = "LIKES"
    df48_.columns.values[-1] = "TEXTO"

    df49_.columns.values[-3] = "COMENTARIOS"
    df49_.columns.values[-2] = "LIKES"
    df49_.columns.values[-1] = "TEXTO"

    df = pd.concat([df0_, df1_, df2_, df3_, df4_, df5_, df6_, df7_, df8_, df9_,
                    df10_, df11_, df12_, df13_, df14_, df15_, df16_, df17_, df18_, df19_,
                    df20_, df21_, df22_, df23_, df24_, df25_, df26_, df27_, df28_, df29_,
                    df30_, df31_, df32_, df33_, df34_, df35_, df36_, df37_, df38_, df39_,
                    df40_, df41_, df42_, df43_, df44_, df45_, df46_, df47_, df48_, df49_], axis=0).reset_index()

    df['TIME'] = [datetime.fromtimestamp(x) for x in df['taken_at_timestamp']]
    df['HORA'] = pd.to_datetime(df['TIME']).dt.hour
    df['DIA'] = pd.to_datetime(df['TIME']).dt.date
    df['DIA'] = df['DIA'].apply(lambda x: x.strftime('%Y-%m-%d'))
    df['SEMANA'] = pd.to_datetime(df['TIME']).apply(lambda x: x.weekday())

    conditions_semana = [(df['SEMANA'] == 0), (df['SEMANA'] == 1), (df['SEMANA'] == 2),
                         (df['SEMANA'] == 3), (df['SEMANA'] == 4), (df['SEMANA'] == 5), (df['SEMANA'] == 6)]

    df['SEMANA'] = np.select(conditions_semana,
                             ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo'])

    conditions = [(df['HORA'] >= 6) & (df['HORA'] <= 12),
                  (df['HORA'] >= 12) & (df['HORA'] <= 18),
                  (df['HORA'] >= 18) & (df['HORA'] <= 24),
                  (df['HORA'] >= 0) & (df['HORA'] <= 6)]
    values = ['Manhã', 'Tarde', 'Noite', 'Madrugada']
    df['TURNO'] = np.select(conditions, values)
    df['UNIDADE'] = np.where(df['LIKES'] == 2, 0, 1)
    df['shortcode'] = 'https://www.instagram.com/p/'+df['shortcode']

    df['COMENTARIOS'] = pd.to_numeric(df['COMENTARIOS'], errors='coerce').astype('Int64')
    df['LIKES'] = pd.to_numeric(df['LIKES'], errors='coerce').astype('Int64')
    df['HORA'] = pd.to_numeric(df['HORA'], errors='coerce').astype('Int64')

    df['INTERAÇÕES'] = df['LIKES'] + df['COMENTARIOS']

    df['% COMENTOU'] = df.apply(lambda row: round(row['COMENTARIOS']*100 / row['LIKES'], 2), axis=1)
    df['%VAR INTERAÇÕES'] = round((df['INTERAÇÕES'] - df['INTERAÇÕES'].shift(-1)) / df['INTERAÇÕES'].shift(-1) * 100, 2)
    df['VARIAÇÃO INTERAÇÕES'] = round((df['INTERAÇÕES'] - df['INTERAÇÕES'].shift(-1)), 2)

    df['UNIDADE'] = np.where(df['TIME'] == 2, 0, 1)

    df['__typename'].replace('GraphSidecar', 'Coleção', inplace=True)
    df['__typename'].replace('GraphImage', 'Imagem', inplace=True)
    df['__typename'].replace('GraphVideo', 'Vídeo', inplace=True)
    df = df[['TIME', '__typename', 'TEXTO', 'LIKES', 'COMENTARIOS', '% COMENTOU',
             'INTERAÇÕES', 'VARIAÇÃO INTERAÇÕES', '%VAR INTERAÇÕES',
             'shortcode', 'SEMANA', 'TURNO', 'HORA', 'DIA', 'id', 'UNIDADE']]

    df = df.rename(columns={'__typename': 'TIPO POST', 'shortcode': 'LINK', 'id': 'ID POST', 'TEXTO':'LEGENDA'})

    return df


#####################################################################################################################################
####################################################################################################################################

@st.cache_data
def convert_midias1(res, df_zero):
    df0 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][0]['node']
    df1 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][1]['node']
    df2 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][2]['node']
    df3 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][3]['node']
    df4 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][4]['node']
    df5 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][5]['node']
    df6 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][6]['node']
    df7 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][7]['node']
    df8 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][8]['node']
    df9 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][9]['node']
    df10 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][10]['node']
    df11 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][11]['node']
    df12 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][12]['node']
    df13 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][13]['node']
    df14 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][14]['node']
    df15 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][15]['node']
    df16 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][16]['node']
    df17 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][17]['node']
    df18 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][18]['node']
    df19 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][19]['node']
    df20 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][20]['node']
    df21 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][21]['node']
    df22 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][22]['node']
    df23 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][23]['node']
    df24 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][24]['node']
    df25 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][25]['node']
    df26 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][26]['node']
    df27 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][27]['node']
    df28 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][28]['node']
    df29 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][29]['node']
    df30 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][30]['node']
    df31 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][31]['node']
    df32 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][32]['node']
    df33 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][33]['node']
    df34 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][34]['node']
    df35 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][35]['node']
    df36 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][36]['node']
    df37 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][37]['node']
    df38 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][38]['node']
    df39 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][39]['node']
    df40 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][40]['node']
    df41 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][41]['node']
    df42 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][42]['node']
    df43 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][43]['node']
    df44 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][44]['node']
    df45 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][45]['node']
    df46 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][46]['node']
    df47 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][47]['node']
    df48 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][48]['node']
    df49 = res["data"]["user"]["edge_owner_to_timeline_media"]['edges'][49]['node']

    df0_1 = df0["edge_media_to_comment"]['count'];
    df0_1 = pd.DataFrame([df0_1])
    df0_2 = df0["edge_media_preview_like"]['count'];
    df0_2 = pd.DataFrame([df0_2])
    df0_3 = df0["edge_media_to_caption"]['edges'][0]['node']['text'];
    df0_3 = pd.DataFrame([df0_3])

    df1_1 = df1["edge_media_to_comment"]['count'];
    df1_1 = pd.DataFrame([df1_1])
    df1_2 = df1["edge_media_preview_like"]['count'];
    df1_2 = pd.DataFrame([df1_2])
    df1_3 = df1["edge_media_to_caption"]['edges'][0]['node']['text'];
    df1_3 = pd.DataFrame([df1_3])

    df2_1 = df2["edge_media_to_comment"]['count'];
    df2_1 = pd.DataFrame([df2_1])
    df2_2 = df2["edge_media_preview_like"]['count'];
    df2_2 = pd.DataFrame([df2_2])
    df2_3 = df2["edge_media_to_caption"]['edges'][0]['node']['text'];
    df2_3 = pd.DataFrame([df2_3])

    df3_1 = df3["edge_media_to_comment"]['count'];
    df3_1 = pd.DataFrame([df3_1])
    df3_2 = df3["edge_media_preview_like"]['count'];
    df3_2 = pd.DataFrame([df3_2])
    df3_3 = df3["edge_media_to_caption"]['edges'][0]['node']['text'];
    df3_3 = pd.DataFrame([df3_3])

    df4_1 = df4["edge_media_to_comment"]['count'];
    df4_1 = pd.DataFrame([df4_1])
    df4_2 = df4["edge_media_preview_like"]['count'];
    df4_2 = pd.DataFrame([df4_2])
    df4_3 = df4["edge_media_to_caption"]['edges'][0]['node']['text'];
    df4_3 = pd.DataFrame([df4_3])

    df5_1 = df5["edge_media_to_comment"]['count'];
    df5_1 = pd.DataFrame([df5_1])
    df5_2 = df5["edge_media_preview_like"]['count'];
    df5_2 = pd.DataFrame([df5_2])
    df5_3 = df5["edge_media_to_caption"]['edges'][0]['node']['text'];
    df5_3 = pd.DataFrame([df5_3])

    df6_1 = df6["edge_media_to_comment"]['count'];
    df6_1 = pd.DataFrame([df6_1])
    df6_2 = df6["edge_media_preview_like"]['count'];
    df6_2 = pd.DataFrame([df6_2])
    df6_3 = df6["edge_media_to_caption"]['edges'][0]['node']['text'];
    df6_3 = pd.DataFrame([df6_3])

    df7_1 = df7["edge_media_to_comment"]['count'];
    df7_1 = pd.DataFrame([df7_1])
    df7_2 = df7["edge_media_preview_like"]['count'];
    df7_2 = pd.DataFrame([df7_2])
    df7_3 = df7["edge_media_to_caption"]['edges'][0]['node']['text'];
    df7_3 = pd.DataFrame([df7_3])

    df8_1 = df8["edge_media_to_comment"]['count'];
    df8_1 = pd.DataFrame([df8_1])
    df8_2 = df8["edge_media_preview_like"]['count'];
    df8_2 = pd.DataFrame([df8_2])
    df8_3 = df8["edge_media_to_caption"]['edges'][0]['node']['text'];
    df8_3 = pd.DataFrame([df8_3])

    df9_1 = df9["edge_media_to_comment"]['count'];
    df9_1 = pd.DataFrame([df9_1])
    df9_2 = df9["edge_media_preview_like"]['count'];
    df9_2 = pd.DataFrame([df9_2])
    df9_3 = df9["edge_media_to_caption"]['edges'][0]['node']['text'];
    df9_3 = pd.DataFrame([df9_3])

    df10_1 = df10["edge_media_to_comment"]['count'];
    df10_1 = pd.DataFrame([df10_1])
    df10_2 = df10["edge_media_preview_like"]['count'];
    df10_2 = pd.DataFrame([df10_2])
    df10_3 = df10["edge_media_to_caption"]['edges'][0]['node']['text'];
    df10_3 = pd.DataFrame([df10_3])

    df11_1 = df11["edge_media_to_comment"]['count'];
    df11_1 = pd.DataFrame([df11_1])
    df11_2 = df11["edge_media_preview_like"]['count'];
    df11_2 = pd.DataFrame([df11_2])
    df11_3 = df11["edge_media_to_caption"]['edges'][0]['node']['text'];
    df11_3 = pd.DataFrame([df11_3])

    df12_1 = df12["edge_media_to_comment"]['count'];
    df12_1 = pd.DataFrame([df12_1])
    df12_2 = df12["edge_media_preview_like"]['count'];
    df12_2 = pd.DataFrame([df12_2])
    df12_3 = df12["edge_media_to_caption"]['edges'][0]['node']['text'];
    df12_3 = pd.DataFrame([df12_3])

    df13_1 = df13["edge_media_to_comment"]['count'];
    df13_1 = pd.DataFrame([df13_1])
    df13_2 = df13["edge_media_preview_like"]['count'];
    df13_2 = pd.DataFrame([df13_2])
    df13_3 = df13["edge_media_to_caption"]['edges'][0]['node']['text'];
    df13_3 = pd.DataFrame([df13_3])

    df14_1 = df14["edge_media_to_comment"]['count'];
    df14_1 = pd.DataFrame([df14_1])
    df14_2 = df14["edge_media_preview_like"]['count'];
    df14_2 = pd.DataFrame([df14_2])
    df14_3 = df14["edge_media_to_caption"]['edges'][0]['node']['text'];
    df14_3 = pd.DataFrame([df14_3])

    df15_1 = df15["edge_media_to_comment"]['count'];
    df15_1 = pd.DataFrame([df15_1])
    df15_2 = df15["edge_media_preview_like"]['count'];
    df15_2 = pd.DataFrame([df15_2])
    df15_3 = df15["edge_media_to_caption"]['edges'][0]['node']['text'];
    df15_3 = pd.DataFrame([df15_3])

    df16_1 = df16["edge_media_to_comment"]['count'];
    df16_1 = pd.DataFrame([df16_1])
    df16_2 = df16["edge_media_preview_like"]['count'];
    df16_2 = pd.DataFrame([df16_2])
    df16_3 = df16["edge_media_to_caption"]['edges'][0]['node']['text'];
    df16_3 = pd.DataFrame([df16_3])

    df17_1 = df17["edge_media_to_comment"]['count'];
    df17_1 = pd.DataFrame([df17_1])
    df17_2 = df17["edge_media_preview_like"]['count'];
    df17_2 = pd.DataFrame([df17_2])
    df17_3 = df17["edge_media_to_caption"]['edges'][0]['node']['text'];
    df17_3 = pd.DataFrame([df17_3])

    df18_1 = df18["edge_media_to_comment"]['count'];
    df18_1 = pd.DataFrame([df18_1])
    df18_2 = df18["edge_media_preview_like"]['count'];
    df18_2 = pd.DataFrame([df18_2])
    df18_3 = df18["edge_media_to_caption"]['edges'][0]['node']['text'];
    df18_3 = pd.DataFrame([df18_3])

    df19_1 = df19["edge_media_to_comment"]['count'];
    df19_1 = pd.DataFrame([df19_1])
    df19_2 = df19["edge_media_preview_like"]['count'];
    df19_2 = pd.DataFrame([df19_2])
    df19_3 = df19["edge_media_to_caption"]['edges'][0]['node']['text'];
    df19_3 = pd.DataFrame([df19_3])

    df20_1 = df20["edge_media_to_comment"]['count'];
    df20_1 = pd.DataFrame([df20_1])
    df20_2 = df20["edge_media_preview_like"]['count'];
    df20_2 = pd.DataFrame([df20_2])
    df20_3 = df20["edge_media_to_caption"]['edges'][0]['node']['text'];
    df20_3 = pd.DataFrame([df20_3])

    df21_1 = df21["edge_media_to_comment"]['count'];
    df21_1 = pd.DataFrame([df21_1])
    df21_2 = df21["edge_media_preview_like"]['count'];
    df21_2 = pd.DataFrame([df21_2])
    df21_3 = df21["edge_media_to_caption"]['edges'][0]['node']['text'];
    df21_3 = pd.DataFrame([df21_3])

    df22_1 = df22["edge_media_to_comment"]['count'];
    df22_1 = pd.DataFrame([df22_1])
    df22_2 = df22["edge_media_preview_like"]['count'];
    df22_2 = pd.DataFrame([df22_2])
    df22_3 = df22["edge_media_to_caption"]['edges'][0]['node']['text'];
    df22_3 = pd.DataFrame([df22_3])

    df23_1 = df23["edge_media_to_comment"]['count'];
    df23_1 = pd.DataFrame([df23_1])
    df23_2 = df23["edge_media_preview_like"]['count'];
    df23_2 = pd.DataFrame([df23_2])
    df23_3 = df23["edge_media_to_caption"]['edges'][0]['node']['text'];
    df23_3 = pd.DataFrame([df23_3])

    df24_1 = df24["edge_media_to_comment"]['count'];
    df24_1 = pd.DataFrame([df24_1])
    df24_2 = df24["edge_media_preview_like"]['count'];
    df24_2 = pd.DataFrame([df24_2])
    df24_3 = df24["edge_media_to_caption"]['edges'][0]['node']['text'];
    df24_3 = pd.DataFrame([df24_3])

    df25_1 = df25["edge_media_to_comment"]['count'];
    df25_1 = pd.DataFrame([df25_1])
    df25_2 = df25["edge_media_preview_like"]['count'];
    df25_2 = pd.DataFrame([df25_2])
    df25_3 = df25["edge_media_to_caption"]['edges'][0]['node']['text'];
    df25_3 = pd.DataFrame([df25_3])

    df26_1 = df26["edge_media_to_comment"]['count'];
    df26_1 = pd.DataFrame([df26_1])
    df26_2 = df26["edge_media_preview_like"]['count'];
    df26_2 = pd.DataFrame([df26_2])
    df26_3 = df26["edge_media_to_caption"]['edges'][0]['node']['text'];
    df26_3 = pd.DataFrame([df26_3])

    df27_1 = df27["edge_media_to_comment"]['count'];
    df27_1 = pd.DataFrame([df27_1])
    df27_2 = df27["edge_media_preview_like"]['count'];
    df27_2 = pd.DataFrame([df27_2])
    df27_3 = df27["edge_media_to_caption"]['edges'][0]['node']['text'];
    df27_3 = pd.DataFrame([df27_3])

    df28_1 = df28["edge_media_to_comment"]['count'];
    df28_1 = pd.DataFrame([df28_1])
    df28_2 = df28["edge_media_preview_like"]['count'];
    df28_2 = pd.DataFrame([df28_2])
    df28_3 = df28["edge_media_to_caption"]['edges'][0]['node']['text'];
    df28_3 = pd.DataFrame([df28_3])

    df29_1 = df29["edge_media_to_comment"]['count'];
    df29_1 = pd.DataFrame([df29_1])
    df29_2 = df29["edge_media_preview_like"]['count'];
    df29_2 = pd.DataFrame([df29_2])
    df29_3 = df29["edge_media_to_caption"]['edges'][0]['node']['text'];
    df29_3 = pd.DataFrame([df29_3])

    df30_1 = df30["edge_media_to_comment"]['count'];
    df30_1 = pd.DataFrame([df30_1])
    df30_2 = df30["edge_media_preview_like"]['count'];
    df30_2 = pd.DataFrame([df30_2])
    df30_3 = df30["edge_media_to_caption"]['edges'][0]['node']['text'];
    df30_3 = pd.DataFrame([df30_3])

    df31_1 = df31["edge_media_to_comment"]['count'];
    df31_1 = pd.DataFrame([df31_1])
    df31_2 = df31["edge_media_preview_like"]['count'];
    df31_2 = pd.DataFrame([df31_2])
    df31_3 = df31["edge_media_to_caption"]['edges'][0]['node']['text'];
    df31_3 = pd.DataFrame([df31_3])

    df32_1 = df32["edge_media_to_comment"]['count'];
    df32_1 = pd.DataFrame([df32_1])
    df32_2 = df32["edge_media_preview_like"]['count'];
    df32_2 = pd.DataFrame([df32_2])
    df32_3 = df32["edge_media_to_caption"]['edges'][0]['node']['text'];
    df32_3 = pd.DataFrame([df32_3])

    df33_1 = df33["edge_media_to_comment"]['count'];
    df33_1 = pd.DataFrame([df33_1])
    df33_2 = df33["edge_media_preview_like"]['count'];
    df33_2 = pd.DataFrame([df33_2])
    df33_3 = df33["edge_media_to_caption"]['edges'][0]['node']['text'];
    df33_3 = pd.DataFrame([df33_3])

    df34_1 = df34["edge_media_to_comment"]['count'];
    df34_1 = pd.DataFrame([df34_1])
    df34_2 = df34["edge_media_preview_like"]['count'];
    df34_2 = pd.DataFrame([df34_2])
    df34_3 = df34["edge_media_to_caption"]['edges'][0]['node']['text'];
    df34_3 = pd.DataFrame([df34_3])

    df35_1 = df35["edge_media_to_comment"]['count'];
    df35_1 = pd.DataFrame([df35_1])
    df35_2 = df35["edge_media_preview_like"]['count'];
    df35_2 = pd.DataFrame([df35_2])
    df35_3 = df35["edge_media_to_caption"]['edges'][0]['node']['text'];
    df35_3 = pd.DataFrame([df35_3])

    df36_1 = df36["edge_media_to_comment"]['count'];
    df36_1 = pd.DataFrame([df36_1])
    df36_2 = df36["edge_media_preview_like"]['count'];
    df36_2 = pd.DataFrame([df36_2])
    df36_3 = df36["edge_media_to_caption"]['edges'][0]['node']['text'];
    df36_3 = pd.DataFrame([df36_3])

    df37_1 = df37["edge_media_to_comment"]['count'];
    df37_1 = pd.DataFrame([df37_1])
    df37_2 = df37["edge_media_preview_like"]['count'];
    df37_2 = pd.DataFrame([df37_2])
    df37_3 = df37["edge_media_to_caption"]['edges'][0]['node']['text'];
    df37_3 = pd.DataFrame([df37_3])

    df38_1 = df38["edge_media_to_comment"]['count'];
    df38_1 = pd.DataFrame([df38_1])
    df38_2 = df38["edge_media_preview_like"]['count'];
    df38_2 = pd.DataFrame([df38_2])
    df38_3 = df38["edge_media_to_caption"]['edges'][0]['node']['text'];
    df38_3 = pd.DataFrame([df38_3])

    df39_1 = df39["edge_media_to_comment"]['count'];
    df39_1 = pd.DataFrame([df39_1])
    df39_2 = df39["edge_media_preview_like"]['count'];
    df39_2 = pd.DataFrame([df39_2])
    df39_3 = df39["edge_media_to_caption"]['edges'][0]['node']['text'];
    df39_3 = pd.DataFrame([df39_3])

    df40_1 = df40["edge_media_to_comment"]['count'];
    df40_1 = pd.DataFrame([df40_1])
    df40_2 = df40["edge_media_preview_like"]['count'];
    df40_2 = pd.DataFrame([df40_2])
    df40_3 = df40["edge_media_to_caption"]['edges'][0]['node']['text'];
    df40_3 = pd.DataFrame([df40_3])

    df41_1 = df41["edge_media_to_comment"]['count'];
    df41_1 = pd.DataFrame([df41_1])
    df41_2 = df41["edge_media_preview_like"]['count'];
    df41_2 = pd.DataFrame([df41_2])
    df41_3 = df41["edge_media_to_caption"]['edges'][0]['node']['text'];
    df41_3 = pd.DataFrame([df41_3])

    df42_1 = df42["edge_media_to_comment"]['count'];
    df42_1 = pd.DataFrame([df42_1])
    df42_2 = df42["edge_media_preview_like"]['count'];
    df42_2 = pd.DataFrame([df42_2])
    df42_3 = df42["edge_media_to_caption"]['edges'][0]['node']['text'];
    df42_3 = pd.DataFrame([df42_3])

    df43_1 = df43["edge_media_to_comment"]['count'];
    df43_1 = pd.DataFrame([df43_1])
    df43_2 = df43["edge_media_preview_like"]['count'];
    df43_2 = pd.DataFrame([df43_2])
    df43_3 = df43["edge_media_to_caption"]['edges'][0]['node']['text'];
    df43_3 = pd.DataFrame([df43_3])

    df44_1 = df44["edge_media_to_comment"]['count'];
    df44_1 = pd.DataFrame([df44_1])
    df44_2 = df44["edge_media_preview_like"]['count'];
    df44_2 = pd.DataFrame([df44_2])
    df44_3 = df44["edge_media_to_caption"]['edges'][0]['node']['text'];
    df44_3 = pd.DataFrame([df44_3])

    df45_1 = df45["edge_media_to_comment"]['count'];
    df45_1 = pd.DataFrame([df45_1])
    df45_2 = df45["edge_media_preview_like"]['count'];
    df45_2 = pd.DataFrame([df45_2])
    df45_3 = df45["edge_media_to_caption"]['edges'][0]['node']['text'];
    df45_3 = pd.DataFrame([df45_3])

    df46_1 = df46["edge_media_to_comment"]['count'];
    df46_1 = pd.DataFrame([df46_1])
    df46_2 = df46["edge_media_preview_like"]['count'];
    df46_2 = pd.DataFrame([df46_2])
    df46_3 = df46["edge_media_to_caption"]['edges'][0]['node']['text'];
    df46_3 = pd.DataFrame([df46_3])

    df47_1 = df47["edge_media_to_comment"]['count'];
    df47_1 = pd.DataFrame([df47_1])
    df47_2 = df47["edge_media_preview_like"]['count'];
    df47_2 = pd.DataFrame([df47_2])
    df47_3 = df47["edge_media_to_caption"]['edges'][0]['node']['text'];
    df47_3 = pd.DataFrame([df47_3])

    df48_1 = df48["edge_media_to_comment"]['count'];
    df48_1 = pd.DataFrame([df48_1])
    df48_2 = df48["edge_media_preview_like"]['count'];
    df48_2 = pd.DataFrame([df48_2])
    df48_3 = df48["edge_media_to_caption"]['edges'][0]['node']['text'];
    df48_3 = pd.DataFrame([df48_3])

    df49_1 = df49["edge_media_to_comment"]['count'];
    df49_1 = pd.DataFrame([df49_1])
    df49_2 = df49["edge_media_preview_like"]['count'];
    df49_2 = pd.DataFrame([df49_2])
    df49_3 = df49["edge_media_to_caption"]['edges'][0]['node']['text'];
    df49_3 = pd.DataFrame([df49_3])

    df0 = pd.DataFrame([df0])
    df1 = pd.DataFrame([df1])
    df2 = pd.DataFrame([df2])
    df3 = pd.DataFrame([df3])
    df4 = pd.DataFrame([df4])
    df5 = pd.DataFrame([df5])
    df6 = pd.DataFrame([df6])
    df7 = pd.DataFrame([df7])
    df8 = pd.DataFrame([df8])
    df9 = pd.DataFrame([df9])

    df10 = pd.DataFrame([df10])
    df11 = pd.DataFrame([df11])
    df12 = pd.DataFrame([df12])
    df13 = pd.DataFrame([df13])
    df14 = pd.DataFrame([df14])
    df15 = pd.DataFrame([df15])
    df16 = pd.DataFrame([df16])
    df17 = pd.DataFrame([df17])
    df18 = pd.DataFrame([df18])
    df19 = pd.DataFrame([df19])
    df20 = pd.DataFrame([df20])

    df21 = pd.DataFrame([df21])
    df22 = pd.DataFrame([df22])
    df23 = pd.DataFrame([df23])
    df24 = pd.DataFrame([df24])
    df25 = pd.DataFrame([df25])
    df26 = pd.DataFrame([df26])
    df27 = pd.DataFrame([df27])
    df28 = pd.DataFrame([df28])
    df29 = pd.DataFrame([df29])

    df30 = pd.DataFrame([df30])
    df31 = pd.DataFrame([df31])
    df32 = pd.DataFrame([df32])
    df33 = pd.DataFrame([df33])
    df34 = pd.DataFrame([df34])
    df35 = pd.DataFrame([df35])
    df36 = pd.DataFrame([df36])
    df37 = pd.DataFrame([df37])
    df38 = pd.DataFrame([df38])
    df39 = pd.DataFrame([df39])

    df40 = pd.DataFrame([df40])
    df41 = pd.DataFrame([df41])
    df42 = pd.DataFrame([df42])
    df43 = pd.DataFrame([df43])
    df44 = pd.DataFrame([df44])
    df45 = pd.DataFrame([df45])
    df46 = pd.DataFrame([df46])
    df47 = pd.DataFrame([df47])
    df48 = pd.DataFrame([df48])
    df49 = pd.DataFrame([df49])

    df0_ = pd.concat([df0, df0_1, df0_2, df0_3], axis=1)
    df1_ = pd.concat([df1, df1_1, df1_2, df1_3], axis=1)
    df2_ = pd.concat([df2, df2_1, df2_2, df2_3], axis=1)
    df3_ = pd.concat([df3, df3_1, df3_2, df3_3], axis=1)
    df4_ = pd.concat([df4, df4_1, df4_2, df4_3], axis=1)
    df5_ = pd.concat([df5, df5_1, df5_2, df5_3], axis=1)
    df6_ = pd.concat([df6, df6_1, df6_2, df6_3], axis=1)
    df7_ = pd.concat([df7, df7_1, df7_2, df7_3], axis=1)
    df8_ = pd.concat([df8, df8_1, df8_2, df8_3], axis=1)
    df9_ = pd.concat([df9, df9_1, df9_2, df9_3], axis=1)

    df10_ = pd.concat([df10, df10_1, df10_2, df10_3], axis=1)
    df11_ = pd.concat([df11, df11_1, df11_2, df11_3], axis=1)
    df12_ = pd.concat([df12, df12_1, df12_2, df12_3], axis=1)
    df13_ = pd.concat([df13, df13_1, df13_2, df13_3], axis=1)
    df14_ = pd.concat([df14, df14_1, df14_2, df14_3], axis=1)
    df15_ = pd.concat([df15, df15_1, df15_2, df15_3], axis=1)
    df16_ = pd.concat([df16, df16_1, df16_2, df16_3], axis=1)
    df17_ = pd.concat([df17, df17_1, df17_2, df17_3], axis=1)
    df18_ = pd.concat([df18, df18_1, df18_2, df18_3], axis=1)
    df19_ = pd.concat([df19, df19_1, df19_2, df19_3], axis=1)

    df20_ = pd.concat([df20, df20_1, df20_2, df20_3], axis=1)
    df21_ = pd.concat([df21, df21_1, df21_2, df21_3], axis=1)
    df22_ = pd.concat([df22, df22_1, df22_2, df22_3], axis=1)
    df23_ = pd.concat([df23, df23_1, df23_2, df23_3], axis=1)
    df24_ = pd.concat([df24, df24_1, df24_2, df24_3], axis=1)
    df25_ = pd.concat([df25, df25_1, df25_2, df25_3], axis=1)
    df26_ = pd.concat([df26, df26_1, df26_2, df26_3], axis=1)
    df27_ = pd.concat([df27, df27_1, df27_2, df27_3], axis=1)
    df28_ = pd.concat([df28, df28_1, df28_2, df28_3], axis=1)
    df29_ = pd.concat([df29, df29_1, df29_2, df29_3], axis=1)

    df30_ = pd.concat([df30, df30_1, df30_2, df30_3], axis=1)
    df31_ = pd.concat([df31, df31_1, df31_2, df31_3], axis=1)
    df32_ = pd.concat([df32, df32_1, df32_2, df32_3], axis=1)
    df33_ = pd.concat([df33, df33_1, df33_2, df33_3], axis=1)
    df34_ = pd.concat([df34, df34_1, df34_2, df34_3], axis=1)
    df35_ = pd.concat([df35, df35_1, df35_2, df35_3], axis=1)
    df36_ = pd.concat([df36, df36_1, df36_2, df36_3], axis=1)
    df37_ = pd.concat([df37, df37_1, df37_2, df37_3], axis=1)
    df38_ = pd.concat([df38, df38_1, df38_2, df38_3], axis=1)
    df39_ = pd.concat([df39, df39_1, df39_2, df39_3], axis=1)

    df40_ = pd.concat([df40, df40_1, df40_2, df40_3], axis=1)
    df41_ = pd.concat([df41, df41_1, df41_2, df41_3], axis=1)
    df42_ = pd.concat([df42, df42_1, df42_2, df42_3], axis=1)
    df43_ = pd.concat([df43, df43_1, df43_2, df43_3], axis=1)
    df44_ = pd.concat([df44, df44_1, df44_2, df44_3], axis=1)
    df45_ = pd.concat([df45, df45_1, df45_2, df45_3], axis=1)
    df46_ = pd.concat([df46, df46_1, df46_2, df46_3], axis=1)
    df47_ = pd.concat([df47, df47_1, df47_2, df47_3], axis=1)
    df48_ = pd.concat([df48, df48_1, df48_2, df48_3], axis=1)
    df49_ = pd.concat([df49, df49_1, df49_2, df49_3], axis=1)

    df0_.columns.values[-3] = "COMENTARIOS"
    df0_.columns.values[-2] = "LIKES"
    df0_.columns.values[-1] = "TEXTO"

    df1_.columns.values[-3] = "COMENTARIOS"
    df1_.columns.values[-2] = "LIKES"
    df1_.columns.values[-1] = "TEXTO"

    df2_.columns.values[-3] = "COMENTARIOS"
    df2_.columns.values[-2] = "LIKES"
    df2_.columns.values[-1] = "TEXTO"

    df3_.columns.values[-3] = "COMENTARIOS"
    df3_.columns.values[-2] = "LIKES"
    df3_.columns.values[-1] = "TEXTO"

    df4_.columns.values[-3] = "COMENTARIOS"
    df4_.columns.values[-2] = "LIKES"
    df4_.columns.values[-1] = "TEXTO"

    df5_.columns.values[-3] = "COMENTARIOS"
    df5_.columns.values[-2] = "LIKES"
    df5_.columns.values[-1] = "TEXTO"

    df6_.columns.values[-3] = "COMENTARIOS"
    df6_.columns.values[-2] = "LIKES"
    df6_.columns.values[-1] = "TEXTO"

    df7_.columns.values[-3] = "COMENTARIOS"
    df7_.columns.values[-2] = "LIKES"
    df7_.columns.values[-1] = "TEXTO"

    df8_.columns.values[-3] = "COMENTARIOS"
    df8_.columns.values[-2] = "LIKES"
    df8_.columns.values[-1] = "TEXTO"

    df9_.columns.values[-3] = "COMENTARIOS"
    df9_.columns.values[-2] = "LIKES"
    df9_.columns.values[-1] = "TEXTO"

    df10_.columns.values[-3] = "COMENTARIOS"
    df10_.columns.values[-2] = "LIKES"
    df10_.columns.values[-1] = "TEXTO"

    df11_.columns.values[-3] = "COMENTARIOS"
    df11_.columns.values[-2] = "LIKES"
    df11_.columns.values[-1] = "TEXTO"

    df12_.columns.values[-3] = "COMENTARIOS"
    df12_.columns.values[-2] = "LIKES"
    df12_.columns.values[-1] = "TEXTO"

    df13_.columns.values[-3] = "COMENTARIOS"
    df13_.columns.values[-2] = "LIKES"
    df13_.columns.values[-1] = "TEXTO"

    df14_.columns.values[-3] = "COMENTARIOS"
    df14_.columns.values[-2] = "LIKES"
    df14_.columns.values[-1] = "TEXTO"

    df15_.columns.values[-3] = "COMENTARIOS"
    df15_.columns.values[-2] = "LIKES"
    df15_.columns.values[-1] = "TEXTO"

    df16_.columns.values[-3] = "COMENTARIOS"
    df16_.columns.values[-2] = "LIKES"
    df16_.columns.values[-1] = "TEXTO"

    df17_.columns.values[-3] = "COMENTARIOS"
    df17_.columns.values[-2] = "LIKES"
    df17_.columns.values[-1] = "TEXTO"

    df18_.columns.values[-3] = "COMENTARIOS"
    df18_.columns.values[-2] = "LIKES"
    df18_.columns.values[-1] = "TEXTO"

    df19_.columns.values[-3] = "COMENTARIOS"
    df19_.columns.values[-2] = "LIKES"
    df19_.columns.values[-1] = "TEXTO"

    df20_.columns.values[-3] = "COMENTARIOS"
    df20_.columns.values[-2] = "LIKES"
    df20_.columns.values[-1] = "TEXTO"

    df21_.columns.values[-3] = "COMENTARIOS"
    df21_.columns.values[-2] = "LIKES"
    df21_.columns.values[-1] = "TEXTO"

    df22_.columns.values[-3] = "COMENTARIOS"
    df22_.columns.values[-2] = "LIKES"
    df22_.columns.values[-1] = "TEXTO"

    df23_.columns.values[-3] = "COMENTARIOS"
    df23_.columns.values[-2] = "LIKES"
    df23_.columns.values[-1] = "TEXTO"

    df24_.columns.values[-3] = "COMENTARIOS"
    df24_.columns.values[-2] = "LIKES"
    df24_.columns.values[-1] = "TEXTO"

    df25_.columns.values[-3] = "COMENTARIOS"
    df25_.columns.values[-2] = "LIKES"
    df25_.columns.values[-1] = "TEXTO"

    df26_.columns.values[-3] = "COMENTARIOS"
    df26_.columns.values[-2] = "LIKES"
    df26_.columns.values[-1] = "TEXTO"

    df27_.columns.values[-3] = "COMENTARIOS"
    df27_.columns.values[-2] = "LIKES"
    df27_.columns.values[-1] = "TEXTO"

    df28_.columns.values[-3] = "COMENTARIOS"
    df28_.columns.values[-2] = "LIKES"
    df28_.columns.values[-1] = "TEXTO"

    df29_.columns.values[-3] = "COMENTARIOS"
    df29_.columns.values[-2] = "LIKES"
    df29_.columns.values[-1] = "TEXTO"

    df30_.columns.values[-3] = "COMENTARIOS"
    df30_.columns.values[-2] = "LIKES"
    df30_.columns.values[-1] = "TEXTO"

    df31_.columns.values[-3] = "COMENTARIOS"
    df31_.columns.values[-2] = "LIKES"
    df31_.columns.values[-1] = "TEXTO"

    df32_.columns.values[-3] = "COMENTARIOS"
    df32_.columns.values[-2] = "LIKES"
    df32_.columns.values[-1] = "TEXTO"

    df33_.columns.values[-3] = "COMENTARIOS"
    df33_.columns.values[-2] = "LIKES"
    df33_.columns.values[-1] = "TEXTO"

    df34_.columns.values[-3] = "COMENTARIOS"
    df34_.columns.values[-2] = "LIKES"
    df34_.columns.values[-1] = "TEXTO"

    df35_.columns.values[-3] = "COMENTARIOS"
    df35_.columns.values[-2] = "LIKES"
    df35_.columns.values[-1] = "TEXTO"

    df36_.columns.values[-3] = "COMENTARIOS"
    df36_.columns.values[-2] = "LIKES"
    df36_.columns.values[-1] = "TEXTO"

    df37_.columns.values[-3] = "COMENTARIOS"
    df37_.columns.values[-2] = "LIKES"
    df37_.columns.values[-1] = "TEXTO"

    df38_.columns.values[-3] = "COMENTARIOS"
    df38_.columns.values[-2] = "LIKES"
    df38_.columns.values[-1] = "TEXTO"

    df39_.columns.values[-3] = "COMENTARIOS"
    df39_.columns.values[-2] = "LIKES"
    df39_.columns.values[-1] = "TEXTO"

    df40_.columns.values[-3] = "COMENTARIOS"
    df40_.columns.values[-2] = "LIKES"
    df40_.columns.values[-1] = "TEXTO"

    df41_.columns.values[-3] = "COMENTARIOS"
    df41_.columns.values[-2] = "LIKES"
    df41_.columns.values[-1] = "TEXTO"

    df42_.columns.values[-3] = "COMENTARIOS"
    df42_.columns.values[-2] = "LIKES"
    df42_.columns.values[-1] = "TEXTO"

    df43_.columns.values[-3] = "COMENTARIOS"
    df43_.columns.values[-2] = "LIKES"
    df43_.columns.values[-1] = "TEXTO"

    df44_.columns.values[-3] = "COMENTARIOS"
    df44_.columns.values[-2] = "LIKES"
    df44_.columns.values[-1] = "TEXTO"

    df45_.columns.values[-3] = "COMENTARIOS"
    df45_.columns.values[-2] = "LIKES"
    df45_.columns.values[-1] = "TEXTO"

    df46_.columns.values[-3] = "COMENTARIOS"
    df46_.columns.values[-2] = "LIKES"
    df46_.columns.values[-1] = "TEXTO"

    df47_.columns.values[-3] = "COMENTARIOS"
    df47_.columns.values[-2] = "LIKES"
    df47_.columns.values[-1] = "TEXTO"

    df48_.columns.values[-3] = "COMENTARIOS"
    df48_.columns.values[-2] = "LIKES"
    df48_.columns.values[-1] = "TEXTO"

    df49_.columns.values[-3] = "COMENTARIOS"
    df49_.columns.values[-2] = "LIKES"
    df49_.columns.values[-1] = "TEXTO"

    df = pd.concat([df0_, df1_, df2_, df3_, df4_, df5_, df6_, df7_, df8_, df9_,
                    df10_, df11_, df12_, df13_, df14_, df15_, df16_, df17_, df18_, df19_,
                    df20_, df21_, df22_, df23_, df24_, df25_, df26_, df27_, df28_, df29_,
                    df30_, df31_, df32_, df33_, df34_, df35_, df36_, df37_, df38_, df39_,
                    df40_, df41_, df42_, df43_, df44_, df45_, df46_, df47_, df48_, df49_], axis=0)

    df['TIME'] = [datetime.fromtimestamp(x) for x in df['taken_at_timestamp']]
    df['HORA'] = pd.to_datetime(df['TIME']).dt.hour
    df['DIA'] = pd.to_datetime(df['TIME']).dt.date
    df['DIA'] = df['DIA'].apply(lambda x: x.strftime('%Y-%m-%d'))
    df['SEMANA'] = pd.to_datetime(df['TIME']).apply(lambda x: x.weekday())

    conditions_semana = [(df['SEMANA'] == 0), (df['SEMANA'] == 1), (df['SEMANA'] == 2),
                         (df['SEMANA'] == 3), (df['SEMANA'] == 4), (df['SEMANA'] == 5), (df['SEMANA'] == 6)]

    df['SEMANA'] = np.select(conditions_semana,
                             ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo'])

    conditions = [(df['HORA'] >= 6) & (df['HORA'] <= 12),
                  (df['HORA'] >= 12) & (df['HORA'] <= 18),
                  (df['HORA'] >= 18) & (df['HORA'] <= 24),
                  (df['HORA'] >= 0) & (df['HORA'] <= 6)]
    values = ['Manhã', 'Tarde', 'Noite', 'Madrugada']
    df['TURNO'] = np.select(conditions, values)
    df['UNIDADE'] = np.where(df['LIKES'] == 2, 0, 1)

    df['COMENTARIOS'] = pd.to_numeric(df['COMENTARIOS'], errors='coerce').astype('Int64')
    df['LIKES'] = pd.to_numeric(df['LIKES'], errors='coerce').astype('Int64')
    df['HORA'] = pd.to_numeric(df['HORA'], errors='coerce').astype('Int64')

    df['INTERAÇÕES'] = df['LIKES'] + df['COMENTARIOS']

    df['UNIDADE'] = np.where(df['TIME'] == 2, 0, 1)
    df['shortcode'] = 'https://www.instagram.com/p/'+df['shortcode']

    df['% COMENTOU'] = df.apply(lambda row: round(row['COMENTARIOS'] * 100 / row['LIKES'], 2), axis=1)
    df['%VAR INTERAÇÕES'] = round((df['INTERAÇÕES'] - df['INTERAÇÕES'].shift(-1)) / df['INTERAÇÕES'].shift(-1) * 100, 2)
    df['VARIAÇÃO INTERAÇÕES'] = round((df['INTERAÇÕES'] - df['INTERAÇÕES'].shift(-1)), 2)

    df['UNIDADE'] = np.where(df['TIME'] == 2, 0, 1)

    df['__typename'].replace('GraphSidecar', 'Coleção', inplace=True)
    df['__typename'].replace('GraphImage', 'Imagem', inplace=True)
    df['__typename'].replace('GraphVideo', 'Vídeo', inplace=True)
    df = df[['TIME', '__typename', 'TEXTO', 'LIKES', 'COMENTARIOS', '% COMENTOU',
             'INTERAÇÕES', 'VARIAÇÃO INTERAÇÕES', '%VAR INTERAÇÕES',
             'shortcode', 'SEMANA', 'TURNO', 'HORA', 'DIA', 'id', 'UNIDADE']]

    df1 = df.rename(columns={'__typename': 'TIPO POST', 'shortcode': 'LINK', 'id': 'ID POST', 'TEXTO':'LEGENDA'})

    df = pd.concat([df_zero, df1], axis=0)

    df.drop_duplicates(keep=False)

    return df


@st.cache_data
def api_feed(end_cursor, res_midias, df_midia, userid):
    if end_cursor >= 100:
        end1 = res_midias["data"]["user"]["edge_owner_to_timeline_media"]["page_info"]["end_cursor"]
        res_midias1 = requi_midias1(userid, "50", end1)
        df_midia = convert_midias1(res_midias1, df_midia)
        if end_cursor >= 150:
            end2 = res_midias1["data"]["user"]["edge_owner_to_timeline_media"]["page_info"]["end_cursor"]
            res_midias2 = requi_midias2(userid, "50", end2)
            df_midia = convert_midias1(res_midias2, df_midia)
            if end_cursor >= 200:
                end3 = res_midias2["data"]["user"]["edge_owner_to_timeline_media"]["page_info"]["end_cursor"]
                res_midias3 = requi_midias3(userid, "50", end3)
                df_midia = convert_midias1(res_midias3, df_midia)
                if end_cursor == 250:
                    end4 = res_midias3["data"]["user"]["edge_owner_to_timeline_media"]["page_info"]["end_cursor"]
                    res_midias4 = requi_midias3(userid, "50", end4)
                    df_midia = convert_midias1(res_midias4, df_midia)

    return df_midia




html_card_1="""
<div class="card" style="border-radius: 10px 10px 10px 10px; background: #F5F5F5; 
                         border:solid; border-color: black; border-width: 1px 1px 1px 1px;
                         width: 100%; height: 100%;
                         padding-top: 5px; padding-right: 20px; padding-bottom: 5px; padding-left: 20px;">
    <p class="card-title" style="background-color:#F5F5F5; color:#0d0d0d; 
                                  margin-top: 10px; margin-bottom: 10px; margin-left: 10px; margin-right: 10px;
                                  font-family:sans-serif; text-align: justify; font-size: 90%" 
                                  > Bem-vindo(a) ao Instagram Monitor, uma ferramenta web para análise de dados do Instagram! 
                                  Com essa ferramenta, você poderá obter informações básicas de qualquer 
                                  conta do Instagram, bem como analisar as últimas 12 publicações (ou até 
                                  250 publicações) de uma conta específica.</p>
    <p class="card-title" style="background-color:#F5F5F5; color:#0d0d0d; 
                                  margin-top: 10px; margin-bottom: 10px; margin-left: 10px; margin-right: 10px;
                                  font-family:sans-serif; text-align: justify; font-size: 90%" 
                                  > Nossa ferramenta oferece tabelas dinâmicas e gráficos interativos que 
                                  permitem uma análise detalhada das publicações do Instagram. Além disso, 
                                  você poderá aplicar diversos filtros para facilitar a visualização das 
                                  informações e obter insights mais precisos.</p>
    <p>Com nossa ferramenta, você poderá:</p>
	<ul>
		<li>Obter informações básicas de qualquer conta do Instagram, como número de seguidores, número de seguindo, biografia, nome de usuário e foto do perfil.</li>
		<li>Analisar as últimas 12 publicações (ou até 250 publicações) de uma conta específica, visualizando informações como curtidas, comentários, data de publicação, hashtags utilizadas e muito mais.</li>
		<li>Utilizar tabelas dinâmicas e gráficos interativos para facilitar a análise e obter insights precisos.</li>
		<li>Aplicar diversos filtros para obter uma visualização mais precisa dos dados, como filtro por data, tipo de conteúdo, hashtags, localização e muito mais.</li>
	</ul>
</div>
"""






