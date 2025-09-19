# 📝 Gestor de Artículos Científicos

## 🌟 Descripción
Aplicación en **Python con PyQt6** para gestionar artículos científicos en `.txt`.  
Permite **cargar, almacenar, consultar, editar y eliminar artículos**, utilizando **tablas hash e índices secundarios** para búsquedas rápidas y detección de duplicados.

---

## 🚀 Funcionalidades
- **Agregar artículos:** título, autor(es), año y archivo `.txt`.  
- **Editar artículos:** modificar autor(es) o año usando hash.  
- **Eliminar artículos:** elimina archivo y registro en base de datos.  
- **Listar artículos:** por autor o título alfabéticamente.  
- **Búsquedas rápidas:** por autor o año usando índices secundarios.  
- **Gestión eficiente:** todas las operaciones en memoria, sincronización automática con `articulos_db.txt`.

---

## 📁 Estructura de archivos
- `main.py` → Ejecuta la aplicación  
- `articulos_db.txt` → Base de datos persistente  
- `articles/` → Carpeta de archivos `.txt` de los artículos  
- `gui/main_window.py` → Interfaz gráfica principal (PyQt6)  
- `core/hash_table.py` → Tabla hash y índices secundarios  
- `core/hash_utils.py` → Función de hash FNV-1a

---

## ⚙️ Requisitos
- Python 3.10+  
- PyQt6 (`pip install PyQt6`)

---

## ▶️ Ejecución
Ejecutar en terminal:

```bash
python main.py

---

## 📝 Uso rápido
- **Agregar artículo:** llenar título, autor(es), año y seleccionar archivo `.txt`. Presionar **Guardar artículo**.  
- **Editar artículo:** clic en **Editar artículo**, ingresar hash, modificar autor(es) y/o año.  
- **Eliminar artículo:** clic en **Eliminar artículo**, ingresar hash y confirmar.  
- **Listar artículos:** clic en **Listar artículos**, elegir criterio (Autor/Título).  
- **Buscar rápido:** clic en **Buscar rápido (autor/año)**, elegir criterio e ingresar valor.

---

## 🛠 Tecnologías
- **Python 3**  
- **PyQt6**  
- Tablas hash con encadenamiento  
- Índices secundarios por autor y año  
- Hash FNV-1a como identificador único  
- Persistencia en `articulos_db.txt`

---

## 💡 Ventajas
- Evita duplicados automáticamente  
- Búsquedas ultrarrápidas  
- Gestión completa y segura de artículos  
- Interfaz intuitiva y estética  
- Modular y escalable
