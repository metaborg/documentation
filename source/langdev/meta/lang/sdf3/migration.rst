

Migrating SDF2 grammars to SDF3 grammars
----------------------------------------

The conversion of SDF2 (.sdf) or template language (.tmpl) files into
SDF3 can be done (semi) automatically.

For SDF2 files, it is possible to apply the Spoofax builder Lift to SDF3
to get a SDF3 file that corresponds to the SDF2 grammar. Another way of
doing that is to apply the same builder to a definition (.def) file (in
the include directory), that contains all SDF2 modules of your language.
The result is a list of SDF3 files corresponding to all modules of your
grammar. All SDF3 files are generated in the src-gen/sdf3-syntax
directory.

For template language files with deprecated constructors, you can also
apply the Lift to SDF3 builder, to convert the grammar into a SDF3
grammar in the src-gen/formatted directory.

Lift to SDF3 has two different versions: it can lift productions into
templates or it can lift it into productive productions. In the case of
wanting to have productive productions out of templates, the Extract
productions builder can be used.
