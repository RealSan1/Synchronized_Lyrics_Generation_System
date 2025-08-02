# YouTube Music 실시간 가사 Chrome 확장 프로그램

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Issues](https://img.shields.io/github/issues/RealSan1/youtube-realtime-lyrics)](https://github.com/RealSan1/youtube-realtime-lyrics/issues)

YouTube Music PC 버전에서 실시간 가사 동기화를 제공하는 Chrome 확장 프로그램입니다. PC 버전은 가사 기능이 없어 사용자 불편을 초래하며, 본 프로젝트는 OpenAI Whisper 모델과 코사인 유사도를 활용한 임베딩 매칭으로 가사를 동기화하여 음악 감상 경험을 향상시킵니다.

## 목차
- [프로젝트 개요](#프로젝트-개요)
- [주요 기능](#주요-기능)
- [기술 스택](#기술-스택)
- [확장 프로그램 구조](#확장-프로그램-구조)
- [데이터베이스 ERD](#데이터베이스-erd)
- [API 문서](#api-문서)
- [사용자 인터페이스](#사용자-인터페이스)
- [성능 결과](#성능-결과)
- [이슈](#이슈)
- [라이선스](#라이선스)

## 프로젝트 개요
YouTube Music의 PC 버전은 실시간 가사 기능을 지원하지 않아 사용자 경험에 한계가 있습니다. 이 Chrome 확장 프로그램은 다음 목표를 달성합니다:
- 현재 재생 중인 음악에 맞춰 가사를 실시간으로 표시.
- OpenAI Whisper 모델로 일반 가사를 시간 동기화된 가사로 변환.
- 코사인 유사도를 활용한 임베딩 매칭으로 동기화 정확도 향상.
- YouTube Music 웹 플레이어에 통합된 직관적 UI 제공.
- 자체 가사 데이터베이스를 통해 최소 80% 동기화 정확도 목표.

## 주요 기능

### 실시간 가사 동기화
- YouTube Music에서 재생 중인 음악에 가사를 실시간으로 동기화.
- 자체 데이터베이스를 통해 80% 이상의 동기화 정확도 제공.

### Whisper 모델 기반 가사 생성
- OpenAI Whisper 모델을 활용해 오디오 스트림에서 가사를 추출하고 시간 동기화:
  - "그렇게 말하지 마" → `[00:31.29] 그렇게 말하지 마`
  - "제발 그녈 욕하지 말아줘" → `[00:34.74] 제발 그녈 욕하지 말아줘`
  - "그 누구보다도 내겐 좋은 여자니까" → `[00:38.91] 그 누구보다도 내겐 좋은 여자니까`

### 코사인 유사도를 이용한 임베딩 매칭
가사 동기화 정확도를 높이기 위해 다음 과정을 거칩니다:
1. **입력 수집**: 사용자가 음악 파일과 원본 가사를 업로드.
2. **보컬 분리 및 정규화**: Demucs를 이용해 보컬을 분리하고, 음성 인식 성능 향상을 위해 음량을 정규화.
3. **Whisper 기반 음성 인식**: OpenAI Whisper 모델을 통해 오디오에서 시간 정보가 포함된 문장을 추출.
4. **임베딩 기반 문장 매칭**: Whisper 결과와 원본 가사를 Sentence-BERT로 임베딩하고, 코사인 유사도를 계산하여 정합 문장을 매칭.
5. **정합 가사 생성**: 매칭된 문장을 시간 순으로 정렬하여 `.json` 형식의 싱크 가사 파일 생성.

### 사용자 인터페이스
- YouTube Music 플레이어에 통합된 간단하고 직관적인 UI.
- 가사 패널을 토글 가능하며, 재생과 동기화된 가사 강조 표시.

## 기술 스택

### 개발 언어
- **Python 3.10.11**: 백엔드 및 Whisper 모델 처리.
- **HTML5**: UI 구조.
- **JavaScript**: 확장 프로그램 로직.
- **CSS**: UI 스타일링.

### AI 모델
- **OpenAI Whisper**: 자동 음성 인식(ASR) 모델. [모델 선정 과정](https://github.com/RealSan1/youtube-realtime-lyrics/issues/1).

### 데이터베이스
- **SQLite**: 트랙 메타데이터 및 동기화 가사 저장.

### 서버
- **FastAPI**: 가사 조회 및 입력 API.

### 개발 환경
- **Visual Studio Code**: 코딩 및 디버깅.
- **HeidiSQL**: SQLite 데이터베이스 관리.
- **FFmpeg**: 오디오/비디오 스트림 처리 및 변환.

## 확장 프로그램 구조
![확장 프로그램 구조](https://github.com/user-attachments/assets/84156811-168b-4011-9535-45f77f1523d8)

- **content.js**: YouTube Music 페이지에서 DOM 정보를 추출하여 트랙 및 재생 상태 식별.
- **background.js**: 브라우저 영역에서 이벤트 리스너 관리.
- **popup.js**: UI 렌더링 및 API 호출.
- **manifest.json**: 확장 프로그램 권한 및 설정.

## 데이터베이스 ERD
![ERD](https://github.com/user-attachments/assets/3aac9f10-2491-4228-b592-2ca755eb4951)

- **lyrics_pending**: 관리자 검증 대기 가사.
- **lyrics**: 동기화된 가사 데이터.
- **tracks**: 트랙 메타데이터(제목, 가수, 앨범).
- **tracks_fts_v2**: 효율적 검색을 위한 Full-Text Search 테이블.

## API 문서

### GET /api/get
- **설명**: 트랙에 대한 동기화된 가사 조회.
- **쿼리 파라미터**:
  | 필드        | 타입   | 설명         |
  |-------------|--------|--------------|
  | trackName   | String | 트랙 제목    |
  | artistName  | String | 가수 이름    |
  | albumName   | String | 앨범 이름    |
- **응답**: JSON 형식의 동기화 가사.
  ![API 응답](https://github.com/user-attachments/assets/cb0d815d-9287-4c78-b401-5a9effca1710)
- **이슈**: 응답 지연 문제 ([이슈 #2](https://github.com/RealSan1/youtube-realtime-lyrics/issues/2)).

### POST /api/input
- **설명**: 새로운 동기화 가사 입력.
- **쿼리 파라미터**:
  | 필드          | 타입   | 설명               |
  |---------------|--------|--------------------|
  | trackName     | String | 트랙 제목          |
  | artistName    | String | 가수 이름          |
  | albumName     | String | 앨범 이름          |
  | duration      | Number | 트랙 길이(초)      |
  | synced_lyrics | String | 동기화 가사        |
- **응답**: 입력 성공/실패 메시지.

## 사용자 인터페이스
![인터페이스](https://github.com/user-attachments/assets/765b8d6c-7bc3-4a15-be5f-ee467c70578c)

- YouTube Music 플레이어에 통합된 스크롤 가능 가사 패널.
- 재생과 동기화된 가사 강조 표시.
- 팝업 버튼으로 가사 패널 토글 가능.

## 성능 결과
- **동기화 정확도**: Whisper 모델로 약 80% 정확도 달성.
- **코사인 유사도**: 입바딩 매칭으로 동기화 오류 10% 감소.
- **API 응답 시간**: 평균 500ms, 최적화 진행 중 ([이슈 #2](https://github.com/RealSan1/youtube-realtime-lyrics/issues/2)).
- **사용자 피드백**: UI 직관성 호평, 테마 사용자화 제안.

## 이슈
- [모델 선정 과정](https://github.com/RealSan1/youtube-realtime-lyrics/issues/1)
- [API 응답 지연](https://github.com/RealSan1/youtube-realtime-lyrics/issues/2)

## 라이선스
이 프로젝트는 [MIT 라이선스](https://github.com/RealSan1/youtube-realtime-lyrics/blob/main/LICENSE)에 따라 배포됩니다.
