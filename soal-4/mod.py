from sympy import Matrix

# Definisi matriks 
C = Matrix([[2, 2, 3],
            [3, 2, 10],
            [4, 25, 16]])

P = Matrix([[7, 11, 24],
            [4, 14, 1],
            [11, 2, 4]])

# Hitung invers P dalam mod 26
try:
    P_inv_mod26 = P.inv_mod(26)
    # Hitung K = C * P^-1 mod 26a
    K = (C * P_inv_mod26) % 26
except ValueError:
    P_inv_mod26 = "Matriks P tidak memiliki invers dalam mod 26"
    K = None

P_inv_mod26, K
