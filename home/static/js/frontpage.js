var fp = new Vue({
  delimiters: ["[", "]"],
  el: '#vue-frontpage',
  data: {
    posts: [],
    category: 'hot',
    page: 1,
    loaded: false,
    user: ''
  },
  mounted: function() {
    default_endpoint = "/api/frontpage/hot/1"
    fp = this;
    $.get(default_endpoint, function(data) {
    if (data){
      fp.loaded = true;
      fp.posts = data;
    }
    });
  },
  methods: {
    fetchPosts: function(cat, page=1) {
      endpoint = `/api/frontpage/${cat}/${page}/`
      var fp = this;
      fp.loaded = false;
      $.get(endpoint, function(data) {
        if (data){
          fp.loaded = true;
          if (fp.category == cat)
            fp.posts = [...fp.posts, ...data]
          else
            fp.posts = data;
          fp.category = cat;
          fp.page = page;
        }
      });
    }
  }
});

fp.user = $("#vue-frontpage").data('user');
