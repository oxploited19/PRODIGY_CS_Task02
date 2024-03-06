from PIL import Image
import numpy as np
import os
import time
import subprocess

try:
    from tqdm import tqdm
    from colorama import Fore, Style
except ImportError:
    print("Required libraries not found. Installing...")
    subprocess.run(['pip', 'install', 'tqdm', 'colorama'])
    print("Libraries installed successfully. You can now run the script.")
    exit()

def get_username():
    return os.getenv('USER') or os.getenv('USERNAME')

def get_function_from_user():
    while True:
        choice = input("Do you want to (e)ncrypt or (d)ecrypt an image? ").lower()
        if choice in ['e', 'd']:
            return choice
        else:
            print("Invalid choice. Please enter 'e' for encrypt or 'd' for decrypt.")

def get_image_path_from_user():
    while True:
        path = input(f"{get_username()}, enter the path of the image: ")
        if os.path.isfile(path):
            return path
        else:
            print("Invalid path. Please enter a valid file path.")

def get_output_path_from_user(default_path):
    while True:
        choice = input(f"Do you want to save the result in the same location as the original image? (y/n): ").lower()
        
        if choice == 'y':
            return default_path
        elif choice == 'n':
            path = input("Enter the path where you want to save the result: ")
            if os.path.isdir(path):
                return path
            else:
                print("Invalid path. Please enter a valid directory path.")
        else:
            print("Invalid choice. Please enter 'y' for yes or 'n' for no.")

def get_key_from_user():
    while True:
        try:
            return int(input("Enter the encryption/decryption key: "))
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

def simulate_process(process_name):
    # ASCII art banners
    encrypt_banner = r"""
 __    __ _ \ / _ ______    __
|_ |\|/  |_) Y |_) |  | |\|/__
|__| |\__| \ | |   | _|_| |\_|

                                       
    """
    decrypt_banner = r"""

 _  __ __ _ \ / _ ______    __
| \|_ /  |_) Y |_) |  | |\|/__
|_/|__\__| \ | |   | _|_| |\_|

                                  
    """
    if process_name == "Encrypting":
        print(Fore.CYAN + encrypt_banner + Style.RESET_ALL)
    elif process_name == "Decrypting":
        print(Fore.MAGENTA + decrypt_banner + Style.RESET_ALL)
    print(f"\n{process_name}")

    for _ in tqdm(range(5), desc="Progress", unit="s", dynamic_ncols=True, colour='GREEN'):
        time.sleep(1)

def encrypt_image(image, key):
    simulate_process("Encrypting")

    img_array = np.array(image)
    np.random.seed(key)
    permutation = np.random.permutation(img_array.size)
    encrypted_array = img_array.flatten()[permutation].reshape(img_array.shape)

    encrypted_image = Image.fromarray(encrypted_array.astype('uint8'))

    print("\nEncryption complete.")
    return encrypted_image

def decrypt_image(image, key):
    simulate_process("Decrypting")

    img_array = np.array(image)
    np.random.seed(key)
    inv_permutation = np.argsort(np.random.permutation(img_array.size))
    decrypted_array = img_array.flatten()[inv_permutation].reshape(img_array.shape)

    decrypted_image = Image.fromarray(decrypted_array.astype('uint8'))

    print("\nDecryption complete.")
    return decrypted_image

def save_image(image, output_path, file_name):
    file_path = os.path.join(output_path, file_name)

    count = 1
    while os.path.exists(file_path):
        count += 1
        file_name = f"{os.path.splitext(file_name)[0]}_{count}.jpg"
        file_path = os.path.join(output_path, file_name)

    try:
        image.save(file_path)
        print(f"Result saved as '{file_name}'.")
        print(f"File saved at: {file_path}")
    except Exception as e:
        print(f"Error saving the result: {e}")

function_choice = get_function_from_user()
input_image_path = get_image_path_from_user()
original_image = Image.open(input_image_path)
output_path = get_output_path_from_user(os.path.dirname(input_image_path))

if function_choice == 'e':
    key = get_key_from_user()
    result_image = encrypt_image(original_image, key)
    save_image(result_image, output_path, "Encrypted_file.jpg")
else:
    key = get_key_from_user()
    result_image = decrypt_image(original_image, key)
    save_image(result_image, output_path, "Decrypted_file.jpg")

print("\nThank you for using my script Oxploited19")
