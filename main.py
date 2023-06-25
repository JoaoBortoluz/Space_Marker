import pygame
import pickle
from tkinter import simpledialog

pygame.init()
pygame.mixer.init()
tamanho = (1200, 700)#tupla
display = pygame.display.set_mode(tamanho)
pygame.display.set_caption("Jogo SPACE MARKER")
icone = pygame.image.load("icone.png")
reduzirIcone = pygame.transform.scale(icone, (32, 32))
pygame.display.set_icon(reduzirIcone)
branco = (225, 225, 225)#tupla
clock = pygame.time.Clock()
running = True
estrelas = {}
posicoes = []
posicaoX = []
posicaoY = []

fundo = pygame.image.load("space.png")
musica = pygame.mixer.music.load("musica_espaço.mp3")
pygame.mixer.music.play(-1)

def instrucoes():
    fonte = pygame.font.SysFont(None, 24)
    linhas = [
        "Pressione F10 para salvar o progresso",
        "Pressione F11 para carregar o progresso",
        "Pressione F12 para deletar o progresso"
    ]
    y = 0
    for linha in linhas:
        texto = fonte.render(linha, True, branco)
        display.blit(texto, (0, y))
        y += texto.get_height()

def salvarProgresso():
    with open("DadosSalvos.pickle", "wb") as arquivo:
        pickle.dump((estrelas, posicoes), arquivo)
    calcularDistancias()

def carregarProgresso():
    try:
        with open("DadosSalvos.pickle", "rb") as arquivo:
            estrelas_salvas, posicoes_salvas = pickle.load(arquivo)
            estrelas.clear()
            posicoes.clear()
            estrelas.update(estrelas_salvas)
            posicoes.extend(posicoes_salvas)

    except FileNotFoundError:
        salvarProgresso()
    calcularDistancias()

def calcularDistancias():
    for i in range(len(posicoes) - 1):
        x1, y1 = posicoes[i]
        x2, y2 = posicoes[i + 1]
        distancia = abs(int(((x2 - x1)**2 + (y2 - y1)**2)**0.5))
        mediaX = (x1 + x2) // 2
        mediaY = (y1 + y2) // 2
        exibir = pygame.font.SysFont(None, 24).render(str(distancia), True, branco)
        display.blit(exibir, (mediaX, mediaY))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            salvarProgresso()
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            posicao = pygame.mouse.get_pos()
            pergunta = simpledialog.askstring("Espaço", "Nome da estrela:")
            if pergunta is not None and pergunta.strip() != "":
                pergunta = pergunta + str(posicao)
            else:
                pergunta = "Estrela Desconhecida" + str(posicao)
            estrelas[pergunta] = posicao
            posicoes.append(posicao)
            posicaoX.append(posicao[0])
            posicaoY.append(posicao[1])

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F10 or event.key == pygame.K_ESCAPE:
                salvarProgresso()

            elif event.key == pygame.K_F11:
                carregarProgresso()

            elif event.key == pygame.K_F12:
                estrelas.clear()
                posicoes.clear()
                posicaoX.clear()
                posicaoY.clear()
                salvarProgresso()
                calcularDistancias()

    display.blit(fundo, (0, 0))
    calcularDistancias()
    instrucoes()

    for pergunta, posicao in estrelas.items():
        mensagem_display = pygame.font.SysFont(None, 24).render(pergunta, True, branco)
        posicao_mensagem = (posicao[0] - 10, posicao[1] + 10)

        # Verifica se a posição da mensagem ultrapassa os limites da tela
        if posicao_mensagem[0] + mensagem_display.get_width() > tamanho[0]:
            posicao_mensagem = (tamanho[0] - mensagem_display.get_width(), posicao_mensagem[1])
        if posicao_mensagem[1] + mensagem_display.get_height() > tamanho[1]:
            posicao_mensagem = (posicao_mensagem[0], tamanho[1] - mensagem_display.get_height())

        display.blit(mensagem_display, posicao_mensagem)
        pygame.draw.circle(display, branco, posicao, 4)

    if len(posicoes) > 1:
        pygame.draw.lines(display, branco, False, posicoes, 1)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()