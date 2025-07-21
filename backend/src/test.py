import bcrypt

a = bcrypt.checkpw("qwerty".encode(), "$2b$12$2kGr/K91KOFf3fXkdll8xullRouCwWzHK2Htp5OgZfKNBOQOlFNlS".encode())
print(a)