===========================
Test suites
===========================

Test cases in SPT are grouped in test suites (or modules).
Each SPT file contains exactly 1 test suite.

Test suites allow you to group together the test cases that test similar aspects of your language, making it easier to organize your tests.
They also allow you to reduce the size of your test cases by using configuration options like *headers* and *test fixtures* that apply to all test cases in the test suite.
We will describe those later on.

The syntax for a test suite is as follows::

	TestSuite = <
	  module <MODULENAME>
	  <Header?>
	  <TestFixture?>
	  <TestCase*>
	>


The modulename must start with a letter and can be followed by any number of letters, digits, underscores, and dashes.

If you are following along, you can create your first SPT test suite.
Just create a file with the extension ``.spt`` and paste the following::

	module my-first-test-suite
	
	language MyLanguageName

Be sure to replace ``MyLanguageName`` with the name of the language you want to test.
Also, feel free to use a more descriptive module name if you like.

Headers
-------------------------

Headers are a configuration option for all test cases in a test suite.
The most important header is the language header.
If you are following along with the example, you have already used it to specify which language you wanted to test.
All test cases in the test suite will be ran against the language you specify with the language header.
This language will be called the *language under test* (LUT)::

   Header.Language = <language <LANGNAME>>


For now, there is only one other header: the start symbol header.
This optional header allows you to specify a nonterminal from your grammar from which the test cases will be parsed.
Don't worry if that doesn't make any sense yet.
We will look at an example later::

   Header.StartSymbol = <start symbol <ID>>


Where the ``ID`` must start with a letter, and can be followed by any number of letters or digits.

As our example test suite already contains the language header, we will move on to writing our first test.

Test Cases
-------------------------

Test cases are the most important parts of SPT.
Each test case is a behaviorial test, or black-box test, for your language.
A behavioral test consists of a component that should be tested, an initial state for that component, input for that component, and the expected output after running the component on the input.

First, let's look at the input of a test case.
As we are testing languages, the input of a test case is always a program written in the language under test.
Such a program written in the language under test is called a *fragment*, and it is embedded in the SPT test suite.
In the future, we want to offer all editor services of your language under test (e.g., syntax highlighting) while you are writing such a fragment.
However, for now this is not yet supported.

The component that should be tested and the expected output are captured in *test expectations*.
We will discuss those in a later section.

Finally, the initial state of the test case can be specified in a *test fixture*, analogous to the JUnit ``setUp`` and ``tearDown`` methods.
These fixtures will also be discussed in a later section.

The syntax of test case is as follows::

	TestCase = <
	  test <Description> <OpenMarker>
	    <Fragment>
	  <CloseMarker>
	  <Expectation*>
	>

Where ``Description`` is the name of the test and can contain any character that is not a newline or ``[``.
The ``OpenMarker`` marks the start of the fragment and can be one of ``[[``, ``[[[``, or ``[[[[``.
The ``CloseMarker`` marks the end of the fragment and should be the counter part of the ``OpenMarker``, so either ``]]``, ``]]]``, or ``]]]]``.

The ``Fragment`` is a piece of text written in the language under test, about which we want to reason in our test case.
It may contain any sequence of characters that are not open- or closing markers.
For example, if the ``[[[`` and ``]]]`` markers are used, the fragment may contain at most 2 consecutive open or closing square brackets.
If the ``[[[[`` and ``]]]]`` markers are used, the fragment may contain at most 3 consecutive open or closing square brackets.

Parts of the fragment may be selected, by surrounding the text with the same open- and closing markers that were used to delimit the fragment. These *selections* can later be referred to in the test expectations to allow more precise reasoning about the fragment.

We will discuss selections and expectations later, but note that not supplying any test expectation is equivalent to supplying only a ``parse succeeds`` expectation, indicating that the fragment is expected to be valid syntax and parsing it with the language under test is expected to succeed without errors.

If you are following along with your own test suite, let's create our first test case.
I will be using a simplified version of Java (called MiniJava) as my language under test, but it shouldn't be too hard to write a simple test for your own language.
We will be writing a MiniJava program with valid syntax and test that it does indeed parse.
The input for our test case will simply be a main class in MiniJava.
The component that we will be testing is the parser, and the expected output is a successful parse result::

	module simple-parse-tests
	
	language MiniJava
	
	test check if this simple program parses sucessfully [[
	  class Main {
	    public static void main(String[] args) {
	      System.out.println(42);
	    }
	  }
	]] parse succeeds


Change the language header to refer to the name of your language and change the fragment to be a valid specification in your language, and you should have your first working test case.
Try messing up the syntax of your fragment and an error message should be displayed to indicate that the test failed, as the fragment failed to be parsed correctly.
These error messages can be displayed directly inside the fragment you wrote, to make it easier for you to spot why the test failed.
This is the power of SPT fragments!

Now that we know the basic structure of a test, we can already see how the start symbol header can be used to decrease the size of our test::

	module statement-parse-tests
	
	language MiniJava
	start symbol Statement
	
	test check if a printline is a valid statement [[
	  System.out.println(42);
	]]

Note how the fragment is now no longer a proper MiniJava program.
The test still passes, as the fragment is now parsed starting from the ``Statement`` nonterminal.
Note that this only works if ``Statement`` is exported as a start symbol in the MiniJava language.
These start symbols are a way of indicating what the initial state of the component under test should be.
In this case, it influences the state of the parser and only allows it to successfully parse statements.

Before we move on to discuss the set of all supported test expectations, we will first look at another way to influence the initial state and reduce the size of our test cases: test fixtures.

Test Fixtures
-------------------------

A test fixture offers a template for all test cases in the test suite.
Using test fixtures, you can factor out common boilerplate from your tests and write it only once.

The syntax for a test fixture is as follows::

	TestFixture = <
	  fixture <OpenMarker>
	    <StringPart>
	    <OpenMarker> ... <CloseMarker>
	    <StringPart>
	  <CloseMarker>
	>

Where the ``OpenMarker`` is one of ``[[``, ``[[[``, or ``[[[[``, and the ``CloseMarker`` is one of ``]]``, ``]]]``, or ``]]]]``.
The ``StringPart`` can contain any sequence of characters that is not an open- or closing marker, just like a fragment from a test.
However, unlike a fragment of a test, it can not contain selections.

For each test case, the fragment of the test will be inserted into the fixture at the marked location (``<OpenMarker> ... <CloseMarker>``), before the test expectations will be evaluated.

We can now use a test fixture to test the syntax of statements in MiniJava without the use of the start symbol header::

	module statements-parse-test
	
	language MiniJava
	
	fixture [[
	  class Main {
	    public static void main(String[] args) {
	      [[...]]
	    }
	  }
	]]
	
	test check if printing an integer is allowed [[
	  System.out.println(42);
	]]
	
	test check if printing a String is allowed [[
	  System.out.println("42");
	]]

Note that test fixtures offer a fully language implementation agnostic way of factoring out boiler plate code,
whereas the start symbol header requires knowledge of the non terminals of the language implementation.
