<template>
  <div class="assign-guide">
    <h2>指派导游</h2>

    <div v-if="routes.length === 0">暂无可指派的路线</div>
    <div v-else>
      <form @submit.prevent="assignGuideToRoute">
        <div class="form-group">
          <label for="route">选择路线</label>
          <select v-model="selectedRoute" id="route" required>
            <option v-for="route in routes" :key="route.id" :value="route.id">{{ route.name }}</option>
          </select>
        </div>

        <div class="form-group">
          <label for="guide">选择导游</label>
          <select v-model="selectedGuide" id="guide" required>
            <option v-for="guide in guides" :key="guide.id" :value="guide.id">
              导游：{{ guide.id }}  
            </option>
          </select>
        </div>

        <div class="form-group">
          <label for="trip-start-time">选择行程开始日期</label>
          <input
            type="date"
            id="trip-start-time"
            v-model="tripStartTime"
            required
          />
        </div>

        <div class="form-group">
          <label for="trip-end-time">选择行程结束日期</label>
          <input
            type="date"
            id="trip-end-time"
            v-model="tripEndTime"
            required
          />
        </div>

        <button type="submit" class="button">指派导游</button>
      </form>
    </div>

    <div v-if="assignStatus" class="status-message">
      {{ assignStatus }}
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from '@/utils/request';

// 接收父组件传递的 agencyId
const props = defineProps({
  agencyId: {
    type: Number,
    required: true
  }
});

const selectedRoute = ref(null);
const selectedGuide = ref(null);
const routes = ref([]);
const guides = ref([]);
const assignStatus = ref('');  // 指派状态消息
const tripStartTime = ref('');
const tripEndTime = ref('');

// 使用传递的 agencyId 获取数据
onMounted(async () => {
  try {
    const routeResponse = await axios.get(`/routes/assign/${props.agencyId}`);  // 根据旅行社获取路线
    routes.value = routeResponse.data;

    const guideResponse = await axios.get(`/route_guide/get_guides_by_agency/${props.agencyId}`);  // 根据旅行社获取导游
    guides.value = guideResponse.data;
  } catch (error) {
    console.error('获取数据失败:', error);
    assignStatus.value = '获取数据失败，请重试';
  }
});

const assignGuideToRoute = async () => {
  if (!selectedRoute.value || !selectedGuide.value || !tripStartTime.value || !tripEndTime.value) {
    assignStatus.value = '请选择路线、导游及行程时间';
    return;
  }

  // 直接使用日期格式传递，不需要再格式化
  const formattedStartTime = tripStartTime.value;  // YYYY-MM-DD 格式
  const formattedEndTime = tripEndTime.value;      // YYYY-MM-DD 格式

  // 构建请求数据对象，发送给后端
  const requestData = {
    route_id: selectedRoute.value,
    guide_id: selectedGuide.value,
    trip_start_time: formattedStartTime,  // 发送日期格式
    trip_end_time: formattedEndTime,      // 发送日期格式

  };

  console.log("发送的请求数据：", requestData);

  try {
    const response = await axios.post('/route_guide/create', requestData);  // 修改为后端正确的 API 路径

    console.log("后端响应：", response.data);

    // 根据后端返回的数据设置指派状态
    if (response.data.id) {
      assignStatus.value = '导游指派成功';
    } else {
      assignStatus.value = '导游指派失败，请重试';
    }
  } catch (error) {
    console.error('指派导游失败:', error);
    if (error.response) {
      console.log('错误响应数据:', error.response.data);
      assignStatus.value = `指派失败: ${error.response.data.detail || '未知错误'}`;
    } else {
      assignStatus.value = '指派导游失败，请重试';
    }
  }
};
</script>



<style scoped>
.assign-guide {
  font-family: 'Arial', sans-serif;
  padding: 20px;
  background-color: #f4f7fb;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  max-width: 600px;
  margin: 0 auto;
}

.assign-guide h2 {
  font-size: 24px;
  color: #333;
  margin-bottom: 20px;
  text-align: center;
}

.form-group {
  margin-bottom: 15px;
}

label {
  font-size: 16px;
  color: #555;
  display: block;
  margin-bottom: 8px;
}

select,
input[type="datetime-local"] {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
  background-color: #fff;
  color: #333;
}

select:focus,
input[type="datetime-local"]:focus {
  outline: none;
  border-color: #007BFF;
}

button {
  background-color: #007BFF;
  color: #fff;
  padding: 12px 20px;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  width: 100%;
}

button:hover {
  background-color: #0056b3;
}

.status-message {
  margin-top: 20px;
  font-size: 18px;
  color: #28a745;
  text-align: center;
}

.status-message.error {
  color: #dc3545;
}

.form-group select,
.form-group input {
  background-color: #f9f9f9;
  color: #333;
}

.form-group select:focus,
.form-group input:focus {
  background-color: #fff;
}

.form-group input[type="datetime-local"] {
  background-color: #fff;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

@media (max-width: 600px) {
  .assign-guide {
    padding: 15px;
    width: 100%;
  }

  button {
    width: auto;
  }
}
</style>

