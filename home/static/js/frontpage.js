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
      console.log('Category: ', cat);
      console.log('Page: ', page);
      endpoint = `/api/frontpage/${cat}/${page}/`
      var fp = this;
      // Return the jquery ajax object
      return $.get(endpoint, function(data) {
        if (data){
          if (fp.category == cat)
            fp.posts = [...fp.posts, ...data]
          else
            fp.posts = data;
          fp.category = cat;
          fp.page = page;
        }
      })
      .done(function(data){
        if (data.length)
          InfiniteScroll.enable();
      })
      .fail(function(){
        InfiniteScroll.enable();
        console.error('No network connectivity.');
      });
    },
    infiScroll: function() {
      this.fetchPosts(this.category, ++this.page, 3);
    }
  }
});

fp.user = $("#vue-frontpage").data('user');

InfiniteScroll.init('vue-frontpage', fp.infiScroll, 5);
