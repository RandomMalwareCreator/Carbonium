import random
import math
import win32api
import win32gui
import win32con
import time
import threading
from ctypes import windll

# Obtém o tamanho da tela (largura e altura)
SW = win32api.GetSystemMetrics(0)
SH = win32api.GetSystemMetrics(1)

circle_radius = 50  # O raio do círculo é metade de 100, que é o tamanho do círculo desenhado
x, y = 10, 10  # Posição inicial da bola
signX, signY = 1, 1  # Direção inicial do movimento
incrementor = 10  # Velocidade do movimento da bola

# Função para desenhar círculos na tela
def ci(x, y, w, h):
    # Obter o contexto do dispositivo da tela
    hdc = win32gui.GetDC(0)
    # Criar uma região elíptica (máscara)
    hrgn = windll.gdi32.CreateEllipticRgn(x, y, w + x, h + y)
    # Selecionar a região na área de clip do hdc
    windll.gdi32.SelectClipRgn(hdc, hrgn)
    # Realizar o BitBlt (operar a cópia de pixels com a operação NOTSRCCOPY)
    windll.gdi32.BitBlt(hdc, x, y, w, h, hdc, x, y, win32con.NOTSRCCOPY)
    # Deletar o objeto de região (para liberar a memória)
    windll.gdi32.DeleteObject(hrgn)
    # Liberar o contexto de dispositivo
    win32gui.ReleaseDC(0, hdc)

# Função que simula a animação do seno
def sines():
    # Obtém o "device context" (DC) da tela
    hwnd = win32gui.GetDesktopWindow()
    hdc = win32gui.GetDC(hwnd)

    angle = 0
    while True:
        # Loop para criar o efeito de movimento
        for i in range(0, SH):  # Limita o loop até a altura da tela
            # Calcula o valor da seno para o movimento
            a = int(math.sin(angle) * 20)
            
            # Realiza a cópia dos pixels (simulando o efeito)
            win32gui.BitBlt(hdc, 0, i, SW, 1, hdc, a, i, win32con.SRCCOPY)
            
            # Atualiza o ângulo para o próximo ponto da curva seno
            angle += math.pi / 40

        # Dá um pequeno tempo de espera para não sobrecarregar a CPU
        time.sleep(0.01)

    # Libera o DC depois que o loop terminar (isso na prática não será alcançado porque o loop é infinito)
    win32gui.ReleaseDC(hwnd, hdc)

# Função para iniciar o thread da animação do seno
def start_thread():
    thread = threading.Thread(target=sines)
    thread.daemon = True  # Garante que o thread termine quando o programa principal finalizar
    thread.start()

# Função para desenhar e mover a bola
def draw_moving_circle():
    global x, y, signX, signY

    # Obter as dimensões da tela
    w = SW - circle_radius * 2  # Largura da tela menos o dobro do raio do círculo
    h = SH - circle_radius * 2  # Altura da tela menos o dobro do raio do círculo

    while True:
        # Gerar coordenadas x e y aleatórias
        x += incrementor * signX
        y += incrementor * signY

        # Criar círculos com tamanhos progressivamente maiores
        for i in range(0, 1000, 100):
            ci(x - i // 2, y - i // 2, i, i)

        # Criando uma cor aleatória para o círculo
        brush = win32gui.CreateSolidBrush(win32api.RGB(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        
        # Obter o contexto de dispositivo para desenhar na tela
        hdc = win32gui.GetDC(0)

        # Desenhando o círculo na tela
        win32gui.SelectObject(hdc, brush)
        win32gui.Ellipse(hdc, x, y, x + circle_radius * 2, y + circle_radius * 2)

        # Detecção de bordas para mover o círculo
        if y >= h:  # Se o círculo atingiu a borda inferior
            signY = -1  # Inverte o movimento no eixo Y
        if x >= w:  # Se o círculo atingiu a borda direita
            signX = -1  # Inverte o movimento no eixo X
        if y <= 0:  # Se o círculo atingiu a borda superior
            signY = 1  # Inverte o movimento no eixo Y
        if x <= 0:  # Se o círculo atingiu a borda esquerda
            signX = 1  # Inverte o movimento no eixo X

        # Limpeza do contexto de dispositivo (para evitar borrões de desenho)
        win32gui.DeleteObject(brush)
        win32gui.ReleaseDC(0, hdc)

        # Dá um pequeno tempo de espera para não sobrecarregar a CPU
        time.sleep(0.01)

if __name__ == "__main__":
    # Iniciar a animação do seno em um thread separado
    start_thread()

    # Iniciar o movimento da bola
    draw_moving_circle()
