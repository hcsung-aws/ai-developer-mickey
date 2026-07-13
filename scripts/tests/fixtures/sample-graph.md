# Test Knowledge Graph Fixture

> WELC 스냅샷 목적. parser 회귀 감지용 최소 케이스.

## Nodes
| ID | Title | Tags | Core |
|----|-------|------|------|
| alpha | Alpha Node | tag-a, tag-b | Core desc A |
| beta | Beta Node | tag-b, tag-c | Core desc B |
| gamma | Gamma Node | tag-c | Core desc C |
| alpha | Alpha Duplicate | tag-d | Ignored core |

## Edges
| From | To | Type | Reason |
|------|----|------|--------|
| alpha | beta | applies-to | test reason A |
| beta | gamma | extends | test reason B |
| alpha | ghost | similar-to | dangling target for test |

## Last Updated
2026-07-02 (Test fixture, do not edit outside tests/)
