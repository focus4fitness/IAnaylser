import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import numpy as np
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from wordcloud import STOPWORDS
from PIL import Image

from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode

im1 = Image.open("image/publicacao.jpeg")
im2 = Image.open("image/like.png")
im3 = Image.open("image/comentario.png")


def metricas(df):
    df_metricas = df.describe().reset_index()
    #GRÁFICO 2:
    num_post_like = df_metricas["LIKES"].iloc[0]
    soma_post_like = int(df['LIKES'].sum())
    media_post_like = df_metricas["LIKES"].iloc[1]
    min_post_like = df_metricas["LIKES"].iloc[3]
    max_post_like = df_metricas["LIKES"].iloc[7]
    #GRÁFICO 3:
    soma_post_comments = int(df['COMENTARIOS'].sum())
    media_post_comments = df_metricas["COMENTARIOS"].iloc[1]
    min_post_comments = df_metricas["COMENTARIOS"].iloc[3]
    max_post_comments = df_metricas["COMENTARIOS"].iloc[7]

    # CONFIGURANDO GRAFICO INDICADOR 2 -  METRICAS LIKES
    fig1 = go.Figure()
    fig1.add_trace(go.Indicator(
        mode="number",
        number_font_size=22,
        number_font_color="#E1306C",
        value=soma_post_like,
        title={"text": "<span style='font-size:16px;color:black'>Total:</span>"},
        domain = {'y': [0, 1], 'x': [0.2, 0.4]}))
    fig1.add_trace(go.Indicator(
        mode="number",
        number_font_size=22,
        number_font_color="#E1306C",
        value=media_post_like,
        title={"text": "<span style='font-size:16px;color:black'>Média:</span>"},
        domain = {'y': [0, 1], 'x': [0.4, 0.6]}))
    fig1.add_trace(go.Indicator(
        mode="number",
        number_font_size=22,
        number_font_color="#E1306C",
        value=max_post_like,
        title={"text": "<span style='font-size:16px;color:black'>Máximo:</span>"},
        domain={'y': [0, 1], 'x': [0.6, 0.8]}))
    fig1.add_trace(go.Indicator(
        mode="number",
        number_font_size=22,
        number_font_color="#E1306C",
        value=min_post_like,
        title={"text": "<span style='font-size:16px;color:black'>Mínimo:</span>"},
        domain={'y': [0, 1], 'x': [0.8, 1]}))
    fig1.update_layout(
        paper_bgcolor="#F8F8FF", height=90, margin=dict(l=1, r=1, b=1, t=30),
        grid={'rows': 1, 'columns': 3})

    fig1.add_layout_image(dict(source=im2, xref="paper", yref="paper", x=0.05, y=0.75, xanchor='left', yanchor='middle',
                               sizex=1.0, sizey=1.0))

    fig2 = go.Figure()
    fig2.add_trace(go.Indicator(
        mode="number",
        number_font_size=22,
        number_font_color="#833AB4",
        value=soma_post_comments,
        title={"text": "<span style='font-size:16px;color:black'>Total:</span>"},
        domain={'y': [0, 1], 'x': [0.2, 0.4]}))
    fig2.add_trace(go.Indicator(
        mode="number",
        number_font_size=22,
        number_font_color="#833AB4",
        value=media_post_comments,
        title={"text": "<span style='font-size:16px;color:black'>Média:</span>"},
        domain={'y': [0, 1], 'x': [0.4, 0.6]}))
    fig2.add_trace(go.Indicator(
        mode="number",
        number_font_size=22,
        number_font_color="#833AB4",
        value=max_post_comments,
        title={"text": "<span style='font-size:16px;color:black'>Máximo:</span>"},
        domain={'y': [0, 1], 'x': [0.6, 0.8]}))
    fig2.add_trace(go.Indicator(
        mode="number",
        number_font_size=22,
        number_font_color="#833AB4",
        value=min_post_comments,
        title={"text": "<span style='font-size:16px;color:black'>Mínimo:</span>"},
        domain={'y': [0, 1], 'x': [0.8, 1]}))
    fig2.update_layout(
        paper_bgcolor="#F8F8FF", height=90, margin=dict(l=1, r=1, b=0, t=30),
        grid={'rows': 1, 'columns': 3})

    fig2.add_layout_image(
        dict(source=im3, xref="paper", yref="paper", x=0.01, y=0.75, xanchor='left', yanchor='middle',
             sizex=0.90, sizey=0.9))

    return fig1, fig2



