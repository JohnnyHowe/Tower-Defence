import os

def list_files(dir):
    r = []
    for root, dirs, files in os.walk(dir):
        for name in files:
            r.append(os.path.join(root, name))
    return r

print('What file should I search?')
dir = input()

# Get all files
files = list_files(dir)

# Get all python files
python_files = []

for file_name in files:
    if file_name[len(file_name) - 4:] == '.pyw' or file_name[len(file_name) - 3:] == '.py':
        if not 'TEMP' in file_name:
            python_files.append(file_name)

# Get the length of each file
length = 0
length2 = 0

for file_name in python_files:
    contents = open(file_name, 'r').read()
    lines = contents.splitlines()
    length += len(lines)

    for line in lines:
        okay = True

        # Check if it's empty
        for char in line:

            if char != ' ':
                okay = False

        if okay:
            length2 += 1

length2 = length - length2


# Show
print(length, 'lines in', len(python_files), 'python files')
print(str(length2) + ' lines excluding blank ones')
input()
