<?php

function test(int $a, string &$b, Foo... $c) {}

echo new ReflectionFunction(test(...));

?>