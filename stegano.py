from cryptography.fernet import Fernet
from PIL import Image
import os.path

def encode_image(img, msg):
    """
    use the red portion of an image (r, g, b) tuple to
    hide the msg string characters as ASCII values
    red value of the first pixel is used for length of string
    """
    length = len(msg)
    # limit length of message to 255
    if length > 255:
        print("text too long! (don't exeed 255 characters)")
        return False
    if img.mode != 'RGB':
        print("image mode needs to be RGB")
        return False
    # use a copy of image to hide the text in
    encoded = img.copy()
    width, height = img.size
    index = 0
    for row in range(height):
        for col in range(width):
            r, g, b = img.getpixel((col, row))
            # first value is length of msg
            if row == 0 and col == 0 and index < length:
                asc = length
            elif index <= length:
                c = msg[index -1]
                asc = ord(str(c))
            else:
                asc = r
            encoded.putpixel((col, row), (asc, g , b))
            index += 1
    return encoded

def decode_image(img):
    """
    check the red portion of an image (r, g, b) tuple for
    hidden message characters (ASCII values)
    """
    width, height = img.size
    msg = ""
    index = 0
    for row in range(height):
        for col in range(width):
            try:
                r, g, b = img.getpixel((col, row))
            except ValueError:
                # need to add transparency a for some .png files
                r, g, b, a = img.getpixel((col, row))		
            # first pixel r value is length of message
            if row == 0 and col == 0:
                length = r
            elif index <= length:
                msg += chr(r)
            index += 1
    return msg

def write_key():
    if os.path.exists("key.key"):
        print("key already exists")
        print("encrypting using existing key")
    else:
        key = Fernet.generate_key()
        with open("key.key", "wb") as key_file:
            key_file.write(key)
            print("new key generated! encrypting using new key")
            print("keep this key for future else you cannot decrypt ")

def load_key():
    return open("key.key", "rb").read()

def encrypt(filename, key):
    f = Fernet(key)
        # read all file data
    file_data = filename
    # encrypt data
    encrypted_data = f.encrypt(file_data.encode())
    with open("encoded.txt", "wb") as file:
        file.write(encrypted_data)

def decrypt(filename, key):
    global decrypted_data
    f = Fernet(key)
        # read the encrypted data
    encrypted_data = filename
    # decrypt data
    decrypted_data = f.decrypt(encrypted_data)
    return decrypted_data

def openfile(path):
    with open(path) as f:
        lines = f.read()
    return lines





banner= '''\033[92m

███████╗████████╗███████╗ ██████╗  █████╗ ███╗   ██╗ ██████╗
██╔════╝╚══██╔══╝██╔════╝██╔════╝ ██╔══██╗████╗  ██║██╔═══██╗
███████╗   ██║   █████╗  ██║  ███╗███████║██╔██╗ ██║██║   ██║
╚════██║   ██║   ██╔══╝  ██║   ██║██╔══██║██║╚██╗██║██║   ██║
███████║   ██║   ███████╗╚██████╔╝██║  ██║██║ ╚████║╚██████╔╝
╚══════╝   ╚═╝   ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝

        ▂▃▄▅▆▇▓▒░\033[91m CREATED BY MR.ETHICAL YT\033[92m ░▒▓▇▆▅▄▃▂
                    -------------------------

\033[95mlink: https://youtube.com/channel/UC9mBBFxkVWsTtLyuHUjvdbg\033[00m
'''
print(banner)
'''original_image_file = "Pic.png"

img = Image.open(original_image_file)
print(img, img.mode)  # test
write_key()
encoded_image_file = "enc_" + original_image_file

# don't exceed 255 characters in the message
secret_msg = "this is a secret message added to the image"
secret_file=encrypt("hello.txt",load_key())
print(secret_file)
with open("encoded.txt") as f:
    secret_msg=f.read()
img_encoded = encode_image(img,secret_msg)
if img_encoded:
    # save the image with the hidden text
    img_encoded.save(encoded_image_file)
    print("{} saved!".format(encoded_image_file))

    # get the hidden text back ...
    img2 = Image.open(encoded_image_file)
    hidden_text = decode_image(img2)
    decrypted_text=decrypt("encoded.txt",load_key())
    print(decrypted_text)
    with open('retrived.txt', 'wb') as file:
        file.write(decrypted_text)
    print("Hidden text:\n{}".format(decrypted_text))

'''
print("1.ENCODE TEXT INTO IMAGE\n2.DECODE TEXT FROM IMAGE\n")
try:
    input1=int(input("choose method :"))
    if input1 == 1:
        original_image_file=input("choose image : ")
        if os.path.exists(original_image_file):
            encoded_image_file = "enc_" + original_image_file
            text=input("enter text : ")
            print("Do you want to encrypt text")
            is_encrypt=input("y/n : ")
            if is_encrypt == "y":
                write_key()
                encrypt(text,load_key())
                encrypted_text=openfile("encoded.txt")
                img = Image.open(original_image_file)
                img_encoded = encode_image(img,encrypted_text)
                img_encoded.save(encoded_image_file)
                print("{} saved!".format(encoded_image_file))
                os.remove("encoded.txt")
            else:
                img = Image.open(original_image_file)
                img_encoded = encode_image(img,text)
                img_encoded.save(encoded_image_file)
                print("{} saved!".format(encoded_image_file))
        else :
            print("image was not found")
    elif input1==2:
        decoded_image_file=input("choose image : ")
        if os.path.exists(decoded_image_file):
            img2 = Image.open(decoded_image_file)
            hidden_text = decode_image(img2)
            print("is text encrypted : ")
            is_text_encrypted=input("y/n :")
            if is_text_encrypted == "y":
                hidden_text=bytes(hidden_text, 'utf-8')
                decrypted_text=decrypt(hidden_text,load_key())
                with open('retrived.txt', 'wb') as file:
                    file.write(decrypted_text)
                    print("{}saved!".format(file))
                print("Hidden text:\n{}".format(decrypted_text))
            elif is_text_encrypted == "n":
                hidden_text=bytes(hidden_text,'utf-8')
                with open('retrived.txt', 'wb') as file:
                    file.write(hidden_text)
                    print("retrived.txt saved!")
                print("Hidden text:\n{}".format(hidden_text)) 
except ValueError:
    print("not a valid input")
#encrypt("hello.txt",load_key())



