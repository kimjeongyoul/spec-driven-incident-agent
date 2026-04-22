# Architecture Specification: AI-Era Experience Sharing (AEES)

## 1. System Overview
이 프로젝트는 AI 시대에 개인이 겪는 실제 기술적 경험, 시행착오, 그리고 해결책을 **'AI가 읽기 쉬운 명세(Spec)'**와 **'사람이 쓰기 좋은 소스(Source)'**로 구조화하여 공유하는 것을 목표로 합니다. 

## 2. Technical Stack & Rationale
- **Documentation**: Markdown (Spec-Driven) - AI와 인간 모두에게 최적화된 인터페이스.
- **Methodology**: Spec-kit Standard - 명세가 코드를 리드하는 방식.
- **Sharing Strategy**: OSS-friendly structure - 누구나 쉽게 가져다 쓰고 기여할 수 있는 구조.

## 3. Layered Architecture
- **Experience Layer (Input)**: 실제 개발 환경에서의 문제 상황과 통찰 기록.
- **Specification Layer (Blueprint)**: 경험을 추상화하여 표준화된 설계도로 변환.
- **Implementation Layer (Source)**: 설계도에 기반한 실제 동작하는 코드와 라이브러리.

## 4. Key Decisions (ADR)
- **ADR-001: Spec-First Approach**: 모든 소스 코드는 반드시 `specs/` 내의 명세를 먼저 가짐으로써 코드의 의도(Intent)를 명확히 함.
