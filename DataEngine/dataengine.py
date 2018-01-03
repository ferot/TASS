import codecs
import re
import unidecode
from xml.etree import ElementTree as ET
import Common

"""Parser for posts content. Component responsible for extracting desired elements such as cities,
name of geographical lands, etc"""


class DataEngine:
    def __init__(self, filename):
        self.file_handler = open("./" + filename, 'r')

    """Reads file's content and returns it as string (without decoding)"""
    def read_content(self):
        content = self.file_handler.read()
        return content

    """Splits chunk into posts list"""
    def split_post(self, chunk):
        posts_list = chunk.split(Common.post_splitter)
        return posts_list

    """Extracts lists of single words begginning with upper-case"""
    def get_upper_case_names(self, content):
        word_list = []
        for post in self.split_post(content):
            print "\n"

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

    """Extracts root of gml file"""
    def open_gml(self, filename):
        with open(filename, 'r') as f:
            tree = ET.parse(f)

        return tree
