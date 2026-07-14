<script setup>
import { ref, onMounted } from "vue"
import api from "../api"

import { useRouter } from 'vue-router'
import { Flame, MapPin, Star, Gift, ArrowRight } from '@lucide/vue'
import HeroBanner from '../components/HeroBanner.vue'

const PLACEHOLDER = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='300'%3E%3Cdefs%3E%3ClinearGradient id='g' x1='0%25' y1='0%25' x2='100%25' y2='100%25'%3E%3Cstop offset='0%25' style='stop-color:%232a1f14'/%3E%3Cstop offset='50%25' style='stop-color:%233a2a18'/%3E%3Cstop offset='100%25' style='stop-color:%232a1f14'/%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width='400' height='300' fill='url(%23g)'/%3E%3C/svg%3E"

const router = useRouter()
const hotStalls = ref([])

onMounted(async () => {
  try {
    const { data } = await api.get('/stores/')
    hotStalls.value = (Array.isArray(data) ? data : []).sort((a, b) => b.popularity - a.popularity).slice(0, 4)
  } catch {}
})

const onImgError = (e) => { if (e.target.src !== PLACEHOLDER) e.target.src = PLACEHOLDER }
</script>

<template>
  <div class="home-page">
    <HeroBanner />

    <section class="quick-links">
      <div class="ql-grid">
        <div class="ql-card" @click="router.push('/food-map')">
          <MapPin :size="28" class="ql-icon" />
          <h3>店铺目录</h3>
          <p>探索50+摊位</p>
          <ArrowRight :size="16" class="ql-arrow" />
        </div>
        <div class="ql-card" @click="router.push('/today')">
          <Flame :size="28" class="ql-icon" />
          <h3>今日推荐</h3>
          <p>主厨特选每日更新</p>
          <ArrowRight :size="16" class="ql-arrow" />
        </div>
        <div class="ql-card" @click="router.push('/events')">
          <Gift :size="28" class="ql-icon" />
          <h3>限时活动</h3>
          <p>精彩活动不间断</p>
          <ArrowRight :size="16" class="ql-arrow" />
        </div>
        <div class="ql-card" @click="router.push('/reviews')">
          <Star :size="28" class="ql-icon" />
          <h3>食客口碑</h3>
          <p>看看大家怎么说</p>
          <ArrowRight :size="16" class="ql-arrow" />
        </div>
      </div>
    </section>

    <section class="intro-section">
      <div class="intro-content">
        <h2>欢迎来到烟火美食街</h2>
        <p class="intro-desc">
          成立于2010年，从最初十几个路边摊发展到如今汇聚50多家特色美食的包头最大夜市。<br/>
          每晚17:00至凌晨02:00，钢铁大街包百商圈，烟火气里寻美味，最抚凡人心。
        </p>
        <div class="intro-stats">
          <div class="stat"><strong>50+</strong><span>特色摊位</span></div>
          <div class="stat"><strong>100+</strong><span>美食种类</span></div>
          <div class="stat"><strong>5K+</strong><span>日均客流</span></div>
          <div class="stat"><strong>9h</strong><span>每晚营业</span></div>
        </div>
      </div>
    </section>

    <section class="hot-section">
      <div class="section-header">
        <h2><Flame :size="24" class="title-fire" /> 人气最高</h2>
        <p>看看大家都在排队吃什么</p>
      </div>
      <div class="hot-grid">
        <div class="hot-card" v-for="s in hotStalls" :key="s.id" @click="router.push('/food-map')">
          <div class="hot-rank">{{ s.popularity }}%推荐</div>
          <img :src="s.image_url" :alt="s.name" class="hot-img" @error="onImgError" />
          <div class="hot-body">
            <h3>{{ s.name }}</h3>
            <span class="hot-price">{{ s.price }}</span>
          </div>
        </div>
      </div>
    </section>

    <section class="info-banner">
      <div class="banner-content">
        <div class="banner-text">
          <h3>&#127753; 每晚 17:00 — 凌晨 02:00</h3>
          <p>节假日照常营业 · 风雨无阻 · 等您来尝</p>
        </div>
        <router-link to="/transport" class="banner-btn">如何到达</router-link>
      </div>
    </section>
  </div>
</template>


<style scoped>
.home-page { overflow: hidden; }

