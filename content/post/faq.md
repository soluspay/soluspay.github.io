+++
date = 2019-04-17
linktitle = "FAQ: your first support for any EBS issue"
url = "/faq/"
excerpt = "We introduce noebs, a free open source payment gateway"

tags =  [
	"noebs",
	 "electronic-payment",
     "faq",
     "ebs error"
]
prev = "/tutorials/mathjax"
title = "FAQ: your first support for any EBS issue"
weight = 10
+++


# List of common EBS errors and their meaninings

| error code | error meaning | how to solve |
|-------------|---------------|---------------|
| 196 | System error | regarding the pin block [see our post on pin block calculations](/post/pin_block) |
|000|	Approval	|
|103|	Format Error	| Invalid merchant or service provider|
|130| 	Invalid format	| The transaction has invalid format. After the transaction authorization, the terminal or external host will declined the response|
|178|	Original request not found	|Returned if the voucher is not found for the particular phone number sent on the request of cash out voucher, the phone number entered isn’t the same as the one used to generate the voucher  |
|158|	Invalid processing code|	|
|161|	Withdrawal limit exceeded	| |
|191| 	Destination not available|	The transaction destination (e.g. bank or biller) is unreachable, or didn't respond during timeout period. In case of timeout with a biller, there is a chance that biller provided actual service to customer, so debited amount won’t be reversed.|
|194|	Duplicate transaction|	|
|196|	System error	|Unexpected error occurred in the system|
|201|	Contact Card Issuer	|
|205|	External decline	|The external system, e.g. biller, has declined the transaction, usually because provided customer data are not accepted. E.g. wrong phone number for top-up transactions.|
|251|	Insufficient fund	|Customer doesn't have enough balance|
|281|	Wrong customer information	|Mostly used to indicate wrong customer payment info that is not accepted by the biller, or a missing parameter of the “PersonalPaymentInfo” field. |
|338|	PIN tries limit exceeded|	|
|355|	Invalid PIN|	PIN entered was wrong|
|375|	PIN Tries Limit Reached|	Customer reached the max allowed number of wrong PIN entries|
|362|	Encryption error|	For future use|
|389|	Invalid terminal ID|	|
|412|	Invalid transaction	|The transaction is not allowed for the profile of this customer|
|413|	Merchant limit exceeded	| |
|467|	Invalid amount	| |
|514|	Invalid track 2	| |
|536|	Restricted card	| Card status is "Restricted"|
|541|	Lost card	| |
|543|	Stolen card	| |
|550|	Closed card	| |
|552|	Declared card	| |
|554|	Expired card	| |
|600|	Invalid client Id	| |
|601|	Invalid Card Number Format	| |
|602|	Invalid Expiry Date Format	| |
|603|	Format Error |	There is a missing parameter of the transaction request, or invalid request in general.|
|604|	Invalid Currency Code	| | 
|605|	Invalid Account Format	| |
|606|	Invalid System Trace Audit Number Format |	|
|607|	Invalid Personal Payment Information Format	| |
|608|	Invalid Payee Identification	| |
|609|	Invalid Phone Number Format	| |
|610|	Invalid voucher number Format	| |
|611|	Invalid Transaction Date Format	| |
|615|	Invalid Service Id	| |
|616|	Invalid original transaction system trace audit number Format |	|
|617|	MCS Time out	| | 
|618|	This service cannot be reversed	Related to reversal service| |
|619|	Invalid Terminal Id Format	| |
|620|	Invalid PIN Format	| |
|621|	Invalid Amount Format	| |
|622|	Invalid Cash Back Amount Format	| |
|632|	MCS Invalid Cash out Transaction due to Invalid voucher length	| |
|633|	MCS invalid track2|	|
|923|	Could not send the OTP	| |
|934|	OTP expired  	| |
|935|	OTP tries limit exceeded  	| | 
|936|	Invalid  OTP  	| |
|636|	Invalid entityId  	| |
|637|	Invalid entityType  	| |
|638|	Invalid channelType  	| | 
|639|	OTP ChannelId (phoneNO) Not Found for this Entity	| |
|903|	No Data (OTP) found to be validated  	| |
|905|	OTP Operation Failed  	| |
|634|	Invalid OTP field   	| |
|635|	Invalid generated OTP id	| | 
|696|	MCS System Error	| |
