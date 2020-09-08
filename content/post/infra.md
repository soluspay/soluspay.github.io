+++
date = 2019-04-27
linktitle = "noebs technology stack"
excerpt = "We introduce noebs, a free open source payment gateway"

tags =  [
	"noebs",
	 "electronic-payment",
]
title = "noebs technology stack"
weight = 20
url = "/infra"
+++

noebs supports interesting technologies that makes it the best in class solution. We support HTTP/2, server push (for live dashboard updates). It comes with Redis support and optional classical DB (you can use sqlite, mysql, and postgres). Resiliency and database distributions are first class citizen. When using proper setup, you can scale upto how your load balancer can handle. We use nginx as a reverse proxy and load balancer, and using this awesome setup we were able to scale to multiple servers without changing a single line of code in noebs.

# Technology stack
noebs is written in Go, with gin as a router. We experienced a lot of productivity boost while using Go and that encouraged us to adopt Go for our other backend projects.

We use nginx as a reverse proxy to application server. nginx gives a nice separation of concerns; the application doesn't need to care about things like access log and security. This also helps our team to be more productive as now each task can be handled by different team members.

In short, noebs uses these technologies:

- is written in Go using gin framework
- we use Gorm for its ORM features (but lots of queries are written in SQL)
- we use sqlite3 as a persistent storage layer (database)
- we also use redis and we are willing to replace all of Gorm/sqlite with it
- nginx is used as a reverse proxy and it handles securtiy, TLS certificates as well as authentication


## API first
noebs is an API-first middleware. Every response is of type `application/json`, and this is really important. Using a universal-easy to parse responses will allow noebs consumers to easily interact and handle our responses. Parsing json is a lot easier (and widely supported) than text/html. And this is for all of our responses, including `404, 401, 400` as well.

This is quite what noebs is all about. Simplicity built-in.

Next blog post will be about our deployment practices. Stay tuned for more open source noebs!