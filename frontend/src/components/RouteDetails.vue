
  
  <!-- <template>
    <div class="route-details">
    
      <div id="route-map" style="height: 400px; margin-bottom: 20px;"></div>
  

      <div class="route-spots">
        <h3>景点列表</h3>
        <ul v-if="spots.length > 0">
          <li v-for="spot in spots" :key="spot.id" style="border: 1px solid #ccc; padding: 10px; margin-bottom: 10px;">
            <strong>{{ spot.name }}</strong>
            <p>{{ spot.description }}</p>
          </li>
        </ul>
        <p v-else>暂无景点数据</p>
      </div>
  
    </div>
  </template> -->
  
<!-- 
  <script setup>
  import { ref, watch, onMounted } from 'vue'
  import AMapLoader from '@amap/amap-jsapi-loader'
  import axios from '@/utils/request'
  
  const props = defineProps({
    routeId: {
      type: Number,
      required: true,
    },
  })
  
  const spots = ref([])
  const map = ref(null)
  
  const fetchRouteDetails = async () => {
    try {
      console.log('请求 routeId:', props.routeId)
      const response = await axios.get(`/routes/spots/${props.routeId}`)
      console.log('接口返回:', response.data)
  
      if (Array.isArray(response.data)) {
        spots.value = response.data
        showSpotsOnMap(response.data)
      } else {
        console.warn('接口返回格式异常')
      }
    } catch (error) {
      console.error('获取路线失败', error)
    }
  }
  
  const showSpotsOnMap = (data) => {
    if (!data || data.length === 0) return
  
    AMapLoader.load({
      key: import.meta.env.VITE_AMAP_KEY,
      version: '2.0',
      plugins: ['AMap.ToolBar'],
    }).then((AMap) => {
      map.value = new AMap.Map('route-map', {
        zoom: 12,
        center: [data[0].longitude, data[0].latitude],
      })
  
      map.value.addControl(new AMap.ToolBar())
  
      data.forEach(spot => {
        new AMap.Marker({
          position: [spot.longitude, spot.latitude],
          title: spot.name,
          map: map.value,
        })
      })
    }).catch(e => {
      console.error('地图加载失败', e)
    })
  }
  
  watch(() => props.routeId, (newVal) => {
    if (newVal) fetchRouteDetails()
  })
  
  onMounted(() => {
    if (props.routeId) fetchRouteDetails()
  })
  </script>
  
  <style scoped>
 .route-details {
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-height: calc(100vh - 60px);  /* 限制最大高度为视窗高度减去顶部区域 */
  overflow-y: auto;  /* 当内容超出最大高度时显示滚动条 */
  margin: 0 auto;
}

  
  /* 地图区域 */
  #route-map {
    width: 100%;
    height: 400px;
    border-radius: 8px;
    margin-bottom: 20px;
  }
  
  /* 景点列表 */
  .route-spots {
    background-color: #448098;
    padding: 15px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  }
  
  .route-spots h3 {
    font-size: 20px;
    color: #333;
    margin-bottom: 15px;
  }
  
  /* 列表项 */
  .route-spots ul {
    list-style: none;
    padding-left: 0;
    margin: 0;
  }
  
  .route-spots li {
    margin-bottom: 15px;
    padding: 10px;
    background-color: #fafafa;
    border-radius: 8px;
    box-shadow: 0 1px 5px rgba(0, 0, 0, 0.1);
  }
  
  .route-spots li strong {
    font-size: 16px;
    color: #333;
    font-weight: bold;
  }
  
  .route-spots li p {
    font-size: 14px;
    color: #666;
    margin-top: 5px;
  }
  </style> -->
  
  <template>
    <div class="route-details">
      <!-- 地图展示区域 -->
      <div id="route-map" style="height: 400px; margin-bottom: 20px;"></div>
  
      <!-- 景点信息列表 -->
      <div class="route-spots">
        <h3>景点列表</h3>
        <ul v-if="spots.length > 0">
          <li v-for="spot in spots" :key="spot.id" style="border: 1px solid #ccc; padding: 10px; margin-bottom: 10px;">
            <strong>{{ spot.name }}</strong>
            <p>{{ spot.description }}</p>
            <!-- 显示景点图片 -->
            <div v-if="spot.image_url">
              <img :src="getFullImageUrl(spot.image_url)" alt="景点图像" style="max-width: 100%; height: auto; border-radius: 8px; margin-top: 10px;">
            </div>
          </li>
        </ul>
        <p v-else>暂无景点数据</p>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, watch, onMounted } from 'vue'
  import AMapLoader from '@amap/amap-jsapi-loader'
  import axios from '@/utils/request'
  
  const props = defineProps({
    routeId: {
      type: Number,
      required: true,
    },
  })
  
  const spots = ref([])
  const map = ref(null)
  
  // 拼接完整的图片 URL
  const getFullImageUrl = (relativeUrl) => {
    const baseUrl = axios.defaults.baseURL // 使用axios默认的baseURL
    return baseUrl ? `${baseUrl}${relativeUrl}` : relativeUrl // 拼接完整的URL
  }
  
  const fetchRouteDetails = async () => {
    try {
      console.log('请求 routeId:', props.routeId)
      const response = await axios.get(`/routes/spots/${props.routeId}`)
      console.log('接口返回:', response.data)
  
      if (Array.isArray(response.data)) {
        spots.value = response.data
        showSpotsOnMap(response.data)
      } else {
        console.warn('接口返回格式异常')
      }
    } catch (error) {
      console.error('获取路线失败', error)
    }
  }
  
  const showSpotsOnMap = (data) => {
    if (!data || data.length === 0) return
  
    AMapLoader.load({
      key: import.meta.env.VITE_AMAP_KEY,
      version: '2.0',
      plugins: ['AMap.ToolBar'],
    }).then((AMap) => {
      map.value = new AMap.Map('route-map', {
        zoom: 12,
        center: [data[0].longitude, data[0].latitude],
      })
  
      map.value.addControl(new AMap.ToolBar())
  
      data.forEach(spot => {
        new AMap.Marker({
          position: [spot.longitude, spot.latitude],
          title: spot.name,
          map: map.value,
        })
      })
    }).catch(e => {
      console.error('地图加载失败', e)
    })
  }
  
  watch(() => props.routeId, (newVal) => {
    if (newVal) fetchRouteDetails()
  })
  
  onMounted(() => {
    if (props.routeId) fetchRouteDetails()
  })
  </script>
  
  <style scoped>
  .route-details {
    padding: 20px;
    background-color: #f9f9f9;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    width: 100%;
    max-height: 80vh;  /* 限制最大高度为视口的 80% */
    overflow-y: auto;  /* 超出时显示滚动条 */
    margin: 0 auto;
  }

  /* 地图区域 */
  #route-map {
    width: 100%;
    height: 200px;
    border-radius: 8px;
    margin-bottom: 20px;
    object-fit: cover;  /* 确保地图适应容器 */
  }

  /* 景点列表 */
  .route-spots {
    background-color: #448098;
    padding: 15px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    max-height: 600px;  /* 限制景点列表的最大高度 */
    overflow-y: auto;  /* 允许滚动 */
  }

  .route-spots h3 {
    font-size: 20px;
    color: #333;
    margin-bottom: 15px;
  }

  /* 列表项 */
  .route-spots ul {
    list-style: none;
    padding-left: 0;
    margin: 0;
  }

  .route-spots li {
    margin-bottom: 15px;
    padding: 10px;
    background-color: #fafafa;
    border-radius: 8px;
    box-shadow: 0 1px 5px rgba(0, 0, 0, 0.1);
    overflow: hidden;  /* 防止溢出 */
  }

  .route-spots li strong {
    font-size: 16px;
    color: #333;
    font-weight: bold;
  }

  .route-spots li p {
    font-size: 14px;
    color: #666;
    margin-top: 5px;
  }
</style>
