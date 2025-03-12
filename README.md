# YouTube Music RealTime Lyrics
- 유튜브 뮤직 PC버전에서 실시간 가사를 지원하는 확장 프로그램 개발
- PC버전은 가사 기능이 없어 불편한 사용자가 많습니다.
- 이 프로젝트는 사용자 경험을 개선하고 음악 감상 몰입도를 높이는 데 목표를 두고 있습니다.

## 개발 도구 및 기술 스택
### 개발 언어
- Python 3.12.3
- HTML5
- JavaScript
- CSS

### 데이터베이스
- SQLite

### 서버
- FastAPI
  
### 개발 환경
- Visual Studio Code
- HeidiSQL

## 주요 기능 및 기술적 접근
### 실시간 가사 연동
- 유튜브 뮤직에서 재생 중인 음악에 맞춰 가사를 실시간으로 표시
- 자체 가사 데이터베이스를 구축하여 정확도 95%이상의 가상 싱크를 목표

### 사용자 인터페이스
- 직관적이고 사용하기 쉬운 인터페이스를 디자인
- 다크 모드를 지원하여 사용자의 편의성을 높입니다.

### 기술 스택
- JavaScript, HTML, CSS를 사용하여 개발합니다.
- 가사 데이터베이스 구축 및 관리를 위해 SQLite와 Node.js를 활용

## DataBase ERD
![ERD](https://github.com/user-attachments/assets/0ffdb6bb-08b7-4495-b086-48c794c54882)

## 크롬 플러그인 구조
![struct](https://github.com/user-attachments/assets/b0dd3a8e-c299-4dd8-952c-9faeb3a4ba33)

### contentscript.js
- 사용자가 방문한 영역에서 작동하는 스크립트
- 현재 페이지의 DOM의 정보를 전달
  
### background.js
- 브라우저 영역에서 작동하는 스크립트
- 중요한 모든 이벤트 리스너 저장

### popup.js
- 시각적인 기능을 담당
- HTML과 직접 상호작용, background 스크립트와 함께 API 호출
