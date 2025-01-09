import random
import pygame
import sys
import time

# Inicializa pygame
pygame.init()

# Define el tamaño de la pantalla
tamanio = ancho, alto = 1024, 768

# Inicializa la fuente
pygame.font.init()
pantalla = pygame.display.set_mode(tamanio)
clock = pygame.time.Clock()
pygame.display.set_caption("Solitario Reloj")
halved = pygame.image.load("deck/b2pr.gif")
halved_rect = halved.get_rect()
negro = 0, 0, 0
fondos = ["default", "default", "calaca", "romboide", "griego", "maya", "futuro", "chino", "magic", "uno", "poke", "yugi"]
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
GRIS = (100, 100, 100)
FONDO_COLOR = (50, 50, 50)
AZUL = (0, 0, 255)
ROJIZO = (228, 55, 61)
CELESTE = (10, 148, 237)
AMARILLO = (233, 146, 5)
VERDESITO = (71, 169, 120)
fuente = pygame.font.Font("deck/fonts/StepalangeShort-p7GZd.otf", 50)
fuente_botones = pygame.font.Font("deck/fonts/StepalangeShort-p7GZd.otf", 40)
fuente_titulo = pygame.font.Font("deck/fonts/StepalangeShort-p7GZd.otf", 200)
fuente_texto = pygame.font.Font("deck/fonts/StepalangeShort-p7GZd.otf", 20)
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
patron = random.randint(0, 2)

