#Version utilizada: python 3.11.4
import tkinter as tk
import tkinter.font as tkFont
import random
from PIL import Image
from PIL import ImageTk
import cv2
import imutils
import os

datos_sesion=["",""]
nombre_introducido=False


def dividir_cifras(numero):#le agrega comas al numero
    texto = "{:,}"
    texto = texto.format(numero)
    return texto

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

def actualizar_record():#Actualiza el scoreboard con el nuevo record:   
    archivo_records = open("carpeta_datos/records.txt","r")
    lineas_texto=archivo_records.read()
    archivo_records.close()

    texto= dividir_cifras(int(datos_sesion[1]))

    lineas_texto_separado = lineas_texto.split()
    
    #si el record que se quiere agregar es de alguien que ya estaba en el scoreboard:
    if datos_sesion[0] in lineas_texto_separado:
        
        #se busca las fichas que tenia en el scoreboard:
        posicion = (lineas_texto_separado.index(datos_sesion[0])+1)
        record_anterior_string = str(lineas_texto_separado[posicion])
        record_anterior_string= record_anterior_string.replace(",","")
        record_anterior=int(record_anterior_string)

        #se compara el record anterior con el record que se quiere agregar
        #Si el record actual es mejor que el de antes se actualiza:
        if int(datos_sesion[1])>int(record_anterior):
            #se sobreescribe el record:
            lineas_texto_separado[posicion]=texto

    #Si el jugador no estaba en el scoreboard:
    else:
        datos_sesion[1]=texto
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

        fuente=tkFont.Font(family="Lucida Grande",size=18)
        fuente_2=tkFont.Font(family="Lucida Grande",size=20)
        fuente_3=tkFont.Font(family="Impact",size=12)
        fuente_4=tkFont.Font(family="Segoe Script",size=16)
        self.fuente_fea=tkFont.Font(family="fixedsys",size=12)
        self.fuente_fea_grande=tkFont.Font(family="fixedsys",size=40)
        
        #========================
        self.lista_cartas_skynet=[]
        self.lista_labels_skynet=[]

        self.lista_cartas_jugador=[]
        self.lista_labels_jugador=[]

        self.total_cartas_skynet=0
        self.total_cartas_jugador=0

        self.fichas_jugador=100
        self.fichas_sumadas=0        

        self.apuesta=tk.StringVar(value="10")
        self.record=tk.StringVar(value="100")

        #========================
        self.contador= 0
        self.ases_totales = 0

        #========================
        self.se_ha_apostado=tk.BooleanVar(value=False)
        self.jugador_gano=tk.BooleanVar(value=False)
        self.jugador_empato=tk.BooleanVar(value=False)
        self.continuar=tk.BooleanVar(value=False)#cambia el boton pedir por continuar

        self.videos=tk.BooleanVar(value=True)
        self.radio_video_variable = tk.IntVar(value=1)
        self.animaciones=tk.BooleanVar(value=True)
        self.radio_animaciones_variable = tk.IntVar(value=1)
        self.radio_tema_variable=tk.IntVar(value=0)
        self.tema=tk.StringVar(value="clasico")


        #========================
        for i in range (5):
            self.label_carta=tk.Label(self.ventana1,text="  ", background="brown",foreground="white",font=fuente_2,width=2,height=2)
            self.label_carta.grid(column=i+1, row=0)
            self.lista_labels_skynet.insert(i,self.label_carta)

            self.label_carta_jugador=tk.Label(self.ventana1,text="  ", background="brown",foreground="white",font=fuente_2,width=2,height=2)
            self.label_carta_jugador.grid(column=i+1, row=5)
            self.lista_labels_jugador.insert(i,self.label_carta_jugador)

        #========================
        self.suma_total_skynet_label=tk.Label(self.ventana1,font=fuente)
        self.suma_total_skynet_label.grid(column=6, row=0)

        self.suma_total_jugador_label=tk.Label(self.ventana1,text="",font=self.fuente_fea_grande)
        self.suma_total_jugador_label.grid(column=0, row=10)

        self.resultado_label=tk.Label(self.ventana1,text=" \n ",font=fuente_3)
        self.resultado_label.grid(column=6, row=1,rowspan=2)

        self.label_fichas_jugador=tk.Label(self.ventana1,text="fichas: "+str(self.fichas_jugador),font=fuente_4)
        self.label_fichas_jugador.grid(column=2, row=8,columnspan=3)

        self.label_fichas_sumadas_jugador=tk.Label(self.ventana1,text="\n\n\n\n",font=self.fuente_fea)
        self.label_fichas_sumadas_jugador.grid(column=3, row=6,rowspan=2,pady=20)

        self.label_record=tk.Label(self.ventana1,text="Record actual: "+self.record.get(),font=self.fuente_fea)
        self.label_record.grid(column=6,row=9)

        self.label1=tk.Label(self.ventana1,text="Blackjack!",font=fuente_4)
        self.label1.grid(column=1, row=2,columnspan=5,padx=100,pady=80)
        
        #============
        self.botonPedir=tk.Button(self.ventana1,width=20,  text="Pedir", command=self.pedir,font=fuente_4,bd=6,relief="sunken")
        self.botonPedir.grid(column=0, row=7,columnspan=2)

        self.botonQuedarse=tk.Button(self.ventana1,width=20, text="Quedarse", command=self.quedarse,font=fuente_4,state=tk.DISABLED,bd=6,relief="sunken")
        self.botonQuedarse.grid(column=5, row=7,columnspan=2)
        
        self.botonCambiar=tk.Button(self.ventana1,width=20,  text="", command=self.cambiar,font=fuente,bd=0,relief="sunken",state=tk.DISABLED)
        self.botonCambiar.grid(column=0, row=8,columnspan=2,rowspan=2)

        self.botonRecords=tk.Button(self.ventana1,text="Scoreboard",font=("Segoe Script", 14), command=self.record_boton)
        self.botonRecords.grid(column=6, row=10)
        
        self.entrada_apuesta=tk.Entry(self.ventana1, width=10,font=fuente_4, textvariable=self.apuesta,background="purple",foreground="white",insertbackground="white",borderwidth=5,justify=tk.CENTER)
        self.entrada_apuesta.grid(column=3, row=9)

        self.boton_configuracion=tk.Button(self.ventana1,width=15,  text="Configuración",font=self.fuente_fea, command=self.configuracion)
        self.boton_configuracion.grid(column=6, row=11)

        global cambiar_tema
        def cambiar_tema(tema):
            if tema=="oscuro":
                self.botonPedir.configure(background="black",foreground="magenta",activebackground="grey20",activeforeground="white")
                self.botonQuedarse.configure(background="black",foreground="magenta",activebackground="grey20",activeforeground="white")
                self.botonRecords.configure(background="black",foreground="gold2")
                self.boton_configuracion.configure(background="black",foreground="purple")
                self.resultado_label.configure(background="black",foreground="white")
                self.suma_total_skynet_label.configure(foreground="red", background="black")
                self.botonCambiar.configure(background="black")
                self.suma_total_jugador_label.configure(foreground="white", background="black")
                self.label1.configure(foreground="white",background="black")
                self.label_record.configure(background="black",foreground="white")
                self.label_fichas_sumadas_jugador.configure(background="black",foreground="white")
                self.label_fichas_jugador.configure(background="black",foreground="white")
                self.ventana1.configure(background="black")

            elif tema=="claro":
                self.botonPedir.configure(background="white",foreground="magenta",activebackground="grey20",activeforeground="black")
                self.botonQuedarse.configure(background="white",foreground="magenta",activebackground="grey20",activeforeground="black")
                self.botonRecords.configure(background="dark slate gray",foreground="gold2")
                self.boton_configuracion.configure(background="white",foreground="black")
                self.resultado_label.configure(background="light gray",foreground="black")
                self.suma_total_skynet_label.configure(foreground="red", background="light gray")
                self.botonCambiar.configure(background="light gray")
                self.suma_total_jugador_label.configure(foreground="black", background="light gray")
                self.label1.configure(foreground="black",background="light gray")
                self.label_record.configure(background="light gray",foreground="black")
                self.label_fichas_sumadas_jugador.configure(background="light gray",foreground="black")
                self.label_fichas_jugador.configure(background="light gray",foreground="black")
                self.ventana1.configure(background="light gray")
            
            elif tema=="clasico":
                self.botonPedir.configure(background="white",foreground="black",activebackground="gray",activeforeground="white")
                self.botonQuedarse.configure(background="white",foreground="black",activebackground="gray",activeforeground="white")
                self.botonRecords.configure(background="brown",foreground="gold2")
                self.boton_configuracion.configure(background="white",foreground="purple")
                self.resultado_label.configure(background="dark slate gray",foreground="white")
                self.suma_total_skynet_label.configure(foreground="red", background="dark slate gray")
                self.botonCambiar.configure(background="dark slate gray")
                self.suma_total_jugador_label.configure(foreground="white", background="dark slate gray")
                self.label1.configure(foreground="white",background="dark slate gray")
                self.label_record.configure(background="dark slate gray",foreground="white")
                self.label_fichas_sumadas_jugador.configure(background="dark slate gray",foreground="white")
                self.label_fichas_jugador.configure(background="dark slate gray",foreground="white")
                self.ventana1.configure(background="dark slate gray")


        cambiar_tema(self.tema.get())

        global escribir
        def escribir(inicio,palabra_a_escribir,label,ventana):
            palabra_final=inicio
            if self.animaciones.get():
                tiempo=700//len(palabra_a_escribir)
                for letra in palabra_a_escribir:
                    palabra_final+=letra
                    label.config(text=palabra_final)
                    ventana.after(tiempo,ventana.update())
            else:
                palabra_final=inicio+palabra_a_escribir
                label.config(text=palabra_final)
        
        self.ventana1.mainloop()
        
