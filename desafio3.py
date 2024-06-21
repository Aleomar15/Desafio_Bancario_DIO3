from datetime import datetime
from abc import ABC, abstractmethod

class Transacao(ABC):
   @property
   @abstractmethod
   def valor(self):
       pass


   def registrar(self, conta):
       pass
        


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.conta = []
    
    def realizar_Transacao(self, conta, transacao):
        tra = Transacao
        tra.registrar(conta, transacao)

    def adcionar_conta(self, conta):
        self.conta.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data, endereco):
        super.__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data = data
        #self.data_de_nascimento = date.today()

class Conta():
    def __init__(self, numero, cliente) -> None:
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero,cliente)

    @property
    def saldo(self):
        return self.saldo
    
    @property
    def numero(self):
        return self.numero
    
    @property
    def agencia(self):
        return self.agencia
    
    @property
    def cliente(self):
        return self.cliente
    
    @property
    def historico(self):
        return self.historico
    
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n Saldo insuficiente!!")
        
        elif valor > 0:
            self._saldo -= valor
            print("\n Saque realizado com sucesso!!")
            return True
        
        else:
            print("\n O valor informado é invalido!!!")
            return False
        
        return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n deposito feito com sucesso")

        else:
            print("\nO valor informado é inválido.")
            return False

        return True
    
class ContaCorrente(Conta):
    def __init__(self, numero, agencia, cliente, limite= 500, limite_saques=3) -> None:
        super().__init__(numero, agencia, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque._name_])

        excedeu_limite = valor > self.limite

        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("\nO valor execedeu o limite!!")
        
        elif excedeu_saques:
            print("\n Número máximo de saques foi execedido")

        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f"""\
            Agencia:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """
    

class Historico:
    def __init__(self) -> None:
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
        })

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self.valor
    
    def registrar(self, conta):
        trasacao_sucedida = conta.sacar(self.valor)

        if trasacao_sucedida:
            conta.historico.adicionar_transacao(self)  

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self.valor
    
    def registrar(self, conta):
        trasacao_sucedida = conta.depositar(self.valor)

        if trasacao_sucedida:
            conta.historico.adicionar_transacao(self)  