Differences from Mock
=====================

If you've previously used the `Mock <http://www.voidspace.org.uk/python/mock/>`_ package, you may be wondering how **dobles** is different and why you might want to use it. There are a few main differences:

* **Mock** follows what it describes as the "action --> assertion" pattern, meaning that you make calls to test dobles and then make assertions afterwards about how they are used. **dobles** takes the reverse approach: you declare explicitly how your test dobles should behave, and any expectations you've made will be verified automatically at the end of the test.
* **Mock** has one primary class, also called Mock, which can serve the purpose of different types of test dobles depending on how it's used. **dobles** uses explicit terminology to help your tests better convey their intent. In particulary, there is a clear distinction between a stub and a mock, with separate syntax for each.
* **dobles** ensures that all test dobles adhere to the interface of the real objects they double. This is akin to **Mock**'s "spec" feature, but is *not* optional. This prevents drift between test double usage and real implementation. Without this feature, it's very easy to have a passing test but broken behavior in production.
* **dobles** has a fluid interface, using method chains to build up a specification about how a test double should be used which matches closely with how you might describe it in words.
