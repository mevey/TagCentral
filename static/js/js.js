$(document).ready(function() {
  $('#wiki-search').focus()

  var recommendationURL = 'http://127.0.0.1:5000/r';
  var autocompleteURL = 'http://127.0.0.1:5000/ac'
  var template = '<div class="card result"><h2 class="title">{{title}}</h2><div class="snippet">{{snippet}}</div><a href="{{url}}" class="read-more-link">Read More</a></div>';

  //handels error to update ui
  function showError(error) {
    $('.error').text(error).removeClass('zoomOutRight').addClass('slideInRight').show();
    setTimeout(function() {
      $('.error').removeClass('slideInRight').addClass('zoomOutRight').hide(1000).text('');
    }, 3000);
  }

  //sends ajax request to wiki api to get results
  function wikiRequest(query) {
    $.ajax({
      url: recommendationURL + '?q=' + query,
      beforeSend: function(xhr) {
        console.log('Before: ' + xhr);
        $('.result').remove();
        $('.content .loading').show();
      },
      complete: function(xhr, status) {
        console.log('complete: ' + status);
        $('.content .loading').hide();
      },
      success: function(result, status, xhr) {
        $('.suggestions').html("")
        $('.chosen-tags').append('<a>'+ result.query +' <span>X</span></a>')
        arr = result.results[0]
        for (var i = 0; i < arr.length; i++) {
            $('.suggestions').append('<a>'+ arr[i] +' <span>X</span></a>')
        }
        $('.suggestions a').click(function() {
            val = $(this).html().replace("<span>X</span>","")
             $('.chosen-tags').append('<a>'+ val +' <span>X</span></a>')
             $(this).css("display","none")
             //$('.suggestions').html("")
             //wikiRequest(val)
             $('.chosen-tags a').click(function() {
                 $(this).css("display","none")
                 $('.suggestions').html("")
             })
        })
        $('.chosen-tags a').click(function() {
            $(this).css("display","none")
            $('.suggestions').html("")
        })
        $('#wiki-search').val('')
        $('#wiki-search').focus()
      },
      error: function(xhr, status, error) {
        console.log(error);
      }
    });
  }

  //listens for clear button click of search input and removes existing results
  $('#wiki-search').on('search', function(e) {
    if (this.value == "") {
      $('.result').remove();
    }
  });

  //Written before autocomplete plugin added , it will call wikiRequest() when user press Enter in searcg bar.
  $('#wiki-search-form').on('submit', function(e) {
    e.preventDefault();

    var query = $('#wiki-search').val();
    if (!query) {
      showError('Type something to search!..');
      return;
    }else{
      wikiRequest(query);
    }

  })

  //handels autocomplete
  $('#wiki-search').autocomplete({
    lookup: function(query, done) {
      $.ajax({
        url: autocompleteURL + '?q=' + query,
        //delay: 2000,
        success: function(data) {
          console.log("Done")
          //data = JSON.parse(data)
          console.log(data);
          var results = data.results
//          results.sort(function(a, b) {
//            return a.localeCompare(b);
//          })

          data = {
            suggestions: results.map(function(item, index) {
              return {
                value: item,
                data: index
              };
            })
          };
          done(data);
        }
      });
    },
    onSelect: function(suggestion) {
      wikiRequest(suggestion.value);
    }
  });

  //if user deletes text in search feild then existing results are removed
  $('#wiki-search').on('change', function() {
    if (this.value == "") {
      $('.result').remove();
    }
  });

});
