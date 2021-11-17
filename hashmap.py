class Underflow(Exception):
    def __init__(self):
        self.message = 'Valor minimo de elementos excedido'

    def __str__(self):
        return f'{self.message}: Underflow!'


class ChaveJaExiste(Exception):
    def __init__(self):
        self.message = 'Chave já existe'

    def __str__(self):
        return f'{self.message}: propriedade de chave única violada!'


class ChaveInexistente(Exception):
    def __init__(self):
        self.message = 'Chave não existe'

    def __str__(self):
        return f'{self.message}'


class Overflow(Exception):
    def __init__(self):
        self.message = 'Estrutura não suporta mais elementos'

    def __str__(self):
        return f'{self.message}: Overflow!'


class NoListaDuplamenteEncadeada:

    def __init__(self, key, value, hashcode, add_prev=None, add_post=None):
        self.key = key
        self.value = value
        self.hashcode = hashcode
        self.add_prev = add_prev
        self.add_post = add_post


class ListaDuplamenteEncadeada:

    def __init__(self):
        self.head = NoListaDuplamenteEncadeada(None, None, None)

    def buscar(self, key):

        last_address = self.head.add_post
        while last_address is not None:
            if last_address.key == key:
                return last_address
            last_address = last_address.add_post

        return None

    def inserir(self, key, value, hashcode):

        if self.buscar(key) is None:
            no = NoListaDuplamenteEncadeada(key, value, hashcode)
            last_address = self.head.add_post
            while last_address is not None:
                if last_address.add_post is None:
                    last_address.add_post = no
                    no.add_prev = last_address
                    return
                last_address = last_address.add_post
            self.head.add_post = no
            no.add_prev = self.head
        else:
            raise ChaveJaExiste

    def remover(self, key):
        target_address = self.head.add_post

        while target_address is not None:
            if target_address.key == key:
                if target_address.add_post is None:
                    target_address.add_prev.add_post = None
                    target_address.add_prev, target_address.add_post = None, None
                    return target_address
                else:
                    target_address.add_prev.add_post = target_address.add_post
                    target_address.add_post.add_prev = target_address.add_prev
                    target_address.add_prev, target_address.add_post = None, None
                    return target_address
            target_address = target_address.add_post

        if self.head.add_post is not None:
            raise ChaveInexistente
        else:
            raise Underflow

    def __str__(self):
        if self.head.add_post is None:
            return '[]'

        res = ''
        address = self.head.add_post
        while address is not None:
            res = res + f'| Key:{address.key}, Value:{address.value}, Hashcode:{address.hashcode} |'
            address = address.add_post
        return res


class NoListaEstatica:

    def __init__(self, key, value, hashcode):
        self.key = key
        self.value = value
        self.hashcode = hashcode


class ListaEstatica:

    def __init__(self, tam_max):
        self.tam_max = tam_max
        self.last_added = -1
        self.array = []

        for i in range(0, self.tam_max, 1):
            self.array.append(None)

    def buscar(self, key):

        for i in range(0, self.last_added+1, 1):
            if self.array[i].key == key:
                return self.array[i]

        if self.last_added == 0:
            if self.array[0].key == key:
                return self.array[0]

        return None

    def buscar_indice(self, key):
        for i in range(0, self.last_added+1, 1):
            if self.array[i].key == key:
                return i

    def inserir(self, key, value, hashcode):

        if self.buscar(key) is None:
            if self.last_added < self.tam_max - 1:
                self.last_added = self.last_added + 1
                self.array[self.last_added] = NoListaEstatica(key, value, hashcode)
                return
            else:
                raise Overflow
        else:
            raise ChaveJaExiste

    def remover(self, key):
        indice = self.buscar_indice(key)
        removido = self.buscar(key)
        if indice is not None and removido is not None:
            for i in range(indice, self.last_added+1, 1):
                if i == self.last_added:
                    self.array[i] = None
                else:
                    self.array[i] = self.array[i + 1]
            if self.last_added == 0:
                self.array[0] = None
            self.last_added = self.last_added - 1
            return removido
        else:
            raise ChaveInexistente

    def __str__(self):

        if self.last_added == 0:
            return f'[{self.array[0].value}]'
        elif self.last_added == -1:
            return 'Lista vazia'

        res = '['
        for i in range(0, self.tam_max, 1):
            if i != self.tam_max-1:
                if self.array[i] is not None:
                    res = res + f'{self.array[i].value}, '
                else:
                    res = res + f'{None}, '
            else:
                if self.array[i] is not None:
                    res = res + f'{self.array[i].value}]'
                else:
                    res = res + f'{None}]'

        return res


