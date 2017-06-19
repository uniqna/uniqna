new Vue({
  el: '.nav',
  data: {
    isActive: false
  },
  methods: {
    toggleNav: function() {
      this.isActive = !this.isActive;
    }
  }
});
