# Virtual File System
Virtual File Systems are used to abstract different file systems in a uniform
way. IntelliJ IDEA uses it for its representation of project files, and
Metaborg Core uses it for uniform access to resources, regardless of where
they physically live.



## IntelliJ VFS
IntelliJ IDEA uses its own Virtual File System, whose main class is the
`VirtualFile` class. It captures a snapshot of the physical file which is
periodically synchronized. You can find more information [here][1] and
[here][2].

The textual content of a file is represented by a `Document`.
[More information][3].

A file may be part of a PSI tree. In that case the file is a `PsiFile`
([more information][4]) and it contains PSI elements ([more information][5]).
Think of the PSI tree as a mix between an Abstract Syntax Tree and a Parse Tree,
but it also extends outside the file to represent the project that contains
the file.

```eval_rst
.. note:: While `VirtualFile` has an `exists()` method that can be used to
   check whether a file exists, it's also possible for functions such as the
   following to return `null` when the file is not found::

       this.file = LocalFileSystem.getInstance().refreshAndFindFileByPath("/home/user/test.txt");

```


## Apache VFS
Metaborg Core uses [Apache Commons VFS][6], which despite the similar name and
function is completely different from IntelliJ's VFS. An implementation of the
Apache VFS for IntelliJ resides in the [`org.metaborg.intellij.vfs`][7] package.

The default scheme for the implementation is `intellij://`, and any IntelliJ VFS
virtual files are resolved to Apache VFS file objects in the `intellij://`
file system using the [default implementation][8] of the
[`IIntelliJResourceService`][9].


[1]: http://www.jetbrains.org/intellij/sdk/docs/basics/virtual_file_system.html
[2]: http://www.jetbrains.org/intellij/sdk/docs/basics/architectural_overview/virtual_file.html
[3]: http://www.jetbrains.org/intellij/sdk/docs/basics/architectural_overview/documents.html
[4]: http://www.jetbrains.org/intellij/sdk/docs/basics/architectural_overview/psi_files.html
[5]: http://www.jetbrains.org/intellij/sdk/docs/basics/architectural_overview/psi_elements.html
[6]: https://commons.apache.org/proper/commons-vfs/
[7]: https://github.com/metaborg/spoofax-intellij/tree/develop/org.metaborg.intellij/src/main/java/org/metaborg/intellij/vfs
[8]: https://github.com/metaborg/spoofax-intellij/blob/develop/org.metaborg.intellij/src/main/java/org/metaborg/intellij/resources/DefaultIntelliJResourceService.java
[9]: https://github.com/metaborg/spoofax-intellij/blob/develop/org.metaborg.intellij/src/main/java/org/metaborg/intellij/resources/IIntelliJResourceService.java
