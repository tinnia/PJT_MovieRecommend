<template>
  <div>
    <h1>테스트 전용 페이지</h1>
    <hr>
    <!-- <select v-model="searchType">
        <option disabled value="">Please select one</option>
        <option>d</option>
        <option>n</option>
        <option>p</option>
        <option>r</option>
        <option>s</option>
    </select>
    <hr>
    <input  v-model="pageData" type="text"  placeholder="페이지를 입력해 주세요."/>
    <button @click="getsplitMovie">페이지</button>
    <br>
    <input  v-model="keywordData" type="text"  placeholder="영화 제목을 입력해 주세요."/>
    <button @click="movieSearch">검색</button>
    <br> -->
    <button @click="movieRecommend">추천영화</button>


    <b-card-group deck class="mb-2 p-0 border-0 col-xm-12 col-md-6 col-lg-3 card-deck" v-for="movie in rec_movies" :key="movie.id" >
        <b-card no-body overlay :ref="movie.id"  @mouseover="mouseOver(movie.id)" v-show="!active" class="bcard card m-2 border-0 text-center review-card" style="box-shadow: 0px 2px 4px 0px rgba(0,0,0,0.5); object-fit: cover;" @click="getArticles(movie.id)">
          <img :src="giveposterURL(movie.poster_path)" style="border-radius:0; height:100%; overflow:hidden; object-fit: cover;" alt="movie poster" class="border-0 card-img">
        </b-card>
        <b-card no-body overlay :ref="movie.id"  @mouseout="mouseOut" v-show="active" id="hoverimg" class="bcard card m-2 border-0 text-center review-card" style="box-shadow: 0px 2px 4px 0px rgba(0,0,0,0.5); object-fit: cover;" @click="getArticles(movie.id)">
          <img id="hoverImg" :src="giveposterURL(movie.poster_path)" style="border-radius:0; height:100%; overflow:hidden; object-fit: cover;" alt="movie poster" class="border-0 card-img">
          <div class="after" v-if="movie.id === moviePk">
            <p class="px-3 pt-5 pb-0 font-weight-bolder">{{movie.title}}</p>
            <div class="text-center pt-4">
              <p class="font-weight-bold text-warning">관람평 : {{fixedNum(movie.vote_average)}}</p>
            </div>
            <div class="cardgenre2 px-3 pr-3 pb-4">
              <b-badge pill variant="warning" class="font-weight-bold float-left m-2" v-for="genre in movie.genres" :key="genre.name">
                {{ genre.name }}  
              </b-badge>
            </div>
          </div>
        </b-card>
      </b-card-group>

  </div>
</template>

<script>
import axios from "axios"

const SERVER_URL = "http://localhost:8000";

export default {
  name:"AdminView",
  data : function () {
    return{
      users:[],
      // superusers:[],
      // nosuperusers:[],
      // noactiveusers:[],
      user_data:[],
      tick:'',
      pageData:1,
      movies:[],
      // active:false,
      moviePk:0,
      // keywordData:'',
      // searchType:'d',
      rec_movies:[],
      rec_movies_tmp:[],
    }
  },
  methods:{
    checkLoggedIn() {
      if (!this.$cookies.isKey('auth-token')) {
        this.$router.push({ name: 'LoginView' })
      } 
    },
    admin_check: function () {
      if (this.$cookies.isKey("username")){
        axios.get(`${SERVER_URL}/accounts/getuserdetail/${this.$cookies.get('username')}/`)
        .then(res=>{
          this.user_data = res.data
          console.log(this.user_data)
        })
        .catch(err=>{
          console.log(err)
        })
      }
      if (this.user_data.is_superuser==false){
        console.log(this.user_data)
        console.log('운영자가 아님')
        this.$router.push({ name: 'LoginView' })
      }
    },
    movieRecommend(){
      const config = {
        headers: {
          Authorization: `Token ${this.$cookies.get('auth-token')}`
        }
      }
        axios.get(`${SERVER_URL}/movies/${this.user_data.username}/recommends`,config)
        .then(res=>{
          console.log(res)
            this.rec_movies = res.data

            
        })
        .catch(err=>{
          console.log(err)
        })
    },
    getsplitMovie () {
        axios.get(`${SERVER_URL}/movies/split/${this.searchType}/${this.pageData}`)
        .then(res=>{
            console.log(res)
            this.movies=res.data
        })
        .catch(err=>{
            console.error(err)
        })
    },
    movieSearch () {
        axios.get(`${SERVER_URL}/movies/search/${this.keywordData}`)
        .then(res=>{
            console.log(res)
            this.movies=res.data
        })
        .catch(err=>{
            console.error(err)
        })
    },
        mouseOver(movie_pk){
      this.active = true
      this.moviePk = movie_pk
    },
    mouseOut(){
      this.active=false
    },
    giveposterURL(url){
      return `https://image.tmdb.org/t/p/w780/${url}`
    },
    fixedNum(num){
        return num.toFixed(2);
    },
    


  },
  mounted (){
    this.checkLoggedIn()

  },
  created(){
    this.admin_check()
    // this.getsplitMovie()
  }
}
</script>

<style>
</style>