def plot_point_nome(df):

    df_gp = df

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df_gp['LIKES'], y=df_gp['COMENTARIOS'], customdata=df_gp['TIPO POST'],
                             mode='markers', text=df_gp['UNIDADE'], name='',
                             hovertemplate="</br><b>Likes:</b> %{x:,.0f}" +
                                           "</br><b>Comentários:</b> %{y:,.0f}"
                                           "</br><b>Publicações:</b> %{text}"+
                                           "</br><b>Agrupamento:</b> %{customdata}",
                             marker=dict(
                                 size=20,
                                 color=df_gp['INTERAÇÕES'],
                                 colorscale='Portland',
                                 showscale=True)
                             ))
    fig.update_layout(
        paper_bgcolor="#F8F8FF", plot_bgcolor="#F8F8FF", font={'color': "#000000", 'family': "sans-serif"},
        height=250, margin=dict(l=10, r=10, b=10, t=10))
    fig.update_xaxes(
        title_text="Likes", title_font=dict(family='Sans-serif', size=18), zeroline=False,
        tickfont=dict(family='Sans-serif', size=12), nticks=7, showgrid=True, gridwidth=0.8, gridcolor='#D3D3D3')
    fig.update_yaxes(
        title_text="Comentários", title_font=dict(family='Sans-serif', size=20), zeroline=False,
        tickfont=dict(family='Sans-serif', size=14), nticks=7, showgrid=True, gridwidth=0.8, gridcolor='#D3D3D3')

    return fig



def bar_hora(df):
    df_week = df.groupby('HORA').agg('mean').reset_index()
    df_week_soma = df.groupby('HORA').agg('mean').reset_index()

    values = df_week.HORA.unique()
    y_like = df_week['LIKES']
    y_comments = df_week['COMENTARIOS']

    y_num = df_week_soma['UNIDADE']
    y_num_soma = df_week_soma['LIKES']
    y_num_comments = df_week_soma['COMENTARIOS']

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name='Likes', x=values, y=y_num_soma,
        hovertemplate="</br><b>Média de Likes:</b> %{y:,.0f}",
        textposition='none', marker_color='#E1306C'
    ))
    fig.add_trace(go.Bar(
        name='Comentários', x=values, y=y_num_comments,
        hovertemplate="</br><b>Média de Comentários:</b> %{y:,.0f}",
        textposition='none', marker_color='#833AB4'
    ))
    fig.add_trace(go.Bar(
        name='Publicações', x=values, y=y_num,
        hovertemplate="</br><b>Publicações:</b> %{y:,.0f}",
        textposition='none', marker_color='#405DE6'
    ))
    fig.update_layout(
        paper_bgcolor="#F8F8FF", plot_bgcolor="#F8F8FF", font={'color': "#000000", 'family': "sans-serif"},
        legend=dict(font_size=11, orientation="h", yanchor="top", y=1.20, xanchor="center", x=0.5),
        height=200, barmode='stack', margin=dict(l=1, r=10, b=25, t=10), autosize=True, hovermode="x", )
    fig.update_yaxes(
        title_text="Número de Interações",title_font=dict(family='Sans-serif', size=12),
        tickfont=dict(family='Sans-serif', size=9), nticks=7, showgrid=True, gridwidth=0.5, gridcolor='#D3D3D3')

    fig.update_xaxes(
        tickfont=dict(family='Sans-serif', size=9), nticks=20, showgrid=False)

    return fig

def bar_semana(df):
    df_week_soma = df.groupby('SEMANA').agg('mean').reset_index().sort_values(by='LIKES', ascending=False)

    values = df_week_soma['SEMANA'].unique()

    y_num = df_week_soma['UNIDADE']
    y_num_soma = df_week_soma['LIKES']
    y_num_comments = df_week_soma['COMENTARIOS']

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name='Likes', x=values, y=y_num_soma,
        hovertemplate="</br><b>Média de Likes:</b> %{y:,.0f}",
        textposition='none', marker_color='#E1306C'
    ))
    fig.add_trace(go.Bar(
        name='Comentários', x=values, y=y_num_comments,
        hovertemplate="</br><b>Média de Comentários:</b> %{y:,.0f}",
        textposition='none', marker_color='#833AB4'
    ))
    fig.add_trace(go.Bar(
        name='Publicações', x=values, y=y_num,
        hovertemplate="</br><b>Publicações:</b> %{y:,.0f}",
        textposition='none', marker_color='#405DE6'
    ))
    fig.update_layout(
        paper_bgcolor="#F8F8FF", plot_bgcolor="#F8F8FF", font={'color': "#000000", 'family': "sans-serif"},
        legend=dict(font_size=11, orientation="h", yanchor="top", y=1.20, xanchor="center", x=0.5),
        height=200, barmode='stack', margin=dict(l=1, r=10, b=25, t=10), autosize=True, hovermode="x", )
    fig.update_yaxes(
        title_text="Número de Interações",title_font=dict(family='Sans-serif', size=12),
        tickfont=dict(family='Sans-serif', size=9), nticks=7, showgrid=True, gridwidth=0.5, gridcolor='#D3D3D3')

    fig.update_xaxes(
        tickfont=dict(family='Sans-serif', size=9), nticks=20, showgrid=False)

    return fig

