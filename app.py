import os
import hashlib
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# ---------------------------
# 预存字符串列表
strings = [
    "hello",
    "test",
    "123",
    "flask",
    "openai",
    "chatbot",
]

# 计算字符串的SSH SHA-512哈希，并以字典存储
# 这里使用SHA-512算法的十六进制表示
hash_map = {}
for s in strings:
    sha512_hash = hashlib.sha512(s.encode()).hexdigest()
    hash_map[sha512_hash] = s

# ---------------------------
# 指定需要扫描的文件目录，该目录下的文件会被计算SHA-512
FILE_SCAN_DIR = "./files_to_check"

# 计算目录下所有文件的SHA-512哈希，存到文件哈希字典，key为哈希，value为文件路径
file_hash_map = {}

def compute_file_sha512(file_path):
    """
    计算单个文件的SHA-512值，读取文件以二进制模式，分块读取
    """
    sha512 = hashlib.sha512()
    try:
        with open(file_path, "rb") as f:
            while True:
                chunk = f.read(8192)
                if not chunk:
                    break
                sha512.update(chunk)
        return sha512.hexdigest()
    except Exception as e:
        print(f"读取文件出错 {file_path}: {e}")
        return None

def scan_files_in_directory(dir_path):
    """
    遍历目录，递归扫描所有文件，计算SHA-512后存入 file_hash_map
    """
    for root, dirs, files in os.walk(dir_path):
        for filename in files:
            full_path = os.path.join(root, filename)
            file_sha512 = compute_file_sha512(full_path)
            if file_sha512 is not None:
                file_hash_map[file_sha512] = full_path

# 启动时扫描文件目录，构建文件哈希表
if os.path.exists(FILE_SCAN_DIR) and os.path.isdir(FILE_SCAN_DIR):
    scan_files_in_directory(FILE_SCAN_DIR)
else:
    print(f"警告：目录 {FILE_SCAN_DIR} 不存在或者不是目录，文件哈希功能不可用")

