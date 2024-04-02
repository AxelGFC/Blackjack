import tkinter as tk
import tkinter.font as tkFont
import random

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
        
        self.skynet_contador=tk.IntVar()
        self.total_cartas_skynet=tk.IntVar()
        
        #============LABELS DE SKYNET============
        self.label_skynet_Carta1=tk.Label(self.ventana1,text="  ", background="brown",font=fuente)
        self.label_skynet_Carta1.grid(column=1, row=0)
        self.label_skynet_Carta1.configure(foreground="white")

        self.label_skynet_Carta2=tk.Label(self.ventana1,text="   ", background="brown",font=fuente)
        self.label_skynet_Carta2.grid(column=2, row=0)
        self.label_skynet_Carta2.configure(foreground="white")

        self.label_skynet_Carta3=tk.Label(self.ventana1,text="   ", background="brown",font=fuente)
        self.label_skynet_Carta3.grid(column=3, row=0)
        self.label_skynet_Carta3.configure(foreground="white")

        self.label_skynet_Carta4=tk.Label(self.ventana1,text="   ", background="brown",font=fuente)
        self.label_skynet_Carta4.grid(column=4, row=0)
        self.label_skynet_Carta4.configure(foreground="white")

        self.label_skynet_Carta5=tk.Label(self.ventana1,text="   ", background="brown",font=fuente)
        self.label_skynet_Carta5.grid(column=5, row=0)
        self.label_skynet_Carta5.configure(foreground="white")
        
        #============PRIMERAS DOS CARTAS DE SKYNET============
        self.skynet_carta1 = random.randint(1,10)
        self.total_cartas_skynet.set(self.skynet_carta1)

        self.skynet_carta2 = random.randint(1,10)
        self.total_cartas_skynet.set(self.total_cartas_skynet.get()+self.skynet_carta2)

        #============CENTRO DE LA MESA============

        self.label_extra_1=tk.Label(self.ventana1,text="aaaaa", background="black",font=fuente)
        self.label_extra_1.grid(column=2, row=1)
        
        self.label1=tk.Label(self.ventana1,text="Blackjack!", background="black",font=fuente_4)
        self.label1.grid(column=3, row=2)
        self.label1.configure(foreground="white")

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
        
        #============LABELS DEL JUGADOR============
        self.labelCarta1=tk.Label(self.ventana1,text="   ", background="brown",font=fuente)
        self.labelCarta1.grid(column=1, row=5)
        self.labelCarta1.configure(foreground="white")

        self.labelCarta2=tk.Label(self.ventana1,text="   ", background="brown",font=fuente)
        self.labelCarta2.grid(column=2, row=5)
        self.labelCarta2.configure(foreground="white")

        self.labelCarta3=tk.Label(self.ventana1,text="  ", background="brown",font=fuente)
        self.labelCarta3.grid(column=3, row=5)
        self.labelCarta3.configure(foreground="white")

        self.labelCarta4=tk.Label(self.ventana1,text="   ", background="brown",font=fuente)
        self.labelCarta4.grid(column=4, row=5)
        self.labelCarta4.configure(foreground="white")

        self.labelCarta5=tk.Label(self.ventana1,text="   ", background="brown",font=fuente)
        self.labelCarta5.grid(column=5, row=5)
        self.labelCarta5.configure(foreground="white")
        
        #============PRIMERAS DOS CARTAS DEL JUGADOR============
        self.jugador_carta1 = random.randint(1,10)
        self.total_cartas_jugador.set(self.jugador_carta1)
        self.labelCarta1.configure(text=self.jugador_carta1,background="white",foreground="black")
        
        self.jugador_carta2 = random.randint(1,10)
        self.total_cartas_jugador.set(self.total_cartas_jugador.get()+self.jugador_carta2)
        self.labelCarta2.configure(text=self.jugador_carta2,background="white",foreground="black")
        
        #============DECLARANDO BOTONES============
        self.botonPedir=tk.Button(self.ventana1,width=20,  text="Pedir", command=self.pedir,font=fuente_4)
        self.botonPedir.grid(column=0, row=6)
        
        self.botonQuedarse=tk.Button(self.ventana1,width=20,  text="Quedarse", command=self.quedarse,font=fuente_4)
        self.botonQuedarse.grid(column=6, row=6)

        self.botonReiniciar=tk.Button(self.ventana1,width=3,height=1,  text="R", command=self.reiniciar,font=fuente)
        self.botonReiniciar.grid(column=6, row=8)

        #============LABEL DE TOTAL DEL JUGADOR============
        self.suma_total_jugador_label=tk.Label(self.ventana1,text="Total: "+str(self.total_cartas_jugador.get()), background="black",font=fuente_2)
        self.suma_total_jugador_label.grid(column=0, row=7)
        self.suma_total_jugador_label.configure(foreground="white")

        #============LABEL DE TOTAL DE SKYNET============
        self.suma_total_skynet_label=tk.Label(self.ventana1, background="black",font=fuente_2, relief="solid")
        self.suma_total_skynet_label.grid(column=6, row=7)
        self.suma_total_skynet_label.configure(foreground="red")

        #============LABEL DE RESULTADO============
        self.resultado_label=tk.Label(self.ventana1,text=" \n ", background="black",font=fuente_3)
        self.resultado_label.grid(column=0, row=8)
        self.resultado_label.configure(foreground="white")
        
        self.ventana1.mainloop()
        
