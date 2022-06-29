<template>
  <div class="scroll">
    <ul>
      <div v-if="!user">
        Please Login.
      </div>
    </ul>
    <ul class="list-group list-group-flush" v-if="user">
      <li
        v-for="tweet in this.tweets"
        :key="tweet.id"
        class="list-group-item"
      >
        <div class="d-flex">
          <div class="d-flex flex-column justify-content-center text-center">
            <img
              :src="!tweet.is_anonymous?'http://localhost:5050' + tweet.avatar:'http://localhost:5050/avatars/default-avatar.png'"
              alt=""
              width="64"
              height="64"
              class="rounded-circle me-2"
            >
            <span v-if="!tweet.is_anonymous">{{tweet.username}}</span>
          </div>
          <p>{{tweet.content}}</p>
        </div>
        <div class="d-flex justify-content-around">
          <div class="emoji-invoker" @click="like(tweet.id)">
            <img src="../assets/thumb-up.png" alt=""><span style="font-size:13px; color:green">{{tweet.likes}}</span>
          </div>
          <div class="action">
            <img @click="showComments(tweet)" src="../assets/comment.png" alt="">
          </div>
          <div class="emoji-invoker" @click="fav(tweet.id)">
            <img src="../assets/favourite.png" alt=""><span style="font-size:13px; color:pink">{{tweet.favourites}}</span>
          </div>
          <div v-if="tweet.is_encryption==1" class="action" @click="decrypt(tweet)">
            <img src="../assets/unlock.png" alt="">
          </div>
        </div>
        <div v-if="comments.id === tweet.id">
          <div>
            <comments
              v-if="comments.show"
              :user="user"
              :tweet_id="comments.id"
              @updateComments="getComments(tweet.id)"
              @hideComment ="hideComment"
            />
            <ul class="list-group list-group-flush">
              <li
                v-for="comment in comments.items"
                :key="comment.id"
                class="list-group-item"
              >
                <div class="d-flex text-muted pt-3">
                  <img
                    :src="!comment.is_anonymous?'http://localhost:5050' + comment.avatar:'http://localhost:5050/avatars/default-avatar.png'"
                    alt=""
                    width="32"
                    height="32"
                    class="rounded-circle me-2"
                  >
                  <p class="pb-3 mb-0 small lh-sm border-bottom">
                    <strong class="d-block text-gray-dark">@{{!comment.is_anonymous?comment.username:'anonymous'}}</strong>
                    <span>{{comment.content}}</span>
                  </p>
                </div>
              </li>
            </ul>
          </div>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios'
import Comments from './Comments.vue'
export default {
  data () {
    return {
      favourite: false,
      comments: {
        id: 0,
        items: [],
        show: true,
        tweets: []
      }
    }
  },
  components: {
    Comments
  },
  name: 'posts',
  props: ['user', 'tweets'],
  // mounted () {
  //   this.getTweets()
  // },
  methods: {
    // checkLogin () {
    //   if (!this.user) {
    //     this.getOpenTweets()
    //   } else {
    //     this.getTweets()
    //   }
    // },
    // getOpenTweets () {
    //   axios.get('http://localhost:5050/api/tweets/open')
    //     .then((response) => {
    //       this.tweets = response.data
    //     })
    // },
    // getTweets () {
    //   axios.get('http://localhost:5050/api/tweets/')
    //     .then(response => {
    //       this.tweets = response.data
    //     })
    // },
    hideComment () {
      // this.comments.show = false
    },
    async showComments (tweet) {
      if (!this.user) {
        this.$toast.open({
          message: 'Login Required',
          type: 'error'
        })
        this.comments.show = false
      } else {
        // this.comments.id = tweet.id
        console.log('test')
        if (this.comments.id === tweet.id) {
          this.comments.id = 0
          this.comments.items = []
          this.comments.show = true
          return
        }
        this.comments.show = true
        this.comments.id = tweet.id
        await this.getComments(tweet.id)
      }
    },
    async getComments (id) {
      const response = await axios.get('http://localhost:5050/api/comments/' + id)
      this.comments.items = response.data
    },
    decrypt (tweet) {
      var content = ''
      content = tweet.content
      // console.log(content)
      this.$router.push({
        name: 'Decryption',
        params: {
          content: content
        }
      })
    },
    async fav (id) {
      this.favourite = !this.favourite
      axios.put('http://localhost:5050/api/tweets/fav/' + id, {}, {
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.token}`
        }
      }).then(() => {
        this.$emit('updateTweets', {})
      }).catch(err => {
        this.$toast.open({
          error: err,
          message: 'Error',
          type: 'error'
        })
      })
    },
    async like (id) {
      axios.put('http://localhost:5050/api/tweets/like/' + id, {}, {
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.token}`
        }
      }).then(() => {
        this.$emit('updateTweets', {})
      }).catch(err => {
        this.$toast.open({
          error: err,
          message: 'You have liked',
          type: 'error'
        })
      })
    }
  }

}
</script>

<style>
.action {
  margin-left: 0.5rem;
  margin-right: 0.5rem;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.2s;
}
.scroll {
  max-height: 60vh;
  overflow-y: scroll;
}
</style>
