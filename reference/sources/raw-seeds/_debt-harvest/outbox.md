Pattern: Transactional outbox


#### [Microservice Architecture](/index.html)

**Supported by [Kong](https://konghq.com/)**

* [Patterns](/patterns/index.html)
* [Articles](/articles/index.html)
* [Presentations](/presentations/index.html)
* [Adopt](/adopt/index.html)
* [Refactoring](/refactoring/index.html)
* [Testing](/testing/index.html)
* [Modernization Help](https://chrisrichardson.net/)

* [About](/about.html)

Pattern: Transactional outbox
=============================

[pattern](/tags/pattern) 

[transactional messaging](/tags/transactional%20messaging) 

[service design](/tags/service%20design) 

[inter-service communication](/tags/inter-service%20communication) 
  

---

Also known as
-------------

Application events

Context
-------

A service command typically needs to create/update/delete [aggregates](aggregate.html) in the database **and** send messages/events to a message broker.
For example, a service that participates in a [saga](/patterns/data/saga.html) needs to update business entities and send messages/events.
Similarly, a service that publishes a [domain event](domain-event.html) must update an [aggregate](aggregate.html) and publish an event.

The command must atomically update the database and send messages in order to avoid data inconsistencies and bugs.
However, it is not viable to use a traditional distributed transaction (2PC) that spans the database and the message broker
The database and/or the message broker might not support 2PC.
And even if they do, it’s often undesirable to couple the service to both the database and the message broker.

But without using 2PC, sending a message in the middle of a transaction is not reliable.
There’s no guarantee that the transaction will commit.
Similarly, if a service sends a message after committing the transaction there’s no guarantee that it won’t crash before sending the message.

In addition, messages must be sent to the message broker in the order they were sent by the service.
They must usually be delivered to each consumer in the same order although that’s outside the scope of this pattern.
For example, let’s suppose that an aggregate is updated by a series of transactions `T1`, `T2`, etc.
This transactions might be performed by the same service instance or by different service instances.
Each transaction publishes a corresponding event: `T1 -> E1`, `T2 -> E2`, etc.
Since `T1` precedes `T2`, event `E1` must be published before `E2`.

Problem
-------

How to atomically update the database and send messages to a message broker?

Forces
------

* 2PC is not an option. The database and/or the message broker might not support 2PC. Also, it’s often undesirable to couple the service to both the database and the message broker.
* If the database transaction commits then the messages must be sent. Conversely, if the database rolls back, the messages must not be sent
* Messages must be sent to the message broker in the order they were sent by the service. This ordering must be preserved across multiple service instances that update the same aggregate.

Solution
--------

The solution is for the service that sends the message to first store the message in the database as part of the transaction that updates the business entities.
A separate process then sends the messages to the message broker.

![](/i/patterns/data/ReliablePublication.png)

The participants in this pattern are:

* Sender - the service that sends the message
* Database - the database that stores the business entities and message outbox
* Message outbox - if it’s a relational database, this is a table that stores the messages to be sent. Otherwise, if it’s a NoSQL database, the outbox is a property of each database record (e.g. document or item)
* Message relay - sends the messages stored in the outbox to the message broker

Result context
--------------

This pattern has the following benefits:

* 2PC is not used
* Messages are guaranteed to be sent if and only if the database transaction commits
* Messages are sent to the message broker in the order they were sent by the application

This pattern has the following drawbacks:

* Potentially error prone since the developer might forget to publish the message/event after updating the database.

This pattern also has the following issues:

* The Message relay might publish a message more than once.
  It might, for example, crash after publishing a message but before recording the fact that it has done so.
  When it restarts, it will then publish the message again.
  As a result, a message consumer must be idempotent, perhaps by tracking the IDs of the messages that it has already processed.
  Fortunately, since message Consumers usually need to be idempotent (because a message broker can deliver messages more than once) this is typically not a problem.

Related patterns
----------------

* The [Saga](saga.html) and [Domain event](domain-event.html) patterns create the need for this pattern.
* The [Event sourcing](event-sourcing.html) is an alternative solution
* There are two patterns for implementing the Message relay:
  + The [Transaction log tailing](transaction-log-tailing.html) pattern
  + The [Polling publisher](polling-publisher.html) pattern

Learn more
----------

* My book [Microservices patterns](/book) describes this pattern in a lot more detail.
* The [Eventuate Tram framework](https://github.com/eventuate-tram/eventuate-tram-core) implements this pattern

---

[pattern](/tags/pattern) 

[transactional messaging](/tags/transactional%20messaging) 

[service design](/tags/service%20design) 

[inter-service communication](/tags/inter-service%20communication) 
  

---

---

[Modernization Help](https://chrisrichardson.net/)

Copyright © 2026 Chris Richardson • All rights reserved • Supported by [Kong](https://konghq.com/).

#### About Microservices.io

![](https://gravatar.com/avatar/a290a8643359e2495e1c6312e662012f)

Microservices.io is created by [Chris Richardson](/about.html), software architect, creator of the original CloudFoundry.com, and author of *Microservices Patterns*. Chris helps organizations modernize their architecture to enable fast flow and GenAI-powered software delivery.

#### Need help modernizing your architecture?

Avoid the trap of creating a modern legacy system — a new architecture with the same old problems.  
Contact me to discuss your modernization goals.

[Get Help](https://www.linkedin.com/in/pojos/)

#### Microservices Patterns, 2nd edition

![](/i/posts/mp2e-book-cover.png)

I am very excited to announce that the MEAP for the second edition of my book, Microservices Patterns is now available!

[Learn more](/post/architecture/2025/06/26/announcing-meap-microservices-patterns-2nd-edition.html)

#### ASK CHRIS

?

Got a question about microservices?

Fill in [this form](https://forms.gle/ppYDAF1JxHGec8Kn9). If I can, I'll write a blog post that answers your question.

#### NEED HELP?

![](/i/posts/cxo-wondering.webp)

I help organizations improve agility and competitiveness through better software architecture.

Learn more about my [consulting engagements](https://chrisrichardson.net/consulting.html), and [training workshops](https://chrisrichardson.net/training.html).

#### PREMIUM CONTENT

![](/i/posts/premium-logo.png)
Premium content now available for paid subscribers at [premium.microservices.io](https://premium.microservices.io).

#### MICROSERVICES WORKSHOPS

![](/i/workshop-kata_small.jpg)

Chris teaches [comprehensive workshops](http://chrisrichardson.net/training.html) for architects and developers that will enable your organization use microservices effectively.

Avoid the pitfalls of adopting microservices and learn essential topics, such as service decomposition and design and how to refactor a monolith to microservices.

[Learn more](http://chrisrichardson.net/training.html)

#### Remote consulting session

![](/i/posts/zoom-consulting.webp)

Got a specific microservice architecture-related question? For example:

* Wondering whether your organization should adopt microservices?
* Want to know how to migrate your monolith to microservices?
* Facing a tricky microservice architecture design problem?

Consider signing up for a [two hour, highly focussed, consulting session.](https://chrisrichardson.net/consulting-office-hours.html)

#### ASSESS your architecture

Assess your application's microservice architecture and identify what needs to be improved. [Engage Chris](http://www.chrisrichardson.net/consulting.html) to conduct an architect review.

#### LEARN about microservices

Chris offers numerous other resources for learning the microservice architecture.

#### Get the book: Microservices Patterns

Read Chris Richardson's book:
[![](/i/Microservices-Patterns-Cover-published.png)](/book)

---

#### Example microservices applications

Want to see an example? Check out Chris Richardson's example applications.
[See code](http://eventuate.io/exampleapps.html)

#### Virtual bootcamp: Distributed data patterns in a microservice architecture

![](/i/Chris_Speaking_Mucon_2018_a.jpg)

My virtual bootcamp, distributed data patterns in a microservice architecture, is now open for enrollment!

It covers the key distributed data management patterns including Saga, API Composition, and CQRS.

It consists of video lectures, code labs, and a weekly ask-me-anything video conference repeated in multiple timezones.

The regular price is $395/person but use coupon OFFEFKCW to sign up for $95 (valid until Sept 30th, 2025).
There are deeper discounts for buying multiple seats.

[Learn more](https://chrisrichardson.net/virtual-bootcamp-distributed-data-management.html)

#### Learn how to create a service template and microservice chassis

Take a look at my [Manning LiveProject](/post/patterns/2022/03/15/service-template-chassis-live-project.html) that teaches you how to develop a service template and microservice chassis.

![](/i/patterns/microservice-template-and-chassis/Microservice_chassis.png)

[Signup for the newsletter](http://visitor.r20.constantcontact.com/d.jsp?llr=ula8akwab&p=oi&m=1123470377332&sit=l6ktajjkb&f=15d9bba9-b33d-491f-b874-73a41bba8a76)

For Email Marketing you can trust.

#### BUILD microservices

Ready to start using the microservice architecture?

#### Consulting services

[Engage Chris](http://www.chrisrichardson.net/consulting.html) to create a microservices adoption roadmap and help you define your microservice architecture,

---

#### The Eventuate platform

Use the [Eventuate.io platform](https://eventuate.io) to tackle distributed data management challenges in your microservices architecture.

[![](https://eventuate.io/i/logo.gif)](https://eventuate.io)

Eventuate is Chris's latest startup. It makes it easy to use the Saga pattern to manage transactions and the CQRS pattern to implement queries.

---

Join the [microservices google group](https://groups.google.com/forum/#!forum/microservices)

Please enable JavaScript to view the [comments powered by Disqus.](https://disqus.com/?ref_noscript)