import { createRouter, createWebHistory } from 'vue-router'

// Lazy-loaded routes
const HomePage = () => import('../views/HomePage.vue')
const FoodMapPage = () => import('../views/FoodMapPage.vue')
const TodaySpecialPage = () => import('../views/TodaySpecialPage.vue')
const EventsPage = () => import('../views/EventsPage.vue')
const ReviewsPage = () => import('../views/ReviewsPage.vue')
const TransportPage = () => import('../views/TransportPage.vue')
const AboutPage = () => import('../views/AboutPage.vue')
const JoinUsPage = () => import('../views/JoinUsPage.vue')
const MerchantDashboard = () => import('../views/MerchantDashboard.vue')
const StorePage = () => import('../views/StorePage.vue')
const NotFound = () => import('../views/NotFound.vue')

const routes = [
  { path: '/', name: 'HomePage', component: HomePage },
  { path: '/food-map', name: 'FoodMap', component: FoodMapPage },
  { path: '/today', name: 'TodaySpecial', component: TodaySpecialPage },
  { path: '/events', name: 'Events', component: EventsPage },
  { path: '/reviews', name: 'Reviews', component: ReviewsPage },
  { path: '/transport', name: 'Transport', component: TransportPage },
  { path: '/about', name: 'About', component: AboutPage },
  { path: '/store/:slug', name: 'StoreDetail', component: StorePage },
  { path: '/join-us', name: 'JoinUs', component: JoinUsPage },
  { path: '/merchant', name: 'MerchantDashboard', component: MerchantDashboard },
  // 404 catch-all
  { path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFound },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  // Scroll to top on route change
  scrollBehavior() { return { top: 0 } },
})

export default router
