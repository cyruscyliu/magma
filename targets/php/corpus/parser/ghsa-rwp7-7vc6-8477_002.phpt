<?php

class Foo {
    public int $prop;

    public function foo() {
        return $this;
    }
}

$foo = new Foo();

try {
    $foo->foo()->prop ??= 'foo';
} catch (Error $e) {
    echo $e->getMessage();
}

?>