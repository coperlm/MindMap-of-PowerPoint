<template>
  <div 
    ref="jsmindContainer"
    tabindex="0"
    class="relative w-full h-full bg-white focus:outline-none"
  >
    <!-- 控制按钮和提示 -->
    <div class="absolute top-4 right-4 z-10 flex flex-col gap-2">
      <div class="flex gap-2">
        <button 
          @click="zoomIn"
          class="px-4 py-2 bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow border border-gray-200 text-sm font-medium text-gray-700 hover:text-blue-600"
        >
          放大
        </button>
        <button 
          @click="zoomOut"
          class="px-4 py-2 bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow border border-gray-200 text-sm font-medium text-gray-700 hover:text-blue-600"
        >
          缩小
        </button>
      </div>
      
      <!-- 键盘提示 - 可折叠 -->
      <div class="bg-white rounded-lg shadow-md border border-gray-200 overflow-hidden">
        <button 
          @click="toggleKeyboardHelp"
          class="w-full px-4 py-2 text-xs font-semibold text-gray-800 hover:bg-gray-50 transition-colors flex items-center justify-between"
        >
          <span>⌨️ 键盘导航</span>
          <svg 
            :class="['w-4 h-4 transition-transform', { 'rotate-180': showKeyboardHelp }]"
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </button>
        <div 
          v-show="showKeyboardHelp"
          class="px-4 pb-3 pt-1 text-xs text-gray-600 space-y-1 border-t border-gray-100"
        >
          <div><span class="font-mono bg-gray-100 px-2 py-0.5 rounded">→</span> 进入子节点/下一个</div>
          <div><span class="font-mono bg-gray-100 px-2 py-0.5 rounded">←</span> 返回父节点</div>
          <div><span class="font-mono bg-gray-100 px-2 py-0.5 rounded">Enter</span> 查看图片</div>
        </div>
      </div>
    </div>
    
    <!-- 思维导图内容区 -->
    <div ref="mindmapContent" class="w-full h-full"></div>
    
    <!-- 提示信息 -->
    <div v-if="!markdown" class="absolute inset-0 flex items-center justify-center">
      <div class="text-center">
        <div class="text-6xl mb-4">🧠</div>
        <p class="text-gray-500">加载中...</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted, nextTick, computed } from 'vue'
import jsMind from 'jsmind'
import 'jsmind/style/jsmind.css'