.quick-links { max-width: 1100px; margin: -40px auto 0; padding: 0 16px; position: relative; z-index: 5; }
.ql-grid { display: grid; grid-template-columns: 1fr; gap: 12px; }
.ql-card {
  background: rgba(26,22,18,0.9); border: 1px solid rgba(255,107,53,0.15);
  border-radius: 14px; padding: 24px 20px; cursor: pointer; text-align: center;
  transition: all 0.3s; position: relative; overflow: hidden;
}
.ql-card:hover { transform: translateY(-4px); border-color: #FF6B35; box-shadow: 0 8px 30px rgba(255,107,53,0.15); }
.ql-icon { color: #FF6B35; margin-bottom: 10px; }
.ql-card h3 { color: #e0d6c8; font-size: 1em; margin: 0 0 4px; }
.ql-card p { color: #887766; font-size: 0.8em; margin: 0 0 12px; }
.ql-arrow { color: #FF6B35; opacity: 0; transition: all 0.3s; }
.ql-card:hover .ql-arrow { opacity: 1; }

.intro-section { max-width: 900px; margin: 0 auto; padding: 60px 16px 40px; }
.intro-content { text-align: center; }
.intro-content h2 { font-size: 1.6em; color: #FF6B35; margin: 0 0 16px; font-weight: 800; }
.intro-desc { color: #a89880; font-size: 1.05em; max-width: 700px; margin: 0 auto 40px; line-height: 1.8; }
.intro-stats { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; }
.stat { display: flex; flex-direction: column; align-items: center; }
.stat strong { font-size: 1.8em; color: #e0d6c8; font-weight: 800; }
.stat span { font-size: 0.9em; color: #887766; margin-top: 4px; }

.hot-section { max-width: 1100px; margin: 0 auto; padding: 32px 16px 60px; }
.section-header { text-align: center; margin-bottom: 32px; }
.section-header h2 { font-size: 2em; color: #FF6B35; display: flex; align-items: center; justify-content: center; gap: 8px; margin: 0 0 8px; font-weight: 800; }
.section-header p { color: #a89880; font-size: 1em; }
.title-fire { animation: pulse 2s ease-in-out infinite; }
@keyframes pulse { 0%,100%{color:#FF6B35} 50%{color:#f0932b;transform:scale(1.1)} }

.hot-grid { display: grid; grid-template-columns: 1fr; gap: 16px; }
.hot-card {
  background: rgba(26,22,18,0.6); border: 1px solid rgba(255,255,255,0.04);
  border-radius: 12px; overflow: hidden; cursor: pointer; transition: all 0.3s;
}
.hot-card:hover { transform: translateY(-4px); border-color: rgba(255,107,53,0.2); }
.hot-rank {
  position: absolute; top: 10px; left: 10px; z-index: 1;
  background: rgba(255,107,53,0.9); color: #fff; padding: 3px 10px;
  border-radius: 8px; font-size: 0.75em; font-weight: 600;
}
.hot-card { position: relative; }
.hot-img { width: 100%; height: 160px; object-fit: cover; }
.hot-body { padding: 14px 16px; }
.hot-body h3 { color: #e0d6c8; font-size: 0.95em; margin: 0 0 6px; }
.hot-price { color: #FF6B35; font-weight: 700; font-size: 0.9em; }

.info-banner { max-width: 1100px; margin: 0 auto 60px; padding: 0 16px; }
.banner-content {
  display: flex; align-items: center; justify-content: space-between;
  background: linear-gradient(135deg, rgba(255,107,53,0.1), rgba(255,107,53,0.03));
  border: 1px solid rgba(255,107,53,0.2); border-radius: 16px; padding: 32px 36px;
  gap: 20px;
}
.banner-text h3 { color: #FF6B35; font-size: 1.2em; margin: 0 0 6px; }
.banner-text p { color: #a89880; font-size: 0.9em; margin: 0; }
.banner-btn {
  flex-shrink: 0; background: linear-gradient(135deg, #FF6B35, #f0932b);
  color: #fff; padding: 12px 28px; border-radius: 50px; text-decoration: none;
  font-weight: 600; font-size: 0.95em; transition: all 0.3s;
  box-shadow: 0 4px 16px rgba(255,107,53,0.3);
}
.banner-btn:hover { transform: translateY(-2px); box-shadow: 0 6px 24px rgba(255,107,53,0.5); }

/* Mobile-first: default = 1col mobile, enhanced up */
@media (min-width: 480px) {
  .ql-grid { grid-template-columns: repeat(2, 1fr); }
  .hot-grid { grid-template-columns: repeat(2, 1fr); }
  .intro-stats { gap: 16px; }
  .intro-stats { grid-template-columns: repeat(2, 1fr); }
}
@media (min-width: 768px) {
  .ql-grid { grid-template-columns: repeat(4, 1fr); gap: 16px; }
  .hot-grid { grid-template-columns: repeat(4, 1fr); gap: 20px; }
  .intro-stats { display: flex; flex-direction: row; gap: 32px; }
  .stat strong { font-size: 1.8em; }
  .intro-content h2 { font-size: 1.6em; }
}
@media (min-width: 1024px) {
  .intro-stats { gap: 60px; }
  .intro-section { padding: 80px 20px 60px; }
}
</style>