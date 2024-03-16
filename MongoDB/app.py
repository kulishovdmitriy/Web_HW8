from models import Author, Quote


def search_by_author(author: str):
    authors = Author.objects(fullname__iregex=author)
    result = {}
    for a in authors:
        quotes = Quote.objects(author=a)
        result[a.fullname] = [q.quote for q in quotes]
    return result


def search_by_tag(tag: str):
    quotes = Quote.objects(tags__iregex=tag)
    result = [q.quote for q in quotes]
    return result


def search_by_tags(tags):
    tags_list = tags.split(',')
    quotes = Quote.objects(tags__in=tags_list)
    return [quote.quote for quote in quotes]


if __name__ == '__main__':

    # while True:
    print("\nДоступные команды:")
    print("1. Поиск цитат по автору (формат: name: <автор>)")
    print("2. Поиск цитат по тегу (формат: tag: <тег>)")
    print("3. Поиск цитат по набору тегов (формат: tags: <тег1>,<тег2>,...)")
    print("4. Выход (exit)")
    while True:
        command = input("Введите команду: ").strip()

        if command.startswith("name:"):
            author = command.split("name:")[1].strip()
            print(search_by_author(author))
        elif command.startswith("tag:"):
            tag = command.split("tag:")[1].strip()
            print(search_by_tag(tag))
        elif command.startswith("tags:"):
            tags = command.split("tags:")[1].strip()
            print(search_by_tags(tags))
        elif command == "exit":
            print("Завершение работы скрипта.")
            break
        else:
            print("Неверный формат команды. Пожалуйста, введите команду в правильном формате.")
