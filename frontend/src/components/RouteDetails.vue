<!-- <template>
    <div class="route-details">
      <div v-if="route" class="route-info">
        <h2>{{ route.name }}</h2>
        <p>{{ route.description }}</p>
      </div>
  
 
      <div id="route-map" style="height: 400px; margin-top: 20px;"></div>
  
 
      <div class="route-spots">
        <ul>
          <li v-for="spot in spots" :key="spot.id">
            <strong>{{ spot.name }}</strong>
            <p>{{ spot.description }}</p>
          </li>
        </ul>
      </div>
    </div>
  </template> -->

<!-- <script setup>
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
const markers = ref([])

const fetchRouteDetails = async () => {
  if (!props.routeId) {
    console.error('无效的 routeId')
    alert('无效的路线 ID')
    return
  }
  try {
    const response = await axios.get(`/routes/spots/${props.routeId}`)
    console.log(response.data)
    if (response.data && Array.isArray(response.data)) {
      spots.value = response.data
      if (spots.value.length === 0) {
        alert('没有找到景点数据')
      } else {
        showRouteOnMap(spots.value)
      }
    } else {
      console.error('返回的数据格式不正确', response.data)
      alert('无法加载路线详情')
    }
  } catch (error) {
    console.error('获取路线详情失败', error)
    alert('无法获取路线详情')
  }
}

const showRouteOnMap = (spotsData) => {
  if (!spotsData.length) return

  AMapLoader.load({
    key: import.meta.env.VITE_AMAP_KEY,
    version: '2.0',
    plugins: ['AMap.ToolBar'],
  }).then((AMap) => {
    // 初始化地图
    map.value = new AMap.Map('route-map', {
      zoom: 12,
      center: [spotsData[0].longitude, spotsData[0].latitude],
    })

    map.value.addControl(new AMap.ToolBar())

    // 添加标记
    spotsData.forEach(spot => {
      const marker = new AMap.Marker({
        position: [spot.longitude, spot.latitude],
        title: spot.name,
        map: map.value,
      })
      markers.value.push(marker)
    })

    // 绘制路径线
    const path = spotsData.map(s => [s.longitude, s.latitude])
    const polyline = new AMap.Polyline({
      path,
      strokeColor: "#3388FF",
      strokeOpacity: 1,
      strokeWeight: 6,
    })
    polyline.setMap(map.value)
  }).catch((e) => {
    console.error('地图加载失败', e)
  })
}

// 当 routeId 改变时重新加载
watch(() => props.routeId, (newId) => {
  if (newId) {
    fetchRouteDetails()
  }
})

// 初次挂载时，如果已经传入 routeId 就立即加载
onMounted(() => {
  if (props.routeId) {
    fetchRouteDetails()
  }
})
</script> -->

  
  <!-- <script>
  import axios from '@/utils/request';
  import AMapLoader from '@amap/amap-jsapi-loader';
  

  const spots = ref([])
  const map = ref(null)  // 保存地图实例
  const markers = ref([])  // 标记数组
  const polyline = ref(null)  // 保存路线线条

 
   export default {
    props: {
      routeId: {
        type: Number,
        required: true,
      },
    },
    data() {
      return {
        route: null,
        spots: [],
      };
    },
    watch: {
      // 监听 routeId 变化
      routeId(newRouteId) {
        if (newRouteId) {
          this.fetchRouteDetails(); // 当 routeId 改变时重新请求
        }
      },
    },
    mounted() {
      // 如果 routeId 在 mounted 时已经传递过来，立即请求
      if (this.routeId) {
        this.fetchRouteDetails();
      } else {
        console.error('routeId 为空');
      }
    },
    methods: {
      async fetchRouteDetails() {
        if (!this.routeId) {
          console.error('无效的 routeId');
          alert('无效的路线 ID');
          return;
        }
        try {
          const response = await axios.get(`/routes/spots/${this.routeId}`);
          console.log(response.data)
          if (response.data && Array.isArray(response.data)) {
            this.spots = response.data;
          if (this.spots.length === 0) {
            alert('没有找到景点数据');
          } else {
            this.showRouteOnMap(this.spots); // 在地图上显示景点
          }
        } else {
          console.error('返回的数据格式不正确', response.data);
          alert('无法加载路线详情');
        }
      } catch (error) {
        console.error('获取路线详情失败', error);
        alert('无法获取路线详情');
      }
      },
      // 显示路线在地图上
      showRouteOnMap(spots) {
        if (spots.length === 0) {
          alert('没有景点信息');
          return;
        }
  
        const map = new AMap.Map('route-map', {
          zoom: 12,
          center: [spots[0].longitude, spots[0].latitude], // 设置中心点为第一个景点
        });
  
        // 在地图上添加每个景点的标记
        spots.forEach(spot => {
          const marker = new AMap.Marker({
            position: [spot.longitude, spot.latitude],
            title: spot.name,
          });
          marker.setMap(map);
        });
  
        // 根据景点的坐标画出路径
        const path = spots.map(spot => [spot.longitude, spot.latitude]);
        const polyline = new AMap.Polyline({
          path: path,
          strokeColor: "#3388FF",
          strokeOpacity: 1,
          strokeWeight: 6,
        });
        polyline.setMap(map);
      },
    },
  };
  </script>
   -->
  
  <!-- <style scoped>
  .route-details {
    padding: 20px;
    background-color: #fff;
    border-radius: 8px;
  }
  
  .route-info h2 {
    font-size: 24px;
    font-weight: bold;
  }
  
  .route-info p {
    color: #666;
  }
  
  .route-spots ul {
    list-style-type: none;
    padding: 0;
  }
  
  .route-spots li {
    margin-bottom: 10px;
  }
  
  .route-spots li strong {
    font-size: 16px;
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
          </li>
        </ul>
        <p v-else>暂无景点数据</p>
      </div>
  
      <!-- 调试用 -->
      <!-- <pre>{{ JSON.stringify(spots, null, 2) }}</pre> -->
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
  </style>
  
  