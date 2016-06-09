# SPT

The SPoofax Testing language (SPT) allows language developers to test their language in a declarative way.
It offers a language to express test cases for any textual language that you want to test, and a framework for executing those tests on language implementation created with Spoofax.

We will first describe the syntax and semantics of the SPT language.
Then, we will discuss how you can execute your SPT test cases, and finally we conclude with an overview of the architecture of the SPT framework.

## Syntax and Semantics of SPT

In this section we will describe the syntax and semantics of SPT.

If you want to write your own tests you can follow along as the different concepts are explained.
We suggest using the Spoofax Eclipse plugins, as they contain an editor for SPT files.
In an Eclipse with Spoofax installed, simply create a new file with the extension `.spt` and follow along to create your first SPT test suite.

### Test suites

Test cases in SPT are grouped in test suites (or modules).
Each SPT file contains exactly 1 test suite.

Test suites allow you to group together the test cases that test similar aspects of your language, making it easier to organize you tests.
They also allow you to reduce the size of your test cases by using *headers* and *test fixtures* that apply to all test cases in the test suite.

The syntax for a test suite is as follows:
```
TestSuite = <
  module <MODULENAME>
  <Header+>
  <TestFixture?>
  <TestCase*>
>
```

The modulename must start with a letter and can be followed by any number of letters, digits, underscores, and dashes.

If you are following along, you can create your first SPT test suite.
Just create a file with the extension `.spt` and paste the following:
```
module my-first-test-suite

language MyLanguageName
```
Be sure to replace `MyLanguageName` with the name of the language you want to test.
Also, feel free to use a more descriptive module name if you like.

### Headers

Headers supply information for all the test cases in a test suite.

The only mandatory header is the language header.
The language header specifies which language you want to test.
This language will be called the *language under test* (LUT).

```
Header.Language = <language <LANGNAME>>
```

For now, there is only one other header: the start symbol header.
This optional header allows you to specify a nonterminal from your grammar from which the test cases will be parsed.
We will look at an example later.

```
Header.StartSymbol = <start symbol <ID>>
```

Where the `ID` must start with a letter, and can be followed by any number of letters or digits.

As our example test suite already contains the language header, we will move on to writing our first test.

### Test Cases

A test case in SPT consists of a name, a *fragment* written in the language under test, and a set of *test expecations* that declare what you want to do with the fragment and what you expect to happen.

```
TestCase = <
  test <Description> <OpenMarker>
    <Fragment>
  <CloseMarker>
  <Expectation*>
>
```

Where `Description` is the name of the test and can contain any character that is not a newline or `[`.
The `OpenMarker` marks the start of the fragment and can be one of `[[`, `[[[`, or `[[[[`.
The `CloseMarker` marks the end of the fragment and should be the counter part of the `OpenMarker`, so either `]]`, `]]]`, or `]]]]`.

The `Fragment` is a piece of text written in the language under test, about which we want to reason in our test case.
It may contain any sequence of characters that are not open- or closing markers.
For example, if the `[[[` and `]]]` markers are used, the fragment may contain at most 2 consecutive open or closing square brackets.
If the `[[[[` and `]]]]` markers are used, the fragment may contain at most 3 consecutive open or closing square brackets.

Parts of the fragment may be selected, by surrounding the text with the same open- and closing markers that were used to delimit the fragment. These selections can later be referred to in the test expectations to allow more precise reasoning about the fragment.

We will discuss the `Expectation` later, but note that not supplying any test expectation is equivalent to supplying only a `parse succeeds` expectation, indicating that the fragment was expected to be valid syntax and parsing it with the language under test is expected to succeed without errors.

If you are following along with your own test suite, let's create our first test case.
I will be using a simplified version of Java (called MiniJava) as my language under test, but it shouldn't be too hard to write a simple test for your own language.
We will be writing a MiniJava program with valid syntax and test that it does indeed parse.

```
module simple-parse-tests

language MiniJava

test check if this simple program parses sucessfully [[
  class Main {
    public static void main(String[] args) {
      System.out.println(42);
    }
  }
]]
```

Change the language header to refer to the name of your language and change the fragment to be a valid specification in your language, and you should have your first working test case.
Try messing up the syntax of your fragment and an error message should be displayed, to indicate that the test failed, as the fragment failed to be parsed correctly.

Now that we know the basic structure of a test, we can already see how the start symbol header can be used to decrease the size of our test:
```
module statement-parse-tests

language MiniJava
start symbol Statement

test check if a printline is a valid statement [[
  System.out.println(42);
]]
```

Note how the fragment is now no longer a proper MiniJava program.
The test still passes, as the fragment is now parsed starting from the `Statement` non terminal.

