<template>
  <div class="container">
    <b-form
      @submit="onSubmit"
      @reset="onReset"
      v-if="show"
    >
      <h1 id="login">Login</h1>

      <b-form-group
        class="mb-2"
        id="input-group-2"
        label="Email:"
        label-for="input-2"
      >
        <b-form-input
          id="input-2"
          v-model="form.email"
          placeholder="Enter Email"
          required
        ></b-form-input>
      </b-form-group>

      <b-form-group
        class="mb-2"
        id="input-group-3"
        label="Password:"
        label-for="input-3"
      >
        <b-form-input
          id="input-3"
          type="password"
          v-model="form.password"
          placeholder="Enter password"
          required
        ></b-form-input>
      </b-form-group>

      <b-button
        id="submit"
        type="submit"
        variant="primary"
      >Submit</b-button>
    </b-form>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      form: {
        email: '',
        password: ''
      },
      show: true
    }
  },
  props: ['doLogin', 'showLogin'],
  methods: {
    onSubmit (event) {
      event.preventDefault()
      // alert(JSON.stringify(this.form))
      axios.post('http://localhost:5050/api/users/login', this.form).then((response) => {
        this.doLogin(response.data.user)
        this.showLogin(false)
        localStorage.token = response.data.access_token
      }).catch(err => {
        this.$toast.open({
          message: err.response.data.message,
          type: 'error'
        })
      })
    },
    onReset (event) {
      event.preventDefault()
      // Reset our form values
      this.form.email = ''
      this.form.password = ''
      // Trick to reset/clear native browser form validation state
      this.show = false
      this.$nextTick(() => {
        this.show = true
      })
    }
  }
}
</script>
