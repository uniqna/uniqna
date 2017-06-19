new Vue({
  el: '.submit',
  data: {
    isActive: false
  },
  methods: {
    toggleLoading: function() {
      this.isActive = true;
    }
  }
});
