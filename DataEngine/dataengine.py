import codecs
import re
import unidecode
from xml.etree import ElementTree as ET
import Common
from optparse import BadOptionError

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
        post_words_list = []

        for post in self.split_post(content):
            words_in_post = []
            post = self.decode_content(post)
            filtered_post = self.filter_post(post)

            split_words = filtered_post.split(" ")
            aggregated_name = []
            for word in split_words:
                if len(word) > 1 and word[0].isupper():
                    aggregated_name.append(word)
                else:
                    if aggregated_name:
                        # merge words into final within space
                        final_name = ' '.join(aggregated_name)
                        words_in_post.append(unidecode.unidecode(final_name))
                        aggregated_name = []
                        #print final_name

            post_words_list.append(words_in_post)
        return post_words_list

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

    """convert string contain degree minutes and seconds to one float number"""
    def _convert_geo_coordinates(self, h, l):
        h_converted = int(h[0:2]) + (float(h[5:7]) / 60) + (float(h[8:10])/3600)
        l_converted = int(l[0:2]) + (float(l[5:7]) / 60) + (float(l[8:10])/3600)
        return (l_converted, h_converted)

    """TODO rozwinac dla nazw dwoczlonowych """
    def _create_dopelniacz(self, mianownik, suffix):
        dopelniacz = ''

        if suffix == None:
            return ''

        if suffix[0] != '-':
            return suffix

        for i in range(len(mianownik)):
            if mianownik[-1 - i] == suffix[1]:
                dopelniacz = mianownik[0 : - i] + suffix[2:]

        return dopelniacz
    
    """ find closest places, coord_list contain route with all
         possibility of repeated name of places """
    def _find_best_coords(self, coord_list):

        # check if cord list is no empty
        if len(coord_list) == 0:
            return []

        # This list contain list of next closest places, started by
        # all possibility of 1st place 
        best_posiblitesFor1stelem = []

        # iterate on all possibility of 1st places in route 
        for firstElemList in coord_list[0]:
            #this list contain best places started by one of first place
            best_list = []
            best_list.append(firstElemList)
            # iterate on rest of places to find closest
            for i in range (1, len(coord_list)):
                # omit empty lists
                if len(coord_list[i]) == 0:
                    continue

                best_list.append(coord_list[i][0])
                #iterate on cords of repeated names
                #to find closest place to the previous
                for e in coord_list[i]:
                    #check if next element is better than previous
                    if ((abs(e[0]-best_list[-2][0])+abs(e[1]-best_list[-2][1])) <
                        (abs(best_list[-1][0]-best_list[-2][0]) + 
                         abs(best_list[-1][1] -best_list[-2][1]))):

                        best_list[-1]=e;

            best_posiblitesFor1stelem.append(best_list)


        # Find best route for all possibility of 1st place
        tmp_sum_diff = 1000000
        best_route = []    
        for list in best_posiblitesFor1stelem:
            sum=0
            for i in range(0, len(list)-1):
                sum+=abs(list[i][0]+list[i][1]-list[i+1][0]-list[i+1][1])

            if sum < tmp_sum_diff:
                tmp_sum_diff = sum
                best_route = list


        return best_route
    """Iterates over PRNG elements and checks if they contain name desired to find. 
    Returns list of coords associated with that name"""

    def build_track_list(self, elements, names_to_find):
        # TODO : all those generic tags generated by csv-xml converter should be renamed into more readable
        main_name_tag = "FIELD1"
        dopelniacz_tag = "FIELD4"
        coord1_tag = "FIELD8"
        coord2_tag = "FIELD9"


        coord_list = []
        #iterate over names in one post
        for name in names_to_find:
        #iterate over elements returned
            coords_repated_names = []
            for elem in elements:
                for child in elem:

                    if main_name_tag in child.tag: # 1st stage : we check if name matches
                        found = False
                        mianownik = child.text
                        if name == child.text: # very primitive check if just name consists name_to_find
                            # TODO: extend it!
                            #print "FOUND: " + name
                            found = True
                        else:
                            found = False
                            continue
                    #if not find in basic form try in dopelniacz
                    if (not found) and (dopelniacz_tag in child.tag):
                        if name == self._create_dopelniacz(mianownik, child.text):
                            # TODO: extend it!
                            found = True
                        else:
                            found = False
                            continue

                    if found: # 2nd stage : found main name. let's extract coords
                        if coord1_tag in child.tag: # check if current tag is that related to coords
                            #print "coords_1 : " + child.text
                            coord1 = child.text
                        if coord2_tag in child.tag:
                            #print "coords_2 : " + child.text
                            coord2 = child.text
                            coord_coverted = self._convert_geo_coordinates(
                                                                coord1, coord2)
                            coords_repated_names.append(coord_coverted)

            # if do not find any place with given name omit this                
            if len(coords_repated_names) > 0:
                coord_list.append(coords_repated_names)


        return self._find_best_coords(coord_list)
