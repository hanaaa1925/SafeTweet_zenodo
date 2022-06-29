<template>
  <div class="container">
    <b-form
      @submit="onSubmit"
      @reset="onReset"
      v-if="show"
    >
      <h1>Register</h1>
      <b-form-group
        id="input-group-1"
        label="Email address:"
        label-for="input-1"
        description="We'll never share your email with anyone else."
      >
        <b-form-input
          id="input-1"
          v-model="form.email"
          type="email"
          placeholder="Enter email"
          required
        ></b-form-input>
      </b-form-group>

      <b-form-group
        id="input-group-2"
        label="Your Full Name:"
        label-for="input-2"
      >
        <b-form-input
          id="input-2"
          v-model="form.username"
          placeholder="Enter Your Full Name"
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

      <b-form-group
        id="input-group-4"
        label="Your Company:"
        label-for="input-4"
      >
        <b-form-input
          class="mb-2"
          id="input-4"
          v-model="form.company"
          placeholder="Enter company"
          required
        ></b-form-input>
      </b-form-group>

      <b-button
        id="input-5"
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
        username: '',
        password: '',
        company: ''
      },
      show: true
    }
  },
  props: ['showLogin', 'showRegister'],
  methods: {
    onSubmit (event) {
      event.preventDefault()
      // alert(JSON.stringify(this.form))
      // const _this = this
      // this.form.password = this.$md5(_this.form.password)
      axios.post('http://localhost:5050/api/users/register', this.form).then((response) => {
        console.log(response)
        this.$toast.open({
          message: response.data.message,
          type: 'success'
        })
        this.showRegister(false)
        this.showLogin(true)
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
      this.form.username = ''
      this.form.password = ''
      this.form.company = ''
      // Trick to reset/clear native browser form validation state
      this.show = false
      this.$nextTick(() => {
        this.show = true
      })
    }
  }
}
</script>
