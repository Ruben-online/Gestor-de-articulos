import os
import shutil
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton,
    QLabel, QFileDialog, QMessageBox, QInputDialog
)
from core.hash_utils import fnv1a_hash
from core.hash_table import Article, HashTable

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestor de Artículos Científicos")
        self.resize(600, 500)

        # Tabla hash en memoria
        self.hash_table = HashTable()

        # Archivo base de datos
        self.db_file = "articulos_db.txt"

        # Variables temporales
        self.title_input = QLineEdit()
        self.author_input = QLineEdit()
        self.year_input = QLineEdit()
        self.file_label = QLabel("Ningún archivo seleccionado")
        self.file_path = None

        # Cargar base de datos
        self.load_database()

        # Configurar interfaz
        self.setup_ui()

    # -------------------------
    # Interfaz y UI
    # -------------------------
    def setup_ui(self):
        self.title_input.setPlaceholderText("Ingrese el título del artículo")
        self.author_input.setPlaceholderText("Ingrese el/los autor(es)")
        self.year_input.setPlaceholderText("Ingrese el año de publicación")
        self.title_input.setMinimumHeight(30)
        self.author_input.setMinimumHeight(30)
        self.year_input.setMinimumHeight(30)

        # Botones
        self.file_button = QPushButton("Seleccionar archivo (.txt)")
        self.save_button = QPushButton("Guardar artículo")
        self.edit_button = QPushButton("Editar artículo")
        self.delete_button = QPushButton("Eliminar artículo")
        self.list_button = QPushButton("Listar artículos")
        self.search_index_button = QPushButton("Buscar rápido (autor/año)")

        for btn in [self.file_button, self.save_button, self.edit_button, self.delete_button, self.list_button, self.search_index_button]:
            btn.setMinimumHeight(35)

        # Conexiones
        self.file_button.clicked.connect(self.select_file)
        self.save_button.clicked.connect(self.save_article)
        self.edit_button.clicked.connect(self.edit_article)
        self.delete_button.clicked.connect(self.delete_article)
        self.list_button.clicked.connect(self.list_articles)
        self.search_index_button.clicked.connect(self.search_by_author_or_year)

        # Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        layout.addWidget(QLabel("Título:"))
        layout.addWidget(self.title_input)
        layout.addWidget(QLabel("Autor(es):"))
        layout.addWidget(self.author_input)
        layout.addWidget(QLabel("Año:"))
        layout.addWidget(self.year_input)
        layout.addWidget(self.file_button)
        layout.addWidget(self.file_label)
        layout.addWidget(self.save_button)
        layout.addWidget(self.edit_button)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.list_button)
        layout.addWidget(self.search_index_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Estilos
        self.setStyleSheet("""
            QWidget { font-family: Arial; font-size: 14px; }
            QLineEdit { border: 1px solid #aaa; border-radius: 8px; padding: 5px; }
            QPushButton { background-color: #0078d7; color: white; border-radius: 8px; padding: 6px; }
            QPushButton:hover { background-color: #005a9e; }
            QLabel { font-weight: bold; }
        """)

    # -------------------------
    # Base de datos
    # -------------------------
    def load_database(self):
        """Cargar articulos desde articulos_db.txt a la tabla hash en memoria"""
        try:
            with open(self.db_file, "r", encoding="utf-8") as f:
                for line in f:
                    article = Article.from_record(line)
                    if article:
                        self.hash_table.insert(article)
            print("Base de datos cargada correctamente.")
        except FileNotFoundError:
            print("No se encontró base de datos, se creará al guardar.")

    def save_database(self):
        """Guardar todos los articulos de la tabla hash en articulos_db.txt"""
        with open(self.db_file, "w", encoding="utf-8") as f:
            for article in self.hash_table.get_all_articles():
                f.write(article.to_record() + "\n")
        print("Base de datos actualizada.")

    # -------------------------
    # Interaccion
    # -------------------------
    def select_file(self):
        """Abrir explorador de archivos para seleccionar un .txt"""
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self,
            "Seleccionar archivo de artículo",
            "",
            "Archivos de texto (*.txt)"
        )
        if file_path:
            self.file_path = file_path
            self.file_label.setText(f"Archivo: {file_path}")

    def save_article(self):
        """Guardar articulo: leer archivo, calcular hash, verificar duplicados"""
        title = self.title_input.text().strip()
        authors = self.author_input.text().strip()
        year = self.year_input.text().strip()

        if not title or not authors or not year or not self.file_path:
            QMessageBox.warning(self, "Error", "Debe llenar todos los campos y seleccionar un archivo")
            return

        # Leer contenido del archivo
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo leer el archivo: {e}")
            return

        # Calcular hash FNV-1
        article_hash = fnv1a_hash(content)

        # Verificar duplicado
        if self.hash_table.search(article_hash):
            QMessageBox.information(self, "Duplicado", "Este artículo ya está registrado en el sistema.")
            return

        # Crear carpeta articles si no existe
        os.makedirs("articles", exist_ok=True)

        # Copiar archivo con nombre <hash>.txt
        new_filename = f"{article_hash}.txt"
        new_filepath = os.path.join("articles", new_filename)
        try:
            shutil.copy(self.file_path, new_filepath)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo copiar el archivo: {e}")
            return

        # Crear articulo y guardar en tabla hash
        article = Article(article_hash, title, authors, year, new_filename)
        self.hash_table.insert(article)

        # Guardar en base de datos
        self.save_database()

        # Mensajes de confirmacion
        QMessageBox.information(self, "Éxito", f"Artículo guardado con hash {article_hash}")
        print("=== Artículo guardado ===")
        print(article.to_record())

    # -------------------------
    # Gestión de articulos
    # -------------------------
    def edit_article(self):
        """Editar autor(es) o año de un artículo existente"""
        hash_input, ok = QInputDialog.getText(self, "Editar artículo", "Ingrese el hash del artículo:")
        if not ok or not hash_input.strip():
            return

        article = self.hash_table.search(hash_input.strip())
        if not article:
            QMessageBox.warning(self, "No encontrado", "No se encontró un artículo con ese hash.")
            return

        # Pedir nuevos valores
        new_authors, ok1 = QInputDialog.getText(self, "Editar autor(es)", "Autor(es):", text=article.authors)
        if not ok1: return
        new_year, ok2 = QInputDialog.getText(self, "Editar año", "Año:", text=article.year)
        if not ok2: return

        # Actualizar datos
        article.authors = new_authors.strip()
        article.year = new_year.strip()
        self.hash_table.insert(article)

        # Guardar cambios
        self.save_database()
        QMessageBox.information(self, "Éxito", f"Artículo {hash_input} actualizado.")

    def delete_article(self):
        """Eliminar un articulo existente"""
        hash_input, ok = QInputDialog.getText(self, "Eliminar artículo", "Ingrese el hash del artículo:")
        if not ok or not hash_input.strip():
            return

        hash_value = hash_input.strip()
        article = self.hash_table.search(hash_value)
        if not article:
            QMessageBox.warning(self, "No encontrado", "No se encontró un artículo con ese hash.")
            return

        # Confirmacion
        reply = QMessageBox.question(
            self,
            "Confirmar eliminación",
            f"¿Está seguro de eliminar el artículo '{article.title}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        # Borrar archivo
        try:
            os.remove(os.path.join("articles", article.filename))
        except Exception as e:
            print(f"No se pudo borrar archivo: {e}")

        # Borrar registro de tabla hash
        self.hash_table.delete(hash_value)

        # Guardar cambios
        self.save_database()
        QMessageBox.information(self, "Éxito", f"Artículo {hash_value} eliminado.")

    def list_articles(self):
        """Listar articulos por autor o titulo"""
        options = ["Autor", "Título"]
        choice, ok = QInputDialog.getItem(self, "Listar artículos", "Ordenar por:", options, 0, False)
        if not ok:
            return

        articles = self.hash_table.get_all_articles()
        if choice == "Autor":
            articles.sort(key=lambda x: x.authors.lower())
        else:
            articles.sort(key=lambda x: x.title.lower())

        text = "\n".join([f"Hash: {a.hash_value} | Título: {a.title} | Autor(es): {a.authors} | Año: {a.year}" for a in articles])
        if not text:
            text = "No hay artículos guardados."

        # Mostrar en ventana
        msg = QMessageBox(self)
        msg.setWindowTitle(f"Artículos ordenados por {choice}")
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()

    def search_by_author_or_year(self):
        """Buscar articulos usando indices secundarios"""
        options = ["Autor", "Año"]
        choice, ok = QInputDialog.getItem(self, "Buscar artículos", "Buscar por:", options, 0, False)
        if not ok: return

        query, ok2 = QInputDialog.getText(self, f"Buscar por {choice}", f"Ingrese {choice}:")
        if not ok2 or not query.strip(): return
        query = query.strip()

        if choice == "Autor":
            articles = self.hash_table.get_articles_by_author(query)
        else:
            articles = self.hash_table.get_articles_by_year(query)

        text = "\n".join([f"Hash: {a.hash_value} | Título: {a.title} | Autor(es): {a.authors} | Año: {a.year}" for a in articles])
        if not text:
            text = "No se encontraron artículos."

        msg = QMessageBox(self)
        msg.setWindowTitle(f"Resultados por {choice}: {query}")
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()
