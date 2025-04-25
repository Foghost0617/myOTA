<!-- <template>
    <div class="upload-container">
      <h2>为景点上传图像</h2>
  
      <div v-for="route in routes" :key="route.id" class="route-card">
        <div class="route-header">
          <h3>{{ route.name }}</h3>
          <button @click="toggleSpots(route.id)">
            {{ expandedRoutes.includes(route.id) ? '收起' : '添加景点图像' }}
          </button>
        </div>
  
        <div v-if="expandedRoutes.includes(route.id)" class="spot-list">
          <div v-for="spot in route.spots" :key="spot.id" class="spot-card">
            <div class="spot-info">
              <p><strong>景点：</strong>{{ spot.name }}</p>
              <p><strong>描述：</strong>{{ spot.description }}</p>
            </div>
            <div class="upload-box">
              <input type="file" accept="image/*" @change="handleFileUpload($event, spot.id)" />
              <button @click="submitImage(spot.id)">上传</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
import { ref, onMounted } from 'vue'
  import axios from '@/utils/request'

// 获取 localStorage 中旅社 ID
const agencyId = localStorage.getItem('agency_id')

// 所有路线列表
const routes = ref([])
// 当前展开的路线（显示景点上传）
const expandedRoutes = ref([])
// 景点对应的图片文件
const imageMap = ref({})

// 切换展开/收起
function toggleSpots(routeId) {
  const index = expandedRoutes.value.indexOf(routeId)
  if (index === -1) {
    expandedRoutes.value.push(routeId)
    fetchSpots(routeId)
  } else {
    expandedRoutes.value.splice(index, 1)
  }
}

// 拉取该路线的景点
async function fetchSpots(routeId) {
  try {
    const res = await axios.get(`/routes/spots/${routeId}`)
    const route = routes.value.find(r => r.id === routeId)
    if (route) route.spots = res.data
  } catch (err) {
    console.error('获取景点失败:', err)
  }
}

// 选取文件时记录
function handleFileUpload(event, spotId) {
  const file = event.target.files[0]
  if (file) {
    imageMap.value[spotId] = file
  }
}

