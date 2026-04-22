import os
import glob

def spec_search(keyword: str, base_path: str = "specs"):
    """
    'specs/' 디렉토리 내에서 주어진 키워드를 포함하는 문서를 찾아 내용을 반환합니다.
    """
    results = []
    # specs 폴더 내의 모든 .md 파일 검색
    search_pattern = os.path.join(base_path, "**", "*.md")
    files = glob.glob(search_pattern, recursive=True)

    for file_path in files:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            if keyword.lower() in content.lower():
                results.append(f"--- File: {file_path} ---\n{content}\n")

    if not results:
        return f"키워드 '{keyword}'를 포함하는 명세를 찾을 수 없습니다."
    
    return "\n".join(results)

def code_read(file_path: str):
    """
    파일의 내용을 읽어옵니다.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f"--- File: {file_path} ---\n{f.read()}"
    except Exception as e:
        return f"파일을 읽는 중 오류가 발생했습니다: {str(e)}"
