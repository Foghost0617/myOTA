<template>
    <div class="add-route">
      <h2>创建路线</h2>
      <input v-model="routeName" placeholder="路线名称" />
      <textarea v-model="routeDesc" placeholder="路线简介"></textarea>
  
      <div id="map" class="map-container"></div>
  
      <h3>景点列表</h3>
      <div v-for="(spot, index) in spots" :key="index" class="spot-item">
        <input v-model="spot.name" placeholder="景点名称" />
        <input v-model="spot.description" placeholder="景点介绍" />
        <span>纬度: {{ spot.latitude.toFixed(6) }} 经度: {{ spot.longitude.toFixed(6) }}</span>
        <button @click="removeSpot(index)">删除</button>
      </div>
  
      <button @click="submitRouteInfo" :disabled="routeId">提交基本路线信息</button>
      <!-- 第二个按钮只有在成功提交基本路线后才显示 -->
      <button v-if="routeId" @click="submitRouteSpots">提交景点信息</button>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import AMapLoader from '@amap/amap-jsapi-loader'
  import axios from '@/utils/request'
  
  // 基本信息
  const routeName = ref('')
  const routeDesc = ref('')
  const spots = ref([])
  
  // 存储已创建的 route_id
  const routeId = ref(null)
  
  // 模拟 agency_id（建议登录状态中保存到 localStorage 或 Vuex）
  const agency_id = parseInt(localStorage.getItem('agency_id') || '1')
  
  // 加载地图
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
  
      // 点击地图添加标点
      map.on('click', function (e) {
        const { lng, lat } = e.lnglat
        spots.value.push({
          name: '',
          description: '',
          latitude: lat,
          longitude: lng,
          sequence: spots.value.length + 1
        })
  
        new AMap.Marker({ position: [lng, lat], map })
      })
    }).catch(console.error)
  }
  
  // 删除景点
  const removeSpot = (index) => {
    spots.value.splice(index, 1)
    spots.value.forEach((s, i) => s.sequence = i + 1)
  }
  
  // 提交基本路线信息（名称、描述、旅社id）
  const submitRouteInfo = async () => {
    if (!routeName.value || !routeDesc) {
      alert('请先填写路线名称和描述')
      return
    }
    
    try {
      // 创建路线，获取 route_id
      console.log(routeName.value,routeDesc.value,agency_id)
      const res = await axios.post('/routes/info/', {
        name: routeName.value,
        description: routeDesc.value,
        agency_id: agency_id
      })
      console.log(res.data)
  
      routeId.value = res.data.id
      if (!routeId.value) {
        throw new Error('未获取到路线ID')
      }
      alert('基本路线信息已提交，接下来请提交景点信息')
  
    } catch (err) {
      alert(err.response?.data?.detail || '创建失败')
    }
  }
  
  // 提交景点信息，带上 route_id
  const submitRouteSpots = async () => {
    if (!routeId.value) {
      alert('请先提交基本路线信息')
      return
    }
  
    try {
      // 提交景点信息
      const spotPayload = spots.value.map((s) => ({
        route_id: routeId.value,
        name: s.name,
        description: s.description,
        latitude: s.latitude,
        longitude: s.longitude,
        sort_order: s.sequence
      }))
  
      await axios.post('/routes/route_spots/', spotPayload)
  
      alert('景点信息创建成功')
  
      // 清空表单
      routeName.value = ''
      routeDesc.value = ''
      spots.value = []
      routeId.value = null
  
    } catch (err) {
      alert(err.response?.data?.detail || '创建失败')
    }
  }
  
  onMounted(() => loadMap())
  </script>
  
  <style scoped>
  .add-route {
    max-width: 800px;
    margin: auto;
  }
  .map-container {
    width: 100%;
    height: 400px;
    margin-bottom: 20px;
    border: 1px solid black;
  }
  .spot-item {
    background: #f2f2f2;
    padding: 10px;
    margin-bottom: 10px;
    border-radius: 6px;
  }
  </style>
  
  
  
  
  