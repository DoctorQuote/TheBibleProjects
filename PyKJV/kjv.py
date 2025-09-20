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
    print('(done)')


def do_func(prompt, options, level):
    choice = None
    while choice != options[-1][0]:
        print(level * 15)
        for o in options:
            print(o[0], o[1])
        choice = input(prompt)
        if not choice:
            continue
        choice = choice[0].lower()
        print(f">> {choice}")
        for o in options:
            if o[0] == choice:
                print(o[1])
                o[2]()
                break


def do_book_cv():
    print('do_book_cv')


def do_book_vnum():
    print('do_book_vnum')


def do_search():
    options = [
    ("b", "List Books", do_list_books),
    ("c", "book:chapter:verse", do_book_cv),
    ("a", "absolute verse #", do_book_vnum),
    ("q", "Quit", dum)
    ]
    do_func("Search Menu: ", options, '?')


def do_list_books(bSaints=True)->int:
    ''' Displays the books. Saint = superset. Returns number
        of books displayed to permit selections of same.
    '''
    for ss, book in enumerate(SierraDAO.ListBooks(bSaints),1):
        if(ss % 3) == 0:
            print(f"{ss:02}.) {book['book']:<18}")
        else:
            print(f"{ss:02}.) {book['book']:<18}", end = '')
    return ss


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
    option = input('Book # > ')
    try:
        inum = int(option)
        if inum < 1 or inum > last_book:
            return
        ubook = books[inum-1]
        print(f'Got {ubook}.')
        vrange = SierraDAO.GetBookRange(inum)
        option = input(f'Enter a number between {vrange}, inclusive. > ')
        return browse_from(int(option))               
    except:
        return 0
    
def browse_from(sierra,bSaints=True)->int:
    ''' Start reading at a Sierra location.
        Return the last Sierra number shown.
    '''
    dao = SierraDAO.GetDAO(bSaints)
    res = dao.conn.execute('SELECT COUNT(*) FROM SqlTblVerse;')
    vmax = res.fetchone()[0]+1
    
    verse = dict(*dao.search_verse(sierra))
    option = ''
    while option != 'q':
        BasicTui.DisplayVerse(verse)
        # do_func too much for a reader, methinks.
        option = input('[n]ext, [p]revious, [q]uit > ')
        try:
            o = option[0]
            if o == 'n':
                if sierra == vmax:
                    print('At the end.')
                    continue
                sierra += 1
                verse = dict(*dao.search_verse(sierra))
            elif o == 'p':
                if sierra == 1:
                    print('At the top.')
                    continue
                sierra -= 1
                verse = dict(*dao.search_verse(sierra))
            elif o == 'q':
                return sierra
            else:
                print('Enter either n, p, or q.')
        except Exception as ex:
            print(ex)
            return sierra


options = [
    ("b", "List Books", do_list_books),
    ("v", "Verse Reader", do_reader),
    ("r", "Random Reader", do_random_reader),
    ("s", "Search", do_search),
    ("q", "Quit", dum)
]

do_func("Main Menu: ", options, '#')
print(".")
