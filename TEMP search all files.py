import os

def list_files(dir):
    r = []
    for root, dirs, files in os.walk(dir):
        for name in files:

            # Is it a python file?
            if name[len(name) - 3:] == '.py' or name[len(name) - 4:] == '.pyw':
                r.append(os.path.join(root, name))
    return r

# print('What file should I search?')
# dir = input()
# By defult dir will be data

# Get all files
files = list_files('data')

while True:

    print()
    print('What am I searching for?')
    s = input()

    instances = []
    for file in files:

        lines = open(file, 'r').read().splitlines()

        for index in range(len(lines)):
            line = lines[index]
            
            if s in line:
                instances.append((file, index + 1))


    for i in instances: print(i)
    print('Showing ' + str(len(instances)) + " instances of '" + s + "'")