#============
    def configuracion(self):
        ventana_configuracion = tk.Toplevel()
        ventana_configuracion.title("Configuracion del juego")
        ventana_configuracion.configure(background="black")

        cuadro1=tk.LabelFrame(ventana_configuracion,text="Live Camera",bd=5,padx=15,pady=15,background="black",font=self.fuente_fea,foreground="white")
        cuadro1.grid(column=0,row=0)

        tk.Radiobutton(cuadro1, text="Habilitar", variable=self.radio_video_variable, value=1,pady=10,background="black",font=self.fuente_fea,foreground="purple",activeforeground="green",activebackground="black").grid(column=0,row=1)
        tk.Radiobutton(cuadro1, text="Desabilitar", variable=self.radio_video_variable, value=2,pady=10,background="black",font=self.fuente_fea,foreground="purple",activeforeground="green",activebackground="black").grid(column=0,row=2)

        cuadro2=tk.LabelFrame(ventana_configuracion,text="Animaciones",bd=5,padx=15,pady=15,background="black",font=self.fuente_fea,foreground="white")
        cuadro2.grid(column=0,row=1)
        
        tk.Radiobutton(cuadro2, text="Habilitar", variable=self.radio_animaciones_variable, value=1,pady=10,background="black",font=self.fuente_fea,foreground="purple",activeforeground="green",activebackground="black").grid(column=0,row=1)
        tk.Radiobutton(cuadro2, text="Desabilitar", variable=self.radio_animaciones_variable, value=2,pady=10,background="black",font=self.fuente_fea,foreground="purple",activeforeground="green",activebackground="black").grid(column=0,row=2)

        cuadro3=tk.LabelFrame(ventana_configuracion,text="Tema",bd=5,padx=30,pady=15,background="black",font=self.fuente_fea,foreground="white")
        cuadro3.grid(column=0,row=2)
        
        tk.Radiobutton(cuadro3, text="Clásico", variable=self.radio_tema_variable, value=0,pady=10,background="black",font=self.fuente_fea,foreground="purple",activeforeground="green",activebackground="black").grid(column=0,row=1)
        tk.Radiobutton(cuadro3, text="Claro", variable=self.radio_tema_variable, value=1,pady=10,background="black",font=self.fuente_fea,foreground="purple",activeforeground="green",activebackground="black").grid(column=0,row=2)
        tk.Radiobutton(cuadro3, text="Oscuro", variable=self.radio_tema_variable, value=2,pady=10,background="black",font=self.fuente_fea,foreground="purple",activeforeground="green",activebackground="black").grid(column=0,row=3)

        def aplicar():
            if self.radio_video_variable.get()==1:
                self.videos.set(True)
            else:
                self.videos.set(False)


            if self.radio_animaciones_variable.get()==1:
                self.animaciones.set(True)
            else:
                self.animaciones.set(False)


            if self.radio_tema_variable.get()==0:
                self.tema.set("clasico")
            elif self.radio_tema_variable.get()==1:
                self.tema.set("claro")
            else:
                self.tema.set("oscuro")
            cambiar_tema(self.tema.get())
            ventana_configuracion.after(300,ventana_configuracion.destroy)

        boton_aplicar=tk.Button(ventana_configuracion,width=20,  text="Aplicar", command=aplicar,font=self.fuente_fea,background="purple",foreground="white")
        boton_aplicar.grid(column=0,row=3)

    def record_boton(self):#Boton Ingresar / mostrar Scoreboard
        if nombre_introducido==False:#si el jugador aun no ha ingresado su usuario
            abrir_ventana_usuario()
        
        else: #Si el jugador ya ingreso su nombre:
            abrir_ventana_scoreboard()

    def pedir(self):#Boton pedir otra carta
        #Habilitar boton quedarse:
        self.botonQuedarse.configure(state=tk.NORMAL)

        if self.se_ha_apostado.get()==False:#Si se aposto:
            if int(self.apuesta.get()) > 0 and int(self.apuesta.get()) <= self.fichas_jugador and self.fichas_jugador>0:
                self.fichas_jugador-=int(self.apuesta.get())#se resta lo apostado a la cantidad total de fichas:
                self.label_fichas_jugador.configure(text="fichas: "+dividir_cifras(self.fichas_jugador))

                self.se_ha_apostado.set(True)
                self.entrada_apuesta.configure(state=tk.DISABLED)#se desactiva la entrada de la apuesta:

        #=================
        if self.contador==0:#Cuando empiece el juego te da otra mas, asi son dos (reglas)
            self.lista_cartas_jugador.insert(self.contador,carta_aleatoria())
            self.lista_labels_jugador[self.contador].config(text=convertir_carta(self.lista_cartas_jugador[self.contador]),background="white",foreground="black")
            
            if self.lista_cartas_jugador[self.contador] ==1:
                self.ases_totales += 1
                self.lista_labels_jugador[self.contador].config(background="yellow")
            self.contador+=1
        
        if self.contador<5:
            self.lista_cartas_jugador.insert(self.contador,carta_aleatoria())
            self.lista_labels_jugador[self.contador].config(text=convertir_carta(self.lista_cartas_jugador[self.contador]),background="white",foreground="black")
            if self.lista_cartas_jugador[self.contador] ==1:
                self.ases_totales += 1
                self.lista_labels_jugador[self.contador].config(background="yellow")
        self.total_cartas_jugador=sum(self.lista_cartas_jugador)
                    
        if self.ases_totales > 0:#Si se detecta que hay ases
            self.botonCambiar.configure(state=tk.NORMAL,background="black",foreground="yellow",text="Cambiar",bd=6)
            if self.tema.get()=="oscuro":
                self.botonCambiar.configure(background="black",foreground="yellow")
            else:
                self.botonCambiar.configure(background="yellow",foreground="black")

        #Se actualiza el total de las cartas del jugador:
        self.suma_total_jugador_label.configure(text=str(self.total_cartas_jugador))

        if self.total_cartas_jugador ==21:#Si llega justo a 21:
            self.suma_total_jugador_label.configure(foreground="purple")
            self.botonQuedarse.configure(background="purple",foreground="white")

        
        if self.contador < 5:#se le suma 1 cada vez que se presione el boton pedir:
            self.contador+=1

    def cambiar(self):#Boton Cambiar ases por 11
        #Comprobar cual carta es la que tiene el As para asignarle el 10
        indice = self.lista_cartas_jugador.index(1)
        self.lista_cartas_jugador[indice]=11
        self.lista_labels_jugador[indice].config(text=11,background="white")
        
        self.ases_totales-=1#Restar 1 al contador de Ases

        #Corregir el resultado al total
        self.total_cartas_jugador+=10
        self.suma_total_jugador_label.configure(text=str(self.total_cartas_jugador))

        if self.total_cartas_jugador ==21:#Si con el cambio llega justo a 21:
            self.suma_total_jugador_label.configure(foreground="lightgreen")
            self.botonQuedarse.configure(background="purple",foreground="white")

        if self.ases_totales < 1:#Si no hay mas ases se desactiva el boton:
            self.botonCambiar.configure(state=tk.DISABLED,text="",bd=0)
            if self.tema.get()=="oscuro":
                self.botonCambiar.configure(background="black")
            elif self.tema.get()=="claro":
                self.botonCambiar.configure(background="light gray")
            elif self.tema.get()=="clasico":
                self.botonCambiar.configure(background="dark slate gray")
         
    def quedarse(self):#Boton Quedarse
        record_mejorado=False
        self.botonPedir.configure(state=tk.DISABLED,background="grey")
        self.botonCambiar.configure(state=tk.DISABLED,background="black",text="",bd=0)
        if self.tema.get()=="oscuro":
            self.botonCambiar.configure(background="black")
        elif self.tema.get()=="claro":
            self.botonCambiar.configure(background="light gray")
        elif self.tema.get()=="clasico":
            self.botonCambiar.configure(background="dark slate gray")

        if self.continuar.get()==False:
            self.botonQuedarse.configure(state=tk.DISABLED)#desactiva el boton quedarse
            for i in range(0,5):#Se generan las cartas de skynet
                if self.total_cartas_skynet <17:
                    self.lista_cartas_skynet.append(carta_aleatoria_skynet(self.total_cartas_skynet))
                    self.lista_labels_skynet[i].config(text=convertir_carta(self.lista_cartas_skynet[i]),background="white",foreground="black")           

                    self.total_cartas_skynet=sum(self.lista_cartas_skynet)
                    self.suma_total_skynet_label.configure(text="Skynet: "+ str(self.total_cartas_skynet))

                    self.ventana1.update()
                    self.ventana1.after(350)
                else:
                    break

            #============
            mensaje=""
            #Si los dos se pasan de 21 (empatan):
            if self.total_cartas_jugador > 21 and self.total_cartas_skynet > 21:
                mensaje="VOS Y SKYNET SE PASAN  DE 21,\n EMPATE"
                self.jugador_empato.set(True)
            
            #Si suman la misma cantidad de cartas (empatan):    
            elif self.total_cartas_jugador == self.total_cartas_skynet:
                mensaje="HUBO UN EMPATE\n"
                self.jugador_empato.set(True)
                
            #Si el jugador se pasa de 21 pero Skynet no (Skynet gana):            
            elif self.total_cartas_jugador > 21 and self.total_cartas_skynet <= 21:
                mensaje="TE PASASTE DE 21,\n SKYNET GANA"

            #Si Skynet se pasa de 21 pero el jugador no (jugador gana):    
            elif self.total_cartas_jugador <= 21 and self.total_cartas_skynet > 21:
                mensaje="SKYNET SE PASA DE 21,\n LO HAS DERROTADO"
                self.jugador_gano.set(True)

            #Si el jugador esta mas cerca de 21 (jugador gana):    
            elif self.total_cartas_jugador > self.total_cartas_skynet:
                mensaje="HAS DERROTADO A SKYNET\n"
                self.jugador_gano.set(True)

            #Si Skynet esta mas cerca de 21 (Skynet gana):    
            elif self.total_cartas_jugador < self.total_cartas_skynet:
                mensaje="HA SIDO DERROTADO\n POR SKYNET"

        #============
            #Si hubo un empate:
            if self.jugador_empato.get()==True:
                if self.se_ha_apostado.get():
                    self.fichas_sumadas=int(self.apuesta.get())
                    self.fichas_jugador+=self.fichas_sumadas
                    self.label_fichas_sumadas_jugador.configure(foreground="white",text="\n\n\n\n+"+str(self.fichas_sumadas))

            #Si el jugador gana:
            elif self.jugador_gano.get()==True:
                self.resultado_label.configure(foreground="green")
                self.suma_total_skynet_label.configure(foreground="green")

                if self.se_ha_apostado.get():
                    #se le dan sus fichas multiplicadas por 5
                    self.fichas_sumadas=int(self.apuesta.get())*5
                    self.fichas_jugador+=self.fichas_sumadas
                    self.label_fichas_sumadas_jugador.configure(foreground="green",text="\n\n\n\n+"+str(self.fichas_sumadas))

                    if self.fichas_jugador > int(self.record.get()):#si se mejora el record
                        record_mejorado=True
                        self.record.set(self.fichas_jugador)
                
                        if datos_sesion[0] !="":
                            datos_sesion[1] = self.record.get()
                            actualizar_record()

            else:#Si el jugador pierde
                self.resultado_label.configure(foreground="red")
                self.suma_total_skynet_label.configure(foreground="red") 
                self.label_fichas_sumadas_jugador.configure(foreground="red",text="\n\n\n\n-"+(self.apuesta.get())) 

            escribir("",mensaje,self.resultado_label,self.ventana1)
            escribir("fichas: ",dividir_cifras(self.fichas_jugador),self.label_fichas_jugador,self.ventana1)
            if record_mejorado:
                escribir("Record actual: ",dividir_cifras(int(self.record.get())),self.label_record,self.ventana1)

            #============


            self.continuar.set(True)
            self.botonQuedarse.configure(text="Continuar",state=tk.NORMAL)
            if self.jugador_empato.get()==True:
                self.botonQuedarse.configure(background="lightgreen",foreground="black")

            elif self.jugador_gano.get()==True: 
                if self.tema.get()=="oscuro":
                    self.botonQuedarse.configure(background="black",foreground="green")
                else:
                    self.botonQuedarse.configure(background="green",foreground="white")

            else:
                if self.tema.get()=="oscuro":
                    self.botonQuedarse.configure(background="black",foreground="red")
                else:
                    self.botonQuedarse.configure(background="red",foreground="white")

            #============
            if self.videos.get():#Si estan activados los videos
                if self.jugador_empato.get()==False:
                    if random.randint(1,3) == random.randint(1,3):
                        eleccion,pov=elegir_video(self.jugador_gano.get(),self.jugador_empato.get())
                        abrir_ventana_camara(eleccion,pov)
                else:
                    if random.choice([True,True,False])==True:
                        eleccion,pov=elegir_video(self.jugador_gano.get(),self.jugador_empato.get())
                        abrir_ventana_camara(eleccion,pov)


        #============
        else:#Cuando el jugador presione Continuar
            self.contador = 0
            self.ases_totales = 0
            self.total_cartas_skynet=0
            self.lista_cartas_jugador=[]
            self.lista_cartas_skynet=[]
            self.jugador_gano.set(False)
            self.se_ha_apostado.set(False)
            self.jugador_empato.set(False)
            self.continuar.set(False)
            
            #============
            for i in range(5):
                self.lista_labels_skynet[i].config(text="   ",background="brown",foreground="white")
                self.lista_labels_jugador[i].config(text="   ",background="brown",foreground="white")

            self.suma_total_skynet_label.configure(text="",foreground="white")
            self.suma_total_jugador_label.configure(text="0",foreground="white")
            self.resultado_label.configure(text="\n")
            self.label_fichas_sumadas_jugador.configure(foreground="white",text="\n\n\n\n")

            self.entrada_apuesta.configure(state=tk.NORMAL)
            self.botonPedir.configure(state=tk.NORMAL,background="black")
            self.botonQuedarse.configure(state=tk.DISABLED,text="Quedarse",background="black",foreground="magenta")

            cambiar_tema(self.tema.get())

