<?php

try {
    die(new stdClass);
} catch (TypeError $e) {
    echo $e->getMessage(), PHP_EOL;
}

?>