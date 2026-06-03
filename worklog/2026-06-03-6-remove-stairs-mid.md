# 2026-06-03 — 층사이계단(stairs_mid) 노드 제거 (계단 단순화)

## 한 일
- floor1_hall 제거와 동일 패턴으로 **stairs_mid 제거**, 1층계단↔지하계단 직접 연결.
- 그래프 `data/*.json` 3개 + `tests/fixtures/*.json` 3개 + 테스트 4건 + `docs/05` 정합화.
- DB: `scripts/migrations/drop_stairs_mid.sql`(autocommit) 작성·적용 — fp 28·raw 261·노드·엣지·방위각 삭제 + 1층계단↔지하계단 추가. (화경 영역 대행)
- 전체 79 테스트 그린, 서버 재시작, route 확인(stairs_mid 빠짐), /direction 321° 정상.

## 왜
- 계단(1층계단→층사이계단→지하계단)은 연속 구간인데 중간 노드 때문에 다 안 내려가도 조기 인식. 중간점 제거로 조기전진 지점 1개 감소.
- 방위각은 계단 edge라 진입방향 근사값(1층계단→지하계단 321, 역방향 323). 박경찬 실측 시 교체.

## 롤백 (되돌리기)
- DB: `rollback_stairs_mid.sql` 실행 + `cat _backup/stairs_mid_*.sql | mysql` (백업 보존: scripts/migrations/_backup/)
- 코드: `git revert <이 커밋>`
- 서버 재시작

## 주의 / 다음
- ⚠️ 화경에게 "stairs_mid 제거 내가 함, 중복 작업·시드(subway_nav_full.sql) 갱신은 화경이 정식 반영" 공유 필요 (현재 라이브 DB만 반영, 시드 SQL은 미수정).
- 앱: 구간별 딜레이 적용키로 함(조기전진 보완).

## 관련 커밋
- (이 커밋) feat: stairs_mid 노드 제거 (계단 1층↔B1 직접 연결) + 마이그레이션/롤백