# Clase que representa una carta de la baraja
class card:
    # Color rosa claro en hexadecimal
    colors = [0XFFFFFF, 0XFFFFFF, 0x8E7F48, 0xC5E5EA, 0x7F7F7F, 0xAE9C88, 0x919192, 0xFFFFFE, 0xD56F44, 0xE2E2E1, 0xD5D5E8, 0xFAC78E]
    backfaces = ["Incoloro","Tradicional", "Calaca", "Geométrico", "Griego", "Maya", "Futuro", "Dragón Chino", "Magic the Gathering", "Uno", "Pokémon", "Yu-Gi-Oh"]
    TINT_COLOR = colors[0]  # Color de tinte para las cartas, agregar para las ultimas 4 cartas

    def __init__(self, type, value):
        self.type = type
        self.value = value
        self.volteada = True
        self.set_backface()
        self.set_color()

    def set_color(self):
        if GLOBAL_BACKFACE_INDEX < 0 or GLOBAL_BACKFACE_INDEX >= len(self.colors):
            # Usar color por defecto si el índice no es válido
            self.TINT_COLOR = 0x8E7F48
        else:
            # Usar el color seleccionado
            self.TINT_COLOR = self.colors[GLOBAL_BACKFACE_INDEX]
    def set_backface(self):
        global backface_name
        backface_name = self.backfaces[GLOBAL_BACKFACE_INDEX]
        if GLOBAL_BACKFACE_INDEX == 0:
            self.carta_imagen = self._load_and_tint_blank("deck/backfaces/Incoloro.png", patron)
        else:
            self.carta_imagen = pygame.image.load(f"deck/backfaces/{backface_name}.png").convert()

    def _load_and_tint_blank(self, image_path, patron):
        """
        Carga una imagen y la tinta con un patrón aleatorio y un color seleccionado dinámicamente.

        Args:
            image_path (str): Ruta de la imagen a cargar.

        Returns:
            pygame.Surface: Imagen tintada.
        """

        # Patrones predefinidos
        def stripe_pattern(x, y, color):
            """Patrón de rayas horizontales."""
            return y % 10 < 5

        def checkerboard_pattern(x, y, color):
            """Patrón de tablero de ajedrez."""
            return (x // 10 + y // 10) % 2 == 0

        def diagonal_stripes(x, y, color):
            """Patrón de rayas diagonales."""
            return (x + y) % 20 < 10

        # Lista de patrones
        patterns = [stripe_pattern, checkerboard_pattern, diagonal_stripes]

        # Seleccionamos un patrón aleatorio
        pattern_func = patterns[patron]  # Seleccionamos el patrón basado en el índice

        # Seleccionamos un color aleatorio
        rgb = cp.get_color()
        r = rgb.r
        g = rgb.g
        b = rgb.b

        # Carga la imagen y la convierte al formato correcto
        original = pygame.image.load(image_path).convert()
        tinted = original.copy()

        # Aplicamos el tinte según el patrón seleccionado
        for x in range(tinted.get_width()):
            for y in range(tinted.get_height()):
                color = tinted.get_at((x, y))
                if pattern_func(x, y, color):
                    tinted.set_at((x, y), (r, g, b))
        return tinted

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
        self.deck = []  # Dacia la baraja porsiacaso
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

    def comprobar_grupos(self):
        for ite, grupo in enumerate(self.arrays_mini):
            aux = 0
            if ite != 12:
                # Verificar si el grupo tiene exactamente 4 cartas y todas están volteadas
                if len(grupo) == 4:
                    for carta in grupo:
                        if carta.volteada:
                            break
                    else:
                        grupos_completos[ite] = True
            else:
                # Verificar las condiciones especiales para el grupo 12
                for carta in grupo:
                    if carta.volteada:
                        break
                    if carta.value == 13:
                        aux += 1
                if aux == 4:
                    grupos_completos[ite] = True

class ColorPicker:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)  # Superficie con canal alfa
        self.image.fill((0, 0, 0, 150))  # Fondo transparente opaco (negro con alfa 150)
        self.rad = h // 2
        self.pwidth = w - self.rad * 2

        # Generar el espectro de colores
        for i in range(self.pwidth):
            color = pygame.Color(0)
            hue = int(360 * i / self.pwidth)  # Cálculo correcto para el espectro
            color.hsla = (hue, 100, 50, 100)
            pygame.draw.rect(self.image, color, (i + self.rad, h // 3, 1, h - 2 * h // 3))

        self.p = 0

    def get_color(self):
        color = pygame.Color(0)
        hue = int(self.p * 360)  # Mantén la correspondencia con el rango 360°
        color.hsla = (hue, 100, 50, 100)
        return color

    def update(self):
        moude_buttons = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if moude_buttons[0] and self.rect.collidepoint(mouse_pos):
            self.p = (mouse_pos[0] - self.rect.left - self.rad) / self.pwidth
            self.p = max(0, min(self.p, 1))

    def draw(self, surf):
        surf.blit(self.image, self.rect)
        center = self.rect.left + self.rad + self.p * self.pwidth, self.rect.centery
        pygame.draw.circle(surf, self.get_color(), center, self.rect.height // 3)  # Tamaño de la bolita ajustado

class GestorSonidos:
    def __init__(self):
        pygame.mixer.pre_init(48000, -16, 1, 1024)  # Configuración previa
        pygame.mixer.init()
        self.sonidos = {
            "mover": pygame.mixer.Sound("sounds/ponerla.ogg"),
            "poner": pygame.mixer.Sound("sounds/moverla.ogg")
        }
        # Ajustar volumen de los sonidos
        self.sonidos["poner"].set_volume(0.8)
        self.sonidos["mover"].set_volume(0.8)

    def reproducir(self, nombre):
        if nombre in self.sonidos:
            self.sonidos[nombre].play(fade_ms=50)  # Añadir fade-in para suavizar
        else:
            print(f"Sonido '{nombre}' no encontrado.")


sound = GestorSonidos()
"""METODOS UI"""


def dibujar_cartas_centro(dealer, initial_coords, repartir=False):
    global centro_x, altura_y, cartas_centro, cartas_muestra, pantalla, background_image
    # Redibujar el fondo

    # Reducir el montón si se están repartiendo cartas
    if repartir and len(cartas_centro) > 0:
        cartas_centro.pop()  # Elimina la última carta del montón central

    # Dibujar todas las cartas restantes en el grupo central
    offset_centro = 0
    for _ in range(len(cartas_centro) - 3):
        sombra_rect = pygame.Surface((cartas_muestra[0].get_width(), cartas_muestra[0].get_height()), pygame.SRCALPHA)
        sombra_rect.fill((0, 0, 0, 100))  # Sombra con transparencia
        pantalla.blit(sombra_rect, (centro_x +1 + offset_centro, altura_y))
        pantalla.blit(cartas_muestra[0], (centro_x + offset_centro, altura_y))
        offset_centro -= 1.5  # Espaciado entre las cartas
        
def animacion_barajado(dealer, initial_coords):
    # Coordenadas para los grupos de cartas
    global centro_x, altura_y
    global cartas_centro, cartas_muestra
    centro_x = ancho // 2 - 40
    grupo_izq_x = centro_x - 200
    grupo_der_x = centro_x + 200
    altura_y = initial_coords[1]  # Mantener la misma altura para todos los grupos

    # Cargar algunas cartas para la animación
    cartas_muestra = []
    for i in range(4):
        if GLOBAL_BACKFACE_INDEX == 0:
            carta = dealer.heartsDeck[0]._load_and_tint_blank("deck/backfaces/Incoloro.png", patron).convert()
        else:
            carta = pygame.image.load(f"deck/backfaces/{backface_name}.png").convert()
        cartas_muestra.append(carta)

    # Animación de división en dos grupos
    for step in range(30):
        pantalla.blit(background_image, (0, 0))  # Redibuja el fondo

        # Calcular posiciones para cada carta (manteniendo la misma altura)
        pos_izq_1 = (
            initial_coords[0] + (grupo_izq_x - initial_coords[0]) * (step / 30),
            altura_y
        )
        pos_der_1 = (
            initial_coords[0] + (grupo_der_x - initial_coords[0]) * (step / 30),
            altura_y
        )

        # Dibujar sombras y cartas
        for pos in [pos_izq_1, pos_der_1]:
            sombra_rect = pygame.Surface((cartas_muestra[0].get_width(), cartas_muestra[0].get_height()), pygame.SRCALPHA)
            sombra_rect.fill((0, 0, 0, 100))
            pantalla.blit(sombra_rect, (pos[0] +1, pos[1]))
            pantalla.blit(cartas_muestra[0], pos)

        pygame.display.flip()
        time.sleep(0.01)

    # Lista para mantener un registro de las cartas en el grupo central
    cartas_centro = []

    # Animación de mezcla al centro
    for _ in range(8):  # 4 iteraciones de mezcla
        # Mover carta del grupo izquierdo al centro
        for step in range(30):
            pantalla.blit(background_image, (0, 0))  # Redibuja el fondo

            # Dibujar las cartas que ya están en el centro
            offset_centro = 0
            for carta_pos in cartas_centro:
                sombra_rect = pygame.Surface((cartas_muestra[0].get_width(), cartas_muestra[0].get_height()), pygame.SRCALPHA)
                sombra_rect.fill((0, 0, 0, 100))
                pantalla.blit(sombra_rect, (centro_x +1 + offset_centro, altura_y))
                pantalla.blit(cartas_muestra[0], (centro_x + offset_centro, altura_y))
                offset_centro -= 1.5

            # Mantener cartas estáticas en sus grupos
            for i in range(1):
                sombra_rect = pygame.Surface((cartas_muestra[0].get_width(), cartas_muestra[0].get_height()), pygame.SRCALPHA)
                sombra_rect.fill((0, 0, 0, 100))
                pantalla.blit(sombra_rect, (grupo_izq_x +1, altura_y + i * 20))
                pantalla.blit(cartas_muestra[0], (grupo_izq_x, altura_y + i * 20))
                pantalla.blit(sombra_rect, (grupo_der_x +1, altura_y + i * 20))
                pantalla.blit(cartas_muestra[0], (grupo_der_x, altura_y + i * 20))

            # Animar carta en movimiento
            pos_x = grupo_izq_x + (centro_x - grupo_izq_x) * (step / 30)

            sombra_rect = pygame.Surface((cartas_muestra[0].get_width(), cartas_muestra[0].get_height()), pygame.SRCALPHA)
            sombra_rect.fill((0, 0, 0, 100))
            pantalla.blit(sombra_rect, (pos_x +1, altura_y ))
            pantalla.blit(cartas_muestra[0], (pos_x, altura_y))

            pygame.display.flip()
            time.sleep(0.01)

        cartas_centro.append((centro_x, altura_y))

        # Mover carta del grupo derecho al centro
        for step in range(30):
            pantalla.blit(background_image, (0, 0))  # Redibuja el fondo

            # Dibujar las cartas que ya están en el centro
            offset_centro = 0
            for carta_pos in cartas_centro:
                sombra_rect = pygame.Surface((cartas_muestra[0].get_width(), cartas_muestra[0].get_height()), pygame.SRCALPHA)
                sombra_rect.fill((0, 0, 0, 100))
                pantalla.blit(sombra_rect, (centro_x +1 + offset_centro, altura_y))
                pantalla.blit(cartas_muestra[0], (centro_x + offset_centro, altura_y))
                offset_centro -= 1.5

            # Mantener cartas estáticas en sus grupos
            for i in range(1):
                sombra_rect = pygame.Surface((cartas_muestra[0].get_width(), cartas_muestra[0].get_height()), pygame.SRCALPHA)
                sombra_rect.fill((0, 0, 0, 100))
                pantalla.blit(sombra_rect, (grupo_izq_x + 1, altura_y + i * 20))
                pantalla.blit(cartas_muestra[0], (grupo_izq_x, altura_y + i * 20))
                pantalla.blit(sombra_rect, (grupo_der_x + 1, altura_y + i * 20))
                pantalla.blit(cartas_muestra[0], (grupo_der_x, altura_y + i * 20))

            # Animar carta en movimiento
            pos_x = grupo_der_x + (centro_x - grupo_der_x) * (step / 30)

            sombra_rect = pygame.Surface((cartas_muestra[0].get_width(), cartas_muestra[0].get_height()), pygame.SRCALPHA)
            sombra_rect.fill((0, 0, 0, 100))
            pantalla.blit(sombra_rect, (pos_x +1, altura_y))
            pantalla.blit(cartas_muestra[0], (pos_x, altura_y))

            pygame.display.flip()
            time.sleep(0.01)

        cartas_centro.append((centro_x, altura_y))

    dibujar_cartas_centro(dealer, initial_coords, repartir=True)
    for step in range(30):
        pantalla.blit(background_image, (0, 0))  # Redibuja el fondo
        dibujar_cartas_centro(dealer, initial_coords)
        # Calcular posiciones para cada carta en movimiento inverso
        pos_izq_1 = (
            grupo_izq_x + (initial_coords[0] - grupo_izq_x) * (step / 30),
            altura_y
        )
        pos_der_1 = (
            grupo_der_x + (initial_coords[0] - grupo_der_x) * (step / 30),
            altura_y
        )

        # Dibujar sombras y cartas
        for pos in [pos_izq_1, pos_der_1]:
            sombra_rect = pygame.Surface((cartas_muestra[0].get_width(), cartas_muestra[0].get_height()),
                                         pygame.SRCALPHA)
            sombra_rect.fill((0, 0, 0, 100))
            pantalla.blit(sombra_rect, (pos[0] +1, pos[1]))
            pantalla.blit(cartas_muestra[0], pos)

        pygame.display.flip()
        time.sleep(0.01)
    # Mostrar el mazo final por un momento sin que desaparezca

    for _ in range(20):
        pantalla.blit(background_image, (0, 0))  # Redibuja el fondo
        offset_centro = 0
        for _ in range(len(cartas_centro)):
            sombra_rect = pygame.Surface((cartas_muestra[0].get_width(), cartas_muestra[0].get_height()), pygame.SRCALPHA)
            sombra_rect.fill((0, 0, 0, 100))
            pantalla.blit(sombra_rect, (centro_x +1 + offset_centro, altura_y))
            pantalla.blit(cartas_muestra[0], (centro_x + offset_centro, altura_y))
            offset_centro -= 1.5
        pygame.display.flip()
        time.sleep(0.02)

    return False

def establecer_fondo():
    global background_image
    if GLOBAL_BACKFACE_INDEX <= 1:
        background_image = pygame.image.load("deck/background/default.jpg")
    else:
        background_image = pygame.image.load(f"deck/background/{fondos[GLOBAL_BACKFACE_INDEX]}.jpeg")
    background_image = pygame.transform.scale(background_image, (ancho, alto))

def dibujar_cartas(wid, hei, hour, dealer, coords):
    offset = 0  # Desplazamiento inicial para apilar las cartas
    aux = reversed(dealer.arrays_mini[hour])

    # Coordenadas iniciales
    start_x, start_y = centro_x, altura_y

    cartas_colocadas = []  # Registro de cartas ya colocadas con sus sombras

    for i, carta in enumerate(aux):
        # Calcula la posición final para cada carta
        end_x = wid - offset
        end_y = hei
        current_x = start_x
        current_y = start_y

        # Antes de animar cada carta, actualiza el montón central
        dibujar_cartas_centro(dealer, coords)

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

            # Redibuja las cartas ya colocadas con sus sombras
            for colocada, (x, y) in cartas_colocadas:
                sombra_rect = pygame.Surface((colocada.carta_imagen.get_width(), colocada.carta_imagen.get_height()), pygame.SRCALPHA)
                sombra_rect.fill((0, 0, 0, 100))  # Negro semitransparente
                pantalla.blit(sombra_rect, (x +1, y))
                pantalla.blit(colocada.carta_imagen, (x, y))

            # Dibuja la sombra de la carta en movimiento
            sombra_rect = pygame.Surface((carta.carta_imagen.get_width(), carta.carta_imagen.get_height()), pygame.SRCALPHA)
            sombra_rect.fill((0, 0, 0, 100))  # Negro semitransparente
            pantalla.blit(sombra_rect, (current_x - 2, current_y + 2))

            # Dibuja la carta en movimiento
            pantalla.blit(carta.carta_imagen, (current_x, current_y))

            # Actualiza la pantalla
            dibujar_cartas_centro(dealer, coords)  # Redibuja el montón central durante la animación
            pygame.display.flip()
            time.sleep(0.00001)

        # Agrega la carta a la lista de cartas colocadas
        cartas_colocadas.append((carta, (end_x, end_y)))

        # Dibuja la sombra de la carta final colocada
        sombra_rect = pygame.Surface((carta.carta_imagen.get_width(), carta.carta_imagen.get_height()), pygame.SRCALPHA)
        sombra_rect.fill((0, 0, 0, 100))  # Negro semitransparente
        pantalla.blit(sombra_rect, (end_x - 2, end_y + 2))  # Sombra desplazada ligeramente

        # Actualiza el desplazamiento para la siguiente carta
        offset -= 12  # Incrementa el desplazamiento horizontal para apilar las cartas



def dibujar_grupos(wid, hei, hour, dealer):
    # Dibuja las cartas del grupo actual (hour) en la posición especificada (wid, hei)
    offset = 0  # Desplazamiento inicial para apilar las cartas
    aux = reversed(dealer.arrays_mini[hour])

    for i, carta in enumerate(aux):
        # Dibuja la sombra de cada carta apilada
        sombra_rect = pygame.Surface((carta.carta_imagen.get_width(), carta.carta_imagen.get_height()), pygame.SRCALPHA)
        sombra_rect.fill((0, 0, 0, 100))  # Negro semitransparente
        pantalla.blit(sombra_rect, (wid - offset - 2, hei + 2))

        # Dibuja la carta
        pantalla.blit(carta.carta_imagen, (wid - offset, hei))
        offset -= 12  # Incrementa el desplazamiento horizontal para apilar las cartas


def mostrar_mensaje(texto, x, y, color=BLANCO):
    mensaje = fuente.render(texto, True, color)
    pantalla.blit(mensaje, (x, y))


def dibujar_boton(texto, x, y, ancho, alto, color, color_texto, accion=None, transparente=False):
    if transparente:
        # Crear una superficie transparente para el botón
        superficie = pygame.Surface((ancho, alto), pygame.SRCALPHA)
        superficie.fill((0, 0, 0, 150))  # Fondo negro con transparencia
        pantalla.blit(superficie, (x, y))  # Dibujar la superficie en la pantalla
    else:
        # Dibujar un rectángulo sólido si no es transparente
        pygame.draw.rect(pantalla, color, (x, y, ancho, alto))

    # Agregar el texto al botón
    mensaje = fuente.render(texto, True, color_texto)
    pantalla.blit(
        mensaje,
        (
            x + (ancho - mensaje.get_width()) // 2,
            y + (alto - mensaje.get_height()) // 2,
        ),
    )

    # Retornar el rectángulo del botón
    return pygame.Rect(x, y, ancho, alto)



"""METODOS JUEGO"""


# Función para dibujar el tablero
def tablero_animacion(dealer, coords):
    for i in range(13):
        dibujar_cartas(posiciones[i][0], posiciones[i][1], i, dealer, coords)
        dibujar_cartas_centro(dealer, coords, repartir=True)
        if i == 13:  # Último grupo
            tablero(dealer)  # Dibuja el tablero final
            return False
    pygame.display.flip()


def tablero(dealer):
    for i in range(13):
        dibujar_grupos(posiciones[i][0], posiciones[i][1], i, dealer)
    pygame.display.flip()

cp = ColorPicker(ancho // 2 + 25, alto // 2 + 150, 175, 50) #creo la instancia del color, (x, y, alto, ancho)

class InputBox:
    def __init__(self, x, y, w, h, texto_inicial='', color_inactivo=(200, 200, 200), color_activo=(0, 128, 255), fuente=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactivo = color_inactivo
        self.color_activo = color_activo
        self.color = color_inactivo
        self.texto = texto_inicial
        self.fuente = fuente or pygame.font.Font(None, 32)
        self.activo = False
        self.guardo = False  # Variable para verificar si el deseo fue guardado

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos) and not self.guardo:  # Solo si no está guardado
                self.activo = True
                self.color = self.color_activo
            else:
                self.activo = False
                self.color = self.color_inactivo

        if event.type == pygame.KEYDOWN:
            if self.activo and not self.guardo:  # Solo permite escribir si no está guardado
                if event.key == pygame.K_RETURN:
                    self.guardo = True  # El deseo se guarda
                    self.activo = False  # Bloquear el input
                    return self.texto  # Retorna el texto cuando se presiona Enter
                elif event.key == pygame.K_BACKSPACE:
                    self.texto = self.texto[:-1]  # Borra el último carácter
                else:
                    self.texto += event.unicode  # Agrega el carácter al texto

        return None

    def draw(self, pantalla):
        # Dibuja el rectángulo del input box
        pygame.draw.rect(pantalla, self.color, self.rect)
        # Dibuja el texto
        txt_surface = self.fuente.render(self.texto, True, (0, 0, 0))
        pantalla.blit(txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(pantalla, (0, 0, 0), self.rect, 2)  # Borde

        if self.guardo:  # Si el deseo está guardado, muestra un mensaje
            mensaje_guardado = self.fuente.render("¡Deseo guardado!", True, (0, 255, 0))  # Color verde para indicar éxito
            pantalla.blit(mensaje_guardado, (self.rect.x, self.rect.y + self.rect.height + 10))
 # Variable para almacenar el deseo del usuario
def set_deseo(self, deseo):
    global cumplira
    cumplira = deseo
    print(f"Deseo ingresado: {cumplira}")

def get_deseo():
    return cumplira
    
def mostrar_menu_inicial():
    backfaces = card.backfaces
    global GLOBAL_BACKFACE_INDEX
    GLOBAL_BACKFACE_INDEX = 0
    menu_img = pygame.image.load("deck/menu.png")  # Cambia por tu imagen
    menu_img = pygame.transform.scale(menu_img, (ancho, alto))
    input_box = InputBox(ancho // 2 - 200, alto // 2 + 230, 400, 40)
    while True:
        pantalla.blit(menu_img, (0, 0))

        titulo_blanco = fuente_titulo.render("Oráculo", True, BLANCO)
        titulo_rojo = fuente_titulo.render("Oráculo", True, ROJO)
        x_pos = ancho // 2 - titulo_blanco.get_width() // 2
        y_pos = alto // 6

        pantalla.blit(titulo_rojo, (x_pos - 5, y_pos - 5))  # Arriba-izquierda
        pantalla.blit(titulo_rojo, (x_pos + 5, y_pos - 5))  # Arriba-derecha
        pantalla.blit(titulo_rojo, (x_pos - 5, y_pos + 5))  # Abajo-izquierda
        pantalla.blit(titulo_rojo, (x_pos + 5, y_pos + 5)) # Abajo-derecha
        pantalla.blit(titulo_blanco, (x_pos, y_pos))


        boton_manual = dibujar_boton(
            "Jugar Manual", ancho // 2 - 200, alto // 2 - 50, 400, 60, AMARILLO, BLANCO, False
        )

        boton_auto = dibujar_boton(
            "Jugar Automático", ancho // 2 - 200, alto // 2 + 50, 400, 60, CELESTE, BLANCO, False
        )
        boton_dorsal_superior = dibujar_boton(
            "<<", ancho // 2 - 180, alto // 2 + 150, 50, 50, GRIS, BLANCO, transparente=True
        )
        boton_dorsal_inferior = dibujar_boton(
            ">>", ancho // 2 - 50, alto // 2 + 150, 50, 50, GRIS, BLANCO, transparente=True
        )

        cp.update() # dibuja el colorimetro
        cp.draw(pantalla) # dibuja el colorimetro

        # Dibujar la dorsal seleccionada
        dorsal_actual = backfaces[GLOBAL_BACKFACE_INDEX]
        back_image = pygame.image.load(f"deck/backfaces/{dorsal_actual}.png").convert()
        sombra_rect = pygame.Surface((back_image.get_width(), back_image.get_height()), pygame.SRCALPHA)
        sombra_rect.fill((0, 0, 0, 100))  # Negro semitransparente
        pantalla.blit(sombra_rect, (ancho // 2 - 127, alto // 2 + 132))
        pantalla.blit(back_image, (ancho // 2 - 125, alto // 2 + 130))  # Ajusta posición y tamaño según sea necesario
        nombre_dorsal = fuente_texto.render(f"{dorsal_actual.upper()}", True, BLANCO)
        nombre_dorsal2 = fuente_texto.render(f"{dorsal_actual.upper()}", True, ROJO)
        pantalla.blit(nombre_dorsal2, (ancho // 2 - 130 +1, alto // 2 + 225-1))
        pantalla.blit(nombre_dorsal2, (ancho // 2 - 130 -1, alto // 2 + 225+1))
        pantalla.blit(nombre_dorsal2, (ancho // 2 - 130 +1, alto // 2 + 225-1))
        pantalla.blit(nombre_dorsal2, (ancho // 2 - 130 -1, alto // 2 + 225+1))
        pantalla.blit(nombre_dorsal, (ancho // 2 - 130, alto // 2 + 225))

        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #AQUI SE LEEE EL TEXTOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
            ############################################################################################################
            ############################################################################################################
            ############################################################################################################
            ############################################################################################################
            ############################################################################################################
            ############################################################################################################
            texto = input_box.handle_event(event)
            if texto:  # Si se presionó Enter y hay texto, se guarda
                set_deseo(texto)
            else:
                set_deseo("")

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
        #Pone el textfiel, capaazz hacerlo aca abajo tiene algo que ver
        input_box.draw(pantalla)
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
        #aqui se lee el texto del deseo, pero no llega porque no se define bien ahisito
        ###################
        ####################
        ###################
        #################
        ###################
        #####################
        ##################
        ######################
        if perder:
            mostrar_mensaje("Has perdido el juego!", ANCHO // 2 - 150, ALTO // 2 - 100, ROJO)
            if get_deseo == "":
                mostrar_mensaje("Lamento que tu deseo, no se cumplira", ANCHO // 2 - 300, ALTO // 2 - 200, ROJO)
            else:
                mostrar_mensaje("Lamento que tu deseo, "+get_deseo+", no se cumplira", ANCHO // 2 - 300, ALTO // 2 - 200, ROJO)
        else:
            mostrar_mensaje("¡Felicidades, has ganado!", ANCHO // 2 - 150, ALTO // 2 - 100, VERDE)
            if get_deseo == "":
                mostrar_mensaje("Eres afortunado, tu deseo se va a cumplir", ANCHO // 2 - 150, ALTO // 2 - 200, VERDE)
            else:
                mostrar_mensaje("Eres afortunado, tu deseo "+get_deseo+" se cumplira", ANCHO // 2 - 150, ALTO // 2 - 200, VERDE)
        # Dibujar botones sobre el rectángulo gris
        boton_reiniciar = dibujar_boton(
            "Reiniciar", ancho // 2 - 150, alto // 2 - 100, 300, 50, VERDESITO, BLANCO
        )
        boton_salir = dibujar_boton(
            "Salir", ancho // 2 - 150, alto // 2, 300, 50, ROJIZO, BLANCO
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
                dealer.comprobar_grupos()

                # Actualizamos el mazo actual para que sea el mazo destino
                juego_automatico.mazo_actual = destino

        # Verificamos si el grupo 12 está completo o si todos los grupos lo están
        if grupos_completos[12]:
            perder = True
            endgame(perder, grupos_completos)


# Función principal del juego
def main():
    global cartas_centro, temp_pos
    global grupos_completos
    global GLOBAL_BACKFACE_INDEX
    global background_image
    coords = [ancho // 2, alto // 2 + 250]
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
    barajando = True
    establecer_fondo()
    while True:
        pantalla.blit(background_image, (0, 0))
        pos = pygame.mouse.get_pos()
        while barajando:
            barajando = animacion_barajado(dealer, coords)
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
                    dealer.comprobar_grupos()
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
                        dealer.comprobar_grupos()
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
                        dealer.comprobar_grupos()
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
            while barajando:
                barajando = animacion_barajado(dealer, coords)
            while repartiendo:
                repartiendo = tablero_animacion(dealer, coords)
            juego_automatico(dealer)
            print("Juego automático")

        MousePressed = False
        MouseReleased = False
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
