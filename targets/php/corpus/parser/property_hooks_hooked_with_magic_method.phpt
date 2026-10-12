<?php

class Test {
    private $prop {
        get { echo __METHOD__, "\n"; return 42; }
        set { echo __METHOD__, "\n"; }
    }

    public function __get($name) {
        return $this->{$name};
    }

    public function __set($name, $value) {
        $this->{$name} = $value;
    }
}

$test = new Test;
$test->prop;
$test->prop = 42;

?>