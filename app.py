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
    # 访问主页可以看到所有库存
    items = "".join([f"<li>{k}: {v}</li>" for k, v in inventory.items()])
    return f"<h1>鑫宝通讯 - 实时库存控制台</h1><ul>{items}</ul><p>状态：系统正常运行中</p >"

@app.route('/sale', methods=['POST'])
def sale():
    # 拿到 Jotform 发送的所有原始数据
    data = request.form.to_dict()
    print(f"DEBUG - 收到原始数据: {data}")

    product = None
    qty_raw = None

    # 【终极保障】：遍历所有数据，只要看到名字里带 'product' 或 'quantity' 的就抓取
    for key, value in data.items():
        if 'product' in key.lower():
            product = value.strip()
        if 'quantity' in key.lower():
            qty_raw = value

    if not product or qty_raw is None:
        return f"错误：未找到有效字段。收到的数据: {data}", 400

    try:
        quantity = int(qty_raw)
    except:
        return f"错误：数量 '{qty_raw}' 必须是纯数字", 400

    # 核心扣除逻辑
    if product in inventory:
        if inventory[product] >= quantity:
            inventory[product] -= quantity
            res = f"【交易成功】{product} 减少了 {quantity}，剩余: {inventory[product]}"
            print(res)
            return res
        return f"【库存不足】{product} 仅剩 {inventory[product]}", 400
    
    return f"【商品不匹配】库里没有 '{product}'，请检查名称是否完全一致", 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
