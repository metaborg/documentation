## Audiences and requirements

* Language developers
    * Setup
        * In Eclipse
        * In IntelliJ
    * Language development
        * Configuration
        * Syntax
        * Static semantics
        * Transformation
    * Export language
        * As Eclipse plugin
            * Customizing the Eclipse plugin
        * As IntelliJ plugin
            * Customizing the IntelliJ plugin
        * As custom library/application using the core API
            * Bundling/loading the language implementation
            * Running the compiler
            * Parsing
            * Analysis
            * Custom
        * With Sunshine
            * Command-line interface
            * Server interface
    * Language composition
        * Base language with extensions (source composition)
        * Multiple back-ends (dynamic composition)
        * Adding a builder to an existing language
    * Continuous integration
        * Maven build
        * Gradle build
* Tool developers
    * Integration of parsing, analysis, etc. tools into MetaBorg core
    * How to write a tool plugin
    * How to fork and integrate a tool if plugin is not possible
* Platform developers
    * Integration into another editor or IDE platform
    * What needs to be implemented and how to do that
* Workbench developers
    * Instantiating MetaBorg core with a set of tools to develop a new workbench
    * What needs to be implemented and how to do that
    * Instantiating various platforms with their implementations
        * MetaBorg core
        * Eclipse plugin
        * IntelliJ plugin
        * Maven plugin
        * Gradle plugin
        * Sunshine
* Core developers
    * MetaBorg/Spoofax core framework developers
* End-users
    * Use a language made with Spoofax
