mport os
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
    return "<h1>库存管理系统已在云端运行</h1><p>接口已就绪。</@app.route('/sale', methods=['POST'])
def sale():
    # 获取表单数据
    data = request.form
    
    # 【核心改动】：兼容你截图里那个带左大括号的字段名
    # 它会同时尝试找 "{product" 和 "product"
    product = data.get('{product') or data.get('product')
    qty_raw = data.get('{quantity') or data.get('quantity')
    
    # 打印日志（方便你在 Render 的 Logs 里看清楚收到了什么）
    print(f"收到请求 - 商品: {product}, 数量: {qty_raw}")

    if not product or qty_raw is None:
        return f"错误：未收到有效数据。收到的原始数据为: {list(data.keys())}", 400

    try:
        quantity = int(qty_raw)
    except (ValueError, TypeError):
        return "错误：数量必须是数字", 400

    # 逻辑判断
    if product in inventory:
        if inventory[product] >= quantity:
            inventory[product] -= quantity
            res_msg = f"成功！{product} 减去 {quantity}，剩余库存: {inventory[product]}"
            print(res_msg)
            return res_msg
        return f"错误：{product} 库存不足（现存 {inventory[product]}）", 400
    else:
        return f"错误：仓库中没有商品 '{product}'，请检查名称是否完全一致", 400

