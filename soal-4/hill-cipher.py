import numpy as np
from sympy import Matrix, mod_inverse
import time
import re

# Fungsi untuk membersihkan teks (menghapus spasi dan tanda baca)
def clean_text(text):
    return re.sub(r'[^A-Za-z]', '', text).upper()

# Konversi huruf ke angka dan sebaliknya
def text_to_numbers(text):
    return [ord(c) - ord('A') for c in text]

def numbers_to_text(nums):
    return ''.join(chr(n % 26 + ord('A')) for n in nums)

# Fungsi untuk menghitung invers matriks modulo m
def matrix_mod_inv(matrix, mod):
    det = matrix.det() % mod
    if det == 0 or not mod_inverse(det, mod):
        raise ValueError(f"Determinan matriks adalah {det}, yang tidak memiliki invers modulo {mod}")
    return (matrix.adjugate() * mod_inverse(det, mod)) % mod

# Fungsi untuk mendekripsi ciphertext menggunakan matriks kunci
def decrypt_hill_cipher(ciphertext, key_matrix, block_size=3):
    # Hitung invers kunci K^(-1)
    K = Matrix(key_matrix)
    try:
        K_inv = matrix_mod_inv(K, 26)
    except ValueError as e:
        raise ValueError(f"Gagal menghitung invers matriks kunci: {e}")

    # Konversi kembali ke numpy array untuk kemudahan komputasi
    K_inv_np = np.array(K_inv.tolist(), dtype=int)

    # Dekripsi ciphertext
    plaintext = ""
    for i in range(0, len(ciphertext), block_size):
        # Ambil blok ciphertext
        block = ciphertext[i:i+block_size]

        # Jika blok kurang dari block_size, abaikan (biasanya di akhir)
        if len(block) < block_size:
            break

        # Konversi blok ke angka
        block_nums = text_to_numbers(block)

        # Ubah menjadi vektor kolom
        cipher_vector = np.array(block_nums).reshape(-1, 1)

        # Dekripsi blok: P = K^(-1) * C mod 26
        decrypted_vector = (K_inv_np @ cipher_vector) % 26

        # Konversi kembali ke teks
        plaintext += numbers_to_text(decrypted_vector.flatten())

    return plaintext, K_inv.tolist()

# Ciphertext yang diberikan
ciphertext = "CDECCZDKQFYRYRWYWXKVTSBQABTRVRITRXVVKWKJKEMUEVKLYUPUAFSPPSFSKZVGJKKNLWNFXSMUDVHKSWMFERVUWEVZTZQVOGWALCAYTKXAKNKYDTZMTWATADALYSANZSBMIGPUGNTMHFJRSKSTLQKFRXAKHMOHEYQDUMSFIAMOBSKBFWZKGZEVAKSHQHPGJUKKLNSZAIFCWUKUKWMMJUDVVOWHWXEAVWODIAMOBSDNNNUYYRVRWMPQPYJDZRXDZBJUKOPUXIZQTHSKKHEYATYCONMHOACPMNIESNKZZYBKTZHXCGOABREJCIDCJCRVRWNFCJPCUWYNQGCGSLJDWLCHBWNFLCMGNNTDLMPTLSYFWAUMGWFMWQCCWPLAMTSZXAULWDEADALPBQIDUTSJGSWPGKBIAMOBSOKSPGFBDDLMECGVUDVEEZYCORCJEIOMXENEQUMGZHUUSOSCNSFSMDPALWXAHIDEWNFJOQJLLELRNAUVOQQDUINZIKVMSSSGOMGRHSKZWJVOQASVCKVIZGIQWPIQGJKLWURYLIQBOAZMHOACPMNIESNCUKXWSGIYEBHTYIBEIMHOACPMNIESNSKKHEYOOPTSOFRFHSGBZHXCXATDOOFNOEWKQXHJYCUYUZBPXSMDESDJDOZGANUGMFWSMMLMCYZEVECXLFNUACWPYMHOBSWQCQWROHPVUMDOTEMXBGDANZKNUCSLFSKPCJUGAURCOQZOUEXTFWNFETPUPLZMTAVZQOZCJCRVRWNFYILHSXUSQBXBNSIFSFCWPHAVOHVWCRTNPIWQWLYTEEEQXEMXBUPCAFBXBPGMPGVTFDTDLNGOCPMPUYXHWVZNMVDMZGOZDGQHSGWAQXLZGPGSYUZAPVSBQBXBPGMPGVTFDVGGAWQOPAAVZDSSNLJANNSETBGXSSBFCJDWLCHBWNFMULCJCRVRNWJIUIFFVBVLHYCKKSTRZPQICAQUUPEKMEYLECLAHACASRIADDUVDHIQWZAIORLZMCAIEOMJNGONEDVCCOGXQMPXHJYCUYUZJOQDTJMXFWQCEQXQJOMJPOJIABTRVRPUYEDSDDHSUOFIUTQJFESFWGATDZQVZVHBHZAPVSBQCBOXUNFQGZZPKSQQDUWUTGYNXLXFYEVZAYRFLAMDUNZUMPVDZZDMETGIVHMDNHXAXPLLNCAYNSVDNAXSMVVLYDTCRPLRFLAMTSZXAULWDHCVAKKOHPVUMKJOSQGQBWYKLKRQSKKMMJLWWWTCYKEUGNWBGKNLWUTRYYYBLOIDNWREQXACLBEVUDDECEQXMFWFRFUMONGIENMOEY"

# Matriks Kunci
known_key = [
    [6, 13, 20],
    [24, 16, 17],
    [1, 10, 15]
]

if __name__ == "__main__":
    print("=== DEKRIPSI HILL CIPHER ===")
    print("Menggunakan Matriks Kunci yang Diketahui")

    start_time = time.time()

    try:
        decryption_result = decrypt_hill_cipher(ciphertext, known_key, 3)
        decrypted_text = decryption_result[0]
        inverse_key = decryption_result[1]
        end_time = time.time()

        print("\n## Plainteks hasil dekripsi")
        print(decrypted_text)

        print("\n## Matriks Kunci")
        print(Matrix(known_key))

        print("\n## Matriks Invers Kunci")
        print(Matrix(inverse_key))

        print(f"\n## Waktu Dekripsi: {end_time - start_time:.4f} detik")

    except ValueError as e:
        print(f"\n[!] Dekripsi gagal: {e}")