<template>
    <div class="container m-5 mx-auto w-75">
        <div class="card shadow p-3">
            <div class="card-body">
                <div class="row d-flex">
                    <div class="col-lg-2 col-md-3 col-sm-4 pb-5 col-xs-4 d-flex align-items-center justify-content-center">
                        <b-avatar size="7rem"></b-avatar>
                    </div>
                    <div class="col-lg-10 col-md-9 col-sm-7 col-xs-6">
                        <h3 class="pl-3 text-left font-weight-bold">My Profile</h3>
                        <hr>
                        <div class="card-body">
                            <div class="d-flex flex-column p-0">
                                <div class="float-left">
                                    <p class="float-left font-weight-bold pr-3">Username :</p>
                                    <div class="float-left">
                                        <p class="pr-3"> {{userdata.username }} </p>
                                    </div>
                                </div>
    
                                <div class="float-left">
                                    <p class="float-left font-weight-bold pr-3">Class :</p>
                                    <div class="float-left">
                                        <p class="float-left pr-3" v-if="userdata.is_superuser">Manager</p>
                                        <p class="float-left pr-3" v-if="!userdata.is_superuser">User</p>
                                    </div>
                                </div>
                                <div class="float-left">
                                    <p class="float-left font-weight-bold">성향 : </p>
                                    <p class="float-left px-3 my-0 text-warning">{{ userdata.karma }}</p>
                                    <br>
                                    <b-icon class="float-left font-weight-bold mt-3" @click="getKarma(userdata.username)" icon="award" variant="warning" aria-hidden="true" font-scale="1.5"></b-icon>             
                                    <div class="float-left">
                                        <!-- <p class="float-left px-3 text-secondary"  v-if="!isit">글을 작성한 적이 있다면, 아이콘을 눌러서 내 성향을 확인하세요.</p> -->
                                        <p class="p-3 font-weight-bold text-secondary text-left">글을 작성한 적이 있다면, 왼쪽 아이콘을 눌러보세요.</p>
                                    </div>
                                </div>
                                
                                 <!-- <b-button variant="outline-primary" @click="getKarma(userdata.username)">내 성향은?</b-button> -->
                            </div>
                        </div>
                    </div>
                        <!-- <img :src="giveposterURL(movie.poster_path)" alt="profile" class="h-100 float-right col-4 p-0" /> -->
                </div>
            </div>
        </div>
        <div class="card shadow p-3 mt-3">
            <div class="card-body">
                <div class="row">
                    <div class="col-8 col-md-6 col-sm-4">
                        <h4 class="text-left font-weight-bold">Written Rates</h4>
                    </div>
                </div>
                <hr>
                <div class="card-body text-left p-0" v-if="rates.length==0">
                <p class="p-3 font-weight-bold text-secondary text-left">작성한 영화 평가가 없습니다.</p>
                </div>
                <div class="text-left movie-title" v-for="rate in rates" :key="rate.id" >
                    <div class="row">
                        <p @click='gotoMovies(rate.movie.id)' id="movietitle" class="col-xs-4 col-sm-8 col-lg-10 m-0 mt-1 float-left font-weight-bold pr-3">{{ rate.movie.title }}</p>
                        <b-form-rating id="rating-sm-no-border" variant="warning" class="col-lg-2 col-md-3 float-right w-25 px-3" readonly :value="rate.score/2" no-border size="sm"></b-form-rating>
                    </div>
                    <p >{{ rate.content }}</p>
                    <hr>
                </div>
            </div>
        </div>
        <div class="card shadow p-3 mt-3">
            <div class="card-body">
                <div class="row">
                        <h4 class="text-left font-weight-bold">Written Articles</h4>
                    <div class="col-8 col-md-6 col-sm-4">
                    </div>
                </div>
                <hr>
                <div class="card-body text-left p-0" v-if="articles.length==0">
                <p class="p-3 font-weight-bold text-secondary text-left">작성한 글이 없습니다.</p>
                </div>
                <div class="text-left movie-title" v-for="article in articles" :key="article.id" >
                    <div class="row targetArticle" @click='gotoArticles(comment.article.id)'>
                        <p  id="articletitle" class="col-xs-4 col-sm-8 col-lg-10 m-0 mt-1 float-left font-weight-bold pr-3">{{ article.title }}</p>
                    </div>
                    <p >{{ article.content }}</p>
                    <hr>
                </div>
            </div>
        </div>
        <div class="card shadow p-3 mt-3">
            <div class="card-body">
                <div class="row">
                        <h4 class="text-left font-weight-bold">Written Comments</h4>
                    <div class="col-8 col-md-6 col-sm-4">
                    </div>
                </div>
                <hr>
                <div class="card-body text-left p-0" v-if="comments.length==0">
                <p class="p-3 font-weight-bold text-secondary text-left">작성한 댓글이 없습니다.</p>
                </div>
                <div class="text-left movie-title" v-for="comment in comments" :key="comment.id" >
                    <div class="row" @click='gotoArticles(comment.article.id)'>
                        <p  id="commenttitle" class="col-xs-4 col-sm-8 col-lg-10 m-0 mt-1 float-left font-weight-bold pr-3">{{ comment.article.title }}</p>
                    </div>
                    <p >{{ comment.content }}</p>
                    <hr>
                </div>
            </div>
        </div>
        
    </div>