class HashMap:

    def __init__(self, tam_inicial):
        self.table = []
        self.tam_inicial = tam_inicial
        self.to_closed = False

        for i in range(0, tam_inicial, 1):
            self.table.append(ListaDuplamenteEncadeada())

    def hash_function(self, key):
        return key%self.tam_inicial

    def buscar(self, key):
        hashcode = self.hash_function(key)
        if self.table[hashcode].head.add_post is not None and self.table[hashcode].head.add_post.key == key:
            return self.table[hashcode].head.add_post
        else:
            i = self.hash_function(hashcode + 1)
            while i != hashcode:
                if self.table[hashcode].head.add_post is not None and self.table[hashcode].head.add_post.key == key:
                    return self.table[hashcode].head.add_post
                i = self.hash_function(i + 1)

            return None

    def inserir(self, key, value):
        hashcode = self.hash_function(key)

        if not self.to_closed:
            if self.table[hashcode].head.add_post is None:
                self.table[hashcode].inserir(key, value, hashcode)
                return
            else:
                if self.table[hashcode].head.add_post.key == key:
                    raise ChaveJaExiste

                i = self.hash_function(hashcode + 1)
                while i != hashcode:
                    if self.table[i].head.add_post is None:
                        self.table[i].inserir(key, value, hashcode)
                        return
                    else:
                        if self.table[i].head.add_post.key == key:
                            raise ChaveJaExiste

                    i = self.hash_function(i + 1)

                self.open_to_closed()
                self.to_closed = True
        else:
            self.table[hashcode].inserir(key, value, hashcode)

    def remover(self, key):
        hashcode = self.hash_function(key)
        if not self.to_closed:
            if self.table[hashcode].head.add_post is not None and self.table[hashcode].head.add_post.key == key:
                elemento = self.table[hashcode].head.add_post
                self.table[hashcode].head.add_post = None
                return elemento
            else:
                i = self.hash_function(hashcode + 1)
                while i != hashcode:
                    if self.table[i].head.add_post is not None and self.table[i].head.add_post.key == key:
                        elemento = self.table[i].head.add_post
                        self.table[i].head.add_post = None
                        return elemento
                    i = self.hash_function(i + 1)

                return None
        else:
            return self.table[hashcode].remover(key)


    def open_to_closed(self):
        i = 0
        for j in range(0, self.tam_inicial, 1):
            if self.table[j].head.add_post is not None and self.table[j].head.add_post.hashcode == i:
                temp = self.table[j].head.add_post
                self.table[j].remover(temp.key)
                self.table[i].inserir(temp.key, temp.value, temp.hashcode)

        i = self.hash_function(i + 1)
        while i != 0:
            for j in range(0, self.tam_inicial, 1):
                if self.table[j].head.add_post is not None and self.table[j].head.add_post.hashcode == i:
                    temp = self.table[j].head.add_post
                    self.table[j].remover(temp.key)
                    self.table[i].inserir(temp.key, temp.value, temp.hashcode)
            i = self.hash_function(i + 1)

    def __str__(self):
        res = ''
        for i in range(0, self.tam_inicial, 1):
            res = res + f'\n{self.table[i]}'
        return res
