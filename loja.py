class Cpf:
    # Valida e representa o CPF do cliente.
    def __init__(self, valor):
        if len(valor) != 11:
            raise ValueError("cpf invalido")
        self.__valor = valor


class Email:
    # Valida e representa o email do cliente.
    def __init__(self, valor):
        if not valor:
            raise ValueError("email vazio")
        if "@" not in valor:
            raise ValueError("email invalido")
        self.__valor = valor


class Cep:
    # Valida e representa o CEP do endereço.
    def __init__(self, valor):
        if len(valor) != 8:
            raise ValueError("cep invalido")
        self.__valor = valor


class Dinheiro:
    # Representa valores monetários em centavos inteiros.
    def __init__(self, centavos):
        self.__centavos = centavos

    def somar(self, outro_valor):
        centavos_outro_valor = outro_valor.__centavos
        return Dinheiro(self.__centavos + centavos_outro_valor)

    def subtrair(self, outro_valor):
        centavos_outro_valor = outro_valor.__centavos
        return Dinheiro(self.__centavos - centavos_outro_valor)

    def multiplicar(self, quantidade):
        return Dinheiro(self.__centavos * quantidade)

    def calcular_percentual(self, percentual):
        return Dinheiro(self.__centavos * percentual // 100)

    def __str__(self):
        centavos = self.__centavos
        return "R$ %d.%02d" % (centavos // 100, centavos % 100)


class Status:
    # Guarda o código e executa transições do estado de um pedido.
    def __init__(self, codigo):
        self.__codigo = codigo

    def esta_aberto(self):
        return self.__codigo == "A"

    def esta_pago(self):
        return self.__codigo == "P"

    def marcar_pago(self):
        self.__codigo = "P"

    def marcar_cancelado(self):
        self.__codigo = "C"

    def imprimir_descricao(self):
        descricoes = {
            "A": "aberto",
            "P": "pago",
            "C": "cancelado",
        }
        print("  status:", descricoes[self.__codigo])


class Pessoa:
    # Reúne os dados pessoais e documentos de uma pessoa.
    def __init__(self, nome, cpf, email):
        self.__nome = nome
        self.__cpf = cpf
        self.__email = email

    def imprimir_nome(self):
        print(self.__nome, end=" ")


class Endereco:
    # Reúne os dados de localização de um cliente.
    def __init__(self, rua, cidade, cep):
        self.__rua = rua
        self.__cidade = cidade
        self.__cep = cep

    def imprimir_cidade(self):
        print(self.__cidade)


class TipoNormal:
    # Define a política de desconto para clientes normais.
    def desconto_sobre(self, valor):
        return Dinheiro(0)


class TipoVip:
    # Define a política de desconto para clientes VIP.
    def desconto_sobre(self, valor):
        return valor.calcular_percentual(10)


class TipoFuncionario:
    # Define a política de desconto para funcionários.
    def desconto_sobre(self, valor):
        return valor.calcular_percentual(20)


class Cliente:
    # Conecta os dados pessoais, endereço e tipo de desconto do cliente.
    def __init__(self, pessoa, endereco, tipo):
        self.__pessoa = pessoa
        self.__endereco = endereco
        self.__tipo = tipo

    def desconto_sobre(self, valor):
        tipo = self.__tipo
        return tipo.desconto_sobre(valor)

    def imprimir_identificacao(self, numero_pedido):
        print("Pedido", numero_pedido, "-", end=" ")
        pessoa = self.__pessoa
        pessoa.imprimir_nome()
        print("-", end=" ")
        endereco = self.__endereco
        endereco.imprimir_cidade()


class Produto:
    # Representa um produto pelo nome e preço unitário.
    def __init__(self, nome, preco):
        self.__nome = nome
        self.__preco = preco

    def calcular_preco_para(self, quantidade):
        preco = self.__preco
        return preco.multiplicar(quantidade)

    def imprimir_item(self, quantidade, valor_total):
        print("   " + str(quantidade) + " x " + self.__nome + " = " + str(valor_total))


class ItemDoPedido:
    # Associa um produto a uma quantidade comprada.
    def __init__(self, produto, quantidade):
        self.__produto = produto
        self.__quantidade = quantidade

    def calcular_total(self):
        produto = self.__produto
        quantidade = self.__quantidade
        return produto.calcular_preco_para(quantidade)

    def imprimir(self):
        produto = self.__produto
        quantidade = self.__quantidade
        valor_total = self.calcular_total()
        produto.imprimir_item(quantidade, valor_total)


class ItensDoPedido:
    # Mantém e opera sobre os itens de um pedido.
    def __init__(self):
        self.__itens = []

    def adicionar(self, item):
        itens = self.__itens
        itens.append(item)

    def esta_vazia(self):
        return len(self.__itens) == 0

    def calcular_total(self):
        total = Dinheiro(0)
        for item in self.__itens:
            valor_item = item.calcular_total()
            total = total.somar(valor_item)
        return total

    def imprimir(self):
        for item in self.__itens:
            item.imprimir()


class Pedido:
    # Aplica as regras de negócio e apresenta os dados de um pedido.
    def __init__(self, cliente):
        self.__cliente = cliente
        self.__itens = ItensDoPedido()
        self.__status = Status("A")

    def adicionar_item(self, produto, quantidade):
        item = ItemDoPedido(produto, quantidade)
        itens = self.__itens
        itens.adicionar(item)

    def pagar(self):
        status = self.__status
        if not status.esta_aberto():
            return False
        itens = self.__itens
        if itens.esta_vazia():
            return False
        status.marcar_pago()
        return True

    def cancelar(self):
        status = self.__status
        if not status.esta_aberto():
            return False
        status.marcar_cancelado()
        return True

    def calcular_total(self):
        itens = self.__itens
        return itens.calcular_total()

    def calcular_desconto(self):
        cliente = self.__cliente
        total = self.calcular_total()
        return cliente.desconto_sobre(total)

    def calcular_valor_a_pagar(self):
        total = self.calcular_total()
        desconto = self.calcular_desconto()
        return total.subtrair(desconto)

    def esta_pago(self):
        status = self.__status
        return status.esta_pago()

    def esta_aberto(self):
        status = self.__status
        return status.esta_aberto()

    def valor_arrecadado(self):
        if not self.esta_pago():
            return Dinheiro(0)
        return self.calcular_valor_a_pagar()

    def contar_se_aberto(self):
        if not self.esta_aberto():
            return 0
        return 1

    def imprimir(self, numero_pedido):
        cliente = self.__cliente
        cliente.imprimir_identificacao(numero_pedido)
        status = self.__status
        status.imprimir_descricao()
        itens = self.__itens
        itens.imprimir()
        if not itens.esta_vazia():
            self.imprimir_totais()

    def imprimir_totais(self):
        total = self.calcular_total()
        desconto = self.calcular_desconto()
        valor_a_pagar = self.calcular_valor_a_pagar()
        print(
            "  total: %s | desconto: %s | a pagar: %s"
            % (str(total), str(desconto), str(valor_a_pagar))
        )


class Pedidos:
    # Registra pedidos pelo número e produz os totais da loja.
    def __init__(self):
        self.__pedidos = {}

    def criar_pedido(self, numero_pedido, cliente):
        pedido = Pedido(cliente)
        self.__pedidos[numero_pedido] = pedido
        return pedido

    def imprimir_relatorio(self):
        pedidos = self.__pedidos
        for numero_pedido, pedido in pedidos.items():
            pedido.imprimir(numero_pedido)

    def calcular_total_arrecadado(self):
        total = Dinheiro(0)
        pedidos = self.__pedidos
        for pedido in pedidos.values():
            valor_arrecadado = pedido.valor_arrecadado()
            total = total.somar(valor_arrecadado)
        return total

    def contar_pedidos_abertos(self):
        quantidade = 0
        pedidos = self.__pedidos
        for pedido in pedidos.values():
            quantidade = quantidade + pedido.contar_se_aberto()
        return quantidade


def criar_cliente(nome, cpf_texto, email_texto, rua, cidade, cep_texto, tipo):
    email = Email(email_texto)
    cpf = Cpf(cpf_texto)
    cep = Cep(cep_texto)
    pessoa = Pessoa(nome, cpf, email)
    endereco = Endereco(rua, cidade, cep)
    return Cliente(pessoa, endereco, tipo)


pedidos_da_loja = Pedidos()

cliente_ana = criar_cliente(
    "Ana Souza",
    "12345678901",
    "ana@mail.com",
    "Rua das Flores, 10",
    "Sorocaba",
    "18010000",
    TipoVip(),
)
pedido_da_ana = pedidos_da_loja.criar_pedido(1, cliente_ana)
pedido_da_ana.adicionar_item(Produto("Caderno", Dinheiro(1550)), 2)
pedido_da_ana.adicionar_item(Produto("Caneta", Dinheiro(250)), 5)

try:
    cliente_bruno = criar_cliente(
        "Bruno Lima",
        "123",
        "bruno@mail.com",
        "Av. Central, 200",
        "Votorantim",
        "18110000",
        TipoNormal(),
    )
    pedidos_da_loja.criar_pedido(2, cliente_bruno)
except ValueError as erro:
    print("pedido", 2, "recusado:", erro)

pedido_da_ana_no_segundo_numero = pedidos_da_loja.criar_pedido(3, cliente_ana)
pedido_da_ana_no_segundo_numero.adicionar_item(Produto("Livro", Dinheiro(8950)), 1)

try:
    cliente_carla = criar_cliente(
        "Carla Dias",
        "98765432100",
        "carla.mail.com",
        "Rua do Sol, 55",
        "Sorocaba",
        "18020000",
        TipoFuncionario(),
    )
    pedidos_da_loja.criar_pedido(4, cliente_carla)
except ValueError as erro:
    print("pedido", 4, "recusado:", erro)

cliente_diego = criar_cliente(
    "Diego Rocha",
    "11122233344",
    "diego@mail.com",
    "Rua Nova, 7",
    "Itu",
    "13300000",
    TipoNormal(),
)
pedido_do_diego = pedidos_da_loja.criar_pedido(5, cliente_diego)

cliente_eva = criar_cliente(
    "Eva Nunes",
    "55566677788",
    "eva@mail.com",
    "Alameda Azul, 1",
    "Itu",
    "13300001",
    TipoFuncionario(),
)
pedido_da_eva = pedidos_da_loja.criar_pedido(6, cliente_eva)
produto_fone = Produto("Fone", Dinheiro(6000))
pedido_da_eva.adicionar_item(produto_fone, 1)

try:
    cliente_fabio = criar_cliente(
        "Fabio Costa",
        "99988877766",
        "fabio@mail.com",
        "Rua Velha, 3",
        "Itu",
        "123",
        TipoNormal(),
    )
    pedidos_da_loja.criar_pedido(7, cliente_fabio)
except ValueError as erro:
    print("pedido", 7, "recusado:", erro)

cliente_gil = criar_cliente(
    "Gil Alves",
    "44455566677",
    "gil@mail.com",
    "Rua do Meio, 9",
    "Sorocaba",
    "18030000",
    TipoNormal(),
)
pedido_do_gil = pedidos_da_loja.criar_pedido(8, cliente_gil)
pedido_do_gil.adicionar_item(produto_fone, 2)

print("pagar 1:", pedido_da_ana.pagar())
print("pagar 3:", pedido_da_ana_no_segundo_numero.pagar())
print("pagar 5:", pedido_do_diego.pagar())
print("pagar 6:", pedido_da_eva.pagar())
print("cancelar 5:", pedido_do_diego.cancelar())
print("cancelar 1:", pedido_da_ana.cancelar())

pedidos_da_loja.imprimir_relatorio()
print("arrecadado:", pedidos_da_loja.calcular_total_arrecadado())
print("abertos:", pedidos_da_loja.contar_pedidos_abertos())
