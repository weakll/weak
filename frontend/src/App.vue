<script setup>
import NavBar from './components/NavBar.vue'
import FooterBar from './components/FooterBar.vue'
import FloatingButton from './components/FloatingButton.vue'
import AuthModal from './components/AuthModal.vue'
import { useAuth } from './composables/useAuth.js'

const { init } = useAuth()
init()
</script>

<template>
  <NavBar />
  <router-view />
  <FooterBar />
  <FloatingButton />
  <AuthModal />
</template>
