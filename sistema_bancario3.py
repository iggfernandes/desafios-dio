from datetime import datetime

class Cliente():
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, dn, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.dn = dn


class Conta():
    def __init__(self, cliente, numero):
        self.cliente = cliente
        self.numero = numero
        self.saldo = 0
        self.agencia = '0322-1'
        self.historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(cliente, numero)

    def sacar(self, valor):
        saldo = self.saldo
        saldo_insuficiente = valor > saldo

        if saldo_insuficiente:
            print('&&& Falhou! Você não tem saldo suficiente.')
        elif valor > 0:
            self.saldo -= valor
            print(f'--- Sucesso! Saque de R${valor} realizado!')
            return True
        else:
            print('&&& Falhou! Valor inválido.')
        return False

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            print(f'--- Sucesso! R${valor} depositado.')
            
        else:
            print('&&& Falhou! Valor inválido.')
            return False
        
        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("\n&&& Falhou! O valor do saque excede o limite.")

        elif excedeu_saques:
            print("\n&&& Falhou! Número máximo de saques atingido.")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime('%d/%m/%Y, %H:%M:%S'),
            }
        )


class Saque():
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito():
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def encontrar_conta(cliente):
    if not cliente.contas:
        print("\n&&& Cliente não possui conta.")
        return

    # FIXME: não permite cliente escolher a conta
    return cliente.contas[0]

def procurar_conta(clientes):
    cpf = input('Qual o CPF do cliente?: ')
    cliente = filtrar_cliente(cpf, clientes)
    if encontrar_conta(cliente):
        print("=" * 100)
        print(cliente.contas)
    else:
        print('Conta não cadastrada.')
        
def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n&&& Cliente não cadastrado.")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = encontrar_conta(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n&&& Cliente não cadastrado.")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = encontrar_conta(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

def novo_cliente(clientes):
    cpf = input('Digite o CPF do cliente (somente números): ')
    cliente = filtrar_cliente(cpf, clientes)
    if cliente:
        print('&&& Este cliente já está cadastrado!')

    else:    
        nome = input('Digite o nome do cliente: ').upper()
        dn = input('Digite a data de nascimento do cliente (dd/mm/aaaa): ')
        endereco = input('Digite o endereço do cliente (logradouro, nro - bairro - cidade/sigla estado): ').upper()

        cliente = PessoaFisica(cpf = cpf, nome = nome, dn = dn, endereco = endereco)
        clientes.append(cliente)
        
        print('--- Cliente cadastrado com sucesso!')

def nova_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n&&& Cliente não encontrado, necessário cadastrar novo cliente.")
        return

    else:
        conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
        contas.append(conta)
        cliente.contas.append(conta)

        print("\n--- Conta criada com sucesso!")

def mostrar_contas(contas):
    for conta in contas:
        print("=" * 50)
        print(str(conta))

def mostrar_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n&&& Cliente não cadastrado.")
        return

    conta = encontrar_conta(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")

menu = '''
    ########## BEM VINDO! ##########
            
            [1] Sacar
            [2] Depositar
            [3] Exibir Extrato
            
            [4] Menu de Cadastros
            
            [q] Sair

    ################################
            Escolha uma opção: '''
menu2 = '''
    ############## CADASTROS ##############

            [1] Cadastrar Cliente
            [2] Abrir Nova Conta
            [3] Procurar Conta
            [4] Listar Todas as Contas 
            ###[5] Listar Dados Clientes
            ###[6] Encerrar Conta
            
            [q] Sair

    #######################################        
            Escolha uma opção: '''          

def start():
    clientes = []
    contas = []

    while True:
        opcao = input(menu)

        if opcao == '1':
            sacar(clientes)
        
        elif opcao == '2':
            depositar(clientes)
        
        elif opcao == '3':
            mostrar_extrato(clientes)

        elif opcao == '4':
            while True:
                opcao2 = input(menu2)

                if opcao2 == '1':
                    novo_cliente(clientes)
                elif opcao2 == '2':
                    numero_conta = len(contas) + 100
                    nova_conta(numero_conta, clientes, contas)
                
                elif opcao2 == '3':
                    procurar_conta(clientes)

                elif opcao2 == '4':
                    mostrar_contas(clientes, contas)

                elif opcao2 == '5':
                    pass
                
                
                elif opcao2 == 'q':
                    break
        
        elif opcao == 'q':
            break
        else:
            print('&& inválido.')
        

start()









