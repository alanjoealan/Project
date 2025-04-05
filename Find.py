from PIL import Image
import sys

#binary to int converting
def bin_to_int(b):
    return int(b, 2)

def decode_image(hidden_image_path, output_file_path):

    #loads image to get pixel data
    image = Image.open(hidden_image_path)
    pixels = list(image.getdata())

    #extract the hidden bits
    bits = ''
    for r, g, b in pixels:
        bits += str(b & 1)

    #first 32 bits = size of hidden file
    size_bits = bits[:32]
    data_size = bin_to_int(size_bits)

    #extract the data bits
    data_bits = bits[32:32 + data_size * 8]

    #convert the bits to bytes
    data = bytearray()
    for i in range(0, len(data_bits), 8):
        byte = data_bits[i:i+8]
        data.append(bin_to_int(byte))

    with open(output_file_path, 'wb') as f:
        f.write(data)

    print(f"Data extracted to {output_file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage:python find.py <hidden_image> <output_file>")
    else:
        decode_image(sys.argv[1], sys.argv[2])
