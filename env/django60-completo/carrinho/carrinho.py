from decimal import Decimal

from produto.models import Produto
from projeto import settings


class Carrinho(object):

    def __init__(self, request):
        self.session = request.session
        self.carrinho = self.session.get(settings.CARRINHO_SESSION_ID)

        if not self.carrinho:
            self.carrinho = self.session[settings.CARRINHO_SESSION_ID] = {}

    def atualiza(self, id, quantidade):

        #   {'1': {'id': '1', 'preco': '7.70', 'quantidade': 10, 'preco_total': '77.0'},
        #    '2': {'id': '2', 'preco': '3.30', 'quantidade': 3, 'preco_total': '9.90'}}

        produto = Produto.objects.get(id=id, disponivel=True)

        if id not in self.carrinho:
            self.carrinho[id] = {'id': id, 'preco': str(produto.preco), 'quantidade': quantidade,
                                 'preco_total': str(produto.preco * quantidade)}
        else:
            self.carrinho[id]['quantidade'] = quantidade
            self.carrinho[id]['preco_total'] = str(self.carrinho[id]['quantidade'] * Decimal(self.carrinho[id]['preco']))

        self.salvar()

    def salvar(self):
        self.session.modified = True

    def remover(self, id):
        if id in self.carrinho:
            del self.carrinho[id]
            self.salvar()

    def get_preco_total(self, id):
        return self.carrinho[id]['preco_total']

    def get_quantidade_total(self, id):
        id = str(id)
        if id in self.carrinho:
            return self.carrinho[id]['quantidade']
        else:
            return 0

    def get_preco_carrinho(self):
        return sum(Decimal(item['preco_total']) for item in self.carrinho.values())

    def get_quantidade_carrinho(self):
        return sum(item['quantidade'] for item in self.carrinho.values())

    def get_produtos(self):

        #   {'1': {'id': '1', 'preco': '7.70', 'quantidade': 10, 'preco_total': '77.0'},
        #    '2': {'id': '2', 'preco': '3.30', 'quantidade': 3, 'preco_total': '9.90'}}

        lista = []
        for item in self.carrinho.values():
            produto = Produto.objects.get(id=item['id'])
            lista.append({'produto': produto,
                          'id': item['id'],
                          'preco': Decimal(item['preco']),
                          'quantidade': item['quantidade'],
                          'preco_total': Decimal(item['preco_total'])})
        return lista

        # [{'produto': obj_produto1, 'id': '1', 'preco': Decimal('7.70'), 'quantidade': 10, 'preco_total': Decimal('77.0')},
        #  {'produto': obj_produto2, 'id': '2', 'preco': Decimal('3.30'), 'quantidade': 3, 'preco_total': Decimal('9.90')}]
