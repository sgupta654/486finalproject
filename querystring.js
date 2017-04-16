// Code from http://stackoverflow.com/questions/2907482/how-to-get-the-query-string-by-javascript by Josh Stodola
function getQueryStrings() { 
  var assoc  = {};
  var decode = function (s) { return decodeURIComponent(s.replace(/\+/g, " ")); };
  var queryString = location.search.substring(1); 
  var keyValues = queryString.split('&'); 

  for(var i in keyValues) { 
    var key = keyValues[i].split('=');
    if (key.length > 1) {
      assoc[decode(key[0])] = decode(key[1]);
    }
  } 

  return assoc; 
} 

function getSubreddit(CONST) {
CONST.SUBREDDIT = window.location.href.split("/");
CONST.SUBREDDIT = CONST.SUBREDDIT[CONST.SUBREDDIT.length-1].split("?");
CONST.SUBREDDIT = CONST.SUBREDDIT[0]; // Get the current URL's final part and set it as the subreddit! It's a hack, but it probably works.
var temp = getQueryStrings()
CONST.LIMIT = temp["limit"];
CONST.ALGORITHM = temp["algorithm"];
if (CONST.ALGORITHM === undefined) {
            CONST.ALGORITHM = "openord";
        }
console.log(CONST.SUBREDDIT, CONST.LIMIT);
}
