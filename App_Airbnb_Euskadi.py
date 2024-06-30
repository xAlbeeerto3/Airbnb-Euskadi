#---LIBRERÍAS EMPLEADAS---#
import numpy as np 
import pandas as pd 
import csv
import seaborn as sns
import matplotlib.pyplot as plt
import plotly_express as px
import streamlit as st
import base64
from datetime import datetime 
from dateutil.relativedelta import relativedelta
import requests
from bs4 import BeautifulSoup
sns.set()
import plotly as pt
from streamlit_folium import st_folium
import folium
from streamlit_folium import folium_static
from folium.plugins import HeatMap
from folium.plugins import FastMarkerCluster
import streamlit as st
import requests

#---DISEÑO BÁSICO---#

# Nombre e icono de la web
st.set_page_config(page_title="Airbnb Data - Euskadi",
        layout="wide",
        page_icon="🏠")

# Eliminamos la barra superior
st.markdown(
    """
    <style>
    [data-testid="stHeader"] {
        background-color: rgba(0, 0, 0, 0);
    }
    </style>
    """,
    unsafe_allow_html=True)

# Fondo de la web
url_imagen_fondo = "https://media.traveler.es/photos/62e035edbb3fef99d2f94cbd/16:9/w_2560%2Cc_limit/2BFR0JF.jpg"

def add_bg_from_url(url_imagen_fondo):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url({url_imagen_fondo});
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True)

add_bg_from_url(url_imagen_fondo)

# Estilos para el sidebar y contenido principal
st.markdown(
    f"""
    <style>
    .sidebar-content {{
        background-color: #008080 !important;
        padding: 10px !important;
        border: 1px solid #008080 !important;
        border-radius: 5px !important;
    }}
    </style>
    """,
    unsafe_allow_html=True)

# Sidebar para el menú principal
st.sidebar.header("Menú principal", divider='rainbow')
menu = st.sidebar.radio("Selecciona una opción:", ["Inicio", "Dataframe", "EDA", "Pruebas Estadísticas", "Mapas","Power Bi","Conclusión"]) # Cinco pilares de la App


#---LECTURA---#
listing = pd.read_csv('listings2.csv')


# ---PREPROCESAMIENTO Y LIMPIEZA---#
variables = ["id", "name", "host_id", "host_name", "host_response_rate", "host_is_superhost", "host_total_listings_count", "neighbourhood_cleansed", "neighbourhood_group_cleansed", "latitude", "longitude", "property_type", "accommodates", "bathrooms", "bedrooms", "amenities", "price", "minimum_nights", "availability_365", "number_of_reviews", "review_scores_rating", "reviews_per_month", "review_scores_location", 'review_scores_cleanliness','review_scores_value','review_scores_communication','review_scores_checkin', 'review_scores_accuracy','room_type'] 
listing = listing[variables]

listing.drop(['host_response_rate','review_scores_rating','reviews_per_month'], axis=1, inplace=True)

listing['bathrooms']= listing['bathrooms'].median()
listing['bedrooms']= listing['bedrooms'].median()
listing['price'] = listing['price'].str.replace('[\$]', '').str.replace(',','')

listing['bathrooms']= listing['bathrooms'].astype(int)
listing['bedrooms']= listing['bedrooms'].astype(int)
listing['price']=listing['price'].astype(float)
precio_medio = listing['price'].mean()
listing['price'].round(2)
listing['price'].fillna(precio_medio, inplace=True)

listing.rename({'name': 'Descripción','host_name':'Anfitrión','host_is_superhost': 'Superhost','host_total_listings_count':'Total_anuncios','neighbourhood_cleansed':'Localidades','neighbourhood_group_cleansed':'Zonas','latitude':'Latitud','longitude':'Longitud','property_type':'Tipo_propiedad','accommodates':'Total_huespedes','bathrooms':'Total_baños','bedrooms':'Total_dormitorios','amenities':'Servicios','price':'Precio','minimum_nights':'Mínima_estancia','availability_365':'Disponibilidad_anual','number_of_reviews':'Total_reseñas'}, axis=1, inplace=True)

listing['Superhost']=listing['Superhost'].str.replace('t','Sí').str.replace('f', 'No')

listing['Localidades'] = listing['Localidades'].str.replace('SebastiÃ¡n', 'Sebastián').str.replace('Ãlava','Álava').str.replace('GuipÃºzcoa','Guipúzcoa').str.replace('AbadiÃ±o','Abadiño').str.replace('EreÃ±o','Ereaño').str.replace('CiÃ©rvana','Ciérvana').str.replace('MaÃ±aria','Mañaria').str.replace('OyÃ³n','Oyón')

listing['Zonas'] = listing['Zonas'].str.replace('Ãlava','Álava').str.replace('GuipÃºzcoa','Guipúzcoa')

listing['Descripción'] = listing['Descripción'].str.replace('+', ' ').str.replace(',','')

listing.rename({'review_scores_location':'Localización','review_scores_cleanliness':'Limpieza','review_scores_value':'Experiencia_General','review_scores_communication':'Comunicación','review_scores_checkin':'Checkin', 'review_scores_accuracy': 'Precisión', 'room_type':'Tipo_habitación'}, axis=1, inplace=True)

