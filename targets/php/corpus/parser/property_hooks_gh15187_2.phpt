<?php

class Test {
    public int $prop { set => $value; }
}

$test = new Test();
var_dump($test);
foreach ($test as $key => $value) {
    var_dump($key, $value);
}

?>