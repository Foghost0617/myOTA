<template>
    <div class="login-container">
      <h2>{{ isRegistering ? '注册' : '登录' }}</h2>
  
      <input v-model="account" placeholder="请输入账号" />
      <input v-model="password" placeholder="请输入密码" type="password" />
  
      <select v-model="role">
        <option disabled value="">请选择身份</option>
        <option value="1">游客</option>
        <option value="2">导游</option>
        <option value="3">旅行社</option>
        <option value="4">文旅局</option>
      </select>
  
      <button @click="isRegistering ? register() : login()">
        {{ isRegistering ? '注册' : '登录' }}
      </button>
  
      <p class="toggle" @click="isRegistering = !isRegistering">
        {{ isRegistering ? '已有账号？登录' : '没有账号？注册' }}
      </p>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import axios from 'axios';
  
  const isRegistering = ref(false)
  const account = ref('')
  const password = ref('')
  const role = ref(0)  // 1~4
  
  const register = async () => {
    if (!account.value || !password.value || !role.value) {
    alert("请完善填写");
    return;
  }
    console.log({
      account: account.value,
      password: password.value,
      role: role.value
    });
  
    try {
      const res = await axios.post('http://localhost:8001/users/register', {
        account: account.value,
        password: password.value,
        role: role.value
      });
      alert("登录成功！");
      account.value = '';
      password.value = '';
      role.value = 0;
      isRegistering.value = false;  // 注册后自动切换到登录
    } catch (error) {
        if (error.response) {
      alert(error.response.data.detail);
    } else {
      alert("请求失败，请稍后再试");
    }
    }
  }
  
  const login = async () => {
    console.log({
      account: account.value,
      password: password.value,
      role: role.value
    });
    if (!account.value || !password.value || !role.value) {
    alert("请完善填写");
    return;
  }
    console.log({
        role:role.value
    });
  
    try {
      const res = await axios.post('http://localhost:8001/users/login', {
        account: account.value,
        password: password.value,
        role: role.value
      });
      alert("登录成功！");
    } catch (error) {
       // 添加对 error.response 的检查
    if (error.response) {
      alert(error.response.data.detail);
    } else {
      alert("请求失败，请稍后再试");
    }
    account.value = '';
    password.value = '';
    role.value = 0;
    }
  }
  </script>
  
  <style scoped>
  h2{
    color:black;
    font-weight:bold;
    font-size:24px;
    text-align: center;
  }
  .login-container {
    max-width: 300px;
    margin: 60px auto;
    display: flex;
    flex-direction: column;
    gap: 10px;
    background: #f9f9f9;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }
  input, select {
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  button {
    padding: 10px;
    background-color: #42b983;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  .toggle {
    color: #007bff;
    cursor: pointer;
    font-size: 14px;
    text-align: center;
    margin-top: 10px;
  }
  </style>