<script setup>
import { ref, onMounted } from "vue"
import api from "../api"

const PLACEHOLDER = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='300'%3E%3Cdefs%3E%3ClinearGradient id='g' x1='0%25' y1='0%25' x2='100%25' y2='100%25'%3E%3Cstop offset='0%25' style='stop-color:%232a1f14'/%3E%3Cstop offset='50%25' style='stop-color:%233a2a18'/%3E%3Cstop offset='100%25' style='stop-color:%232a1f14'/%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width='400' height='300' fill='url(%23g)'/%3E%3C/svg%3E"
const onImgError = (e) => { if (e.target.src !== PLACEHOLDER) e.target.src = PLACEHOLDER }

const special = ref(null)
const currentEvent = ref(null)
const events = ref([])

onMounted(async () => {
  try {
    const [specRes, evtRes] = await Promise.all([
      api.get('/todays-special/'),
      api.get('/events/')
    ])
    if (specRes.data) special.value = specRes.data
    if (Array.isArray(evtRes.data) && evtRes.data.length) events.value = evtRes.data
      currentEvent.value = evtRes.data[0]
  } catch {}
})
</script>

<template>
  <section id="活动公告" class="today-section">
    <div class="section-header">
      <h2 class="section-title"><span class="title-icon">&#127881;</span> 今日推荐 & 限时活动</h2>
    </div>
    <div class="today-grid">
      <div class="special-card">
        <div class="special-tag">{{ special?.tag || '' }}</div>
        <img :src="special?.image_url || special?.store_image || PLACEHOLDER" :alt="special?.name || ''" class="special-img" @error="onImgError" />
        <div class="special-body">
          <h3>{{ special?.name || '' }}</h3>
          <p>{{ special?.description || '' }}</p>
          <span class="special-price">{{ special?.price || '' }}</span>
        </div>
      </div>

      <div class="events-list">
        <h3 class="events-title">&#128197; 限时活动</h3>
        <div class="event-card" v-for="e in events" :key="e.id">
          <div class="event-tag">{{ e.tag }}</div>
          <div class="event-info">
            <h4>{{ e.title }}</h4>
            <p class="event-date">{{ e.date }}</p>
            <p class="event-desc">{{ e.description }}</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.today-section { max-width: 1280px; margin: 0 auto; padding: 80px 20px; }
.section-header { text-align: center; margin-bottom: 40px; }
.section-title { font-size: clamp(2em, 4vw, 2.6em); font-weight: 800; color: #FF6B35; display: flex; align-items: center; justify-content: center; gap: 12px; margin: 0; }

.today-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }

.special-card {
  background: rgba(26,22,18,0.8); border: 1px solid rgba(255,107,53,0.2);
  border-radius: 16px; overflow: hidden; position: relative; transition: all 0.3s;
}
.special-card:hover { box-shadow: 0 8px 30px rgba(255,107,53,0.2); }
.special-tag {
  position: absolute; top: 16px; left: 16px; z-index: 1;
  background: linear-gradient(135deg, #FF6B35, #f0932b); color: #fff;
  padding: 5px 14px; border-radius: 12px; font-size: 0.8em; font-weight: 700;
}
.special-img { width: 100%; height: 240px; object-fit: cover; }
.special-body { padding: 20px; }
.special-body h3 { color: #e0d6c8; font-size: 1.3em; margin: 0 0 8px; }
.special-body p { color: #a89880; font-size: 0.9em; margin: 0 0 12px; line-height: 1.6; }
.special-price { color: #FF6B35; font-weight: 700; font-size: 1.2em; }

.events-list { display: flex; flex-direction: column; gap: 12px; }
.events-title { color: #e0d6c8; font-size: 1.2em; margin: 0 0 4px; }
.event-card {
  display: flex; gap: 14px; background: rgba(26,22,18,0.6);
  border: 1px solid rgba(255,255,255,0.04); border-radius: 12px; padding: 16px;
  transition: all 0.3s;
}
.event-card:hover { border-color: rgba(255,107,53,0.2); background: rgba(26,22,18,0.9); }
.event-tag {
  flex-shrink: 0; width: 48px; height: 48px; display: flex; align-items: center; justify-content: center;
  background: rgba(255,107,53,0.15); color: #FF6B35; border-radius: 10px; font-size: 0.75em; font-weight: 700;
}
.event-info { flex: 1; }
.event-info h4 { color: #e0d6c8; margin: 0 0 4px; font-size: 0.95em; }
.event-date { color: #FF6B35; font-size: 0.8em; margin: 0 0 4px; }
.event-desc { color: #a89880; font-size: 0.82em; margin: 0; line-height: 1.5; }

@media (max-width: 768px) {
  .today-grid { grid-template-columns: 1fr; }
}
</style>