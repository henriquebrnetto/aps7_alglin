import requests, collections
import scipy.stats as stats
import numpy as np
import pandas as pd

class Jogador:
    def __init__(self, len_palavra):

        self.len_palavra = len_palavra
        self.palavra = np.empty(len_palavra, dtype=str)

        self.vocabulario = self.init_vocab()
        self.probs  = self.compute_probs()

    def init_vocab(self):
        r = requests.get('https://www.ime.usp.br/~pf/dicios/br-sem-acentos.txt', allow_redirects=True)

        if r.status_code == 200:
            palavras = str(r.content.decode()).split('\n')
        else:
            return None
        
        return pd.DataFrame([list(palavra) for palavra in palavras if len(palavra) == self.len_palavra]).to_numpy()
        
    def compute_probs(self):
        counter = collections.Counter(self.vocabulario.flatten())
        return {k : v for k, v in counter.items() if k not in set(self.palavra)}

    def filter_palavras(self, letra, idxs):

        if not idxs:
            filtro = ~np.any(self.vocabulario == letra, axis=1)
        else:
            self.palavra[idxs] = letra
            filtro = np.all(self.vocabulario[:, idxs] == letra, axis=1)
        
        self.vocabulario = self.vocabulario[filtro]
        self.probs = self.compute_probs()

    def guess_letter(self):
        return max(self.probs, key=self.probs.get)