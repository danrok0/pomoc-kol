const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');

const app = express();
app.use(express.static(__dirname));
app.use(express.json());

const db = new sqlite3.Database('./platforma.db');

// TWORZENIE STRUKTURY BAZY DANYCH
db.serialize(() => {
    // Tabela autoryzacji (nie wlicza się do limitu 4)
    db.run("CREATE TABLE IF NOT EXISTS uzytkownicy (id INTEGER PRIMARY KEY, login TEXT UNIQUE, haslo TEXT, rola TEXT)");
    
    // Tabele domenowe (Minimum 4, mamy 6)
    db.run("CREATE TABLE IF NOT EXISTS kategorie (id INTEGER PRIMARY KEY, nazwa TEXT)");
    db.run("CREATE TABLE IF NOT EXISTS tagi (id INTEGER PRIMARY KEY, nazwa TEXT)");
    
    // Związek 1:N (Kategoria -> Kursy)
    db.run("CREATE TABLE IF NOT EXISTS kursy (id INTEGER PRIMARY KEY, nazwa TEXT, cena REAL, kategoria_id INTEGER, FOREIGN KEY(kategoria_id) REFERENCES kategorie(id))");
    
    // Związek N:M (Kursy <-> Tagi)
    db.run("CREATE TABLE IF NOT EXISTS kursy_tagi (kurs_id INTEGER, tag_id INTEGER, FOREIGN KEY(kurs_id) REFERENCES kursy(id), FOREIGN KEY(tag_id) REFERENCES tagi(id))");
    
    // Tabele dla funkcjonalności nietrywialnej (Zamówienie i jego pozycje - relacja 1:N)
    db.run("CREATE TABLE IF NOT EXISTS zamowienia (id INTEGER PRIMARY KEY, uzytkownik_id INTEGER, data TEXT, suma REAL, FOREIGN KEY(uzytkownik_id) REFERENCES uzytkownicy(id))");
    db.run("CREATE TABLE IF NOT EXISTS pozycje_zamowienia (id INTEGER PRIMARY KEY, zamowienie_id INTEGER, kurs_id INTEGER, FOREIGN KEY(zamowienie_id) REFERENCES zamowienia(id), FOREIGN KEY(kurs_id) REFERENCES kursy(id))");

    // Dane startowe - Konta do logowania
    db.run("INSERT OR IGNORE INTO uzytkownicy (login, haslo, rola) VALUES ('admin', 'admin123', 'admin'), ('klient', 'klient123', 'user')");
    db.run("INSERT OR IGNORE INTO kategorie (id, nazwa) VALUES (1, 'Programowanie'), (2, 'Biznes i Marketing')");
});

// --- 1. SYSTEM AUTORYZACJI (LOGOWANIE) ---
app.post('/api/login', (req, res) => {
    const { login, haslo } = req.body;
    db.get("SELECT id, login, rola FROM uzytkownicy WHERE login = ? AND haslo = ?", [login, haslo], (err, row) => {
        if (row) {
            res.json({ success: true, user: row }); // Zwraca dane użytkownika po udanym logowaniu
        } else {
            res.status(401).json({ success: false, message: "Nieprawidłowy login lub hasło." });
        }
    });
});

// --- 2. PANEL ADMINISTRATORA (PEŁNY CRUD KURSÓW) ---
app.get('/api/kursy', (req, res) => {
    const sql = `SELECT k.id, k.nazwa, k.cena, k.kategoria_id, kat.nazwa as kategoria_nazwa 
                 FROM kursy k JOIN kategorie kat ON k.kategoria_id = kat.id`;
    db.all(sql, [], (err, rows) => res.json(rows || []));
});

app.post('/api/kursy', (req, res) => {
    const { nazwa, cena, kategoria_id } = req.body;
    db.run("INSERT INTO kursy (nazwa, cena, kategoria_id) VALUES (?, ?, ?)", [nazwa, cena, kategoria_id], function(err) {
        if (err) return res.status(500).json({ error: err.message });
        res.json({ komunikat: "Dodano kurs" });
    });
});

app.put('/api/kursy/:id', (req, res) => {
    const { nazwa, cena } = req.body;
    db.run("UPDATE kursy SET nazwa = ?, cena = ? WHERE id = ?", [nazwa, cena, req.params.id], () => {
        res.json({ komunikat: "Zaktualizowano kurs" });
    });
});

app.delete('/api/kursy/:id', (req, res) => {
    db.run("DELETE FROM pozycje_zamowienia WHERE kurs_id = ?", req.params.id); // Usunięcie powiązań
    db.run("DELETE FROM kursy WHERE id = ?", req.params.id, () => {
        res.json({ komunikat: "Usunięto kurs" });
    });
});

// --- 3. AKCJA NIETRYWIALNA UŻYTKOWNIKA (Złożenie zamówienia z koszyka) ---
app.post('/api/zamowienia', (req, res) => {
    const { uzytkownik_id, koszyk, suma } = req.body;
    const dataZamowienia = new Date().toISOString();
    
    // Zapisujemy nagłówek zamówienia
    db.run("INSERT INTO zamowienia (uzytkownik_id, data, suma) VALUES (?, ?, ?)", [uzytkownik_id, dataZamowienia, suma], function(err) {
        if (err) return res.status(500).json({ error: err.message });
        
        const zamowienieId = this.lastID;
        
        // Zapisujemy każdą pozycję z koszyka
        const stmt = db.prepare("INSERT INTO pozycje_zamowienia (zamowienie_id, kurs_id) VALUES (?, ?)");
        koszyk.forEach(item => {
            stmt.run([zamowienieId, item.id]);
        });
        stmt.finalize();

        res.json({ success: true, message: "Zamówienie złożone pomyślnie!" });
    });
});

app.listen(3000, () => console.log("Serwer działa na porcie 3000!"));
