#Version utilizada: python 3.1
import tkinter as tk
import tkinter.font as tkFont
import random
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
import cv2
import imutils
import os

datos_sesion=["",""]
nombre_introducido=False

def elegir_video(gano,empato):
    eleccion=""
    pov=""
    if gano==True:
        eleccion = "carpeta_datos/videos/jugador_gana/"
        pov = random.choice(os.listdir("carpeta_datos/videos/jugador_gana/"))
        eleccion += pov
        eleccion +="/"+random.choice(os.listdir(eleccion))
    
    elif gano==False:
        eleccion = "carpeta_datos/videos/jugador_pierde/"
        pov = random.choice(os.listdir("carpeta_datos/videos/jugador_pierde/"))
        eleccion += pov
        eleccion +="/"+random.choice(os.listdir(eleccion))
    elif empato==True:
        eleccion = "carpeta_datos/videos/jugador_empata/"
        pov = random.choice(os.listdir("carpeta_datos/videos/jugador_pierde/"))
        eleccion += pov
        eleccion +="/"+random.choice(os.listdir(eleccion))

    pov = pov.replace("_"," ")
    pov = pov.upper()
    return eleccion,pov
    

def abrir_ventana_camara(eleccion,pov):
    ventana_camara = tk.Toplevel()
    ventana_camara.title("Ventana camara")
    global cap

    video_path = eleccion
    cap = cv2.VideoCapture(video_path)

    label_info = tk.Label(ventana_camara, text=pov,font=("Impact", 24),foreground="red")
    label_info.grid(column=0,row=0)

    label_video = tk.Label(ventana_camara)
    label_video.grid(column=0,row=2,columnspan=2)
    def visualizar_video():
        global cap
        ret, frame = cap.read()
        if ret == True:
            frame = imutils.resize(frame, width=280)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)

            label_video.configure(image=img)
            label_video.image = img
            label_video.after(13,visualizar_video)
        else:
            label_video.image = ""
            cap.release()
            ventana_camara.destroy()
    visualizar_video()

def abrir_ventana_usuario():#Ventana secundaria donde se introduce el nombre de usuario
    
    ventana_usuario = tk.Toplevel()
    ventana_usuario.title("Nombre de usuario")
    ventana_usuario.configure(background="dark slate gray")

    #Label de bienvenida:
    label_cartel_1=tk.Label(ventana_usuario,text="Ingresa tu nombre de usuario!",foreground="yellow",background="dark slate gray",font=("Gabriola", 20))
    label_cartel_1.grid(column=0, row=0)

    #Label de informacion:
    label_cartel_2=tk.Label(ventana_usuario,text="\n\n\n\nEste nombre se utilizara para guardar\n tu record de fichas y podra ser visto por\n los demas usuarios en el Scoreboard\n elige con cuidado!",foreground="white",background="dark slate gray",font=("Lucida Grande",10))
    label_cartel_2.grid(column=0, row=3)

    entrada_nombre=tk.Entry(ventana_usuario, width=14, textvariable="Sapos", background="purple",foreground="white",insertbackground="white",font=("Lucida Grande", 14))
    entrada_nombre.grid(column=0, row=1)
    
    def guardar():#Funcion del boton guardar el nombre
        #Si el nombre introducido no esta vacio y ocupa menos de 20 caracteres:
        if entrada_nombre.get() != "" and len(entrada_nombre.get()) <20:
            global datos_sesion
            global nombre_introducido

            datos_sesion[0] = entrada_nombre.get()
            nombre_introducido=True

            #Luego de 1 segundo cerrar la ventana:
            ventana_usuario.after(1000)
            abrir_ventana_scoreboard()
            ventana_usuario.destroy()

    #Declarando el boton guardar de esta ventana secundaria:
    botonGuardar=tk.Button(ventana_usuario, width=14, text="Guardar nombre",background="black",foreground="white",font=("Lucida Grande", 10),command=guardar)
    botonGuardar.grid(column=0, row=2)


