#python 3.1
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
import random

#============
#Funciones que se utilizaran en el programa:

#Devuelve una carta aleatoria para el jugador:
def carta_aleatoria(): 
    return random.randint(1,10)

#Devuelve una carta aleatoria para sktnet:
def carta_aleatoria_skynet(total_skynet):
    carta_generada=random.randint(1,11)
    if carta_generada==11:
        if carta_generada + total_skynet>21:
            carta_generada=1
    return carta_generada

#Si es necesario, a partir de el numero de la carta generada devuelve una letra:
def convertir_carta(carta): 
    if carta==10:
        return random.choice(["Q","J","K"])
    elif carta==1 or carta==11:
        return "A"
    else:
        return carta
    

#============JUEGO============    
class Aplicacion:
    def __init__(self):
        #========================
        self.ventana1=tk.Tk()

        #Configurando parametros basicos de la ventana:
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
        self.skynet_carta1=tk.IntVar()
        self.skynet_carta2=tk.IntVar()
        self.skynet_carta3=tk.IntVar()
        self.skynet_carta4=tk.IntVar()
        self.skynet_carta5=tk.IntVar()

        #Variable donde se sumaran las cartas de skynet:
        self.total_cartas_skynet=tk.IntVar()


        #Variables donde se guardaran que numero vale cada carta del jugador:
        self.jugador_carta1=tk.IntVar()
        self.jugador_carta2=tk.IntVar()
        self.jugador_carta3=tk.IntVar()
        self.jugador_carta4=tk.IntVar()
        self.jugador_carta5=tk.IntVar()

        #Variable donde se sumaran las cartas del jugador:
        self.total_cartas_jugador=tk.IntVar()


        #Variable donde se guardaran las fichas del jugador:
        self.fichas_jugador=tk.StringVar(value="100")

        #Variable donde se guardara la apuesta que hizo el jugador
        self.apuesta=tk.StringVar(value="10")

        #Variable en la que se ira guardando el record de fichas obtenidas
        self.record=tk.StringVar(value=self.fichas_jugador.get())

        #========================
        #Variable contador que se usara en el boton pedir
        #Se usa para saber a que carta asignarle el nuevo valor
        self.contador=tk.IntVar(value=0)

        #Variable donde se guardara la cantidad de Ases que tenga el jugador
        #Se usa en el boton cambiar:        
        self.total_A=tk.IntVar()

        #========================
        #Variables Booleanas(Verdadero o Falso):
        self.se_ha_apostado=tk.BooleanVar(value=False)
        self.jugador_gano=tk.BooleanVar(value=False)
        self.jugador_empato=tk.BooleanVar(value=False)
        self.continuar=tk.BooleanVar(value=False)#cambia el boton pedir por continuar       
        

        #========================
        #Declarando las labels donde se mostraran por pantalla las cartas de Skynet:

        self.label_skynet_Carta1=tk.Label(self.ventana1,text="  ", background="brown",foreground="white",font=fuente)
        self.label_skynet_Carta1.grid(column=1, row=0)

        self.label_skynet_Carta2=tk.Label(self.ventana1,text="   ",foreground="white", background="brown",font=fuente)
        self.label_skynet_Carta2.grid(column=2, row=0)

        self.label_skynet_Carta3=tk.Label(self.ventana1,text="   ",foreground="white", background="brown",font=fuente)
        self.label_skynet_Carta3.grid(column=3, row=0)

        self.label_skynet_Carta4=tk.Label(self.ventana1,text="   ",foreground="white", background="brown",font=fuente)
        self.label_skynet_Carta4.grid(column=4, row=0)

        self.label_skynet_Carta5=tk.Label(self.ventana1,text="   ",foreground="white", background="brown",font=fuente)
        self.label_skynet_Carta5.grid(column=5, row=0)

        #Label donde se mostrara el total de Skynet 
        self.suma_total_skynet_label=tk.Label(self.ventana1,foreground="red", background="black",font=fuente_2, relief="solid")
        self.suma_total_skynet_label.grid(column=0, row=0)


        #Declarando las labels donde se mostraran por pantalla las cartas del jugador:
        self.labelCarta1=tk.Label(self.ventana1,text="   ", background="brown",foreground="white",font=fuente)
        self.labelCarta1.grid(column=1, row=5)

        self.labelCarta2=tk.Label(self.ventana1,text="   ",foreground="white", background="brown",font=fuente)
        self.labelCarta2.grid(column=2, row=5)

        self.labelCarta3=tk.Label(self.ventana1,text="  ",foreground="white", background="brown",font=fuente)
        self.labelCarta3.grid(column=3, row=5)

        self.labelCarta4=tk.Label(self.ventana1,text="   ",foreground="white", background="brown",font=fuente)
        self.labelCarta4.grid(column=4, row=5)

        self.labelCarta5=tk.Label(self.ventana1,text="   ",foreground="white", background="brown",font=fuente)
        self.labelCarta5.grid(column=5, row=5)

        #Label donde se mostrara la suma total de las cartas del jugador
        self.suma_total_jugador_label=tk.Label(self.ventana1,text="Total: 0",foreground="white", background="black",font=fuente_2)
        self.suma_total_jugador_label.grid(column=0, row=9)

        #Label donde se mostrara el resultado(si gano, ubo un empate o perdio):
        self.resultado_label=tk.Label(self.ventana1,text=" \n ",foreground="white", background="black",font=fuente_3)
        self.resultado_label.grid(column=0, row=10)

        #Label donde se mostraran las fichas que tiene el jugador:
        self.label_fichas_jugador=tk.Label(self.ventana1,text=self.fichas_jugador.get()+" fichas",background="black",foreground="white",font=fuente_4)
        self.label_fichas_jugador.grid(column=3, row=7)

        self.label_record=tk.Label(self.ventana1,text="Record:"+self.record.get(),background="black",foreground="white")
        self.label_record.grid(column=6,row=10)

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
        
        #Entrada donde el jugador escribira por teclado la apuesta que desea hacer
        self.entrada_apuesta=tk.Entry(self.ventana1, width=6,font=fuente_4, textvariable=self.apuesta,background="purple",foreground="white",insertbackground="white",borderwidth=5)
        self.entrada_apuesta.grid(column=3, row=8)



        self.ventana1.mainloop()

