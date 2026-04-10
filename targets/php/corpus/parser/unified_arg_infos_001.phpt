<?php

$o = new _ZendTestClass();
$o->testTmpMethodWithArgInfo(null);

echo new ReflectionFunction($o->testTmpMethodWithArgInfo(...));

?>