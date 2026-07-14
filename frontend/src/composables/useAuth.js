import { ref, computed } from 'vue'

function getCsrfToken() {
  const match = document.cookie.match(/csrftoken=([^;]+)/)
  return match ? match[1] : ''
}

const currentUser = ref(null)
const showModal = ref(false)
const authError = ref('')
const authLoading = ref(false)

let initialized = false

const api = {
  async request(method, url, data = null) {
    const opts = {
      method,
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken(),
      },
      credentials: 'include',
    }
    if (data) opts.body = JSON.stringify(data)
    const res = await fetch('/api/auth' + url, opts)
    const json = await res.json()
    if (!res.ok) throw new Error(json.error || '请求失败')
    return json
  },
  register(username, email, password) {
    return this.request('POST', '/register/', { username, email, password })
  },
  login(username, password) {
    return this.request('POST', '/login/', { username, password })
  },
  logout() {
    return this.request('POST', '/logout/')
  },
  me() {
    return this.request('GET', '/me/')
  }
}

export function useAuth() {
  const isLoggedIn = computed(() => !!currentUser.value)

  const init = async () => {
    if (initialized) return
    initialized = true
    authLoading.value = true
    try {
      const user = await api.me()
      currentUser.value = user
    } catch {
      currentUser.value = null
    } finally {
      authLoading.value = false
    }
  }

  const login = async (username, password) => {
    authError.value = ''
    authLoading.value = true
    try {
      const user = await api.login(username, password)
      currentUser.value = user
      showModal.value = false
      return true
    } catch (e) {
      authError.value = e.message
      return false
    } finally {
      authLoading.value = false
    }
  }

  const register = async (username, email, password, confirmPassword) => {
    authError.value = ''
    if (!username || !username.trim()) { authError.value = '请输入用户名'; return false }
    if (username.trim().length < 2) { authError.value = '用户名至少2个字符'; return false }
    if (!password || password.length < 6) { authError.value = '密码至少6位'; return false }
    if (password !== confirmPassword) { authError.value = '两次密码不一致'; return false }

    authLoading.value = true
    try {
      const user = await api.register(username.trim(), email.trim(), password)
      currentUser.value = user
      showModal.value = false
      return true
    } catch (e) {
      authError.value = e.message
      return false
    } finally {
      authLoading.value = false
    }
  }

  const logout = async () => {
    try { await api.logout() } catch {}
    currentUser.value = null
  }

  const getUserAvatar = () => ''

  const openAuthModal = () => {
    authError.value = ''
    showModal.value = true
  }
  const closeAuthModal = () => {
    showModal.value = false
    authError.value = ''
  }

  return {
    currentUser,
    isLoggedIn,
    showModal,
    authError,
    authLoading,
    init,
    login,
    register,
    logout,
    getUserAvatar,
    openAuthModal,
    closeAuthModal,
  }
}
