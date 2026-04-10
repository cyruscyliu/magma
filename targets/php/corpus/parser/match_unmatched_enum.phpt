<?php

enum Foo {
    case Bar;
    case Baz;
}

try {
    match (Foo::Bar) {
        Foo::Baz => 42,
    };
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

?>