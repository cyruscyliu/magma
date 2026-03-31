<?php

enum Foo implements ArrayAccess {
    case Bar;

    public function offsetGet($key): mixed {
        return 42;
    }

    public function offsetExists($key): bool {}
    public function offsetSet($key, $value): void {}
    public function offsetUnset($key): void {}
}

class X {
    const FOO_BAR = Foo::Bar[0];
}

var_dump(X::FOO_BAR);

?>