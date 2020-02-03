============================
Running SPT Tests
============================

SPT tests can be run different ways.
Each one corresponds to a different use case of SPT.
In the end, they all use the common core SPT Java API for extracting and executing tests.

We will now briefly discuss the different ways to run an SPT test suite based on the use case.
If you are new to SPT, the Interactive Test Design use case will be the one for you.

Interactive Test Design
----------------------------

SPT was originally designed for this use case.
Its goal was to lower the threshold of writing tests for your language, by allowing you to concisely declare test inputs and outputs, offering editor services for the fragments that you write, and providing you with real time in-editor feedback on whether your test fails or passes.

For this use case you would be using Eclipse with the Spoofax plugin.
When you open a test suite in the Eclipse editor, all failing test cases will have error markers on them.
By turning the test results into message markers inside the editor, we can provide you with a detailed location on where it went wrong. Especially for parsing or analysis errors.
However, to keep the error message readable, they can not contain full stack traces, which you might need to debug transformation or Stratego run tests.
It is also impractical to check all your test suites this way if you have many of them in your project.

To solve this, we have created a JUnit style test runner in Eclipse.
It is available through the ``Spoofax (meta)`` menu bar entry, and offers two ways to run tests.

The first one is called ``Run tests of SPT files``.
If you click this, it will check if you currently have an SPT file that is open and, if so, launch the test runner to run all tests in this file.
This mode can be useful if one of your tests is failing and you would like to see a more detailed error message.

The second entry is called ``Run all selected tests``.
It will check what you selected in the package or project explorer.
If you selected any SPT files, directories, or projects, it will scan **all** of the selected locations and run all of the SPT files it found within those selections.
This method is useful for running regression tests.

The user interface of the test runner consists of 3 parts.
The first part is the progress bar, which is followed by two numbers that indicate the progress of your current test runs.
This part is displayed at the top of the runner.
The second part is the overview of all the test suites and their test cases which are part of this test run.
This part is displayed in the bottom left.
The final part is a console window, which contains more detailed error messages about the test suite or test case you selected in the second part.
This part is displayed in the bottom right::

   !["SPT TestRunner Layout"](images/SPTTestRunner.png)

The test runner will start displaying any test suites and test cases within those test suites as soon as it discovers them.
Then, after they are all loaded, they will be executed one by one, and the progress bar at the top will increase.
As long as the progress bar remains green, no tests failed yet.
As soon as a single test fails, the progress bar will turn red to indicate so.

The numbers next to the progress bar also indicate the progress.
For example, ``5 / 7`` means 5 tests passed already out of a total of 7 tests.
This can mean that either 2 tests failed, or some tests have not been executed yet.
Which case applies can be determined by looking at the progress bar.

Any SPT files that fail can't be parsed or from which we can't extract test cases for some other reason, will be included in the list on the bottom left side, along with the test suites that did manage to get extracted.
The ones that did not extract properly will be displayed in red, as opposed to the default black color for test suites.
By selecting a red test suite, the extraction errors will be displayed in the console on the bottom right.
Any test suite can be double clicked to open the corresponding file in Eclipse.
Test suites that got extracted succesfully can be expanded if they contained any test cases.
This will show all the test cases of that suite as child elements of the test suite in the bottom left view.

Test cases are displayed in the default black color if they have not been executed yet.
Test cases that have finished will have their duration appended to their name.
Failed test cases are displayed in red, and passing test cases are displayed in green.
A red test case can be selected, doing so will show the messages about the test failure,
including the exceptions that caused them (e.g. a ``StrategoRuntimeException`` with a stacktrace) in the console on the bottom right.
Double clicking a test case will open the corresponding SPT file and jump to the location of the test case.

When a test case fails, the test suite that contained the failing test case will be appended with the number of failed tests in that test suite so far.


Run using the Command Line Runner
---------------------------------------

At https://github.com/metaborg/spt/tree/master/org.metaborg.spt.cmd there is a project that creates an executable jar with which you can run all the test suites in a given directory.
It is more of a proof of concept and an example of how to use our core SPT Java API than a full fledged test runner.

For those interested in giving it a try:

1. Obtaining the test runner jar::

    bash
    $ git clone https://github.com/metaborg/spt.git
    $ cd spt/org.metaborg.spt.cmd
    $ mvn package
    $ ls target/org.metaborg.spt.cmd*
      target/org.metaborg.spt.cmd-2.0.0-SNAPSHOT.jar

This jar is the executable jar that contains the test runner. Next up, we want to run the tests for our language. To do so, we need:

  1. the directory with tests to run (e.g., ``path/to/test/project``)
  2. the language under test (e.g. ``path/to/MiniJava/project``)
  3. the SPT language, to be able to extract the tests from the specification
  4. (Optionally) the Stratego language if we want to be able to execute the ``run`` or ``transform`` expectations

