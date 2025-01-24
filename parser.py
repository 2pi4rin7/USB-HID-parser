from time import sleep
from pynput.keyboard import Controller, Key, KeyCode

keyboard = Controller()

KEYMAP = {
    # Alphanumeric Keys
    0x04: KeyCode.from_vk(0x41), 0x05: KeyCode.from_vk(0x42),
    0x06: KeyCode.from_vk(0x43), 0x07: KeyCode.from_vk(0x44),
    0x08: KeyCode.from_vk(0x45), 0x09: KeyCode.from_vk(0x46),
    0x0A: KeyCode.from_vk(0x47), 0x0B: KeyCode.from_vk(0x48),
    0x0C: KeyCode.from_vk(0x49), 0x0D: KeyCode.from_vk(0x4A),
    0x0E: KeyCode.from_vk(0x4B), 0x0F: KeyCode.from_vk(0x4C),
    0x10: KeyCode.from_vk(0x4D), 0x11: KeyCode.from_vk(0x4E),
    0x12: KeyCode.from_vk(0x4F), 0x13: KeyCode.from_vk(0x50),
    0x14: KeyCode.from_vk(0x51), 0x15: KeyCode.from_vk(0x52),
    0x16: KeyCode.from_vk(0x53), 0x17: KeyCode.from_vk(0x54),
    0x18: KeyCode.from_vk(0x55), 0x19: KeyCode.from_vk(0x56),
    0x1A: KeyCode.from_vk(0x57), 0x1B: KeyCode.from_vk(0x58),
    0x1C: KeyCode.from_vk(0x59), 0x1D: KeyCode.from_vk(0x5A),

    # Numbers
    0x1E: KeyCode.from_vk(0x31), 0x1F: KeyCode.from_vk(0x32),
    0x20: KeyCode.from_vk(0x33), 0x21: KeyCode.from_vk(0x34),
    0x22: KeyCode.from_vk(0x35), 0x23: KeyCode.from_vk(0x36),
    0x24: KeyCode.from_vk(0x37), 0x25: KeyCode.from_vk(0x38),
    0x26: KeyCode.from_vk(0x39), 0x27: KeyCode.from_vk(0x30),

    # Keypad
    0x58: KeyCode.from_vk(0x0D),
    0x54: KeyCode.from_vk(0xBF),
    0x59: KeyCode.from_vk(0x61), 0x5A: KeyCode.from_vk(0x62),
    0x5B: KeyCode.from_vk(0x63), 0x5C: KeyCode.from_vk(0x64),
    0x5D: KeyCode.from_vk(0x65), 0x5E: KeyCode.from_vk(0x66),
    0x5F: KeyCode.from_vk(0x67), 0x60: KeyCode.from_vk(0x68),
    0x61: KeyCode.from_vk(0x69), 0x62: KeyCode.from_vk(0x60),

    # Punctuation
    0x2B: KeyCode.from_vk(0x09),
    0x2C: KeyCode.from_vk(0x20), 0x2D: KeyCode.from_vk(0xBD),
    0x2E: KeyCode.from_vk(0xBB), 0x31: KeyCode.from_vk(0xDC),
    0x33: KeyCode.from_vk(0xBA), 0x34: KeyCode.from_vk(0xDE),
    0x36: KeyCode.from_vk(0xBC), 0x37: KeyCode.from_vk(0xBE),

    # Special Keys
    0x28: KeyCode.from_vk(0x0D), 0x29: KeyCode.from_vk(0x1B),
    0x2A: KeyCode.from_vk(0x08),
    0x3B: KeyCode.from_vk(0x71),
    0x4D: KeyCode.from_vk(0x23),
    0x4F: KeyCode.from_vk(0x27), 0x50: KeyCode.from_vk(0x25),
    0x51: KeyCode.from_vk(0x28), 0x52: KeyCode.from_vk(0x26),
}

