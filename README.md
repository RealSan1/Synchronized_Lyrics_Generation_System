# YouTube Music RealTime Lyrics
- 유튜브 뮤직 PC버전에서 실시간 가사를 지원하는 확장 프로그램 개발
- PC버전은 가사 기능이 없어 불편한 사용자가 많습니다.
- 이 프로젝트는 사용자 경험을 개선하고 음악 감상 몰입도를 높이는 데 목표를 두고 있습니다.

## 개발 도구 및 기술 스택

### 개발 언어
- Python 3.10.11
- HTML5
- JavaScript
- CSS

### A.I 모델
- OpenAI whisper (자동 음성 인식(Automatic Speech Recognition, ASR) 모델)

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
- JavaScript, HTML, CSS를 사용하여 개발합니다.

## DataBase ERD
![ERD](https://github.com/user-attachments/assets/0ffdb6bb-08b7-4495-b086-48c794c54882)

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

## Ai모델 선정 과정
### Google Could
  ![GC](https://github.com/user-attachments/assets/9479564e-3662-4464-99dc-d92c8cb47970)

음성을 문자로 변환 시 낮은 정확성과 시간대별 **가사 출력 불가**

### DeepSeek-r1:32B  
1. DeepSeek
![Deep1](https://github.com/user-attachments/assets/afc1e907-f79a-4905-b148-5fee1e195a28)
음악 파일을 단독으로 사용 시 DeepSeek-r1:32B **사용불가**
<br>

2. DeepSeek
![Deep2](https://github.com/user-attachments/assets/51e10bf8-746c-4952-bd5a-edf53fad7d46)
음악 파일 + 가사 파일 함께 사용 시 DeepSeek-r1:32B **사용 가능**

![Deep3](https://github.com/user-attachments/assets/3c6ff58b-2641-435c-805d-51473114a2a0)
77.55%의 정확도 차이로 인한 싱크 **불균형 발생**

## User Interface
![Interface](https://github.com/user-attachments/assets/765b8d6c-7bc3-4a15-be5f-ee467c70578c)

