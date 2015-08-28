import sys


RIGHT = 0
LEFT = 1
INC = 2
DEC = 3
LOOP_START = 4
LOOP_END = 5
GETC = 6
PUTC = 7


def compile_file(source_file):
    program_n = 0

    try:
        with open(source_file, "r") as f:
            eof = False
            while not eof:
                c = f.read(1)
                if len(c) == 0:
                    eof = True
                elif c == '.':
                    program_n += 1
    except IOError:
        print "Error: could not open file."
        sys.exit(1)

    binary = bin(program_n)[3:]

    if len(binary) % 3 != 0:
        print "Error: either you have too many or two few dots."
        sys.exit(1)

    program = []
    for i in xrange(0, len(binary), 3):
        b = binary[i:i+3]
        inst = int(b, 2)
        program.append(inst)

    return program


def match_loop(text, start):
    if text[start] == LOOP_START:
        stop = len(text)
        dir = 1
        search = LOOP_END
    elif text[start] == LOOP_END:
        stop = -1
        dir = -1
        search = LOOP_START
    else:
        raise ValueError('Incorrect number of dots.')
        return -1
    
    depth = 0
    
    for i in range(start, stop, dir):
        c = text[i]
        if c == LOOP_START:
            depth += 1
        elif c == LOOP_END:
            depth -= 1
        if c == search and depth == 0:
            return i
    return -1
    

def run(program):
    pc = 0

    mem = [0 for i in xrange(30000)]
    pointer = 0
            
    while pc < len(program):
        c = program[pc]
        old_pc = pc
        if c == RIGHT:
            pointer += 1
            pointer %= len(mem)
        elif c == LEFT:
            pointer -= 1
            pointer %= len(mem)
        elif c == INC:
            mem[pointer] += 1
            mem[pointer] %= 256
        elif c == DEC:
            mem[pointer] -= 1
            mem[pointer] %= 256
        elif c == PUTC:
            sys.stdout.write(chr(mem[pointer]))
        elif c == GETC:
            mem[pointer] = ord(sys.stdin.read(1))
        elif c == LOOP_START:
            if mem[pointer] == 0:
                pc = match_loop(program, pc)
                if pc < 0:
                    print "Error: either you have too many or two few dots."
                    break
        elif c == LOOP_END:
            if mem[pointer] != 0:
                pc = match_loop(program, pc)
                if pc < 0:
                    print "Error: either you have too many or two few dots."
                    break
        else:
            pass
        pc += 1
            

def main():
    if len(sys.argv) <= 1:
        print "usage: %s sourcefile" % sys.argv[0]
        sys.exit(1)

    source_file = sys.argv[1]
    program = compile_file(source_file)
    run(program)


if __name__ == "__main__":
    main()

