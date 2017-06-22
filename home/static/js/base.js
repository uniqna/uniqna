var nav = new Vue({
  el: '.nav',
  data: {
    isActive: false,
    notification: `<i class="material-icons">notifications</i>`
  },
  methods: {
    toggleNav: function() {
      this.isActive = !this.isActive;
      if(this.isActive) {
        this.notification = 'Notifications';
      }
      else {
        this.notification = `<i class="material-icons">notifications</i>`;
      }
    }
  }
});

$(".post").click(function(){
    $(".modal-nav").addClass("is-active");
});

$(".modal-close").click(function(){
    $(".modal-nav").removeClass("is-active");
});

$(".modal-background").click(function(){
    $(".modal-nav").removeClass("is-active");
});
