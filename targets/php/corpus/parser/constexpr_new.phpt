<?php

try {
    eval('static $a = new DoesNotExist;');
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

static $b = new stdClass;
var_dump($b);

try {
    eval('static $c = new stdClass([] + 0);');
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

class Test {
    public function __construct(public $a, public $b) {}
}

try {
    eval('static $d = new Test(new stdClass, [] + 0);');
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

static $e = new Test(new stdClass, 42);
var_dump($e);

class Test2 {
    public function __construct() {
        echo "Side-effect\n";
        throw new Exception("Failed to construct");
    }
}

try {
    eval('static $f = new Test2();');
} catch (Exception $e) {
    echo $e->getMessage(), "\n";
}

?>