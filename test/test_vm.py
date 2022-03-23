from src.vm import VirtualMachine


class TestVM:
    def test_sample_program(self):
        char = 'G'
        program = "9,32768,32769,4,19,32768".split(',')

        vm = VirtualMachine(interactive=False)
        for i, val in enumerate(program):
            vm.memory[i] = int(val)
        vm.registers[1] = ord(char)-4
        vm.run()
        assert vm.output_buffer == char

    def test_boot(self):
        fn = 'data/challenge.bin'
        vm = VirtualMachine(fn, interactive=False)
        assert vm.run() == 1
