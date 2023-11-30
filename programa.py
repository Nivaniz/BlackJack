import sys
from PySide6 import QtCore, QtGui, QtWidgets
from functools import partial
from helpers import absPath
from cartas import *


class Jugador:
    """
    Clase que representa a un jugador en el juego de Blackjack.

    Atributos:
    - mano: Lista de cartas en la mano del jugador.
    - nombre: Nombre del jugador.
    - puntos: Puntuación total de las cartas en la mano.
    - plantado: Indica si el jugador ha decidido plantarse en el juego.
    """
    
    def __init__(self, nombre):
        """
        Inicializa un nuevo jugador con el nombre proporcionado.

        Parámetros:
        - nombre (str): El nombre del jugador.
        """
        
        self.mano = []  # Lista para almacenar las cartas en la mano del jugador
        self.nombre = nombre  # Asigna el nombre proporcionado al jugador
        self.puntos = 0  # Inicializa la puntuación del jugador en 0
        self.plantado = False  # Inicialmente, el jugador no está plantado en el juego
    
    def sumar(self, carta):
        """
        Agrega una carta a la mano del jugador y recalcula la puntuación.

        Parámetros:
        - carta (Carta): La carta que se agrega a la mano del jugador.
        """
        
        self.mano.append(carta)  # Agrega la carta a la mano del jugador
        self.calcular()  # Recalcula la puntuación total
    
    def calcular(self):
        """
        Calcula la puntuación total de las cartas en la mano del jugador,
        considerando la lógica de los ases.
        """
        
        self.puntos = 0 # Reinicia la puntuación
        # Suma las cartas que no son ases y que son visibles
        for carta in self.mano:
            if carta.visible:
                if carta.nombre not in ["As", "Jota", "Reina", "Rey"]:
                    self.puntos += carta.numero
                elif carta.nombre in ["Jota", "Reina", "Rey"]:
                    self.puntos += 10
        # Sumamos los ases que son visibles
        for carta in self.mano:
            if carta.visible:
                if carta.nombre == "As":
                    self.manejar_ases() # Llamada a la función para manejar la lógica de los ases
    
    def manejar_ases(self):
        """
        Maneja la lógica de los ases en la mano del jugador.
        Si la suma de los puntos con un as igual a 11 no supera 21, se suma 11; 
        de lo contrario, se suma 1 por cada as.
        """
        
        for carta in self.mano:
            if carta.visible and carta.nombre == "As":
                if self.puntos + 11 <= 21:
                    self.puntos += 11
                else:
                    self.puntos += 1
                    

    def consultar(self):
        """
        Imprime en la consola la información de la mano del jugador,
        mostrando solo las cartas visibles y la puntuación total.
        """
        
        print(f"{self.nombre}: {[f'{c.nombre} de {c.palo}' for c in self.mano if c.visible]} ({self.puntos})")


class Blackjack:
    """
    Clase que representa el juego de Blackjack.

    Atributos:
    - baraja (Baraja): La baraja de cartas utilizada en el juego.
    - humano (Jugador): El jugador humano.
    - banca (Jugador): El jugador que representa la banca del casino.
    """
    
    def __init__(self, baraja):
        """
        Inicializa una nueva instancia del juego de Blackjack.

        Parámetros:
        - baraja (Baraja): La baraja de cartas que se utilizará en el juego.
        """
        
        self.baraja = baraja  # Asigna la baraja proporcionada al juego
        self.humano = Jugador("Jugador 1")  # Crea un jugador humano con nombre "Jugador 1"
        self.banca = Jugador("Banca")  # Crea un jugador que representa la banca
        
    
    def repartir(self, jugador, voltear=True):  
        """
        Reparte una carta al jugador especificado.

        Parámetros:
        - jugador (Jugador): El jugador al que se le repartirá la carta.
        - voltear (bool): Indica si la carta debe mostrarse volteada. Por defecto, True.

        Retorna:
        - carta (Carta): La carta repartida al jugador.
        """
        
        carta = self.baraja.extraer()  # Extrae una carta de la baraja
        if carta:
            if voltear:
                carta.mostrar()  # Muestra la carta si es necesario voltearla
            jugador.sumar(carta)  # Añade la carta al jugador
        return carta

    def ganador(self):
        """
        Determina el ganador del juego.

        Retorna:
        - int: 0 si hay empate, 1 si gana el jugador humano, o 2 si gana la banca.
        """
        
        if self.humano.puntos > 21:
            return 2
        if self.banca.puntos > 21:
            return 1
        if self.humano.puntos > self.banca.puntos:
            return 1
        elif self.banca.puntos > self.humano.puntos:
            return 2
        else:
            return 0
    
    def comprobarGanador(self):
        """
        Imprime en la consola el resultado del juego (Ganador, Perdedor o Empate).
        """
        
        ganador = self.ganador()
        if ganador == 2:
            print("Gana la banca")
        elif ganador == 1:
            print("Gana el jugador")
        else:
            print("Empate")      
    
    def reiniciar(self):
        """
        Reinicia el juego restableciendo la baraja y creando nuevos jugadores.
        """
        
        self.baraja.reiniciar()  # Restablece la baraja
        self.humano = Jugador("Jugador 1")  # Crea un nuevo jugador humano
        self.banca = Jugador("Banca")  # Crea un nuevo jugador que representa la banca 
        
              
