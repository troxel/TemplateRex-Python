# using groupby

from itertools import groupby
from operator import itemgetter

# list of dictionaries
my_list = [
	{'name': 'joao', 'birth': '20/10/1989'},
	{'name': 'maria', 'birth': '15/12/1993'},
	{'name': 'pedro', 'birth': '10/13/1991'},
	{'name': 'catarina', 'birth': '04/08/1980'},
	{'name': 'felipe', 'birth': '15/12/1993'},
	{'name': 'adriana', 'birth': '15/12/1993'},
	{'name': 'yankee', 'birth': '04/08/1980'}
]

# order by field birth
my_list.sort(key=itemgetter('birth'))

print(my_list)


# shows the groups by date of birth
for birth, items in groupby(my_list, key=itemgetter('birth')):
	print('Birth %s: %s' % (birth, ' '.join(item['name'] for item in items)))

