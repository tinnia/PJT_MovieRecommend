<template>
  <div id="carouse">
    <b-carousel
      id="carousel-fade"
      v-model="slide"
      :interval="4000"
      controls
      indicators
      background="#ababab"
      img-width="1024"
      img-height="780"

      style="text-shadow: 1px 1px 2px #333;"
      @sliding-start="onSlideStart"
      @sliding-end="onSlideEnd"
    >
      

      <!-- Slide with blank fluid image to maintain slide aspect ratio -->
      <b-carousel-slide class="maincarousel" v-for="movie in rec_movies" v-show="ischecked"
        :key="movie.id"
        :img-src="giveposterURL(movie.backdrop_path)" alt="poster" 
        :img-width="1024"
        :img-height="780"
        @click.native="getArticles(movie.id)">
        <div>
          <h3>{{movie.title}}</h3>
          <p>
            {{ movie.overview.slice(0,150) }} ...
          </p>
        </div>
      </b-carousel-slide>

      <b-carousel-slide class="maincarousel" img-blank img-alt="Blank image" v-if="!ischecked & isLoggedIn">
        <p class="text-dark">
          평점을 작성하셨다면, 영화 추천을 클릭하여 자신에게 맞을지도 모르는 영화를 둘러보세요
        </p>
      </b-carousel-slide>

      <b-carousel-slide class="maincarousel" img-blank img-alt="Blank image" v-if="!ischecked & !isLoggedIn">
        <p class="text-dark">
          회원가입을 하여 더 많은 서비스를 즐기세요.
        </p>
      </b-carousel-slide>
    </b-carousel>


    <!-- 추천 알고리즘 -->
    <div class="container">
      <div class="d-flex inline mt-5" v-if="isLoggedIn">
        <b-button class="bg-transparent border-0 text-dark mt-4 ml-3 p-0"> <p id="vuecarouselfont" @click="movieRecommend" class="bg-warning m-0 text-left font-weight-bold">추천 영화 </p>
        </b-button>
        <div class="mt-1 d-flex inline" >
          <b-icon variant="danger" shift-v="-1" class="ml-2 mt-2" animation="fade" icon="cursor" rotate="-180" font-scale="1.4"></b-icon>
          <p class="text-danger font-weight-bold ml-1"> click!!</p>
        </div>
      </div>
      <!-- <div v-if="ischecked" class="p-0 mt-3 mb-5">
        <vueper-slides 
          class="mx-4" 
          :visible-slides="5"
          slide-multiple
          :gap="1"
          :slide-ratio="1 / 3.5"
          :dragging-distance="100"
          :breakpoints="{ 800: { visibleSlides: 3, slideMultiple: 2 },}">
          <vueper-slide class="shadow" v-for="item in rec_movies" :key="item.id" :image="giveposterURL(item.poster_path)" alt="poster" @click.native="getArticles(item.id)" />
        </vueper-slides>
      </div> -->

      
      <p id="vuecarouselfont" class="mt-5 mx-3 text-left font-weight-bold">최근에 나온 영화</p>
      <div class="p-0 mb-5">
        <vueper-slides 
          class="mx-4" 
          :visible-slides="5"
          slide-multiple
          :gap="1"
          :slide-ratio="1 / 3.5"
          :dragging-distance="100"
          :breakpoints="{ 800: { visibleSlides: 3, slideMultiple: 2 },}">
          <vueper-slide class="shadow" v-for="item in datemovies" :key="item.id" :image="giveposterURL(item.poster_path)" alt="poster" @click.native="getArticles(item.id)" />
        </vueper-slides>
      </div>

      <p id="vuecarouselfont" class="mt-5 mx-3 text-left font-weight-bold">인기있는 영화</p>
      <div class="p-0 mb-5">
        <vueper-slides 
          class="mx-4" 
          :visible-slides="5"
          slide-multiple
          :gap="1"
          :slide-ratio="1 / 3.5"
          :dragging-distance="100"
          :breakpoints="{ 800: { visibleSlides: 3, slideMultiple: 2 },}">
          <vueper-slide class="shadow" v-for="item in popularitymovies" :key="item.id" :image="giveposterURL(item.poster_path)" alt="poster" @click.native="getArticles(item.id)" />
        </vueper-slides>
      </div>

      <p id="vuecarouselfont" class="mt-5 mx-3 text-left font-weight-bold">추천수가 많은 영화</p>
      <div class="p-0 mb-5">
        <vueper-slides 
          class="mx-4" 
          :visible-slides="5"
          slide-multiple
          :gap="1"
          :slide-ratio="1 / 3.5"
          :dragging-distance="100"
          :breakpoints="{ 800: { visibleSlides: 3, slideMultiple: 2 },}">
          <vueper-slide class="shadow" v-for="item in votemovies" :key="item.id" :image="giveposterURL(item.poster_path)" alt="poster" @click.native="getArticles(item.id)" />
        </vueper-slides>
      </div>
    </div>

  </div>