class MainWindow(QtWidgets.QMainWindow):
    """
        Clase principal que representa la ventana principal del juego de 21.

    """
    
    def __init__(self):
        super().__init__()
        # Configuramos la ventana y el fondo
        self.setWindowTitle("21")
        self.setFixedSize(900, 630)
        # Configuración de la baraja
        self.baraja = Baraja(self)
        self.setCentralWidget(self.baraja)
        # Crear el juego
        self.bj = Blackjack(self.baraja)
        # Interfaz (después de asignar el widget central para sobreponerla)
        self.setupUi()
        # Posicionamos las cartas y hacemos el reparto inicial
        self.preparar()
        # Creamos las señales
        self.btnPedir.clicked.connect(self.pedir)
        self.btnPlantar.clicked.connect(self.plantar)
        self.btnReiniciar.clicked.connect(self.reiniciar)
        # fINALIZACIÓN
        self.finalizado = False

    def preparar(self):
        """ Posiciona la baraja inicial y ejecuta los primeros repartos"""
        self.registro.append(f"== Inicio ==")
        offset = 0
        for carta in self.baraja.cartas:
            carta.posicionar(45 + offset, 205 + offset)
            offset += 0.25
        # activar los botones
        self.habilitar_botones()
        # Haremos el reparto inicial de cartas
        self.repartir(self.bj.humano)
        self.repartir(self.bj.humano)
        self.repartir(self.bj.banca)
        self.repartir(self.bj.banca, False)

    def repartir(self, jugador, voltear=True):
        """
        Reparte una carta al jugador y realiza la animación correspondiente.

        Parámetros:
        - jugador (Jugador): Jugador al que se le repartirá la carta.
        - voltear (bool): True para mostrar la carta, False para ocultarla.
        """
        
        carta = self.bj.repartir(jugador, voltear)
        if jugador == self.bj.humano:
            offset_x = len(self.bj.humano.mano) * 40
            carta.mover(195+offset_x, 320, duracion=750)
        elif jugador == self.bj.banca:
            offset_x = len(self.bj.banca.mano) * 25
            carta.mover(251+offset_x, 110, duracion=750, escalado=0.8)
        self.marcadores()


    def pedir(self):
        """ Desactiva los botones de la interfaz y pide una carta """
        self.deshabilitar_botones()
        self.repartir(self.bj.humano)
        self.comprobar()
    
    def comprobar(self):
        """
        Comprueba la puntuación del jugador y habilita los botones correspondientes.
        """
        
        self.habilitar_botones()
        if self.bj.humano.puntos >= 21:
            self.bj.humano.plantado = True
            self.jugarBanca()

    def plantar(self):
        """ Planta al usuario e inicia la jugada de la banca """
        self.deshabilitar_botones()
        self.bj.humano.plantado = True
        self.jugarBanca()
    
    def jugarBanca(self):
        """
        Lógica de la jugada de la banca, incluyendo la animación de las cartas.
        """
        
        if self.bj.humano.puntos > 21:
            self.bj.banca.plantado = True 
            self.mostrar_cartas_banca()
        else:
            # si la banca tiene dos cartas voltearemos la segunda y calcularemos su puntuación
            if len(self.bj.banca.mano) == 2:
                self.bj.banca.mano[-1].mostrar()
                self.bj.banca.calcular()
                # además actualizamos el marcador
                self.marcadores()
            # si la banca tiene 17 puntos o más la plantamos
            # o si la banca tiene más puntos que el jugador
            if self.bj.banca.puntos >= 17 or self.bj.banca.puntos > self.bj.humano.puntos:
                self.bj.banca.plantado = True
            # si la banca no se ha plantado, le repartiremos una carta
            if not self.bj.banca.plantado:
                self.repartir(self.bj.banca)
                self.jugarBanca()
        # comprobamos el ganador siempre al final del turno de la banca
        self.ganador()
        self.habilitar_botones()


    def reiniciar(self):
        # Reiniciar el juego: esconder, reestablecer y mezclar las cartas
        self.finalizado = False
        self.marcadorJugador.setText("0")
        self.marcadorBanca.setText("0")
        self.registro.setText("")
        self.bj.reiniciar()
        self.preparar()
        
    def marcadores(self):
        """
        Actualiza los marcadores de puntuación en la interfaz.
        """
        
        self.marcadorJugador.setText(f"{self.bj.humano.puntos}")
        self.marcadorBanca.setText(f"{self.bj.banca.puntos}")
        self.registro.append(f"{self.bj.humano.nombre} [{self.bj.humano.puntos}], {self.bj.banca.nombre} [{self.bj.banca.puntos}]")
        self.registro.verticalScrollBar().setValue(self.registro.verticalScrollBar().maximum())

    def ganador(self):
        """
        Comprueba el ganador y actualiza el registro en la interfaz.
        """
        
        if self.bj.humano.plantado and self.bj.banca.plantado and not self.finalizado:
            if self.bj.ganador() == 2:
                self.registro.append(f"== Ganador {self.bj.banca.nombre} ==")
            elif self.bj.ganador() == 1:
                self.registro.append(f"== Ganador {self.bj.humano.nombre} ==")
            else:
                self.registro.append(f"====== Empate ======")
            self.registro.verticalScrollBar().setValue(self.registro.verticalScrollBar().maximum())
            self.finalizado = True
    
    def habilitar_botones(self):
        """
        Habilita los botones de la interfaz.
        """
        
        self.btnPedir.setEnabled(True)
        self.btnPlantar.setEnabled(True)
        self.btnReiniciar.setEnabled(True)
    
    def deshabilitar_botones(self):
        """
        Deshabilita los botones de la interfaz.
        """
        
        self.btnPedir.setEnabled(False)
        self.btnPlantar.setEnabled(False)
        self.btnReiniciar.setEnabled(False)
    
    def mostrar_cartas_banca(self):
        # Mostrar las cartas de la banca cuando el jugador ha perdido
        for carta in self.bj.banca.mano:
            carta.mostrar()
        self.bj.banca.calcular()
        self.marcadores()


    def setupUi(self):
        self.setStyleSheet("""
            QTextEdit {background-color: #ddd; font-size:13px }
            QLabel { color: white; font-size: 40px; font-weight: 500 }
            QPushButton { background-color: #20581e; color: white;font-size: 15px }
            QPushButton:disabled { background-color: #163914 }""")
        # Configuración del fondo
        tablero = QtGui.QImage(absPath("images/Tablero.png"))
        paleta = QtGui.QPalette()
        paleta.setBrush(QtGui.QPalette.Window, QtGui.QBrush(tablero))
        self.setPalette(paleta)
        # Marcadores
        self.marcadorBanca = QtWidgets.QLabel("0", self)
        self.marcadorBanca.resize(50, 50)
        self.marcadorBanca.move(342, 19)
        self.marcadorJugador = QtWidgets.QLabel("0", self)
        self.marcadorJugador.resize(50, 50)
        self.marcadorJugador.move(355, 557)
        # Botones
        self.btnPedir = QtWidgets.QPushButton("Pedir carta", self)
        self.btnPedir.resize(175, 32)
        self.btnPedir.move(692, 495)
        self.btnPlantar = QtWidgets.QPushButton("Quedarse", self)
        self.btnPlantar.resize(175, 32)
        self.btnPlantar.move(692, 535)
        self.btnReiniciar = QtWidgets.QPushButton("Reiniciar", self)
        self.btnReiniciar.resize(175, 32)
        self.btnReiniciar.move(692, 575)
        # Texto para el registro
        self.registro = QtWidgets.QTextEdit(self)
        self.registro.setReadOnly(True)
        self.registro.move(692, 285)
        self.registro.resize(175, 185)
 

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
