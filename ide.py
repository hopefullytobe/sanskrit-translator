# -*- coding: utf-8 -*-

# Devanagari Editor

import pygtk, pango
pygtk.require('2.0')
import gtk
from decoders import devanagari

Vowels = 'aAiIuUReoMH'
Consonants = 'kgGcjJTDNtdnpbmyrlvzSsh'
Numbers = '0123456789'
other = ". |-\r\n\t"
virama = u'\u094d'

map_vowels = {'a':u'\u0905', 'A':u'\u0906', 'i':u'\u0907', 'I':u'\u0908', 'u':u'\u0909', \
              'U':u'\u090a', 'R':u'\u090b', 'RR':u'\u0960', 'lR':u'\u090c', 'lRR':u'\u0961', \
              'e':u'\u090f', 'ai':u'\u0910', 'o':u'\u0913', 'au':u'\u0914', \
              'M':u'\u0902', 'H':u'\u0903'}
#x -> 0960?
map_vowel_signs = {'a':'', 'A':u'\u093e', 'i':u'\u093f', 'I':u'\u0940', 'u':u'\u0941', \
                   'U':u'\u0942', 'R':u'\u0943', 'RR':u'\u0944', 'lR':u'\u0962', 'lRR':u'\u0963', \
                   'e':u'\u0947', 'ai':u'\u0948', 'o':u'\u094b', 'au':u'\u094c', \
                   'M':u'\u0902', 'H':u'\u0903', '_':u'\u094d'}

map_consonants = {'k':u'\u0915', 'kh':u'\u0916', 'g':u'\u0917', 'gh':u'\u0918', 'G':u'\u0919', \
                  'c':u'\u091a', 'ch':u'\u091b', 'j':u'\u091c', 'jh':u'\u091d', 'J':u'\u091e', \
                  'T':u'\u091f', 'Th':u'\u0920', 'D':u'\u0921', 'Dh':u'\u0922', 'N':u'\u0923', \
                  't':u'\u0924', 'th':u'\u0925', 'd':u'\u0926', 'dh':u'\u0927', 'n':u'\u0928', \
                  'p':u'\u092a', 'ph':u'\u092b', 'b':u'\u092c', 'bh':u'\u092d', 'm':u'\u092e', \
                  'y':u'\u092f', 'r':u'\u0930', 'l':u'\u0932', 'v':u'\u0935', 'z':u'\u0936', \
                  'S':u'\u0937', 's':u'\u0938', 'h':u'\u0939'}

map_numbers = {'0':u'\u0966', '1':u'\u0967', '2':u'\u0968', '3':u'\u0969', '4':u'\u096A', \
               '5':u'\u096B', '6':u'\u096C', '7':u'\u096D', '8':u'\u096E', '9':u'\u096F'}
def isVowel(ch):
    return ch in Vowels
def isConsonant(ch):
    return ch in Consonants
def isNumber(ch):
    return ch in Numbers
def isUVowel(ch):
    if ch > u'\u0901' and ch < u'\u0915':
        return True
    elif ch == u'\u0960' or ch == u'\u0961':
        return True
    else:
        return False
def isUConsonant(ch):
    if isUVowel(ch):
        return False
    elif ch > u'\u0914' and ch < u'\u0940':
        return True
    else:
        return False
    
