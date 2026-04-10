<?php

class Test {
    public string $prop {
        set => strtoupper($value);
    }
}

$test = new Test();
$test->prop = 'foo';
var_dump($test);

?>