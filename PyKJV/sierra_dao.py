'''
File: sierra_dao.py
Problem Domain: Database / DAO
Status: PRODUCTION / STABLE
Revision: 1.5.1

Source: 
https://github.com/DoctorQuote/TheBibleProjects

'''
import sys
import sqlite3


class SierraDAO:
    ''' Extract a nominal PROBLEM DOMAIN dictionary,
        from the database. Partial S3D2 pattern.'''
    
    def __init__(self, cursor, bSaints=False):
        self.conn = cursor
        self.bSaints = bSaints
        self.sql_sel = "SELECT Verse, Book, BookChapterID, BookVerseID, V.ID, BookID \
FROM SqlTblVerse AS V JOIN SqlBooks as B WHERE (B.ID=BookID) AND {zmatch} ORDER BY V.ID;"

    def source(self):
        result = {
            "sierra":None,
            "book":None,
            "chapter":None,
            "verse":None,
            "text":None,
           }
        return result

    def classic2sierra(self, book, chapt, verse):
        # print([book, chapt, verse], file=sys.stderr)
        cmd = f"SELECT V.ID FROM SqlTblVerse AS V JOIN SqlBooks as B \
WHERE (B.ID=BookID) AND BOOK LIKE '%{book}%' AND BookChapterID='{chapt}' AND BookVerseID='{verse}' LIMIT 1;"
        print(cmd, file=sys.stderr)
        res = self.conn.execute(cmd)
        try:
            zrow = res.fetchone()
            print(zrow, file=sys.stderr)
            if zrow:
                return zrow[0]
        except:
            raise
        return None
            
    def search_verse(self, sierra_num):
        ''' Lookup a single sierra verse number. Presently unloved. '''
        for result in self.search(f"V.ID={sierra_num}"):
            yield result

    def search_books(self):
        ''' Locate the book inventory - Name of book, only '''
        cmd = "SELECT Book FROM SqlBooks ORDER BY ID;"
        res = self.conn.execute(cmd)
        response = self.source()
        try:
            zrow = res.fetchone()
            while zrow:
                response['book'] = zrow[0]
                if zrow[0].find('.') != -1:
                    cols = zrow[0].split('.')
                    if self.bSaints == False and cols[1] != 'nt' and cols[1] != 'ot':
                        zrow = res.fetchone()
                        continue
                    response['book'] = cols[2]
                yield response
                zrow = res.fetchone()
        except Exception as ex:
            print(ex, file=sys.stderr)
            raise ex
        return None
    
    def search(self, where_clause):
        ''' Search using a LIKE-match - one or many. '''
        cmd = self.sql_sel.replace('{zmatch}', where_clause)
        res = self.conn.execute(cmd)
        response = self.source()
        try:
            zrow = res.fetchone()
            while zrow:
                response['sierra'] = str(zrow[4])
                response['book'] = zrow[1]
                if zrow[1].find('.') != -1:
                    cols = zrow[1].split('.')
                    if self.bSaints == False and cols[1] != 'nt' and cols[1] != 'ot':
                        zrow = res.fetchone()
                        continue
                    response['book'] = cols[2]
                response['chapter'] = zrow[2]
                response['verse'] = zrow[3]
                response['text'] = zrow[0]
                yield response
                zrow = res.fetchone()
        except Exception as ex:
            print(ex, file=sys.stderr)
            raise ex
        return None

    
    @staticmethod
    def GetDAO(bSaints=False):
        ''' Connect to the database & return the DAO '''
        conn = sqlite3.connect("./biblia.sqlt3")
        # conn.row_factory = dict_factory
        curs = conn.cursor()
        dao = SierraDAO(curs, bSaints)
        return dao

    
    @staticmethod
    def ListBooks(bSaints=False) -> list():
        ''' Get the major books '''
        results = list()
        dao = SierraDAO.GetDAO(bSaints)
        if not dao:
            return results
        books = dao.search_books()
        if not books:
            return results
        return books

    @staticmethod
    def GetBookRange(book_id:int, bSaints=True)->tuple:
        ''' Get the minimum and maximum sierra
            number for the book #, else None
        '''
        try:
            dao = SierraDAO.GetDAO(bSaints)
            cmd = f'select min(id), max(id) from SqlTblVerse where BookID = {book_id};'
            result = dao.conn.execute(cmd)
            return tuple(result.fetchone())
        except Exception as ex:
            print(ex)
            return None
                
if __name__ == "__main__":
    ''' Ye Olde Testing '''
    from tui import BasicTui
    for ss, row in enumerate(SierraDAO.ListBooks(True), 1):
        print(ss, row)
    for ss, row in enumerate(SierraDAO.ListBooks(True), 1):
        print(ss * 1000, row)
    dao = SierraDAO.GetDAO()

    for row in dao.search("verse LIKE '%PERFECT%'"):
        BasicTui.DisplayVerse(row)
