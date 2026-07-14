<script setup>
import EventsSection from '../components/EventsSection.vue'
import { CalendarDays, Clock, MapPin } from '@lucide/vue'

const PLACEHOLDER = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='300'%3E%3Cdefs%3E%3ClinearGradient id='g' x1='0%25' y1='0%25' x2='100%25' y2='100%25'%3E%3Cstop offset='0%25' style='stop-color:%232a1f14'/%3E%3Cstop offset='50%25' style='stop-color:%233a2a18'/%3E%3Cstop offset='100%25' style='stop-color:%232a1f14'/%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width='400' height='300' fill='url(%23g)'/%3E%3C/svg%3E"
const onImgError = (e) => { if (e.target.src !== PLACEHOLDER) e.target.src = PLACEHOLDER }

const pastEvents = [
  { title: '端午粽子节', date: '2026年6月', desc: '20家摊位推出限定粽子口味，现场包粽比赛吸引500+人参与。', image: 'https://images.unsplash.com/photo-1584720553964-2c269efd7291?w=400&h=250&fit=crop' },
  { title: '五一美食狂欢周', date: '2026年5月', desc: '连续7天美食特惠，累计接待食客超8万人次，创历史新高。', image: 'https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=400&h=250&fit=crop' },
  { title: '春季烧烤节', date: '2026年4月', desc: '联合10家烧烤摊位举办户外烧烤派对，啤酒畅饮搭配炭火烤肉。', image: 'https://images.unsplash.com/photo-1558030006-450675393462?w=400&h=250&fit=crop' },
]
</script>

<template>
  <div class="events-page-wrap">
    <div class="page-top-spacer"></div>
    <section class="page-hero">
      <h1>活动公告</h1>
      <p>精彩活动不间断 · 总有一款适合你</p>
    </section>
    <EventsSection />
    <section class="past-events">
      <h2 class="section-title"><CalendarDays :size="22" /> 往期活动回顾</h2>
      <div class="past-grid">
        <div class="past-card" v-for="e in pastEventsList" :key="e.id">
          <img :src="e.image_url" :alt="e.title" class="past-img" @error="onImgError" />
          <div class="past-body">
            <h3>{{ e.title }}</h3>
            <p class="past-date"><Clock :size="12" /> {{ e.date }}</p>
            <p class="past-desc">{{ e.description }}</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.events-page-wrap { min-height: 100vh; }
.page-top-spacer { height: 80px; }
.page-hero { text-align: center; padding: 40px 20px; background: linear-gradient(135deg, rgba(255,107,53,0.06), transparent); }
.page-hero h1 { font-size: 2.4em; font-weight: 800; color: #FF6B35; margin: 0 0 6px; letter-spacing: 3px; }
.page-hero p { color: #a89880; font-size: 1em; }

.section-title { font-size: 1.8em; font-weight: 800; color: #e0d6c8; display: flex; align-items: center; gap: 10px; }

.past-events { max-width: 1100px; margin: 0 auto; padding: 60px 20px 80px; }
.past-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-top: 28px; }
.past-card { background: rgba(26,22,18,0.6); border: 1px solid rgba(255,255,255,0.04); border-radius: 12px; overflow: hidden; transition: all 0.3s; }
.past-card:hover { transform: translateY(-4px); border-color: rgba(255,107,53,0.15); }
.past-img { width: 100%; height: 180px; object-fit: cover; }
.past-body { padding: 18px; }
.past-body h3 { color: #e0d6c8; font-size: 1.05em; margin: 0 0 8px; }
.past-date { display: flex; align-items: center; gap: 4px; color: #FF6B35; font-size: 0.8em; margin: 0 0 8px; }
.past-desc { color: #a89880; font-size: 0.85em; margin: 0; line-height: 1.5; }

@media (max-width: 768px) { .past-grid { grid-template-columns: 1fr; } }
</style>