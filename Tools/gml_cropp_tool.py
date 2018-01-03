from xml.etree import ElementTree as ET



class GmlCropper:
    def __init__(self, filepath):
        file_handler = open(filepath, 'rw')

        self.tree = self._parse_gml(file_handler)
        if self.tree is not None:
            self.parsed_flag = True
        else:
            self.parsed_flag = False
            print "Cannot parse file!!!"

    """Extracts Element Tree root for further processing"""
    def _parse_gml(self, filename):
        tree = ET.parse(filename)
        return tree

    """Iterates over document's children and erase those with unnesecary tags"""
    def remove_tags(self, tag_tails_list):
        tag_head = '{urn:gugik:specyfikacje:gmlas:panstwowyRejestrNazwGeograficznych:1.0}'

        if self.parsed_flag:
            for elem in self.tree.iter ():
                for child in list(elem):
                    for tag_tail in tag_tails_list:
                        if tag_tail in child.tag:
                            elem.remove(child)

    """Saves output file."""
    def save_cropped_gml(self, name):
        self.tree.write(open(name, 'w'), encoding='utf-8')


def main():
    original_file_path = "utils/miejscowosci.gml"
    output_path = "../utils/cropp_miejsc.gml"
    crop_inst = GmlCropper(original_file_path)

    remove_tag_list = ['waznyOd', 'cyklZycia', 'panstwo', 'zrodloInformacji', 'idTERYT', 'statusNazwy', ]

    crop_inst.remove_tags(remove_tag_list)
    crop_inst.save_cropped_gml(output_path)


if __name__ == "__main__":
    main()