</template>

<script>
import axios from 'axios'
import { VueperSlides, VueperSlide } from 'vueperslides'
import 'vueperslides/dist/vueperslides.css'

const SERVER_URL = 'http://localhost:8000'

export default {
  name: 'Home',
  data() {
    return {
      slide: 0,
      sliding: null,
      real_date :0,
      ischecked:false,
      user_data:[],
      rec_movies:[],
      datemovies:[],
      votemovies:[],
      popularitymovies:[],
      isLoggedIn:false,
    }
  },
  components: {
    VueperSlides, VueperSlide
  },
  methods: {
    giveposterURL(url){
      return `https://image.tmdb.org/t/p/w780/${url}`
    },
    givemainposterURL(url){
      return `https://image.tmdb.org/t/p/w780/${url}`
    },
    dateMovies() {
      axios.get(SERVER_URL + '/movies/')
      .then(res=>{
        this.movies = res.data
        this.movies.sort((a,b)=>b.release_date.replace(/-/g,'') - a.release_date.replace(/-/g,'') )
        this.datemovies = this.movies.slice(0,10)
        // console.log(this.datemovies)
      })
      .catch(err => console.log(err))
    },
    popularityMovies() {
      axios.get(SERVER_URL + '/movies/')
      .then(res=>{
        this.movies = res.data  
        this.movies.sort((a,b)=>b.popularity - a.popularity)
        this.popularitymovies = this.movies.slice(0,10)
        // console.log(this.popularitymovies)
      })
      .catch(err => console.log(err))
    },
    voteMovies() {
      axios.get(SERVER_URL + '/movies/')
      .then(res=>{
        this.movies = res.data  
        this.movies.sort((a,b)=>b.vote_count - a.vote_count)
        this.votemovies = this.movies.slice(0,10)
        // console.log(this.votemovies)
      })
      .catch(err => console.log(err))
    },
    movieRecommend(){
      const config = {
        headers: {
          Authorization: `Token ${this.$cookies.get('auth-token')}`
        }
      }
      axios.get(`${SERVER_URL}/movies/${this.user_data.username}/recommends/`,config)
      .then(res=>{
        console.log(res.data)
        this.rec_movies = res.data 
        if (this.ischecked){
          this.ischecked = false
        }
        else{
          this.ischecked = true
        }
        console.log(this.rec_movies)
      })
      .catch(() => {
        this.$bvToast.toast('로그인 해주세요. 만약 로그인을 했다면, 영화의 평점을 등록해주세요.', {title: `ERROR`, toaster:'b-toaster-top-center', variant: 'danger', autoHideDelay: 1000, solid: true})
        
      })
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
    // rateMovies() {
    //   axios.get(SERVER_URL + '/movies/')
    //   .then(res=>{
    //     this.movies = res.data  
    //     this.movies.sort(function(a,b) {
    //       if (b.vote_average === a.vote_average){
    //         var x = a.vote_count, y= b.vote_count;
    //         return x>y?-1:x<y?1:0;
    //       }
    //       return b.vote_average - a.vote_average;
    //     });
    //     this.ratemovies = this.movies.slice(0,10)
    //     // console.log(this.ratemovies)
    //   })
    //   .catch(err => console.log(err))
    // },
    getArticles(movie_pk){
      this.$router.push({name:'MovieDetailView', params: { movie_pk: movie_pk } })
    },
    onSlideStart() {
      this.sliding = true
    },
    onSlideEnd() {
      this.sliding = false
    },
    checkLogin : function() {
      if(this.$cookies.isKey('auth-token')){
        this.isLoggedIn=true
      }else{
        this.isLoggedIn=false
      }
    },
  },
  mounted(){
    this.popularityMovies()
    this.dateMovies()
    this.voteMovies()
    // this.movieRecommend()
    // this.rateMovies()
  },
  created(){
    this.admin_check()
    this.checkLogin()
  }
}
</script>

<style>
#vuecarouselfont{
  font-size:1vw;
}
#carousel-fade{
  height:240;
}
.maincarousel{
  width:1024px;
  height:480px;

}
</style>