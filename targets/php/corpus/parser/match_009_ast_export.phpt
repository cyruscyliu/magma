<?php

try {
assert((function () {
    match ('foo') {
        'foo', 'bar' => false,
        'baz' => 'a',
        default => 'b',
    };
})());
} catch (AssertionError $e) {
    echo 'assert(): ', $e->getMessage(), ' failed', PHP_EOL;
}

?>