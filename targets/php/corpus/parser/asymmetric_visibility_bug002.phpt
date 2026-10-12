<?php

class C {
    public private(set) int $a = 1;
    public function __construct() {
        unset($this->a);
    }
}

class D extends C {
    public function __set($name, $value) {
        $this->a = $value;
    }
}

$c = new D();
try {
    $c->a = 2;
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
var_dump($c);

?>