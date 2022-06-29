<template>
  <form @submit="submitPost">
    <div class="wrapper">
      <textarea
        class="regular-input"
        v-model="input"
      ></textarea>

      <emoji-picker
        @emoji="append"
        :search="search"
      >
        <div
          class="emoji-invoker"
          slot="emoji-invoker"
          slot-scope="{ events: { click: clickEvent } }"
          @click.stop="clickEvent"
        >
          <b-icon icon="emoji-smile"></b-icon>
        </div>
        <div
          slot="emoji-picker"
          slot-scope="{ emojis, insert }"
        >
          <div
            class="emoji-picker"
            :style="{ top: '100px', rigth: '0px' }"
          >
            <div class="emoji-picker__search">
              <input
                type="text"
                v-model="search"
              >
            </div>
            <div>
              <div
                v-for="(emojiGroup, category) in emojis"
                :key="category"
              >
                <h5>{{ category }}</h5>
                <div class="emojis">
                  <span
                    v-for="(emoji, emojiName) in emojiGroup"
                    :key="emojiName"
                    @click="insert(emoji)"
                    :title="emojiName"
                  >{{ emoji }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </emoji-picker>
      <div
        class="emoji-invoker"
        @click="privacy = !privacy"
      >
        <img v-if="privacy" src="../assets/anonymous.png" alt="" title="Already Anonymous">
        <img v-if="!privacy" src="../assets/non-anonymous.png" alt=""  title="No Anonymous">
      </div>
    </div>
    <div class="w-100 d-flex justify-content-end">
      <b-button
        type="submit"
        variant="primary"
        size="sm"
      >Comment</b-button>
    </div>
  </form>
</template>

<script>
import axios from 'axios'
// import axios from 'axios'
import { EmojiPicker } from 'vue-emoji-picker'
export default {
  name: 'comments',
  components: {
    EmojiPicker
  },
  props: ['user', 'tweet_id'],
  data () {
    return {
      input: '',
      search: '',
      privacy: false
    }
  },
  methods: {
    append (emoji) {
      this.input += emoji
    },
    submitPost (e) {
      if (!this.user) {
        this.$toast.open({
          message: 'Login Required',
          type: 'error'
        })
      }
      e.preventDefault()
      if (this.input === '') {
        return
      }
      axios.post('http://localhost:5050/api/comments/', {
        content: this.input,
        is_anonymous: this.privacy,
        tweet_id: this.tweet_id
      }, {
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.token}`
        }
      }).then(response => {
        this.$toast.open({
          message: response.data.message,
          type: 'success'
        })
        this.input = ''
        this.$emit('updateComments')
        this.$emit('hideComment')
      })
    }
  }
}
</script>

<style scoped>

.wrapper {
  position: relative;
  display: inline-block;
  width: 100%;
  margin: 20px 0px;
  border: 1px solid #ccc;
}

.regular-input {
  padding: 0.5rem 1rem;
  border-radius: 3px;
  border: none;
  width: 100%;
  height: 4rem;
  outline: none;
}

.regular-input:focus {
  /* box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.5); */
  outline: none;
}

.emoji-invoker {
  /* position: absolute;
  bottom: 0.5rem;
  left: 0.5rem;
  width: 1.5rem;
  height: 1.5rem; */
  float: left;
  margin-left: 0.5rem;
  margin-right: 0.5rem;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.2s;
}
.emoji-invoker:hover {
  transform: scale(1.1);
}
.emoji-invoker > svg {
  fill: #b1c6d0;
}

.emoji-picker {
  position: absolute;
  z-index: 1;
  font-family: Montserrat;
  border: 1px solid #ccc;
  width: 15rem;
  height: 20rem;
  overflow: scroll;
  padding: 1rem;
  box-sizing: border-box;
  border-radius: 0.5rem;
  background: #fff;
  box-shadow: 1px 1px 8px #c7dbe6;
}
.emoji-picker__search {
  display: flex;
}
.emoji-picker__search > input {
  flex: 1;
  border-radius: 10rem;
  border: 1px solid #ccc;
  padding: 0.5rem 1rem;
  outline: none;
}
.emoji-picker h5 {
  margin-bottom: 0;
  color: #b1b1b1;
  text-transform: uppercase;
  font-size: 0.8rem;
  cursor: default;
}
.emoji-picker .emojis {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
}
.emoji-picker .emojis:after {
  content: "";
  flex: auto;
}
.emoji-picker .emojis span {
  padding: 0.2rem;
  cursor: pointer;
  border-radius: 5px;
}
.emoji-picker .emojis span:hover {
  background: #ececec;
  cursor: pointer;
}
</style>
