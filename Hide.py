from PIL import Image
import sys
import os  #to check the size of the image file (larger than 1MB for testing)

#convert int to binary string
def int_to_bin(value, bits=8):
    return format(value, f'0{bits}b')

def encode_image(cover_image_path, file_to_hide_path, output_image_path):
    #check if the image size is larger than 1MB
    image_size = os.path.getsize(cover_image_path)  #get image size in bytes
    if image_size > 1 * 1024 * 1024:  #1MB = 1 * 1024 * 1024 bytes
        print("Error: The image is too large (greater than 1MB).")
        return

    #make sure that image is in RGB mode
    image = Image.open(cover_image_path)
    if image.mode != 'RGB':
        image = image.convert('RGB')
    pixels = list(image.getdata())

    #read the file to hide in binary (hidden message file)
    with open(file_to_hide_path, 'rb') as f:
        data = f.read()

    #convert the data to bits
    data_size = len(data)
    size_bits = int_to_bin(data_size, 32)  #32-bit header
    data_bits = ''.join(int_to_bin(byte) for byte in data)
    full_data = size_bits + data_bits  #full bitstream to hide

    new_pixels = []
    data_index = 0

    #embedding the data
    for i, (r, g, b) in enumerate(pixels):
        if data_index < len(full_data):
            b = (b & ~1) | int(full_data[data_index])  #modifying the blue channel LSB
            data_index += 1
        new_pixels.append((r, g, b))

    image.putdata(new_pixels)
    image.save(output_image_path)
    print(f"Data encoded into {output_image_path}")

#argument layout
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python hide.py <cover_image> <file_to_hide> <output_image>")
    else:
        encode_image(sys.argv[1], sys.argv[2], sys.argv[3])

