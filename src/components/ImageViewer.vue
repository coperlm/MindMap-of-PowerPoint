<template>
  <div 
    class="fixed inset-0 z-50 bg-black flex items-center justify-center"
    @click="handleBackdropClick"
  >
    <!-- 关闭按钮 - 更小更透明 -->
    <button 
      @click="close"
      class="absolute top-4 right-4 w-10 h-10 rounded-full bg-white bg-opacity-5 hover:bg-opacity-15 flex items-center justify-center transition-all z-10 group opacity-50 hover:opacity-100"
    >
      <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
      </svg>
    </button>

    <!-- 标题 - 半透明悬浮 -->
    <div class="absolute top-4 left-4 z-10 bg-black bg-opacity-30 rounded-lg px-4 py-2 backdrop-blur-sm opacity-80 hover:opacity-100 transition-opacity">
      <h2 class="text-white text-lg font-medium">{{ title }}</h2>
      <p class="text-gray-300 text-xs mt-0.5">
        <span v-if="images.length > 1">{{ currentIndex + 1 }} / {{ images.length }}</span>
      </p>
    </div>

    <!-- 主内容区 - 全屏图片 -->
    <div class="absolute inset-0 flex items-center justify-center">
      <!-- 图片 - 完全填充屏幕 -->
      <img 
        :key="currentImage"
        :src="currentImage" 
        :alt="title"
        class="w-screen h-screen object-contain"
        @error="handleImageError"
      />
    </div>

    <!-- 键盘提示 - 更小更透明 -->
    <div class="absolute bottom-4 right-4 text-gray-400 text-xs bg-black bg-opacity-30 rounded-lg px-3 py-2 backdrop-blur-sm opacity-60 hover:opacity-100 transition-opacity">
      <p>← → 切换 · ESC 退出</p>
    </div>

    <!-- 底部进度指示器（仅多图时显示） -->
    <div 
      v-if="images.length > 1" 
      class="absolute bottom-4 left-1/2 transform -translate-x-1/2 flex gap-2 bg-black bg-opacity-30 px-4 py-2 rounded-full backdrop-blur-sm opacity-70 hover:opacity-100 transition-opacity"
    >
      <button
        v-for="(img, index) in images"
        :key="index"
        @click.stop="goToImage(index)"
        :class="[
          'h-1.5 rounded-full transition-all',
          currentIndex === index 
            ? 'bg-white w-6' 
            : 'bg-white bg-opacity-40 hover:bg-opacity-70 w-1.5'
        ]"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'

const props = defineProps({
  images: {
    type: Array,
    required: true
  },
  title: {
    type: String,
    default: ''
  },
  hasPrevNode: {
    type: Boolean,
    default: false
  },
  hasNextNode: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close', 'prev-node', 'next-node'])

const currentIndex = ref(0)

// 监听 images 变化，重置索引
watch(() => props.images, () => {
  // 不自动重置，保持由父组件控制
}, { deep: true })

const currentImage = computed(() => {
  return props.images[currentIndex.value]
})

// 上一张
const prevImage = () => {
  if (currentIndex.value > 0) {
    currentIndex.value--
  } else if (props.hasPrevNode) {
    // 当前是第一张图片，跳到上一个节点
    emit('prev-node')
    // 重置到新节点的最后一张
    nextTick(() => {
      currentIndex.value = props.images.length - 1
    })
  }
}

// 下一张
const nextImage = () => {
  if (currentIndex.value < props.images.length - 1) {
    currentIndex.value++
  } else if (props.hasNextNode) {
    // 当前是最后一张图片，跳到下一个节点
    emit('next-node')
    // 重置到新节点的第一张
    nextTick(() => {
      currentIndex.value = 0
    })
  }
}

// 跳转到指定图片
const goToImage = (index) => {
  currentIndex.value = index
}

// 关闭
const close = () => {
  emit('close')
}

// 点击背景关闭
const handleBackdropClick = (e) => {
  if (e.target === e.currentTarget) {
    close()
  }
}

// 图片加载失败
const handleImageError = (e) => {
  console.error('图片加载失败:', currentImage.value)
  e.target.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="400" height="300"%3E%3Crect width="400" height="300" fill="%23333"/%3E%3Ctext x="50%25" y="50%25" fill="%23999" text-anchor="middle" dy=".3em" font-size="20"%3E图片加载失败%3C/text%3E%3C/svg%3E'
}

// 键盘事件处理
const handleKeydown = (e) => {
  switch (e.key) {
    case 'Escape':
      close()
      break
    case 'ArrowLeft':
      prevImage()
      break
    case 'ArrowRight':
      nextImage()
      break
  }
}

onMounted(() => {
  window.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown)
})
</script>

<style scoped>
/* 确保图片真正全屏 */
img {
  width: 100vw;
  height: 100vh;
  object-fit: contain;
}
</style>
