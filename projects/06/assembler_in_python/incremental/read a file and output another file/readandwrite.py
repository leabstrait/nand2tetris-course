
import sys

# Specifying the parameters
sys.argv = ['readandwrite.py', 'test.asm', 'testRW.asm']

# Open the .asm file and store it's lines in an array
assembly_file = open(sys.argv[1], 'r')
assembly_file_lines = assembly_file.readlines()
assembly_file.close()

# Open the .hack file and write the assembly file's lines into it
machine_file=open(sys.argv[2], 'w')
machine_file.writelines(assembly_file_lines)
machine_file.close()
