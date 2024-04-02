import tkinter as tk
from tkinter.font import Font
from random import randint,choice

nombre_global="" #nombre del usuario actual
fichas_global="0" #fichas del usuario actual
nombre_introducido=False#indica si el jugador ya introdujo su nombre
dificultad="normal" #dificultad por defecto

dividir_cifras=lambda numero,texto="{:,}":texto.format(numero)#funcion que le agrega comas al numero introducido
carta_aleatoria=lambda:randint(1,10)#Funcion que devuelve una carta aleatoria para el jugador

def carta_aleatoria_skynet(total_skynet):#Devuelve una carta aleatoria para sktnet:
    carta_generada=randint(1,11)
    if carta_generada==11 and (carta_generada + total_skynet)>21:
        carta_generada=1
    return carta_generada

def convertir_carta(carta): #Si es necesario, a partir de el numero de la carta generada devuelve una letra:
    if carta==10:
        return choice(["Q","J","K"])
    elif carta==1 or carta==11:
        return "A"
    else:
        return str(carta)
    
def separar_nombre_record(lista):#a partir de una lista, la separa en nombres, records y la ordena
    n=2
    nombres=[]
    records=[]
    diccionario_final={}
    for elemento in lista:
        if n % 2 == 0: #si "n" es par es porque esta leyendo un nombre
            nombres.append(elemento)
        else:
            records.append(elemento)
        n+=1

    diccionario = dict(zip(nombres, records))#se juntan las listas en un solo dicionario
    for elemento in sorted(diccionario,key= lambda elemento: int(diccionario[elemento]),reverse=True):#se ordena el diccionario por sus valores
        diccionario_final[elemento]=diccionario[elemento]

    return diccionario_final

def leer_archivo():#Funcion que devuelve los scoreboards ordenados
    try:
        with open("carpeta_datos/records.txt","r") as archivo_records:
            linea1=(archivo_records.readline()).split("-")
            linea2=(archivo_records.readline()).split("-")

        diccionario_normal=separar_nombre_record(linea1)
        diccionario_hardcore=separar_nombre_record(linea2)

        return diccionario_normal,diccionario_hardcore
    except FileNotFoundError:
        print("ERROR: No se encontro el arcivo _records.txt_")
        return "",""
    except:
        print("Error al leer el archivo")


def actualizar_record():#Actualiza el archivo con el nuevo record:   
    datos_normal,datos_hardcore=leer_archivo()
    normal_texto_final = ""
    hardcore_texto_final = ""
    
    if dificultad=="normal":#si la dificultad es normal se busca en el modo normal
        if not nombre_global in datos_normal:#si el nombre no esta guardado en el archivo
            datos_normal[nombre_global]=fichas_global

        else:#si ya estaba guardado comprueba si el record es mejor
            if int(fichas_global)>int(datos_normal[nombre_global]):
                datos_normal[nombre_global]=fichas_global

    elif dificultad=="hardcore":#si la dificultad es hardcore se busca en el modo hardcore
        if not nombre_global in datos_hardcore:#si el nombre no esta guardado en el archivo
            datos_hardcore[nombre_global]=fichas_global

        else:#si ya estaba guardado comprueba si el record es mejor
            if int(fichas_global)>int(datos_hardcore[nombre_global]):
                datos_hardcore[nombre_global]=fichas_global
    
    for clave, valor in datos_normal.items():#se crea el string final
        normal_texto_final += clave + "-" + valor + "-"
    
    for clave, valor in datos_hardcore.items():
        hardcore_texto_final += clave + "-" + valor + "-"

    try:
        with open("carpeta_datos/records.txt","w") as archivo_records:
            archivo_records.write(normal_texto_final+"\n"+hardcore_texto_final)#se escribe el archivo´
            
    except FileNotFoundError:
        print("ERROR: No se encontro el arcivo _records.txt_")

