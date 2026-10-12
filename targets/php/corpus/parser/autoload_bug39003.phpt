<?php

class ClassName
{
    public $var = 'bla';
}

function test (OtherClassName $object) { }

spl_autoload_register(function ($class) {
    var_dump("__autoload($class)");
});

$obj = new ClassName;
test($obj);

echo "Done\n";
?>