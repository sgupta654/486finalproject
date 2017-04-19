EECS 486: Information Retreival 
WINTER 17
Final Project: Reddit Subreddit Suggester
Elaine Apaza, Brian Lim, Sandeep Gupta, Scot Freysinger

This project is a subreddit suggester for the popular social media site, Reddit. 

The general algorithm involves three main components: a web crawler, PageRank algorithm, and vector space model implementation.

Crawler:

	*******NOT ALL OF THE CRAWLER CODE WAS WRITTEN BY US, ORIGINAL CRAWLER CAN BE FOUND AT THIS LINK: https://github.com/Skyyrunner/RedditSocialGrapher.git**********

	*******Our crawler is added code on top of the RedditSocialGrapher open source project*********

	Our crawler makes a simple request to the Reddit API for a particular subreddit in the following format:

	r = requests.get(r'http://www.reddit.com/r/%s/top.json?limit=100&t=week' % (sub_r), headers = headers)

	sub_r = target subreddit
	top.json - gets the top post
	limit=100 - limit number of posts from subreddit to 100 (max is 100)
	t=week - constraint posts to the past week

	When making a call to the Reddit API, it is important you place an UserAgent in the header:

		headers = {
            'User-Agent': "University project for subreddit suggester"
          }

    To individually run crawler, run:

    	python commentArchiver.py

    The crawler will store posts in the r/ directory

    To parse comments from the r/ directory, run:

    	python parseComments.py

Building PageRank:

	To build PageRank:

		python RedditRank.py userLinks.txt

Running whole application:

		python RedditSuggester.py

		-- Follow instruction on command line