"""
routes_gestione.py
------------------
Tutte le rotte POST, PUT, DELETE per la gestione dei dati.
Responsabile: Federico
"""

from flask import Blueprint, jsonify, request
from database import get_connection

gestione_bp = Blueprint('gestione', __name__)


# =============================================
# GIOCATORI
# =============================================

# Inserimento nuovo giocatore
@gestione_bp.route('/giocatori', methods=['POST'])
def inserisci_giocatore():
    try:
        dati = request.get_json()

        campi_obbligatori = ['id_giocatore', 'nome', 'cognome', 'eta', 'ruolo', 'squadra', 'nazionalita', 'num_maglia']
        for campo in campi_obbligatori:
            if dati.get(campo) is None:
                return jsonify({'errore': f'Campo obbligatorio mancante: {campo}'}), 400

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Giocatore (id_giocatore, nome, cognome, eta, ruolo, squadra, nazionalita, num_maglia)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            dati['id_giocatore'], dati['nome'], dati['cognome'], dati['eta'],
            dati['ruolo'], dati['squadra'],
            dati['nazionalita'], dati['num_maglia']
        ))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'messaggio': 'Giocatore inserito con successo', 'id': dati['id_giocatore']}), 201

    except Exception as e:
        return jsonify({'errore': str(e)}), 500

# Modifica giocatore esistente
@gestione_bp.route('/giocatori/<int:id_giocatore>', methods=['PUT'])
def modifica_giocatore(id_giocatore):
    try:
        dati = request.get_json()
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Giocatore WHERE id_giocatore = %s", (id_giocatore,))
        if not cursor.fetchone():
            return jsonify({'errore': 'Giocatore non trovato'}), 404

        cursor.execute("""
            UPDATE Giocatore
            SET nome = %s, cognome = %s, eta = %s,
                ruolo = %s, squadra = %s,
                nazionalita = %s, num_maglia = %s
            WHERE id_giocatore = %s
        """, (
            dati['nome'], dati['cognome'], dati['eta'],
            dati['ruolo'], dati['squadra'],
            dati['nazionalita'], dati['num_maglia'],
            id_giocatore
        ))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'messaggio': 'Giocatore modificato con successo'}), 200

    except Exception as e:
        return jsonify({'errore': str(e)}), 500


# Eliminazione giocatore
@gestione_bp.route('/giocatori/<int:id_giocatore>', methods=['DELETE'])
def elimina_giocatore(id_giocatore):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Giocatore WHERE id_giocatore = %s", (id_giocatore,))
        if not cursor.fetchone():
            return jsonify({'errore': 'Giocatore non trovato'}), 404

        cursor.execute("DELETE FROM Contratto WHERE id_giocatore = %s", (id_giocatore,))
        cursor.execute("DELETE FROM Infortunio WHERE id_giocatore = %s", (id_giocatore,))
        cursor.execute("DELETE FROM Eventi WHERE id_giocatore = %s", (id_giocatore,))
        cursor.execute("DELETE FROM Convocazione WHERE id_giocatore = %s", (id_giocatore,))
        cursor.execute("DELETE FROM Giocatore WHERE id_giocatore = %s", (id_giocatore,))

        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'messaggio': 'Giocatore eliminato con successo'}), 200

    except Exception as e:
        return jsonify({'errore': str(e)}), 500


# =============================================
# SQUADRE
# =============================================

# Inserimento nuova squadra
@gestione_bp.route('/squadre', methods=['POST'])
def inserisci_squadra():
    try:
        dati = request.get_json()

        campi_obbligatori = ['nome_squadra', 'ranking', 'presidente', 'anno_fondazione', 'num_giocatori', 'trofei_vinti']
        for campo in campi_obbligatori:
            if dati.get(campo) is None:
                return jsonify({'errore': f'Campo obbligatorio mancante: {campo}'}), 400

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Squadra (nome_squadra, capitano, ranking, presidente, anno_fondazione, num_giocatori, trofei_vinti)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            dati['nome_squadra'], dati.get('capitano'),
            dati['ranking'], dati['presidente'],
            dati['anno_fondazione'], dati['num_giocatori'],
            dati['trofei_vinti']
        ))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'messaggio': 'Squadra inserita con successo'}), 201

    except Exception as e:
        return jsonify({'errore': str(e)}), 500


# Modifica squadra
@gestione_bp.route('/squadre/<nome_squadra>', methods=['PUT'])
def modifica_squadra(nome_squadra):
    try:
        dati = request.get_json()
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Squadra WHERE nome_squadra = %s", (nome_squadra,))
        if not cursor.fetchone():
            return jsonify({'errore': 'Squadra non trovata'}), 404

        cursor.execute("""
            UPDATE Squadra
            SET capitano = %s, ranking = %s, presidente = %s,
                anno_fondazione = %s, num_giocatori = %s, trofei_vinti = %s
            WHERE nome_squadra = %s
        """, (
            dati.get('capitano'), dati['ranking'],
            dati['presidente'], dati['anno_fondazione'],
            dati['num_giocatori'], dati['trofei_vinti'],
            nome_squadra
        ))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'messaggio': 'Squadra modificata con successo'}), 200

    except Exception as e:
        return jsonify({'errore': str(e)}), 500


