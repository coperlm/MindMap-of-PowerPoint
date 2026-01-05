#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import os

# 确保目录存在
os.makedirs('public/images', exist_ok=True)

# 图片配置
images = [
    {'file': 'slide_2.png', 'title': '第一部分：项目概述', 'color': (50, 100, 200)},
    {'file': 'slide_3.png', 'title': '1.1 项目背景', 'color': (57, 105, 197)},
    {'file': 'slide_4.png', 'title': '1.2 市场分析', 'color': (64, 110, 194)},
    {'file': 'slide_5.png', 'title': '1.3 项目目标', 'color': (71, 115, 191)},
    {'file': 'slide_6.png', 'title': '1.4 核心价值', 'color': (78, 120, 188)},
    {'file': 'slide_7.png', 'title': '第二部分：技术方案', 'color': (85, 125, 185)},
    {'file': 'slide_8.png', 'title': '2.1 系统架构', 'color': (92, 130, 182)},
    {'file': 'slide_9.png', 'title': '2.2 前端技术栈', 'color': (99, 135, 179)},
    {'file': 'slide_10.png', 'title': '2.3 后端技术栈', 'color': (106, 140, 176)},
    {'file': 'slide_11.png', 'title': '2.4 数据库设计', 'color': (113, 145, 173)},
    {'file': 'slide_12.png', 'title': '2.5 安全方案', 'color': (120, 150, 170)},
    {'file': 'slide_13.png', 'title': '第三部分：功能模块', 'color': (127, 155, 167)},
    {'file': 'slide_14.png', 'title': '3.1 用户管理', 'color': (134, 160, 164)},
    {'file': 'slide_15.png', 'title': '3.2 权限系统', 'color': (141, 165, 161)},
    {'file': 'slide_16.png', 'title': '3.3 数据分析', 'color': (148, 170, 158)},
    {'file': 'slide_17.png', 'title': '3.4 报表系统', 'color': (155, 175, 155)},
    {'file': 'slide_18.png', 'title': '3.5 消息通知', 'color': (162, 180, 152)},
    {'file': 'slide_19.png', 'title': '第四部分：实施计划', 'color': (169, 185, 149)},
    {'file': 'slide_20.png', 'title': '4.1 第一阶段：需求分析', 'color': (176, 190, 146)},
    {'file': 'slide_21.png', 'title': '4.2 第二阶段：系统设计', 'color': (183, 195, 143)},
    {'file': 'slide_22.png', 'title': '4.3 第三阶段：开发实施', 'color': (190, 200, 140)},
    {'file': 'slide_23.png', 'title': '4.4 第四阶段：测试上线', 'color': (197, 205, 137)},
    {'file': 'slide_24.png', 'title': '第五部分：团队协作', 'color': (204, 210, 134)},
    {'file': 'slide_25.png', 'title': '5.1 团队架构', 'color': (211, 215, 131)},
    {'file': 'slide_26.png', 'title': '5.2 开发流程', 'color': (218, 220, 128)},
    {'file': 'slide_27.png', 'title': '5.3 质量保障', 'color': (225, 225, 125)},
    {'file': 'slide_28.png', 'title': '第六部分：风险管理', 'color': (232, 230, 122)},
    {'file': 'slide_29.png', 'title': '6.1 技术风险', 'color': (239, 235, 119)},
    {'file': 'slide_30.png', 'title': '6.2 进度风险', 'color': (246, 240, 116)},
    {'file': 'slide_31.png', 'title': '6.3 应对策略', 'color': (253, 245, 113)},
    {'file': 'slide_32.png', 'title': '第七部分：总结展望', 'color': (260, 250, 110)},
    {'file': 'slide_33.png', 'title': '7.1 项目成果', 'color': (267, 255, 107)},
    {'file': 'slide_34.png', 'title': '7.2 经验总结', 'color': (274, 260, 104)},
    {'file': 'slide_35.png', 'title': '7.3 未来规划', 'color': (281, 265, 101)}
]

# 生成图片
for i, img_info in enumerate(images, 1):
    img = Image.new('RGB', (1200, 800), img_info['color'])
    draw = ImageDraw.Draw(img)
    
    try:
        font_title = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 48)
        font_subtitle = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 24)
    except:
        font_title = ImageFont.load_default()
        font_subtitle = ImageFont.load_default()
    
    # 绘制标题
    title_text = img_info['title']
    draw.text((50, 350), title_text, fill='white', font=font_title)
    draw.text((50, 420), f'幻灯片 {i}', fill='white', font=font_subtitle)
    
    # 保存
    filepath = os.path.join('public/images', img_info['file'])
    img.save(filepath)
    print(f'✅ 生成: {img_info["file"]} - {title_text}')

print(f'\n🎉 成功生成 {len(images)} 张图片！')
