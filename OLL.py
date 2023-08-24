import keyboard
import clipboard
import time
import xml.etree.ElementTree as ET

def save_clipboard_to_file():
    clipboard_text = clipboard.paste()
    current_time = time.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"clipboard.txt"
    with open(filename, 'w') as f:
        f.write(clipboard_text)
    print(f"Clipboard content saved to {filename}")

def process_file(filename):
    with open(filename, 'r+') as file:
        lines = file.readlines()
        file.seek(0)
        new_lines = []

        for line in lines:
            stripped_line = line.strip()
            if stripped_line:
                parts = stripped_line.split('\t')
                dimensions = parts[0].replace('x', ' ')
                first_value = int(dimensions.split()[0]) + 2
                second_value = int(dimensions.split()[1]) + 2
                new_line = f"{first_value} {second_value} {parts[2]} {parts[1]}\n"
                new_lines.append(new_line)

        file.writelines(new_lines)
        file.truncate()

def create_xml_file():
    data = ET.Element("data")
    parts = ET.SubElement(data, "parts")

    with open("clipboard.txt", "r") as file:
        for line in file:
            values = line.strip().split()
            if len(values) == 4:
                length, width, quantity, label = values
                row_data = {
                    "length": length,
                    "width": width,
                    "quantity": quantity,
                    "label": label,
                    "allow_rotation": "1"
                }
                row = ET.SubElement(parts, "row")
                for key, value in row_data.items():
                    element = ET.SubElement(row, key)
                    element.text = value

    xml_tree = ET.ElementTree(data)
    xml_tree.write("output.xml", encoding="utf-8", xml_declaration=True)
    print("XML data saved to output.xml")

def main():
    while True:
        keyboard.wait('ctrl+v')
        save_clipboard_to_file()
        print("Clipboard content saved to clipboard.txt")

        try:
            process_file('clipboard.txt')
            print("Operations performed and saved in the source file after removing empty lines and making changes.")

            create_xml_file()
            print("XML data saved to output.xml\n")
        except Exception as e:
            print(f"An error occurred: {e}\n")

if __name__ == "__main__":
    main()
