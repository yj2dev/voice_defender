## 딥보이스 및 보이스 피싱 탐지 앱
- 통화 종료 후 딥보이스 또는 보이스 피싱 여부를 탐지 후 알림을 제공하는 앱
## 개발 기간
- 23.10 ~ 11 1개월
## 개발 인원
- 6명: 앱(본인 외 1명), 서버(본인), 모델(3명), 기획(1명)
## 개발 내용
- 통화 종료 이벤트를 받기 위해 네이티브 코드 작성
- 포그라운드 모드에서 목소리 분석 결과 푸시 알림 구현
- 음성 파일 보안 조치
    - 음성 파일 저장시 cryptography를 사용해 암호화
    - 분석 후 음성 파일 제거
## 시연 영상
<a href="https://www.youtube.com/watch?v=76D2DsDsIkc">보이스 디펜더 시연 영상</a>
## 참고 사항
- 모델 관련 폴더는 용량이 커서 제거했습니다.
<br/><br/>

![image](https://github.com/yj2dev/voice_defender/assets/72322679/8cd73c63-579e-44e2-a06f-07a72f418caa)
![image](https://github.com/yj2dev/voice_defender/assets/72322679/66dded65-5acd-46e2-942d-2ac12a21b595)
![image](https://github.com/yj2dev/voice_defender/assets/72322679/a14410f5-a1b7-4e03-8b37-1e4856be9056)
