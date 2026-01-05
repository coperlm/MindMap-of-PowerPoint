<template>
  <div 
    ref="appContainer"
    class="w-full h-full bg-gray-50 flex flex-col outline-none"
    tabindex="0"
    @click="focusApp"
  >
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
        :image-viewer-open="showImageViewer"
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
import { ref, onMounted, nextTick } from 'vue'
import MindMap from './components/MindMap.vue'
import ImageViewer from './components/ImageViewer.vue'

const markdown = ref('')
const imageMapping = ref({})
const showImageViewer = ref(false)
const currentImages = ref([])
const currentNodeTitle = ref('')
const allNodes = ref([])
const currentNodeIndex = ref(0)

// 预加载图片
const preloadImages = (imagePaths) => {
  imagePaths.forEach(path => {
    const img = new Image()
    img.src = path
  })
}

// 预加载相邻节点的图片
const preloadAdjacentNodes = (currentIndex) => {
  const toPreload = []
  
  // 预加载上一个节点
  if (currentIndex > 0) {
    const prevNode = allNodes.value[currentIndex - 1]
    const prevImages = imageMapping.value[prevNode]?.images || []
    toPreload.push(...prevImages)
  }
  
  // 预加载下一个节点
  if (currentIndex < allNodes.value.length - 1) {
    const nextNode = allNodes.value[currentIndex + 1]
    const nextImages = imageMapping.value[nextNode]?.images || []
    toPreload.push(...nextImages)
  }
  
  if (toPreload.length > 0) {
    preloadImages(toPreload)
  }
}

// 加载 Markdown 文件
const loadMarkdown = async () => {
  try {
    const response = await fetch('/index.md')
    markdown.value = await response.text()
  } catch (error) {
    console.error('加载 Markdown 文件失败:', error)
    markdown.value = `# MMPPPT

## 欢迎
### 思维导图式 PPT
### 纯键盘操作
### 全屏图片展示

## 开始使用
### 点击节点查看内容
### 左右键浏览
### Enter 查看图片`
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
    
    // 预加载所有图片（后台静默加载）
    const allImages = []
    Object.values(imageMapping.value).forEach(node => {
      if (node.images) {
        allImages.push(...node.images)
      }
    })
    if (allImages.length > 0) {
      console.log(`开始预加载 ${allImages.length} 张图片...`)
      preloadImages(allImages)
    }
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
    
    // 预加载相邻节点的图片
    preloadAdjacentNodes(currentNodeIndex.value)
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
    
    // 预加载相邻节点
    preloadAdjacentNodes(currentNodeIndex.value)
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
    
    // 预加载相邻节点
    preloadAdjacentNodes(currentNodeIndex.value)
    return true
  }
  return false
}

// 关闭图片查看器
const closeImageViewer = () => {
  showImageViewer.value = false
  currentImages.value = []
  // 恢复焦点到主容器
  nextTick(() => {
    focusApp()
  })
}

// 聚焦到主容器
const focusApp = () => {
  if (appContainer.value) {
    appContainer.value.focus()
  }
}

onMounted(() => {
  loadMarkdown()
  loadConfig()
  
  // 页面加载后自动聚焦
  nextTick(() => {
    focusApp()
  })
})
</script>