def abrir_ventana_scoreboard():#Ventana del scoreboard
    ventana_scoreboard = tk.Toplevel()
    ventana_scoreboard.title("Ventana secundaria")
    ventana_scoreboard.configure(background="dark slate gray")

    lineas_texto_modificado =[]
    n=2
    
    #se leen los datos del archivo "records" y se guardan en la variable "lineas_texto"
    archivo_records = open("carpeta_datos/records.txt","r")
    lineas_texto=archivo_records.read()
    archivo_records.close()

    #Se dividen los datos y se guardan en "lineas_texto_separado" en forma de lista:
    lineas_texto_separado = lineas_texto.split()

    #Por cada palabra en "lineas_texto_separado" se da una vuelta (un ciclo):
    for palabra in lineas_texto_separado:

        #si "n" es par es porque esta leyendo un nombre en la lista
        #Si no es par es porque esta leyendo el record del nombre
        #Esto funciona asi por como estan ordenados los datos en el archivo:
        
        if n % 2 == 0:
            lineas_texto_modificado.append(palabra+": ")
        else:
            lineas_texto_modificado.append(palabra+"\n\n")
        #cada vez que se da un ciclo a "n" se le suma 1    
        n+=1
        
    #luego de procesar la lista "lineas_texto_modificado" se transforma en un string:
    lineas_texto_final = " ".join(lineas_texto_modificado)

    #label donde se muestran los datos del archivo ya procesados:
    label_records=tk.Label(ventana_scoreboard,text=lineas_texto_final,foreground="white",background="dark slate gray",font=("Segoe Script", 14))
    label_records.grid(column=0, row=1)

    #label del titulo
    label_scoreboard=tk.Label(ventana_scoreboard,text="~~~~~~~~~~~~~~Scoreboard~~~~~~~~~~~~~~",foreground="yellow",background="dark slate gray",font=("Gabriola", 20))
    label_scoreboard.grid(column=0, row=0)



def carta_aleatoria(): #Devuelve una carta aleatoria para el jugador:
    return random.randint(1,10)

def carta_aleatoria_skynet(total_skynet):#Devuelve una carta aleatoria para sktnet:
    #se genera un numero entre 1 y 11:
    carta_generada=random.randint(1,11)

    #leer las reglas del juego para entender lo siguiente:
    #Si el numero generado es igual a 11 (as):
    if carta_generada==11:
        #Si con 11 se pasa de 21:
        if carta_generada + total_skynet>21:
            #se transforma en 1 para que no se pase de 21:
            carta_generada=1

    return carta_generada

def convertir_carta(carta): #Si es necesario, a partir de el numero de la carta generada devuelve una letra:
    if carta==10:
        return random.choice(["Q","J","K"])
    
    #si la carta vale 1 o 11 (11 solo para skynet):
    elif carta==1 or carta==11:
        return "A"
    
    else:
        return carta

def actualizar_record(lista_datos):#Actualiza el scoreboard con el nuevo record:   
    archivo_records = open("carpeta_datos/records.txt","r")
    lineas_texto=archivo_records.read()
    archivo_records.close()

    lineas_texto_separado = lineas_texto.split()
    
    #si el record que se quiere agregar es de alguien que ya estaba en el scoreboard:
    if datos_sesion[0] in lineas_texto_separado:
        
        #se busca las fichas que tenia en el scoreboard:
        posicion = (lineas_texto_separado.index(datos_sesion[0])+1)
        record_anterior = lineas_texto_separado[posicion]

        #se compara el record anterior con el record que se quiere agregar
        #Si el record actual es mejor que el de antes se actualiza:
        if int(datos_sesion[1])>int(record_anterior):
            #se sobreescribe el record:
            lineas_texto_separado.pop(posicion)
            lineas_texto_separado.insert(posicion,datos_sesion[1])

            #se junta todo en un string y se guarda en el archivo:
            lineas_texto_final = " ".join(lineas_texto_separado)
            archivo_records = open("carpeta_datos/records.txt","w")
            archivo_records.write(lineas_texto_final)
            archivo_records.close()

    #Si el jugador no estaba en el scoreboard:
    else:
        #se agregan los nuevos datos a la lista:
        lineas_texto_separado.extend(datos_sesion)
                
        #se transforma la lista anterior en un string
        lineas_texto_final = " ".join(lineas_texto_separado)

        #se guarda el string y se guardan en el archivo
        archivo_records = open("carpeta_datos/records.txt","w")
        archivo_records.write(lineas_texto_final)
        archivo_records.close()

