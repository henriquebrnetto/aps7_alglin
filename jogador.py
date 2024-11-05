import requests, collections
import scipy.stats as stats
import numpy as np
import pandas as pd

class Jogador:
    def __init__(self, len_palavra):

        self.len_palavra = len_palavra
        self.palavra = np.empty(len_palavra, dtype=str) # Inicializa array da palavra

        self.vocabulario = self.init_vocab() # Matriz de palavras disponíveis
        self.probs  = self.compute_probs() # Inicializa probabilidades de cada letra

    def init_vocab(self):
        """
        Faz request de palavras disponíveis, e transforma em matriz.

        Returns:
            numpy.ndarray : Matriz com palavras x linhas
        """
        r = requests.get('https://www.ime.usp.br/~pf/dicios/br-sem-acentos.txt', allow_redirects=True)

        if r.status_code == 200:
            palavras = str(r.content.decode()).split('\n')
        else:
            return None
        
        return pd.DataFrame([list(palavra) for palavra in palavras if len(palavra) == self.len_palavra]).to_numpy()
        
    def compute_probs(self):
        """
        Conta ocorrências de cada letra disponível no vocabulário.

        Returns:
            dict : Dicionário {letra : contagem}
        """
        counter = collections.Counter(self.vocabulario.flatten())
        return {k : v for k, v in counter.items() if k not in set(self.palavra)}

    def filter_palavras(self, letra : str, idxs : list):
        """
        Filtra palavras de 'self.vocabulario' e computa contagens novamente a partir do novo vocabulário.
        Se não houver nenhuma repetição daquela letra (idxs == []) na palavra-alvo, irá remover todas as palavras que possuem tal letra.
        Caso contrário, irá preencher self.palavra e remover as palavras que não possuirem tal letra nas posições determinadas.

        Args:
            letra (str): Letra a ser filtrada do vocabulário
            idxs (list): Posições da letra
        """
        if not idxs: # idxs == []
            filtro = ~np.any(self.vocabulario == letra, axis=1) # Palavras que não possuem letra de input
        else:
            self.palavra[idxs] = letra # Preenche palavra
            filtro = np.all(self.vocabulario[:, idxs] == letra, axis=1) # Palavras com letra de input nas posições idxs
        
        self.vocabulario = self.vocabulario[filtro] # Altera vocabulário
        self.probs = self.compute_probs() # Calcula novas contagens

    def guess_letter(self):
        """
        Escolhe a letra com mais ocorrências no vocabulário.

        Returns:
            str: Letra com maior número de ocorrências
        """
        return max(self.probs, key=self.probs.get)