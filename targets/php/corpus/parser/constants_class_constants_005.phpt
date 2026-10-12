<?php
define ("A", "." . ord(2) . ".");
eval("class A {const a = A;}");
var_dump(A::a);
?>