#Ventana principal:
class Aplicacion:
    def __init__(self):
        self.ventana1=tk.Tk()
        self.ventana1.title("Blackjack")
        self.ventana1.configure(bg="dark slate gray")

        #Fuentes que se usan en el programa
        fuente=Font(family="Lucida Grande",size=18)
        fuente_2=Font(family="Lucida Grande",size=20)
        fuente_3=Font(family="Impact",size=12)
        fuente_4=Font(family="Segoe Script",size=16)
        self.fuente_fea=Font(family="fixedsys",size=12)
        self.fuente_fea_grande=Font(family="fixedsys",size=40)
        
        #========================
        self.lista_cartas_skynet=[]#donde se guarda el valor real de la carta de skynet
        self.lista_labels_skynet=[]#donde se guardan las labels de skynet

        self.lista_cartas_jugador=[]#donde se guarda el valor real de la carta del jugador
        self.lista_labels_jugador=[]#donde se guardan las labels del jugador

        self.total_cartas_jugador=0 #total del jugador
        self.total_cartas_skynet=0#total de skynet
        
        self.fichas_jugador=100#donde se guardan las variables del jugador
        self.fichas_sumadas=0#donde se guardan las fichas que suma o pierde el jugador        

        self.apuesta=tk.StringVar(value="10")#donde se guarda las fichas que apuesta el jugador
        self.record=tk.StringVar(value="100")#donde se guarda el record de la sesion actual

        #========================
        self.ases_totales = 0#contador de ases
        self.contador= 0 #y contador que se usa al pedir cartas

        #========================
        self.se_ha_apostado=tk.BooleanVar(value=False)#indica si el jugador ingreso una apuesta
        self.jugador_gano=tk.BooleanVar(value=False)#indica si el jugador gano la partida
        self.jugador_empato=tk.BooleanVar(value=False)#indica si el jugador empato la partida
        self.continuar=tk.BooleanVar(value=False)#cambia el boton pedir por continuar
        self.reiniciar=tk.BooleanVar(value=False)
        self.radio_dificultad=tk.IntVar(value=0)

        #========================
        for i in range (5):#for en donde se crean las labels de las cartas y los frames para que quede lindo
            self.frame_carta=tk.LabelFrame(self.ventana1,bd=2,padx=1,pady=1,bg="orange",relief="flat")
            self.frame_carta.grid(column=i+1, row=0)
            self.label_carta=tk.Label(self.frame_carta,text="", bg="brown",fg="black",font=fuente_2,width=2,height=2)
            self.label_carta.grid(column=0,row=0)
            self.lista_labels_skynet.insert(i,self.label_carta)

            self.frame_carta=tk.LabelFrame(self.ventana1,bd=2,padx=1,pady=1,bg="orange",relief="flat")
            self.frame_carta.grid(column=i+1, row=5)
            self.label_carta_jugador=tk.Label(self.frame_carta,text="", bg="brown",fg="black",font=fuente_2,width=2,height=2)
            self.label_carta_jugador.grid(column=0, row=0)
            self.lista_labels_jugador.insert(i,self.label_carta_jugador)

        #========================
        #label donde se muestra el total de skynet al finalizar
        self.suma_total_skynet_label=tk.Label(self.ventana1,font=self.fuente_fea_grande,bg="dark slate gray",fg="white")
        self.suma_total_skynet_label.grid(column=6, row=0,columnspan=2)

        #label donde se muestra el total del jugador
        self.suma_total_jugador_label=tk.Label(self.ventana1,text="",font=self.fuente_fea_grande,bg="dark slate gray",fg="white")
        self.suma_total_jugador_label.grid(column=0, row=10,columnspan=2)

        #label donde se muestra el mensaje con el resultado de la partida
        self.resultado_label=tk.Label(self.ventana1,text="",font=fuente_3,bg="dark slate gray")
        self.resultado_label.grid(column=2, row=10,columnspan=3)

        #label que muestra las fichas que tiene el jugador
        self.label_fichas_jugador=tk.Label(self.ventana1,text="fichas: "+str(self.fichas_jugador),font=fuente_4,bg="dark slate gray",fg="white")
        self.label_fichas_jugador.grid(column=2, row=8,columnspan=3)

        #label donde se muestran las fichas sumadas o restadas del jugador
        self.label_fichas_sumadas_jugador=tk.Label(self.ventana1,text="",font=self.fuente_fea,bg="dark slate gray")
        self.label_fichas_sumadas_jugador.grid(column=3, row=6,rowspan=2,pady=50)

        #label donde se muestra el record de la sesion actual
        self.label_record=tk.Label(self.ventana1,text="Record actual: "+self.record.get(),font=self.fuente_fea,bg="dark slate gray",fg="white")
        self.label_record.grid(column=5,row=8,columnspan=2)

        #label de Blackjack!
        self.label1=tk.Label(self.ventana1,text="Blackjack!",font=fuente_4,bg="dark slate gray",fg="white")
        self.label1.grid(column=2, row=2,columnspan=3,padx=100,pady=80)
        
        #============BOTONES==========
        #boton para pedir mas cartas
        self.botonPedir=tk.Button(self.ventana1,width=20,  text="Pedir", command=self.pedir,bd=6,bg="maroon",fg="white",activebackground="gray",activeforeground="white",font=fuente_4,relief="sunken")
        self.botonPedir.grid(column=0, row=7,columnspan=2)

        #boton para no pedir mas cartas
        self.botonQuedarse=tk.Button(self.ventana1,width=20, text="Quedarse", command=self.quedarse,state=tk.DISABLED,bd=6,bg="maroon",fg="white",activebackground="gray",activeforeground="white",font=fuente_4,relief="sunken")
        self.botonQuedarse.grid(column=5, row=7,columnspan=2)

        #boton para cambiar un as por un 11
        self.botonCambiar=tk.Button(self.ventana1,width=20,  text="", command=self.cambiar,font=fuente,bd=0,relief="sunken",state=tk.DISABLED,bg="dark slate gray")
        self.botonCambiar.grid(column=0, row=8,columnspan=2,rowspan=2)

        #boton para ingresar el nombre de usuario y ver el scoreboard
        self.botonRecords=tk.Button(self.ventana1,text="Scoreboard",font=("Segoe Script", 14), command=self.record_boton,bg="brown",fg="gold2")
        self.botonRecords.grid(column=5, row=9,columnspan=2)
        
        #entrada donde el jugador ingresa las fichas que quiere apostar
        self.entrada_apuesta=tk.Entry(self.ventana1, width=15,font=fuente_4, textvariable=self.apuesta,bg="purple",fg="white",insertbackground="white",borderwidth=5,justify=tk.CENTER)
        self.entrada_apuesta.grid(column=3, row=9)

        self.boton_configuracion=tk.Button(self.ventana1,width=15,  text="Dificultad",font=self.fuente_fea, command=self.configuracion)
        self.boton_configuracion.grid(column=5, row=10,columnspan=2)

        global reiniciar_blackjack
        def reiniciar_blackjack():#funcion para reiniciar la partida (resetea todo por defecto)
            self.total_cartas_skynet=self.ases_totales =self.contador = 0
            self.lista_cartas_jugador=[]
            self.lista_cartas_skynet=[]
            self.jugador_gano.set(False)
            self.se_ha_apostado.set(False)
            self.jugador_empato.set(False)
            self.continuar.set(False)
            
            #============
            for i in range(5):
                self.lista_labels_skynet[i].config(text="",bg="brown")
                self.lista_labels_jugador[i].config(text="",bg="brown")

            self.suma_total_skynet_label.configure(text="",fg="white")
            self.suma_total_jugador_label.configure(text="",fg="white")
            self.resultado_label.configure(text="")
            self.label_fichas_sumadas_jugador.configure(fg="white",text="")

            self.botonPedir.configure(state=tk.NORMAL,bg="maroon")
            self.botonQuedarse.configure(state=tk.DISABLED,text="Quedarse",bg="maroon",fg="white")

        global escribir #se hace global para que se use en todas las ventanas
        def escribir(inicio,palabra_a_escribir,label,ventana):#efecto de escritura (animacion)
            palabra_final=inicio
            tiempo=500//len(palabra_a_escribir)
            for letra in palabra_a_escribir:
                palabra_final+=letra
                ventana.after(tiempo,label.config(text=palabra_final))
                ventana.update()
    
        self.ventana1.mainloop()

    def configuracion(self): #cuando se presiona el boton configuracion (dificultad)
        ventana_configuracion = tk.Toplevel()
        ventana_configuracion.title("Configuracion del juego")
        ventana_configuracion.configure(bg="dark slate gray")

        cuadro1=tk.LabelFrame(ventana_configuracion,text="Dificultad",bd=5,padx=30,pady=20,bg="dark slate gray",font=self.fuente_fea,fg="white")
        cuadro1.grid(column=0,row=2)

        cuadro2=tk.LabelFrame(ventana_configuracion,text="Explicacion",bd=5,bg="dark slate gray",font=self.fuente_fea,fg="white")
        cuadro2.grid(column=0,row=3)

        explicacion="Cambiar de modo reiniciara\n la partida actual\n"
        label_explicacion=tk.Label(cuadro2,text=explicacion,bg="dark slate gray",fg="white")
        label_explicacion.grid(column=0,row=0)
        
        def normal_exp():#cuando se presione el radiobutton del Modo Normal
            explicacion=" En el modo Normal se \n   puede apostar tan poco    \n como lo quiera el jugador "
            label_explicacion.configure(text=explicacion)

        def hardcore_exp():#Cuando se presiona el radiobutton del Modo Hardcore
            explicacion="En el modo Hardcore se \napuestan todas las fichas, si\n perdes empezas de nuevo"
            label_explicacion.configure(text=explicacion)
        
        #Radiobuttons con las opciones de dificultad
        tk.Radiobutton(cuadro1, text="Normal", variable=self.radio_dificultad, value=0,pady=10,bg="dark slate gray",font=self.fuente_fea,fg="#009BFF",activeforeground="green",activebackground="dark slate gray",command=normal_exp).grid(column=0,row=1)
        tk.Radiobutton(cuadro1, text="Hardcore", variable=self.radio_dificultad, value=1,pady=10,bg="dark slate gray",font=self.fuente_fea,fg="red",activeforeground="green",activebackground="dark slate gray",command=hardcore_exp).grid(column=0,row=2)

        def reiniciar():#Boton para aplicar los cambios y reiniciar la partida
            global dificultad
            if self.radio_dificultad.get()==0:#si se eligio el Modo Normal
                dificultad="normal"
                self.label1.configure(text="Blackjack!",fg="white")
                self.apuesta.set(10)
                self.entrada_apuesta.configure(state="normal")

            elif self.radio_dificultad.get()==1:#si se eligio el Modo Hardcore
                dificultad="hardcore"
                self.label1.configure(text="Hardcore",fg="red")
                self.apuesta.set(100)
                self.entrada_apuesta.configure(state="disabled")
            
            self.label_record.configure(text="Record actual: 100")
            self.label_fichas_jugador.configure(text="fichas: 100")
            self.record.set("100")
            self.fichas_jugador=100
            reiniciar_blackjack()#se reinicia todo

            ventana_configuracion.after(300,ventana_configuracion.destroy)

        tk.Button(ventana_configuracion,width=20,  text="Reiniciar", command=reiniciar,font=self.fuente_fea,bg="brown",fg="white").grid(column=0,row=4)
        ventana_configuracion.focus()

    def record_boton(self):#Boton Ingresar / mostrar Scoreboard
        if nombre_introducido==False:#si el jugador aun no ha ingresado su nombre usuario
            abrir_ventana_usuario()
        else: #Si el jugador ya ingreso su nombre:
            abrir_ventana_scoreboard()

    def pedir(self):#Boton pedir otra carta
        self.botonQuedarse.configure(state=tk.NORMAL,bg="maroon")
        self.label_fichas_sumadas_jugador.configure(text="")

        if self.contador==0:
            self.lista_cartas_skynet.insert(0,carta_aleatoria_skynet(self.total_cartas_skynet))
            self.lista_labels_skynet[0].config(text=convertir_carta(self.lista_cartas_skynet[0]),bg="white",fg="black")           

            self.total_cartas_skynet=sum(self.lista_cartas_skynet)
            self.suma_total_skynet_label.configure(text=self.total_cartas_skynet)

        #=================
        if self.se_ha_apostado.get()==False:#Si no se aposto:
            try:
                if int(self.apuesta.get()) > 0 and int(self.apuesta.get()) <= self.fichas_jugador and self.fichas_jugador>0:

                    self.fichas_jugador-=int(self.apuesta.get())#se resta lo apostado a la cantidad total de fichas:
                    self.label_fichas_jugador.configure(text="fichas: "+dividir_cifras(self.fichas_jugador))
                    self.label_fichas_sumadas_jugador.configure(fg="red",text="-"+(self.apuesta.get())) 

                    self.se_ha_apostado.set(True)
                    self.entrada_apuesta.configure(state=tk.DISABLED)#se desactiva la entrada de la apuesta:
                else:
                    self.resultado_label.configure(text="Fichas insuficientes",fg="#F05000")
            except:
                self.apuesta.set(0)
                self.resultado_label.configure(text="Solo se aceptan numeros",fg="#F05000")

        #=================
        if self.contador==0:#Cuando empiece el juego te da otra mas, asi son dos (reglas)
            self.lista_cartas_jugador.insert(self.contador,carta_aleatoria())
            self.lista_labels_jugador[self.contador].config(text=convertir_carta(self.lista_cartas_jugador[self.contador]),bg="white")
            
            if self.lista_cartas_jugador[self.contador] ==1:#si al jugador le toco un as
                self.ases_totales += 1
                self.lista_labels_jugador[self.contador].config(bg="yellow")

            self.contador+=1
        
        #=================
        
        if self.contador<5:#si el jugador tiene menos de 5 cartas

            self.lista_cartas_jugador.insert(self.contador,carta_aleatoria())
            self.lista_labels_jugador[self.contador].config(text=convertir_carta(self.lista_cartas_jugador[self.contador]),bg="white")

            if self.lista_cartas_jugador[self.contador] ==1:#si al jugador le toco un as
                self.ases_totales += 1
                self.lista_labels_jugador[self.contador].config(bg="yellow")
            self.contador+=1
        else:
            self.botonPedir.config(state=tk.DISABLED)

        self.total_cartas_jugador=sum(self.lista_cartas_jugador)#se actualiza el total del jugador
        self.suma_total_jugador_label.configure(text=str(self.total_cartas_jugador),fg="white")

        if self.ases_totales>0:
            self.botonCambiar.configure(state=tk.NORMAL,bg="yellow",fg="black",text="Cambiar",bd=6)

        if self.total_cartas_jugador>20:
            self.botonPedir.config(state=tk.DISABLED)

        elif self.total_cartas_jugador ==21:#Si llega justo a 21:
            self.suma_total_jugador_label.configure(fg="magenta")
            self.botonQuedarse.configure(bg="purple",fg="white")        

    #=================
    def cambiar(self):#Boton para cambiar ases por 11
        #se busca en que carta esta el as y se aplica el 11
        indice = self.lista_cartas_jugador.index(1)
        self.lista_cartas_jugador[indice]=11
        self.lista_labels_jugador[indice].config(text=11,bg="white")
        
        self.ases_totales-=1

        #Corregir el resultado al total
        self.total_cartas_jugador+=10
        self.suma_total_jugador_label.configure(text=str(self.total_cartas_jugador))

        if self.total_cartas_jugador ==21:#Si con el cambio llega justo a 21:
            self.suma_total_jugador_label.configure(fg="magenta")
            self.botonQuedarse.configure(bg="purple",fg="white")

        if self.ases_totales < 1:#Si no hay mas ases se desactiva el boton:
            self.botonCambiar.configure(state=tk.DISABLED,text="",bd=0,bg="dark slate gray")

    #=================
    def quedarse(self):#Boton para quedarse y no pedir mas cartas
        record_mejorado=False #variable que detecta si se mejoro el record anterior

        self.botonPedir.configure(state=tk.DISABLED,bg="grey")
        self.botonCambiar.configure(state=tk.DISABLED,bg="dark slate gray",text="",bd=0)

        if self.continuar.get()==False:#si aun no se activo el boton continuar
            self.botonQuedarse.configure(state=tk.DISABLED)#desactiva el boton quedarse

            for i in range(1,5):#Se generan las cartas de skynet
                if self.total_cartas_skynet <17:#mientras tenga menos de 17 sigue pidiendo
                    self.lista_cartas_skynet.append(carta_aleatoria_skynet(self.total_cartas_skynet))
                    self.lista_labels_skynet[i].config(text=convertir_carta(self.lista_cartas_skynet[i]),bg="white",fg="black")           

                    self.total_cartas_skynet=sum(self.lista_cartas_skynet)
                    self.suma_total_skynet_label.configure(text=self.total_cartas_skynet)

                    self.ventana1.update()
                    self.ventana1.after(300)
                else:
                    break

            #============
            mensaje=""#variable donde se guarda el mensje final
            #Si los dos se pasan de 21 (empatan):
            if self.total_cartas_jugador > 21 and self.total_cartas_skynet > 21:
                mensaje="VOS Y SKYNET SE PASAN  DE 21, EMPATE"
                self.jugador_empato.set(True)
            
            #Si suman la misma cantidad de cartas (empatan):    
            elif self.total_cartas_jugador == self.total_cartas_skynet:
                mensaje="HUBO UN EMPATE"
                self.jugador_empato.set(True)
                
            #Si el jugador se pasa de 21 pero Skynet no (Skynet gana):            
            elif self.total_cartas_jugador > 21 and self.total_cartas_skynet <= 21:
                mensaje="TE PASASTE DE 21, SKYNET GANA"

            #Si Skynet se pasa de 21 pero el jugador no (jugador gana):    
            elif self.total_cartas_jugador <= 21 and self.total_cartas_skynet > 21:
                mensaje="SKYNET SE PASA DE 21, LO HAS DERROTADO"
                self.jugador_gano.set(True)

            #Si el jugador esta mas cerca de 21 (jugador gana):    
            elif self.total_cartas_jugador > self.total_cartas_skynet:
                mensaje="HAS DERROTADO A SKYNET"
                self.jugador_gano.set(True)

            #Si Skynet esta mas cerca de 21 (Skynet gana):    
            elif self.total_cartas_jugador < self.total_cartas_skynet:
                mensaje="HA SIDO DERROTADO POR SKYNET"

        #============
            #Si hubo un empate:
            if self.jugador_empato.get()==True:
                if self.se_ha_apostado.get():
                    self.resultado_label.configure(fg="white")
                    self.fichas_sumadas=int(self.apuesta.get())
                    self.fichas_jugador+=self.fichas_sumadas
                    self.label_fichas_sumadas_jugador.configure(fg="white",text="+"+str(self.fichas_sumadas))

            #Si el jugador gana:
            elif self.jugador_gano.get()==True:
                self.resultado_label.configure(fg="lightgreen")
                self.suma_total_skynet_label.configure(fg="green")

                if self.se_ha_apostado.get():
                    self.fichas_sumadas=int(self.apuesta.get())*2
                    self.fichas_jugador+=self.fichas_sumadas
                    self.label_fichas_sumadas_jugador.configure(fg="green",text="+"+str(self.fichas_sumadas))

                    if self.fichas_jugador > int(self.record.get()):#si se mejora el record
                        global fichas_global
                        record_mejorado=True
                        self.record.set(self.fichas_jugador)
                        fichas_global = self.record.get()
                
                        if nombre_introducido:#si el jugador ingreso un nombre
                            actualizar_record()

            else:#Si el jugador pierde
                self.resultado_label.configure(fg="red")
                self.botonQuedarse.configure(bg="red")
                self.suma_total_skynet_label.configure(fg="red") 

            if self.jugador_gano.get()==True or self.jugador_empato.get()==True:
                escribir("fichas: ",dividir_cifras(self.fichas_jugador),self.label_fichas_jugador,self.ventana1)

            if self.jugador_empato.get()==True:#si el jugador empato
                self.botonQuedarse.configure(bg="lightgreen",fg="black")

            elif self.jugador_gano.get()==True: #si el jugador empato
                self.botonQuedarse.configure(bg="green",fg="white")
                
            escribir("",mensaje,self.resultado_label,self.ventana1)

            if record_mejorado:#si el jugador mejoro su record
                escribir("Record actual: ",dividir_cifras(int(self.record.get())),self.label_record,self.ventana1)

            self.continuar.set(True)#se activa el boton continuar
            if self.fichas_jugador==0:
                self.botonQuedarse.configure(text="Reiniciar",state=tk.NORMAL)
                self.reiniciar.set(True)
            else:
                self.botonQuedarse.configure(text="Continuar",state=tk.NORMAL)

        #============
        else:#Cuando el jugador presione Continuar (se reinicia todo)
            reiniciar_blackjack()

            if self.reiniciar.get():
                self.reiniciar.set(False)
                self.fichas_jugador=100
                self.label_fichas_jugador.configure(text="fichas: 100")
                if dificultad=="normal":
                    self.apuesta.set(10)  

                elif dificultad=="hardcore":
                    self.apuesta.set(self.fichas_jugador)                

            if dificultad=="normal":
                self.entrada_apuesta.configure(state=tk.NORMAL)
            elif dificultad=="hardcore":
                self.apuesta.set(self.fichas_jugador)