Before moving on to a list of all supported test expectations, we will first look at another way to reduce the size of our test cases: test fixtures.

### Test Fixtures

A test fixture offers a template for all test cases in the test suite.
Using test fixtures, you can factor out common boilerplate from your tests and write it only once.

The syntax for a test fixture is as follows:
```
TestFixture = <
  fixture <OpenMarker>
    <StringPart>
    <OpenMarker> ... <CloseMarker>
    <StringPart>
  <CloseMarker>
>
```

Where the `OpenMarker` is one of `[[`, `[[[`, or `[[[[`, and the `CloseMarker` is one of `]]`, `]]]`, or `]]]]`.
The `StringPart` can contain any sequence of characters that is not an open- or closing marker, just like a fragment from a test.
However, unlike a fragment of a test, it can not contain selections.

For each test case, the fragment of the test will be inserted into the fixture at the marked location (`<OpenMarker> ... <CloseMarker>`), before the test expectations will be evaluated.

We can now use a test fixture to test the syntax of statements in MiniJava:
```
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
```

Note that test fixtures offer a fully language implementation agnostic way of factoring out boiler plate code,
whereas the start symbol header requires knowledge of the non terminals of the language implementation.

### Test Expectations

We have already briefly mentioned that a test case without any test expectations, is the same as a test case with a `parse succeeds` expectation.
We will now list the syntax and semantics of all the currently supported test expectations:

#### Parse Expectations

- `Expectation.ParseSucceeds = <parse succeeds>`  
  Parse the fragment and expect the parsing to succeed.
- `Expectation.ParseFails = <parse fails>`  
  Parse the fragment and expect the parsing to fail (i.e., produce an error).
- `Expectation.ParseToAterm = <parse to <ATerm>>`  
  Parse the fragment, expect parsing to succeed, and compare it to the given ATerm AST.
  When using test fixtures, the ATerm should only be the AST of the fragment of the test, not of the entire test fixture.
- `Expectation.ParseToFragment = <parse to <Language?> <OpenMarker> <Fragment> <CloseMarker>]]>`  
  Parse the fragment, expect parsing to succeed, and compare it to the result of parsing the given `Fragment` with the given `Language`.
  When the `Language` is omitted the language under test will be used to parse the given fragment.
  When using test fixtures, only the test's fragment will be combined with the test fixture.
  The fragment in this expectation will **not** be combined with it, even if the language under test is used to parse it.
  To counteract this, the entire AST (including the nodes from the fixture) will be compared to the expectation's fragment's AST.

#### Analysis Expectations

##### Analysis Message Expectations

Analysis message expectations will parse the fragment and expect parsing to succeed.
Then, the parse result will be analyzed (e.g., name and type analysis and static error checking).
Finally, the resulting messages will be compared to the expectation.
Note that, when test fixtures are present, all analysis messages within the fixture will be ignored.
Only the messages within the test's fragment will be compared to the expectation.

- `Expectation.OneError = <1 error>`  
  `Expectation.Errors = <<INT> errors>`  
  These expectations will check if the number of error messages generated by the analysis matches the given number.
  Any other messages (warnings, notes, and messages in the test fixture) will be ignored by this expectation.
- `Expectation.OneWarning = <1 warning>`  
  `Expectation.Warnings = <<INT> warnings>`  
  These expectations will check if the number of warning messages generated by the analysis matches the given number.
  Any other messages (errors, notes, and messages in the test fixture) will be ignored by this expectation.
- `Expectation.OneNote = <1 note>`  
  `Expectation.Notes = <<INT> notes>`  
  These expectations will check if the number of note messages generated by the analysis matches the given number.
  Any other messages (warnings, errors, and messages in the test fixture) will be ignored by this expectation.
- Any of the above expectations may be followed by the `at` keyword and a list of one or more comma separated references to selections of the test's fragment: `#<INT>, #<INT>, #<INT>, ...`.
  This will cause SPT to check if the specified messages appeared at the location of the given selection references.
  It is allowed to give less selection references than the number of expected messages.
  In this case SPT assumes you don't care about the location of the other messages.

  Let's look at an example to illustrate this:
  ```
  module analysis-tests
  
  language MiniJava
  
  fixture [[
    class Main {
      public static void main(String[] args) {
        System.out.println(42);
      }
    }
    [[...]]
  ]]
  
  test check error on duplicate class names [[
    class [[A]] {}
    class [[A]] {}
  ]] 2 errors at #1, #2
  ```
  Note the use of open- and closing markers to select the locations where the errors are expected to occur.
  Also note that references to selections start at 1 being the first selection in the fragment.

##### Name Analysis Expectations

