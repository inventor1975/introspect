# stubs — API surface only, for the corpus compile check

Minimal signatures of javax.servlet, Spring (web, jdbc, http, stereotype), commons-text/lang3, the OWASP
Java Encoder and ESAPI, so every case in `../cases/` can be checked with `javac` without downloading jars:

    javac -d /tmp/blind-out -sourcepath java2zfl/blind/stubs $(find java2zfl/blind/cases -name '*.java')

Bodies are placeholders (escapers return their argument); nothing here runs. Not part of the analyzed corpus.
