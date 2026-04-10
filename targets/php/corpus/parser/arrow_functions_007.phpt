<?php

try {
    assert((fn() => false)());
} catch (AssertionError $e) {
    echo 'assert(): ', $e->getMessage(), ' failed', PHP_EOL;
}

try {
    assert((fn&(int... $args): ?bool => $args[0])(false));
} catch (AssertionError $e) {
    echo 'assert(): ', $e->getMessage(), ' failed', PHP_EOL;
}

?>