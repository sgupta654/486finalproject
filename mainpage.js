function init(){
    d3.select("#submit").on("click", function(){redirect(this.form);});
    
    // Tracked subreddits.
    d3.text("http://localhost:8080/graph/tracked_subreddits", function(error, text) {
                                 var reddits = text.split("\n");
                                 var tracked = d3.select("#tracked");
                                 for (var i = 0; i < reddits.length-1; i+=1) {
                                    tracked.append("p").attr("class", "listing").append("a").attr("href", "http://www.reddit.com/r/" + reddits[i]).text("/r/" + reddits[i]);
                                 }
    } );
}

function validate(name, limit, algo) {
    var alertdiv = d3.select("#alerts");
    var subredditAlert = "";
    var limitAlert = "";
    var algorithmAlert = "";
    var problems = false;
    if (name == "") {
        subredditAlert = "\tSupply subreddit name.";
        problems = true;
    }   
    if (parseInt(limit) > 100) {
        limitAlert = "\tThreshold cannot exceed 100.";
        problems = true;
    }
    else if (limit == "") {
        limitAlert = "\tInput a threshold.";
        problems = true;
    }
    else if (parseInt(limit) != limit) {
        problems = true;
        limitAlert = "\tInput a proper limit.";
    }
    if (algo == "") {
        algorithmAlert = "\tSelect an algorithm.";
        problems = true;
    }
    
    d3.select("#subredditError").text(subredditAlert);
    d3.select("#limitError").text(limitAlert);
    d3.select("#algoError").text(algorithmAlert);
    console.log(name, limit, algo);
    if (problems) {
        return;
    }
    window.location.replace("http://localhost:8080/grapher/" + name + "?limit=" + limit + "&algorithm=" + algo);
}

function redirect(form) {
    var algo = "";
    for (var i = 0; i < form.algorithm.length; i+=1) {
        if (form.algorithm[i].checked) {
            algo = form.algorithm[i].value;
        }
    }
    validate(form.SubredditName.value, form.Threshold.value, algo);
}

document.addEventListener("DOMContentLoaded", init);
