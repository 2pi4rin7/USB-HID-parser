import sys

# Key codes mapping (đầy đủ)
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
    0x2B: ['\t', '\t'], 0x2C: [' ', ' '], 0x2D: ['-', '_'], 0x2E: ['=', '+'],
    0x2F: ['[', '{'], 0x30: [']', '}'], 0x31: ['\\', '|'], 0x32: ['#', '~'],
    0x33: [';', ':'], 0x34: ['\'', '"'], 0x35: ['`', '~'], 0x36: [',', '<'],
    0x37: ['.', '>'], 0x38: ['/', '?'], 0x39: ['[CAPS]', '[CAPS]'],
    0x4F: [u'→', u'→'], 0x50: [u'←', u'←'], 0x51: [u'↓', u'↓'], 0x52: [u'↑', u'↑'],
    # keypad
    0x53: ['NumL', 'NumL'], 0x54: ['/', '/'], 0x55: ['*', '*'], 0x56: ['-', '-'],
    0x57: ['+', '+'], 0x58: ['\n', '\n'], 0x59: ['1', '1'], 0x5A: ['2', '2'],
    0x5B: ['3', '3'], 0x5C: ['4', '4'], 0x5D: ['5', '5'], 0x5E: ['6', '6'],
    0x5F: ['7', '7'], 0x60: ['8', '8'], 0x61: ['9', '9'], 0x62: ['0', '0'],
    0x63: ['.', '.'], 0x67: ['=', '=']
}

def diff_keys(prev, curr):
    prev_set = set([k for k in prev[2:] if k != '00'])
    curr_set = set([k for k in curr[2:] if k != '00'])
    pressed = curr_set - prev_set
    released = prev_set - curr_set
    return pressed, released

def solve(file, output_file="result.txt"):
    with open(file, 'r') as f:
        lines = f.readlines()

    buffer = []
    cursor = 0
    previous = ['00']*8
    left_shift = right_shift = 0
    left_alt = right_alt = 0
    left_ctrl = right_ctrl = 0
    is_cap = 0

    with open(output_file, 'w', encoding="utf-8") as output:
        for line in lines:
            line = line.strip().split(':')
            pressed, released = diff_keys(previous, line)

            status = int(line[0], 16)
            left_ctrl = (status & 1) != 0
            left_shift = (status >> 1) & 1
            left_alt = (status >> 2) & 1
            right_ctrl = (status >> 4) & 1
            right_shift = (status >> 5) & 1
            right_alt = (status >> 6) & 1

            for key_hex in pressed:
                keycode = int(key_hex, 16)
                if keycode not in KEY_CODES:
                    output.write(f"[UNK-{key_hex}]")
                    continue

                key = KEY_CODES[keycode][(left_shift | right_shift) ^ is_cap]
                # CapsLock
                if key == '[CAPS]':
                    is_cap ^= 1
                    continue

                # Backspace
                if key == '[BACKSPACE]':
                    if cursor > 0:
                        buffer.pop(cursor-1)
                        cursor -= 1
                        # ghi lại toàn bộ buffer sau khi xóa
                        output.seek(0)
                        output.truncate()
                        output.write("".join(buffer))
                    continue

                # Tab thường
                if key == '\t':
                    spaces = " " * 4
                    for ch in spaces:
                        buffer.insert(cursor, ch)
                        cursor += 1
                    output.write(spaces)
                    continue

                # Mũi tên
                if key == u'→':
                    cursor = min(len(buffer), cursor + 1)
                    continue
                if key == u'←':
                    cursor = max(0, cursor - 1)
                    continue
                if key == u'↓':
                    output.write("[↓]")
                    continue
                if key == u'↑':
                    output.write("[↑]")
                    continue

                # Enter
                if key == '\n':
                    buffer.insert(cursor, key)
                    cursor += 1
                    output.write(key)
                    continue

                # Ký tự bình thường
                buffer.insert(cursor, key)
                cursor += 1
                output.write(key)

            previous = line

def main():
    args = sys.argv
    if len(args) != 3:
        print(f"Usage: {args[0]} <file capture.txt>" " <output file>")
        return
    solve(args[1], args[2])

if __name__ == "__main__":
    main()
