from cryptography.fernet import Fernet
import redis

r = redis.Redis(host="localhost", port=6739, decode_responses=True)
newkey = Fernet.generate_key()
f = Fernet(newkey)

print("{} is your encryption key. dont lose it!".format(f))


def encrypt(plainPassword, encryptKey):
    EncryptedPassword = encryptKey.encrypt(plainPassword)
    return EncryptedPassword


def decrypt(EncryptedPassword, decryptKey):
    DecryptedPassword = decryptKey.decrypt(EncryptedPassword)
    return DecryptedPassword


print("type 'exit' to finish program")
print("type 'encrypt password' to enter new data")
print("type 'decrypt password' to pull existing data")

while not input == "exit":
    if input == "encrypt password":
        userName = input("Please enter the user name: ")
        password = input("Please enter the password: ")
        source = input("Please enter the site/application: ")
        storedPassword = encrypt(password, f)

        r.hset(source, mapping={
            "uname": "{}".format(userName),
            "Password": "{}".format(storedPassword)
        })
        print("Data saved.")
    elif input == "decrypt password":
        source = input("Please enter the site/application: ")
        oldkey = input("Please enter the encryption key: ")
        enc_password = r.smembers(source)
        dec_password = decrypt(enc_password, oldkey)
        print(dec_password)

print("program closed")
