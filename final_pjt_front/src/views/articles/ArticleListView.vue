<template>
  <div class="container m-5 mx-auto w-75">
    <div class="d-flex inline px-5 m-3">
      <h2 class="font-weight-bold" v-if="articleHasSelected">Review List</h2>
      <div class="ml-auto">
        <b-button class="mx-2 bg-transparent border-0" @click="goCreate"><b-icon variant="secondary" font-scale="1.8" aria-hidden="true" icon="pencil-square"></b-icon></b-button>
        <b-button class="p-0 bg-transparent border-0" @click="goBack"><b-icon icon="backspace" variant="secondary" aria-hidden="true" font-scale="1.8"></b-icon></b-button>
      </div>
    </div>
    <br>
    <div v-if="articleHasSelected" class="px-5 justify-content-center">
      <div class="card-deck px-3" v-for="article in articles" :key="`article_${article.id}`">
        <div class="card shadow m-2 text-center review-card" style="width: 18rem;" @click="getArticles(article.id)">
          <div>
            <div class="card-body row">
              <div class="col-lg-10 float-left">
                <p class="w-100 card-title p-2 text-left font-weight-bold pr-3">{{ article.title }}</p>
                <small class="text-left float-left pl-2">
                  작성 : {{article.created_at.substring(5,10) + ' ' + article.created_at.substring(11,19)}}, 
                  수정 : {{article.updated_at.substring(5,10) + ' ' + article.updated_at.substring(11,19)}} 
                </small>
              </div>
              <div class="col-lg-2 col-md-3 align-items-center">
                <p class="card-text pt-2"><b-icon icon="person"></b-icon><small class="text-muted"> {{ article.user.username }}</small></p>
                <p><b-icon icon="chat-dots"></b-icon> {{article.comments.length}}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

const SERVER_URL = "http://localhost:8000";

export default {
  name: "ArticleListView",
  data() {
    return {
      articles: [],
      articleHasSelected:true,
      selectedArticle : { user:{username:'',},},
      selectedUser:[],
      commentData: {
        content: null,
      },
      comments:[],
      counttotal: 0,
      users:[],
      isLoggedIn:false,
      create_date:'',
      update_date:'',
    }
  },
  methods: {
    countcomment(count){
      this.counttotal = count
      console.log(this.counttotal)
    },
    fetchArticles() {
      axios.get(SERVER_URL + "/articles/")
      .then(res => {
        console.log(res.data)
        this.articles = res.data
        
      })
      .catch(err => console.error(err))
      axios.get(SERVER_URL + "/accounts/users/")
      .then(res => this.users = res.data)
      .catch(err => console.error(err))
    },
    getArticles : function(article_pk){
      this.$router.push({name:'ArticleDetailView', params: { article_pk: article_pk } })
    },
    checkLogin : function() {
      if(this.$cookies.isKey('auth-token')){
        this.isLoggedIn=true
      }else{
        this.$router.push({ name: 'LoginView' })
        this.isLoggedIn=false
      }
    },
    goBack:function(){
        this.$router.push({ name: 'Home' })
    },
    goCreate:function(){
      this.$router.push({ name: 'ArticleCreateView' })
    },
    createArticle: function(){
      this.$router.push({ name: 'ArticleCreateView' })
    }
  },
  created(){
    this.fetchArticles()
    this.checkLogin()
  },
  mounted(){
    this.articleHasSelected=true
  },
}
</script>

<style>
.Article:hover{
    background-color: #eee;
    cursor : pointer;
}
div.review-card {
        display: flex;
        cursor: pointer;
    }
div.review-card:hover {
    filter: brightness(80%); 
    cursor: pointer;
}
</style>
