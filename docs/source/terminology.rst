Terminology
===========

Terminology used when discussing test doubles has often been confused, historically. To alleviate confusion, at least within the scope of using the Doubles library, the following definitions are provided:

test double
  An object that stands in for another object during the course of a test. This is a generic term that describes all the different types of objects the Doubles library provides.
stub
  A test double that returns a predetermined value when called.
fake
  A test double that has a full implementation that determines what value it will return when called.
mock
  A test double that expects to be called in a certain way, and will cause the test to fail if it is not.
pure double
  A basic test double that does not modify any existing object in the system.
partial double
  A test double that modifies a real object from the production code, doubling some of its methods but leaving others unmodified.
verifying double
  A test double that ensures any methods that are doubled on it match the contract of the real object they are standing in for.
allowance
  A declaration that one of an object's methods can be called. This is the manner by which stubs are created.
expectation
  A declaration that one of an object's methods must be called. This is the manner by which mocks are created.

Examples of each of these are provided in the :doc:`usage` section.
