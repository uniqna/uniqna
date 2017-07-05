function validateForm() {
  var isValid = true;
  $('.input').filter('[required]').each(function() {
    if ( $(this).val() === '' )
        isValid = false;
  });
  // Check for username availability
  var isAvail = $("#id_username").hasClass("is-success");
  console.log(isAvail);
  return isValid && isAvail;
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
