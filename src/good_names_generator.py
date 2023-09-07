from argparse import ArgumentParser

parser = ArgumentParser(prog="good_names_generator")
parser.add_argument("--from", default="list.txt", dest="source_file", type=str, help="Path to txt file with input names")
parser.add_argument("--to", default="list.txt", type=str, help="Path to file with generated results")
parser.add_argument("-og", "--off-generator", action="store_true", help="Off generating files")
parser.add_argument("-t", "--transliteration", action="store_true", help="Enable transliteration")
args = parser.parse_args()


def append_telesales_mail_address(string: str, postfix: str = "@telesales-service.org") -> str:
    return f"{string}{postfix}"


def from_bad_name_to_good(name: str) -> str:
    separated_name = name.split()
    surname, name, patronymic = separated_name[0], separated_name[1], separated_name[2]
    return f"{surname}.{name[0]}.{patronymic[0]}\n"

    
def transliterate(name):
    slovar = {'а':'a','б':'b','в':'v','г':'g','д':'d','е':'e','ё':'e',
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
    for key in slovar:
        name = name.replace(key, slovar[key])
    return name


def main():
    result = []
    
    with open(args.source_file, "r") as source_file:
        for n, line in enumerate(source_file):
            try:
                new_line = from_bad_name_to_good(line)
                if args.transliteration:
                    new_line = transliterate(new_line).lower()
                result.append(new_line)
            except IndexError:
                print(f"Something wrong with {n+1} line ({repr(line)})")
    
    
    if not args.off_generator:
        with open(args.to, "w") as out_file:
            for line in result:
                out_file.write(line)


if __name__ == "__main__":
    main()
