<template>
    <div class="container w-50">
        <div class="text-center shadow border mb-5 bg-white rounded-lg m-5">
            <form>
                <p class="font-weight-bold h4 text-center my-4">SIGNUP</p>
                <hr><br>
                <div class="mt-2 mb-5 w-75 d-flex inline mx-auto">
                    <b-icon class="align-self-center" icon="person-fill" font-scale="1.7" variant="secondary"></b-icon>
                    <input type="username" id="defaultFormLoginEmailEx" class="form-control form-control-lg mx-3 rounded-0" v-model="signupData.username" placeholder="Username" />
                </div>
                <div class="mb-5 w-75 d-flex inline mx-auto">
                    <b-icon class="align-self-center" icon="lock-fill" font-scale="1.7" variant="secondary"></b-icon>
                    <input type="password" v-model="signupData.password1" id="defaultFormLoginPasswordEx" class="form-control form-control-lg mx-3 rounded-0" placeholder="Password"/>
                </div>
                <div class="mb-5 w-75 d-flex inline mx-auto">
                    <b-icon class="align-self-center" icon="lock-fill" font-scale="1.7" variant="secondary"></b-icon>
                    <input type="password" v-model="signupData.password2" id="defaultFormLoginPasswordEx2" class="form-control form-control-lg mx-3 rounded-0" placeholder="Password 확인"/>
                </div>
                <b-button class="m-3 font-weight-bold" @click="signup" variant="outline-secondary">Sign up</b-button>
                <hr class='mb-0'>
                <div class="bg-light rounded-lg">
                    <p class="m-0 p-3 font-weight-bold">Already have an account?
                    <br>
                    <a href="" class="font-weight-bold" @click="login">Login</a>
                    </p>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
export default {
    name:'SignupView',
    data: function() {
        return {
            signupData:{
                username:'',
                password1:'',
                password2:'',
            },
        }
    },
    methods:{
        signup: function() {
            this.$emit('submit-signup-data',this.signupData)
        },
        login() {
            this.$router.push({ name: 'LoginView' })
        },
    }
}
</script>

<style>

</style>