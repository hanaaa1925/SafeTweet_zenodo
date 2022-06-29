<template>
  <div onselectstart="return false" οndragstart="return false" class="contentWrapper">
    <div class="content">{{ content }}</div>
    <b-button
      @click="goBack"
      type="submit"
      variant="primary"
      size="sm"
      class="back"
      >Back</b-button>
  </div>
</template>

<script>
import { removeWatermark, setWaterMark } from '../js/watermark'
// Disable open the menu with the right mouse button
document.oncontextmenu = function () { return false }
export default {
  name: 'Decryption',
  props: ['user', 'tweets'],
  data () {
    return {
      content: ''
    }
  },
  mounted () {
    setWaterMark(this.user.username, this.user.email)
    var Base64 = require('js-base64').Base64
    this.content = Base64.decode(this.$route.params.content)
  },
  destroyed () {
    removeWatermark()
  },
  methods: {
    goBack () {
      this.$router.go(-1)
    }
  }
}
</script>

<style>
.contentWrapper {
  margin-top: 250px;
}
.content {
  z-index: 100000;
  font: 36px Times;
  text-align: center;
  top: 150px;
}
.back {
  margin-top: 200px;
  margin-left: 380px;
}
</style>
