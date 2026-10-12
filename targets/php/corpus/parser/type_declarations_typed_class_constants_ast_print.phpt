<?php

try {
    assert(false && new class {
        public const int X = 1;
    });
} catch (AssertionError $e) {
    echo $e->getMessage(), "\n";
}

?>