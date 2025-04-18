<template>
    <div class="route-details">
      <div v-if="route" class="route-info">
        <h2>{{ route.name }}</h2>
        <p>{{ route.description }}</p>
      </div>
  
      <!-- 高德地图展示 -->
      <div id="route-map" style="height: 400px; margin-top: 20px;"></div>
  
      <!-- 景点列表展示 -->
      <div class="route-spots">
        <ul>
          <li v-for="spot in spots" :key="spot.id">
            <strong>{{ spot.name }}</strong>
            <p>{{ spot.description }}</p>
          </li>
        </ul>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        routeId: this.$route.params.routeId, // 从路由中获取 route_id
        route: null,
        spots: [],
      };
    },
    mounted() {
      // 页面加载时获取路线详情
      this.fetchRouteDetails();
    },
    methods: {
      async fetchRouteDetails() {
        try {
          const response = await axios.get(`/routes/${this.routeId}/details`);
          const { route, spots } = response.data;
  
          // 保存数据
          this.route = route;
          this.spots = spots;
  
          // 调用函数显示路线和景点
          this.showRouteOnMap(spots);
        } catch (error) {
          console.error('获取路线详情失败', error);
          alert('无法获取路线详情');
        }
      },
      showRouteOnMap(spots) {
        // 高德地图初始化
        const map = new AMap.Map('route-map', {
          zoom: 12, // 初始地图缩放级别
          center: [spots[0].longitude, spots[0].latitude], // 设置中心点为第一个景点
        });
  
        // 依照景点顺序，展示每个景点的标记
        spots.forEach(spot => {
          const marker = new AMap.Marker({
            position: [spot.longitude, spot.latitude],
            title: spot.name,
          });
          marker.setMap(map);
        });
  
        // 规划路径（基于景点的顺序）
        const path = spots.map(spot => [spot.longitude, spot.latitude]);
        const polyline = new AMap.Polyline({
          path: path, // 路线坐标
          strokeColor: "#3388FF", // 线路颜色
          strokeOpacity: 1,
          strokeWeight: 6,
        });
        polyline.setMap(map);
      },
    },
  };
  </script>
  
  <style scoped>
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
  </style>
  