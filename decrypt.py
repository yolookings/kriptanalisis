import time
from collections import Counter
from spellchecker import SpellChecker


# Mulai waktu analisis
start_time = time.time()

# Fungsi untuk mencari posisi huruf dalam key square
def find_pos(c, key_square):
    for row in range(5):
        for col in range(5):
            if key_square[row][col] == c:
                return row, col

# Fungsi dekripsi Playfair
def playfair_decrypt(ciphertext, key_square):
    plaintext = ""
    i = 0
    while i < len(ciphertext):
        a, b = ciphertext[i], ciphertext[i + 1]
        r1, c1 = find_pos(a, key_square)
        r2, c2 = find_pos(b, key_square)

        if r1 == r2:
            plaintext += key_square[r1][(c1 - 1) % 5]
            plaintext += key_square[r2][(c2 - 1) % 5]
        elif c1 == c2:
            plaintext += key_square[(r1 - 1) % 5][c1]
            plaintext += key_square[(r2 - 1) % 5][c2]
        else:
            plaintext += key_square[r1][c2]
            plaintext += key_square[r2][c1]
        i += 2
    return plaintext

# Fungsi hitung digram
def count_digrams(text):
    digrams = [text[i:i+2] for i in range(0, len(text)-1, 2)]
    return Counter(digrams)

# Kunci dan key square
key = "FYBDEQUMOPHXVWZGASRITKLCN"
key_square = [list(key[i:i+5]) for i in range(0, 25, 5)]

# Baca ciphertext dari file
with open("cipherteks.txt", "r") as file:
    cipher = file.read().upper().replace(" ", "").replace("\n", "")
    cipher = ''.join(filter(str.isalpha, cipher))

# Hitung frekuensi digram ciphertext
cipher_digram_freq = count_digrams(cipher)

# Dekripsi Playfair
decrypted_text = playfair_decrypt(cipher, key_square)

# Simpan hasil dekripsi awal (sebelum spell check)
with open("decrypted_raw.txt", "w") as f:
    f.write(decrypted_text)

# Spell checking
spell = SpellChecker()
segments = [decrypted_text[i:i+12] for i in range(0, len(decrypted_text), 12)]

corrected = []
for seg in segments:
    guesses = spell.candidates(seg.lower())
    if guesses:
        corrected.append(list(guesses)[0].upper())
    else:
        corrected.append(seg)

final_text = " ".join(corrected)

# Simpan hasil setelah spell check
with open("decrypted_spellchecked.txt", "w") as f:
    f.write(final_text)

# Hitung waktu selesai
end_time = time.time()
total_time = end_time - start_time

# Digram referensi bahasa Inggris (contoh sederhana — kamu bisa ganti dari file referensi lain)
english_digrams = ["TH", "HE", "IN", "ER", "AN", "RE", "ED", "ON", "ES", "ST"]
english_digram_freq = {d: cipher.count(d) for d in english_digrams}

# Output ke terminal
print("\n===== Output =====")
print("\n• Tabel frekuensi digram dalam bahasa Inggris (contoh):")
for digram, freq in english_digram_freq.items():
    print(f"{digram}: {freq}")

print("\n• Tabel frekuensi digram dalam ciphertext:")
for digram, freq in cipher_digram_freq.most_common(10):
    print(f"{digram}: {freq}")

print("\n• Kunci enkripsi:")
print(key)

print("\n• Waktu kriptanalisis:")
print(f"{total_time:.2f} detik")

print("\n• File hasil dekripsi:")
print("- decrypted_raw.txt (hasil sebelum spell check)")
print("- decrypted_spellchecked.txt (hasil setelah spell check)")
