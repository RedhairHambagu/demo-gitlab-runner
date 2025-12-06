from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# 内存存储示例数据
items_db = {
    1: {"id": 1, "name": "示例项目1", "description": "这是第一个示例项目", "created_at": "2024-01-01T10:00:00"},
    2: {"id": 2, "name": "示例项目2", "description": "这是第二个示例项目", "created_at": "2024-01-02T11:00:00"},
    3: {"id": 3, "name": "示例项目3", "description": "这是第三个示例项目", "created_at": "2024-01-03T12:00:00"},
}
next_id = 4

@app.route('/')
def hello():
    """欢迎页面"""
    return """
    <h1>欢迎使用 Flask REST API Demo!</h1>
    <p>这是一个简化的 GitLab CI/CD 演示项目</p>
    <h2>可用的 API 端点:</h2>
    <ul>
        <li>GET / - 欢迎页面（当前页面）</li>
        <li>GET /health - 健康检查</li>
        <li>GET /api/info - 应用信息</li>
        <li>GET /api/items - 获取所有项目</li>
        <li>GET /api/items/&lt;id&gt; - 获取单个项目</li>
        <li>POST /api/items - 创建新项目</li>
    </ul>
    """

@app.route('/health')
def health():
    """健康检查端点"""
    return jsonify({
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "service": "flask-api-demo"
    })

@app.route('/api/info')
def api_info():
    """返回应用信息"""
    return jsonify({
        "app_name": "Flask REST API Demo",
        "version": "1.0.0",
        "description": "简化的 GitLab CI/CD 演示项目",
        "endpoints": {
            "welcome": "/",
            "health": "/health",
            "info": "/api/info",
            "items_list": "/api/items",
            "item_detail": "/api/items/<id>",
            "create_item": "/api/items (POST)"
        }
    })

@app.route('/api/items', methods=['GET'])
def get_items():
    """获取所有项目列表"""
    return jsonify({
        "total": len(items_db),
        "items": list(items_db.values())
    })

@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """获取单个项目详情"""
    item = items_db.get(item_id)
    if item:
        return jsonify(item)
    else:
        return jsonify({"error": "项目不存在"}), 404

@app.route('/api/items', methods=['POST'])
def create_item():
    """创建新项目"""
    global next_id

    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"error": "缺少必需字段 'name'"}), 400

    new_item = {
        "id": next_id,
        "name": data['name'],
        "description": data.get('description', ''),
        "created_at": datetime.now().isoformat()
    }

    items_db[next_id] = new_item
    next_id += 1

    return jsonify(new_item), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=18000)
