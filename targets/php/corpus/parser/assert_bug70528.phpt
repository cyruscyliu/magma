<?php

namespace Foo;
class Bar {}

$bar = "Bar";
try {
    assert(new \stdClass instanceof $bar);
} catch (\AssertionError $e) {
    echo 'assert(): ', $e->getMessage(), ' failed', PHP_EOL;
}
try {
    assert(new \stdClass instanceof Bar);
} catch (\AssertionError $e) {
    echo 'assert(): ', $e->getMessage(), ' failed', PHP_EOL;
}
try {
    assert(new \stdClass instanceof \Foo\Bar);
} catch (\AssertionError $e) {
    echo 'assert(): ', $e->getMessage(), ' failed', PHP_EOL;
}
?>