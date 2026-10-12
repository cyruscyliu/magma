<?php
[list(__FILE__ => $foo) = [__FILE__ => 'foo']];
var_dump($foo);
[[__FILE__ => $foo] = [__FILE__ => 'foo']];
var_dump($foo);
?>