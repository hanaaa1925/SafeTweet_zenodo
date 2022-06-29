<template>
  <div
    id="app"
    class="h-100 "
  >
    <div class="row h-100">
      <div class="col col-md-2 d-flex flex-column flex-shrink-0 p-3 bg-light h-100">
        <a
          href="/"
          class="d-flex align-items-center mb-3 mb-md-0 me-md-auto link-dark text-decoration-none"
        >
          <span class="fs-2 text-info">SafeTweet</span>
        </a>
        <hr>
        <ul class="nav nav-pills flex-column mb-auto">
          <li class="nav-item">
            <router-link
              class="nav-link"
              to="/"
            >
              <b-icon icon="house-door"></b-icon> <span class="ms-2" id="home">Home</span>
            </router-link>
          </li>
          <li>
            <router-link
              class="nav-link"
              to="/about"
            >
              <b-icon icon="envelope"></b-icon><span class="ms-2" id="notice">Notice</span>
            </router-link>
          </li>
          <li>
            <router-link
              class="nav-link"
              to="/profile"
            >
              <b-icon icon="person"></b-icon><span class="ms-2">Profile</span>
            </router-link>
          </li>
        </ul>
        <hr>
      </div>
      <div class="col col-md-7 h-100">
        <router-view
          :user="user"
          @updateUser="updateUser"
        />
      </div>
      <div class="col col-md-3 d-flex flex-column flex-shrink-0 p-3 bg-light position-relative ">
        <div
          v-if="!user"
          class="d-flex justify-content-end align-items-center"
        >
          <a
            class="me-2"
            href="#"
            @click="login=true"
          >
            <strong>Login</strong>
          </a>

          <a
            class="me-2"
            href="#"
            @click="register=true"
          >Register </a>
        </div>
        <div
          v-if="user"
          class="d-flex justify-content-end align-items-center"
        >
          <span>Welcome, {{user.username}}</span>
          <a
            class="me-2 ms-2"
            href="#"
            @click="logout"
          >Logout </a>
          <router-link
            to="/profile"
          >
          <img
            :src="'http://localhost:5050' + user.avatar + '?'+ Date.now()"
            alt=""
            width="32"
            height="32"
            class="rounded-circle ms-2"
          >
          </router-link>
        </div>
        <b-form-group class="mt-3">
          <b-form-input
            id="search"
            v-model="search"
            type="search"
            placeholder="Search"
            required
          ></b-form-input>
        </b-form-group>
        <b-button
          size="sm mt-2"
          @click="searchTweets"
        >search</b-button>
        <div  style="height:80%;overflow-y: scroll;">
          <b-list-group
            class="mt-2"

          >
            <b-list-group-item
              v-for="tw in searchResult"
              :key="tw.id"
              class="flex-column align-items-start"
            >
              <div class="d-flex w-100 justify-content-between align-items-center">
                <img
                  :src="!tw.is_anonymous?'http://localhost:5050' + tw.avatar:'http://localhost:5050/avatars/default-avatar.png'"
                  alt=""
                  width="30"
                  height="30"
                  class="rounded-circle ms-2"
                >
                <h6 v-if="!tw.is_anonymous" class="mb-1">@{{tw.username}}</h6>
                <!-- <small>3 days ago</small> -->
              </div>

              <p class="mb-1 px-3">
                {{tw.content}}
              </p>

            </b-list-group-item>
          </b-list-group>
        </div>
        <div class="position-absolute feedback"><a href="">FeedBack</a></div>
      </div>
    </div>

    <b-modal
      v-model="login"
      id="register"
      title="Register"
      hide-footer
      hide-header
      centered
    >
      <login
        :doLogin="doLogin"
        :showLogin="showLogin"
      />
    </b-modal>
    <b-modal
      v-model="register"
      id="register"
      title="Register"
      hide-footer
      hide-header
      centered
    >
      <register
        :showLogin="showLogin"
        :showRegister="showRegister"
      />
    </b-modal>
  </div>
</template>
<script>
import Register from './views/Register.vue'
import Login from './views/Login.vue'
import axios from 'axios'
export default {
  components: {
    Register,
    Login
  },
  data () {
    return {
      search: '',
      company: '',
      user: null,
      login: false,
      register: false,
      searchResult: []
    }
  },
  mounted () {
    this.getUser()
  },
  methods: {
    doLogin (user) {
      this.user = user
    },
    showLogin (show) {
      this.login = show
    },
    showRegister (show) {
      this.register = show
    },
    getUser () {
      if (localStorage.token) {
        axios.get('http://localhost:5050/api/users/', {
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${localStorage.token}`
          }
        })
          .then(response => {
            this.user = response.data
          })
      }
    },
    logout () {
      this.user = null
      delete localStorage.token
      location.reload()
    },
    updateUser (data) {
      this.user = data
    },
    searchTweets () {
      axios.get('http://localhost:5050/api/tweets/search/' + this.search)
        .then(response => {
          this.searchResult = response.data
        }).catch(err => {
          this.$toast.open({
            error: err,
            message: 'Please login.',
            type: 'error'
          })
        })
    }
  }
}
</script>
<style>
html,
body {
  padding: 0px;
  margin: 0px;
  height: 100%;
}
*,
::after,
::before {
  box-sizing: border-box;
}
.main {
  display: flex;
  flex-wrap: nowrap;
  height: 100vh;
  height: -webkit-fill-available;
  max-height: 100vh;
  overflow-x: auto;
  overflow-y: hidden;
}

.-divider {
  flex-shrink: 0;
  width: 1.5rem;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.1);
  border: solid rgba(0, 0, 0, 0.15);
  border-width: 1px 0;
  box-shadow: inset 0 0.5em 1.5em rgb(0 0 0 / 10%),
    inset 0 0.125em 0.5em rgb(0 0 0 / 15%);
}

.nav-link {
  color: black !important;
}

.nav-pills .nav-link {
  border: inherit !important;
}

.nav-link.router-link-exact-active {
  /* // color: black !important; */
  background-color: lightblue !important;
  color: rgb(51, 158, 224) !important;
  border-radius: 0px;
  border-right: 3px solid rgb(51, 158, 224);
}
.row {
  margin: 0px !important;
}
.feedback {
  bottom: 10px;
  right: 10px;
}
</style>
