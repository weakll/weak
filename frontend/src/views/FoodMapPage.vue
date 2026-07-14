<script setup>
import api from "../api"

import { ref, computed } from 'vue'
import FoodCards from '../components/FoodCards.vue'
import FoodMap from '../components/FoodMap.vue'
import { Search, Info } from '@lucide/vue'

const searchText = ref('')
const sortBy = ref('popularity')

const tips = [
  { icon: '&#128064;', text: '灰色圆点表示摊位位置，点击可查看详情' },
  { icon: '&#128269;', text: '右下角按钮可缩放地图，双指也可缩放' },
  { icon: '&#127830;', text: '彩色标记颜色对应美食类别：红=肉、蓝=鲜、绿=素、橙=甜' },
]
</script>

<template>
  <div class="foodmap-page">
    <div class="page-top-spacer"></div>
    <section class="page-hero">
      <h1>店铺目录</h1>
      <p>50+摊位 · 100+美食 · 一图掌握</p>
    </section>
    <section class="search-section">
      <div class="search-bar">
        <Search :size="18" class="search-icon" />
        <input v-model="searchText" placeholder="搜索摊位或美食..." class="search-input" />
      </div>
      <div class="sort-bar">
        <span class="sort-label">排序：</span>
        <button :class="{ active: sortBy === 'popularity' }" @click="sortBy = 'popularity'">人气最高</button>
        <button :class="{ active: sortBy === 'name' }" @click="sortBy = 'name'">名称</button>
      </div>
    </section>
    <FoodCards :searchText="searchText" :sortBy="sortBy" />
    <FoodMap />
    <section class="tips-section">
      <div class="tips-card">
        <Info :size="20" class="tips-icon" />
        <div>
          <h4>地图使用小贴士</h4>
          <div class="tips-list">
            <p v-for="t in tips" :key="t.icon"><span v-html="t.icon"></span> {{ t.text }}</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.foodmap-page { min-height: 100vh; }
.page-top-spacer { height: 80px; }
.page-hero {
  text-align: center; padding: 40px 20px;
  background: linear-gradient(135deg, rgba(255,107,53,0.06), transparent);
}
.page-hero h1 { font-size: 2.4em; font-weight: 800; color: #FF6B35; margin: 0 0 6px; letter-spacing: 3px; }
.page-hero p { color: #a89880; font-size: 1em; }

.search-section { max-width: 800px; margin: 0 auto; padding: 32px 20px 0; display: flex; gap: 16px; align-items: center; justify-content: center; flex-wrap: wrap; }
.search-bar { position: relative; flex: 1; min-width: 240px; }
.search-icon { position: absolute; left: 14px; top: 50%; transform: translateY(-50%); color: #887766; }
.search-input {
  width: 100%; padding: 12px 16px 12px 42px; background: rgba(26,22,18,0.8);
  border: 1px solid rgba(255,255,255,0.08); border-radius: 50px;
  color: #e0d6c8; font-size: 0.95em; outline: none; transition: border-color 0.2s;
}
.search-input:focus { border-color: #FF6B35; }
.sort-bar { display: flex; align-items: center; gap: 8px; }
.sort-label { color: #887766; font-size: 0.85em; }
.sort-bar button {
  background: transparent; border: 1px solid rgba(255,255,255,0.08);
  color: #a89880; padding: 8px 16px; border-radius: 20px; cursor: pointer;
  font-size: 0.85em; transition: all 0.2s;
}
.sort-bar button.active, .sort-bar button:hover {
  background: rgba(255,107,53,0.15); border-color: #FF6B35; color: #FF6B35;
}

.tips-section { max-width: 800px; margin: 0 auto; padding: 40px 20px 80px; }
.tips-card {
  display: flex; gap: 16px; background: rgba(255,107,53,0.05);
  border: 1px solid rgba(255,107,53,0.15); border-radius: 12px; padding: 24px;
}
.tips-icon { color: #FF6B35; flex-shrink: 0; margin-top: 2px; }
.tips-card h4 { color: #e0d6c8; font-size: 1em; margin: 0 0 12px; }
.tips-list p { color: #a89880; font-size: 0.88em; margin: 0 0 8px; line-height: 1.5; }
.tips-list p span { margin-right: 6px; }
</style>