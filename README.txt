¿QUÉ ES BUSCAPYTHON?:

    Es un trabajo realizado para la asignatura de Inteligencia Artificial del 
    grado Ingeniería informática - Ingeniería del Software en la Universidad de 
    Sevilla.

    Buscapython contiene una implementación del juego "Buscaminas" junto con 
    un mecanismo de sugerencia probabilístico. Este mecanismo de sugerencia 
    está basado en una red bayesiana a la que se aplica inferencia exacta (en 
    concreto eliminación de variables) para calcular, en todo momento, la 
    casilla con menor probabilidad de contener una mina.

    Para más detalles ver el documento "Memoria Buscapython".


REQUISITOS:

    - Python 3: https://www.python.org/downloads/
    - Pgmpy: https://github.com/pgmpy/pgmpy
    - PyQt5: https://www.riverbankcomputing.com/software/pyqt/download5


ESTRUCTURA DEL CÓDIGO:

    En primer lugar tenemos un archivo "main.py", que es el que se encarga de 
    llamar o bien a los test, o bien directamente al código fuente para una 
    ejecución normal de la aplicación.

    El código fuente de la aplicación se encuentra en la carpeta "src/", y los 
    tests en la carpeta "tests/". Dentro de la carpeta "src/" tenemos los 
    siguientes ficheros:

    - additional_windows.py: Implementa las ventanas auxiliares de la interfaz.
    - square.py: Implementa la lógica de una casilla de forma individual.
    - board.py: Implementa la lógica del tablero junto con la ventana principal 
                del juego.
    
    Además, dentro de la carpeta "src/" se encuentra la carpeta "inference/",
    donde se encuentran los ficheros que implementan la lógica necesaria para
    realizar la inferencia. Dentro de esta última carpeta tenemos:

    - bayesian_network.py: Implementa la lógica necesaria para crear la red 
                bayesiana.
    - variable_elimination.py: Implementa el algoritmo de eliminación de 
                variables modificado, gracias al cuál se realizan las consultas 
                sobre la red bayesiana.


EJECUCIÓN:

    Para ejecutar el programa basta con ejecutar el archivo "main.py" desde un
    terminal con Python 3:
    
        $ python main.py

    Si se desea ejecutar el programa con una configuración de tablero distinta
    a la que viene por defecto (5x5 con 5 minas), se puede ejecutar lo siguiente:

        $ python main.py -4 -5 -6

    El primer argumento corresponde a la altura del tablero, el segundo a la
    anchura y el tercero al número de minas. En el ejemplo mostrado, se generaría
    un tablero de 4x5 con 6 minas. (Una vez iniciado el juego, también existe un 
    menú para poder personalizar el tablero).

    Para ejecutar el test de rendimiento de tiempo de ejecución es necesario 
    pasar los argumentos de configuración más un argumento extra, como se puede 
    ver en el ejemplo:
	
        $ python main.py --testime -4 -5 -6	

    Para ejecutar el test de efectividad del sistema (tasa de partidas ganadas)
    es necesario pasar los argumentos de configuración más un argumento extra:

        $ python main.py --testsuccess -4 -5 -6


    NOTA: En caso de introducir los argumentos de manera incorrecta, no se 
          mostrará ningún mensaje de error y se iniciará una partida con la 
          configuración por defecto.

    NOTA: La palabra clave usada en los ejemplos para ejecutar un archivo con 
          Python 3 es "python". Sin embargo, dependiendo del ordenador esta 
          palabra clave puede variar, como por ejemplo "py -3" o "python3".


DESCRIPCIÓN DE LA INTERFAZ:

    1.- Barra de menú:

        - Apartado "Juego". Dentro tenemos tres secciones:
            + "Nueva partida": Reinicia el juego y crea un nuevo tablero con las 
               mismas propiedades (anchura, altura y número de minas).
            + "Configurar partida": Abre una ventana para poder configurar las 
               propiedades (anchura, altura y número de minas) de la siguiente 
               partida.
            + "Resolver automáticamente": Esta opción emplea el algoritmo de 
               inferencia exacta (usado para la sugerencia de casillas) para 
               resolver de manera automática el tablero. Una vez resuelto, se 
               indicará al usuario si ha ganado o ha perdido y en la consola de 
               comandos aparecerán las posiciones de las casillas que ha ido 
               eligiendo el algoritmo.

        - Apartado "Ayuda". Dentro tenemos dos secciones:
            + "Reglas del juego del Buscaminas": Se describen las reglas del 
               juego y los controles básicos.
            + "Mecanismo de sugerencia": Se describe como usar el mecanismo de 
               sugerencia y la resolución automática.

    2.- Tablero de juego: 
        
        Al arrancar el programa se inicia por defecto un tablero de 5x5 con 5 
        minas.

    3.- Barra de estado (barra inferior de la ventana):

        Ofrece un contador de minas del tablero para que el usuario sepa en 
        todo momento cuántas minas hay en el tablero y cuántas banderas le 
        queda por poner. Cuando se coloca una bandera el contador se decrementa 
        en 1.


CONTROLES BÁSICOS:

    Los controles de Buscapython son los típicos de cualquier juego basado en
    el buscaminas:
    
    - Para revelar una casilla: hacer click izquierdo del ratón sobre dicha 
      casilla.
    - Para poner una bandera sobre una casilla: hacer click derecho del ratón 
      sobre dicha casilla.
    - Una vez acabado el juego es necesario, o bien crear una nueva partida con 
      la misma configuración (Juego > Nueva partida), o bien crear una nueva 
      partida con otra configuración (Juego > Configurar partida)
    - Tras elegir el primer movimiento de una partida, se marcará (de color 
      verde) en todo momento la casilla sugerida por el sistema. Será decisión 
      del usuario clickar sobre esa casilla u otra.