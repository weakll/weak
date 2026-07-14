<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Menu, X, Clock, User, LogOut } from '@lucide/vue'
import { useAuth } from '../composables/useAuth.js'

const router = useRouter()
const route = useRoute()
const menuOpen = ref(false)
const status = ref('营业中')
const scrolled = ref(false)

const toggleMenu = () => { menuOpen.value = !menuOpen.value }

const { currentUser, isLoggedIn, openAuthModal, logout } = useAuth()

const countdown = ref('')
let timer = null

const updateCountdown = () => {
  const now = new Date()
  const h = now.getHours()
  const m = now.getMinutes()
  if (h >= 17 || h < 2 || (h === 2 && m === 0)) {
    status.value = '营业中'
    const end = new Date(now)
    end.setHours(2, 0, 0, 0)
    if (h < 2) end.setDate(end.getDate())
    else if (h >= 17) end.setDate(end.getDate() + 1)
    let diff = Math.round((end - now) / 1000)
    if (diff < 0) diff = 0
    const hh = Math.floor(diff / 3600)
    const mm = Math.floor((diff % 3600) / 60)
    const ss = diff % 60
    countdown.value = `${String(hh).padStart(2,'0')}:${String(mm).padStart(2,'0')}:${String(ss).padStart(2,'0')}`
  } else {
    status.value = '已打烊'
    const open = new Date(now)
    open.setHours(17, 0, 0, 0)
    if (h >= 2) open.setDate(open.getDate())
    let diff = Math.round((open - now) / 1000)
    if (diff < 0) diff = 0
    const hh = Math.floor(diff / 3600)
    const mm = Math.floor((diff % 3600) / 60)
    const ss = diff % 60
    countdown.value = `${String(hh).padStart(2,'0')}:${String(mm).padStart(2,'0')}:${String(ss).padStart(2,'0')}`
  }
}

onMounted(() => {
  updateCountdown()
  timer = setInterval(updateCountdown, 1000)
  window.addEventListener('scroll', () => { scrolled.value = window.scrollY > 50 })
})
onUnmounted(() => { clearInterval(timer) })

const navItems = [
  { label: '首页', path: '/' },
  { label: '今日推荐', path: '/today' },
  { label: '活动公告', path: '/events' },
  { label: '店铺目录', path: '/food-map' },
  { label: '食客点评', path: '/reviews' },
  { label: '交通指南', path: '/transport' },
  { label: '关于我们', path: '/about' },
]
</script>

<template>
  <nav class="navbar" :class="{ scrolled }">
    <div class="nav-inner">
      <router-link to="/" class="logo" @click="menuOpen = false">
        <span class="logo-icon">&#127753;</span>
        <span class="logo-text">烟火美食街</span>
      </router-link>
      <ul class="nav-links" :class="{ open: menuOpen }">
        <li v-for="item in navItems" :key="item.path">
          <router-link
            :to="item.path"
            :class="{ active: route.path === item.path }"
            @click="menuOpen = false"
          >{{ item.label }}</router-link>
        </li>
      </ul>
      <div class="nav-right">
        <span class="status-badge" :class="status === '营业中' ? 'open' : 'closed'">
          <span class="status-dot"></span>
          {{ status }}
        </span>
        <span class="countdown-box">
          <Clock :size="14" />
          {{ status === '营业中' ? '距收市' : '距开市' }} {{ countdown }}
        </span>
        <template v-if="isLoggedIn">
          <div class="user-menu">
            <img :src="currentUser.avatar" class="user-avatar" :alt="currentUser.username" />
            <span class="user-name">{{ currentUser.username }}</span>
            <button class="logout-btn" @click="logout" title="退出登录"><LogOut :size="15" /></button>
          </div>
        </template>
        <button v-else class="auth-btn" @click="openAuthModal">
          <User :size="16" />
          <span>登录</span>
        </button>
      </div>
      <button class="menu-btn" @click="toggleMenu">
        <Menu v-if="!menuOpen" :size="24" />
        <X v-else :size="24" />
      </button>
    </div>
  </nav>
</template>

