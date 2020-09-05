<template>
  <div class="container m-5 mx-auto w-75">
    <p class="font-weight-bold h4 text-left my-4">Manager</p>
    <div class="row">
      <div class="border rounded py-3 text-center col-xs-12 col-lg-2 col-sm-4 mb-3 mx-2 col-md-3" v-for="superuser in superusers" :key="superuser.id">
        <b-avatar badge-variant="danger"><template v-slot:badge><b-icon icon="award" variant="white" class="font-text-bold"></b-icon></template></b-avatar>
        <p class="m-2">{{ superuser.username }}</p>
        <b-icon icon="award" variant="warning"></b-icon>
      </div>
    </div>
    <br>
    <p class="font-weight-bold h4 text-left my-4">Members</p>
    <div class="row">
      <div class="border rounded py-3 text-center col-xs-6 col-lg-2 col-sm-4 mb-3 mx-2 col-md-3" v-for="nosuperuser in nosuperusers" :key="nosuperuser.id">
        <b-icon icon="person-circle" font-scale="1.5"></b-icon>
        <p class="m-2">{{ nosuperuser.username }}</p>
        <b-button variant="outline-secondary" class="mx-auto w-25 border rounded p-1" @click="disableUser(nosuperuser.id)" :style="tick">
          <small v-if='nosuperuser.is_active'><b-icon icon="emoji-frown"></b-icon></small>
        </b-button>
      </div>
    </div>
    <br>
    <p class="font-weight-bold h4 text-left my-4 text-black-50">Inactive Members</p>
    <div class="row">
      <div class="border rounded py-3 text-center col-xs-12 col-lg-2 col-sm-4 mb-3 mx-2 col-md-3" v-for="noactiveuser in noactiveusers" :key="noactiveuser.id">
        <b-icon icon="person-circle" class="text-black-50" font-scale="1.5"></b-icon>
        <p class="m-2">{{ noactiveuser.username }}</p>
        <b-button variant="outline-secondary" class="mx-auto w-25 border rounded p-1" @click="disableUser(noactiveuser.id)" :style="tick">
          <small v-if="!noactiveuser.is_active"><b-icon icon="emoji-smile"></b-icon></small>
        </b-button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios"

const SERVER_URL = "http://localhost:8000";

export default {
  name:"AdminView",
  data : function () {
    return{
      users:[],
      superusers:[],
      nosuperusers:[],
      noactiveusers:[],
      user_data:[],
      tick:'',
    }
  },
  methods:{
    checkLoggedIn() {
      if (!this.$cookies.isKey('auth-token')) {
        this.$router.push({ name: 'LoginView' })
      } 
    },
    getUsers() {
      axios.get(SERVER_URL + "/accounts/users/")
      .then(res => {
        this.users = res.data
        for (let i = 0; i < this.users.length ; i++) {
          if (this.users[i].is_superuser){
            this.superusers.push(this.users[i])
          }
          else if (!this.users[i].is_superuser & this.users[i].is_active){
            this.nosuperusers.push(this.users[i])
          }
          else if (!this.users[i].is_superuser & !this.users[i].is_active){
            this.noactiveusers.push(this.users[i])
          }
        }
      })
      .catch(err => console.error(err))
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
      // if (!this.user_data.is_superuser){
      //   console.log(this.user_data)
      //   console.log('운영자가 아님')
      //   this.$bvToast.toast('운영자가 아닙니다.', {title: `ERROR`, toaster:'b-toaster-top-center', variant: 'danger', autoHideDelay: 1000, solid: true})
      //   this.$router.push({ name: 'LoginView' })
      // }
    },
    disableUser : function(user_id) {
      const config = {
        headers: {
          Authorization: `Token ${this.$cookies.get('auth-token')}`
        }
      }
      axios.post(SERVER_URL + '/accounts/disable/' + user_id +'/' ,null, config)    
      .then(res=>{
        this.$bvToast.toast('해당 회원의 정보가 변경되었습니다.', {title: `Success`, toaster:'b-toaster-top-center', variant: 'success', autoHideDelay: 1000, solid: true})
        console.log(res)
        this.tick=' '
        this.$router.go()
      })
      .catch(err => console.error(err))
    },
  },
  mounted (){
    this.checkLoggedIn()
    this.getUsers()
    this.admin_check()
  },
  created(){
    
  }
}
</script>

<style>
</style>