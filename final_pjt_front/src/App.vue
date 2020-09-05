<template>
  <div id="app">
    <b-navbar toggleable="lg" type="light" variant="light" class="px-auto sticky-top row shadow">
      <b-navbar-brand tag="router-link" to="/" class="col-lg-3 offset-lg-1 offset-md-4 col-md-5 col-sm-5 col-xs-5 font-weight-bold text-monospace"><b-icon icon="house-door"></b-icon> MOVIE HOUSE</b-navbar-brand>
      <b-navbar-toggle target="nav-collapse" class="ml-auto"></b-navbar-toggle>
      <b-collapse id="nav-collapse" class="col-lg-4 offset-lg-3" is-nav>
        
        <b-navbar-nav class="d-flex mx-auto">
          <!-- movie dropdown -->
          <b-nav-item-dropdown right toggle-class="text-decoration-none" no-caret>
            <template v-slot:button-content><b-icon icon="film"></b-icon><span class="text-dark"> Movie</span></template>
            <b-dropdown-item class="text-center" tag="router-link" to="/movies"><div class="d-flex justify-content-between align-items-center"><b-icon icon="list-ul"  variant="secondary" aria-hidden="true"></b-icon> MovieList</div></b-dropdown-item>
            <b-dropdown-item class="text-center" tag="router-link" to="/articles"><div class="d-flex justify-content-between align-items-center"><b-icon icon="file-richtext"  variant="secondary" aria-hidden="true"></b-icon> Review</div></b-dropdown-item>
          </b-nav-item-dropdown>

          <!-- user dropdown -->
          <b-nav-item-dropdown right toggle-class="text-decoration-none" no-caret>
            <template v-slot:button-content><b-icon icon="person-circle"></b-icon><span class="text-dark"> Accounts</span></template>
            <div v-if="!isLoggedIn" class="text-left">
              <b-dropdown-item  tag="router-link" to="/accounts/login"><div class="d-flex justify-content-between align-items-center"><b-icon icon="unlock-fill" variant="secondary" aria-hidden="true"></b-icon> Login</div></b-dropdown-item>
              <b-dropdown-item  tag="router-link" to="/accounts/signup"><div class="d-flex justify-content-between align-items-center"><b-icon icon="person-plus-fill" variant="secondary" aria-hidden="true"></b-icon> Signup</div></b-dropdown-item>
            </div>
            <div v-if="isLoggedIn" class="text-center">
              <b-dropdown-item  tag="router-link" to="/profile"><div class="d-flex justify-content-between align-items-center"><b-icon icon="person-lines-fill"  variant="secondary" aria-hidden="true"></b-icon> Profile</div></b-dropdown-item>
              <b-dropdown-item  v-if="userdata.is_superuser" tag="router-link" to="/admin"><div class="d-flex justify-content-between align-items-center"><b-icon icon="person-check-fill"  variant="secondary" aria-hidden="true"></b-icon> Admin</div></b-dropdown-item>
              <b-dropdown-item  @click="logout" tag="router-link" to="/accounts/login"><div class="d-flex justify-content-between align-items-center"><b-icon icon="lock-fill"  variant="secondary" aria-hidden="true"></b-icon> Logout</div></b-dropdown-item>
            </div>
          </b-nav-item-dropdown>
        </b-navbar-nav>
        
      </b-collapse>
    </b-navbar>
    <router-view @submit-login-data="login" @submit-signup-data="signup" />
  </div>
</template>


<script>
import axios from 'axios'

const BACK_URL = 'http://127.0.0.1:8000'


