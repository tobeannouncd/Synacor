with open('data/arch-spec') as f:
    specs = f.read()

CODES = {}
for line in specs.splitlines()[35::2]:
    name, spec = line.split(': ')
    code, *args = spec.split()
    CODES[int(code)] = name, len(args)


if __name__ == '__main__':
    for code, (name, n_args) in sorted(CODES.items()):
        print(f'Opcode {code} is {name} and takes {n_args} args')
