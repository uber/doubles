Differences from Mock
=====================

If you've previously used the `Mock <http://www.voidspace.org.uk/python/mock/>`_ package, you may be wondering how **Doubles** is different and why you might want to use it. There are a few main differences:

* **Mock** follows what it describes as the "action --> assertion" pattern, meaning that you make calls to test doubles and then make assertions afterwards about how they are used. **Doubles** takes the reverse approach: you declare explicitly how your test doubles should behave, and any expectations you've made will be verified automatically at the end of the test.
* **Mock** has one primary class, also called Mock, which can serve the purpose of different types of test doubles depending on how it's used. **Doubles** uses explicit terminology to help your tests better convey their intent. In particulary, there is a clear distinction between a stub and a mock, with separate syntax for each.
* **Doubles** ensures that all test doubles adhere to the interface of the real objects they double. This is akin to **Mock**'s "spec" feature, but is *not* optional. This prevents drift between test double usage and real implementation. Without this feature, it's very easy to have a passing test but broken behavior in production.
* **Doubles** has a fluid interface, using method chains to build up a specification about how a test double should be used which matches closely with how you might describe it in words.