export default {
  name:'App',
  data : function () {
    return{
      isLoggedIn:false,
      user:'',
      username: this.$route.params.username,
      userdata:[],
    }
  },
  methods : {
    setCookiesAndLogin : function(key) {
      this.$cookies.set('auth-token',key)
      this.isLoggedIn = true
    },
    setCookiesUserName : function(user_name){
      this.$cookies.set("username",user_name)
      this.admin_check()
    },
    login: function(loginData) {
      axios.post(`${BACK_URL}/rest-auth/login/`, loginData)
      .then((response)=> {
        this.$router.push({ name: 'Home' })
        this.setCookiesAndLogin(response.data.key)
        this.user = loginData.username
        this.setCookiesUserName(this.user)
        this.$bvToast.toast(loginData.username+'님, 환영합니다.', {title: `WELCOME`, toaster:'b-toaster-top-center', variant: 'success', autoHideDelay: 1000, solid: true})
        this.admin_check()
      })
      .catch(error => {
        if (loginData.username === null | loginData.username === ''){
          this.$bvToast.toast('Username을 입력해 주세요.', {title: `ERROR`, toaster:'b-toaster-top-center', variant: 'danger', autoHideDelay: 1000, solid: true})
        } 
        if (loginData.password === null | loginData.password === ''){
          this.$bvToast.toast('Password를 입력해 주세요.', {title: `ERROR`, toaster:'b-toaster-top-center', variant: 'danger', autoHideDelay: 1000, solid: true})
        } 
        else {
          this.$bvToast.toast('한 번 더 확인해 주세요.', {title: `ERROR`, toaster:'b-toaster-top-center', variant: 'danger', autoHideDelay: 1000, solid: true})
        }
        console.log(error.response.data)
      })
    },
    logout : function() {
      const axiosConfig ={
        headers:{
          Authorization : `Token ${this.$cookies.get('auth-token')}`
        },
      }
      axios.post(`${BACK_URL}/rest-auth/logout/`,null,axiosConfig)
      .then(()=>{
        this.$cookies.remove('auth-token')
        this.$cookies.remove('username')
        this.isLoggedIn=false
        this.$router.push({ name: 'Home' })
      })
      .catch((error)=>{
        console.log(error.response.data)
      })
    },
    signup: function(signupData){
      axios.post(`${BACK_URL}/rest-auth/signup/`,signupData)
      .then((response)=>{
        // this.setCookiesAndLogin(response.data.key)
        console.log(response)
        // this.setCookiesUserName(this.user)
        this.$router.push({ name: 'LoginView' })
      })
      .catch((error)=>{
        if (signupData.username === null | signupData.username === ''){
          this.$bvToast.toast('Username을 입력해 주세요.', {title: `ERROR`, toaster:'b-toaster-top-center', variant: 'danger', autoHideDelay: 1000, solid: true})
        } 
        else if (signupData.password1 === null | signupData.password1 === '' | signupData.password2 === null | signupData.password2 === ''){
          this.$bvToast.toast('Password를 입력해 주세요.', {title: `ERROR`, toaster:'b-toaster-top-center', variant: 'danger', autoHideDelay: 1000, solid: true})
        } 
        else if (signupData.password1 !== signupData.password2) {
          this.$bvToast.toast("비밀번호가 일치하지 않습니다.", {title: `ERROR`, toaster:'b-toaster-top-center', variant: 'danger', autoHideDelay: 1000, solid: true})
        }
        else if (signupData.password1.length <8 | signupData.password2.length <8){
          this.$bvToast.toast(error.response.data.password1[0], {title: `ERROR`, toaster:'b-toaster-top-center', variant: 'danger', autoHideDelay: 1000, solid: true})
        }
        else {
          this.$bvToast.toast('username이 이미 존재하거나, password형식이 맞지 않습니다.', {title: `ERROR`, toaster:'b-toaster-top-center', variant: 'danger', autoHideDelay: 1000, solid: true})
        }
        console.log(error.response)
      })
    },
    admin_check : function(){
      if (this.$cookies.isKey("username")){
        axios.get(`${BACK_URL}/accounts/getuserdetail/${this.$cookies.get('username')}/`)
        .then(res=>{
          console.log(res)
          this.userdata = res.data
          console.log(this.userdata)
        })
        .catch(err=>{
          console.log(err)
        })
      }
    },
  },
  created : function() {
    if(this.$cookies.isKey('auth-token')){
      this.isLoggedIn=true
    }
    else{
      this.isLoggedIn=false
    }
  },
}
</script>


<style>
#app {
  font-family: 'Nanum Gothic Coding', monospace;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
#nav a {
  font-weight: bold;
  color: #2c3e50;
}
#nav a.router-link-exact-active {
  color: #42b983;
}
#navbar{
  background-color: rgba(0,0,0,.3);
}
/* #navbarhead{
  position: absolute;
  left: 50%;
  width: 140px;
  height: 56px;
  margin: 0 0 0 -70px;
  padding: 0;
  line-height: 56px;
} */
</style>
