function init() {
    getSubreddit(CONSTANTS);
    d3.select("body").append("div").attr("id","log");
    refreshtext();
}

var CONSTANTS = {"SUBREDDIT":"", "LIMIT":"" , "ALGORITHM":""};


function refreshtext() {    
    d3.text("http://localhost:8080/logs/" + CONSTANTS.SUBREDDIT +  CONSTANTS.LIMIT + CONSTANTS.ALGORITHM + ".lock", "text/plain", function(error, text) {
        var lines = text.split("\n");
        if (lines[lines.length-1] == "Done.") {
            window.location.replace("http://localhost:8080/grapher/" + CONSTANTS.SUBREDDIT + "?limit=" + CONSTANTS.LIMIT + "&algorithm=" + CONSTANTS.ALGORITHM);
        }
        d3.select("#log").selectAll("p").data(lines).enter().append("p").text(function(d) { return d } );
        setTimeout(refreshtext, 3000);
    });
}

document.addEventListener("DOMContentLoaded", init);