const props = defineProps({
  markdown: {
    type: String,
    default: ''
  },
  imageMapping: {
    type: Object,
    default: () => ({})
  },
  imageViewerOpen: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['node-click'])

const imageMapping = computed(() => props.imageMapping)

const jsmindContainer = ref(null)
const mindmapContent = ref(null)
let jm = null
const nodeList = ref([])
const currentNodeIndex = ref(0)
const nodeElements = ref([])
const nodeDataMap = ref(new Map())
const showKeyboardHelp = ref(false)

// 切换键盘提示显示
const toggleKeyboardHelp = () => {
  showKeyboardHelp.value = !showKeyboardHelp.value
}

// 检查节点是否有图片
const hasImages = (topic) => {
  return imageMapping.value[topic]?.images?.length > 0
}

// 解析 Markdown 为树结构
const parseMarkdown = (markdown) => {
  const lines = markdown.split('\n').filter(line => line.trim())
  const root = { id: 'root', topic: '根节点', children: [] }
  const stack = [{ level: 0, node: root }]
  
  lines.forEach((line, index) => {
    const match = line.match(/^(#{1,6})\s+(.+)$/)
    if (match) {
      const level = match[1].length
      const topic = match[2].trim()
      const node = {
        id: `node_${index}`,
        topic: topic,
        children: []
      }
      
      // 找到父节点
      while (stack.length > 0 && stack[stack.length - 1].level >= level) {
        stack.pop()
      }
      
      if (stack.length > 0) {
        const parent = stack[stack.length - 1].node
        if (!parent.children) parent.children = []
        parent.children.push(node)
      }
      
      stack.push({ level, node })
    }
  })
  
  return root.children.length > 0 ? root.children[0] : root
}

// 初始化思维导图
const initJsMind = () => {
  if (!mindmapContent.value || !props.markdown) return
  
  const mindData = parseMarkdown(props.markdown)
  
  const options = {
    container: mindmapContent.value,
    theme: 'primary',
    editable: false,
    depth: 4,
    view: {
      hmargin: 120,
      vmargin: 20,
      line_width: 2,
      line_color: '#558'
    },
    layout: {
      hspace: 50,
      vspace: 20,
      pspace: 15
    },
    // 完全禁用展开/收起功能
    support_html: false
  }
  
  const mind = {
    meta: {
      name: 'MMPPPT',
      version: '1.0'
    },
    format: 'node_tree',
    data: mindData
  }
  
  if (jm) {
    jm = null
    mindmapContent.value.innerHTML = ''
  }
  
  jm = new jsMind(options)
  jm.show(mind)
  
  // 禁用展开/收起功能但保留图标
  if (jm) {
    jm.expand_node = function() { return false }
    jm.collapse_node = function() { return false }
  }
  
  // 构建导航列表
  nodeList.value = buildNavigationList(mindData)
  console.log('导航节点列表:', nodeList.value.map(n => n.topic))
  
  // 添加点击事件
  addClickListeners()
  
  // 初始高亮第一个有图片的节点
  if (nodeList.value.length > 0) {
    const firstWithImages = getNextNodeWithImages(0)
    if (firstWithImages !== -1) {
      currentNodeIndex.value = firstWithImages
      setTimeout(() => {
        highlightNode(currentNodeIndex.value)
      }, 600)
    }
  }
  
  // 确保容器可聚焦
  if (jsmindContainer.value) {
    jsmindContainer.value.setAttribute('tabindex', '0')
  }
}

// 构建节点导航列表（深度优先遍历）
const buildNavigationList = (node, list = [], parent = null, level = 0) => {
  if (!node) return list
  
  const nodeInfo = {
    id: node.id,
    topic: node.topic,
    parent: parent,
    children: node.children || [],
    level: level
  }
  
  list.push(nodeInfo)
  nodeDataMap.value.set(node.id, nodeInfo)
  
  if (node.children && node.children.length > 0) {
    node.children.forEach(child => {
      buildNavigationList(child, list, nodeInfo, level + 1)
    })
  }
  
  return list
}

// 高亮当前节点
const highlightNode = (index) => {
  // 移除所有高亮
  nodeElements.value.forEach(el => {
    el.style.outline = ''
    el.style.backgroundColor = ''
    el.style.fontWeight = ''
  })
  
  if (index >= 0 && index < nodeElements.value.length) {
    const element = nodeElements.value[index]
    element.style.outline = '3px solid #3b82f6'
    element.style.backgroundColor = 'rgba(59, 130, 246, 0.1)'
    element.style.fontWeight = 'bold'
    
    // 滚动到视图中
    element.scrollIntoView({ behavior: 'smooth', block: 'center' })
  }
}

// 获取下一个有图片的节点索引
const getNextNodeWithImages = (startIndex) => {
  for (let i = startIndex; i < nodeList.value.length; i++) {
    const node = nodeList.value[i]
    if (hasImages(node.topic)) {
      return i
    }
  }
  return -1
}

// 获取上一个有图片的节点索引
const getPrevNodeWithImages = (startIndex) => {
  for (let i = startIndex; i >= 0; i--) {
    const node = nodeList.value[i]
    if (hasImages(node.topic)) {
      return i
    }
  }
  return -1
}

// 键盘导航处理
const handleKeyNavigation = (e) => {
  console.log('MindMap 键盘事件:', e.key, '图片查看器状态:', props.imageViewerOpen)
  
  if (!nodeList.value.length) return
  
  // 如果图片查看器打开，不处理
  if (props.imageViewerOpen) {
    console.log('图片查看器开启，跳过MindMap键盘处理')
    return
  }
  
  const current = nodeList.value[currentNodeIndex.value]
  
  if (e.key === 'ArrowRight') {
    e.preventDefault()
    
    // 如果有子节点，跳到第一个有图片的子节点
    if (current.children && current.children.length > 0) {
      for (let child of current.children) {
        const childId = child.id
        const childIndex = nodeList.value.findIndex(n => n.id === childId)
        if (childIndex !== -1 && hasImages(nodeList.value[childIndex].topic)) {
          currentNodeIndex.value = childIndex
          highlightNode(currentNodeIndex.value)
          return
        }
      }
      // 如果所有子节点都没有图片，继续查找下一个兄弟
    }
    
    // 否则跳到下一个有图片的兄弟节点
    if (current.parent) {
      const siblings = current.parent.children
      const currentIndexInSiblings = siblings.findIndex(s => s.id === current.id)
      
      // 从下一个兄弟开始查找
      for (let i = currentIndexInSiblings + 1; i < siblings.length; i++) {
        const siblingId = siblings[i].id
        const siblingIndex = nodeList.value.findIndex(n => n.id === siblingId)
        if (siblingIndex !== -1 && hasImages(nodeList.value[siblingIndex].topic)) {
          currentNodeIndex.value = siblingIndex
          highlightNode(currentNodeIndex.value)
          return
        }
      }
      
      // 最后一个子节点，找父节点的下一个有图片的兄弟
      let parentNode = current.parent
      while (parentNode && parentNode.parent) {
        const parentSiblings = parentNode.parent.children
        const parentIndexInSiblings = parentSiblings.findIndex(s => s.id === parentNode.id)
        
        for (let i = parentIndexInSiblings + 1; i < parentSiblings.length; i++) {
          const uncleId = parentSiblings[i].id
          const uncleIndex = nodeList.value.findIndex(n => n.id === uncleId)
          if (uncleIndex !== -1 && hasImages(nodeList.value[uncleIndex].topic)) {
            currentNodeIndex.value = uncleIndex
            highlightNode(currentNodeIndex.value)
            return
          }
        }
        parentNode = parentNode.parent
      }
    }
  } else if (e.key === 'ArrowLeft') {
    e.preventDefault()
    
    // 左键：右键的逆操作，跳过没有图片的节点
    if (current.parent) {
      const siblings = current.parent.children
      const currentIndexInSiblings = siblings.findIndex(s => s.id === current.id)
      
      // 查找上一个有图片的兄弟节点
      for (let i = currentIndexInSiblings - 1; i >= 0; i--) {
        const prevSiblingId = siblings[i].id
        const prevSiblingNode = nodeDataMap.value.get(prevSiblingId)
        
        if (hasImages(prevSiblingNode.topic)) {
          // 找到这个兄弟节点的最后一个有图片的后代
          let targetNode = prevSiblingNode
          while (targetNode.children && targetNode.children.length > 0) {
            let foundChild = false
            for (let j = targetNode.children.length - 1; j >= 0; j--) {
              const lastChild = targetNode.children[j]
              const childNode = nodeDataMap.value.get(lastChild.id)
              if (hasImages(childNode.topic)) {
                targetNode = childNode
                foundChild = true
                break
              }
            }
            if (!foundChild) break
          }
          
          const targetIndex = nodeList.value.findIndex(n => n.id === targetNode.id)
          if (targetIndex !== -1) {
            currentNodeIndex.value = targetIndex
            highlightNode(currentNodeIndex.value)
            return
          }
        }
      }
      
      // 没有找到上一个兄弟，跳到父节点（如果父节点有图片）
      if (hasImages(current.parent.topic)) {
        const parentIndex = nodeList.value.findIndex(n => n.id === current.parent.id)
        if (parentIndex !== -1) {
          currentNodeIndex.value = parentIndex
          highlightNode(currentNodeIndex.value)
          return
        }
      }
    }
  } else if (e.key === 'Enter' || e.key === ' ') {
    e.preventDefault()
    // 触发点击事件
    const currentNode = nodeList.value[currentNodeIndex.value]
    if (currentNode && currentNode.topic !== '根节点') {
      emit('node-click', { content: currentNode.topic })
    }
  }
}

// 添加节点点击事件
const addClickListeners = () => {
  nextTick(() => {
    if (!jsmindContainer.value) return
    
    setTimeout(() => {
      const nodes = jsmindContainer.value.querySelectorAll('jmnode')
      nodeElements.value = Array.from(nodes)
      console.log('找到节点数量:', nodes.length)
      
      nodes.forEach((node, index) => {
        const topic = node.textContent.trim()
        console.log(`节点 ${index + 1}: "${topic}"`)
        
        // 移除旧的监听器
        const newNode = node.cloneNode(true)
        node.parentNode.replaceChild(newNode, node)
        nodeElements.value[index] = newNode
        
        newNode.style.cursor = 'pointer'
        newNode.addEventListener('click', (e) => {
          e.stopPropagation()
          const clickedTopic = newNode.textContent.trim()
          console.log('点击节点:', clickedTopic)
          
          // 更新当前选中的索引
          currentNodeIndex.value = index
          highlightNode(currentNodeIndex.value)
          
          if (clickedTopic && clickedTopic !== '根节点') {
            emit('node-click', { content: clickedTopic })
          }
        })
        
        // 添加悬停效果 - 只改变背景色
        newNode.addEventListener('mouseenter', () => {
          if (index !== currentNodeIndex.value) {
            newNode.style.backgroundColor = 'rgba(59, 130, 246, 0.05)'
          }
          newNode.style.transition = 'background-color 0.2s'
        })
        
        newNode.addEventListener('mouseleave', () => {
          if (index !== currentNodeIndex.value) {
            newNode.style.backgroundColor = ''
          }
        })
      })
    }, 500) // 增加延迟时间
  })
}

// 放大
const zoomIn = () => {
  if (jm) jm.view.zoom_in()
}

// 缩小
const zoomOut = () => {
  if (jm) jm.view.zoom_out()
}

// 监听 markdown 变化
watch(() => props.markdown, () => {
  nextTick(() => {
    initJsMind()
  })
})

// 监听 imageMapping 变化
watch(() => props.imageMapping, () => {
  // imageMapping 更新后重新高亮
  if (nodeList.value.length > 0) {
    const firstWithImages = getNextNodeWithImages(0)
    if (firstWithImages !== -1) {
      currentNodeIndex.value = firstWithImages
      setTimeout(() => {
        highlightNode(currentNodeIndex.value)
      }, 100)
    }
  }
}, { deep: true })

onMounted(() => {
  // 添加键盘事件监听 - 使用window确保全局捕获
  window.addEventListener('keydown', handleKeyNavigation, true)
  console.log('MindMap 挂载，添加键盘监听器')
  
  // 立即聚焦到容器
  nextTick(() => {
    if (jsmindContainer.value) {
      jsmindContainer.value.focus()
      console.log('MindMap 容器聚焦')
    }
  })
  
  if (props.markdown) {
    nextTick(() => {
      initJsMind()
    })
  }
})

onUnmounted(() => {
  // 移除键盘事件监听
  window.removeEventListener('keydown', handleKeyNavigation, true)
})
</script>

<style scoped>
:deep(jmnodes) {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

:deep(jmnode) {
  cursor: pointer;
  transition: background-color 0.2s;
  border-radius: 4px;
}

:deep(jmnode:hover) {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

/* 禁用展开/收起按钮的点击功能但保留显示 */
:deep(jmexpander),
:deep(.jmexpander) {
  pointer-events: none !important;
  cursor: default !important;
}
</style>
