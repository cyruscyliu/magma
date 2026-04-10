<?php

class Test {
    var $prop { get => 42; }
}

$test = new Test();
var_dump($test->prop);

?>