def fnv1a_hash(text):
    """Calcular hash FNV-1"""
    FNV_prime = 1099511628211
    offset_basis = 14695981039346656037
    hash_value = offset_basis
    for c in text:
        hash_value ^= ord(c)
        hash_value *= FNV_prime
        hash_value &= 0xFFFFFFFFFFFFFFFF  # Mantener 64 bits
    return hex(hash_value)[2:]
