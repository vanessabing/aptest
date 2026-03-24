import os
from flask import Flask, request

app = Flask(__name__)

# 初始库存数据库
inventory = {
    "数据线": 50,
    "耳机": 30,
    "充电器": 20,
    "屏幕": 10,
    "维修配件": 40
}

@app.route('/')
def home():
    # 访问主页直接显示当前所有库存
    items = "".join([f"<li>{k}: {v}</li>" for k, v in inventory.items()])
    return f"<h1>鑫宝通讯 - 当前库存控制台</h1><ul>{items}</ul><p>状态：运行中</p >"

@app.route('/sale', methods=['POST'])
def sale():
    # 强制将表单数据转为字典，方便查找
    data = request.form.to_dict()
    print(f"DEBUG - 收到原始数据: {data}")

    product = None
    qty_raw = None

    # 模糊匹配：只要键名里包含 'product' 或 'quantity' 就拿走
    for key, value in data.items():
        if 'product' in key.lower():
            product = value.strip() # 去掉多余空格
        if 'quantity' in key.lower():
            qty_raw = value

    if not product or not qty_raw:
        return f"错误：表单字段不匹配。收到的字段名有: {list(data.keys())}", 400

    try:
        quantity = int(qty_raw)
    except:
        return f"错误：数量 '{qty_raw}' 不是有效数字", 400

    # 执行库存扣减
    if product in inventory:
        if inventory[product] >= quantity:
            inventory[product] -= quantity
            msg = f"成功！{product} 减少 {quantity}，剩余: {inventory[product]}"
            print(msg)
            return msg
        return f"错误：{product} 库存不足（仅剩 {inventory[product]}）", 400
    
    return f"错误：未在库中找到商品 '{product}'。请确认表单填写内容与代码一致。", 400

if __name__ == "__main__":
    # Render 要求的端口配置
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
