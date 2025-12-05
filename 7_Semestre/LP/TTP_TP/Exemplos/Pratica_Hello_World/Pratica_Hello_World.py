aluno=""
def Hello_World(nome:str)->str:
    aluno=nome
    return f"Olá {nome}, Bem-vindo ao Python"
def pratica():

    def Hello_World(nome:str)->str:
        return f"Olá {nome}, Bem-vindo ao Python"

    def Hello_World2(nome):
        return f"Olá {nome}, Bem-vindo ao Python"

    def Hello_World3(nome:str):
        print(f"Olá {nome}, Bem-vindo ao Python")
    print("Função 1 pratica")
    print(Hello_World(input("Por favor digite o seu nome:------:>")))
    print("Função 2 pratica")
    print(Hello_World2(input("Por favor digite o seu nome:------:>")))
    print("Procedimento pratica")
    nome_pessoa=input("Por favor digite o seu nome:------:>")
    Hello_World3(nome_pessoa)

if __name__ == '__main__':
    print("Procedimento pratica")
    pratica()
    print("Fora do Procedimento pratica")
    print("Função")
    print(Hello_World(input("Por favor digite o seu nome:------:>")))
    print(f"Muito, Obrigado, {aluno}")