import unidecode
from xml.etree import ElementTree as ET


class XMLDecoder:
    def __init__(self, filename):
        with open(filename, 'r') as f:
            self.root = ET.parse(f)

    def decode(self):
        found_tags = self.root.findall("row")
        for tag in found_tags:
            for child in tag:
                if child.text:
                    child.text = unidecode.unidecode(child.text)
                    print child.text

    def save_file(self, name):
        self.root.write(open (name, 'w'))


def main():
    original_file_path = "../utils/miejscowosci.xml"
    output_path = "../utils/decoded_miejsc.xml"

    decoder = XMLDecoder(original_file_path)
    decoder.decode()
    decoder.save_file(output_path)


if __name__ == "__main__":
    main()
