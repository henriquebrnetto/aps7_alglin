from jogador import Jogador
from jogoForca import JogoDeForca
import numpy as np



forca = JogoDeForca()
tam = forca.novo_jogo()
jogador = Jogador(tam)

init = False
palavras_certas = 0
while forca.vidas > 0:
    
    if init:
        tam = forca.novo_jogo()
        jogador = Jogador(tam)
        init = False

    letra = jogador.guess_letter()
    idxs = forca.tentar_letra(letra)

    jogador.filter_palavras(letra, idxs)

    if ~np.any(jogador.palavra == ''):
        if forca.tentar_palavra(''.join(jogador.palavra)):
            palavras_certas += 1
            init = True
            print(f'Você já acertou {palavras_certas} palavras, e possui {forca.vidas} vidas.')
        else:
            pass

print()
print('Acabou o jogo!')
print(f'Você acertou {palavras_certas} palavras, parabéns!')