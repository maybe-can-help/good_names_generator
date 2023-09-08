from argparse import ArgumentParser
from sys import stdin, argv

parser = ArgumentParser(prog="good_names_generator")
parser.add_argument("--from",
                    dest="input",
                    default="list.txt",
                    type=str,
                    help="Path to txt file with input names")
parser.add_argument("--to",
                    dest="output",
                    default="list.txt",
                    type=str,
                    help="Path to file with generated results")
parser.add_argument("-og",
                    "--off-generator",
                    action="store_true",
                    help="Off generating files")
parser.add_argument("-t",
                    "--transliteration",
                    action="store_true",
                    help="Enable transliteration")
args = parser.parse_args()


def append_telesales_mail_address(string: str,
                                  postfix: str = "@telesales-service.org") -> str:
    return f"{string}{postfix}"


def from_bad_name_to_good(name: str) -> str:
    separated_name = name.split()
    surname = separated_name[0]
    name = separated_name[1]
    patronymic = separated_name[2]
    return f"{surname}.{name[0]}.{patronymic[0]}"

    
def transliterate(name):
    _dict = {'а':'a','б':'b','в':'v','г':'g','д':'d','е':'e','ё':'e',
          'ж':'zh','з':'z','и':'i','й':'i','к':'k','л':'l','м':'m','н':'n',
          'о':'o','п':'p','р':'r','с':'s','т':'t','у':'u','ф':'f','х':'h',
          'ц':'c','ч':'cz','ш':'sh','щ':'scz','ъ':'','ы':'y','ь':'','э':'e',
          'ю':'yu','я':'ja', 'А':'A','Б':'B','В':'V','Г':'G','Д':'D','Е':'E','Ё':'E',
          'Ж':'ZH','З':'Z','И':'I','Й':'I','К':'K','Л':'L','М':'M','Н':'N',
          'О':'O','П':'P','Р':'R','С':'S','Т':'T','У':'U','Ф':'F','Х':'H',
          'Ц':'C','Ч':'CZ','Ш':'sh','Щ':'sch','Ъ':'','Ы':'y','Ь':'','Э':'e',
          'Ю':'yu','Я':'ya',',':'','?':'',' ':' ','~':'','!':'','@':'','#':'',
          '$':'','%':'','^':'','&':'','*':'','(':'',')':'','-':'','=':'','+':'',
          ':':'',';':'','<':'','>':'','\'':'','"':'','\\':'','/':'','№':'',
          '[':'',']':'','{':'','}':'','ґ':'','ї':'', 'є':'','Ґ':'g','Ї':'i',
          'Є':'e', '—':''}
    for key in _dict:
        name = name.replace(key, _dict[key])
    return name


def main():
    result = []
    # If true - terminal, false - pipe mode
    if stdin.isatty():
        with open(args.input, "r", encoding="utf-8") as source_file:
            for n, line in enumerate(source_file):
                try:
                    if args.transliteration:
                        new_line = from_bad_name_to_good(transliterate(line).lower()) + "\n"
                    else:
                        new_line = from_bad_name_to_good(line) + "\n"
                    result.append(new_line)
                except IndexError:
                    print(f"Something wrong with {n+1} line ({repr(line)})")
        if not args.off_generator:
            with open(args.output, "w", encoding="utf-8") as out_file:
                for line in result:
                    out_file.write(line)
    else:
        for n, line in enumerate(stdin):
            try:
                if args.transliteration:
                    new_line = from_bad_name_to_good(transliterate(line).lower())
                else:
                    new_line = from_bad_name_to_good(line)
                result.append(new_line)
            except IndexError:
                print(f"Something wrong with {n+1} line ({repr(line)})")
        if not args.off_generator:
            with open(args.output, "w", encoding="utf-8") as out_file:
                for line in result:
                    out_file.write(line)
        else:
            for line in result:
                print(repr(line))

    
if __name__ == "__main__":
    main()
