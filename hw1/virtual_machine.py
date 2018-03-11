import sys
import argparse
import struct

import numpy as np

from commands import *


class VirtualMachine(object):
    def __init__(self, memory_size, input_file):
        self.memory = np.zeros(shape=(memory_size * 16), dtype=np.int32)
        with open(input_file, mode='rb') as memory:
            a = memory.read()
            assert len(a) % 4 == 0
            for i in range(0, len(a), 4):
                self.memory[i // 4] = int.from_bytes(a[i:i + 4], 'little')

        self.frame_pointer = self.memory.shape[0] - 1 - 3
        self.exec_pointer = 0
        self.push_delta = 0

    @property
    def exec_pointer(self):
        return self.at(-1)

    @exec_pointer.setter
    def exec_pointer(self, value):
        self.memory[-1] = value

    @property
    def frame_pointer(self):
        return self.at(-2)

    @frame_pointer.setter
    def frame_pointer(self, value):
        self.memory[-2] = value

    @property
    def push_delta(self):
        return self.at(-3)

    @push_delta.setter
    def push_delta(self, value):
        self.memory[-3] = value

    def __repr__(self):
        return str(self.memory[:10])

    def at(self, pointer, shift=0):
        return self.memory[pointer + shift]

    def exec(self, shift=0):
        return self.at(self.exec_pointer, shift)

    def frame(self, shift=0):
        return self.at(self.frame_pointer, shift)

    def frame_exec(self, shift=0):
        return self.frame_pointer + self.exec(shift)

    def read_string(self, pointer, length):
        bytes_length = (length + 3) // 4
        s = struct.pack('<' + 'i' * bytes_length, *self.memory[pointer:pointer + bytes_length])
        return s[:length].decode("utf-8")

    def add(self, pointer, value):
        self.memory[pointer] += value

    def write(self, pointer, value):
        self.memory[pointer] = value

    def next_exec_pointer(self, command):
        if command in {LOCAL}:
            return self.exec_pointer + 1
        elif command in {PRINT, PRINT_INT, IN, PUSH, PUSH_C, REDUCE, DEC}:
            return self.exec_pointer + 2
        elif command in {ADD, ADD_C, ASS, ASS_C}:
            return self.exec_pointer + 3
        elif command in {JUMP, JUMP_BACK, CALL, LC_JUMP}:
            return self.exec_pointer
        else:
            raise NotImplementedError()

    def PRINT(self):
        start = self.exec(1) + 1
        length = self.at(start, -1)
        print(self.read_string(start, length))

    def PRINT_INT(self):
        pointer = self.frame_exec(1)
        print(self.at(pointer))

    def ADD(self):
        to = self.frame_exec(1)
        self.add(to, self.at(self.frame_exec(2)))

    def ADD_C(self):
        to = self.frame_exec(1)
        self.add(to, self.exec(2))

    def ASS(self):
        to = self.frame_exec(1)
        self.write(to, self.at(self.frame_exec(2)))

    def ASS_C(self):
        to = self.frame_exec(1)
        self.write(to, self.exec(2))

    def PUSH(self):
        self.write(self.frame_pointer - self.push_delta, self.at(self.frame_exec(1)))
        self.push_delta += 1

    def PUSH_C(self):
        self.write(self.frame_pointer - self.push_delta, self.exec(1))
        self.push_delta += 1

    def JUMP(self):
        self.exec_pointer = self.exec(1)

    def JUMP_BACK(self):
        self.exec_pointer = self.at(self.frame_exec(1))
        self.frame_pointer += 2

    def IN(self):
        self.write(self.frame_exec(1), int(sys.stdin.readline()))

    def REDUCE(self):
        self.frame_pointer += self.exec(1)

    def CALL(self):
        self.frame_pointer -= + self.push_delta
        self.push_delta = 0
        self.write(self.frame_pointer, 0)
        self.write(self.frame_pointer - 1, self.exec_pointer + 2)
        self.frame_pointer -= 2
        self.exec_pointer = self.exec(1)

    def LOCAL(self):
        self.write(self.frame_pointer, 0)
        self.frame_pointer -= 1

    def LC_JUMP(self):
        if self.at(self.frame_exec(1)) < self.exec(2):
            self.exec_pointer = self.exec(3)
        else:
            self.exec_pointer += 4

    def DEC(self):
        to = self.frame_exec(1)
        self.write(to, self.at(to) - 1)

    def run(self):
        command = self.exec()
        # print(command)

        if self.exec() == PRINT:
            self.PRINT()
        elif self.exec() == PRINT_INT:
            self.PRINT_INT()
        elif self.exec() == ADD:
            self.ADD()
        elif self.exec() == ADD_C:
            self.ADD_C()
        elif self.exec() == ASS:
            self.ASS()
        elif self.exec() == ASS_C:
            self.ASS_C()
        elif self.exec() == JUMP:
            self.JUMP()
        elif self.exec() == PUSH:
            self.PUSH()
        elif self.exec() == PUSH_C:
            self.PUSH_C()
        elif self.exec() == IN:
            self.IN()
        elif self.exec() == CALL:
            self.CALL()
        elif self.exec() == JUMP_BACK:
            self.JUMP_BACK()
        elif self.exec() == REDUCE:
            self.REDUCE()
        elif self.exec() == LOCAL:
            self.LOCAL()
        elif self.exec() == LC_JUMP:
            self.LC_JUMP()
        elif self.exec() == DEC:
            self.DEC()

        else:
            return False

        self.exec_pointer = self.next_exec_pointer(command)

        return True

    def dump(self, filename):
        with open(filename, 'wb') as h:
            h.write(struct.pack('<' + 'i' * self.memory.shape[0], *self.memory))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--memory', help='memory file', required=True)
    parser.add_argument('--stack-size', type=int, help='stack size in kB', default=1024)
    return parser.parse_args()


def main():
    args = parse_args()
    machine = VirtualMachine(args.stack_size, args.memory)
    while machine.run():
        # print(machine.memory[machine.frame_pointer + 1:])
        pass
        # print(machine.memory[machine.frame_pointer + 1:])


if __name__ == '__main__':
    main()
