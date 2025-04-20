<template>
    <div>
      <!-- 导游信息填写表单 -->
      <form @submit.prevent="submitInfo">
        <div>
          <label for="guide_name">导游姓名：</label>
          <input v-model="guideName" type="text" id="guide_name" :disabled="isCompleted" required />
          
        </div>
        <div>
          <label for="phone">电话：</label>
          <input v-model="phone" type="text" id="phone" :disabled="isCompleted" required />

        </div>
        <div>
          <label for="agency">所属旅行社：</label>
          <select v-model="agencyId" :disabled="isCompleted" required>
            <option v-for="agency in agencies" :key="agency.id" :value="agency.id">
              {{ agency.agency_name || "未命名旅行社" }}
            </option>
          </select>
         
        </div>
        <button type="submit" :disabled="isCompleted">提交</button>
      </form>
      <!-- 如果信息已填写，展示已填写提示 -->
      <div v-if="isCompleted" class="info-completed">
        <p>您已填写过信息。</p>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import axios from '@/utils/request'
  
  const guideName = ref('')
  const phone = ref('')
  const agencyId = ref(null)
  const agencies = ref([])
  const isCompleted = ref(false)  // 新增字段判断是否已填写过信息
  
  // 获取所有旅行社
  const fetchAgencies = async () => {
    try {
      const response = await axios.get('/guides/allTA')
      agencies.value = response.data
    } catch (err) {
      console.error("获取旅行社列表失败", err)
    }
  }
  
  // 页面加载时从 localStorage 获取数据
  const savedGuideInfo = JSON.parse(localStorage.getItem('guideInfo') || '{}')
  if (savedGuideInfo.guide_name && savedGuideInfo.phone && savedGuideInfo.agency_id) {
    guideName.value = savedGuideInfo.guide_name
    phone.value = savedGuideInfo.phone
    agencyId.value = savedGuideInfo.agency_id
    isCompleted.value = true  // 已填写信息
  }
  
  const submitInfo = async () => {
    const payload = {
      guide_name: guideName.value,
      phone: phone.value,
      agency_id: agencyId.value,
    }
  
    try {
      // 保存数据到 localStorage
      localStorage.setItem('guideInfo', JSON.stringify(payload))
  
      // 这里可以模拟后端更新请求（如果有的话）
      alert('信息更新成功！')
      isCompleted.value = true  // 更新后标记信息为已填写
      localStorage.setItem('isCompleted', 'true')  // 更新 localStorage 中的状态
    } catch (err) {
      console.error("信息更新失败", err)
      alert("信息更新失败，请稍后重试！")
    }
  }
  
  // 在页面加载时获取所有旅行社
  fetchAgencies()
  </script>

  
<style scoped>


.info-completed {
    margin-top: 20px;
    color: #34495e; /* 深色文字 */
    font-size: 16px; /* 增加字体大小 */
    line-height: 1.5; /* 适当增加行高 */
    text-align: center; /* 居中显示文字 */
  }

  .complete-guide-info {
    background-color: #fff;
    padding: 30px;
    border-radius: 8px;
    box-shadow: 0 0 12px rgba(0, 0, 0, 0.1); /* 更柔和的阴影 */
    max-width: 500px;
    margin: 0 auto;
    font-family: Arial, sans-serif; /* 使用更清晰的字体 */
  }

  h2 {
    margin-bottom: 20px;
    font-size: 26px; /* 增大标题字体 */
    color: #2c3e50; /* 使用更深的颜色 */
    text-align: center;
  }

  .form-group {
    margin-bottom: 20px;
  }

  label {
    display: block;
    margin-bottom: 8px;
    font-size: 18px; /* 增加标签字体大小 */
    color: #34495e; /* 更深的字体颜色 */
  }

  input, select {
    width: 80%;
    padding: 14px; /* 增加内边距 */
    border: 1px solid #ccc;
    border-radius: 6px;
    font-size: 16px;
    box-sizing: border-box;
    color: #333; /* 深色文字，增强可读性 */
    background-color: #f9f9f9; /* 更明亮的背景颜色 */
  }

  input:focus, select:focus {
    border-color: #1abc9c; /* 聚焦时输入框高亮 */
    outline: none;
  }

  button {
    background-color: #1abc9c;
    color: #fff;
    padding: 14px 20px; /* 增加按钮内边距 */
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 18px; /* 增大按钮字体 */
    width: 80%;
    margin-top: 20px;
  }

  button:hover {
    background-color: #16a085; /* 按钮悬停时颜色更深 */
  }

  /* 使表单内容更为清晰 */
  .form-group input,
  .form-group select {
    margin-bottom: 12px; /* 增加输入框与标签之间的间距 */
  }
</style>
