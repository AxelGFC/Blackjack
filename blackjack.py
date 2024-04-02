import tkinter as tk
import tkinter.font as tkFont
import random

#============FUNCIONES============
def carta_aleatoria():
    return random.randint(1,10)

def convertir_carta(carta):
    if carta==10:
        return random.choice(["Q","J","K"])
    elif carta==1:
        return "A"
    else:
        return carta
#=================================
    
class Aplicacion:
    def __init__(self):
        #============VENTANA============
        self.ventana1=tk.Tk()
        
        self.ventana1.title("Blackjack")
        self.ventana1.configure(background="black")

        fuente=tkFont.Font(family="Lucida Grande",size=14)
        fuente_2=tkFont.Font(family="Lucida Grande",size=20)
        fuente_3=tkFont.Font(family="Impact",size=12)
        fuente_4=tkFont.Font(family="Segoe Script",size=16)
        
        #============SKYNET LORE============
        self.skynet_carta1=tk.IntVar()
        self.skynet_carta2=tk.IntVar()
        self.skynet_carta3=tk.IntVar()
        self.skynet_carta4=tk.IntVar()
        self.skynet_carta5=tk.IntVar()
        
        self.total_cartas_skynet=tk.IntVar()
        
        #============LABELS DE SKYNET============
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

        #============CENTRO DE LA MESA============

        #labels extra invisibles para que no parezca que esta todo muy junto
        self.label_extra_1=tk.Label(self.ventana1,text="aaaaa", background="black",font=fuente)
        self.label_extra_1.grid(column=2, row=1)
        
        self.label1=tk.Label(self.ventana1,text="Blackjack!",foreground="white",background="black",font=fuente_4)
        self.label1.grid(column=3, row=2)

        self.label_extra_2=tk.Label(self.ventana1,text="aaaaa", background="black",font=fuente)
        self.label_extra_2.grid(column=4, row=3)
        
        #============JUGADOR LORE============
        self.jugador_carta1=tk.IntVar()
        self.jugador_carta2=tk.IntVar()
        self.jugador_carta3=tk.IntVar()
        self.jugador_carta4=tk.IntVar()
        self.jugador_carta5=tk.IntVar()
        
        self.contador=tk.IntVar()
        self.total_cartas_jugador=tk.IntVar()
        self.total_A=tk.IntVar()
        
        #============LABELS DEL JUGADOR============
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
        
        #============DECLARANDO BOTONES============
        self.botonPedir=tk.Button(self.ventana1,width=20,  text="Pedir", command=self.pedir,font=fuente_4)
        self.botonPedir.grid(column=0, row=6)
        
        self.botonQuedarse=tk.Button(self.ventana1,width=20,  text="Quedarse", command=self.quedarse,font=fuente_4)
        self.botonQuedarse.grid(column=6, row=6)

        self.botonReiniciar=tk.Button(self.ventana1,width=3,height=1,  text="R", command=self.reiniciar,font=fuente)
        self.botonReiniciar.grid(column=0, row=9)

        self.botonCambiar=tk.Button(self.ventana1,width=10,height=1,  text="Cambiar", command=self.cambiar,font=fuente,background="black",borderwidth=0,state=tk.DISABLED)
        self.botonCambiar.grid(column=6, row=7)

        #============LABEL DE TOTAL DE SKYNET============
        self.suma_total_skynet_label=tk.Label(self.ventana1,foreground="red", background="black",font=fuente_2, relief="solid")
        self.suma_total_skynet_label.grid(column=0, row=0)

        #============LABEL DE RESULTADO============
        self.resultado_label=tk.Label(self.ventana1,text=" \n ",foreground="white", background="black",font=fuente_3)
        self.resultado_label.grid(column=0, row=8)

        #============PRIMERAS DOS CARTAS DEL JUGADOR============
        self.jugador_carta1 = carta_aleatoria()
        self.total_cartas_jugador.set(self.jugador_carta1)
        self.labelCarta1.configure(text=convertir_carta(self.jugador_carta1),background="white",foreground="black")
        if self.jugador_carta1==1:
            self.total_A.set(1)
            self.labelCarta1.configure(background="yellow")
        
        self.jugador_carta2 = carta_aleatoria()
        self.total_cartas_jugador.set(self.total_cartas_jugador.get()+self.jugador_carta2)
        self.labelCarta2.configure(text=convertir_carta(self.jugador_carta2),background="white",foreground="black")
        if self.jugador_carta2==1:
            self.total_A.set(self.total_A.get()+1)
            self.labelCarta2.configure(background="yellow")

        #Si se detecta que hay mas de 0 Ases que se active el boton Cambiar
        if self.total_A.get()>0:
            self.botonCambiar.configure(state=tk.NORMAL,background="yellow")

        #============LABEL DE TOTAL DEL JUGADOR============
        self.suma_total_jugador_label=tk.Label(self.ventana1,text="Total: "+str(self.total_cartas_jugador.get()),foreground="white", background="black",font=fuente_2)
        self.suma_total_jugador_label.grid(column=0, row=7)

        self.ventana1.mainloop()
        
