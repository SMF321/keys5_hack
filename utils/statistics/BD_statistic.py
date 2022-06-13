#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from PIL import Image
import time
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator, get_single_color_func

#Создание облака слов
def Cloud(id, a1):
    data2 = {'text': a1}
    start_time = time.time()
    print(data2)
    a1 = pd.DataFrame(data2)
    a3 = pd.DataFrame.to_string(a1)
    a0 = a3.upper()

    building = np.array(Image.open(
        'utils/statistics/photo_2022-06-12_03-34-18.jpg'))
    wordcloud = WordCloud(max_words=50000,

                          prefer_horizontal=.7,
                          colormap='Blues',
                          min_font_size=5,
                          max_font_size=70,
                          background_color="Black",
                          width=7680,
                          height=4320,
                          margin=2,
                          collocations=False,
                          mask=building,
                          repeat=False,
                          relative_scaling=0,
                          scale=1,
                          min_word_length=3,
                          include_numbers=False,
                          normalize_plurals=False,
                          font_step=1).generate(a0)

    print(wordcloud.layout_)
    print(' ')
    print("time elapsed: {:.2f}s".format(time.time() - start_time))

    plt.figure(figsize=(30, 30))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig(f'utils/statistics/{id}.png')
