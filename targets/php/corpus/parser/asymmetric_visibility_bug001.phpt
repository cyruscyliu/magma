<?php

class C {
    public private(set) int $a = 1;
    public function __construct() {
        unset($this->a);
    }
}

class D extends C {
    public function __unset($name) {
        unset($this->a);
    }
}

$c = new D();
try {
    unset($c->a);
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
var_dump($c);

?>