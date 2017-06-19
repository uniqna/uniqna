new Vue({
  el: '.notification',
  data: {
    value: 'inherit'
  },
  methods: {
    triggerDelete: function() {
      this.value = 'none';
    }
  }
});
