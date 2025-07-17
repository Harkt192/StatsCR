import bcrypt


password = "qwertyasfafasfassssssssasfasfasfqwfq2413241"
print(type(password), password)
print(type(password.encode()), password.encode())
hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
print(type(hashed_password), hashed_password)

unhashed_password = bcrypt.checkpw(password.encode(), hashed_password)
print(unhashed_password)
