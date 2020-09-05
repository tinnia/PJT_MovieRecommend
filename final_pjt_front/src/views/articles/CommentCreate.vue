<template>
  <div>
      댓글작성완료
  </div>
</template>

<script>
export default {
    name:"CommentCreate",
    params:{
        article:'',
    },
    methods: {
        gotoArticle: function() {
            this.$router.push({ name: 'ArticleListView'})
        }
    },
    created() {
        this.gotoArticle()
    },
}
</script>

<style>

</style>