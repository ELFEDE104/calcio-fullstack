import pymysql
import sys
sys.path.append('../backend')
from config import TIDB_HOST, TIDB_PORT, TIDB_USER, TIDB_PASSWORD, TIDB_DATABASE

def get_connection():
    return pymysql.connect(
        host=TIDB_HOST,
        port=TIDB_PORT,
        user=TIDB_USER,
        password=TIDB_PASSWORD,
        database=TIDB_DATABASE,
        ssl_verify_cert=True,
        ssl_verify_identity=True,
    )

def crea_tabelle(cursor):
    print("Creazione tabelle...")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Stadio (
            id_stadio INTEGER PRIMARY KEY,
            citta VARCHAR(50) NOT NULL,
            capienza INTEGER NOT NULL,
            nome_stadio VARCHAR(50) NOT NULL UNIQUE,
            nome_squadra VARCHAR(50) NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Squadra (
            nome_squadra VARCHAR(50) PRIMARY KEY,
            capitano VARCHAR(50),
            ranking DECIMAL NOT NULL,
            presidente VARCHAR(30) NOT NULL,
            anno_fondazione DECIMAL NOT NULL,
            num_giocatori DECIMAL NOT NULL,
            trofei_vinti DECIMAL NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Sponsor (
            regione_sponsor VARCHAR(50) NOT NULL,
            nome_sponsor VARCHAR(50) PRIMARY KEY,
            nome_squadra VARCHAR(50) NOT NULL,
            anni_contratto INTEGER NOT NULL,
            FOREIGN KEY (nome_squadra) REFERENCES Squadra(nome_squadra)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Allenatore (
            id_allenatore INTEGER PRIMARY KEY,
            nome VARCHAR(50) NOT NULL,
            cognome VARCHAR(50) NOT NULL,
            eta INTEGER NOT NULL,
            nazionalita VARCHAR(50) NOT NULL,
            squadra VARCHAR(50) NOT NULL,
            trofei_vinti INTEGER NOT NULL,
            FOREIGN KEY (squadra) REFERENCES Squadra(nome_squadra)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS CentroAllenamento (
            id_centro INTEGER PRIMARY KEY,
            nome_squadra VARCHAR(50) NOT NULL,
            nome_centro VARCHAR(50) NOT NULL,
            citta VARCHAR(50) NOT NULL,
            num_campi INTEGER NOT NULL,
            FOREIGN KEY (nome_squadra) REFERENCES Squadra(nome_squadra)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Giocatore (
            id_giocatore INTEGER PRIMARY KEY,
            nome VARCHAR(50) NOT NULL,
            cognome VARCHAR(50) NOT NULL,
            eta INTEGER NOT NULL,
            ruolo VARCHAR(30) NOT NULL,
            squadra VARCHAR(50) NOT NULL,
            nazionalita VARCHAR(50) NOT NULL,
            num_maglia INTEGER NOT NULL,
            FOREIGN KEY (squadra) REFERENCES Squadra(nome_squadra)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Contratto (
            id_contratto INTEGER PRIMARY KEY,
            data_inizio DATE NOT NULL,
            data_fine DATE NOT NULL,
            id_giocatore INTEGER NOT NULL,
            stipendio DECIMAL NOT NULL,
            clausola_rescissoria DECIMAL,
            FOREIGN KEY (id_giocatore) REFERENCES Giocatore(id_giocatore)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Competizione (
            id_competizione INTEGER PRIMARY KEY,
            nome VARCHAR(50) NOT NULL,
            paese VARCHAR(50) NOT NULL,
            num_partite INTEGER NOT NULL,
            data_inizio DATE NOT NULL,
            data_fine DATE NOT NULL,
            tipo_palla VARCHAR(50)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Partita (
            id_partita INTEGER PRIMARY KEY,
            meteo VARCHAR(50) NOT NULL,
            orario_partita TIME NOT NULL,
            squadra VARCHAR(50) NOT NULL,
            squadra_ospite VARCHAR(50) NOT NULL,
            arbitro VARCHAR(50) NOT NULL,
            data_partita DATE NOT NULL,
            id_competizione INTEGER NOT NULL,
            giornata INTEGER NOT NULL,
            risultato INTEGER NOT NULL,
            nome_stadio VARCHAR(50) NOT NULL,
            FOREIGN KEY (squadra) REFERENCES Squadra(nome_squadra),
            FOREIGN KEY (squadra_ospite) REFERENCES Squadra(nome_squadra),
            FOREIGN KEY (id_competizione) REFERENCES Competizione(id_competizione),
            FOREIGN KEY (nome_stadio) REFERENCES Stadio(nome_stadio)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Convocazione (
            nome_squadra VARCHAR(50) NOT NULL,
            num_maglia INTEGER NOT NULL,
            id_partita INTEGER NOT NULL,
            id_giocatore INTEGER NOT NULL,
            PRIMARY KEY (num_maglia, nome_squadra),
            FOREIGN KEY (nome_squadra) REFERENCES Squadra(nome_squadra),
            FOREIGN KEY (id_partita) REFERENCES Partita(id_partita),
            FOREIGN KEY (id_giocatore) REFERENCES Giocatore(id_giocatore)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Infortunio (
            id_infortunio INTEGER PRIMARY KEY,
            tipo_infortunio VARCHAR(50) NOT NULL,
            data_infortunio DATE NOT NULL,
            giorni_prognosi INTEGER NOT NULL,
            parte_corpo VARCHAR(50) NOT NULL,
            causa VARCHAR(50) NOT NULL,
            id_giocatore INTEGER NOT NULL,
            id_partita INTEGER NOT NULL,
            FOREIGN KEY (id_giocatore) REFERENCES Giocatore(id_giocatore),
            FOREIGN KEY (id_partita) REFERENCES Partita(id_partita)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Eventi (
            id_evento INTEGER PRIMARY KEY,
            tipo_evento VARCHAR(50) NOT NULL,
            squadra VARCHAR(50) NOT NULL,
            id_giocatore INTEGER NOT NULL,
            id_partita INTEGER NOT NULL,
            FOREIGN KEY (squadra) REFERENCES Squadra(nome_squadra),
            FOREIGN KEY (id_giocatore) REFERENCES Giocatore(id_giocatore),
            FOREIGN KEY (id_partita) REFERENCES Partita(id_partita)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Classifica (
            id_competizione INTEGER PRIMARY KEY,
            stagione INTEGER NOT NULL,
            partite_giocate INTEGER NOT NULL,
            vittorie INTEGER NOT NULL,
            pareggi INTEGER NOT NULL,
            sconfitte INTEGER NOT NULL,
            gol_fatti INTEGER NOT NULL,
            gol_subiti INTEGER NOT NULL,
            differenza_reti INTEGER AS (gol_fatti - gol_subiti) VIRTUAL,
            FOREIGN KEY (id_competizione) REFERENCES Competizione(id_competizione)
        )
    """)

    print("✅ Tabelle create con successo!")


def popola_tabelle(cursor):
    print("Popolamento tabelle...")

    cursor.execute("""
        INSERT IGNORE INTO Stadio (id_stadio, citta, capienza, nome_stadio, nome_squadra) VALUES
        (1, 'Milano', 75923, 'San Siro', 'Inter'),
        (2, 'Milano', 75923, 'San Siro', 'AC Milan'),
        (3, 'Torino', 41507, 'Allianz Stadium', 'Juventus'),
        (4, 'Roma', 70634, 'Stadio Olimpico', 'AS Roma'),
        (5, 'Napoli', 54726, 'Stadio Diego Armando Maradona', 'Napoli'),
        (6, 'Firenze', 43147, 'Stadio Artemio Franchi', 'Fiorentina'),
        (7, 'Bergamo', 21747, 'Gewiss Stadium', 'Atalanta'),
        (8, 'Verona', 39211, 'Stadio Marcantonio Bentegodi', 'Hellas Verona'),
        (9, 'Genova', 36536, 'Stadio Luigi Ferraris', 'Genoa'),
        (10, 'Bologna', 38279, 'Stadio Renato Dall Ara', 'Bologna'),
        (11, 'Torino', 27958, 'Stadio Olimpico Grande Torino', 'Torino FC'),
        (12, 'Roma', 70634, 'Stadio Olimpico', 'Lazio'),
        (13, 'Udine', 25144, 'Dacia Arena', 'Udinese'),
        (14, 'Venezia', 11150, 'Stadio Pier Luigi Penzo', 'Venezia'),
        (15, 'Empoli', 19847, 'Stadio Carlo Castellani', 'Empoli'),
        (16, 'Lecce', 33876, 'Stadio Via del Mare', 'Lecce'),
        (17, 'Cagliari', 16416, 'Unipol Domus', 'Cagliari'),
        (18, 'Como', 13602, 'Stadio Giuseppe Sinigaglia', 'Como'),
        (19, 'Parma', 22352, 'Stadio Ennio Tardini', 'Parma'),
        (20, 'Monza', 18568, 'Stadio Brianteo', 'Monza'),
        (21, 'Reggio Emilia', 21525, 'Mapei Stadium', 'Sassuolo'),
        (22, 'Salerno', 23000, 'Stadio Arechi', 'Salernitana'),
        (23, 'Frosinone', 16227, 'Stadio Benito Stirpe', 'Frosinone'),
        (24, 'Cremona', 20750, 'Stadio Giovanni Zini', 'Cremonese'),
        (25, 'Spezia', 10336, 'Stadio Alberto Picco', 'Spezia'),
        (26, 'Pisa', 23176, 'Arena Garibaldi', 'Pisa'),
        (27, 'Palermo', 36349, 'Stadio Renzo Barbera', 'Palermo'),
        (28, 'Bari', 58270, 'Stadio San Nicola', 'Bari'),
        (29, 'Brescia', 16999, 'Stadio Mario Rigamonti', 'Brescia'),
        (30, 'Catanzaro', 12988, 'Stadio Nicola Ceravolo', 'Catanzaro'),
        (31, 'Modena', 21151, 'Stadio Alberto Braglia', 'Modena'),
        (32, 'Cosenza', 24768, 'Stadio San Vito-Gigi Marulla', 'Cosenza'),
        (33, 'Ascoli', 22742, 'Stadio Cino e Lillo Del Duca', 'Ascoli'),
        (34, 'Venezia', 11150, 'Stadio Pier Luigi Penzo', 'Venezia FC'),
        (35, 'Perugia', 28169, 'Stadio Renato Curi', 'Perugia'),
        (36, 'Benevento', 16867, 'Stadio Ciro Vigorito', 'Benevento'),
        (37, 'Pescara', 20476, 'Stadio Adriatico', 'Pescara'),
        (38, 'Piacenza', 10000, 'Stadio Leonardo Garilli', 'Piacenza'),
        (39, 'Trieste', 8500, 'Stadio Nereo Rocco', 'Triestina'),
        (40, 'Novara', 16959, 'Stadio Silvio Piola', 'Novara'),
        (41, 'Vicenza', 12500, 'Stadio Romeo Menti', 'Vicenza'),
        (42, 'Livorno', 19238, 'Stadio Armando Picchi', 'Livorno'),
        (43, 'Ancona', 28782, 'Stadio Del Conero', 'Ancona'),
        (44, 'Ravenna', 12000, 'Stadio Bruno Benelli', 'Ravenna'),
        (45, 'Siena', 15373, 'Stadio Artemio Franchi Montepaschi', 'Siena'),
        (46, 'Avellino', 26350, 'Stadio Partenio', 'Avellino'),
        (47, 'Reggina', 27000, 'Stadio Oreste Granillo', 'Reggina'),
        (48, 'Ternana', 22000, 'Stadio Libero Liberati', 'Ternana'),
        (49, 'Messina', 38765, 'Stadio San Filippo', 'Messina'),
        (50, 'Foggia', 19871, 'Stadio Pino Zaccheria', 'Foggia')
    """)

    cursor.execute("""
        INSERT IGNORE INTO Squadra (nome_squadra, capitano, ranking, presidente, anno_fondazione, num_giocatori, trofei_vinti) VALUES
        ('Inter', 'Lautaro Martinez', 1, 'Giuseppe Marotta', 1908, 25, 31),
        ('AC Milan', 'Davide Calabria', 2, 'Paolo Scaroni', 1899, 25, 29),
        ('Juventus', 'Danilo', 3, 'Gianluca Ferrero', 1897, 25, 70),
        ('AS Roma', 'Lorenzo Pellegrini', 4, 'Dan Friedkin', 1927, 25, 14),
        ('Napoli', 'Giovanni Di Lorenzo', 5, 'Aurelio De Laurentiis', 1926, 25, 8),
        ('Fiorentina', 'Cristiano Biraghi', 6, 'Rocco Commisso', 1926, 25, 7),
        ('Atalanta', 'Marten de Roon', 7, 'Antonio Percassi', 1907, 25, 2),
        ('Hellas Verona', 'Darko Lazovic', 8, 'Maurizio Setti', 1903, 25, 1),
        ('Genoa', 'Domenico Criscito', 9, 'Alberto Zangrillo', 1893, 25, 1),
        ('Bologna', 'Nicola Mancini', 10, 'Joey Saputo', 1909, 25, 7),
        ('Torino FC', 'Ricardo Rodriguez', 11, 'Urbano Cairo', 1906, 25, 7),
        ('Lazio', 'Ciro Immobile', 12, 'Claudio Lotito', 1900, 25, 17),
        ('Udinese', 'Tolgay Arslan', 13, 'Giampaolo Pozzo', 1896, 25, 0),
        ('Venezia', 'Haji Wright', 14, 'Duncan Niederauer', 1907, 25, 0),
        ('Empoli', 'Fabiano Parisi', 15, 'Fabrizio Corsi', 1920, 25, 0),
        ('Lecce', 'Wladimiro Falcone', 16, 'Saverio Sticchi Damiani', 1908, 25, 0),
        ('Cagliari', 'Leonardo Pavoletti', 17, 'Tommaso Giulini', 1920, 25, 0),
        ('Como', 'Cesc Fabregas', 18, 'Robert Hartono', 1907, 25, 0),
        ('Parma', 'Gianluigi Buffon', 19, 'Kyle Krause', 1913, 25, 3),
        ('Monza', 'Stefano Sensi', 20, 'Adriano Galliani', 1912, 25, 1),
        ('Sassuolo', 'Francesco Magnanelli', 21, 'Carlo Rossi', 1920, 25, 0),
        ('Salernitana', 'Franck Ribery', 22, 'Danilo Iervolino', 1919, 25, 0),
        ('Frosinone', 'Luca Mazzitelli', 23, 'Maurizio Stirpe', 1928, 25, 0),
        ('Cremonese', 'Francesco Bastrini', 24, 'Giovanni Arvedi', 1903, 25, 0),
        ('Spezia', 'Giulio Maggiore', 25, 'Philip Platek', 1906, 25, 0),
        ('Pisa', 'Rolando Maran', 26, 'Alexander Knaster', 1909, 25, 0),
        ('Palermo', 'Francesco Di Mariano', 27, 'Dario Mirri', 1900, 25, 0),
        ('Bari', 'Michele Maiello', 28, 'Luigi De Laurentiis', 1908, 25, 2),
        ('Brescia', 'Sandro Tonali', 29, 'Massimo Cellino', 1911, 25, 1),
        ('Catanzaro', 'Antonio Iemmello', 30, 'Floriano Noto', 1929, 25, 0),
        ('Modena', 'Davide Diaw', 31, 'Carlo Rivetti', 1912, 25, 0),
        ('Cosenza', 'Gianmarco Cimino', 32, 'Eugenio Guarascio', 1914, 25, 0),
        ('Ascoli', 'Francesco Forte', 33, 'William De Angelis', 1898, 25, 0),
        ('Venezia FC', 'Thomas Chryssochoidis', 34, 'Duncan Niederauer', 1907, 25, 0),
        ('Perugia', 'Filippo Sanchez', 35, 'Massimiliano Santopadre', 1905, 25, 0),
        ('Benevento', 'Gaetano Letizia', 36, 'Oreste Vigorito', 1929, 25, 1),
        ('Pescara', 'Luca Clemenza', 37, 'Daniele Sebastiani', 1936, 25, 0),
        ('Piacenza', 'Manuel Corbari', 38, 'Roberto Pighi', 1919, 25, 0),
        ('Triestina', 'Filippo Morse', 39, 'Giorgio Ferrara', 1918, 25, 0),
        ('Novara', 'Lorenzo Peli', 40, 'Enrico Sozzani', 1908, 25, 0),
        ('Vicenza', 'Michele Cavion', 41, 'Giuseppe Rosso', 1902, 25, 0),
        ('Livorno', 'Davide Marsura', 42, 'Aldo Spinelli', 1915, 25, 0),
        ('Ancona', 'Pietro Tommasini', 43, 'Tony Tiong', 1905, 25, 0),
        ('Ravenna', 'Simone Gori', 44, 'Roberto Molinelli', 1913, 25, 0),
        ('Siena', 'Alessandro Guberti', 45, 'Carlo Nistri', 1904, 25, 2),
        ('Avellino', 'Mickaël Birighitti', 46, 'Carlo Goglia', 1912, 25, 0),
        ('Reggina', 'Jeremy Menez', 47, 'Felice Saladini', 1914, 25, 0),
        ('Ternana', 'Luca Salzano', 48, 'Stefano Bandecchi', 1927, 25, 0),
        ('Messina', 'Giulio Cinaglia', 49, 'Pietro Sciotto', 1900, 25, 0),
        ('Foggia', 'Riccardo Marchizza', 50, 'Giuseppe Felleca', 1920, 25, 0)
    """)

    cursor.execute("""
        INSERT IGNORE INTO Sponsor (regione_sponsor, nome_sponsor, nome_squadra, anni_contratto) VALUES
        ('Lombardia', 'Pirelli', 'Inter', 5),
        ('Lombardia', 'Emirates', 'AC Milan', 4),
        ('Piemonte', 'Jeep', 'Juventus', 6),
        ('Lazio', 'Qatar Airways', 'AS Roma', 3),
        ('Campania', 'IQOS', 'Napoli', 4),
        ('Toscana', 'Mediacom', 'Fiorentina', 3),
        ('Lombardia', 'Gewiss', 'Atalanta', 5),
        ('Veneto', 'AGSM', 'Hellas Verona', 2),
        ('Liguria', 'Genova Airport', 'Genoa', 3),
        ('Emilia-Romagna', 'Valleverde', 'Bologna', 4),
        ('Piemonte', 'Kappa', 'Torino FC', 3),
        ('Lazio', 'Binance', 'Lazio', 5),
        ('Friuli', 'Dacia', 'Udinese', 4),
        ('Veneto', 'VPO', 'Venezia', 2),
        ('Toscana', 'Mumm', 'Empoli', 3),
        ('Puglia', 'Criptan', 'Lecce', 2),
        ('Sardegna', 'Sardinia Film', 'Cagliari', 3),
        ('Lombardia', 'GreenCredit', 'Como', 2),
        ('Emilia-Romagna', 'Parmalat', 'Parma', 5),
        ('Lombardia', 'Mapei', 'Monza', 3),
        ('Emilia-Romagna', 'Mapei', 'Sassuolo', 6),
        ('Campania', 'Banca Campania', 'Salernitana', 2),
        ('Lazio', 'Supermercati Dok', 'Frosinone', 2),
        ('Lombardia', 'Credem', 'Cremonese', 3),
        ('Liguria', 'Cassa Rurale', 'Spezia', 2),
        ('Toscana', 'Pisa Airport', 'Pisa', 2),
        ('Sicilia', 'Palermo Calcio Store', 'Palermo', 3),
        ('Puglia', 'Banca di Bari', 'Bari', 4),
        ('Lombardia', 'Brescia Mobilità', 'Brescia', 2),
        ('Calabria', 'Banca Progresso', 'Catanzaro', 2),
        ('Emilia-Romagna', 'Modena FC Store', 'Modena', 2),
        ('Calabria', 'Cosenza Calcio Partner', 'Cosenza', 2),
        ('Marche', 'Ascoli Calcio Store', 'Ascoli', 2),
        ('Veneto', 'Venezia Store', 'Venezia FC', 2),
        ('Umbria', 'Perugina', 'Perugia', 3),
        ('Campania', 'Benevento Calcio Store', 'Benevento', 2),
        ('Abruzzo', 'Delfino Store', 'Pescara', 2),
        ('Emilia-Romagna', 'Piacenza Calcio Store', 'Piacenza', 2),
        ('Friuli', 'Porto Trieste', 'Triestina', 2),
        ('Piemonte', 'Novara Calcio Store', 'Novara', 2),
        ('Veneto', 'Vicenza Calcio Store', 'Vicenza', 2),
        ('Toscana', 'Livorno Port', 'Livorno', 3),
        ('Marche', 'Ancona Porto', 'Ancona', 2),
        ('Emilia-Romagna', 'Ravenna Calcio Store', 'Ravenna', 2),
        ('Toscana', 'Monte dei Paschi', 'Siena', 4),
        ('Campania', 'Avellino Calcio Store', 'Avellino', 2),
        ('Calabria', 'Porto di Gioia Tauro', 'Reggina', 3),
        ('Umbria', 'Terni Acciai', 'Ternana', 3),
        ('Sicilia', 'Messina Peloro', 'Messina', 2),
        ('Puglia', 'Foggia Calcio Store', 'Foggia', 2)
    """)

    cursor.execute("""
        INSERT IGNORE INTO Allenatore (id_allenatore, nome, cognome, eta, nazionalita, squadra, trofei_vinti) VALUES
        (1, 'Simone', 'Inzaghi', 48, 'Italiana', 'Inter', 8),
        (2, 'Stefano', 'Pioli', 58, 'Italiana', 'AC Milan', 5),
        (3, 'Massimiliano', 'Allegri', 57, 'Italiana', 'Juventus', 11),
        (4, 'Jose', 'Mourinho', 61, 'Portoghese', 'AS Roma', 25),
        (5, 'Rudi', 'Garcia', 60, 'Francese', 'Napoli', 6),
        (6, 'Vincenzo', 'Italiano', 47, 'Italiana', 'Fiorentina', 2),
        (7, 'Gian Piero', 'Gasperini', 66, 'Italiana', 'Atalanta', 3),
        (8, 'Marco', 'Baroni', 60, 'Italiana', 'Hellas Verona', 1),
        (9, 'Alberto', 'Gilardino', 46, 'Italiana', 'Genoa', 1),
        (10, 'Thiago', 'Motta', 42, 'Italiana', 'Bologna', 2),
        (11, 'Ivan', 'Juric', 48, 'Croata', 'Torino FC', 2),
        (12, 'Maurizio', 'Sarri', 65, 'Italiana', 'Lazio', 7),
        (13, 'Gabriele', 'Cioffi', 48, 'Italiana', 'Udinese', 1),
        (14, 'Paolo', 'Vanoli', 52, 'Italiana', 'Venezia', 1),
        (15, 'Davide', 'Nicola', 50, 'Italiana', 'Empoli', 1),
        (16, 'Roberto', 'DAversa', 49, 'Italiana', 'Lecce', 2),
        (17, 'Claudio', 'Ranieri', 72, 'Italiana', 'Cagliari', 5),
        (18, 'Cesc', 'Fabregas', 37, 'Spagnola', 'Como', 1),
        (19, 'Fabio', 'Pecchia', 51, 'Italiana', 'Parma', 2),
        (20, 'Raffaele', 'Palladino', 40, 'Italiana', 'Monza', 1),
        (21, 'Alessio', 'Dionisi', 44, 'Italiana', 'Sassuolo', 1),
        (22, 'Paulo', 'Sousa', 53, 'Portoghese', 'Salernitana', 3),
        (23, 'Eusebio', 'Di Francesco', 54, 'Italiana', 'Frosinone', 2),
        (24, 'Davide', 'Ballardini', 61, 'Italiana', 'Cremonese', 2),
        (25, 'Luca', 'Gotti', 56, 'Italiana', 'Spezia', 1),
        (26, 'Alberto', 'Aquilani', 40, 'Italiana', 'Pisa', 1),
        (27, 'Eugenio', 'Corini', 54, 'Italiana', 'Palermo', 1),
        (28, 'Michele', 'Mignani', 51, 'Italiana', 'Bari', 1),
        (29, 'Pep', 'Guardiola', 53, 'Spagnola', 'Brescia', 32),
        (30, 'Vincenzo', 'Vivarini', 55, 'Italiana', 'Catanzaro', 1),
        (31, 'Attilio', 'Tesser', 62, 'Italiana', 'Modena', 1),
        (32, 'William', 'Viali', 46, 'Italiana', 'Cosenza', 1),
        (33, 'William', 'Viali', 46, 'Italiana', 'Ascoli', 1),
        (34, 'Filippo', 'Inzaghi', 50, 'Italiana', 'Venezia FC', 3),
        (35, 'Silvio', 'Baldini', 63, 'Italiana', 'Perugia', 1),
        (36, 'Fabio', 'Cannavaro', 50, 'Italiana', 'Benevento', 2),
        (37, 'Zdenek', 'Zeman', 76, 'Ceca', 'Pescara', 4),
        (38, 'Cristiano', 'Scazzola', 53, 'Italiana', 'Piacenza', 1),
        (39, 'Bruno', 'Caneo', 58, 'Italiana', 'Triestina', 1),
        (40, 'Alessandro', 'Nesta', 48, 'Italiana', 'Novara', 2),
        (41, 'Francesco', 'Baldini', 51, 'Italiana', 'Vicenza', 1),
        (42, 'Marco', 'Amelia', 43, 'Italiana', 'Livorno', 1),
        (43, 'Gianluca', 'Colavitto', 50, 'Italiana', 'Ancona', 1),
        (44, 'Mauro', 'Antonioli', 52, 'Italiana', 'Ravenna', 1),
        (45, 'Andrea', 'Troise', 44, 'Italiana', 'Siena', 1),
        (46, 'Roberto', 'Taurino', 47, 'Italiana', 'Avellino', 1),
        (47, 'Filippo', 'Inzaghi', 50, 'Italiana', 'Reggina', 3),
        (48, 'Cristiano', 'Lucarelli', 50, 'Italiana', 'Ternana', 2),
        (49, 'Gaetano', 'Auteri', 62, 'Italiana', 'Messina', 2),
        (50, 'Delio', 'Rossi', 66, 'Italiana', 'Foggia', 3)
    """)

    cursor.execute("""
        INSERT IGNORE INTO CentroAllenamento (id_centro, nome_squadra, nome_centro, citta, num_campi) VALUES
        (1, 'Inter', 'Suning Training Centre', 'Appiano Gentile', 8),
        (2, 'AC Milan', 'Milanello', 'Carnago', 10),
        (3, 'Juventus', 'Juventus Training Center', 'Torino', 12),
        (4, 'AS Roma', 'Centro Sportivo Fulvio Bernardini', 'Roma', 7),
        (5, 'Napoli', 'SSC Napoli Konami Training Center', 'Napoli', 6),
        (6, 'Fiorentina', 'Centro Sportivo Davide Astori', 'Firenze', 5),
        (7, 'Atalanta', 'Centro Sportivo Bortolotti', 'Zingonia', 8),
        (8, 'Hellas Verona', 'Centro Sportivo AGSM Forum', 'Verona', 4),
        (9, 'Genoa', 'Centro Sportivo Signorini', 'Genova', 5),
        (10, 'Bologna', 'Centro Tecnico Federale Casteldebole', 'Bologna', 6),
        (11, 'Torino FC', 'Centro Sportivo Robaldo', 'Torino', 5),
        (12, 'Lazio', 'Centro Sportivo Formello', 'Roma', 7),
        (13, 'Udinese', 'Bruseschi Training Center', 'Udine', 4),
        (14, 'Venezia', 'Centro Sportivo Taliercio', 'Venezia', 3),
        (15, 'Empoli', 'Centro Sportivo La Castellana', 'Empoli', 4),
        (16, 'Lecce', 'Centro Sportivo Via del Mare', 'Lecce', 4),
        (17, 'Cagliari', 'Centro Sportivo Asseminello', 'Cagliari', 5),
        (18, 'Como', 'Centro Sportivo Comense', 'Como', 3),
        (19, 'Parma', 'Centro Sportivo Collecchio', 'Parma', 6),
        (20, 'Monza', 'Centro Sportivo Monzello', 'Monza', 5),
        (21, 'Sassuolo', 'Centro Sportivo Riccione', 'Sassuolo', 4),
        (22, 'Salernitana', 'Centro Sportivo Mary Rosy', 'Salerno', 3),
        (23, 'Frosinone', 'Centro Sportivo Guido Angelini', 'Frosinone', 4),
        (24, 'Cremonese', 'Centro Sportivo Giovanni Arvedi', 'Cremona', 3),
        (25, 'Spezia', 'Centro Sportivo Intels', 'La Spezia', 3),
        (26, 'Pisa', 'Centro Sportivo Arena Garibaldi', 'Pisa', 4),
        (27, 'Palermo', 'Centro Sportivo Tenente Onorato', 'Palermo', 5),
        (28, 'Bari', 'Centro Sportivo San Pio', 'Bari', 5),
        (29, 'Brescia', 'Centro Sportivo di Torbole Casaglia', 'Brescia', 4),
        (30, 'Catanzaro', 'Centro Sportivo Enzo Ferrari', 'Catanzaro', 3),
        (31, 'Modena', 'Centro Sportivo Mirandola', 'Modena', 4),
        (32, 'Cosenza', 'Centro Sportivo Donato Bergamini', 'Cosenza', 3),
        (33, 'Ascoli', 'Centro Sportivo Picchio Village', 'Ascoli Piceno', 4),
        (34, 'Venezia FC', 'Centro Sportivo Ca Noghera', 'Venezia', 3),
        (35, 'Perugia', 'Centro Sportivo Pian di Massiano', 'Perugia', 4),
        (36, 'Benevento', 'Centro Sportivo Francesca', 'Benevento', 3),
        (37, 'Pescara', 'Centro Sportivo Poggio degli Ulivi', 'Pescara', 4),
        (38, 'Piacenza', 'Centro Sportivo Veggioletta', 'Piacenza', 3),
        (39, 'Triestina', 'Centro Sportivo Valmaura', 'Trieste', 3),
        (40, 'Novara', 'Centro Sportivo La Mandria', 'Novara', 3),
        (41, 'Vicenza', 'Centro Sportivo Palladio', 'Vicenza', 3),
        (42, 'Livorno', 'Centro Sportivo Livorno', 'Livorno', 3),
        (43, 'Ancona', 'Centro Sportivo Passo Varano', 'Ancona', 4),
        (44, 'Ravenna', 'Centro Sportivo Cava Maldini', 'Ravenna', 3),
        (45, 'Siena', 'Centro Sportivo Acquacalda', 'Siena', 4),
        (46, 'Avellino', 'Centro Sportivo Zoccolari', 'Avellino', 3),
        (47, 'Reggina', 'Centro Sportivo Sant Agata', 'Reggio Calabria', 4),
        (48, 'Ternana', 'Centro Sportivo Cesi', 'Terni', 3),
        (49, 'Messina', 'Centro Sportivo San Filippo', 'Messina', 3),
        (50, 'Foggia', 'Centro Sportivo Bisceglie', 'Foggia', 3)
    """)

    cursor.execute("""
        INSERT IGNORE INTO Giocatore (id_giocatore, nome, cognome, eta, ruolo, squadra, nazionalita, num_maglia) VALUES
        (1, 'Lautaro', 'Martinez', 26, 'Attaccante', 'Inter', 'Argentina', 10),
        (2, 'Nicolo', 'Barella', 27, 'Centrocampista', 'Inter', 'Italiana', 23),
        (3, 'Federico', 'Dimarco', 26, 'Difensore', 'Inter', 'Italiana', 32),
        (4, 'Mike', 'Maignan', 28, 'Portiere', 'AC Milan', 'Francese', 16),
        (5, 'Rafael', 'Leao', 24, 'Attaccante', 'AC Milan', 'Portoghese', 10),
        (6, 'Theo', 'Hernandez', 26, 'Difensore', 'AC Milan', 'Francese', 19),
        (7, 'Federico', 'Chiesa', 26, 'Attaccante', 'Juventus', 'Italiana', 7),
        (8, 'Adrien', 'Rabiot', 28, 'Centrocampista', 'Juventus', 'Francese', 25),
        (9, 'Wojciech', 'Szczesny', 33, 'Portiere', 'Juventus', 'Polacca', 1),
        (10, 'Paulo', 'Dybala', 30, 'Attaccante', 'AS Roma', 'Argentina', 21),
        (11, 'Lorenzo', 'Pellegrini', 27, 'Centrocampista', 'AS Roma', 'Italiana', 7),
        (12, 'Romelu', 'Lukaku', 30, 'Attaccante', 'AS Roma', 'Belga', 90),
        (13, 'Victor', 'Osimhen', 25, 'Attaccante', 'Napoli', 'Nigeriana', 9),
        (14, 'Khvicha', 'Kvaratskhelia', 23, 'Attaccante', 'Napoli', 'Georgiana', 77),
        (15, 'Giovanni', 'Di Lorenzo', 30, 'Difensore', 'Napoli', 'Italiana', 22),
        (16, 'Nikola', 'Milenkovic', 26, 'Difensore', 'Fiorentina', 'Serba', 4),
        (17, 'Cristiano', 'Biraghi', 31, 'Difensore', 'Fiorentina', 'Italiana', 3),
        (18, 'Nicolas', 'Gonzalez', 25, 'Attaccante', 'Fiorentina', 'Argentina', 10),
        (19, 'Gianluca', 'Scamacca', 25, 'Attaccante', 'Atalanta', 'Italiana', 9),
        (20, 'Marten', 'de Roon', 32, 'Centrocampista', 'Atalanta', 'Olandese', 15),
        (21, 'Giorgio', 'Scalvini', 20, 'Difensore', 'Atalanta', 'Italiana', 42),
        (22, 'Thomas', 'Henry', 29, 'Attaccante', 'Hellas Verona', 'Francese', 29),
        (23, 'Darko', 'Lazovic', 33, 'Difensore', 'Hellas Verona', 'Serba', 23),
        (24, 'Albert', 'Gudmundsson', 26, 'Attaccante', 'Genoa', 'Islandese', 11),
        (25, 'Radu', 'Dragusin', 22, 'Difensore', 'Genoa', 'Rumena', 5),
        (26, 'Joshua', 'Zirkzee', 23, 'Attaccante', 'Bologna', 'Olandese', 9),
        (27, 'Riccardo', 'Orsolini', 27, 'Attaccante', 'Bologna', 'Italiana', 7),
        (28, 'Stefan', 'Posch', 26, 'Difensore', 'Bologna', 'Austriaca', 13),
        (29, 'Antonio', 'Sanabria', 27, 'Attaccante', 'Torino FC', 'Paraguayana', 9),
        (30, 'Ricardo', 'Rodriguez', 31, 'Difensore', 'Torino FC', 'Svizzera', 13),
        (31, 'Ciro', 'Immobile', 34, 'Attaccante', 'Lazio', 'Italiana', 17),
        (32, 'Luis', 'Alberto', 31, 'Centrocampista', 'Lazio', 'Spagnola', 10),
        (33, 'Mattia', 'Zaccagni', 28, 'Attaccante', 'Lazio', 'Italiana', 20),
        (34, 'Destiny', 'Udogie', 21, 'Difensore', 'Udinese', 'Italiana', 3),
        (35, 'Gerard', 'Deulofeu', 29, 'Attaccante', 'Udinese', 'Spagnola', 11),
        (36, 'Joel', 'Pohjanpalo', 29, 'Attaccante', 'Venezia', 'Finlandese', 9),
        (37, 'Haji', 'Wright', 25, 'Attaccante', 'Venezia', 'Americana', 99),
        (38, 'Mattia', 'Destro', 32, 'Attaccante', 'Empoli', 'Italiana', 9),
        (39, 'Fabiano', 'Parisi', 22, 'Difensore', 'Empoli', 'Italiana', 3),
        (40, 'Lorenzo', 'Colombo', 21, 'Attaccante', 'Lecce', 'Italiana', 9),
        (41, 'Wladimiro', 'Falcone', 27, 'Portiere', 'Lecce', 'Italiana', 30),
        (42, 'Leonardo', 'Pavoletti', 35, 'Attaccante', 'Cagliari', 'Italiana', 29),
        (43, 'Alessandro', 'Deiola', 29, 'Centrocampista', 'Cagliari', 'Italiana', 4),
        (44, 'Nico', 'Paz', 19, 'Centrocampista', 'Como', 'Argentina', 10),
        (45, 'Patrick', 'Cutrone', 26, 'Attaccante', 'Como', 'Italiana', 9),
        (46, 'Gianluigi', 'Buffon', 46, 'Portiere', 'Parma', 'Italiana', 77),
        (47, 'Dennis', 'Man', 25, 'Attaccante', 'Parma', 'Rumena', 10),
        (48, 'Valentin', 'Mihailovic', 24, 'Centrocampista', 'Monza', 'Americana', 8),
        (49, 'Andrea', 'Petagna', 29, 'Attaccante', 'Monza', 'Italiana', 9),
        (50, 'Domenico', 'Berardi', 29, 'Attaccante', 'Sassuolo', 'Italiana', 10)
    """)

    cursor.execute("""
        INSERT IGNORE INTO Contratto (id_contratto, data_inizio, data_fine, id_giocatore, stipendio, clausola_rescissoria) VALUES
        (1,  '2021-07-01', '2026-06-30', 1,  8000000.00, 111000000.00),
        (2,  '2020-09-01', '2026-06-30', 2,  5500000.00, 80000000.00),
        (3,  '2021-07-01', '2025-06-30', 3,  2500000.00, 40000000.00),
        (4,  '2021-06-01', '2026-06-30', 4,  5000000.00, 70000000.00),
        (5,  '2022-01-01', '2027-06-30', 5,  7000000.00, 175000000.00),
        (6,  '2021-07-01', '2026-06-30', 6,  6000000.00, 80000000.00),
        (7,  '2020-07-01', '2025-06-30', 7,  5000000.00, 60000000.00),
        (8,  '2019-07-01', '2024-06-30', 8,  7000000.00, NULL),
        (9,  '2017-07-01', '2024-06-30', 9,  6500000.00, NULL),
        (10, '2022-08-01', '2026-06-30', 10, 6000000.00, 20000000.00),
        (11, '2019-07-01', '2025-06-30', 11, 3500000.00, 40000000.00),
        (12, '2023-08-01', '2026-06-30', 12, 7500000.00, NULL),
        (13, '2020-07-01', '2025-06-30', 13, 10000000.00, 130000000.00),
        (14, '2022-07-01', '2027-06-30', 14, 5000000.00, 100000000.00),
        (15, '2019-07-01', '2025-06-30', 15, 2800000.00, 35000000.00),
        (16, '2019-07-01', '2024-06-30', 16, 2500000.00, 30000000.00),
        (17, '2018-07-01', '2024-06-30', 17, 1800000.00, NULL),
        (18, '2021-07-01', '2025-06-30', 18, 3000000.00, 40000000.00),
        (19, '2023-07-01', '2027-06-30', 19, 3500000.00, 50000000.00),
        (20, '2017-07-01', '2025-06-30', 20, 2500000.00, NULL),
        (21, '2022-07-01', '2027-06-30', 21, 1500000.00, 40000000.00),
        (22, '2022-07-01', '2025-06-30', 22, 1200000.00, NULL),
        (23, '2018-07-01', '2024-06-30', 23, 1000000.00, NULL),
        (24, '2022-07-01', '2026-06-30', 24, 2000000.00, 25000000.00),
        (25, '2023-01-01', '2027-06-30', 25, 1500000.00, 30000000.00),
        (26, '2022-07-01', '2025-06-30', 26, 2000000.00, 40000000.00),
        (27, '2020-07-01', '2025-06-30', 27, 1800000.00, 20000000.00),
        (28, '2022-07-01', '2026-06-30', 28, 1500000.00, 20000000.00),
        (29, '2021-07-01', '2025-06-30', 29, 2000000.00, NULL),
        (30, '2021-07-01', '2024-06-30', 30, 1500000.00, NULL),
        (31, '2017-09-01', '2026-06-30', 31, 4000000.00, NULL),
        (32, '2018-07-01', '2025-06-30', 32, 3500000.00, NULL),
        (33, '2021-07-01', '2025-06-30', 33, 2000000.00, 25000000.00),
        (34, '2021-07-01', '2023-06-30', 34, 800000.00,  15000000.00),
        (35, '2021-07-01', '2024-06-30', 35, 1500000.00, NULL),
        (36, '2023-07-01', '2026-06-30', 36, 900000.00,  NULL),
        (37, '2023-07-01', '2025-06-30', 37, 700000.00,  NULL),
        (38, '2022-07-01', '2024-06-30', 38, 800000.00,  NULL),
        (39, '2022-07-01', '2025-06-30', 39, 600000.00,  NULL),
        (40, '2023-07-01', '2025-06-30', 40, 700000.00,  NULL),
        (41, '2021-07-01', '2025-06-30', 41, 500000.00,  NULL),
        (42, '2022-07-01', '2025-06-30', 42, 800000.00,  NULL),
        (43, '2021-07-01', '2024-06-30', 43, 600000.00,  NULL),
        (44, '2023-07-01', '2026-06-30', 44, 1000000.00, 15000000.00),
        (45, '2022-07-01', '2025-06-30', 45, 700000.00,  NULL),
        (46, '2023-07-01', '2024-06-30', 46, 1500000.00, NULL),
        (47, '2023-07-01', '2026-06-30', 47, 1200000.00, 15000000.00),
        (48, '2022-07-01', '2025-06-30', 48, 800000.00,  NULL),
        (49, '2022-07-01', '2025-06-30', 49, 1000000.00, NULL),
        (50, '2017-07-01', '2024-06-30', 50, 4000000.00, NULL)
    """)

    cursor.execute("""
        INSERT IGNORE INTO Competizione (id_competizione, nome, paese, num_partite, data_inizio, data_fine, tipo_palla) VALUES
        (1,  'Serie A 2023/24',                    'Italia',       380, '2023-08-19', '2024-05-26', 'Puma Orbita 1'),
        (2,  'Serie A 2022/23',                    'Italia',       380, '2022-08-13', '2023-06-04', 'Puma Orbita 1'),
        (3,  'Serie A 2021/22',                    'Italia',       380, '2021-08-21', '2022-05-22', 'Puma Orbita 1'),
        (4,  'UEFA Champions League 2023/24',      'Europa',       225, '2023-09-19', '2024-06-01', 'Adidas UCL Pro'),
        (5,  'UEFA Champions League 2022/23',      'Europa',       225, '2022-09-06', '2023-06-10', 'Adidas UCL Pro'),
        (6,  'UEFA Champions League 2021/22',      'Europa',       225, '2021-09-14', '2022-05-28', 'Adidas UCL Pro'),
        (7,  'Coppa Italia 2023/24',               'Italia',        63, '2023-08-06', '2024-05-15', 'Puma Orbita 1'),
        (8,  'Coppa Italia 2022/23',               'Italia',        63, '2022-08-05', '2023-05-24', 'Puma Orbita 1'),
        (9,  'Coppa Italia 2021/22',               'Italia',        63, '2021-08-08', '2022-05-11', 'Puma Orbita 1'),
        (10, 'UEFA Europa League 2023/24',         'Europa',       189, '2023-09-21', '2024-05-22', 'Adidas Europa Pro'),
        (11, 'UEFA Europa League 2022/23',         'Europa',       189, '2022-09-08', '2023-05-31', 'Adidas Europa Pro'),
        (12, 'UEFA Europa League 2021/22',         'Europa',       189, '2021-09-16', '2022-05-18', 'Adidas Europa Pro'),
        (13, 'UEFA Conference League 2023/24',     'Europa',       189, '2023-09-21', '2024-05-29', 'Adidas Europa Pro'),
        (14, 'UEFA Conference League 2022/23',     'Europa',       189, '2022-09-08', '2023-06-07', 'Adidas Europa Pro'),
        (15, 'Supercoppa Italiana 2024',           'Italia',         3, '2024-01-18', '2024-01-22', 'Puma Orbita 1'),
        (16, 'Supercoppa Italiana 2023',           'Italia',         3, '2023-01-18', '2023-01-22', 'Puma Orbita 1'),
        (17, 'Premier League 2023/24',             'Inghilterra',  380, '2023-08-11', '2024-05-19', 'Nike Flight'),
        (18, 'Premier League 2022/23',             'Inghilterra',  380, '2022-08-05', '2023-05-28', 'Nike Flight'),
        (19, 'LaLiga 2023/24',                     'Spagna',       380, '2023-08-11', '2024-05-26', 'Adidas LaLiga Pro'),
        (20, 'LaLiga 2022/23',                     'Spagna',       380, '2022-08-12', '2023-06-04', 'Adidas LaLiga Pro'),
        (21, 'Bundesliga 2023/24',                 'Germania',     306, '2023-08-18', '2024-05-18', 'Adidas Torfabrik'),
        (22, 'Bundesliga 2022/23',                 'Germania',     306, '2022-08-05', '2023-05-27', 'Adidas Torfabrik'),
        (23, 'Ligue 1 2023/24',                    'Francia',      380, '2023-08-11', '2024-05-18', 'Uhlsport Match'),
        (24, 'Ligue 1 2022/23',                    'Francia',      380, '2022-08-05', '2023-06-03', 'Uhlsport Match'),
        (25, 'Primeira Liga 2023/24',              'Portogallo',   306, '2023-08-11', '2024-05-18', 'Nike Flight'),
        (26, 'Eredivisie 2023/24',                 'Olanda',       306, '2023-08-04', '2024-05-19', 'Nike Flight'),
        (27, 'UEFA Nations League 2022/23',        'Europa',       171, '2022-06-02', '2023-06-18', 'Adidas Nations'),
        (28, 'Mondiali 2022',                      'Qatar',         64, '2022-11-20', '2022-12-18', 'Adidas Al Rihla'),
        (29, 'Europei 2020',                       'Europa',        51, '2021-06-11', '2021-07-11', 'Adidas Uniforia'),
        (30, 'Europei 2024',                       'Germania',      51, '2024-06-14', '2024-07-14', 'Adidas Fussballliebe'),
        (31, 'Serie B 2023/24',                    'Italia',       380, '2023-08-18', '2024-05-10', 'Puma Orbita 2'),
        (32, 'Serie B 2022/23',                    'Italia',       380, '2022-08-12', '2023-05-05', 'Puma Orbita 2'),
        (33, 'Serie C 2023/24',                    'Italia',       798, '2023-08-27', '2024-04-28', 'Puma Orbita 3'),
        (34, 'Coppa Italia Serie C 2023/24',       'Italia',        64, '2023-09-10', '2024-04-17', 'Puma Orbita 3'),
        (35, 'FA Cup 2023/24',                     'Inghilterra',   82, '2023-11-04', '2024-05-25', 'Nike Flight'),
        (36, 'Copa del Rey 2023/24',               'Spagna',        83, '2023-10-25', '2024-05-06', 'Adidas LaLiga Pro'),
        (37, 'DFB Pokal 2023/24',                  'Germania',      63, '2023-10-31', '2024-05-25', 'Adidas Torfabrik'),
        (38, 'Coupe de France 2023/24',            'Francia',      128, '2024-01-06', '2024-05-25', 'Uhlsport Match'),
        (39, 'UEFA Super Cup 2023',                'Europa',         1, '2023-08-16', '2023-08-16', 'Adidas UCL Pro'),
        (40, 'FIFA Club World Cup 2023',           'Arabia Saudita', 8, '2023-12-12', '2023-12-22', 'Adidas Al Rihla'),
        (41, 'UEFA Youth League 2023/24',          'Europa',       125, '2023-09-19', '2024-04-22', 'Adidas UCL Pro'),
        (42, 'Serie A Femminile 2023/24',          'Italia',       132, '2023-09-09', '2024-05-18', 'Puma Orbita 1'),
        (43, 'Coppa Italia Femminile 2023/24',     'Italia',        32, '2023-11-01', '2024-05-08', 'Puma Orbita 1'),
        (44, 'Supercoppa Europea 2024',            'Europa',         1, '2024-08-14', '2024-08-14', 'Adidas UCL Pro'),
        (45, 'Amichevoli Nazionali Marzo 2024',    'Internazionale', 20, '2024-03-21', '2024-03-26', 'Varie'),
        (46, 'Amichevoli Pre-Stagione 2023',       'Italia',        30, '2023-07-10', '2023-08-05', 'Varie'),
        (47, 'Playoff Serie B 2023/24',            'Italia',        16, '2024-05-13', '2024-06-10', 'Puma Orbita 2'),
        (48, 'Playout Serie B 2023/24',            'Italia',         4, '2024-05-13', '2024-05-26', 'Puma Orbita 2'),
        (49, 'Torneo di Viareggio 2024',           'Italia',        40, '2024-03-13', '2024-03-28', 'Puma Orbita 3'),
        (50, 'Supercoppa di Lega Serie B 2024',    'Italia',         4, '2024-01-14', '2024-01-21', 'Puma Orbita 2')
    """)

    cursor.execute("""
        INSERT IGNORE INTO Partita (id_partita, meteo, orario_partita, squadra, squadra_ospite, arbitro, data_partita, id_competizione, giornata, risultato, nome_stadio) VALUES
        (1,  'Soleggiato',  '20:45:00', 'Inter',         'AC Milan',      'Daniele Orsato',      '2023-09-16', 1, 4,  1, 'San Siro'),
        (2,  'Nuvoloso',    '18:00:00', 'Juventus',       'AS Roma',       'Marco Guida',         '2023-09-17', 1, 4,  0, 'Allianz Stadium'),
        (3,  'Pioggia',     '20:45:00', 'Napoli',         'Lazio',         'Maurizio Mariani',    '2023-09-23', 1, 5,  1, 'Stadio Diego Armando Maradona'),
        (4,  'Soleggiato',  '15:00:00', 'AC Milan',       'Inter',         'Fabio Maresca',       '2024-02-04', 1, 23, 1, 'San Siro'),
        (5,  'Nuvoloso',    '20:45:00', 'AS Roma',        'Napoli',        'Luca Pairetto',       '2023-10-29', 1, 10, 0, 'Stadio Olimpico'),
        (6,  'Soleggiato',  '18:00:00', 'Atalanta',       'Fiorentina',    'Davide Massa',        '2023-10-01', 1, 7,  2, 'Gewiss Stadium'),
        (7,  'Nuvoloso',    '20:45:00', 'Lazio',          'Juventus',      'Daniele Orsato',      '2023-11-05', 1, 11, 1, 'Stadio Olimpico'),
        (8,  'Pioggia',     '15:00:00', 'Bologna',        'Torino FC',     'Marco Piccinini',     '2023-10-07', 1, 8,  2, 'Stadio Renato Dall Ara'),
        (9,  'Soleggiato',  '20:45:00', 'Inter',          'Atalanta',      'Marco Guida',         '2023-10-28', 1, 10, 3, 'San Siro'),
        (10, 'Nuvoloso',    '18:00:00', 'Napoli',         'Fiorentina',    'Maurizio Mariani',    '2023-11-12', 1, 12, 0, 'Stadio Diego Armando Maradona'),
        (11, 'Soleggiato',  '20:45:00', 'Inter',          'Juventus',      'Daniele Orsato',      '2023-11-26', 1, 13, 1, 'San Siro'),
        (12, 'Pioggia',     '15:00:00', 'AS Roma',        'Lazio',         'Davide Massa',        '2023-12-10', 1, 15, 1, 'Stadio Olimpico'),
        (13, 'Neve',        '15:00:00', 'Juventus',       'Napoli',        'Luca Pairetto',       '2023-12-08', 1, 15, 1, 'Allianz Stadium'),
        (14, 'Soleggiato',  '20:45:00', 'AC Milan',       'Atalanta',      'Marco Guida',         '2023-12-06', 1, 15, 3, 'San Siro'),
        (15, 'Nuvoloso',    '18:00:00', 'Fiorentina',     'Bologna',       'Maurizio Mariani',    '2023-12-17', 1, 16, 1, 'Stadio Artemio Franchi'),
        (16, 'Soleggiato',  '20:45:00', 'Inter',          'Lazio',         'Daniele Orsato',      '2024-01-06', 1, 19, 2, 'San Siro'),
        (17, 'Nuvoloso',    '15:00:00', 'Napoli',         'Inter',         'Fabio Maresca',       '2024-01-21', 1, 21, 0, 'Stadio Diego Armando Maradona'),
        (18, 'Pioggia',     '18:00:00', 'Juventus',       'AC Milan',      'Marco Guida',         '2024-02-11', 1, 24, 0, 'Allianz Stadium'),
        (19, 'Soleggiato',  '20:45:00', 'AS Roma',        'Inter',         'Luca Pairetto',       '2024-03-10', 1, 27, 2, 'Stadio Olimpico'),
        (20, 'Nuvoloso',    '20:45:00', 'Atalanta',       'Juventus',      'Davide Massa',        '2024-02-25', 1, 26, 1, 'Gewiss Stadium'),
        (21, 'Soleggiato',  '20:45:00', 'Inter',          'Napoli',        '2024-04-21', '2024-04-21', 1, 33, 2, 'San Siro'),
        (22, 'Pioggia',     '18:00:00', 'AC Milan',       'AS Roma',       'Daniele Orsato',      '2024-04-18', 1, 33, 1, 'San Siro'),
        (23, 'Soleggiato',  '20:45:00', 'Inter',          'Torino FC',     'Marco Piccinini',     '2024-04-28', 1, 34, 2, 'San Siro'),
        (24, 'Nuvoloso',    '15:00:00', 'Bologna',        'Juventus',      'Maurizio Mariani',    '2024-05-20', 1, 38, 0, 'Stadio Renato Dall Ara'),
        (25, 'Soleggiato',  '20:45:00', 'AC Milan',       'Cagliari',      'Fabio Maresca',       '2024-05-24', 1, 38, 5, 'San Siro'),
        (26, 'Soleggiato',  '21:00:00', 'Inter',          'Real Madrid',   'Slavko Vincic',       '2023-11-28', 4, 5,  1, 'San Siro'),
        (27, 'Nuvoloso',    '21:00:00', 'Napoli',         'Real Madrid',   'Felix Brych',         '2023-03-07', 5, 7,  1, 'Stadio Diego Armando Maradona'),
        (28, 'Pioggia',     '21:00:00', 'AC Milan',       'PSG',           'Anthony Taylor',      '2023-10-25', 4, 3,  2, 'San Siro'),
        (29, 'Soleggiato',  '21:00:00', 'Lazio',          'Celtic',        'Slavko Vincic',       '2023-10-04', 4, 2,  2, 'Stadio Olimpico'),
        (30, 'Nuvoloso',    '21:00:00', 'Fiorentina',     'Braga',         'Istvan Kovacs',       '2023-10-05', 13, 2, 3, 'Stadio Artemio Franchi'),
        (31, 'Soleggiato',  '20:45:00', 'Inter',          'Bologna',       'Marco Guida',         '2024-03-04', 1, 27, 1, 'San Siro'),
        (32, 'Nuvoloso',    '20:45:00', 'Juventus',       'Fiorentina',    'Daniele Orsato',      '2024-03-03', 1, 27, 1, 'Allianz Stadium'),
        (33, 'Pioggia',     '15:00:00', 'Genoa',          'Lecce',         'Luca Pairetto',       '2024-03-03', 1, 27, 1, 'Stadio Luigi Ferraris'),
        (34, 'Soleggiato',  '18:00:00', 'Lazio',          'Udinese',       'Fabio Maresca',       '2024-03-04', 1, 27, 2, 'Stadio Olimpico'),
        (35, 'Nuvoloso',    '15:00:00', 'Cagliari',       'Venezia',       'Marco Piccinini',     '2024-03-10', 1, 28, 1, 'Unipol Domus'),
        (36, 'Soleggiato',  '20:45:00', 'Napoli',         'Juventus',      'Davide Massa',        '2024-03-29', 1, 30, 2, 'Stadio Diego Armando Maradona'),
        (37, 'Pioggia',     '18:00:00', 'Torino FC',      'Fiorentina',    'Marco Guida',         '2024-04-07', 1, 31, 0, 'Stadio Olimpico Grande Torino'),
        (38, 'Soleggiato',  '20:45:00', 'AS Roma',        'Bologna',       'Maurizio Mariani',    '2024-04-22', 1, 33, 1, 'Stadio Olimpico'),
        (39, 'Nuvoloso',    '15:00:00', 'Udinese',        'Empoli',        'Luca Pairetto',       '2024-04-28', 1, 34, 1, 'Dacia Arena'),
        (40, 'Soleggiato',  '20:45:00', 'Atalanta',       'AS Roma',       'Daniele Orsato',      '2024-05-02', 1, 35, 2, 'Gewiss Stadium'),
        (41, 'Pioggia',     '20:45:00', 'Inter',          'Frosinone',     'Fabio Maresca',       '2024-05-10', 1, 36, 5, 'San Siro'),
        (42, 'Soleggiato',  '20:45:00', 'AC Milan',       'Genoa',         'Marco Guida',         '2024-05-13', 1, 37, 3, 'San Siro'),
        (43, 'Nuvoloso',    '20:45:00', 'Juventus',       'Bologna',       'Maurizio Mariani',    '2024-05-20', 1, 38, 3, 'Allianz Stadium'),
        (44, 'Soleggiato',  '15:00:00', 'Napoli',         'Lecce',         'Marco Piccinini',     '2024-05-26', 1, 38, 2, 'Stadio Diego Armando Maradona'),
        (45, 'Nuvoloso',    '20:45:00', 'AS Roma',        'Empoli',        'Davide Massa',        '2024-05-26', 1, 38, 2, 'Stadio Olimpico'),
        (46, 'Soleggiato',  '21:00:00', 'Juventus',       'Lazio',         'Daniele Orsato',      '2024-01-16', 7, 1,  2, 'Allianz Stadium'),
        (47, 'Pioggia',     '21:00:00', 'Inter',          'Bologna',       'Marco Guida',         '2024-01-30', 7, 2,  1, 'San Siro'),
        (48, 'Soleggiato',  '20:45:00', 'Lazio',          'AS Roma',       'Maurizio Mariani',    '2024-01-10', 7, 1,  1, 'Stadio Olimpico'),
        (49, 'Nuvoloso',    '20:45:00', 'Fiorentina',     'Napoli',        'Luca Pairetto',       '2024-01-17', 7, 1,  1, 'Stadio Artemio Franchi'),
        (50, 'Soleggiato',  '20:45:00', 'Atalanta',       'AC Milan',      'Fabio Maresca',       '2024-04-10', 1, 32, 0, 'Gewiss Stadium')
    """)

    cursor.execute("""
        INSERT IGNORE INTO Convocazione (nome_squadra, num_maglia, id_partita, id_giocatore) VALUES
        ('Inter',         10, 1,  1),
        ('Inter',         23, 1,  2),
        ('Inter',         32, 1,  3),
        ('AC Milan',      16, 1,  4),
        ('AC Milan',      10, 1,  5),
        ('AC Milan',      19, 1,  6),
        ('Juventus',       7, 2,  7),
        ('Juventus',      25, 2,  8),
        ('Juventus',       1, 2,  9),
        ('AS Roma',       21, 2,  10),
        ('AS Roma',        7, 2,  11),
        ('AS Roma',       90, 2,  12),
        ('Napoli',         9, 3,  13),
        ('Napoli',        77, 3,  14),
        ('Napoli',        22, 3,  15),
        ('Fiorentina',     4, 6,  16),
        ('Fiorentina',     3, 6,  17),
        ('Fiorentina',    10, 6,  18),
        ('Atalanta',       9, 6,  19),
        ('Atalanta',      15, 6,  20),
        ('Atalanta',      42, 6,  21),
        ('Hellas Verona', 29, 8,  22),
        ('Hellas Verona', 23, 8,  23),
        ('Genoa',         11, 33, 24),
        ('Genoa',          5, 33, 25),
        ('Bologna',        9, 8,  26),
        ('Bologna',        7, 8,  27),
        ('Bologna',       13, 8,  28),
        ('Torino FC',      9, 8,  29),
        ('Torino FC',     13, 8,  30),
        ('Lazio',         17, 7,  31),
        ('Lazio',         10, 7,  32),
        ('Lazio',         20, 7,  33),
        ('Udinese',        3, 34, 34),
        ('Udinese',       11, 34, 35),
        ('Venezia',        9, 35, 36),
        ('Venezia',       99, 35, 37),
        ('Empoli',         9, 39, 38),
        ('Empoli',         3, 39, 39),
        ('Lecce',          9, 33, 40),
        ('Lecce',         30, 33, 41),
        ('Cagliari',      29, 35, 42),
        ('Cagliari',       4, 35, 43),
        ('Como',          10, 23, 44),
        ('Como',           9, 23, 45),
        ('Parma',         77, 46, 46),
        ('Parma',         10, 46, 47),
        ('Monza',          8, 23, 48),
        ('Monza',          9, 23, 49),
        ('Sassuolo',      10, 24, 50)
    """)

    cursor.execute("""
        INSERT IGNORE INTO Infortunio (id_infortunio, tipo_infortunio, data_infortunio, giorni_prognosi, parte_corpo, causa, id_giocatore, id_partita) VALUES
        (1,  'Distorsione',         '2023-09-16', 21,  'Caviglia',       'Contrasto',         1,  1),
        (2,  'Stiramento',          '2023-09-17', 30,  'Coscia',         'Sforzo muscolare',  2,  2),
        (3,  'Contusione',          '2023-09-23', 7,   'Ginocchio',      'Caduta',            3,  3),
        (4,  'Frattura',            '2023-10-01', 90,  'Piede',          'Contrasto',         4,  6),
        (5,  'Lacerazione',         '2023-10-29', 14,  'Sopracciglio',   'Gomitata',          5,  5),
        (6,  'Distorsione',         '2023-11-05', 28,  'Caviglia',       'Cambio direzione',  6,  7),
        (7,  'Stiramento',          '2023-10-07', 21,  'Polpaccio',      'Sprint',            7,  8),
        (8,  'Tendinite',           '2023-10-28', 14,  'Ginocchio',      'Sovraccarico',      8,  9),
        (9,  'Contusione',          '2023-11-12', 5,   'Costole',        'Contrasto aereo',   9,  10),
        (10, 'Rottura legamento',   '2023-11-26', 180, 'Ginocchio',      'Torsione',          10, 11),
        (11, 'Stiramento',          '2023-12-10', 25,  'Ischiocrurali',  'Sforzo muscolare',  11, 12),
        (12, 'Distorsione',         '2023-12-08', 10,  'Caviglia',       'Contrasto',         12, 13),
        (13, 'Contusione',          '2023-12-06', 7,   'Tibia',          'Tackle',            13, 14),
        (14, 'Lussazione',          '2023-12-17', 45,  'Spalla',         'Caduta',            14, 15),
        (15, 'Stiramento',          '2024-01-06', 21,  'Coscia',         'Sprint',            15, 16),
        (16, 'Distorsione',         '2024-01-21', 14,  'Caviglia',       'Contrasto',         16, 17),
        (17, 'Frattura',            '2024-02-11', 60,  'Naso',           'Contrasto aereo',   17, 18),
        (18, 'Tendinite',           '2024-03-10', 20,  'Tendine Achille','Sovraccarico',       18, 19),
        (19, 'Stiramento',          '2024-02-25', 30,  'Adduttori',      'Cambio direzione',  19, 20),
        (20, 'Contusione',          '2024-03-04', 5,   'Quadricipite',   'Tackle',            20, 31),
        (21, 'Distorsione',         '2024-03-03', 21,  'Polso',          'Caduta',            21, 32),
        (22, 'Stiramento',          '2024-03-03', 28,  'Polpaccio',      'Sprint',            22, 33),
        (23, 'Lesione menisco',     '2024-03-04', 90,  'Ginocchio',      'Torsione',          23, 34),
        (24, 'Contusione',          '2024-03-10', 7,   'Costole',        'Contrasto',         24, 35),
        (25, 'Stiramento',          '2024-03-29', 21,  'Ischiocrurali',  'Sforzo muscolare',  25, 36),
        (26, 'Distorsione',         '2024-04-07', 14,  'Caviglia',       'Contrasto',         26, 37),
        (27, 'Contusione',          '2024-04-22', 5,   'Tibia',          'Tackle',            27, 38),
        (28, 'Frattura',            '2024-04-28', 45,  'Dito',           'Contrasto',         28, 39),
        (29, 'Stiramento',          '2024-05-02', 30,  'Coscia',         'Sprint',            29, 40),
        (30, 'Tendinite',           '2024-05-10', 14,  'Ginocchio',      'Sovraccarico',      30, 41),
        (31, 'Distorsione',         '2024-05-13', 21,  'Caviglia',       'Cambio direzione',  31, 42),
        (32, 'Lacerazione',         '2024-05-20', 10,  'Testa',          'Contrasto aereo',   32, 43),
        (33, 'Stiramento',          '2024-05-26', 28,  'Polpaccio',      'Sprint',            33, 44),
        (34, 'Contusione',          '2024-05-26', 7,   'Costole',        'Contrasto',         34, 45),
        (35, 'Distorsione',         '2024-01-16', 14,  'Caviglia',       'Contrasto',         35, 46),
        (36, 'Stiramento',          '2024-01-30', 21,  'Coscia',         'Sforzo muscolare',  36, 47),
        (37, 'Frattura',            '2024-01-10', 60,  'Costola',        'Contrasto aereo',   37, 48),
        (38, 'Tendinite',           '2024-01-17', 20,  'Tendine Achille','Sovraccarico',       38, 49),
        (39, 'Contusione',          '2024-04-10', 5,   'Quadricipite',   'Tackle',            39, 50),
        (40, 'Distorsione',         '2023-11-28', 21,  'Caviglia',       'Contrasto',         40, 26),
        (41, 'Stiramento',          '2023-10-25', 30,  'Ischiocrurali',  'Sprint',            41, 28),
        (42, 'Lesione muscolare',   '2023-10-04', 45,  'Coscia',         'Sforzo muscolare',  42, 29),
        (43, 'Contusione',          '2023-10-05', 7,   'Tibia',          'Tackle',            43, 30),
        (44, 'Distorsione',         '2023-09-16', 14,  'Polso',          'Caduta',            44, 1),
        (45, 'Stiramento',          '2023-09-17', 21,  'Polpaccio',      'Sprint',            45, 2),
        (46, 'Contusione',          '2023-09-23', 5,   'Costole',        'Contrasto aereo',   46, 3),
        (47, 'Frattura',            '2023-10-01', 90,  'Piede',          'Contrasto',         47, 6),
        (48, 'Tendinite',           '2023-10-29', 20,  'Ginocchio',      'Sovraccarico',      48, 5),
        (49, 'Distorsione',         '2023-11-05', 14,  'Caviglia',       'Cambio direzione',  49, 7),
        (50, 'Stiramento',          '2023-10-07', 28,  'Coscia',         'Sforzo muscolare',  50, 8)
    """)

    cursor.execute("""
        INSERT IGNORE INTO Eventi (id_evento, tipo_evento, squadra, id_giocatore, id_partita) VALUES
        (1,  'Gol',            'Inter',         1,  1),
        (2,  'Assist',         'Inter',         2,  1),
        (3,  'Ammonizione',    'AC Milan',      4,  1),
        (4,  'Gol',            'AC Milan',      5,  1),
        (5,  'Gol',            'Juventus',      7,  2),
        (6,  'Ammonizione',    'AS Roma',       10, 2),
        (7,  'Espulsione',     'AS Roma',       11, 2),
        (8,  'Gol',            'Napoli',        13, 3),
        (9,  'Assist',         'Napoli',        14, 3),
        (10, 'Ammonizione',    'Lazio',         31, 3),
        (11, 'Gol',            'AC Milan',      5,  4),
        (12, 'Assist',         'AC Milan',      6,  4),
        (13, 'Gol',            'AC Milan',      5,  4),
        (14, 'Ammonizione',    'Inter',         2,  4),
        (15, 'Gol',            'Atalanta',      19, 6),
        (16, 'Assist',         'Atalanta',      20, 6),
        (17, 'Ammonizione',    'Fiorentina',    16, 6),
        (18, 'Gol',            'Lazio',         31, 7),
        (19, 'Assist',         'Lazio',         32, 7),
        (20, 'Ammonizione',    'Juventus',      8,  7),
        (21, 'Gol',            'Bologna',       26, 8),
        (22, 'Assist',         'Bologna',       27, 8),
        (23, 'Ammonizione',    'Torino FC',     29, 8),
        (24, 'Gol',            'Inter',         1,  9),
        (25, 'Assist',         'Inter',         3,  9),
        (26, 'Gol',            'Inter',         1,  9),
        (27, 'Gol',            'Inter',         2,  9),
        (28, 'Ammonizione',    'Atalanta',      21, 9),
        (29, 'Rigore',         'Napoli',        13, 10),
        (30, 'Parata',         'Juventus',      9,  13),
        (31, 'Gol',            'AC Milan',      5,  14),
        (32, 'Assist',         'AC Milan',      6,  14),
        (33, 'Gol',            'AC Milan',      5,  14),
        (34, 'Gol',            'Inter',         1,  16),
        (35, 'Assist',         'Inter',         2,  16),
        (36, 'Gol',            'Inter',         1,  16),
        (37, 'Ammonizione',    'Lazio',         32, 16),
        (38, 'Gol',            'Inter',         1,  19),
        (39, 'Gol',            'Inter',         2,  19),
        (40, 'Assist',         'Inter',         3,  19),
        (41, 'Gol',            'Napoli',        13, 36),
        (42, 'Assist',         'Napoli',        14, 36),
        (43, 'Ammonizione',    'Juventus',      8,  36),
        (44, 'Gol',            'Inter',         1,  41),
        (45, 'Gol',            'Inter',         2,  41),
        (46, 'Gol',            'Inter',         1,  41),
        (47, 'Assist',         'Inter',         3,  41),
        (48, 'Gol',            'Atalanta',      19, 40),
        (49, 'Assist',         'Atalanta',      20, 40),
        (50, 'Ammonizione',    'AS Roma',       10, 40)
    """)

    cursor.execute("""
        INSERT IGNORE INTO Classifica (id_competizione, stagione, partite_giocate, vittorie, pareggi, sconfitte, gol_fatti, gol_subiti) VALUES
        (1,  2024, 38, 29, 7,  2,  89, 22),
        (2,  2023, 38, 27, 9,  2,  84, 28),
        (3,  2022, 38, 26, 8,  4,  84, 32),
        (4,  2024, 13, 10, 2,  1,  35, 15),
        (5,  2023, 13, 11, 1,  1,  40, 12),
        (6,  2022, 13, 9,  3,  1,  30, 16),
        (7,  2024, 7,  5,  1,  1,  15, 6),
        (8,  2023, 7,  4,  2,  1,  12, 7),
        (9,  2022, 7,  6,  0,  1,  18, 5),
        (10, 2024, 8,  5,  2,  1,  18, 9),
        (11, 2023, 8,  4,  3,  1,  14, 10),
        (12, 2022, 8,  6,  1,  1,  20, 8),
        (13, 2024, 8,  5,  2,  1,  16, 8),
        (14, 2023, 8,  3,  3,  2,  10, 9),
        (15, 2024, 3,  2,  0,  1,  5,  3),
        (16, 2023, 3,  1,  1,  1,  3,  3),
        (17, 2024, 38, 28, 7,  3,  96, 26),
        (18, 2023, 38, 26, 8,  4,  94, 33),
        (19, 2024, 38, 27, 7,  4,  79, 26),
        (20, 2023, 38, 28, 6,  4,  75, 31),
        (21, 2024, 34, 29, 3,  2,  94, 32),
        (22, 2023, 34, 27, 4,  3,  101,32),
        (23, 2024, 38, 26, 8,  4,  83, 37),
        (24, 2023, 38, 24, 7,  7,  75, 45),
        (25, 2024, 34, 22, 9,  3,  74, 29),
        (26, 2024, 34, 25, 6,  3,  100,38),
        (27, 2023, 6,  3,  2,  1,  10, 6),
        (28, 2022, 7,  4,  1,  2,  12, 8),
        (29, 2021, 7,  5,  1,  1,  14, 7),
        (30, 2024, 7,  4,  2,  1,  10, 5),
        (31, 2024, 38, 22, 9,  7,  60, 35),
        (32, 2023, 38, 20, 10, 8,  55, 40),
        (33, 2024, 38, 18, 8,  12, 50, 48),
        (34, 2024, 5,  3,  1,  1,  8,  4),
        (35, 2024, 6,  4,  1,  1,  13, 6),
        (36, 2024, 6,  3,  2,  1,  10, 7),
        (37, 2024, 6,  4,  1,  1,  12, 5),
        (38, 2024, 6,  3,  2,  1,  9,  6),
        (39, 2023, 1,  1,  0,  0,  3,  1),
        (40, 2023, 3,  2,  1,  0,  7,  3),
        (41, 2024, 8,  5,  2,  1,  18, 9),
        (42, 2024, 22, 15, 4,  3,  48, 18),
        (43, 2024, 5,  3,  1,  1,  9,  4),
        (44, 2024, 1,  0,  0,  1,  0,  2),
        (45, 2024, 2,  1,  1,  0,  3,  2),
        (46, 2024, 3,  2,  1,  0,  6,  3),
        (47, 2024, 4,  2,  1,  1,  5,  4),
        (48, 2024, 2,  1,  0,  1,  2,  3),
        (49, 2024, 4,  3,  0,  1,  8,  4),
        (50, 2024, 2,  1,  1,  0,  3,  2)
    """)

   
    print("✅ Tabelle popolate con successo!")


def main():
    print("Connessione a TiDB Cloud...")
    try:
        conn = get_connection()
        cursor = conn.cursor()
        print("✅ Connessione riuscita!")

        crea_tabelle(cursor)
        popola_tabelle(cursor)

        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Database pronto!")

    except Exception as e:
        print(f"❌ Errore: {e}")


if __name__ == "__main__":
    main()