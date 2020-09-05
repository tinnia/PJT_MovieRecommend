<template>
  <div class="container m-5 mx-auto w-75">
    <div class="d-flex inline py-5">
      <h2 class="ml-3 font-weight-bold">Movie List</h2>
      <div class="mx-auto">
      </div>
      <div class="d-flex inline ml-auto">
        <div class=" w-100 d-flex inline mx-auto border-bottom border-secondary" style="border-bottom: 4px solid;">
          <b-icon class="align-self-end mb-3 mr-2" icon="search" font-scale="1.3" variant="secondary"></b-icon>
          <input class=" border-0 pb-1" @keypress.enter="movieSearch" v-model="keywordData" type="search" placeholder="Search"/>
        </div>
        <b-button class="p-1 bg-transparent border-0 mr-3" v-if="userdata.is_superuser" @click="createMovie"><b-icon icon="pen" variant="secondary" aria-hidden="true" font-scale="2"></b-icon></b-button>
        <b-button class="mr-3 p-0 bg-transparent border-0" @click="goBack"><b-icon icon="backspace" variant="secondary" aria-hidden="true" font-scale="2"></b-icon></b-button>
      </div>
    </div>
    <b-card no-body>
      <b-tabs content-class="px-5" nav-class="text-secondary font-weight-bold " active-nav-item-class="font-weight-bold text-dark" card justified>
        <b-tab id="tabtitle" title="LIST" active @click="is_click('d')">
          <div class="row justify-content-between my-4" v-if="searchType==='d'">
            <b-card-group deck class="mb-2 p-0 border-0 col-xm-12 col-sm-6 col-md-4 col-lg-3 card-deck" v-for="movie in movies" :key="movie.id" >
              <b-card no-body overlay :ref="movie.id"  @mouseover="mouseOver(movie.id)" v-show="!active" class="bcard card m-2 border-0 text-center review-card" style="box-shadow: 0px 2px 4px 0px rgba(0,0,0,0.5); object-fit: cover;" @click="getArticles(movie.id)">
                <img :src="giveposterURL(movie.poster_path)" style="border-radius:0; height:100%; overflow:hidden; object-fit: cover;" alt="movie poster" class="border-0 card-img">
              </b-card>
              <b-card no-body overlay :ref="movie.id"  @mouseout="mouseOut" v-show="active" id="hoverimg" class="bcard card m-2 border-0 text-center review-card" style="box-shadow: 0px 2px 4px 0px rgba(0,0,0,0.5); object-fit: cover;" @click="getArticles(movie.id)">
                <img id="hoverImg" :src="giveposterURL(movie.poster_path)" style="border-radius:0; height:100%; overflow:hidden; object-fit: cover;" alt="movie poster" class="border-0 card-img">
                <div class="after px-3 text-left align-items-end" v-if="movie.id === moviePk">
                  <p class="pt-5 pb-0 font-weight-bolder">{{movie.title}}</p>
                  <p class="pt-0 font-weight-bold text-warning">관람평 : {{fixedNum(movie.vote_average)}}</p>
                  <div class="pr-3 pb-4">
                    <b-badge small pill variant="warning" class="small font-weight-bold mr-2" v-for="genre in movie.genres" :key="genre.name">
                      {{ genre.name }}
                    </b-badge>
                  </div>
                </div>
              </b-card>
            </b-card-group>
          </div>
        </b-tab>

        <b-tab title="추천순" @click="is_click('r')">
          <div class="row justify-content-between my-4" v-if="searchType=='r'">
            <b-card-group deck class="mb-2 p-0 border-0 col-xm-12 col-md-6 col-lg-3 card-deck" v-for="movie in movies" :key="movie.id" >
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
        </b-tab>

        <b-tab title="개봉순" @click="is_click('n')">
          <div class="row justify-content-between my-4" v-if="searchType=='n'">
            <b-card-group deck class="mb-2 p-0 border-0 col-xm-12 col-sm-6 col-md-4 col-lg-3 card-deck" v-for="movie in movies" :key="movie.id" >
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
        </b-tab>

        <b-tab title="인기순" @click="is_click('p')">
          <div class="row justify-content-between my-4" v-if="searchType=='p'">
            <b-card-group deck class="mb-2 p-0 border-0 col-xm-12 col-md-6 col-lg-3 card-deck" v-for="movie in movies" :key="movie.id" >
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
        </b-tab>

        <b-tab title="평점순" @click="is_click('s')">
          <div class="row justify-content-between my-4" v-if="searchType=='s'">
            <b-card-group deck class="mb-2 p-0 border-0 col-xm-12 col-md-6 col-lg-3 card-deck" v-for="movie in movies" :key="movie.id" >
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
        </b-tab>
      </b-tabs>
    </b-card>


    <nav aria-label="Page navigation example mt-3">
      <ul class="pagination mt-3 justify-content-center">
        <li class="page-item m-1"><a class=" rounded-circle page-link" aria-label="Previous" @click="changePage(1)"><span aria-hidden="true">&laquo;</span></a></li>
        <li class="page-item m-1"><a class="page-link rounded-circle"  v-if="pageVis.first" @click="changePage(currentPage-1)">{{currentPage-1}}</a></li>
        <li class="page-item m-1"><a class="page-link rounded-circle" href="#">{{currentPage}}</a></li>
        <li class="page-item m-1"><a class="page-link rounded-circle" v-if="pageVis.next" @click="changePage(currentPage+1)">{{currentPage+1}}</a></li>
        <li class="page-item m-1"><a class="page-link rounded-circle" aria-label="Next" @click="changePage(totalpage)"><span aria-hidden="true">&raquo;</span></a></li>
      </ul>
    </nav>

  </div>
