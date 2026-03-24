import os
from flask import Flask, request

app = Flask(__name__)

# 初始库存清单
inventory = {
    "耳机": 30,
    "数据线": 50,
    "充电器": 20,
    "屏幕": 10,
    "维修配件": 40
}

@app.route('/')
def home():
    # 访问主页直接看实时库存
    items = "".join([f"<li>{k}: {v}</li>" for k, v in inventory.items()])
    return f"<h1>鑫宝通讯 - 实时库存控制台</h1><ul>{items}</ul>"

@app.route('/sale', methods=['POST'])
def sale():
    # 获取原始数据
    data = request.form.to_dict()
    print(f"DEBUG - 原始数据: {data}")

    product = None
    qty_raw = None

    # 1. 自动寻找商品名和数量（适配 q5, q6 或任何带关键字的名字）
    for key, value in data.items():
        if 'product' in key.lower():
            product = value
        if 'quantity' in key.lower():
            qty_raw = value

    if not product or qty_raw is None:
        return f"错误：未找到字段。收到的键: {list(data.keys())}", 400

    # 2. 【核心修复】处理中文编码（把 \u8033 这种转回“耳机”）
    if '\\u' in product:
        try:
            product = product.encode('utf-8').decode('unicode_escape')
        except:
            # 如果转换失败，尝试另一种方式
            import json
            product = json.loads(f'"{product}"')

    try:
        quantity = int(qty_raw)
    except:
        return f"错误：数量 '{qty_raw}' 不是数字", 400

    # 3. 匹配库存
    # 移除可能存在的空格
    product = product.strip()
    
    if product in inventory:
        if inventory[product] >= quantity:
            inventory[product] -= quantity
            res = f"【交易成功】{product} 减少 {quantity}，剩余: {inventory[product]}"
            print(res)
            return res
        return f"【库存不足】{product} 仅剩 {inventory[product]}", 400
    
    return f"【错误】库里没找到 '{product}'。请检查名称是否完全一致。", 400

if __name__ == "__main__":
    # 适配 Render 端口
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