#============BOTON PEDIR============
    def pedir(self):
        self.contador.set(self.contador.get()+1)
        if self.contador.get() == 1:
            self.jugador_carta3 = random.randint(1,10)
            self.total_cartas_jugador.set(self.total_cartas_jugador.get()+self.jugador_carta3)
            self.labelCarta3.configure(text=self.jugador_carta3,background="white",foreground="black")

            if self.total_cartas_skynet.get() < 17:
                self.skynet_carta3 = random.randint(1,10)
                self.total_cartas_skynet.set(self.total_cartas_skynet.get()+self.skynet_carta3)

        elif self.contador.get() ==2:
            self.jugador_carta4 = random.randint(1,10)
            self.total_cartas_jugador.set(self.total_cartas_jugador.get()+self.jugador_carta4)
            self.labelCarta4.configure(text=self.jugador_carta4,background="white",foreground="black")

            if self.total_cartas_skynet.get() < 17:
                self.skynet_carta4 = random.randint(1,10)
                self.total_cartas_skynet.set(self.total_cartas_skynet.get()+self.skynet_carta4)
        elif self.contador.get() ==3:
            self.jugador_carta5 = random.randint(1,10)
            self.total_cartas_jugador.set(self.total_cartas_jugador.get()+self.jugador_carta5)
            self.labelCarta5.configure(text=self.jugador_carta5,background="white",foreground="black")
            
            if self.total_cartas_skynet.get() < 17:
                self.skynet_carta5 = random.randint(1,10)
                self.total_cartas_skynet.set(self.total_cartas_skynet.get()+self.skynet_carta5)

        self.suma_total_jugador_label.configure(text="Total: "+str(self.total_cartas_jugador.get()))
        
            
#============BOTON QUEDARSE============
    def quedarse(self):
        
        #============MOSTRAR LAS CARTAS DE SKYNET============
        self.label_skynet_Carta1.configure(text=self.skynet_carta1,background="white",foreground="black")
        self.label_skynet_Carta2.configure(text=self.skynet_carta2,background="white",foreground="black")
        
        #============Dependiendo del contador muestra las cartas:
        if self.contador.get() >=1:
            self.label_skynet_Carta3.configure(text=self.skynet_carta3,background="white",foreground="black")
        if self.contador.get() >=2:
            self.label_skynet_Carta4.configure(text=self.skynet_carta4,background="white",foreground="black")
        if self.contador.get() >=3:
            self.label_skynet_Carta5.configure(text=self.skynet_carta5,background="white",foreground="black")
            
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

        self.botonQuedarse.configure(state=tk.DISABLED)
        self.botonPedir.configure(state=tk.DISABLED)
        
#============BOTON REINICIAR============        
    def reiniciar(self):
        #============Reiniciar contador
        self.contador.set(0)

        #============Primeras dos cartas de skynet============
        self.skynet_carta1 = random.randint(1,10)
        self.total_cartas_skynet.set(self.skynet_carta1)

        self.skynet_carta2 = random.randint(1,10)
        self.total_cartas_skynet.set(self.total_cartas_skynet.get()+self.skynet_carta2)
        
        #============limpiar labels de skynet
        self.label_skynet_Carta1.configure(text="   ",background="brown",foreground="white")
        self.label_skynet_Carta2.configure(text="   ",background="brown",foreground="white")
        self.label_skynet_Carta3.configure(text="   ",background="brown",foreground="white")
        self.label_skynet_Carta4.configure(text="   ",background="brown",foreground="white")
        self.label_skynet_Carta5.configure(text="   ",background="brown",foreground="white")

        #============Reiniciar label total de Skynet
        self.suma_total_skynet_label.configure(text="")
        
        #============Primeras dos cartas del jugador============
        self.jugador_carta1 = random.randint(1,10)
        self.total_cartas_jugador.set(self.jugador_carta1)
        self.labelCarta1.configure(text=self.jugador_carta1)
        
        self.jugador_carta2 = random.randint(1,10)
        self.total_cartas_jugador.set(self.total_cartas_jugador.get()+self.jugador_carta2)
        self.labelCarta2.configure(text=self.jugador_carta2)
        
        #============limpiar labels del jugador
        self.labelCarta3.configure(text="   ",background="brown",foreground="white")
        self.labelCarta4.configure(text="   ",background="brown",foreground="white")
        self.labelCarta5.configure(text="   ",background="brown",foreground="white")

        #============Reiniciar label total del jugador
        self.suma_total_jugador_label.configure(text="Total: "+str(self.total_cartas_jugador.get()))
        self.resultado_label.configure(text="")

        #============Habilitar botones
        self.botonQuedarse.configure(state=tk.NORMAL)
        self.botonPedir.configure(state=tk.NORMAL)
            
aplicacion1=Aplicacion()