#============BOTON PEDIR============
    def pedir(self):
        self.contador.set(self.contador.get()+1)
        
        if self.contador.get() == 1:
            self.jugador_carta3 = carta_aleatoria()
            self.total_cartas_jugador.set(self.total_cartas_jugador.get()+self.jugador_carta3)
            self.labelCarta3.configure(text=convertir_carta(self.jugador_carta3),background="white",foreground="black")
            if self.jugador_carta3==1:
                self.total_A.set(self.total_A.get()+1)
                self.labelCarta3.configure(background="yellow")

        elif self.contador.get() ==2:
            self.jugador_carta4 = carta_aleatoria()
            self.total_cartas_jugador.set(self.total_cartas_jugador.get()+self.jugador_carta4)
            self.labelCarta4.configure(text=convertir_carta(self.jugador_carta4),background="white",foreground="black")
            if self.jugador_carta4==1:
                self.total_A.set(self.total_A.get()+1)
                self.labelCarta4.configure(background="yellow")
                
        elif self.contador.get() ==3:
            self.jugador_carta5 = carta_aleatoria()
            self.total_cartas_jugador.set(self.total_cartas_jugador.get()+self.jugador_carta5)
            self.labelCarta5.configure(text=convertir_carta(self.jugador_carta5),background="white",foreground="black")
            if self.jugador_carta5==1:
                self.total_A.set(self.total_A.get()+1)
                self.labelCarta5.configure(background="yellow")
            
        #Si se detecta que hay mas de 0 Ases que se active el boton Cambiar    
        if self.total_A.get()>0:
            self.botonCambiar.configure(state=tk.NORMAL,background="yellow")

        #============Mostrar el total del jugador:
        self.suma_total_jugador_label.configure(foreground="white",text="Total: "+str(self.total_cartas_jugador.get()))

        #Si llega justo a 21:
        if self.total_cartas_jugador.get() ==21:
            self.suma_total_jugador_label.configure(foreground="lightgreen")
              
#============BOTONES CAMBIAR============
    def cambiar(self):
        #Comprobar cual carta es la que tiene el As para asignarle el 10
        if self.jugador_carta1 == 1:
            self.jugador_carta1=10
            self.labelCarta1.configure(text=10)
            self.labelCarta1.configure(background="white")
        elif self.jugador_carta2 == 1:
            self.jugador_carta2=10
            self.labelCarta2.configure(text=10)
            self.labelCarta2.configure(background="white")
        elif self.jugador_carta3 == 1:
            self.jugador_carta3=10
            self.labelCarta3.configure(text=10)
            self.labelCarta3.configure(background="white")
        elif self.jugador_carta4 == 1:
            self.jugador_carta4=10
            self.labelCarta4.configure(text=10)
            self.labelCarta4.configure(background="white")
        elif self.jugador_carta5 == 1:
            self.jugador_carta5=10
            self.labelCarta5.configure(text=10)
            self.labelCarta5.configure(background="white")
        
        #Restar 1 al contador de As's
        self.total_A.set(self.total_A.get()-1)

        #sumar el resultado al total
        self.total_cartas_jugador.set(self.total_cartas_jugador.get()+9)
        self.suma_total_jugador_label.configure(text="Total: "+str(self.total_cartas_jugador.get()))

        if self.total_A.get()<1:
            self.botonCambiar.configure(state=tk.DISABLED,background="black")