2. You should already have your tests and your language project, so next up is the SPT language.
   This is in the same repo as the command line runner::

     $ cd spt/org.metaborg.meta.lang.spt
     $ mvn verify

3. If you want to use the ``run`` and ``transform`` expectations, you also need the Stratego language::

     $ git clone https://github.com/metaborg/stratego.git
     $ cd stratego/org.metaborg.meta.lang.stratego
     $ mvn verify

4. Now we can run the tests::

	  $ java -jar spt/org.metaborg.spt.cmd/target/org.metaborg.spt.cmd-2.0.0-SNAPSHOT.jar -h
	  Usage: <main class> [options]
	    Options:
	      --help, -h
	         Shows usage help
	         Default: false
	      --lang, -ol
	         Location of any other language that should be loaded
	         Default: []
	    * --lut, -l
	         Location of the language under test
	    * --spt, -s
	         Location of the SPT language
	      --start-symbol, -start
	         Start Symbol for these tests
	    * --tests, -t
	       Location of test files
	  $ java -jar spt/org.metaborg.spt.cmd/target/org.metaborg.spt.cmd-2.0.0-SNAPSHOT.jar
	     --lut /path/to/MiniJava/project
	     --tests /path/to/test/project
	     --spt spt/org.metaborg.meta.lang.spt
	     --lang stratego/org.metaborg.meta.lang.stratego


Run using the SPT Framework
---------------------------------

The SPT framework at https://github.com/metaborg/spt offers a Java API to run SPT test suites.
The framework is split between the generic part (``org.metaborg.mbt.core`` - MetaBorg Testing (MBT)) and the Spoofax specific part (``org.metaborg.spt.core`` SPoofax Testing (SPT)).

The first step in running tests is to extract them from an SPT test suite.
``org.metaborg.mbt.core`` provides a Java object model to represent SPT test cases.
To extract test cases from a test suite to the Java model, you can use the ``ITestCaseExtractor``.
You can either implement this for your own version of the SPT language, or use our SPT language (``org.metaborg.meta.lang.spt``) and our extractor (``ISpoofaxTestCaseExtractor``).

Now that you have the tests in Java objects, you can execute them with the ``ITestCaseRunner``.
If the language you are testing is not integrated with Metaborg Core, you will either have to do so and subclass the ``TestCaseRunner``, or make your own implementation for the ``ITestCaseRunner``.
If your language under test *is* integrated with Metaborg Core (this is the case for all languages created with Spoofax), you can use our ``ISpoofaxTestCaseRunner``.

For an example on how to use dependency injection to obtain the correct classes and extract and run SPT tests using the Java API, see the ``TestRunner`` class at (https://github.com/metaborg/spt/tree/master/org.metaborg.spt.core).

Run using Maven
-------------------------

For regression testing and continuous integration, it can be useful to be able to execute tests from a maven build.
To do so, create a pom.xml file in your test project with the following content::

	<?xml version="1.0" encoding="UTF-8"?>
	<project
	  xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd"
	  xmlns="http://maven.apache.org/POM/4.0.0"
	  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	>
	  <modelVersion>4.0.0</modelVersion>
	  <groupId>your.group.id</groupId>
	  <artifactId>your.test.project.name</artifactId>
	  <version>0.0.1-SNAPSHOT</version>
	  <packaging>spoofax-test</packaging>
	
	  <parent>
	    <groupId>org.metaborg</groupId>
	    <artifactId>parent.language</artifactId>
	    <version>2.1.0-SNAPSHOT</version>
	  </parent>
	
	  <dependencies>
	    <dependency>
	      <groupId>your.group.id</groupId>
	      <artifactId>your.language.under.test.id</artifactId>
	      <version>1.0.0-SNAPSHOT</version>
	      <type>spoofax-language</type>
	    </dependency>
	    <dependency>
	      <groupId>org.metaborg</groupId>
	      <artifactId>org.metaborg.meta.lang.spt</artifactId>
	      <version>${metaborg-version}</version>
	      <type>spoofax-language</type>
	      <scope>test</scope>
	    </dependency>
	  </dependencies>
	
	  <build>
	    <plugins>
	      <plugin>
	        <groupId>org.metaborg</groupId>
	        <artifactId>spoofax-maven-plugin</artifactId>
	        <version>${metaborg-version}</version>
	        <configuration>
	          <languageUnderTest>your.group.id:your.language.under.test.id:1.0.0-SNAPSHOT</languageUnderTest>
	        </configuration>
	      </plugin>
	    </plugins>
	  </build>
	</project>


You should now be able to execute the tests with ``mvn verify``.