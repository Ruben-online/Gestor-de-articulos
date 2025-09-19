class Article:
    def __init__(self, hash_value, title, authors, year, filename):
        self.hash_value = hash_value
        self.title = title
        self.authors = authors
        self.year = year
        self.filename = filename

    def to_record(self):
        return f"{self.hash_value}|{self.title}|{self.authors}|{self.year}|{self.filename}"

    @staticmethod
    def from_record(record_line):
        parts = record_line.strip().split("|")
        if len(parts) != 5:
            return None
        return Article(*parts)


class HashTable:
    def __init__(self):
        self.table = {}
        self.author_index = {}  # Índice por autor
        self.year_index = {}    # Índice por año

    def insert(self, article):
        """Insertar articulo y actualizar indices secundarios"""
        self.table[article.hash_value] = article

        # Actualizar indice por autor
        for author in article.authors.split(","):
            author = author.strip()
            if author not in self.author_index:
                self.author_index[author] = []
            if article not in self.author_index[author]:
                self.author_index[author].append(article)

        # Actualizar indice por año
        if article.year not in self.year_index:
            self.year_index[article.year] = []
        if article not in self.year_index[article.year]:
            self.year_index[article.year].append(article)

    def delete(self, hash_value):
        """Eliminar articulo y actualizar indices secundarios"""
        article = self.table.pop(hash_value, None)
        if not article:
            return

        # Eliminar de autor_index
        for author in article.authors.split(","):
            author = author.strip()
            if author in self.author_index:
                self.author_index[author] = [a for a in self.author_index[author] if a.hash_value != hash_value]
                if not self.author_index[author]:
                    del self.author_index[author]

        # Eliminar de year_index
        if article.year in self.year_index:
            self.year_index[article.year] = [a for a in self.year_index[article.year] if a.hash_value != hash_value]
            if not self.year_index[article.year]:
                del self.year_index[article.year]

    def get_articles_by_author(self, author):
        """Devolver lista de articulos de un autor"""
        return self.author_index.get(author.strip(), [])

    def get_articles_by_year(self, year):
        """Devolver lista de articulos de un año"""
        return self.year_index.get(year.strip(), [])

    def get_all_articles(self):
        return list(self.table.values())

    def search(self, hash_value):
        return self.table.get(hash_value, None)
