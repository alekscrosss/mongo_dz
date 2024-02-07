from models import Author, Quote
import redis
import re

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)


def search_quotes():
    while True:
        command = input("Enter your command: ")
        if command == "exit":
            break

        if ":" not in command:
            print("Invalid command format. Please use 'cmd:value'.")
            continue

        cmd, value = command.split(":", 1)
        value = value.strip()
        cache_key = f"{cmd}:{value}"

        if r.exists(cache_key):
            print(f"Retrieving from cache: {cache_key}")
            print(r.get(cache_key))
            continue

        if cmd == "name":

            authors = Author.objects(fullname__icontains=value)
            if not authors:
                print("Author not found.")
                continue

            quotes = Quote.objects(author__in=[author.id for author in authors])
        elif cmd == "tag":
            regex = re.compile(f".*{value}.*", re.IGNORECASE)
            quotes = Quote.objects(tags=regex)
        else:
            print("Unknown command.")
            continue

        if quotes:
            result = '\n'.join([f"{quote.quote} - {quote.author.fullname}" for quote in quotes])
            print(result)

            r.set(cache_key, result)
        else:
            print("No quotes found.")
            r.set(cache_key, "No quotes found.")


if __name__ == "__main__":
    search_quotes()
