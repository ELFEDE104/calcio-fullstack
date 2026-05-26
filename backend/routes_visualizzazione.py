"""
routes_visualizzazione.py
-------------------------
Tutte le rotte GET per visualizzazione e ricerca dati.
Responsabile: Laura
"""

from flask import Blueprint, jsonify, request
from database import get_connection

visualizzazione_bp = Blueprint('visualizzazione', __name__)


# =============================================
# SQUADRE
# =============================================

# Lista di tutte le squadre (con filtro opzionale per nome)
@visualizzazione_bp.route('/squadre', methods=['GET'])
def get_squadre():
    try:
        nome = request.args.get('nome', '')
        conn = get_connection()
        cursor = conn.cursor()
        if nome:
            cursor.execute("""
                SELECT * FROM Squadra
                WHERE nome_squadra LIKE %s
                ORDER BY ranking
            """, (f'%{nome}%',))
        else:
            cursor.execute("SELECT * FROM Squadra ORDER BY ranking")
        squadre = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(squadre), 200
    except Exception as e:
        return jsonify({'errore': str(e)}), 500


# Dettaglio di una squadra con allenatore e giocatori
@visualizzazione_bp.route('/squadre/<nome_squadra>', methods=['GET'])
def get_dettaglio_squadra(nome_squadra):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Dati squadra
        cursor.execute("SELECT * FROM Squadra WHERE nome_squadra = %s", (nome_squadra,))
        squadra = cursor.fetchone()
        if not squadra:
            return jsonify({'errore': 'Squadra non trovata'}), 404

        # Allenatore della squadra
        cursor.execute("""
            SELECT * FROM Allenatore WHERE squadra = %s
        """, (nome_squadra,))
        allenatore = cursor.fetchone()

        # Giocatori della squadra
        cursor.execute("""
            SELECT * FROM Giocatore WHERE squadra = %s ORDER BY num_maglia
        """, (nome_squadra,))
        giocatori = cursor.fetchall()

        # Sponsor della squadra
        cursor.execute("""
            SELECT * FROM Sponsor WHERE nome_squadra = %s
        """, (nome_squadra,))
        sponsor = cursor.fetchone()

        cursor.close()
        conn.close()

        return jsonify({
            'squadra': squadra,
            'allenatore': allenatore,
            'giocatori': giocatori,
            'sponsor': sponsor
        }), 200

    except Exception as e:
        return jsonify({'errore': str(e)}), 500


# =============================================
# GIOCATORI
# =============================================

# Lista giocatori con filtri opzionali
@visualizzazione_bp.route('/giocatori', methods=['GET'])
def get_giocatori():
    try:
        squadra = request.args.get('squadra', '')
        ruolo = request.args.get('ruolo', '')
        nazionalita = request.args.get('nazionalita', '')

        conn = get_connection()
        cursor = conn.cursor()

        query = """
            SELECT g.*, c.stipendio, c.clausola_rescissoria, c.data_fine
            FROM Giocatore g
            LEFT JOIN Contratto c ON g.id_giocatore = c.id_giocatore
            WHERE 1=1
        """
        params = []

        if squadra:
            query += " AND g.squadra LIKE %s"
            params.append(f'%{squadra}%')
        if ruolo:
            query += " AND g.ruolo = %s"
            params.append(ruolo)
        if nazionalita:
            query += " AND g.nazionalita LIKE %s"
            params.append(f'%{nazionalita}%')

        query += " ORDER BY g.cognome"

        cursor.execute(query, params)
        giocatori = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(giocatori), 200

    except Exception as e:
        return jsonify({'errore': str(e)}), 500


# Dettaglio giocatore con contratto e infortuni
@visualizzazione_bp.route('/giocatori/<int:id_giocatore>', methods=['GET'])
def get_dettaglio_giocatore(id_giocatore):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Giocatore WHERE id_giocatore = %s", (id_giocatore,))
        giocatore = cursor.fetchone()
        if not giocatore:
            return jsonify({'errore': 'Giocatore non trovato'}), 404

        cursor.execute("SELECT * FROM Contratto WHERE id_giocatore = %s", (id_giocatore,))
        contratto = cursor.fetchone()

        cursor.execute("SELECT * FROM Infortunio WHERE id_giocatore = %s", (id_giocatore,))
        infortuni = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify({
            'giocatore': giocatore,
            'contratto': contratto,
            'infortuni': infortuni
        }), 200

    except Exception as e:
        return jsonify({'errore': str(e)}), 500


# =============================================
# PARTITE
# =============================================

# Lista partite con filtro opzionale per squadra
@visualizzazione_bp.route('/partite', methods=['GET'])
def get_partite():
    try:
        squadra = request.args.get('squadra', '')
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            SELECT p.id_partita, p.meteo,
                   CAST(p.orario_partita AS CHAR) as orario_partita,
                   p.squadra, p.squadra_ospite, p.arbitro,
                   CAST(p.data_partita AS CHAR) as data_partita,
                   p.id_competizione, p.giornata, p.risultato,
                   p.nome_stadio, c.nome as competizione
            FROM Partita p
            LEFT JOIN Competizione c ON p.id_competizione = c.id_competizione
            WHERE 1=1
        """
        params = []

        if squadra:
            query += " AND (p.squadra LIKE %s OR p.squadra_ospite LIKE %s)"
            params.extend([f'%{squadra}%', f'%{squadra}%'])

        query += " ORDER BY p.data_partita DESC"

        cursor.execute(query, params)
        partite = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(partite), 200

    except Exception as e:
        return jsonify({'errore': str(e)}), 500

# Dettaglio partita con eventi e infortuni
@visualizzazione_bp.route('/partite/<int:id_partita>', methods=['GET'])
def get_dettaglio_partita(id_partita):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT p.id_partita, p.meteo,
                   CAST(p.orario_partita AS CHAR) as orario_partita,
                   p.squadra, p.squadra_ospite, p.arbitro,
                   CAST(p.data_partita AS CHAR) as data_partita,
                   p.id_competizione, p.giornata, p.risultato,
                   p.nome_stadio, c.nome as competizione
            FROM Partita p
            LEFT JOIN Competizione c ON p.id_competizione = c.id_competizione
            WHERE p.id_partita = %s
        """, (id_partita,))
        partita = cursor.fetchone()
        if not partita:
            return jsonify({'errore': 'Partita non trovata'}), 404

        cursor.execute("SELECT * FROM Eventi WHERE id_partita = %s", (id_partita,))
        eventi = cursor.fetchall()

        cursor.execute("SELECT * FROM Infortunio WHERE id_partita = %s", (id_partita,))
        infortuni = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify({
            'partita': partita,
            'eventi': eventi,
            'infortuni': infortuni
        }), 200

    except Exception as e:
        return jsonify({'errore': str(e)}), 500


# =============================================
# CLASSIFICA
# =============================================

@visualizzazione_bp.route('/classifica', methods=['GET'])
def get_classifica():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT cl.*, co.nome as competizione
            FROM Classifica cl
            JOIN Competizione co ON cl.id_competizione = co.id_competizione
            ORDER BY cl.vittorie DESC
        """)
        classifica = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(classifica), 200

    except Exception as e:
        return jsonify({'errore': str(e)}), 500


# =============================================
# ALLENATORI
# =============================================

@visualizzazione_bp.route('/allenatori', methods=['GET'])
def get_allenatori():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.*, s.ranking
            FROM Allenatore a
            JOIN Squadra s ON a.squadra = s.nome_squadra
            ORDER BY a.cognome
        """)
        allenatori = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(allenatori), 200

    except Exception as e:
        return jsonify({'errore': str(e)}), 500