#==================

def abrir_ventana_usuario():#Ventana secundaria donde se introduce el nombre de usuario
    ventana_usuario = tk.Toplevel()
    ventana_usuario.title("Nombre de usuario")
    ventana_usuario.configure(bg="dark slate gray")

    cuadro1=tk.LabelFrame(ventana_usuario,bd=5,padx=15,pady=15,bg="dark slate gray")
    cuadro1.grid(column=0,row=0)
    cuadro2=tk.LabelFrame(ventana_usuario,bd=5,padx=103,pady=15,fg="white",font=("Fixedsys", 10),bg="dark slate gray",text="Usuarios en modo Normal")
    cuadro2.grid(column=0,row=1)
    cuadro3=tk.LabelFrame(ventana_usuario,bd=5,padx=103,pady=15,fg="white",font=("Fixedsys", 10),bg="dark slate gray",text="Usuarios en modo Hardcore")
    cuadro3.grid(column=0,row=2)

    tk.Label(cuadro1,text="Ingresa tu nombre de usuario!",fg="orange",bg="dark slate gray",font=("Gabriola", 20,"bold")).grid(column=0, row=0,pady=10)
    tk.Label(cuadro1,pady=25,fg="white",bg="dark slate gray",font=("Lucida Grande",10),text="Este nombre se utilizara para guardar tu record de fichas\n y sera visto por los demas usuarios en el Scoreboard\n\nSi tu nombre aparece en la lista de Usuarios Guardados\ningresalo para mantenerlo actualizado").grid(column=0, row=3)

    entrada_nombre=tk.Entry(cuadro1, width=14, bg="purple",fg="white",insertbackground="white",font=("Lucida Grande", 14))
    entrada_nombre.grid(column=0, row=1,pady=10)
    
    def guardar():#boton para guardar el nombre
        #Si el nombre introducido no esta vacio y ocupa menos de 30 caracteres:
        if entrada_nombre.get() != "" and len(entrada_nombre.get()) <30 and not "-" in entrada_nombre.get():
            global nombre_global,nombre_introducido
            nombre_global = entrada_nombre.get()
            nombre_introducido=True

            actualizar_record()
            ventana_usuario.after(300)
            abrir_ventana_scoreboard()
            ventana_usuario.destroy()

    tk.Button(cuadro1, width=14, text="Guardar nombre",bg="brown",fg="white",font=("Segoe Script", 10),command=guardar).grid(column=0, row=2)

    datos_normal,datos_hardcore=leer_archivo()

    for i,elemento in enumerate(datos_normal.keys()):#se crean labels conforme jugadores guardados haya
        tk.Label(cuadro2,text=elemento,bg="dark slate gray",fg="orange",font=("fixedsys",12)).grid(column=0, row=i)
    for i,elemento in enumerate(datos_hardcore.keys()):#lo mismo pero con los hardcore
        tk.Label(cuadro3,text=elemento,bg="dark slate gray",fg="orange",font=("fixedsys",12)).grid(column=0, row=i)