# ---------------------------------------------------------
# HTML模板，使用Bootstrap 5，美化界面，护眼模式：黑底+红字
HTML = '''
<!doctype html>
<html lang="zh-CN">
<head>
    <meta charset="utf-8">
    <title>哈希查字符串 & 文件内容 (SHA-512)</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- 引入Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

    <style>
        /* 护眼模式 黑底红字 */
        body, html {
            height: 100%;
            background-color: #121212;
            color: #f44336; /* 红色字体 */
            margin: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        }
        a {
            color: #f44336;
        }
        #chat-container {
            max-width: 600px;
            margin: 30px auto;
            background: #1e1e1e;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgb(244 67 54 / 0.5);
            display: flex;
            flex-direction: column;
            height: 80vh;
            border: 1px solid #f44336;
        }
        #chat-window {
            flex-grow: 1;
            overflow-y: auto;
            padding: 20px;
            border-bottom: 1px solid #f44336;
        }
        .message {
            max-width: 80%;
            margin-bottom: 12px;
            padding: 12px 18px;
            border-radius: 20px;
            word-wrap: break-word;
            white-space: pre-wrap;
        }
        .user-message {
            background-color: #b71c1c; /* 深红背景 */
            color: #ffebee; /* 浅红字体 */
            align-self: flex-end;
            border-bottom-right-radius: 0;
        }
        .bot-message {
            background-color: #311b1b; /* 深暗红背景 */
            color: #f44336; /* 红色字体 */
            align-self: flex-start;
            border-bottom-left-radius: 0;
        }
        #input-area {
            padding: 15px;
            background-color: #1e1e1e;
            border-top: 1px solid #f44336;
        }
        input.form-control {
            background-color: #311b1b;
            border: 1px solid #f44336;
            color: #f44336;
        }
        input.form-control:focus {
            background-color: #4a1313;
            color: #ff7961;
            border-color: #ff7961;
            box-shadow: 0 0 0 0.2rem rgb(244 67 54 / .25);
        }
        button.btn-primary {
            background-color: #b71c1c;
            border-color: #b71c1c;
            color: #ffebee;
        }
        button.btn-primary:hover, button.btn-primary:focus {
            background-color: #f44336;
            border-color: #f44336;
            color: #fff;
            box-shadow: 0 0 8px #f44336;
        }
        /* 滚动条美化 */
        #chat-window::-webkit-scrollbar {
            width: 8px;
        }
        #chat-window::-webkit-scrollbar-thumb {
            background-color: #b71c1c;
            border-radius: 4px;
        }
        #chat-window::-webkit-scrollbar-track {
            background-color: #1e1e1e;
        }
    </style>
</head>
<body>
    <div id="chat-container" class="d-flex flex-column" role="main" aria-label="聊天窗口">
        <div id="chat-window" class="flex-grow-1" aria-live="polite" aria-atomic="false"></div>
        <form id="input-area" class="input-group" onsubmit="return sendMessage();" aria-label="输入哈希查询">
            <input id="hash-input" type="text" class="form-control" placeholder="请输入SHA-512哈希值 (128个十六进制字符)" aria-label="哈希输入" autocomplete="off" required minlength="128" maxlength="128" pattern="[a-fA-F0-9]{128}">
            <button class="btn btn-primary" type="submit" aria-label="发送查询">发送</button>
        </form>
    </div>

    <!-- Bootstrap 5 JS Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>

    <script>
        const chatWindow = document.getElementById('chat-window');
        const hashInput = document.getElementById('hash-input');

        // 向聊天窗口添加信息
        function appendMessage(text, sender) {
            const messageDiv = document.createElement('div');
            messageDiv.classList.add('message');
            if (sender === 'user') {
                messageDiv.classList.add('user-message');
                messageDiv.textContent = "你说：" + text;
            } else if (sender === 'bot') {
                messageDiv.classList.add('bot-message');
                messageDiv.textContent = "系统：" + text;
            }
            chatWindow.appendChild(messageDiv);
            chatWindow.scrollTop = chatWindow.scrollHeight;  // 滚动到底部
        }

        // 发送消息触发事件，调用后端API查询
        function sendMessage() {
            let hashVal = hashInput.value.trim();
            // 校验是否是128个16进制字符
            let regex = /^[a-fA-F0-9]{128}$/;
            if (!regex.test(hashVal)) {
                appendMessage("请输入有效的SHA-512哈希值（128个十六进制字符）", 'bot');
                return false;
            }
            appendMessage(hashVal, 'user');
            hashInput.value = '';
            hashInput.focus();

            fetch('/api/query', {
                method: 'POST',
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({hash: hashVal.toLowerCase()})
            })
            .then(response => response.json())
            .then(data => {
                if (data.result) {
                    appendMessage(data.result, 'bot');
                } else {
                    appendMessage("未找到对应字符串或文件", 'bot');
                }
            })
            .catch(error => {
                appendMessage("查询出错，请稍后再试", 'bot');
            });

            return false; // 阻止默认表单提交
        }

    </script>
</body>
</html>
'''

# ---------------------------
# Flask 路由，渲染主页
@app.route('/')
def index():
    return render_template_string(HTML)

# 查询API，接收哈希，返回字符串或文件路径
@app.route('/api/query', methods=['POST'])
def query_hash():
    data = request.get_json()
    hash_val = data.get('hash','').lower().strip()

    # 先查预存字符串的哈希映射
    if hash_val in hash_map:
        found_str = hash_map[hash_val]
        return jsonify({"result": f"字符串: {found_str}"})

    # 没找到字符串时，查文件哈希映射
    if hash_val in file_hash_map:
        found_path = file_hash_map[hash_val]
        return jsonify({"result": f"文件路径: {found_path}"})

    # 两者都没找到
    return jsonify({"result": None})

# ---------------------------
if __name__ == "__main__":
    # 调试模式启动
    app.run(debug=True)