Name analysis expectations will check if use sites can be resolved and, if required, if they resolve to the correct definition.
The fragment will be parsed, and parsing will be expected to succeed.
The fragment will be analyzed, but any number and severity of analysis messages is allowed.

- `Expectation.Resolve = <resolve #<INT>>`  
  Try to resolve the AST node at the given selection. Expect it to successfully resolve to any definition site.
- `Expectation.ResolveTo = <resolve #<INT> to #<INT>>`  
  Try to resolve the AST node at the first given selection. Expect it to successfully resolve to the location marked by the second given selection.

Note that selections can only occur in the test's fragment, not in the test fixture.
So name analysis can only be tested within a test's fragment.

#### Transformation Expectations

A transformation transforms an AST to another AST.
The idea within Spoofax is that a transformation has a name, and can be nested within a structure of menu's.
Furthermore, it can have additional information about whether it transforms the raw AST (i.e. the parse result) or the analyzed AST (i.e. the result of desugaring and analysis).
In languages created with Spoofax, transformations are Stratego strategies that are registered in the `Menus.esv` file.

Transformation expectations will first look up a given transformation using the name under which it was registered.
Note that, for Spoofax languages, this is *not* necessarily the name of the Stratego strategy, but the name under which it is registered in the `Menus.esv` file.
If this name is not unique, the menu structure can be used to look up the proper transformation.

Once the transformation is found, SPT will determine if it requires the raw AST, or the analyzed AST.
If the raw AST is required, it will only parse the fragment, expecting parsing to succeed.
If the analyzed AST is required, it will also analyze the parse result.
However, analysis is allowed to produce any number and severity of messages.
Then, SPT will run the transformation on the entire AST, **including** the nodes from the test fixture, if there was one.

- `Expectation.TransformToAterm = <transform <STRING> to <ATerm>>`  
  The `STRING` should be delimited by double quotes and contain the name of the transformation.
  If the name is not unique, the menu structure can be included as well, seperated by `->`.
  For example: `transform "Menu name -> transformation name" to Some(Result())`.

  The result of the transformation is compared to the given AST.
- `Expectation.TransformToFragment = <transform <STRING> to <Language?> <OpenMarker> <Fragment> <CloseMarker>>`  
  Does the same as `TransformToAterm`, but compares the result of the transformation to the AST of the given fragment.
  If the applied transformation required the raw AST, the given fragment will only be parsed with the given language.
  If no language is given, the language under test will be used.
  If the applied transformation required an analyzed AST, the given fragment will be parsed and analyzed.

#### Other Expectations

##### Run Stratego Expectations

These test expectations are really only applicable to languages that use Stratego strategies in their implementation.
They will parse and analyze the fragment and run a given Stratego strategy (with no arguments) and compare its output to the expectation.

- `Expectation.Run = <run <STRATEGY>>`  
  This expectation will lookup the given strategy name and run it on the AST node in the test's fragment.
  If the fragment contains multiple nodes (e.g., it's a list of Statements but some Statements were in the test fixture) the strategy will be run on each of these nodes. Either until it completes successfully, or until it failed on all these nodes.

  Note that it wil **not** be executed on the nodes in the test fixture, if there was one.
- `Expectation.RunOn = <run <STRATEGY> on #<INT>>`  
  This expectation does the same as `Run`, except it runs the strategy on the nodes at the given selection instead of the nodes of the test's fragment.
- `Expectation.RunToAterm = <run <STRATEGY> to <ATerm>>`  
  `Expectation.RunToAtermOn = <run <STRATEGY> on #<INT> to <ATerm>>`  
  These expectations are similar to the first two, but they require the result of running the strategy to match the given AST.
- `Expectation.RunToFragment = <run <STRATEGY> to <Language?> <OpenMarker> <Fragment> <CloseMarker>>`  
  `Expectation.RunToFragmentOn = <run <STRATEGY> on #<INT> to <Language?> <OpenMarker> <Fragment> <CloseMarker>>`  
  These expectations are similar to the first two, but they require the result of running the strategy to match the result of analyzing the given fragment with the given language.
  If no language is given, the language under test is used.

##### Origin Location Expectations

- `Expectation.HasOrigins = <has origin locations>`  
  This expectation parses and anlyzes the fragment and expects parsing to succeed.
  Analysis may return any number and severity of messages.

  It then checks if all AST nodes in the test's fragment (except for Lists in Spoofax) have a source region (an origin) associated with them.
  It does **not** check the AST nodes in the test fixture.
  
  When using Spoofax, there are some strategies that will break the origin information when used.
  This can lead to desugarings that create AST nodes without origin information, which can cause problems when trying to create messages at their location and with other services.
  This expectation can be used to check that your analysis is origin preserving.

```eval_rst
.. todo:: This part of the documentation has not been written yet.
```
