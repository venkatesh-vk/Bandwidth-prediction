def crc_remainder(message, polynomial):
    message = message + '0' * (len(polynomial) - 1)  # Pad message with zeros
    crc = '0' * (len(polynomial) - 1)  # Initialize CRC with zeros

    for i in range(len(message) - len(polynomial) + 1):
        if crc[0] == '1':
            crc = xor(crc, polynomial)
        crc = crc[1:] + message[i]

    return crc

def xor(a, b):
    result = ''
    for i in range(len(a)):
        result += str(int(a[i]) ^ int(b[i]))
    return result

def main():
    message = input("Enter the message (binary): ")
    polynomial = input("Enter the polynomial (binary): ")
    crc = crc_remainder(message, polynomial)
    print("CRC:", crc)

if __name__ == "__main__":
    main()
