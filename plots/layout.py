import streamlit
import streamlit.type_util

from plots.plots_insta1 import *
from plots.plots import *

from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode

from PIL import Image
from io import BytesIO



def rodape():
    html_rodape = """
    <hr style= "display: block;
      margin-top: 0.5em;
      margin-bottom: 0.5em;
      margin-left: auto;
      margin-right: auto;
      border-style: inset;
      border-width: 1.5px;">
      <p style="color:Gainsboro; text-align: center;">Última atualização: 27/10/2022</p>
    """

    st.markdown(html_rodape, unsafe_allow_html=True) # ---- by: mateus
    return None

@st.cache_resource(experimental_allow_widgets=True)
def parte1(df_info, df_midia):

    response = requests.get(df_info["FOTO HD"][0])
    img = Image.open(BytesIO(response.content))

    st.markdown("<h2 style='font-size:150%; text-align: center; color: #8435B4; padding: 0px 0px 10px 0px;"
                ">Informações básicas sobre o perfil </h2>",
                unsafe_allow_html=True)
    col1A, col2A = st.columns([10, 1])
    with col1A:
        st.dataframe(df_info)
    with col2A:
        st.image(img, use_column_width=True)

    df_size = str(len(df_midia))

    st.markdown("<h2 style='font-size:150%; text-align: center; color: #8435B4; padding: 0px 0px 10px 0px;'" +
                ">Informações sobre às "+df_size+" últimas publicações - Tabela Dinâmica</h2>",
                unsafe_allow_html=True)
    agg_tabela(df_midia, True)
    st.markdown('---')



    with st.expander("Edição do Gráfico"):
        grafico = st.selectbox('Tipo do Gráfico:',
                               ['Barra Simples', 'Linha Simples', 'Barras Empilhadas', 'Barras Agrupadas',
                                'Multiplas Linhas', 'Multiplas Áreas', 'Área Normalizada', 'Nuvem de Palavras'],
                               index=0, key=1)

        if grafico == 'Barra Simples' or grafico == 'Linha Simples':
            col1, col2, col3, col4 = st.columns([2, 5, 5, 2])
            with col1:
                cor1 = st.color_picker('Cor do Gráfico:', '#05A854', key=2)
            with col2:
                df_y = df_midia[['LIKES', 'COMENTARIOS','% COMENTOU', 'INTERAÇÕES','VARIAÇÃO INTERAÇÕES', '%VAR INTERAÇÕES', 'UNIDADE']]
                vary = st.selectbox('Selecione o eixo Y:', df_y.columns.unique(), index=0, key=3)
            with col3:
                df_x = df_midia[['TIPO POST', 'TIME', 'DIA', 'HORA', 'SEMANA', 'TURNO', 'LINK']]
                varx = st.selectbox('Selecione o eixo X:', df_x.columns.unique(), index=0, key=4)
            with col4:

                tipo = st.radio('Tipo de agrupamento:',
                                ['Soma', 'Média'], index=0, key=5,horizontal=True)
                if tipo == 'Soma':
                    df_midia = df_midia.groupby(varx).sum().reset_index()
                elif tipo == 'Média':
                    df_midia = df_midia.groupby(varx).mean().reset_index()


    if grafico == 'Linha Simples':
        fig1 = line_plot(df_midia, varx, vary, cor1)
    elif grafico == 'Barra Simples':
        fig1 = bar_plot(df_midia, varx, vary, cor1)

    if grafico == 'Barra Simples' or grafico == 'Linha Simples':
        st.markdown("<h3 style='font-size:150%; text-align: center; color: #8435B4; padding: 10px 0px 10px 0px;'" +
                    ">"+tipo+" dos " + vary + " por " + varx + " - " + grafico + "</h3>",
                    unsafe_allow_html=True)
        st.plotly_chart(fig1, use_container_width=True, config=config)

    elif grafico == 'Nuvem de Palavras':
        st.markdown("<h3 style='font-size:150%; text-align: center; color: #05A854; padding: 10px 0px 10px 0px;'" +
                    ">Palavras mais frequentes nas legendas " + grafico + "</h3>",
                    unsafe_allow_html=True)
        df1 = df_midia[['LEGENDA']]
        fig1 = wordcloud(df1)
        st.pyplot(fig1)


    return



