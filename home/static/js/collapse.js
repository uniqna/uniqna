
(function(){
  // Collapse the replies

  $(".minimize").on("click", function(e) {
    e.preventDefault();

    var text = $(this).text();
    var childReplies = $(this).parents("article").siblings(".children");
    var childCount = $(this).parents("article").find(".child-count");
    var childs = childReplies.children(".box").length;

    // Don't do anything if it has zero children
    if (childs == 0)
      return;

    if (text == "[-]"){
      childReplies.hide();
      childCount.text(childs + " replies collapsed.")
      $(this).text("[+]");
    }
    else if (text == "[+]"){
      childReplies.show();
      childCount.text("");
      $(this).text("[-]");
    }

  });

  // Collapse multi level replies

  var leafs = $(".leaf-node");
  var threshold = 5;
  $.each(leafs, function(index, leaf) {
    var parentNodes = $(leaf).parents(".children");
    var level = parentNodes.length + 1;
    var replyUrl = $
    if (level > threshold) {
      // parentNodes[level-threshold-1] will always be a 3rd level node
      // we are removing every node after that level
      for (var i = level - threshold - 1; i >= 0; i--) {
        parentNodes[i].style.display = "none";
      }

      // Element to attach the "Read Thread" link
      // Currently the last 
      var container = $(parentNodes[level - threshold]);

      //Check whether a "read Thread" link is already present
      if (container.children(".readthread").length == 0) {
        var reply_url = $(container).data("url");
        var readThreadElement = "<a class='readthread' href='" + reply_url + "''><small>Read the full train [ " + (level - threshold) + ((level - threshold) > 1 ? " Replies" : " Reply") + " ]</small></a>";
        container.append($(readThreadElement));
      }
    }
  });

})();


