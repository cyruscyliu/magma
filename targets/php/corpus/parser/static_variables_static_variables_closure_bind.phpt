<?php

$a = null;

function () use (&$a) {
    static $a;
};

?>