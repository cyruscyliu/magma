<?php

try {
    assert(false && function () {
        (void) somefunc();
    });
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

?>