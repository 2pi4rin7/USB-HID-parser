import sys
import subprocess
# Key codes mapping
KEY_CODES = {
    0x04: ['a', 'A'], 0x05: ['b', 'B'], 0x06: ['c', 'C'], 0x07: ['d', 'D'],
    0x08: ['e', 'E'], 0x09: ['f', 'F'], 0x0A: ['g', 'G'], 0x0B: ['h', 'H'],
    0x0C: ['i', 'I'], 0x0D: ['j', 'J'], 0x0E: ['k', 'K'], 0x0F: ['l', 'L'],
    0x10: ['m', 'M'], 0x11: ['n', 'N'], 0x12: ['o', 'O'], 0x13: ['p', 'P'],
    0x14: ['q', 'Q'], 0x15: ['r', 'R'], 0x16: ['s', 'S'], 0x17: ['t', 'T'],
    0x18: ['u', 'U'], 0x19: ['v', 'V'], 0x1A: ['w', 'W'], 0x1B: ['x', 'X'],
    0x1C: ['y', 'Y'], 0x1D: ['z', 'Z'], 0x1E: ['1', '!'], 0x1F: ['2', '@'],
    0x20: ['3', '#'], 0x21: ['4', '$'], 0x22: ['5', '%'], 0x23: ['6', '^'],
    0x24: ['7', '&'], 0x25: ['8', '*'], 0x26: ['9', '('], 0x27: ['0', ')'],
    0x28: ['\n', '\n'], 0x29: ['[ESC]', '[ESC]'], 0x2A: ['[BACKSPACE]', '[BACKSPACE]'],
    0x2C: [' ', ' '], 0x2D: ['-', '_'], 0x2E: ['=', '+'], 0x2F: ['[', '{'],
    0x30: [']', '}'], 0x32: ['#', '~'], 0x33: [';', ':'], 0x34: ['\'', '"'],
    0x36: [',', '<'], 0x37: ['.', '>'], 0x38: ['/', '?'], 0x39: ['[CAPSLOCK]', '[CAPSLOCK]'],
    0x2B: ['\t', '\t'], 0x4F: [u'→', u'→'], 0x50: [u'←', u'←'], 0x51: [u'↓', u'↓'],
    0x52: [u'↑', u'↑'], 0x39: [u'[CAPS]', u'[CAPS]'], 0x81: ['VDn', 'VDn'], 0x80: ['VUp', 'VUp'],
    0x7F: ['Mut', 'Mut'], 0x53: ['NumL', 'NumL'], 0x54: ['/', '/'], 0x55: ['*', '*'], 0x56:['-', '-'],
    0x5F: ['7', '7'], 0x60: ['8', '8'], 0x61: ['9', '9'], 0x57: ['+', '+'], 0x5C: ['4', '4'], 0x5D: ['5', '5'], 
    0x5E: ['6', '6'], 0x85: [',', ','], 0x59: ['1', '1'], 0x5A: ['2', '2'], 0x5B: ['3', '3'], 0x58: ['\n', '\n'],
    0x62: ['0', '0'], 0x63: ['.', '.'], 0x67: ['=', '=']
}

def compare(previous, present):
    for a, b in zip(previous, present):
        c = int(a, 16)
        d = int(b, 16)
        if c != d and d == 0:
            return "release_key"
    return "new_key"


def solve(file):
    result = [["" for i in range(10000)] for j in range(10000)]
    x = 0
    y = 0
    previous = ['00', '00', '00', '00', '00', '00', '00', '00']
    left_shift = 0
    is_cap = 0
    left_alt = 0
    left_ctrl = 0
    right_shift = 0
    right_alt = 0
    right_ctrl = 0
    with open(file, 'r') as f:
        lines = f.readlines()        
    output = open("result.txt", 'w') 
    for line in lines:
        line = line.strip().split(':')
        if compare(previous, line) == 'release_key':
            previous = line
            continue
        status = int(line[0], 16)
        if (status & 1):
            left_ctrl = 1
        if (status >> 1) & 1:
            left_shift = 1
        if (status >> 2) & 1:
            left_alt = 1
        if (status >> 4) & 1:
            right_ctrl = 1
        if (status >> 5) & 1:
            right_shift = 1
        if (status >> 6) & 1:
            right_alt = 1
        if status == 0:
            left_ctrl = left_alt = left_shift = 0
            right_alt = right_ctrl = right_shift = 0
        
        command = ""
        if status != 0x02 and status != 0 and status != 0x20:
            if left_shift:
                command += " [left_shift] "
            if left_ctrl: 
                command += " [left_ctrl] "
            if left_alt:
                command += " [left_alt] "
            if right_shift:
                command += " [right_shift] "
            if right_ctrl:
                command += " [right_ctrl] "
            if right_alt:
                command += " [right_alt] "   
            output.write(command)
        for i in range(2, len(line)):
            if line[i] == '00':
                continue
            try:
                key = KEY_CODES[int(line[i], 16)][(left_shift | right_shift) ^ is_cap]
                if left_alt == True:
                    print(f'alt + {key}')
                if key == u'[CAPS]':
                    is_cap = not is_cap
                elif key == u'→':
                    y += 1
                elif key == u'←':
                    y -= 1
                    y = max(y, 0)
                elif key == u'↓':
                    x += 1
                elif key == u'↑':
                    x -= 1
                    x = max(x, 0)
                elif key == '\n':
                    output.write(key)
                    x += 1
                    y = 0
                else:
                    output.write(key)
                    y += 1
            except:
                print(f"Can found the key {line[i]}")
        previous = line
        if status != 0x02 and status != 0 and status != 0x20:
            output.write('\n')

def main():
    args = sys.argv
    if len(args) != 2:
        print(f"Usage: {args[0]} <file capture.pcapng>")
        return
    solve(args[1])

if __name__ == "__main__":
    main()
