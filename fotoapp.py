from PIL import Image,ImageFilter,ImageDraw
import matplotlib.pyplot as mpl
import cv2 as opencv
import os #para poder verificar la existencia de rutas o archivos

rutaImagenes = ""

def mostrarImgMPL(img,figsize=(10,10)):
    fig,ax = mpl.subplots(figsize=figsize)
    ax.set_axis_off()
    ax.set_frame_on(False)
    ax.imshow(img)

def establecerRutaImagenes(ruta:str)->bool:
    global rutaImagenes
    if os.path.isdir(ruta):
        rutaImagenes = ruta
        #la ruta siempre debe terminar con / para que podamos concatenarla con el nombre de la imagen
        if not rutaImagenes[-1] == "/":
            rutaImagenes+="/"
        return True
    return False

#1
dimensionesReferencia = {
    'youtube':(1280,720),
    'instagram':(320,320),
    'twitter':(1000,300),
    'facebook':(400,500)
}

def redimensionarImg(nombreImg:str,formato:str):
    dimensiones = dimensionesReferencia.get(formato.lower())
    if dimensiones is None:
        return None
    imgRedimensionar = Image.open(rutaImagenes+nombreImg)
    imgRedimensionar = imgRedimensionar.resize(dimensiones)
    return imgRedimensionar


#2
def ajustarHistograma(nombreImg:str):
    imgOriginal = opencv.imread(rutaImagenes+nombreImg,opencv.IMREAD_GRAYSCALE)
    img = opencv.equalizeHist(imgOriginal)
    #convirtiendolas a imagenes de pillow
    imgOriginal = Image.fromarray(imgOriginal)
    img = Image.fromarray(img)
    imgCombinada = Image.new("RGB",(img.size[0]*2,img.size[1]),(1,1,1))
    imgCombinada.paste(imgOriginal,(0,0))
    imgCombinada.paste(img,(img.size[0],0))

    mpl.rcParams['image.cmap'] = 'gray'
    mostrarImgMPL(imgCombinada)
    imgCombinada.save(rutaImagenes + "Hist_" + nombreImg)
    #return imgCombinada


#3
filtros = {
    "none":None,
    "blur":ImageFilter.BLUR,
    "contour":ImageFilter.CONTOUR,
    "detail":ImageFilter.DETAIL,
    "edge_enhance":ImageFilter.EDGE_ENHANCE,
    "edge_enhance_more":ImageFilter.EDGE_ENHANCE_MORE,
    "emboss":ImageFilter.EMBOSS,
    "find_edges":ImageFilter.FIND_EDGES,
    "sharpen":ImageFilter.SHARPEN,
    "smooth":ImageFilter.SMOOTH
}

columnasImagen = 2
def aplicarFiltroImagen(nombreImg:str,filtroElegido:str):
    imgOriginal = Image.open(rutaImagenes+nombreImg)
    dimensiones = imgOriginal.size
    imgCombinada = Image.new("RGB",(dimensiones[0]*2,dimensiones[1]*5),(1,1,1))
    columna = 0
    fila = 0
    for nombreFiltro, filtro in zip(filtros.keys(),filtros.values()):
        imgFiltrada = not filtro and imgOriginal.copy() or imgOriginal.filter(filtro)
        textoFiltro = not filtro and "Original" or nombreFiltro.capitalize()
        colorTexto = filtro and nombreFiltro.lower() == filtroElegido.lower() and (0,255,0) or (255,0,0)
        draw = ImageDraw.Draw(imgFiltrada)
        draw.text((0, 0), textoFiltro, colorTexto, font_size=dimensiones[1]/12)
        imgFiltrada = draw._image
        imgCombinada.paste(imgFiltrada, (dimensiones[0] * columna, dimensiones[1] * fila))
        if columna == columnasImagen-1:
            columna = 0
            fila += 1
        else:
            columna += 1

    mpl.rcParams['image.cmap'] = 'viridis'
    mostrarImgMPL(imgCombinada)
    imgCombinada.save(rutaImagenes + "Filtrada_" + nombreImg)
    #return imgCombinada

#4
def buscarBoceto(nombreImg:str):
    img = opencv.imread(rutaImagenes+nombreImg,opencv.IMREAD_GRAYSCALE)
    img = opencv.Canny(img,110,150)
    img = Image.fromarray(img)

    mpl.rcParams['image.cmap'] = 'gray'
    mostrarImgMPL(img)
    img.save(rutaImagenes + "Boceto_" + nombreImg)
    #return img


#5
def menuMain():
    print("Bienvenido a la aplicacion de FotoApp. Antes de comenzar, debemos establecer la ruta donde estan sus imagenes.")
    while not establecerRutaImagenes(input("Ingrese la ruta de imagenes (./ para ruta actual): ")):
        print("Ruta invalida")

    print("Ahora, debemos establecer la imagen con la cual vamos a trabajar")
    nombreImagen = input("Ingrese el nombre de la imagen a procesar (extension incluida): ")
    while not os.path.isfile(rutaImagenes+nombreImagen):
        print("Nombre invalido")
        nombreImagen = input("Ingrese el nombre de la imagen a procesar: ")

    print("Ahora, debemos redimensionar la imagen acorde a alguno de los formatos disponibles")
    print("Formatos disponibles:")
    for nombreFormato in dimensionesReferencia:
        print("\t"+nombreFormato)
    formatoImagen = input("\nIngrese el formato de la imagen: ")
    imgRedimensionada = redimensionarImg(nombreImagen,formatoImagen)
    while not imgRedimensionada:
        print("Formato invalido")
        formatoImagen = input("\nIngrese el formato de la imagen: ")
        imgRedimensionada = redimensionarImg(nombreImagen, formatoImagen)

    imgRedimensionada.save(rutaImagenes+formatoImagen.lower()+"_"+nombreImagen)
    nombreImagen = formatoImagen.lower()+"_"+nombreImagen

    opcionEditarImg = ""
    while opcionEditarImg != "4":
        print("\nQue quiere hacer ahora con la imagen?")
        print("1. Normalizar histograma")
        print("2. Filtrar imagen")
        print("3. Buscar bordes")
        print("4. Salir del programa")
        opcionEditarImg = input("Ingrese una opcion: ")
        match opcionEditarImg:
            case "1":
                ajustarHistograma(nombreImagen)
            case "2":
                print("Filtros disponibles: ")
                for nombreFiltro in filtros.keys():
                    print("\t"+nombreFiltro)
                nombreFiltro = input("Ingrese el filtro que desea: ")
                aplicarFiltroImagen(nombreImagen,nombreFiltro)
            case "3":
                buscarBoceto(nombreImagen)
            case "4":
                break
            case _:
                pass
