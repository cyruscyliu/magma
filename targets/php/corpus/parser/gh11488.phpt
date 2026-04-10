<?php
function a(
    string|null $a = null,
    $b,
) {}
function b(
    Foo&Bar $c = null,
    $d,
) {}
function c(
    (Foo&Bar)|null $e = null,
    $f,
) {}
?>