#============
#Ventana principal:
class Aplicacion:
    def __init__(self):
        self.ventana1=tk.Tk()
        self.ventana1.title("Blackjack")
        self.ventana1.configure(background="black")

        #Fuentes que se utilizaran en diferentes labels:
        fuente=tkFont.Font(family="Lucida Grande",size=18)
        fuente_2=tkFont.Font(family="Lucida Grande",size=20)
        fuente_3=tkFont.Font(family="Impact",size=12)
        fuente_4=tkFont.Font(family="Segoe Script",size=16)
        
        #========================
        #Declarando las variables de skynet y del jugador: 

        #Variables donde se guardaran que numero vale cada carta de Skynet:
        self.lista_cartas_skynet=[]
        self.lista_labels_skynet=[]

        self.lista_cartas_jugador=[]
        self.lista_labels_jugador=[]

        #Variable donde se sumaran las cartas de skynet:
        self.total_cartas_skynet=0

        #Variable donde se sumaran las cartas del jugador:
        self.total_cartas_jugador=0


        #Variable donde se guardaran las fichas del jugador:
        self.fichas_jugador=100

        #Variable donde se guardara la apuesta que hizo el jugador
        self.apuesta=tk.StringVar(value="10")

        #Variable en la que se ira guardando el record de fichas obtenidas
        self.record=tk.StringVar(value=str(self.fichas_jugador))

        #========================
        #Variable contador que se usara en el boton pedir
        #Se usa para saber a que carta asignarle el nuevo valor
        self.contador= 0

        #Variable donde se guardara la cantidad de Ases que tenga el jugador
        #Se usa en el boton cambiar:        
        self.total_A = 0

        #========================
        #Variables Booleanas(Verdadero o Falso):
        self.se_ha_apostado=tk.BooleanVar(value=False)
        self.jugador_gano=tk.BooleanVar(value=False)
        self.jugador_empato=tk.BooleanVar(value=False)
        self.continuar=tk.BooleanVar(value=False)#cambia el boton pedir por continuar
        

        #========================
        #Declarando las labels donde se mostraran por pantalla las cartas:

        for i in range (5):
            self.label_carta=tk.Label(self.ventana1,text="  ", background="brown",foreground="white",font=fuente)

            self.label_carta.grid(column=i+1, row=0)
            self.lista_labels_skynet.insert(i,self.label_carta)

            self.label_carta_jugador=tk.Label(self.ventana1,text="  ", background="brown",foreground="white",font=fuente)
            self.label_carta_jugador.grid(column=i+1, row=5)
            self.lista_labels_jugador.insert(i,self.label_carta_jugador)

        #Label donde se mostrara el total de Skynet 
        self.suma_total_skynet_label=tk.Label(self.ventana1,foreground="red", background="black",font=fuente_2, relief="solid")
        self.suma_total_skynet_label.grid(column=6, row=0)

        #Label donde se mostrara la suma total de las cartas del jugador
        self.suma_total_jugador_label=tk.Label(self.ventana1,text="Total: 0",foreground="white", background="black",font=fuente_2)
        self.suma_total_jugador_label.grid(column=0, row=9)

        #Label donde se mostrara el resultado(si gano, ubo un empate o perdio):
        self.resultado_label=tk.Label(self.ventana1,text=" \n ",foreground="white", background="black",font=fuente_3)
        self.resultado_label.grid(column=0, row=10)

        #Label donde se mostraran las fichas que tiene el jugador:
        self.label_fichas_jugador=tk.Label(self.ventana1,text=str(self.fichas_jugador)+" fichas",background="black",foreground="white",font=fuente_4)
        self.label_fichas_jugador.grid(column=3, row=7)

        #Label donde se motrara el record de la sesion actual:
        self.label_record=tk.Label(self.ventana1,text="Record actual: "+self.record.get(),background="black",foreground="white")
        self.label_record.grid(column=6,row=9)

        #=================
        #labels extra invisibles para que no parezca que esta todo muy junto
        self.label_extra_1=tk.Label(self.ventana1,text="aaaaa", background="black",font=fuente)
        self.label_extra_1.grid(column=2, row=1)
        self.label_extra_2=tk.Label(self.ventana1,text="aaaaa\n\n\n\n\n", background="black",font=fuente_4)
        self.label_extra_2.grid(column=4, row=6)

        #label que estara entre las cartas de skynet y las del jugador (Blackjack!)
        self.label1=tk.Label(self.ventana1,text="Blackjack!",foreground="white",background="black",font=fuente_4)
        self.label1.grid(column=3, row=2)
        

        #============
        #Declarando botones

        #Boton para que Skynet le de cartas al jugador:
        self.botonPedir=tk.Button(self.ventana1,width=20,  text="Pedir", command=self.pedir,font=fuente_4)
        self.botonPedir.grid(column=0, row=7)


        #Boton para quedarse con las cartas obtenidas y saber el resultado del juego:
        self.botonQuedarse=tk.Button(self.ventana1,width=20,background="grey", text="Quedarse", command=self.quedarse,font=fuente_4,state=tk.DISABLED)
        self.botonQuedarse.grid(column=6, row=7)
        
        #Boton para cambiar un As por un 11
        self.botonCambiar=tk.Button(self.ventana1,width=10,height=1,  text="Cambiar", command=self.cambiar,font=fuente,background="black",borderwidth=0,state=tk.DISABLED)
        self.botonCambiar.grid(column=0, row=8)

        #Boton para ver los records 
        self.botonRecords=tk.Button(self.ventana1,width=10,  text="Scoreboard",background="dark slate gray",foreground="yellow",font=("Segoe Script", 14), command=self.record_boton)
        self.botonRecords.grid(column=6, row=10)
        
        #Entrada donde el jugador escribira por teclado la apuesta que desea hacer
        self.entrada_apuesta=tk.Entry(self.ventana1, width=6,font=fuente_4, textvariable=self.apuesta,background="purple",foreground="white",insertbackground="white",borderwidth=5,justify=tk.CENTER)
        self.entrada_apuesta.grid(column=3, row=8)

        
        self.ventana1.mainloop()
        
