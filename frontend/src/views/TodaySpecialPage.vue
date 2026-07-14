<script setup>
import { ref, computed, onMounted } from "vue"
import api from "../api"

import { stalls } from '../data/foodData.js'
import TodaySpecial from '../components/TodaySpecial.vue'
import { Flame, TrendingUp, ThumbsUp } from '@lucide/vue'

const topStalls = stalls.sort((a, b) => b.popularity - a.popularity).slice(0, 5)
const cheapEats = [...stalls].sort((a, b) => {
  const priceA = parseInt(a.price.replace(/[^0-9]/g, ''))
  const priceB = parseInt(b.price.replace(/[^0-9]/g, ''))
  return priceA - priceB
}).slice(0, 4)
</script>

<template>
  <div class="today-page">
    <div class="page-top-spacer"></div>
    <section class="page-hero">
      <h1>今日推荐</h1>
      <p>每日精选 · 不容错过</p>
    </section>

    <TodaySpecial />

    <section class="ranking-section">
      <h2 class="section-title"><TrendingUp :size="24" /> 本周人气排行</h2>
      <p class="section-desc">基于本周实际销量和食客评价综合排名</p>
      <div class="ranking-list">
        <div class="rank-item" v-for="(s, i) in topStalls" :key="s.id">
          <span class="rank-num" :class="'rank-' + (i + 1)">#{{ i + 1 }}</span>
          <img :src="s.image || s.image_url" :alt="s.name" class="rank-img" />
          <div class="rank-info">
            <h3>{{ s.name }}</h3>
            <span class="rank-meta">{{ s.price }} · {{ s.popularity }}%推荐</span>
          </div>
          <div class="rank-bar"><div class="rank-fill" :style="{ width: s.popularity + '%' }"></div></div>
        </div>
      </div>
    </section>

    <section class="cheap-section">
      <h2 class="section-title"><ThumbsUp :size="24" /> 性价比之选</h2>
      <p class="section-desc">十元左右吃饱吃好，学生党福音</p>
      <div class="cheap-grid">
        <div class="cheap-card" v-for="s in cheapEats" :key="s.id">
          <img :src="s.image || s.image_url" :alt="s.name" />
          <div class="cheap-body">
            <h3>{{ s.name }}</h3>
            <span>{{ s.price }}</span>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.today-page { min-height: 100vh; }
.page-top-spacer { height: 80px; }
.page-hero {
  text-align: center; padding: 40px 20px;
  background: linear-gradient(135deg, rgba(255,107,53,0.06), transparent);
}
.page-hero h1 { font-size: 2.4em; font-weight: 800; color: #FF6B35; margin: 0 0 6px; letter-spacing: 3px; }
.page-hero p { color: #a89880; font-size: 1em; }

.section-title { font-size: 1.8em; font-weight: 800; color: #e0d6c8; display: flex; align-items: center; gap: 10px; }
.section-desc { color: #887766; font-size: 0.9em; margin: 0 0 28px; }

.ranking-section { max-width: 900px; margin: 0 auto; padding: 60px 20px; }
.ranking-list { display: flex; flex-direction: column; gap: 12px; }
.rank-item { display: flex; align-items: center; gap: 16px; background: rgba(26,22,18,0.6); border: 1px solid rgba(255,255,255,0.04); border-radius: 12px; padding: 14px 20px; position: relative; overflow: hidden; }
.rank-num { font-size: 1.2em; font-weight: 800; width: 44px; text-align: center; color: #887766; }
.rank-1 { color: #f0932b; font-size: 1.4em; }
.rank-2 { color: #a0a0a0; }
.rank-3 { color: #cd7f32; }
.rank-img { width: 56px; height: 56px; border-radius: 10px; object-fit: cover; flex-shrink: 0; }
.rank-info { flex: 1; }
.rank-info h3 { color: #e0d6c8; font-size: 1em; margin: 0 0 4px; }
.rank-meta { color: #887766; font-size: 0.8em; }
.rank-bar { width: 100px; height: 6px; background: rgba(255,255,255,0.06); border-radius: 3px; flex-shrink: 0; }
.rank-fill { height: 100%; background: linear-gradient(90deg, #FF6B35, #f0932b); border-radius: 3px; transition: width 0.6s ease; }

.cheap-section { max-width: 900px; margin: 0 auto; padding: 0 20px 80px; }
.cheap-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }
.cheap-card { background: rgba(26,22,18,0.6); border: 1px solid rgba(255,255,255,0.04); border-radius: 12px; overflow: hidden; transition: all 0.3s; }
.cheap-card:hover { transform: translateY(-2px); border-color: rgba(255,107,53,0.15); }
.cheap-card img { width: 100%; height: 120px; object-fit: cover; }
.cheap-body { padding: 12px; }
.cheap-body h3 { color: #e0d6c8; font-size: 0.88em; margin: 0 0 4px; }
.cheap-body span { color: #FF6B35; font-size: 0.85em; font-weight: 600; }

@media (max-width: 768px) { .cheap-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 480px) { .rank-bar { display: none; } .cheap-grid { grid-template-columns: 1fr; } }
</style>