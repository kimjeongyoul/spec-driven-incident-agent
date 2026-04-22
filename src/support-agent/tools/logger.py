import logging
import os
from datetime import datetime

def setup_agent_logger(name="IncidentAgent"):
    """
    에이전트 전용 로그 설정을 생성합니다.
    콘솔 출력과 파일 저장을 모두 지원하며, AI 에이전트 특화 형식을 사용합니다.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # 로그 폴더 생성
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 로그 파일명 (날짜별)
    log_file = os.path.join(log_dir, f"agent_{datetime.now().strftime('%Y%m%d')}.log")

    # 포맷 설정: [시간] [레벨] [컴포넌트] 메시지
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] [%(name)s] %(message)s')

    # 파일 핸들러 (실제 운영 분석용)
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    # 콘솔 핸들러 (실시간 모니터링용)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# 싱글톤 패턴으로 전역에서 사용 가능하도록 설정
agent_logger = setup_agent_logger()
