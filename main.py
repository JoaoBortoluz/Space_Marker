import pygame

#biblioteca de serialização(obj->bytes) e de desserialização(bytes->obj)
import pickle 
from tkinter import simpledialog

pygame.init()
pygame.mixer.init()  # Inicializa o mixer do Pygame
tamanho = (1200,700)
display = pygame.display.set_mode(tamanho)
pygame.display.set_caption("Jogo SPACE MARKER")
icone = pygame.image.load("icone.png")
reduzirIcone = pygame.transform.scale(icone, (32,32)) #Reduz o ícone para 32px por 32px
pygame.display.set_icon(reduzirIcone)
branco = (225,225,225)
clock = pygame.time.Clock()
running = True
estrelas = {} #Dicionário
posicoes = []
posicaoX = []# posições separadas para ajudar a realização do ponto extra
posicaoY = []

#Imagens e musica
fundo = pygame.image.load("space.png")

#Bloco para exibir as instruções no canto superior esquerdo da tela
def instrucoes():
    fonte = pygame.font.SysFont(None, 24)
    linhas = ["Pressione F10 para salvar o progresso",
              "Pressione F11 para carregar o progresso",
              "Pressione F12 para deletar o progresso"]
    y = 0
    for linha in linhas:
        texto = fonte.render(linha, True, branco)
        display.blit(texto,(0,y))
        y += texto.get_height()

#Bloco para salvar as estrelas(=progresso) selecionadas através de um arquivo
def salvarProgresso():
    with open("DadosSalvos.pickle", "wb") as arquivo:
        pickle.dump((estrelas, posicoes), arquivo) #pickle.dump() = obj->bytes e grava ele em um arquivo
    calcularDistancias()

#Bloco para carregar as estrelas(=progresso) salvas e caso não tenha nenhum arquivo salvo(FileNotFoundError) é criado um arquivo 
def carregarProgresso():
    try:
        with open("DadosSalvos.pickle", "rb") as arquivo:
            #pickle.load() = bytes->obj e lê o arquivo
            estrelas_salvas, posicoes_salvas = pickle.load(arquivo)
            estrelas.clear()
            posicoes.clear()
            estrelas.update(estrelas_salvas)
            posicoes.extend(posicoes_salvas)
            

    except FileNotFoundError:
        salvarProgresso()
    calcularDistancias()

#Bloco para calcular a distância de cada estrela em pixels
def calcularDistancias():
    for i in range(len(posicoes) - 1):
        x1, y1 = posicoes[i]
        x2, y2 = posicoes[i + 1]
        distancia = abs((x2 - x1) + (y2 - y1))
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
            pergunta = simpledialog.askstring("Espaço","Nome da estrela:")
            #Verifica se a pergunta não é igual a none ou a um espaço em branco
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
        

            #Bloco que exclui as estrelas(=progresso) salvas
            elif event.key == pygame.K_F12:
                estrelas.clear() #Limpa o dicionário
                posicoes.clear()
                posicaoX.clear()
                posicaoY.clear()
                salvarProgresso() #salva 00 pickle em branco
                calcularDistancias()
        
    display.blit(fundo,(0,0))
    calcularDistancias()
    instrucoes()
    
    #Cria a mensagem e posiciona onde foi clicado        
    for pergunta, posicao in estrelas.items():
        mensagem_display = pygame.font.SysFont(None, 24).render(pergunta, True, branco)
        posicao_mensagem = (posicao[0]-10, posicao[1]+10) # ajusta a mensagem na tela
        display.blit(mensagem_display, posicao_mensagem)
        pygame.draw.circle(display, branco, posicao,4)
        
    #Adiciona uma linha que liga uma estrela na outra
    if len(posicoes) > 1:
        pygame.draw.lines(display, branco, False, posicoes, 1)

    # atualizção da tela
    pygame.display.flip() # mudei para flip porque estava travando muito
    clock.tick(60) 

pygame.quit()