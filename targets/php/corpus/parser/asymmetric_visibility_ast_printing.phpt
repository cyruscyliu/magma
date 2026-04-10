<?php

try {
    assert(function () {
        class Foo {
            public private(set) string $bar;
            public protected(set) string $baz;
        }
    } && false);
} catch (Error $e) {
    echo $e->getMessage();
}

?>