#SECCION DE BOTONES:

    #Boton pedir:
    def pedir(self):

        
        #Habilitar boton quedarse:
        self.botonQuedarse.configure(state=tk.NORMAL,background="white")

        #Comprobar si ya se habia apostado:
        if self.se_ha_apostado.get()==False:

            #Si se ha apostado y si se ha hecho correctamente procesar la apuesta:
            if int(self.apuesta.get()) >0 and int(self.apuesta.get()) <= int(self.fichas_jugador.get()):

                self.fichas_jugador.set(int(self.fichas_jugador.get())-int(self.apuesta.get()))
                self.label_fichas_jugador.configure(text=self.fichas_jugador.get()+" fichas")

                self.se_ha_apostado.set(True)
                self.entrada_apuesta.configure(state=tk.DISABLED)

        #=================
        #=========Seccion en la que se le dan cartas al jugador:

        #contador que se le suma 1 cada vez que se presione el boton pedir:
        self.contador.set(self.contador.get()+1)

        #si el contador esta en 1, que se procese la carta 1 y la 2, ya que
        #las primeras 2 cartas se las da juntas, segun las reglas:

        if self.contador.get()==1:
            #Se le asigna un numero aleatorio usando la funcion carta_aleatoria:
            self.jugador_carta1 = carta_aleatoria()
            self.total_cartas_jugador.set(self.jugador_carta1)

            #se muestra el valor en su label, se usa la funcion de convertir_carta:
            self.labelCarta1.configure(text=convertir_carta(self.jugador_carta1),background="white",foreground="black")

            #Si le ha tocado la carta con el numero 1 (As):
            if self.jugador_carta1==1:

                #al contador de Ases sumarle 1:
                self.total_A.set(1)

                #que el fondo de la carta sea amarillo asi resalta:
                self.labelCarta1.configure(background="yellow")
            
            #Basicamente hacer lo mismo con la segunda
            self.jugador_carta2 = carta_aleatoria()
            self.total_cartas_jugador.set(self.total_cartas_jugador.get()+self.jugador_carta2)
            self.labelCarta2.configure(text=convertir_carta(self.jugador_carta2),background="white",foreground="black")
            if self.jugador_carta2==1:
                self.total_A.set(self.total_A.get()+1)
                self.labelCarta2.configure(background="yellow")
        
        #Si el contador esta en 2 se procesa la carta 3:
        elif self.contador.get() == 2:
            self.jugador_carta3 = carta_aleatoria()
            self.total_cartas_jugador.set(self.total_cartas_jugador.get()+self.jugador_carta3)
            self.labelCarta3.configure(text=convertir_carta(self.jugador_carta3),background="white",foreground="black")
            if self.jugador_carta3==1:
                self.total_A.set(self.total_A.get()+1)
                self.labelCarta3.configure(background="yellow")

        #Si el contador esta en 2 se procesa la carta 4:
        elif self.contador.get() ==3:
            self.jugador_carta4 = carta_aleatoria()
            self.total_cartas_jugador.set(self.total_cartas_jugador.get()+self.jugador_carta4)
            self.labelCarta4.configure(text=convertir_carta(self.jugador_carta4),background="white",foreground="black")
            if self.jugador_carta4==1:
                self.total_A.set(self.total_A.get()+1)
                self.labelCarta4.configure(background="yellow")
                
        #Si el contador esta en 2 se procesa la carta 5:
        elif self.contador.get() ==4:
            self.jugador_carta5 = carta_aleatoria()
            self.total_cartas_jugador.set(self.total_cartas_jugador.get()+self.jugador_carta5)
            self.labelCarta5.configure(text=convertir_carta(self.jugador_carta5),background="white",foreground="black")
            if self.jugador_carta5==1:
                self.total_A.set(self.total_A.get()+1)
                self.labelCarta5.configure(background="yellow")
            
        #Si se detecta que hay ases se activa el boton cambiar    
        if self.total_A.get()>0:
            self.botonCambiar.configure(state=tk.NORMAL,background="yellow")

        #Se actualiza el total de las cartas del jugador:
        self.suma_total_jugador_label.configure(foreground="white",text="Total: "+str(self.total_cartas_jugador.get()))

        #Si el total llega justo a 21:
        if self.total_cartas_jugador.get() ==21:
            self.suma_total_jugador_label.configure(foreground="lightgreen")
            self.botonQuedarse.configure(background="purple",foreground="white")
              

    #Boton Cambiar:
    def cambiar(self):
        #Comprobar cual carta es la que tiene el As para asignarle el 10
        if self.jugador_carta1 == 1:
            
            #Se le cambia el valor de 1 a 11
            self.jugador_carta1=11
            self.labelCarta1.configure(text=11)
            self.labelCarta1.configure(background="white")
        elif self.jugador_carta2 == 1:
            self.jugador_carta2=11
            self.labelCarta2.configure(text=11)
            self.labelCarta2.configure(background="white")
        elif self.jugador_carta3 == 1:
            self.jugador_carta3=11
            self.labelCarta3.configure(text=11)
            self.labelCarta3.configure(background="white")
        elif self.jugador_carta4 == 1:
            self.jugador_carta4=11
            self.labelCarta4.configure(text=11)
            self.labelCarta4.configure(background="white")
        elif self.jugador_carta5 == 1:
            self.jugador_carta5=11
            self.labelCarta5.configure(text=11)
            self.labelCarta5.configure(background="white")
        
        #Restar 1 al contador de Ases
        self.total_A.set(self.total_A.get()-1)

        #Corregir el resultado al total
        self.total_cartas_jugador.set(self.total_cartas_jugador.get()+10)
        self.suma_total_jugador_label.configure(text="Total: "+str(self.total_cartas_jugador.get()))

        #Si con el cambio llega justo a 21:
        if self.total_cartas_jugador.get() ==21:
            self.suma_total_jugador_label.configure(foreground="lightgreen")
            self.botonQuedarse.configure(background="purple",foreground="white")

        #Si no hay mas ases en la baraja que se desactive el boton cambiar:
        if self.total_A.get()<1:
            self.botonCambiar.configure(state=tk.DISABLED,background="black")
        
        

    #Boton Quedarse:
    def quedarse(self):
        if self.continuar.get()==False:

            #===========
            #Se le asignan las cartas a skynet:
            self.skynet_carta1 = carta_aleatoria_skynet(self.total_cartas_skynet.get())
            self.total_cartas_skynet.set(self.skynet_carta1)
            self.label_skynet_Carta1.configure(text=convertir_carta(self.skynet_carta1),background="white",foreground="black")
            
            self.skynet_carta2 = carta_aleatoria_skynet(self.total_cartas_skynet.get())
            self.total_cartas_skynet.set(self.total_cartas_skynet.get()+self.skynet_carta2)
            self.label_skynet_Carta2.configure(text=convertir_carta(self.skynet_carta2),background="white",foreground="black")

            #============
            # Seguir asignando mientras tenga menos de 17:
            if self.total_cartas_skynet.get() < 17:
                self.skynet_carta3 = carta_aleatoria_skynet(self.total_cartas_skynet.get())
                self.total_cartas_skynet.set(self.total_cartas_skynet.get()+self.skynet_carta3)
                self.label_skynet_Carta3.configure(text=convertir_carta(self.skynet_carta3),background="white",foreground="black")
                
                if self.total_cartas_skynet.get() < 17:
                    self.skynet_carta4 = carta_aleatoria_skynet(self.total_cartas_skynet.get())
                    self.total_cartas_skynet.set(self.total_cartas_skynet.get()+self.skynet_carta4)
                    self.label_skynet_Carta4.configure(text=convertir_carta(self.skynet_carta4),background="white",foreground="black")
                    
                    if self.total_cartas_skynet.get() < 17:
                        self.skynet_carta5 = carta_aleatoria_skynet(self.total_cartas_skynet.get())
                        self.total_cartas_skynet.set(self.total_cartas_skynet.get()+self.skynet_carta5)
                        self.label_skynet_Carta5.configure(text=convertir_carta(self.skynet_carta5),background="white",foreground="black")
                                                                                                
            #Se muestra el total de Skynet:
            self.suma_total_skynet_label.configure(text="Skynet: "+ str(self.total_cartas_skynet.get()))

            #============
            #Seccion en la que se calcula quien gana:

            #Si los dos se pasan de 21 (empatan):
            if self.total_cartas_jugador.get() > 21 and self.total_cartas_skynet.get() > 21:
                self.resultado_label.configure(text="VOS Y SKYNET SE PASAN  DE 21,\n EMPATE")
                self.jugador_empato=tk.BooleanVar(value=True)
            
            #Si suman la misma cantidad de cartas (empatan):    
            elif self.total_cartas_jugador.get() == self.total_cartas_skynet.get():
                self.resultado_label.configure(text="HUBO UN EMPATE\n")
                self.jugador_empato=tk.BooleanVar(value=True)
                
            #Si el jugador se pasa de 21 pero Skynet no (Skynet gana):            
            elif self.total_cartas_jugador.get() > 21 and self.total_cartas_skynet.get() <= 21:
                self.resultado_label.configure(foreground="red",text="TE PASASTE DE 21,\n SKYNET GANA")
                self.jugador_gano.set(False)

            #Si Skynet se pasa de 21 pero el jugador no (jugador gana):    
            elif self.total_cartas_jugador.get() <= 21 and self.total_cartas_skynet.get() > 21:
                self.resultado_label.configure(foreground="lightgreen",text="SKYNET SE PASA DE 21,\n LO HAS DERROTADO")
                self.jugador_gano.set(True)

            #Si el jugador esta mas cerca de 21 (jugador gana):    
            elif self.total_cartas_jugador.get() > self.total_cartas_skynet.get():
                self.resultado_label.configure(foreground="lightgreen",text="HAS DERROTADO A SKYNET\n")
                self.jugador_gano.set(True)

            #Si Skynet esta mas cerca de 21 (Skynet gana):    
            elif self.total_cartas_jugador.get() < self.total_cartas_skynet.get():
                self.resultado_label.configure(foreground="red",text="HA SIDO DERROTADO\n POR SKYNET")
                self.jugador_gano.set(False)


            #Si hubo un empate:
            if self.jugador_empato.get()==True:
                self.fichas_jugador.set(int(self.fichas_jugador.get())+int(self.apuesta.get()))
                self.botonQuedarse.configure(background="lightgreen",foreground="black")

            #Si el jugador gana:
            elif self.jugador_gano.get()==True:
                self.fichas_jugador.set(int(self.fichas_jugador.get())+int(self.apuesta.get())*5)
                self.botonQuedarse.configure(background="green",foreground="white")
                if int(self.fichas_jugador.get())>int(self.record.get()):
                    self.record.set(int(self.fichas_jugador.get()))

            #Si el jugador pierde
            else:
                self.botonQuedarse.configure(background="red",foreground="white")    


            #Actualizar las fichas del jugador
            self.label_fichas_jugador.configure(text=self.fichas_jugador.get()+" fichas")
            
            #Actualizar el record
            self.label_record.configure(text="Record: "+self.record.get())

            #============
            #Desabilitar botones
            self.botonPedir.configure(state=tk.DISABLED,background="grey")
            self.botonCambiar.configure(state=tk.DISABLED,background="black")

            #Habilitar continuar
            self.continuar.set(True)
            self.botonQuedarse.configure(text="Continuar")


        #Cuando el jugador presione Continuar
        else:
            #Reiniciar contadores y booleanos
            self.contador.set(0)
            self.total_A.set(0)
            self.jugador_gano.set(False)
            self.se_ha_apostado.set(False)
            self.jugador_empato.set(False)
            self.continuar.set(False)
            
            #============
            #limpiar labels de las cartas de skynet
            self.label_skynet_Carta1.configure(text="   ",background="brown",foreground="white")
            self.label_skynet_Carta2.configure(text="   ",background="brown",foreground="white")
            self.label_skynet_Carta3.configure(text="   ",background="brown",foreground="white")
            self.label_skynet_Carta4.configure(text="   ",background="brown",foreground="white")
            self.label_skynet_Carta5.configure(text="   ",background="brown",foreground="white")

            #limpiar label total de Skynet:
            self.suma_total_skynet_label.configure(text="")

            #impiar labels de las cartas del jugador:
            self.labelCarta1.configure(text="   ",background="brown",foreground="black")
            self.labelCarta2.configure(text="   ",background="brown",foreground="black")
            self.labelCarta3.configure(text="   ",background="brown",foreground="white")
            self.labelCarta4.configure(text="   ",background="brown",foreground="white")
            self.labelCarta5.configure(text="   ",background="brown",foreground="white")

            #limpiar label total del jugador y label de resultado:
            self.suma_total_jugador_label.configure(text="Total: 0",foreground="white")
            self.resultado_label.configure(text="\n")

            #Habilitar botones:
            self.entrada_apuesta.configure(state=tk.NORMAL)
            self.botonPedir.configure(state=tk.NORMAL,background="white")

            #Desabilitar boton quedarse:
            self.botonQuedarse.configure(state=tk.DISABLED,text="Quedarse",background="grey",foreground="black")

aplicacion1=Aplicacion()