
DESCRIPCIÓN:

    Este programa contiene una implementación del juego "Buscaminas" junto con 
    un mecanismo de sugerencia probabilístico. Este mecanismo de sugerencia 
    está basado en una Red Bayesiana a la que se aplica inferencia exacta (en 
    concreto eliminación de variables) para calcular, en todo momento, la 
    casilla con menor probabilidad de contener una mina.

    Para más detalles ver la documentación en "./docs/Documentación.doc".


REQUISITOS:

    - Python 3: https://www.python.org/downloads/
    - Pgmpy: https://github.com/pgmpy/pgmpy
    - PyQt5: https://www.riverbankcomputing.com/software/pyqt/download5


EJECUCIÓN:

    Para ejecutar el programa basta con ejecutar el archivo "main.py" desde la
    consola de comandos:
    
        $ python main.py

    Si se desea ejecutar el programa con una configuración de tablero distinta
    a la que viene por defecto (5x5 con 5 minas), se puede ejecutar lo siguiente:

        $ python main.py -4 -5 -6

    El primer argumento corresponde a la altura del tablero, el segundo a la
    anchura y el tercero al número de minas. En el ejemplo mostrado, se generaría
    un tablero de 4x5 con 6 minas.

    Una vez iniciado el juego, también existe un menú para poder personalizar el
    tablero.

    Para ejecutar el test de rendimiento de tiempo de ejecución es necesario 
    pasar los argumentos de configuración más un argumento extra, como se puede 
    ver en el ejemplo:
	
        $ python main.py --testime -4 -5 -6	


MENÚ Y OPCIONES DEL JUEGO:

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