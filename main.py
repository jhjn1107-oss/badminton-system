from flask import Flask, Response, request, redirect, url_for


app = Flask(__name__)

# ===== 선착순 신청 데이터 =====
participants = []
MAX_COUNT = 24


# ===== 메인 페이지 =====
@app.route('/')
def index():
    html = f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="utf-8">
        <title>배드민턴 스매싱</title>
        <style>
            body {{ text-align: center; font-family: Arial, sans-serif; }}
            h1 {{ font-size: 40px; }}
            button {{ font-size: 18px; padding: 10px 20px; margin: 5px; }}
        </style>
    </head>
    <body>
        <h1>2026년 1학기 수원대학교 배드민턴 동아리 스매싱입니다</h1>

        <button onclick="location.href='/where'">활동시간 및 장소</button>
        <button onclick="location.href='/money'">회비 내역</button>
        <button onclick="location.href='/apply'">참여 신청</button>
        <button onclick="location.href='/list'">신청자 목록 보기</button>


        <p>현재 신청 인원: {len(participants)} / {MAX_COUNT}</p>
    </body>
    </html>
    """
    return Response(html, content_type='text/html; charset=utf-8')


# ===== 활동시간 / 장소 =====
@app.route('/where')
def where():
    html = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="utf-8">
        <title>활동시간 및 장소</title>
        <style>
            body { text-align: center; font-family: Arial, sans-serif; }
            h1 { font-size: 40px; }
            h2 { font-size: 24px; }
            button { font-size: 16px; padding: 8px 16px; margin-top: 20px; }
        </style>
    </head>
    <body>
        <h1>활동시간 및 장소</h1>
        <h2>화 · 목 17시부터 19시</h2>
        <img src="/static/익스민턴 위치.jpg" width="600">
        <br>
        <button onclick="location.href='/'">돌아가기</button>
    </body>
    </html>
    """
    return Response(html, content_type='text/html; charset=utf-8')


# ===== 회비 내역 =====
@app.route('/money')
def money():
    html = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="utf-8">
        <title>회비 내역</title>
        <style>
            body { text-align: center; font-family: Arial, sans-serif; }
            h1 { font-size: 40px; }
            p { font-size: 20px; }
            button { font-size: 16px; padding: 8px 16px; margin-top: 20px; }
        </style>
    </head>
    <body>
        <h1>회비 내역</h1>
        <p>학기당 회비: 70,000원</p>
        <p>엑셀 들어갈 위치</p>
        <p>추가 문의는 개인톡으로 부탁드립니다.</p>
        <button onclick="location.href='/'">돌아가기</button>
    </body>
    </html>
    """
    return Response(html, content_type='text/html; charset=utf-8')


# ===== 신청 페이지 =====
@app.route('/apply')
def apply():
    html = f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="utf-8">
        <title>참여 신청</title>
    </head>
    <body style="text-align:center;">
        <h1>참여 신청 (선착순 {MAX_COUNT}명)</h1>
        <p>현재 신청 인원: {len(participants)}명</p>

        <form action="/submit" method="post">
            <input type="text" name="name" placeholder="이름 입력" required>
            <button type="submit">신청</button>
        </form>

        <br>
        <button onclick="location.href='/'">돌아가기</button>
    </body>
    </html>
    """
    return Response(html, content_type='text/html; charset=utf-8')


# ===== 신청 처리 =====
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')

    if len(participants) >= MAX_COUNT:
        return Response("❌ 신청 마감되었습니다.<br><a href='/'>돌아가기</a>",
                        content_type='text/html; charset=utf-8')

    if name in participants:
        return Response("⚠ 이미 신청된 이름입니다.<br><a href='/'>돌아가기</a>",
                        content_type='text/html; charset=utf-8')

    participants.append(name)

    return Response(f"✅ 신청 완료: {name}<br><a href='/'>메인으로</a>",
                    content_type='text/html; charset=utf-8')


#신청자 명단
@app.route('/list')
def public_list():
    names = "<br>".join(f"{i+1}. {n}" for i, n in enumerate(participants))

    html = f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="utf-8">
        <title>신청자 목록</title>
        <style>
            body {{ text-align:center; font-family: Arial, sans-serif; }}
            h1 {{ font-size: 36px; }}
            p {{ font-size: 18px; }}
        </style>
    </head>
    <body>
        <h1>신청자 목록</h1>
        <p>현재 신청 인원: {len(participants)}명 / {MAX_COUNT}명</p>

        <div>
            {names if names else "아직 신청자가 없습니다."}
        </div>

        <br>
        <button onclick="location.href='/'">메인으로</button>
    </body>
    </html>
    """
    return Response(html, content_type='text/html; charset=utf-8')



# 관리자 페이지
@app.route('/admin')
def admin():
    names = "<br>".join(f"{i+1}. {n}" for i, n in enumerate(participants))

    html = f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="utf-8">
        <title>신청자 명단</title>
        <style>
            body {{ text-align:center; font-family: Arial, sans-serif; }}
            button {{ font-size:16px; padding:8px 16px; margin:10px; }}
            .danger {{ background-color:#e74c3c; color:white; border:none; }}
        </style>
    </head>
    <body>
        <h1>신청자 명단</h1>
        <p>총 {len(participants)}명</p>

        <div>
            {names if names else "아직 신청자 없음"}
        </div>

        <form action="/admin/reset" method="post"
              onsubmit="return confirm('정말로 모든 신청자를 초기화하시겠습니까?');">
            <button type="submit" class="danger">인원 초기화</button>
        </form>

        <button onclick="location.href='/'">메인으로</button>
    </body>
    </html>
    """
    return Response(html, content_type='text/html; charset=utf-8')

# ===== 관리자: 인원 초기화 (자동으로 /admin으로 돌아감) =====
@app.route('/admin/reset', methods=['POST'])
def admin_reset():
    participants.clear()
    return redirect(url_for('admin'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
