<template>
    <div class="container m-5 mx-auto w-75">
        <div class="d-flex inline px-3">
            <h2 class="font-weight-bold">Review Detail</h2>
            <b-button class="ml-auto p-0 bg-transparent border-0" @click="goback"><b-icon icon="backspace" variant="secondary" aria-hidden="true" font-scale="1.8"></b-icon></b-button>
        </div>
        <br>
        <div class="card shadow">
            <div class="card-header font-weight-bold">
                <h5 class="float-left font-weight-bold m-2">REVIEW</h5>  
            </div>
            <div class="card-body d-flex p-4">
                <h4 class="w-100 text-left font-weight-bold">{{ article.title }}</h4>
                <small class="ml-auto"><b-icon icon="person"></b-icon> {{article.user.username}}</small>
            </div>
            <p class="w-100 px-4 text-left ">{{ article.content }}</p>
            <small class="ml-4 mb-4 mr-auto">
                작성 : {{article.created_at.substring(5,10) + ' ' + article.created_at.substring(11,19)}}
                수정 : {{article.updated_at.substring(5,10) + ' ' + article.updated_at.substring(11,19)}}
            </small>
            <div class="ml-auto">
                <b-button variant="outline-primary" v-if="userdata.username==article.user.username" @click="articleModify(article.id)">Edit</b-button>
                <b-button variant="outline-danger" class="m-3" v-if="userdata.username==article.user.username" @click="articleDelete(article.id)">Delete</b-button>
            </div>
        </div>
        <br>
        <div class="card shadow" >
            <div class="card-header font-weight-bold"><h5 class="float-left font-weight-bold m-2">COMMENTS</h5></div>
            <div class="card-body text-left p-0" v-for="comment in comments" :key="comment.content">
                <div class="p-3 d-flex inline">
                    <p class="px-2 m-0 col-xs-4 col-sm-7">{{ comment.content }}</p>
                    <small class="ml-auto text-muted"><b-icon icon="person"></b-icon> {{ comment.user.username }}</small>
                </div>
                <div class="pt-0 px-4 text-secondary d-flex inline card-body text-left">    
                    <small class="mt-auto">
                        작성 : {{changeDatedata(comment.created_at)}}, 
                        수정 : {{changeDatedata(comment.updated_at)}}
                    </small>
                    <b-button class="ml-auto" size="sm" variant="outline-danger" v-if="userdata.username==comment.user.username" @click="commentDelete(article.id,comment.id)"><small>Delete</small></b-button>
                </div>
                <hr class="m-0">
            </div>
            <div class="p-3 pb-4">
                <p class="align-self-center m-1 text-left font-weight-bold">Comments</p>
                <div class="d-flex inline">
                    <textarea type="text" v-model="commentData.content" id="content" class="w-100" />
                    <b-button class="ml-3" variant="outline-secondary" @click="createComment(user.id)"><b-icon icon="pencil"></b-icon></b-button>
                </div>
            </div>
        </div>
        <br>
    </div>
</template>

<script>
import axios from 'axios'

const SERVER_URL = 'http://localhost:8000'
const BACK_URL = 'http://127.0.0.1:8000'

export default {
    name: 'ArticleDetailView',
    data() {
        return {
            article_pk: this.$route.params.article_pk,
            article: {user:{username:'',},},
            user: '',
            commentData: { content: null, },
            comments:[],
            count : 0,
            isLoggedIn:false,
            userdata:[],
            create_date:'',
            update_date:'',
        }
    },
    methods: {
        getArticleDetail() {
            axios.get(SERVER_URL + '/articles/' + this.article_pk + '/')
            .then(res => {
                console.log(res)
                this.article = res.data
                this.user = res.data.user.username
            })
            .catch(err => console.log(err))
            
            axios.get(SERVER_URL + "/articles/" + this.article_pk+"/comments/")
            .then(res => {
                this.comments = res.data
                console.log(this.comments)
                this.count = this.comments.length
                // console.log(this.count)
                // console.log(this.article)
                // const str1 = this.comments[0].created_at
                // const str2 = this.comments[0].updated_at
                // this.create_date = str1.substring(5,10) + ' ' + str1.substring(11,19)
                // this.update_date = str2.substring(5,10) + ' ' + str2.substring(11,19)
            })
            .catch(err => console.error(err))
            this.$emit('counter',this.count)
        },
        changeDatedata(time) {
            return time.substring(5,10) + ' ' + time.substring(11,19);
        },
        createComment() {
            if (this.isLoggedIn==false){
                this.$bvToast.toast('먼저 Login 해주세요.', {title: `ERROR`, toaster:'b-toaster-top-center', variant: 'danger', autoHideDelay: 1000, solid: true})
                this.$router.push({ name: 'LoginView' })
            } 
            else{
                const config = { headers: {
                    Authorization: `Token ${this.$cookies.get('auth-token')}`
                }}
                // console.log(this.commentData)
                axios.post(SERVER_URL + `/articles/${this.article_pk}/comment_create/`, this.commentData, config)
                .then(res => { 
                    console.log(res.data) 
                    this.$router.go()
                })
                .catch(() => this.$bvToast.toast('내용을 입력해주세요.', {title: `ERROR`, toaster:'b-toaster-top-center', variant: 'danger', autoHideDelay: 1000, solid: true}))
            }  
        },
        commentDelete (article_id,comment_id){
            const config = { headers: {
                Authorization: `Token ${this.$cookies.get('auth-token')}`
            }}
            axios.post(SERVER_URL + `/articles/${article_id}/comment_delete/${comment_id}/`, null, config)
            .then(()=>{
                this.$router.go()
                this.$bvToast.toast('댓글 삭제가 완료되었습니다.', {title: `SUCCESS`, toaster:'b-toaster-top-center', variant: 'success', autoHideDelay: 1000, solid: true})
            })
            .catch(err => console.log(err))
        },
        articleModify : function(article_pk){
            this.$router.push({name:'ArticleModifyView', params: { article_pk: article_pk } })
        },
        articleDelete(article_id){
            const config = { headers: {
                Authorization: `Token ${this.$cookies.get('auth-token')}`
            }}
            axios.post(SERVER_URL + `/articles/${article_id}/delete/`, null, config)
            .then(()=>{
                this.$bvToast.toast('글 삭제가 완료되었습니다.', {title: `SUCCESS`, toaster:'b-toaster-top-center', variant: 'success', autoHideDelay: 1000, solid: true})
                this.$router.push({ name: 'ArticleListView' })
            })
            .catch(err => console.log(err))
        },
        checkLogin : function() {
            if(this.$cookies.isKey('auth-token')){
                this.isLoggedIn=true
            }
            else{
                this.isLoggedIn=false
            }
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
        goback:function(){
            this.$router.push({ name: 'ArticleListView' })
        },
    },
    created() {
        this.checkLogin()
    },
    mounted(){
        this.getArticleDetail()
        this.admin_check()
    },
}
</script>

<style>

</style>