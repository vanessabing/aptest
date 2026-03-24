import os
from flask import Flask, request

app = Flask(__name__)

# 初始库存
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
    data = request.form.to_dict()
    print(f"收到请求: {data}")

    # 根据你日志里的真实键名来抓取
    product = data.get('q5_product')
    qty_raw = data.get('q6_quantity')

    if not product or not qty_raw:
        return f"错误：没拿到数据。收到的键名是: {list(data.keys())}", 400

    try:
        quantity = int(qty_raw)
    except:
        return "错误：数量必须是数字", 400

    if product in inventory:
        if inventory[product] >= quantity:
            inventory[product] -= quantity
            return f"【交易成功】{product} 减少 {quantity}，剩余: {inventory[product]}"
        return f"【库存不足】{product} 仅剩 {inventory[product]}", 400
    
    return f"【商品不存在】库里没有 '{product}'，请检查表单填写的字是否完全一致", 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
