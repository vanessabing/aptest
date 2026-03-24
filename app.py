import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# 你的初始库存数据库
inventory = {
    "耳机": 30,
    "数据线": 50,
    "充电器": 20,
    "屏幕": 10,
    "维修配件": 40
}

@app.route('/')
def home():
    # 访问这个链接可以直接看到当前库存，方便你点“库存”按钮查看
    items = "".join([f"<li>{k}: {v}</li>" for k, v in inventory.items()])
    return f"<h1>鑫宝通讯 - 当前库存</h1><ul>{items}</ul>"

@app.route('/sale', methods=['POST'])
def sale():
    # 获取 Jotform 发来的所有数据
    data = request.form.to_dict()
    
    # 打印收到的原始数据到 Render 日志，方便调试
    print(f"收到表单数据: {data}")

    # 【核心逻辑】：遍历所有可能的键名，只要包含 product 或 quantity 就抓取
    product = None
    qty_raw = None

    for key, value in data.items():
        if 'product' in key.lower():
            product = value
        if 'quantity' in key.lower():
            qty_raw = value

    # 验证数据是否存在
    if not product:
        return f"错误：未找到商品字段。收到的键名有: {list(data.keys())}", 400
    if not qty_raw:
        return "错误：未找到数量字段", 400

    try:
        quantity = int(qty_raw)
    except (ValueError, TypeError):
        return f"错误：数量 '{qty_raw}' 不是有效的数字", 400

    # 检查库存并扣除
    if product in inventory:
        if inventory[product] >= quantity:
            inventory[product] -= quantity
            msg = f"成功！{product} 减少了 {quantity}，剩余库存: {inventory[product]}"
            print(msg)
            return msg
        else:
            return f"错误：{product} 库存不足（仅剩 {inventory[product]}）", 400
    else:
        # 如果名字不匹配（比如表单填“耳机 ”多了个空格），也会报错提醒
        return f"错误：商品 '{product}' 不在库存清单中。请检查名称是否完全一致。", 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

    else:
        return f"错误：仓库中没有商品 '{product}'，请检查名称是否完全一致", 400

