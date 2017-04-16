var zoomHandler = d3.behavior.zoom().on("zoom", redraw); // Save the Zoom object to use later in resetting the "camera"


var CONSTANTS = {"SUBREDDIT":"", "LIMIT":"", "ALGORITHM":""};


function center() {
    var container = d3.select("#container");
    zoomHandler.translate([0, 0]);
    zoomHandler.scale(1);
    container.transition()
        .duration(750)
        .attr("transform", "translate(0, 0) scale(1)");
}

function hide(button) {
    var labels = d3.select("#labels");
    hidden = !hidden;
    if (hidden) {
        button.innerHTML = "Show labels";
        labels.attr("display", "none");
    } else {
        button.innerHTML = "Hide labels";
        labels.attr("display", "");
    }
}

var svgWidth = 0;
var svgHeight = 0;
var startX = 0;
var startY = 0;
var hidden = false;
var context; // array from json
var removedNodes = [];
var focusedNode = undefined;

// code ran on load
function init() {
    getSubreddit(CONSTANTS);
    var svg = d3.select("#graph").append("svg").attr("id", "myGraph");
    d3.json("http://localhost:8080/graph/out/" + CONSTANTS.SUBREDDIT + CONSTANTS.LIMIT  + CONSTANTS.ALGORITHM + ".json",
        function (error, jsonData) {
            var data = jsonData[0];
            context = jsonData[1];

            var viewboxArray = data["viewBox"].split(" ");
            startX = viewboxArray[0];
            startY = viewboxArray[1];
            svgWidth = viewboxArray[2];
            svgHeight = viewboxArray[3];


            svg.attr("width", data["width"].slice(0,data["width"].length-2))
                .attr("height", data["height"].slice(0,data["height"].length-2))
                .attr("viewBox", data["viewBox"])
                .call(zoomHandler);
            resizeSVG();
            // append container to hold all the sub-groups
            var container = svg.append("g").attr("id", "container");

            var edges = container.append("g").attr("id", "edges");
            edges.selectAll("path")
                .data(data["edges"])
                .enter()
                .append("path")
                .attr("fill", function (d) {return d["fill"];})
                .attr("stroke-width", function (d) {return d["stroke-width"];})
                .attr("d", function (d) {return d["d"]; })
                .attr("class", function (d) {return d["class"];})
                .attr("stroke", function (d) {return d["stroke"];})

            var arrows = container.append("g").attr("id", "arrows");
            arrows.selectAll("polyline")
                .data(data["arrows"])
                .enter()
                .append("polyline")
                .attr("fill", function (d) {return d["fill"];})
                .attr("class", function (d) {return d["class"];})
                .attr("points", function (d) {return d["points"];})
                .attr("stroke", function (d) {return d["stroke"];});

            var nodes = container.append("g").attr("id", "nodes");
            nodes.selectAll("circle")
                .data(data["nodes"])
                .enter()
                .append("circle")
                .attr("r", function (d) {return d["r"];})
                .attr("fill", function (d) {return d["fill"];})
                .attr("cx", function (d) {return d["cx"];})
                .attr("cy", function (d) {return d["cy"];})
                .attr("class", function (d) {return d["class"];})
                .attr("stroke", function (d) {return d["stroke"];})
                .attr("stroke-width", function (d) {return d["stroke-width"];})
                .on("click", function (d) { setAndShowDetails(d); })
                .on("contextmenu", function(d) {removeElement(d);} );

            var labels = container.append("g").attr("id", "labels");
            labels.selectAll("text")
                .data(data["labels"])
                .enter()
                .append("text")
                .attr("font-size", function (d) {return d["font-size"];})
                .attr("x", function (d) {return d["x"];})
                .attr("y", function (d) {return d["y"];})
                .attr("fill", function (d) {return d["fill"];})
                .attr("style", function (d) {return d["style"];})
                .attr("font-family", function (d) {return d["font-family"];})
                .attr("class", function (d) {return d["class"];})
                .text(function (d) {return d["text"];})
                .on("click", function (d) { setAndShowDetails(d); })
            
        });
        
    showControls();
    d3.select(window).on("resize", resizeSVG);
}

function redraw() {
    d3.select("#container").attr("transform", "translate(" + d3.event.translate + ")" + " scale(" + d3.event.scale + ")");
}

function helloWorld() {
    console.log("hello world!");
}

function showInfo(d) {
    var elementname = d["class"];
    console.log(elementname);
}

function removeElement (d) {
    d3.event.preventDefault();
    var elementname = d["class"];
    d3.selectAll("." + elementname).attr("display", "none");
    removedNodes.push(elementname);
    updateNodeList();
}

function restoreElement (d, i) {
    removedNodes.splice(i, 1);
    d3.selectAll("." + d).attr("display", "");
    updateNodeList();
}

function restoreElement_NoUpdate(d) {
    d3.selectAll("." + d).attr("display","");
}

function clearList() {
    for (var it = 0; it < removedNodes.length; it++) {
        restoreElement_NoUpdate(removedNodes[it]);
    }
    
    removedNodes.length = 0;
    updateNodeList();
}

function updateNodeList() {
    showNodes();
    var div = d3.select(".list");
    div.selectAll("*").remove();
    
    if (removedNodes.length > 0) {
        div.append("button").attr("type","button").on("click", clearList).html("Clear list");
        div.append("br");
    }
    
    div.append("div").attr("class","list").attr("id","nodeList");
    var list = d3.select("#nodeList");
    
    list.selectAll("a").data(removedNodes).enter()
      .append("a").attr("class", "javascriptlink").text(function(d) { return (d + "\n"); }).on("click", function(d, i) { restoreElement(d, i);} ).append("br");
}

