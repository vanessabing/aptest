import os
from flask import Flask, request

app = Flask(__name__)

# 初始库存 - 增加了一些容错性
inventory = {
    "耳机": 30,
    "数据线": 50,
    "充电器": 20,
    "屏幕": 10,
    "维修配件": 40
}

@app.route('/')
def home():
    items = "".join([f"<li>{k}: {v}</li>" for k, v in inventory.items()])
    return f"<h1>鑫宝通讯 - 实时库存</h1><ul>{items}</ul>"

@app.route('/sale', methods=['POST'])
def sale():
    # 拿到 Jotform 发送的所有原始数据
    data = request.form.to_dict()
    print(f"收到请求: {data}")

    product = None
    qty_raw = None

    # 模糊匹配：只要键名里包含 'product' 或 'quantity' 就抓取
    for key, value in data.items():
        if 'product' in key.lower():
            product = value.strip()
        if 'quantity' in key.lower():
            qty_raw = value

    if not product or not qty_raw:
        return f"错误：未找到字段。收到的键有: {list(data.keys())}", 400

    # 处理编码问题：如果 product 是编码格式，尝试转换
    if "\\u" in product:
        try:
            product = product.encode('utf-16').decode('unicode_escape')
        except:
            pass

    try:
        quantity = int(qty_raw)
    except:
        return "错误：数量必须是数字", 400

    # 检查库存
    if product in inventory:
        if inventory[product] >= quantity:
            inventory[product] -= quantity
            return f"【交易成功】{product} 减少 {quantity}，剩余: {inventory[product]}"
        return f"【库存不足】{product} 仅剩 {inventory[product]}", 400
    
    return f"【商品不存在】库里没有 '{product}'，请确保填写的名称与库存清单一致", 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
