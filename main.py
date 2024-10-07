from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os



# Define your global constants here
INPUT_IMAGE_PATH = r"data\new3\adjusted_eye_131x87_12col.png"
OUT_FOLDER = r"out"
OUTPUT_IMAGE_PATH = r"out\converted"
OUTPUT_COLORS_PDF = r"out\colors.pdf"

def create_out_folder_if_not_exists():
    if not os.path.exists(OUT_FOLDER):
        os.makedirs(OUT_FOLDER)   

def number_to_letter(number):
    # Check if the number is within the range of 1 to 26
    if 0 <= number <= 25:
        # Convert the number to a letter
        return chr(number + 97)
    else:
        # Return an error message or handle the case where the number is out of range
        return "Number out of range"

def reduce_colors_and_resize(num_colors=20, new_width=120, new_height=120):
    # Open an existing image from the hardcoded path
    image = Image.open(INPUT_IMAGE_PATH)
    
     # Resize the image using the LANCZOS resampling method
    image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Convert the image to P mode which is a format for storing palettes
    image = image.convert('P', palette=Image.ADAPTIVE, colors=num_colors)
    
    # Save the image to the hardcoded path
    image.save(OUTPUT_IMAGE_PATH + '_w' + str(new_width) + '_h' + str(new_height) + '_col' + str(num_colors) + '.png')
    return image

def count_unique_colors(image):
    # Ensure the image is in RGB mode to get three components of the color
    image = image.convert('RGB')
    
    # Get data of the image
    image_data = image.getdata()
    
    # Using a set to store unique colors
    unique_colors = set(image_data)
    
    # Returning the number of unique colors
    return len(unique_colors)

def print_color_indices(image):
    # Create a dictionary to map index to RGB values
    palette = image.getpalette()
    index_to_color = {i // 3: tuple(palette[i:i+3]) for i in range(0, len(palette), 3)}
    
    for y in range(image.height):
        print("{:2}".format(y + 1), end = ') ')

        # Variables to keep track of the current and previous colors and their counts
        previous_color = None
        color_sequence = []
        count = 0

        for x in range(image.width):
            index = image.getpixel((x, y))
            color_letter = number_to_letter(index)
            print(color_letter, end='')

            # Check if the color is different from the previous color
            if color_letter != previous_color and previous_color is not None:
                # Append the count and previous color to the sequence
                color_sequence.append(f"{previous_color}({count})")
                count = 1  # Reset count for the new color
            else:
                count += 1  # Increment count for the same color

            previous_color = color_letter

        # Append the last color and its count
        color_sequence.append(f"{previous_color}({count})")

        print()  # Newline after printing all colors in the row

        # Print the color sequence summary for the line
        #print(' '.join(color_sequence))

    
    

    # Print the index to RGB mapping
    print("\nIndex to RGB Mapping:")
    for index, rgb in index_to_color.items():
        print(f"{index} = RGB{rgb}")

    output_rgb_mapping_to_pdf(index_to_color)

def output_rgb_mapping_to_pdf(index_to_color, filename=OUTPUT_COLORS_PDF):
    c = canvas.Canvas(filename, pagesize=letter)
    y_position = 750

    c.drawString(100, y_position, "Index to RGB Mapping:")
    y_position -= 20

    for index, rgb in index_to_color.items():
        # Normalize RGB values to the range [0, 1] for ReportLab
        normalized_rgb = tuple(val / 255 for val in rgb)

        # Set the fill color and draw a square
        c.setFillColorRGB(*normalized_rgb)
        # Draw the text
        c.drawString(100, y_position, f"{number_to_letter(index)} = RGB{rgb}")
        c.rect(300, y_position - 2, 20, 20, fill=1)

        y_position -= 30
        if y_position < 100:
            c.showPage()
            y_position = 750

    c.save()

create_out_folder_if_not_exists()
reduced_and_resized_image = reduce_colors_and_resize(12, 131, 87)
#print(count_unique_colors(reduced_and_resized_image))
print_color_indices(reduced_and_resized_image)
