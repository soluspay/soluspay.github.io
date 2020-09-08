+++
date = 2019-04-20
linktitle = "Pin block calculations for EBS"
link = "pin_block"

tags =  [
	"noebs",
	 "electronic-payment",
     "faq",
     "ebs error",
     "pin block",
     "des",
     "dukpt",
     "authentication",

]
title = "Pin block calculations for EBS"
weight = 10
+++

In financial transactions, pin block calculations is one of the most important tasks and it's often a source for mistakes. In this article, we will be discussing pin block calculations in EBS system (it uses DES) while using our implementation, TA. 
[TA](https://beta.soluspay.net/pin) is written in Python and it is used internally by our team for all of our testing and pin calculations. The source code is also available in [Github](https://github.com/adonese/ta).

## Little about technology stach
We used a very interesting new-in-the town Python framework built on the new async, [Starlette](https://github.com/encode/starlette). Starlette and its server [uvicron](https://github.com/encode/uvicorn) are very interesting addition to Python world as they allow for high throughput, something was not easily achievable in Python before. The standardization of async framework is for the best interest of the language; people can focus their effort on one place. We are very excited about uvicorn and starlette and we couldn't have recommended them enough!

- we use Jinja2 as template engine
- gunicorn is used as application server (with uvicorn worker class)
- we use systemd for running the service (restart, etc)
- the whole application is running behind nginx server

We feel people might find it interesting or useful to know more about our infrastructure and what technologies we are using. We tried different technologies than the mentioned there; we tried to use `supervisor` instead of `systemd`, but `systemd` Just Works (TM). We have not experiement with any other python web server than gunicorn; I worked with uWSGI before and it was just hard to get it works (maybe because i used apache?). Gunicorn is as performant as uWSGI and more simplified. For all practical reasons, gunicorn is just better.
We use nginx as a reverse proxy and load balancer so that's that. Also, now the whole world is running nginx 🤷‍.

If you have any questions, please reach out and let us know! We also glad to hear from you!

