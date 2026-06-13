-- Tworzymy tabelę logowania (pomijana przy liczeniu wymogu 4 tabel)
CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, role TEXT);

-- Tabela 1: Kategorie
CREATE TABLE IF NOT EXISTS categories (id INTEGER PRIMARY KEY, name TEXT);

-- Tabela 2: Tagi
CREATE TABLE IF NOT EXISTS tags (id INTEGER PRIMARY KEY, name TEXT);

-- Tabela 3: Kursy (Związek 1:N z kategoriami - ma category_id)
CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY, 
    title TEXT, 
    category_id INTEGER, 
    FOREIGN KEY(category_id) REFERENCES categories(id)
);

-- Tabela 4: Łącznik kursów i tagów (Związek N:M)
CREATE TABLE IF NOT EXISTS course_tags (
    course_id INTEGER, 
    tag_id INTEGER, 
    FOREIGN KEY(course_id) REFERENCES courses(id), 
    FOREIGN KEY(tag_id) REFERENCES tags(id)
);

-- Tabela zapisów na kurs (Akcja nietrywialna użytkownika)
CREATE TABLE IF NOT EXISTS enrollments (
    id INTEGER PRIMARY KEY, 
    user_id INTEGER, 
    course_id INTEGER
);

-- Wrzucamy do bazy jakieś dane na start, żeby było co wyświetlać
INSERT INTO users (username, role) VALUES ('admin', 'admin'), ('Kowalski', 'user');
INSERT INTO categories (name) VALUES ('Programowanie'), ('Języki obce');
