+++
date = 2019-04-21
linktitle = "How to use noebs"
excerpt = "We introduce noebs, a free open source payment gateway"

tags =  [
	"noebs",
	 "electronic-payment",
]
title = "Guides on how to deploy your noebs applications"
weight = 20
url = "/guides/use-noebs"
+++
## Why Go?

Go is really fast! Our application can happily serve more than 60k req/sec. The bottleneck will never be on your payment gateway service! Plus, Go helps with many of the problems I faced while working with Python, the static typing can prevent your errors from occurring only at runtime, and your code will compile into a single binary that you just run. I’ve been very excited to write web services Go and this project offers me just that!

# How to use noebs
There are different ways to use noebs:

## Building using Docker and docker-compose
We provide an easier way to build and run noebs using Docker.
- Fork this repository (e.g., `git clone https://github.com/adonese/noebs`)
- `cd` to noebs root directory (E.g., $HOME/src/noebs)
- `docker build -t noebs .`  # -t for giving it a name
- `docker run -it -p 8000:8000 noebs:latest`
- Open `localhost:8000/test` in your broswer to interact with noebs


## Building with go get command [not recommended]
- make sure you have Go installed [Consult go website to see various ways to install go](https://golang.org)
- Then
```shell
# this command may likely takes along time depending on your internet connections.
# also, make sure you are using a vpn since some of the libraries are hosted in GCE hosting which forbids Sudan
go get github.com/adonese/noebs
cd $GOPATH/github.com/adonese/noebs
go build .
```
You will have a binary that after running it will spawn a production ready server!

## Notes on installation
noebs needs to be connected with EBS merchant server in order to get useful responses. *However, you can run our embedded server that mocks EBS responses in cases where you cannot reach EBS server*. To do that, you need to enable the development mode using a special env var, `EBS_LOCAL_DEV`. You need to set `EBS_LOCAL_DEV=1` in order to use the mocking functionality.

- Using Docker
```shell
docker run -it -p 8000:8000 -e EBS_LOCAL_DEV=1 noebs:latest
```

- Using `go get` method
```shell
export EBS_LOCAL_DEV=1 noebs
```

# This project philosophy
noebs is not meant to be a full e-payment framework (e.g., unlike Morsal). It is meant as a generic e-payment gateway system. Currently, it implements EBS services, but we might add new gateway. Being such, adapts to Unix philosophy; doing one thing and do it good. Also, with our experience with embedded devices, working with authorizations and handling all of these headers and tokens (esp. JWT ones) has proven to be challenging as simply some of the older models cannot handle lengthy headers.
You can however have this system architecture, suppose that you're building a mobile payment application system:
- a mobile application app (with its backend system, obviously). This app will encapsulates the business logic and authenticate the incoming requests.
- a chatting service. Like WeChat, where people can send their money to their friends and families, in a very friendly way.
- ecommerce platform. The idea is _not_ just to offer an epayment gateway, well, EBS offers that through their MCS web services.
- and finally the payment gateway layer which handles the payment part.
- there could be other services e.g., push notifications, SMS, 2FA and plenty of others.
- logging and the reporting system.
- rate limiting, geographical blocking and other API gateway protections.
All of these will be implemented in a microservice archiectural design pattern, and it is your decision to choose what services you want. A mobile payment provider can use our payment service inside their application whenever their users are requesting any transactions. _It is not our responsibility to authenticate your users_. This way, we can use this application in virtually any place. Our client consumers are held responsible for providing any kind of authentication for their requests.


## Services we offer
noebs implements *ALL* of EBS merchant services. We are working to extend our support into other EBS services, e.g., consumer services, TITP, etc. However, those other services are not stable and some of them (consumer) are deem to deprecation.

If YOU are interested in other services, please reach out and we will be more than happy to discuss them with you.
