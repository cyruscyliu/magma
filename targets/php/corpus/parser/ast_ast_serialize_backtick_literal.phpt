<?php

try {
    assert(false && `echo -n ""`);
} catch (AssertionError $e) {
    echo 'assert(): ', $e->getMessage(), ' failed', PHP_EOL;
}

?>