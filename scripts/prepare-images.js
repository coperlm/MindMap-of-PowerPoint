import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// 生成 Python 脚本来创建图片
function generatePythonScript() {
  const configPath = path.join(__dirname, '../public/config.json');
  const config = JSON.parse(fs.readFileSync(configPath, 'utf-8'));
  
  const imageFiles = new Set();
  Object.entries(config.nodes).forEach(([title, data]) => {
    data.images.forEach(img => {
      const filename = path.basename(img);
      imageFiles.add({ filename, title });
    });
  });
  
  const pythonScript = `#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import os

# 确保目录存在
os.makedirs('public/images', exist_ok=True)

# 图片配置
images = [
${Array.from(imageFiles).map(({ filename, title }, index) => 
  `    {'file': '${filename}', 'title': '${title}', 'color': (${50 + index * 7}, ${100 + index * 5}, ${200 - index * 3})}`
).join(',\n')}
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

print(f'\\n🎉 成功生成 {len(images)} 张图片！')
`;

  const scriptPath = path.join(__dirname, 'generate_images.py');
  fs.writeFileSync(scriptPath, pythonScript);
  fs.chmodSync(scriptPath, '755');
  
  return scriptPath;
}

// 主函数
function main() {
  try {
    console.log('🚀 开始生成图片脚本...');
    const scriptPath = generatePythonScript();
    console.log(`✅ Python脚本生成成功: ${scriptPath}`);
    console.log('\n📝 下一步：运行以下命令生成图片');
    console.log('   npm run gen:images');
    
  } catch (error) {
    console.error('❌ 生成失败:', error.message);
    process.exit(1);
  }
}

main();
