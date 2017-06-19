function validateForm() {
  var isValid = true;
  $('.input').filter('[required]').each(function() {
    if ( $(this).val() === '' )
        isValid = false;
  });
  return isValid;
}

new Vue({
  el: '.submit',
  data: {
    isActive: false
  },
  methods: {
    toggleLoading: function() {
      if (validateForm()) {
        this.isActive = true;
      }
    }
  }
});