#============BOTON QUEDARSE============
    def quedarse(self):

    #===========ASIGNAR Y MOSTRAR LAS CARTAS DE SKYNET==========
        self.skynet_carta1 = carta_aleatoria()
        self.total_cartas_skynet.set(self.skynet_carta1)
        self.label_skynet_Carta1.configure(text=convertir_carta(self.skynet_carta1),background="white",foreground="black")
        
        self.skynet_carta2 = carta_aleatoria()
        self.total_cartas_skynet.set(self.total_cartas_skynet.get()+self.skynet_carta2)
        self.label_skynet_Carta2.configure(text=convertir_carta(self.skynet_carta2),background="white",foreground="black")

        #============Seguir asignando mientras tenga menos de 17
        if self.total_cartas_skynet.get() < 17:
            self.skynet_carta3 = carta_aleatoria()
            self.total_cartas_skynet.set(self.total_cartas_skynet.get()+self.skynet_carta3)
            self.label_skynet_Carta3.configure(text=convertir_carta(self.skynet_carta3),background="white",foreground="black")
            
            if self.total_cartas_skynet.get() < 17:
                self.skynet_carta4 = carta_aleatoria()
                self.total_cartas_skynet.set(self.total_cartas_skynet.get()+self.skynet_carta4)
                self.label_skynet_Carta4.configure(text=convertir_carta(self.skynet_carta4),background="white",foreground="black")
                
                if self.total_cartas_skynet.get() < 17:
                    self.skynet_carta5 = carta_aleatoria()
                    self.total_cartas_skynet.set(self.total_cartas_skynet.get()+self.skynet_carta5)
                    self.label_skynet_Carta5.configure(text=convertir_carta(self.skynet_carta5),background="white",foreground="black")
                                                                                              
        #============Mostrar el total de SKYNET:
        self.suma_total_skynet_label.configure(text="Skynet: "+ str(self.total_cartas_skynet.get()))

        #============CALCULAR QUIEN GANA============
        #Si los dos se pasan de 21:
        if self.total_cartas_jugador.get() > 21 and self.total_cartas_skynet.get() > 21:
            self.resultado_label.configure(text="VOS Y SKYNET SE PASAN  DE 21,\n NADIE GANA")
            
        #============Si el jugador se pasa de 21 pero Skynet no:            
        elif self.total_cartas_jugador.get() > 21 and self.total_cartas_skynet.get() <= 21:
            self.resultado_label.configure(foreground="red",text="TE PASASTE DE 21,\n SKYNET GANA")

        #============Si Skynet se pasa de 21 pero el jugador no:    
        elif self.total_cartas_jugador.get() <= 21 and self.total_cartas_skynet.get() > 21:
            self.resultado_label.configure(foreground="lightgreen",text="SKYNET SE PASA DE 21,\n LO HAS DERROTADO")

        #============Si el jugador esta mas cerca de 21:    
        elif self.total_cartas_jugador.get() > self.total_cartas_skynet.get():
            self.resultado_label.configure(foreground="lightgreen",text="HAS DERROTADO A SKYNET")

        #============Si Skynet esta mas cerca de 21:    
        elif self.total_cartas_jugador.get() < self.total_cartas_skynet.get():
            self.resultado_label.configure(foreground="red",text="HA SIDO DERROTADO\n POR SKYNET")

        #============Si empatan:    
        elif self.total_cartas_jugador.get() == self.total_cartas_skynet.get():
            self.resultado_label.configure(text="HUBO UN EMPATE")

        #============Desabilitar botones
        self.botonQuedarse.configure(state=tk.DISABLED)
        self.botonPedir.configure(state=tk.DISABLED)
        
#============BOTON REINICIAR============        
    def reiniciar(self):
        #============Reiniciar contadores
        self.contador.set(0)
        self.total_A.set(0)

        self.botonCambiar.configure(state=tk.DISABLED,background="black")

        #============Primeras dos cartas de skynet============
        self.skynet_carta1 = carta_aleatoria()
        self.total_cartas_skynet.set(self.skynet_carta1)

        self.skynet_carta2 = carta_aleatoria()
        self.total_cartas_skynet.set(self.total_cartas_skynet.get()+self.skynet_carta2)
        
        #============limpiar labels de skynet
        self.label_skynet_Carta1.configure(text="   ",background="brown",foreground="white")
        self.label_skynet_Carta2.configure(text="   ",background="brown",foreground="white")
        self.label_skynet_Carta3.configure(text="   ",background="brown",foreground="white")
        self.label_skynet_Carta4.configure(text="   ",background="brown",foreground="white")
        self.label_skynet_Carta5.configure(text="   ",background="brown",foreground="white")

        #============limpiar labels del jugador
        self.labelCarta1.configure(text="   ",background="white",foreground="black")
        self.labelCarta2.configure(text="   ",background="white",foreground="black")
        self.labelCarta3.configure(text="   ",background="brown",foreground="white")
        self.labelCarta4.configure(text="   ",background="brown",foreground="white")
        self.labelCarta5.configure(text="   ",background="brown",foreground="white")

        #============Reiniciar label total de Skynet
        self.suma_total_skynet_label.configure(text="")
        
        #============Primeras dos cartas del jugador============
        self.jugador_carta1 = carta_aleatoria()
        self.total_cartas_jugador.set(self.jugador_carta1)
        self.labelCarta1.configure(text=convertir_carta(self.jugador_carta1))
        if self.jugador_carta1==1:
            self.total_A.set(self.total_A.get()+1)
            self.labelCarta1.configure(background="yellow")

        self.jugador_carta2 = carta_aleatoria()
        self.total_cartas_jugador.set(self.total_cartas_jugador.get()+self.jugador_carta2)
        self.labelCarta2.configure(text=convertir_carta(self.jugador_carta2))
        if self.jugador_carta2==1:
            self.total_A.set(self.total_A.get()+1)
            self.labelCarta2.configure(background="yellow")
    
        #============Reiniciar label total del jugador
        self.suma_total_jugador_label.configure(text="Total: "+str(self.total_cartas_jugador.get()),foreground="white")
        self.resultado_label.configure(text="\n")

        #============Habilitar botones
        self.botonQuedarse.configure(state=tk.NORMAL)
        self.botonPedir.configure(state=tk.NORMAL)
        if self.total_A.get()>0:
            self.botonCambiar.configure(state=tk.NORMAL,background="yellow")

aplicacion1=Aplicacion()