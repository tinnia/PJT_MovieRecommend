<template>
  <div class="container m-5 mx-auto w-75 font-weight-bold">
    
    <div class="text-center shadow border mb-5 bg-white rounded-lg m-5">
      <form>
        <p class="font-weight-bold h4 text-center my-4">Create Movie<p>
        <hr><br>
        <div class="mt-2 mb-5 w-75 mx-auto">
          <p class="align-self-center m-1 text-left">Title</p>
          <input  v-model="articleData.title" id="title" type="text" class="form-control form-control-lg" placeholder="제목을 입력해 주세요."/>
        </div>
        <!-- <div class="mt-2 mb-5 w-75 mx-auto">
          <p class="align-self-center m-1 text-left">평점</p>
        </div>
        <div class="mt-2 mb-5 w-75 mx-auto">
          <p class="align-self-center m-1 text-left">Rank</p>
        </div> -->
        <div class="mt-2 mb-5 w-75 mx-auto">
          <p class="align-self-center m-1 text-left">Overview</p>
          <textarea placeholder="내용을 입력해 주세요." class="form-control form-control-lg" v-model="articleData.overview" id="content" cols="30" rows="10"></textarea>
        </div>
        <div class="pb-5">
          <b-button class="font-weight-bold" variant="outline-secondary" @click="createArticle">Submit</b-button>
        </div>
      </form> 
    </div>
  </div>
</template>

<script>
import axios from 'axios'

const SERVER_URL = 'http://localhost:8000'
// const BACK_URL = 'http://127.0.0.1:8000'

export default {
  name: "MovieCreateView",
  data() {
    return {
      articleData: {
        title: null,
        content: null,
      },
      user_data:{},
    }
  },
  methods: {
    createArticle() {
      const config = {
        headers: {
          Authorization: `Token ${this.$cookies.get('auth-token')}`
        }
      }
      this.articleData.genres=[]
      this.articleData.vote_count=0
      this.articleData.vote_average=0
      this.articleData.release_date='2000-01-01'
      this.articleData.popularity=0
      this.articleData.poster_path='none'
      this.articleData.backdrop_path='none'
      this.articleData.original_title = 'none'
      this.articleData.original_language='none'

      axios.post(SERVER_URL + '/movies/create/', this.articleData, config)
      .then(() => { 
        // console.log(res.data) 
        this.$bvToast.toast('새로운 글이 작성되었습니다.', {title: `SUCCESS`, toaster:'b-toaster-top-center', variant: 'success', autoHideDelay: 1000, solid: true})
        this.$router.push({ name: 'MovieListView' })
      })
      .catch(error => {
        if (this.articleData.content === null | this.articleData.content === ''){
          this.$bvToast.toast('내용을 입력해 주세요.', {title: `ERROR`, toaster:'b-toaster-top-center', variant: 'danger', autoHideDelay: 1000, solid: true})
        } 
        else if (this.articleData.title === null | this.articleData.title === ''){
          this.$bvToast.toast('제목을 입력해 주세요.', {title: `ERROR`, toaster:'b-toaster-top-center', variant: 'danger', autoHideDelay: 1000, solid: true})
        } 
        else {
          this.$bvToast.toast('다시 한 번 확인해 주세요.', {title: `ERROR`, toaster:'b-toaster-top-center', variant: 'danger', autoHideDelay: 1000, solid: true})
        }
        console.log(error.response.data)
      })
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
        this.$router.push({name:'MovieListView' })
      }
    },
  },
  beforeMount(){
    this.checkLoggedIn()
    this.admin_check()  
    // this.adminorLogin()
  },
}
</script>

<style>
#title{
  font-size: 100%;
  padding: 25px 25px;
}
</style>
