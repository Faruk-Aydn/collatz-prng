import hashlib
from collections import deque

# =====================================================
# 1️⃣ Collatz tabanlı entropy (SAFE & FAST)
# =====================================================
def collatz_entropy(seed, max_bits):
    n = seed
    bits = []
    steps = 0
    MAX_STEPS = max_bits * 5  # güvenlik freni

    while len(bits) < max_bits and steps < MAX_STEPS:
        # Bias azaltan non-linear bit
        bit = (n ^ (n >> 1) ^ (n >> 2)) & 1
        bits.append(bit)

        # Collatz adımı
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1

        # sayı patlamasını engelle
        n = (n % 1_000_000) + 1
        steps += 1

    return bits


# =====================================================
# 2️⃣ Non-linear LFSR (sabit register)
# =====================================================
def nlfsr(bits, reg_size=32):
    reg = deque(bits[:reg_size], maxlen=reg_size)
    out = []

    for _ in range(len(bits)):
        # non-linear feedback
        new_bit = (reg[0] & reg[1]) ^ reg[3] ^ reg[-1]
        out.append(reg[-1])
        reg.appendleft(new_bit)

    return out


# =====================================================
# 3️⃣ Hash whitening (counter-based expansion)
# =====================================================
def hash_whitening(bits, out_bits):
    # bit → byte
    data = bytearray()
    for i in range(0, len(bits), 8):
        b = 0
        for j in range(8):
            if i + j < len(bits):
                b = (b << 1) | bits[i + j]
        data.append(b)

    output = []
    counter = 0

    while len(output) < out_bits:
        h = hashlib.sha256(data + counter.to_bytes(4, "big")).digest()
        for byte in h:
            for i in range(8):
                output.append((byte >> (7 - i)) & 1)
                if len(output) >= out_bits:
                    break
        counter += 1

    return output


# =====================================================
# 4️⃣ Ana RNG
# =====================================================
def generate_rng(seed=9, total_bits=65536):
    print("PROGRAM BAŞLADI")

    print("Collatz entropy üretiliyor...")
    bits = collatz_entropy(seed, total_bits)
    print("Collatz OK")

    print("NLFSR çalışıyor...")
    bits = nlfsr(bits)
    print("NLFSR OK")

    print("Hash whitening...")
    bits = hash_whitening(bits, total_bits)
    print("Whitening OK")

    return bits


# =====================================================
# 5️⃣ Çalıştır & dosyaya yaz
# =====================================================
if __name__ == "__main__":
    STREAM_BITS = 65536  # 8 KB (ENT için yeterli)

    stream = generate_rng(seed=9, total_bits=STREAM_BITS)

    print("Toplam Bit:", len(stream))
    print("0 Sayısı:", stream.count(0))
    print("1 Sayısı:", stream.count(1))
    print("0 Oranı:", stream.count(0) / len(stream))
    print("1 Oranı:", stream.count(1) / len(stream))

    with open("output.txt", "w") as f:
        f.write("".join(str(b) for b in stream))

    print("output.txt yazıldı")
    print("BİTTİ")
