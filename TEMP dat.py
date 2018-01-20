
while True:
        
    try:
            
        import pickle

        file_name = input('Name: ')

        read_file = open(file_name + '.txt', 'r')
        info = eval(read_file.read())

        write_file = open(file_name, 'wb')
        pickle.dump(info, write_file)

        write_file.close()
        read_file.close()
        quit()


    except Exception as error:

        print(error)
        input()
