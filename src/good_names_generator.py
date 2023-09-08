from argparse import ArgumentParser
from sys import stdin


def add_email_prefix(line: str, postfix: str = "@telesales-service.org") -> str:
    return f"{line}{postfix}"


def transliterate(string):
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
        string = string.replace(key, _dict[key])
    return string 


def generate_cert_name(name: [str], transliteration: bool = True) -> str:
    if transliteration:
        name = transliterate(name)
    separated_name = name.split() 
    separated_name_length = len(separated_name)
    surname = separated_name[0]
    name = separated_name[1]
    if separated_name_length >= 3: 
        patronymic = separated_name[2]
        return f"{surname}.{name[0]}.{patronymic[0]}".lower()
    else:
        return f"{surname}.{name[0]}".lower()


def emails(argparse_arguments):
    result = []
    if stdin.isatty():
        try:
            inputfile = open(argparse_arguments.inputfile, "r", encoding=argparse_arguments.encoding)
        except FileNotFoundError:
            print(f"File {argparse_arguments.inputfile} does not exists")
        try:
            for n, line in enumerate(inputfile):
                result.append(add_email_prefix(generate_cert_name(line)) + "\n")
        except IndexError:
            print(f"Something wrong with {n+1} line ({repr(line)})")
        inputfile.close()
    if not stdin.isatty():
        for line in stdin:
            result.append(add_email_prefix(generate_cert_name(line)) + "\n")
    result = set(result)

    if not argparse_arguments.disable_generator:
        try:
            if argparse_arguments.append_to_outputfile:
                outputfile = open(argparse_arguments.outputfile, "a", encoding=argparse_arguments.encoding)
            else:
                outputfile = open(argparse_arguments.outputfile, "w", encoding=argparse_arguments.encoding)
        except Exception as e:
            raise e
        for line in result:
            outputfile.write(line)
        outputfile.close()
    if argparse_arguments.enable_printing:
        for line in result:
            print(repr(line))


def certnames(argparse_arguments):
    result = []
    if stdin.isatty():
        try:
            inputfile = open(argparse_arguments.inputfile, "r", encoding=argparse_arguments.encoding)
        except FileNotFoundError:
            print(f"File {argparse_arguments.inputfile} does not exists")
        try:
            for n, line in enumerate(inputfile):
                result.append(generate_cert_name(line) + "\n")
        except IndexError:
            print(f"Something wrong with {n+1} line ({repr(line)})")
        inputfile.close()
    if not stdin.isatty():
        for line in stdin:
            result.append(generate_cert_name(line) + "\n")
    result = set(result)

    if not argparse_arguments.disable_generator:
        try:
            if argparse_arguments.append_to_outputfile:
                outputfile = open(argparse_arguments.outputfile, "a", encoding=argparse_arguments.encoding)
            else:
                outputfile = open(argparse_arguments.outputfile, "w", encoding=argparse_arguments.encoding)
        except Exception as e:
            raise e
        for line in result:
            outputfile.write(line)
        outputfile.close()
    if argparse_arguments.enable_printing:
        for line in result:
            print(repr(line))


parser = ArgumentParser("Good names generator")


commands = parser.add_subparsers()
generator = commands.add_parser("generate")
generator_commands = generator.add_subparsers()


parser_certnames = generator_commands.add_parser("certnames")
parser_certnames.add_argument("--from", dest="inputfile", help="Path to file with names")
parser_certnames.add_argument("--to", dest="outputfile", help="Path to output file (Will be generated if does not exist)")
parser_certnames.add_argument("-dg", "--disable-generator", action="store_true", help="Path to output file (Will be generated if does not exist)")
parser_certnames.add_argument("-a", "--append", dest="append_to_outputfile", action="store_true", help="Path to output file (Will be generated if does not exist)")
parser_certnames.add_argument("-p", "--printing", dest="enable_printing", action="store_true", help="Path to output file (Will be generated if does not exist)")
parser_certnames.add_argument("--encoding", type=str, default="utf-8", help="Path to output file (Will be generated if does not exist)")
parser_certnames.set_defaults(func=certnames)


parser_emails = generator_commands.add_parser("emails")
parser_emails.add_argument("--from", dest="inputfile", help="Path to file with names")
parser_emails.add_argument("--to", dest="outputfile", help="Path to output file (Will be generated if does not exist)")
parser_emails.add_argument("-dg", "--disable-generator", action="store_true", help="Path to output file (Will be generated if does not exist)")
parser_emails.add_argument("-a", "--append", dest="append_to_outputfile", action="store_true", help="Path to output file (Will be generated if does not exist)")
parser_emails.add_argument("-p", "--printing", dest="enable_printing", action="store_true", help="Path to output file (Will be generated if does not exist)")
parser_emails.add_argument("--encoding", type=str, default="utf-8", help="Path to output file (Will be generated if does not exist)")
parser_emails.set_defaults(func=emails)


args = parser.parse_args()
args.func(args)
