// ----- custom js ----- //

// hide initial
$("#searching").hide();
$("#searched").hide();
$("#results-table").hide();
$("#error").hide();

// global
var url = 'http://static.pyimagesearch.com.s3-us-west-2.amazonaws.com/vacation-photos/dataset/';
var data = [];

$(function() {

  // sanity check
  console.log( "ready!" );
  var i = 0;

  // image click
  $(".query1").keyup(function(e) {
    console.log('here', i, e.keyCode)
    if(e.keyCode >= 33){
      i++;
    }

    if(e.keyCode != 13 && i%4 && e.keyCode != 32){
      return
    }
    i++;
    // if (e.keyCode != 13){
    //   return
    // }

    // empty/hide results
    $("#results").empty();
    $("#results-table").hide();
    $("#error").hide();

    // remove active class
    // $(".query1").removeClass("active")

    // add active class to clicked picture
    // $(this).addClass("active")

    // grab image url
    var image = $(this).val()
    console.log(image)

    // show searching text
    $("#searched").hide();
    $("#searching").show();
    console.log("searching...")

    // ajax request
    $.ajax({
      type: "POST",
      url: "/search",
      data : { img : image },
      // handle success
      success: function(result) {
        console.log(result.results);
        var data = result.results
        // show table
        $("#results-table").show();
        // loop through results, append to dom
        for (i = 0; i < data.length; i++) {
          $("#results").append('<tr><th>' + data[i]["candidate"] + '</th><th>'+data[i]['cosine']+'</th></tr>')
        };
        
        setTimeout(function(){ $("#searching").hide();$("#searched").show(); }, 1500);
      },
      // handle error
      error: function(error) {
        console.log(error);
        // append to dom
        $("#error").append()
      }
    });

  });

});