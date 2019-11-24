#!/usr/bin/env python3
import sys
import platform


class USBInput:
    def __init__(self):
        self.posX = 0
        self.posY = 0

        self.screenx = 1600
        self.screeny = 900

        self.shift_down = False

        if platform.system() == 'Windows':
            self.keyboard_fd = open('C:\\Users\\Richard\\PycharmProjects\\keyboard_input\\keyboard', 'wb+', buffering=8)
            self.mouse_fd = open('C:\\Users\\Richard\\PycharmProjects\\keyboard_input\\mouse', 'wb+', buffering=3)
        else:
            self.keyboard_fd = open('/dev/hidg0', 'rb+', buffering=8)
            self.mouse_fd = open('/dev/hidg1', 'rb+', buffering=3)

        self.outm = bytearray(b'\x00\x00\x00')
        self.outk = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00')

    def keyboard_down(self, key):
        if key == 'Shift':
            self.outk[0] = 32
        else:
            if str(key).isupper():
                key = ord(key)
            else:
                key = ord(key) - 93
            print(f'{key}')
            self.outk[2] = key
            self.keyboard_fd.write(self.outk)
            self.keyboard_fd.flush()

            self.outk[2] = 0
            self.keyboard_fd.write(self.outk)
            self.keyboard_fd.flush()

    def keyboard_up(self, key):
        if key == 'Shift':
            self.outk[0] = 0

    def keyboard(self, key):
        if key == 'Shift':
            self.shift_down = False if self.shift_down else True
            return
        if self.shift_down:
            self.outk[0] = chr(32)
        self.outk[2] = ord(key) - 93
        self.keyboard_fd.write(self.outk)
        self.keyboard_fd.flush()

        self.outk[2] = 0
        self.keyboard_fd.write(self.outk)
        self.keyboard_fd.flush()

    @staticmethod
    def mbut(n):
        k = {
            0: 0b00000100,  # bit 2 is L_Button
            1: 0b00000010,  # bit 1 is M_Button
            2: 0b00000001,  # bit 0 is R_Button
            3: 0b10000000,  # bit 8 is ???
            4: 0b01000000,  # bit 7 is ???
            # unable to test.
            5: 0b00100000,  # bit 6 is ???
            6: 0b00010000,  # bit 5 is ???
        }
        return k.get(n, 0x00)

    def mouse_button_down(self, data):
        print(f'{data}')
        self.outm[0] = self.outm[0] | self.mbut(data)
        self.mouse_fd.write(self.outm)
        self.mouse_fd.flush()

    def mouse_button_up(self, data):
        self.outm[0] = self.outm[0] ^ self.mbut(data)
        self.mouse_fd.write(self.outm)
        self.mouse_fd.flush()

    def mouse_move(self, x, y):
        xv = x - self.posX
        yv = y - self.posY

        self.posX = x
        self.posY = y

        self.mouse(xv, yv)

    def mouse(self, x, y):
        xv = 255 + x if x < 0 else x
        yv = 255 + y if y < 0 else y

        self.outm[1] = xv if 0 <= xv <= 255 else 0
        self.outm[2] = yv if 0 <= yv <= 255 else 0

        print(f'mouse button {self.outm}')

        self.mouse_fd.write(self.outm)
        self.mouse_fd.flush()


if __name__ == '__main__':
    test = USBInput()
    test.keyboard(sys.argv[1])
