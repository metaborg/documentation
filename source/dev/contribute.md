# Contributing to Spoofax
Thank you for your interest in contributing to Spoofax! We appreciate
any way in which you contribute.



## Bug Reports

> "If debugging is the process of removing bugs,
> then programming must be the process of putting them in."
> – Edsger W. Dijkstra

Unfortunately all but the most trivial software contains bugs. We'll try to fix them, but first
we need to know about them. Feel free to report bugs liberally, even if you're not sure if something
is a bug or not. If you can, please [search existing issues][1], as someone else may already have
reported the issue. However, we won't mind if you accidentally submit a duplicate bug report.

[Please file your issue here][2].

For an issue of Spoofax in IntelliJ IDEA, if you can, please include the `idea.log`
and `build-log/build.log` files. You can find them by clicking on menu _Help_ → _Show Log in Files_
menu, or by executing the _Show Log in Explorer_ action.



## Feature Requests
To request a feature for the Spoofax for IntelliJ IDEA plugin, you can also file an issue.

[Please file your feature request here][2].



## Pull Requests
You are welcome to implement a feature or fix a bug in Spoofax. We use
the _fork, branch and pull_ model described in [GitHub's documentation][3] for pull requests. First
you need to [fork][6] the relevant repository and clone it locally. Then create a new
topic branch, for example:

```bash
git checkout -b fix-rtl-languages
```

Now you work in this branch. Once you're done, you need to build and test your changes. See the
chapter on [building][5] for more information. Once everything succeeds, file a pull request as
described in the [GitHub documentation][3].



## Writing Documentation
The documentation needs to be kept up-to-date, and any improvements are very welcome. The
documentation you're reading now is generated from the documentation source files in our
[documentation repository][7]. Documentation pull requests function in the same way as code
pull requests. You can see your changes to the documentation in action by building it locally.
Follow the instructions in the [documentation's Readme][8] for more information.


[1]: http://yellowgrass.org/project/Spoofax
[2]: http://yellowgrass.org/createIssue/Spoofax
[3]: https://help.github.com/articles/using-pull-requests/
[5]: build.md
[6]: https://help.github.com/articles/fork-a-repo/
[7]: https://github.com/metaborg/documentation
[8]: https://github.com/metaborg/documentation/blob/master/README.md
