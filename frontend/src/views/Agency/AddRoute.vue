  <!-- <template>
    <div class="add-route-container">
      
      <div class="left-pane">
        <h2>创建路线</h2>
        <input v-model="routeName" placeholder="路线名称" />
        <textarea v-model="routeDesc" placeholder="路线简介"></textarea>
        <div id="map" class="map-container"></div>
      </div>
  
      
      <div class="right-pane">
        <h3>景点列表</h3>
        <div
          v-for="(spot, index) in spots"
          :key="index"
          class="spot-item"
        >
          <input v-model="spot.name" placeholder="景点名称" />
          <input v-model="spot.description" placeholder="景点介绍" />
          <span>
            纬度: {{ spot.latitude.toFixed(6) }} 经度: {{ spot.longitude.toFixed(6) }}
          </span>
          <button @click="removeSpot(index)">删除</button>
        </div>
      </div>
    </div>
  
    
    <div class="button-row">
      <button
        @click="submitRouteInfo"
        :disabled="!routeName || !routeDesc"
      >提交基本路线信息</button>
  
      <button
        @click="submitRouteSpots"
        :disabled="!routeId || spots.length === 0 || hasInvalidSpots"
      >提交景点信息</button>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, onMounted } from 'vue'
  import AMapLoader from '@amap/amap-jsapi-loader'
  import axios from '@/utils/request'
  
  // 表单数据
  const routeName = ref('')
  const routeDesc = ref('')
  const routeId = ref(null)
  const spots = ref([])
  
  

  // 判断是否有未填写完整的景点
  const hasInvalidSpots = computed(() => {
    return spots.value.some(s => !s.name || !s.latitude || !s.longitude)
  })
  
  // 地图初始化
  const loadMap = () => {
    AMapLoader.load({
      key: import.meta.env.VITE_AMAP_KEY,
      version: '2.0',
      plugins: ['AMap.PlaceSearch', 'AMap.Geocoder', 'AMap.ToolBar'],
    }).then((AMap) => {
      const map = new AMap.Map('map', {
        zoom: 12,
        center: [114.35806, 30.533177],
      })
  

      map.addControl(new AMap.ToolBar())
  
      map.on('click', (e) => {
        const { lng, lat } = e.lnglat
        spots.value.push({
          name: '',
          description: '',
          latitude: lat,
          longitude: lng,
          sequence: spots.value.length + 1,
        })
        new AMap.Marker({ position: [lng, lat], map })
      })
    }).catch(console.error)
  }
  
  onMounted(() => loadMap())
  
  // 删除景点
  const removeSpot = (index) => {
    spots.value.splice(index, 1)
    // 更新排序
    spots.value.forEach((s, i) => (s.sequence = i + 1))
  }
  
  // 提交基本路线信息
  const submitRouteInfo = async () => {
    const agency_id = parseInt(localStorage.getItem('agency_id') || '0')
    if (!agency_id) {
    alert('请重新登录获取身份信息')
    return
    }

    try {
      const res = await axios.post('/routes/info/', {
        name: routeName.value,
        description: routeDesc.value,
        agency_id: agency_id
      })
      routeId.value = res.data.id
      alert('路线创建成功，接下来可以提交景点信息')
    } catch (err) {
      alert(err.response?.data?.detail || '路线创建失败')
    }
  }
  
  // 提交景点信息
  const submitRouteSpots = async () => {
    try {
      const payload = spots.value.map(s => ({
        route_id: routeId.value,
        name: s.name,
        description: s.description || '',
        latitude: s.latitude,
        longitude: s.longitude,
        sequence: s.sequence
      }))
      await axios.post('/routes/route_spots/', payload)
      alert('景点提交成功')
  
      // 重置
      routeName.value = ''
      routeDesc.value = ''
      routeId.value = null
      spots.value = []
    } catch (err) {
      alert(err.response?.data?.detail || '提交失败')
    }
  }
  </script>
  
  <style scoped>
  .add-route-container {
    display: flex;
    justify-content: space-between;
    gap: 20px;
    padding: 20px;
  }
  
  .left-pane, .right-pane {
    flex: 1;
    display: flex;
    flex-direction: column;
  }
  
  .map-container {
    width: 100%;
    height: 400px;
    margin-top: 10px;
    border: 1px solid black;
  }
  
  .spot-item {
    background: #f2f2f2;
    padding: 10px;
    margin-bottom: 10px;
    border-radius: 6px;
  }
  
  .button-row {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin-top: 20px;
  }
  </style> -->
  
  <template>
    <div class="add-route-container">
      <div class="left-pane">
        <h2>创建路线</h2>
        <input v-model="routeName" placeholder="路线名称" />
        <textarea v-model="routeDesc" placeholder="路线简介"></textarea>
        <div id="map" class="map-container"></div>
      </div>
  
      <div class="right-pane">
        <h3>景点列表</h3>
        <div v-for="(spot, index) in spots" :key="index" class="spot-item">
          <input v-model="spot.name" placeholder="景点名称" />
          <input v-model="spot.description" placeholder="景点介绍" />
          <span>
            纬度: {{ spot.latitude.toFixed(6) }} 经度: {{ spot.longitude.toFixed(6) }}
          </span>
          <button @click="removeSpot(index)">删除</button>
        </div>
      </div>
    </div>
  
    <div class="button-row">
      <button @click="submitRouteInfo" :disabled="!routeName || !routeDesc">
        提交基本路线信息
      </button>
  
      <button @click="submitRouteSpots" :disabled="!routeId || spots.length === 0 || hasInvalidSpots">
        提交景点信息
      </button>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, onMounted, reactive } from 'vue'
  import AMapLoader from '@amap/amap-jsapi-loader'
  import axios from '@/utils/request'
  
  const routeName = ref('')
  const routeDesc = ref('')
  const routeId = ref(null)
  const spots = ref([])
  const markers = ref([]) // 用来存储每个标记
  
  // 判断是否有未填写完整的景点
  const hasInvalidSpots = computed(() => {
    return spots.value.some(s => !s.name || !s.latitude || !s.longitude)
  })
  
  // 地图初始化
  const loadMap = () => {
    AMapLoader.load({
      key: import.meta.env.VITE_AMAP_KEY,
      version: '2.0',
      plugins: ['AMap.PlaceSearch', 'AMap.Geocoder', 'AMap.ToolBar'],
    }).then((AMap) => {
      const map = new AMap.Map('map', {
        zoom: 12,
        center: [114.35806, 30.533177],
      })
  
      map.addControl(new AMap.ToolBar())
  
      map.on('click', (e) => {
        const { lng, lat } = e.lnglat
        spots.value.push({
          name: '',
          description: '',
          latitude: lat,
          longitude: lng,
          sequence: spots.value.length + 1,
        })
        const marker = new AMap.Marker({ position: [lng, lat], map })
        markers.value.push(marker)  // 将每个新标记存入 markers 数组
      })
    }).catch(console.error)
  }
  
  onMounted(() => loadMap())
  
  // 删除景点及对应标记
  const removeSpot = (index) => {
    const marker = markers.value[index]  // 获取对应的标记
    if (marker) {
      marker.setMap(null)  // 从地图上删除标记
    }
    spots.value.splice(index, 1)
    // 更新排序
    spots.value.forEach((s, i) => (s.sequence = i + 1))
    markers.value.splice(index, 1)  // 从 markers 数组中删除对应的标记
  }
  
  // 提交基本路线信息
  const submitRouteInfo = async () => {
    const agency_id = parseInt(localStorage.getItem('agency_id') || '0')
    console.log(agency_id)
    if (!agency_id) {
      alert('请重新登录获取身份信息')
      return
    }
    console.log('进入基本提交')
  
    try {
      const res = await axios.post('/routes/info', {
        name: routeName.value,
        description: routeDesc.value,
        agency_id: agency_id
      })
      console.log(res.data)
      routeId.value = res.data.id
      alert('路线创建成功，接下来可以提交景点信息')
    } catch (err) {
      alert(err.response?.data?.detail || '路线创建失败')
    }
  }

  
  // 提交景点信息
  const submitRouteSpots = async () => {
    try {
      const payload = spots.value.map(s => ({
        route_id: routeId.value,
        name: s.name,
        description: s.description || '',
        latitude: s.latitude,
        longitude: s.longitude,
        sequence: s.sequence
      }))
      console.log(payload.data)
      const res=await axios.post('/routes/route_spots', payload)
      console.log(res.data)
      alert('景点提交成功')
  
      // 清除标记
      markers.value.forEach(marker => marker.setMap(null))  // 删除所有标记
      markers.value = []  // 清空标记数组
  
      // 重置
      routeName.value = ''
      routeDesc.value = ''
      routeId.value = null
      spots.value = []
    } catch (err) {
      alert(err.response?.data?.detail || '提交失败')
    }
  }
  </script>
  
  
  <!-- <style scoped>

