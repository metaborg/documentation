# Directory structure migration

To clean up the structure of a language specification project, we've made the following changes:

* ESV
  * Main ESV file must be at <span class='file'>editor/Main.esv</span>. If it does not exist, no packed ESV file will be generated.
  * Packed ESV file: <span class='file'>target/metaborg/editor.esv.af</span>
* SDF
  * The RTG and signatures files are no longer generated for SDF3 projects, since SDF3 generates its own signatures.
  * The generated box pp files are no longer generated, and box pp files are no longer converted into pp.af files.
  * Definition: <span class='file'>src-gen/syntax/[LanguageName].def</span>
  * Permissive definition: <span class='file'>src-gen/syntax/[LanguageName]-permissive.def</span>
  * Parenthesizer: <span class='file'>src-gen/pp/[LanguageName]-parenthesize.str</span>
  * Parse table: <span class='file'>target/metaborg/sdf.tbl</span>
* Stratego
  * 'editor-common.generated' file: <span class='file'>src-gen/stratego/metaborg.str</span>
  * Ctree: <span class='file'>target/metaborg/stratego.ctree</span>
  * Generated Java files: <span class='file'>src-gen/stratego-java</span>
  * JAR: <span class='file'>target/metaborg/stratego.jar</span>
  * Java strategies: <span class='file'>src/main/strategies</span>
  * Java strategies JAR: <span class='file'>target/metaborg/stratego-javastrat.jar</span>
  * Build cache: <span class='file'>target/stratego-cache</span>
* DynSem
  * Manual Java: <span class='file'>src/main/ds</span>
  * Generated Java: <span class='file'>src-gen/ds-java</span>
* Other
  * Pluto build cache: <span class='file'>target/pluto</span>

To migrate your project, make the following changes:

* Change the file name of the main ESV file to <span class='file'>Main.esv</span>, and change its module to `Main`.
* In the main ESV file:
  * Change the parse table:
    ```esv
    table : target/metaborg/sdf.tbl
    ```
  * Change the Stratego providers
    * For ctree projects:
      ```esv
      provider : target/metaborg/stratego.ctree
      ```
    * For jar projects:
      ```esv
      provider : target/metaborg/stratego.jar
      ```
    * For projects with Java strategies:
      ```esv
      provider : target/metaborg/stratego.jar
      provider : target/metaborg/stratego-javastrat.jar
      ```
* In all Stratego, NaBL, TS files
  * Instead of importing `lib/editor-common.generated`, import `stratego/metaborg`.
  * Instead of importing `include/<langname>-parenthesize`, import `pp/<langname>-parenthesize`.
  * If you're using SDF3:
    * Instead of importing the signatures from `include/<langname>`, import them from `signatures/<langname>-sig`. These signatures are spread over multiple files, import all the required files to fix errors, since the Stratego editor does not handle transitive imports. You can also use the wildcard import `signatures/-` to import all signature files, if your syntax definition is not spread over multiple directories.
  * If you're using SDF2 or an external definition file:
    * Instead of importing the signatures from `include/<langname>`, import them from `signatures/<langname>`.
* If your project has Java strategies:
  * Create the <span class='file'>src/main/strategies</span> directory.
  * Move Java strategies from <span class='file'>editor/java</span> into the <span class='file'>src/main/strategies</span> directory. Be sure to preserve the existing Java package structure.
* If your project has manual DynSem Java files:
  * Create the <span class='file'>src/main/ds</span> directory.
  * Move manual DynSem Java files from <span class='file'>editor/java</span> into the <span class='file'>src/main/ds</span> directory. Be sure to preserve the existing Java package structure.
* Perform a Maven update by right clicking the project and choosing <span class='menuselection'>Maven ‣ Update Project...</span>, to update the Java source directories of the project.
* If you are still using SDF2 instead of SDF3, add the following setting to the <span class='file'>metaborg.yaml</span> file:
```yaml
language:
  sdf:
    version: sdf2
```
