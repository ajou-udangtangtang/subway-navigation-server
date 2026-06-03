-- =============================================================================
-- 층사이계단 중앙(stairs_mid) 노드 제거 마이그레이션
-- =============================================================================
-- 작성: 이예진 (화경 영역 대행, 2026-06-03) | 패턴: drop_floor1_hall.sql
--
-- 배경:
--   계단(1층계단→층사이계단→지하계단)은 물리적으로 하나의 연속 계단인데
--   노드가 3개라, 다 안 내려갔는데 다음 노드로 일찍 인식되는 문제.
--   → 중간 노드 stairs_mid 제거, 1층계단↔지하계단 직접 연결로 단순화.
--
-- 영향:
--   - nodes:          -1 (stairs_mid)
--   - node_edges:     stairs_mid 관련 4개 삭제 + 1층계단↔지하계단 2개 추가
--   - node_directions: 동일 패턴
--   - fingerprints:   -28, raw_measurements: -261
--
-- 방위각 (계단 edge라 진입방향 근사값, 박경찬 실측 시 교체):
--   1층계단 → 지하계단: 321 (NW, 11시) — 기존 1층계단→층사이계단과 동일
--   지하계단 → 1층계단: 323 (NW, 11시) — 기존 지하계단→층사이계단과 동일
--
-- ⚠️ drop_floor1_hall.sql 과 달리 트랜잭션 래퍼 없이 autocommit 으로 즉시 반영.
--    (mysql < file 로 그냥 실행하면 됨)
-- 롤백: rollback_stairs_mid.sql + _backup/stairs_mid_*.sql 참고
-- =============================================================================

USE subway_nav;

-- 1. stairs_mid 관련 엣지/방위각 삭제
DELETE FROM node_edges      WHERE from_node = 'stairs_mid' OR to_node = 'stairs_mid';
DELETE FROM node_directions WHERE from_node = 'stairs_mid' OR to_node = 'stairs_mid';

-- 2. 1층계단 ↔ 지하계단 직접 엣지/방위각 추가
INSERT INTO node_edges (from_node, to_node, edge_type) VALUES
    ('floor1_stairs', 'b1_stairs',     'stairs'),
    ('b1_stairs',     'floor1_stairs', 'stairs');

INSERT INTO node_directions (from_node, to_node, heading_degrees, cardinal, clock_position) VALUES
    ('floor1_stairs', 'b1_stairs',     321, 'NW', 11),
    ('b1_stairs',     'floor1_stairs', 323, 'NW', 11);

-- 3. stairs_mid 측정 데이터/노드 삭제
DELETE FROM raw_measurements WHERE location = 'stairs_mid';
DELETE FROM fingerprints     WHERE location = 'stairs_mid';
DELETE FROM nodes            WHERE location = 'stairs_mid';

-- 결과 확인 (기대: stairs_mid 흔적 0, 신규 엣지 2)
SELECT 'stairs_mid_fp'  AS chk, COUNT(*) AS n FROM fingerprints WHERE location='stairs_mid'
UNION ALL SELECT 'new_edges', COUNT(*) FROM node_edges
    WHERE (from_node,to_node) IN (('floor1_stairs','b1_stairs'),('b1_stairs','floor1_stairs'));
