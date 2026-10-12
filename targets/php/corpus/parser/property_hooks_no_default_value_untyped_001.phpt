<?php

class Test {
    public $prop {
        get => $this->prop;
        set => $value;
    }
}

$test = new Test;
var_dump($test->prop);

?>