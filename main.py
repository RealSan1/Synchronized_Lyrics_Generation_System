import os, shutil, sys, subprocess, re
import whisper, uvicorn
from fastapi import FastAPI, UploadFile, Form, File, Request, Query
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from whisper_utils import find_best_match_mcp, get_embedding
from DBconn import get_connection

conn = get_connection()
cursor = conn.cursor()

def parse_time_string(time_str):
    try:
        minutes, seconds = time_str.strip().split(":")
        return float(minutes) * 60 + float(seconds)
    except Exception:
        return None

app = FastAPI()
origins = [
    "http://localhost",  # 허용할 출처 (로컬 환경에서 실행하는 경우)
    "http://localhost:8000",  # 로컬 서버에서 실행 중인 경우
]

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인에서의 요청 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

model = whisper.load_model("large-v3")  # large-v3, base

@app.get("/", response_class=HTMLResponse)
async def serve_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "synced_lyrics_list": None})

@app.post("/search", response_class=HTMLResponse)
async def search_lyrics(request: Request, query: str = Form(...)):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT t.name AS track_title, t.artist_name, l.synced_lyrics
        FROM tracks_fts_v2 f
        JOIN tracks t ON t.id = f.rowid
        JOIN lyrics l ON l.track_id = t.id
        WHERE tracks_fts_v2 MATCH ?
        """, (query,))

    results = cursor.fetchall()
    conn.close()

    synced_lyrics_list = [
        {"track_title": result[0], "artist_name": result[1], "synced_lyrics": result[2]}
        for result in results
    ] if results else None

    return templates.TemplateResponse("index.html", {
        "request": request,
        "synced_lyrics_list": synced_lyrics_list
    })

@app.get("/input", response_class=HTMLResponse)
async def serve_form(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})

@app.post("/process")
async def process(
    request: Request,
    audioFile: UploadFile = File(...),
    plainLyrics: str = Form(...)
):
    filename = os.path.splitext(audioFile.filename)[0]
    input_path = f"uploads/{audioFile.filename}"
    separated_dir = "separated"
    # vocals_path = os.path.join(separated_dir, "htdemucs_ft", filename, "vocals.wav")
    vocals_path = "C:\\Users\\San\\Desktop\\server\\separated\\htdemucs_ft\\카더가든 - 명동콜링 [가사Lyrics]\\vocals.wav"
    os.makedirs("uploads", exist_ok=True)
    print("[1] 파일 저장 완료")
    with open(input_path, "wb") as f:
        shutil.copyfileobj(audioFile.file, f)

    # print("[2] Demucs로 보컬 분리 시작")
    # subprocess.run([
    #     sys.executable, "-m", "demucs",
    #     "--two-stems", "vocals",
    #     "-n", "htdemucs_ft",
    #     "--segment", "7",
    #     "-o", separated_dir,
    #     input_path
    # ], check=True)

    print("[3] Whisper로 분석 시작")
    result = model.transcribe(
        vocals_path,
        language="ko",
        temperature=0.0,
        beam_size=5,
        best_of=5,
        condition_on_previous_text=False,
        verbose=False
    )

    print("[4] 가사 교정 진행 중")
    original_lines = [line.strip() for line in plainLyrics.strip().splitlines() if line.strip()]
    used_originals = set()
    segments = result["segments"]

    matched = 0
    total_score = 0.0
    matched_score = 0.0

    for seg in segments:
        w_line = seg["text"].strip()
        best_line, score = find_best_match_mcp(w_line, original_lines, used_originals)
        seg["corrected_text"] = best_line if best_line else w_line

        total_score += score
        if best_line:
            matched += 1
            matched_score += score
            used_originals.add(best_line)


    print("[5] 분석 및 교정 완료. 결과 반환")
    def format_timestamp(seconds: float) -> str:
        minutes = int(seconds // 60)
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:05.2f}"

    for seg in segments:
        timestamp = format_timestamp(seg['start'])
        print(f"[{timestamp}] {seg['corrected_text']}")

    return templates.TemplateResponse("result.html", {
        "request": request,
        "segments": segments,
    })

@app.post("/save")
async def save_result(request: Request):
    form = await request.form()
    cleaned_data = []

    title = form.get("title")
    artist = form.get("artist")
    album = form.get("album")
    duration = form.get("duration") 

    for key in form:
        if key.startswith("start"):
            index = key[5:]
            start = form.get(f"start{index}")
            text = form.get(f"text{index}")
            deleted = form.get(f"delete{index}") == "1"

            if not start or not text or deleted:
                continue

            cleaned_data.append({
                "start": start,
                "text": text
            })

    synced_lyrics = "\n".join(f"[{item['start']}] {item['text']}" for item in cleaned_data)

    # DB 저장
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO lyrics_pending (
                plain_lyrics, synced_lyrics, track_title, artist_name, album_name, duration,
                source, created_at, updated_at
            )
            VALUES (NULL, ?, ?, ?, ?, ?, 'user', datetime('now'), datetime('now'))
        """, (synced_lyrics, title, artist, album, duration))
        conn.commit()
        conn.close()
    except Exception as e:
        return JSONResponse(content={"message": f"DB 저장 중 오류 발생: {str(e)}"})

    return JSONResponse(content={"message": "DB 저장 완료"})

