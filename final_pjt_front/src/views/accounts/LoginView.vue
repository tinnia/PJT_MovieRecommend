<template>
    <div class="container w-50">
        <div class="text-center shadow border mb-5 bg-white rounded-lg m-5">
            <form>
                <p class="font-weight-bold h4 text-center my-4">LOGIN</p>
                <hr><br>
                <div class="mt-2 mb-5 w-75 d-flex inline mx-auto">
                    <b-icon class="align-self-center" icon="person-fill" font-scale="1.7" variant="secondary"></b-icon>
                    <input type="username" v-model="username" id="defaultFormLoginEmailEx" class="form-control form-control-lg mx-3 rounded-0" placeholder="Username" />
                </div>
                <div class="mb-5 w-75 d-flex inline mx-auto">
                    <b-icon class="align-self-center" icon="lock-fill" font-scale="1.7" variant="secondary"></b-icon>
                    <input type="password" v-model="password" id="defaultFormLoginPasswordEx" class="form-control form-control-lg mx-3 rounded-0" placeholder="Password"/>
                </div>
                <b-button class="m-3 font-weight-bold" @click="login" variant="outline-secondary">Login</b-button>
                <hr class='mb-0'>
                <div class="bg-light rounded-lg">
                    <p class="m-0 p-3 font-weight-bold">Don't have an account?
                    <br>
                    <a href="" class="font-weight-bold" @click="signup">Sign Up</a>
                    </p>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
export default {
    name:'LoginView',
    data: function() {
        return{
            username:'',
            password:'',
        }
    },
    methods:{
        login: function() {
            const loginData ={
                username : this.username,
                password : this.password,
            }
            this.$emit('submit-login-data',loginData)
        },
        signup() {
            this.$router.push({ name: 'SignupView' })
        }
    }
}
</script>

<style>
#defaultFormLoginEmailEx{
    font-size: 100%;
    padding: 25px 25px;
    border: none;
    border-bottom: 1.5px solid gray;
}
#defaultFormLoginPasswordEx{
    font-size: 100%;
    padding: 25px 25px;
    border: none;
    border-bottom: 1.5px solid gray;
}
#defaultFormLoginPasswordEx2{
    font-size: 100%;
    padding: 25px 25px;
    border: none;
    border-bottom: 1.5px solid gray;
}
</style>