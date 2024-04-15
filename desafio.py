import os
from datetime import datetime

menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[c] Criar Usuário
[q] Sair

=> """


VALOR_LIMITE_SAQUE = 500
LIMITE_SAQUES = 3



def criar_usuario(agencia, login):
    nome = agencia + "-" + login
    
    if os.path.exists(f"./usuarios/{nome}"):
        print("Usuário já cadastrado no sistema!")
        return
    else:
        with open(f"./usuarios/{nome}", 'w') as arquivo:
            arquivo.write("data_operacao,operacao,saldo,limite_saque")
        print(f"Usuário {nome} criado!")
        
    

def contar_linhas(path):
    contador = 0
    with open(path, "r") as arquivo:
        for linha in arquivo:
            contador += 1
    return contador


def depositar(agencia, login):
    valor_deposito = float(input("Valor a ser depositado: "))
    saldo = 0
    caminho_arquivo = f"./usuarios/{agencia}-{login}"
    
    if contar_linhas(caminho_arquivo) == 1:
        with open(caminho_arquivo,"a") as arquivo:
            saldo += valor_deposito
            arquivo.write(f"\n{datetime.now().date()},+{valor_deposito},{saldo},{LIMITE_SAQUES}")
            print(f"Depositado: R${valor_deposito}, Saldo atual R${saldo}")
    else:
        with open(caminho_arquivo, "r") as arquivo:
            linhas = arquivo.readlines()
            ultimo_saldo = float(linhas[-1].split(",")[2])
            ultimo_limite_saque = linhas[-1].split(",")[-1]
        
        novo_saldo = ultimo_saldo + valor_deposito
        with open(caminho_arquivo, "a") as arquivo:
            arquivo.write(f"\n{datetime.now().date()},+{valor_deposito},{novo_saldo},{ultimo_limite_saque}")
            print(f"Depositado R${valor_deposito}, Saldo atual: R${novo_saldo}")  
        
def sacar(agencia, login):
    valor_saque = float(input("Saque desejado: "))
    caminho_arquivo = f"./usuarios/{agencia}-{login}"
    
    if valor_saque <= VALOR_LIMITE_SAQUE:
        with open(caminho_arquivo,"r") as arquivo:
            linhas = arquivo.readlines()
            ultimo_limite_saque = int(linhas[-1].split(",")[-1])
            ultimo_saldo = float(linhas[-1].split(",")[2])
        
        novo_limite_saque = ultimo_limite_saque - 1
        if valor_saque <= ultimo_saldo:
            novo_saldo = ultimo_saldo - valor_saque
        else:
            print(f"Saldo indisponível para saque. O seu saldo é: R${ultimo_saldo}")
            return
        
        if not ultimo_limite_saque == 0:
            with open(caminho_arquivo, "a") as arquivo:
                arquivo.write(f"\n{datetime.now().date()},-{valor_saque},{novo_saldo},{novo_limite_saque}")
                print(f"Saque de R${valor_saque}, Saldo atual: R${novo_saldo}")
        else:
            print("Limite de saques diários atingidos")
            return
    else:
        print("Valor de saque acima do limite permitido!")
        return   

def extrato(agencia, login):
    caminho_arquivo = f"./usuarios/{agencia}-{login}"
    with open(caminho_arquivo,"r") as arquivo:
       arquivo.readline()
       print("============EXTRATO============")
       for linha in arquivo:
           elementos = linha.strip().split(",")
           data_operacao = elementos[0]
           if float(elementos[1]) < 0:
            operacao = "Saque:R${:.2f}".format(float(elementos[1]))
           else:
               operacao = "Depósito:R${:.2f}".format(float(elementos[1]))
           saldo = "R${:.2f}".format(float(elementos[2]))
           limite_de_saque = f"{elementos[3]}"
           print(f"Data de Operação: {data_operacao}, {operacao}, Saldo: {saldo}, Limite de Saques: {limite_de_saque}")
       print("===============================")
while True:
    opcao = input(menu)
    
    if opcao == "d":
        agencia = input("Digite o número da agência:")
        login = input("Digite o nome do usuário:")
        depositar(agencia,login)
        
    elif opcao == "s":
        agencia = input("Digite o número da agência:")
        login = input("Digite o nome do usuário:")
        sacar(agencia,login)
        
    elif opcao == "e":
        agencia = input("Digite o número da agência:")
        login = input("Digite o nome do usuário:")
        extrato(agencia,login)
        
    elif opcao == "c":
        agencia = input("Digite o número da agência:")
        login = input("Digite o nome do usuário:") 
        criar_usuario(agencia,login)
        
    elif opcao == "q":
        break
    
    else:
        print("Opção inválida, por favor selecione novamente a operação desejada.")    
        


    
    
    