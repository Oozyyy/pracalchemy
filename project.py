from sqlalchemy import func, select
from database import engine, create_tables, SessionLocal, Author, Book


create_tables()


with SessionLocal() as session:
    print("\nНАЧАЛО ОПЕРАЦИЙ\n")


    if session.scalar(select(func.count(Author.id))) == 0:
        author1 = Author(name="Джордж Оруэлл", birth_year=1903)
        author2 = Author(name="Лев Толстой", birth_year=1828)
        author3 = Author(name="Фёдор Достоевский", birth_year=1821)

        session.add_all([author1, author2, author3])
        session.flush()  

        books = [
            Book(title="1984", year=1949, author_id=author1.id),
            Book(title="Скотный двор", year=1945, author_id=author1.id),
            Book(title="Война и мир", year=1869, author_id=author2.id),
            Book(title="Преступление и наказание", year=1866, author_id=author3.id),
            Book(title="Идиот", year=1869, author_id=author3.id),
        ]
        session.add_all(books)
        session.commit()
        print("[Инфо]: Базовые данные успешно добавлены.")


    print("\n-> Имена всех авторов:")
    authors = session.scalars(select(Author)).all()
    for author in authors:
        print(author.name)


    print("\n-> Изменение имени автора...")
    author_to_update = session.scalars(
        select(Author).where(Author.name == "Лев Толстой")
    ).first()
    if author_to_update:
        author_to_update.name = "Лев Николаевич Толстой"
        session.commit()
        print(f"[Инфо]: Имя изменено на: {author_to_update.name}")


    print("\n-> Удаление одной книги...")
    book_to_delete = session.scalars(
        select(Book).where(Book.title == "Скотный двор")
    ).first()
    if book_to_delete:
        session.delete(book_to_delete)
        session.commit()
        print(f"[Инфо]: Книга '{book_to_delete.title}' успешно удалена.")


    print("\n-> Книги, отсортированные по году (от новых к старым):")
    stmt_sort = select(Book).order_by(Book.year.desc())
    for book in session.scalars(stmt_sort):
        print(f"{book.title} ({book.year})")


    print("\n-> Книги, изданные после 1950 года:")
    stmt_after_1950 = select(Book).where(Book.year > 1950)
    books_after_1950 = session.scalars(stmt_after_1950).all()
    if books_after_1950:
        for book in books_after_1950:
            print(f"{book.title} ({book.year})")
    else:
        print("Таких книг в базе нет.")


    target_name = "Джордж Оруэлл"
    print(f"\n-> Поиск автора по имени '{target_name}':")
    author_by_name = session.scalars(
        select(Author).where(Author.name == target_name)
    ).first()
    print(author_by_name)


    print("\n-> Общее количество книг в базе:")
    total_books = session.scalar(select(func.count(Book.id)))
    print(f"Количество книг: {total_books}")


    print("\n-> Первые 3 книги в алфавитном порядке:")
    stmt_alpha = select(Book).order_by(Book.title).limit(3)
    for book in session.scalars(stmt_alpha):
        print(book.title)