import requests
import re

class BuscaEndereco:

    def __init__(self, cep):
        # Valida se o cep e válido
        resposta = self.validar_cep
        if resposta(cep):
            self.cep = cep
            self.busca_cep()
        else:
            raise ValueError("Cep inválido")

        self.logradouro = None
        self.complemento = None
        self.bairro = None
        self.localidade = None
        self.uf = None

    def __str__(self):
        #Retorna o objeto formatado
        return (
            f"CEP: {self.cep}\n"
            f"Logradouro: {self.logradouro}\n"
            f"Complemento: {self.complemento}\n"
            f"Bairro: {self.bairro}\n"
            f"Localidade: {self.localidade}\n"
            f"UF: {self.uf}\n"
        )

    def validar_cep(self, cep):
        # Valida se o tamanho do cep e válido
        tamanho_cep = len(cep)
        if (tamanho_cep < 8 or tamanho_cep > 9):
            print("passei por aqui")
            return False
        else:
            regex = "[0-9]{5}-?[0-9]{3}"
            resposta = re.match(regex, cep)
            if resposta:
                return True
            else:
                return False

    def busca_cep(self):
        url = f"http://viacep.com.br/ws/{self.cep}/json/"
        try:
            # fazendo a requisição do tipo get
            response = requests.get(url)

            # verifica se a requisição foi bem sucedida! (codigo - 200)
            if response.status_code == 200:
                # Preenchendo os campos
                self.preencher_campos(response.json())
        except requests.RequestException as e:
            return f"Erro ao acessar a API: {e}"

    def preencher_campos(self, response):
        # atribuindo as variáveis valor da resposta da requisição
        self.logradouro = response.get("logradouro")
        self.complemento = response.get("complemento")
        self.bairro = response.get("bairro")
        self.localidade = response.get("localidade")
        self.uf = response.get("uf")

    def mascara_cep(self):
        # aplicando a mascara no cep
        padrao = re.compile("-")
        resultado = padrao.search(self.cep)
        if resultado is None:
            primeira_parte = self.cep[:5]
            segunda_parte = self.cep[5:]
            return f"{primeira_parte}-{segunda_parte}"
        else:
            return self.cep



