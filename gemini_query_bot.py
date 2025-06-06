from google import genai         
from google.genai import types 
import sqlite3
import schedule
import time
from datetime import datetime
from config import GEMINI_API_KEY
from database_helper import get_db_connection, init_database, IS_RAILWAY

# 환경변수에서 API 키 가져오기
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY 환경변수를 설정해주세요!")

client = genai.Client(api_key=GEMINI_API_KEY) # Initialize client globally or pass it

# 제미나이한테 보낼 text 작성
query_text = """
1.  페르소나 : 컴퓨터 공학과의 학부 졸업생이 10분 정도 고민해야 풀 수 있는 중상급 수준의 코딩 테스트, 알고리즘, SQL 문제를 출제하는 AI.

2. 작업
1) 너는 대답하지 말고 바로 문제를 출제하면 돼.
2) 아래 알고리즘 카테고리 중에서 랜덤하게 하나를 선택해서 문제를 출제해야 해:
   - 배열/리스트 조작 (Array/List Manipulation)
   - 문자열 처리 (String Processing)  
   - 해시테이블/딕셔너리 (Hash Table/Dictionary)
   - 스택/큐 (Stack/Queue)
   - 연결리스트 (Linked List)
   - 트리 순회 및 탐색 (Tree Traversal/Search)
   - 그래프 탐색 (Graph Search - BFS/DFS)
   - 이진 탐색 (Binary Search)
   - 투 포인터 (Two Pointers)
   - 슬라이딩 윈도우 (Sliding Window)
   - 정렬 알고리즘 (Sorting Algorithms)
   - 그리디 알고리즘 (Greedy Algorithm)
   - 백트래킹 (Backtracking)
   - 비트 조작 (Bit Manipulation)
   - 수학적 알고리즘 (Mathematical Algorithms)
   - 동적 계획법 (Dynamic Programming) - 전체 중 10% 확률로만 선택
3) 문제 중 코딩테스트의 경우는 파이썬으로 내줘. 선택된 알고리즘 카테고리에 맞는 적절한 난이도의 문제를 출제해줘.
4) 학습한 개념을 가지고 객관식 또는 빈칸채우기 문제를 1문제만 문제와 답을 출력 하는데 문제의 답 앞에는 반드시 ★을 넣어 문제와 답을 구분하기 위한 구분자로 사용할거야. 문제는 단순 암기보다는 깊은 이해와 응용이 필요한 수준으로 출제해줘.
5) 디스코드에 문제를 전송할 거라 MarkDown 문법의 수식 표현은 사용하지 말아줘. (예: LaTeX 수식 표현은 사용하지 말 것)

주의사항)
- 반드시 문제는 1문제만 출제해야 해.
- 문제는 객관식 또는 빈칸채우기 중 하나로 출제해야 해. 객관식 문제는 4지선다형으로 출제하고, 빈칸채우기 문제는 코드에서 핵심 부분을 ______로 표시해줘.
- 빈칸채우기 문제에서는 빈칸이 1~3개 정도가 적당해. 너무 많으면 어려워져.
- 빈칸에 들어갈 답은 1~2줄의 간단한 코드여야 해.
- 위에 나열된 알고리즘 카테고리 중에서 매번 다른 주제를 랜덤하게 선택해야 해. 같은 주제가 연속으로 나오면 안 돼.
- 특히 동적 계획법(DP)은 다른 주제들에 비해 덜 자주 선택해야 해. 배열, 문자열, 해시테이블, 트리 등 기본적인 자료구조 문제도 자주 출제해줘.
- ★ 기호는 정확히 "★답:" 형태로 작성해야 해.

3. 예시(객관식 문제 - 이진 탐색 트리)
오늘의 문제- 다음 중 이진 탐색 트리에서 특정 값 k보다 작은 모든 노드의 개수를 O(log n) 시간 복잡도로 구하기 위해 각 노드에 추가로 저장해야 하는 정보는?
- a) 왼쪽 서브트리의 노드 개수
- b) 오른쪽 서브트리의 노드 개수
- c) 자신을 루트로 하는 서브트리의 전체 노드 개수
- d) 부모 노드에 대한 포인터
★답: c) 자신을 루트로 하는 서브트리의 전체 노드 개수

4. 예시(빈칸채우기 문제 - 이진 탐색)
오늘의 문제- 다음은 이진 탐색을 구현한 코드입니다. 빈칸을 채워 완성하세요.

```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = ______
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            ______
        else:
            ______
    
    return -1
```

★답:
1번 빈칸: (left + right) // 2
2번 빈칸: left = mid + 1  
3번 빈칸: right = mid - 1

5. 예시(객관식 문제 - 해시테이블)  
오늘의 문제- 다음 중 Python 딕셔너리에서 키의 해시 충돌이 발생했을 때 사용되는 충돌 해결 방법은?
- a) 체이닝 (Chaining)
- b) 개방 주소법 (Open Addressing)
- c) 이중 해싱 (Double Hashing)
- d) 로빈 후드 해싱 (Robin Hood Hashing)
★답: b) 개방 주소법 (Open Addressing)

6. 예시(빈칸채우기 문제 - 스택)
오늘의 문제- 다음은 괄호의 균형을 확인하는 코드입니다. 빈칸을 채워 완성하세요.

```python
def is_balanced(s):
    stack = []
    pairs = {'(': ')', '[': ']', '{': '}'}
    
    for char in s:
        if char in pairs:
            ______
        elif char in pairs.values():
            if not stack or ______:
                return False
            ______
    
    return len(stack) == 0
```

★답:
1번 빈칸: stack.append(char)
2번 빈칸: pairs[stack[-1]] != char
3번 빈칸: stack.pop()
"""


