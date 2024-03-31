from hashlib import sha256

senha="1234"

senha_cripto = sha256(senha.encode()).hexdigest()

print(senha)
print(senha_cripto)