* {
    box-sizing: border-box;
  }
  .add-route-container {
    display: flex;
    justify-content: space-between;
    gap: 20px;
    padding: 20px;
  }
  
  .left-pane, .right-pane {
    flex: 1;
    display: flex;
    flex-direction: column;
  }
  
  .map-container {
    width: 100%;
    height: 400px;
    margin-top: 10px;
    border: 1px solid black;
  }
  
  .spot-item {
    background: #f2f2f2;
    padding: 10px;
    margin-bottom: 10px;
    border-radius: 6px;
  }
  
  .button-row {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin-top: 20px;
  }
  </style> -->

  <style scoped>
  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }
  
  h2, h3 { /* 直接选择 h2 和 h3 标签 */
    font-size: 1rem;
    font-weight: bold;
    color: #333;
    text-align: center;
    margin-bottom: 30px;
  }

  .add-route-container {
    display: flex;
    justify-content: space-between;
    gap: 20px;
    padding: 20px;
    background-color: #f9f9f9; /* 背景色稍微浅一些 */
    border-radius: 8px; /* 给容器加圆角 */
  }
  
  .left-pane, .right-pane {
    flex: 1;
    display: flex;
    flex-direction: column;
  }
  
  .map-container {
    width: 100%;
    height: 400px;
    margin-top: 10px;
    border: 2px solid #ddd; /* 使边框颜色变浅 */
    border-radius: 8px; /* 给地图容器加圆角 */
    background-color: #eaeaea; /* 给地图容器设置浅灰背景 */
  }
  
  .spot-item {
    background: #ffffff;
    padding: 15px;
    margin-bottom: 12px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* 给每个景点添加阴影 */
    color: #333; /* 设置深色文字 */
    font-size: 14px; /* 字体大小稍微调整 */
    line-height: 1.5;
  }
  
  .spot-item:hover {
    background-color: #f4f4f4; /* 鼠标悬停时背景变亮 */
  }
  
  .button-row {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin-top: 20px;
  }
  
  button {
    background-color: #4CAF50; /* 主按钮颜色 */
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 6px; /* 圆角按钮 */
    cursor: pointer;
    font-size: 16px;
  }
  
  button:hover {
    background-color: #45a049; /* 按钮悬停效果 */
  }
  
  button:active {
    background-color: #387f37; /* 按钮按下效果 */
  }
  
  button:disabled {
    background-color: #bdbdbd; /* 禁用按钮颜色 */
    cursor: not-allowed;
  }
  </style>
  

  






