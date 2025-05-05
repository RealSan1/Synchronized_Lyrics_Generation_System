# YouTube Music RealTime Lyrics
- 유튜브 뮤직 PC버전에서 실시간 가사를 지원하는 확장 프로그램 개발
- PC버전은 가사 기능이 없어 불편을 겪는 사용자 ↑
- 이 프로젝트는 사용자 경험을 개선하고 음악 감상 몰입도를 높이는 것을 목표

## 개발 도구 및 기술 스택

### 개발 언어
- Python 3.10.11
- HTML5
- JavaScript
- CSS

### A.I 모델
- OpenAI whisper (자동 음성 인식(Automatic Speech Recognition, ASR) 모델) [선정 과정](https://github.com/RealSan1/youtube-realtime-lyrics/issues/1)

### 데이터베이스
- SQLite

### 서버
- FastAPI
  
### 개발 환경
- Visual Studio Code
- HeidiSQL
- FFmpeg (디지털 음성 스트림과 영상 스트림에 대해서 다양한 종류의 형태로 기록하고 변환)
  
## 주요 기능 및 기술적 접근

### 실시간 가사 연동
- 유튜브 뮤직에서 재생 중인 음악에 맞춰 가사를 실시간으로 표시
- 자체 가사 데이터베이스를 구축하여 정확도 80%이상의 가상 싱크를 목표

### Ai모델을 활용한 싱크가사 생성
- OpenAI whisper모델을 활용하여 일반가사를 싱크가사로 변경
  - 그렇게 말하지 마 -> [00:31.29] 그렇게 말 하지마
  - 제발 그녈 욕하지 말아줘 -> [00:34.74] 제발 그녈 욕하지 말아줘
  - 그 누구보다도 내겐 좋은 여자니까 -> [00:38.91] 그 누구보다도 내겐 좋은 여자니까

### 사용자 인터페이스
- 직관적이고 사용하기 쉬운 인터페이스를 디자인

### 기술 스택
- JavaScript, HTML, CSS

## 크롬 플러그인 구조
![struct](https://github.com/user-attachments/assets/84156811-168b-4011-9535-45f77f1523d8)

### content.js
- 사용자가 방문한 영역에서 작동하는 스크립트
- 현재 페이지의 DOM의 정보를 전달
  
### background.js
- 브라우저 영역에서 작동하는 스크립트
- 중요한 모든 이벤트 리스너 저장

### popup.js
- 시각적인 기능을 담당
- HTML과 직접 상호작용, background 스크립트와 함께 API 호출

### manifest.json
- 확장프로그램 권한 설정
## DataBase ERD
![ERD](https://github.com/user-attachments/assets/3aac9f10-2491-4228-b592-2ca755eb4951)
- lyrics_pending Table : 관리자 검증 임시 테이블
- lyrics Table : 가사 정보 테이블
- tracks Table : 제목 가수 앨범 정보 테이블
- tracks_fts_v2 : FTS 테이블

## API Documentation 
- GET api/get (싱크가사 제공) [응답 지연 발생](https://github.com/RealSan1/youtube-realtime-lyrics/issues/2)
  - 쿼리 파라미터
    |필드|타입|설명|
    |------|---|---|
    |trackName|String|제목|
    |artistName|String|가수|
    |albumName|String|앨범|
  - 응답
   
    ![응답](https://github.com/user-attachments/assets/cb0d815d-9287-4c78-b401-5a9effca1710)
    
- Post api/input (싱크가사 입력)
  - 쿼리 파라미터
    |필드|타입|설명|
    |------|---|---|
    |trackName|String|제목|
    |artistName|String|가수|
    |albumName|String|앨범|
    |duration|Number|노래 길이|
    |synced_lyrics|String|싱크 가사|

## User Interface
![Interface](https://github.com/user-attachments/assets/765b8d6c-7bc3-4a15-be5f-ee467c70578c)
