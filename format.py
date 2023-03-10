class shellColors:
    TITLE = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    PURPLE = '\033[35m'
    UNDERLINE = '\033[4m'
    BOLD = '\033[1m'
    ENDCOLOR = '\033[0m'


class Symbols:
    PLANE = '✈️'
    MEMO = '📝'
    CASE = '🧳'
    MONEY = '💰'
    JOURNAL = '📒'
    PHONE = '☎️'
    TIPS = '💁'


class Format:
    NEWLINE = '\n'
    LINE = f'{shellColors.GREEN}{shellColors.UNDERLINE}{"-"*50}{shellColors.ENDCOLOR}'
    LINEBLU = f'{shellColors.BLUE}{shellColors.UNDERLINE}{"-"*50}{shellColors.ENDCOLOR}'
    LINEPUR = f'{shellColors.PURPLE}{shellColors.UNDERLINE}{"-"*50}{shellColors.ENDCOLOR}'
    APPNAME = f'-       {shellColors.GREEN}{shellColors.BOLD}{Symbols.PLANE}         Travel Planner        {Symbols.PLANE}{shellColors.ENDCOLOR}      -'
    ITINAME = f'-       {shellColors.BLUE}{shellColors.BOLD}{Symbols.MEMO}           Itinerary              {Symbols.MEMO}{shellColors.ENDCOLOR}   -'
    PCKNAME = f'-       {shellColors.BLUE}{shellColors.BOLD}{Symbols.CASE}           Packing List        {Symbols.CASE}{shellColors.ENDCOLOR}      -'
    BDGNAME = f'-       {shellColors.BLUE}{shellColors.BOLD}{Symbols.MONEY}          Budget                {Symbols.MONEY}{shellColors.ENDCOLOR}     -'
    CONNAME = f'-       {shellColors.BLUE}{shellColors.BOLD}{Symbols.PHONE}         Important Contacts        {Symbols.PHONE}{shellColors.ENDCOLOR}    -'
    TIPNAME = f'-       {shellColors.BLUE}{shellColors.BOLD}{Symbols.TIPS}           Tips               {Symbols.TIPS}{shellColors.ENDCOLOR}        -'
    PLRNAME = f'-       {shellColors.BLUE}{shellColors.BOLD}{Symbols.JOURNAL}        Planner                {Symbols.JOURNAL}{shellColors.ENDCOLOR}     -'