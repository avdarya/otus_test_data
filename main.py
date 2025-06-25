import json
import csv
import math
from pathlib import Path

base_dir = Path(__file__).resolve().parent
books_path = base_dir / 'books.csv'
users_path = base_dir / 'users.json'
result_path = base_dir / 'result.json'

books_left = 0
users_left = 0

with open(books_path, 'r') as books_file:
    books_reader = csv.reader(books_file)
    header = next(books_reader)
    books = []
    for row in books_reader:
        books.append(dict(zip(header, row)))
    books_left = len(books)

with open(users_path, 'r') as users_file:
    users = json.load(users_file)
    users_left = len(users)

avg_book_count = 0
book_index_offset = 0

result_data = []
for user in users:
    avg_book_count = math.ceil(books_left / users_left)
    books_left = books_left - avg_book_count
    users_left -= 1

    current_min_index = book_index_offset
    current_max_index = avg_book_count + book_index_offset

    books_for_user = [
        {
            'title': b.get('Title'),
            'author': b.get('Author'),
            'pages': b.get('Pages'),
            'genre': b.get('Genre'),
        }
        for b in books[current_min_index:current_max_index]
    ]

    result_data.append({
        'name': user.get('name'),
        'gender': user.get('gender'),
        'address': user.get('address'),
        'age': user.get('age'),
        'books': books_for_user,
    })

    book_index_offset += avg_book_count

with open(result_path, 'w') as result_file:
    result_file.write(json.dumps(result_data, indent=2))
