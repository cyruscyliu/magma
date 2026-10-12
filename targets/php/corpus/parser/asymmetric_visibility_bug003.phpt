<?php

class C {
    public private(set) int $a = 1;
    public function __construct() {
        unset($this->a);
    }
}

$c = new C();
try {
    $c->a = 2;
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
try {
    unset($c->a);
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

?>