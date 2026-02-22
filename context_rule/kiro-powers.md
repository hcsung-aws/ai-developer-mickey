# Kiro Powers 작업 가이드

## Powers 동작 방식
- **키워드 기반 동적 활성화**: 설치 후 항상 로딩이 아닌, 대화에서 키워드 매칭 시 POWER.md + steering + MCP 도구가 context에 로딩
- **Hook은 Power와 독립 동작**: `.kiro/hooks/`에 설치되면 Power 활성화 여부와 무관하게 트리거 조건에 따라 실행. 따라서 hook prompt에 필요한 지시를 직접 포함해야 함
- **Steering 조건부 로딩**: POWER.md의 "When to Load Steering Files" 매핑에 따라 작업 맥락별 선택적 로딩

## power-mickey 설계 결정
- Hook: userTriggered + askAgent 방식 (Kiro IDE에서 agentSpawn + runCommand는 동작하지 않음)
- Context loading: 하이브리드 (SESSION-BRIEF + memorygraph 제목/태그만 → on-demand 상세 조회)
- 세션 스크립트: Python (크로스 플랫폼)
- PURPOSE-SCENARIO 관련 내용은 steering 동적 로딩 특성상 5개 파일에 분산 배치

## 알려진 이슈
- memorygraph `get_recent_activity`: Windows에서 `project` 파라미터 필수 (누락 시 hang)
- memorygraph `store_memory`: context에 `{"project_path": "..."}` 키 사용 (`{"project": "..."}` 는 무시됨)
- Kiro IDE `userTriggered` hook은 `askAgent`만 지원

## Windows 반영 명령어
```bash
cp power-mickey/POWER.md /mnt/c/Users/hcsung/work/q/power-mickey/
cp power-mickey/steering/*.md /mnt/c/Users/hcsung/work/q/power-mickey/steering/
sed -i 's/$/\r/' /mnt/c/Users/hcsung/work/q/power-mickey/POWER.md /mnt/c/Users/hcsung/work/q/power-mickey/steering/*.md
```

## Last Updated
2026-02-22