def map(df):

    df_map = df.groupby(['SEMANA', 'TURNO']).agg('sum').sort_values(by='TURNO').reset_index()

    filtro1 = (df_map['SEMANA'] == 'Segunda') & (df_map['TURNO'] == 'Manhã')
    filtro2 = (df_map['SEMANA'] == 'Terça') & (df_map['TURNO'] == 'Manhã')
    filtro3 = (df_map['SEMANA'] == 'Quarta') & (df_map['TURNO'] == 'Manhã')
    filtro4 = (df_map['SEMANA'] == 'Quinta') & (df_map['TURNO'] == 'Manhã')
    filtro5 = (df_map['SEMANA'] == 'Sexta') & (df_map['TURNO'] == 'Manhã')
    filtro6 = (df_map['SEMANA'] == 'Sábado') & (df_map['TURNO'] == 'Manhã')
    filtro7 = (df_map['SEMANA'] == 'Domingo') & (df_map['TURNO'] == 'Manhã')

    filtro11 = (df_map['SEMANA'] == 'Segunda') & (df_map['TURNO'] == 'Tarde')
    filtro21 = (df_map['SEMANA'] == 'Terça') & (df_map['TURNO'] == 'Tarde')
    filtro31 = (df_map['SEMANA'] == 'Quarta') & (df_map['TURNO'] == 'Tarde')
    filtro41 = (df_map['SEMANA'] == 'Quinta') & (df_map['TURNO'] == 'Tarde')
    filtro51 = (df_map['SEMANA'] == 'Sexta') & (df_map['TURNO'] == 'Tarde')
    filtro61 = (df_map['SEMANA'] == 'Sábado') & (df_map['TURNO'] == 'Tarde')
    filtro71 = (df_map['SEMANA'] == 'Domingo') & (df_map['TURNO'] == 'Tarde')

    filtro12 = (df_map['SEMANA'] == 'Segunda') & (df_map['TURNO'] == 'Noite')
    filtro22 = (df_map['SEMANA'] == 'Terça') & (df_map['TURNO'] == 'Noite')
    filtro32 = (df_map['SEMANA'] == 'Quarta') & (df_map['TURNO'] == 'Noite')
    filtro42 = (df_map['SEMANA'] == 'Quinta') & (df_map['TURNO'] == 'Noite')
    filtro52 = (df_map['SEMANA'] == 'Sexta') & (df_map['TURNO'] == 'Noite')
    filtro62 = (df_map['SEMANA'] == 'Sábado') & (df_map['TURNO'] == 'Noite')
    filtro72 = (df_map['SEMANA'] == 'Domingo') & (df_map['TURNO'] == 'Noite')

    filtro13 = (df_map['SEMANA'] == 'Segunda') & (df_map['TURNO'] == 'Madrugada ')
    filtro23 = (df_map['SEMANA'] == 'Terça') & (df_map['TURNO'] == 'Madrugada')
    filtro33 = (df_map['SEMANA'] == 'Quarta') & (df_map['TURNO'] == 'Madrugada')
    filtro43 = (df_map['SEMANA'] == 'Quinta') & (df_map['TURNO'] == 'Madrugada')
    filtro53 = (df_map['SEMANA'] == 'Sexta') & (df_map['TURNO'] == 'Madrugada')
    filtro63 = (df_map['SEMANA'] == 'Sábado') & (df_map['TURNO'] == 'Madrugada')
    filtro73 = (df_map['SEMANA'] == 'Domingo') & (df_map['TURNO'] == 'Madrugada')


    try:
        dom_MD = df_map[filtro73]['INTERAÇÕES'].values[0]
    except:
        dom_MD = 0
    try:
        seg_MD = df_map[filtro13]['INTERAÇÕES'].values[0]
    except:
        seg_MD = 0
    try:
        ter_MD = df_map[filtro23]['INTERAÇÕES'].values[0]
    except:
        ter_MD = 0
    try:
        qua_MD = df_map[filtro33]['INTERAÇÕES'].values[0]
    except:
        qua_MD = 0
    try:
        qui_MD = df_map[filtro43]['INTERAÇÕES'].values[0]
    except:
        qui_MD = 0
    try:
        sex_MD = df_map[filtro53]['INTERAÇÕES'].values[0]
    except:
        sex_MD = 0
    try:
        sab_MD = df_map[filtro63]['INTERAÇÕES'].values[0]
    except:
        sab_MD = 0

    try:
        dom_NT = df_map[filtro72]['INTERAÇÕES'].values[0]
    except:
        dom_NT = 0
    try:
        seg_NT = df_map[filtro12]['INTERAÇÕES'].values[0]
    except:
        seg_NT = 0
    try:
        ter_NT = df_map[filtro22]['INTERAÇÕES'].values[0]
    except:
        ter_NT = 0
    try:
        qua_NT = df_map[filtro32]['INTERAÇÕES'].values[0]
    except:
        qua_NT = 0
    try:
        qui_NT = df_map[filtro42]['INTERAÇÕES'].values[0]
    except:
        qui_NT = 0
    try:
        sex_NT = df_map[filtro52]['INTERAÇÕES'].values[0]
    except:
        sex_NT = 0
    try:
        sab_NT = df_map[filtro62]['INTERAÇÕES'].values[0]
    except:
        sab_NT = 0

    try:
        dom_TD = df_map[filtro71]['INTERAÇÕES'].values[0]
    except:
        dom_TD = 0
    try:
        seg_TD = df_map[filtro11]['INTERAÇÕES'].values[0]
    except:
        seg_TD = 0
    try:
        ter_TD = df_map[filtro21]['INTERAÇÕES'].values[0]
    except:
        ter_TD = 0
    try:
        qua_TD = df_map[filtro31]['INTERAÇÕES'].values[0]
    except:
        qua_TD = 0
    try:
        qui_TD = df_map[filtro41]['INTERAÇÕES'].values[0]
    except:
        qui_TD = 0
    try:
        sex_TD = df_map[filtro51]['INTERAÇÕES'].values[0]
    except:
        sex_TD = 0
    try:
        sab_TD = df_map[filtro61]['INTERAÇÕES'].values[0]
    except:
        sab_TD = 0

    try:
        dom_MN = df_map[filtro7]['INTERAÇÕES'].values[0]
    except:
        dom_MN = 0
    try:
        seg_MN = df_map[filtro1]['INTERAÇÕES'].values[0]
    except:
        seg_MN = 0
    try:
        ter_MN = df_map[filtro2]['INTERAÇÕES'].values[0]
    except:
        ter_MN = 0
    try:
        qua_MN = df_map[filtro3]['INTERAÇÕES'].values[0]
    except:
        qua_MN = 0
    try:
        qui_MN = df_map[filtro4]['INTERAÇÕES'].values[0]
    except:
        qui_MN = 0
    try:
        sex_MN = df_map[filtro5]['INTERAÇÕES'].values[0]
    except:
        sex_MN = 0
    try:
        sab_MN = df_map[filtro6]['INTERAÇÕES'].values[0]
    except:
        sab_MN = 0

    matriz = [[dom_NT, seg_NT, ter_NT, qua_NT, qui_NT, sex_NT, sab_NT],
              [dom_TD, seg_TD, ter_TD, qua_TD, qui_TD, sex_TD, sab_TD],
              [dom_MN, seg_MN, ter_MN, qua_MN, qui_MN, sex_MN, sab_MN],
              [dom_MD, seg_MD, ter_MD, qua_MD, qui_MD, sex_MD, sab_MD],]

    figC2 = go.Figure(data=go.Heatmap(
                       z=matriz, name="", text=matriz,
                       x=['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado'],
                       y=['Noite', 'Tarde', 'Manhã', 'Madrugada'],
                       texttemplate="%{text:,.0f}",
                       hovertemplate="</br><b>Dia:</b> %{x}"+
                                     "</br><b>Turno:</b> %{y}"+
                                     "</br><b>Interações:</b> %{z:,.0f}",
                       colorscale='Portland'))
    figC2.update_layout(autosize=True,
                       height=200, margin=dict(l=1, r=10, b=10, t=15),
                       paper_bgcolor="#F8F8FF", font={'size': 12})



    return figC2