GROUPPING = {
    (Key.shift_l, KeyCode.from_vk(0x61)): KeyCode.from_vk(0x23), # 1: End
    (Key.shift_r, KeyCode.from_vk(0x61)): KeyCode.from_vk(0x23),
    (Key.shift_l, KeyCode.from_vk(0x62)): KeyCode.from_vk(0x28), # 2: Down
    (Key.shift_r, KeyCode.from_vk(0x62)): KeyCode.from_vk(0x28),
    (Key.shift_l, KeyCode.from_vk(0x63)): KeyCode.from_vk(0x22), # 3: PgDn
    (Key.shift_r, KeyCode.from_vk(0x63)): KeyCode.from_vk(0x22),
    (Key.shift_l, KeyCode.from_vk(0x64)): KeyCode.from_vk(0x25), # 4: Left
    (Key.shift_r, KeyCode.from_vk(0x64)): KeyCode.from_vk(0x25),
    (Key.shift_l, KeyCode.from_vk(0x66)): KeyCode.from_vk(0x27), # 6: Right
    (Key.shift_r, KeyCode.from_vk(0x66)): KeyCode.from_vk(0x27),
    (Key.shift_l, KeyCode.from_vk(0x67)): KeyCode.from_vk(0x24), # 7: Home
    (Key.shift_r, KeyCode.from_vk(0x67)): KeyCode.from_vk(0x24),
    (Key.shift_l, KeyCode.from_vk(0x68)): KeyCode.from_vk(0x26), # 8: Up
    (Key.shift_r, KeyCode.from_vk(0x68)): KeyCode.from_vk(0x26),
    (Key.shift_l, KeyCode.from_vk(0x69)): KeyCode.from_vk(0x21), # 9: PgUp
    (Key.shift_r, KeyCode.from_vk(0x69)): KeyCode.from_vk(0x21),
}

usbhid_data: list[tuple[float, bytes]] = []
with open('usbhid.data.hex', 'rt') as source_file:
    for line in source_file:
        if not line.strip():
            continue
        time, data = line.strip().split('\t')
        usbhid_data.append((float(time), bytes.fromhex(data)))

key_names: list[tuple[float, list[str]]] = []
for time, data in usbhid_data:
    modifiers, key = data[0], data[2]
    keys = []

    modifiers & 0b00000001 and keys.append(Key.ctrl_l)
    modifiers & 0b00000010 and keys.append(Key.shift_l)
    modifiers & 0b00000100 and keys.append(Key.alt_l)
    modifiers & 0b00001000 and keys.append(Key.cmd_l)
    modifiers & 0b00010000 and keys.append(Key.ctrl_r)
    modifiers & 0b00100000 and keys.append(Key.shift_r)
    modifiers & 0b01000000 and keys.append(Key.alt_r)
    modifiers & 0b10000000 and keys.append(Key.cmd_r)

    if key in KEYMAP:
        keys.append(KEYMAP[key])
    elif key != 0:
        assert False, f'<unknown key {key:02x}>'

    key_names.append((time, keys))

for i in range(1, len(key_names) - 1):
    for group, replacement in GROUPPING.items():
        priority, key = group
        if priority in key_names[i][1] and key in key_names[i][1]:
            for j in range(3):
                key in key_names[i+j][1] and key_names[i+j][1].remove(key)
            key_names[i][1].append(replacement)

with open('result.txt', 'wt') as result_file:
    for time, keys in key_names:
        result_file.write(f'{time}\t{keys}\n')

sleep(2)

current_time = 0
pressed_keys = set()
for i, keys in enumerate(key_names):
    time, data = keys
    if time < 1550:
        sleep_time = 0
    elif time < 3200:
        sleep_time = 0.02
    elif time > 3500:
        break
    else:
        sleep_time = min(0.2, time - current_time)
    print(*keys)
    sleep(sleep_time)
    for key in pressed_keys - set(data):
        keyboard.release(key)
        pressed_keys.remove(key)
    for key in set(data) - pressed_keys:
        keyboard.press(key)
        pressed_keys.add(key)
    current_time = time