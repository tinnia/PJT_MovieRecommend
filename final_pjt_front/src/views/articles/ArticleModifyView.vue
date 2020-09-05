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
          <p class="align-self-center m-1 text-left">Content</p>
          <textarea placeholder="내용을 입력해 주세요." class="form-control form-control-lg" v-model="existingArticleData.content" id="content" cols="30" rows="10"></textarea>
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

const SERVER_URL = 'http://localhost:8000'

export default {
  name: "ArticleModifyView",
  data() {
    return {
      article_pk: this.$route.params.article_pk,
      articleData: {
        title: null,
        content: null,
      },
      existingArticleData:{
        title: null,
        content : null,
      },
    }
  },
  methods: {
    modifyArticle() {
      const config = {
        headers: {
          Authorization: `Token ${this.$cookies.get('auth-token')}`
        }
      }
      axios.post(SERVER_URL + `/articles/${this.article_pk}/modify/`, this.existingArticleData, config)
      // console.log(this.existingArticleData)
      .then(() => { 
        // console.log(res.data) 
        this.$bvToast.toast('수정이 완료되었습니다.', {title: `SUCCESS`, toaster:'b-toaster-top-center', variant: 'success', autoHideDelay: 1000, solid: true})
        this.$router.push({name:'ArticleDetailView', params: { article_pk: this.article_pk } })
      })
      .catch((error) => {    
        if (this.existingArticleData.content === null | this.existingArticleData.content === ''){
          this.$bvToast.toast('내용을 입력해 주세요.', {title: `ERROR`, toaster:'b-toaster-top-center', variant: 'danger', autoHideDelay: 1000, solid: true})
        } 
        else if (this.existingArticleData.title === null | this.existingArticleData.title === ''){
          this.$bvToast.toast('제목을 입력해 주세요.', {title: `ERROR`, toaster:'b-toaster-top-center', variant: 'danger', autoHideDelay: 1000, solid: true})
        }
        console.error(error)
      })
    },
    getArticleData(){
      const config = {
        headers: {
          Authorization: `Token ${this.$cookies.get('auth-token')}`
        }
      }
      axios.get(SERVER_URL + `/articles/${this.article_pk}/modify/`,config)
      .then(res=>{
        console.log(res.data)
        this.existingArticleData = res.data
      })
      .catch(err=>console.error(err))
    },
    checkLoggedIn() {
      if (!this.$cookies.isKey('auth-token')) {
        this.$router.push({ name: 'LoginView' })
      } 
    },
  },
  beforeMount(){
    this.checkLoggedIn()
    this.getArticleData()
  },
}
</script>

<style>
#title{
  font-size: 100%;
  padding: 25px 25px;
}
</style>
