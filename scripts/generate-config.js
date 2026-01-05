import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// 解析 Markdown 文件，提取所有节点
function parseMarkdown(content) {
  const lines = content.split('\n');
  const nodes = [];
  
  lines.forEach(line => {
    const match = line.match(/^(#{1,6})\s+(.+)$/);
    if (match) {
      const level = match[1].length;
      const title = match[2].trim();
      nodes.push({ level, title });
    }
  });
  
  return nodes;
}

// 生成 config.json
function generateConfig(nodes) {
  const config = {
    nodes: {}
  };
  
  nodes.forEach((node, index) => {
    // 跳过一级标题（根节点）
    if (node.level === 1) {
      return;
    }
    
    const title = node.title;
    
    // 为每个节点生成图片路径
    // 根据节点索引生成对应的图片文件名
    const imageIndex = index + 1;
    
    config.nodes[title] = {
      images: [`/images/slide_${imageIndex}.png`]
    };
  });
  
  return config;
}

// 主函数
function main() {
  try {
    // 读取 index.md
    const mdPath = path.join(__dirname, '../public/index.md');
    const mdContent = fs.readFileSync(mdPath, 'utf-8');
    
    // 解析节点
    const nodes = parseMarkdown(mdContent);
    console.log(`📖 解析到 ${nodes.length} 个节点`);
    
    // 生成配置
    const config = generateConfig(nodes);
    
    // 写入 config.json
    const configPath = path.join(__dirname, '../public/config.json');
    fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
    
    console.log('✅ config.json 生成成功！');
    console.log(`📁 文件位置: ${configPath}`);
    console.log(`📊 配置了 ${Object.keys(config.nodes).length} 个节点`);
    
    // 显示前几个节点
    console.log('\n🔍 节点预览：');
    Object.entries(config.nodes).slice(0, 5).forEach(([title, data]) => {
      console.log(`  - ${title}: ${data.images.join(', ')}`);
    });
    if (Object.keys(config.nodes).length > 5) {
      console.log(`  ... 还有 ${Object.keys(config.nodes).length - 5} 个节点`);
    }
    
  } catch (error) {
    console.error('❌ 生成失败:', error.message);
    process.exit(1);
  }
}

main();
