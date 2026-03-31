<?php
class Foo { 
    public static function method() { 
        return static::class;
    }
}

class Bar extends Foo {}

$bar = Bar::method(...);

echo $bar();
?>