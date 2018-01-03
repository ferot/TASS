import unidecode
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
    def get_upper_case_name(self, content):
        for post in self.split_post(content):
            print "\n"
            decoded_post =  unidecode.unidecode(post.decode('utf-8'))
            split_words = decoded_post.split(" ")
            for word in split_words:
                if len(word) > 1 and word[0].isupper():
                        print unidecode.unidecode(word)

