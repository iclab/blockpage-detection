#! /usr/bin/python
# -*- coding: utf-8 -*-

# global import
# from bs4 import BeautifulSoup
from BeautifulSoup import BeautifulSoup
import collections
from HTMLParser import HTMLParser
import math
import numpy as np
import sys
import traceback
import urllib2


class TagParser(HTMLParser):
    cnt = collections.Counter()    # counter of  html tag frequency
    attr_list = [u'color', u'width', u'height']    # listed of interested signature attributes

    def handle_starttag(self, tag, attributes):
        # extract attributes and their values into a single list if they appear in attr_list
        attr_with_value = [item for sub_list in
                           [list(attr) for attr in attributes if attr[0] in self.attr_list] for item in sub_list]
        # concatenate html tag, attribute, and value with underscores
        index = u'_'.join([tag] + attr_with_value)
        # increase combined 'new' tag counts by 1
        self.cnt[index] += 1

    def handle_endtag(self, tag):
        self.cnt[unicode(tag)] += 1

    def reset_counter(self):
        self.cnt.clear()

    def __str__(self):
        return str(self.cnt)


def get_term_frequency_vectors(content):
    tp = TagParser()
    tp.feed(content)
    return dict(tp.cnt)


def cosine_similarity(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[key] * vec2[key] for key in intersection])
    sum1 = sum([vec1[key]**2 for key in vec1.keys()])
    sum2 = sum([vec2[key]**2 for key in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator


def equal_weight(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    union = set(vec1.keys()) | set(vec2.keys())
    numerator = reduce(float.__add__,
                       [1.0 - abs(float(vec1[key]-vec2[key]) / (vec1[key]+vec2[key])) for key in intersection])
    denominator = len(union)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator


def length_ratio(page1, page2):
    small, large = sorted([len(page1), len(page2)])
    return float(small) / large


def dom_similarity(page1, page2):
    # return 1 if lab and field are identical
    if page1 == page2:
        return 1.0

    # return 0 if one of the page is empty
    if page1 is None or page2 is None:
        return 0.0

    # compute all parent-child couples
    tags = ['[document]']    # root tag for BeautifulSoup
    couples_lab = []
    couples_field = []
    dom1 = BeautifulSoup(page1)
    dom2 = BeautifulSoup(page2)
    for x in dom1.findAll():
        couples_lab.append((str(x.parent.name), str(x.name)))
        if str(x.name) not in tags:
            tags.append(str(x.name))
    for x in dom2.findAll():
        couples_field.append((str(x.parent.name), str(x.name)))
        if str(x.name) not in tags:
            tags.append(str(x.name))

    # compute DOM couples matrix
    matrix1 = np.zeros((len(tags), len(tags)))
    matrix2 = np.zeros((len(tags), len(tags)))
    for c in couples_lab:
        x = tags.index(c[0])
        y = tags.index(c[1])
        matrix1[x, y] += 1
    for c in couples_field:
        x = tags.index(c[0])
        y = tags.index(c[1])
        matrix2[x, y] += 1

    correlation = np.vdot(matrix1, matrix2)
    correlation /= np.linalg.norm(matrix1) * np.linalg.norm(matrix2)
    return abs(correlation)


def similarity_metrics(page1, page2):
    vec1 = get_term_frequency_vectors(page1)
    vec2 = get_term_frequency_vectors(page2)

    results = {
        'cosine similarity': cosine_similarity(vec1, vec2),
        'equal weight': equal_weight(vec1, vec2),
        'length ratio': length_ratio(page1, page2),
        'dom similarity': dom_similarity(page1, page2)
    }
    return results


def get_file_content(filename):
    """Read in the contents of the file or download the site if appropriate"""
    if "http://" in filename:
        try:
            return urllib2.urlopen(filename).read()
        except urllib2.URLError as exp:
            print "Error: cannot open %s" % filename
            raise exp
    else:
        try:
            with open(filename, 'r') as file_p:
                return file_p.read()
        except IOError:
            print "Error: cannot open %s" % filename
            raise exp

def compare_files(file1, file2):
    try:
        page1 = get_file_content(file1)
        page2 = get_file_content(file2)
    except Exception:
        traceback.print_exc()
        sys.exit(1)
    return similarity_metrics(page1, page2)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "Usage: % python <FILENAME1> <FILENAME2>"
    else:
        print compare_files(sys.argv[1], sys.argv[2])
