<?php

class C
{
    public string $prop {
        set => $value;
    }
}

$c = new C;
$c->prop = 42;

var_dump($c);
var_dump(get_object_vars($c));
var_export($c);
echo "\n";
var_dump(json_encode($c));
var_dump((array)$c);

?>