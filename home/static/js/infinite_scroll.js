var InfiniteScroll = function(element_id, callback, threshold=7){
  
  // element_id - id of the element to attach the infinite scroll listener
  // callback - function to callback
  // threshold - more the threshold, the earlier the function will be called
  var posts_container = document.getElementById(element_id);
  var container_height = posts_container.offsetHeight;
  var already_called_flag = 0;
  window.onscroll = function() {
    var scrollY = window.scrollY;
    if ((scrollY + (threshold*100)) >= container_height){
      if (!already_called_flag){
        already_called_flag = 1;
        callback();
      }
    }
  } 

}