</template>

<script>
import axios from 'axios'

const SERVER_URL = 'http://localhost:8000'
const BACK_URL = 'http://127.0.0.1:8000'

export default {
  name: "MovieListView",
  data() {
    return {
      active: false,
      moviePk:'',
      perPage:20,

      what:0,
      movies:[],
      userdata:[],

      currentPageIndex:0,
      currentPage:1,
      nbPages:0,
      searchType:'d',
      pageData:1,
      movieLength:500,
      totalpage:0,

      keywordData:'',

      pageVis:{
        first:false,
        prev:false,
        next:false,
        last:false,
      }
    }
  },
  computed:{
    pageCount() {
      let l = this.movieLength,
           s = this.perPage;
      // console.log( Math.floor(l / s))
      // this.totalpage = Math.floor(l / s)
      return Math.floor(l / s);
    },

        
  },
  methods:{
    is_click(res){
      this.searchType = res
      this.currentPage = 1
      this.pageCheck()
      this.getsplitMovie()
    },
    getMovieLength() {
      axios.get(SERVER_URL + '/movies/')
      .then(res=>{
        this.movieLength = res.data.length 
      })
      .catch(err => console.log(err))
    },

    getsplitMovie () {
        axios.get(`${SERVER_URL}/movies/split/${this.searchType}/${this.currentPage}`)
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
    getArticles(movie_pk){
      this.$router.push({name:'MovieDetailView', params: { movie_pk: movie_pk } })
    },
    giveposterURL(url){
      return `https://image.tmdb.org/t/p/w780/${url}`
    },
    goBack:function(){
      this.$router.push({ name: 'Home' })
    },
    createMovie(){
      this.$router.push({ name: 'MovieCreateView' })
    },
    admin_check : function(){
      if (this.$cookies.isKey("username")){
        axios.get(`${BACK_URL}/accounts/getuserdetail/${this.$cookies.get('username')}/`)
        .then(res=>{
          // console.log(res)
          this.userdata = res.data
        })
        .catch(err=>{
          console.log(err)
        })
      }
    },
    fixedNum(num){
        return num.toFixed(2);
    },
    changePage (num) {
      console.log(num)
      this.currentPage=num
      this.getsplitMovie()
      this.pageCheck()
    },
    gettotalpages(){
      let l = this.movieLength,
           s = this.perPage;
      this.totalpage = Math.floor(l / s)
    },
    pageCheck() {
      console.log(this.currentPage)
      if (this.currentPage<=1){
        this.pageVis.first=false
        this.pageVis.prev=false
      } else {
        this.pageVis.first=true
        this.pageVis.prev=true
      }

      if (this.currentPage>=this.totalpage){
        this.pageVis.next=false
        this.pageVis.last=false
      } else {
        this.pageVis.next=true
        this.pageVis.last=true
      } 

      
    },
    
  },
  mounted(){
    this.admin_check()
    this.getsplitMovie()
    this.getMovieLength()
    // this.test()
    this.gettotalpages()
    this.pageCheck()
  },
}
</script>

<style>
.card-body{
  padding: 0;
}
#hoverImg{
  position:relative
}
#hoverimg .after{
  font-family: 'Do Hyeon', sans-serif; 
  font-weight: bold;
  color:white;
  width:100%;
  height:100%;
  position:absolute;
  background-color:rgba(0, 0, 0, 0.74);
  padding: 10px;
}
.cardgenre2{
  color:white;
  position: absolute;;
  bottom: 0px;
  padding:10px 0 0 0;
}

.pagenum:hover{
    background:black;
    color:white
    /* color:grey; */
}

.currentnum{
  color:white;
}

.DIYPage{
  background:grey;
  font-size:18px;

}
.nav-tabs .nav-link, {
  color:darkgray !important;
  font-weight:bold !important;
}
.nav-tabs .nav-link.active,{
  color:black !important;
}

</style>