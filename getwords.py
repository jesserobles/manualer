#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 18:11:10 2018

@author: jesse
"""

from bs4 import BeautifulSoup
import numpy as np
import pandas as pd


def get_coords(word, scale=0.2):
    bbox = word['title'].replace('bbox', '').strip().split(';')[0]
    coords = [int(i) for i in bbox.split()]
    coords = [int(i * scale) for i in coords]
    return coords


def get_height_width(coords, scale=0.2):
    x = coords[::2]
    y = coords[1::2]
    dx = x[-1] - x[0]
    dy = y[-1] - y[0]
    return (dx, dy)
    

def build_string(word, scale=0.2):
    div_fmt = ('<div class="word" style="position: absolute; left: {}px; top:'
               ' {}px; height: {}px; width: {}px; margin: 0px; '
               'padding: 0px;">{}</div>')
    coords = get_coords(word, scale=scale)
    width, height = get_height_width(coords, scale=scale)
    div = div_fmt.format(*coords[:2], height, width, word.get_text())
    return div


def get_distance(word1, word2, scale=0.2):
    x_coords_1 = get_coords(word1, scale=scale)[::2]
    x_coords_2 = get_coords(word2, scale=scale)[::2]
    return x_coords_2[0] - x_coords_1[1]
    

with open('test.hocr') as file:
    html = file.read()

word_class = 'ocrx_word'
line_class = 'ocr_line'

soup = BeautifulSoup(html, 'lxml')
words = soup.find_all('span', attrs={'class': word_class})
words = [w for w in words if w.get_text().strip()]
div_string = ''

for word in words:
    div_string += build_string(word) + '\n'

with open('div.txt', 'w') as file:
    file.write(div_string)

lines = soup.find_all('span', attrs={'class': line_class})

div_fmt = ('<div class="word" style="position: absolute; left: {}px; top:'
           ' {}px; height: {}px; width: {}px; margin: 0px; '
           'padding: 0px; font-size: 14px;">{}</div>')
ratio = 1.8
scale = 0.2
sentences = None
errs = []

text = '' # Initialize variable to hold all text
all_sentences = []
line = lines[0]
all_heights = []

for line in lines:
    x_start, y_start = get_coords(line, scale=scale)[:2]
    
    sentence_height = get_height_width(get_coords(line, scale=scale), scale=scale)[-1]
    all_heights.append(sentence_height)
    dist_thresh = int(sentence_height // ratio)
    
    words = line.findAll('span', attrs={'class': word_class})
    
    sentence = [] # Current sentence
    line_sentences = [] # All sentences in line
    for ix, word in enumerate(words):
        text = word.text
        if not word.text.strip():
            continue
        c = get_coords(word) # x1, y2, x2, y2
        if ix == len(words) - 1:
            sentence.append(text)
            sentence = ' '.join(sentence).strip()
            sentence_width = c[2] - x_start
            div = div_fmt.format(x_start, y_start, 
                                 sentence_height, sentence_width, 
                                 sentence)
            line_sentences.append(div)
            break
        
        dist_to_next = get_distance(word, words[ix + 1])
        if dist_to_next <= dist_thresh:
            sentence.append(text)
        else:
            sentence.append(text)
            sentence = ' '.join(sentence).strip()
            sentence_width = c[2] - x_start
            div = div_fmt.format(x_start, y_start, 
                                 sentence_height, sentence_width, 
                                 sentence)
            line_sentences.append(div)
            sentence = []
            x_start = get_coords(words[ix + 1])[0]
    all_sentences.extend(line_sentences)

all_sentences = '\n      '.join(all_sentences)

html_fmt = """<!DOCTYPE html>
<html>
  <head>
    <title>Test App</title>
    <link rel="stylesheet" href="css/style.css" type="text/css" media="screen"/>
  </head>
  <body>
    <div class="ler_image">
      {}
    </div>
  </body>
</html>"""

html = html_fmt.format(all_sentences)

with open('index.html', 'w') as file:
    file.write(html)
