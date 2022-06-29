<template>
  <div class="home">
    <tweet :user="user" @created="getTweets" />
    <hr />
    <posts :user="user" :tweets="tweets" @updateTweets="getTweets"/>
  </div>
</template>

<script>
import Tweet from '../components/Tweet.vue'
import Posts from '../components/Posts.vue'
import axios from 'axios'
export default {
  name: 'Home',
  data () {
    return {
      tweets: []
    }
  },
  mounted () {
    this.getTweets()
  },
  props: ['user'],
  components: {
    Tweet,
    Posts
  },
  methods: {
    getTweets () {
      axios.get('http://localhost:5050/api/tweets/')
        .then(response => {
          this.tweets = response.data
        })
    },

    getCompanyTweets () {
      axios.get('http://localhost:5050/api/tweets/company/')
        .then(response => {
          this.tweets = response.data
        })
    }
  }
}
</script>
<style scoped>
</style>
