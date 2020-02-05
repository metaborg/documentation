============
Requirements
============

Spoofax can be run on macOS, Linux, and Windows. Building is directly supported on macOS and Linux. Building on Windows is supported through the `Windows Subsystem for Linux (Bash on Windows) <https://msdn.microsoft.com/en-us/commandline/wsl/install_guide>`_.

The following tools are required to build and develop Spoofax:


Git 1.8.2 or higher
  Required to check out the source code from our GitHub repositories. Instructions on how to install Git for your platform can be found here: http://git-scm.com/downloads.

  If you run macOs and have `Homebrew <http://brew.sh/>`_ installed, you can install Git by executing ``brew install git``. Confirm your Git installation by executing ``git version``.

Java JDK 8 or higher
  Required to build and run Java components. The latest JDK can be downloaded and installed from: http://www.oracle.com/technetwork/java/javase/downloads/index.html.

  On macOs, it can be a bit tricky to use the installed JDK, because Apple by default installs JRE 6. To check which version of Java you are running, execute the ``java -version`` command. If this tells you that the Java version is 1.8, everything is fine. If not, the Java version can be set with a command. After you have installed JDK, execute:

  .. code:: bash

      export JAVA_HOME=`/usr/libexec/java_home -v 1.8`

  .. note:: Such an export is not permanent. To make it permanent, add that line to :file:`~/.bashrc` or equivalent for your OS/shell (create the file if it does not exist), which will execute it whenever a new shell is opened.

  Confirm your JDK installation and version by executing ``java -version`` and ``javac -version``.

Python 3.4 or higher
  Python scripts are used to orchestrate the build. Instructions on how to install Python for your platform can be found here: https://www.python.org/downloads/.

  If you run macOs and have `Homebrew <http://brew.sh/>`__ installed, you can install Python by executing ``brew install python3``. Confirm your Python installation by executing ``python3 --version`` or ``python --version``, depending on how your package manager sets up Python.

Pip 7.0.3 or higher
  Pip is used to download some python dependencies. A version comes preinstalled with Python 3, but you need to make sure that you have version 7.0.3 or higher.

  To upgrade to the newest version use ``pip install --upgrade pip`` or ``pip3 install --upgrade pip``, depending on if your OS uses a different ``pip`` command for Python 3. Confirm using ``pip3 --version`` or ``pip --version``.

Maven 3.5.4 or higher (except Maven 3.6.1 and 3.6.2)
  Required to build most components of Spoofax. Our Maven artifact server must also be registered with Maven since the build depends on artifacts from previous builds for bootstrapping purposes. We explain how to install and set up Maven in the :ref:`next section <dev-maven>`.

  .. note:: Spoofax cannot be built using Maven 3.6.1 or 3.6.2 due to these bugs: https://issues.apache.org/jira/browse/MNG-6642 and https://issues.apache.org/jira/browse/MNG-6765
  
