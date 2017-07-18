(function(){

  
  // Hash such as #a12 /thread/1/#a12
  const hash = location.hash;

  // Return if there is no hash
  if (hash == "")
    return;

  // Pixels of the element from the top
  const offset = $(hash).offset().top - 100;

  // Animate that using scrollTop 
  // Executing the animation after a second is smoother
  // Than executing onload.
  setTimeout(function(){
    $('html, body').animate({
      scrollTop: offset
    }, 600);
  }, 1000);

})();
