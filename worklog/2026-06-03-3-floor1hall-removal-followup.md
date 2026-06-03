# 2026-06-03 — 1층홀 제거 PR 후속: 테스트·docs·DB 정합화

## 한 일
- 화경 PR #4(그래프 JSON에서 floor1_hall 제거, 출입구↔개찰구 직접 연결) + PR #5(DB 마이그레이션 SQL) 머지분 수신
- PR이 손대지 않은 **내 영역 정합화**: `tests/fixtures/*.json` 3개, unit/integration/e2e 테스트 5개, `docs/05-API명세.md`, README·ONBOARDING 스모크 예시, `direction.py`·`route.py` Swagger docstring에서 floor1_hall 제거 → 출입구↔개찰구(268°/81°) 토폴로지로 갱신
- 로컬 DB에 마이그레이션 적용, 서버·ngrok 재기동, 전체 79 테스트 그린 확인

## 왜 이렇게 했는지
- PR #4가 `data/*.json`만 바꿔서 e2e 2건이 깨졌고(실데이터 사용), fixtures는 별도라 안 깨졌지만 프로덕션과 어긋남 → CLAUDE.md "fixtures lockstep" 위반 상태였음
- 방위각은 화경이 기존 값 재배치(출입구→개찰구 268°, 역방향 81°)해서 테스트 기대값 그대로 사용 가능 → 기계적 치환

## 막힌 것 / 결정 미뤄진 것
- **마이그레이션 SQL 함정**: `drop_floor1_hall.sql`이 `START TRANSACTION`만 있고 COMMIT은 의도적으로 뺌(수동 검토용). `mysql < file`로 파이프하면 연결 종료 시 자동 롤백돼 반영 0. autocommit 직접 실행으로 해결. → 팀에 "끝에 COMMIT 필요" 공유 필요
- ngrok 터널이 중간에 죽어있었음 → 재기동 (현장 테스트 전 항상 공개주소 확인 권장)

## 다음에 할 일
- 서버 과제 "이미 지나온 노드 비교 제외"는 estimator 인터페이스에 exclude 인자 추가 합의 후 진행 (앱이 지나온 노드 전송 → 서버 전달 → KNN 제외)
- 앱(최수빈): 경로 안내 중 위치 잡히면 3초간 수집 중단 (회의 결정)

## 관련 커밋
- (이 커밋) test/docs: floor1_hall 제거 후속 정합화
- 선행: e296530(PR#4 그래프), c7a6968(PR#5 마이그레이션 SQL)
