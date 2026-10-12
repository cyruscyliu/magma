<?php
$foo = function(){};
$bar = $foo(...);

if ($foo === $bar) {
    echo "OK";
}
?>