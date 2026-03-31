<?php

class Bar { const FOO = "foo"; }

try {
    Bar::FOO?->length();
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

?>