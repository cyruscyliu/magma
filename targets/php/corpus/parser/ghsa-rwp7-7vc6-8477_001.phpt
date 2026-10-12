<?php

class Foo {
    public function foo() {
        return $this;
    }

    public function __set($name, $value) {
        throw new Exception('Hello');
    }
}

$foo = new Foo();

try {
    $foo->foo()->baz ??= 1;
} catch (Exception $e) {
    echo $e->getMessage();
}

?>