</template>

<script>
import axios from 'axios'

// const SERVER_URL = "http://localhost:8000"
const BACK_URL = 'http://127.0.0.1:8000'

export default {
    name: 'profile',
    data () {
        return {
            username: this.$route.params.username,
            userdata:[],
            rates:[],
            articles:[],
            comments:[],
            // isit:false,
        }
    },
    methods: {
        checkLoggedIn() {
            if (!this.$cookies.isKey('auth-token')) {
                this.$router.push({ name: 'LoginView' })
            } 
        },
        admin_check : function(){
            if (this.$cookies.isKey("username")){
                axios.get(`${BACK_URL}/accounts/getuserdetail/${this.$cookies.get('username')}/`)
                .then(res=>{
                    this.userdata = res.data
                    console.log(this.userdata)
                })
                .catch(err=>{console.log(err)})
            } 
        },
        getRates : function(){
            if (this.$cookies.isKey("username")){
                axios.get(`${BACK_URL}/movies/${this.$cookies.get('username')}/rates/`)
                .then(res=>{
                    this.rates = res.data
                    console.log(this.rates)
                })
                .catch(err=>{console.log(err)})
            }
        },
        getArticles : function(){
            if (this.$cookies.isKey("username")){
                axios.get(`${BACK_URL}/articles/${this.$cookies.get('username')}/articles/`)
                .then(res=>{
                    this.articles = res.data
                })
                .catch(err=>{console.log(err)})
            }
        },
        getComments : function(){
            if (this.$cookies.isKey("username")){
                axios.get(`${BACK_URL}/articles/${this.$cookies.get('username')}/comments/`)
                .then(res=>{
                    this.comments = res.data
                })
                .catch(err=>{console.log(err)})
            }
        },
        gotoMovies (moviePk){
            this.$router.push({name:'MovieDetailView', params: { movie_pk: moviePk } })
        },
        gotoArticles : function(article_pk){
      this.$router.push({name:'ArticleDetailView', params: { article_pk: article_pk } })
        },

        getKarma(user_name){
            const config = {
                headers: {
          Authorization: `Token ${this.$cookies.get('auth-token')}`
                }
            }
            axios.post(`${BACK_URL}/accounts/karma/${user_name}/`,null,config)
            .then(res=>{
                console.log(res)
                this.$router.go()
                // this.isit = true
                
            })
            .catch(err=>{
                console.log(err)
            })
        },
    },
    beforeMount(){
        this.checkLoggedIn()
        this.admin_check()
        this.getRates()
        this.getArticles()
        this.getComments()
    }
}
</script>

<style>
.movie-title:hover{
    background:#aaaaaa;
    color:white;
}

</style>