def linha_nome(df):
    df_day = df.groupby(['HORA', 'TIPO POST']).agg('sum').reset_index()

    figB2 = go.Figure()
    figB2.add_trace(go.Scatter(
        x=df_day['HORA'], y=df_day['INTERAÇÕES'],
        name='Coleção', mode='lines',  hovertemplate=None, xhoverformat="%d %b %y",
        line=dict(width=3, color='#C41A1B')))


    figB2.update_layout(
        paper_bgcolor="#F8F8FF", plot_bgcolor="#F8F8FF", font={'color': "#000000", 'family': "sans-serif"},
        legend=dict(font_size=14, orientation="h", yanchor="top", y=1.50, xanchor="center", x=0.5),
        height=250, hovermode="x unified", margin=dict(l=10, r=10, b=0, t=10))
    figB2.update_xaxes(
        rangeslider_visible=True, showgrid=False,
        rangeselector=dict(
            buttons=list([
                dict(count=5, label="5D", step="day", stepmode="backward"),
                dict(count=15, label="15D", step="day", stepmode="backward"),
                dict(count=1, label="1M", step="month", stepmode="backward"),
                dict(count=2, label="2M", step="month", stepmode="backward"),
                dict(label="TUDO", step="all")
            ])
        )
    )
    figB2.update_yaxes(
        title_text="Número de Interações", title_font=dict(family='Sans-serif', size=12),
        tickfont=dict(family='Sans-serif', size=9), nticks=7, showgrid=True, gridwidth=0.5, gridcolor='#D3D3D3')
    return figB2




