import operator
from src.utils import from_bin
from src.ops import CODES

NUM_REGISTERS = 8
ADDRESS_SPACE = 2**15
MOD = 2**15


class VirtualMachine:
    def __init__(self, filename=None, interactive=True) -> None:
        self.memory = [0]*ADDRESS_SPACE
        self.registers = [0]*NUM_REGISTERS
        self.i = 0
        self.stack = []
        self.input_buffer = []
        self.output_buffer = ''
        self.interactive = interactive

        if filename:
            for i, val in enumerate(from_bin(filename)):
                self.memory[i] = val

    def read(self, n=1):
        vals = []
        for _ in range(n):
            vals.append(self.memory[self.i])
            self.i += 1
        if n == 1:
            return vals[0]
        return vals

    def value(self, n):
        if n < ADDRESS_SPACE:
            return n
        return self.registers[n % NUM_REGISTERS]

    def step(self):
        opcode = self.read()
        name, n_args = CODES[opcode]
        args = self.read(n_args)

        if opcode == 0:
            return 0
        elif opcode == 1:
            a, b = args
            self.set_register(a, b)
        elif opcode == 2:
            self.push(args)
        elif opcode == 3:
            self.set_register(args, self.stack.pop())
        elif opcode == 4:
            a, b, c = args
            val = int(self.operate(operator.eq, b, c))
            self.set_register(a, val)
        elif opcode == 5:
            a, b, c = args
            val = int(self.operate(operator.gt, b, c))
            self.set_register(a, val)
        elif opcode == 6:
            self.jump(args)
        elif opcode == 7:
            a, b = args
            if self.value(a):
                self.jump(b)
        elif opcode == 8:
            a, b = args
            if not self.value(a):
                self.jump(b)
        elif opcode == 9:
            a, b, c = args
            val = self.operate(operator.add, b, c)
            self.set_register(a, val)
        elif opcode == 10:
            a, b, c = args
            val = self.operate(operator.mul, b, c)
            self.set_register(a, val)
        elif opcode == 11:
            a, b, c = args
            val = self.operate(operator.mod, b, c)
            self.set_register(a, val)
        elif opcode == 12:
            a, b, c = args
            val = self.operate(operator.and_, b, c)
            self.set_register(a, val)
        elif opcode == 13:
            a, b, c = args
            val = self.operate(operator.or_, b, c)
            self.set_register(a, val)
        elif opcode == 14:
            a, b = args
            val = self.value(b) ^ (2**15 - 1)
            self.set_register(a, val)
        elif opcode == 15:
            a, b = args
            self.set_register(a, self.memory[self.value(b)])
        elif opcode == 16:
            a, b = args
            self.memory[self.value(a)] = self.value(b)
        elif opcode == 17:
            self.push(self.i)
            self.jump(args)
        elif opcode == 18:
            if not self.stack:
                return 2
            self.jump(self.stack.pop())
        elif opcode == 19:
            a = args
            self.output(a)
        elif opcode == 20:
            return self.input(args)
        elif opcode == 21:
            pass
        else:
            raise NotImplementedError(f'{opcode}: {name} {n_args}')

    def push(self, val):
        self.stack.append(self.value(val))

    def input(self, i):
        if not self.input_buffer and not self.interactive:
            self.i -= 2
            return 1
        if self.interactive and not self.input_buffer:
            s = input('>>> ') + '\n'
            self.input_buffer.extend(s[::-1])
        self.set_register(i, ord(self.input_buffer.pop()))

    def output(self, val):
        char = chr(self.value(val))
        if self.interactive:
            print(char, end='')
        else:
            self.output_buffer += char

    def jump(self, i):
        self.i = self.value(i)

    def operate(self, func, b, c):
        return func(self.value(b), self.value(c)) % MOD

    def set_register(self, i, val):
        self.registers[i % NUM_REGISTERS] = self.value(val)

    def run(self):
        while True:
            status = self.step()
            if status is None:
                continue
            return status
