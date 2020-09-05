<template>
  <div class="container m-5 mx-auto w-75 font-weight-bold">
    <div class="text-center shadow border mb-5 bg-white rounded-lg m-5">
      <form>
        <p class="font-weight-bold h4 text-center my-4">Edit Review<p>
        <hr><br>
        <div class="mt-2 mb-5 w-75 mx-auto">
          <p class="align-self-center m-1 text-left">Title</p>
          <input  v-model="existingArticleData.title" id="title" type="text" class="form-control form-control-lg" placeholder="제목을 입력해 주세요."/>
        </div>
        <!-- <div class="mt-2 mb-5 w-75 mx-auto">
          <p class="align-self-center m-1 text-left">평점</p>
        </div>
        <div class="mt-2 mb-5 w-75 mx-auto">
          <p class="align-self-center m-1 text-left">Rank</p>
        </div> -->
        <div class="mt-2 mb-5 w-75 mx-auto">
          <p class="align-self-center m-1 text-left">Overview</p>
          <textarea placeholder="내용을 입력해 주세요." class="form-control form-control-lg" v-model="existingArticleData.overview" id="content" cols="30" rows="10"></textarea>
        </div>
        <div class="pb-5">
          <b-button class="font-weight-bold" variant="outline-secondary" @click="modifyArticle">Submit</b-button>
        </div>
      </form> 
    </div>
  </div>
</template>

<script>
import axios from 'axios'

// const BACK_URL = 'http://127.0.0.1:8000'
const SERVER_URL = 'http://localhost:8000'

export default {
  name: "ArticleModifyView",
  data() {
    return {
      movie_pk: this.$route.params.movie_pk,
      existingArticleData:{
        title: null,
        overview : null,
      },
      user_data:{},
    }
  },
  methods: {
    modifyArticle() {
      const config = {
        headers: {
          Authorization: `Token ${this.$cookies.get('auth-token')}`
        }
      }
      if (this.existingArticleData.content === null | this.existingArticleData.content === ''){
          this.$bvToast.toast('내용을 입력해 주세요.', {title: `ERROR`, variant: 'danger', autoHideDelay: 1000, solid: true})
      } 
      else if (this.existingArticleData.title === null | this.existingArticleData.title === ''){
        this.$bvToast.toast('제목을 입력해 주세요.', {title: `ERROR`, variant: 'danger', autoHideDelay: 1000, solid: true})
      } 
      else {
      // this.existingArticleData.user=null
        axios.post(SERVER_URL + `/movies/${this.movie_pk}/modify/`, this.existingArticleData, config)
        // console.log(this.existingArticleData)
        .then(res => { 
          console.log(res.data) 
          this.$router.push({name:'MovieDetailView', params: { movie_pk: this.movie_pk } })
        })
        .catch(error => {    
          console.error(error)
        })
      }
    },
    getArticleData(){
      const config = {
        headers: {
          Authorization: `Token ${this.$cookies.get('auth-token')}`
        }
      }
      axios.get(SERVER_URL + `/movies/${this.movie_pk}/modify/`,config)
      .then(res=>{
        console.log(res.data)
        this.existingArticleData = res.data
      })
      .catch(err=>console.error(err))
    },
    admin_check: function () {
      if (this.$cookies.isKey("username")){
        axios.get(`${SERVER_URL}/accounts/getuserdetail/${this.$cookies.get('username')}/`)
        .then(res=>{
          if (!res.data.is_superuser){
        console.log(this.user_data)
        console.log('운영자가 아님')
          this.$bvToast.toast('운영자가 아닙니다.', {title: `ERROR`, toaster:'b-toaster-top-center', variant: 'danger', autoHideDelay: 1000, solid: true})
          this.$router.push({ name: 'LoginView' })
        }
          this.user_data = res.data
          console.log(this.user_data)
        })
        .catch(err=>{
          console.log(err)
        })
      }
    },
    checkLoggedIn() {
      if (!this.$cookies.isKey('auth-token')) {
        this.$router.push({ name: 'LoginView' })
      } 
    },
    adminorLogin(){
      if (!this.userdata.is_superuser){
        // console.log('운영자가 아니다')
        this.$router.push({name:'MovieDetailView', params: { movie_pk: this.movie_pk } })
      }
    },
  },
  beforeMount(){
      this.checkLoggedIn()
      this.admin_check()  
      this.getArticleData()
      this.adminorLogin()
  },
}
</script>

<style>
#title{
  font-size: 100%;
  padding: 25px 25px;
}
</style>
