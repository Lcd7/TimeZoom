from io import BytesIO
import base64
from PIL import Image, ImageFont, ImageDraw
from flask import request

def PhotoAddNumber():
    if not request.json:
        return
    number = request.json.get("number")
    if not number:
        print("数据不能为空！")

    img_file = Image.open(r"图片地址")
    font_1 = ImageFont.truetype(r"字体地址", 36)#36为字体大小
    #获取图片对象
    add_number = ImageDraw.Draw(img_file)
    # 添加数字，text里的参数是图片的x，y轴，fill是字体颜色
    add_number.text((355, 20), number, font=font_1, fill="#262728")

    #将图片保存到内存中
    f = BytesIO()
    img_file.save(f, 'jpeg')
    #从内存中取出bytes类型的图片
    data = f.getvalue()
    #将bytes转成base64
    data = base64.b64encode(data).decode()
    return data

'''
前端
# this.edit携带的数据
this.$http.post('请求后端的地址', this.edit
        ).then(res => {
            #创建一个a标签，并将图片的base64直接赋给a标签的href
            var a = document.createElement("a")
            #base64图片显示的固定格式，这里我是直接下载的，没有在html中显示
            a.href = "data:image/jpg;base64," + res.data
            let name = prompt("输入图片名")
            a.download = name + ".jpeg"
            a.click();
          }
        ).catch(e => {
          alert("提交失败，数据有误！")
          console.log(e)
        })       
'''