def elegir_video(gano,empato):
    eleccion=""
    pov=""
    if empato==True:
        eleccion = "carpeta_datos/videos/jugador_empata/"
        pov = random.choice(os.listdir("carpeta_datos/videos/jugador_empata/"))
        
    elif gano==True:
        eleccion = "carpeta_datos/videos/jugador_gana/"
        pov = random.choice(os.listdir("carpeta_datos/videos/jugador_gana/"))
    
    elif gano==False:
        eleccion = "carpeta_datos/videos/jugador_pierde/"
        pov = random.choice(os.listdir("carpeta_datos/videos/jugador_pierde/"))

    eleccion += pov
    eleccion +="/"+random.choice(os.listdir(eleccion))

    pov = pov.replace("_"," ")
    pov = pov.upper()

    return eleccion,pov
    

def abrir_ventana_camara(eleccion,pov):
    ventana_camara = tk.Toplevel()
    ventana_camara.title("Camara en vivo")

    global cap
    cap = cv2.VideoCapture(eleccion)

    label_info = tk.Label(ventana_camara, text=pov,font=("Impact", 24),foreground="red",justify="center")
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
    ventana_usuario.configure(background="")

    label_cartel_1=tk.Label(ventana_usuario,text="Ingresa tu nombre de usuario!",foreground="gold2",background="dark slate gray",font=("Gabriola", 20))
    label_cartel_1.grid(column=0, row=0)

    label_cartel_2=tk.Label(ventana_usuario,text="\n\n\n\nEste nombre se utilizara para guardar\n tu record de fichas y podra ser visto por\n los demas usuarios en el Scoreboard\n elige con cuidado!",foreground="white",background="dark slate gray",font=("Lucida Grande",10))
    label_cartel_2.grid(column=0, row=3)

    entrada_nombre=tk.Entry(ventana_usuario, width=14, textvariable="Sapos", background="purple",foreground="white",insertbackground="white",font=("Lucida Grande", 14))
    entrada_nombre.grid(column=0, row=1)
    
    def guardar():#boton guardar
        #Si el nombre introducido no esta vacio y ocupa menos de 20 caracteres:
        if entrada_nombre.get() != "" and len(entrada_nombre.get()) <20:
            global datos_sesion
            global nombre_introducido

            datos_sesion[0] = entrada_nombre.get()
            nombre_introducido=True

            #Luego de 1 segundo cerrar la ventana:
            ventana_usuario.after(500)
            abrir_ventana_scoreboard()
            ventana_usuario.destroy()

    botonGuardar=tk.Button(ventana_usuario, width=14, text="Guardar nombre",background="black",foreground="white",font=("Lucida Grande", 10),command=guardar)
    botonGuardar.grid(column=0, row=2)

