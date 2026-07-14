<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { ChevronLeft, ChevronRight } from '@lucide/vue'

const PLACEHOLDER = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='1400' height='700'%3E%3Cdefs%3E%3ClinearGradient id='g' x1='0%25' y1='0%25' x2='100%25' y2='100%25'%3E%3Cstop offset='0%25' style='stop-color:%232a1f14'/%3E%3Cstop offset='50%25' style='stop-color:%233a2a18'/%3E%3Cstop offset='100%25' style='stop-color:%232a1f14'/%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width='1400' height='700' fill='url(%23g)'/%3E%3C/svg%3E"

const slides = [
  { image: 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=1400&h=700&fit=crop', title: '越夜越美味', subtitle: '烟火美食街' },
  { image: 'https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=1400&h=700&fit=crop', title: '地道夜市风味', subtitle: '每晚17:00 – 凌晨02:00 不见不散' },
  { image: 'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=1400&h=700&fit=crop', title: '百种美食等你来', subtitle: '烟火气里寻美味' },
  { image: 'https://images.unsplash.com/photo-1550966871-3ed3cdb51f3a?w=1400&h=700&fit=crop', title: '人间烟火味', subtitle: '最抚凡人心' },
]

const current = ref(0)
let timer = null

const onImgError = (e) => { if (e.target.src !== PLACEHOLDER) e.target.src = PLACEHOLDER }

const next = () => { current.value = (current.value + 1) % slides.length }
const prev = () => { current.value = (current.value - 1 + slides.length) % slides.length }
const goTo = (i) => { current.value = i }

onMounted(() => { timer = setInterval(next, 5000) })
onUnmounted(() => { clearInterval(timer) })
</script>

<template>
  <section id="首页" class="hero">
    <div class="hero-slides">
      <div class="slide" v-for="(s, i) in slides" :key="i" :class="{ active: i === current }">
        <img :src="s.image" :alt="s.title" class="slide-img" @error="onImgError" />
      </div>
    </div>
    <div class="hero-overlay"></div>
    <div class="hero-content">
      <h1 class="hero-title">{{ slides[current].title }}</h1>
      <p class="hero-sub">{{ slides[current].subtitle }}</p>
      <router-link to="/food-map" class="hero-btn">
        立即探索摊位
        <span class="btn-arrow">&#8594;</span>
      </router-link>
    </div>
    <div class="hero-nav">
      <button class="hero-arrow" @click="prev"><ChevronLeft :size="28" /></button>
      <div class="hero-dots">
        <span v-for="(s, i) in slides" :key="i" class="dot" :class="{ active: i === current }" @click="goTo(i)"></span>
      </div>
      <button class="hero-arrow" @click="next"><ChevronRight :size="28" /></button>
    </div>
  </section>
</template>

<style scoped>
.hero {
  position: relative; width: 100%; height: 100vh; min-height: 560px;
  overflow: hidden; display: flex; align-items: center; justify-content: center;
}
.hero-slides { position: absolute; inset: 0; }
.slide { position: absolute; inset: 0; opacity: 0; transition: opacity 1s ease; }
.slide.active { opacity: 1; }
.slide-img { width: 100%; height: 100%; object-fit: cover; }
.hero-overlay {
  position: absolute; inset: 0;
  background: linear-gradient(to bottom, rgba(20,14,8,0.6) 0%, rgba(20,14,8,0.8) 60%, #14120e 100%);
}
.hero-content {
  position: relative; z-index: 2; text-align: center; padding: 0 20px;
}
.hero-title {
  font-size: clamp(2.5em, 6vw, 4.5em); font-weight: 900; color: #fff;
  text-shadow: 0 0 40px rgba(255,107,53,0.5); margin: 0; letter-spacing: 6px;
}
.hero-sub {
  font-size: clamp(1em, 2vw, 1.3em); color: #c0a880; margin: 16px 0 32px; letter-spacing: 2px;
}
.hero-btn {
  display: inline-flex; align-items: center; gap: 8px;
  background: linear-gradient(135deg, #FF6B35, #f0932b);
  color: #fff; padding: 14px 36px; border-radius: 50px; text-decoration: none;
  font-size: 1.1em; font-weight: 600; letter-spacing: 2px;
  transition: all 0.3s; box-shadow: 0 4px 20px rgba(255,107,53,0.4);
}
.hero-btn:hover { transform: translateY(-2px); box-shadow: 0 8px 30px rgba(255,107,53,0.6); }
.btn-arrow { font-size: 1.2em; animation: bounce 1.5s infinite; }
@keyframes bounce { 0%,100%{transform:translateY(0)} 50%{transform:translateY(6px)} }
.hero-nav {
  position: absolute; bottom: 40px; z-index: 3;
  display: flex; align-items: center; gap: 16px;
}
.hero-arrow {
  background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2);
  color: #fff; border-radius: 50%; width: 44px; height: 44px;
  display: flex; align-items: center; justify-content: center; cursor: pointer;
  transition: all 0.2s;
}
.hero-arrow:hover { background: rgba(255,107,53,0.3); border-color: #FF6B35; }
.hero-dots { display: flex; gap: 10px; }
.dot { width: 10px; height: 10px; border-radius: 50%; background: rgba(255,255,255,0.3); cursor: pointer; transition: all 0.3s; }
.dot.active { background: #FF6B35; box-shadow: 0 0 10px #FF6B35; width: 28px; border-radius: 10px; }
@media (max-width: 767px) { .hero-title { font-size: 1.8em !important; } .hero-sub { font-size: 0.9em !important; } .hero-content { padding: 80px 20px !important; } } </style>