<?php

class B
{
}

class A
{
    public static $prop = B::class;
}

var_dump(new A::$prop);

?>