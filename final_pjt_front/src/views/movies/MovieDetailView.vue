<template>
    <div class="container m-5 mx-auto w-75">
        <div class="card shadow p-3">
            <div class="card-body">
                <div class="row">
                    <div class="col-8 col-md-6 col-sm-4">
                        <h3 class="text-left font-weight-bold">{{ movie.title }}</h3>
                        <small class="float-left">{{ movie.original_title }}, </small>
                        <small class="d-flex inline">{{release_date_cut}}</small>
                    </div>
                    <div class="ml-auto col-4 text-right mt-2">
                        <b-button size="sm" class="mr-2 font-weight-bold" variant="outline-primary" v-if="userdata.is_superuser" @click="movieModify">Edit</b-button>
                        <b-button size="sm" class="mr-2 font-weight-bold" variant="outline-danger" v-if="userdata.is_superuser" @click="movieDelete">Delete</b-button>
                        <b-button class="p-0 bg-transparent border-0" @click="goback"><b-icon icon="backspace" variant="secondary" aria-hidden="true" font-scale="1.8"></b-icon></b-button>
                    </div>
                </div>
                <hr>
                <div class="card-body row">
                    <div class="d-flex flex-column col-8 p-0">
                        <div class="float-left">
                            <p class="float-left font-weight-bold pr-3">장르</p>
                            <div class="float-left" v-for="genre in movie.genres" :key="genre.name">
                                <p class="pr-3">{{ genre.name }} </p>
                            </div>
                        </div>
                        <div class="float-left">
                            <p class="float-left font-weight-bold pr-3">개봉</p>
                            <p class="float-left">{{movie.release_date}}</p>
                        </div>
                        <div class="float-left">
                            <p class="float-left font-weight-bold pr-3">등급</p>
                            <p v-if="movie.adult" class="float-left"> 청소년 관람불가</p>
                            <p v-if="!movie.adult" class="float-left"> 청소년 관람가능</p>
                        </div>
                        <div class="d-flex float-left align-items-center">
                            <p class="float-left font-weight-bold pr-3">평점 </p>
                            <p class="float-left text-left pr-3"><small class="align-items-center"><star-rating :show-rating="true" :star-size="22" :rating="fixedNum(movie.vote_average/2)*1" :read-only="true" :increment="0.5" class="h6"></star-rating></small></p><p> | {{ movie.vote_count}}명</p>
                        </div>
                        <div class="float-left">
                            <p class="float-left font-weight-bold pr-3">줄거리 </p>
                            <p class="float-left text-left pr-3">{{ movie.overview }}</p>
                        </div>
                    </div>
                    <img :src="giveposterURL(movie.poster_path)" alt="movie poster" class="h-100 float-right col-4 p-0" />
                </div>
            </div>
        </div>
        <div class="card shadow p-3 mt-3">
            <div class="row">
                <div class="col-7">
                    <h3 class="pl-3 mt-2 text-left font-weight-bold">Rates</h3>
                </div>
                <div class="ml-auto col-4 text-right mt-2 mr-2">
                    <button class="p-0 bg-transparent border-0" @click="activateRateWindow" v-if="!activateRate & isLoggedIn"><b-icon icon="pen" variant="secondary" aria-hidden="true" font-scale="1.5"></b-icon></button>
                    <button class="p-0 bg-transparent border-0" @click="activateRateWindow" v-if="activateRate & isLoggedIn "><b-icon icon="box-arrow-left" variant="secondary" aria-hidden="true" font-scale="1.5"></b-icon></button>    
                </div>
            </div>
            <hr>
            <div class="card-body text-left p-0" v-for="rate in rates" :key="rate.id">
                <div class="px-3 pt-0 d-flex inline">
                    <small class="px-0 m-0 col-xs-4 col-sm-7"><star-rating :show-rating="false" :star-size="18" :rating="rate.score/2" :read-only="true" :increment="0.5"></star-rating></small>
                    <small class="ml-auto text-muted"><b-icon icon="person"></b-icon> {{ rate.user.username }}</small>
                </div>
                <div class="pt-0 px-3 text-secondary d-flex inline card-body text-left">    
                    <p class="pt-2 m-0 w-75">{{ rate.content }}</p>
                    <b-button class="ml-auto font-weight-bold" size="sm" variant="outline-danger" v-if="rate.user.username==userdata.username" @click="deleteRate"><small class=" font-weight-bold">Delete</small></b-button>
                </div>
                <!-- <hr class="m-0"> -->
            </div>
            <div class="card-body text-left p-0" v-if="rates.length==0">
                <p class="p-3 font-weight-bold text-secondary text-left">이 영화의 평가가 아직 없습니다.</p>
            </div>
            <div v-if="activateRate">
                <div v-if="!hasRated">
                    <hr />
                    <p class="p-3 align-self-center m-1 text-center font-weight-bold">평점</p>
                    <div @mouseleave="showCurrentRating(0)" style="display:inline-block;">
                        <star-rating :star-size="25" v-model="rateData.score" :show-rating="false" @current-rating="showCurrentRating" @rating-selected="setCurrentSelectedRating" :increment="0.5"></star-rating>
                    </div>
                    <div style="margin-top:10px;font-weight:bold;">{{currentRating/2}}</div>
                    <div class="p-3 d-flex inline">
                        <textarea type="text" v-model="rateData.content" id="content" class="w-100"   />
                        <b-button class="ml-3" variant="outline-secondary" @click="doRate"><b-icon icon="pencil"></b-icon></b-button>
                    </div>
                </div>

                <div v-if="hasRated">
                    <hr />
                    <p class="p-3 align-self-center m-1 text-center font-weight-bold">평점</p>
                    <div @mouseleave="showCurrentRating(0)" style="display:inline-block;">
                        <star-rating :star-size="25" v-model="modifyrateData.score" :show-rating="false" @current-rating="showCurrentRating" @rating-selected="setCurrentSelectedRating" :increment="0.5"></star-rating>
                    </div>
                    <div style="margin-top:10px;font-weight:bold;">{{currentRating/2}}</div>
                    <div class="p-3 d-flex inline">
                        <textarea type="text" v-model="modifyrateData.content" id="content" class="w-100"  />
                        <b-button class="ml-3" variant="outline-secondary" @click="modifyRate"><b-icon icon="pencil"></b-icon></b-button>
                    </div>
                </div>
            </div>
        
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import StarRating from 'vue-star-rating'

