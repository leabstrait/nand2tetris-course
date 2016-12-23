import sys

# Specifying the parameters
sys.argv = ['processeachline.py', 'Max.asm', 'Max.hack']

# Open the .asm file and store it's lines in a list
assembly_file = open(sys.argv[1], 'r')
assembly_file_lines = assembly_file.readlines()
assembly_file.close()


# Trim the whitespaces
def trim_whitespaces(aline):
    processing_chars = ""
    for char in aline:
        if not(char == ' '):
            processing_chars = processing_chars + char
    return processing_chars


# Trim the comments
def trim_comments(aline):
    processing_chars = aline
    for index, char in enumerate(aline):
        if aline[index] == '/' and aline[index+1] == '/':
            processing_chars = aline[:index] + '\n'
    return processing_chars 

# Make a new list without whitespaces and comments
processing_lines=[]
for lines in assembly_file_lines:
    lines = trim_comments(trim_whitespaces(lines))
    if lines != '\n':
        processing_lines.append(lines)

# Remove the extra new line at the end of processing_lines
#processing_lines[-1] = processing_lines[-1].strip('\n')

# Initialize an empty symbol table and append symbol->value tuples,
# first for predefined symbols. Tuples are used as they are immutable
symbol_table = []
symbol_table.append(('SP', 0))
symbol_table.append(('LCL', 1))
symbol_table.append(('ARG', 2))
symbol_table.append(('THIS', 3))
symbol_table.append(('THAT', 4))
symbol_table.append(('R0', 0))
symbol_table.append(('R1', 1))
symbol_table.append(('R2', 2))
symbol_table.append(('R3', 3))
symbol_table.append(('R4', 4))
symbol_table.append(('R5', 5))
symbol_table.append(('R6', 6))
symbol_table.append(('R7', 7))
symbol_table.append(('R8', 8))
symbol_table.append(('R9', 9))
symbol_table.append(('R10', 10))
symbol_table.append(('R11', 11))
symbol_table.append(('R12', 12))
symbol_table.append(('R13', 13))
symbol_table.append(('R14', 14))
symbol_table.append(('R15', 15))
symbol_table.append(('SCREEN', 16384))
symbol_table.append(('KBD', 24576))

# Address each instruction in processing_lines by creating a 2D-list
# Append label->new_address_of_next_instruction to the symbol table

addressing_lines = []
addressing_lines=list(enumerate(processing_lines))
address = 0
for not_needed, code in addressing_lines:
    if code[0] == '(':
        symbol_table.append((code[1:-2], address))
        processing_lines.remove(code)
        continue
    address +=1

# Regenerate updated addressing_lines from processing_lines
addressing_lines=list(enumerate(processing_lines))

# Search the symbol table if a symbol->value pairing exists
def find_value(symbol_table, symbol_to_find):
    for symbol, value in symbol_table:
        if symbol_to_find == symbol:
            return (True, value)
    return (False, 0)

# If exists symbol->value pairing, subtitute value to symbol in the code
# Else append symbol->value to the symbol table and substitute
address_of_variables = 16
for address, code in addressing_lines:
    found, value = find_value(symbol_table, code[1:-1])
# Use exception Handling used to check if the @instruction is a variable
# or a numerical address
    try:
        if_a_num = int(code[1:-1])
        num = True
    except:
        num = False
    if code[0] == '@':
        if found:
            processing_lines[address] = '@' + str(value) + '\n'
        if not num and not found:
            symbol_table.append((code[1:-1], address_of_variables))
            processing_lines[address] = '@' + str(address_of_variables) + '\n'
            address_of_variables = address_of_variables + 1

# Translate A-instructions and C-instructions

# First we need to convert numbers to 15-bit binary
# This is for A-instructions only
def convert_to_15_bit_binary(number):
    conversion = ''
    for i in range(15):
        remainder = number%2
        conversion += str(remainder)
        number=(number-remainder)/2
    return conversion[::-1]

