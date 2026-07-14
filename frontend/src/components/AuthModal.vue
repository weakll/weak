<script setup>
import { ref, watch } from 'vue'
import { X, User, Mail, Lock, Eye, EyeOff } from '@lucide/vue'
import { useAuth } from '../composables/useAuth.js'

const { showModal, authError, authLoading, login, register, closeAuthModal } = useAuth()

const activeTab = ref('login')
const form = ref({ username: '', email: '', password: '', confirm: '' })
const showPassword = ref(false)
const localError = ref('')

const switchTab = (tab) => {
  activeTab.value = tab
  localError.value = ''
  authError.value = ''
}

const loginDisabled = ref(false)

const handleLogin = async () => {
  localError.value = ''
  if (!form.value.username.trim()) { localError.value = '请输入用户名或邮箱'; return }
  if (!form.value.password) { localError.value = '请输入密码'; return }
  login(form.value.username, form.value.password)
}

const handleRegister = async () => {
  localError.value = ''
  if (!form.value.username.trim()) { localError.value = '请输入用户名'; return }
  if (form.value.password.length < 6) { localError.value = '密码至少6位'; return }
  if (form.value.password !== form.value.confirm) { localError.value = '两次密码不一致'; return }
  register(form.value.username, form.value.email, form.value.password, form.value.confirm)
}

watch(showModal, (val) => {
  if (!val) { form.value = { username: '', email: '', password: '', confirm: '' }; localError.value = '' }
})
</script>

