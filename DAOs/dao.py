import pickle
from abc import ABC, abstractmethod


class DAO(ABC):
    @abstractmethod
    def __init__(self, datasource=""):
        self.__datasource = datasource
        self.__cache = (
            {}
        )  
        try:
            self.__load()
        except FileNotFoundError:
            self.__dump()

    def __dump(self):
        pickle.dump(self.__cache, open(self.__datasource, "wb"))

    def __load(self):
        self.__cache = pickle.load(open(self.__datasource, "rb"))

    def add(self, key, obj):
        try:
            self.__load() # Recarrega os dados do disco antes de alterar
        except FileNotFoundError:
            pass
        self.__cache[key] = obj
        self.__dump()
        
    def update(self, key, obj):
        try:
            self.__load() # Recarrega antes de alterar
        except FileNotFoundError:
            pass
        try:
            if self.__cache[key] != None:
                self.__cache[key] = obj
                self.__dump()
        except KeyError:
            raise("Chave inválida")
    def get(self, key):
        try:
            self.__load() # Recarrega antes de ler
        except FileNotFoundError:
            pass
        try:
            return self.__cache[key]
        except KeyError:
            raise("Chave inválida")
    def remove(self, key):
        try:
            self.__load() # Recarrega antes de remover
        except FileNotFoundError:
            pass
        try:
            self.__cache.pop(key)
            self.__dump()
        except KeyError:
            raise("Chave inválida")
            
    def get_all(self):
        try:
            self.__load() # Recarrega antes de listar
        except FileNotFoundError:
            pass
        return self.__cache.values()
