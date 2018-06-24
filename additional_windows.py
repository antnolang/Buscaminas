from PyQt5 import QtGui
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QGridLayout,
                             QLayout, QSpinBox, QPushButton, QDialogButtonBox,
                             QMessageBox)


TEXT_RULES = '<h1>Reglas básicas del buscaminas</h1><p>El juego consiste en despejar todas las casillas de una pantalla que no oculten una mina.</p><p>Algunas casillas tienen un número, el cual indica la cantidad de minas que hay en las casillas circundantes. Así, si una casilla tiene el número 3, significa que de las ocho casillas que hay alrededor (si no es en una esquina o borde) hay 3 con minas y 5 sin minas. Si se descubre una casilla sin número indica que ninguna de las casillas vecinas tiene mina y éstas se descubren automáticamente.</p><p>Si se descubre una casilla con una mina se pierde la partida.</p><p>Se puede poner una marca en las casillas que el jugador piensa que hay minas para ayudar a descubrir las que están cerca.</p><h3>Controles</h3><p>Para descubrir una casilla oculta basta con hacer click izquierdo sobre ella y para marcarla, click derecho sobre la misma.</p><p>Las marcas se pueden poner y quitar pulsando repetidamente click derecho sobre la casilla.</p><p>Solo se pueden descubrir (click izquierdo) casillas que no estén marcadas.</p>'
TEXT_SUGGESTION = '<h1>Mecanismo de sugerencia de casillas</h1><p>La implementación de este buscaminas incluye un mecanismo que sugiere las casillas con menor probabilidad de contener una mina.</p><p>Las minas sugeridas son aquellas con el fondo de color verde.</p><p>El mecanismo de sugerencia está basado en redes bayesianas y calcula las probabilidades mediante inferencia exacta. Sin embargo, al tratarse de una sugerencia probabilística, habrá casos en los que la casilla sugerida pueda contener una mina.</p><h3>Resolución automática</h3><p>El juego también posee una opción para la resolución automática del juego usando el mismo mecanismo de sugerencia. Como se ha mencionado anteriormente, este mecanismo de sugerencia es probabilístico, por lo que habrá ocasiones en las que la propia resolución automática falle.</p><p>Para usar esta opción, seleccionar en el menú Juego &gt; Resolver automáticamente, o pulsar Ctrl+A.</p><p>En caso de usar la resolución automática, se puede ver en la pantalla del terminal la posición de las casillas que ha ido seleccionando el mecanismo.</p>'

IMAGE_ICON = 'images/icon.png'

class Configuration(QDialog):

    def __init__(self, main_window):
        super().__init__()

        # Obtenemos la QMainWindow para poder llamarla al enviar el formulario
        self.main_window = main_window
        
        # Inicializar texto de cabecera
        guide = QLabel('<h3>Introduce los siguientes parámetros para' 
                       + ' configurar la partida</h3>')
        
        
        # Inicializar etiquetas de los campos del formulario
        height_label = QLabel('Altura: ')
        width_label = QLabel('Anchura: ')
        num_of_mines_label = QLabel('Número de minas: ')

        # Inicializar campos del formulario
        self.height_spin = QSpinBox()
        self.height_spin.setRange(1, 10)
        self.width_spin = QSpinBox()
        self.width_spin.setRange(1, 10)
        self.num_of_mines_spin = QSpinBox()
        self.num_of_mines_spin.setMinimum(1)

        # Inicializar botones de envío del formulario
        button_box = QDialogButtonBox()
        button_box.addButton(button_box.Ok)
        button_box.addButton(button_box.Cancel)
        button_box.button(QDialogButtonBox.Ok).setText('Aceptar')
        button_box.button(QDialogButtonBox.Cancel).setText('Cancelar')
        button_box.setCenterButtons(True)

        button_box.accepted.connect(self.init_game)
        button_box.rejected.connect(self.close)
        
        # Inicializar etiqueta de errores del formulario
        self.form_errors = QLabel('')
        self.form_errors.setStyleSheet('color: red')
        self.form_errors.setWordWrap(True)

        # Configuración de layouts
        self.grid = QGridLayout()
        self.grid.addWidget(height_label, 0, 0)
        self.grid.addWidget(self.height_spin, 0, 1)
        self.grid.addWidget(width_label, 1, 0)
        self.grid.addWidget(self.width_spin, 1, 1)
        self.grid.addWidget(num_of_mines_label, 2, 0)
        self.grid.addWidget(self.num_of_mines_spin, 2, 1)
        self.grid.setSizeConstraint(QLayout.SetFixedSize)

        ver_box = QVBoxLayout()
        ver_box.addWidget(guide)
        ver_box.addLayout(self.grid)
        ver_box.addWidget(button_box)
        ver_box.addWidget(self.form_errors)

        # Pasar a QDialog los layouts con los elementos inicializados
        self.setLayout(ver_box)

        # Inicialización del resto de atributos de la ventana
        self.setWindowTitle('Configuración')
        self.adjustSize()
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon(IMAGE_ICON))
        self.show()

    def init_game(self):
        height = self.height_spin.value()
        width = self.width_spin.value()
        num_of_mines = self.num_of_mines_spin.value()

        if self.check_params(height, width, num_of_mines):
            self.main_window.close()
            self.main_window.__init__(height, width, num_of_mines)
            self.close()
        else:
            self.form_errors.setText('Valores incorrectos. Recuerda que el' 
                            + ' número de minas del tablero debe ser menor'
                            + ' que el número total de casillas.')

    def check_params(self, height, width, num_of_mines):
        return num_of_mines < height*width


class Help(QDialog):

    def __init__(self, text):
        super().__init__()

        widget = QLabel()
        widget.setText(text)
        widget.setWordWrap(True)

        layout = QVBoxLayout()
        layout.addWidget(widget)

        self.setLayout(layout)
        self.setWindowTitle('Ayuda')
        self.setWindowIcon(QtGui.QIcon(IMAGE_ICON))
        self.show()


class HelpRules(Help):

    def __init__(self):
        super().__init__(TEXT_RULES)
        self.setGeometry(0, 0, 700, 400)


class HelpSuggestion(Help): 

    def __init__(self):
        super().__init__(TEXT_SUGGESTION)
        self.setGeometry(0, 0, 700, 400)


class EndGame(QMessageBox):

    def __init__(self, victory):
        super().__init__()

        if victory:
            self.setText('¡Felicidades! Has ganado')
            self.setWindowTitle('Has ganado')
        else:
            self.setText('Has perdido')
            self.setWindowTitle('Has perdido')

        self.addButton('Aceptar', QMessageBox.AcceptRole)        
        self.setIcon(QMessageBox.Information)
        self.setWindowIcon(QtGui.QIcon(IMAGE_ICON))
        self.adjustSize()
        self.setFixedSize(self.size())
        self.show()