listing['Limpieza'].fillna(listing['Limpieza'].mean(), inplace=True)
listing['Localización'].fillna(listing['Localización'].mean(), inplace=True)
listing['Experiencia_General'].fillna(listing['Experiencia_General'].mean(), inplace=True)
listing['Comunicación'].fillna(listing['Comunicación'].mean(), inplace=True)
listing['Checkin'].fillna(listing['Checkin'].mean(), inplace=True)
listing['Precisión'].fillna(listing['Precisión'].mean(), inplace=True)


#---INICIO---#
if menu =="Inicio":
    
    st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: center; color: #ffffff; font-size: 70px; margin: 0; text-shadow: 6px 6px 6px #000000;'>Inicio</h1></div>", unsafe_allow_html=True)

    
    st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: left; color: #ffffff; font-size: 40px; margin: 0; text-shadow: 6px 6px 6px #000000;'>Breve Historia 📜</h1></div>", unsafe_allow_html=True)
    
    st.markdown(
    """
    <div style="background-color: rgba(255, 90, 95, 0.8); padding: 20px; color: #ffffff; font-size: 20px;">
    Euskadi es una comunidad autónoma considerada nacionalidad histórica.
    Se compone de las provincias y territorios (Zonas) de Álava, Guipúzcoa y Vizcaya.
    Es una de las diecisiete Comunidades Autónomas que forman España.
    El turismo en Euskadi, a simple vista tiene dos efectos directos en la industria
    turística:
    El primero incrementa la oferta de alojamientos y ofrece opciones diferentes a los
    hoteles de toda la vida, frente a una segunda que compite directamente con los
    precios en temporadas de alta demanda, provocando bajadas de precios.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""<div style="margin-bottom: 20px;"></div>""", unsafe_allow_html=True)

    st.markdown(
    """
    <div style="background-color: rgba(255, 90, 95, 0.8); padding: 20px; color: #ffffff; font-size: 20px;">
    Airbnb es una plataforma que facilita el alquiler temporal de viviendas o habitaciones, fundada en 2008 y presente en Euskadi desde 2009. Desde entonces, ha experimentado un crecimiento significativo, generando debates y controversias sobre su impacto en la oferta de alojamiento en la ciudad.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""<div style="margin-bottom: 20px;"></div>""", unsafe_allow_html=True)
    
    columaimagen1, columaimagen2 = st.columns(2)

    # Primera columna: recortes de periodicos
    with columaimagen1:
        imagen_periodico = (r'Imágenes\airbnb_periodico.PNG')
        imagen_desconocida = (r'Imágenes\ciudad_desconocida.PNG')
        st.image(imagen_periodico)
        st.image(imagen_desconocida)
        st.markdown(
    """
    <div style=" padding: 20px; color: #ffffff; font-size: 15px; text-shadow: 6px 6px 6px #000000">
    Fuente: Viajestic
    </div>
    """, unsafe_allow_html=True)

    # Segunda columna: Imagen de la web Airbnb de Euskadi
    with columaimagen2:
        imagen_web_euskadi = (r'Imágenes\airbnb_web_euskadi.PNG')
        st.image(imagen_web_euskadi)
        
        st.markdown(
    """
    <div style=" padding: 20px; color: #ffffff; font-size: 15px; text-shadow: 6px 6px 6px #000000">
    Fuente: Airbnb
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""<div style="margin-bottom: 20px;"></div>""", unsafe_allow_html=True)
    
    st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: left; color: #ffffff; font-size: 40px; margin: 0; text-shadow: 6px 6px 6px #000000;'>Objetivo del Análisis 🎯</h1></div>", unsafe_allow_html=True)
    
    st.markdown(
        """
        <div style="background-color: rgba(255, 90, 95, 0.8); padding: 20px; color: #ffffff; font-size: 20px;">
        Este proyecto tiene como finalidad comprender y analizar los datos provenientes de la web InsideAirbnb. Así como observar posibles tendencias en cuanto al número de viviendas, precios, tipos de propiedades,etc para entender como está afectando esto al mercado de los viajes y alojamientos en Euskadi.
        La propuesta que se plantea es la siguiente:
        ¿Es Airbnb una opción rentable y proporciona al turista alojamientos más asequibles
        para disfrutar en cualquier época del año?
        """, unsafe_allow_html=True)
    
    st.markdown("""<div style="margin-bottom: 20px;"></div>""", unsafe_allow_html=True)
    
    mapas_juntos = (r'Imágenes\mapas_juntos.png')
    
    st.image(mapas_juntos, use_column_width=True, width=700)
    
    st.markdown(
    """
    <div style=" padding: 20px; color: #ffffff; font-size: 15px; text-shadow: 6px 6px 6px #000000">
    Fuente: Elaboracion propia.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(
        """
        <div style="background-color: rgba(255, 90, 95, 0.8); padding: 20px; color: #ffffff; font-size: 20px;">
        Podemos observar tres mapas, político, geográfico y el mapa de la 
        distribución de alojamientos por zonas, observando que la costa es la que contiene 
        más alojamientos.
        """, unsafe_allow_html=True)


#---DATAFRAME---#
if menu == "Dataframe":
    st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: center; color: #ffffff; font-size: 70px; margin: 0; text-shadow: 6px 6px 6px #000000;'>Dataframe 📚​ </h1></div>", unsafe_allow_html=True)
    
    url_imagen_fondo_dataframe = "https://image.lexica.art/full_webp/096b545a-d952-49b7-aaa9-0da2445b8132"

    def add_bg_from_url(url_imagen_fondo_dataframe):
            st.markdown(
                f"""
                <style>
                .stApp {{
                    background-image: url({url_imagen_fondo_dataframe});
                    background-size: cover;
                    background-repeat: no-repeat;
                    background-attachment: fixed;
                }}
                </style>
                """,
                unsafe_allow_html=True)

    add_bg_from_url(url_imagen_fondo_dataframe)
    
    st.sidebar.header("Encuentra tu hogar: :mag_right:")
    
    # Creamos los filtros en el sidebar
    seleccion_zona = st.sidebar.multiselect("Zonas: :house_with_garden:", options=listing["Zonas"].unique(), default=listing["Zonas"].unique())
    seleccion_tipo_habitacion = st.sidebar.multiselect("Tipo_habitación: :bed:", options=listing["Tipo_habitación"].unique(), default=listing["Tipo_habitación"].unique())
    seleccion_precio = st.sidebar.slider("Precio: 💲", min_value=5, max_value=21000, value=(5, 21000))
    seleccion_total_reseñas = st.sidebar.slider("Total_reseñas: ⭐", min_value=0, max_value=1162, value=(0, 1162))
    seleccion_estancia_mínima = st.sidebar.slider("Mínima_estancia: 🌒", min_value=1, max_value=365, value=(1, 365))
    
    # DataFrame con los filtros aplicados
    seleccion_df = listing.query("Zonas == @seleccion_zona & Tipo_habitación == @seleccion_tipo_habitacion & Precio >= @seleccion_precio[0] & Precio <= @seleccion_precio[1] & Total_reseñas >= @seleccion_total_reseñas[0] & Total_reseñas <= @seleccion_total_reseñas[1] & Mínima_estancia >= @seleccion_estancia_mínima[0] & Mínima_estancia <= @seleccion_estancia_mínima[1] ")
    st.dataframe(seleccion_df)

    # Resultados obtenidos
    resultado_df = seleccion_df.shape[0]
    st.markdown(f"*Resultados obtenidos: **{resultado_df}** *")

    st.markdown("""<br><br>""", unsafe_allow_html=True)
  
    col1, col2, col3 = st.columns(3)

    # Primera columna y primer grafico
    with col1:
        st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: center; color: #ffffff; font-size: 35px; margin: 0; text-shadow: 6px 6px 6px #000000;'>🏡 Zonas vs Tipo de Habitación 🛏️</h1></div>", unsafe_allow_html=True)
        fig1 = px.bar(seleccion_df, x='Zonas', y='Tipo_habitación')
        st.plotly_chart(fig1, use_container_width=True)

    # Segunda columna y segundo grafico
    with col2:
        st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: center; color: #ffffff; font-size: 35px; margin: 0; text-shadow: 6px 6px 6px #000000;'>🛏️ Tipo de Habitación vs Precio 💲</h1></div>", unsafe_allow_html=True)
        fig2 = px.scatter(seleccion_df, x='Tipo_habitación', y='Precio')
        st.plotly_chart(fig2, use_container_width=True)

    # Tercera columna y tercer grafico
    with col3:
        st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: center; color: #ffffff; font-size: 35px; margin: 0; text-shadow: 6px 6px 6px #000000;'>⭐ Total de Reseñas vs Precio 💲</h1></div>", unsafe_allow_html=True)
        fig3 = px.bar(seleccion_df, x='Total_reseñas', y='Precio')
        st.plotly_chart(fig3, use_container_width=True)
        
  
#---EDA---#    
if menu == "EDA":
    st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: center; color: #ffffff; font-size: 70px; margin: 0; text-shadow: 6px 6px 6px #000000;'>Análisis Exploratorio 📊</h1></div>", unsafe_allow_html=True)
    
    url_imagen_fondo_eda = "https://image.lexica.art/full_webp/1dba513e-fc92-42b1-82f7-cffa4a1089c8"

    def add_bg_from_url(url_imagen_fondo_eda):
            st.markdown(
                f"""
                <style>
                .stApp {{
                    background-image: url({url_imagen_fondo_eda});
                    background-size: cover;
                    background-repeat: no-repeat;
                    background-attachment: fixed;
                }}
                </style>
                """,
                unsafe_allow_html=True)

    add_bg_from_url(url_imagen_fondo_eda)
    
    # Rutas de las imagenes utilizadas
    ruta_grafica1 = r"Imágenes\grafica_01.png"
    ruta_grafica2 = r"Imágenes\grafica_02.png"
    ruta_grafica3 = r"Imágenes\grafica_03.png"
    ruta_grafica4 = r"Imágenes\grafica_04.png"
    ruta_grafica5 = r"Imágenes\grafica_05.png"
    ruta_grafica6 = r"Imágenes\grafica_06.png"
    ruta_grafica7 = r"Imágenes\grafica_07.png"
    ruta_grafica8 = r"Imágenes\grafica_08.png"
    ruta_grafica9 = r"Imágenes\grafica_09.png"
    ruta_grafica10 = r"Imágenes\grafica_10.png"
    ruta_grafica11 = r"Imágenes\grafica_11.png"
    ruta_grafica12 = r"Imágenes\grafica_12.png"
    ruta_grafica13 = r"Imágenes\grafica_13.png"
    ruta_grafica20 = r"Imágenes\grafica_20.PNG"
    
    # Título gráfica
    st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: left; color: #ffffff; font-size: 35px; margin: 0; text-shadow: 6px 6px 6px #000000;'>Total de alojamientos por Zonas</h1></div>", unsafe_allow_html=True)

    # Mostramos la imagen
    st.image(ruta_grafica1, width=700)

    # Botón que muestra el comentario
    if st.button("Comentario sobre la gráfica", key="1"):
        st.markdown(
        """
        <div style="text-align: left; border: 1px solid #000000; padding: 10px; background-color: rgba(255, 255, 255, 0.5); color: #000000; box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.5); border-radius: 10px;">
            <b>Comentario:</b><br>
            En el total de alojamientos por zonas hemos dividido el precio en rangos para ver 
            de manera grupal la relación directa que tienen el precio y la cantidad de 
            alojamientos según la zona.
        </div>
        """, unsafe_allow_html=True)
        
    # Título gráfica
    st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: left; color: #ffffff; font-size: 35px; margin: 0; text-shadow: 6px 6px 6px #000000;'>Zonas con más reseñas</h1></div>", unsafe_allow_html=True)

    # Mostramos la imagen
    st.image(ruta_grafica4, width=700)

    # Botón que muestra el comentario
    if st.button("Comentario sobre la gráfica", key="4"):
        st.markdown(
        """
        <div style="text-align: left; border: 1px solid #000000; padding: 10px; background-color: rgba(255, 255, 255, 0.5); color: #000000; box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.5); border-radius: 10px;">
            <b>Comentario 1:</b><br>
            Hay un desnivel considerable de las reseñas de los usuarios, 
            siendo Álava la que menos reseñas tiene y que como veremos más adelante es a. 
            causa de su baja cantidad de alojamientos.
        </div>
        """, unsafe_allow_html=True)

    # Título gráfica
    st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: left; color: #ffffff; font-size: 35px; margin: 0; text-shadow: 6px 6px 6px #000000;'>Número de habitaciones privadas por zonas</h1></div>", unsafe_allow_html=True)

    # Mostramos la imagen
    st.image(ruta_grafica8, width=700)

    # Botón que muestra el comentario
    if st.button("Comentario sobre la gráfica", key="8"):
        st.markdown(
        """
        <div style="text-align: left; border: 1px solid #000000; padding: 10px; background-color: rgba(255, 255, 255, 0.5); color: #000000; box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.5); border-radius: 10px;">
            <b>Comentario:</b><br>
          Muchos anfitriones alquilan, habitaciones privadas, siendo Vizcaya la zona que
          más habitaciones ofrece dos a uno frente Álava y Guipúzcoa.  
        </div>
        """, unsafe_allow_html=True)
        
    # Título gráfica
    st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: left; color: #ffffff; font-size: 35px; margin: 0; text-shadow: 6px 6px 6px #000000;'>Distribución de precios por zonas</h1></div>", unsafe_allow_html=True)

    # Mostramos la imagen
    st.image(ruta_grafica5, width=700)

    # Botón que muestra el comentario
    if st.button("Comentario sobre la gráfica", key="5"):
        st.markdown(
        """
        <div style="text-align: left; border: 1px solid #000000; padding: 10px; background-color: rgba(255, 255, 255, 0.5); color: #000000; box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.5); border-radius: 10px;">
            <b>Comentario:</b><br>
            Entre el rango de precios 0-200, Vizcaya es la zona mas frecuentada a ese precio.
        </div>
        """, unsafe_allow_html=True)
        
    # Título gráfica
    st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: left; color: #ffffff; font-size: 35px; margin: 0; text-shadow: 6px 6px 6px #000000;'>Precio medio por persona y zona</h1></div>", unsafe_allow_html=True)

    # Mostramos la imagen
    st.image(ruta_grafica20, width=1200)

    # Botón que muestra el comentario
    if st.button("Comentario sobre la gráfica", key="20"):
        st.markdown(
        """
        <div style="text-align: left; border: 1px solid #000000; padding: 10px; background-color: rgba(255, 255, 255, 0.5); color: #000000; box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.5); border-radius: 10px;">
            <b>Comentario:</b><br>
            Calculando la el precio por persona se han graficado las zonas donde el precio
            por persona es más alto, siendo sorprendentemente Álava la zona más cara pese a
            su baja cantidad de alojamientos.
        </div>
        """, unsafe_allow_html=True)
        
     # Título gráfica
    st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: left; color: #ffffff; font-size: 35px; margin: 0; text-shadow: 6px 6px 6px #000000;'>Disponibilidad anual vs Precio</h1></div>", unsafe_allow_html=True)

    # Mostramos la imagen
    st.image(ruta_grafica6, width=700)

    # Botón que muestra el comentario
    if st.button("Comentario sobre la gráfica", key="6"):
        st.markdown(
        """
        <div style="text-align: left; border: 1px solid #000000; padding: 10px; background-color: rgba(255, 255, 255, 0.5); color: #000000; box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.5); border-radius: 10px;">
            <b>Comentario:</b><br>
            observamos la abundancia del
            amarillo y del rojo, siendo las dos zonas las que más disponibilidad anual tienen
            pese a tener unos precios más altos.
        </div>
        """, unsafe_allow_html=True)
        
    # Título gráfica
    st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: left; color: #ffffff; font-size: 35px; margin: 0; text-shadow: 6px 6px 6px #000000;'>Precio medio diario para 2 personas</h1></div>", unsafe_allow_html=True)

    # Mostramos la imagen
    st.image(ruta_grafica12, width=700)

    # Botón que muestra el comentario
    if st.button("Comentario sobre la gráfica", key="12"):
        st.markdown(
        """
        <div style="text-align: left; border: 1px solid #000000; padding: 10px; background-color: rgba(255, 255, 255, 0.5); color: #000000; box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.5); border-radius: 10px;">
            <b>Comentario:</b><br>
            precio promedio para dos personas en las diferentes zonas
            siendo Guipúzcoa la que más cara de las tres zonas.
        </div>
        """, unsafe_allow_html=True)
    
    # Título gráfica
    st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: left; color: #ffffff; font-size: 35px; margin: 0; text-shadow: 6px 6px 6px #000000;'>Disponibilidad anual promedio según top 10 localidades más visitadas</h1></div>", unsafe_allow_html=True)

    # Mostramos la imagen
    st.image(ruta_grafica2, width=700)

    # Botón que muestra el comentario
    if st.button("Comentario sobre la gráfica", key="2"):
        st.markdown(
        """
        <div style="text-align: left; border: 1px solid #000000; padding: 10px; background-color: rgba(255, 255, 255, 0.5); color: #000000; box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.5); border-radius: 10px;">
            <b>Comentario:</b><br>
            Podemos ver que ni Bilbao, ni Donostia-San Sebastian, principales ciudades de 
            Euskadi no están entre las tres primeras, siendo Bermeo , Irún y Barakaldo las tres 
            mas elegidas para visitar a lo largo del año.
        </div>
        """, unsafe_allow_html=True)
        
     # Título gráfica
    st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: left; color: #ffffff; font-size: 35px; margin: 0; text-shadow: 6px 6px 6px #000000;'>Top 10 localidades</h1></div>", unsafe_allow_html=True)

    # Mostramos la imagen
    st.image(ruta_grafica13, width=700)

    # Botón que muestra el comentario
    if st.button("Comentario sobre la gráfica", key="13"):
        st.markdown(
        """
        <div style="text-align: left; border: 1px solid #000000; padding: 10px; background-color: rgba(255, 255, 255, 0.5); color: #000000; box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.5); border-radius: 10px;">
            <b>Comentario:</b><br>
            Las localidades con mas cantidad de hospedaje de Airbnb en Euskadi son estas
            10 , siendo Dosnostia, Vitoria-Gasteiz y Bilbao las tres primeras.
        </div>
        """, unsafe_allow_html=True)
        
    # Título gráfica
    st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: left; color: #ffffff; font-size: 35px; margin: 0; text-shadow: 6px 6px 6px #000000;'>Superhost VS No Superhost</h1></div>", unsafe_allow_html=True)

    # Mostramos la imagen
    st.image(ruta_grafica3, width=700)

    # Botón que muestra el comentario
    if st.button("Comentario sobre la gráfica", key="3"):
        st.markdown(
        """
        <div style="text-align: left; border: 1px solid #000000; padding: 10px; background-color: rgba(255, 255, 255, 0.5); color: #000000; box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.5); border-radius: 10px;">
            <b>Comentario:</b><br>
            Hay un mayor porcentaje de No Superhosts en Euskadi respecto a los que son Superhost. Las etiquetas Superhost pueden 
            desaparecer en los próximos años.
        </div>
        """, unsafe_allow_html=True)
        
    # Título gráfica
    st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: left; color: #ffffff; font-size: 35px; margin: 0; text-shadow: 6px 6px 6px #000000;'>Top 10 servicios más comunes</h1></div>", unsafe_allow_html=True)

    # Mostramos la imagen
    st.image(ruta_grafica7, width=700)

    # Botón que muestra el comentario
    if st.button("Comentario sobre la gráfica", key="7"):
        st.markdown(
        """
        <div style="text-align: left; border: 1px solid #000000; padding: 10px; background-color: rgba(255, 255, 255, 0.5); color: #000000; box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.5); border-radius: 10px;">
            <b>Comentario 1:</b><br>
            Top 10 servicios que podemos encontrar en los alojamientos son
            estos , siendo el secador de pelo y el wifi, de los más comunes.
        </div>
        """, unsafe_allow_html=True)
        
    # Título gráfica
    st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: left; color: #ffffff; font-size: 35px; margin: 0; text-shadow: 6px 6px 6px #000000;'>Puntuación media de la comunicación respecto a las 10 propiedades más frecuentadas</h1></div>", unsafe_allow_html=True)

    # Mostramos la imagen
    st.image(ruta_grafica9, width=700)

    # Botón que muestra el comentario
    if st.button("Comentario sobre la gráfica", key="9"):
        st.markdown(
        """
        <div style="text-align: left; border: 1px solid #000000; padding: 10px; background-color: rgba(255, 255, 255, 0.5); color: #000000; box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.5); border-radius: 10px;">
            <b>Comentario 1:</b><br>
        Puntuacion media de la comunicacion segun el tipo de propiedad.
        </div>
        """, unsafe_allow_html=True)
        
    # Título gráfica
    st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: left; color: #ffffff; font-size: 35px; margin: 0; text-shadow: 6px 6px 6px #000000;'>Puntuación media de limpieza por localidad</h1></div>", unsafe_allow_html=True)

    # Mostramos la imagen
    st.image(ruta_grafica10, width=700)

    # Botón que muestra el comentario
    if st.button("Comentario sobre la gráfica", key="10"):
        st.markdown(
        """
        <div style="text-align: left; border: 1px solid #000000; padding: 10px; background-color: rgba(255, 255, 255, 0.5); color: #000000; box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.5); border-radius: 10px;">
            <b>Comentario 1:</b><br>
            Top 10 de ciudades con
            alojamientos más limpios de Euskadi. 
        </div>
        """, unsafe_allow_html=True)
        
    # Título gráfica
    st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: left; color: #ffffff; font-size: 35px; margin: 0; text-shadow: 6px 6px 6px #000000;'>Puntuación media de limpieza por tipo de habitación</h1></div>", unsafe_allow_html=True)

    # Mostramos la imagen
    st.image(ruta_grafica11, width=700)

    # Botón que muestra el comentario
    if st.button("Comentario sobre la gráfica", key="11"):
        st.markdown(
        """
        <div style="text-align: left; border: 1px solid #000000; padding: 10px; background-color: rgba(255, 255, 255, 0.5); color: #000000; box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.5); border-radius: 10px;">
            <b>Comentario:</b><br>
            el tipo de propiedad va directamente ligada a la limpieza de
            las mismas, para ello este gráfico nos muestra la puntuación media por tipo de
            habitación dada la limpieza.
        </div>
        """, unsafe_allow_html=True)
        
        
#---PRUEBAS ESTADÍSTICAS---#

if menu == "Pruebas Estadísticas":
    st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: center; color: #ffffff; font-size: 70px; margin: 0; text-shadow: 6px 6px 6px #000000;'>Pruebas estadísticas 🔢</h1></div>", unsafe_allow_html=True)
    
    url_imagen_fondo_estadistica = "https://media.traveler.es/photos/61377eab70e3cff8b85f9f7f/master/w_1600%2Cc_limit/76275.jpg"

    def add_bg_from_url(url_imagen_fondo_estadistica):
            st.markdown(
                f"""
                <style>
                .stApp {{
                    background-image: url({url_imagen_fondo_estadistica});
                    background-size: cover;
                    background-repeat: no-repeat;
                    background-attachment: fixed;
                }}
                </style>
                """,
                unsafe_allow_html=True)

    add_bg_from_url(url_imagen_fondo_estadistica)
    
    ruta_grafica14 = r"Imágenes\grafica_14.png"
    ruta_grafica15 = r"Imágenes\grafica_15.png"
    ruta_grafica16 = r"Imágenes\grafica_16.png"
    ruta_grafica17 = r"Imágenes\grafica_17.png"
    ruta_grafica18 = r"Imágenes\grafica_18.png"
    ruta_grafica19 = r"Imágenes\grafica_19.png"

    tamaños_imagenes = 700
    
    st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: left; color: #ffffff; font-size: 35px; margin: 0; text-shadow: 6px 6px 6px #000000;'>Shapiro-Wilk ⤵️</h1></div>", unsafe_allow_html=True)

    colshapiro1, colshapiro2, colshapiro3 = st.columns(3)

    # Añadimos las imágenes a la primera columna
    with colshapiro1:
        st.image(ruta_grafica14, width=tamaños_imagenes)
        if st.button("Conocer distribuciones 1"):
            st.write("""
            <div style='color:white;'>
                

                Estadístico=0.8126984792240446, p-value=1.5442788908309796e-65.
                La variable Total_huespedes no sigue una distribución normal.
            </div>
            """, unsafe_allow_html=True)

    # Añadimos las imágenes a la segunda columna
    with colshapiro2:
        st.image(ruta_grafica15, width=tamaños_imagenes)
        if st.button("Conocer distribuciones 2"):
            st.write("""
            <div style='color:white;'>
                

                Estadístico=0.7516819279199426, p-value=3.362563685681209e-71.
                La variable Localización no sigue una distribución normal.
            </div>
            """, unsafe_allow_html=True)
            

    # Añadimos las imágenes a la tercera columna
    with colshapiro3:
        st.image(ruta_grafica16, width=tamaños_imagenes)
        if st.button("Conocer distribuciones 3"):
            st.write("""
            <div style='color:white;'>
                

                Estadístico=0.9486595572349767, p-value=1.2326387211925094e-42.
                La variable Disponibilidad_anual no sigue una distribución normal.
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: left; color: #ffffff; font-size: 35px; margin: 0; text-shadow: 6px 6px 6px #000000;'>chi-cuadrado ⤵️</h1></div>", unsafe_allow_html=True)

    colchicuadrado2, colchicuadrado21 = st.columns(2)

    # Añadimos imágenes a la primera columna
    with colchicuadrado2:
        st.image(ruta_grafica17, width=830)
        if st.button("Conocer distribuciones 1", key='17'):
            st.write("""
            <div style='color:white;'>
                

                Chi-cuadrado: 258.5793445634242 P-value: 0.08023917459207192
                No podemos rechazar la hipótesis nula: Las zonas de Vizcaya y Guipúzcoa son las que tienen más reseñas.
            </div>
            """, unsafe_allow_html=True)

    # Añadimos imágenes a la segunda columna
    with colchicuadrado21:
        st.image(ruta_grafica18, width=tamaños_imagenes)
        if st.button("Conocer distribuciones 2",key='18'):
            st.write("""
            <div style='color:white;'>
                

                Chi-cuadrado: 42.12623083520939 P-value: 7.118773948386667e-10.
                Rechazamos la hipótesis nula: Hay más Superhost en Guipúzcoa que en las otras zonas.
            </div>
            """, unsafe_allow_html=True)
    
        
#---MAPAS---#

if menu == "Mapas":
    st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: center; color: #ffffff; font-size: 70px; margin: 0; text-shadow: 6px 6px 6px #000000;'>Mapas 🗺️</h1></div>", unsafe_allow_html=True)
    
    url_imagen_fondo_mapas = "https://image.lexica.art/full_webp/249c41e9-7e42-40bc-8d02-52270c259922"
    
    st.markdown(
    """
    <div style="background-color: rgba(255, 90, 95, 0.8); padding: 20px; color: #ffffff; font-size: 20px;">
    Este apartado contiene dos mapas interactivos: un mapa de calor con el precio segun localizacion y un mapa de las ubicaciones de las propiedades. Ambos mapas ofrecen como resultado que en la zona mas costeras aumenta la demanda de propiedades y con ello sus precios.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""<div style="margin-bottom: 20px;"></div>""", unsafe_allow_html=True)
    

    def add_bg_from_url(url_imagen_fondo_mapas):
            st.markdown(
                f"""
                <style>
                .stApp {{
                    background-image: url({url_imagen_fondo_mapas});
                    background-size: cover;
                    background-repeat: no-repeat;
                    background-attachment: fixed;
                }}
                </style>
                """,
                unsafe_allow_html=True)

    add_bg_from_url(url_imagen_fondo_mapas)
    
    colmap1, colmap2 = st.columns(2)
    with colmap1:
        st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: left; color: #ffffff; font-size: 35px; margin: 0; text-shadow: 6px 6px 6px #000000;'>Mapa de calor según el precio por localización 🌍</h1></div>", unsafe_allow_html=True)
        # Creamos un mapa respecto a longitud y latitud
        map = folium.Map(location=[listing['Latitud'].mean(), listing['Longitud'].mean()], zoom_start=8.5)

        # Convertimos los datos a formato (lat, lon, precio) y calculamos el promedio de precios
        heat_data = listing[['Latitud', 'Longitud', 'Precio']].groupby(['Latitud', 'Longitud']).mean().reset_index().values.tolist()

        # Añadimos el HeatMap al mapa de Folium
        HeatMap(heat_data).add_to(map)

        # Mostramos el mapa en Streamlit usando folium_static
        folium_static(map)

    with colmap2:
        st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: left; color: #ffffff; font-size: 35px; margin: 0; text-shadow: 6px 6px 6px #000000;'>Mapa de ubiaciones de propiedades 🏠</h1></div>", unsafe_allow_html=True)
        lats2024 = listing['Latitud'].tolist()
        lons2024 = listing['Longitud'].tolist()
        locations = list(zip(lats2024, lons2024))

        # Creamos un mapa con folium con [42.7500, -2.3990] y zoom
        mapa = folium.Map(location=[42.7500, -2.3990], zoom_start=9.48)

        # Añadimos FastMarkerCluster al mapa
        FastMarkerCluster(data=locations).add_to(mapa)

        # Mostramos mapa
        folium_static(mapa)
        

### EASTRER EGG -> st.image('https://pbs.twimg.com/media/E_e8qASXIAE6TCq.jpg')

#---POWER BI---#

if menu == "Power Bi":
    st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: center; color: #ffffff; font-size: 70px; margin: 0; text-shadow: 6px 6px 6px #000000;'>Panel de Power Bi 📈</h1></div>", unsafe_allow_html=True)
    
    power_bi_html = '''
    <iframe title="Euskadi_airbnb" width="1920" height="1080" src="https://app.powerbi.com/view?r=eyJrIjoiYzc3Yzc2NGYtZWMxNy00NTMyLWEwZmYtYTZjNGNhMDU1ZmVhIiwidCI6IjhhZWJkZGI2LTM0MTgtNDNhMS1hMjU1LWI5NjQxODZlY2M2NCIsImMiOjl9" frameborder="0" allowFullScreen="true"></iframe>
    '''

    # Mostramos el iframe en Streamlit usando html
    st.components.v1.html(power_bi_html, width=1920, height=1080)
        
#---CONCLUSIÓN---#

if menu == "Conclusión":
    st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: center; color: #ffffff; font-size: 70px; margin: 0; text-shadow: 6px 6px 6px #000000;'>Conclusión 🏁</h1></div>", unsafe_allow_html=True)
    
    url_imagen_fondo_conclusion = "https://www.cuadrilladeanana.es/wp-content/uploads/2024/03/viajar-al-Pais-Vasco-2.jpg"

    def add_bg_from_url(url_imagen_fondo_conclusion):
            st.markdown(
                f"""
                <style>
                .stApp {{
                    background-image: url({url_imagen_fondo_conclusion});
                    background-size: cover;
                    background-repeat: no-repeat;
                    background-attachment: fixed;
                }}
                </style>
                """,
                unsafe_allow_html=True)
    add_bg_from_url(url_imagen_fondo_conclusion)
    
    colconclusion1, colconclusion2 = st.columns(2)
    
    with colconclusion1:
        
        st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: left; color: #ffffff; font-size: 35px; margin: 0; text-shadow: 6px 6px 6px #000000;'>Mapa de correlación de variables 🌡️</h1></div>", unsafe_allow_html=True)
        
        ruta_grafica19 = r'Imágenes\grafica_19.png'
        st.image(ruta_grafica19,width=800)
        
        st.markdown(
    """
    <div style="background-color: rgba(255, 90, 95, 0.8); padding: 20px; color: #ffffff; font-size: 20px;">
    El gráfico de correlación no siendo una distribución normal y según Spearman no 
    hace suposiciones sobre la distribución de las variables y mide la correlación 
    monótona entre ellas.
    Podemos observar que las variables mejor relacionadas o con una relación 
    moderada son las que superan el 0.6 en valores absolutos y siendo una correlación 
    monótona leve las que se encuentran por debajo de este umbral.
    </div>
    """, unsafe_allow_html=True)
        
    with colconclusion2:
        st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: left; color: #ffffff; font-size: 35px; margin: 0; text-shadow: 6px 6px 6px #000000;'>Ejemplos reales de apartamentos en Euskadi 🏘️</h1></div>", unsafe_allow_html=True)
        
        airbnb_conclusion_foto = (r'Imágenes\airbnb_fotos_euskadi.PNG')
        
        st.image(airbnb_conclusion_foto,width=975)
    
        st.markdown("""<div style="margin-bottom: 20px;"></div>""", unsafe_allow_html=True)
    
        st.markdown(
    """
    <div style="background-color: rgba(255, 90, 95, 0.0); padding: 20px; color: #ffffff; font-size: 20px;">
    </div>
    """, unsafe_allow_html=True)
        
        st.markdown(
    """
    <div style="background-color: rgba(255, 90, 95, 0.0); padding: 20px; color: #ffffff; font-size: 20px;">
    </div>
    """, unsafe_allow_html=True)
        
        st.markdown(
    """
    <div style="background-color: rgba(255, 90, 95, 0.0); padding: 20px; color: #ffffff; font-size: 20px;">
    </div>
    """, unsafe_allow_html=True)
        
        st.markdown(
    """
    <div style="background-color: rgba(255, 90, 95, 0.0); padding: 20px; color: #ffffff; font-size: 20px;">
    </div>
    """, unsafe_allow_html=True)
        

        st.markdown(
    """
    <div style="background-color: rgba(255, 90, 95, 0.8); padding: 20px; color: #ffffff; font-size: 20px;">
    Como conclusión podemos observar que Euskadi no es una de las regiones de España donde Airbnb ha tenido un gran exito frente a otras, pues según la página “IsideAirbnb” se encuentra la penúltima 
    del ranking con más alojamientos de Airbnb en España. 
    Esto indica que la parte norte de España todavía está lejos de ser una de las zonas 
    o regiones más visitadas por el turismo en España pese al incremento de alojamientos mencionados al principio de la presentacion.
    </div>
    """, unsafe_allow_html=True)
        
    st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: left; color: #ffffff; font-size: 35px; margin: 0; text-shadow: 6px 6px 6px #000000;'>Palabras de reseñas ⭐</h1></div>", unsafe_allow_html=True)
    
    ruta_graficafinal = r'Imágenes\palabras_reseñas.png'
    st.image(ruta_graficafinal,width=900)

    if st.button('Eskerrik asko, agur 👋', key='123', help=None, on_click=None, args=None, kwargs=None, use_container_width=True):
        meme = (r'Imágenes\meme.jpg')
        st.image(meme, width=700) 