#print processing_lines    
# The translation
counter = 0
for code in processing_lines:
    replacing_string = ''
    if code[0] == '@':                      # then it is an A-instruction
        replacing_string += '0'
        replacing_string += convert_to_15_bit_binary(int(code[1:]))
        replacing_string += '\n'
    else:                                   # then it is a C-instruction
        print '_____________________'
        print code
        replacing_string += '111'

        # Parsing the C-instructions, awful to look at but works
        if '=' in code:
            eq_index = code.index('=')
        else:
            eq_index = 0
        if ';' in code:
            semcol_index = code.index(';')
        else:
            semcol_index = code.index('\n')
        print 'eq_index', eq_index
        print 'semcol_index', semcol_index

        if '=' in code: 
            dest = code[:eq_index]
            comp = code[eq_index+1:semcol_index]
            jump = code[semcol_index:-2]

        if ';' in code:
            dest = code[:eq_index]
            comp = code[eq_index:semcol_index]
            jump = code[semcol_index+1:-1]
            
        print dest, 'EQUALS', comp, 'SEMCOL', jump
        print len(dest), len(comp), len(jump)

        # Encode the dest bits
        if dest == '' :     dest_code = '000'
        if dest == 'M' :    dest_code = '001'
        if dest == 'D' :    dest_code = '010'
        if dest == 'MD' :   dest_code = '011'
        if dest == 'A' :    dest_code = '100'
        if dest == 'AM' :   dest_code = '101'
        if dest == 'AD' :   dest_code = '110'
        if dest == 'AMD' :  dest_code = '111'
            
        # Encode the comp bits
        # # Hellisly long mapping table
        if comp == '0':    comp_code = '0101010'
        if comp == '1':    comp_code = '0111111'
        if comp == '-1' :   comp_code = '0111010'
        if comp == 'D' :    comp_code = '0001100'
        if comp == 'A' :    comp_code = '0110000'
        if comp == 'M' :    comp_code = '1110000'
        if comp == '!D' :   comp_code = '0001101'
        if comp == '!A' :   comp_code = '0110001'
        if comp == '!M' :   comp_code = '1110001'
        if comp == '-D' :   comp_code = '0001111'
        if comp == '-A' :   comp_code = '0110011'
        if comp == '-M' :   comp_code = '1110011'
        if comp == 'D+1' :  comp_code = '0011111'
        if comp == 'A+1' :  comp_code = '0110111'
        if comp == 'M+1' :  comp_code = '1110111'
        if comp == 'D-1' :  comp_code = '0001110'
        if comp == 'A-1' :  comp_code = '0110010'
        if comp == 'M-1' :  comp_code = '1110010'
        if comp == 'D+A' :  comp_code = '0000010'
        if comp == 'D+M' :  comp_code = '1000010'
        if comp == 'D-A' :  comp_code = '0010011'
        if comp == 'D-M' :  comp_code = '1010011'
        if comp == 'A-D' :  comp_code = '0000111'
        if comp == 'M-D' :  comp_code = '1000111'
        if comp == 'D&A' :  comp_code = '0000000'
        if comp == 'D&M' :  comp_code = '1000000'
        if comp == 'D|A' :  comp_code = '0010101'
        if comp == 'D|M' :  comp_code = '1010101'

        # Encode the jump bits
        if jump == '' :     jump_code = '000'
        if jump == 'JGT' :  jump_code = '001'
        if jump == 'JEQ' :  jump_code = '010'
        if jump == 'JGE' :  jump_code = '011'
        if jump == 'JLT' :  jump_code = '100'
        if jump == 'JNE' :  jump_code = '101'
        if jump == 'JLE' :  jump_code = '110'
        if jump == 'JMP' :  jump_code = '111'

        print dest_code, 'EQUALS', comp_code, 'SEMCOL', jump_code

        replacing_string += comp_code + dest_code + jump_code
        replacing_string += '\n' 

    processing_lines[counter] = replacing_string
    counter += 1

# Remove the extra new line at the end of processing_lines
#processing_lines[-1] = processing_lines[-1].strip('\n')
   
# Open the .hack file and write the processed assembly file's lines into it
machine_file=open(sys.argv[2], 'w')
machine_file.writelines(processing_lines)
machine_file.close()
