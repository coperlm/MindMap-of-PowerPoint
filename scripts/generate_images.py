#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import os

# 确保目录存在
os.makedirs('public/images', exist_ok=True)

# 图片配置
images = [
    {'file': 'slide_2.png', 'title': '🎯 核心功能', 'color': (50, 100, 200)},
    {'file': 'slide_3.png', 'title': '思维导图展示', 'color': (57, 105, 197)},
    {'file': 'slide_4.png', 'title': '全屏图片浏览', 'color': (64, 110, 194)},
    {'file': 'slide_35.png', 'title': '纯键盘操作', 'color': (71, 115, 191)},
    {'file': 'slide_6.png', 'title': '无缝切换', 'color': (78, 120, 188)},
    {'file': 'slide_7.png', 'title': '⌨️ 键盘导航', 'color': (85, 125, 185)},
    {'file': 'slide_8.png', 'title': '左右键浏览节点', 'color': (92, 130, 182)},
    {'file': 'slide_9.png', 'title': 'Enter 查看图片', 'color': (99, 135, 179)},
    {'file': 'slide_10.png', 'title': 'ESC 退出查看', 'color': (106, 140, 176)},
    {'file': 'slide_11.png', 'title': '支持跨节点切换', 'color': (113, 145, 173)},
    {'file': 'slide_12.png', 'title': '🎨 界面特点', 'color': (120, 150, 170)},
    {'file': 'slide_13.png', 'title': '响应式设计', 'color': (127, 155, 167)},
    {'file': 'slide_14.png', 'title': '简洁现代', 'color': (134, 160, 164)},
    {'file': 'slide_15.png', 'title': '高效交互', 'color': (141, 165, 161)},
    {'file': 'slide_16.png', 'title': '专注内容', 'color': (148, 170, 158)},
    {'file': 'slide_17.png', 'title': '🧠 思维导图', 'color': (155, 175, 155)},
    {'file': 'slide_18.png', 'title': '树状结构展示', 'color': (162, 180, 152)},
    {'file': 'slide_19.png', 'title': '节点可展开折叠', 'color': (169, 185, 149)},
    {'file': 'slide_20.png', 'title': '支持多层嵌套', 'color': (176, 190, 146)},
    {'file': 'slide_21.png', 'title': '清晰的层级关系', 'color': (183, 195, 143)},
    {'file': 'slide_22.png', 'title': '📸 图片展示', 'color': (190, 200, 140)},
    {'file': 'slide_23.png', 'title': '100% 全屏显示', 'color': (197, 205, 137)},
    {'file': 'slide_24.png', 'title': '高清无损渲染', 'color': (204, 210, 134)},
    {'file': 'slide_25.png', 'title': '流畅切换体验', 'color': (211, 215, 131)},
    {'file': 'slide_26.png', 'title': '自动预加载', 'color': (218, 220, 128)},
    {'file': 'slide_27.png', 'title': '⚡ 性能优化', 'color': (225, 225, 125)},
    {'file': 'slide_28.png', 'title': '图片预加载', 'color': (232, 230, 122)},
    {'file': 'slide_29.png', 'title': '相邻节点缓存', 'color': (239, 235, 119)},
    {'file': 'slide_30.png', 'title': '无动画切换', 'color': (246, 240, 116)},
    {'file': 'slide_31.png', 'title': '即时响应', 'color': (253, 245, 113)},
    {'file': 'slide_32.png', 'title': '🎓 学术演示', 'color': (260, 250, 110)},
    {'file': 'slide_33.png', 'title': '专业简洁', 'color': (267, 255, 107)},
    {'file': 'slide_34.png', 'title': '无干扰设计', 'color': (274, 260, 104)},
    {'file': 'slide_36.png', 'title': '高效展示', 'color': (281, 265, 101)},
    {'file': 'slide_37.png', 'title': '📱 移动友好', 'color': (288, 270, 98)},
    {'file': 'slide_38.png', 'title': '响应式布局', 'color': (295, 275, 95)},
    {'file': 'slide_39.png', 'title': '触摸支持', 'color': (302, 280, 92)},
    {'file': 'slide_40.png', 'title': '自适应缩放', 'color': (309, 285, 89)},
    {'file': 'slide_41.png', 'title': '完美兼容', 'color': (316, 290, 86)},
    {'file': 'slide_42.png', 'title': '🔧 技术栈', 'color': (323, 295, 83)},
    {'file': 'slide_43.png', 'title': 'Vue 3 框架', 'color': (330, 300, 80)},
    {'file': 'slide_44.png', 'title': 'Vite 构建工具', 'color': (337, 305, 77)},
    {'file': 'slide_45.png', 'title': 'jsMind 导图库', 'color': (344, 310, 74)},
    {'file': 'slide_46.png', 'title': 'Tailwind CSS', 'color': (351, 315, 71)},
    {'file': 'slide_47.png', 'title': '🚀 快速开始', 'color': (358, 320, 68)},
    {'file': 'slide_48.png', 'title': '编辑 index.md', 'color': (365, 325, 65)},
    {'file': 'slide_49.png', 'title': '运行 gen:all', 'color': (372, 330, 62)},
    {'file': 'slide_50.png', 'title': '替换图片', 'color': (379, 335, 59)},
    {'file': 'slide_51.png', 'title': '立即使用', 'color': (386, 340, 56)}
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
