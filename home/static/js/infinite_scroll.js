var InfiniteScroll = (function(){

  exports = {};

  flag = 1;

  exports.init = function(element_id, callback, threshold){
    // element_id - id of the element to attach the infinite scroll listener
    // callback - function to callback
    // threshold - more the threshold, the earlier the function will be called
    window.onscroll = function() {
      var posts_container = document.getElementById(element_id);
      var container_height = posts_container.offsetHeight;
      var scroll = window.scrollY + threshold*100;
      if (scroll >= container_height){
        if (flag){
          flag = 0;
          callback();
        }
      }
    } 
  }

  exports.enable = function() {
    flag = 1;
    return flag;
  }

  exports.disable = function() {
    flag = 0;
    return flag;
  }

  return exports;

})();
