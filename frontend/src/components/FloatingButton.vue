<script setup>
import { ref } from 'vue'
import { foodRecommendations } from '../data/foodData.js'
import { UtensilsCrossed, X } from '@lucide/vue'

const showRec = ref(false)
const recText = ref('')

const getRandomRec = () => {
  const i = Math.floor(Math.random() * foodRecommendations.length)
  recText.value = foodRecommendations[i]
  showRec.value = true
  setTimeout(() => { showRec.value = false }, 4000)
}
</script>

<template>
  <div class="floating-btn-wrap">
    <button class="floating-btn" @click="getRandomRec" title="今天想吃什么？">
      <UtensilsCrossed :size="22" />
    </button>
    <transition name="fade">
      <div v-if="showRec" class="floating-rec">
        <span>{{ recText }}</span>
        <button @click="showRec = false"><X :size="14" /></button>
      </div>
    </transition>
  </div>
</template>

<style scoped>
.floating-btn-wrap { position: fixed; bottom: 28px; right: 28px; z-index: 999; display: flex; flex-direction: column; align-items: flex-end; gap: 8px; }
.floating-btn {
  width: 52px; height: 52px; border-radius: 50%;
  background: linear-gradient(135deg, #FF6B35, #f0932b);
  border: none; color: #fff; cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 4px 20px rgba(255,107,53,0.5);
  transition: all 0.3s; animation: float 3s ease-in-out infinite;
}
.floating-btn:hover { transform: scale(1.1); box-shadow: 0 8px 30px rgba(255,107,53,0.7); }
@keyframes float { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-6px)} }

.floating-rec {
  display: flex; align-items: center; gap: 8px;
  background: rgba(26,22,18,0.95); border: 1px solid rgba(255,107,53,0.3);
  color: #e0d6c8; padding: 10px 16px; border-radius: 20px;
  font-size: 0.85em; white-space: nowrap; box-shadow: 0 4px 16px rgba(0,0,0,0.4);
}
.floating-rec button { background: none; border: none; color: #887766; cursor: pointer; padding: 0; display: flex; }

.fade-enter-active, .fade-leave-active { transition: opacity 0.3s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>