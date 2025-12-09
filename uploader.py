import os, time, requests
from datetime import datetime

# Configure these
SERVER = 'http://127.0.0.1:5000/api/lap'
FILE_PATH = os.path.join(os.path.dirname(__file__), 'session_info.txt')


def tail_and_post(path):
    pos = 0
    if os.path.exists(path):
        pos = os.path.getsize(path)
    while True:
        try:
            if not os.path.exists(path):
                time.sleep(1)
                continue
            size = os.path.getsize(path)
            if size < pos:
                pos = 0
            if size > pos:
                with open(path, 'rb') as f:
                    f.seek(pos)
                    for line in f:
                        try:
                            s = line.decode('utf-8').strip()
                        except Exception:
                            s = line.strip()
                        if not s:
                            continue
                        parts = s.split(',', 2)
                        if len(parts) == 3:
                            car, lap_time, track = parts
                        else:
                            # best-effort parsing
                            car = parts[0] if len(parts) > 0 else ''
                            lap_time = parts[1] if len(parts) > 1 else ''
                            track = parts[2] if len(parts) > 2 else ''
                        ts = datetime.utcnow().isoformat()
                        payload = {'car': car, 'track': track, 'time': lap_time, 'timestamp': ts}
                        try:
                            requests.post(SERVER, json=payload, timeout=5)
                        except Exception as e:
                            print('POST failed:', e)
                    pos = f.tell()
        except Exception as e:
            print('Uploader error:', e)
        time.sleep(1)


if __name__ == '__main__':
    print('Uploader tailing', FILE_PATH)
    tail_and_post(FILE_PATH)
