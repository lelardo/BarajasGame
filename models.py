import random
import pygame
import sys
import time
from pygame.locals import *

# Inicializa pygame
pygame.init()

# Define el tamaño de la pantalla
tamanio = ancho, alto = 1024, 768

# Inicializa la fuente
pygame.font.init()
fuente = pygame.font.SysFont("monospace", 15)
pantalla = pygame.display.set_mode(tamanio)
clock = pygame.time.Clock()
pygame.display.set_caption("Solitario Reloj")
halved = pygame.image.load("deck/b2pr.gif")
halved_rect = halved.get_rect()
negro = 0, 0, 0
background_image = pygame.image.load("deck/background.jpg")  # Cambia por tu imagen
background_image = pygame.transform.scale(background_image, (ancho, alto))
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
GRIS = (100, 100, 100)
FONDO_COLOR = (50, 50, 50)
fuente = pygame.font.Font(None, 74)
fuente_botones = pygame.font.SysFont("comicsansms", 40, bold=True)
fuente_titulo = pygame.font.SysFont("comicsansms", 70, bold=True)
fuente_texto = pygame.font.SysFont("comicsansms", 20, bold=True)
ANCHO, ALTO = 800, 600
# Define las posiciones de las cartas en la pantalla
posiciones = [
    (ancho / 2 - 200, alto / 2 - 300),
    (ancho / 2 - 50, alto / 2 - 300),
    (ancho / 2 + 100, alto / 2 - 300),
    (ancho / 2 + 225, alto / 2 - 200),
    (ancho / 2 + 225, alto / 2 - 75),
    (ancho / 2 + 225, alto / 2 + 50),
    (ancho / 2 + 100, alto / 2 + 150),
    (ancho / 2 - 50, alto / 2 + 150),
    (ancho / 2 - 200, alto / 2 + 150),
    (ancho / 2 - 325, alto / 2 + 50),
    (ancho / 2 - 325, alto / 2 - 75),
    (ancho / 2 - 325, alto / 2 - 200),
    (ancho / 2 - 50, alto / 2 - 75),
]


# Clase que representa una carta de la baraja
class card:
    # Color rosa claro en hexadecimal
    colors = [0x8E7F48, 0xC5E5EA, 0x7F7F7F, 0xAE9C88, 0x919192, 0xFFFFFE, 0xD56F44, 0xE2E2E1, 0xD5D5E8, 0xFAC78E]
    backfaces = ["calaca", "geom", "greek", "maya", "rara", "sheng", "magic", "uno", "poke", "yugi"]
    sele = 9
    TINT_COLOR = colors[sele]  # Color de tinte para las cartas, agregar para las ultimas 4 cartas

    def __init__(self, type, value):
        self.type = type
        self.value = value
        self.volteada = True
        self.set_backface()

    def set_backface(self):
        if GLOBAL_BACKFACE_INDEX < 0 or GLOBAL_BACKFACE_INDEX >= len(self.backfaces):
            # Usar diseño por defecto si el índice no es válido
            self.carta_imagen = pygame.image.load("deck/b2fv.gif").convert()
        else:
            # Cargar la cara trasera seleccionada
            backface_name = self.backfaces[GLOBAL_BACKFACE_INDEX]
            self.carta_imagen = pygame.image.load(f"deck/backfaces/{backface_name}.png").convert()

    def _load_and_tint(self, image_path):
        # Convertimos el hexadecimal a RGB
        r = (self.TINT_COLOR >> 16) & 255
        g = (self.TINT_COLOR >> 8) & 255
        b = self.TINT_COLOR & 255

        # Carga la imagen y la convierte al formato correcto
        original = pygame.image.load(image_path).convert()
        tinted = original.copy()

        # Aplicamos el tinte pixel por pixel
        for x in range(tinted.get_width()):
            for y in range(tinted.get_height()):
                color = tinted.get_at((x, y))
                # Solo modificamos los píxeles blancos o casi blancos
                if color.r > 240 and color.g > 240 and color.b > 240:
                    tinted.set_at((x, y), (r, g, b))

        return tinted

    def frente(self):
        self.volteada = False
        self.carta_imagen = self._load_and_tint(
            "deck/" + self.simbolo() + str(self.value) + ".gif"
        )

    def reverso(self):
        self.volteada = True
        self.carta_imagen = pygame.image.load("deck/b2fv.gif").convert()

    def simbolo(self):
        if self.type == "hearts":
            return "h"
        if self.type == "diamonds":
            return "d"
        if self.type == "clubs":
            return "c"
        if self.type == "spades":
            return "s"

    def toString(self):
        return f"Simbolo: {self.type}, Valor: {self.value}"