#============
    def record_boton(self):#Boton Ingresar / mostrar Scoreboard

        #si el jugador aun no ha ingresado su usuario:
        if nombre_introducido==False:
            #se abre la ventana para que ingrese su usuario:
            abrir_ventana_usuario()

            #el boton ingresar cambia a boton Scoreboard:
            

        #Si el jugador ya ingreso su nombre:
        else: 
            abrir_ventana_scoreboard()

    def pedir(self):#Boton pedir otra carta
        #Habilitar boton quedarse:
        self.botonPedir.configure(foreground="black")
        self.botonQuedarse.configure(state=tk.NORMAL,background="white")

        #Comprobar si ya se habia apostado:
        if self.se_ha_apostado.get()==False:

            #Si se ha apostado y si se ha hecho correctamente procesar la apuesta:
            if int(self.apuesta.get()) > 0 and int(self.apuesta.get()) <= self.fichas_jugador and self.fichas_jugador>0:
                #se resta lo apostado a la cantidad total de fichas:
                self.fichas_jugador-=int(self.apuesta.get())
                #se actualiza el label:
                self.label_fichas_jugador.configure(text=str(self.fichas_jugador)+" fichas")

                self.se_ha_apostado.set(True)
                #se desactiva la entrada de la apuesta:
                self.entrada_apuesta.configure(state=tk.DISABLED)

        #=================
        if self.contador==0:#Cuando empiece el juego te da otra mas, asi son dos (reglas)
            self.lista_cartas_jugador.insert(self.contador,carta_aleatoria())
            self.lista_labels_jugador[self.contador].config(text=convertir_carta(self.lista_cartas_jugador[self.contador]),background="white",foreground="black")
            
            if self.lista_cartas_jugador[self.contador] ==1:
                self.total_A += 1
                self.lista_labels_jugador[self.contador].config(background="yellow")
            self.contador+=1
        
        if self.contador<5:
            self.lista_cartas_jugador.insert(self.contador,carta_aleatoria())
            self.lista_labels_jugador[self.contador].config(text=convertir_carta(self.lista_cartas_jugador[self.contador]),background="white",foreground="black")
            if self.lista_cartas_jugador[self.contador] ==1:
                self.total_A += 1
                self.lista_labels_jugador[self.contador].config(background="yellow")
        self.total_cartas_jugador=sum(self.lista_cartas_jugador)
                    
        #Si se detecta que hay ases se activa el boton cambiar    
        if self.total_A > 0:
            self.botonCambiar.configure(state=tk.NORMAL,background="yellow")

        #Se actualiza el total de las cartas del jugador:
        self.suma_total_jugador_label.configure(foreground="white",text="Total: "+str(self.total_cartas_jugador))

        #Si el total llega justo a 21:
        if self.total_cartas_jugador ==21:
            self.suma_total_jugador_label.configure(foreground="lightgreen")
            self.botonQuedarse.configure(background="purple",foreground="white")

        #contador que se le suma 1 cada vez que se presione el boton pedir:
        if self.contador < 5:
            self.contador+=1

    def cambiar(self):#Boton Cambiar ases por 11
        #Comprobar cual carta es la que tiene el As para asignarle el 10
        indice = self.lista_cartas_jugador.index(1)
        self.lista_cartas_jugador.pop(indice)
        self.lista_cartas_jugador.insert(indice,11)
        self.lista_labels_jugador[indice].config(text=11,background="white")
        
        #Restar 1 al contador de Ases
        self.total_A-=1

        #Corregir el resultado al total
        self.total_cartas_jugador+=10
        self.suma_total_jugador_label.configure(text="Total: "+str(self.total_cartas_jugador))

        #Si con el cambio llega justo a 21:
        if self.total_cartas_jugador ==21:
            self.suma_total_jugador_label.configure(foreground="lightgreen")
            self.botonQuedarse.configure(background="purple",foreground="white")

        #Si no hay mas ases en la baraja que se desactive el boton cambiar:
        if self.total_A < 1:
            self.botonCambiar.configure(state=tk.DISABLED,background="black")
         
    def quedarse(self):#Boton Quedarse
        if self.continuar.get()==False:

            #Se le asignan y muestran las cartas de Skynet
            for i in range(0,5):
                if self.total_cartas_skynet <17:
                    self.lista_cartas_skynet.append(carta_aleatoria_skynet(self.total_cartas_skynet))
                    self.lista_labels_skynet[i].config(text=convertir_carta(self.lista_cartas_skynet[i]),background="white",foreground="black")           
                    self.total_cartas_skynet=sum(self.lista_cartas_skynet)
                else:
                    break

            #Se muestra el total de Skynet:
            self.suma_total_skynet_label.configure(text="Skynet: "+ str(self.total_cartas_skynet))

            #============
            #Seccion en la que se calcula quien gana:

            #Si los dos se pasan de 21 (empatan):
            if self.total_cartas_jugador > 21 and self.total_cartas_skynet > 21:
                self.resultado_label.configure(text="VOS Y SKYNET SE PASAN  DE 21,\n EMPATE")
                self.jugador_empato.set(True)
            
            #Si suman la misma cantidad de cartas (empatan):    
            elif self.total_cartas_jugador == self.total_cartas_skynet:
                self.resultado_label.configure(text="HUBO UN EMPATE\n")
                self.jugador_empato.set(True)
                
            #Si el jugador se pasa de 21 pero Skynet no (Skynet gana):            
            elif self.total_cartas_jugador > 21 and self.total_cartas_skynet <= 21:
                self.resultado_label.configure(foreground="red",text="TE PASASTE DE 21,\n SKYNET GANA")
                self.jugador_gano.set(False)

            #Si Skynet se pasa de 21 pero el jugador no (jugador gana):    
            elif self.total_cartas_jugador <= 21 and self.total_cartas_skynet > 21:
                self.resultado_label.configure(foreground="lightgreen",text="SKYNET SE PASA DE 21,\n LO HAS DERROTADO")
                self.jugador_gano.set(True)

            #Si el jugador esta mas cerca de 21 (jugador gana):    
            elif self.total_cartas_jugador > self.total_cartas_skynet:
                self.resultado_label.configure(foreground="lightgreen",text="HAS DERROTADO A SKYNET\n")
                self.jugador_gano.set(True)

            #Si Skynet esta mas cerca de 21 (Skynet gana):    
            elif self.total_cartas_jugador < self.total_cartas_skynet:
                self.resultado_label.configure(foreground="red",text="HA SIDO DERROTADO\n POR SKYNET")
                self.jugador_gano.set(False)

            

        #============
            #Si hubo un empate:
            if self.jugador_empato.get()==True:
                self.botonQuedarse.configure(background="lightgreen",foreground="black")
                if self.se_ha_apostado.get():
                    self.fichas_jugador=+int(self.apuesta.get())

            #Si el jugador gana:
            elif self.jugador_gano.get()==True:
                self.suma_total_skynet_label.configure(foreground="green")
                self.botonQuedarse.configure(background="green",foreground="white")
                if self.se_ha_apostado.get():
                    #se le dan sus fichas multiplicadas por 5
                    self.fichas_jugador+=int(self.apuesta.get())*5
                    

                    #si la cantidad de fichas actual es mayor a la del record:
                    if self.fichas_jugador > int(self.record.get()):
                        #se actualiza el record:
                        self.record.set(str(self.fichas_jugador))

                        #se actualiza el archivo de la sesion actual con el nuevo record:
                        if datos_sesion[0] !="":
                            datos_sesion[1] = self.record.get()

                            #se actualiza el archivo scoreboard:
                            actualizar_record(datos_sesion)

            #Si el jugador pierde
            else:
                self.suma_total_skynet_label.configure(foreground="red")
                self.botonQuedarse.configure(background="red",foreground="white")    

            #Actualizar labels
            self.label_fichas_jugador.configure(text=str(self.fichas_jugador)+" fichas")
            self.label_record.configure(text="Record actual: "+self.record.get())

            #============
            #Desabilitar botones
            self.botonPedir.configure(state=tk.DISABLED,background="grey")
            self.botonCambiar.configure(state=tk.DISABLED,background="black")

            #Habilitar continuar
            self.continuar.set(True)
            self.botonQuedarse.configure(text="Continuar")

            if random.randint(1,4)==random.randint(1,4):
                eleccion,pov=elegir_video(self.jugador_gano.get(),self.jugador_empato.get())
                abrir_ventana_camara(eleccion,pov)

        #============
        else:#Cuando el jugador presione Continuar
            #Reiniciar contadores y booleanos
            self.contador = 0
            self.total_A = 0
            self.total_cartas_skynet=0
            self.lista_cartas_jugador=[]
            self.lista_cartas_skynet=[]
            self.jugador_gano.set(False)
            self.se_ha_apostado.set(False)
            self.jugador_empato.set(False)
            self.continuar.set(False)
            
            #============
            #limpiar labels:
            for i in range(5):
                self.lista_labels_skynet[i].config(text="   ",background="brown",foreground="white")
                self.lista_labels_jugador[i].config(text="   ",background="brown",foreground="white")

            self.suma_total_skynet_label.configure(text="",foreground="white")
            self.suma_total_jugador_label.configure(text="Total: 0",foreground="white")
            self.resultado_label.configure(text="\n")

            #botones:
            self.entrada_apuesta.configure(state=tk.NORMAL)
            self.botonPedir.configure(state=tk.NORMAL,background="white")
            
            self.botonQuedarse.configure(state=tk.DISABLED,text="Quedarse",background="grey",foreground="black")

aplicacion1=Aplicacion()