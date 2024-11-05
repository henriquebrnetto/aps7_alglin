from jogador import Jogador
from jogoForca import JogoDeForca
import numpy as np



forca = JogoDeForca() # Inicializa o jogo da forca
tam = forca.novo_jogo() # Cria nova partida, escolhe a palavra e salva o tamanho da palavra
jogador = Jogador(tam) # Inicializa um jogador apenas com as palavras daquele tamanho

init = False
palavras_certas = 0
while forca.vidas > 0: # Enquanto o jogador não errar
    
    if init: # Caso o jogador tenha acertado a palavra, gera um novo jogador e nova partida
        tam = forca.novo_jogo()
        jogador = Jogador(tam)
        init = False

    letra = jogador.guess_letter() # Jogador escolhe letra
    idxs = forca.tentar_letra(letra) # Indexes onde aquela letra está presente na palavra

    jogador.filter_palavras(letra, idxs) # Reduz o vocabulário de acordo com a informação de indexes obtida

    if ~np.any(jogador.palavra == ''): # Se o array da palavra do jogador estiver preenchida
        if forca.tentar_palavra(''.join(jogador.palavra)): # Se o jogador acertar a palavra
            palavras_certas += 1
            init = True
            print(f'Você já acertou {palavras_certas} palavras, e possui {forca.vidas} vidas.')

print()
print('Acabou o jogo!')
print(f'Você acertou {palavras_certas} palavras, parabéns!')