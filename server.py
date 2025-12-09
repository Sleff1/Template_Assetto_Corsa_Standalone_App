from flask import Flask, request, jsonify, send_from_directory
import sqlite3
import os
from datetime import datetime

DB = os.path.join(os.path.dirname(__file__), 'laps.db')
APP_DIR = os.path.dirname(__file__)
app = Flask(__name__, static_folder=os.path.join(APP_DIR, 'static'))


def init_db():
    with sqlite3.connect(DB) as conn:
        # Create table with lap_seconds for numeric queries
        conn.execute('''CREATE TABLE IF NOT EXISTS laps
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         car TEXT,
                         track TEXT,
                         lap_time TEXT,
                         lap_seconds REAL,
                         timestamp TEXT)''')
        # If lap_seconds column missing in older DBs, try to add it
        try:
            cur = conn.execute("PRAGMA table_info(laps)")
            cols = [r[1] for r in cur.fetchall()]
            if 'lap_seconds' not in cols:
                conn.execute('ALTER TABLE laps ADD COLUMN lap_seconds REAL')
        except Exception:
            pass


init_db()


@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/api/lap', methods=['POST'])
def post_lap():
    data = request.get_json(force=True)
    car = data.get('car', '')
    track = data.get('track', '')
    lap_time = data.get('time', '')
    ts = data.get('timestamp', datetime.utcnow().isoformat())

    def parse_time_to_seconds(t):
        # Expect formats like MM:SS.mmm or M:SS.mmm or SS.mmm
        try:
            if ':' in t:
                parts = t.split(':')
                minutes = float(parts[-2]) if len(parts) >= 2 else 0.0
                seconds = float(parts[-1])
                return minutes * 60.0 + seconds
            else:
                return float(t)
        except Exception:
            return None

    lap_seconds = parse_time_to_seconds(lap_time)

    with sqlite3.connect(DB) as conn:
        conn.execute('INSERT INTO laps (car, track, lap_time, lap_seconds, timestamp) VALUES (?, ?, ?, ?, ?)',
                     (car, track, lap_time, lap_seconds, ts))
    return jsonify({'status': 'ok'}), 201


@app.route('/api/laps', methods=['GET'])
def get_laps():
    limit = request.args.get('limit', 1000)
    with sqlite3.connect(DB) as conn:
        cur = conn.execute('SELECT id, car, track, lap_time, lap_seconds, timestamp FROM laps ORDER BY id DESC LIMIT ?', (limit,))
        rows = [dict(id=r[0], car=r[1], track=r[2], time=r[3], seconds=r[4], timestamp=r[5]) for r in cur.fetchall()]
    return jsonify(rows)


@app.route('/api/stats', methods=['GET'])
def stats():
    # Basic stats: total laps, best lap per track
    with sqlite3.connect(DB) as conn:
        cur = conn.execute('SELECT COUNT(*) FROM laps')
        total = cur.fetchone()[0]
        cur = conn.execute("SELECT track, MIN(lap_seconds) FROM laps GROUP BY track")
        best_by_track = [{'track': r[0], 'best_time_seconds': r[1]} for r in cur.fetchall()]
    return jsonify({'total': total, 'best_by_track': best_by_track})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
