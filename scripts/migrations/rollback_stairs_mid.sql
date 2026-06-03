-- =============================================================================
-- stairs_mid 제거 롤백 (drop_stairs_mid.sql 되돌리기)
-- =============================================================================
-- 사용법 (DB 복구):
--   1) 이 파일 실행 — 추가했던 1층계단↔지하계단 직통 엣지/방위각 제거
--      docker exec -i <CID> mysql -uroot -plowell subway_nav < rollback_stairs_mid.sql
--   2) 백업된 stairs_mid 행 복구
--      cat _backup/stairs_mid_*.sql | docker exec -i <CID> mysql -uroot -plowell subway_nav
--   3) 코드 되돌리기: git revert <커밋 sha> (data/*.json·tests·docs 복원)
--   4) 서버 재시작
-- =============================================================================

USE subway_nav;

-- drop_stairs_mid.sql 가 추가한 직통 엣지/방위각 제거
DELETE FROM node_edges
WHERE (from_node='floor1_stairs' AND to_node='b1_stairs')
   OR (from_node='b1_stairs' AND to_node='floor1_stairs');

DELETE FROM node_directions
WHERE (from_node='floor1_stairs' AND to_node='b1_stairs')
   OR (from_node='b1_stairs' AND to_node='floor1_stairs');

-- 이후 _backup/stairs_mid_*.sql 의 INSERT 들을 실행하면 stairs_mid 완전 복구됨.