@app.get("/admin", response_class=HTMLResponse)
async def review_pending(request: Request):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM lyrics_pending")
    entries = cursor.fetchall()
    print(entries)
    conn.close()
    return templates.TemplateResponse("admin.html", {"request": request, "pending_list": entries})

@app.post("/admin/action")
async def handle_admin_action(request: Request):
    form = await request.form()
    entry_id = form.get("entry_id")
    action = form.get("action")

    conn = get_connection()
    cursor = conn.cursor()

    if action == "approve":
        cursor.execute("SELECT * FROM lyrics_pending WHERE id = ?", (entry_id,))
        row = cursor.fetchone()

        if row:
            plain, synced, title, artist, album, duration, source = row[1:8]

            # 소문자 변환
            title_lower = title.lower()
            artist_lower = artist.lower()
            album_lower = album.lower()

            # 트랙 존재 여부 확인
            cursor.execute("""
                SELECT id FROM tracks
                WHERE name_lower = ? AND artist_name_lower = ? AND album_name_lower = ? AND duration = ?
            """, (title_lower, artist_lower, album_lower, duration))
            track = cursor.fetchone()

            if track:
                track_id = track[0]
            else:
                # 트랙 신규 추가
                cursor.execute("""
                    INSERT INTO tracks (name, name_lower, artist_name, artist_name_lower, album_name, album_name_lower, duration, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))
                """, (title, title_lower, artist, artist_lower, album, album_lower, duration))
                track_id = cursor.lastrowid

            # 가사 추가
            cursor.execute("""
                INSERT INTO lyrics (plain_lyrics, synced_lyrics, track_id, has_plain_lyrics, has_synced_lyrics, instrumental, source, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))
            """, (
                plain,
                synced,
                track_id,
                1 if plain else 0,
                1 if synced else 0,
                0,  # instrumental 여부 없음 → 0으로 가정
                source
            ))
            lyrics_id = cursor.lastrowid

            # track에 마지막 가사 ID 업데이트
            cursor.execute("UPDATE tracks SET last_lyrics_id = ?, updated_at = datetime('now') WHERE id = ?", (lyrics_id, track_id))


    elif action == "delete":
        cursor.execute("DELETE FROM lyrics_pending WHERE id = ?", (entry_id,))

    conn.commit()
    conn.close()

    return RedirectResponse(url="/admin", status_code=303)

def normalize_query(s: str) -> str:
    if not s:
        return ""
    s = s.lower()
    s = re.sub(r"\(.*?\)", "", s)
    s = re.sub(r"[^\w\s가-힣]", " ", s)
    return s.strip()

@app.get("/api/get")
async def get_lyrics(
    trackName: str = Query(...),
    artistName: str = Query(...),
    albumName: str = Query(None)
):
    conn = get_connection()
    cursor = conn.cursor()

    # 핵심: 전체 텍스트에 대해 AND 검색
    search_string = f'{normalize_query(trackName)} AND {normalize_query(artistName)} AND {normalize_query(albumName or "")}'

    try:
        cursor.execute("""
            SELECT t.name AS track_title, t.artist_name, t.album_name, l.synced_lyrics 
            FROM tracks_fts_v2 f
            JOIN tracks t ON t.id = f.rowid
            JOIN lyrics l ON l.track_id = t.id
            WHERE tracks_fts_v2 MATCH ?
            ORDER BY 1
        """, (search_string,))

        row = cursor.fetchone()
        if not row:
            return JSONResponse(status_code=404, content={"message": "해당 곡의 가사를 찾을 수 없습니다."})

        return {
            "track_title": row[0],
            "artist_name": row[1],
            "album_name": row[2],
            "synced_lyrics": row[3]
        }

    finally:
        conn.close()



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

# python.exe -m uvicorn main:app --reload