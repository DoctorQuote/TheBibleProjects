#!/usr/bin/env python3
'''
File: kjv.py
Problem Domain: Console Application
Status: Production
Revision: 1.0.0

MISSION
=======
Create a simple way to read & collect your favorite passages
using every operating system where Python is available.

NEXUS
----- 
https://github.com/DoctorQuote/TheBibleProjects
'''

import argparse
from sierra_dao import SierraDAO
from tui import BasicTui

def dum():
    BasicTui.Display('(done)')


def do_func(prompt, options, level):
    '''Menued operations. '''
    choice = None
    while choice != options[-1][0]:
        BasicTui.Display(level * 15)
        for o in options:
            BasicTui.Display(o[0], o[1])
        choice = BasicTui.Input(prompt)
        if not choice:
            continue
        choice = choice[0].lower()
        BasicTui.Display(f">> {choice}")
        for o in options:
            if o[0] == choice:
                BasicTui.DisplayTitle(o[1])
                o[2]()


def do_search_books(bSaints=True):
    ''' Search books & read from results. '''
    BasicTui.Display("Example: +word -word")
    BasicTui.Display("Enter q to quit")
    inc = ''; count = 0
    words = BasicTui.Input("+/-words: ")
    for word in words.strip().split(' '):
        if not word or word == 'q':
            return
        if inc:
            inc += ' AND '
        if word[0] == '-':
            inc += f'VERSE NOT LIKE "%{word[1:]}%"'
            count += 1
        if word[0] == '+':
            inc += f'VERSE LIKE "%{word[1:]}%"'
            count += 1
    if not count:
        return
    dao = SierraDAO.GetDAO(bSaints)
    BasicTui.Display(inc)
    sigma = 0
    for row in dao.search(inc):
        sigma += 1
        BasicTui.DisplayVerse(row)
    BasicTui.DisplayTitle(f"Found {sigma} Verses")


def do_list_books(bSaints=True):
    ''' Displays the books. Saint = superset. Returns number
        of books displayed to permit selections of same.
    '''
    return BasicTui.DisplayBooks()


def do_random_reader(bSaints=True)->int:
    ''' Start reading at a random location.
        Return the last Sierra number shown.
    '''
    dao = SierraDAO.GetDAO(bSaints)
    res = dao.conn.execute('SELECT COUNT(*) FROM SqlTblVerse;')
    vmax = res.fetchone()[0]+1
    import random    
    sierra = random.randrange(1,vmax)
    return browse_from(sierra)


def do_sierra_reader(bSaints=True)->int:
    ''' Start reading at a Sierra location.
        Return the last Sierra number shown.
        Zero on error.
    '''
    books = []
    for row in SierraDAO.ListBooks(bSaints):
        books.append(row['book'].lower())
    last_book = do_list_books()
    option = BasicTui.Input('Book # > ')
    try:
        inum = int(option)
        if inum < 1 or inum > last_book:
            return
        ubook = books[inum-1]
        BasicTui.Display(f'Got {ubook}.')
        vrange = SierraDAO.GetBookRange(inum)
        option = BasicTui.Input(f'Enter a number between {vrange}, inclusive. > ')
        return browse_from(int(option))               
    except:
        return 0


def do_classic_reader(bSaints=True):
    ''' Start browsing by classic chapter:verse. '''
    BasicTui.DisplayBooks()
    try:
        ibook = int(BasicTui.Input("Book #> "))
        ichapt = int(BasicTui.Input("Chapter #> "))
        iverse = int(BasicTui.Input("Verse #> "))
        dao = SierraDAO.GetDAO(bSaints)
        for res in dao.search(f'BookID = {ibook} AND BookChapterID = {ichapt} AND BookVerseID = {iverse}'):
            browse_from(dict(res)['sierra'])
    except Exception as ex:
        BasicTui.DisplayError(ex)

    
def browse_from(sierra,bSaints=True)->int:
    ''' Start reading at a Sierra location.
        Return the last Sierra number shown.
        Zero on error.
    '''
    sierra = int(sierra)
    dao = SierraDAO.GetDAO(bSaints)
    res = dao.conn.execute('SELECT COUNT(*) FROM SqlTblVerse;')
    vmax = res.fetchone()[0]+1
    
    verse = dict(*dao.search_verse(sierra))
    option = ''
    while option != 'q':
        if not BasicTui.DisplayVerse(verse):
            return 0
        # do_func too much for a reader, methinks.
        option = BasicTui.Input('[n]ext, [p]revious, [q]uit > ').strip()
        if not option:
            continue
        try:
            o = option[0]
            if o == 'n':
                if sierra == vmax:
                    BasicTui.Display('At the end.')
                    continue
                sierra += 1
                verse = dict(*dao.search_verse(sierra))
            elif o == 'p':
                if sierra == 1:
                    BasicTui.Display('At the top.')
                    continue
                sierra -= 1
                verse = dict(*dao.search_verse(sierra))
            elif o == 'q':
                return sierra
            else:
                BasicTui.Display('Enter either n, p, or q.')
        except Exception as ex:
            BasicTui.DisplayError(ex)
            return sierra


options = [
    ("b", "List Books", do_list_books),
    ("v", "Sierra Reader", do_sierra_reader),
    ("c", "Classic Reader", do_classic_reader),
    ("r", "Random Reader", do_random_reader),
    ("s", "Search", do_search_books),
    ("q", "Quit", dum)
]

BasicTui.SetTitle('The Stick of Joseph')
do_func("Main Menu: ", options, '#')
BasicTui.Display(".")
