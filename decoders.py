# -*- coding: utf-8 -*-

#the program encodes text between slp1, hk, wx and itrans formats

##Usage Guidelines: 
##1) Copy the module to your
##    working directory 
##2) import Transcode 
##3) use the methods as per your need 
##
##example: if you have your source byte stream
##              in HK transliteration format, you can
##              encode it to slp1 by the command
##              'Transcode.slp1('hk', stream), which returns
##              the encoded slp1 stream of data

#import the pickle module for loading the encoding map files
import pickle
import t_map

#implementation does not notify source encoding errors

def slp1(src_format, source_text):
    #load the mappings file for slp1 and the source format
    if src_format == 'hk':
        maplist = t_map.hk_map 
    elif src_format == 'wx':
        maplist = t_map.wx_map
    elif src_format == 'itrans':
        maplist = t_map.itrans_map
    else:
        return ''
    index = 0
    #encode the source text to an intermediate format
    for slp1, src_fmt in maplist:
        source_text = source_text.replace(src_fmt, ('#' + str(index) + '#'))
        index = index + 1
    index = 0
    #decode the SLP1 format from the encoded intermediate format
    for slp1, src_fmt in maplist:
        source_text = source_text.replace(('#' + str(index) + '#'), slp1)
        index = index + 1
    return source_text

def hk(src_format, source_txt):
    #convert the source to SLP1 format
    if src_format != 'slp1':
        source_txt = slp1(src_format, source_txt)
    #load the HK SLP1 mapping
    maplist = t_map.hk_map
    index = 0
    #encode the source text to an intermediate format
    for slp1_v, src_fmt in maplist:
        source_txt = source_txt.replace(slp1_v, ('#' + str(index) + '#'))
        index = index + 1
    index = 0
    #decode the SLP1 format from the encoded intermediate format
    for slp1_v, src_fmt in maplist:
        source_txt = source_txt.replace(('#' + str(index) + '#'), src_fmt)
        index = index + 1
    return source_txt

def wx(src_format, source_txt):
    #convert the source to SLP1 format
    if src_format != 'slp1':
        source_txt = slp1(src_format, source_txt)
    #load SLP1 WX format
    maplist = t_map.wx_map
    index = 0
    #encode the source text to an intermediate format
    for slp1_v, src_fmt in maplist:
        source_txt = source_txt.replace(slp1_v, ('#' + str(index) + '#'))
        index = index + 1
    index = 0
    #decode the SLP1 format from the encoded intermediate format
    for slp1_v, src_fmt in maplist:
        source_txt = source_txt.replace(('#' + str(index) + '#'), src_fmt)
        index = index + 1
    return source_txt

def itrans(src_format, source_txt):
    #convert the source to SLP1 format
    if src_format != 'slp1':
        source_txt = slp1(src_format, source_txt)
    #load SLP1 ITRANS mapping
    maplist = t_map.itrans_map
    index = 0
    #encode the source text to an intermediate format
    for slp1_v, src_fmt in maplist:
        source_txt = source_txt.replace(slp1_v, ('#' + str(index) + '#'))
        index = index + 1
    index = 0
    #decode the SLP1 format from the encoded intermediate format
    for slp1_v, src_fmt in maplist:
        source_txt = source_txt.replace(('#' + str(index) + '#'), src_fmt)
        index = index + 1
    return source_txt

def devanagari(src_format, source_txt):
    #convert the source to SLP1 format
    if src_format != 'slp1':
        source_txt = slp1(src_format, source_txt)
    from u_ import devanagari_l
    return devanagari_l(source_txt)
