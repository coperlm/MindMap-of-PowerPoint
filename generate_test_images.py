#!/usr/bin/env python3
"""
生成测试图片的脚本
为MMPPPT项目生成示例图片
"""

from PIL import Image, ImageDraw, ImageFont
import os
import json

# 配置
IMAGE_WIDTH = 1200
IMAGE_HEIGHT = 800
OUTPUT_DIR = "public/images"

# 颜色方案
COLORS = [
    ("#3b82f6", "#ffffff"),  # 蓝色
    ("#8b5cf6", "#ffffff"),  # 紫色
    ("#ec4899", "#ffffff"),  # 粉色
    ("#f59e0b", "#ffffff"),  # 橙色
    ("#10b981", "#ffffff"),  # 绿色
    ("#ef4444", "#ffffff"),  # 红色
    ("#06b6d4", "#ffffff"),  # 青色
    ("#8b5cf6", "#ffffff"),  # 靛色
]

def create_test_image(text, output_path, color_index=0):
    """创建一张测试图片"""
    # 创建图片
    bg_color, text_color = COLORS[color_index % len(COLORS)]
    img = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT), bg_color)
    draw = ImageDraw.Draw(img)
    
    # 尝试使用系统字体
    try:
        # Linux 常见中文字体
        font_paths = [
            "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        ]
        
        font = None
        for font_path in font_paths:
            if os.path.exists(font_path):
                font = ImageFont.truetype(font_path, 80)
                break
        
        if font is None:
            font = ImageFont.load_default()
            
    except Exception as e:
        print(f"警告: 无法加载字体，使用默认字体。错误: {e}")
        font = ImageFont.load_default()
    
    # 绘制主标题
    draw.text((IMAGE_WIDTH // 2, IMAGE_HEIGHT // 2 - 50), 
              text, 
              fill=text_color, 
              font=font, 
              anchor="mm")
    
    # 绘制副标题
    try:
        small_font = ImageFont.truetype(font_paths[0] if os.path.exists(font_paths[0]) else font_paths[1], 40)
    except:
        small_font = font
    
    draw.text((IMAGE_WIDTH // 2, IMAGE_HEIGHT // 2 + 80), 
              f"示例图片 - {os.path.basename(output_path)}", 
              fill=text_color, 
              font=small_font, 
              anchor="mm")
    
    # 绘制装饰圆圈
    circle_radius = 150
    draw.ellipse([IMAGE_WIDTH // 2 - circle_radius, 
                  IMAGE_HEIGHT // 2 - circle_radius - 50,
                  IMAGE_WIDTH // 2 + circle_radius, 
                  IMAGE_HEIGHT // 2 + circle_radius - 50], 
                 outline=text_color, 
                 width=5)
    
    # 确保目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # 保存图片
    img.save(output_path, 'PNG')
    print(f"✓ 已生成: {output_path}")

def generate_images_from_config():
    """根据config.json生成所有需要的图片"""
    config_path = "public/config.json"
    
    if not os.path.exists(config_path):
        print(f"错误: 找不到配置文件 {config_path}")
        return
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    color_index = 0
    nodes = config.get('nodes', {})
    
    print(f"\n开始生成测试图片...")
    print(f"共需生成 {sum(len(node['images']) for node in nodes.values())} 张图片\n")
    
    for node_name, node_data in nodes.items():
        images = node_data.get('images', [])
        
        for i, image_path in enumerate(images):
            # 去掉开头的 /
            if image_path.startswith('/'):
                image_path = image_path[1:]
            
            full_path = os.path.join(image_path)
            
            # 生成图片文本
            if len(images) > 1:
                text = f"{node_name}\n({i+1}/{len(images)})"
            else:
                text = node_name
            
            create_test_image(text, full_path, color_index)
            color_index += 1
    
    print(f"\n✅ 所有测试图片生成完成！")
    print(f"📁 图片位置: {OUTPUT_DIR}/")

def generate_additional_examples():
    """生成一些额外的示例图片"""
    examples = [
        ("欢迎页", "public/images/examples/welcome.png", 0),
        ("感谢观看", "public/images/examples/thanks.png", 1),
        ("问题讨论", "public/images/examples/qa.png", 2),
    ]
    
    print("\n生成额外示例图片...")
    for text, path, color in examples:
        create_test_image(text, path, color)

if __name__ == "__main__":
    print("=" * 60)
    print("MMPPPT - 测试图片生成器")
    print("=" * 60)
    
    generate_images_from_config()
    
    # 可选：生成额外的示例图片
    # generate_additional_examples()
    
    print("\n现在可以运行 'npm run dev' 启动项目查看效果！")