def generate_quiz():
    """퀴즈를 생성하고 데이터베이스에 저장"""
    max_retries = 5

    for attempt in range(max_retries):
        try:
            print(f"[{datetime.now()}] 새로운 퀴즈를 생성 중... (시도 {attempt + 1}/{max_retries})")
            print(f"🗄️ 데이터베이스 모드: {'메모리 (Railway)' if IS_RAILWAY else '파일 (로컬)'}")            
            response = client.models.generate_content(
                                model = "gemini-2.5-flash-preview-05-20",
                                contents=query_text,
                                config=types.GenerateContentConfig(                                                                                                                                                                
                                    temperature=1.2,
                                    max_output_tokens=5000
                                )
                            )

            if response is None or not hasattr(response, 'text') or response.text is None:
                print(f"❌ 시도 {attempt + 1}: response가 None이거나 text 속성이 없거나 text가 None입니다.")
                continue

            quiz_content = response.text.strip() # Directly access response.text

            if not quiz_content:
                print(f"❌ 시도 {attempt + 1}: 생성된 퀴즈 내용이 비어있거나 공백입니다.")
                continue

            # ★ 구분자 검증
            if '★답:' not in quiz_content: # Only check for the exact '★답:'
                print(f"❌ 시도 {attempt + 1}: 퀴즈에 '★답:' 구분자가 없습니다.")
                continue

            # 성공적으로 응답을 받았으면 나머지 로직 실행
            print(f"✅ 시도 {attempt + 1}에서 성공!")
            break

        except Exception as e:
            print(f"❌ 시도 {attempt + 1} 실패: {e}")
            import traceback
            traceback.print_exc() # Print full traceback for debugging
            if attempt == max_retries - 1:
                print("❌ 모든 재시도 실패. 나중에 다시 시도하세요.")
                return
            time.sleep(5)  # 재시도 전 5초 대기
    else: # This else block runs if the loop completes without a 'break'
        print("❌ 모든 시도에서 유효한 응답을 받지 못했습니다.")
        return    # 나머지 데이터베이스 저장 로직은 그대로...
    try:
        # ★ 구분자로 문제와 답 분리
        def parse_quiz_content(content):
            """퀴즈 내용을 문제와 답으로 분리"""
            if '★답:' not in content:
                return content, "답 없음"
            
            parts = content.split('★답:', 1)
            question = parts[0].strip()
            answer = parts[1].strip() if len(parts) > 1 else "답 없음"
            return question, answer
        
        question, answer = parse_quiz_content(quiz_content)
        
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            'INSERT INTO quizzes (content, question, answer) VALUES (?, ?, ?)',
            (quiz_content, question, answer)
        )

        conn.commit() # Commit regardless of Railway or local for consistency
        conn.close()

        quiz_id = cursor.lastrowid

        print(f"✅ 퀴즈 ID {quiz_id} 생성 완료!")
        print(f"📝 내용 미리보기: {quiz_content[:100]}...")

        # 파일 백업 저장
        try:
            with open("cote_bot.txt", "a", encoding="utf-8") as file:
                file.write(f"\n[{datetime.now()}] Quiz ID: {quiz_id}\n")
                file.write(quiz_content)
                file.write("\n" + "="*130 + "\n")
        except Exception as file_error:
            print(f"⚠️ 파일 백업 실패: {file_error}") # This is usually fine on Railway if it's ephemeral storage

    except Exception as e:
        print(f"❌ 데이터베이스 저장 중 오류: {e}")
        import traceback
        traceback.print_exc()

def run_scheduler():
    """스케줄러 실행"""
    print("🕐 퀴즈 생성 스케줄러를 시작합니다...")
    print("📅 30분마다 새로운 퀴즈가 생성됩니다.")
    
    # 데이터베이스 초기화
    init_database()
    
    
    # 첫 번째 퀴즈 즉시 생성
    generate_quiz()

    # 30분마다 퀴즈 생성 스케줄
    schedule.every(30).minutes.do(generate_quiz)

    # 스케줄러 실행
    while True:
        schedule.run_pending()
        time.sleep(60)  # 1분마다 체크

if __name__ == "__main__":
    run_scheduler()
