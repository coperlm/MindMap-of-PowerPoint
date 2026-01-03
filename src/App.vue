<template>
  <div class="w-full h-full bg-gray-50 flex flex-col">
    <!-- 顶部导航栏 -->
    <header class="bg-white shadow-sm px-6 py-4 flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <div class="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
          <span class="text-white font-bold text-sm">MM</span>
        </div>
        <h1 class="text-xl font-bold text-gray-800">MMPPPT</h1>
      </div>
      <div class="text-sm text-gray-600">
        {{ currentNodeTitle || '点击节点查看内容' }}
      </div>
    </header>

    <!-- 主内容区 -->
    <main class="flex-1 overflow-hidden relative">
      <!-- 思维导图 -->
      <MindMap 
        :markdown="markdown" 
        :image-mapping="imageMapping"
        @node-click="handleNodeClick"
        class="w-full h-full"
      />

      <!-- 图片查看器 -->
      <ImageViewer 
        v-if="showImageViewer"
        :images="currentImages"
        :title="currentNodeTitle"
        :has-prev-node="currentNodeIndex > 0"
        :has-next-node="currentNodeIndex < allNodes.length - 1"
        @close="closeImageViewer"
        @prev-node="gotoPrevNode"
        @next-node="gotoNextNode"
      />
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import MindMap from './components/MindMap.vue'
import ImageViewer from './components/ImageViewer.vue'

const markdown = ref('')
const imageMapping = ref({})
const showImageViewer = ref(false)
const currentImages = ref([])
const currentNodeTitle = ref('')
const allNodes = ref([])
const currentNodeIndex = ref(0)

// 加载 Markdown 文件
const loadMarkdown = async () => {
  try {
    const response = await fetch('/index.md')
    markdown.value = await response.text()
  } catch (error) {
    console.error('加载 Markdown 文件失败:', error)
    markdown.value = `# 欢迎使用 MMPPPT

## 快速开始
### 创建你的内容
### 添加图片映射

## 示例章节
### 示例节点 1
### 示例节点 2

## 更多功能
### 支持多级嵌套
### 自由扩展结构`
  }
}

// 加载配置文件
const loadConfig = async () => {
  try {
    const response = await fetch('/config.json')
    const config = await response.json()
    imageMapping.value = config.nodes || {}
    
    // 构建所有有图片的节点列表
    allNodes.value = Object.keys(imageMapping.value).filter(key => {
      return imageMapping.value[key]?.images?.length > 0
    })
    console.log('所有有图片的节点:', allNodes.value)
  } catch (error) {
    console.warn('未找到配置文件，将使用默认配置')
  }
}

// 处理节点点击
const handleNodeClick = (nodeData) => {
  const title = nodeData.content
  currentNodeTitle.value = title
  
  console.log('App 收到点击事件:', title)
  console.log('当前图片映射:', imageMapping.value)
  
  // 从映射中查找对应的图片
  const images = imageMapping.value[title]?.images || []
  
  console.log('找到的图片:', images)
  
  if (images.length > 0) {
    // 找到当前节点在列表中的索引
    currentNodeIndex.value = allNodes.value.indexOf(title)
    currentImages.value = images
    showImageViewer.value = true
  } else {
    // 显示提示信息
    alert(`节点 "${title}" 没有关联的图片\n\n请在 config.json 中为该节点配置图片路径`)
    console.log('该节点没有关联的图片，可用的节点:', Object.keys(imageMapping.value))
  }
}

// 切换到上一个节点
const gotoPrevNode = () => {
  if (currentNodeIndex.value > 0) {
    currentNodeIndex.value--
    const nodeName = allNodes.value[currentNodeIndex.value]
    currentNodeTitle.value = nodeName
    currentImages.value = imageMapping.value[nodeName]?.images || []
    return true
  }
  return false
}

// 切换到下一个节点
const gotoNextNode = () => {
  if (currentNodeIndex.value < allNodes.value.length - 1) {
    currentNodeIndex.value++
    const nodeName = allNodes.value[currentNodeIndex.value]
    currentNodeTitle.value = nodeName
    currentImages.value = imageMapping.value[nodeName]?.images || []
    return true
  }
  return false
}

// 关闭图片查看器
const closeImageViewer = () => {
  showImageViewer.value = false
  currentImages.value = []
}

onMounted(() => {
  loadMarkdown()
  loadConfig()
})
</script>