<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="showModal" class="modal-overlay" @click.self="closeAuthModal">
        <div class="modal-box">
          <button class="modal-close" @click="closeAuthModal"><X :size="20" /></button>

          <div class="modal-header">
            <div class="modal-logo">&#127753; 烟火美食街</div>
            <div class="modal-tabs">
              <button :class="{ active: activeTab === 'login' }" @click="switchTab('login')">登录</button>
              <button :class="{ active: activeTab === 'register' }" @click="switchTab('register')">注册</button>
            </div>
          </div>

          <div class="modal-body" v-if="activeTab === 'login'">
            <p class="modal-desc">登录后即可发表食客点评</p>
            <div class="input-group">
              <User :size="16" class="input-icon" />
              <input v-model="form.username" type="text" placeholder="用户名或邮箱" @keyup.enter="handleLogin" />
            </div>
            <div class="input-group">
              <Lock :size="16" class="input-icon" />
              <input v-model="form.password" :type="showPassword ? 'text' : 'password'" placeholder="密码" @keyup.enter="handleLogin" />
              <button class="toggle-pw" @click="showPassword = !showPassword">
                <EyeOff v-if="showPassword" :size="16" /><Eye v-else :size="16" />
              </button>
            </div>
            <p class="error-msg" v-if="localError || authError">{{ localError || authError }}</p>
            <button class="modal-btn" @click="handleLogin" :disabled="authLoading">{{ authLoading ? '登录中...' : '登 录' }}</button>
            <p class="modal-hint">还没有账号？<a @click="switchTab('register')">立即注册</a></p>
          </div>

          <div class="modal-body" v-else>
            <p class="modal-desc">注册账号，成为烟火美食街的一员</p>
            <div class="input-group">
              <User :size="16" class="input-icon" />
              <input v-model="form.username" type="text" placeholder="用户名（至少2个字符）" />
            </div>
            <div class="input-group">
              <Mail :size="16" class="input-icon" />
              <input v-model="form.email" type="email" placeholder="邮箱（选填）" />
            </div>
            <div class="input-group">
              <Lock :size="16" class="input-icon" />
              <input v-model="form.password" :type="showPassword ? 'text' : 'password'" placeholder="密码（至少6位）" />
              <button class="toggle-pw" @click="showPassword = !showPassword">
                <EyeOff v-if="showPassword" :size="16" /><Eye v-else :size="16" />
              </button>
            </div>
            <div class="input-group">
              <Lock :size="16" class="input-icon" />
              <input v-model="form.confirm" type="password" placeholder="确认密码" />
            </div>
            <p class="error-msg" v-if="localError || authError">{{ localError || authError }}</p>
            
            <button class="modal-btn" @click="handleRegister" :disabled="authLoading">{{ authLoading ? '注册中...' : '注 册' }}</button>
            <p class="modal-hint">已有账号？<a @click="switchTab('login')">立即登录</a></p>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.modal-overlay {
  position: fixed; inset: 0; z-index: 2000;
  background: rgba(0,0,0,0.7); backdrop-filter: blur(6px);
  display: flex; align-items: center; justify-content: center; padding: 20px;
}
.modal-box {
  background: #1e1a16; border: 1px solid rgba(255,107,53,0.2);
  border-radius: 16px; width: 100%; max-width: 400px;
  position: relative; overflow: hidden;
  box-shadow: 0 20px 60px rgba(0,0,0,0.5);
}
.modal-close {
  position: absolute; top: 14px; right: 14px; z-index: 1;
  background: rgba(255,255,255,0.06); border: none; color: #887766;
  border-radius: 50%; width: 32px; height: 32px;
  display: flex; align-items: center; justify-content: center; cursor: pointer;
  transition: all 0.2s;
}
.modal-close:hover { background: rgba(255,107,53,0.2); color: #FF6B35; }
.modal-header { padding: 28px 28px 0; text-align: center; }
.modal-logo { font-size: 1.1em; font-weight: 700; color: #FF6B35; margin-bottom: 20px; letter-spacing: 2px; }
.modal-tabs { display: flex; gap: 0; border-bottom: 1px solid rgba(255,255,255,0.08); }
.modal-tabs button {
  flex: 1; background: none; border: none; color: #887766;
  padding: 12px; font-size: 0.95em; cursor: pointer; transition: all 0.2s;
  border-bottom: 2px solid transparent;
}
.modal-tabs button.active { color: #FF6B35; border-bottom-color: #FF6B35; }
.modal-tabs button:hover { color: #c0a880; }

.modal-body { padding: 24px 28px 32px; }
.modal-desc { color: #a89880; font-size: 0.85em; text-align: center; margin: 0 0 20px; }

.input-group {
  display: flex; align-items: center; gap: 10px;
  background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08);
  border-radius: 10px; padding: 0 14px; margin-bottom: 12px; transition: border-color 0.2s;
}
.input-group:focus-within { border-color: rgba(255,107,53,0.4); }
.input-icon { color: #887766; flex-shrink: 0; }
.input-group input {
  flex: 1; background: none; border: none; color: #e0d6c8;
  padding: 12px 0; font-size: 0.9em; outline: none;
}
.input-group input::placeholder { color: #665544; }
.toggle-pw { background: none; border: none; color: #887766; cursor: pointer; padding: 4px; display: flex; }
.toggle-pw:hover { color: #c0a880; }

.error-msg { color: #ef4444; font-size: 0.8em; margin: 0 0 10px; text-align: center; min-height: 18px; }

.modal-btn {
  width: 100%; background: linear-gradient(135deg, #FF6B35, #f0932b);
  color: #fff; border: none; border-radius: 10px; padding: 13px;
  font-size: 0.95em; font-weight: 600; cursor: pointer; letter-spacing: 2px;
  transition: all 0.3s; box-shadow: 0 4px 16px rgba(255,107,53,0.3);
}
.modal-btn:hover { transform: translateY(-1px); box-shadow: 0 6px 24px rgba(255,107,53,0.5); }

.modal-hint { color: #887766; font-size: 0.8em; text-align: center; margin: 14px 0 0; }
.modal-hint a { color: #FF6B35; cursor: pointer; }
.modal-hint a:hover { text-decoration: underline; }

.demo-notice {
  background: rgba(255,193,7,0.1); border: 1px solid rgba(255,193,7,0.2);
  color: #c0a060; font-size: 0.72em; padding: 8px 12px; border-radius: 8px;
  margin-bottom: 14px; text-align: center; line-height: 1.5;
}

.modal-enter-active, .modal-leave-active { transition: all 0.3s ease; }
.modal-enter-from, .modal-leave-to { opacity: 0; }
.modal-enter-from .modal-box, .modal-leave-to .modal-box { transform: scale(0.95) translateY(10px); }
.modal-leave-active .modal-box, .modal-enter-active .modal-box { transition: all 0.3s ease; }
</style>