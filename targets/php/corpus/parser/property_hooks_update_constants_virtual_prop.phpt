<?php

class Test {
    public $prop { get {} }
    public $prop2 = FOO;
}
define('FOO', 42);
$test = new Test;
var_dump($test->prop2);

?>