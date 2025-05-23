class Book:
    def __init__(self, book_id, isbn, title, author, publisher, publication_year,
                 category, total_copies, available_copies, shelf_location, added_by, added_on=None):
        ...

        self.book_id = book_id
        self.isbn = isbn
        self.title = title
        self.author = author
        self.publisher = publisher
        self.publication_year = publication_year
        self.category = category
        self.total_copies = total_copies
        self.available_copies = available_copies
        self.shelf_location = shelf_location
        self.added_by = added_by

    def to_dict(self):
        return self.__dict__