const SERVER_URL = 'http://localhost:8000'

const BACK_URL = 'http://127.0.0.1:8000'



export default {
    name: 'MovieDetailView',
    data() {
        return {
            movie_pk: this.$route.params.movie_pk,
            movie: {vote_average:0},
            // user: '',
            rateData: { content: null,score:null,movie:this.movie_pk,user:null, },
            modifyrateData: { content: null,score:null,movie:this.movie_pk,user:null, },
            comments:[],
            isLoggedIn:false,
            release_date_cut : '',
            userdata:[],
            rates:[],
            writtenRate:null,
            hasRated:false,
            activateRate:false,
            rating: 0,
            currentRating: 0,
            currentSelectedRating: 0,
        }
    },
    components: {
        StarRating
    },
    methods: {
        setRating: function(rating) {
            this.rating = rating*2
        },
        showCurrentRating: function(rating) {
            this.currentRating = (rating === 0) ? this.currentSelectedRating : rating*2
        },
        setCurrentSelectedRating: function(rating) {
            this.currentSelectedRating = rating*2
        },
        getArticleDetail() {
            axios.get(SERVER_URL + '/movies/' + this.movie_pk + '/')
            .then(res => {
                this.movie = res.data
                const str = res.data.release_date
                this.release_date_cut = str.substring(0,4)
                })
            .catch(err => console.log(err))
        },
        giveposterURL: function(url){
            return `https://image.tmdb.org/t/p/w780/${url}`
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
        checkLogin : function() {
            if(this.$cookies.isKey('auth-token')){
                this.isLoggedIn=true
            }
            else{
                this.isLoggedIn=false
            }
        },
        goback:function(){
            this.$router.push({ name: 'MovieListView' })
        },
        movieModify: function (){
            this.$router.push({name:'MovieModifyView', params: { movie_pk: this.movie_pk } })
            this.$bvToast.toast('수정이 완료되었습니다.', {title: `SUCCESS`, toaster:'b-toaster-top-center', variant: 'success', autoHideDelay: 1000, solid: true})
        },
        movieDelete: function (){
            const config = { headers: {
                    Authorization: `Token ${this.$cookies.get('auth-token')}`
                }}
                axios.post(SERVER_URL + `/movies/${this.movie.id}/delete/`, null, config)
                .then(() => { 
                    this.$bvToast.toast('삭제가 완료되었습니다.', {title: `SUCCESS`, toaster:'b-toaster-top-center', variant: 'success', autoHideDelay: 1000, solid: true})
                    this.$router.push({ name: 'MovieListView' })
                })
                .catch(err => console.log(err.response.data))
        },
        doRate() {
            if (this.isLoggedIn==false){
                this.$bvToast.toast('먼저 로그인 해주세요.', {title: `ERROR`, toaster:'b-toaster-top-center', variant: 'danger', autoHideDelay: 1000, solid: true})
                this.$router.push({ name: 'LoginView' })
            } 
            else{
                const config = { headers: {
                    Authorization: `Token ${this.$cookies.get('auth-token')}`
                }}
                this.rateData.movie = this.movie_pk
                this.rateData.user = this.userdata
                this.rateData.score = Number((this.rateData.score * 2).toFixed(0))
                console.log(this.rateData)
                axios.post(SERVER_URL + `/movies/${this.movie_pk}/rate/create/`, this.rateData, config)
                .then(res => { 
                    console.log(res.data) 
                    this.$bvToast.toast('평점이 등록되었습니다.', {title: `SUCCESS`, toaster:'b-toaster-top-center', variant: 'success', autoHideDelay: 1000, solid: true})
                    this.$router.go()
                })
                .catch((error)=>{
                    if (this.rateData.content === null){
                        this.$bvToast.toast('내용을 입력해 주세요.', {title: `ERROR`, toaster:'b-toaster-top-center', variant: 'danger', autoHideDelay: 1000, solid: true})
                    }
                    console.log(error.response)
                })
            }  
        },
        modifyRate() {
            if (this.isLoggedIn==false){
                this.$bvToast.toast('먼저 로그인 해주세요.', {title: `ERROR`, toaster:'b-toaster-top-center', variant: 'danger', autoHideDelay: 1000, solid: true})
                this.$router.push({ name: 'LoginView' })
            } 
            else{
                const config = { headers: {
                    Authorization: `Token ${this.$cookies.get('auth-token')}`
                }}
                this.modifyrateData.movie = this.movie_pk
                this.modifyrateData.user = this.userdata
                this.modifyrateData.score = Number((this.modifyrateData.score * 2).toFixed(0))
                axios.post(SERVER_URL + `/movies/${this.movie_pk}/rate/${this.modifyrateData.id}/modify/`, this.modifyrateData, config)
                .then(res => { 
                    console.log(res.data) 
                    this.$bvToast.toast('수정이 완료되었습니다.', {title: `SUCCESS`, toaster:'b-toaster-top-center', variant: 'success', autoHideDelay: 1000, solid: true})
                    this.$router.go()
                })
                .catch(err => console.log(err.response.data))
            }  
        },
        deleteRate(){
            if (this.isLoggedIn==false){
                this.$bvToast.toast('먼저 로그인 해주세요.', {title: `ERROR`, toaster:'b-toaster-top-center', variant: 'danger', autoHideDelay: 1000, solid: true})
                this.$router.push({ name: 'LoginView' })
            } 
            else{
                const config = { headers: {
                    Authorization: `Token ${this.$cookies.get('auth-token')}`
                }}
                axios.post(SERVER_URL + `/movies/${this.movie_pk}/rate/${this.modifyrateData.id}/delete/`, null, config)
                .then(res => { 
                    console.log(res.data) 
                    this.$bvToast.toast('삭제가 완료되었습니다.', {title: `SUCCESS`, toaster:'b-toaster-top-center', variant: 'success', autoHideDelay: 1000, solid: true})
                    this.$router.go()
                })
                .catch(err => console.log(err.response.data))
            } 
        },
        getRates() {
            axios.get(SERVER_URL + '/movies/' + this.movie_pk + '/rate/')
            .then(res => {
                this.rates = res.data
                // console.log(res.data)
                // for (var i in this.rates){
                // console.log(this.rates[i].user.id)
                // console.log(this.userdata)
                // if (this.rates[i].user.id==this.userdata.id){
                //     console.log("이미 평가했습니다.")
                //     this.hasRated=true
                //     this.writtenRate = this.rates[i].id
                //     this.modifyrateData.score = this.rates[i].score
                //     this.modifyrateData.content = this.rates[i].content
            })
            .catch(err => console.log(err))
        },
        ratecheck () {
            if(this.$cookies.isKey('auth-token')){
                axios.get(`${BACK_URL}/movies/${this.movie_pk}/ratedcheck/${this.$cookies.get('username')}/`)
                .then(res =>{
                    this.modifyrateData=res.data
                    // console.log(res.data)
                    this.hasRated = true
                })
                .catch(err=> console.log(err))
            }
        },
        activateRateWindow (){
            this.activateRate=!this.activateRate
        },
        fixedNum(num){
            return num.toFixed(2);
        },
        fixedNum2(num){
            return num.toFixed(0);
        },
    },
    mounted(){
        this.checkLogin()     
        this.getArticleDetail()
        this.getRates()
        // this.checkAlreadyRated()
        this.admin_check()
        this.ratecheck()
    },
}
</script>

<style>

.custom-text {
  font-weight: bold;
  font-size: 1.9em;
  border: 1px solid #cfcfcf;
  padding-left: 10px;
  padding-right: 10px;
  border-radius: 5px;
  color: #999;
  background: #fff;
}
</style>