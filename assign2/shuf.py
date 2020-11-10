#!/usr/bin/python
import argparse 
import random, sys

class shuf:
    def __init__(self, filename):
        f = open(filename, 'r')
        self.lines = f.readlines()
        self.num_lines = len(self.lines)
        f.close()
    def getline(self, line_no):
        return self.lines[line_no]
    
    def chooseline(self):
        return random.choice(self.lines)

def main():
    descript_msg = """%prog [OPTION... FILE Output randomly selected lines from FILE."""

    parser = argparse.ArgumentParser(description = descript_msg)
    # file
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    
    # numlines
    parser.add_argument("-n", "--head-count", action="store", dest="numlines", default=-1, help="output NUMLINES lines (default 1)")

    # echo
    parser.add_argument("-e", "--echo", action="append", nargs='+', dest="echo", default=[], help="Treat each ARG as an input line\n")
    
    # repeat
    parser.add_argument("-r", "--repeat", action="store_true", dest="replace", default=False, help="Repeat output values, that is, select with replacement\n")

    # input-range
    parser.add_argument("-i", "--input-range", action="store", dest="input_range", default=None, type=str, help="Act as if input came from a file containing the range of unsigned decimal integers lo...hi, one per line\n")
    
    args = parser.parse_args(sys.argv[1:])
    
    
    numline_set = True
    # for numlines
    try:
        if args.numlines != -1: # -n flag is used
            numlines = int(args.numlines)
        else:
            numlines = 1
            numline_set = False
    except:
        parser.error("invalid NUMLINES: {0}".format(args.numlines))
    if numlines < 0:
        parser.error("negative count: {0}".format(args.numlines))

    input_file = args.infile.name
    
    # for echo
    if args.echo != []:
        if args.input_range == '':
            parser.error('cannot combine -e and -i options')
        words = args.echo[0]
        if args.infile.name != '<stdin>':
            words.append(args.infile.name)
        lines = []

        # replace
        if args.replace == True:
            if not numline_set:
                while(True):
                    word = random.choice(words)
                    sys.stdout.write(f'{word}\n')
            else:
                while(numlines > 0):
                    word = random.choice(words)
                    sys.stdout.write(f'{word}\n')
                    numlines -= 1
                sys.exit()
        
        # no replace
        if numline_set:
            if numlines > len(words):
                lines = random.sample(range(len(words)), len(words))
            else:
                lines = random.sample(range(len(words)), numlines)
            
            for line in lines:
                sys.stdout.write(f'{words[line]}\n')
            sys.exit()
        else:
            lines = random.sample(range(len(words)), len(words))
        
        for line in lines:
            sys.stdout.write(f'{words[line]}\n')
        sys.exit()
    
    # for input-range
    if args.input_range != None:
        if args.infile.name != '<stdin>' or args.echo != []:
            parser.error("extra operand")
        num_range = args.input_range.split("-")
        if len(num_range) != 2:
            parser.error("invalid input range")
        try:
            lo = int(num_range[0])
        except:
            parser.error(f"invalid input range '{num_range[0]}'")
        try:
            hi = int(num_range[1])
        except:
            parser.error(f"invalid input range '{num_range[1]}'")

        if lo > hi :
            parser.error(f"invalid range {lo}-{hi}")

        nums = [x for x in range(lo, hi+1)]
        lines = []
        
        # replace
        if args.replace == True:
            if not numline_set:
                while(True):
                    num = random.choice(nums)
                    sys.stdout.write(f'{num}\n')
            else:
                while(numlines > 0):
                    num = random.choice(nums)
                    sys.stdout.write(f'{num}\n')
                    numlines -= 1
                sys.exit()

        # no replace
        if numline_set:
            if numlines > len(nums):
                lines = random.sample(range(len(nums)), len(nums))
            else:
                lines = random.sample(range(len(nums)), numlines)
        else:
            lines = random.sample(range(len(nums)), len(nums))
        
        for line in lines:
            sys.stdout.write(f"{nums[line]}\n")
        sys.exit()

    # no replacement
    try:
        generator = shuf(input_file)
        lines = []

        # replace
        if args.replace == True:
            if not numline_set:
                while(True):
                    sys.stdout.write(generator.chooseline())
            else:
                while(numlines > 0):
                    sys.stdout.write(generator.chooseline())
                    numlines -= 1
                sys.exit()

        # no replace
        if numlines > generator.num_lines:
            lines = random.sample(range(generator.num_lines), generator.num_lines)
        else:
            lines = random.sample(range(generator.num_lines), numlines)

        for line in lines:
            sys.stdout.write(generator.getline(line))
    except IOError as err:
        parser.error("I/O error({0}): {1}". format(err.errno, err.strerror))

if __name__ == "__main__":
    main()
