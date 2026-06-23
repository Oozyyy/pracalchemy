from sqlalchemy import create_engine, ForeignKey, String, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


engine = create_engine("sqlite:///library.db", echo=True)

print("Созданный Engine")
print(engine)



SessionLocal = sessionmaker(bind=engine)



class Base(DeclarativeBase):
    pass



class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    birth_year: Mapped[int] = mapped_column(Integer, nullable=False)

    def __repr__(self) -> str:
        return f"Author(id={self.id}, name='{self.name}', birth_year={self.birth_year})"



class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))

    def __repr__(self) -> str:
        return f"Book(id={self.id}, title='{self.title}', year={self.year})"



def create_tables():
    Base.metadata.create_all(engine)