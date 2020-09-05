<template>
  <div class="container m-5 mx-auto w-75 font-weight-bold">
    <div class="text-center shadow border mb-5 bg-white rounded-lg m-5">
      <form>
        <div class="d-flex inline">
          <p class="w-75 font-weight-bold h4 my-4 text-left ml-5 pl-5">New Review</p>
          <b-button @click="goback" class="bg-transparent border-0 p-0 my-4 ml-auto mr-4">
            <b-icon variant="secondary" icon="x-square"></b-icon>
          </b-button>
        </div>
        <hr class="mt-0"><br>
        <div class="mt-2 mb-5 w-75 mx-auto">
          <p class="align-self-center m-1 text-left">Title</p>
          <input v-model="articleData.title" id="title" type="text" class="form-control form-control-lg" placeholder="제목을 입력해 주세요."/>
        </div>
        <!-- <div class="mt-2 mb-5 w-75 mx-auto">
          <p class="align-self-center m-1 text-left">평점</p>
        </div>
        <div class="mt-2 mb-5 w-75 mx-auto">
          <p class="align-self-center m-1 text-left">Rank</p>
        </div> -->
        <div class="mt-2 mb-5 w-75 mx-auto">
          <p class="align-self-center m-1 text-left">Content</p>
          <textarea placeholder="내용을 입력해 주세요." class="form-control form-control-lg" v-model="articleData.content" id="content" cols="30" rows="10"></textarea>
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

export default {
  name: "ArticleCreateView",
  data() {
    return {
      articleData: {
        title: null,
        content: null,
      }
    }
  },
  methods: {
    createArticle() {
      const config = {
        headers: {
          Authorization: `Token ${this.$cookies.get('auth-token')}`
        }
      }
      axios.post(SERVER_URL + '/articles/create/', this.articleData, config)
      .then(res => { 
        console.log(res.data) 
        this.$router.push({ name: 'ArticleListView' })
        this.$bvToast.toast('글 작성을 완료하였습니다.', {title: `SUCCESS`, toaster:'b-toaster-top-center', variant: 'success', autoHideDelay: 1000, solid: true}) 
      })
      .catch(error => {
        if (this.articleData.content === null | this.articleData.content === ''){
          this.$bvToast.toast('내용을 입력해 주세요.', {title: `ERROR`, toaster:'b-toaster-top-center', variant: 'danger', autoHideDelay: 1000, solid: true})} 
        else if (this.articleData.title === null | this.articleData.title === ''){
          this.$bvToast.toast('제목을 입력해 주세요.', {title: `ERROR`, toaster:'b-toaster-top-center', variant: 'danger', autoHideDelay: 1000, solid: true})
        } 
        // else {
        //   this.$message.error("다시 한 번 확인해 주세요.", {duration: 3000,})
        // }
        console.log(error.response.data)
      })
    },
    checkLoggedIn() {
      if (!this.$cookies.isKey('auth-token')) {
        this.$router.push({ name: 'LoginView' })
      } 
    },
    goback:function(){
      this.$router.push({ name: 'ArticleListView' })
    },
  },
  beforeMount(){
    this.checkLoggedIn()
  },
}
</script>

<style>
#title{
  font-size: 100%;
  padding: 25px 25px;
}
</style>
