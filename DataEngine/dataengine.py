import codecs
import re
import unidecode
from xml.etree import ElementTree as ET
import Common

"""Parser for posts content. Component responsible for extracting desired elements such as cities,
name of geographical lands, etc"""


class DataEngine:
    def __init__(self):
        pass

    """Reads file's chunk's content by provided filename and returns it as string (without decoding)."""
    def read_content(self, filename):
        file_handler = open("./" + filename, 'r')
        content = file_handler.read()
        return content

    """Splits chunk into posts list"""
    def split_post(self, chunk):
        posts_list = chunk.split(Common.post_splitter)
        return posts_list

    """Extracts lists of single words begginning with upper-case"""
    def get_upper_case_names(self, content):
        word_list = []
        for post in self.split_post(content):

            post = self.decode_content(post)
            filtered_post = self.filter_post(post)

            split_words = filtered_post.split(" ")
            for word in split_words:
                if len(word) > 1 and word[0].isupper():
                        word_list.append(unidecode.unidecode(word))
        return word_list

    """Decodes post content into utf-8 standard"""
    def decode_content(self, content):
        decoded_post = unidecode.unidecode(content.decode('utf-8'))
        return decoded_post

    """Filter post from unwanted characters"""
    def filter_post(self, post):
        restricted_symbols = '[!@#$.,?()*:;"]'  # special symbols to be omitted
        post = re.sub (restricted_symbols, '', post)

        return post

    """Extracts root of PRNG reference file.
    By default it expects XML file, but GML are still compatible."""
    def open_prng(self, filename):
        with open(filename, 'r') as f:
            tree = ET.parse(f)

        return tree

    """Iterates over PRNG elements and checks if they contain name desired to find. 
    Returns list of coords associated with that name"""

    def build_track_list(self, elements, name_to_find):
        # TODO : all those generic tags generated by csv-xml converter should be renamed into more readable
        main_name_tag = "FIELD1"
        coord1_tag = "FIELD8"
        coord2_tag = "FIELD9"

        coord_list = []
        #iterate over elements returned
        for elem in elements:
            for child in elem:
                if main_name_tag in child.tag: # 1st stage : we check if name matches
                    found = False
                    if name_to_find in child.text: # very primitive check if just name consists name_to_find
                                                   # TODO: extend it!
                        print "FOUND: " + name_to_find
                        found = True
                    else:
                        found = False
                        continue
                if found: # 2nd stage : found main name. let's extract coords
                    if coord1_tag in child.tag: # check if current tag is that related to coords
                        print "coords_1 : " + child.text
                        coord1 = child.text
                    if coord2_tag in child.tag:
                        print "coords_2 : " + child.text
                        coord2 = child.text
                        coord_list.append((coord1, coord2))

        return coord_list