def abrir_ventana_scoreboard():#Ventana del scoreboard
    ventana_scoreboard = tk.Toplevel()
    ventana_scoreboard.title("Ventana secundaria")
    ventana_scoreboard.configure(background="dark slate gray")
    ventana_scoreboard.geometry("400x400")

    lineas_texto_modificado =[]
    n=2
    
    archivo_records = open("carpeta_datos/records.txt","r")
    lineas_texto=archivo_records.read()
    archivo_records.close()

    #Se dividen los datos y se guardan en "lineas_texto_separado" en forma de lista:
    lineas_texto_separado = lineas_texto.split()

    for palabra in lineas_texto_separado:
        if n % 2 == 0:#si "n" es par es porque esta leyendo un nombre en la lista
            lineas_texto_modificado.append(palabra+": ")
        else:#Si no es par es porque esta leyendo el record del nombre
            lineas_texto_modificado.append(palabra+"\n\n")    
        n+=1
        
    #luego de procesar la lista "lineas_texto_modificado" se transforma en un string:
    lineas_texto_final = " ".join(lineas_texto_modificado)

    label_scoreboard=tk.Label(ventana_scoreboard,text="~~~~~~~~~~~~~~Scoreboard~~~~~~~~~~~~~~",foreground="gold2",background="dark slate gray",font=("Gabriola", 20))
    label_scoreboard.grid(column=0, row=0)

    label_records=tk.Label(ventana_scoreboard,foreground="white",background="dark slate gray",font=("Segoe Script", 14))
    label_records.grid(column=0, row=1)

    escribir("",lineas_texto_final,label_records,ventana_scoreboard)
    ventana_scoreboard.focus()

aplicacion1=Aplicacion()