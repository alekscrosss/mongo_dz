import json
from models import Author, Quote


def load_authors(filename='authors.json'):
    with open(filename, 'r', encoding='utf-8') as file:
        authors_data = json.load(file)
        for author_data in authors_data:
            author = Author.objects(fullname=author_data['fullname']).first()
            if not author:  #
                author = Author(**author_data)
                author.save()
            else:
                for key, value in author_data.items():
                    setattr(author, key, value)
                author.save()


def load_quotes(filename='qoutes.json'):
    with open(filename, 'r', encoding='utf-8') as file:
        quotes_data = json.load(file)
        for quote_data in quotes_data:
            author = Author.objects(fullname=quote_data['author']).first()
            if author:
                quote_data.pop('author')
                Quote.objects.create(author=author, **quote_data)


if __name__ == "__main__":
    load_authors()
    load_quotes()
