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
    beforeEnter: function(el){
      el.style.opacity = 0;
      el.style.height = 0;
    },

    enter: function(el, done) {
      var delay = el.dataset.index * 150;
      setTimeout(function(){
        Velocity(
          el,
          { opacity: 1, height: 120},
          { complete: done}
        );
      }, delay);
    },

    leave: function(el, done) {
      var delay = el.dataset.index * 50;
      setTimeout(function(){
        Velocity(
          el,
          { opacity: 0, height: 0},
          { complete: done }
        );
      }, delay);
    },

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
    },

    voteSuccess: function(post) {
      var author_voted = 0;
      for(var user of post.ups) {
        if (user.username === this.user){
            author_voted = 1;
            break;
        }
      }
      if(author_voted)
        return true;
      else
        return false;
    },

    voteDanger: function(post) {
      var author_voted = 0;
      for(var user of post.downs) {
        if (user.username === this.user){
            author_voted = 1;
            break;
        }
      }
      if(author_voted)
        return true;
      else
        return false;
    },

    userUrl: function(username) {
      return `/@${username}/`;
    },

    channelUrl: function(channel) {
      return `/channel/${channel}/`;
    },

    postUrl: function(post) {
      slug = post.title.toLowerCase().split(' ').join('-');
      return `/thread/${post.id}-${slug}`;
    },

    voteUrl: function(post, type) {
      return `/api/vote/question/${post.id}/${type}`
    }
  }
});

fp.user = $("#vue-frontpage").data('user');

InfiniteScroll.init('vue-frontpage', fp.infiScroll, 7);
