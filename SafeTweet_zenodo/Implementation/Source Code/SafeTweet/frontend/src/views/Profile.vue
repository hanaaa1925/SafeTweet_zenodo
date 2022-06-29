<template>
  <div class="container mt-5">
    <div class="row">
      <div class="col-12 bg-white p-0 px-3 py-5 mb-3">
        <div class="d-flex flex-column align-items-center">
          <b-avatar
            :src="'http://localhost:5050' + user.avatar + '?'+ Date.now()"
            size="8rem"
          ></b-avatar>
          <div class="my-3">
            <b-button
              class="border-0 bg-white text-muted"
              v-b-toggle.avatar
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="16"
                height="16"
                fill="currentColor"
                class="bi bi-camera-fill"
                viewBox="0 0 16 16"
              >
                <path d="M10.5 8.5a2.5 2.5 0 1 1-5 0 2.5 2.5 0 0 1 5 0z" />
                <path d="M2 4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2h-1.172a2 2 0 0 1-1.414-.586l-.828-.828A2 2 0 0 0 9.172 2H6.828a2 2 0 0 0-1.414.586l-.828.828A2 2 0 0 1 3.172 4H2zm.5 2a.5.5 0 1 1 0-1 .5.5 0 0 1 0 1zm9 2.5a3.5 3.5 0 1 1-7 0 3.5 3.5 0 0 1 7 0z" />
              </svg>
            </b-button>
          </div>

          <b-collapse id="avatar">
            <b-card class="card">
              <div class="d-flex justify-content-between align-items-center">
                <label class="fs-3">
                  <input
                    type="file"
                    @change="onFileChange"
                  />
                  <a
                    class="fs-5"
                    size="sm"
                  >
                    Choose File
                  </a>
                </label>
                <b-button
                  @click="upload"
                  size="sm"
                >
                  Upload
                </b-button>
              </div>
              <div id="preview">
                <img
                  v-if="url"
                  :src="url"
                />
              </div>

            </b-card>
          </b-collapse>
          <p class="fw-bold h4 mt-3">{{user.username}}</p>
          <div class="w-100 d-flex justify-content-end">
            <a
              class="border-0 bg-white"
              style="cursor:pointer"
              @click="showEdit(true)"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                fill="currentColor"
                class="bi bi-pencil-square"
                viewBox="0 0 16 16"
              >
                <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z" />
                <path
                  fill-rule="evenodd"
                  d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5v11z"
                />
              </svg>
            </a>
          </div>
        </div>
        <div class="col-12 bg-white px-3 mb-3 pb-3">
          <div class="d-flex align-items-center justify-content-between border-bottom">
            <p class="py-2">Email</p>
            <p class="py-2 text-muted">{{user.email}}</p>
          </div>
          <div class="d-flex align-items-center justify-content-between border-bottom">
            <p class="py-2">Phone</p>
            <p class="py-2 text-muted">{{user.phone}}</p>
          </div>
          <div class="d-flex align-items-center justify-content-between">
            <p class="py-2">Company</p>
            <p class="py-2 text-muted"> {{user.company}}</p>
          </div>
        </div>
      </div>
    </div>
    <b-modal
      v-model="edit"
      id="edit"
      size="lg"
      title="Edit Profile"
      hide-footer
      hide-header
    >
      <b-form @submit="onSubmit">
        <h1>Edit Profile</h1>
        <b-form-group
          id="input-group-2"
          label="Your Email:"
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
          id="input-group-3"
          label="Your Company:"
          label-for="input-3"
        >
          <b-form-input
            id="input-3"
            v-model="form.company"
            placeholder="Enter Company"
          ></b-form-input>
        </b-form-group>
        <b-form-group
          id="input-group-4"
          label="Your Phone:"
          label-for="input-4"
        >
          <b-form-input
            id="input-4"
            v-model="form.phone"
            placeholder="Enter Phone"
          ></b-form-input>

        </b-form-group>
        <b-form-group
          id="input-group-5"
          label="Your Password:"
          label-for="input-5"
        >
          <b-form-input
            id="input-5"
            class="mb-3"
            type="password"
            v-model="form.password"
            placeholder="Enter Password"
          ></b-form-input>
        </b-form-group>
        <b-button
          type="submit"
          size="sm"
          variant="primary"
        >Update</b-button>
        <b-button
          @click="edit=false"
          class="ms-2"
          size="sm"
          variant="secondary"
        >Cancel</b-button>
      </b-form>
    </b-modal>
  </div>
</template>
<script>
import axios from 'axios'
export default {
  data () {
    return {
      edit: false,
      form: {
        email: '',
        company: '',
        phone: ''
      },
      url: null,
      file: null
    }
  },
  props: ['user'],
  mounted () {

  },
  methods: {
    onFileChange (e) {
      const file = e.target.files[0]
      this.file = file
      this.url = URL.createObjectURL(file)
    },
    showEdit (show) {
      if (show) {
        this.form.file = null
        this.form.company = this.user.company
        this.form.email = this.user.email
        this.form.phone = this.user.phone
      }
      this.edit = show
    },
    upload () {
      const formData = new FormData()
      formData.append('file', this.file)
      const headers = { 'Content-Type': 'multipart/form-data', Authorization: `Bearer ${localStorage.token}` }
      axios.post('http://localhost:5050/api/users/upload', formData, {
        headers
      }).then((response) => {
        console.log(response)
        this.$emit('updateUser', response.data)
      })
    },
    onSubmit (event) {
      event.preventDefault()
      axios.put('http://localhost:5050/api/users/profile', this.form, {
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.token}`
        }
      }).then((response) => {
        this.$toast.open({
          message: 'Profile updated',
          type: 'success'
        })
        this.showEdit(false)
        this.$emit('updateUser', response.data)
      }).catch(err => {
        this.$toast.open({
          message: err.response.data.message,
          type: 'error'
        })
      })
    }
  }
}
</script>
<style >
#preview {
  display: flex;
  justify-content: center;
  align-items: center;
}

#preview img {
  max-width: 200px;
  max-height: 200px;
}

input[type="file"] {
  display: none;
}

.card {
  width: 400px;
  height: 340px;
}
</style>
