# 작업 일지 (worklog)

본 폴더는 코드/문서로 남지 않는 **작업 진행 이력**(무엇을·왜 결정했는지, 뭐에 막혔는지, 다음에 뭘 할지)을 시간순으로 누적합니다. 중간 미팅·최종 발표 시 "어떻게 만들었는지" 설명 자료로 활용 가능합니다.

## 작성 규칙

### 파일 명명

- `YYYY-MM-DD-<slug>.md`
- 예: `2026-05-10-initial-scaffold.md`, `2026-05-15-mid-meeting-prep.md`
- 하루에 여러 건 작업 시: `-1`, `-2` 접미사 또는 슬러그로 구분

### 작성 시점

- **작업 단위**가 끝났을 때 (= 의미 있는 커밋 직후)
- 단순 파일 한두 개 수정은 통합해서 하루 단위로 작성
- 막혀서 중단했을 때도 작성 (다음 세션에서 컨텍스트 회복용)

### 작성 분량

- 한 일: bullet 3~7개
- 왜: bullet 2~4개
- 다음에 할 일: bullet 1~3개
- **문장 X, bullet O. 짧게 유지.**

## 일지 템플릿

````markdown
# YYYY-MM-DD — <한 줄 제목>

## 한 일
- 무엇을 추가/변경했는지

## 왜 이렇게 했는지
- 결정 사유, 대안 비교

## 막힌 것 / 결정 미뤄진 것
- (있을 때만)

## 다음에 할 일
- 다음 작업 단위 1~3개

## 관련 커밋
- `<commit hash>` <commit subject>
````

## 인덱스

| 날짜 | 제목 |
|---|---|
| 2026-05-10 | [Initial scaffold (Flask + 3 APIs + tests + Swagger)](./2026-05-10-initial-scaffold.md) |
| 2026-05-19 | [팀 진척 상황 정리 (단톡방 동기화)](./2026-05-19-team-progress-update.md) |
| 2026-05-21 | [실데이터 통합 + E2E 테스트 + Playwright Swagger UI 검증](./2026-05-21-real-data-integration.md) |
| 2026-05-25 | [팀 진척 동기화 (5/22 미팅 + 안드로이드 앱 1차 완료)](./2026-05-25-team-progress-update.md) |
| 2026-05-25 | [서버 호스팅(ngrok) + 로컬 DB 구축 + 실데이터 검증](./2026-05-25-hosting-and-verification.md) |
| 2026-05-25 | [API 명세↔구현 정합성 점검 + 수정 (rssi float / SSID 필터 / 문서 3건)](./2026-05-25-api-spec-consistency.md) |
| 2026-05-28 | [KNN 측위 개선: 마스킹 거리 (화경, dropout 21%→87.5%)](./2026-05-28-knn-masked-distance.md) |
| 2026-05-31 | [PR #3 main 동기화 + 라이브 서버 갱신](./2026-05-31-pull-knn-update-restart.md) |
| 2026-06-03 | [통합 테스트 진척·이슈 동기화 + 현장 미팅 준비](./2026-06-03-integration-issues-and-onsite-prep.md) |
| 2026-06-03 | [API 로그에 한국어 위치 라벨 추가 (현장 디버깅용)](./2026-06-03-2-korean-location-log.md) |
| 2026-06-03 | [1층홀 제거 PR 후속: 테스트·docs·DB 정합화](./2026-06-03-3-floor1hall-removal-followup.md) |
| 2026-06-03 | [/locate 에 '지나온 노드 제외'(exclude/passed) 옵션 추가](./2026-06-03-4-locate-exclude-passed-nodes.md) |
| 2026-06-03 | [/locate 경로 기반 스무딩 (뒤로 금지 + 한 칸 전진)](./2026-06-03-5-locate-smoothing.md) |
| 2026-06-03 | [층사이계단(stairs_mid) 노드 제거 (계단 단순화)](./2026-06-03-6-remove-stairs-mid.md) |
