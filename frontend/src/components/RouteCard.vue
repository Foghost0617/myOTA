<template>
  <div class="route-card">
    <h2>{{ route.name }}</h2>
    <p>{{ route.description }}</p>
    <div class="buttons">
      <button @click="$emit('view', route.id)">查看详情</button>
      <button v-if="showDelete" @click="$emit('delete', route.id)" class="delete-button">删除</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RouteCard',
  props: {
    route: {
      type: Object,
      required: true,
    },
    showDelete: {
      type: Boolean,
      default: false,
    },
  },
};
</script>

<style scoped>
.route-card {
  background-color: #ffffff;
  padding: 15px;
  margin-bottom: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}
.route-card h2 {
  font-size: 1.1rem;
  color: #2d87f0;
  margin-bottom: 10px;
  font-weight: 500;
}
.route-card p {
  font-size: 1rem;
  color: #666;
  margin-bottom: 15px;
  line-height: 1.6;
  max-height: 50px;
  overflow: hidden;
}
.buttons button {
  background-color: #2d87f0;
  color: white;
  padding: 8px 16px;
  margin-right: 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.delete-button {
  background-color: #e74c3c;
}
.delete-button:hover {
  background-color: #c0392b;
}
</style>
