import pygame
from tkinter import simpledialog

pygame.init()
tamanho = (1200,700)
display = pygame.display.set_mode(tamanho)
pygame.display.set_caption("Jogo SPACE MARKER")
branco = (225,225,225)
preto = (0,0,0)
pergunta = ""
perguntas = []
posicoes = []
posicao = (0,0)
clock = pygame.time.Clock()
running = True
#imagens e objetos
fundo = pygame.image.load("space.png")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            posicao = pygame.mouse.get_pos()
            pergunta = simpledialog.askstring("Espaço","Nome da estrela:")
            #verifica se a pergunta é igual a none ou a um espaço em branco
            if pergunta is not None and pergunta.strip() != "":
                pergunta = pergunta + str(posicao)
            else:
                pergunta = "estrela desconhecida" + str(posicao)
            perguntas.append((pergunta, posicao))

        display.blit(fundo,(0,0))
        #cria a mensagem e posiciona onde foi clicado        
        for pergunta,posicao in perguntas:
            mensagem_display = pygame.font.SysFont(None, 24).render(pergunta, True, branco)
            display.blit(mensagem_display, (posicao)) 
    
    #atualização e clock da tela
    pygame.display.update()
    clock.tick(60)

pygame.quit()