def pie3(df):

    df = df.rename(columns={'TIPO POST': 'tipo'})

    df_type = df.groupby('tipo').agg('sum').reset_index()
    df_ima = df_type.query("tipo == 'Imagem'")
    df_col = df_type.query("tipo == 'Coleção'")
    df_vid = df_type.query("tipo == 'Vídeo'")

    try:
        IMAGEM = df_ima["UNIDADE"].iloc[0]
        IMAGEM_LIKES = df_ima["LIKES"].iloc[0]
        IMAGEM_COMENTARIOS = df_ima["COMENTARIOS"].iloc[0]
    except:
        IMAGEM = 0
        IMAGEM_LIKES = 0
        IMAGEM_COMENTARIOS = 0

    try:
        VIDEO = df_vid["UNIDADE"].iloc[0]
        VIDEO_LIKES = df_vid["LIKES"].iloc[0]
        VIDEO_COMENTARIOS = df_vid["COMENTARIOS"].iloc[0]
    except:
        VIDEO = 0
        VIDEO_LIKES = 0
        VIDEO_COMENTARIOS = 0

    try:
        COLECAO = df_col["UNIDADE"].iloc[0]
        COLECAO_LIKES = df_col["LIKES"].iloc[0]
        COLECAO_COMENTARIOS = df_col["COMENTARIOS"].iloc[0]
    except:
        COLECAO = 0
        COLECAO_LIKES = 0
        COLECAO_COMENTARIOS = 0

    labels = ['Imagem', "Coleção", 'Vídeo']
    colors = ['#FCAF45', '#F77737', '#FD1D1D']
    fig = make_subplots(rows=1, cols=3, specs=[[{'type':'domain'}, {'type':'domain'}, {'type':'domain'}]],
                          subplot_titles=['Publicações:', 'Likes:', 'Comentários:'])

    fig.add_trace(go.Pie(labels=labels, name="",
                           values=[IMAGEM, COLECAO, VIDEO],
                           textinfo='none', showlegend=True,
                           domain={'y': [0, 1], 'x': [0, 0.3]},
                           marker=dict(colors=colors, line=dict(color='#000010', width=2))))

    fig.add_trace(go.Pie(labels=labels, name="",
                           values=[IMAGEM_LIKES, COLECAO_LIKES, VIDEO_LIKES],
                           textinfo='none', showlegend=True,
                           domain={'y': [0, 1], 'x': [0.35, 0.65]},
                           marker=dict(colors=colors, line=dict(color='#000010', width=2))))
    fig.add_trace(go.Pie(labels=labels, name="",
                           values=[IMAGEM_COMENTARIOS, COLECAO_COMENTARIOS, VIDEO_COMENTARIOS],
                           textinfo='none', showlegend=True,
                           domain={'y': [0, 1], 'x': [0.7, 1]},
                           marker=dict(colors=colors, line=dict(color='#000010', width=2))))

    fig.update_traces(hole=.4, hoverinfo="label+name+percent+value",
                        hovertemplate="</br><b>Publicação:</b> %{label} " +
                                      "</br><b>Quantidade:</b>  %{value}" +
                                      "</br><b>Proporção:</b>  %{percent}")
    fig.update_layout(autosize=True,
                       height=200, margin=dict(l=10, r=10, b=20, t=40),
                       legend=dict(font_size=14, orientation="h", yanchor="top",
                                   y=-0.05, xanchor="center", x=0.5),
                       paper_bgcolor="#F8F8FF", font={'size': 20})


    return fig