class DevanagariTextEditor:
    
    def close_application(self, widget):
        gtk.main_quit()
            
    def key_pressed(self, widget, event):
        # F2 to convert the selected text to devanagari
        if event.keyval == 65471:
            try:
                start, end = self.textbuffer.get_selection_bounds()
                text = start.get_text(end)
                self.textbuffer.delete(start, end)
                devanagari_string = devanagari("hk", text)
                self.textbuffer.insert_at_cursor(devanagari_string)
            except ValueError:
                pass
        # F5 to toggle editing mode
        elif event.keyval == 65474:
            if self.Mode == 'Devanagari':
                self.window.disconnect(self.handler)
                self.Mode = 'Roman'
            else:
                self.handler = self.window.connect("key_release_event", self.key_released)
                self.Mode = 'Devanagari'
    def delete_previous_char(self, Start, End):
        start = self.textbuffer.get_iter_at_mark(self.textbuffer.get_insert())
        end = self.textbuffer.get_iter_at_mark(self.textbuffer.get_insert())
        start.backward_chars(Start)
        end.backward_chars(End)
        self.textbuffer.delete(start, end)
    def get_previous_char(self, Start, End):
        start = self.textbuffer.get_iter_at_mark(self.textbuffer.get_insert())
        end = self.textbuffer.get_iter_at_mark(self.textbuffer.get_insert())
        start.backward_chars(Start)
        end.backward_chars(End)
        return start.get_text(end)
    
    def key_released(self, widget, event):
        if event.keyval > 255:
            return
        ch = self.get_previous_char(1,0) #check for null
        if ch == '':
            return
        if ord(ch) <= 255:
            if isVowel(ch):
                self.delete_previous_char(1,0)
                if self.get_previous_char(1,0) == u'\u094d': # is virama?
                    if self.get_previous_char(2,1) == u'\u0932' and ch == 'R': # for lR
                        if self.get_previous_char(3,2) == u'\u094d':
                            self.delete_previous_char(3,0)
                            self.textbuffer.insert_at_cursor(u'\u0962') # sign lR
                        else:
                            self.delete_previous_char(2,0)
                            self.textbuffer.insert_at_cursor(u'\u090c') # lR
                    else:
                        self.delete_previous_char(1,0)
                        self.textbuffer.insert_at_cursor(map_vowel_signs[ch])
                else:
                    if self.get_previous_char(1,0) == u'\u090b' and ch == 'R': # RR
                        self.delete_previous_char(1,0)
                        self.textbuffer.insert_at_cursor(u'\u0960')
                    elif self.get_previous_char(1,0) == u'\u0943' and ch == 'R': # sign R + R
                        self.delete_previous_char(1,0)
                        self.textbuffer.insert_at_cursor(u'\u0944') # sign RR
                    elif self.get_previous_char(1,0) == u'\u0962' and ch == 'R': # sign l + R
                        self.delete_previous_char(1,0)
                        self.textbuffer.insert_at_cursor(u'\u0963') # sign lRR
                    elif self.get_previous_char(1,0) == u'\u0905' and ch == 'u':
                        self.delete_previous_char(1,0)
                        self.textbuffer.insert_at_cursor(map_vowels['au'])
                    elif self.get_previous_char(1,0) == u'\u0905' and ch == 'i':
                        self.delete_previous_char(1,0)
                        self.textbuffer.insert_at_cursor(map_vowels['ai'])
                    elif isUConsonant(self.get_previous_char(1,0)):
                        if ch == 'u':
                            self.textbuffer.insert_at_cursor(map_vowel_signs['au'])
                        elif ch == 'i':
                            self.textbuffer.insert_at_cursor(map_vowel_signs['ai'])
                        else:
                            self.textbuffer.insert_at_cursor(map_vowels[ch])
                    else:
                        self.textbuffer.insert_at_cursor(map_vowels[ch])
            if isConsonant(ch):
                self.delete_previous_char(1,0)
                if ch == 'h':
                    if self.get_previous_char(2,1) == u'\u0915': # kh
                        self.delete_previous_char(2,0)
                        self.textbuffer.insert_at_cursor(map_consonants['kh'])
                    elif self.get_previous_char(2,1) == u'\u0917': # gh
                        self.delete_previous_char(2,0)
                        self.textbuffer.insert_at_cursor(map_consonants['gh'])
                    elif self.get_previous_char(2,1) == u'\u091a': # ch
                        self.delete_previous_char(2,0)
                        self.textbuffer.insert_at_cursor(map_consonants['ch'])
                    elif self.get_previous_char(2,1) == u'\u091c': # jh
                        self.delete_previous_char(2,0)
                        self.textbuffer.insert_at_cursor(map_consonants['jh'])
                    elif self.get_previous_char(2,1) == u'\u091f': # Th
                        self.delete_previous_char(2,0)
                        self.textbuffer.insert_at_cursor(map_consonants['Th'])
                    elif self.get_previous_char(2,1) == u'\u0921': # Dh
                        self.delete_previous_char(2,0)
                        self.textbuffer.insert_at_cursor(map_consonants['Dh'])
                    elif self.get_previous_char(2,1) == u'\u0924': # th
                        self.delete_previous_char(2,0)
                        self.textbuffer.insert_at_cursor(map_consonants['th'])
                    elif self.get_previous_char(2,1) == u'\u0926':# dh
                        self.delete_previous_char(2,0)
                        self.textbuffer.insert_at_cursor(map_consonants['dh'])
                    elif self.get_previous_char(2,1) == u'\u092a':# ph
                        self.delete_previous_char(2,0)
                        self.textbuffer.insert_at_cursor(map_consonants['ph'])
                    elif self.get_previous_char(2,1) == u'\u092c':# bh
                        self.delete_previous_char(2,0)
                        self.textbuffer.insert_at_cursor(map_consonants['bh'])
                    else:
                        self.textbuffer.insert_at_cursor(map_consonants['h'])
                else:
                    self.textbuffer.insert_at_cursor(map_consonants[ch])
                self.textbuffer.insert_at_cursor(u'\u094d')
            if isNumber(ch):
                self.delete_previous_char(1,0)
                self.textbuffer.insert_at_cursor(map_numbers[ch])

    def save_devanagari_file(self, widget):
        start, end = self.textbuffer.get_bounds()
        string = self.textbuffer.get_text(start, end)
        filechooserdialog = gtk.FileChooserDialog("Save Destination File",
                                                  None, gtk.FILE_CHOOSER_ACTION_SAVE,
                                                  (gtk.STOCK_CANCEL,
                                                   gtk.RESPONSE_CANCEL,
                                                   gtk.STOCK_OK, gtk.RESPONSE_OK))
        response = filechooserdialog.run()
        if response == gtk.RESPONSE_OK:
            filename = filechooserdialog.get_filename()
            FILE = open(filename, 'w')
            FILE.write(string)
            FILE.close()            
        filechooserdialog.destroy()

    def open_devanagari_file(self, widget):
        filechooserdialog = gtk.FileChooserDialog("Save Destination File",
                                                  None, gtk.FILE_CHOOSER_ACTION_OPEN,
                                                  (gtk.STOCK_CANCEL,
                                                   gtk.RESPONSE_CANCEL,
                                                   gtk.STOCK_OK, gtk.RESPONSE_OK))
        response = filechooserdialog.run()
        if response == gtk.RESPONSE_OK:
            filename = filechooserdialog.get_filename()
            FILE = open(filename, 'r')
            string = FILE.read()
            FILE.close()
            self.textbuffer.set_text(string)
        filechooserdialog.destroy()
        
            
    def transcode_the_text(self, widget):
        start, end = self.textbuffer.get_bounds()
        hk_string = self.textbuffer.get_text(start, end)
        devanagari_string = devanagari("hk", hk_string)
        self.textbuffer.set_text(devanagari_string)
        self.textview.set_buffer(self.textbuffer)

           
    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_resizable(True)
        self.window.set_size_request(450,540)
        self.window.connect("destroy", self.close_application)
        self.window.connect("key_press_event", self.key_pressed)
        self.handler = self.window.connect("key_release_event", self.key_released)
        self.window.set_title("Devanagari Editor")
        self.window.set_border_width(0)
        self.window.set_icon_from_file("DElogo.ico")

        menubar = gtk.MenuBar()
        
        menu_file = gtk.Menu()
        menu_edit = gtk.Menu()
        menu_help = gtk.Menu()
        
        item_open = gtk.MenuItem("Open")
        item_open.connect("activate", self.open_devanagari_file)
        item_save = gtk.MenuItem("Save")
        item_save.connect("activate", self.save_devanagari_file)
        item_quit = gtk.MenuItem("Quit")
        item_quit.connect("activate", self.close_application)
        menu_file.append(item_open)
        menu_file.append(item_save)
        menu_file.append(item_quit)

        item_cut = gtk.MenuItem("Cut")
        item_copy = gtk.MenuItem("Copy")
        item_paste = gtk.MenuItem("Paste")
        menu_edit.append(item_cut)
        menu_edit.append(item_copy)
        menu_edit.append(item_paste)
        
        item_about = gtk.MenuItem("About")
        menu_help.append(item_about)
        
        item_file = gtk.MenuItem("File")
        item_edit = gtk.MenuItem("Edit")
        item_help = gtk.MenuItem("Help")
        
        item_file.set_submenu(menu_file)
        item_edit.set_submenu(menu_edit)
        item_help.set_submenu(menu_help)
        
        menubar.append(item_file)
        menubar.append(item_edit)
        menubar.append(item_help)
        

        self.box1 = gtk.VBox(False, 0)
        self.window.add(self.box1)
        self.box1.show()

        self.box1.pack_start(menubar, False, False, 0)
        
        box2 = gtk.VBox(False, 0)
        box2.set_border_width(0)
        self.box1.pack_start(box2, True, True, 0)
        box2.show()

        # the source text buffer
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

        self.Mode = 'Devanagari'

        # clipboard
        self.clipboard = gtk.Clipboard(gtk.gdk.display_get_default(), "CLIPBOARD")
        
        # show the window 
        self.window.show_all()

def main():
    gtk.main()
    return 0       

if __name__ == "__main__":
    DevanagariTextEditor()
    main()


