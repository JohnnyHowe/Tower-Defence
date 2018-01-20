import pickle

data = pickle.load(open('user_data', 'rb'))
data['level'] = 0
write_file = open('user_data', 'wb')
pickle.dump(data, write_file)
