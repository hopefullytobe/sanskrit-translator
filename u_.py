# -*- coding: utf-8 -*-

vowels = 'aAiIuUfFxXeEoOMH'
consonants = 'kKgGNcCjJYwWqQRtTdDnpPbBmyrlvSzsh'
other = ". |-\r\n\t"
virama = u'\u094d'

map_vowels = {'a':u'\u0905', 'A':u'\u0906', 'i':u'\u0907', 'I':u'\u0908', 'u':u'\u0909', \
              'U':u'\u090a', 'f':u'\u090b', 'F':u'\u0960', 'x':u'\u090c', 'X':u'\u0961', \
              'e':u'\u090f', 'E':u'\u0910', 'o':u'\u0913', 'O':u'\u0914', \
              'M':u'\u0902', 'H':u'\u0903'}
#x -> 0960?
map_vowel_signs = {'a':'', 'A':u'\u093e', 'i':u'\u093f', 'I':u'\u0940', 'u':u'\u0941', \
                   'U':u'\u0942', 'f':u'\u0943', 'F':u'\u0944', 'x':u'\u0902', 'X':u'\u0963', \
                   'e':u'\u0947', 'E':u'\u0948', 'o':u'\u094b', 'O':u'\u094c', \
                   'M':u'\u0902', 'H':u'\u0903', '_':u'\u094d'}

map_consonants = {'k':u'\u0915', 'K':u'\u0916', 'g':u'\u0917', 'G':u'\u0918', 'N':u'\u0919', \
                  'c':u'\u091a', 'C':u'\u091b', 'j':u'\u091c', 'J':u'\u091d', 'Y':u'\u091e', \
                  'w':u'\u091f', 'W':u'\u0920', 'q':u'\u0921', 'Q':u'\u0922', 'R':u'\u0923', \
                  't':u'\u0924', 'T':u'\u0925', 'd':u'\u0926', 'D':u'\u0927', 'n':u'\u0928', \
                  'p':u'\u092a', 'P':u'\u092b', 'b':u'\u092c', 'B':u'\u092d', 'm':u'\u092e', \
                  'y':u'\u092f', 'r':u'\u0930', 'l':u'\u0932', 'v':u'\u0935', 'S':u'\u0936', \
                  'z':u'\u0937', 's':u'\u0938', 'h':u'\u0939'}

def isVowel(ch):
    return ch in vowels
def isConsonant(ch):
    return ch in consonants
def atomize(source_text_slp1):
    index = 0
    text_length = len(source_text_slp1)
    array = []
    while index < text_length:
        ch = source_text_slp1[index]
        if (index+1) < text_length:
            ch1 = source_text_slp1[index+1]
        else:
            ch1 = ''
        if isVowel(ch):
            array.append(ch)
            index = index + 1
        elif isConsonant(ch) and isVowel(ch1):
            array.append(ch+ch1)
            index = index + 2
        else:
            array.append(ch)
            index = index + 1
    return array
def devanagari_l(src_txt_slp1):
    arr = atomize(src_txt_slp1)
    deva_str = []
    for ch in arr:
        if len(ch) == 1:
            if isVowel(ch):
                deva_str.append(map_vowels[ch])
            elif isConsonant(ch):
                deva_str.append(map_consonants[ch] + virama)
            else:
                deva_str.append(ch)
        else:
            deva_str.append(map_consonants[ch[0]]+map_vowel_signs[ch[1]])
    return "".join(deva_str)

