class BasicTui:
    
    @staticmethod
    def ClearScreen():
        ''' No ANSI codes assumed here, so we'll scroll. '''
        for _ in range(30):
            print()
    
    @staticmethod
    def DisplayVerse(row:dict)->bool:
        ''' Common display for all verses. '''
        from verse import Verse
        if not row:
            print('[null]')
            return False
        v = Verse()
        line = row['text']
        print(v.center(' {0} {1}:{2} '.format(
            row['book'],row['chapter'],row['verse']), '='))
        for zline in v.wrap(line.strip()):
            print(zline)
        print(v.center(' Sierra Bible #{0} '.format(
            row['sierra']), '='))
        return True
