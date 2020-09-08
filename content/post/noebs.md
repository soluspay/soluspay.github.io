+++
date = 2019-04-17
linktitle = "noebs: the most secure middleware"
excerpt = "We introduce noebs, a free open source payment gateway"

tags =  [
	"noebs",
	 "electronic-payment",
]
prev = "/tutorials/mathjax"
title = "noebs: the most secure middleware"
weight = 10
+++

>API-first, high performant middleware. noebs is the most secure and modern middleware.

# What is noebs

It is definitely not a replacement for EBS, if anything we embrace the use of EBS and its role as a unified switching system. But, we aim to provide a thin wrapper around EBS functionalities that can be exposed to both POS and mobile applications. A starting point where you can write your business logic. It is free and open source built using Go. noebs encapsulates many of the things I learned while working with a full fledged payment gateway. It is very fast and robust and doesn’t get on your way while using it. The design of noebs makes it very simple for the developers to work with and extend it. It is not opinionated, we assume that the developers know better what their business needs and tailor noebs to their requirements. You can add as much of other middlewares as you wish; be it a logger, sms gateway or any other service. We highly encourage you to adapt this microservice architecture, where the whole application is layered on top of each other’s.

## This project goals

Provide a highly scalable payment gateway that can handles tens of thousands of concurrent requests. Currently, we are only interfacing with EBS, but we plan to cover other private switches as well. It is also open source meaning you can use for free! We don’t have any hidden subscription fees or anything. Totally free and open source.

## Commercial plans

We do have commercial plans. In fact, we can help you in every part of your electronic payment system. You can use our hosted middleware service without the need of hosting it yourself.

- EBS simulator (you can use it in during your development phase)
- We also have QA developers that can help you during your tests. They’re as lame and bureaucratic as EBS ones are
- we can help you write your clients applications, whether they’re mobile, or POS
- we can assist and help you plan for your business model

For more details, contact us at mmbusif@gmail.com.


# Consultancy
While everything you see here is very and open source; we don't hide any fees or charges, we expect that some might be interested in a commercial plans. We offer our consultancy services via Gndi. We have a team with variety of proficiency, from backend engineers, mobile developers to UX/UI and QA testing engineers. Some of our team members have worked at EBS, while most of the team have a huge experience in e-payment systems.

Contact us: +249 925343834 (Mohamed Yousif) | +249 9023 00672 (Mohamed Gafar) | adonese@acts-sd.com (Mohamed Yousif)

# Our simulator and EBS services
Our team have developed an internal EBS QA test system that emulates EBS test environment. We offer our simulator as a paid service 
- very superior to that of EBS testing server. It runs on weekends. Well, 24/7, just like any server should work ¯\\_(ツ)\_/¯.
- hate EBS's bureaucracy? We do too. No need for the EBS busy servers, you can test our server at any time.
- we have two plans for the simulator: 
	- you can use our EBS simulator on your own; we won't test your services.
	- we can use our EBS simulator while we do the plan for you, the exact way EBS does. Bear in mind that our testers are highly competitive and they're all ex-EBSers.

**We plan on releasing our simulator very soon. Stay tuned.**
