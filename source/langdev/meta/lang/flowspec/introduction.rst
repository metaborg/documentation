Introduction
============

.. highlight:: flowspec

FlowSpec is a domain-specific meta-language for the specification of static control-flow and data-flow analysis over that control flow. We briefly explain these basic concepts. 

Control Flow Graphs
-------------------

Control-flow represents the execution order of a program. Depending on the input given to the program, or other things the program may observe of its execution environment (e.g. network communication, or a source of noise used to generate pseudo-random numbers), a program may execute a different trace of instructions. Since in general programs may not terminate at all, and humans are not very adapt at reasoning about possible infinities, we use a finite representation of possibly infinite program traces using control-flow graphs. 

`Control-flow graphs <https://en.wikipedia.org/wiki/Control_flow_graph>`__ are similarly finite as program text and are usually very similar, giving rise to a visual representation of the program. Loops in the program are represented as cycles in the control-flow graph, conditional code is represented by a split in control-flow which is merged again automatically after the conditional code. 

Data Flow Analysis over Control Flow Graphs
-------------------------------------------

Data-flow analysis propagates information either forward or backward along the control-flow graph. This can be information that approximates the data that is handled by the program, or the way in which the program interacts with memory, or something else altogether. 

Examples of data-flow analysis include `constant analysis <https://en.wikipedia.org/wiki/Constant_propagation>`__ which checks when variables that are used in the program are guaranteed to have the same value regardless of the execution circumstances of the program, or `live variables analysis <https://en.wikipedia.org/wiki/Live_variable_analysis>`__ which identifies if values in variables are actually observable by the program. 
