<script setup>
import { events } from '../data/foodData.js'
</script>

<template>
  <section id="活动公告" class="events-page">
    <div class="section-header">
      <h2 class="section-title"><span class="title-icon">&#127881;</span> 活动公告</h2>
      <p class="section-desc">精彩活动不间断，总有一款适合你</p>
    </div>
    <div class="events-grid">
      <div class="event-card" v-for="e in events" :key="e.id">
        <div class="event-tag">{{ e.tag }}</div>
        <div class="event-body">
          <h3>{{ e.title }}</h3>
          <p class="event-date">&#128197; {{ e.date }}</p>
          <p class="event-desc">{{ e.desc }}</p>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.events-page { max-width: 1280px; margin: 0 auto; padding: 80px 20px; }
.section-header { text-align: center; margin-bottom: 40px; }
.section-title { font-size: clamp(2em, 4vw, 2.6em); font-weight: 800; color: #FF6B35; display: flex; align-items: center; justify-content: center; gap: 12px; margin: 0 0 8px; }
.section-desc { color: #a89880; font-size: 1.1em; }

.events-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 24px; }
.event-card {
  background: rgba(26,22,18,0.8); border: 1px solid rgba(255,255,255,0.06);
  border-radius: 16px; overflow: hidden; transition: all 0.3s;
}
.event-card:hover { border-color: rgba(255,107,53,0.2); transform: translateY(-4px); box-shadow: 0 8px 30px rgba(255,107,53,0.1); }
.event-tag {
  padding: 12px 20px;
  background: linear-gradient(135deg, rgba(255,107,53,0.15), rgba(255,107,53,0.05));
  color: #FF6B35; font-weight: 700; font-size: 0.85em;
}
.event-body { padding: 20px; }
.event-body h3 { color: #e0d6c8; font-size: 1.2em; margin: 0 0 8px; }
.event-date { color: #FF6B35; font-size: 0.85em; margin: 0 0 8px; }
.event-desc { color: #a89880; font-size: 0.9em; margin: 0; line-height: 1.6; }

@media (max-width: 640px) { .events-grid { grid-template-columns: 1fr; } }
</style>
