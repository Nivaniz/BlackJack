from PySide6 import QtCore, QtGui, QtWidgets
from helpers import absPath
import random


class Carta(QtWidgets.QLabel):
    """
        Clase que representa una carta en el juego.

        Parámetros:
        - imagenPath (str): Nombre de la imagen de la carta.
        - numero (int): Número de la carta.
        - nombre (str): Nombre de la carta (As, Dos, Tres, ...).
        - palo (str): Palo de la carta (Treboles, Diamantes, Corazones, Picas).
        - parent (QWidget): Widget padre, por defecto es None.
    """
        
    def __init__(self, imagenPath, numero, nombre, palo, parent=None):
        super().__init__(parent)
        # Propiedades de la carta
        self.imagenPath = imagenPath
        self.numero = numero
        self.nombre = nombre
        self.palo = palo
        self.visible = False
        
        # Configuración de la imagen
        self.imagen = QtGui.QPixmap(absPath("images/Reverso.png"))
        self.setPixmap(self.imagen)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # Fix Alpha
        self.setScaledContents(True) 
        # Tamaño base de la carta
        self.anchoBase = self.sizeHint().width()
        self.altoBase = self.sizeHint().height()
        
        # Grupo de animaciones para movimiento y reescalado
        self.animaciones = QtCore.QParallelAnimationGroup()

    def mostrar(self):
        """
        Muestra la imagen de la carta.
        """

        self.imagen = QtGui.QPixmap(absPath(f"images/{self.imagenPath}.png"))
        self.setPixmap(self.imagen)
        self.visible = True

    def esconder(self):
        """
        Esconde la carta mostrando la imagen reversa.
        """
        
        self.imagen = QtGui.QPixmap(absPath("images/Reverso.png"))
        self.setPixmap(self.imagen)
        self.visible = False

    def posicionar(self, x, y, sobreponer=True):
        """
        Posiciona la carta en la posición especificada.

        Parámetros:
        - x (int): Coordenada x.
        - y (int): Coordenada y.
        - sobreponer (bool): True para sobreponer la carta, False en caso contrario.
        """
        
        if sobreponer:
            self.raise_()  # Sobreponer la carta si es necesario
        self.move(x, y)

    def mover(self, x, y, duracion=1000, escalado=1, sobreponer=True):
        """
        Mueve la carta con animación de posición y reescalado.

        Parámetros:
        - x (int): Coordenada x final.
        - y (int): Coordenada y final.
        - duracion (int): Duración de la animación en milisegundos, por defecto es 1000.
        - escalado (float): Factor de escala para la animación de reescalado, por defecto es 1.
        - sobreponer (bool): True para sobreponer la carta, False en caso contrario.
        """
        
        if sobreponer:
            self.raise_()  # sobreponer la carta
        self.animaciones = QtCore.QParallelAnimationGroup()
        self.raise_()  # sobreponer la carta
        # Animación de movimiento
        pos = QtCore.QPropertyAnimation(self, b"pos")
        pos.setEndValue(QtCore.QPoint(x, y))
        pos.setDuration(duracion)
        # Animación de reescalado
        self.animaciones.addAnimation(pos)
        size = QtCore.QPropertyAnimation(self, b"size")
        size.setStartValue(QtCore.QSize(self.anchoBase, self.altoBase))
        size.setEndValue(QtCore.QSize(self.anchoBase * escalado, self.altoBase * escalado))
        size.setDuration(duracion)
        self.animaciones.addAnimation(size)
        # Iniciar las animaciones
        self.animaciones.start()

    def reestablecer(self):
        """
        Detiene las animaciones actuales y restaura los tamaños originales.
        """
        
        # Detener las animaciones actuales
        self.animaciones.stop()
        # Reiniciar el grupo de animaciones
        self.animaciones = QtCore.QParallelAnimationGroup()
        # Restaurar los tamaños originales
        self.resize(self.anchoBase, self.altoBase)



class Baraja(QtWidgets.QWidget):
    """
        Clase que representa la baraja de cartas en el juego.

        Parámetros:
        - parent (QWidget): Widget padre, por defecto es None.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        # Nombres y palos de las cartas
        nombres = ["As", "Dos", "Tres", "Cuatro", "Cinco", "Seis", "Siete", "Ocho", "Nueve", "Diez", "Jota", "Reina", "Rey"]
        palos = ["Treboles", "Diamantes", "Corazones", "Picas"]
        # Listas de cartas en la pila y cartas fuera de la pila
        self.cartas = []  # Lista de cartas en la pila
        self.jugadas = []  # Lista de cartas fuera de la pila
        # Crear cartas y añadirlas a la lista
        for palo in palos:
            for i, nombre in enumerate(nombres):
                carta = Carta(f"{i+1}{palo[0]}", i+1, nombre, palo, self)
                self.cartas.append(carta)  # Añadir a la lista
        self.mezclar()  # Mezclar las cartas

    def mezclar(self):
        """
        Mezcla las cartas en la pila.
        """
        
        random.shuffle(self.cartas)

    def extraer(self):
        """
        Extrae una carta de la pila.

        Retorna:
        - Carta or None: La carta extraída o None si la pila está vacía.
        """
        
        if len(self.cartas) > 0:
            carta = self.cartas.pop() # Sacar la última carta (la de arriba)
            self.jugadas.append(carta) # Añadir a la lista de cartas jugadas
            return carta
        return None

    def reiniciar(self):
        """
        Reinicia el juego: esconde, restablece y mezcla las cartas.
        """
        
        for carta in self.jugadas:
            carta.esconder()  # Esconder las cartas jugadas
            carta.reestablecer()  # Restablecer tamaños y animaciones
            self.cartas.append(carta)  # Recuperar las cartas jugadas
        self.jugadas = []  # Borrar todas las cartas jugadas
        self.mezclar()  # Mezclar la baraja
