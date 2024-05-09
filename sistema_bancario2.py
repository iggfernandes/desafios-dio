
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
            [5] Listar Dados Clientes 
            [6] Encerrar Conta
            
            [q] Sair

    #######################################        
            Escolha uma opção: '''          

def sacar(saldo, valor, extrato, limite, numero_saques, limite_saques):

    excedeu_limite = valor > limite
    excedeu_saldo = valor > saldo
    excedeu_saques = numero_saques >= limite_saques
    
    if excedeu_limite:
        print(f'&&& Você não tem limite suficiente. Seu limite é R$ {limite:.2f}.')
    elif excedeu_saldo:
        print(f'&&& Você não tem saldo suficiente. Seu saldo disponível é R$ {saldo:.2f}.')        
    elif excedeu_saques:
        print(f'&&& Você atingiu o limite de saques. Seu limite é {limite_saques} saques por dia.')
    elif  valor > 0:
        saldo -= valor
        numero_saques += 1
        extrato += f'Saque de R$ {valor:.2f} efetuado\n'
        print(f'--- Saque de R$ {valor:.2f} efetuado com sucesso! ---\n--- Seu saldo atual é R$ {saldo:.2f}.')
    else:
        print('&&& Valor inválido, seu espertinho.')

    return saldo, extrato

def depositar(saldo, valor, extrato):

    if valor > 0:
        saldo += valor
        extrato += f'Deposito de R$ {valor:.2f} efetuado\n'
        print(f'--- Você depositou R$ {valor:.2f}')
        print(f'--- Seu saldo atual é de R$ {saldo:.2f}\n')
    else:
        print('&&& Operação inválida!')

    return saldo, extrato

def exibir_extrato(saldo, extrato):
            print('---------- EXTRATO ----------\n') 
            print('Não foram realizadas movimentações\n' if not extrato else extrato)
            print(f'Seu saldo atual é R$ {saldo:.2f}')
            print('------- Fim do Extrato -------')

def cadastrar_cliente(clientes):
    cpf = input('Digite o CPF do cliente (somente números): ')
    if cpf in clientes:
        print('&&& Este cliente já está cadastrado!')
        return
    else: None

    nome = input('Digite o nome do cliente: ').upper()
    data_nascimento = input('Digite a data de nascimento do cliente (dd/mm/aaaa): ')
    endereco = input('Digite o endereço do cliente (logradouro, nro - bairro - cidade/sigla estado): ').upper()

    clientes[cpf] = {'nome': nome,
                     'data_nascimento': data_nascimento,
                     'endereco': endereco}
    print('--- Cliente cadastrado com sucesso!')

def nova_conta(agencia, numero_conta, clientes, contas):
    cpf = input('Digite o CPF do cliente (somente números): ')
    if cpf in clientes:
        contas[cpf] = {'nome': clientes[cpf]['nome'],
                       'agencia': agencia,
                       'numero_conta': numero_conta,}
        print(f'--- Conta número {contas[cpf]['numero_conta']} para cliente {contas[cpf]['nome']} criada com sucesso!')
    else: print('&&& Cliente não cadastrado.')

def procurar_conta(contas):
    cpf = input('Digite o CPF para procurar (somente número): ')
    if cpf in contas:
        texto = f'''
        Titular: \t{contas[cpf]['nome']}
        Agência: \t{contas[cpf]['agencia']}
        Número da Conta (C/C): \t{contas[cpf]['numero_conta']}'''
        print(texto)
        
    else: print('&&& Não encontrado.')

def listar_contas(contas):
    for conta in contas:
        print(f'Titular: \t{contas[conta]['nome']}')
        print(f'Agência: \t{contas[conta]['agencia']}')
        print(f'Número da Conta (C/C): \t{contas[conta]['numero_conta']}')
        print('=' * 40)
        print(' ')
    if not contas: print('&&& Não há contas cadastradas.')

def listar_clientes(clientes):
    for cliente in clientes:
        print(f'CPF: \t{cliente}')
        print(f'Nome: \t{clientes[cliente]['nome']}')
        print(f'Data Nascimento: \t{clientes[cliente]['data_nascimento']}')
        print(f'Endereço: \t{clientes[cliente]['endereco']}')
        print('=' * 40)
        print(' ')
    if not clientes: print('&&& Não há clientes cadastrados.')

def encerrar_conta(contas):
    cpf = input('Digite o CPF do cliente que deseja encerrar a conta (somente número): ')
    if cpf in contas:
         contas.pop(cpf)
         print('--- Conta encerrada com sucesso!')
    else: print('&&& Conta ou Cliente não cadastrados')

def main():
    
    AGENCIA = '777-1'
    LIMITE_SAQUES = 3
    
    clientes = {}
    contas = {}
    saldo = 0
    limite = 500
    extrato = ''
    numero_saques = 0
    
    while True:

        opcao = input(menu)
        
        if opcao == '1':
            
            valor = float(input('Digite o valor a ser sacado: R$ '))
            
            saldo, extrato = sacar(saldo=saldo, 
                  valor=valor,
                  extrato=extrato,
                  limite=limite,
                  numero_saques=numero_saques,
                  limite_saques=LIMITE_SAQUES)
            
            if sacar: numero_saques += 1

        if opcao == '2':
            
            valor = float(input('Digite o valor a ser depositado: R$ '))
            
            saldo, extrato = depositar(saldo, valor, extrato)

        if opcao == '3':
            exibir_extrato(saldo, extrato=extrato)
    
        if opcao == '4': # AVANÇA PARA O MENU DE CADASTROS
            while True: 
                opcao2 = input(menu2)
                
                if opcao2 == '1':
                    cadastrar_cliente(clientes)

                if opcao2 == '2':
                    número_conta = len(contas) + 1
                    nova_conta(AGENCIA, número_conta, clientes, contas)

                if opcao2 == '3':
                    procurar_conta(contas)
                
                if opcao2 == '4':
                    listar_contas(contas)

                if opcao2 == '5':
                    listar_clientes(clientes)

                if opcao2 == '6':
                    encerrar_conta(contas)

                if opcao2 == 'q':
                    break
        
        if opcao == 'q':
            break

main()

