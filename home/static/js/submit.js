function validateForm() {
  var isValid = true;
  $('.input').filter('[required]').each(function() {
    if ( $(this).val().trim() === '' )
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
      this.isActive = validateForm();
    }
  }
});
