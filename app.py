import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# 你的模拟数据库
inventory = {
    "数据线": 50,
    "耳机": 30,
    "充电器": 20,
    "屏幕": 10,
    "维修配件": 40
}

@app.route('/')
def home():
    # 访问根目录时返回一个简单的欢迎页，方便测试程序是否活着
    return "<h1>库存管理系统已在云端运行</h1><p>接口已就绪。</p >"

@app.route('/sale', methods=['POST'])
def sale():
    # 兼容 Jotform 的数据获取方式
    # 如果是 JSON 格式（小程序），用 request.json
    # 如果是表单格式（Jotform），用 request.form
    data = request.json if request.is_json else request.form.to_dict()
    
    # 这里的 key "product" 和 "quantity" 需要和你在前端设置的字段名一致
    product = data.get("product")
    qty_raw = data.get("quantity")
    
    if not product or not qty_raw:
        return jsonify({"status": "error", "message": "参数不全"}), 400

    try:
        quantity = int(qty_raw)
    except ValueError:
        return jsonify({"status": "error", "message": "数量必须是数字"}), 400

    if product in inventory:
        if inventory[product] >= quantity:
            inventory[product] -= quantity
            return jsonify({
                "status": "success",
                "product": product,
                "remaining": inventory[product]
            })
        else:
            return jsonify({"status": "error", "message": "库存不足"})
    else:
        return jsonify({"status": "error", "message": "商品不存在"})

# 核心改动：云端部署专用启动代码
if __name__ == "__main__":
    # Render 等平台会通过环境变量 PORT 告诉程序该用哪个端口
    port = int(os.environ.get("PORT", 8080)) 
    # host="0.0.0.0" 意味着允许外网访问
    app.run(host="0.0.0.0", port=port)
