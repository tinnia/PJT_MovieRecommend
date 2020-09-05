import Vue from 'vue'
import VueRouter from 'vue-router'

import Home from '../views/Home.vue'

import LoginView from '../views/accounts/LoginView.vue'
import SignupView from '../views/accounts/SignupView.vue'
import AdminView from '../views/accounts/AdminView.vue'
import ProfileView from '../views/accounts/ProfileView.vue'
import TestView from '../views/accounts/TestView.vue'

import ArticleListView from '../views/articles/ArticleListView.vue'
import ArticleDetailView from '../views/articles/ArticleDetailView.vue'
import ArticleCreateView from '../views/articles/ArticleCreateView.vue'
import ArticleModifyView from '../views/articles/ArticleModifyView.vue'

import CommentCreate from '../views/articles/CommentCreate.vue'

import MovieListView from '../views/movies/MovieListView.vue'
import MovieCreateView from '../views/movies/MovieCreateView.vue'
import MovieDetailView from '../views/movies/MovieDetailView.vue'
import MovieModifyView from '../views/movies/MovieModifyView.vue'


Vue.use(VueRouter)
  const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/accounts/signup',
    name: 'SignupView',
    component: SignupView,
  },
  {
    path: '/accounts/login',
    name: 'LoginView',
    component: LoginView,
  },
  {
    path: '/admin',
    name: 'AdminView',
    component: AdminView,
  },
    {
    path: '/admin/test',
    name: 'TestView',
    component: TestView,
  },
  {
    path: '/profile',
    name: 'profile',
    component: ProfileView,
  },
  {
    path: '/movies',
    name: 'MovieListView',
    component: MovieListView,
  },
  {
    path: '/movies/create',
    name: 'MovieCreateView',
    component: MovieCreateView,
  },
  {
    path: '/movies/:movie_pk',
    name: 'MovieDetailView',
    component: MovieDetailView,
  },
  {
    path: '/movies/modify/:movie_pk',
    name: 'MovieModifyView',
    component: MovieModifyView,
  },
  {
    path: '/articles',
    name: 'ArticleListView',
    component: ArticleListView,
  },
  {
    path: '/articles/create',
    name: 'ArticleCreateView',
    component: ArticleCreateView,
  },
  {
    path: '/articles/modify/:article_pk',
    name: 'ArticleModifyView',
    component: ArticleModifyView,
  },
  {
    path: '/articles/:article_pk',
    name: 'ArticleDetailView',
    component: ArticleDetailView,
  },
  {
    path: '/articles/comment_create',
    name: 'CommentCreate',
    component: CommentCreate,
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
