from argparse import ArgumentParser

parser = ArgumentParser(
    prog="good_names_generator",
)

parser.add_argument("--from", default="list.txt", dest="source_file", type=str, help="Path to txt file with input names")
parser.add_argument("--to", default="list.txt", type=str, help="Path to file with generated results")
parser.add_argument("-og", "--off-generator", action="store_true", help="Off generating files")

args = parser.parse_args()

def from_bad_name_to_good(name: str) -> str:
    separated_name = name.split()
    surname, name, patronymic = separated_name[0], separated_name[1], separated_name[2]
    return f"{surname}.{name[0]}.{patronymic[0]}\n"
    

if __name__ == "__main__":
    result = []
    
    with open(args.source_file, "r") as source_file:
        for n, line in enumerate(source_file):
            try:
                result.append(from_bad_name_to_good(line))
            except IndexError:
                print(f"Something wrong with {n+1} line ({repr(line)})")
    
    
    if not args.off_generator:
        with open(args.to, "w") as out_file:
            for line in result:
                out_file.write(line)
