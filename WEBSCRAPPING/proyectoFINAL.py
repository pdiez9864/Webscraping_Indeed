from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from datetime import date
import pandas as pd
import re
from bs4 import BeautifulSoup
from datetime import date
import warnings
#para poder quitar los warning de la terminal:
warnings.simplefilter(action='ignore', category=DeprecationWarning)
warnings.simplefilter(action='ignore', category=FutureWarning)



def proyecto(puesto):
    """
    Descripcion: Código para realizar webscrapping de la página web indeed, obtendremos información de las
    ofertas de trabajo de un puesto en específico, posteriormente exportaremos a un csv

        Input:
        Puesto: Indica el empleo que estamos buscando.
        puesto="Data Scientist"
        Webdriver: Indica el path donde se encuentra el ejecutor del explorador, en nuestro caso se ha utilizado chrome.
        driver = webdriver.Chrome("C:/Users/Olalla/Downloads/chromedriver/chromedriver")
        driver.get(r'https://es.indeed.com/jobs?q&l=Madrid%2C%20Madrid%20provincia')
        Output: Devolvera un Dataframe con las siguientes columnas :
        Puesto, Ubicacion, Compañia, Publicado, Fecha_busqueda, Jk, Efccid, Srcid, Cmpid.
    """

    #VARIABLE DEL DIA DE HOY QUE UTILIZAREMOS PARA SABER  LA FECHA DE BUSQUEDA.
    today = date.today().strftime("%d/%m/%Y")
    #LISTA CON LOS DATOS QUE VAMOS A USAR
    datos=[]

    #ABRIR INDEED
    driver = webdriver.Chrome(r"C:\Users\Olalla\Downloads\chromedriver\chromedriver")
    driver.get(r'https://es.indeed.com/jobs?q&l=Madrid%2C%20Madrid%20provincia')
    #RECHAZAR TODAS LAS COOKIES
    driver.find_element_by_xpath('//*[@id="onetrust-reject-all-handler"]').click()
    #BUSCAR DATA SCIENTIST
    driver.find_element_by_id("text-input-what").send_keys(puesto)
    driver.find_element_by_xpath('//*[@id="jobsearch"]/button').click()

    #CONSTRUIMOS UN SCROLL PARA RECORRER TODA LA PÁGINA,(TODAVÍA SIN LA OBTENCIÓN DE LOS DATOS).
    iter = 1
    while True:
        scrollHeight = driver.execute_script("return document.documentElement.scrollHeight")
        Height = 250 * iter
        driver.execute_script("window.scrollTo(0, " + str(Height) + ");")

        if Height > scrollHeight:
            print('End of page')
            break

        iter += 1
    #CREAMOS UN BUCLE QUE RECORRA LAS PRIMERAS 4 PÁGINAS.
    URL_BASE=driver.current_url
    #creamos un try y except por si en la busqueda se introduce un puesto el cual no existiera.
    try:
        base, location, vjk = URL_BASE.split('&')
    except:
        print ("no hay busquedas")
        exit()
        
    #CREAMOS UN BUCLE QUE RECORRA LAS PRIMERAS 4 PÁGINAS.
    URL_BASE=driver.current_url
    
    for i in range(0, 4):
        if i > 0:
            #CONSTRUIMOS LA URL QUE REALIZA EL CAMBIO DE PÁGINA MODIFICANDO DICHA URL.
            base, location , vjk = URL_BASE.split('&')
            url = '&'.join([base, location, 'start='+str(i*10)])
            driver.get(url)
            iter = 1
            #EL MISMO SCROLL QUE HEMOS REALIZADO ANTES PERO DENTRO DEL BUCLE PARA QUE LO HAGA EN TODAS LAS PÁGINAS
            while True:
                scrollHeight = driver.execute_script("return document.documentElement.scrollHeight")
                Height = 250 * iter
                driver.execute_script("window.scrollTo(0, " + str(Height) + ");")

                if Height > scrollHeight:
                    print('End of page')
                    break
                iter += 1
            #TRAER DATOS DE INDEED
            src = driver.page_source
            bs = BeautifulSoup(src,"html.parser")
            buscador = re.findall('jobmap.[[0-9]+]=.*', str(bs))
            #YA QUE LA FECHA DE PUBLICACIÓN NO ESTA EN LA MISMA CLASE QUE LOS DEMÁS DATOS, LA EXTRAEMOS, INDICANDOLO POSTERIORMENTE CON LA VARIABLE POSTED.
            posted = bs.find_all('span', attrs={'class': 'date'})
            #A CONTINUACION CON ESTE BUCLE RECORREMOS TODOS LOS DATOS Y ESCOGEMOS LOS CAMPOS QUE NECESITAMOS
            for item, a in zip(buscador, posted):
                # PUESTO
                puesto = re.findall(r'title:.*,locid:', item)[0].split(':')[1].split(',')[0][1:-1]
                # UBICACION
                ubicacion = re.findall(r'loc:.*,country:', item)[0].split(':')[1].split(',')[0]
                # COMPAÑIA
                compañia = re.findall(r'srcname:.*,cmp:', item)[0].split(':')[1].split(',')[0][1:-1]
                # PUBLICADO
                publicado=a.text.strip().replace('Posted', '').replace("hace","").replace(" días","").replace("+ días","").replace(" día","")
                # FECHA BUSQUEDA
                today
                # JK
                jk = re.findall(r'jk:.*,efccid:', item)[0].split(':')[1].split(',')[0][1:-1]
                # EFCCID
                efccid = re.findall(r'efccid:.*,srcid:', item)[0].split(':')[1].split(',')[0][1:-1]
                # SRCID
                srcid = re.findall(r'srcid:.*,cmpid:', item)[0].split(':')[1].split(',')[0][1:-1]
                # CMPID
                cmpid = re.findall(r'cmpid:.*,num:', item)[0].split(':')[1].split(',')[0][1:-1]
                #LAS VARIALES QUE CREAMOS ANTERIORMENTE CON EL CONTENIDO DE LOS CAMPOS, LAS INTRODUCIMOS EN UNA LISTA
                datos.append([puesto, ubicacion, compañia, publicado, today, jk, efccid, srcid, cmpid])
        #UNA VEZ QUE HEMOS REALIZADO LO NECESARIO EN LOS SALTOS DE PAGINA ES DECIR (pagina 2,3,4, LO REALIZAMOS EN LA PAGINA PRINCIPAL.
        else:
            #TRAER DATOS
            src = driver.page_source
            bs = BeautifulSoup(src,"html.parser")

            buscador = re.findall('jobmap.[[0-9]+]=.*', str(bs))
            posted = bs.find_all('span', attrs={'class': 'date'})
            for item,a in zip(buscador,posted):
                #PUESTO
                puesto= re.findall(r'title:.*,locid:', item)[0].split(':')[1].split(',')[0][1:-1]
                #UBICACION
                ubicacion= re.findall(r'loc:.*,country:', item)[0].split(':')[1].split(',')[0]
                #COMPAÑIA
                compañia=re.findall(r'srcname:.*,cmp:', item)[0].split(':')[1].split(',')[0][1:-1]
                #PUBLICADO
                publicado = a.text.strip().replace('Posted', '').replace("hace", "").replace(" días", "").replace("+ días", "").replace(" día", "")
                #FECHA BUSQUEDA
                today
                #JK
                jk=re.findall(r'jk:.*,efccid:', item)[0].split(':')[1].split(',')[0][1:-1]
                #EFCCID
                efccid=re.findall(r'efccid:.*,srcid:', item)[0].split(':')[1].split(',')[0][1:-1]
                #SRCID
                srcid=re.findall(r'srcid:.*,cmpid:', item)[0].split(':')[1].split(',')[0][1:-1]
                #CMPID
                cmpid=re.findall(r'cmpid:.*,num:', item)[0].split(':')[1].split(',')[0][1:-1]
                datos.append([puesto,ubicacion,compañia,publicado,today,jk,efccid,srcid,cmpid])
    #CREAMOS UN DATAFRAME CON LOS DATOS QUE HEMOS SELECCIONADO, INDICANDO LOS NOMBRES DE LAS COLUMNAS.
    dataframe=pd.DataFrame(datos,columns=["puesto", "ubicacion", "compañia", "publicado", "fecha_publicacion", "jk", "efccid", "srcid", "cmpid"])
    #MOSTRAMOS DATAFRAME
    print(dataframe)
    #PASAMOS DICHO DATAFRAME A CSV.
    dataframe.to_csv("proyectoBUENO.csv", encoding='utf-8', index=False)
    driver.close()
    #LLAMAMOS A LA FUNCION.
if  __name__ ==  '__main__' :
    puesto='Data Scientist'
    proyecto(puesto)

