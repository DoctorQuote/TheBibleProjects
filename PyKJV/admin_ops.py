from sierra_dao import SierraDAO
    
tables = {
    'SqlTblVerse':'CREATE TABLE IF NOT EXISTS SqlTblVerse (ID Integer PRIMARY KEY AUTOINCREMENT, BookID int, BookChapterID int, BookVerseID int, Verse String, VerseType int);',
    'SqlNotes'   :'CREATE TABLE IF NOT EXISTS SqlNotes (ID Integer PRIMARY KEY AUTOINCREMENT, vStart int, vEnd int, kwords String, Subject String, Notes String, NextId int);',
    'SqlBooks'   :'CREATE TABLE IF NOT EXISTS SqlBooks (ID Integer PRIMARY KEY AUTOINCREMENT, Book String, BookMeta String);',
    }

def destroy_notes():
    ''' Re-create the SqlNotes Table from scratch. Will destroy SqlNotes!'''
    key = 'SqlNotes'
    dao = SierraDAO.GetDAO()
    dao.conn.execute(f'DROP TABLE IF EXISTS {key};')
    dao.conn.execute(tables[key])
    dao.conn.connection.commit()
    

def destroy_everything():
    ''' Re-create the database from scratch. Will destroy SqlNotes!'''
    import os.path
    ''' My thing - not to worry. '''
    zfile = r'C:\d_drive\USR\code\TheBibleProjects\TheBibleProjects-main\SierraBible\biblia\b1.tab'
    if not os.path.exists(zfile):
        return

    dao = SierraDAO.GetDAO()
    for key in tables:
        dao.conn.execute(f'DROP TABLE IF EXISTS {key};')
        dao.conn.execute(tables[key])

    vtags = ['zb','book','verse','text']
    books = dict()
    lines = []
    with open(zfile) as fh:
        for line in fh:
            row = line.split('\t')
            zd = dict(zip(vtags,row))
            if len(books) < 40:
                my_book = 'kjv.ot.'+ zd['book']
                books[zd['book']] = my_book
            elif len(books) < 67:
                my_book = 'kjv.nt.'+ zd['book']
                books[zd['book']] = my_book
            else:
                my_book = 'lds.bom.'+ zd['book']
                books[zd['book']] = my_book
            zd['book'] = [my_book, len(books)]
            zd['verse'] = zd['verse'][2:].split(':')
            lines.append(zd)
                
    print(len(lines), len(books))
    for ss, b in enumerate(books, 1):
        print(ss,books[b])
        cmd = f'insert into SqlBooks (Book) VALUES ("{books[b]}");'
        dao.conn.execute(cmd)
    for line in lines:
        cmd = f'''insert into SqlTblVerse
    (BookID, BookChapterID, BookVerseID, Verse) VALUES
    ({line['book'][1]}, {line['verse'][0]}, {line['verse'][1]}, "{line['text'].strip()}")
    ;'''
        dao.conn.execute(cmd)
    dao.conn.connection.commit()
        