function showControls() {
    d3.selectAll(".sidebar").selectAll("*").remove();
    var page = d3.select("#controls");
    var button = page.append("button").attr("type","button").attr("onclick", "hide(this)");
    if (hidden) {
        button.text("Show labels");
    } else {
        button.text("Hide labels");
    }
    page.append("button").attr("type","button").text("Center").on("click", center);
    page.append("button").attr("type","button").text("New graph").on("click", function(){window.location.replace("http://localhost:8080/grapher/");});
}

function showNodes(buttoned) {
    if (buttoned == undefined) {
        buttoned = false;
    }
    
    d3.selectAll(".sidebar").selectAll("*").remove();
    var page = d3.select("#removedNodes");
    page.append("div").attr("class","list");
    if (buttoned) {
        updateNodeList();
    }
}

function setAndShowDetails(d) {
    focusedNode = d;
    showDetails();
}

function showDetails() {
    d3.selectAll(".sidebar").selectAll("*").remove();
    var page = d3.select("#details");
    if (focusedNode == undefined) {
        return;
    }
    page.append("span").attr("id","top");
    var data = context[focusedNode["class"]];
    // Displays name & link to
    page.append("strong").append("a").attr("target","_blank").attr("href","http://www.reddit.com/user/" + data["name"]).text("/r/" + data["name"]);    
    
    var row = page.append("table").append("tr");
    row.append("td").html("<em>Replies recieved:</em>");
    row.append("td").style("padding-left","5%").html(data["in"]);
    
    row = page.select("table").append("tr");
    row.append("td").html("<em>Replies written:</em>");
    row.append("td").style("padding-left","5%").html(data["out"]);
    
    var links = data["contexts"];
    var comment = page.append("div").attr("class","commentHolder");
    comment.selectAll("p").data(links).enter().append("p").append("a").on("click", function(d) {expandComment(d, this);}).text(function(d) {return d;});
    
    page.append("a").attr("href","#top");
}

function resizeSVG() {
    var graph = d3.select("#myGraph");
    var ratio = graph.attr("height") / graph.attr("width");
    var newWidth = d3.select("#graph").style("width");
    newWidth = newWidth.slice(0,newWidth.length-2);
    graph.attr("width", newWidth);
    graph.attr("height", newWidth * ratio);
}

// Turn a Reddit json comment into html
function getUsernameSpan(data) {
    return "<span class=\"username\">" + data["author"] + "</span>";
}

var divre = new RegExp("<div class=\"md\">", "g");
function unescapeHTML(html) {
    var string = html;
    string = string.replace(/&apos;/g, "\'");
    string = string.replace(/&quot;/g,"\"");
    string = string.replace(/&amp;/g,"\&");
    string = string.replace(/&lt;/g,"<");
    string = string.replace(/&gt;/g,">");
    string = string.replace(divre, "");
    string = string.replace(/<\/div>/g, "");
    return string;
}

function writeComment(data) {
    return "<span class=\"body\">" + data["body"]+ "</span>";
}

function writeFoldedComment(data) {
    var result = data["author"];
    if (data["replies"] != "")
        if (data["replies"]["data"]["children"].length > 0) {
            result += " and " + data["replies"]["data"]["children"].length + " comments";
        }
    return result;
}

function writePoints(data) {
    var points = data["ups"] - data["downs"];
    return " " + points + " points";
}

function foldComment(par) {
console.log("fold!");
    var base = d3.select(par.parentNode.parentNode);
    base.attr("class", "foldedComment"); 
}

function unfoldComment(par) {
    var base = d3.select(par.parentNode.parentNode);
    base.attr("class", "comment"); 
}

// First param should be an unfoldedComment, the second the json
function recursivelyDrawComments(parent, data, baselink) {
    // The container for folded/unfolded pair
    var thisComment = parent.append("div").attr("class","comment");
        
    // Next draw the unfolded comment
    var unfolded = thisComment.append("div").attr("class","unfoldedCommentContent");
    // Link the click to unfolding
    unfolded.append("span").attr("class","foldbutton").html("[–]").on("click", function(d) {foldComment(this);});
    unfolded.append("span").attr("class","username").text(data["author"]);
    unfolded.append("span").attr("class","points").text(writePoints(data));
    unfolded.append("p").html(writeComment(data) + "\n").append("a").attr("class","context").attr("target","_blank").attr("href",baselink + data["id"]).text("context");
    // Draw the folded version
    
    var folded = thisComment.append("div").attr("class","foldedCommentContent");
    folded.append("span").attr("class","unfoldbutton").text("[+]").on("click", function(d) {unfoldComment(this);})
    folded.append("span").attr("class", "foldedName").text(" " + writeFoldedComment(data));
    folded.append("span").attr("class","points").text(writePoints(data));
    
   if (data.replies != "")
    for (var i = 0; i < data["replies"]["data"]["children"].length; i++) {
        recursivelyDrawComments(unfolded, data["replies"]["data"]["children"][i]["data"], baselink);
    }
}

// Currently link->comment
function expandComment(d, a) {
    d3.json("http://www.reddit.com" + d + ".json", function(error, jsondata) {
            var topComment = jsondata[1]["data"]["children"][0]["data"];
            var baselink = "http://www.reddit.com" + jsondata[0].data.children[0].data.permalink;
            var p = d3.select(a.parentNode);
            p.select("a").remove();
            recursivelyDrawComments(p, topComment, baselink);            
        });
}

document.addEventListener("DOMContentLoaded", init);
