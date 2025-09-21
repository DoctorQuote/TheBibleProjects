from verse import Verse
v = Verse()

class BasicTui:
    
    @staticmethod
    def ClearScreen():
        ''' No ANSI codes assumed here, so we'll scroll. '''
        for _ in range(30):
            print()
    
    @staticmethod
    def Input(prompt:str)->str:
        return input(prompt)

    @staticmethod
    def DisplayTitle(title:str, char='*'):
        print(v.wrap(char * v._wrap.width)[0])
        for zline in v.wrap(title.strip()):
            print(zline)
        print(v.wrap(char * v._wrap.width)[0])
        
    @staticmethod
    def DisplayBooks(bSaints=True):
        ''' Displays the books. Saint = superset. Returns number
            of books displayed to permit selections of same.
        '''
        from sierra_dao import SierraDAO
        for ss, book in enumerate(SierraDAO.ListBooks(bSaints),1):
            if(ss % 3) == 0:
                print(f"{ss:02}.) {book['book']:<18}")
            else:
                print(f"{ss:02}.) {book['book']:<18}", end = '')
        print()
        return ss
       
    @staticmethod
    def DisplayError(line:str)->bool:
        ''' Common display for all errors. '''
        return BasicTui.Display(str(line))
    
    @staticmethod
    def Display(*args)->bool:
        ''' Common display for all lines. '''
        if not args:
            return False
        line = ' '.join(args)
        for zline in v.wrap(line.strip()):
            print(zline)
        return True
   
    @staticmethod
    def DisplayVerse(row:dict)->bool:
        ''' Common display for all verses. '''
        if not row:
            print('[null]')
            return False
        line = row['text']
        print(v.center(' {0} {1}:{2} '.format(
            row['book'],row['chapter'],row['verse']), '='))
        for zline in v.wrap(line.strip()):
            print(zline)
        print(v.center(' Sierra Bible #{0} '.format(
            row['sierra']), '='))
        return True
