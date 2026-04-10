<?php

class Foo {
    public static function bar(): never {
        if (false) {
            throw new Exception('bad');
        }
    }
}

try {
    Foo::bar();
} catch (TypeError $e) {
    echo $e->getMessage() . "\n";
}
?>