# Eliminazione squadra
@gestione_bp.route('/squadre/<nome_squadra>', methods=['DELETE'])
def elimina_squadra(nome_squadra):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Squadra WHERE nome_squadra = %s", (nome_squadra,))
        if not cursor.fetchone():
            return jsonify({'errore': 'Squadra non trovata'}), 404

        cursor.execute("DELETE FROM Sponsor WHERE nome_squadra = %s", (nome_squadra,))
        cursor.execute("DELETE FROM CentroAllenamento WHERE nome_squadra = %s", (nome_squadra,))
        cursor.execute("DELETE FROM Allenatore WHERE squadra = %s", (nome_squadra,))
        cursor.execute("DELETE FROM Squadra WHERE nome_squadra = %s", (nome_squadra,))

        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'messaggio': 'Squadra eliminata con successo'}), 200

    except Exception as e:
        return jsonify({'errore': str(e)}), 500


# =============================================
# CONTRATTI
# =============================================

# Inserimento nuovo contratto
@gestione_bp.route('/contratti', methods=['POST'])
def inserisci_contratto():
    try:
        dati = request.get_json()

        campi_obbligatori = ['data_inizio', 'data_fine', 'id_giocatore', 'stipendio']
        for campo in campi_obbligatori:
            if not dati.get(campo):
                return jsonify({'errore': f'Campo obbligatorio mancante: {campo}'}), 400

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Contratto (data_inizio, data_fine, id_giocatore, stipendio, clausola_rescissoria)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            dati['data_inizio'], dati['data_fine'],
            dati['id_giocatore'], dati['stipendio'],
            dati.get('clausola_rescissoria')
        ))
        conn.commit()
        nuovo_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return jsonify({'messaggio': 'Contratto inserito con successo', 'id': nuovo_id}), 201

    except Exception as e:
        return jsonify({'errore': str(e)}), 500


# Modifica contratto
@gestione_bp.route('/contratti/<int:id_contratto>', methods=['PUT'])
def modifica_contratto(id_contratto):
    try:
        dati = request.get_json()
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Contratto WHERE id_contratto = %s", (id_contratto,))
        if not cursor.fetchone():
            return jsonify({'errore': 'Contratto non trovato'}), 404

        cursor.execute("""
            UPDATE Contratto
            SET data_inizio = %s, data_fine = %s,
                stipendio = %s, clausola_rescissoria = %s
            WHERE id_contratto = %s
        """, (
            dati['data_inizio'], dati['data_fine'],
            dati['stipendio'], dati.get('clausola_rescissoria'),
            id_contratto
        ))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'messaggio': 'Contratto modificato con successo'}), 200

    except Exception as e:
        return jsonify({'errore': str(e)}), 500


# Eliminazione contratto
@gestione_bp.route('/contratti/<int:id_contratto>', methods=['DELETE'])
def elimina_contratto(id_contratto):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Contratto WHERE id_contratto = %s", (id_contratto,))
        if not cursor.fetchone():
            return jsonify({'errore': 'Contratto non trovato'}), 404

        cursor.execute("DELETE FROM Contratto WHERE id_contratto = %s", (id_contratto,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'messaggio': 'Contratto eliminato con successo'}), 200

    except Exception as e:
        return jsonify({'errore': str(e)}), 500


# =============================================
# ALLENATORI
# =============================================

# Inserimento nuovo allenatore
@gestione_bp.route('/allenatori', methods=['POST'])
def inserisci_allenatore():
    try:
        dati = request.get_json()

        campi_obbligatori = ['nome', 'cognome', 'eta', 'nazionalita', 'squadra', 'trofei_vinti']
        for campo in campi_obbligatori:
            if dati.get(campo) is None:
                return jsonify({'errore': f'Campo obbligatorio mancante: {campo}'}), 400

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Allenatore (nome, cognome, eta, nazionalita, squadra, trofei_vinti)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            dati['nome'], dati['cognome'], dati['eta'],
            dati['nazionalita'], dati['squadra'], dati['trofei_vinti']
        ))
        conn.commit()
        nuovo_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return jsonify({'messaggio': 'Allenatore inserito con successo', 'id': nuovo_id}), 201

    except Exception as e:
        return jsonify({'errore': str(e)}), 500


# Modifica allenatore
@gestione_bp.route('/allenatori/<int:id_allenatore>', methods=['PUT'])
def modifica_allenatore(id_allenatore):
    try:
        dati = request.get_json()
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Allenatore WHERE id_allenatore = %s", (id_allenatore,))
        if not cursor.fetchone():
            return jsonify({'errore': 'Allenatore non trovato'}), 404

        cursor.execute("""
            UPDATE Allenatore
            SET nome = %s, cognome = %s, eta = %s,
                nazionalita = %s, squadra = %s, trofei_vinti = %s
            WHERE id_allenatore = %s
        """, (
            dati['nome'], dati['cognome'], dati['eta'],
            dati['nazionalita'], dati['squadra'],
            dati['trofei_vinti'], id_allenatore
        ))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'messaggio': 'Allenatore modificato con successo'}), 200

    except Exception as e:
        return jsonify({'errore': str(e)}), 500


# Eliminazione allenatore
@gestione_bp.route('/allenatori/<int:id_allenatore>', methods=['DELETE'])
def elimina_allenatore(id_allenatore):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Allenatore WHERE id_allenatore = %s", (id_allenatore,))
        if not cursor.fetchone():
            return jsonify({'errore': 'Allenatore non trovato'}), 404

        cursor.execute("DELETE FROM Allenatore WHERE id_allenatore = %s", (id_allenatore,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'messaggio': 'Allenatore eliminato con successo'}), 200

    except Exception as e:
        return jsonify({'errore': str(e)}), 500