<style scoped>
.navbar {
  position: fixed; top: 0; left: 0; right: 0; z-index: 1000;
  padding: 12px 0; transition: all 0.3s;
  background: transparent;
}
.navbar.scrolled {
  background: rgba(20, 18, 16, 0.95); backdrop-filter: blur(10px);
  box-shadow: 0 2px 20px rgba(0,0,0,0.5);
}
.nav-inner {
  max-width: 1280px; margin: 0 auto; padding: 0 20px;
  display: flex; align-items: center; gap: 24px;
}
.logo { display: flex; align-items: center; gap: 8px; flex-shrink: 0; text-decoration: none; }
.logo-icon { font-size: 1.6em; }
.logo-text { font-size: 1.3em; font-weight: 700; color: #FF6B35; letter-spacing: 2px; }
.nav-links { display: flex; gap: 8px; list-style: none; margin: 0; padding: 0; flex: 1; justify-content: center; }
.nav-links a {
  color: #e0d6c8; text-decoration: none; font-size: 0.9em;
  padding: 6px 14px; border-radius: 6px; transition: all 0.2s;
  white-space: nowrap;
}
.nav-links a:hover { color: #FF6B35; background: rgba(255,107,53,0.1); }
.nav-links a.active {
  color: #FF6B35; background: rgba(255,107,53,0.15);
}
.nav-right { display: flex; align-items: center; gap: 14px; flex-shrink: 0; }
.status-badge {
  display: flex; align-items: center; gap: 6px; padding: 4px 12px;
  border-radius: 20px; font-size: 0.8em; font-weight: 600;
}
.status-badge.open { background: rgba(34,197,94,0.15); color: #22c55e; border: 1px solid rgba(34,197,94,0.3); }
.status-badge.closed { background: rgba(239,68,68,0.15); color: #ef4444; border: 1px solid rgba(239,68,68,0.3); }
.status-dot { width: 6px; height: 6px; border-radius: 50%; display: inline-block; }
.status-badge.open .status-dot { background: #22c55e; box-shadow: 0 0 6px #22c55e; }
.status-badge.closed .status-dot { background: #ef4444; }
.countdown-box {
  display: flex; align-items: center; gap: 5px; color: #a89880; font-size: 0.8em;
  font-family: monospace; letter-spacing: 1px;
}
.menu-btn { display: none; background: none; border: none; color: #e0d6c8; cursor: pointer; padding: 4px; }

.auth-btn {
  display: flex; align-items: center; gap: 6px;
  background: rgba(255,107,53,0.12); border: 1px solid rgba(255,107,53,0.3);
  color: #FF6B35; border-radius: 20px; padding: 6px 16px;
  cursor: pointer; font-size: 0.85em; font-weight: 600; transition: all 0.2s;
}
.auth-btn:hover { background: rgba(255,107,53,0.2); }
.user-menu {
  display: flex; align-items: center; gap: 8px;
  background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08);
  border-radius: 20px; padding: 3px 12px 3px 3px;
}
.user-avatar { width: 28px; height: 28px; border-radius: 50%; object-fit: cover; flex-shrink: 0; }
.user-name { color: #e0d6c8; font-size: 0.82em; max-width: 80px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.logout-btn {
  background: none; border: none; color: #887766; cursor: pointer; padding: 2px;
  display: flex; align-items: center; transition: color 0.2s;
}
.logout-btn:hover { color: #ef4444; }

/* Mobile-first: hamburger by default, desktop nav at 768px+ */
@media (max-width: 767px) {
  .nav-links { display: none; position: fixed; top: 56px; left: 0; right: 0; bottom: 0; background: rgba(20,18,16,0.98); backdrop-filter: blur(12px); flex-direction: column; padding: 8px 16px 24px; gap: 2px; overflow-y: auto; z-index: 999; }
  .nav-links.open { display: flex; }
  .nav-links a { padding: 14px 16px; font-size: 1em; min-height: 48px; display: flex; align-items: center; }
  .menu-btn { display: flex; align-items: center; justify-content: center; min-width: 44px; min-height: 44px; }
  .nav-right { gap: 6px; }
  .countdown-box { display: none; }
  .nav-right .status-badge { padding: 3px 8px; font-size: 0.7em; }
  .nav-right .auth-btn span { display: none; }
  .nav-right .auth-btn { padding: 6px 10px; min-width: 40px; justify-content: center; }
}
@media (min-width: 768px) {
  .menu-btn { display: none; }
  .nav-links { display: flex; flex-direction: row; gap: 2px; list-style: none; margin: 0; padding: 0; flex: 1; justify-content: center; }
  .nav-links a { padding: 8px 14px; font-size: 0.9em; }
  .nav-right .auth-btn { padding: 6px 16px; }
}
.nav-links .hasDropdown { position: relative; }
.dropdown-trigger {
  color: #e0d6c8; text-decoration: none; font-size: 0.9em;
  padding: 6px 14px; border-radius: 6px; cursor: pointer;
  transition: all 0.2s; white-space: nowrap; display: inline-block;
}
.dropdown-trigger:hover { color: #FF6B35; background: rgba(255,107,53,0.1); }
.dropdown-trigger.active { color: #FF6B35; background: rgba(255,107,53,0.15); }
.dropdown-menu {
  display: none; position: absolute; top: 100%; left: 0;
  background: rgba(26,22,18,0.98); border: 1px solid rgba(255,107,53,0.15);
  border-radius: 8px; padding: 6px 0; min-width: 120px;
  list-style: none; margin: 4px 0;
}
.hasDropdown:hover .dropdown-menu { display: block; }
.dropdown-menu li a {
  display: block; padding: 8px 18px; color: #c0a880;
  font-size: 0.85em; text-decoration: none; white-space: nowrap;
  transition: all 0.15s;
}
.dropdown-menu li a:hover { background: rgba(255,107,53,0.1); color: #FF6B35; }
.dropdown-menu li a.active { color: #FF6B35; }
@media (max-width: 767px) {
  .dropdown-menu { position: static; background: none; border: none; padding: 0 0 0 16px; }
  .dropdown-menu li a { padding: 10px 16px; }
}
</style>
