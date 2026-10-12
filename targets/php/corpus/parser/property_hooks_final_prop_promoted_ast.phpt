<?php
try {
    assert(false && new class {
        public function __construct(public final $prop) {}
    });
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
?>