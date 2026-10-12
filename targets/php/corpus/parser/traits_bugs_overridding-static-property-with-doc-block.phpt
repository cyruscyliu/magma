<?php
trait MyTrait {
    /**
     * trait comment
     */
    static $property;
}

class MyClass {
    use MyTrait;

    /**
     * class comment
     */
    static $property;
}
?>