import argparse
import getpass

from crypto_utils import encrypt_file, decrypt_file


def main():
    parser = argparse.ArgumentParser(description="File Encryption Tool")

    parser.add_argument("mode", choices=["encrypt", "decrypt"])
    parser.add_argument("input_file")
    parser.add_argument("-o", "--output")

    args = parser.parse_args()

    password = getpass.getpass("Enter password: ")

    if args.mode == "encrypt":
        output_file = args.output or args.input_file + ".enc"
        encrypt_file(args.input_file, output_file, password)
        print(f"File encrypted successfully: {output_file}")

    elif args.mode == "decrypt":
        output_file = args.output or args.input_file.replace(".enc", "")
        decrypt_file(args.input_file, output_file, password)
        print(f"File decrypted successfully: {output_file}")


if __name__ == "__main__":
    main()