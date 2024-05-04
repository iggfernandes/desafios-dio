
menu = '''
    ########## BEM VINDO! ##########
            
            [s] Sacar
            [d] Depositar
            [e] Exibir Extrato
            [q] Sair

    ################################
            Escolha uma opção: '''

saldo = 0
limite = 500
extrato = ''
MAX_SAQUES = 3
qnt_saques = 0           

def sacar():
    global saldo, limite, extrato, qnt_saques
    
    valor = float(input('Digite o valor a ser sacado: R$ '))
    
    if valor > saldo or valor > limite:
        print(f'Você não tem saldo ou limite suficiente. Seu saldo disponível é R$ {saldo:.2f} e seu limite de saque é R$ {limite:.2f}')        
    elif valor < 0:
        print('Operação Inválida!')
    else:
        saldo -= valor
        print(f'Saque de R$ {valor:.2f} efetuado com sucesso!\nSeu saldo atual é R$ {saldo:.2f}.')
        qnt_saques += 1
        
        extrato += f'Saque de R$ {valor:.2f} efetuado\n'

def depositar():
    global saldo, extrato

    valor = float(input('Digite o valor a ser depositado: R$ '))
    if valor > 0:
        saldo += valor
        print(f'Você depositou R$ {valor:.2f}')
        print(f'Seu saldo atual é de R$ {saldo:.2f}\n')
        
        extrato += f'Deposito de R$ {valor:.2f} efetuado\n'
    else:
        print('Operação inválida!')

while True:

    opcao = input(menu)
    
    if opcao == 's':
        if qnt_saques >= MAX_SAQUES:
            print('Você atingiu o número máximo de saques hoje.')
        else:
            sacar()

    if opcao == 'd':
        depositar()

    if opcao == 'e':
        print('---------- EXTRATO ----------\n') 
        print('Não foram realizadas movimentações\n' if not extrato else extrato)
        print(f'Seu saldo atual é R$ {saldo:.2f}')
        print('------- Fim do Extrato -------')
   
    if opcao == 'q':
        break





