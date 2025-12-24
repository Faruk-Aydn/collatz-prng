def bits_to_bytes(bit_list):
    out = bytearray()
    for i in range(0, len(bit_list), 8):
        byte = 0
        for j in range(8):
            if i + j < len(bit_list):
                byte = (byte << 1) | bit_list[i + j]
        out.append(byte)
    return out


# output.txt -> output.bin
with open("output.txt", "r") as f:
    bits = [int(b) for b in f.read().strip()]

data = bits_to_bytes(bits)

with open("output.bin", "wb") as f:
    f.write(data)

print("output.bin oluşturuldu")