def dashboard(df_info, df):

    response = requests.get(df_info["FOTO HD"][0])
    img = Image.open(BytesIO(response.content))

    #st.markdown('---')
    st.markdown("<h3 style='font-size:150%; text-align: center; color: #8435B4; padding: 0px 0px 10px 0px; padding-top: -40px;'" +
                ">Informações básicas sobre o perfil </h3>",
                unsafe_allow_html=True)
    col1A, col2A = st.columns([10, 1])
    with col1A:
        st.dataframe(df_info)
    with col2A:
        st.image(img, use_column_width=True)

    df_size = str(len(df))

    st.markdown("<h3 style='font-size:150%; text-align: center; color: #8435B4; padding: 0px 0px 10px 0px;'" +
                ">Informações sobre às " + df_size + " últimas publicações - Tabela Dinâmica</h3>",
                unsafe_allow_html=True)
    agg_tabela(df, True)
    st.markdown('---')



    st.markdown("<h3 style='font-size:150%; text-align: center; color: #8435B4; padding: 10px 0px 10px 0px;'" +
                ">Indicadores Chaves sobre Likes e Comentários</h3>",
                unsafe_allow_html=True)
    col2A, col3A, col4A = st.columns([520, 60, 520])
    with col2A:
        fig1, fig2 = metricas(df)
        st.plotly_chart(fig1, use_container_width=True, config=config)
    with col3A:
        st.text("")
    with col4A:
        st.plotly_chart(fig2, use_container_width=True, config=config)

    fig3 = plot_point_nome(df)

    st.markdown("<h3 style='font-size:150%; text-align: center; color: #8435B4; padding: 10px 0px 10px 0px;'" +
                ">N° de Likes e Comentários por Publicação</h3>",
                unsafe_allow_html=True)
    st.plotly_chart(fig3, use_container_width=True, config=config)


    col2, col3, col4 = st.columns([520, 60, 520])
    with col2:
        st.markdown("<h3 style='font-size:150%; text-align: center; color: #8435B4; padding: 10px 0px 10px 0px;'" +
                    ">Comparação entre os Horários</h3>",
                    unsafe_allow_html=True)
        fig1 = bar_hora(df)
        st.plotly_chart(fig1, use_container_width=True, config=config)
    with col3:
        st.text("")
    with col4:
        st.markdown("<h3 style='font-size:143%; text-align: center; color: #8435B4; padding: 10px 0px 10px 0px;'" +
                    ">Comparação entre os Dias da Semana</h3>",
                    unsafe_allow_html=True)

        figC2 = bar_semana(df)
        st.plotly_chart(figC2, use_container_width=True, config=config)

    st.text("")
    st.text("")

    figC2 = map(df)
    st.markdown("<h3 style='font-size:143%; text-align: center; color: #8435B4; padding: 10px 0px 10px 0px;'" +
                ">Total de Interações por Turno e Dia da Semana</h3>",
                unsafe_allow_html=True)
    st.plotly_chart(figC2, use_container_width=True, config=config)

    st.text("")
    st.text("")

    col2, col3, col4 = st.columns([520, 60, 520])
    with col2:
        st.markdown("<h3 style='font-size:150%; text-align: center; color: #8435B4; padding: 10px 0px 10px 0px;'" +
                    ">Análise das Legendas</h3>",
                    unsafe_allow_html=True)
        fig4 = wordcloud(df)
        st.pyplot(fig4)
    with col3:
        st.text("")
    with col4:
        st.markdown("<h3 style='font-size:150%; text-align: center; color: #8435B4; padding: 10px 0px 10px 0px;'" +
                    ">Análise por Tipo de Publicação</h3>",
                    unsafe_allow_html=True)
        st.text("")
        figA4 = pie3(df)
        st.plotly_chart(figA4, use_container_width=True, config=config)

    st.text("")
    st.text("")



    return None