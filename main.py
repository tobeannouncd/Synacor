from src.vm import VirtualMachine


def main():
    fn = 'data/challenge.bin'
    vm = VirtualMachine(fn)
    vm.run()


if __name__ == '__main__':
    main()
