import argparse
import getpass
import os

from crypto_utils import encrypt_file, decrypt_file, get_decrypted_data


def main():
    parser = argparse.ArgumentParser(description="Dual Password File Encryption Tool")

    parser.add_argument(
        "mode",
        choices=["encrypt", "decrypt", "view"],
        help="Choose encrypt, decrypt, or view",
    )

    parser.add_argument(
        "input_file",
        help="Path of the input file",
    )

    args = parser.parse_args()

    access_password = getpass.getpass("Enter access password: ")
    encryption_password = getpass.getpass("Enter encryption password: ")

    try:
        if args.mode == "encrypt":
            output_file = args.input_file + ".enc"
            encrypt_file(args.input_file, output_file, access_password, encryption_password)
            print(f"File encrypted successfully: {output_file}")

        elif args.mode == "decrypt":
            if args.input_file.endswith(".enc"):
                output_file = args.input_file[:-4]
            else:
                output_file = args.input_file + ".decrypted"

            decrypt_file(args.input_file, output_file, access_password, encryption_password)
            print(f"File decrypted successfully: {output_file}")

        elif args.mode == "view":
            decrypted_data = get_decrypted_data(args.input_file, access_password, encryption_password)

            try:
                print("\nDecrypted File Content:\n")
                print(decrypted_data.decode())
            except UnicodeDecodeError:
                print("This file is not a readable text file. Please decrypt it instead.")

    except FileNotFoundError as error:
        print(f"Error: {error}")

    except ValueError as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()