// 上传图片
async function submitImage(spotId) {
  const file = imageMap.value[spotId]
  if (!file) {
    alert('请先选择文件')
    return
  }

  const formData = new FormData()
  formData.append('file', file)

  try {
    await axios.post(`/routes/spot_images/${spotId}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    alert('上传成功')
  } catch (err) {
    console.error('上传失败:', err)
    alert('上传失败，请重试')
  }
}

// 页面加载后获取所有路线
onMounted(async () => {
  try {
    const res = await axios.get(`/routes/agency/${agencyId}`)
    routes.value = res.data
    console.log(res)
  } catch (err) {
    console.error('获取路线失败:', err)
  }
})
</script>

<style scoped>
.upload-container {
  padding: 20px;
}

.route-card {
  border: 1px solid #ccc;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 20px;
}

.route-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.spot-list {
  margin-top: 10px;
  padding-left: 10px;
}

.spot-card {
  border-top: 1px dashed #aaa;
  padding: 10px 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.upload-box {
  display: flex;
  gap: 8px;
}
</style>
 -->

 <!-- <template>
  <div class="upload-container">
    <h2>为景点上传图像</h2>

    <div v-for="route in routes" :key="route.id" class="route-card">
      <div class="route-header">
        <h3>{{ route.name }}</h3>
        <button @click="toggleSpots(route.id)">
          {{ expandedRoutes.includes(route.id) ? '收起' : '添加景点图像' }}
        </button>
      </div> 


      <div v-if="expandedRoutes.includes(route.id)" class="spot-list">
        <div v-for="spot in route.spots" :key="spot.id" class="spot-card">
          <div class="spot-info">
            <p><strong>景点：</strong>{{ spot.name }}</p>
            <p><strong>描述：</strong>{{ spot.description }}</p>
          </div>
          <div class="upload-box">
            <input
              type="file"
              accept="image/*"
              @change="handleFileUpload($event, spot.id)"
              :disabled="spot.image_url"
            />
            <button
              @click="submitImage(spot.id)"
              :disabled="spot.image_url"
            >
              {{ spot.image_url ? '已上传' : '上传' }}
            </button>

  
            <img
              v-if="spot.image_url"
              :src="spot.image_url"
              alt="景点图片"
              class="preview-image"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from '@/utils/request'

const agencyId = localStorage.getItem('agency_id')

const routes = ref([])
const expandedRoutes = ref([])
const imageMap = ref({})

function toggleSpots(routeId) {
  const index = expandedRoutes.value.indexOf(routeId)
  if (index === -1) {
    expandedRoutes.value.push(routeId)
    fetchSpots(routeId)
  } else {
    expandedRoutes.value.splice(index, 1)
  }
}

async function fetchSpots(routeId) {
  try {
    const res = await axios.get(`/routes/spots/${routeId}`)
    const route = routes.value.find(r => r.id === routeId)
    if (route) route.spots = res.data
  } catch (err) {
    console.error('获取景点失败:', err)
  }
}

function handleFileUpload(event, spotId) {
  const file = event.target.files[0]
  if (file) {
    imageMap.value[spotId] = file
  }
}

async function submitImage(spotId) {
  const file = imageMap.value[spotId]
  if (!file) {
    alert('请先选择文件')
    return
  }

  const formData = new FormData()
  formData.append('file', file)

  try {
    const res = await axios.post(`/routes/spot_images/${spotId}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    alert('上传成功')

    // 更新 image_url，让按钮禁用 & 显示图片
    const route = routes.value.find(r => r.spots?.some(s => s.id === spotId))
    if (route) {
      const spot = route.spots.find(s => s.id === spotId)
      if (spot) {
        spot.image_url = res.data.image_url || true  // 如果没返回 URL，就设为 true
      }
    }
  } catch (err) {
    console.error('上传失败:', err)
    alert('上传失败，请重试')
  }
}

onMounted(async () => {
  try {
    const res = await axios.get(`/routes/agency/${agencyId}`)
    routes.value = res.data
  } catch (err) {
    console.error('获取路线失败:', err)
  }
})
</script> -->



<template>
  <div class="upload-container">
    <h2>为景点上传图像</h2>

    <div v-for="route in routes" :key="route.id" class="route-card">
      <div class="route-header">
        <h3>{{ route.name }}</h3>
        <button @click="toggleSpots(route.id)">
          {{ expandedRoutes.includes(route.id) ? '收起' : '添加景点图像' }}
        </button>
      </div> 

      <!-- 展开景点上传区 -->
      <div v-if="expandedRoutes.includes(route.id)" class="spot-list">
        <div v-for="spot in route.spots" :key="spot.id" class="spot-card">
          <div class="spot-info">
            <p><strong>景点：</strong>{{ spot.name }}</p>
            <p><strong>描述：</strong>{{ spot.description }}</p>
          </div>
          <div class="upload-box">
            <input
              type="file"
              accept="image/*"
              @change="handleFileUpload($event, spot.id)"
              :disabled="spot.image_url"
            />
            <button
              @click="submitImage(spot.id)"
              :disabled="spot.image_url"
            >
              {{ spot.image_url ? '已上传' : '上传' }}
            </button>

            <!-- 预览图 -->
            <img
              v-if="spot.image_url"
              :src="getFullImageUrl(spot.image_url)"
              alt="景点图片"
              class="preview-image"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from '@/utils/request'

const agencyId = localStorage.getItem('agency_id')

const routes = ref([])
const expandedRoutes = ref([])
const imageMap = ref({})

// 获取静态文件的完整 URL
function getFullImageUrl(imageUrl) {
  console.log("获取图片路径:", imageUrl)
  
  if (!imageUrl) return ''
  
  // 调试：检查是否需要补充路径
  if (!imageUrl.startsWith('/static')) {
    console.log("补充静态文件路径:", imageUrl)
    return `/static${imageUrl}`
  }
  return `${axios.defaults.baseURL}${imageUrl}`
  
}

function toggleSpots(routeId) {
  const index = expandedRoutes.value.indexOf(routeId)
  if (index === -1) {
    expandedRoutes.value.push(routeId)
    fetchSpots(routeId)
  } else {
    expandedRoutes.value.splice(index, 1)
  }
}

async function fetchSpots(routeId) {
  try {
    const res = await axios.get(`/routes/spots/${routeId}`)
    console.log(`获取路线 ${routeId} 的景点数据:`, res.data)  // 调试：查看景点数据
    const route = routes.value.find(r => r.id === routeId)
    if (route) route.spots = res.data
  } catch (err) {
    console.error('获取景点失败:', err)
  }
}

function handleFileUpload(event, spotId) {
  const file = event.target.files[0]
  if (file) {
    console.log("选取的文件:", file)  // 调试：查看文件对象
    imageMap.value[spotId] = file
  }
}

async function submitImage(spotId) {
  const file = imageMap.value[spotId]
  if (!file) {
    alert('请先选择文件')
    return
  }

  const formData = new FormData()
  formData.append('file', file)

  try {
    console.log("开始上传文件:", file)  // 调试：开始上传文件
    const res = await axios.post(`/routes/spot_images/${spotId}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    console.log("上传成功:", res.data)  // 调试：查看上传响应

    alert('上传成功')

    // 更新 image_url，让按钮禁用 & 显示图片
    const route = routes.value.find(r => r.spots?.some(s => s.id === spotId))
    if (route) {
      const spot = route.spots.find(s => s.id === spotId)
      if (spot) {
        console.log("更新景点图片 URL:", res.data.image_url)
        spot.image_url = res.data.image_url || true  // 如果没返回 URL，就设为 true
      }
    }
  } catch (err) {
    console.error('上传失败:', err)
    alert('上传失败，请重试')
  }
}

onMounted(async () => {
  try {
    const res = await axios.get(`/routes/agency/${agencyId}`)
    console.log("获取旅社的路线数据:", res.data)  // 调试：查看路线数据
    routes.value = res.data
  } catch (err) {
    console.error('获取路线失败:', err)
  }
})
</script>

<style scoped>
.upload-container {
  padding: 1rem;
  max-height: 80vh;
  overflow-y: auto;
  background-color: #f4f4f4; /* 设置容器背景色，避免和白色文字冲突 */
}

.route-card {
  border: 1px solid #ccc;
  margin-bottom: 1rem;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  background-color: #ffffff; /* 卡片背景色 */
  color: #333; /* 设置字体颜色 */
  transition: transform 0.3s ease;
}

.route-card:hover {
  transform: translateY(-5px);
}

.route-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
  font-weight: bold;
  color: #333; /* 文字颜色 */
}

.spot-card {
  margin-top: 1rem;
  padding: 1rem;
  border: 1px dashed #aaa;
  border-radius: 6px;
  background-color: #fafafa;
  color: #333; /* 文字颜色 */
}

.upload-box {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 1rem;
}

.upload-box input {
  padding: 0.3rem;
  font-size: 0.9rem;
  border: 1px solid #ccc; /* 输入框的边框 */
}

.upload-box button {
  padding: 0.5rem 1rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.upload-box button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.upload-box button:hover:not(:disabled) {
  background-color: #0056b3;
}

.preview-image {
  width: 100px;
  height: auto;
  border-radius: 6px;
  margin-top: 0.5rem;
  border: 2px solid #ddd;
}

.route-card .route-header button {
  padding: 0.5rem;
  background-color: #28a745;
  color: white;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  border: none;
}

.route-card .route-header button:hover {
  background-color: #218838;
}

/* 标题字体颜色调整 */
h2 {
  color: #333;
}
</style>

