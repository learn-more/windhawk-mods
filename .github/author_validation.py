from optparse import OptionParser
from pathlib import Path


def add_warning(file: str, line: int):
    print(f'::warning file={file},line={line}::This is not the author of the PR!')


def parse_file(filename, expected_author):
    print(f'Searching {filename=} for {expected_author=}')
    for idx, line in enumerate(Path(filename).read_text().splitlines()):
        if not line.startswith('//'):
            continue
        line = line[2:].strip()
        if not line.startswith('@github'):
            continue
        line = line[7:].strip()
        if line != f'https://github.com/{expected_author}':
            add_warning(filename, idx + 1)

def main():
    parser = OptionParser()
    parser.add_option("--author", help="Specify the PR author")
    (options, args) = parser.parse_args()
    if not options.author:
        parser.error("Please specify the PR author")

    for filename in args:
        if filename.startswith('mods') and filename.endswith('.wh.cpp'):
            parse_file(filename, options.author)

if __name__ == '__main__':
    main()