# Clase que representa al croupier
class croupier:
    def __init__(self):
        self.deck = []  # Baraja de cartas (baraja general)
        self.diamonDeck = []  # Baraja de diamantes
        self.heartsDeck = []  # Baraja de corazones
        self.clubsDeck = []  # Baraja de tréboles
        self.spadesDeck = []  # Baraja de picas
        self.arrays_mini = [
            [] for _ in range(13)
        ]  # pequeños arrays de 4 cartas, simulan los grupos de 4 cartas en el juego

        # Inicializa las cartas de la baraja sin ponerlas en ella
        for i in range(1, 14):
            self.heartsDeck.append(card("hearts", i))  # crea las cartas de corazones
            self.diamonDeck.append(card("diamonds", i))  # crea las cartas de diamantes
            self.clubsDeck.append(card("clubs", i))  # crea las cartas de tréboles
            self.spadesDeck.append(card("spades", i))  # crea las cartas de picas

    def init_deck(self):
        self.deck = []  # vacia la baraja porsiacaso
        types = [
            self.heartsDeck,
            self.diamonDeck,
            self.clubsDeck,
            self.spadesDeck,
        ]  # tipos de cartas
        for deck_type in types:  # recorre los tipos de cartas
            self.deck.extend(deck_type)  # añade las cartas al mazo general
        self.shuffle()  # baraja la baraja segun nuestro metodo

    def shuffle(self):  # Método que baraja la baraja humanamente
        if not self.deck:  # si la baraja está vacía, no se puede barajar
            print("La baraja está vacía. No se puede barajar.")
            return  # termina la función

        shuffle_count = random.randint(
            5, 10
        )  # cantidad de veces que se barajará la baraja

        for _ in range(shuffle_count):  # baraja la baraja shuffle_count veces
            mid = len(self.deck) // 2  # divide la baraja en dos
            first_half = self.deck[:mid]  # primera mitad de la baraja
            second_half = self.deck[mid:]  # segunda mitad de la baraja
            self.deck = []  # vacía la baraja para volver a rellenarla

            while (
                    first_half or second_half
            ):  # mientras haya cartas en alguna de las mitades
                if first_half:  # para la primera mitad
                    num_from_first = random.randint(
                        1, min(len(first_half), 4)
                    )  # cantidad de cartas que se sacarán de la primera mitad
                    for _ in range(num_from_first):  # por cada carta que se sacará
                        if first_half:  # si hay cartas en la primera mitad
                            self.deck.append(
                                first_half.pop(0)
                            )  # saca la carta de la primera mitad y la añade a la baraja

                if second_half:  # para la segunda mitad
                    num_from_second = random.randint(
                        1, min(len(second_half), 4)
                    )  # cantidad de cartas que se sacarán de la segunda mitad
                    for _ in range(num_from_second):  # por cada carta que se sacará
                        if second_half:  # si hay cartas en la segunda mitad
                            self.deck.append(
                                second_half.pop(0)
                            )  # saca la carta de la segunda mitad y la añade a la baraja

    def posicionate(self):  # Método que posiciona las cartas en los grupos de 4 cartas
        counter = 0  # contador para saber en qué grupo de 4 cartas se está
        for i in range(len(self.deck)):  # recorre la baraja
            self.arrays_mini[counter].append(
                self.deck[i]
            )  # añade la carta al grupo de 4 cartas correspondiente
            counter += 1  # aumenta el contador
            if counter == 13:  # si el contador llega a 13
                counter = 0  # reinicia el contador
        self.arrays_mini[12][0].frente()  # voltea la primera carta del último grupo

    def card_game(self):
        aux_end = 0  # Contador para verificar si todos los grupos están completos
        act_array = 12  # Empezamos en el último grupo (13 - 1)
        control = [
            0 for _ in range(13)
        ]  # Control para saber cuántas cartas tiene cada grupo

        while True:
            # Verifica si ya no hay cartas en el grupo actual
            if not self.arrays_mini[act_array]:
                print(
                    f"El grupo {act_array} está vacío. No hay más cartas para mover. ¡Has perdido!"
                )
                break

            # Obtén la carta actual del grupo activo
            act_card = self.arrays_mini[act_array].pop(
                0
            )  # Tomamos la carta de la cabeza del grupo actual
            print(
                f"Carta actual: {act_card.toString()}"
            )  # Imprime la carta que estamos jugando

            # Calcula el índice del siguiente grupo
            next_array = act_card.value - 1

            # Verifica si el grupo de destino ya está lleno (4 cartas)
            if control[next_array] == 4:
                print(
                    f"El grupo {next_array} ya está completo. ¡No puedes mover más cartas! ¡Has perdido!"
                )
                break

            # Mueve la carta al grupo correspondiente
            self.arrays_mini[next_array].append(act_card)

            # Actualiza el contador del grupo
            control[next_array] += 1
            if control[next_array] == 4:  # Si un grupo tiene 4 cartas completas
                aux_end += 1
                print(f"Grupo {next_array} completo.")

            # Verifica si se han completado todos los grupos
            if aux_end >= 13:  # Si todos los grupos tienen 4 cartas
                print("¡Todos los grupos están completos! ¡Has ganado!")
                break

            # Actualiza el grupo activo
            act_array = next_array

            # Verifica si ya no hay cartas en ningún grupo excepto en el activo
            if all(
                    len(group) == 0
                    for i, group in enumerate(self.arrays_mini)
                    if i != act_array
            ):
                print("No hay más cartas disponibles en otros grupos. ¡Has perdido!")
                mostrar_mensaje("¡Game Over!", ANCHO // 2 - 150, ALTO // 2, ROJO)

            # Imprime el estado actual de los grupos
            self.imprimir_grupos()

    def imprimir_grupos(self):  # Método que imprime los grupos de 4 cartas
        for i in range(len(self.arrays_mini)):  # recorre los grupos de 4 cartas
            print(f"Array {i}:")  # imprime el número de grupo
            for card in self.arrays_mini[i]:  # recorre las cartas del grupo
                print(card.toString())  # imprime la carta
        print("")

    def comprobar_grupos(self, ite):
        aux = 0;
        if ite != 12:
            if len(self.arrays_mini[ite]) == 4:
                for carta in self.arrays_mini[ite]:
                    if carta.volteada == True:
                        break
                else:
                    grupos_completos[ite] = True
        else:
            for carta in self.arrays_mini[ite]:
                if carta.volteada == True:
                    break
                if carta.value == 13:
                    aux += 1
            if aux == 4:
                grupos_completos[ite] = True


"""METODOS UI"""


def dibujar_cartas(wid, hei, hour, dealer, coords):
    offset = 0  # Desplazamiento inicial para apilar las cartas
    aux = reversed(dealer.arrays_mini[hour])

    # Coordenadas iniciales
    start_x, start_y = coords

    cartas_colocadas = []  # Mantiene un registro de las cartas ya colocadas

    for i, carta in enumerate(aux):
        # Calcula la posición inicial y final para cada carta
        end_x = wid - offset
        end_y = hei
        current_x = start_x
        current_y = start_y

        # Animación de la carta desde coords hasta (end_x, end_y)
        steps = 30  # Número de pasos en la animación
        for step in range(steps):
            # Interpolación lineal de posición
            current_x = start_x + (end_x - start_x) * (step / steps)
            current_y = start_y + (end_y - start_y) * (step / steps)

            # Redibuja el fondo
            pantalla.blit(background_image, (0, 0))  # Ajusta según tu contexto
            for j in range(hour):
                dibujar_grupos(posiciones[j][0], posiciones[j][1], j, dealer)

            # Redibuja las cartas ya colocadas
            for colocada, (x, y) in cartas_colocadas:
                pantalla.blit(colocada.carta_imagen, (x, y))

            # Dibuja la carta en movimiento
            pantalla.blit(carta.carta_imagen, (current_x, current_y))

            # Actualiza la pantalla y espera un momento
            pygame.display.flip()
            time.sleep(0.00001)

        # Agrega la carta a la lista de cartas colocadas
        cartas_colocadas.append((carta, (end_x, end_y)))

        # Actualiza el desplazamiento para la siguiente carta
        offset -= 12  # Incrementa el desplazamiento horizontal para apilar las cartas


def dibujar_grupos(wid, hei, hour, dealer):
    # Dibuja las cartas del grupo actual (hour) en la posición especificada (wid, hei)
    offset = 0  # Desplazamiento inicial para apilar las cartas
    aux = reversed(dealer.arrays_mini[hour])
    for i, carta in enumerate(aux):
        if i == 3:
            # Dibuja la primera carta completa
            pantalla.blit(carta.carta_imagen, (wid - offset, hei))
        else:
            # Dibuja las siguientes cartas con un desplazamiento para que se apilen
            pantalla.blit(carta.carta_imagen, (wid - offset, hei))
        offset -= 12  # Incrementa el desplazamiento horizontal para apilar las cartas


def mostrar_mensaje(texto, x, y, color=BLANCO):
    mensaje = fuente.render(texto, True, color)
    pantalla.blit(mensaje, (x, y))


def dibujar_boton(texto, x, y, ancho, alto, color, color_texto, accion=None):
    pygame.draw.rect(pantalla, color, (x, y, ancho, alto))
    mensaje = fuente_botones.render(texto, True, color_texto)
    pantalla.blit(
        mensaje,
        (
            x + (ancho - mensaje.get_width()) // 2,
            y + (alto - mensaje.get_height()) // 2,
        ),
    )
    return pygame.Rect(x, y, ancho, alto)


"""METODOS JUEGO"""


# Función para dibujar el tablero
def tablero_animacion(dealer, coords):
    for i in range(13):
        dibujar_cartas(posiciones[i][0], posiciones[i][1], i, dealer, coords)
        if i == 12:  # Último grupo
            return False
    pygame.display.flip()


def tablero(dealer):
    for i in range(13):
        dibujar_grupos(posiciones[i][0], posiciones[i][1], i, dealer)
    pygame.display.flip()


def mostrar_menu_inicial():
    backfaces = card.backfaces
    global GLOBAL_BACKFACE_INDEX
    GLOBAL_BACKFACE_INDEX = 0
    while True:
        pantalla.blit(background_image, (0, 0))

        # Título centrado con una fuente bonita
        titulo = fuente_titulo.render("Solitario Reloj", True, BLANCO)
        pantalla.blit(titulo, (ancho // 2 - titulo.get_width() // 2, alto // 4))
        # Botones centrados
        boton_manual = dibujar_boton(
            "Jugar Manual", ancho // 2 - 200, alto // 2 - 50, 400, 60, GRIS, BLANCO
        )
        boton_auto = dibujar_boton(
            "Jugar Automático", ancho // 2 - 200, alto // 2 + 50, 400, 60, GRIS, BLANCO
        )
        boton_dorsal_superior = dibujar_boton(
            "<<", ancho // 2 - 180, alto // 2 + 150, 50, 50, GRIS, BLANCO
        )
        boton_dorsal_inferior = dibujar_boton(
            ">>", ancho // 2 - 50, alto // 2 + 150, 50, 50, GRIS, BLANCO
        )
        boton_color_superior = dibujar_boton(
            "<<", ancho // 2 + 25, alto // 2 + 150, 50, 50, GRIS, BLANCO
        )
        boton_color_inferior = dibujar_boton(
            ">>", ancho // 2 + 155, alto // 2 + 150, 50, 50, GRIS, BLANCO
        )

        # Dibujar la dorsal seleccionada
        dorsal_actual = backfaces[GLOBAL_BACKFACE_INDEX]
        back_image = pygame.image.load(f"deck/backfaces/{dorsal_actual}.png").convert()
        pantalla.blit(back_image, (ancho // 2 - 125, alto // 2 + 130))  # Ajusta posición y tamaño según sea necesario
        nombre_dorsal = fuente_texto.render(f"{dorsal_actual.upper()}", True, BLANCO)
        pantalla.blit(nombre_dorsal, (ancho // 2 - 130, alto // 2 + 225))

        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_dorsal_superior.collidepoint(event.pos):
                    GLOBAL_BACKFACE_INDEX = (GLOBAL_BACKFACE_INDEX - 1) % len(backfaces)
                    print(f"Dorsal seleccionada: {backfaces[GLOBAL_BACKFACE_INDEX]}")
                if boton_dorsal_inferior.collidepoint(event.pos):
                    GLOBAL_BACKFACE_INDEX = (GLOBAL_BACKFACE_INDEX + 1) % len(backfaces)
                    print(f"Dorsal seleccionada: {backfaces[GLOBAL_BACKFACE_INDEX]}")
                if boton_manual.collidepoint(event.pos):
                    return "manual"
                if boton_auto.collidepoint(event.pos):
                    return "auto"
        pygame.display.flip()


def endgame(perder, grupos_completos):
    casa = False
    if all(grupos_completos) == True:
        perder = False
    while casa == False:
        # Dibujar fondo gris
        rect_x = ANCHO // 2 - 200
        rect_y = ALTO // 2 - 150
        rect_ancho = 600
        rect_alto = 300
        pygame.draw.rect(pantalla, (169, 169, 169), (rect_x, rect_y, rect_ancho, rect_alto))  # Gris claro
        pygame.draw.rect(pantalla, (0, 0, 0), (rect_x, rect_y, rect_ancho, rect_alto), 3)  # Bordes negros

        # Volver a mostrar el mensaje sobre el rectángulo gris
        if perder:
            mostrar_mensaje("Has perdido el juego!", ANCHO // 2 - 150, ALTO // 2 - 100, ROJO)
        else:
            mostrar_mensaje("¡Felicidades, has ganado!", ANCHO // 2 - 150, ALTO // 2 - 100, VERDE)

        # Dibujar botones sobre el rectángulo gris
        boton_reiniciar = dibujar_boton(
            "Reiniciar", ancho // 2 - 150, alto // 2 - 100, 300, 50, VERDE, BLANCO
        )
        boton_salir = dibujar_boton(
            "Salir", ancho // 2 - 150, alto // 2, 300, 50, ROJO, BLANCO
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_reiniciar.collidepoint(event.pos):
                    print("Tocaste el boton de reinicio")
                    main()
                    dealer = croupier()
                    dealer.init_deck()
                    dealer.shuffle()
                    dealer.posicionate()
                    grupos_completos = [False] * 13
                    perder = False
                if boton_salir.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
        pygame.display.flip()


def juego_automatico(dealer):
    time.sleep(0.5)
    global grupos_completos
    grupos_completos = [False] * 13  # Inicializamos el estado de los grupos

    if not hasattr(juego_automatico, "mazo_actual"):
        juego_automatico.mazo_actual = (
            12  # Comenzamos desde el mazo inicial (posición 12)
        )
    casa = True
    while casa:  # Bucle para continuar moviendo mientras sea posible
        mazo_actual = juego_automatico.mazo_actual

        # Verificamos si hay cartas en el mazo actual y si el grupo no está completo
        if not grupos_completos[mazo_actual] and dealer.arrays_mini[mazo_actual]:
            # Tomamos la carta del mazo actual
            carta = dealer.arrays_mini[mazo_actual][0]
            destino = (
                    carta.value - 1
            )  # Calculamos el destino basado en el valor de la carta

            if not grupos_completos[destino]:
                # Animación del movimiento
                inicio_pos = posiciones[mazo_actual]
                fin_pos = posiciones[destino]

                for t in range(30):
                    pantalla.blit(background_image, (0, 0))
                    x = inicio_pos[0] + (fin_pos[0] - inicio_pos[0]) * t / 30
                    y = inicio_pos[1] + (fin_pos[1] - inicio_pos[1]) * t / 30

                    tablero(dealer)
                    pantalla.blit(carta.carta_imagen, (x, y))
                    pygame.display.flip()
                    clock.tick(60)

                # Realizamos el movimiento
                dealer.arrays_mini[mazo_actual].remove(carta)
                dealer.arrays_mini[destino].append(carta)

                # Volteamos la siguiente carta del mazo origen si existe
                if dealer.arrays_mini[mazo_actual]:
                    dealer.arrays_mini[destino][0].frente()

                # Comprobamos si el grupo de destino se ha completado
                dealer.comprobar_grupos(destino)

                # Actualizamos el mazo actual para que sea el mazo destino
                juego_automatico.mazo_actual = destino

        # Verificamos si el grupo 12 está completo o si todos los grupos lo están
        if grupos_completos[12]:
            perder = True
            endgame(perder, grupos_completos)


# Función principal del juego
def main():
    global grupos_completos
    global GLOBAL_BACKFACE_INDEX
    coords = [ancho // 2 - 180, alto // 2 + 150]
    mode = mostrar_menu_inicial()
    grupos_completos = [False] * 13
    dealer = croupier()
    dealer.init_deck()
    dealer.shuffle()
    dealer.posicionate()
    perder = False
    MousePressed = False
    MouseDown = False
    MouseReleased = False
    Target = None
    cought = False
    print(posiciones[0])
    print(len(posiciones))
    print(len(dealer.arrays_mini))
    for numero in dealer.arrays_mini[12]:
        print(numero.toString())
    repartiendo = True
    while True:
        pantalla.blit(background_image, (0, 0))
        pos = pygame.mouse.get_pos()
        while repartiendo:
            repartiendo = tablero_animacion(dealer, coords)
        tablero(dealer)
        if mode == "manual":
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    MousePressed = True
                    MouseDown = True
                if event.type == pygame.MOUSEBUTTONUP:
                    MouseReleased = True
                    MouseDown = False
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if MousePressed == True:
                for ite in range(13):
                    if (
                            pos[0] >= (posiciones[ite][0])
                            and pos[0] <= (posiciones[ite][0] + 96)
                            and pos[1] >= (posiciones[ite][1])
                            and pos[1] <= (posiciones[ite][1] + 96)
                            and dealer.arrays_mini[ite][0].volteada == False
                            and grupos_completos[ite] == False
                    ):
                        Target = dealer.arrays_mini[ite][0]
                        dealer.arrays_mini[ite].remove(Target)
                        temp_pos = ite
                        cought = True
                        dealer.comprobar_grupos(ite)
                        print(f"Carta seleccionada: {Target.value}")
                        break
                else:
                    cought = False
            if MouseDown and Target is not None and cought is True:
                pantalla.blit(Target.carta_imagen, (pos[0] - 20, pos[1] - 20))
            if MouseReleased and cought is True:
                for ite in range(13):
                    if (
                            pos[0] >= (posiciones[ite][0])
                            and pos[0] <= (posiciones[ite][0] + 96)
                            and pos[1] >= (posiciones[ite][1])
                            and pos[1] <= (posiciones[ite][1] + 96)
                            and Target.value - 1 == ite
                    ):
                        dealer.arrays_mini[ite].append(Target)
                        print(f"Carta movida a grupo {ite}")
                        dealer.arrays_mini[ite][0].frente()
                        temp_pos = None
                        Target = None
                        dealer.comprobar_grupos(ite)
                        if (grupos_completos[ite] == True) and (ite != 12):
                            i = ite
                            while dealer.arrays_mini[i][0].volteada is False:
                                if i >= 11:
                                    i = i - 12
                                dealer.arrays_mini[i + 1][0].frente()
                                i = i + 1
                        if grupos_completos[12] == True:
                            perder = True
                            endgame(perder, grupos_completos)
                else:
                    if temp_pos is not None:
                        dealer.arrays_mini[temp_pos].insert(0, Target)
                        grupos_completos[temp_pos] = False
                        Target = None
                        temp_pos = None
        else:
            while repartiendo:
                repartiendo = tablero_animacion(dealer, coords)
            tablero(dealer)
            juego_automatico(dealer)
            print("Juego automático")

        MousePressed = False
        MouseReleased = False
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
