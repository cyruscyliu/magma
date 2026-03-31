<?php

class A {
    public static function invalid($x = new parent) {
    }
}
class B extends A {
    public static function method($x = new self, $y = new parent) {
        var_dump($x, $y);
    }
}

function invalid($x = new self) {}

B::method();

try {
    invalid();
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

try {
    B::invalid();
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

?>