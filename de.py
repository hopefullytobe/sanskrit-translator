#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Devanagari Editor

import pygtk, pango
pygtk.require('2.0')
import gtk
from Transcode.decoders import devanagari

help_string = '''
अ	आ	इ	ई	उ	ऊ	ऋ	ॠ	ऌ	ॡ	ए	ऐ	ओ	औ	अं	अः
a	A	i	I	u	U	R	RR	lR	lRR	e	ai	o	au	M	H

क	ख	ग	घ	ङ	|	य	र	ल	व
k	kh	g	gh	G	|	y	r	l	v
च	छ	ज	झ	ञ	|	श	ष	स	ह
c	ch	j	jh	J	|	z	S	s	h
ट	ठ	ड	ढ	ण	|	
T	Th	D	Dh	N	|	०	१	२	३	४	५	६	७	८	९
त	थ	द	ध	न	|	0	1	2	3	4	5	6	7	8	9
t	th	d	dh	n	|
प	फ	ब	भ	म	|
p	ph	b	bh	m	|
'''

class DevanagariTextEditor:
    
    def close_application(self, widget):
        gtk.main_quit()

    def key_pressed(self, widget, event):
        # F5
        if event.keyval == 65474:
            start, end = self.textbuffer_src.get_bounds()
            hk_string = self.textbuffer_src.get_text(start, end)
            devanagari_string = devanagari("hk", hk_string)
            self.textbuffer.set_text(devanagari_string)
            self.textview.set_buffer(self.textbuffer)
        # F1 to display transliteration help
        elif event.keyval == 65470:
            self.textbuffer.set_text(help_string)
            self.textview.set_buffer(self.textbuffer)
        # F2 to save the source file
        elif event.keyval == 65471:
            self.save_src_file()
        # F3 to save the destination file
        elif event.keyval == 65472:
            self.save_devanagari_file()            
        # CTRL + s
        elif event.keyval == 115:
            if event.state & gtk.gdk.CONTROL_MASK:
                self.save_src_file()

    def save_src_file(self):
        start, end = self.textbuffer_src.get_bounds()
        string_src = self.textbuffer_src.get_text(start, end)
        filechooserdialog = gtk.FileChooserDialog("Save Source File",
                                                  None, gtk.FILE_CHOOSER_ACTION_SAVE,
                                                  (gtk.STOCK_CANCEL,
                                                   gtk.RESPONSE_CANCEL,
                                                   gtk.STOCK_OK, gtk.RESPONSE_OK))
        response = filechooserdialog.run()
        if response == gtk.RESPONSE_OK:
            filename = filechooserdialog.get_filename()
            FILE = open(filename, 'w')
            FILE.write(string_src)
            FILE.close()    
        filechooserdialog.destroy()

    def save_devanagari_file(self):
        start, end = self.textbuffer.get_bounds()
        string = self.textbuffer.get_text(start, end)
        filechooserdialog = gtk.FileChooserDialog("Save Destination File",
                                                  None, gtk.FILE_CHOOSER_ACTION_SAVE,
                                                  (gtk.STOCK_CANCEL,
                                                   gtk.RESPONSE_CANCEL,
                                                   gtk.STOCK_OK, gtk.RESPONSE_OK))
        filechooserdialog.set_filename(".rtf")
        response = filechooserdialog.run()
        if response == gtk.RESPONSE_OK:
            filename = filechooserdialog.get_filename()
            FILE = open(filename, 'w')
            FILE.write(string)
            FILE.close()            
        filechooserdialog.destroy()

            
    def transcode_the_text(self, widget):
        start, end = self.textbuffer_src.get_bounds()
        hk_string = self.textbuffer_src.get_text(start, end)
        devanagari_string = devanagari("hk", hk_string)
        self.textbuffer.set_text(devanagari_string)
        self.textview.set_buffer(self.textbuffer)

           
    def __init__(self):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_resizable(True)
        window.set_size_request(450,540)
        window.connect("destroy", self.close_application)
        window.connect("key_press_event", self.key_pressed)
        window.set_title("Devanagari Editor")
        window.set_border_width(0)
        window.set_icon_from_file("DElogo.ico")

        self.box1 = gtk.VBox(False, 0)
        window.add(self.box1)
        self.box1.show()

        box2 = gtk.VBox(False, 10)
        box2.set_border_width(10)
        self.box1.pack_start(box2, True, True, 0)
        box2.show()

        # the source text buffer
        sw_src = gtk.ScrolledWindow()
        sw_src.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.textview_src = gtk.TextView()
        self.textbuffer_src = self.textview_src.get_buffer()
        self.textview_src.set_wrap_mode(gtk.WRAP_WORD)
        self.textview_src.modify_font(pango.FontDescription("Courier New 12"))
        sw_src.add(self.textview_src)
        sw_src.show()
        self.textview_src.show()

        box2.pack_start(sw_src)

        # the display text buffer
        sw = gtk.ScrolledWindow()
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.textview = gtk.TextView()
        self.textbuffer = self.textview.get_buffer()
        self.textview.set_wrap_mode(gtk.WRAP_WORD)
        self.textview.modify_font(pango.FontDescription("Sans 12"))
        sw.add(self.textview)
        sw.show()
        self.textview.show()

        box2.pack_start(sw)

        # clipboard
        self.clipboard = gtk.Clipboard(gtk.gdk.display_get_default(), "CLIPBOARD")
        
        # show the window 
        window.show()

def main():
    gtk.main()
    return 0       

if __name__ == "__main__":
    DevanagariTextEditor()
    main()
