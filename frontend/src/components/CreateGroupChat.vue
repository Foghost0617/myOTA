<!-- <template>
  <div class="create-group-chat">
    <h2>创建群聊</h2>

    <div class="form-group">
      <label>群聊名称：</label>
      <input v-model="groupName" type="text" placeholder="请输入群聊名称" />
    </div>

    <div class="form-group">
      <label>选择群聊成员：</label>
      <div class="member-list">
        <div v-for="member in availableMembers" :key="member.user_id" class="member-item">
          <label>
            <input
              type="checkbox"
              :value="member"
              v-model="selectedMembers"
            />
            {{ roleNameMap[member.user_role] }} - 用户ID：{{ member.user_id }}
          </label>
        </div>
      </div>
    </div>

    <div class="form-group">
      <button @click="createGroupChat">创建群聊</button>
    </div>

    <div v-if="successMessage" class="success-message">
      {{ successMessage }}
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from '@/utils/request'

// 接收父组件传来的 props
const props = defineProps({
  creatorId: {
    type: Number,
    required: true
  },
  creatorRole: {
    type: Number,
    required: true
  }
})

// 定义响应式数据
const groupName = ref('');
const availableMembers = ref([]);
const selectedMembers = ref([]);
const successMessage = ref('');

const roleNameMap = {
  1: '游客',
  2: '导游',
  3: '旅行社',
  4: '文旅局'
};

// 组件挂载时加载可选成员
onMounted(async () => {
  try {
    const response = await axios.get('/groupchats/available-members', {
      params: {
        creator_id: props.creatorId,
        creator_role: props.creatorRole
      }
    });

    availableMembers.value = response.data || [];
  } catch (error) {
    console.error('加载可选成员失败：', error);
    alert('无法加载群聊成员');
  }
});

// 创建群聊方法
const createGroupChat = async () => {
  if (!groupName.value.trim()) {
    alert('请输入群聊名称');
    return;
  }

  if (selectedMembers.value.length === 0) {
    alert('请至少选择一个成员');
    return;
  }

  const payload = {
    name: groupName.value,
    creator_id: props.creatorId,
    creator_role: props.creatorRole,
    member_ids: selectedMembers.value.map(m => m.user_id),
    member_roles: selectedMembers.value.map(m => m.user_role)
  };

  try {
    const res = await axios.post('/groupchats/create', payload);
    successMessage.value = `群聊 "${res.data.name}" 创建成功！（群ID：${res.data.group_id}）`;
    groupName.value = '';
    selectedMembers.value = [];
  } catch (err) {
    console.error('创建群聊失败：', err);
    alert('创建失败，请稍后重试');
  }
}
</script>

<style scoped>
.member-list {
  max-height: 200px;
  overflow-y: auto;
  border: 1px solid #ccc;
  padding: 10px;
  margin-top: 5px;
}
.member-item {
  display: block;
  margin-bottom: 5px;
}
.create-group-chat {
  padding: 20px;
}
.form-group {
  margin-bottom: 10px;
}
.success-message {
  margin-top: 20px;
  color: green;
}
</style> -->


<template>
  <div class="create-group-chat">
    <h2>创建群聊</h2>

    <div class="form-group">
      <label>群聊名称：</label>
      <input v-model="groupName" type="text" placeholder="请输入群聊名称" />
    </div>

    <div class="form-group">
      <label>选择群聊成员：</label>
      <div class="member-list">
        <div v-for="member in availableMembers" :key="member.user_id" class="member-item">
          <label>
            <input
              type="checkbox"
              :value="member"
              v-model="selectedMembers"
            />
            {{ roleNameMap[member.user_role] }} - 用户ID：{{ member.user_id }}
          </label>
        </div>
      </div>
    </div>

    <div class="form-group">
      <button @click="createGroupChat">创建群聊</button>
    </div>

    <div v-if="successMessage" class="success-message">
      {{ successMessage }}
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from '@/utils/request'

// 接收父组件传来的 props
const props = defineProps({
  creatorId: {
    type: Number,
    required: true
  },
  creatorRole: {
    type: Number,
    required: true
  }
})

// 定义响应式数据
const groupName = ref('');
const availableMembers = ref([]);
const selectedMembers = ref([]);
const successMessage = ref('');

const roleNameMap = {
  1: '游客',
  2: '导游',
  3: '旅行社',
  4: '文旅局'
};

// 组件挂载时加载可选成员
onMounted(async () => {
  try {
    const response = await axios.get('/groupchats/available-members', {
      params: {
        creator_id: props.creatorId,
        creator_role: props.creatorRole
      }
    });
    console.log(response,'可以搭载的成员')

    availableMembers.value = response.data || [];
  } catch (error) {
    console.error('加载可选成员失败：', error);
    alert('无法加载群聊成员');
  }
});

// 创建群聊方法
const createGroupChat = async () => {
  if (!groupName.value.trim()) {
    alert('请输入群聊名称');
    return;
  }

  if (selectedMembers.value.length === 0) {
    alert('请至少选择一个成员');
    return;
  }

  const payload = {
    name: groupName.value,
    creator_id: props.creatorId,
    creator_role: props.creatorRole,
    member_ids: selectedMembers.value.map(m => m.user_id),
    member_roles: selectedMembers.value.map(m => m.user_role)
  };

  try {
    const res = await axios.post('/groupchats/create', payload);
    successMessage.value = `群聊 "${res.data.name}" 创建成功！（群ID：${res.data.group_id}）`;
    groupName.value = '';
    selectedMembers.value = [];
  } catch (err) {
    console.error('创建群聊失败：', err);
    alert('创建失败，请稍后重试');
  }
}
</script>

<style scoped>
.create-group-chat {
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  max-width: 600px;
  margin: 0 auto;
}

h2 {
  font-size: 24px;
  color: #2c3e50;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 20px;
}

label {
  font-size: 16px;
  color: #34495e;
  margin-bottom: 8px;
  display: block;
}

input[type="text"] {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
  transition: border-color 0.3s;
}

input[type="text"]:focus {
  border-color: #1abc9c;
  outline: none;
}

button {
  width: 100%;
  padding: 12px;
  background-color: #1abc9c;
  color: white;
  font-size: 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #16a085;
}

.member-list {
  max-height: 200px;
  overflow-y: auto;
  border: 1px solid #ddd;
  padding: 10px;
  margin-top: 10px;
  border-radius: 4px;
  background-color: #fafafa;
}

.member-item {
  display: block;
  margin-bottom: 12px;
  color: #34495e;
}

.member-item input {
  margin-right: 10px;
}

.success-message {
  margin-top: 20px;
  padding: 10px;
  background-color: #28a745;
  color: white;
  border-radius: 4px;
  font-size: 16px;
  text-align: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
</style>