def abrir_ventana_scoreboard():#Ventana del scoreboard
    ventana_scoreboard = tk.Toplevel()
    ventana_scoreboard.title("Scoreboard")
    ventana_scoreboard.configure(bg="dark slate gray")

    archivo_normal,archivo_hardcore=leer_archivo()
    cuadro=tk.LabelFrame(ventana_scoreboard,bd=5,padx=2,pady=15,bg="dark slate gray")
    cuadro.grid(column=0,row=0)
    cuadro2=tk.LabelFrame(ventana_scoreboard,bd=5,padx=2,pady=15,bg="dark slate gray")
    cuadro2.grid(column=0,row=1)
    colores=["#FF5000","#FF9000","#FFD000","#FFF400","#00FB00","#00FFF0","#AFFFFF"]#colores de los 3 primeros jugadores
    tk.Label(cuadro,text="~~~~~~~~~~~Modo Normal~~~~~~~~~~~~",fg="gold2",bg="dark slate gray",font=("Gabriola", 20,"bold")).grid(column=0, row=0)

    for i,clave in enumerate (archivo_normal.keys()):#por cada nombre que haya se crea una label
        color="#FFFFFF"
        if i<6:
            color=colores[i]
        tk.Label(cuadro,fg=color,text="\n"+clave+": "+dividir_cifras(int(archivo_normal[clave])),bg="dark slate gray",font=("fixedsys",12),justify="center").grid(column=0, row=i+1)

    tk.Label(cuadro2,text="---------------Modo Hardcore---------------",fg="red",bg="dark slate gray",font=("Gabriola", 20,"bold")).grid(column=0, row=0)
    for i,clave in enumerate (archivo_hardcore.keys()):#por cada nombre que haya se crea una label
        color="#FFFFFF"
        if i<6:
            color=colores[i]
        tk.Label(cuadro2,fg=color,text="\n"+clave+": "+dividir_cifras(int(archivo_hardcore[clave])),bg="dark slate gray",font=("fixedsys",12),justify="center").grid(column=0, row=i+1)
            
    ventana_scoreboard.focus()
aplicacion1=Aplicacion()