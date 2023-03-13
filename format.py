class shellColors:
    """bash colors using ANSI escape codes: https://en.wikipedia.org/wiki/ANSI_escape_code"""
    TITLE = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    PURPLE = '\033[35m'
    UNDERLINE = '\033[4m'
    BOLD = '\033[1m'
    ENDCOLOR = '\033[0m'

class Format:
    """general formatting for the application and symbols"""
    # variables to shorten display
    green, blue, purple = shellColors.GREEN, shellColors.BLUE, shellColors.PURPLE
    underline, bold, end_color = shellColors.UNDERLINE, shellColors.BOLD, shellColors.ENDCOLOR
    # symbols used throughout the application
    PLANE = '✈️'
    MEMO = '📝'
    CASE = '🧳'
    MONEY = '💰'
    JOURNAL = '📒'
    PHONE = '☎️'
    TIPS = '💁'
    # titles and lines used throughout the application
    NEWLINE = '\n'
    LINE = f'{green}{underline}{"-"*50}{shellColors.ENDCOLOR}'
    LINEBLU = f'{blue}{underline}{"-"*50}{shellColors.ENDCOLOR}'
    LINEPUR = f'{purple}{underline}{"-"*50}{shellColors.ENDCOLOR}'
    APPNAME = f'-       {green}{bold}{PLANE}         Travel Planner        {PLANE}{end_color}      -'
    ITINAME = f'-       {blue}{bold}{MEMO}           Itinerary              {MEMO}{end_color}   -'
    PCKNAME = f'-       {blue}{bold}{CASE}           Packing List        {CASE}{end_color}      -'
    BDGNAME = f'-       {blue}{bold}{MONEY}          Budget                {MONEY}{end_color}     -'
    CONNAME = f'-       {blue}{bold}{PHONE}         Important Contacts        {PHONE}{end_color}    -'
    TIPNAME = f'-       {blue}{bold}{TIPS}           Tips               {TIPS}{end_color}        -'
    PLRNAME = f'-       {blue}{bold}{JOURNAL}        Planner                {JOURNAL}{end_color}     -'