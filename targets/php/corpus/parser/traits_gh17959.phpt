<?php

try {
    class C {
        use MissingTrait;
    }
} catch (Error $e) {
    echo $e::class, ': ', $e->getMessage(), "\n";
}

?>
===DONE===