import pygame
#biblioteca de serialização(obj->bytes) e de desserialização(bytes->obj)
import pickle 
from tkinter import simpledialog

pygame.init()
tamanho = (1200,700)
display = pygame.display.set_mode(tamanho)
pygame.display.set_caption("Jogo SPACE MARKER")
icone = pygame.image.load("icone.png")
reduzirIcone = pygame.transform.scale(icone,(32,32)) #Reduz o ícone para 32px por 32px
pygame.display.set_icon(reduzirIcone)
branco = (225,225,225)
preto = (0,0,0)
pergunta = ""
estrelas = {} #Dicionário
posicoes = []
posicao = (0,0)
clock = pygame.time.Clock()
running = True

#Imagens e objetos
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
        pickle.dump(estrelas, arquivo) #pickle.dump() = obj->bytes e grava ele em um arquivo

#Bloco para carregar as estrelas(=progresso) salvas e caso não tenha nenhum arquivo salvo(FileNotFoundError) é criado um arquivo 
def carrgarProgresso():
    try:
        with open("DadosSalvos.pickle", "rb") as arquivo:
            estrelas.update(pickle.load(arquivo)) #pickle.load() = bytes->obj e lê o arquivo
    except FileNotFoundError:
        salvarProgresso()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            salvarProgresso()
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            posicao = pygame.mouse.get_pos()
            pergunta = simpledialog.askstring("Espaço","Nome da estrela:")
            #Verifica se a pergunta é igual a none ou a um espaço em branco
            if pergunta is not None and pergunta.strip() != "":
                pergunta = pergunta + str(posicao)
            else:
                pergunta = "Estrela Desconhecida" + str(posicao)
            estrelas[pergunta] = posicao 
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F10 or event.key == pygame.K_ESCAPE:
               salvarProgresso() 

            elif event.key == pygame.K_F11:
                carrgarProgresso()

            #Bloco que exclui as estrelas(=progresso) salvas
            elif event.key == pygame.K_F12:
                estrelas.clear() #Limpa o dicionário
                with open("DadosSalvos.pickle", "wb") as arquivo:
                    pickle.dump(estrelas, arquivo) 

        display.blit(fundo,(0,0))
        instrucoes()

        #Cria a mensagem e posiciona onde foi clicado        
        for pergunta, posicao in estrelas.items():
            mensagem_display = pygame.font.SysFont(None, 24).render(pergunta, True, branco)
            display.blit(mensagem_display, posicao)
        
    #Atualização e clock da tela
    pygame.display.update()
    clock.tick(60)

pygame.quit()