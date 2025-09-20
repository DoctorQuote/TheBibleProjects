#!/usr/bin/env python3
'''
File: kjv.py
Problem Domain: Console Application
Status: WORK IN PROGRESS
Revision: -1

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
                BasicTui.Display(o[1])
                o[2]()
                break


def do_book_cv():
    BasicTui.Display('do_book_cv')


def do_book_vnum():
    BasicTui.Display('do_book_vnum')


def do_search():
    options = [
    ("b", "List Books", do_list_books),
    ("c", "book:chapter:verse", do_book_cv),
    ("a", "absolute verse #", do_book_vnum),
    ("q", "Quit", dum)
    ]
    do_func("Search Menu: ", options, '~')


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


def do_reader(bSaints=True)->int:
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
    
def browse_from(sierra,bSaints=True)->int:
    ''' Start reading at a Sierra location.
        Return the last Sierra number shown.
        Zero on error.
    '''
    dao = SierraDAO.GetDAO(bSaints)
    res = dao.conn.execute('SELECT COUNT(*) FROM SqlTblVerse;')
    vmax = res.fetchone()[0]+1
    
    verse = dict(*dao.search_verse(sierra))
    option = ''
    while option != 'q':
        if not BasicTui.DisplayVerse(verse):
            return 0
        # do_func too much for a reader, methinks.
        option = BasicTui.Input('[n]ext, [p]revious, [q]uit > ')
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
    ("v", "Verse Reader", do_reader),
    ("r", "Random Reader", do_random_reader),
    ("s", "Search", do_search),
    ("q", "Quit", dum)
]

do_func("Main Menu: ", options, '#')
BasicTui.Display(".")
